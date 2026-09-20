"""
Monte Carlo combat loop: N party members vs. M enemies, repeated many
times with fresh card flips to estimate win rate, average rounds to
resolve, and party Health remaining on a win.

Deliberately simplified, not a full combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of
what's NOT modeled (no Extra Successes from suit-pool matching, no
Techniques/items beyond Weapon/Armor/Support, no real initiative, rough
Battle Tactics targeting proxies, no Shallow/Deep Health split - so
"Wounded" is approximated as half max Health, see tactics.
strategy_support_healer). Good for catching relative differences
between builds and Tiers; the exact win percentages aren't precise
predictions of real play.

## How a turn works (rulebook.md's "Actions on a Turn")

Every unit - PC or enemy - gets tunables.AP_PER_TURN (4) Action Points
on its own turn, spent in this order:

1. **A support strategy, if the unit has one** (tactics.
   resolve_pc_strategy - currently just a support healer) - spends
   whatever AP that costs (Healing Magic: tunables.HEALING_MAGIC_AP_COST,
   1) and reports it, before anything else happens this turn.
2. **Movement**, if `movement=True` (spend_movement_ap) - as many move
   actions (tunables.MOVE_AP_COST, 1 AP each, up to Speed meters) as it
   takes to close on the unit's target and stop in range, or exactly
   one retreat action for a Kiting unit - "as many action points as
   required," per the designer, not an artificial cap; a unit that
   needs its whole turn's worth of AP just to close the gap simply
   doesn't get to attack this round. Skipped entirely when
   `movement=False` (see below).
3. **Attacks**, tunables.ATTACK_AP_COST (2) AP each - as many as the
   remaining AP allows, capped at 1 for a non-Flurry enemy Fighting
   Style (tactics.attack_cap - Guarded/Aimed Shot/Skirmisher
   deliberately give up a possible 2nd attack for their own
   compensating bonus, see tactics.py's own Fighting Style section) but
   uncapped for everyone else - which in practice always means "up to
   2," since 4 AP only ever buys 2 attacks. PCs have no Fighting Style
   at all and are always uncapped, matching the designer's own "bread
   and butter" default: move into range, attack, attack again if the
   AP's there.

`movement=False` (the default) skips the whole movement step - every
unit is always "in range" - so a plain attacker still gets up to 2
attacks a turn (0 AP spent moving leaves the full 4 for attacks). This
used to be a flat 1 attack/turn regardless of AP; this file's old
"movement=False must stay byte-identical" invariant doesn't hold
anymore now that the AP economy is real on both paths, not just under
`movement=True` - expect both paths' numbers to have moved together.

## Where the "AI" and the numbers live

Every "AI" decision a unit makes on its own turn - who it targets, how
it moves, how many attacks it gets, whether a PC does something other
than attack - lives in `tactics.py` as small named-function registries,
not as `if` branches in this file's `run_fight`; "which suit is this
card" assumptions live the same way in `cards.py`. Both exist so a new
tactic/strategy/style/card-rule is one function plus one registry
entry, not a new conditional threaded through run_fight - see either
module's own docstring before adding one. The actual numbers (AP costs,
Armor bonuses, the Level curve, ...) live in `tunables.py`, same
"numbers vs. shape" split as everywhere else in this project.

`run_fight(..., trace=[])` records a full round-by-round log of
whatever a fight actually did (positions, moves, attacks, heals) for
one specific run rather than just its final tally - `narrate_fight.py`
renders one into a position table plus a combat log (and, with
`--html`, a real self-contained replay page you can open in a browser
on your own - see its own docstring), for actually looking at what
this simulator does instead of only reading aggregate win rates.

## Resist, by damage type, on both sides

A PC's attack draws on the target enemy's `physres` (Physical) or
`elemres` (Fire/Frost/Brilliant/Shadow, one pool in this sim) depending
on the PC's own `dmg_type` (enemy_resist_for_pc_attack); an enemy's
attack against a PC now does the same in reverse
(pc_resist_for_enemy_attack) - this used to always use `physres`
regardless of the enemy's own `dmg_type`, so a Fire-damage enemy Action
(Melee/Ranged Spell) was being resisted by a PC's Physical Resist
instead of their usually-lower elemental one (no Armor bonus there -
see below). Both a PC's and an enemy's Physical Resist now include
worn Armor (tunables.ARMOR, the real armor_categories.csv table,
shared by both sides - see party.py's own Armor paragraph for the PC
side) - PCs used to have no Armor modeled at all (bare Essence only),
which read as enemies dealing full, only lightly resisted damage on
every hit.

## Enemy Abilities

The subset in tunables.ABILITY_COST: Crippled/Vulnerable/Bleeding
stacks on PCs from Strike (Crippling)/Strike (Vulnerable)/Poison
(Bleeding), Durable's per-turn Protected regen on enemies, all
following rulebook.md/glossary.md's numbers (Crippled -1 to
attacks/stack, Vulnerable -1 to Vital/Mental/Vigilant Defenses/stack,
Bleeding 1 damage per stack that decays, Protected absorbs Health loss
1-for-1). Fleeting effects (all of the above) decay 1 stack per
bearer's own turn, per glossary.md's [Fleeting] rule - not all stacks
at once.

## Good Luck / Bad Luck

`resolve_card` combines a flipper's own Good Luck stacks (`good_luck=N`
on `run_fight`/`simulate`, `make_party`'s own param - N stacks means N
extra cards flipped, keep the best) with a defender's Bad Luck (a
Guarded enemy that held its ground last turn - tactics.
defense_has_bad_luck) into one net flip. rulebook.md defines Good Luck
and Bad Luck individually but doesn't state how they interact if both
apply to the same flip at once - **this is an assumption, not a
confirmed rule**: modeled here as cancelling 1-for-1, the closest
documented analogy this project's own source text gives (glossary.md's
Range increase/decrease: "1 meter of each effect cancels out until
only one remains"). Good Luck's own win-rate-swing experiment
(comparing a simulated swing against balance_weights_notes.md's
hand-derived value of 2.4) predates the AP-economy/Armor fixes above
and hasn't been rerun since - treat that comparison as stale until it
is.

`max_rounds` (30, not the original 10) matters more than it looks: a
fight that's close but slow-grinding (both sides doing modest damage
against Resist/Defense) can hit a too-low round cap as an unresolved
"draw" most of the time instead of actually playing out. Always
sanity-check a low win rate against the raw party/enemies/draw counts
(`simulate()`'s 4th return value) before assuming it means "this build
loses," not just "this build is slow to resolve."
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


def flip_worst_of(n):
    return min(flip() for _ in range(n))


def resolve_card(good_luck_stacks, bad_luck_active):
    """One flip, combining a flipper's own Good Luck stacks with a
    target's Bad Luck (tactics.defense_has_bad_luck) into a single net
    result - **an assumption, not a confirmed rulebook.md rule**, see
    this module's own docstring for the reasoning. Net positive -> Good
    Luck with that many extra cards; net negative -> Bad Luck; net zero
    -> one plain flip."""
    net = good_luck_stacks - (1 if bad_luck_active else 0)
    if net > 0:
        return flip_best_of(1 + net)
    if net < 0:
        return flip_worst_of(1 - net)
    return flip()


def effective_range(unit):
    """The distance a unit's own action actually reaches - PCs use
    Melee's flat MELEE_RANGE unless `Weapon` gives them a real
    attack_range (party.py); enemies use their own attack_range if it's
    a real ranged Action, or MELEE_RANGE if it's 0 (a melee Action, per
    enemy_builder's own formula - 0 doesn't mean 'must be standing on
    the same point,' see tunables.MELEE_RANGE's comment)."""
    return unit.get('attack_range') or T.MELEE_RANGE


def spend_movement_ap(unit, target, ap, reach):
    """Spends AP on move actions (tunables.MOVE_AP_COST each) closing on
    `target`, stopping once in range or out of AP to spend - "as many
    action points as required," per the designer, not an artificial
    cap (see tactics.py's own note on why Skirmisher doesn't need a
    separate move-count rule as a result). A Kiting unit spends exactly
    one move action instead, retreating rather than closing (tactics.
    move_kite) - "keeps max range" is a positioning preference, not
    "flee as far as possible every turn." Returns (ap_remaining,
    in_range, moved) - `moved` is whether any move action was actually
    taken, for Guarded's own stand-still bonus to check (see
    run_fight's Enemies' turn)."""
    kiting = unit.get('battle_tactic') == 'Kiting'
    moved = False
    while ap >= T.MOVE_AP_COST:
        if not kiting and movement.distance(unit['pos'], target['pos']) <= reach + 1e-6:
            break
        tactics.move_unit(unit, target, reach)
        ap -= T.MOVE_AP_COST
        moved = True
        if kiting:
            break
    # 1e-6 slack: move_toward's own stop_at logic can land a unit a
    # floating-point hair past `reach` (float division/subtraction isn't
    # exact) - without it, two units that just closed to melee range can
    # get flagged permanently out-of-range by a fraction no real ruler
    # would ever measure, freezing the fight into an unresolved draw
    # (found via a real seeded fight that stalemated at exactly this gap).
    in_range = movement.distance(unit['pos'], target['pos']) <= reach + 1e-6
    return ap, in_range, moved


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


def pc_resist_for_enemy_attack(e, target):
    """The mirror of enemy_resist_for_pc_attack - an enemy's own
    `dmg_type` (tunables.ACTIONS - Physical or Fire) picks which of the
    target PC's Resist pools its attack draws from. Used to always read
    `physres` regardless of the enemy's own dmg_type - a real bug once
    a Fire-damage enemy Action (Melee/Ranged Spell) is in play, since a
    PC's `elemres` gets no Armor bonus (party.py's Armor paragraph) and
    is usually lower than `physres`."""
    if e.get('dmg_type') == 'Fire':
        return target.get('elemres', 0)
    return target.get('physres', 0)


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


def _retarget(unit, remaining, movement_on):
    """Same-round retarget after a kill, mid-attack-sequence: reuses the
    plain movement-aware default (tactics.target_closest/target_first)
    rather than re-running a Battle-Tactic-specific rule like Assassin's
    - "not a super intensive analysis," same simplification as
    everywhere else in movement mode. Returns None if nothing's left to
    retarget to."""
    if not remaining:
        return None
    return (tactics.target_closest if movement_on else tactics.target_first)(unit, remaining)


def run_fight(tier, enemy_level, n_enemies=4, max_rounds=30, seed=None, good_luck=0, movement=False, start_gap=None,
              trace=None, enemies=None):
    """`enemies`: pass a pre-built list of enemy dicts (e.g. from
    sample_enemies.build_encounter([...])) to fight that exact mix
    instead of `n_enemies` identical copies of `make_enemy(enemy_level)`
    - `enemy_level`/`n_enemies` are ignored when this is given. Lets a
    single fight mix Levels/Slots/Archetypes freely (a 2-slot Tank plus
    a handful of 0.5-slot Minions, say) rather than always facing one
    enemy type - see sample_enemies.total_slots to check the mix
    against "one slot per PC."

    `movement=True` turns on the optional 2D-arena mode (movement.py):
    the party starts in a compact 2x2 block (_party_formation), enemies
    spread down the y-axis (_start_positions), the two sides' front
    lines a random tunables.START_GAP_RANGE meters apart by default
    (`start_gap` overrides this with a fixed distance instead, e.g. for
    a controlled before/after comparison - see _random_front_lines).
    See this module's own docstring ("How a turn works") for the full
    AP-based movement/attack economy, which applies whether or not
    `movement` is on - `movement=False` just means every unit is always
    "in range," skipping the movement step of that economy entirely.

    `trace`: pass a list (e.g. `trace=[]`) to have this call record what
    happened, round by round, instead of just returning the final tally
    - meant for actually looking at one fight (`narrate_fight.py`), not
    for `simulate()`'s thousands of trials, so it's `None` (skip
    entirely, via `_log`) by default. Events are plain dicts, always
    carrying `round`; a `type='positions'` event (movement mode only,
    once per round, before any of that round's actions) snapshots every
    living unit's `pos`/`health`; everything else carries `side`
    ('party'/'enemy') and `unit`, and is either `action='move'` (this
    unit actually spent AP moving this turn - `pos`, `in_range` says
    whether that got it into range or it's still short and doesn't
    attack this round), `action='attack'` (`target`, `roll`, `defense`,
    `hit`, `dmg`, `target_hp_after`), or whatever a PC's own strategy
    function logs (`tactics.strategy_support_healer` logs
    `action='heal'` - see tactics.py's own `log` parameter). An
    `action='attack'` event also carries `raw_dmg` (damage before
    Resist - PCs' includes Gambling's +1/success, already never
    negative) and `resist` (the Resist pool actually applied -
    enemy_resist_for_pc_attack/pc_resist_for_enemy_attack), so
    `dmg == max(0, raw_dmg - resist)` minus whatever Protected
    absorbed (`protected_absorbed`, PC attacks only - enemies have no
    Protected-granting Ability modeled) is always visible in the trace,
    not just the final post-Resist number. A final `type='result'` event
    carries `winner`."""
    if seed is not None:
        random.seed(seed)
    pcs = make_party(tier, good_luck=good_luck)
    if enemies is not None:
        enemies = [copy.deepcopy(e) for e in enemies]
    else:
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

        # ---- Party's turn (see module docstring's "How a turn works") ----
        for pc in pcs:
            if pc['health'] <= 0:
                continue
            ap = T.AP_PER_TURN - tactics.resolve_pc_strategy(pc, pcs, log=party_log)
            targets = [e for e in enemies if e['health'] > 0]
            if not targets:
                break
            target = tactics.select_target(pc, targets, movement)
            if movement:
                ap, in_range, moved = spend_movement_ap(pc, target, ap, effective_range(pc))
                if moved:
                    _log(trace, round=rnd, side='party', unit=pc['name'], action='move', pos=pc['pos'], in_range=in_range)
                if not in_range:
                    continue

            while ap >= T.ATTACK_AP_COST and target is not None:
                defense = enemy_defense_for_pc_attack(pc, target)
                resist = enemy_resist_for_pc_attack(pc, target)
                gambles = pc_gamble_count(pc, target)
                crippled = pc.get('crippled', 0)
                bad_luck = tactics.defense_has_bad_luck(target, pc.get('opp_def', 'Parry/Dodge'))
                card = resolve_card(pc.get('good_luck', 0), bad_luck)
                roll = pc['skill_total'] - crippled + card - 2 * gambles  # PCs attack vs. the enemy's opposed Defense (pc['opp_def'])
                pc_attacks += 1
                ap -= T.ATTACK_AP_COST
                hit = roll >= defense
                dmg = 0
                raw_dmg = 0
                protected_absorbed = 0
                if hit:
                    raw_dmg = pc['damage'] + gambles
                    dmg = max(0, raw_dmg - resist)
                    protected = target.get('protected', 0)
                    if protected > 0 and dmg > 0:
                        protected_absorbed = min(dmg, protected)
                        target['protected'] -= protected_absorbed
                        dmg -= protected_absorbed
                    target['health'] -= dmg
                    pc_damage_dealt += dmg
                if party_log:
                    party_log(unit=pc['name'], action='attack', target=target['name'], roll=roll, defense=defense,
                               hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, protected_absorbed=protected_absorbed,
                               target_hp_after=target['health'])
                if target['health'] <= 0:
                    target = _retarget(pc, [e for e in enemies if e['health'] > 0], movement)
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

        # ---- Enemies' turn (see module docstring's "How a turn works") ----
        for e in enemies:
            if e['health'] <= 0:
                continue
            abilities = e.get('abilities', [])
            if 'Durable' in abilities and e.get('protected', 0) < 4:
                e['protected'] = e.get('protected', 0) + 1
            living_pcs = [p for p in pcs if p['health'] > 0]
            if not living_pcs:
                break
            fighting_style = e.get('fighting_style', 'Guarded')
            ap = T.AP_PER_TURN
            target = tactics.select_target(e, living_pcs, movement)
            moved = False
            in_range = True
            if movement:
                ap, in_range, moved = spend_movement_ap(e, target, ap, effective_range(e))
            # Guarded's own stand-still bonus (tactics.
            # defense_has_bad_luck) - set here, at the end of resolving
            # this enemy's own movement, so it's ready for the PARTY's
            # next turn to check (Party's turn runs before Enemies'
            # turn within a round, so this is necessarily a one-round-
            # lagged "held its ground last time" bonus, not instant).
            e['guarded_active'] = (fighting_style == 'Guarded' and not moved)
            if moved:
                _log(trace, round=rnd, side='enemy', unit=e['name'], action='move', pos=e['pos'], in_range=in_range)
            if movement and not in_range:
                continue

            cap = tactics.attack_cap(e)
            attacks_made = 0
            while ap >= T.ATTACK_AP_COST and (cap is None or attacks_made < cap) and target is not None:
                roll = e['accuracy'] + (flip_best_of(2) if fighting_style == 'Aimed Shot' else flip())
                opp_def_val = pc_defense_for(target, e['opp_def'])
                hit = roll >= opp_def_val
                dmg = 0
                raw_dmg = 0
                resist = 0
                if hit:
                    resist = pc_resist_for_enemy_attack(e, target)
                    raw_dmg = e['attack_damage']
                    dmg = max(0, raw_dmg - resist)
                    target['health'] -= dmg
                    if 'Strike (Crippling)' in abilities:
                        target['crippled'] = target.get('crippled', 0) + 1
                    if 'Strike (Vulnerable)' in abilities:
                        target['vulnerable'] = target.get('vulnerable', 0) + 1
                    if 'Poison (Bleeding)' in abilities:
                        target['bleeding'] = target.get('bleeding', 0) + 2
                ap -= T.ATTACK_AP_COST
                attacks_made += 1
                if enemy_log:
                    enemy_log(unit=e['name'], action='attack', target=target['name'], roll=roll, defense=opp_def_val,
                               hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, target_hp_after=target['health'])
                if target['health'] <= 0:
                    target = _retarget(e, [p for p in pcs if p['health'] > 0], movement)
        if all(p['health'] <= 0 for p in pcs):
            _log(trace, round=rnd, type='result', winner='enemies')
            return dict(winner='enemies', rounds=rnd, party_hp_pct=0.0,
                        pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)

    _log(trace, round=max_rounds, type='result', winner='draw')
    return dict(winner='draw', rounds=max_rounds,
                party_hp_pct=sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs),
                pc_attacks=pc_attacks, pc_damage_dealt=pc_damage_dealt)


def simulate(tier, enemy_level, n_enemies=4, trials=4000, good_luck=0, movement=False, start_gap=None, enemies=None):
    results = {'party': 0, 'enemies': 0, 'draw': 0}
    rounds_list = []
    hp_list = []
    total_attacks = 0
    total_damage = 0
    for _ in range(trials):
        r = run_fight(tier, enemy_level, n_enemies=n_enemies, good_luck=good_luck, movement=movement,
                       start_gap=start_gap, enemies=enemies)
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
