"""An enemy base table against parties across each Level's XP band (2026-11-02).

Per the designer: Level N enemies are for PCs within 25 XP of that Level's
schedule, so a party at the bottom of the band should feel some friction
and one at the top should be comfortable. Each Level plays its four
mixes under the day standard (day_sim, two fights) against:

- Level 1: the six sample parties (75 XP, the bottom of the band) and
  four Baseline Tier 1 rows;
- Levels 2-3: eight normalized parties (baseline_check's spread) at the
  bottom, middle and top of the band in combat XP (band_builds.py);
- Levels 4-5: the same eight parties grown from their Level 3 exports
  (band_builds.GROWN_FROM: more ranks, the Level 3 Techniques), against
  the Level 3 mixes built Levels higher (tunables.ENEMY_LEVEL_UP);
  `--standins` plays four plain stand-ins at every Level instead.

Since 2026-11-09 a day's fights are the monster manual's own encounters
at the Level (DAY_SOURCE 'manual', `--days roster` for the old four
mixes; Levels 4-5 then build the Level 3 mixes Levels higher).

Every point is a composite (total) XP, the designer's unit, played at
its combat share (combat_xp.combat_for).

    python3 experiments/enemies/table_check.py -t v1,v2 -n 100
"""
import argparse
import copy
import json
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import tunables as T  # noqa: E402
import combat_xp  # noqa: E402
import party_power as pp  # noqa: E402
import build_optimizer as bo  # noqa: E402
import baseline_check as bc  # noqa: E402
import band_builds  # noqa: E402
import calibrate  # noqa: E402

# Combat XP at the bottom / middle / top of each band (band_builds.combat_budget).
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
    base = band_builds.GROWN_FROM.get(level, level)
    for trio in bc.parties(base, 8):
        names, swaps = [], {}
        for arch in trio:
            row = bo.row_name(arch, base)
            b = party.read_build(band_builds.path(arch, level, budget))
            names.append(row)
            swaps[row] = ({"build": b}, bo.choices_for(rows[row], b))
        out.append(("+".join(trio), names, swaps))
    return out


# Where a day's fights come from (designer, 2026-11-09: one set of monsters
# decides difficulty). 'manual': MANUAL_MIXES of the monster manual's own
# encounters at the Level (manual_check's draws, 4 Slots, no solo boss),
# built at that Level; the same number of days in all (n per mix times 4,
# spread over them). 'roster': the old sample roster's four mixes
# (Frontline, Shield Wall, Warband, Horde), Levels 4-5 built up from 3.
DAY_SOURCE = ["manual"]
MANUAL_MIXES = 8


def _manual_mixes(level, n):
    """Registers the manual's encounters as this Level's day mixes and
    returns days per mix that keep the total the same as four mixes."""
    import sample_enemies as se
    import manual_check as mc
    T.ENEMY_LEVEL_UP = 0
    encs = [e for e in mc.encounters(level, MANUAL_MIXES, 1)
            if not any(se.get_enemy(f"{x}@{level}").get("slots", 1) == 4 for x in e)][:MANUAL_MIXES]
    lvl = min(level, 3)
    keys = []
    for i, e in enumerate(encs):
        key = f"Manual {i + 1}"
        se.ENCOUNTERS.setdefault(lvl, {})[key] = [f"{x}@{level}" for x in e]
        keys.append(key)
    se.CURRENT_MIXES = tuple(keys)
    return max(1, round(n * 4 / len(keys)))


def _job(args):
    table, level, budget, gi, n, seed, standins, nudge = args
    STANDINS_ONLY[0] = standins
    import stat_sweep
    stat_sweep.install(stat_sweep.parse(nudge or ""))
    T.ENEMY_TABLE = table
    T.ENEMY_LEVEL_UP = max(0, level - 3)
    ds.set_mult(1.0)
    gname, names, swaps = groups(level, budget)[gi]
    if DAY_SOURCE[0] == "manual":
        n = _manual_mixes(level, n)
    recs = ds.run(names, swaps, min(level, 3), n, seed=seed)
    return table, level, budget, gname, [r.get("per_fight", []) for r in recs]


def summarize(by_group):
    every = [d for g, days in by_group.items() if g != "stand-ins" or len(by_group) == 1 for d in days]
    s = bc.stats(every)
    per = [bc.stats(days)["day"] for g, days in by_group.items() if g != "stand-ins" or len(by_group) == 1]
    s["worst"], s["best"] = min(per), max(per)
    return s


def line(table, level, budget, s):
    f1, f2 = s[1], s.get(2, {})
    where = "75" if budget is None else str(COMPOSITE[budget])
    return (f"{table} L{level} {where:>3s} XP days {s['day']:5.1f}% (worst {s['worst']:3.0f} best {s['best']:3.0f})"
            f" | F1 lose {f1['lose']:4.1f} Down {f1['down']:3.0f} Wnd {f1['wounded']:3.0f} rds {f1['rounds']:.1f}"
            f" again {f1['again']:2.0f} | F2 lose {f2.get('lose', 0):4.1f} Down {f2.get('down', 0):3.0f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", default="v1,v2")
    ap.add_argument("-L", default="1,2,3,4,5")
    ap.add_argument("-n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", help="append readings here (jsonl)")
    ap.add_argument("--nudge", default="", help="stat_sweep.py's per-Level nudges on top of the table")
    ap.add_argument("--days", default="manual", choices=("manual", "roster"),
                    help="the day's fights: the monster manual's encounters, or the old roster's four mixes")
    ap.add_argument("--standins", action="store_true", help="four stand-ins at every Level (to read Levels 4-5 against 2-3)")
    a = ap.parse_args()
    tables, levels = a.t.split(","), [int(x) for x in a.L.split(",")]
    DAY_SOURCE[0] = a.days
    STANDINS_ONLY[0] = a.standins
    jobs = [(t, L, b, gi, a.n, a.seed, a.standins, a.nudge) for t in tables for L in levels for b in POINTS[L]
            for gi in range(len(groups(L, b)))]
    res = {}
    with mp.Pool(a.j) as pool:
        for t, L, b, g, days in pool.imap(_job, jobs):
            res.setdefault((t, L, b), {})[g] = days
    for t in tables:
        for L in levels:
            for b in POINTS[L]:
                s = summarize(res[(t, L, b)])
                print(line(t, L, b, s), flush=True)
                if a.o:
                    with open(a.o, "a") as f:
                        f.write(json.dumps(dict(table=t, level=L, budget=b, n=a.n, standins=a.standins,
                                                stats=s)) + "\n")


if __name__ == "__main__":
    main()
