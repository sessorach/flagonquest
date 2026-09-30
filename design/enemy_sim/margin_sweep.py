"""Tries stat-based ways to give the party a margin over PC-modeled enemies
(enemy Health, enemy Stat spread one Level behind) and a flat weapon-base
increase for everyone (fight length). Everything is a real stat change, no
hidden bonuses. Usage: python3 margin_sweep.py [trials]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se, enemy_builder_pcstyle as eb


def run(names, level, enc, trials, health=15, lag=False, dmg=0):
    eb.ENEMY_STAT_LAG = 1 if lag else 0
    eb.ENEMY_HEALTH_BASE = health
    def mp(t, good_luck=0):
        ps = party.make_party_from(names, good_luck)
        for p in ps:
            p['damage'] += dmg
            if p.get('bottled_fire_profile'): p['bottled_fire_profile']['damage'] += dmg
        return ps
    cs.make_party = mp
    w = 0; rs = []; hp = []
    for _ in range(trials):
        es = se.build_encounter(se.ENCOUNTERS[level][enc])
        for e in es:
            if e.get('attack_damage'): e['attack_damage'] += dmg
            if e.get('backup'): e['backup']['attack_damage'] += dmg
        r = cs.run_fight(1, level, movement=True, enemies=es)
        w += r['winner'] == 'party'; rs.append(r['rounds'])
        if r['winner'] == 'party': hp.append(r['party_hp_pct'])
    return 100 * w / trials, st.mean(rs), 100 * st.mean(hp) if hp else 0

L2 = lambda xs: [x + ' (L2)' for x in xs]
PARTIES = {'A': L2(['Hilde', 'Browndog', 'Carrick', 'Sable']), 'B': L2(['Rook', 'Jackal', 'Wren', 'Hanforth']),
           'C': L2(['Hilde', 'Browndog', 'Beornhard', 'Hanforth'])}
VARIANTS = [
    ("PC-modeled, Health 15", {}),
    ("Health 10 (PC base, no Toughened Body)", dict(health=10)),
    ("Stats one Level behind", dict(lag=True)),
    ("Health 10 + Stats one Level behind (default)", dict(health=10, lag=True)),
    ("  ...+ all weapons +1", dict(health=10, lag=True, dmg=1)),
    ("  ...+ all weapons +2", dict(health=10, lag=True, dmg=2)),
]
if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    encs = ('Classic', 'Warband', 'Coven', 'Chapel', 'Horde')
    print("Level 2 parties vs Level 2 mixes: win% / rounds / HP left on a win")
    print(f"{'':40} " + ' | '.join(f"{p}/{e[:4]:4}" for p in PARTIES for e in encs))
    for label, kw in VARIANTS:
        cells = []
        for pn, names in PARTIES.items():
            for e in encs:
                wv, rv, hv = run(names, 2, e, trials, **kw)
                cells.append(f"{wv:3.0f}%{rv:4.1f}r{hv:3.0f}")
        print(f"{label:40} " + ' | '.join(cells), flush=True)
