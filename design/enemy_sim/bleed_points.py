"""How many extra points of damage Bleeding actually lands (2026-10-07).

The designer's intent for Bleeding: extra damage with diminishing returns
built in, so a party can usually get about one extra point of damage a
fight out of it, but stacking more doesn't keep paying. This counts the
Bleeding ticks that land on living enemies per fight (combat_sim's
`bleed_dealt`), next to Plus One Damage's +1s that land on live Health
(`plus_one_dealt`, overkill excluded), for one carrier at a time under
the party's default targeting. Low-noise compared with the Value-ladder
reads, since it counts damage directly.

Usage: python3 bleed_points.py CARRIER"""
import os
import sys
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se
from turnorder_single import build

TRIALS = 800
TESTS = ("Bleeding Once", "Bleeding Strikes", "Bleeding Dump", "Plus One Damage")

if __name__ == "__main__":
    carrier = sys.argv[1]
    for test in TESTS:
        cs.make_party = lambda t, good_luck=0: build(carrier, test, 0)
        pts = []
        for mi, mix in enumerate(se.CURRENT_MIXES):
            for k in range(TRIALS):
                r = cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                                 seed=100_000 * mi + k)
                pts.append(r.get("bleed_dealt", 0) + r.get("plus_one_dealt", 0))
        print(f"{carrier:14} {test:17} {st.mean(pts):.2f} extra points a fight", flush=True)
