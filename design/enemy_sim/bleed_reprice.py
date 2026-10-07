"""Bleeding under the party's 'threat' targeting (2026-10-07).

Same measure as bleed_check.py's standard-four run (one carrier at a
time, party-wide Health ladder, paired seeds), redone after the party's
default targeting changed from "least Health" to "most threat per point
of Health" (tactics.PARTY_TARGETING), since the old rule made fights
longer and left the back line alone. Feeds the Bleeding reprice.

Usage: python3 bleed_reprice.py CARRIER   (e.g. "Hilde (L2)")"""
import os
import sys
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tactics
from turnorder_single import build

TRIALS = 800


def run(carrier, style, health):
    cs.make_party = lambda t, good_luck=0: build(carrier, style, health)
    scores, rounds = [], []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(TRIALS):
            r = cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                             seed=100_000 * mi + k)
            scores.append(100 * r["party_hp_pct"] if r["winner"] == "party" else 0.0)
            rounds.append(r["rounds"])
    return st.mean(scores), st.mean(rounds)


if __name__ == "__main__":
    carrier = sys.argv[1]
    tactics.PARTY_TARGETING = "threat"
    base, rnds = run(carrier, None, 0)
    per = (run(carrier, None, 2)[0] - base) / 8
    print(f"{carrier:14} base {base:.1f} rounds {rnds:.1f} one PC's +1 Health = {per:.2f}", flush=True)
    for test in ("Bleeding Strikes", "Bleeding Dump", "Plus One Damage"):
        v = (run(carrier, test, 0)[0] - base) / per * 4
        print(f"{carrier:14} {test:17} {v:+5.1f}", flush=True)
