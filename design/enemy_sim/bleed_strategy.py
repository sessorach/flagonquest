"""Bleeding in ordinary fights with the party playing to it (2026-10-07).

The earlier checks (bleed_check.py) had the party focus-fire as usual.
Here the Bleeding carrier spreads its stacks instead (tactics' 'Bleed
Spreader': unbled enemies first, then the most Health left after
Bleeding), optionally with the rest of the party also leaving enemies
their Bleeding will finish (tactics.LET_BLEED_OUT). Each variant is
measured against the plain focus-fire party with no Bleeding, so it
includes the cost of the carrier not focusing. "No Bleeding" prices that
cost on its own.

Usage: python3 bleed_strategy.py CARRIER   (e.g. "Hilde (L2)")"""
import os
import sys
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tactics
from turnorder_single import build

TRIALS = 800


def run(carrier, style, health, tactic=None):
    cs.make_party = lambda t, good_luck=0: build(carrier, style, health, tactic)
    scores = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(TRIALS):
            r = cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                             seed=100_000 * mi + k)
            scores.append(100 * r["party_hp_pct"] if r["winner"] == "party" else 0.0)
    return st.mean(scores)


if __name__ == "__main__":
    carrier = sys.argv[1]
    tactics.LET_BLEED_OUT = False
    base = run(carrier, None, 0)
    per = (run(carrier, None, 2) - base) / 8
    for bleed_out in (False, True):
        tactics.LET_BLEED_OUT = bleed_out
        for test in ("Bleeding Strikes", "Bleeding Dump", None):
            v = (run(carrier, test, 0, "Bleed Spreader") - base) / per * 4
            label = f"spread{' + bleed out' if bleed_out else ''}"
            print(f"{carrier:14} {label:20} {test or 'No Bleeding':17} {v:+5.1f}", flush=True)
