"""A flatter enemy table at Levels 2-4, paid back in budget (2026-11-08).

Per the designer: weigh enemy stats a bit flatter at Levels 2-4 and give
back some Ability budget, so the enemies challenge the party without
overwhelming the bottom of the band. A band is about one enemy Level of
PC growth, and the bottom of it loses most days (ENEMY_ENCOUNTER_DESIGN,
"Why the bands are steep"). The variants take the table's Skill (every
Defense) and/or Resist down 1 at Levels 2-4 and add Ability points
(V3_PRUNED_EXTRA) at about the picks' prices: Skill -1 is Dodge, Parry
and Vital/Mental/Vigilant -1, about 3 points; Resist -1 is 4 (Resist +1's
price). The extra points spend offense first (Accuracy, Damage), then the
row's PrunedExtra, then Health. Levels 1 and 5 unchanged.

Read on the band (table_check: bottom, middle and top of each Level's
band, days won) and the manual's fights (manual_check's draws, middle of
the band).

    python3 experiments/enemies/flat_table.py      # round one
    python3 experiments/enemies/flat_table.py 2    # round two
"""
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

LEVELS = (2, 3, 4)
# name: (table changes at Levels 2-4, extra points at Levels 2-4)
VARIANTS = {
    "today": ({}, 0),
    "Defense -1, +3 points": ({"skill": -1}, 3),
    "Resist -1, +4 points": ({"resist": -1}, 4),
    "both -1, +5 points": ({"skill": -1, "resist": -1}, 5),
    "both -1, +7 points": ({"skill": -1, "resist": -1}, 7),
    # Round two: the first round's points (at the picks' prices) bought
    # offense worth more than the Defense and Resist they replaced.
    "both -1, +3 points": ({"skill": -1, "resist": -1}, 3),
    "both -1, +2 points": ({"skill": -1, "resist": -1}, 2),
    "both -1, Health +5": ({"skill": -1, "resist": -1, "health": 5}, 0),
    "both -1, Health +3": ({"skill": -1, "resist": -1, "health": 3}, 0),
}
ROUND = {1: list(VARIANTS)[:5], 2: ["today", *list(VARIANTS)[5:]]}
_BASE = {L: dict(t) for L, t in eb.ENEMY_TABLE_V3_PRUNED.items()}
_EXTRA = dict(T.V3_PRUNED_EXTRA)


def install(v):
    changes, pts = VARIANTS[v]
    for L in _BASE:
        eb.ENEMY_TABLE_V3_PRUNED[L] = dict(_BASE[L])
        if L in LEVELS:
            for k, d in changes.items():
                eb.ENEMY_TABLE_V3_PRUNED[L][k] += d
    T.V3_PRUNED_EXTRA = {L: n + (pts if L in LEVELS else 0) for L, n in _EXTRA.items()}


def _band(args):
    v, job = args
    install(v)
    return v, tc._job(job)


def _manual(args):
    v, job = args
    install(v)
    return v, mc._job(job)


if __name__ == "__main__":
    import sys
    rnd = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    VARIANTS = {v: VARIANTS[v] for v in ROUND[rnd]}
    bjobs, mjobs = [], []
    for v in VARIANTS:
        for L in LEVELS:
            for b in tc.POINTS[L]:
                for gi in range(len(tc.groups(L, b))):
                    bjobs.append((v, ("v3", L, b, gi, 60, 0, False, "")))
            for gi in range(len(tc.groups(L, ps.MID[L]))):
                for e in mc.encounters(L, 40, 1):
                    mjobs.append((v, (L, gi, "|".join(e), list(e), 30, 1)))
    band = collections.defaultdict(dict)
    man = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for v, (t, L, b, g, days) in pool.imap_unordered(_band, bjobs):
            band[(v, L, b)][g] = days
        for v, r in pool.imap_unordered(_manual, mjobs, chunksize=4):
            man[(v, r["level"])].append(r)
    out = ["Band: days won at the bottom / middle / top (worst middle party); middle, first fight: "
           "Down / Wounded / rounds / again. Manual fights (middle): lost / Down / rounds.", ""]
    recs = []
    for L in LEVELS:
        out += [f"### Level {L}", "",
                "| Variant | Days won (bottom / middle / top) | Worst middle party | First fight, middle: Down / Wnd / rounds / again | Manual: lost / Down / rounds |",
                "|---|---|---|---|---|"]
        for v in VARIANTS:
            s = [tc.summarize(band[(v, L, b)]) for b in tc.POINTS[L]]
            f1 = s[1][1]
            rs = man[(v, L)]
            out.append(f"| {v} | {s[0]['day']:.0f}% / {s[1]['day']:.0f}% / {s[2]['day']:.0f}% | {s[1]['worst']:.0f}% | "
                       f"{f1['down']:.0f}% / {f1['wounded']:.0f}% / {f1['rounds']:.1f} / {f1['again']:.0f}% | "
                       f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                       f"{st.mean(r['rounds'] for r in rs):.1f} |")
            recs.append(dict(variant=v, level=L, band=[x["day"] for x in s], worst=s[1]["worst"], f1=f1))
        out.append("")
    text = "\n".join(out)
    print(text)
    base = os.path.join(_paths.ROOT, "results/enemy_stats/flat_table" + ("" if rnd == 1 else f"_{rnd}"))
    open(base + ".txt", "w").write(text + "\n")
    with open(base + ".jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
