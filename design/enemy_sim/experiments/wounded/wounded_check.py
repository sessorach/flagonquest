"""What Wounded's penalties cost the party (designer, 2026-11-23).

Plays the stat_ladder days (each middle party at the Level, the manual's
encounters, `--extra` more attackers each) with whatever Wounded rules
SIM_SET gives, and prints the party's Health left after the day and the
share of days lost. Same seeds as stat_ladder's base cells.

    SIM_SET="WOUNDED_SPEED=0" python3 experiments/wounded/wounded_check.py -L 2 -n 100
"""
import argparse
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: F401
import tunables as T
import day_sim as ds
import party
import stat_ladder as sl
import xp_investments as xi


def job(a):
    level, extra, gi, mi, k0, k1 = a
    xi.register(level, extra)
    _, names, swaps = sl.groups(level)[gi]
    rows, out = party._rows(), []
    for k in range(k0, k1):
        rec, _ = ds.play_day(names, swaps, level, ds.day_mixes(mi, k), 100_000 * mi + k, rows)
        out.append(0 if rec["lost"] else rec["fights"][-1])
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=2)
    ap.add_argument("--extra", type=int, default=0)
    ap.add_argument("-n", type=int, default=100)
    a = ap.parse_args()
    jobs = [(a.L, a.extra, gi, mi, k, min(a.n, k + 25)) for gi in range(len(sl.groups(a.L)))
            for mi in range(T.MANUAL_MIXES) for k in range(0, a.n, 25)]
    with mp.Pool(os.cpu_count()) as pool:
        days = [x for r in pool.map(job, jobs) for x in r]
    print(f"L{a.L} x{a.extra} [{os.environ.get('SIM_SET', 'as written')}]: Health left {st.mean(days):.2f}, "
          f"days lost {100 * st.mean(d == 0 for d in days):.1f}%, n={len(days)}")
