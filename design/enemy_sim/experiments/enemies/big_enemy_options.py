"""Elites and solo bosses with bigger budgets: every option (2026-11-06).

Follows elite_boss_check.py. Per the designer: test the swingier and
the safer settings both ways, thoroughly. A big enemy gets its Ability
budget scaled (tunables.V3_SLOT_BUDGET) and spends all of it on
mechanics, down a priority list per design (`big`, after the Level's
extra points go as they do today), so a setting is read as "this budget,
this Health multiple, fully spent". Five boss designs and five elite
designs: the manual's Brute Warlord, Gravel Ogre and Coven Matriarch
plus test-only ones (a caster, a defender, a kiting archer, ...) so the
answer doesn't hang on one monster. Every party at the low, middle and
high points of its band; bosses alone at Levels 3-5; elites in pairs and
beside two standard monsters at Levels 1-5. Fresh fights, common seeds
across settings (manual_check's), results to a jsonl a rerun resumes.

    python3 experiments/enemies/big_enemy_options.py run -o results/enemy_stats/big_enemy_options.jsonl
    python3 experiments/enemies/big_enemy_options.py read -o results/enemy_stats/big_enemy_options.jsonl
    python3 experiments/enemies/big_enemy_options.py show        # the built enemies, for a sanity look
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import random
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import game_data  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

FILLER = ["Parry and Dodge +1", "Vital/Mental/Vigilant +1"] * 6

# Test-only designs (never in the manual). Columns as monster_manual.csv.
TEST_ROWS = {
    "Brute Warlord (Assassin)": None,  # the Warlord, hunting the softest PC
    "Lich Sovereign": dict(Slots="4", Role="Striker", Action="Shadow Bolt", BackupAction="", MainEffect="",
                           Armor="Unarmored", StrongDefense="Mental", WeakDefense="", BattleTactic="Hit Whatever",
                           PrunedPicks="Powerful Spell; Accuracy +1; Strike (Necrotic); Strike (Necrotic); "
                                       "Strike (Frightening); Strike (Frightening)",
                           PrunedExtra="Strike (Necrotic); Strike (Necrotic)"),
    "Iron Colossus": dict(Slots="4", Role="Defender", Action="Heavy Weapon and Shield", BackupAction="", MainEffect="",
                          Armor="Heavy", StrongDefense="Vital", WeakDefense="", BattleTactic="Hold the Line",
                          PrunedPicks="Strike (Taunting); Strike (Taunting); Omniguard; Sturdy; Resilient; "
                                      "Strike (Battering)",
                          PrunedExtra="Strike (Crippling); Strike (Crippling)"),
    "Dread Huntress": dict(Slots="4", Role="Skirmisher", Action="Bow", BackupAction="", MainEffect="",
                           Armor="Light", StrongDefense="Dodge", WeakDefense="", BattleTactic="Kiting",
                           PrunedPicks="Enhanced Range; Accuracy +1; Strike (Slowing); Strike (Slowing); "
                                       "Strike (Vulnerable); Strike (Vulnerable)",
                           PrunedExtra="Strike (Vulnerable); Strike (Vulnerable)"),
    "Elite Sharpshooter": dict(Slots="2", Role="Striker", Action="Heavy Bow", BackupAction="", MainEffect="",
                               Armor="Light", StrongDefense="Dodge", WeakDefense="", BattleTactic="Assassin",
                               PrunedPicks="Accuracy +1; Enhanced Range; Strike (Vulnerable); Strike (Vulnerable)",
                               PrunedExtra="Strike (Crippling); Strike (Crippling)"),
    "Black Knight": dict(Slots="2", Role="Defender", Action="Heavy Weapon and Shield", BackupAction="", MainEffect="",
                         Armor="Heavy", StrongDefense="Vital", WeakDefense="", BattleTactic="Hold the Line",
                         PrunedPicks="Strike (Taunting); Strike (Taunting); Omniguard; Sturdy",
                         PrunedExtra="Parry and Dodge +1"),
    "Storm Magus": dict(Slots="2", Role="Strategist", Action="Ranged Spell", BackupAction="", MainEffect="",
                        Armor="Unarmored", StrongDefense="Mental", WeakDefense="", BattleTactic="Hit Whatever",
                        PrunedPicks="Powerful Spell; Accuracy +1; Strike (Frightening); Strike (Frightening)",
                        PrunedExtra="Strike (Vulnerable); Strike (Vulnerable)"),
}

# What each spends a bigger budget on, in order; a pick that doesn't fit
# what's left, or would pass a cap, is skipped; FILLER soaks up the rest.
BIG = {
    "Brute Warlord": ["Strike (Crippling)", "Strike (Crippling)", "Strike (Frightening)", "Strike (Frightening)",
                      "Accuracy +1", "Durable", "Damage +1", "Powerful Weapon", "Strike (Frightening)",
                      "Strike (Frightening)", "Enhanced Speed", "Omniguard", "Accuracy +1"],
    "Lich Sovereign": ["Strike (Vulnerable)", "Strike (Vulnerable)", "Accuracy +1", "Shadow Jaunt", "Enhanced Range",
                       "Strike (Frightening)", "Strike (Frightening)", "Enhanced Reflexes", "Durable",
                       "Strike (Vulnerable)", "Strike (Vulnerable)", "Accuracy +1"],
    "Iron Colossus": ["Accuracy +1", "Strike (Taunting)", "Strike (Taunting)", "Action (Taunting)", "Durable",
                      "Damage +1", "Strike (Crippling)", "Strike (Crippling)", "Resist +1", "Accuracy +1"],
    "Dread Huntress": ["Strike (Slowing)", "Strike (Slowing)", "Accuracy +1", "Enhanced Reflexes", "Damage +1",
                       "Strike (Crippling)", "Strike (Crippling)", "Enhanced Speed", "Shadow Jaunt", "Accuracy +1"],
    "Gravel Ogre": ["Accuracy +1", "Damage +1", "Durable", "Strike (Crippling)", "Strike (Crippling)",
                    "Enhanced Speed", "Accuracy +1"],
    "Coven Matriarch": ["Accuracy +1", "Strike (Vulnerable)", "Strike (Vulnerable)", "Enhanced Reflexes", "Durable",
                        "Strike (Vulnerable)", "Strike (Vulnerable)", "Accuracy +1"],
    "Elite Sharpshooter": ["Accuracy +1", "Damage +1", "Strike (Crippling)", "Strike (Crippling)",
                           "Strike (Vulnerable)", "Strike (Vulnerable)", "Enhanced Reflexes", "Accuracy +1"],
    "Black Knight": ["Accuracy +1", "Damage +1", "Strike (Crippling)", "Strike (Crippling)", "Action (Taunting)",
                     "Durable", "Strike (Battering)", "Accuracy +1"],
    "Storm Magus": ["Strike (Frightening)", "Strike (Frightening)", "Accuracy +1", "Strike (Vulnerable)",
                    "Strike (Vulnerable)", "Enhanced Range", "Attunement (Fire)", "Enhanced Reflexes", "Accuracy +1"],
}
BIG["Brute Warlord (Assassin)"] = BIG["Brute Warlord"]

BOSSES = ["Brute Warlord", "Brute Warlord (Assassin)", "Lich Sovereign", "Iron Colossus", "Dread Huntress"]
ELITES = ["Gravel Ogre", "Coven Matriarch", "Elite Sharpshooter", "Black Knight", "Storm Magus"]

# (budget scale, Health multiple). The first of each is today's.
BOSS_SET = [(1, 6), (2, 3), (2, 3.25), (2, 3.5), (2, 3.75), (2, 4), (1.5, 4), (1.5, 4.5), (1.5, 5),
            (3, 2.5), (3, 3), (2, 4.25), (2, 4.5)]
ELITE_SET = [(1, 3), (2, 2), (2, 2.25), (2, 2.5), (2, 2.75), (1.5, 2.5), (1.5, 2.75), (2, 3)]
MIX_SET = [(1, 3), (2, 2), (2, 2.5), (2, 2.75), (2, 3)]

# --rule offense: the points a size adds can't buy Defenses, Resist or
# Health (what's left is Health, at the scaled rate); see
# big_enemy_variants.py --prices for why.
RULE = [None]
DEFENSIVE = {"Parry and Dodge +1", "Vital/Mental/Vigilant +1", "Resist +1", "Durable", "Omniguard", "Resilient",
             "Enhanced Health", "Sturdy"}

_ROWS = {}


def rows():
    if not _ROWS:
        manual = {r["Name"]: dict(r) for r in game_data.csv_rows(se._MANUAL_PATH)}
        for n in BOSSES + ELITES:
            if n in manual:
                _ROWS[n] = manual[n]
        _ROWS["Brute Warlord (Assassin)"] = dict(manual["Brute Warlord"], BattleTactic="Assassin")
        for n, r in TEST_ROWS.items():
            if r:
                _ROWS[n] = dict(r, Name=n, Concept="test only")
    return _ROWS


def picks_for(name, level):
    """The design's whole pick list at `level` under the current
    V3_SLOT_BUDGET: its PrunedPicks, the Level's extra points spent as
    _pruned_picks spends them, then its `big` list and FILLER with the
    budget the size adds."""
    r = rows()[name]
    slots = float(r["Slots"])
    picks = [p.strip() for p in r["PrunedPicks"].split(";") if p.strip()]
    extra = T.V3_PRUNED_EXTRA.get(level, 0)
    left = extra
    order = [p.strip() for p in r["PrunedExtra"].split(";") if p.strip()]
    order = ["Accuracy +1", "Damage +1"] + [p for p in order if p not in ("Accuracy +1", "Damage +1")]
    for p in order:
        price = eb.ABILITY_HEALTH_V3P[p]
        if price <= left:
            picks.append(p)
            left -= price
    # Only the points the size adds go down `big`; what the Level's extra
    # leaves stays Health, as it does today (so budget x1 is today's build).
    k = T.V3_SLOT_BUDGET.get(slots, 1)
    left = (T.V3_PRUNED_ALLOWANCE + extra) * (k - 1)
    t = eb.ENEMY_TABLE_V3_PRUNED[level]
    role_acc = eb.ROLE_ADDS_V3_ADDITIVE.get(r["Role"], {}).get("acc", 0)
    for p in BIG[name] + ([] if RULE[0] == "offense" else FILLER):
        price = eb.ABILITY_HEALTH_V3P[p]
        if price > left + 1e-9:
            continue
        if RULE[0] == "offense" and (p in DEFENSIVE or p.startswith("Resist (")):
            continue
        n = picks.count(p)
        rider = p.startswith("Strike (") or p.startswith("Poison (")
        if rider and n >= (eb.POISON_CAP_V3 if p.startswith("Poison (") else eb.RIDER_CAP_V3):
            continue
        if n and not rider and p not in eb.REPEATABLE_V3:
            continue
        if p == "Accuracy +1" and t["accuracy"] + role_acc + n + 1 > eb.SKILL_CAP:
            continue
        picks.append(p)
        left -= price
    return picks


def install():
    """Route these designs through picks_for (in this process, once)."""
    if getattr(se, "_big_enemy_options", False):
        return
    se._big_enemy_options = True
    orig_row, orig_picks = se._manual_row, se._pruned_picks

    def manual_row(name):
        base, _, level = name.partition("@")
        r = rows().get(base)
        if r is None:
            return orig_row(name)
        return dict(r, Name=name, Level=level, AttackTier="primary", Abilities="", HealthBonus="",
                    FightingStyle="None", PrunedAction=r["Action"], Roster="FALSE",
                    _final=picks_for(base, int(level)))

    def pruned_picks(row, abilities):
        if "_final" in row:
            return list(row["_final"]), row["PrunedAction"]
        return orig_picks(row, abilities)
    se._manual_row, se._pruned_picks = manual_row, pruned_picks


def setting(slots, scale, hp):
    T.V3_SLOT_BUDGET = {slots: scale} if scale != 1 else {}
    if slots == 4:
        T.V3_SOLO_HEALTH = hp
    else:
        T.V3_ELITE_HEALTH = hp


def companions(level, k=6, seed=7):
    """k fixed pairs of standard monsters (two Slots between them) to
    stand beside an elite, drawn from the manual; attackers only, since
    the Matriarch already fills the one non-attacking place."""
    rng = random.Random(seed * 100 + level)
    pool = []
    for n in se.manual_names():
        e = se.get_enemy(f"{n}@3")
        if e.get("slots", 1) == 1 and e["kind"] == "attack":
            pool.append(n)
    out = []
    while len(out) < k:
        pair = tuple(sorted(rng.sample(pool, 2)))
        if pair not in out:
            out.append(pair)
    return out


def cases():
    out = []
    for b in BOSSES:
        for L in (3, 4, 5):
            for s, h in BOSS_SET:
                out.append(dict(kind="boss", design=b, level=L, scale=s, hp=h, slots=4, enc=[b]))
    for e in ELITES:
        for L in (1, 2, 3, 4, 5):
            for s, h in ELITE_SET:
                out.append(dict(kind="pair", design=e, level=L, scale=s, hp=h, slots=2, enc=[e, e]))
            for comp in companions(L):
                for s, h in MIX_SET:
                    out.append(dict(kind="mix", design=e, level=L, scale=s, hp=h, slots=2, enc=[e, *comp],
                                    comp="+".join(comp)))
    return out


def points(level, kind):
    if level == 1:
        return [None]
    return [ps.MID[level]] if kind == "mix" else list(tc.POINTS[level])


def _job(args):
    c, budget, gi, n, seed = args
    install()
    RULE[0] = c.get("rule")
    T.ENEMY_LEVEL_UP = 0
    setting(c["slots"], c["scale"], c["hp"])
    L = c["level"]
    gname, pnames, swaps = tc.groups(L, budget)[gi]
    lvl = min(L, 3)
    se.ENCOUNTERS.setdefault(lvl, {})["_test"] = [f"{x}@{L}" for x in c["enc"]]
    prow = party._rows()
    out = collections.Counter()
    for k in range(n):
        rec, _ = ds.play_day(pnames, swaps, lvl, ("_test",), seed + 1000 * k, prow)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["down"] += f["downs"] > 0
        out["down2"] += f["downs"] > 1
        out["wounded"] += bool(f["wounded"])
        out["rounds"] += f["rounds"]
    big = se.get_enemy(f"{c['design']}@{L}")
    return dict(c, budget=budget, party=gname, n=n, health=big["max_health"],
                **{k: out[k] / n for k in ("won", "down", "down2", "wounded", "rounds")})


def key(r):
    return (r.get("rule"), r["kind"], r["design"], r["level"], r["scale"], r["hp"], r.get("comp", ""), r["budget"], r["party"])


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {key(r) for r in map(json.loads, open(a.o)) if r}
    jobs = []
    for c in cases():
        c["rule"] = a.rule
        if a.only and c["kind"] not in a.only.split(","):
            continue
        for b in points(c["level"], c["kind"]):
            for gi, (gname, _, _) in enumerate(tc.groups(c["level"], b)):
                if key(dict(c, budget=b, party=gname)) not in done:
                    jobs.append((c, b, gi, a.n, a.seed))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j, maxtasksperchild=50) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=2)):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
            if i % 250 == 0:
                print(i, flush=True)


def show(a):
    install()
    RULE[0] = a.rule
    for designs, slots, sets in ((BOSSES, 4, BOSS_SET), (ELITES, 2, ELITE_SET)):
        for d in designs:
            for L in ((3, 4, 5) if slots == 4 else (1, 3, 5)):
                for s, h in sets[:1] + [x for x in sets if x in ((2, 3.5), (2, 3), (2, 2.5), (2, 2))]:
                    setting(slots, s, h)
                    e = se.get_enemy(f"{d}@{L}")
                    extra = picks_for(d, L)[len([p for p in rows()[d]["PrunedPicks"].split(";") if p.strip()]):]
                    print(f"{d:26s} L{L} x{s} H{h}: Health {e['max_health']:3d} Acc {e['accuracy']:2d} "
                          f"Dmg {e['attack_damage']:2d} Parry {e['parry']:3d} Dodge {e['dodge']:2d} "
                          f"Res {e['physres']} | + {'; '.join(extra)}")


def _fmt(rs):
    lost = [1 - r["won"] for r in rs]
    by_p = collections.defaultdict(list)
    for r in rs:
        by_p[r["party"]].append(1 - r["won"])
    worst = max(st.mean(v) for v in by_p.values())
    return (f"{100 * st.mean(lost):3.0f}% ({100 * worst:3.0f}%) | {100 * st.mean(r['down'] for r in rs):3.0f}% | "
            f"{100 * st.mean(r['down2'] for r in rs):3.0f}% | {100 * st.mean(r['wounded'] for r in rs):3.0f}% | "
            f"{st.mean(r['rounds'] for r in rs):4.1f}")


def read(a):
    recs = [json.loads(l) for l in open(a.o) if l.strip()]
    out = []
    head = "| Lost (worst party) | Down | 2+ Down | Wounded | Rounds |"
    sub = "|---|---|---|---|---|"

    def table(title, kind, designs, sets, levels, bands=False):
        out.append(f"\n### {title}\n")
        group = collections.defaultdict(list)
        for r in recs:
            if r["kind"] == kind and r["design"] in designs:
                group[(r["scale"], r["hp"], r["level"])].append(r)
        out.append("| Setting | " + " | ".join(f"L{L}" for L in levels) + " | All: " + head[2:])
        out.append("|---|" + "---|" * len(levels) + sub[1:])
        for s, h in sets:
            cells, every = [], []
            for L in levels:
                rs = group.get((s, h, L), [])
                every += rs
                cells.append(f"{100 * (1 - st.mean(r['won'] for r in rs)):.0f}%" if rs else "-")
            if every:
                out.append(f"| budget x{s}, Health x{h} | " + " | ".join(cells) + " | " + _fmt(every) + " |")
        if bands:
            out.append("\nBy band point (lost, all designs and Levels):\n")
            out.append("| Setting | low | middle | high |")
            out.append("|---|---|---|---|")
            for s, h in sets:
                cells = []
                for pos in range(3):
                    rs = [r for (ss, hh, L), v in group.items() if (ss, hh) == (s, h) for r in v
                          if L > 1 and r["budget"] == tc.POINTS[L][pos]]
                    cells.append(f"{100 * (1 - st.mean(r['won'] for r in rs)):.0f}%" if rs else "-")
                out.append(f"| budget x{s}, Health x{h} | " + " | ".join(cells) + " |")

    table("Solo bosses, all five designs (lost by Level)", "boss", BOSSES, BOSS_SET, (3, 4, 5), bands=True)
    for b in BOSSES:
        table(f"{b} alone", "boss", [b], BOSS_SET, (3, 4, 5))
    table("Elite pairs, all five designs", "pair", ELITES, ELITE_SET, (1, 2, 3, 4, 5), bands=True)
    for e in ELITES:
        table(f"Two {e}s", "pair", [e], ELITE_SET, (1, 2, 3, 4, 5))
    table("An elite beside two standard monsters, all designs (middle of the band)", "mix", ELITES, MIX_SET,
          (1, 2, 3, 4, 5))
    for e in ELITES:
        table(f"{e} beside two standard monsters", "mix", [e], MIX_SET, (1, 2, 3, 4, 5))
    out.append("\n### Health of the big one at each setting\n")
    seen = {}
    for r in recs:
        seen[(r["design"], r["level"], r["scale"], r["hp"])] = r["health"]
    for d in BOSSES + ELITES:
        sets = BOSS_SET if d in BOSSES else ELITE_SET
        levels = (3, 4, 5) if d in BOSSES else (1, 2, 3, 4, 5)
        out.append(f"- {d}: " + "; ".join(
            f"x{s}/H{h} " + "/".join(str(seen.get((d, L, s, h), "-")) for L in levels) for s, h in sets))
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read", "show"))
    ap.add_argument("-o", default="results/enemy_stats/big_enemy_options.jsonl")
    ap.add_argument("--txt")
    ap.add_argument("-n", type=int, default=100, help="fights per party per case")
    ap.add_argument("--seed", type=int, default=41)
    ap.add_argument("--only", help="boss,pair,mix")
    ap.add_argument("--rule", help="offense: the size's extra points buy no Defenses, Resist or Health")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    {"run": run, "read": read, "show": show}[a.cmd](a)


if __name__ == "__main__":
    main()
