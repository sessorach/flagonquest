"""Tries flat changes to both sides (damage, Resist, Health) and reports
win rate, fight length and how spread out the party's leftover HP is.
Usage: python3 fight_length.py"""
import sys, statistics as st
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se
def variant(dmg=0, res=0, hp=0):
    def mp(names):
        def f(t,good_luck=0):
            ps=party.make_party_from(names,good_luck)
            for p in ps:
                p['damage']+=dmg; p['physres']=max(0,p['physres']+res); p['elemres']=max(0,p['elemres']+res)
                p['health']=p['max_health']=p['health']+hp
                if p.get('bottled_fire_profile'): p['bottled_fire_profile']['damage']+=dmg
            return ps
        return f
    def enc(names):
        es=se.build_encounter(names)
        for e in es:
            if e.get('attack_damage'): e['attack_damage']+=dmg
            if e.get('backup'): e['backup']['attack_damage']+=dmg
            e['physres']=max(0,e['physres']+res); e['elemres']=max(0,e['elemres']+res)
            add=round(hp*e['health']/15) if e['slots']!=0.5 else round(hp/3)
            e['health']=e['max_health']=max(1,e['health']+add)
        return es
    return mp, enc
A=['Hilde (L2)','Browndog (L2)','Carrick (L2)','Sable (L2)']; B=['Rook (L2)','Jackal (L2)','Wren (L2)','Hanforth (L2)']
V=[('baseline',{}),('damage +2 both sides',dict(dmg=2)),('Resist -2 both sides',dict(res=-2)),('damage +1 & Resist -1',dict(dmg=1,res=-1)),('Health -4 both sides',dict(hp=-4))]
N=600
for label,kw in V:
    mp,enc=variant(**kw); out=[]
    for pname,names in (('A',A),('B',B)):
        for ek in ('Classic','Warband','Horde'):
            cs.make_party=mp(names); w=0; rs=[]; hps=[]
            for _ in range(N):
                r=cs.run_fight(1,2,movement=True,enemies=enc(se.ENCOUNTERS[2][ek]))
                w+=r['winner']=='party'; rs.append(r['rounds'])
                if r['winner']=='party': hps.append(r['party_hp_pct'])
            out.append(f"{pname}/{ek[:4]} {100*w/N:4.0f}% {st.mean(rs):4.1f}r hp{100*st.mean(hps):3.0f}±{100*st.pstdev(hps):2.0f}")
    print(f"{label:24} | "+' | '.join(out), flush=True)
