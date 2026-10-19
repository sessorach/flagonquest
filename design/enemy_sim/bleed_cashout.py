"""Bleeding cash-outs (2026-10-16).

Per the designer: Bleeding ticks off half its stacks, rounded up, and a
few techniques cash in the stacks like War Magic's Reign of Blood (F073:
"remove up to [twice X] + [Clubs] stacks of Bleeding from the target,
and they lose that much Health"). One party of Hilde, Felix, Jackal and
Beornhard, four ways:

- base:  the real builds
- bleed: the Bleeding builds (Furious Rage, Battering, Acidic Flasks,
         Sanguine)
- cash:  Hilde and Jackal apply (Furious Rage, Acidic Flasks); Felix's
         Battle Maneuver has Open the Wound x3 (Reign of Blood's text as a
         Maneuver Feature) and Beornhard's Level 2 War Magic has Reign of
         Blood x2
- yard:  the same appliers, with the cash-outs' points spent on straight
         damage or the real build instead (Felix's Half Guard x3,
         Beornhard's Destructive x2)
- cashB / cashF: the yardstick with only Beornhard's / only Felix's
         cash-out swapped in; battF the yardstick with Felix's Battering

    python3 bleed_cashout.py               # every rule, x1 and x1.75 Health
    python3 bleed_cashout.py -n 100 -m 1"""
import argparse
import math
import os
import statistics as st
import sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T

PARTIES = {
    "base": ["Hilde", "Felix", "Jackal", "Beornhard"],
    "bleed": ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"],
    "cash": ["Hilde (Bleed)", "Felix (Cash)", "Jackal (Bleed)", "Beornhard (Cash)"],
    "yard": ["Hilde (Bleed)", "Felix", "Jackal (Bleed)", "Beornhard (Destr)"],
    # One cash-out at a time, against the yardstick party.
    "cashB": ["Hilde (Bleed)", "Felix", "Jackal (Bleed)", "Beornhard (Cash)"],
    "cashF": ["Hilde (Bleed)", "Felix (Cash)", "Jackal (Bleed)", "Beornhard (Destr)"],
    "battF": ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Destr)"],
}
RULES = {
    "as written": {},
    "tick half": {"BLEED_TICK": 'half'},
    "tick half + execute x1/2": {"BLEED_TICK": 'half', "BLEED_OUT": 'x1/2'},
}
# These tables were made (2026-10-16) under the rule then: one stack a
# tick, straight through Protected. Pinned, so they still reproduce now
# that the defaults follow the 2026-10-19 rule.
BASE = {"BLEED_TICK": 1, "BLEED_PROTECTED": 'through'}
DEFAULTS = {**{k: getattr(T, k) for rule in RULES.values() for k in rule}, **BASE}


def encounter(mix, mult):
    en = se.build_encounter(se.ENCOUNTERS[1][mix])
    for e in en:
        e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
    return en


def one(job):
    rule, pname, n, mult = job
    for k, v in {**DEFAULTS, **RULES[rule]}.items():
        setattr(T, k, v)
    names = PARTIES[pname]
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    R = [cs.run_fight(1, 1, movement=True, enemies=encounter(mix, mult), seed=100_000 * mi + k)
         for mi, mix in enumerate(se.CURRENT_MIXES) for k in range(n)]
    m = lambda key: st.mean(r.get(key, 0) for r in R)
    return (rule, pname, mult), (f"{m('rounds'):.2f} rounds | loses {100 * st.mean(r['winner'] != 'party' for r in R):.1f}% | "
                                 f"Down {100 * m('pc_downed'):.0f}% | Bleeding {m('bleed_dealt'):.2f} | cashed {m('cashed'):.2f} | "
                                 f"bled out {m('executes'):.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=300, help="fights per mix")
    ap.add_argument("-m", type=float, action="append", help="enemy Health multiplier(s); default 1 and 1.75")
    ap.add_argument("-r", action="append", help="rule name(s); default all")
    ap.add_argument("-p", action="append", help="party name(s); default all")
    a = ap.parse_args()
    mults = a.m or [1.0, 1.75]
    rules, parties = a.r or list(RULES), a.p or list(PARTIES)
    jobs = [(r, p, a.n, m) for m in mults for r in rules for p in parties]
    with Pool() as pool:
        res = dict(pool.map(one, jobs))
    for m in mults:
        print(f"== enemy Health x{m}")
        for r in rules:
            print(f"-- {r}")
            for p in parties:
                print(f"   {p:5}: {res[(r, p, m)]}")
