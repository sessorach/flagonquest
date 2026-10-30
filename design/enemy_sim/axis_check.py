"""Does the yardstick favor durability? (2026-10-30)

The headline measure (threshold.py) makes enemies tougher by giving them
more Health. That keeps every enemy hit at its normal size, which is
exactly where flat Resist does the most. Per the designer's question
(why Essence and max-Health Techniques rank so high), this reads the
same changes to Hilde's party (Level 3, a day: day_sim.py) along three
ways of making the day harder:

- health: enemy Health x m (the headline; the toughest m at 50% days
  won). Hits stay their normal size, the best case for flat Resist.
- damage: every enemy attack +a damage (the toughest a). Each point of
  Resist covers less of a bigger hit, the worst case for it.

Damage comes in whole steps, so it's read at every step in a range and
a curve fitted through them (threshold.grid). A change that ranks high
on both is strong whatever "harder" means; one that ranks high on only
one is leaning on the yardstick. (Enemy accuracy was tried and dropped:
days won level off near 50% even at +8 to hit, since an enemy that never
misses still doesn't win the day by itself, so there's no 50% point to
find.)

`--no-tr-shallow` variants play Toughened Resolve's Health as all Deep
(its setup's +2 Shallow skipped), so it can't put off Wounded: what's
left is the pool alone.

    python3 axis_check.py -n 100
"""
import argparse
import multiprocessing as mp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party, tunables as T  # noqa: E402
import day_sim  # noqa: E402
import threshold  # noqa: E402
import techniques  # noqa: E402
import build_optimizer as bo  # noqa: E402
import measure_compare as mc  # noqa: E402

AXES = ("health", "damage")
DAMAGE_STEPS = range(-1, 7)
ACCURACY_STEPS = range(-2, 9)


def two_tr(name):
    return name, party.fit(mc._b(name), add=[{"id": "T019", "level": 3}, {"id": "T019", "level": 3}], free=True)[0]


def variants():
    tr_h = two_tr("Hilde (L3)")
    return [
        ("as built", None, {}),
        ("+1 Essence, Hilde", mc.raised("Hilde (L3)", "Essence"), {}),
        ("+1 Essence, Beornhard", mc.raised("Beornhard (L3)", "Essence"), {}),
        ("+1 Agility, Hilde", mc.raised("Hilde (L3)", "Agility"), {}),
        ("+1 Agility, Carrick", mc.raised("Carrick (L3)", "Agility"), {}),
        ("+1 Acrobatics (her attack), Carrick", mc.raised("Carrick (L3)", "Acrobatics"), {}),
        ("2 Toughened Resolve, Hilde", tr_h, {}),
        ("2 Toughened Resolve, Hilde, Health as Deep only", tr_h, {"no_tr_shallow": True}),
        ("2 Toughened Resolve, Beornhard", two_tr("Beornhard (L3)"), {}),
        ("Toughened Body, Beornhard", mc.added("Beornhard (L3)", "T014", 2), {}),
        ("+1 Body, Beornhard", mc.raised("Beornhard (L3)", "Body"), {}),
        ("Lifeline, Hanforth", mc.added("Hanforth (L3)", "T110", 2), {}),
        ("Hanforth without Healing Magic", mc.edited("Hanforth (L3)", remove=[{"id": "T105", "copy": 1}]), {}),
    ]


def _wins(swap, n, health=1.0, damage=0, accuracy=0):
    T.ENEMY_DAMAGE_ADJ, T.ENEMY_ACCURACY_ADJ = damage, accuracy
    day_sim.set_mult(health)
    rows = party._rows()
    swaps = {} if swap is None else {swap[0]: ({"build": swap[1]}, bo.choices_for(rows[swap[0]], swap[1]))}
    try:
        recs = day_sim.run(mc.NAMES, swaps, 3, n)
    finally:
        T.ENEMY_DAMAGE_ADJ = T.ENEMY_ACCURACY_ADJ = 0
    return sum(not r["lost"] for r in recs), len(recs)


def job(args):
    label, swap, opts, axis, n = args
    saved = techniques.SETUP.get("Toughened Resolve")
    if opts.get("no_tr_shallow"):
        # Toughened Resolve's setup only moves where Wounded starts (+2
        # Shallow); its +4 Health is already in the total. Skipping it
        # leaves the pool and takes away the Wounded buffer.
        techniques.SETUP.pop("Toughened Resolve", None)
    try:
        if axis == "health":
            x, pts = threshold.find(lambda m: _wins(swap, n, health=m), 0.5, 4.0)
        elif axis == "damage":
            x, pts = threshold.grid(lambda a: _wins(swap, n, damage=a), DAMAGE_STEPS)
        else:
            x, pts = threshold.grid(lambda a: _wins(swap, n, accuracy=a), ACCURACY_STEPS)
    finally:
        if saved is not None:
            techniques.SETUP["Toughened Resolve"] = saved
    return label, axis, x, pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=100, help="days per first-fight mix, per reading")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    vs = variants()
    jobs = [(lab, sw, opts, axis, a.n) for lab, sw, opts in vs for axis in AXES]
    with mp.Pool(a.j) as pool:
        res = pool.map(job, jobs, chunksize=1)
    got = {(lab, axis): x for lab, axis, x, _ in res}
    base = {axis: got[("as built", axis)] for axis in AXES}
    print(f"Hilde's party, Level 3, a day (day_sim.py), {4 * a.n} days a reading. The toughest day it wins half "
          f"the time, made harder three ways, and the change against the party as built.\n")
    print("| Change | XP | Enemy Health x (change) | Enemy damage +a per hit (change) |")
    print("|---|---|---|---|")
    for lab, sw, opts in vs:
        xp = mc.xp_of(sw)
        h, d = (got[(lab, ax)] for ax in AXES)
        hp = f"x{h:.2f} ({100 * (h / base['health'] - 1):+.0f}%)"
        dp = "-" if d is None else f"+{d:.2f} ({d - base['damage']:+.2f})"
        print(f"| {lab} | {xp:+d} | {hp} | {dp} |", flush=True)


if __name__ == "__main__":
    main()
