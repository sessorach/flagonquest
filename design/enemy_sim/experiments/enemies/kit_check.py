"""Archetypes, Abilities and armor under the v2 table, priced in enemy Health (2026-11-02).

Per the designer: with the v2 base table as the new ground, check the
pieces a GM builds an enemy from (Role, catalog Abilities, armor) are
in line with each other. Each change goes onto every full-size enemy
(not the minions) in the four current mixes, rebuilt through the
builder, so an Ability's Upgrades come out of the enemy's Health the
way they would on a real stat block. The parties are the eight
normalized ones in the middle of the band (baseline_check's spread) at
Levels 2 and 3, fresh single fights, the same seeds for every change.

Score: party Health lost in the fight, in percentage points of the
party's max (a loss counts 100). It's converted to enemy Health per
Slot with the slope of "every enemy +2 Health" (HealthBonus), so:

- a Role is free, so its reading is what it's worth: Roles should come
  out about even with each other;
- an Ability or armor pays its Upgrades in Health, so its reading is
  worth minus cost: about 0 is fairly priced, + is a bargain, - costs
  more than it gives.

    python3 experiments/enemies/kit_check.py -n 60
"""
import argparse
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import combat_sim as cs  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import build_optimizer as bo  # noqa: E402
import baseline_check as bc  # noqa: E402
import band_builds  # noqa: E402

MID = {2: 105, 3: 145}
ROLES = ("Defender", "Backup", "Striker", "Bruiser", "Skirmisher", "Strategist")
# Only where it means something: a damaging attack for the riders, the
# right Action for weapon/spell/support/range ones. Elemental Spell and
# Weapon are reflavors (0 Upgrades) and Resist/Attunement are read for
# Fire, the one element the parties use (War Magic).
ABILITIES = {
    "Strike (Crippling)": "attack", "Strike (Vulnerable)": "attack", "Strike (Slowing)": "attack",
    "Strike (Frightening)": "attack", "Strike (Taunting)": "attack", "Strike (Necrotic)": "attack",
    "Strike (Harrying)": "attack", "Strike (Battering)": "attack", "Strike (Grappling)": "melee",
    "Strike (Devastating)": "attack", "Strike (Cleaving)": "melee",
    "Poison (Bleeding)": "attack", "Poison (Crippling)": "attack", "Poison (Necrotic)": "attack",
    "Poison (Slowing)": "attack", "Poison (Vulnerable)": "attack",
    "Heavy Weapon": "weapon", "Powerful Weapon": "weapon", "Powerful Spell": "spell",
    "Durable": "any", "Omniguard": "any", "Resilient": "any", "Retribution Aura": "any", "Sturdy": "any",
    "Enhanced Health": "any", "Enhanced Range": "ranged", "Enhanced Speed": "any", "Enhanced Reflexes": "any",
    "Shadow Jaunt": "any", "Improved Support": "support",
    "Action (Parting Shot)": "melee", "Action (Intimidating)": "any", "Action (Taunting)": "any",
    "Resist (Fire)": "any", "Attunement (Fire)": "any",
}
ARMOR = {"Medium Armor": "Medium", "Heavy Armor": "Heavy"}


def fits(row, kind):
    act = eb.ACTIONS[row["Action"]]
    cat = eb.action_category(row["Action"])
    if kind == "any":
        return True
    if kind == "attack":
        return bool(act["dmg_base"]) or bool(row.get("BackupAction"))
    if kind == "melee":
        return act["range"] == 0 and bool(act["dmg_base"])
    if kind == "ranged":
        return act["range"] > 0
    return cat == kind


def edit_for(variant):
    """row -> edited row (or None: leave this enemy as it is). "a|b"
    applies both; "ability:X@1" / "@melee" are the patches in install."""
    if "|" in variant:
        parts = [edit_for(v) for v in variant.split("|")]

        def chain(row):
            for f in parts:
                row = f(row)
                if row is None:
                    return None
            return row
        return chain
    kind, _, what = variant.partition(":")
    what = what.partition("@")[0]

    def edit(row):
        if float(row["Slots"]) < 1:
            return None
        if kind == "base":
            return row
        if kind == "norole":
            return dict(row, Role="")
        if kind == "role":
            return dict(row, Role=what)
        if kind == "hp":
            return dict(row, HealthBonus=str(int(row.get("HealthBonus") or 0) + int(what)))
        if kind == "armor":
            return dict(row, Armor=ARMOR[what])
        if kind == "ability":
            if not fits(row, ABILITIES[what]):
                return None
            have = [a.strip() for a in row["Abilities"].split(";") if a.strip()]
            return dict(row, Abilities="; ".join(have + [what]))
        raise ValueError(variant)
    return edit


_ORIG = {}


