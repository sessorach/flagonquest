"""
Monte Carlo combat loop: 4 party members vs. N copies of one enemy,
repeated many times with fresh card flips to estimate win rate, average
rounds to resolve, and party Health remaining on a win.

Deliberately simplified, not a full combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of what's
NOT modeled (no Extra Successes from suit-pool matching, no Techniques/
items, no distinct PC roles, no positioning, no initiative, rough
Battle Tactics targeting proxies). PCs DO now Gamble (see
`pc_gamble_count`) - added specifically because armored enemies
otherwise had no counter-play modeled at all. Good for catching relative
differences between builds and Tiers; the exact win percentages aren't
precise predictions of real play.

Enemy Abilities (the subset in tunables.ABILITY_COST) are also modeled:
Crippled/Vulnerable/Bleeding stacks on PCs from Strike (Crippling)/
Strike (Vulnerable)/Poison (Bleeding), Durable's per-turn Protected
regen on enemies, all following rulebook.md/glossary.md's numbers
(Crippled -1 to attacks/stack, Vulnerable -1 to Vital/Mental/Vigilant
Defenses/stack, Bleeding 1 damage per stack that decays, Protected
absorbs Health loss 1-for-1). Fleeting effects (all of the above) decay
1 stack per bearer's own turn, per glossary.md's [Fleeting] rule - not
all stacks at once.

`max_rounds` (30, not the original 10) matters more than it looks: a
fight that's close but slow-grinding (both sides doing modest damage
against Resist/Defense) was hitting the old 10-round cap as an
unresolved "draw" most of the time instead of actually playing out -
e.g. one build read as "10% win rate" under the old cap that was
actually a near-even 201-vs-211 split once let run to a conclusion
(1588 of 2000 trials had been draws). Always sanity-check a low win
rate against the raw party/enemies/draw counts (`simulate()`'s 4th
return value) before assuming it means "this build loses," not just
"this build is slow to resolve."

`movement=True` on `run_fight`/`simulate` turns on the optional 2D-arena
mode (movement.py) - a bounded ARENA_SIZE x ARENA_SIZE square, PCs
starting opposite the enemies, everyone closing to their own
effective_range before they can attack (Kiting units retreat instead).
Built specifically to test the earlier Speed-vs-Range discussion: does a
backline caster's range actually let it stay out of melee reach, given
real PC Speed? Answer so far: yes, and it matters a lot more at higher
Levels, since a Ranged Spell's range scales with Level while a
Roster PC's Speed doesn't - the Ranged Caster archetype's win rate
against an on-level party drops hard under movement at Tier 3+ (see
sample_enemies.csv's Archetype rows and run `combat_sim.simulate(tier,
tier, movement=True)` against `sample_enemies.get_enemy('Generic Level N
Ranged Caster')` to reproduce). `movement=False` (the default) is the
exact original list-order-focus-fire behavior - the whole win-rate grid
this file's tuning depends on was built and stays validated against that
path, not the movement one.

Good Luck (`good_luck=N` on `run_fight`/`simulate`, `make_party`'s own
param) is wired the same way as Aimed Shot's best-of-2 flip - N stacks
means `flip_best_of(1 + N)` on the PC's own attack roll. Used once to
compare a simulated swing against `balance_weights_notes.md`'s
hand-derived Good Luck value (2.4) - worth knowing before reading too
much into a result: `good_luck` currently applies to every PC named in
`make_party`, for every attack, all fight. That's a much bigger grant
than the 2.4 figure prices (one stack, one flip), and it swings win
rate dramatically (all 4 PCs at Tier=Level: ~+45-50 points). To
approximate a single item/Technique on one PC, monkeypatch `make_party`
to zero the other three PCs' stacks back out before calling
`simulate()` - even that's still "every attack, all fight" rather than
a single flip, and moved win rate by a more moderate +7 to +9 points in
that test. Neither is directly convertible back to the 2.4 per-flip
figure without a real exchange-rate calibration (what win-rate swing
does an already-priced, fixed mechanic produce in this same sim) - not
built yet. `pc_attacks`/`pc_damage_dealt` (summed into `simulate()`'s
5th return value, damage per PC attack) exist for this kind of
comparison, but a pooled multi-PC average dilutes an effect that's only
live on some of the PCs - isolate the one PC actually being tested
before trusting that number.
"""
import random
import copy
import tunables as T
import movement
from sample_enemies import make_enemy
from party import make_party


def flip():
    return random.randint(1, 13)


