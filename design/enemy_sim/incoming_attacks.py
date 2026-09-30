"""Tallies how many attacks each PC takes per fight (and how many land,
and how many they Parry), for pricing Styles that trigger on being
attacked. Usage: python3 incoming_attacks.py"""
import sys, random, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import combat_sim, party, sample_enemies as se

def run(names, level, trials=3000, movement=True, encounter=None):
    holder = {}
    def mp(tier, good_luck=0):
        holder['pcs'] = party.make_party_from(names, good_luck)
        return holder['pcs']
    combat_sim.make_party = mp
    wins = 0; rounds = 0; hp = []
    agg = collections.defaultdict(lambda: collections.Counter())
    for _ in range(trials):
        enemies = se.build_encounter(se.ENCOUNTERS[level][encounter]) if encounter else se.make_level_encounter(level)
        r = combat_sim.run_fight(1, level, movement=movement, enemies=enemies)
        wins += r['winner'] == 'party'; rounds += r['rounds']
        if r['winner'] == 'party': hp.append(r['party_hp_pct'])
        for p in holder['pcs']:
            key = p['name'][:-1]
            for k in ('attacks_received', 'attacks_vs_parry_dodge', 'hits_received', 'parries'):
                agg[key][k] += p.get(k, 0)
    print(f"\n== {', '.join(names)} vs Level {level} {encounter or ''}: win {100*wins/trials:.1f}%  rounds {rounds/trials:.1f}  HP left on win {100*sum(hp)/max(1,len(hp)):.0f}%")
    tot = 0
    for k, c in agg.items():
        tot += c['attacks_received']
        print(f"   {k:16} attacks {c['attacks_received']/trials:4.2f}  vs Dodge/Parry {c['attacks_vs_parry_dodge']/trials:4.2f}  hits {c['hits_received']/trials:4.2f}  Parries {c['parries']/trials:4.2f}")
    print(f"   party total attacks received {tot/trials:.1f}")

A1 = ['Hilde', 'Browndog', 'Carrick', 'Sable']
B1 = ['Rook', 'Jackal', 'Wren', 'Hanforth']
C1 = ['Hilde', 'Browndog', 'Beornhard', 'Hanforth']
L2 = lambda xs: [x + ' (L2)' for x in xs]
if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for enc in ('Classic', 'Warband', 'Coven'):
        for names, lvl in [(A1, 1), (L2(A1), 2), (L2(A1), 3), (L2(B1), 2), (L2(C1), 2)]:
            run(names, lvl, trials, encounter=enc)
