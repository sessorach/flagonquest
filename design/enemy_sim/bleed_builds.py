"""Bleeding builds in real parties (2026-10-09).

Each sample party next to the same party with its Bleeding variants
swapped in (sample_pcs.csv's "(Bleed)" rows: Hilde with Furious Rage,
Felix's Battle Maneuver with Battering, Jackal throwing Acidic Flasks,
Beornhard with a Sanguine War Magic), under a Bleeding rule from
tunables.py. Prints the calibration checks plus the Bleeding damage that
landed and how many enemies (and PCs) bled out a fight.

    python3 bleed_builds.py                       # the rule as written
    python3 bleed_builds.py -s BLEED_OUT=x1/2     # the half-stacks execute
    python3 bleed_builds.py -s BLEED_OUT=x1/2 -s FURIOUS_RAGE_STACKS=2"""
import argparse
import ast
import os
import statistics as st
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T

PARTIES = {
    "A": (["Hilde", "Browndog", "Carrick", "Sable"], ["Hilde (Bleed)", "Browndog", "Carrick", "Sable"]),
    "S": (["Enith", "Felix", "Jackal", "Hanforth"], ["Enith", "Felix (Bleed)", "Jackal (Bleed)", "Hanforth"]),
    "T": (["Browndog", "Hanforth", "Sable", "Beornhard"], ["Browndog", "Hanforth", "Sable", "Beornhard (Bleed)"]),
    "X": (["Hilde", "Felix", "Jackal", "Beornhard"],
          ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"]),
}


def run(names, n):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    R = [cs.run_fight(1, 1, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[1][mix]), seed=100_000 * mi + k)
         for mi, mix in enumerate(se.CURRENT_MIXES) for k in range(n)]
    m = lambda key: st.mean(r.get(key, 0) for r in R)
    return (f"{st.mean(r['rounds'] for r in R):.2f} rounds | loses {100 * st.mean(r['winner'] != 'party' for r in R):.1f}% | "
            f"Down {100 * m('pc_downed'):.0f}% | Wounded {100 * m('pc_wounded'):.0f}% | Bleeding {m('bleed_dealt'):.2f} a fight | "
            f"bled out {m('executes'):.2f} enemies, {m('pc_executes'):.2f} PCs")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=200, help="fights per mix")
    ap.add_argument("-p", default="ASTX")
    ap.add_argument("-s", action="append", default=[])
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        setattr(T, k, v)
    print("== " + (", ".join(a.s) or "Bleeding as written"), flush=True)
    for p in a.p:
        base, bleed = PARTIES[p]
        print(f"{p} base : {run(base, a.n)}", flush=True)
        print(f"{p} bleed: {run(bleed, a.n)}", flush=True)
