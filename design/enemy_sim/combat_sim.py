"""
Monte Carlo combat loop: 4 party members vs. N copies of one enemy,
repeated many times with fresh card flips to estimate win rate, average
rounds to resolve, and party Health remaining on a win.

Deliberately simplified, not a full combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of what's
NOT modeled (no Extra Successes from suit-pool matching, no Techniques/
items, no distinct PC roles, no real initiative, rough Battle Tactics
targeting proxies). Positioning has a first pass now (see `movement=True`
below), off by default. PCs DO now Gamble (see
`pc_gamble_count`) - added specifically because armored enemies
otherwise had no counter-play modeled at all. Good for catching relative
differences between builds and Tiers; the exact win percentages aren't
precise predictions of real play.

Every "AI" decision a unit makes on its own turn - who it targets, how
it moves, whether a PC attacks or does something else (healing) - lives
in `tactics.py` as a small named-function registry, not as `if`
branches in this file's `run_fight`; "which suit is this card"
assumptions (currently just Healing Magic's Hearts check) live the same
way in `cards.py`. Both exist so a new tactic/strategy/card-rule is one
function plus one registry entry, not a new conditional threaded
through run_fight - see either module's own docstring before adding
one. `run_fight(..., trace=[])` records a full round-by-round log of
whatever a fight actually did (positions, moves, attacks, heals) for
one specific run rather than just its final tally - `narrate_fight.py`
renders one into a position table plus a combat log, for actually
looking at what this simulator does instead of only reading aggregate
win rates.

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

The same question from the PC side: `sample_pcs.csv`'s `Weapon` column
(see party.py's own docstring) adds three ranged reference builds -
Sable (Light Bow, 15m fixed range), Rook (Light Thrown, range = 3 x
Body - 9m for her own Body 3), Wren (War Magic + Lance, range = Sorcery
Skill Total - 6m). Tested as 4-clone parties (`party.make_party_of`)
against the Level 1 Roster enemy (Marsh Viper Scout, Speed 3, melee
Flurry): Sable's 13m head start over the enemy's ~2m melee-closing
distance is enough to win the fight before the enemy ever gets an
attack in most of the time (28% -> 99.8% under movement); Rook's
smaller 7m head start still helps a lot (2.5% -> 43%) but doesn't
dominate; Wren's head start is only 4m - not enough to matter against
an equal-Speed opponent (2.6% -> 1.3%, i.e. no real change, possibly
slightly worse from the extra rounds movement adds before contact).
Range alone isn't the whole story either: a PC's own effective_range
gates *their* attack too, same as an enemy's - a short-ranged build still
has to close most of the gap itself before landing a hit, it just needs
less of a head start than a melee unit to get there first.

Follow-up with a real mixed party (`party.make_party_from([names])`,
not 4 clones): War Magic's damage now actually resolves as Fire, not
Physical - `pc['dmg_type']`/`pc['opp_def']` (party.py's Weapon
paragraph) route a Fire attack through the target's `elemres` instead
of `physres` (see `enemy_resist_for_pc_attack`) and War Magic's own
Dodge-only opposed Defense instead of Parry/Dodge (see
`enemy_defense_for_pc_attack`) - this matters because tunables.ARMOR
only bumps `physres`, so a heavily-armored enemy's `elemres` stays
comparatively low; Wren draws real benefit from this that Sable/Rook's
Physical attacks don't. Movement mode's start now matches "spaced out
slightly but not opposite ends": the party starts in a compact 2x2
block (`_party_formation`, tunables.PARTY_FORMATION_SPACING) instead of
the enemies' own spread line, and the two front lines start a random
tunables.START_GAP_RANGE (5-10m) apart by default instead of the
original fixed 16m corner-to-corner gap - `run_fight`'s own `start_gap`
param overrides this for a controlled comparison. That comparison
matters: sweeping start_gap from 5m to 16m against the Full Utility
comp below showed a real cliff between 5m (~5% win) and 6-8m (~18-31%),
then a plateau from ~8m on - Sable's 15m range already dominates well
before anything gets that close, and Wren's 6m range is already in (or
almost in) range at any gap 6m or wider, so most of the movement
benefit is already captured by 8m; a shorter gap mostly just costs the
ranged builds their head start.

The mixed-party comparisons themselves (Hilde/Browndog/Carrick/Jackal
all-melee; various Sable/Wren/Beornhard swaps) all landed far below the
Roster's own ~50% at n_enemies=4 (3-17% depending on comp/movement) -
**not** a sign these builds or movement are bad, but a reminder that
n_enemies=4 vs a Level 1 Roster enemy is exactly the matchup the Roster
was *calibrated* to be a fair fight for 4 identical, smoothed Roster
PCs, not 4 spikier named reference builds sharing one "combat slot"
with a PC who isn't fighting every round. Re-run at n_enemies=2 (a
lighter, more proportionate encounter) to isolate composition from that
calibration gap: swapping a 4th melee/caster/support into
Hilde+Browndog+Sable put Wren (2nd caster) on top (~96-97%), with
Beornhard (healer, but see below) close behind (~91%, beating a 4th
plain fighter under movement: 91.2% vs 79.9% - the extra fighter, all
melee, doesn't get movement's range benefit the way a caster does, and
seemingly loses more to it than Beornhard's healing gains).

`tactics.strategy_support_healer`'s heal-or-attack rule is a hard-capped
resource, not a per-round coin flip: `pc['heal_uses_left']` starts at hand_size
// 4 (party.py's Support paragraph - 1 use for Beornhard specifically,
his Cunning+Mind being what it is), spent only once a living ally drops
to half Health or below (standing in for Wounded, since there's no
Shallow/Deep Health split here) - "if necessary, ESPECIALLY if wounded"
reads as "only when it's actually needed," given how few uses there
are. Every other round, a support PC just attacks normally like anyone
else - Beornhard's own Melee (2, up from an original 1, paid for by
dropping Medicine 2 to 1 - see his sample_pcs.csv Notes) makes that a
real contribution (Parry 11, Damage 6) instead of dead weight, which is
exactly what closed most of the gap to a dedicated 2nd caster or 4th
fighter above - an earlier version of this build that healed on a ~25%
per-round chance and fought weakly the rest of the time scored
noticeably worse in the same matchups (n_enemies=2, movement=True:
85.4% vs this version's 91.2%).

The heal amount itself later moved from "1 + a 25% chance of +1 more"
to a flat +2 every time (cards.chosen_matches always true now, per the
designer: a discarded card is chosen from the player's whole hand, not
flipped blind, and Healing Magic only ever spends a quarter of that
hand this way - see cards.py's own module docstring). Barely moved win
rate at all (n_enemies=2: 91.2% -> 90.9%/91.4% across two reruns, well
within trial noise) - the reason is the same hard cap that made the
melee fix matter: Beornhard only has 1 heal_uses_left, so the entire
swing from "usually heals 1, sometimes 2" to "always heals 2" is a
one-time +0.75 HP difference across a whole fight already decided by
dozens of other rolls. A build with a bigger hand (more heal uses)
would see this matter more; Beornhard specifically doesn't.

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
import tactics
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
    """Moves `unit` this round per its own Battle Tactic (tactics.
    move_unit - Kiting retreats, everything else closes in, stopping
    `reach` meters short rather than walking on top of `target`), then
    reports whether it ends up within its own effective_range and can
    therefore attack this round. Either way, the same range check
    afterward decides whether an attack is possible - a Kiting unit with
    real range can still retreat *and* attack the same round if its
    range covers the new distance; a melee unit that couldn't fully
    close the gap this round just doesn't get to act."""
    reach = effective_range(unit)
    tactics.move_unit(unit, target, reach)
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
    no other formation logic. Still used for the enemy side; the party
    uses _party_formation instead (see below)."""
    mid = (n - 1) / 2
    return [(x, T.ARENA_SIZE / 2 + (i - mid) * spread) for i in range(n)]


def _party_formation(x):
    """The party's 4 starting positions as a compact 2x2 block centered
    on the arena's y-midpoint - 'for simplicity's sake,' per the
    designer, rather than the single-file line _start_positions gives
    the enemies. Assumes exactly 4 PCs, same as the rest of this file."""
    mid = T.ARENA_SIZE / 2
    half = T.PARTY_FORMATION_SPACING / 2
    return [(x - half, mid - half), (x + half, mid - half),
            (x - half, mid + half), (x + half, mid + half)]


def _random_front_lines(start_gap=None):
    """The party's and enemies' starting x-positions, `start_gap` meters
    apart (tunables.START_GAP_RANGE if not given - a random 5-10m each
    fight) and centered in the arena - 'spaced out slightly but not
    opposite ends,' per the designer, replacing the original fixed 16m
    corner-to-corner start. Returns (party_x, enemy_x)."""
    gap = start_gap if start_gap is not None else random.uniform(*T.START_GAP_RANGE)
    mid = T.ARENA_SIZE / 2
    return mid - gap / 2, mid + gap / 2


def enemy_defense_for_pc_attack(pc, target):
    """A PC's own weapon attack is opposed by Parry or Dodge, the
    target's choice (rulebook.md: "If multiple Defenses are stated, the
    target chooses which to use") - same rule pc_defense_for already
    applies to an enemy's own 'Parry/Dodge' Actions, just the reverse
    direction. Used to be hardcoded to target['parry'] alone; that broke
    badly once Powerful Spell's -99-Parry trick showed up (see
    tunables.ABILITY_COST) - a caster who's given up on Parry entirely
    isn't supposed to be an automatic hit every time, just one who'll
    always be defended by Dodge instead. `pc['opp_def']` (see party.py's
    Weapon paragraph) lets a Spell attack like War Magic override this
    to Dodge alone, matching its own "Dodge or Vital, chosen when you
    learn this" rule instead of a weapon's Parry-or-Dodge one."""
    if pc.get('opp_def') == 'Dodge':
        return target['dodge']
    return max(target['parry'], target['dodge'])


