"""How long enemies last once the party starts hitting them (2026-10-07).

The designer's read of their own table: once an enemy has taken a hit,
it gets another full turn about half the time. This measures the same
thing in the sim from fight traces - for each damaging party hit, does
the target act again afterwards - split into the first hit an enemy
takes and every hit - plus hits-to-kill and damage per hit. An optional
Health multiplier (applied to every enemy) shows how much tougher the
enemies would need to be to match the table, and what Bleeding lands
then.

Usage: python3 enemy_toughness.py [health multiplier, default 1] [Bleeding mode]
(Bleeding mode: tunables.BLEED_MODE - own_turn, round_end or on_damage)"""
import os
import sys
import statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
import combat_sim as cs, sample_enemies as se, party
from turnorder_single import build

TRIALS = 200
PARTY_A = ["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"]


def encounter(mix, mult):
    en = se.build_encounter(se.ENCOUNTERS[2][mix])
    for e in en:
        e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
    return en


def trace_stats(mult):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(PARTY_A, good_luck)
    first, every, hits_to_kill, dmg_per_hit, wins, hp = [], [], [], [], [], []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(TRIALS):
            tr = []
            r = cs.run_fight(1, 2, movement=True, enemies=encounter(mix, mult), seed=100_000 * mi + k, trace=tr)
            wins.append(r['winner'] == 'party')
            hp.append(100 * r['party_hp_pct'] if r['winner'] == 'party' else 0)
            acts = [(i, ev['unit']) for i, ev in enumerate(tr) if ev.get('side') == 'enemy' and ev.get('unit')]
            seen, hits = set(), {}
            for i, ev in enumerate(tr):
                if ev.get('side') == 'party' and ev.get('action') == 'attack' and ev.get('hit') and ev.get('dmg', 0) > 0:
                    t = ev['target']
                    again = any(j > i and u == t for j, u in acts)
                    every.append(again)
                    if t not in seen:
                        first.append(again)
                        seen.add(t)
                    hits[t] = hits.get(t, 0) + 1
                    dmg_per_hit.append(ev['dmg'])
                    if ev.get('target_hp_after', 1) <= 0:
                        hits_to_kill.append(hits[t])
    return dict(first=st.mean(first), every=st.mean(every), htk=st.mean(hits_to_kill),
                dmg=st.mean(dmg_per_hit), win=st.mean(wins), hp=st.mean(hp))


def bleed_points(mult):
    out = {}
    for test in ("Bleeding Once", "Bleeding Strikes", "Bleeding Dump"):
        pts = []
        for c in PARTY_A:
            cs.make_party = lambda t, good_luck=0, c=c: build(c, test, 0)
            for mi, mix in enumerate(se.CURRENT_MIXES):
                pts += [cs.run_fight(1, 2, movement=True, enemies=encounter(mix, mult),
                                     seed=100_000 * mi + k).get('bleed_dealt', 0) for k in range(TRIALS)]
        out[test] = st.mean(pts)
    return out


if __name__ == "__main__":
    mult = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    if len(sys.argv) > 2:
        import tunables
        tunables.BLEED_MODE = sys.argv[2]
    s = trace_stats(mult)
    print(f"Health x{mult}: acts again after its first hit {100 * s['first']:.0f}%, after any hit "
          f"{100 * s['every']:.0f}%; hits to kill {s['htk']:.2f}; damage per hit {s['dmg']:.2f}; "
          f"party wins {100 * s['win']:.0f}%, Health left {s['hp']:.1f}", flush=True)
    b = bleed_points(mult)
    print(f"Health x{mult} ({cs.T.BLEED_MODE}): Bleeding points a fight - Once {b['Bleeding Once']:.2f}, "
          f"Strikes {b['Bleeding Strikes']:.2f}, Dump {b['Bleeding Dump']:.2f}", flush=True)
