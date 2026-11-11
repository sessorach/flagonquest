"""Every enemy Ability re-priced on the current table (2026-11-08).

Per the designer: re-price the Abilities now the table has settled (the
Defense cap, flat Parry, one budget, the flatter table in pencil), then
add the obvious missing mechanics (Area Attack, Strike (Shoving)) and
price those the same way.

How: the monster manual's own encounters (manual_check's draws, 16 a
Level, no solo boss), every party in the middle of its band, Levels 1-4,
fresh single fights on the same seeds for every variant. A variant gives
one Ability to every standard monster in the fight that can take it (a
damaging attack for an on-hit rider, melee for Cleaving and Shoving, its
kind of Action for weapon, spell, range and support picks; not one it
already has once-only or at a cap), free: its price is set to 0 for the
build, so nothing else on the stat block moves. The yardstick is every
standard monster at 2 more and 2 less Health.

Score: the party's Health lost in the fight, in percentage points of its
max (a lost fight counts 100). An Ability's worth, in Health per monster
that took it, is its score change over the Health slope, divided by the
share of standard monsters that took it. Ability points are 1 Health
each, so worth minus price is how far off the price is: + a bargain, - it
costs more than it gives.

    python3 experiments/enemies/reprice.py run            # resumes from its jsonl
    python3 experiments/enemies/reprice.py read
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import combat_sim as cs  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import bands  # noqa: E402

LEVELS = (1, 2, 3, 4)
K_ENC = 16
# What a monster needs to take it.
KIND = {
    **{f"Strike ({x})": "attack" for x in ("Crippling", "Vulnerable", "Slowing", "Frightening", "Taunting",
                                           "Necrotic", "Harrying", "Battering", "Devastating")},
    **{f"Poison ({x})": "attack" for x in ("Bleeding", "Crippling", "Necrotic", "Slowing", "Vulnerable")},
    "Strike (Cleaving)": "melee", "Strike (Grappling)": "melee", "Strike (Shoving)": "melee",
    "Action (Parting Shot)": "melee", "Area Attack": "attack",
    "Powerful Weapon": "weapon", "Powerful Spell": "spell", "Enhanced Range": "ranged",
    "Improved Support": "support",
    **{f"Elemental Weapon ({x})": "weapon" for x in ("Fire", "Frost", "Shadow", "Brilliant")},
    **{f"Elemental Spell ({x})": "spell" for x in ("Fire", "Frost", "Shadow", "Brilliant")},
}
ANY = ["Accuracy +1", "Damage +1", "Dodge +1", "Vital/Mental/Vigilant +1", "Resist +1", "Enhanced Health",
       "Enhanced Speed", "Enhanced Reflexes", "Durable", "Omniguard", "Resilient", "Sturdy", "Retribution Aura",
       "Shadow Jaunt", "Action (Intimidating)", "Action (Taunting)",
       "Resist (Fire)", "Resist (Frost)", "Resist (Shadow)", "Resist (Brilliant)",
       "Attunement (Fire)", "Attunement (Frost)", "Attunement (Shadow)", "Attunement (Brilliant)"]
PICKS = list(KIND) + ANY
REFS = ["base", "hp:2", "hp:-2"]


def fits(row, pick):
    action = (row.get("PrunedAction") or "").strip() or row["Action"]
    act = eb.ACTIONS[action]
    kind = KIND.get(pick, "any")
    if kind == "any":
        return True
    if kind == "attack":
        return bool(act["dmg_base"])
    if kind == "melee":
        return act["range"] == 0 and bool(act["dmg_base"])
    if kind == "ranged":
        return act["range"] > 0 and bool(act["dmg_base"])
    return eb.action_category(action) == kind


_ORIG = {}


def install(variant):
    orig = _ORIG.setdefault("get", se.get_enemy)
    kind, _, what = variant.partition(":")
    seen = collections.Counter()

    def get_enemy(name):
        e = orig(name)
        if e.get("slots", 1) != 1:
            return e
        seen["standard"] += 1
        if kind == "hp":
            e["max_health"] = e["health"] = max(1, e["max_health"] + int(what))
            seen["took"] += 1
            return e
        if kind != "pick":
            return e
        row = se._row_named(name)
        have = list(e.get("abilities", ()))
        rider = what.startswith("Strike (") or what.startswith("Poison (")
        cap = eb.POISON_CAP if what.startswith("Poison (") else eb.RIDER_CAP
        if not fits(row, what) or (what in have and not rider and what not in eb.REPEATABLE) \
                or (rider and have.count(what) >= cap):
            return e
        price = eb.ABILITY_PRICES[what]
        eb.ABILITY_PRICES[what] = 0
        try:
            new = se._build_from_row(dict(row, PrunedPicks=f"{row['PrunedPicks']}; {what}"))
        except ValueError:
            return e  # past a cap: plays as written
        finally:
            eb.ABILITY_PRICES[what] = price
        seen["took"] += 1
        return new
    se.get_enemy = get_enemy
    return seen


def encounters(level):
    return [e for e in mc.encounters(level, K_ENC, 1)
            if not any(se.get_enemy(f"{n}@{level}").get("slots", 1) == 4 for n in e)]


def _job(args):
    variant, level, gi, n = args
    T.ENEMY_LEVEL_UP = 0
    install("base")
    encs = encounters(level)
    seen = install(variant)
    groups = [g for g in bands.groups(level, bands.MID[level]) if g[0] != "stand-ins"]
    gname, names, swaps = groups[gi]
    rows = party._rows()
    cs.make_party = lambda tier, good_luck=0: [
        party.make_pc(m, i, good_luck, rows=rows, edits=swaps.get(m, (None, None))[0],
                      row_changes=swaps.get(m, (None, None))[1])
        for i, m in enumerate(names, 1)]
    out = []
    for ei, enc in enumerate(encs):
        for k in range(n):
            r = cs.run_fight(1, min(level, 3), movement=True,
                             enemies=se.build_encounter([f"{x}@{level}" for x in enc]),
                             seed=1_000_000 * gi + 10_000 * ei + k)
            out.append((100 * (1 - r["party_hp_pct"]), r["rounds"], r["winner"] == "party", r["pc_downed"]))
    return dict(v=variant, L=level, gi=gi, n=n, out=out, took=seen["took"], standard=seen["standard"])


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {(r["v"], r["L"], r["gi"]) for r in map(json.loads, open(a.o)) if r["n"] == a.n}
    jobs = []
    for L in LEVELS:
        ng = len([g for g in bands.groups(L, bands.MID[L]) if g[0] != "stand-ins"])
        for v in REFS + [f"pick:{p}" for p in (a.only.split(";") if a.only else PICKS)]:
            for gi in range(ng):
                if (v, L, gi) not in done:
                    jobs.append((v, L, gi, a.n))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j, maxtasksperchild=20) as pool:
        for r in pool.imap_unordered(_job, jobs):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")


def read(a):
    res = collections.defaultdict(list)
    took = collections.Counter()
    for r in map(json.loads, open(a.o)):
        res[(r["v"], r["L"])].extend(map(tuple, r["out"]))
        took[(r["v"], r["L"], "took")] += r["took"]
        took[(r["v"], r["L"], "standard")] += r["standard"]
    mean = lambda v, L, i=0: st.mean(x[i] for x in res[(v, L)])
    lines = ["| Ability | Price | Worth by Level (1 / 2 / 3 / 4), Health a monster | Worth (Levels 1-4) | "
             "Worth - price | Rounds | Down (points) | Share that took it |", "|---|---|---|---|---|---|---|---|"]
    meta = []
    for L in LEVELS:
        slope = (mean("hp:2", L) - mean("hp:-2", L)) / 4
        meta.append(f"Level {L}: base {mean('base', L):.1f} points of party Health lost, "
                    f"{mean('base', L, 1):.2f} rounds; 1 Health a standard monster = {slope:.2f} points")
    rows = []
    picks = sorted({v[5:] for v, L in res if v.startswith("pick:")})
    for p in picks:
        v = f"pick:{p}"
        worths, rnds, downs, shares = [], [], [], []
        for L in LEVELS:
            if (v, L) not in res:
                worths.append(None)
                continue
            slope = (mean("hp:2", L) - mean("hp:-2", L)) / 4
            share = took[(v, L, "took")] / max(1, took[(v, L, "standard")])
            shares.append(share)
            if share == 0:
                worths.append(None)
                continue
            worths.append((mean(v, L) - mean("base", L)) / slope / share)
            rnds.append((mean(v, L, 1) - mean("base", L, 1)) / share)
            downs.append(100 * (mean(v, L, 3) - mean("base", L, 3)) / share)
        got = [w for w in worths if w is not None]
        if not got:
            continue
        w = st.mean(got)
        price = eb.ABILITY_PRICES[p]
        rows.append((w - price, f"| {p} | {price:g} | " + " / ".join("-" if x is None else f"{x:+.1f}" for x in worths)
                     + f" | {w:+.1f} | {w - price:+.1f} | {st.mean(rnds):+.2f} | {st.mean(downs):+.1f} | "
                       f"{100 * st.mean(shares):.0f}% |"))
    lines += [r for _, r in sorted(rows, reverse=True)]
    text = "\n".join(meta + [""] + lines)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-o", default=os.path.join(_paths.ROOT, "results/enemy_stats/reprice.jsonl"))
    ap.add_argument("--txt", default=os.path.join(_paths.ROOT, "results/enemy_stats/reprice.txt"))
    ap.add_argument("-n", type=int, default=12)
    ap.add_argument("--only", help="these picks only (';'-separated), plus the references")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    {"run": run, "read": read}[a.cmd](a)


if __name__ == "__main__":
    main()
