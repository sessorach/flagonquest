"""Heavy armor from Level 3 only (2026-11-08).

Per the designer: maybe Heavy armor is for Level 3 and higher enemies.
tunables.V3_HEAVY_MIN_LEVEL = 3: at Levels 1-2 a Heavy design wears Medium
(Physical Resist +2, Dodge -1, no Speed -1, 2 points instead of 6) and the
points it saves are Health. Levels 1-2 only (nothing changes from Level
3): the manual's fights (manual_check's draws, middle of the band) and
size_check's Black Knight fights, against the default (Heavy at any
Level).

    python3 experiments/enemies/heavy_level3.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import manual_check as mc  # noqa: E402
import size_check as sc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

HEAVY = ("Ironbranch Warden", "Iron Sentinel")
VARIANTS = {"any Level": None, "Level 3+": 3}
SIZE_LABELS = ("Black Knight + two standard", "Two Black Knights", "Black Knight + two minions + one standard")


def _manual(args):
    v, job = args
    T.V3_HEAVY_MIN_LEVEL = VARIANTS[v]
    return v, mc._job(job)


def _size(args):
    v, job = args
    T.V3_HEAVY_MIN_LEVEL = VARIANTS[v]
    return v, sc._job(job)


if __name__ == "__main__":
    mjobs, sjobs = [], []
    for L in (1, 2):
        groups = tc.groups(L, ps.MID[L])
        for v in VARIANTS:
            for gi in range(len(groups)):
                for e in mc.encounters(L, 40, 1):
                    mjobs.append((v, (L, gi, "|".join(e), list(e), 60, 1)))
            for kind, label, enc in sc.encounters(L):
                if label in SIZE_LABELS:
                    c = dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(1 / 3, 3))
                    for gi in range(len(groups)):
                        sjobs.append((v, (c, ps.MID[L], gi, 60)))
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for v, r in pool.imap_unordered(_manual, mjobs, chunksize=4):
            part = "heavy" if any(n in HEAVY for n in r["enemies"]) else "other"
            res[(v, r["level"], part)].append(r)
            res[(v, r["level"], "all")].append(r)
        for v, r in pool.imap_unordered(_size, sjobs, chunksize=2):
            res[(v, r["level"], r["label"])].append(r)
    line = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                       f"{st.mean(r['rounds'] for r in rs):.1f}" if rs else "-")
    out = ["Lost / Down / Rounds, middle of the band.", "",
           "| | Heavy at any Level (default) | Heavy from Level 3 |", "|---|---|---|"]
    for L in (1, 2):
        for part, name in (("all", "manual fights, all"), ("heavy", "manual, with a Warden or Sentinel"),
                           ("other", "manual, without"), *((x, x) for x in SIZE_LABELS)):
            out.append(f"| Level {L}, {name} | " + " | ".join(line(res[(v, L, part)]) for v in VARIANTS) + " |")
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/heavy_level3.txt"), "w").write(text + "\n")
