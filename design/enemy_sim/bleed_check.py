"""Bleeding on boss fights, and letting enemies bleed out (2026-10-07).

Prices the test-only passives (Bleeding Strikes, Bleeding Dump, Plus One
Damage) on each of four carriers, one at a time, against a party-wide
Health ladder, with the party either focus-firing (the default) or
leaving an enemy its Bleeding will finish (tactics.LET_BLEED_OUT).

Usage: python3 bleed_check.py boss   (Solo Boss, Boss and Guards; both modes)
       python3 bleed_check.py std    (the standard four mixes; bleed-out only)"""
import sys, statistics as st
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tactics
from turnorder_single import build
CARRIERS=["Hilde (L2)","Browndog (L2)","Carrick (L2)","Sable (L2)"]
TESTS=["Bleeding Strikes","Bleeding Dump","Plus One Damage"]
def run(mixes, carrier, style, health, trials=800):
    cs.make_party = lambda t, good_luck=0: build(carrier, style, health)
    sc=[]; rounds=[]
    for mi,mix in enumerate(mixes):
        for k in range(trials):
            r=cs.run_fight(1,2,movement=True,enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),seed=100_000*mi+k)
            sc.append(100*r["party_hp_pct"] if r["winner"]=="party" else 0.0); rounds.append(r.get("rounds",0))
    return st.mean(sc), st.mean(rounds)
groups=[("Standard four",se.CURRENT_MIXES)]+[(m,(m,)) for m in se.BOSS_MIXES]
which=sys.argv[1]
for bleed_out in ([False,True] if which!="std" else [True]):
  tactics.LET_BLEED_OUT=bleed_out
  for name,mixes in (groups[:1] if which=="std" else groups[1:]):
    base,rd=run(mixes,CARRIERS[0],None,0); plus2,_=run(mixes,CARRIERS[0],None,2); per=(plus2-base)/8
    print(f"== {name} | bleed-out={bleed_out} | base {base:.1f} (rounds {rd:.1f}) +2H {plus2:.1f} per {per:.2f}",flush=True)
    for t in TESTS:
      vals=[]
      for c in CARRIERS:
        s,_=run(mixes,c,t,0); vals.append((s-base)/per*4)
      print(f"   {t:17} "+"  ".join(f"{v:+5.1f}" for v in vals)+f"   avg {st.mean(vals):+5.1f}",flush=True)
