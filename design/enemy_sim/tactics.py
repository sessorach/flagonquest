"""
Small, pluggable "AI" for what a unit does on its own turn - who it
targets, how it moves, how many attacks it gets, and (for a PC) whether
it attacks normally or does something else instead (currently: a
support PC healing). Each of these is a plain {name: function} registry
keyed off a CSV column value (`battle_tactic` for enemies -
sample_enemies.csv's BattleTactic column - `fighting_style` for
enemies' action economy - sample_enemies.csv's FightingStyle column -
`strategy` for PCs - see party.py) - add a new tactic/strategy/style by
writing one function with the matching signature and adding it to the
registry, not by adding another `if tactic == '...'` branch inside
combat_sim.py's run_fight. Keeps run_fight itself reading as "whose
turn, then dispatch," and keeps this file the one place to look when
asking "what can a unit's Battle Tactic/Fighting Style/strategy
actually do."

Every function here is pure decision logic - no card flips (that's
combat_sim.py's flip()/flip_best_of()/flip_worst_of(), and cards.py for
suit assumptions), no trace/logging concerns beyond the optional `log`
callback a few functions accept (combat_sim.py's run_fight owns
recording what happened, via its own `trace` param).

The whole file assumes rulebook.md's Action Point economy (see
tunables.AP_PER_TURN/MOVE_AP_COST/ATTACK_AP_COST): every unit gets 4 AP
a turn, a move action costs 1 AP (up to Speed meters, repeatable), and
an attack costs 2 AP - see combat_sim.py's spend_movement_ap and its
Party's/Enemies' turn loops for how a unit's AP actually gets spent
round by round, following whatever this file decides.
"""
import cards
import movement
import tunables as T


# ---- Targeting: which of the given targets does a unit go after? ----
# Signature: (unit, targets) -> one of targets. `targets` is always the
# already-filtered list of currently-living possible targets.

def target_closest(unit, targets):
    """'Attacking the closest enemy is obvious' (the designer's own
    framing) - the default once movement is on, for every Battle Tactic
    without its own targeting rule. Also doubles as Kiting's
    retreat-from reference point (move_kite below), since the nearest
    threat is the one worth running from."""
    return min(targets, key=lambda c: movement.distance(unit['pos'], c['pos']))


def target_first(unit, targets):
    """List-order focus fire - the default when movement is off, and the
    proxy for every Battle Tactic this sim doesn't otherwise model (Hit
    Whatever, Hold the Line, Vanguard alike)."""
    return targets[0]


def target_lowest_health(unit, targets):
    """Assassin: go for whoever's already hurt worst, unaffected by
    position - registered under 'Assassin' below."""
    return min(targets, key=lambda c: c['health'])


TARGETING = {
    'Assassin': target_lowest_health,
}


def select_target(unit, targets, movement_on):
    """Dispatches on unit.get('battle_tactic') - a PC has none set, so
    always falls through to the movement-aware default (closest/first),
    same as any enemy Battle Tactic without its own entry in TARGETING."""
    fn = TARGETING.get(unit.get('battle_tactic'))
    if fn:
        return fn(unit, targets)
    return (target_closest if movement_on else target_first)(unit, targets)


# ---- Movement: how does a unit move toward/away from its target? ----
# Signature: (unit, target, reach) -> None, mutates unit['pos'] in place.
# `reach` is the unit's own effective_range (combat_sim.effective_range).
# Each call here is exactly one MOVE_AP_COST-worth of movement (one move
# action - up to `speed` meters) - combat_sim.spend_movement_ap is what
# decides how many of these a unit's turn actually gets to spend.

def move_approach(unit, target, reach):
    """Close the distance, stopping `reach` meters short rather than
    walking on top of the target - the default for every Battle Tactic
    without its own entry in MOVEMENT_TACTICS."""
    unit['pos'] = movement.move_toward(unit['pos'], target['pos'], unit['speed'], stop_at=reach)


