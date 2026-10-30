"""Two kinds of measure, side by side (2026-10-30).

Per the designer: is "Health left" (or "Health in the morning") the
right yardstick, when a bigger pool scores more just for being bigger?
Two families of measure, read on the same changes to one party:

- What it can take: the enemy Health multiplier at which the party wins
  half its fights (`fight x`), and half its days (`day x`), found by
  halving the interval on fixed fights with a curve fitted through
  every point tried (threshold.py). Reported as how much tougher
  the enemies can get than for the party as built (%). No resource is
  counted; Health, cards and healing only count through winning.
- What it spends: at each standard, how often it wins, how much Health
  it loses on a win (one fight, enemy Health x1.75), and how much is
  still missing the next morning on a won day (day_sim.py, x1.0).

Each change is to Hilde's party at Level 3 (Hilde, Carrick, Hanforth,
Beornhard), with its XP cost, so it can be read per XP.

    python3 measure_compare.py -n 150 --day-n 100
"""
import argparse
import math
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party, tunables as T  # noqa: E402
import technique_pass as tp  # noqa: E402
import day_sim  # noqa: E402
import build_optimizer as bo  # noqa: E402
import threshold  # noqa: E402

NAMES = ["Hilde (L3)", "Carrick (L3)", "Hanforth (L3)", "Beornhard (L3)"]
FIGHT_MULT, STEPS = 1.75, 8


def _b(name):
    return party.read_build(party._rows()[name]["Build"])


def edited(name, **edits):
    return name, party.apply_edits(_b(name), edits)


def added(name, tid, level):
    return name, party.fit(_b(name), add=[{"id": tid, "level": level}], free=True)[0]


def raised(name, key, n=1):
    b = _b(name)
    kind = "stats" if key in b["statPoints"] else "skills"
    pts = b["statPoints" if kind == "stats" else "skillPoints"]
    return name, party.apply_edits(b, {kind: {key: int(pts[key]) + n}})


def variants():
    hilde_bm = [t for t in _b("Hilde (L3)")["techniques"] if t["id"] == "T072"][0]
    return [
        ("as built", None),
        ("as built, other fights (noise)", "repeat"),
        ("2 Toughened Resolve, Hilde", ("Hilde (L3)", party.fit(_b("Hilde (L3)"), add=[
            {"id": "T019", "level": 3}, {"id": "T019", "level": 3}], free=True)[0])),
        ("2 Toughened Resolve, Beornhard", ("Beornhard (L3)", party.fit(_b("Beornhard (L3)"), add=[
            {"id": "T019", "level": 3}, {"id": "T019", "level": 3}], free=True)[0])),
        ("Toughened Body, Beornhard", added("Beornhard (L3)", "T014", 2)),
        ("+1 Body, Beornhard", raised("Beornhard (L3)", "Body")),
        ("+1 Essence, Hilde", raised("Hilde (L3)", "Essence")),
        ("+1 Acrobatics (her attack), Carrick", raised("Carrick (L3)", "Acrobatics")),
        ("another Lunging Maneuver, Hilde", edited("Hilde (L3)", add=[dict(hilde_bm)])),
        ("Lifeline, Hanforth", added("Hanforth (L3)", "T110", 2)),
        ("Hanforth without Healing Magic", edited("Hanforth (L3)", remove=[{"id": "T105", "copy": 1}])),
    ]


def xp_of(swap):
    if swap in (None, "repeat"):
        return 0
    name, b = swap
    return sum(party.xp_spent(b)) - sum(party.xp_spent(_b(name)))


def _fight(swap, mult, n):
    T.ENEMY_HEALTH_MULT = mult
    tp.LEVEL = 3
    tp.SEED = 7_000_000 if swap == "repeat" else 0
    if swap in (None, "repeat"):
        return tp.run(NAMES, None, None, n)[0]
    name, b = swap
    return tp.run(NAMES, name, {"build": b}, n, row_changes=bo.choices_for(party._rows()[name], b))[0]


def _day(swap, mult, n):
    day_sim.set_mult(mult)
    if swap in (None, "repeat"):
        return day_sim.run(NAMES, {}, 3, n, seed=7_000_000 if swap == "repeat" else 0)
    swaps = {swap[0]: ({"build": swap[1]}, bo.choices_for(party._rows()[swap[0]], swap[1]))}
    return day_sim.run(NAMES, swaps, 3, n)


def measure(args):
    label, swap, n, dn = args
    one = isinstance(swap, tuple)
    full = sum(p["max_health"] for p in (
        [party.make_pc(m, i, rows=party._rows(), edits={"build": swap[1]} if one and m == swap[0] else None,
                       row_changes=bo.choices_for(party._rows()[m], swap[1]) if one and m == swap[0] else None)
         for i, m in enumerate(NAMES, 1)]))
    f = _fight(swap, FIGHT_MULT, n)
    fw = [x for x in f if x[1]]
    d = _day(swap, 1.0, dn)
    dw = [r for r in d if not r["lost"]]
    out = dict(label=label, xp=xp_of(swap), full=full,
               fight_win=100 * len(fw) / len(f), fight_lost=st.mean(full - x[0] for x in fw),
               fight_left=st.mean(x[0] for x in f),
               day_win=100 * len(dw) / len(d), morning_short=st.mean(r["full"] - r["morning"] for r in dw),
               morning=st.mean(r["morning"] for r in d))
    out["fight_x"] = threshold.find(lambda m: _wins([x[1] for x in _fight(swap, m, n)]), 1.0, 6.0, STEPS)[0]
    out["day_x"] = threshold.find(lambda m: _wins([not r["lost"] for r in _day(swap, m, dn)]), 0.5, 4.0, STEPS)[0]
    return out


def _wins(won):
    return sum(won), len(won)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=150, help="fights per mix")
    ap.add_argument("--day-n", type=int, default=100, help="days per first mix")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    day_sim.set_mult(1.0)
    vs = variants()
    with mp.Pool(a.j) as pool:
        res = pool.map(measure, [(lab, sw, a.n, a.day_n) for lab, sw in vs])
    base = res[0]
    print(f"Hilde's party, Level 3. One fight at x{FIGHT_MULT}, n={a.n} a mix; a day at x1.0, n={a.day_n} a mix. "
          f"Thresholds: the enemy Health multiplier for half the fights / days won ({STEPS} halvings, "
          "a curve through every point).\n")
    print("| Change | XP | Max Health | Fight: toughest x (vs as built) | Day: toughest x (vs as built) | "
          "Fight wins | Health lost on a win | Day wins | Missing next morning | Health left (old score) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in res:
        fx = 100 * (r["fight_x"] / base["fight_x"] - 1)
        dx = 100 * (r["day_x"] / base["day_x"] - 1)
        print(f"| {r['label']} | {r['xp']:+d} | {r['full']} | x{r['fight_x']:.2f} ({fx:+.0f}%) | x{r['day_x']:.2f} ({dx:+.0f}%) | "
              f"{r['fight_win']:.0f}% | {r['fight_lost']:.1f} | {r['day_win']:.0f}% | {r['morning_short']:.1f} | "
              f"{r['fight_left']:.1f} |", flush=True)


if __name__ == "__main__":
    main()
