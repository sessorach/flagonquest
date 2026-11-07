"""The Black Knight one piece at a time: Omniguard, Taunting, armor
(2026-11-06; ENEMY_ENCOUNTER_DESIGN, "Why the Black Knight is slow").

    python3 experiments/enemies/black_knight_pieces.py
"""
import sys, collections, statistics as st, multiprocessing as mp
sys.path.insert(0,'experiments/enemies')
import _paths, size_check as sc, sample_enemies as se, combat_sim as cs, day_sim as ds, party, table_check as tc, progression_sweep as ps, tunables as T
BK=dict(sc.TEST_ELITES["Black Knight"])
VAR={"as tested": {},
     "no Omniguard": dict(PrunedPicks="Strike (Taunting); Strike (Taunting); Sturdy"),
     "no Taunting": dict(PrunedPicks="Omniguard; Sturdy", BigPicks=BK["BigPicks"].replace("Action (Taunting); ","")),
     "Medium armor": dict(Armor="Medium"),
     "no Omniguard, Medium armor": dict(PrunedPicks="Strike (Taunting); Strike (Taunting); Sturdy", Armor="Medium")}
def job(a):
    v,L,gi=a
    sc.install(); T.ENEMY_LEVEL_UP=0
    sc.TEST_ELITES["Black Knight"]=dict(BK, **VAR[v])
    gname,pn,sw=tc.groups(L,ps.MID[L])[gi]
    make,last=ds._maker(pn,sw,party._rows(),[])
    out=[]
    for k in range(30):
        cs.make_party=make
        tr=[]
        r=cs.run_fight(1,min(L,3),movement=True,enemies=se.build_encounter([f"Black Knight@{L}"]*2),seed=1000+k,trace=tr)
        att=[e for e in tr if e.get('side')=='party' and e.get('action')=='attack' and 'raw_dmg' in e]
        out.append((r['winner']=='party', r['rounds'], sum(e['hit'] for e in att), len(att), sum(e['dmg'] for e in att if e['hit']), sum(bool(p.get('was_downed')) for p in last)>0))
    return v,out
if __name__=='__main__':
    jobs=[(v,L,gi) for v in VAR for L in (3,4,5) for gi in range(8)]
    res=collections.defaultdict(list)
    with mp.Pool(4) as p:
        for v,o in p.imap_unordered(job,jobs): res[v].extend(o)
    for v in VAR:
        o=res[v]
        print(f"{v:28s} lost {100*(1-st.mean(x[0] for x in o)):4.1f}% Down {100*st.mean(x[5] for x in o):3.0f}% rounds {st.mean(x[1] for x in o):4.1f} | PC hit {100*sum(x[2] for x in o)/sum(x[3] for x in o):3.0f}%, damage per hit {sum(x[4] for x in o)/sum(x[2] for x in o):.1f}")