def move_kite(unit, target, reach):
    """Retreat along the straight line away from `target` (per the
    designer: 'the most direct path away') - no check for whether
    retreating is actually necessary this round, and `reach` is unused:
    a Kiting unit with real range can still retreat *and* attack the
    same round if its range covers the new distance, decided afterward
    by the same range check every unit gets. Kiting always spends
    exactly 1 move action (see combat_sim.spend_movement_ap) rather than
    however many AP allows - "keeps max range" is a positioning
    preference, not "flee as far as possible every turn."""
    unit['pos'] = movement.move_away(unit['pos'], target['pos'], unit['speed'])


MOVEMENT_TACTICS = {
    'Kiting': move_kite,
}


def move_unit(unit, target, reach):
    fn = MOVEMENT_TACTICS.get(unit.get('battle_tactic'), move_approach)
    fn(unit, target, reach)


# ---- Fighting Style: an enemy's own action economy ----
# ENEMY_ENCOUNTER_DESIGN.md's own table (ENEMY_ENCOUNTER_DESIGN.md,
# "Battle Tactics and Fighting Style"):
#
#   Flurry      - Attacks/supports twice if possible
#   Guarded     - Attacks/supports once; if it didn't move, attacks
#                 against its Dodge/Parry have Bad Luck this turn
#   Aimed Shot  - Only attacks once, but it has Good Luck
#   Skirmisher  - Only attacks once, but can move up to 3 times
#
# "Only one of the four Fighting Styles (Flurry) is a literal
# double-attack - the other three are deliberately built as
# *alternatives* to a flat double-attack" - mechanically, that means
# Flurry is simply *uncapped* (spends AP on attacks same as anything
# with no Fighting Style at all - a PC, which always behaves this way,
# per the designer's own "bread and butter" framing: move into range,
# attack, attack again if the AP's there) while the other three
# deliberately give up a 2nd attack even when AP would otherwise allow
# one, in exchange for their own compensating bonus. Since AP_PER_TURN
# is 4 and ATTACK_AP_COST is 2, 2 attacks is the hard ceiling regardless
# - "uncapped" and "capped at 2" are the same thing in practice.
ATTACK_CAP = {
    'Guarded': 1,
    'Aimed Shot': 1,
    'Skirmisher': 1,
    # Flurry, and no Fighting Style at all (every PC) -> absent -> uncapped.
}


def attack_cap(unit):
    """None (uncapped, i.e. "however many 2-AP attacks the turn's AP
    allows" - at most 2) unless this unit's Fighting Style deliberately
    gives up its 2nd attack for something else."""
    return ATTACK_CAP.get(unit.get('fighting_style'))


# Movement itself has no separate cap of its own - every unit spends
# "as many action points as required" closing distance (the designer's
# own framing), then whatever's left goes to attacks; a unit that needs
# its whole turn's worth of AP just to close the gap simply doesn't get
# to attack that round (see combat_sim.spend_movement_ap). Skirmisher's
# own "can move up to 3 times" isn't separately encoded as a result -
# nothing here artificially caps any unit's movement below what its AP
# already allows, so Skirmisher doesn't need a higher cap than anyone
# else; its real distinguishing rule is attack_cap above (1, same as
# Guarded/Aimed Shot). Worth revisiting if Skirmisher ever needs a
# sharper mechanical distinction - it isn't used by any current
# sample_enemies.csv row.


def max_move_actions(unit):
    """How many move actions (MOVE_AP_COST each) a unit is willing to
    spend approaching its target before it must stop and preserve
    ATTACK_AP_COST for its (at least one) attack - 2 for everything
    except Skirmisher, which trades its own capped-at-1 attack for real
    extra mobility instead ("can move up to 3 times"), per the table
    above. Kiting ignores this entirely (always exactly 1 retreat
    action, see move_kite) - this only governs closing distance."""
    return 3 if unit.get('fighting_style') == 'Skirmisher' else 2


