"""Heavy armor at a higher price (2026-11-07).

Per the designer: should Heavy armor cost a bit more? It's 4 points today
(Unarmored -2, Light 0, Medium 2). Heavy at 5 and 6, everything else the
same: the manual's fights (manual_check's draws, middle of the band), and
the elite and boss fights with a Heavy-armored big enemy (size_check's
Black Knights and solo Warlord, the Ogre fights for comparison). At 6 two
manual monsters (Ironbranch Warden, Iron Sentinel) go under the Health
floor at Level 1, so the floor is off for the test.

    python3 experiments/enemies/heavy_armor_price.py
"""
import collections
import json
import multiprocessing as mp
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import size_check as sc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

COSTS = [4, 5, 6]
SIZE_LABELS = ("Black Knight + two standard", "Two Black Knights", "Solo Brute Warlord",
               "Gravel Ogre + two standard", "Two Gravel Ogres")


def _manual(args):
    cost, job = args
    eb.ARMOR_HEALTH_V3P["Heavy"] = cost
    T.V3_HEALTH_FLOOR = 0
    return cost, mc._job(job)


def _size(args):
    cost, job = args
    eb.ARMOR_HEALTH_V3P["Heavy"] = cost
    T.V3_HEALTH_FLOOR = 0
    return cost, sc._job(job)


if __name__ == "__main__":
    mjobs, sjobs = [], []
    for L in (1, 2, 3, 4, 5):
        groups = tc.groups(L, ps.MID[L])
        encs = mc.encounters(L, 40, 1)
        heavy = [e for e in encs if any(eb.ARMOR_HEALTH_V3P and n in ("Ironbranch Warden", "Iron Sentinel", "Brute Warlord")
                                         for n in e)]
        for cost in COSTS:
            for gi in range(len(groups)):
                for e in encs:
                    mjobs.append((cost, (L, gi, "|".join(e), list(e), 30, 1)))
        for kind, label, enc in sc.encounters(L):
            if label not in SIZE_LABELS:
                continue
            c = dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(1 / 3, 3))
            for cost in COSTS:
                for gi in range(len(groups)):
                    sjobs.append((cost, (c, ps.MID[L], gi, 60)))
    res = collections.defaultdict(list)
    with mp.Pool(4, maxtasksperchild=50) as pool:
        for cost, r in pool.imap_unordered(_manual, mjobs, chunksize=4):
            res[("manual", cost, r["level"], "heavy" if any(n in ("Ironbranch Warden", "Iron Sentinel", "Brute Warlord")
                                                             for n in r["enemies"]) else "other")].append(r)
        for cost, r in pool.imap_unordered(_size, sjobs, chunksize=2):
            res[("size", cost, r["label"])].append(r)
    line = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                       f"{st.mean(r['rounds'] for r in rs):.1f}")
    out = ["| Manual fights | Heavy 4 (today) | 5 | 6 |", "|---|---|---|---|"]
    for L in (1, 2, 3, 4, 5):
        for part in ("heavy", "other"):
            out.append(f"| Level {L}, {'with' if part == 'heavy' else 'without'} a Heavy-armored monster | "
                       + " | ".join(line(res[("manual", c, L, part)]) for c in COSTS) + " |")
    out += ["", "| Encounter (Levels 1-5) | Heavy 4 (today) | 5 | 6 |", "|---|---|---|---|"]
    for label in SIZE_LABELS:
        out.append(f"| {label} | " + " | ".join(line(res[("size", c, label)]) for c in COSTS) + " |")
    text = "\n".join(out)
    print(text)
    open("results/enemy_stats/heavy_armor_price.txt", "w").write(text + "\n")
