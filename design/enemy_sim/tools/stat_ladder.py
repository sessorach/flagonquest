"""What each base stat is worth, from scratch (designer, 2026-11-13).

The yardstick is measured, not assumed: +1 Accuracy on one PC is 1.
Every test is a number changed directly on a built character (or on
every enemy) and played against the same days as the untouched party
(paired seeds). The score is the party's Health left after a day's
second fight, in points, 0 for a lost day.

Each PC of each middle party at the Level takes a turn as the carrier;
"all" tests change all four PCs, "enemy" tests every enemy. Days are
day_sim's, the manual's encounters with `--extra` more standard
attackers each (xp_investments.register).

    python3 tools/stat_ladder.py -L 2 -n 100               # runs, writes results/stat_ladder/L2_x0.json
    python3 tools/stat_ladder.py -L 2 -n 100 --seed 7      # a second set of shuffles (..._s7.json)
    python3 tools/stat_ladder.py --report "L2_x0"          # the table from saved runs (a glob)
"""
import argparse
import collections
import glob
import json
import math
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import sample_enemies as se  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import bands  # noqa: E402
import resume  # noqa: E402
import xp_investments as xi  # noqa: E402

DEF3 = ("bodily", "mental", "vigilant")
# label -> {key: change}. "passive" adds a combat_sim Test passive.
PC_TESTS = {
    "Null (nothing changed)": {"null_test": 1},
    **{f"Accuracy {n:+d}": {"skill_total": n} for n in (-1, 1, 2, 3)},
    **{f"Damage {n:+d}": {"damage": n} for n in (1, 2)},
    **{f"Health {n:+d}": {"health": n, "max_health": n} for n in (1, 2, 4)},
    "Shallow Health +1": {"health": 1, "max_health": 1, "shallow_max": 1},
    **{f"Parry and Dodge {n:+d}": {"parry": n, "dodge": n} for n in (1, 2)},
    "Parry +1": {"parry": 1},
    "Dodge +1": {"dodge": 1},
    "Vital, Mental, Vigilant +1": dict.fromkeys(DEF3, 1),
    "Every Defense +1": dict.fromkeys(("parry", "dodge") + DEF3, 1),
    "Physical Resist +1": {"physres": 1},
    "Elemental Resist +1": {"elemres": 1},
    "Speed +1": {"speed": 1},
    **{f"Reflex {n:+d}": {"reflex": n} for n in (1, 2)},
    "Hand size +1": {"hand_size": 1},
    "Good Luck, first attack": {"passive": "Test:goodluck:1:first"},
    "Good Luck, every turn": {"passive": "Test:goodluck:1:turn"},
    "One extra attack a fight": {"bonus_attack_control": True},
    "Accuracy +1 and Damage +1": {"skill_total": 1, "damage": 1},
    "Accuracy +1 and Health +2": {"skill_total": 1, "health": 2, "max_health": 2},
}
ALL_TESTS = {f"All four: {k}": PC_TESTS[k] for k in
             ("Accuracy +1", "Damage +1", "Health +1", "Parry and Dodge +1", "Every Defense +1", "Physical Resist +1")}
ENEMY_TESTS = {
    "Enemies: Accuracy -1": {"accuracy": -1},
    "Enemies: Damage -1": {"attack_damage": -1},
    "Enemies: Health -1": {"health": -1, "max_health": -1},
    "Enemies: Health -2": {"health": -2, "max_health": -2},
    "Enemies: every Defense -1": dict.fromkeys(("parry", "dodge") + DEF3, -1),
    "Enemies: Parry and Dodge -1": {"parry": -1, "dodge": -1},
    "Enemies: Resists -1": {"physres": -1, "elemres": -1},
    "Enemies: Speed -1": {"speed": -1},
    "Enemies: Reflex -1": {"reflex": -1},
}
TESTS = {**PC_TESTS, **ALL_TESTS, **ENEMY_TESTS}
OUT = os.path.join(_paths.ROOT, "results", "stat_ladder")


def groups(level):
    return [g for g in bands.groups(level, bands.MID[level]) if g[0] != "stand-ins"]


def cells(level, only=None):
    """(party index, seat or None, label): the base, each PC test on each
    seat, and each all-party or enemy test once a party."""
    out = []
    for gi, g in enumerate(groups(level)):
        out.append((gi, None, "base"))
        for label in TESTS:
            if only and not any(x in label for x in only):
                continue
            out += [(gi, s, label) for s in range(4)] if label in PC_TESTS else [(gi, None, label)]
    return out


def change(u, spec):
    for k, v in spec.items():
        if k == "passive":
            u["passives"] = list(u["passives"]) + [v]
        elif isinstance(v, bool):
            u[k] = v
        elif u.get(k, 0) > -50:  # an enemy with no Parry is -99: leave it
            u[k] = u.get(k, 0) + v
            for prof in [u.get("backup")] if k in ("accuracy", "attack_damage") and u.get("backup") else []:
                prof[k] = prof.get(k, 0) + v


