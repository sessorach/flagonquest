"""Harder enemy hits, paid for in Health (2026-11-08).

Per the designer: hits should be more threatening to the players; a lot
of an offense pick's measured worth (reprice.py: Damage +1 about 8
Health, Powerful Spell 13) comes from enemy attacks being soft, a hit of
3-5 against PC Resist 4-6. The variants raise the table's Damage Stat at
every Level and take enemy Health off to pay for it (and in one, a point
of Accuracy), everything else as it is.

Read on the band (table_check: bottom, middle and top, days won; the
first fight in the middle), the manual's fights (manual_check's draws,
middle), and what an enemy hit does: damage a hit lands after Resist and
Protected, as a share of the PC's max Health (traced fights, the
manual's encounters, the middle parties).

    python3 experiments/enemies/hard_hits.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import combat_sim as cs  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402
import tunables as T  # noqa: E402

LEVELS = (1, 2, 3, 4, 5)
VARIANTS = {
    "today": {},
    "Damage +1, Health -2": dict(damage=1, health=-2),
    "Damage +1, Health -4": dict(damage=1, health=-4),
    "Damage +2, Health -3": dict(damage=2, health=-3),
    "Damage +2, Health -5": dict(damage=2, health=-5),
    "Damage +2, Accuracy -1, Health -3": dict(damage=2, accuracy=-1, health=-3),
}
_BASE = {L: dict(t) for L, t in eb.ENEMY_TABLE_V3_PRUNED.items()}


def install(v):
    for L in _BASE:
        eb.ENEMY_TABLE_V3_PRUNED[L] = {k: x + VARIANTS[v].get(k, 0) for k, x in _BASE[L].items()}


def _band(args):
    v, job = args
    install(v)
    return v, tc._job(job)


def _manual(args):
    v, job = args
    install(v)
    return v, mc._job(job)


def _hits(args):
    """Enemy hits in traced fights: (damage landed, the target's max Health)."""
    v, level, gi = args
    install(v)
    T.ENEMY_LEVEL_UP = 0
    gname, names, swaps = [g for g in tc.groups(level, ps.MID[level]) if g[0] != "stand-ins"][gi]
    rows = party._rows()
    cs.make_party = lambda tier, good_luck=0: [
        party.make_pc(m, i, good_luck, rows=rows, edits=swaps.get(m, (None, None))[0],
                      row_changes=swaps.get(m, (None, None))[1]) for i, m in enumerate(names, 1)]
    out = []
    for ei, enc in enumerate(mc.encounters(level, 12, 1)):
        for k in range(4):
            trace = []
            enemies = se.build_encounter([f"{x}@{level}" for x in enc])
            r = cs.run_fight(1, min(level, 3), movement=True, enemies=enemies, seed=10_000 * gi + 100 * ei + k,
                             trace=trace)
            for t in trace:
                if t.get("side") == "enemy" and t.get("action") == "attack" and t.get("hit"):
                    out.append((t.get("dmg", 0), t.get("target")))
    return v, level, out


def pc_max_health(level):
    gname, names, swaps = [g for g in tc.groups(level, ps.MID[level]) if g[0] != "stand-ins"][0]
    return st.mean(party.make_pc(m, i, edits=swaps.get(m, (None, None))[0],
                                 row_changes=swaps.get(m, (None, None))[1])["max_health"]
                   for i, m in enumerate(names, 1))


if __name__ == "__main__":
    bjobs, mjobs, hjobs = [], [], []
    for v in VARIANTS:
        for L in LEVELS:
            for b in tc.POINTS[L]:
                for gi in range(len(tc.groups(L, b))):
                    bjobs.append((v, ("v3", L, b, gi, 60, 0, False, "")))
            ng = len([g for g in tc.groups(L, ps.MID[L]) if g[0] != "stand-ins"])
            for gi in range(len(tc.groups(L, ps.MID[L]))):
                for e in mc.encounters(L, 40, 1):
                    mjobs.append((v, (L, gi, "|".join(e), list(e), 30, 1)))
            for gi in range(ng):
                hjobs.append((v, L, gi))
    band = collections.defaultdict(dict)
    man = collections.defaultdict(list)
    hits = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for v, (t, L, b, g, days) in pool.imap_unordered(_band, bjobs):
            band[(v, L, b)][g] = days
        for v, r in pool.imap_unordered(_manual, mjobs, chunksize=4):
            man[(v, r["level"])].append(r)
        for v, L, out in pool.imap_unordered(_hits, hjobs):
            hits[(v, L)].extend(d for d, _ in out)
    mh = {L: pc_max_health(L) for L in LEVELS}
    out = ["Band: days won bottom / middle / top; middle, first fight: Down / Wounded / rounds / again. "
           "Manual (middle): lost / Down / rounds. An enemy hit: average damage landed, and as a share of "
           "an average PC's max Health.", ""]
    for L in LEVELS:
        out += [f"### Level {L} (an average PC: {mh[L]:.1f} Health)", "",
                "| Variant | Days won | First fight, middle | Manual | A hit lands |", "|---|---|---|---|---|"]
        for v in VARIANTS:
            s = [tc.summarize(band[(v, L, b)]) for b in tc.POINTS[L]]
            mid = s[len(s) // 2]
            f1 = mid[1]
            days = " / ".join(f"{x['day']:.0f}" for x in s)
            rs = man[(v, L)]
            h = hits[(v, L)]
            out.append(f"| {v} | {days} | {f1['down']:.0f}% / {f1['wounded']:.0f}% / {f1['rounds']:.1f} / "
                       f"{f1['again']:.0f}% | {100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / "
                       f"{100 * st.mean(r['down'] for r in rs):.0f}% / {st.mean(r['rounds'] for r in rs):.1f} | "
                       f"{st.mean(h):.1f} ({100 * st.mean(h) / mh[L]:.0f}%) |")
        out.append("")
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/hard_hits.txt"), "w").write(text + "\n")