def flip_best_of(n):
    return max(flip() for _ in range(n))


def effective_range(unit):
    """The distance a unit's own action actually reaches - PCs always
    use Melee (a flat MELEE_RANGE); enemies use their own attack_range
    if it's a real ranged Action, or MELEE_RANGE if it's 0 (a melee
    Action, per enemy_builder's own formula - 0 doesn't mean 'must be
    standing on the same point,' see tunables.MELEE_RANGE's comment)."""
    return unit.get('attack_range') or T.MELEE_RANGE


def resolve_movement(unit, target):
    """Moves `unit` this round per its own Battle Tactic, then reports
    whether it ends up within its own effective_range of `target` and
    can therefore attack this round. Kiting always retreats from
    `target` (per the designer: 'the most direct path away,' no
    conditional check for whether retreating is actually necessary) -
    everyone else closes toward `target`, stopping at their own
    effective_range rather than walking on top of it. Either way, the
    same range check afterward decides whether an attack is possible -
    a Kiting unit with real range can still retreat *and* attack the
    same round if its range covers the new distance; a melee unit that
    couldn't fully close the gap this round just doesn't get to act."""
    reach = effective_range(unit)
    if unit.get('battle_tactic') == 'Kiting':
        unit['pos'] = movement.move_away(unit['pos'], target['pos'], unit['speed'])
    else:
        unit['pos'] = movement.move_toward(unit['pos'], target['pos'], unit['speed'], stop_at=reach)
    # 1e-6 slack: move_toward's own stop_at logic can land a unit a
    # floating-point hair past `reach` (float division/subtraction isn't
    # exact) - without it, two units that just closed to melee range can
    # get flagged permanently out-of-range by a fraction no real ruler
    # would ever measure, freezing the fight into an unresolved draw
    # (found via a real seeded fight that stalemated at exactly this gap).
    return movement.distance(unit['pos'], target['pos']) <= reach + 1e-6


def _start_positions(n, x, spread=4):
    """n units spread evenly down a vertical line at x, centered on the
    arena - just enough to avoid stacking every unit on one exact point,
    no other formation logic."""
    mid = (n - 1) / 2
    return [(x, T.ARENA_SIZE / 2 + (i - mid) * spread) for i in range(n)]


def _closest(unit, candidates):
    """'Attacking the closest enemy is obvious' (the designer's own
    framing) - the movement-mode target rule for every Battle Tactic
    except Assassin (which already has its own low-Health targeting
    rule, unaffected by position). Also doubles as the retreat-from
    reference point for Kiting, since the nearest threat is the one
    worth running from."""
    return min(candidates, key=lambda c: movement.distance(unit['pos'], c['pos']))


