"""Standard checks for the day measure (2026-10-29): a few plain swaps,
each scored two ways at enemy Health x1.0, so the two can be compared:

- one fight: party Health left (losses 0), technique_pass's setup;
- a day (day_sim.py): party Health the next morning (losses 0), and
  how many days in a row before a fight is lost (up to ten).

Every reading is paired against the same party as built, on the same
fights. "repeat" is the as-built party on other fights: the noise floor.

    python3 day_checks.py -n 250          # every check
    python3 day_checks.py -n 100 --only "+1 Body"
"""
import argparse
import math
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import day_sim as ds, party, tunables as T  # noqa: E402
import technique_pass as tp  # noqa: E402

H = ["Hilde (L3)", "Carrick (L3)", "Hanforth (L3)", "Beornhard (L3)"]
S = ["Enith (L3, proposed)", "Felix (L3, proposed)", "Jackal (L3)", "Hanforth (L3)"]


def plus(name, stat, n=1):
    b = party.read_build(party._rows()[name]["Build"])
    return {"stats": {stat: int(b["statPoints"][stat]) + n}}


def free_add(name, tid, level):
    b = party.read_build(party._rows()[name]["Build"])
    return {"build": party.fit(b, add=[{"id": tid, "level": level}], free=True)[0]}


# (label, party, who, edits or None, day_sim switches)
CHECKS = [
    ("repeat (other fights)", H, None, None, {"seed": 7_000_000}),
    ("nobody heals after fights", H, None, None, {"care": False}),
    ("Carrick without Patch Up", H, "Carrick (L3)", {"remove": [{"id": "T036", "copy": 1}]}, {}),
    ("+1 Body, Beornhard", H, "Beornhard (L3)", lambda: plus("Beornhard (L3)", "Body"), {}),
    ("+1 Body, Hilde", H, "Hilde (L3)", lambda: plus("Hilde (L3)", "Body"), {}),
    ("+1 Body, Hanforth", H, "Hanforth (L3)", lambda: plus("Hanforth (L3)", "Body"), {}),
    ("Toughened Body, Beornhard", H, "Beornhard (L3)", lambda: free_add("Beornhard (L3)", "T014", 2), {}),
    ("Lifeline, Hanforth", H, "Hanforth (L3)", lambda: free_add("Hanforth (L3)", "T110", 2), {}),
    ("Hanforth without Healing Magic", H, "Hanforth (L3)", {"remove": [{"id": "T105", "copy": 1}]}, {}),
    ("+1 Body, Hanforth (Enith's party)", S, "Hanforth (L3)", lambda: plus("Hanforth (L3)", "Body"), {}),
]


def _fight_job(args):
    names, who, edits, n = args
    T.ENEMY_HEALTH_MULT = ds.MULT
    tp.LEVEL = 3
    return tp.run(names, who, edits, n)[0]


def _ci(d):
    return st.mean(d), 1.96 * st.stdev(d) / math.sqrt(len(d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=250, help="fights and days per first mix")
    ap.add_argument("--days-n", type=int, default=100, help="ten-day runs per first mix")
    ap.add_argument("--only")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    ds.set_mult(ds.MULT)
    checks = [c for c in CHECKS if not a.only or a.only in c[0]]
    print(f"Level 3, enemy Health x{ds.MULT}; one fight and a day: n={a.n} a mix; ten days: n={a.days_n} a mix")
    print("| Check | One fight: Health left | A day: morning Health | Days won | Ten days in a row: days |")
    print("|---|---|---|---|---|")
    with mp.Pool(a.j) as pool:
        bases = {}
        for label, names, who, edits, sw in checks:
            key = tuple(names)
            if key not in bases:
                bases[key] = (pool.apply(_fight_job, ((names, None, None, a.n),)),
                              ds.run(names, {}, 3, a.n, pool=pool),
                              ds.run(names, {}, 3, a.days_n, days=10, pool=pool))
            fb, db, tb = bases[key]
            e = edits() if callable(edits) else edits
            seed = sw.get("seed", 0)
            ds.CARE = sw.get("care", True)
            swaps = {who: (e, None)} if who else {}
            if seed:
                fv = None
                dv = ds.run(names, swaps, 3, a.n, seed=seed, pool=pool)
                tv = ds.run(names, swaps, 3, a.days_n, days=10, seed=seed, pool=pool)
            else:
                fv = pool.apply(_fight_job, ((names, who, e, a.n),)) if who else None
                dv = ds.run(names, swaps, 3, a.n, pool=pool)
                tv = ds.run(names, swaps, 3, a.days_n, days=10, pool=pool)
            ds.CARE = True
            f = "{:+.2f} ± {:.2f}".format(*tp.paired(fb, fv)[:2]) if fv else "-"
            d = "{:+.2f} ± {:.2f}".format(*_ci([v["morning"] - b["morning"] for b, v in zip(db, dv)]))
            won = 100 * (sum(not r["lost"] for r in dv) - sum(not r["lost"] for r in db)) / len(db)
            t = "{:+.2f} ± {:.2f}".format(*_ci([v["days"] - b["days"] for b, v in zip(tb, tv)]))
            print(f"| {label} | {f} | {d} | {won:+.1f} pts | {t} |", flush=True)
        for key, (fb, db, tb) in bases.items():
            s = ds.summary(db)
            print(f"\nAs built ({', '.join(n.split(' (')[0] for n in key)}): one fight "
                  f"{st.mean(r[0] for r in fb):.2f} Health left; days won {s['won']:.1f}%, morning "
                  f"{s['morning']:.2f} of {s['full']:.0f}; ten days: {st.mean(r['days'] for r in tb):.2f} days")


if __name__ == "__main__":
    main()
