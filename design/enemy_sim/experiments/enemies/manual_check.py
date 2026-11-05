"""The monster manual in fights (2026-11-05).

Per the designer: test the manual's monsters broadly and see what can be
learned. Encounters are drawn from monster_manual.csv by the designer's
rules (ENEMY_ENCOUNTER_DESIGN.md "Enemy variety standard"): Slots equal
to the party's four, two stat blocks usually and three sometimes, at most
one enemy that doesn't attack, the solo boss alone and only from Level 3.
Every encounter is fought fresh by each of table_check's parties in the
middle of the band (day_sim's fight, care and night, one fight), the
monsters built at the Level itself. Results per encounter and party go to
a jsonl; a rerun skips what's there. --read fits each monster's share of
an encounter's difficulty.

    python3 experiments/enemies/manual_check.py -o results/enemy_stats/manual_check.jsonl
    python3 experiments/enemies/manual_check.py -o results/enemy_stats/manual_check.jsonl --read
"""
import argparse
import collections
import itertools
import json
import multiprocessing as mp
import os
import random
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import sample_enemies as se  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

PARTY_SLOTS = 4
SOLO = 4.0


def monsters(level=3):
    out = {}
    for n in se.manual_names():
        e = se.get_enemy(f"{n}@{level}")
        out[n] = dict(slots=float(e.get("slots", 1)), passive=e["kind"] != "attack")
    return out


def encounters(level, k, seed):
    rng = random.Random(seed * 100 + level)
    ms = monsters()
    pool = [n for n, m in ms.items() if m["slots"] != SOLO]
    out, seen = [], set()
    while len(out) < k:
        picks = rng.sample(pool, 2 if rng.random() < 0.6 else 3)
        options = []
        for counts in itertools.product(range(1, 9), repeat=len(picks)):
            if abs(sum(c * ms[p]["slots"] for c, p in zip(counts, picks)) - PARTY_SLOTS) > 1e-9:
                continue
            if sum(c for c, p in zip(counts, picks) if ms[p]["passive"]) > 1:
                continue
            options.append(counts)
        if not options:
            continue
        counts = rng.choice(options)
        enc = tuple(sorted(n for c, p in zip(counts, picks) for n in [p] * c))
        if enc not in seen:
            seen.add(enc)
            out.append(enc)
    if level >= 3:
        out += [tuple(n for n, m in ms.items() if m["slots"] == SOLO)]
    return out


def reference(level):
    """The four mixes everything was tuned on (Levels 1-3 rows)."""
    return {f"ref:{m}": tuple(se.ENCOUNTERS[level][m]) for m in se.CURRENT_MIXES} if level <= 3 else {}


def _job(args):
    level, gi, key, names, n, seed = args
    T.ENEMY_LEVEL_UP = 0
    gname, pnames, swaps = tc.groups(level, ps.MID[level])[gi]
    lvl = min(level, 3)
    se.ENCOUNTERS.setdefault(lvl, {})["_test"] = list(names) if key.startswith("ref") else [f"{x}@{level}" for x in names]
    rows = party._rows()
    out = collections.Counter()
    for k in range(n):
        rec, _ = ds.play_day(pnames, swaps, lvl, ("_test",), seed + 1000 * k, rows)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["down"] += f["downs"] > 0
        out["wounded"] += bool(f["wounded"])
        out["rounds"] += f["rounds"]
        out["again_n"] += f["again_first"][0]
        out["again_d"] += f["again_first"][1]
    res = {k: out[k] / n for k in ("won", "down", "wounded", "rounds")}
    return dict(level=level, party=gname, key=key, enemies=list(names), n=n,
                again_n=out["again_n"], again_d=out["again_d"], **res)


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {(r["level"], r["party"], r["key"]) for r in map(json.loads, open(a.o)) if r}
    jobs = []
    for L in [int(x) for x in a.L.split(",")]:
        encs = {"|".join(e): e for e in encounters(L, a.k, a.seed)}
        encs.update(reference(L))
        groups = tc.groups(L, ps.MID[L])
        for gi, (gname, _, _) in enumerate(groups):
            for key, names in encs.items():
                if (L, gname, key) not in done:
                    jobs.append((L, gi, key, names, a.n, a.seed))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=4)):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
            if i % 200 == 0:
                print(i, flush=True)