def enemy_resist_for_pc_attack(pc, target):
    """Which of the target's own Resist pools a PC's attack draws from -
    Physical (physres) for a weapon attack, or elemres (enemy_builder.
    py's single elemental-Resist stand-in for Fire/Frost/Brilliant/
    Shadow) for a Spell attack like War Magic, per pc['dmg_type'] (see
    party.py's Weapon paragraph). tunables.ARMOR only adds to physres,
    never elemres, so a heavily-armored enemy's elemental Resist doesn't
    scale up the way its Physical Resist does - a Fire-damage PC can
    come out ahead against a Tank/Heavy-Armor build in a way a
    same-Damage weapon attack doesn't. That's the real
    armor-doesn't-stop-magic tradeoff this is modeling, not a bug."""
    if pc.get('dmg_type') == 'Fire':
        return target['elemres']
    return target['physres']


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
    defense = enemy_defense_for_pc_attack(pc, target)
    resist = enemy_resist_for_pc_attack(pc, target)
    needed = max(0, resist - pc['damage'] + 1)
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


def _log(trace, **event):
    """Appends one structured event to `trace` if it's a list (i.e. the
    caller actually wants a trace), a no-op otherwise - every call site
    in run_fight stays a single line either way, so tracing never grows
    its own parallel set of `if trace:` branches. See run_fight's own
    docstring for the event shapes this produces and narrate_fight.py
    for a renderer that consumes them."""
    if trace is not None:
        trace.append(event)


