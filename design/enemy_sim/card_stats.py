"""Where the cards go (2026-10-09): per PC, averaged over fights, what
the real-cards model spends and what it buys - the starting budget,
cards actually spent, rescues of its own misses and of allies' kill
shots, Gambles backed by a card, kill top-ups, Perfect Strikes, Raise
Spirits boosts and suit-pool Extra Successes. For checking the card
policy against the table, not for balance numbers.

    python3 card_stats.py                 # Level 1 Party A
    python3 card_stats.py -p T -n 300     # another calibrate.py party
    python3 card_stats.py -s CARDS_ALLY_RESCUE=False"""
import argparse
import ast
import os
import sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T, tactics
from calibrate import PARTIES

KEYS = ("budget0", "cards_spent", "rescues", "rescues_given", "backed", "topups", "perfect_strikes",
        "raises", "suit_extras", "hexes_cast", "hexes_hit", "cleansed", "fate_draws")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=200, help="fights per mix")
    ap.add_argument("-p", default="A")
    ap.add_argument("-L", type=int, default=1)
    ap.add_argument("-s", action="append", default=[])
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        setattr(T if hasattr(T, k) else tactics, k, v)
    names = PARTIES[a.L][a.p]
    made = []

    def mk(t, good_luck=0):
        made.append(party.make_party_from(names, good_luck))
        return made[-1]
    cs.make_party = mk
    orig_start = cs.cards.start_fight

    def start(pc):
        orig_start(pc)
        pc['budget0'] = pc['budget']
    cs.cards.start_fight = start
    tot = defaultdict(lambda: defaultdict(float))
    fights = 0
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(a.n):
            cs.run_fight(1, a.L, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[a.L][mix]), seed=100_000 * mi + k)
            fights += 1
            for p in made[-1]:
                for key in KEYS:
                    tot[p['name']][key] += p.get(key, 0)
    print(f"L{a.L} Party {a.p}, {fights} fights, per PC per fight:")
    print("PC".ljust(14) + "".join(k[:12].rjust(13) for k in KEYS))
    for name, d in tot.items():
        print(name.ljust(14) + "".join(f"{d[k] / fights:13.2f}" for k in KEYS))
