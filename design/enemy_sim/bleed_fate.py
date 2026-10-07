"""Where a single Bleeding stack goes (2026-10-07): for the Bleeding Once
test passive on each Party A carrier, whether the stack ticked, or its
target died before the end of its own next turn, or the fight ended
first; plus, for every enemy, how many of its own turns it finished
after first taking damage (the chance any Bleeding gets to tick).

Usage: python3 bleed_fate.py"""
import sys, statistics as st, collections
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, tactics
from turnorder_single import build
print("targeting:", tactics.PARTY_TARGETING)
orig=cs._take_enemy_turn
def wrapped(e,*a,**k):
    r=orig(e,*a,**k)
    if e['health']>0 and e['health']<e['max_health']:
        CUR[id(e)]=CUR.get(id(e),0)+1
    return r
cs._take_enemy_turn=wrapped
CUR={}
CARRIERS=["Hilde (L2)","Browndog (L2)","Carrick (L2)","Sable (L2)"]
fate=collections.Counter(); turns_dist=collections.Counter(); n_en=0
already=collections.Counter()
for car in CARRIERS:
    for mi,mix in enumerate(se.CURRENT_MIXES):
        for k in range(400):
            holder={}
            def mk(t,good_luck=0):
                holder['pcs']=build(car,"Bleeding Once",0); return holder['pcs']
            cs.make_party=mk
            en=se.build_encounter(se.ENCOUNTERS[2][mix])
            CUR.clear()
            r=cs.run_fight(1,2,movement=True,enemies=en,seed=100000*mi+k)
            vals=list(CUR.values())+[0]*(len(en)-len(CUR))
            for v in vals:
                n_en+=1; turns_dist[min(v,3)]+=1
            # the once stack: find enemy with bleed applied by carrier = enemy with bleed_dealt or the one recorded
            tgt=[e for e in en if e.get('once_mark')]
            pc=[p for p in holder['pcs'] if 'Bleeding Once' in p.get('passives',())][0]
            t=pc.get('once_target')
            if t is None: fate['never applied (no hit)']+=1
            elif t.get('bleed_dealt',0)>0: fate['ticked']+=1
            elif t['health']<=0: fate['target died before its turn ended']+=1
            else: fate['fight ended first']+=1
            if t is not None: already['target had already acted that round' if t.get('acted_at_apply') else 'target still to act that round']+=1
tot=sum(fate.values())
for k,v in fate.most_common(): print(f"{k:38} {100*v/tot:5.1f}%")
for k,v in already.items(): print(f"{k:38} {100*v/sum(already.values()):5.1f}%")
print("enemy turns completed after first taking damage (all enemies, no Bleeding needed):")
for k in sorted(turns_dist): print(f"  {k}{'+' if k==3 else ''}: {100*turns_dist[k]/n_en:5.1f}%")