def solve(X, y, ridge=1e-3):
    """Least squares with a little ridge, no numpy."""
    k = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) + (ridge if i == j else 0) for j in range(k)] for i in range(k)]
    b = [sum(r[i] * v for r, v in zip(X, y)) for i in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda i: abs(A[i][c]))
        A[c], A[p], b[c], b[p] = A[p], A[c], b[p], b[c]
        for i in range(k):
            if i != c and A[c][c]:
                f = A[i][c] / A[c][c]
                A[i] = [x - f * yv for x, yv in zip(A[i], A[c])]
                b[i] -= f * b[c]
    return [b[i] / A[i][i] for i in range(k)]


def read(a):
    recs = [json.loads(l) for l in open(a.o) if l.strip()]
    ms = monsters()
    names = sorted(ms)
    out = []
    for L in sorted({r["level"] for r in recs}):
        lv = [r for r in recs if r["level"] == L]
        man = [r for r in lv if not r["key"].startswith("ref")]
        ref = [r for r in lv if r["key"].startswith("ref")]
        line = lambda rs: (f"lose {100 * (1 - st.mean(r['won'] for r in rs)):4.1f}% Down {100 * st.mean(r['down'] for r in rs):3.0f}% "
                           f"Wnd {100 * st.mean(r['wounded'] for r in rs):3.0f}% rds {st.mean(r['rounds'] for r in rs):.1f} "
                           f"again {100 * sum(r['again_n'] for r in rs) / max(1, sum(r['again_d'] for r in rs)):3.0f}%")
        out.append(f"== Level {L}: manual {line(man)}" + (f"\n             old four mixes {line(ref)}" if ref else ""))
        by_party = collections.defaultdict(list)
        for r in man:
            by_party[r["party"]].append(r)
        for p, rs in sorted(by_party.items(), key=lambda kv: st.mean(r["won"] for r in kv[1])):
            out.append(f"   {p:42s} {line(rs)}")
        by_enc = collections.defaultdict(list)
        for r in man:
            by_enc[r["key"]].append(r)
        ranked = sorted(by_enc.items(), key=lambda kv: st.mean(r["down"] for r in kv[1]))
        out.append("   easiest: " + "; ".join(f"{k} (Down {100 * st.mean(r['down'] for r in v):.0f}%)" for k, v in ranked[:3]))
        out.append("   hardest: " + "; ".join(f"{k} (Down {100 * st.mean(r['down'] for r in v):.0f}%)" for k, v in ranked[-3:]))
    # Each monster's share: an encounter's reading (centered on its Level's
    # mean) against the share of its Slots each monster fills.
    for metric in ("down", "lose", "rounds"):
        X, y = [], []
        for L in sorted({r["level"] for r in recs}):
            man = [r for r in recs if r["level"] == L and not r["key"].startswith("ref")]
            val = (lambda r: 1 - r["won"]) if metric == "lose" else (lambda r: r[metric])
            mean = st.mean(val(r) for r in man)
            by_enc = collections.defaultdict(list)
            for r in man:
                by_enc[r["key"]].append(val(r))
            for key, vs in by_enc.items():
                share = collections.Counter()
                for n in key.split("|"):
                    share[n] += ms[n]["slots"] / PARTY_SLOTS
                X.append([share[n] for n in names])
                y.append(st.mean(vs) - mean)
        b = solve(X, y)
        scale = 1 if metric == "rounds" else 100
        unit = "rounds" if metric == "rounds" else "points"
        out.append(f"== A whole encounter of each monster against the average, {metric} ({unit}):")
        for n, v in sorted(zip(names, b), key=lambda t: -t[1]):
            out.append(f"   {n:20s} {scale * v:+6.1f}  ({sum(1 for row in X if row[names.index(n)] > 0)} encounters)")
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("-L", default="1,2,3,4,5")
    ap.add_argument("-k", type=int, default=40, help="encounters drawn per Level")
    ap.add_argument("-n", type=int, default=30, help="fights per encounter per party")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("--read", action="store_true")
    ap.add_argument("--txt", help="write the --read report here")
    a = ap.parse_args()
    read(a) if a.read else run(a)


if __name__ == "__main__":
    main()