def guarded_bonus_active(unit):
    """Whether `unit` is currently benefiting from Guarded's stand-still
    bonus - set at the end of its own last turn (combat_sim.run_fight)
    if its Fighting Style is Guarded and it made zero move actions that
    turn, and checked here by whoever's attacking it now. Persists from
    one of the unit's turns to the opposing side's very next turn (the
    two sides alternate within a round, so this is a one-step-lagged
    "held its ground" bonus, not an instant same-turn one) - see
    combat_sim.py's own note on the exact timing."""
    return bool(unit.get('guarded_active'))


def defense_has_bad_luck(target, opp_def):
    """Guarded's bonus specifically covers "attacks against its
    Dodge/Parry" - a weapon-style opposed Defense, not a Bodily/Mental
    spell attack (Vulnerable's own -1 stacks already carve out that same
    Dodge/Parry-vs-Bodily/Mental split - see combat_sim.pc_defense_for).
    """
    return guarded_bonus_active(target) and opp_def in ('Parry/Dodge', 'Dodge')


# ---- PC strategies: does this PC spend part of its turn on something
# other than attacking? Signature: (pc, party, log) -> AP spent (0 if
# the PC did nothing special and should just proceed to move+attack
# with its full turn). `log` is a one-argument callable (or None) for a
# strategy to report what it did - see combat_sim.py's `_log`/`trace`
# for the event shape a strategy is expected to pass it. AP spent here
# comes out of the same AP_PER_TURN budget as everything else in the
# turn - a strategy that spends less than the full 4 leaves the rest
# for the unit's normal move-then-attack behavior afterward.

def strategy_support_healer(pc, party, log):
    """A hard-capped resource, not a per-round coin flip: `heal_uses_left`
    (party.py's Support paragraph, starts at hand_size // 4) is spent
    only once a living ally drops to half their max Health or below
    (standing in for Wounded, since this sim has no Shallow/Deep Health
    split) - "if necessary, ESPECIALLY if wounded" (the designer's own
    framing) becomes the whole rule once uses are this scarce. Each use
    approximates one casting of T105 Healing Magic at Level 1 - its own
    techniques.csv row costs 1 AP (T.HEALING_MAGIC_AP_COST), not the
    standard 2, leaving 3 AP for this PC to still move and attack the
    same turn - "use its full action pool," per the designer, applies
    to a healer too, not just straight attackers. Heals 1 Shallow
    Health, +1 more since the discarded card is assumed to always be a
    Heart (cards.chosen_matches - the player is choosing from their
    whole hand, not flipping blind, and only spending a quarter of it
    this way). No attack roll - Healing Magic isn't opposed - and the
    target is assumed reachable (an "adjacent ally" per its own Target
    text) without a real range check, since the party's 2x2 formation
    keeps everyone clustered together anyway. Returns 0 (spent nothing,
    proceed to a normal turn) if there's no use left or nobody's
    wounded enough to spend one on."""
    if pc.get('heal_uses_left', 0) <= 0:
        return 0
    wounded = [p for p in party if 0 < p['health'] <= p['max_health'] / 2]
    if not wounded:
        return 0
    target = min(wounded, key=lambda p: p['health'])
    heal = 1 + (1 if cards.chosen_matches('Hearts') else 0)
    before = target['health']
    target['health'] = min(target['max_health'], target['health'] + heal)
    pc['heal_uses_left'] -= 1
    if log:
        log(unit=pc['name'], action='heal', target=target['name'],
            amount=target['health'] - before, target_hp_after=target['health'])
    return T.HEALING_MAGIC_AP_COST


PC_STRATEGIES = {
    'support_healer': strategy_support_healer,
}


def resolve_pc_strategy(pc, party, log=None):
    """Every PC attacks normally by default ('attacker', or no strategy
    set at all) - only a PC with a registered strategy (a support
    healer, say) gets dispatched here at all. Returns the AP that
    strategy spent (0 if it did nothing, e.g. no uses left or nothing to
    do) - the caller spends whatever's left of the turn's AP as normal
    (move, then attack)."""
    fn = PC_STRATEGIES.get(pc.get('strategy'))
    return fn(pc, party, log) if fn else 0
