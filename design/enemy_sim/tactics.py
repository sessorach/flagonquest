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
recording what happened, via its own `trace` param). One exception:
sift_bonus's flat 1-in-4 roll (Hand of Chaos's own designer-specified
simplification) isn't a card flip at all, just a plain probability
check, so it uses `random` directly rather than combat_sim.py's
card-flipping helpers.

The whole file assumes rulebook.md's Action Point economy (see
tunables.AP_PER_TURN/MOVE_AP_COST/ATTACK_AP_COST): every unit gets 4 AP
a turn, a move action costs 1 AP (up to Speed meters, repeatable), and
an attack costs 2 AP - see combat_sim.py's spend_movement_ap and its
Party's/Enemies' turn loops for how a unit's AP actually gets spent
round by round, following whatever this file decides.
"""
import cards
import movement
import random
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


def target_straggler(unit, targets):
    """Hanforth's own Battle Tactic ('he may as well be attacking when
    he can, but not moving too close to too many enemies' - the
    designer's own framing): go after whichever target is most cut off
    from its own side, approximated as the fewest other living targets
    within 5m of it (ties broken by distance to this unit, same
    preference target_closest already has) - a support PC who'd rather
    finish off an isolated straggler than wade into the main clump, so
    closing on his own target doesn't also put him in range of a bunch
    of others. Needs positions (`movement=True`); falls back to
    target_first under static mode, same as every other position-aware
    tactic in this file."""
    if 'pos' not in unit:
        return target_first(unit, targets)

    def isolation(t):
        nearby = sum(1 for o in targets if o is not t and movement.distance(t['pos'], o['pos']) <= 5)
        return (nearby, movement.distance(unit['pos'], t['pos']))
    return min(targets, key=isolation)


def target_kiter(unit, targets):
    """'Kite Hunter': a PC who'd rather chase down whoever's trying to
    stay out of reach than fight whoever's already in front of them -
    Hilde-style priority targeting for a melee duelist who wants her
    Parting Shot (T076) to actually have something to punish, rather
    than falling back to plain closest/focus-wounded and maybe never
    ending up adjacent to the one enemy that matters for it. Prefers
    any living target whose own `battle_tactic` is 'Kiting'
    (sample_enemies.csv's own column) over anything else, closest
    among those if there's more than one; falls back to
    target_closest's own preference (or target_first under static
    mode) when no Kiter is present, same "don't invent a target that
    isn't there" shape as every other tactic here."""
    kiters = [t for t in targets if t.get('battle_tactic') == 'Kiting']
    pool = kiters if kiters else targets
    if 'pos' not in unit:
        return target_first(unit, pool)
    return target_closest(unit, pool)


def target_focus_wounded(unit, targets, allies):
    """The base party strategy (the designer's own priority order, "in
    order: attack twice if possible, focus fire on the most wounded
    enemy, attack an enemy closest to the entire party so it can be
    focused") - attacking twice needs no targeting logic at all (every
    PC is already uncapped, see attack_cap's own comment: no Fighting
    Style means "however many 2-AP attacks the turn's AP allows," which
    is exactly 2 whenever nothing else ate the AP first), so this
    function is priorities 2 and 3. Primary: whoever's already hurt
    worst (same read as target_lowest_health/Assassin). Tiebreak (most
    often turn 1, when every enemy's still at full Health): whichever
    enemy the whole party is collectively closest to - `party_reach`
    sums every living ally's own distance to a candidate, so a target
    the party's already clustered near beats one that's closer to this
    one PC alone but far from the rest, a rough facsimile of "let's all
    go for that one" without any real multi-turn coordination. Falls
    back to Health alone (list order breaks any remaining tie) when
    there's no `pos` to measure with (movement=False)."""
    if 'pos' not in unit:
        return min(targets, key=lambda t: t['health'])

    def party_reach(t):
        return sum(movement.distance(a['pos'], t['pos']) for a in allies if 'pos' in a)
    return min(targets, key=lambda t: (t['health'], party_reach(t)))


TARGETING = {
    'Assassin': target_lowest_health,
    'Straggler Hunter': target_straggler,
    'Kite Hunter': target_kiter,
}


