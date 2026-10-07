"""Party targeting modes side by side (2026-10-07): the old 'wounded'
rule, 'threat' (perfect focus fire on threat per Health) and 'table'
(focus fire done imperfectly - see tactics.target_table). For each:
Party A and D's win rate, Health left and fight length on the standard
four mixes, and how much extra damage Bleeding lands per fight on each
Party A carrier (bleed_points.py's count).

Usage: python3 party_targeting_compare.py MODE"""
import os
import sys
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tactics, party
from turnorder_single import build

TRIALS = 400
PARTIES = {"A": ["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"],
           "D": ["Browndog (L2)", "Hanforth (L2)", "Felix (L2)", "Beornhard (L2)"]}


def fights(make):
    cs.make_party = make
    out = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        out += [cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                             seed=100_000 * mi + k) for k in range(TRIALS)]
    return out


if __name__ == "__main__":
    tactics.PARTY_TARGETING = sys.argv[1]
    for pname, names in PARTIES.items():
        R = fights(lambda t, good_luck=0, names=names: party.make_party_from(names, good_luck))
        print(f"{sys.argv[1]:8} party {pname}: win {100 * st.mean(r['winner'] == 'party' for r in R):.0f}%, "
              f"Health left {st.mean(100 * r['party_hp_pct'] if r['winner'] == 'party' else 0 for r in R):.1f}, "
              f"rounds {st.mean(r['rounds'] for r in R):.1f}", flush=True)
    for test in ("Bleeding Once", "Bleeding Strikes", "Bleeding Dump"):
        pts = []
        for c in PARTIES["A"]:
            R = fights(lambda t, good_luck=0, c=c: build(c, test, 0))
            pts.append(st.mean(r.get("bleed_dealt", 0) for r in R))
        print(f"{sys.argv[1]:8} {test:17} " + "  ".join(f"{p:.2f}" for p in pts) + f"   avg {st.mean(pts):.2f}", flush=True)
