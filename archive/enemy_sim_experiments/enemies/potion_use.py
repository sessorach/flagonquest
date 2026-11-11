"""How the party uses two Healing Potions each (2026-11-09).

Per the designer: give every PC two Healing Potions for the day (2 AP to
drink, heal 2, no refresh; tunables.PC_POTIONS) and see whether they stop
a downward spiral at the bottom of a band, and whether they help in a
fight at all. This counts what gets drunk: table_check's days (two fights
and the care between), every party at the bottom, middle and top of its
band, Levels 1-5, table_check's days (15 a mix); on the pencilled table, or with
V3_HIT_FIT set (SIM_SET="V3_HIT_FIT=True") on the hit-target candidate.
table_check.py itself, run with and without SIM_SET="PC_POTIONS=2", gives
the days won.

    SIM_SET="PC_POTIONS=2" python3 experiments/enemies/potion_use.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import combat_sim as cs  # noqa: E402
import day_sim as ds  # noqa: E402
import table_check as tc  # noqa: E402

_DAYS = []
_orig_fight = cs.run_fight


def _traced(*a, **k):
    """Each fight traced; a day's first fight starts a new count."""
    trace = []
    k["trace"] = trace
    r = _orig_fight(*a, **k)
    if k.get("day_fight") == 1 or not _DAYS:
        _DAYS.append(0)
    _DAYS[-1] += sum(1 for t in trace if t.get("via") == "Healing Potion")
    return r


cs.run_fight = _traced


def _job(args):
    level, budget, gi, n = args
    T.ENEMY_LEVEL_UP = max(0, level - 3)
    ds.set_mult(1.0)
    gname, names, swaps = tc.groups(level, budget)[gi]
    del _DAYS[:]
    recs = ds.run(names, swaps, min(level, 3), n, seed=7_000)
    assert len(recs) == len(_DAYS), (len(recs), len(_DAYS))
    return level, budget, [(d, not r.get("lost"), len(r.get("per_fight", []))) for d, r in zip(_DAYS, recs)]


if __name__ == "__main__":
    jobs = [(L, b, gi, 15) for L in (1, 2, 3, 4, 5) for b in tc.POINTS[L] for gi in range(len(tc.groups(L, b)))]
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count()) as pool:
        for L, b, out in pool.imap_unordered(_job, jobs):
            res[(L, b)].extend(out)
    lines = [f"PC_POTIONS={T.PC_POTIONS}, V3_HIT_FIT={T.V3_HIT_FIT}. Potions drunk a day (of {4 * T.PC_POTIONS}), "
             "in days won and days lost; share of days with any drunk.", "",
             "| Level | Band point | Drunk a day | In days won | In days lost | Days with any |", "|---|---|---|---|---|---|"]
    for L in (1, 2, 3, 4, 5):
        for b in tc.POINTS[L]:
            o = res[(L, b)]
            won = [d for d, w, _ in o if w]
            lost = [d for d, w, _ in o if not w]
            lines.append(f"| {L} | {'mid' if b is None else b} | {st.mean(d for d, _, _ in o):.2f} | "
                         f"{st.mean(won) if won else 0:.2f} | {st.mean(lost) if lost else 0:.2f} | "
                         f"{100 * st.mean(d > 0 for d, _, _ in o):.0f}% |")
    text = "\n".join(lines)
    print(text)
    name = "potion_use_hitfit" if T.V3_HIT_FIT else "potion_use"
    open(os.path.join(_paths.ROOT, "results", "enemy_stats", name + ".txt"), "w").write(text + "\n")