def enemy_defense_for_pc_attack(target):
    """A PC's own weapon attack is opposed by Parry or Dodge, the
    target's choice (rulebook.md: "If multiple Defenses are stated, the
    target chooses which to use") - same rule pc_defense_for already
    applies to an enemy's own 'Parry/Dodge' Actions, just the reverse
    direction. Used to be hardcoded to target['parry'] alone; that broke
    badly once Powerful Spell's -99-Parry trick showed up (see
    tunables.ABILITY_COST) - a caster who's given up on Parry entirely
    isn't supposed to be an automatic hit every time, just one who'll
    always be defended by Dodge instead."""
    return max(target['parry'], target['dodge'])


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
    best possible card (13) couldn't clear the target's Defense, since
    that's a wasted action no one would actually take.

    Only when `needed == 0` (a normal hit is already doing something)
    does the more cautious "plenty of Skill Total to spare" judgment
    call from the rulebook's own Gambling text apply - gamble once more
    for the extra damage, but only if the *average* card (7) would still
    clear the target's Defense.
    """
    effective_skill = pc['skill_total'] - pc.get('crippled', 0)
    defense = enemy_defense_for_pc_attack(target)
    needed = max(0, target['physres'] - pc['damage'] + 1)
    max_possible = max(0, (effective_skill + 13 - defense) // 2)
    if needed > 0:
        return min(needed, max_possible)
    max_safe = max(0, (effective_skill + 7 - defense) // 2)
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


def run_fight(tier, enemy_level, n_enemies=4, max_rounds=30, seed=None, good_luck=0, movement=False):
    """`movement=True` turns on the optional 2D-arena mode (movement.py):
    PCs start at x=2, enemies at x=ARENA_SIZE-2 (tunables.ARENA_SIZE),
    spread down the y-axis (_start_positions), and every unit must move
    into its own effective_range of its target before it can attack this
    round (resolve_movement) - a unit that can't close the gap (or a
    Kiting unit that outruns its pursuer) just doesn't get to act.
    `movement=False` (the default) skips all of this and matches the
    original list-order-focus-fire behavior exactly - kept byte-identical
    on purpose so the already-validated win-rate grid never depends on
    this code path."""
    if seed is not None:
        random.seed(seed)
    pcs = make_party(tier, good_luck=good_luck)
    enemies = [copy.deepcopy(make_enemy(enemy_level)) for _ in range(n_enemies)]
    pc_attacks = 0
    pc_damage_dealt = 0

    if movement:
        for pc, pos in zip(pcs, _start_positions(len(pcs), x=2)):
            pc['pos'] = pos
        for e, pos in zip(enemies, _start_positions(len(enemies), x=T.ARENA_SIZE - 2)):
            e['pos'] = pos

    for rnd in range(1, max_rounds + 1):
        # Party's turn: each living PC attacks the first living enemy
        # (pure focus fire, no target choice) vs. whichever of the
        # enemy's Parry/Dodge is better for it (enemy_defense_for_pc_attack).
        # In movement mode, "first" becomes "closest," and a PC who can't
        # close into effective_range this round doesn't get to attack.
        for pc in pcs:
            if pc['health'] <= 0:
                continue
            targets = [e for e in enemies if e['health'] > 0]
            if not targets:
                break
            if movement:
                target = _closest(pc, targets)
                if not resolve_movement(pc, target):
                    continue
            else:
                target = targets[0]
            defense = enemy_defense_for_pc_attack(target)
            gambles = pc_gamble_count(pc, target)
            crippled = pc.get('crippled', 0)
            card = flip_best_of(1 + pc.get('good_luck', 0))  # Good Luck: flip 1 extra card per stack, keep the highest
            roll = pc['skill_total'] - crippled + card - 2 * gambles  # PCs attack with Melee, vs. the enemy's Parry/Dodge
            pc_attacks += 1
            if roll >= defense:
                dmg = max(0, pc['damage'] + gambles - target['physres'])
                protected = target.get('protected', 0)
                if protected > 0 and dmg > 0:
                    absorbed = min(dmg, protected)
                    target['protected'] -= absorbed
                    dmg -= absorbed
                target['health'] -= dmg
                pc_damage_dealt += dmg
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
                        party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs),
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)
        if all(p['health'] <= 0 for p in pcs):
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0,
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)

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
            elif movement:
                target = _closest(e, living_pcs)  # also Kiting's retreat-from reference point
            else:
                target = living_pcs[0]  # proxy for Hit Whatever / Hold the Line / Vanguard alike
            if movement and not resolve_movement(e, target):
                continue

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
                    # Same-round retarget after a kill: reuses whichever
                    # unit is already in range rather than re-checking
                    # movement, same "not a super intensive analysis"
                    # simplification as everywhere else in movement mode.
                    target = _closest(e, living_pcs) if movement else living_pcs[0]
        if all(p['health'] <= 0 for p in pcs):
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0,
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)

    return dict(winner='draw', rounds=max_rounds,
                party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs),
                pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)


def simulate(tier, enemy_level, n_enemies=4, trials=4000, good_luck=0, movement=False):
    results = {'party': 0, 'enemies': 0, 'draw': 0}
    rounds_list = []
    hp_list = []
    total_attacks = 0
    total_damage = 0
    for _ in range(trials):
        r = run_fight(tier, enemy_level, n_enemies=n_enemies, good_luck=good_luck, movement=movement)
        results[r['winner']] += 1
        rounds_list.append(r['rounds'])
        total_attacks += r['pc_attacks']
        total_damage += r['pc_damage_dealt']
        if r['winner'] == 'party':
            hp_list.append(r['party_hp_pct'])
    win_pct = results['party'] / trials * 100
    avg_rounds = sum(rounds_list) / len(rounds_list)
    avg_hp_on_win = (sum(hp_list) / len(hp_list) * 100) if hp_list else 0
    dmg_per_attack = total_damage / total_attacks if total_attacks else 0
    return win_pct, avg_rounds, avg_hp_on_win, results, dmg_per_attack


if __name__ == "__main__":
    win, rnds, hp, res, dpa = simulate(2, 2, trials=4000)
    print(f"Tier2 vs Level2: win={win:.1f}% rounds={rnds:.1f} hp_on_win={hp:.1f}% dmg/attack={dpa:.3f} raw={res}")
