"""PC damage, gambling and elemental share against two Black Knights and
two Gravel Ogres, read off fight traces (2026-11-06; ENEMY_ENCOUNTER_DESIGN,
"Why the Black Knight is slow").

    python3 experiments/enemies/wall_damage.py
"""
import sys, collections, statistics as st, multiprocessing as mp, re
sys.path.insert(0,'experiments/enemies')
import _paths, size_check as sc, sample_enemies as se, combat_sim as cs, day_sim as ds, party, table_check as tc, progression_sweep as ps, tunables as T
def job(a):
    L, gi, enc_name = a
    sc.install(); T.ENEMY_LEVEL_UP=0
    gname,pn,sw=tc.groups(L,ps.MID[L])[gi]
    make,last=ds._maker(pn,sw,party._rows(),[])
    cs.make_party=make
    enc=[f"{enc_name}@{L}"]*2
    out=[]
    for k in range(30):
        tr=[]
        es=se.build_encounter(enc)
        phys={e['name']:e['physres'] for e in es}
        cs.run_fight(1,min(L,3),movement=True,enemies=es,seed=1000+k,trace=tr)
        for e in tr:
            if e.get('side')=='party' and e.get('action') in ('attack',) and 'raw_dmg' in e:
                name=re.sub(r'\d+$','',e['unit'])
                tgt=e.get('target','')
                pr=None
                for n,v in phys.items():
                    if tgt.startswith(n.split('@')[0]): pr=v
                out.append(dict(pc=name, hit=e['hit'], raw=e['raw_dmg'], res=e['resist'], dmg=e['dmg'],
                                elem=(e['resist']!=pr), gam=e.get('gambles',0) or 0, via=e.get('via') or 'weapon'))
    return L, enc_name, out
if __name__=='__main__':
    jobs=[(L,gi,n) for n in ('Black Knight','Gravel Ogre') for L in (3,4,5) for gi in range(8)]
    res=collections.defaultdict(list)
    with mp.Pool(4) as p:
        for L,n,o in p.imap_unordered(job,jobs): res[(n,L)].extend(o)
    for n in ('Black Knight','Gravel Ogre'):
        for L in (3,4,5):
            o=res[(n,L)]; hits=[x for x in o if x['hit']]
            print(f"== {n} L{L}: attacks {len(o)}, hit {100*len(hits)/len(o):.0f}%, raw on hit {st.mean(x['raw'] for x in hits):.1f}, after Resist {st.mean(x['dmg'] for x in hits):.1f}, elemental {100*sum(x['elem'] for x in o)/len(o):.0f}% of attacks, gambled on {100*sum(x['gam']>0 for x in o)/len(o):.0f}% (mean {st.mean(x['gam'] for x in o):.2f})")
    print("\nPer character vs Black Knights, Levels 3-5 (all parties):")
    o=[x for L in (3,4,5) for x in res[('Black Knight',L)]]
    by=collections.defaultdict(list)
    for x in o: by[x['pc'].strip()].append(x)
    for pc,xs in sorted(by.items()):
        h=[x for x in xs if x['hit']]
        vias=collections.Counter(x['via'].split(' (')[0] for x in xs).most_common(2)
        print(f"  {pc:34s} attacks {len(xs):5d} hit {100*len(h)/len(xs):3.0f}% raw {st.mean(x['raw'] for x in h) if h else 0:4.1f} -> {st.mean(x['dmg'] for x in h) if h else 0:4.1f}  elemental {100*sum(x['elem'] for x in xs)/len(xs):3.0f}%  gamble {100*sum(x['gam']>0 for x in xs)/len(xs):3.0f}%  via {vias}")
