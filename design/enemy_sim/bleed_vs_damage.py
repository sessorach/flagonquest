"""Bleeding against a plain +1 damage, measured the same way (2026-10-07).

THE TABEL prices damage nominally: +1 damage on a hit is a point of
Health off the target, whether or not that point turns out to matter.
In the sim many don't - the hit was going to kill anyway (overkill). A
Bleeding stack has the same problem plus one more (its target has to
live to the end of its own turn). So the fair price for a stack is the
nominal damage rate times (how often a stack lands) / (how often a +1 on
a hit lands). This measures both for each Party A carrier.

Usage: python3 bleed_vs_damage.py [health multiplier] [Level]
(Level 1 uses the Level 1 Party A and Level 1 encounters, 2026-10-08.)"""
import os
import sys
import math
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se
from turnorder_single import build

TRIALS = 400
PARTY_BY_LEVEL = {2: ["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"],
                  1: ["Hilde", "Browndog", "Carrick", "Sable"]}
LEVEL = int(sys.argv[2]) if len(sys.argv) > 2 else 2
CARRIERS = PARTY_BY_LEVEL[LEVEL]


def enc(mix, mult):
    en = se.build_encounter(se.ENCOUNTERS[LEVEL][mix])
    for e in en:
        e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
    return en


if __name__ == "__main__":
    mult = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    once_land = once_n = p1_land = p1_n = 0
    for c in CARRIERS:
        for test in ("Bleeding Once", "Plus One Damage"):
            for mi, mix in enumerate(se.CURRENT_MIXES):
                for k in range(TRIALS):
                    holder = {}
                    def mk(t, good_luck=0, c=c, test=test):
                        holder['pcs'] = build(c, test, 0, party_names=CARRIERS)
                        return holder['pcs']
                    cs.make_party = mk
                    r = cs.run_fight(1, LEVEL, movement=True, enemies=enc(mix, mult), seed=100_000 * mi + k)
                    pc = [p for p in holder['pcs'] if test in p.get('passives', ())][0]
                    if test == "Bleeding Once":
                        if pc.get('once_applied'):
                            once_n += 1
                            once_land += r.get('bleed_dealt', 0)
                    else:
                        p1_n += pc.get('p1_hits', 0)
                        p1_land += pc.get('extra_dmg', 0)
    a, b = once_land / once_n, p1_land / p1_n
    print(f"Level {LEVEL}, Health x{mult}: a Bleeding stack lands {100 * a:.0f}% of the time, a +1 on a hit {100 * b:.0f}%; "
          f"stack = {a / b:.2f} of a nominal point = {4 * a / b:.2f} Value", flush=True)
