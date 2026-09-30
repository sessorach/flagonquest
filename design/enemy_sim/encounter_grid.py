"""Win rate, fight length and who gets attacked, for each sample party
against each named encounter mix (sample_enemies.ENCOUNTERS), plus
Browndog's Challenge on vs off. Usage: python3 encounter_grid.py"""
import sys, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import combat_sim, party, sample_enemies as se
def run(names, level, enc, trials, challenge=True):
    h={}
    def mp(tier,good_luck=0):
        h['p']=party.make_party_from(names,good_luck)
        if not challenge:
            for p in h['p']: p['challenge_uses_left']=0
        return h['p']
    combat_sim.make_party=mp
    w=r=0; agg=collections.Counter(); per=collections.Counter()
    for _ in range(trials):
        res=combat_sim.run_fight(1,level,movement=True,enemies=se.build_encounter(se.ENCOUNTERS[level][enc]))
        w+=res['winner']=='party'; r+=res['rounds']
        for p in h['p']:
            per[p['name'][:-1].replace(' (L2)','')]+=p['attacks_received']; agg['hits']+=p['hits_received']
    tot=sum(per.values())/trials
    return w/trials*100, r/trials, tot, {k:v/trials for k,v in per.items()}
A=['Hilde','Browndog','Carrick','Sable']; B=['Rook','Jackal','Wren','Hanforth']; C=['Hilde','Browndog','Beornhard','Hanforth']
L2=lambda xs:[x+' (L2)' for x in xs]
T=int(sys.argv[1]) if len(sys.argv)>1 else 1000
print("party   lvl  enc      win   rnds  atk/fight  per-PC attacks")
for pname,names,lvl in [('A',A,1),('A',L2(A),2),('A',L2(A),3),('B',L2(B),2),('C',L2(C),2)]:
    for enc in ('Classic','Warband','Coven','Chapel','Horde'):
        wv,rv,tot,per=run(names,lvl,enc,T)
        print(f"{pname}  L{'1' if lvl==1 and pname=='A' else '2'}vL{lvl} {enc:8} {wv:5.1f} {rv:5.1f} {tot:6.1f}   "+'  '.join(f"{k[:6]} {v:.1f}" for k,v in per.items()))
print("\nChallenge on vs off (party A L2 vs L2): Browndog / whole-party attacks")
for enc in ('Classic','Warband','Horde'):
    on=run(L2(A),2,enc,T,True); off=run(L2(A),2,enc,T,False)
    print(f"  {enc:8} on: win {on[0]:.1f} Browndog {on[3]['Browndog']:.1f} of {on[2]:.1f}  | off: win {off[0]:.1f} Browndog {off[3]['Browndog']:.1f} of {off[2]:.1f}")
