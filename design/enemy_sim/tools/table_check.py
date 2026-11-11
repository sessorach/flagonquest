"""The band check: the enemy table against parties across each Level's XP band.

Per the designer (2026-11-02): Level N enemies are for PCs within 25 XP of
that Level's schedule, so a party at the bottom of the band should feel
some friction and one at the top should be comfortable. Each Level's
parties (bands.groups: the eight band parties, Level 1's six sample
parties) play whole days (day_sim, two fights) of the monster manual's
encounters at the Level (`--days roster` for the old four mixes; Levels
4-5 then build Level 3's mixes Levels higher). Every point is a composite
(total) XP, the designer's unit, played at its combat share.

    python3 tools/table_check.py -n 100 -o results/enemy_stats/band.jsonl
"""
import argparse
import json
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401
import day_sim as ds  # noqa: E402
import tunables as T  # noqa: E402
import bands  # noqa: E402
from bands import POINTS, COMPOSITE, STANDINS_ONLY, groups  # noqa: E402

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
    T.ENEMY_LEVEL_UP = 0
    T.MANUAL_MIXES = MANUAL_MIXES
    se.CURRENT_MIXES = se.install_manual_mixes(level_into=min(level, 3), build_level=level)
    return max(1, round(n * 4 / len(se.CURRENT_MIXES)))


def _job(args):
    table, level, budget, gi, n, seed, standins = args
    STANDINS_ONLY[0] = standins
    T.ENEMY_TABLE = table
    T.ENEMY_LEVEL_UP = max(0, level - 3)
    ds.set_mult(1.0)
    gname, names, swaps = groups(level, budget)[gi]
    if DAY_SOURCE[0] == "manual":
        n = _manual_mixes(level, n)
    else:
        import sample_enemies as se
        se.CURRENT_MIXES = se.ROSTER_MIXES
    recs = ds.run(names, swaps, min(level, 3), n, seed=seed)
    return table, level, budget, gname, [r.get("per_fight", []) for r in recs]


def summarize(by_group):
    every = [d for g, days in by_group.items() if g != "stand-ins" or len(by_group) == 1 for d in days]
    s = bands.stats(every)
    per = [bands.stats(days)["day"] for g, days in by_group.items() if g != "stand-ins" or len(by_group) == 1]
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
    ap.add_argument("-t", default="v3")
    ap.add_argument("-L", default="1,2,3,4,5")
    ap.add_argument("-n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", help="append readings here (jsonl)")
    ap.add_argument("--days", default="manual", choices=("manual", "roster"),
                    help="the day's fights: the monster manual's encounters, or the old roster's four mixes")
    ap.add_argument("--standins", action="store_true", help="four stand-ins at every Level (to read Levels 4-5 against 2-3)")
    a = ap.parse_args()
    tables, levels = a.t.split(","), [int(x) for x in a.L.split(",")]
    DAY_SOURCE[0] = a.days
    STANDINS_ONLY[0] = a.standins
    jobs = [(t, L, b, gi, a.n, a.seed, a.standins) for t in tables for L in levels for b in POINTS[L]
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