def install(variant):
    orig = _ORIG.setdefault("get", se.get_enemy)
    # "role:X@k=v/k=v": that Role's bonuses replaced for this variant.
    live = eb.ROLE_ADDS_V2 if getattr(eb.T, "ENEMY_TABLE", "v1") == "v2" else eb.ROLE_ADDS
    roles = _ORIG.setdefault("roles", {k: dict(v) for k, v in live.items()})
    live.clear()
    live.update({k: dict(v) for k, v in roles.items()})
    for part in variant.split("|"):
        if part.startswith("role:") and "@" in part:
            name, _, adds = part[5:].partition("@")
            live[name] = {k: int(v) for k, v in (x.split("=") for x in adds.split("/"))}
    edit = edit_for(variant)
    skipped = set()

    def get_enemy(name):
        row = se._row_named(name)
        new = edit(row)
        if new is None or new is row:
            return orig(name)
        try:
            return se._build_from_row(new)
        except ValueError:
            # Over the Upgrade budget or the Health floor: the enemy can't
            # take it, so it plays as written (counted).
            skipped.add(name)
            return orig(name)
    se.get_enemy = get_enemy
    return skipped


def parties(level):
    rows = party._rows()
    out = []
    for trio in bc.parties(level, 8):
        names, swaps = [], {}
        for arch in trio:
            row = bo.row_name(arch, level)
            b = party.read_build(band_builds.path(arch, level, MID[level]))
            names.append(row)
            swaps[row] = ({"build": b}, bo.choices_for(rows[row], b))
        out.append((names, swaps))
    return out


def _job(args):
    variant, level, pi, n = args
    skipped = install(variant)
    names, swaps = parties(level)[pi]
    rows = party._rows()
    cs.make_party = lambda tier, good_luck=0: [
        party.make_pc(m, i, good_luck, rows=rows, edits=swaps[m][0], row_changes=swaps[m][1])
        for i, m in enumerate(names, 1)]
    out = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(n):
            r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                             seed=1_000_000 * pi + 10_000 * mi + k)
            out.append((100 * (1 - r["party_hp_pct"]), r["rounds"], r["winner"] == "party", r["pc_downed"]))
    return variant, level, out, sorted(skipped)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=60, help="fights per mix per party")
    ap.add_argument("-L", default="2,3")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("--only", help="these variants (';'-separated) plus the reference ones")
    ap.add_argument("-o", default=os.path.join(_paths.ROOT, "results", "enemy_stats", "kit_check.json"))
    a = ap.parse_args()
    levels = [int(x) for x in a.L.split(",")]
    variants = (["base", "norole", "hp:2", "hp:-2"] + [f"role:{r}" for r in ROLES]
                + [f"ability:{x}" for x in ABILITIES] + [f"armor:{x}" for x in ARMOR])
    if a.only:
        variants = variants[:4] + a.only.split(";")
    jobs = [(v, L, pi, a.n) for v in variants for L in levels for pi in range(8)]
    res, skips = {}, {}
    with mp.Pool(a.j) as pool:
        for v, L, out, sk in pool.imap_unordered(_job, jobs):
            res.setdefault((v, L), []).extend(out)
            skips.setdefault((v, L), set()).update(sk)
    table = {}
    for L in levels:
        mean = lambda v, i=0: st.mean(x[i] for x in res[(v, L)])
        slope = (mean("hp:2") - mean("hp:-2")) / 4  # score per enemy Health per Slot
        base, norole = mean("base"), mean("norole")
        print(f"== Level {L}: base lost {base:.1f} pts, {mean('base', 1):.2f} rounds, "
              f"wins {100 * mean('base', 2):.1f}%; 1 Health per Slot = {slope:.2f} pts")
        for v in variants[4:]:
            ref = norole if v.startswith("role:") else base
            d = mean(v) - ref
            table.setdefault(v, {})[L] = dict(health=d / slope, rounds=mean(v, 1) - mean("norole" if v.startswith("role:") else "base", 1),
                                              wins=100 * mean(v, 2), skipped=sorted(skips[(v, L)]))
            sk = f"  (can't take it: {', '.join(sorted(skips[(v, L)]))})" if skips[(v, L)] else ""
            ref_v = "norole" if v.startswith("role:") else "base"
            table[v][L]["down"] = 100 * (mean(v, 3) - mean(ref_v, 3))
            print(f"   {v:34s} {d / slope:+5.1f} Health  rounds {table[v][L]['rounds']:+.2f}  "
                  f"Down {table[v][L]['down']:+4.1f} pts{sk}")
        table.setdefault("_meta", {})[L] = dict(base=base, slope=slope, rounds=mean("base", 1))
    with open(a.o, "w") as f:
        json.dump(table, f, indent=1)


if __name__ == "__main__":
    main()
