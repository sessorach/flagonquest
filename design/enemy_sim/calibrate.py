"""The sim against the designer's table (2026-10-08).

Prints, for each sample party on the standard four Level 2 mixes, the
checks from TABLE_PLAY_NOTES.md's calibration targets: fight length,
how often the party loses, how often someone goes Down or is Wounded,
and how often an enemy that's been hit gets another turn (after its
first hit, any hit, and any hit it survived).

Every stage of the table-play work (Wounded, start distance and line of
sight, play styles, ...) is a switch in tunables.py; flip them with
`-s NAME=VALUE` to see one stage's effect, e.g.

    python3 calibrate.py                      # current defaults
    python3 calibrate.py -s WOUNDED_RULES=False
    python3 calibrate.py -n 800 -p A          # more fights, Party A only
    python3 calibrate.py -L 1 -p ADH          # Level 1 parties against Level 1 enemies"""
import argparse
import ast
import os
import statistics as st
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T, tactics

# Level 2 (125 XP) parties against Level 2 encounters, and Level 1
# (75 XP, the players' own starting builds) against Level 1. Per the
# designer, a party fights Level 1 enemies up to ~100 XP and Level 2
# from 100 to 150. "H" is Party A with HOLE (a real ~90 XP build) in
# Carrick's place, since both are throwers.
PARTIES = {2: {"A": ["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"],
               "D": ["Browndog (L2)", "Hanforth (L2)", "Felix (L2)", "Beornhard (L2)"]},
           1: {"A": ["Hilde", "Browndog", "Carrick", "Sable"],
               "D": ["Browndog", "Hanforth", "Felix", "Beornhard"],
               "H": ["Hilde", "Browndog", "HOLE (90 XP)", "Sable"],
               # The agreed sample parties (TABLE_PLAY_NOTES.md, 2026-10-08):
               # typical table, skirmishers, support-heavy. "A" is the
               # two-front-liner one.
               "T": ["Browndog", "Hanforth", "Sable", "Beornhard"],
               "S": ["Enith", "Felix", "Jackal", "Hanforth"],
               "U": ["Browndog", "Ashleigh", "Sable", "Beornhard"]}}
TARGETS = ("Targets: ~3 rounds (5 at most), losses ~never, someone Down < 1 in 3 fights, "
           "someone Wounded ~1 in 2, a hit enemy acts again ~50%")


def run_party(names, trials, level=2, mixes=None):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    R = []
    for mi, mix in enumerate(mixes or se.CURRENT_MIXES):
        for k in range(trials):
            R.append(cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                                  seed=100_000 * mi + k))
    pool = lambda key: sum(r[key][0] for r in R) / max(1, sum(r[key][1] for r in R))
    return dict(rounds=st.mean(r['rounds'] for r in R),
                lose=st.mean(r['winner'] != 'party' for r in R),
                down=st.mean(r['pc_downed'] for r in R),
                wounded=st.mean(r['pc_wounded'] for r in R),
                first=pool('acts_again_first'), any=pool('acts_again_any'), survived=pool('acts_again_survived'),
                hp=st.mean(100 * r['party_hp_pct'] if r['winner'] == 'party' else 0 for r in R))


def line(name, m):
    return (f"Party {name}: {m['rounds']:.1f} rounds | loses {100 * m['lose']:.1f}% | someone Down "
            f"{100 * m['down']:.0f}% | someone Wounded {100 * m['wounded']:.0f}% | acts again after "
            f"first hit {100 * m['first']:.0f}%, any hit {100 * m['any']:.0f}%, a hit it survived "
            f"{100 * m['survived']:.0f}% | Health left {m['hp']:.1f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=400, help="fights per mix")
    ap.add_argument("-p", default="AD", help="which parties (letters)")
    ap.add_argument("-L", type=int, default=2, help="Level: the parties' and the encounters'")
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE (repeatable)")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        if hasattr(T, k):
            setattr(T, k, v)
        elif hasattr(tactics, k):
            setattr(tactics, k, v)
        else:
            raise SystemExit(f"unknown setting {k}")
    if a.label:
        print(f"== {a.label}", flush=True)
    for name in a.p:
        print(f"L{a.L} " + line(name, run_party(PARTIES[a.L][name], a.n, a.L)), flush=True)
