"""Area Attack and Strike (Shoving) on the monster manual (2026-11-08).

Two new monsters for the test bench: the Blast Mage (Ranged Spell, Area
Attack: its attack also hits each other PC within 1 meter of its target)
and the Ram Brute (Two-Handed Weapon, Strike (Shoving) twice: its last
attack of the turn Pushes the target 4 meters; and Parting Shot). Each
against the nearest monster already in the manual (the Ember Caster, the
Thornhide Brute): four of a kind, and two with two standard companions
(a Brute and a Goblin Cutthroat). Levels 1-5, every party in the middle
of its band, 60 fresh fights a party.

    python3 experiments/enemies/new_mechanics.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

PAIRS = [("Blast Mage", "Ember Caster"), ("Ram Brute", "Thornhide Brute")]
COMPANIONS = ("Brute", "Goblin Cutthroat")


def encounters():
    out = []
    for new, old in PAIRS:
        for m in (new, old):
            out.append((f"Four {m}s", [m] * 4))
            out.append((f"Two {m}s + two standard", [m, m, *COMPANIONS]))
    return out


if __name__ == "__main__":
    jobs = []
    for L in (1, 2, 3, 4, 5):
        for gi in range(len(tc.groups(L, ps.MID[L]))):
            for label, enc in encounters():
                jobs.append((label, (L, gi, label, enc, 60, 1)))
    res = collections.defaultdict(list)

    def _job(args):
        return args[0], mc._job(args[1])
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for label, r in pool.imap_unordered(_job, jobs, chunksize=2):
            res[label].append(r)
            res[(label, r["level"])].append(r)
    f = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                    f"{100 * st.mean(r['wounded'] for r in rs):.0f}% / {st.mean(r['rounds'] for r in rs):.1f}")
    out = ["Lost / Down / Wounded / rounds, middle of the band.", "",
           "| Encounter | Levels 1-5 | By Level: lost / Down |", "|---|---|---|"]
    for label, _ in encounters():
        byL = " ".join(f"L{L} {100 * (1 - st.mean(r['won'] for r in res[(label, L)])):.0f}/"
                       f"{100 * st.mean(r['down'] for r in res[(label, L)]):.0f}" for L in (1, 2, 3, 4, 5))
        out.append(f"| {label} | {f(res[label])} | {byL} |")
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/new_mechanics.txt"), "w").write(text + "\n")