def job(args):
    level, extra, cell, mi, k0, k1, seed = args
    xi.register(level, extra)
    gi, seat, label = cell
    _, names, swaps = groups(level)[gi]
    spec = TESTS.get(label)
    real_maker, real_build = ds._maker, se.build_encounter

    def maker(names_, swaps_, rows_, full):
        make, last = real_maker(names_, swaps_, rows_, full)

        def made(tier, good_luck=0):
            pcs = make(tier, good_luck)
            for i, p in enumerate(pcs):
                if label in PC_TESTS and i == seat or label in ALL_TESTS:
                    change(p, spec)
            full[:] = [p["max_health"] for p in pcs]
            return pcs
        return made, last

    def build(enc):
        en = real_build(enc)
        for e in en:
            change(e, spec)
        return en
    ds._maker = maker
    if label in ENEMY_TESTS:
        se.build_encounter = build
    rows, out = party._rows(), []
    try:
        for k in range(k0, k1):
            rec, _ = ds.play_day(names, swaps, level, ds.day_mixes(mi, k), seed + 100_000 * mi + k, rows)
            out.append(0 if rec["lost"] else rec["fights"][-1])
    finally:
        ds._maker, se.build_encounter = real_maker, real_build
    return cell, mi, k0, out


def run(a, path):
    """Resumable: finished chunks are kept in `path`.partial."""
    cl = cells(a.L, a.only and a.only.split(","))
    jobs = [(a.L, a.extra, c, mi, k, min(a.n, k + 25), a.seed) for c in cl for mi in range(T.MANUAL_MIXES)
            for k in range(0, a.n, 25)]
    part = resume.Partial(path + ".partial")
    todo = [j for j in jobs if (j[2], j[3], j[4]) not in part]
    print(f"{len(cl)} cells, {len(todo)}/{len(jobs)} chunks to play", flush=True)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for i, (cell, mi, k0, out) in enumerate(pool.imap_unordered(job, todo, chunksize=4)):
            part.add((cell, mi, k0), out)
            if i % 500 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    res = collections.defaultdict(list)
    for j in jobs:
        res[j[2]] += part.get((j[2], j[3], j[4]))
    names = [[n.split(" (")[0] for n in g[1]] for g in groups(a.L)]
    json.dump(dict(level=a.L, extra=a.extra, n=a.n, seed=a.seed, names=names,
                   cells=[[list(c), res[c]] for c in cl]), open(path, "w"))
    part.finish()


def load(pattern):
    """label -> list of (carrier name or None, mean Health gained, SE), over
    every saved run matching the glob, plus the base's losses and Health."""
    rows, base = collections.defaultdict(list), []
    for p in sorted(glob.glob(os.path.join(OUT, pattern + ".json"))):
        d = json.load(open(p))
        b = {c[0]: r for c, r in d["cells"] if c[2] == "base"}
        base += [x for r in b.values() for x in r]
        for (gi, seat, label), r in d["cells"]:
            if label == "base":
                continue
            diff = [x - y for x, y in zip(r, b[gi])]
            rows[label].append((None if seat is None else d["names"][gi][seat],
                                st.mean(diff), st.stdev(diff) / math.sqrt(len(diff))))
    return rows, base


def report(pattern):
    rows, base = load(pattern)
    avg = lambda xs: (st.mean(m for _, m, _ in xs), math.sqrt(sum(s * s for _, _, s in xs)) / len(xs))
    unit, unit_se = avg(rows["Accuracy +1"])
    print(f"{pattern}: base Health left {st.mean(base):.1f}, days lost {100 * st.mean(x == 0 for x in base):.1f}%; "
          f"Accuracy +1 on one PC = {unit:.3f} ± {unit_se:.3f} Health = 1 unit\n")
    print("| Test | Health left | ± | In Accuracy +1s | Weakest carrier | Strongest carrier |")
    print("|---|---|---|---|---|---|")
    for label, xs in rows.items():
        m, se_ = avg(xs)
        by = collections.defaultdict(list)
        for who, v, _ in xs:
            by[who].append(v)
        by = {k: st.mean(v) for k, v in by.items()}
        lo, hi = min(by, key=by.get), max(by, key=by.get)
        spread = f"{lo} {by[lo]:+.2f} | {hi} {by[hi]:+.2f}" if lo is not None else " | "
        print(f"| {label} | {m:+.3f} | {se_:.3f} | {m / unit:+.2f} | {spread} |")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=2)
    ap.add_argument("--extra", type=int, default=0)
    ap.add_argument("-n", type=int, default=100, help="days a mix")
    ap.add_argument("--seed", type=int, default=0, help="a different set of shuffles (times 10 million)")
    ap.add_argument("--only", help="only tests whose label contains one of these (comma-separated)")
    ap.add_argument("--report", help="print the table for saved runs matching this glob")
    a = ap.parse_args()
    if a.report:
        report(a.report)
    else:
        os.makedirs(OUT, exist_ok=True)
        a.seed *= 10_000_000
        name = f"L{a.L}_x{a.extra}" + (f"_s{a.seed // 10_000_000}" if a.seed else "")
        run(a, os.path.join(OUT, name + ".json"))
        report(name)
