"""How much of an enemy's budget can go into on-hit debuffs (2026-11-04).

The designer: enemies should apply debuffs and have mechanics as a
standard thing, not be pure Health sponges; pull some other power budget
back to fit them in and see how much each Level can bear before the
missing stats distort the fights. Every full-size enemy in the four mixes
(not the minions) gets a package of on-hit Abilities on top of its own,
priced in Health as usual (enemy_builder_pcstyle.ABILITY_HEALTH_V3), or
paid for from another stat instead (the allowance goes up by the package's
price and the stat comes down). The Health floor is off so the ladder can
run past what a GM could build. Played in the middle of each Level's band
as table_check.py does (day standard), one jsonl line per config, rerun
skips the configs already there.

    python3 experiments/enemies/debuff_budget.py -o results/enemy_stats/debuff_budget.jsonl
"""
import argparse
import json
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401
import sample_enemies as se  # noqa: E402
import tunables as T  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

FREE = ["Strike (Crippling)", "Strike (Slowing)"]
LADDER = [  # cumulative, by price in Health
    ("Strike (Necrotic)",),
    ("Strike (Harrying)",),
    ("Poison (Necrotic)",),
    ("Poison (Bleeding)",),
    ("Strike (Battering)",),
]


def package(k):
    """The free riders plus the ladder's first Abilities up to k Health."""
    out, spent = list(FREE), 0
    for step in LADDER:
        cost = sum(eb.ABILITY_HEALTH_V3[a] for a in step)
        if spent + cost > k:
            break
        out += step
        spent += cost
    assert spent == k, (k, spent)
    return out


# (label, abilities added, paid by: "health" or a stat_sweep nudge spec)
CONFIGS = [("as built", None, "health")] + \
    [(f"debuffs, {k} Health", package(k), "health") for k in (0, 1, 2, 3, 6, 8)] + [
    ("debuffs 2, Damage -1", package(2), "1/2/3/4/5:dmg=-1"),
    ("debuffs 2, Accuracy -1 Resist -1", package(2), "1/2/3/4/5:acc=-1,res=-1"),
    ("debuffs 3, Damage -1 Accuracy -1", package(3), "1/2/3/4/5:dmg=-1,acc=-1"),
]


def install(adds, paid):
    T.V3_HEALTH_FLOOR = 0
    if adds is None:
        return
    import stat_sweep
    get_row = se.__dict__.setdefault("_orig_row_named", se._row_named)
    get_enemy = se.__dict__.setdefault("_orig_get_enemy", se.get_enemy)
    nudges = stat_sweep.parse(paid) if paid != "health" else {}

    def row_named(name):
        row = get_row(name)
        if row is None or float(row["Slots"]) < 1:
            return row
        have = [a.strip() for a in row["Abilities"].split(";") if a.strip()]
        return dict(row, Abilities="; ".join(have + [a for a in adds if a not in have]),
                    _added=[a for a in adds if a not in have])

    def enemy(name):
        e = get_enemy(name)
        if nudges and e.get("slots", 1) >= 1:
            # Paid for by a stat instead: the package's Health goes back on
            # (full-size enemies are all 1 Slot here), the stat comes down.
            new = row_named(name)["_added"]
            e["health"] = e["max_health"] = e["max_health"] + sum(eb.ABILITY_HEALTH_V3[a] for a in new)
            stat_sweep.nudge(e, nudges[e["level"]])
        return e
    se._row_named = row_named
    se.get_enemy = enemy


def _job(args):
    adds, paid, rest = args
    install(adds, paid)
    return tc._job(rest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.o):
        done = {json.loads(l)["label"] for l in open(a.o) if l.strip()}
    with mp.Pool(a.j, maxtasksperchild=1) as pool:
        for label, adds, paid in CONFIGS:
            if label in done:
                continue
            nudge = ""
            pts = [(L, ps.MID[L]) for L in range(1, 6)]
            jobs = [(adds, paid, ("v3", L, b, gi, a.n, 0, False, nudge))
                    for L, b in pts for gi in range(len(tc.groups(L, b)))]
            res = {}
            for t, L, b, g, days in pool.imap(_job, jobs):
                res.setdefault((L, b), {})[g] = days
            rows = {}
            for (L, b), by in sorted(res.items()):
                s = tc.summarize(by)
                rows[f"{L}:{b}"] = s
                f1 = s[1]
                print(f"{label:36s} L{L} days {s['day']:5.1f} (worst {s['worst']:3.0f}) Down {f1['down']:3.0f} "
                      f"Wnd {f1['wounded']:3.0f} rds {f1['rounds']:.1f} again {f1['again']:2.0f}", flush=True)
            with open(a.o, "a") as f:
                f.write(json.dumps(dict(label=label, adds=adds, paid=paid, n=a.n, rows=rows)) + "\n")


if __name__ == "__main__":
    main()
