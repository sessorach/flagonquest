"""Enemy stat progressions closer to the PCs' (2026-11-03).

The designer: can enemies get 4-5 round fights and the right challenge
without so much Health, with numbers closer to what PCs end up with?
Each config is a set of nudges on top of the v2 table (stat_sweep.py's
syntax, "1/2/3/4/5:res=2,hpx=0.6,dmg=1"), played in the middle of every
Level's XP band (table_check.py's parties: Level 1 the sample parties,
2-3 the normalized ones, 4-5 the Level 3 characters grown), under the day
standard. Results append to a jsonl as each config finishes, and a rerun
skips the configs already there, so a container restart costs one config.

    python3 experiments/enemies/progression_sweep.py -o results/enemy_stats/progressions.jsonl \\
        "v2=" "res+2 hp x0.6=1/2/3/4/5:res=2,hpx=0.6"
    python3 experiments/enemies/progression_sweep.py --grid -o ...   # the built-in first grid

Each line also gives the enemies' average numbers at Level 3 (Health per
full-size enemy, Resist, Damage) so they read next to the PCs'.
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import sample_enemies as se  # noqa: E402
import tunables as T  # noqa: E402
import stat_sweep  # noqa: E402
import table_check as tc  # noqa: E402

TABLE = ["v2"]
MID = {1: None, 2: 105, 3: 145, 4: 185, 5: 225}


def grid():
    out = []
    for res, hpx, dmg in itertools.product((0, 1, 2), (1.0, 0.8, 0.65, 0.5), (0, 1)):
        spec = f"1/2/3/4/5:res={res},hpx={hpx},dmg={dmg}"
        out.append((f"res+{res} hpx{hpx} dmg+{dmg}", spec))
    return out


def grid2():
    out = []
    for res, hpx, dmg, acc in itertools.product((1, 2), (0.55, 0.65, 0.75), (0, 1), (0, 1)):
        out.append((f"res+{res} hpx{hpx} dmg+{dmg} acc+{acc}",
                    f"1/2/3/4/5:res={res},hpx={hpx},dmg={dmg},acc={acc}"))
    return out


def enemy_numbers(spec, level=3):
    """Average full-size enemy in the four mixes at `level` under `spec`."""
    stat_sweep.install(stat_sweep.parse(spec))
    T.ENEMY_LEVEL_UP = 0
    T.ENEMY_TABLE = TABLE[0]
    es = [e for m in se.CURRENT_MIXES for e in se.build_encounter(se.ENCOUNTERS[level][m]) if e.get("slots", 1) >= 1]
    dmg = [p["attack_damage"] for e in es for p in (e, e.get("backup")) if p and p.get("attack_damage")][:len(es)]
    return dict(health=st.mean(e["max_health"] for e in es), physres=st.mean(e["physres"] for e in es),
                elemres=st.mean(e["elemres"] for e in es), damage=st.mean(dmg),
                accuracy=st.mean(e["accuracy"] for e in es))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("configs", nargs="*", help="label=spec")
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--grid2", action="store_true", help="res 1-2 x Health 0.55-0.75 x Damage x Accuracy")
    ap.add_argument("-n", type=int, default=60, help="days per mix per party")
    ap.add_argument("--points", default="mid", choices=("mid", "all"))
    ap.add_argument("--table", default="v2", help="tunables.ENEMY_TABLE to play (v2, v3)")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    TABLE[0] = a.table
    configs = [tuple(c.split("=", 1)) for c in a.configs] + (grid() if a.grid else []) + (grid2() if a.grid2 else [])
    done = set()
    if os.path.exists(a.o):
        done = {(json.loads(l)["label"], json.loads(l)["points"]) for l in open(a.o) if l.strip()}
    with mp.Pool(a.j) as pool:
        for label, spec in configs:
            label = label if a.table == "v2" else f"{a.table} {label}"
            if (label, a.points) in done:
                continue
            pts = [(L, MID[L]) for L in range(1, 6)] if a.points == "mid" else \
                [(L, b) for L in range(1, 6) for b in tc.POINTS[L]]
            jobs = [(a.table, L, b, gi, a.n, 0, False, spec) for L, b in pts for gi in range(len(tc.groups(L, b)))]
            res = {}
            for t, L, b, g, days in pool.imap(tc._job, jobs):
                res.setdefault((L, b), {})[g] = days
            rows = {}
            for (L, b), by in sorted(res.items(), key=lambda kv: (kv[0][0], kv[0][1] or 0)):
                s = tc.summarize(by)
                rows[f"{L}:{b}"] = s
                f1 = s[1]
                print(f"{label:30s} L{L} {str(tc.COMPOSITE.get(b, 75)):>3s} days {s['day']:5.1f} "
                      f"(worst {s['worst']:3.0f}) Down {f1['down']:3.0f} Wnd {f1['wounded']:3.0f} "
                      f"rds {f1['rounds']:.1f} again {f1['again']:2.0f}", flush=True)
            nums = enemy_numbers(spec)
            print(f"{label:30s} L3 enemy: Health {nums['health']:.1f} Resist {nums['physres']:.1f}/{nums['elemres']:.1f} "
                  f"Damage {nums['damage']:.1f} Accuracy {nums['accuracy']:.1f}", flush=True)
            with open(a.o, "a") as f:
                f.write(json.dumps(dict(label=label, spec=spec, points=a.points, n=a.n, rows=rows,
                                        enemy_l3=nums)) + "\n")


if __name__ == "__main__":
    main()