def select_target(unit, targets, movement_on, allies=None):
    """Dispatches on unit.get('battle_tactic') (sample_enemies.csv's own
    BattleTactic column for enemies, sample_pcs.csv's Battle Tactic
    column for the rare PC that wants one, e.g. Hanforth's 'Straggler
    Hunter') - a unit with none set falls through to `allies`'s own
    default (target_focus_wounded, the base party strategy - see its
    own docstring) when `allies` is given (currently only _take_pc_turn
    passes one; enemies keep the older closest/first fallback, since
    the designer's ask was specifically about the party's own
    strategy), otherwise the plain movement-aware default (closest/
    first, used for enemies and any other caller without an `allies`
    list)."""
    fn = TARGETING.get(unit.get('battle_tactic'))
    if fn:
        return fn(unit, targets)
    if allies is not None:
        return target_focus_wounded(unit, targets, allies)
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
    approximates one casting of T105 Healing Magic - its own
    techniques.csv row costs 1 AP (T.HEALING_MAGIC_AP_COST) regardless
    of the Spell's own Level, leaving 3 AP for this PC to still move and
    attack the same turn - "use its full action pool," per the
    designer, applies to a healer too, not just straight attackers.
    Heals 1 Shallow Health, + `pc['heal_cards']` more (T105's own Cost
    is "Discard [Level] cards," so a Level 2 Healing Magic discards 2 -
    each assumed a Heart, same guaranteed-favorable-discard
    simplification every other Card Technique makes, via
    cards.chosen_matches), + `pc['heal_bonus']` flat (any Vitality-style
    healing-boost feature's own point total, summed once in party.py
    rather than re-parsed here). Both default to 1/0 (party.py's own
    Weapon/Heal paragraph) - a Level-1-with-no-features build like the
    original Beornhard's still heals exactly 1 + 1 + 0 = 2, unchanged.
    No attack roll - Healing Magic isn't opposed. The target must be
    within `pc['heal_range']` if that's set (party.py's own Heal Range
    paragraph - blank/None means no check at all, the original "adjacent
    ally, assumed reachable" behavior); only enforced when both units
    have a `pos` (movement=True), since there's nothing to check under
    the static default. Returns 0 (spent nothing, proceed to a normal
    turn) if there's no use left or nobody in range is wounded enough to
    spend one on."""
    if pc.get('heal_uses_left', 0) <= 0:
        return 0
    wounded = [p for p in party if 0 < p['health'] <= p['max_health'] / 2]
    heal_range = pc.get('heal_range')
    if heal_range is not None and 'pos' in pc:
        wounded = [p for p in wounded if 'pos' in p and movement.distance(pc['pos'], p['pos']) <= heal_range]
    if not wounded:
        return 0
    target = min(wounded, key=lambda p: p['health'])
    hearts = sum(1 for _ in range(pc.get('heal_cards', 1)) if cards.chosen_matches('Hearts'))
    heal = 1 + hearts + pc.get('heal_bonus', 0)
    before = target['health']
    target['health'] = min(target['max_health'], target['health'] + heal)
    pc['heal_uses_left'] -= 1
    if log:
        log(unit=pc['name'], action='heal', target=target['name'],
            amount=target['health'] - before, target_hp_after=target['health'], via='Healing Magic')
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


# ---- Card Techniques: a PC technique whose own cost is "discard a
# card," not AP (techniques.csv's own Action/Cost columns - Second Wind,
# Perfect Strike and Warmage's Reserves are each literally "0 AP",
# Bottomless Bottles' Cost is card-based too, though its own Action is a
# pre-combat 10-minute crafting step - see party.py's Card Techniques
# paragraph for the shared budget these all draw from
# (`card_uses_left`), computed once from hand_size the same "quick
# check, not real hand/suit tracking" way heal_uses_left already is.
# These three don't share one call signature the way TARGETING/
# MOVEMENT_TACTICS/PC_STRATEGIES above do - each hooks into a genuinely
# different point in a PC's turn (a free self-heal before attacking, a
# swapped-in attack profile inside the attack loop, a one-time luck bonus
# on a specific attack roll) - so each gets its own function, called by
# name from party.py's `card_techniques` list rather than forced through
# a single dispatch table that doesn't fit all three shapes. combat_sim.
# run_fight's Party's-turn block is what actually calls these.

def try_second_wind(pc, log=None):
    """Second Wind (T012, 0 AP, Cost 'Discard a card'): self-heal 2
    Shallow Health (1 base, +1 since the discarded card is assumed a
    Heart - same guaranteed-favorable-discard simplification
    strategy_support_healer already makes) when Wounded (health at or
    below half max, same proxy used everywhere else in this sim) and a
    card_uses_left charge remains. Entirely free of AP - Second Wind's
    own Action cost is 0 - so it never competes with this PC's own
    attack(s) the same turn; combat_sim.run_fight calls this once per PC
    turn, before movement/attacks, regardless of `ap`."""
    if 'Second Wind' not in pc.get('card_techniques', ()):
        return False
    if pc.get('card_uses_left', 0) <= 0:
        return False
    if not (0 < pc['health'] <= pc['max_health'] / 2):
        return False
    pc['card_uses_left'] -= 1
    heal = min(2, pc['max_health'] - pc['health'])
    pc['health'] += heal
    if log:
        log(unit=pc['name'], action='heal', target=pc['name'], amount=heal, target_hp_after=pc['health'], via='Second Wind')
    return True


def perfect_strike_bonus(pc):
    """Perfect Strike (T078, 0 AP - Interrupt 'you declare a weapon
    attack', Cost 'Discard a card'): +2 Good Luck (1 base, +1 for
    choosing 'Good Luck a second time' over the suit-pool option this
    sim doesn't model) on any weapon attack, at will - T078's own
    Effects text has no Gambling requirement at all; earlier framing
    ('an attack where she needs to Gamble') was just one example of
    when a player would actually spend it, not a hard restriction, so
    this now applies to the first attack(s) a charge allows regardless.
    Called from inside combat_sim's attack loop; consumes a
    card_uses_left charge each time it fires, so it self-rations to
    however many charges this PC's hand_size // 3 budget allows."""
    if 'Perfect Strike' not in pc.get('card_techniques', ()):
        return 0
    if pc.get('card_uses_left', 0) <= 0:
        return 0
    pc['card_uses_left'] -= 1
    return 2


def sift_bonus(pc):
    """Hand of Chaos (T131, Passive: 'Whenever you make an attack, Sift 1
    card and add its suit to the pool') - the designer's own explicit
    simplification, since this sim has no real suit-pool/Extra-Success
    tracking (see combat_sim.py's module docstring): approximated as a
    flat 1-in-4 chance of +1 damage on a hit, standing in for 'the
    sifted card happens to match this attack's own governing suit.'
    Always-on (no AP/card cost, unlike the Card Techniques above), so
    this is checked on every attack a PC with 'Hand of Chaos' in
    `pc['passives']` lands, not gated by any budget."""
    return 'Hand of Chaos' in pc.get('passives', ()) and random.random() < 0.25


def bottomless_bottles_choice(pc):
    """Bottomless Bottles (T053): the 10-minute crafting Action that
    actually creates the items happens before the fight (not AP-costed
    here at all) - what this models is spending one of THIS PC's own
    2-AP attack actions on a created item (Bottled Fire, I030 - only
    Jackal has this technique right now, and only makes this one item
    with it, not Healing Potion too) instead of their normal weapon
    attack. Gated by `bottled_fire_uses_left`, a dedicated counter
    (party.py's own Bottomless Bottles paragraph works out the actual
    number from Bottled Fire's real Gold cost - a separate, more
    involved derivation than the flat hand_size // 3 the other three
    Card Techniques share, so it gets its own budget rather than
    overloading card_uses_left). Returns None (fall through to a normal
    weapon attack) if this PC doesn't have the technique or has no
    charge left; otherwise an alternate attack profile (skill_total/
    damage/dmg_type/opp_def/via) the caller temporarily overlays onto
    the PC for that one attack."""
    if 'Bottomless Bottles' not in pc.get('card_techniques', ()):
        return None
    if pc.get('bottled_fire_uses_left', 0) <= 0:
        return None
    pc['bottled_fire_uses_left'] -= 1
    return {'via': 'Bottled Fire', **pc['bottled_fire_profile']}
