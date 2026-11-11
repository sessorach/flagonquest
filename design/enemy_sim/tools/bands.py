"""The parties every band check plays, and the builds behind them.

Level N enemies are for PCs within 25 XP of that Level's schedule
(designer, 2026-11-02), so each Level has a bottom, middle and top of its
band, in combat XP (combat_xp.combat_for of the composite XP the designer
quotes). Levels 2-3: eight normalized parties spread over party_mixes'
own-Level ranking (`parties`), built at each point (`path`, written by
this file's CLI); Levels 4-5 grow the Level 3 exports (GROWN_FROM);
Level 1 plays the six sample parties. `groups(level, budget)` is what a
band tool plays; `stats` reads its days. Gathered here on 2026-11-11
from table_check, baseline_check, band_builds and progression_sweep.

    python3 tools/bands.py          # writes the normalized band builds
    python3 tools/bands.py --check  # the stored builds still come out the same
"""
import argparse
import copy
import json
import os
import statistics as st
import sys

import _paths  # noqa: E402,F401
import party  # noqa: E402
import combat_xp  # noqa: E402
import party_power as pp  # noqa: E402
import build_optimizer as bo  # noqa: E402
import calibrate  # noqa: E402

PICKS = 12  # parties, evenly spread over party_mixes' own-Level ranking

# Composite XP bands per enemy Level (designer: within 25 XP of the
# schedule), and the combat XP of each point (combat_xp.combat_for).
BANDS = {2: (100, 125, 150), 3: (150, 175, 200), 4: (200, 225, 250), 5: (250, 275, 300)}
EDGES = {2: (85, 125), 3: (125, 165), 4: (165, 185, 205), 5: (205, 225, 245)}
assert all(tuple(combat_xp.combat_for(t) for t in BANDS[L])[0] == EDGES[L][0] for L in EDGES)
# Levels 4-5 have no exports: each Level 3 character grown to the budget
# by the same rule (more ranks in the attack Skill and Stat, Essence and
# the Defense Skills, rank cap 5). It keeps its Level 3 Techniques, so
# it's a floor on a real Level 4-5 character, not a stand-in for one.
GROWN_FROM = {4: 3, 5: 3}


def build_at(arch, level, budget):
    level = GROWN_FROM.get(level, level)
    name = bo.row_name(arch, level)
    um = {x.strip() for x in (party._rows()[name].get("Unmodeled") or "").split(",") if x.strip()}
    b = party.read_build(party._rows()[name]["Build"])
    saved = combat_xp.COMBAT_BUDGET[level]
    combat_xp.COMBAT_BUDGET[level] = budget
    try:
        return combat_xp.normalize(b, level, party.make_pc(name)["attack_skill"], um)[0]
    finally:
        combat_xp.COMBAT_BUDGET[level] = saved


def path(arch, level, budget):
    return os.path.join(_paths.ROOT, "builds", "normalized", f"{arch.lower()}_l{level}_c{budget}.json")


# Combat XP at the bottom / middle / top of each band (combat_budget).
POINTS = {1: (None,), 2: (85, 105, 125), 3: (125, 145, 165), 4: (165, 185, 205), 5: (205, 225, 245)}
L1_PARTIES = ("A", "B", "D", "T", "S", "U")
COMPOSITE = {combat_xp.combat_for(t): t for t in range(75, 301, 25)}


def stand_in_at(level, budget):
    """party_power.stand_in's rule at any combat budget, rank cap 5."""
    b = copy.deepcopy(party.read_build(party._rows()[pp.STAND_IN[level]]["Build"]))
    left = budget - combat_xp.split(b)[0]
    order = [("statPoints", s) for s in pp._STAT_ORDER] + [("skillPoints", s) for s in pp._SKILL_ORDER]
    progress = True
    while left > 2 and progress:
        progress = False
        for kind, k in order:
            v = int(b[kind][k])
            cost = 2 * (v + 1) if kind == "statPoints" else v + 1
            if v < 5 and cost <= left:
                b[kind][k] = v + 1
                left -= cost
                progress = True
    return b


STANDINS_ONLY = [False]


def groups(level, budget):
    rows = party._rows()
    if STANDINS_ONLY[0] and level > 1:
        si = pp.STAND_IN[level]
        return [("stand-ins", [si] * 4, {si: ({"build": stand_in_at(level, budget)}, None)})]
    if level == 1:
        return [(k, calibrate.PARTIES[1][k], {}) for k in L1_PARTIES] + \
               [("stand-ins", [pp.STAND_IN[1]] * 4, {})]
    out = []
    base = GROWN_FROM.get(level, level)
    for trio in parties(base, 8):
        names, swaps = [], {}
        for arch in trio:
            row = bo.row_name(arch, base)
            b = party.read_build(path(arch, level, budget))
            names.append(row)
            swaps[row] = ({"build": b}, bo.choices_for(rows[row], b))
        out.append(("+".join(trio), names, swaps))
    return out

# The middle of each band (combat XP), what most tools play.
MID = {L: p[len(p) // 2] for L, p in POINTS.items()}


def parties(level, k=PICKS):
    d = json.load(open(os.path.join(_paths.ROOT, "hall_of_fame", "runs_levelup", f"mixes_l{level}.json")))
    ranked = sorted(d["mixes"], key=lambda m: m["own"])
    idx = sorted({round(i * (len(ranked) - 1) / (k - 1)) for i in range(k)})
    return [tuple(ranked[i]["party"]) for i in idx]


def stats(days):
    out = {}
    for f in (1, 2):
        fights = [d[f - 1] for d in days if len(d) >= f]
        if not fights:
            continue
        won = [x for x in fights if x["won"]]
        # A hit enemy's first hit, as calibrate.py's "after first hit".
        ag = [sum(x["again_first"][i] for x in fights) for i in (0, 1)]
        out[f] = dict(n=len(fights), lose=100 * (1 - len(won) / len(fights)),
                      rounds=st.mean(x["rounds"] for x in won) if won else 0,
                      long=100 * sum(x["rounds"] > 5 for x in won) / max(1, len(won)),
                      down=100 * sum(x["downs"] > 0 for x in fights) / len(fights),
                      downs=st.mean(x["downs"] for x in fights),
                      wounded=100 * sum(x["wounded"] for x in fights) / len(fights),
                      again=100 * ag[0] / max(1, ag[1]))
    out["day"] = 100 * sum(len(d) == 2 and d[1]["won"] for d in days) / len(days)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        bad = 0
        for level, budget in combat_xp.COMBAT_BUDGET.items():
            for arch in bo.ARCHES:
                new = build_at(arch, level, budget)
                old = party.read_build(path(arch, level, budget))
                same = all(new[k] == old.get(k) for k in ("statPoints", "skillPoints", "techniques"))
                bad += not same
                print(f"{arch} L{level}: {'same' if same else 'DIFFERENT'}")
        sys.exit(bad)
    for level, budgets in EDGES.items():
        for budget in budgets:
            for arch in bo.ARCHES:
                b = build_at(arch, level, budget)
                c = combat_xp.split(b)[0]
                with open(path(arch, level, budget), "w") as f:
                    json.dump(b, f, indent=1)
                print(f"{arch} L{level} c{budget}: {c} combat XP")


if __name__ == "__main__":
    main()
