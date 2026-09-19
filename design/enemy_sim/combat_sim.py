"""
Monte Carlo combat loop: 4 party members vs. N copies of one enemy,
repeated many times with fresh card flips to estimate win rate, average
rounds to resolve, and party Health remaining on a win.

Deliberately simplified, not a real combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of what's
NOT modeled (no real Extra Successes from suit-pool matching, no
Techniques/items, no distinct PC roles, no positioning, no real
initiative, rough Battle Tactics targeting proxies). PCs DO now Gamble
(see `pc_gamble_count`) - added specifically because armored enemies
otherwise had no counter-play modeled at all. Good for catching relative
differences between builds and Tiers; the exact win percentages aren't
precise predictions of real play.

Enemy Abilities (the subset in tunables.ABILITY_COST) are also modeled:
Crippled/Vulnerable/Bleeding stacks on PCs from Strike (Crippling)/
Strike (Vulnerable)/Poison (Bleeding), Durable's per-turn Protected
regen on enemies, all following rulebook.md/glossary.md's real numbers
(Crippled -1 to attacks/stack, Vulnerable -1 to Vital/Mental/Vigilant
Defenses/stack, Bleeding 1 damage per stack that decays, Protected
absorbs Health loss 1-for-1). Fleeting effects (all of the above) decay
1 stack per bearer's own turn, per glossary.md's [Fleeting] rule - not
all stacks at once.

`max_rounds` (30, not the original 10) matters more than it looks: a
fight that's genuinely close but slow-grinding (both sides doing modest
damage against real Resist/Defense) was hitting the old 10-round cap as
an unresolved "draw" most of the time rather than actually playing out -
e.g. one build read as "10% win rate" under the old cap that was really
a near-even 201-vs-211 split once let run to a real conclusion (1588 of
2000 trials had been draws). Always sanity-check a low win rate against
the raw party/enemies/draw counts (`simulate()`'s 4th return value)
before assuming it means "this build loses," not just "this build is
slow to resolve."
"""
import random
import copy
from sample_enemies import make_enemy
from party import make_party


def flip():
    return random.randint(1, 13)


def flip_best_of(n):
    return max(flip() for _ in range(n))


def pc_gamble_count(pc, target):
    """How many times a 'clever' PC Gambles on this attack (rulebook.md's
    Gambling rule: each Gamble is -2 to the roll, but grants +1 Extra
    Success - and +1 damage - if the flip still hits). Not modeled at all
    before this - without it, a target whose Physical Resist reaches or
    exceeds the PC's own weapon Damage was untouchable no matter how many
    rounds passed, which isn't how a real player would actually respond
    to a wall of Resist.

    `needed` is how many Extra Successes it takes to make a hit deal net
    +1 damage through the target's Resist - a normal attack against a
    target with `needed > 0` deals exactly 0 on every hit, so a player
    who recognizes that gambles regardless of the accuracy cost: some
    chance of real damage beats a guaranteed zero. `max_possible` is the
    only cap applied then - never gamble past the point where even the
    best possible card (13) couldn't clear the target's Parry, since
    that's a wasted action no one would actually take.

    Only when `needed == 0` (a normal hit is already doing something)
    does the more cautious "plenty of Skill Total to spare" judgment
    call from the rulebook's own Gambling text apply - gamble once more
    for the extra damage, but only if the *average* card (7) would still
    clear the target's Parry.
    """
    effective_skill = pc['skill_total'] - pc.get('crippled', 0)
    needed = max(0, target['physres'] - pc['damage'] + 1)
    max_possible = max(0, (effective_skill + 13 - target['parry']) // 2)
    if needed > 0:
        return min(needed, max_possible)
    max_safe = max(0, (effective_skill + 7 - target['parry']) // 2)
    return min(1, max_safe)


def pc_defense_for(target, opp_def):
    """Route an enemy attack's opp_def to the right PC Defense category -
    'Parry/Dodge' lets the target pick whichever's better, same as
    rulebook.md's real rule ("If multiple Defenses are stated, the target
    chooses which to use"). Vulnerable stacks (-1 to Vital/Mental/
    Vigilant Defenses per stack, glossary.md) apply to the Bodily/Mental
    cases only - Dodge and Parry aren't Vulnerable's targets."""
    vulnerable = target.get('vulnerable', 0)
    if opp_def == 'Parry/Dodge':
        return max(target['parry'], target['dodge'])
    if opp_def == 'Dodge':
        return target['dodge']
    if opp_def == 'Bodily':
        return target['bodily'] - vulnerable
    if opp_def == 'Mental':
        return target['mental'] - vulnerable
    return target['dodge']


def run_fight(tier, enemy_level, n_enemies=4, max_rounds=30, seed=None):
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
            gambles = pc_gamble_count(pc, target)
            crippled = pc.get('crippled', 0)
            roll = pc['skill_total'] - crippled + flip() - 2 * gambles  # PCs attack with Melee, vs. the enemy's Parry
            if roll >= target['parry']:
                dmg = max(0, pc['damage'] + gambles - target['physres'])
                protected = target.get('protected', 0)
                if protected > 0 and dmg > 0:
                    absorbed = min(dmg, protected)
                    target['protected'] -= absorbed
                    dmg -= absorbed
                target['health'] -= dmg
        # Fleeting decay: 1 stack of each per bearer's own turn (glossary.md's
        # [Fleeting] rule), not all stacks at once - Bleeding's decaying
        # stack is what actually deals its 1 damage.
        for pc in pcs:
            if pc['health'] <= 0:
                continue
            if pc.get('crippled', 0) > 0:
                pc['crippled'] -= 1
            if pc.get('vulnerable', 0) > 0:
                pc['vulnerable'] -= 1
            if pc.get('bleeding', 0) > 0:
                pc['bleeding'] -= 1
                pc['health'] -= 1
        if all(e['health'] <= 0 for e in enemies):
            return dict(winner='party', rounds=rnd,
                        party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs))
        if all(p['health'] <= 0 for p in pcs):
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0)

        # Enemies' turn: Fighting Style sets attack count, Battle Tactics
        # picks the target (rough proxies, not a real implementation - see
        # module docstring).
        for e in enemies:
            if e['health'] <= 0:
                continue
            abilities = e.get('abilities', [])
            if 'Durable' in abilities and e.get('protected', 0) < 4:
                e['protected'] = e.get('protected', 0) + 1
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
                    if 'Strike (Crippling)' in abilities:
                        target['crippled'] = target.get('crippled', 0) + 1
                    if 'Strike (Vulnerable)' in abilities:
                        target['vulnerable'] = target.get('vulnerable', 0) + 1
                    if 'Poison (Bleeding)' in abilities:
                        target['bleeding'] = target.get('bleeding', 0) + 2
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
