"""The solo boss's size (2026-11-05).

Per the designer: a solo boss should be swingier and more dangerous than
usual but still not often beat the whole party. The Brute Warlord (4
Slots) alone at Levels 3-5, against every test party in the middle of the
band, fresh fights, with a 4-Slot enemy's Health at each multiple of a
standard enemy's (tunables.V3_SOLO_HEALTH; 9 as first built).

    python3 experiments/enemies/boss_check.py > results/enemy_stats/boss_check.txt
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

MULTS = (9, 8, 7, 6, 5)


def _job(args):
    mult, level, gi, n = args
    T.SLOT_MULTIPLIER[4] = T.V3_SOLO_HEALTH = mult
    out = mc._job((level, gi, f"x{mult}", ["Brute Warlord"], n, 31))
    out.update(mult=mult)
    return out


def main():
    jobs = [(m, L, gi, 60) for m in MULTS for L in (3, 4, 5) for gi in range(len(tc.groups(L, ps.MID[L])))]
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=4) as pool:
        for r in pool.imap_unordered(_job, jobs):
            res[(r["mult"], r["level"])].append(r)
    print("| Health (× a standard enemy) | Level | Lost (worst party) | Down | Wounded | Rounds |\n|---|---|---|---|---|---|")
    for m in MULTS:
        for L in (3, 4, 5):
            rs = res[(m, L)]
            print(f"| {m} | {L} | {100 * (1 - st.mean(r['won'] for r in rs)):.0f}% ({100 * (1 - min(r['won'] for r in rs)):.0f}%) | "
                  f"{100 * st.mean(r['down'] for r in rs):.0f}% | {100 * st.mean(r['wounded'] for r in rs):.0f}% | "
                  f"{st.mean(r['rounds'] for r in rs):.1f} |")


if __name__ == "__main__":
    main()
