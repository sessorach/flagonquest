"""A flatter enemy table at Levels 2-4, paid back in budget (2026-11-08).

Kept for the record: its variants are changes to the table and budget as
they stood before 2026-11-08; with "budget as today" plus the Accuracy
fold in the default (enemy_builder_pcstyle.V3_FLAT_TABLE) it no longer
reproduces as written.

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
    python3 experiments/enemies/flat_table.py 3    # round three, Levels 2-5
    python3 experiments/enemies/flat_table.py size # every size, today against picked
    python3 experiments/enemies/flat_table.py 4    # round four, simpler budgets
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
import size_check as sc  # noqa: E402
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
# Round three (designer, 2026-11-08): split the difference on the step
# from Level 4 to 5 (Level 5 Defense -1 too, Resist as it was), and pay
# the cut back in Ability points, moving some to Health if the points
# make it too dangerous. A grid of points and Health, the same at Levels
# 2-5; each Level's enemies only meet that Level's band, so the best can
# be picked Level by Level.
CUT = {2: {"skill": -1, "resist": -1}, 3: {"skill": -1, "resist": -1}, 4: {"skill": -1, "resist": -1},
       5: {"skill": -1}}
GRID = [(3, 0), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 3), (0, 2)]
for _p, _h in GRID:
    VARIANTS[f"+{_p} points, Health +{_h}"] = {L: (dict(c, health=_h), _p) for L, c in CUT.items()}
# Picked from round three, Level by Level (middle of the band near 90% of
# days, Downs near one fight in five, about 4 rounds): points where they
# keep the fight's length, Health where points cut it short (Level 3).
VARIANTS["picked"] = {2: (dict(CUT[2], health=1), 2), 3: (dict(CUT[3], health=2), 0),
                      4: (dict(CUT[4], health=0), 1), 5: (dict(CUT[5], health=0), 1)}
# Round four (designer, 2026-11-08: is the budget a bit much?). At 13
# points (Levels 4-5) every standard monster can afford Accuracy +1 and
# then Damage +1; at 12 most can't. Two simpler budgets: 12 from Level 2
# on (Levels 4-5's point as Health +1), and today's 8 / 10 / 12 / 12 / 12
# (Level 2's two points as Health too).
VARIANTS["budget 8/12/12/12/12"] = {2: (dict(CUT[2], health=1), 2), 3: (dict(CUT[3], health=2), 0),
                                    4: (dict(CUT[4], health=1), 0), 5: (dict(CUT[5], health=1), 0)}
VARIANTS["budget as today"] = {2: (dict(CUT[2], health=3), 0), 3: (dict(CUT[3], health=2), 0),
                               4: (dict(CUT[4], health=1), 0), 5: (dict(CUT[5], health=1), 0)}
ROUND = {1: list(VARIANTS)[:5], 2: ["today", *list(VARIANTS)[5:9]], 3: ["today", *list(VARIANTS)[9:-3]],
         4: ["today", "picked", "budget 8/12/12/12/12", "budget as today"]}
_BASE = {L: dict(t) for L, t in eb.ENEMY_TABLE_V3_PRUNED.items()}
_EXTRA = dict(T.V3_PRUNED_EXTRA)


def install(v):
    spec = VARIANTS[v]
    # (changes, points) at Levels 2-4, or {Level: (changes, points)}.
    per = spec if isinstance(spec, dict) else {L: spec for L in (2, 3, 4)}
    for L in _BASE:
        eb.ENEMY_TABLE_V3_PRUNED[L] = dict(_BASE[L])
        for k, d in per.get(L, ({}, 0))[0].items():
            eb.ENEMY_TABLE_V3_PRUNED[L][k] += d
    T.V3_PRUNED_EXTRA = {L: n + per.get(L, ({}, 0))[1] for L, n in _EXTRA.items()}


def _band(args):
    v, job = args
    install(v)
    return v, tc._job(job)


def _manual(args):
    v, job = args
    install(v)
    return v, mc._job(job)


def _size(args):
    v, job = args
    install(v)
    return v, sc._job(job)


def size_compare():
    """Every size_check encounter, middle of the band, today against picked."""
    jobs = []
    for L in (1, 2, 3, 4, 5):
        for kind, label, enc in sc.encounters(L):
            c = dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(1 / 3, 3))
            for v in ("today", "picked"):
                for gi in range(len(tc.groups(L, ps.MID[L]))):
                    jobs.append((v, (c, ps.MID[L], gi, 60)))
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for v, r in pool.imap_unordered(_size, jobs, chunksize=2):
            res[(v, r["label"])].append(r)
            res[(v, r["label"], r["level"])].append(r)
    f = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                    f"{st.mean(r['rounds'] for r in rs):.1f}" if rs else "-")
    out = ["Lost / Down / Rounds, middle of the band, Levels 1-5 (Level 5 alone after).", "",
           "| Encounter | Today | Picked | Level 5: today | Level 5: picked |", "|---|---|---|---|---|"]
    for label in dict.fromkeys(k[1] for k in res if len(k) == 2):
        out.append(f"| {label} | {f(res[('today', label)])} | {f(res[('picked', label)])} | "
                   f"{f(res[('today', label, 5)])} | {f(res[('picked', label, 5)])} |")
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/flat_table_size.txt"), "w").write(text + "\n")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["size"]:
        size_compare()
        sys.exit()
    rnd = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    VARIANTS = {v: VARIANTS[v] for v in ROUND[rnd]}
    LEVELS = (2, 3, 4, 5) if rnd >= 3 else LEVELS
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
