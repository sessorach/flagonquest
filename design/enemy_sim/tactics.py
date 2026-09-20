"""
Small, pluggable "AI" for what a unit does on its own turn - who it
targets, how it moves, and (for a PC) whether it attacks normally or
does something else instead (currently: a support PC healing). Each of
these is a plain {name: function} registry keyed off a CSV column value
(`battle_tactic` for enemies - sample_enemies.csv's BattleTactic column
- `strategy` for PCs - see party.py) - add a new tactic/strategy by
writing one function with the matching signature and adding it to the
registry, not by adding another `if tactic == '...'` branch inside
combat_sim.py's run_fight. Keeps run_fight itself reading as "whose
turn, then dispatch," and keeps this file the one place to look when
asking "what can a unit's Battle Tactic/strategy actually do."

Every function here is pure decision logic - no card flips, no Health
changes beyond what a strategy function explicitly returns/mutates, no
trace/logging concerns (combat_sim.py's run_fight owns recording what
happened, via its own `trace` param - these functions just decide).
"""
import cards
import movement


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
    by the same range check every unit gets."""
    unit['pos'] = movement.move_away(unit['pos'], target['pos'], unit['speed'])


MOVEMENT_TACTICS = {
    'Kiting': move_kite,
}


def move_unit(unit, target, reach):
    fn = MOVEMENT_TACTICS.get(unit.get('battle_tactic'), move_approach)
    fn(unit, target, reach)


# ---- PC strategies: does this PC do something other than attack this
# round? Signature: (pc, party, log) -> bool - True if the PC did
# something else this round (skip their normal attack this turn
# entirely, no movement either), False if they should attack as normal.
# `log` is a one-argument callable (or None) for a strategy to report
# what it did - see combat_sim.py's `_log`/`trace` for the event shape a
# strategy is expected to pass it.

def strategy_support_healer(pc, party, log):
    """A hard-capped resource, not a per-round coin flip: `heal_uses_left`
    (party.py's Support paragraph, starts at hand_size // 4) is spent
    only once a living ally drops to half their max Health or below
    (standing in for Wounded, since this sim has no Shallow/Deep Health
    split) - "if necessary, ESPECIALLY if wounded" (the designer's own
    framing) becomes the whole rule once uses are this scarce. Each use
    approximates one casting of T105 Healing Magic at Level 1: heal 1
    Shallow Health, +1 more since the discarded card is assumed to
    always be a Heart (cards.chosen_matches - the player is choosing
    from their whole hand, not flipping blind, and only spending a
    quarter of it this way). No attack roll - Healing Magic isn't
    opposed - and the target is assumed reachable (an "adjacent ally"
    per its own Target text) without a real range check, since the
    party's 2x2 formation keeps everyone clustered together anyway."""
    if pc.get('heal_uses_left', 0) <= 0:
        return False
    wounded = [p for p in party if 0 < p['health'] <= p['max_health'] / 2]
    if not wounded:
        return False
    target = min(wounded, key=lambda p: p['health'])
    heal = 1 + (1 if cards.chosen_matches('Hearts') else 0)
    before = target['health']
    target['health'] = min(target['max_health'], target['health'] + heal)
    pc['heal_uses_left'] -= 1
    if log:
        log(unit=pc['name'], action='heal', target=target['name'],
            amount=target['health'] - before, target_hp_after=target['health'])
    return True


PC_STRATEGIES = {
    'support_healer': strategy_support_healer,
}


def resolve_pc_strategy(pc, party, log=None):
    """Every PC attacks normally by default ('attacker', or no strategy
    set at all) - only a PC with a registered strategy (a support
    healer, say) gets dispatched here at all. Returns True if the PC did
    something else this round (skip their attack), False otherwise."""
    fn = PC_STRATEGIES.get(pc.get('strategy'))
    return fn(pc, party, log) if fn else False
