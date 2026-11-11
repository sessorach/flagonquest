"""Defender walls on the hit-target table, potions on (2026-11-09).

Per the designer: fix the Defender walls. On the hit-target candidate
(tunables.V3_HIT_FIT) a Defender's bumps take its Defenses to the cap
(8 + the Level's Skill + V3_DEFENSE_CAP), and two Black Knights won 23% of
fights over 9.9 rounds. The variants lower the cap; it only binds on an
enemy whose bumps and picks reach it, which is mostly Defenders. Read on
the Defender fights (size_check's Black Knights, four of each manual
Defender) and a control (four standard monsters), Levels 1-5, the middle
of the band, 60 fights a party; the party carries its potions.

    SIM_SET="V3_HIT_FIT=True,V3_HIT_FIT_OVERRIDE='2:skill=2/resist=2/health=5'" \\
        python3 experiments/enemies/wall_fix.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import manual_check as mc  # noqa: E402
import size_check as sc  # noqa: E402
import boss_encounters as be  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

CAPS = (2, 1, 0)
SIZE = ("Black Knight + two standard", "Two Black Knights", "Black Knight + two minions + one standard")
FOURS = ("Iron Sentinel", "Hedge Knight", "Ironbranch Warden")


def _size(args):
    cap, job = args
    T.V3_DEFENSE_CAP = cap
    return cap, sc._job(job)


def _four(args):
    cap, label, job = args
    T.V3_DEFENSE_CAP = cap
    return cap, label, mc._job(job)


if __name__ == "__main__":
    sjobs, fjobs = [], []
    for L in (1, 2, 3, 4, 5):
        groups = tc.groups(L, ps.MID[L])
        for kind, label, enc in sc.encounters(L):
            if label in SIZE:
                c = dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(1 / 3, 3))
                for cap in CAPS:
                    for gi in range(len(groups)):
                        sjobs.append((cap, (c, ps.MID[L], gi, 60)))
        for cap in CAPS:
            for gi in range(len(groups)):
                for m in FOURS:
                    fjobs.append((cap, f"Four {m}s", (L, gi, m, [m] * 4, 60, 1)))
                for comp in be.draws(L, 4, k=2):
                    fjobs.append((cap, "Four standard (control)", (L, gi, "|".join(comp), list(comp), 60, 1)))
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for cap, r in pool.imap_unordered(_size, sjobs, chunksize=2):
            res[(cap, r["label"])].append(r)
        for cap, label, r in pool.imap_unordered(_four, fjobs, chunksize=2):
            res[(cap, label)].append(r)
    f = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                    f"{st.mean(r['rounds'] for r in rs):.1f}")
    labels = list(SIZE) + [f"Four {m}s" for m in FOURS] + ["Four standard (control)"]
    out = ["Lost / Down / rounds, Levels 1-5, middle of the band, potions on.", "",
           "| Encounter | " + " | ".join(f"Defense cap +{c}" for c in CAPS) + " |", "|---|" + "---|" * len(CAPS)]
    for label in labels:
        out.append(f"| {label} | " + " | ".join(f(res[(c, label)]) for c in CAPS) + " |")
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/wall_fix.txt"), "w").write(text + "\n")
