"""Boss encounters on the new defaults (2026-11-06).

The defaults the designer chose: elites at twice the budget (offense
only, the manual's BigPicks) and Health x2.5; a boss-grade elite
("Name@L:boss") at Health x3; the solo boss at twice the budget and
Health x4. Per Level: each manual elite as a boss leading two standard
monsters, the same with an ordinary elite, two boss elites together, the
solo Brute Warlord (Levels 3-5), and all-standard fights of the same
Slots, the companions fixed draws (boss_encounters.draws). Every party
at the low, middle and high points of its band, 60 fresh fights each.

    python3 experiments/enemies/boss_check2.py --txt results/enemy_stats/boss_check2.txt
"""
import argparse
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import table_check as tc  # noqa: E402
import boss_encounters as be  # noqa: E402

ELITES = ["Gravel Ogre", "Coven Matriarch"]


def encounters(L):
    out = []
    for comp in be.draws(L, 4):
        out.append(("Four standard monsters", [f"{c}@{L}" for c in comp]))
    for e in ELITES:
        for comp in be.draws(L, 2):
            rest = [f"{c}@{L}" for c in comp]
            out.append((f"{e} (elite) + two standard", [f"{e}@{L}", *rest]))
            out.append((f"{e} (boss) + two standard", [f"{e}@{L}:boss", *rest]))
    out.append(("Two boss elites (Ogre and Matriarch)", [f"{e}@{L}:boss" for e in ELITES]))
    out.append(("Two Gravel Ogres (boss)", [f"Gravel Ogre@{L}:boss"] * 2))
    if L >= 3:
        out.append(("Solo Brute Warlord", [f"Brute Warlord@{L}"]))
    return out


def _job(args):
    L, budget, gi, label, enc, n = args
    T.ENEMY_LEVEL_UP = 0
    gname, pn, sw = tc.groups(L, budget)[gi]
    se.ENCOUNTERS.setdefault(min(L, 3), {})["_t"] = enc
    rows = party._rows()
    out = collections.Counter()
    for k in range(n):
        rec, _ = ds.play_day(pn, sw, min(L, 3), ("_t",), 41 + 1000 * k, rows)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["down"] += f["downs"] > 0
        out["down2"] += f["downs"] > 1
        out["rounds"] += f["rounds"]
    pos = 1 if L == 1 else tc.POINTS[L].index(budget)
    return dict(level=L, pos=pos, label=label, enc="|".join(enc),
                **{k: out[k] / n for k in ("won", "down", "down2", "rounds")})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("--txt")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    jobs = [(L, b, gi, label, enc, a.n) for L in (1, 2, 3, 4, 5) for b in tc.POINTS[L]
            for gi in range(len(tc.groups(L, b))) for label, enc in encounters(L)]
    recs = []
    with mp.Pool(a.j, maxtasksperchild=50) as pool:
        for r in pool.imap_unordered(_job, jobs, chunksize=2):
            recs.append(r)
    labels = list(dict.fromkeys(label for L in (3,) for label, _ in encounters(L)))
    out = ["| Encounter | Lost (worst encounter) | Down | 2+ Down | Rounds | By Level: lost / Down | Low / high band lost |",
           "|---|---|---|---|---|---|---|"]
    for label in labels:
        rs = [r for r in recs if r["label"] == label]
        mid = [r for r in rs if r["pos"] == 1]
        by_enc = collections.defaultdict(list)
        for r in mid:
            by_enc[(r["level"], r["enc"])].append(1 - r["won"])
        byL = " ".join(f"L{L} {100 * (1 - st.mean(r['won'] for r in mid if r['level'] == L)):.0f}/"
                       f"{100 * st.mean(r['down'] for r in mid if r['level'] == L):.0f}"
                       for L in (1, 2, 3, 4, 5) if any(r["level"] == L for r in mid))
        lo = [r for r in rs if r["pos"] == 0]
        hi = [r for r in rs if r["pos"] == 2]
        out.append(f"| {label} | {100 * (1 - st.mean(r['won'] for r in mid)):.1f}% "
                   f"({100 * max(st.mean(v) for v in by_enc.values()):.0f}%) | "
                   f"{100 * st.mean(r['down'] for r in mid):.0f}% | {100 * st.mean(r['down2'] for r in mid):.0f}% | "
                   f"{st.mean(r['rounds'] for r in mid):.1f} | {byL} | "
                   f"{100 * (1 - st.mean(r['won'] for r in lo)):.0f}% / {100 * (1 - st.mean(r['won'] for r in hi)):.0f}% |")
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


if __name__ == "__main__":
    main()
