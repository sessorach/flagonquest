"""Tune the pruned v3's budget by Level (2026-11-04).

The designer: the Ability budget is the lever. If a Level's enemies come
out weak against what the players get there, give them a few more points
and let each spend them on its main thing (sample_enemies.csv's
PrunedExtra, in order). Each config is extra points by Level on top of
tunables.V3_PRUNED_ALLOWANCE, played in the middle of every Level's band
as table_check.py does (day standard). One jsonl line per config; a rerun
skips the ones already there.

    python3 experiments/enemies/pruned_tune.py -o results/enemy_stats/v3p_tune.jsonl "L3-5 +2=3:2/4:2/5:2"
"""
import argparse
import json
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402


def parse(spec):
    return {int(L): int(n) for L, n in (x.split(":") for x in spec.split("/") if x)}


def _job(args):
    extra, rest = args
    T.V3_VERSION = 3
    T.V3_PRUNED_ROSTER = "picks"
    T.V3_PRUNED_EXTRA = extra
    return tc._job(rest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("configs", nargs="+", help="label=L:n/L:n (extra points by Level)")
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("-L", default="1,2,3,4,5")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    levels = [int(x) for x in a.L.split(",")]
    done = set()
    if os.path.exists(a.o):
        done = {json.loads(l)["label"] for l in open(a.o) if l.strip()}
    with mp.Pool(a.j, maxtasksperchild=1) as pool:
        for c in a.configs:
            label, _, spec = c.partition("=")
            if label in done:
                continue
            extra = parse(spec)
            jobs = [(extra, ("v3", L, ps.MID[L], gi, a.n, 0, False, ""))
                    for L in levels for gi in range(len(tc.groups(L, ps.MID[L])))]
            res = {}
            for t, L, b, g, days in pool.imap(_job, jobs):
                res.setdefault((L, b), {})[g] = days
            rows = {}
            for (L, b), by in sorted(res.items()):
                s = tc.summarize(by)
                rows[f"{L}:{b}"] = s
                f1 = s[1]
                print(f"{label:28s} L{L} days {s['day']:5.1f} (worst {s['worst']:3.0f}) Down {f1['down']:3.0f} "
                      f"Wnd {f1['wounded']:3.0f} rds {f1['rounds']:.1f} again {f1['again']:2.0f}", flush=True)
            with open(a.o, "a") as f:
                f.write(json.dumps(dict(label=label, extra=extra, n=a.n, rows=rows)) + "\n")


if __name__ == "__main__":
    main()
