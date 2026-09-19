"""
Monte Carlo combat loop: 4 party members vs. N copies of one enemy,
repeated many times with fresh card flips to estimate win rate, average
rounds to resolve, and party Health remaining on a win.

Deliberately simplified, not a real combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of what's
NOT modeled (no Extra Successes/Gambling/Techniques/items, no distinct
PC roles, no positioning, no real initiative, rough Battle Tactics
targeting proxies). Good for catching relative differences between
builds and Tiers; the exact win percentages aren't precise predictions
of real play.
"""
import random
import copy
from sample_enemies import make_enemy
from party import make_party


def flip():
    return random.randint(1, 13)


def flip_best_of(n):
    return max(flip() for _ in range(n))


def pc_defense_for(target, opp_def):
    """Route an enemy attack's opp_def to the right PC Defense category -
    'Parry/Dodge' lets the target pick whichever's better, same as
    rulebook.md's real rule ("If multiple Defenses are stated, the target
    chooses which to use")."""
    if opp_def == 'Parry/Dodge':
        return max(target['parry'], target['dodge'])
    if opp_def == 'Dodge':
        return target['dodge']
    if opp_def == 'Bodily':
        return target['bodily']
    if opp_def == 'Mental':
        return target['mental']
    return target['dodge']


def run_fight(tier, enemy_level, n_enemies=4, max_rounds=10, seed=None):
    if seed is not None:
        random.seed(seed)
    pcs = make_party(tier)
    enemies = [copy.deepcopy(make_enemy(enemy_level)) for _ in range(n_enemies)]

    for rnd in range(1, max_rounds + 1):
        # Party's turn: each living PC attacks the first living enemy
        # (pure focus fire, no target choice) vs. that enemy's Parry Defense.
        for pc in pcs:
            if pc['health'] <= 0:
                continue
            targets = [e for e in enemies if e['health'] > 0]
            if not targets:
                break
            target = targets[0]
            roll = pc['skill_total'] + flip()  # PCs attack with Melee, vs. the enemy's Parry
            if roll >= target['parry']:
                dmg = max(0, pc['damage'] - target['physres'])
                target['health'] -= dmg
        if all(e['health'] <= 0 for e in enemies):
            return dict(winner='party', rounds=rnd,
                        party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs))

        # Enemies' turn: Fighting Style sets attack count, Battle Tactics
        # picks the target (rough proxies, not a real implementation - see
        # module docstring).
        for e in enemies:
            if e['health'] <= 0:
                continue
            living_pcs = [p for p in pcs if p['health'] > 0]
            if not living_pcs:
                break
            tactic = e.get('battle_tactic', 'Hit Whatever')
            if tactic == 'Assassin':
                target = min(living_pcs, key=lambda p: p['health'])
            else:
                target = living_pcs[0]  # proxy for Hit Whatever / Hold the Line / Vanguard alike

            fighting_style = e.get('fighting_style', 'Guarded')
            n_attacks = 2 if fighting_style == 'Flurry' else 1
            for _ in range(n_attacks):
                roll = e['accuracy'] + (flip_best_of(2) if fighting_style == 'Aimed Shot' else flip())
                opp_def_val = pc_defense_for(target, e['opp_def'])
                if roll >= opp_def_val:
                    dmg = max(0, e['attack_damage'] - target.get('physres', 0))
                    target['health'] -= dmg
                if target['health'] <= 0:
                    living_pcs = [p for p in pcs if p['health'] > 0]
                    if not living_pcs:
                        break
                    target = living_pcs[0]
        if all(p['health'] <= 0 for p in pcs):
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0)

    return dict(winner='draw', rounds=max_rounds,
                party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs))


def simulate(tier, enemy_level, n_enemies=4, trials=4000):
    results = {'party': 0, 'enemies': 0, 'draw': 0}
    rounds_list = []
    hp_list = []
    for _ in range(trials):
        r = run_fight(tier, enemy_level, n_enemies=n_enemies)
        results[r['winner']] += 1
        rounds_list.append(r['rounds'])
        if r['winner'] == 'party':
            hp_list.append(r['party_hp_pct'])
    win_pct = results['party'] / trials * 100
    avg_rounds = sum(rounds_list) / len(rounds_list)
    avg_hp_on_win = (sum(hp_list) / len(hp_list) * 100) if hp_list else 0
    return win_pct, avg_rounds, avg_hp_on_win, results


if __name__ == "__main__":
    win, rnds, hp, res = simulate(2, 2, trials=4000)
    print(f"Tier2 vs Level2: win={win:.1f}% rounds={rnds:.1f} hp_on_win={hp:.1f}% raw={res}")