def run_fight(tier, enemy_level, n_enemies=4, max_rounds=30, seed=None, good_luck=0, movement=False, start_gap=None,
              trace=None):
    """`movement=True` turns on the optional 2D-arena mode (movement.py):
    the party starts in a compact 2x2 block (_party_formation), enemies
    spread down the y-axis (_start_positions), the two sides' front
    lines a random tunables.START_GAP_RANGE meters apart by default
    (`start_gap` overrides this with a fixed distance instead, e.g. for
    a controlled before/after comparison - see _random_front_lines).
    Every unit must move into its own effective_range of its target
    before it can attack this round (resolve_movement) - a unit that
    can't close the gap (or a Kiting unit that outruns its pursuer) just
    doesn't get to act. `movement=False` (the default) skips all of this
    and matches the original list-order-focus-fire behavior exactly -
    kept byte-identical on purpose so the already-validated win-rate
    grid never depends on this code path.

    `trace`: pass a list (e.g. `trace=[]`) to have this call record what
    happened, round by round, instead of just returning the final tally
    - meant for actually looking at one fight (`narrate_fight.py`), not
    for `simulate()`'s thousands of trials, so it's `None` (skip
    entirely, via `_log`) by default. Events are plain dicts, always
    carrying `round`; a `type='positions'` event (movement mode only,
    once per round, before any of that round's actions) snapshots every
    living unit's `pos`/`health`; everything else carries `side`
    ('party'/'enemy') and `unit`, and is either `action='move'` (this
    unit couldn't reach its target this round - `pos`, `in_range=False`),
    `action='attack'` (`target`, `roll`, `defense`, `hit`, `dmg`,
    `target_hp_after`), or whatever a PC's own strategy function logs
    (`tactics.strategy_support_healer` logs `action='heal'` - see
    tactics.py's own `log` parameter). A final `type='result'` event
    carries `winner`."""
    if seed is not None:
        random.seed(seed)
    pcs = make_party(tier, good_luck=good_luck)
    enemies = [copy.deepcopy(make_enemy(enemy_level)) for _ in range(n_enemies)]
    # Unlike PCs (party.py already suffixes each copy - "Hilde1",
    # "Hilde2"), every enemy copy comes back from make_enemy with the
    # exact same 'name' - fine when nothing ever needs to tell two
    # copies apart, but a real problem for a trace/log that does (see
    # `trace` below) - four identical "Marsh Viper Scout" entries are
    # indistinguishable. `name` is cosmetic only (nothing dispatches
    # game logic on it), so it's safe to suffix here unconditionally.
    for i, e in enumerate(enemies, 1):
        e['name'] = f"{e['name']} {i}"
    pc_attacks = 0
    pc_damage_dealt = 0

    if movement:
        party_x, enemy_x = _random_front_lines(start_gap)
        for pc, pos in zip(pcs, _party_formation(party_x)):
            pc['pos'] = pos
        for e, pos in zip(enemies, _start_positions(len(enemies), x=enemy_x)):
            e['pos'] = pos

    for rnd in range(1, max_rounds + 1):
        # `trace` (see run_fight's own docstring) gets one closure per
        # side per round, not per unit - cheap enough that a caller who
        # isn't tracing (every Monte Carlo trial) pays nothing beyond
        # the `is not None` checks inside _log itself.
        party_log = (lambda **kw: _log(trace, round=rnd, side='party', **kw)) if trace is not None else None
        enemy_log = (lambda **kw: _log(trace, round=rnd, side='enemy', **kw)) if trace is not None else None
        if movement:
            _log(trace, round=rnd, type='positions',
                 party=[{'unit': p['name'], 'pos': p['pos'], 'health': p['health']} for p in pcs if p['health'] > 0],
                 enemies=[{'unit': e['name'], 'pos': e['pos'], 'health': e['health']} for e in enemies if e['health'] > 0])

        # Party's turn: each living PC attacks the closest/first living
        # enemy (tactics.select_target - PCs have no Battle Tactic of
        # their own, so this always falls to the movement-aware default)
        # vs. whichever of the enemy's Defenses is worse for it
        # (enemy_defense_for_pc_attack) - unless a PC's own strategy
        # (tactics.resolve_pc_strategy - a support healer, say) does
        # something else with their turn instead.
        for pc in pcs:
            if pc['health'] <= 0:
                continue
            if tactics.resolve_pc_strategy(pc, pcs, log=party_log):
                continue  # spent this turn on something other than attacking
            targets = [e for e in enemies if e['health'] > 0]
            if not targets:
                break
            target = tactics.select_target(pc, targets, movement)
            if movement and not resolve_movement(pc, target):
                _log(trace, round=rnd, side='party', unit=pc['name'], action='move', pos=pc['pos'], in_range=False)
                continue
            defense = enemy_defense_for_pc_attack(pc, target)
            resist = enemy_resist_for_pc_attack(pc, target)
            gambles = pc_gamble_count(pc, target)
            crippled = pc.get('crippled', 0)
            card = flip_best_of(1 + pc.get('good_luck', 0))  # Good Luck: flip 1 extra card per stack, keep the highest
            roll = pc['skill_total'] - crippled + card - 2 * gambles  # PCs attack vs. the enemy's opposed Defense (pc['opp_def'])
            pc_attacks += 1
            hit = roll >= defense
            dmg = 0
            if hit:
                dmg = max(0, pc['damage'] + gambles - resist)
                protected = target.get('protected', 0)
                if protected > 0 and dmg > 0:
                    absorbed = min(dmg, protected)
                    target['protected'] -= absorbed
                    dmg -= absorbed
                target['health'] -= dmg
                pc_damage_dealt += dmg
            if party_log:
                party_log(unit=pc['name'], action='attack', target=target['name'], roll=roll, defense=defense,
                           hit=hit, dmg=dmg, target_hp_after=target['health'])
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
            _log(trace, round=rnd, type='result', winner='party')
            return dict(winner='party', rounds=rnd,
                        party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs),
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)
        if all(p['health'] <= 0 for p in pcs):
            _log(trace, round=rnd, type='result', winner='enemies')
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0,
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)

        # Enemies' turn: Fighting Style sets attack count, Battle Tactics
        # picks the target (tactics.select_target - rough proxies, not a
        # real implementation, see module docstring).
        for e in enemies:
            if e['health'] <= 0:
                continue
            abilities = e.get('abilities', [])
            if 'Durable' in abilities and e.get('protected', 0) < 4:
                e['protected'] = e.get('protected', 0) + 1
            living_pcs = [p for p in pcs if p['health'] > 0]
            if not living_pcs:
                break
            target = tactics.select_target(e, living_pcs, movement)
            if movement and not resolve_movement(e, target):
                _log(trace, round=rnd, side='enemy', unit=e['name'], action='move', pos=e['pos'], in_range=False)
                continue

            fighting_style = e.get('fighting_style', 'Guarded')
            n_attacks = 2 if fighting_style == 'Flurry' else 1
            for _ in range(n_attacks):
                roll = e['accuracy'] + (flip_best_of(2) if fighting_style == 'Aimed Shot' else flip())
                opp_def_val = pc_defense_for(target, e['opp_def'])
                hit = roll >= opp_def_val
                dmg = 0
                if hit:
                    dmg = max(0, e['attack_damage'] - target.get('physres', 0))
                    target['health'] -= dmg
                    if 'Strike (Crippling)' in abilities:
                        target['crippled'] = target.get('crippled', 0) + 1
                    if 'Strike (Vulnerable)' in abilities:
                        target['vulnerable'] = target.get('vulnerable', 0) + 1
                    if 'Poison (Bleeding)' in abilities:
                        target['bleeding'] = target.get('bleeding', 0) + 2
                if enemy_log:
                    enemy_log(unit=e['name'], action='attack', target=target['name'], roll=roll, defense=opp_def_val,
                               hit=hit, dmg=dmg, target_hp_after=target['health'])
                if target['health'] <= 0:
                    living_pcs = [p for p in pcs if p['health'] > 0]
                    if not living_pcs:
                        break
                    # Same-round retarget after a kill: reuses the same
                    # movement-aware default rather than re-checking a
                    # Battle-Tactic-specific rule like Assassin's, same
                    # "not a super intensive analysis" simplification as
                    # everywhere else in movement mode.
                    target = (tactics.target_closest if movement else tactics.target_first)(e, living_pcs)
        if all(p['health'] <= 0 for p in pcs):
            _log(trace, round=rnd, type='result', winner='enemies')
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0,
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)

    _log(trace, round=max_rounds, type='result', winner='draw')
    return dict(winner='draw', rounds=max_rounds,
                party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs),
                pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)


def simulate(tier, enemy_level, n_enemies=4, trials=4000, good_luck=0, movement=False, start_gap=None):
    results = {'party': 0, 'enemies': 0, 'draw': 0}
    rounds_list = []
    hp_list = []
    total_attacks = 0
    total_damage = 0
    for _ in range(trials):
        r = run_fight(tier, enemy_level, n_enemies=n_enemies, good_luck=good_luck, movement=movement, start_gap=start_gap)
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
