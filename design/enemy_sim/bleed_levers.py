"""Bleeding levers side by side (2026-10-16).

Per the designer: move the levers Bleeding has (the execute threshold,
how many stacks a tick takes off, and anything else that might work) and
see which gets it near its goal, about one extra point a fight that feels
effective without being as good as straight damage.

One carrier at a time in Party A, Level 1, the standard four mixes. For
each rule, the extra points that land on live Health per fight from the
test passives (Bleeding Once: 1 stack on the first hit; Bleeding Strikes:
1 stack on every hit or Parry; Bleeding Strikes 2: 2 stacks; Bleeding
Dump: 5 stacks on the first hit), and their straight-damage twins under
the same rule (+1 on the first hit, +1 on every hit, +5 on the first
hit).

    python3 bleed_levers.py                 # every rule in RULES
    python3 bleed_levers.py -n 100 -r tick2 # one rule, fewer fights
    python3 bleed_levers.py -m 1.75         # every enemy's Health x1.75

The multiplier is for checking against the designer's table, where a hit
enemy acts again about half the time (TABLE_PLAY_NOTES.md, open question
4): the sim's Level 1 fights give 21% as built, 53% at x1.75."""
import argparse
import math
import os
import statistics as st
import sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tunables as T
from turnorder_single import build

PARTY = ["Hilde", "Browndog", "Carrick", "Sable"]
CARRIERS = ("Hilde", "Sable")
TESTS = ("Bleeding Once", "Bleeding Strikes", "Bleeding Strikes 2", "Bleeding Dump",
         "Damage Once", "Plus One Damage", "Damage Dump")
# Bleeding test -> its straight-damage twin (Strikes 2 has none).
TWIN = {"Bleeding Once": "Damage Once", "Bleeding Strikes": "Plus One Damage", "Bleeding Dump": "Damage Dump"}

RULES = {
    "as written": {},
    "tick2": {"BLEED_TICK": 2},
    "tick3": {"BLEED_TICK": 3},
    "tick half": {"BLEED_TICK": 'half'},
    "tick all": {"BLEED_TICK": 'all'},
    "execute x1/2": {"BLEED_OUT": 'x1/2'},
    "execute x1/3": {"BLEED_OUT": 'x1/3'},
    "tick2 + execute x1/2": {"BLEED_TICK": 2, "BLEED_OUT": 'x1/2'},
    "tick2 + execute x1/3": {"BLEED_TICK": 2, "BLEED_OUT": 'x1/3'},
    "tick3 + execute x1/2": {"BLEED_TICK": 3, "BLEED_OUT": 'x1/2'},
    "wound +1": {"BLEED_WOUND": 1},
    "wound +1 + execute x1/2": {"BLEED_WOUND": 1, "BLEED_OUT": 'x1/2'},
}
# Pool workers run many jobs, so each one starts from the defaults.
DEFAULTS = {k: getattr(T, k) for rule in RULES.values() for k in rule}


def encounter(mix, mult):
    en = se.build_encounter(se.ENCOUNTERS[1][mix])
    for e in en:
        e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
    return en


def one(job):
    rule, carrier, test, n, mult = job
    for k, v in {**DEFAULTS, **RULES[rule]}.items():
        setattr(T, k, v)
    cs.make_party = lambda t, good_luck=0: build(carrier, test, 0, party_names=PARTY)
    pts = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(n):
            r = cs.run_fight(1, 1, movement=True, enemies=encounter(mix, mult),
                             seed=100_000 * mi + k)
            pts.append(r.get("bleed_dealt", 0) + r.get("plus_one_dealt", 0))
    return (rule, carrier, test), st.mean(pts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=300, help="fights per mix")
    ap.add_argument("-r", action="append", help="rule name(s) from RULES; default all")
    ap.add_argument("-m", type=float, default=1.0, help="enemy Health multiplier")
    a = ap.parse_args()
    rules = a.r or list(RULES)
    jobs = [(r, c, t, a.n, a.m) for r in rules for c in CARRIERS for t in TESTS]
    with Pool() as pool:
        res = dict(pool.map(one, jobs))
    print("| Rule | 1 stack, first hit | 1 stack every hit or Parry | 2 stacks every hit or Parry | 5 stacks, first hit |")
    print("|---|---|---|---|---|")
    for r in rules:
        cells = []
        for t in TESTS[:4]:
            v = [res[(r, c, t)] for c in CARRIERS]
            cell = " / ".join(f"{x:.2f}" for x in v)
            if t in TWIN:
                cell += " (" + " / ".join(f"{100 * x / res[(r, c, TWIN[t])]:.0f}%" for x, c in zip(v, CARRIERS)) + ")"
            cells.append(cell)
        print(f"| {r} | " + " | ".join(cells) + " |", flush=True)
    print("\nStraight-damage twins (+1 first hit / +1 every hit / +5 first hit), Hilde / Sable:")
    for r in rules:
        print(f"  {r}: " + " | ".join(" / ".join(f"{res[(r, c, t)]:.2f}" for c in CARRIERS) for t in TESTS[4:]))
