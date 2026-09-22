"""
Monte Carlo combat loop: N party members vs. M enemies, repeated many
times with fresh card flips to estimate win rate, average rounds to
resolve, and party Health remaining on a win.

Deliberately simplified, not a full combat engine - see design/
ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the full list of
what's NOT modeled (no Extra Successes from suit-pool matching beyond
tactics.sift_bonus's own flat-probability stand-in, no Techniques/items
beyond Weapon/Armor/Support/Card Techniques/Passives, rough Battle
Tactics targeting proxies, no Shallow/Deep Health split - so "Wounded"
is approximated as half max Health, see tactics.strategy_support_healer).
Good for catching relative differences between builds and Tiers; the
exact win percentages aren't precise predictions of real play.

Harried (glossary.md: -1 to Dodge/Parry per stack, gained "regardless
of the attack's result" by whoever applies Parry or Dodge against an
attack, rulebook.md) IS modeled, on both sides - see
enemy_defense_for_pc_attack/pc_defense_for (the -1 read) and
_take_pc_turn/_take_enemy_turn (the +1 grant, at the real attack-roll
call site only, and the "clear all stacks" decay at the bearer's own
turn end). It was left out of the original Ability-catalog pass
(tunables.py's own comment) since it isn't an Ability at all - a
base rule that applies to every attack, not something a build opts
into.

Interrupts (rulebook.md: "Some abilities let you act on other turns,
and interrupt their actions with your own... when such an action is
declared, but before any of its effects happen, you may use the
Interrupt ability") are now modeled too, specifically for Magehunter
(T075, synthetic test field `pc['magehunter']`, real persistent AP
via `pc['ap_bank']`) - see _take_pc_turn's own end-of-turn AP-refresh
step and _magehunter_interrupt/_take_enemy_turn for the actual
off-turn preemptive attack. This is a genuine Interrupt, not another
`_bonus_attack`-style synthetic flag layered onto a PC's own turn
(Whirlwind/Flurry/Feint's pattern) - the PC's attack really does
resolve on the ENEMY's turn, before that enemy's own Spell attack
does, and can kill the caster first.

## Turn order (rulebook.md's real Reflex/initiative rule)

Every unit - PC or enemy - rolls Reflex once at encounter start
(`_roll_initiative`: a card flip + Reflex, highest to lowest, ties
broken by re-flipping just the tied units - rulebook.md's own worked
example) and that order is fixed for the whole fight, interleaved
across both sides - not "all 4 PCs, then all enemies," which is what
this file did before real initiative existed. Every round just replays
that same order, skipping whoever's already dead. A PC's own
`turn_order_shift` field (not read from any real build yet - see
`_shift_in_order`) can push a hit target later in this same order,
modeling Backfoot/Alacrity/Heroic Inspiration's shared mechanic.

## How a turn works (rulebook.md's "Actions on a Turn")

Every unit - PC or enemy - gets tunables.AP_PER_TURN (4) Action Points
on its own turn (`_take_pc_turn`/`_take_enemy_turn`), spent in this
order:

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

## Card Techniques

A small set of PC techniques whose real cost is "discard a card," not
AP (techniques.csv's own Action/Cost columns say so directly - Second
Wind, Perfect Strike and Warmage's Reserves are each literally "0 AP").
`tactics.try_second_wind`/`perfect_strike_bonus`/`bottomless_bottles_
choice` implement the three currently in use (self-heal when Wounded,
+2 Good Luck on any weapon attack - not gated behind Gambling, per
T078's own Effects text - substituting a created item for one attack
action) against a shared per-fight budget - `card_uses_left`,
computed once in party.py as `hand_size // 3` ("say 1/3 of" a full
hand, the designer's own quick-check framing, same shape as
heal_uses_left's `// 4`) - rather than tracking real hand composition
or suits. This is deliberately a rough stand-in, same spirit as Good
Luck/Bad Luck's `resolve_card` above: good enough to make a Technique
that's otherwise completely invisible to this sim show up as a
real, budget-limited effect, not a claim that it's tracking actual
cards. `weapon_uses_left` is the separate, related idea of an
Encounter-Technique Weapon (a PC whose own attack is itself a
Technique with a limited number of known copies, like Beornhard's 3x
War Magic) running out of charges partway through a long fight -
Warmage's Reserves adds `ceil(hand_size / 3)` more on top of the base
copy count. See tactics.py's own "Card Techniques" section and party.py
's own paragraph on both columns for the full picture.

`tactics.sift_bonus` is a related but distinct idea: an always-on
Technique effect with no AP/card cost of its own (`pc['passives']`,
party.py's own Passives column) rather than a budget-limited one - Hand
of Chaos (T131) is the first, approximated per the designer's own call
as a flat 1-in-4 chance of +1 damage on a hit, standing in for this
sim's complete lack of real suit-pool/Extra-Success tracking.

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
from movement import distance as _distance  # run_fight's own `movement` param (bool) shadows the module name
import tactics
from sample_enemies import make_level_encounter
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
        if not kiting and movement.distance(unit['pos'], target['pos']) <= reach:
            break
        tactics.move_unit(unit, target, reach)
        ap -= T.MOVE_AP_COST
        moved = True
        if kiting:
            break
    # Exact integer comparison - movement is whole spaces (movement.py's
    # own docstring), so there's no floating-point slack to account for
    # the way the old continuous-coordinate model needed.
    in_range = movement.distance(unit['pos'], target['pos']) <= reach
    return ap, in_range, moved


def _start_positions(n, x, spread=4):
    """n units spread evenly down a vertical line at x, centered on the
    arena - just enough to avoid stacking every unit on one exact point,
    no other formation logic. Still used for the enemy side; the party
    uses _party_formation instead (see below). Whole spaces throughout
    (movement.py's own docstring) - `spread` is even, so `(i - mid) *
    spread` always lands on a whole number even when `mid` itself is a
    half-space (an even `n`)."""
    mid = (n - 1) / 2
    return [(x, T.ARENA_SIZE // 2 + round((i - mid) * spread)) for i in range(n)]


def _party_formation(x):
    """The party's 4 starting positions as a compact 2x2 block centered
    on the arena's y-midpoint - 'for simplicity's sake,' per the
    designer, rather than the single-file line _start_positions gives
    the enemies. Assumes exactly 4 PCs, same as the rest of this file.
    Whole spaces throughout - `half` is exact since
    PARTY_FORMATION_SPACING is even."""
    mid = T.ARENA_SIZE // 2
    half = T.PARTY_FORMATION_SPACING // 2
    return [(x - half, mid - half), (x + half, mid - half),
            (x - half, mid + half), (x + half, mid + half)]


def _random_front_lines(start_gap=None):
    """The party's and enemies' starting x-positions, `start_gap` whole
    spaces apart (tunables.START_GAP_RANGE if not given - a random 5-10
    each fight) and centered in the arena - 'spaced out slightly but not
    opposite ends,' per the designer, replacing the original fixed 16m
    corner-to-corner start. Returns (party_x, enemy_x), both ints -
    `gap - gap // 2` (rather than a second `gap // 2`) on the enemy side
    keeps the actual gap between the two exactly `gap` spaces even when
    `gap` is odd, instead of losing a space to double-rounding."""
    gap = start_gap if start_gap is not None else random.randint(*T.START_GAP_RANGE)
    mid = T.ARENA_SIZE // 2
    return mid - gap // 2, mid + (gap - gap // 2)


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
    learn this" rule instead of a weapon's Parry-or-Dodge one. Also
    reads `target['harried']` (glossary.md: "-1 penalty to Dodge and
    Parry Defense" per stack) - a pure read here, since this also gets
    called from pc_gamble_count's own odds check; the actual +1 stack
    only gets granted at the real attack-roll call site in
    _take_pc_turn, per rulebook.md's trigger rule ("a target who applied
    their Parry or Dodge Defense... is Harried once"). 'Vigilant' is a
    third override (Feint's own text: "against the target's Vigilant
    Defense") - Harried doesn't apply to it at all (glossary.md's -1 is
    Dodge/Parry only), so no harried subtraction there, matching
    rulebook.md's own Harried-grant trigger which only fires for a
    target who "applied their Parry or Dodge Defense" - Vigilant isn't
    either, so a Feint attack doesn't grant Harried from this rule
    (whatever Harried Feint itself grants on a hit is a separate,
    explicit effect, not this one). Also reads `target['vulnerable']`
    against the Vigilant case specifically - glossary.md's own
    Vulnerable text is explicit ("-1 penalty to Vital, Mental, AND
    Vigilant Defenses" per stack), and `pc_defense_for` already applies
    it to the enemy-attacks-PC direction's own Bodily/Mental cases; this
    was the missing reverse-direction half (Vigilant only - Vulnerable
    was never meant to touch Parry/Dodge, same split Harried's own
    Dodge/Parry-only rule makes in the other direction) - harmless until
    now since nothing granted an enemy Vulnerable before Demon School -
    Plague Fist (T083)."""
    harried = target.get('harried', 0)
    vulnerable = target.get('vulnerable', 0)
    if pc.get('opp_def') == 'Dodge':
        return target['dodge'] - harried
    if pc.get('opp_def') == 'Vigilant':
        return target['vigilant'] - vulnerable
    return max(target['parry'], target['dodge']) - harried


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


def pc_gamble_count(pc, target, defense_override=None):
    """How many times a 'clever' PC Gambles on this attack (rulebook.md's
    Gambling rule: each Gamble is -2 to the roll, but grants +1 Extra
    Success - and +1 damage - if the flip still hits). Not modeled at all
    originally - without it, a target whose Physical Resist reaches or
    exceeds the PC's own weapon Damage was untouchable no matter how many
    rounds passed, which isn't how a real player would actually respond
    to a wall of Resist.

    Picks whichever gamble count actually maximizes *expected* net
    damage, rather than a hand-picked "safe" cutoff - a real fix, not
    just a tighter constant, after the designer caught the old "gamble
    until the average card still clears" heuristic overcommitting once
    Defense is cratered (see balance_weights_notes.md's Feint pass): a
    card is uniform 1-13, so P(hit | n gambles) is exactly linear in n,
    which makes E[net damage] = P(hit|n) x (successes on a hit) a
    single-peaked (concave) function of n - there's one true
    EV-maximizing count, not a threshold to eyeball. Worked out
    analytically it's n* = (S - D + 12) / 4, roughly HALF the old
    "average card clears" count for the same margin, landing at a hit
    chance around half of what 0 gambles would give (not the ~50/50 the
    old heuristic actually produced once a big margin was in play) -
    but computed here directly per-attack (looping every candidate `n`
    up to where even a 13 can't hit) rather than trusting the closed
    form at every edge case, since a real Resist wall shifts which
    `n` pays off in a way the plain formula doesn't reflect on its own.

    `defense_override`: bypasses `enemy_defense_for_pc_attack` with a
    flat value instead - for Cloak and Dagger (T079), whose "unaware"
    target reads as Defense 8 (rulebook.md: "The target may choose not
    (or be unable) to apply any Defenses against an attack, in which
    case it is considered to be 8"), not the target's real Parry/Dodge.
    A player who already knows their attack faces this much softer
    Defense would rationally re-optimize how hard to Gamble, same as
    any other Defense-lowering effect already feeds into this search.
    """
    effective_skill = pc['skill_total'] - pc.get('crippled', 0)
    defense = defense_override if defense_override is not None else enemy_defense_for_pc_attack(pc, target)
    resist = enemy_resist_for_pc_attack(pc, target)
    sift = 1 if tactics.sift_bonus(pc) else 0
    best_n, _ = _gamble_search(effective_skill, defense, pc['damage'], resist, sift)
    return best_n


def _gamble_search(effective_skill, defense, damage, resist, sift):
    """The EV-maximizing search itself, factored out of pc_gamble_count
    so a caller that also needs the resulting EV (not just the best `n`)
    - Cloak and Dagger's own "is this attempt even worth it" check below
    - can reuse the identical search rather than a second, possibly
    drifting copy. Returns (best_n, best_ev)."""
    max_possible = max(0, int((effective_skill + 13 - defense) // 2))
    best_n, best_ev = 0, 0.0
    for n in range(max_possible + 1):
        threshold = defense - effective_skill + 2 * n  # min card needed to hit
        p_hit = max(0.0, min(1.0, (14 - threshold) / 13))
        net_dmg = max(0, damage + n + sift - resist)
        ev = p_hit * net_dmg
        if ev > best_ev:
            best_n, best_ev = n, ev
    return best_n, best_ev


def _p_flip_at_least(threshold, n_flips=1):
    """P(the best of `n_flips` uniform 1-13 cards >= threshold) - the
    same formula used throughout balance_weights_notes.md's own
    Good-Luck-stacking derivations, now shared by the actual sim code
    (Cloak and Dagger's own Stealth-check odds) instead of living only
    in a hand-math script - one formula, not two that could drift."""
    if threshold <= 1:
        return 1.0
    if threshold > 13:
        return 0.0
    p_single_fail = (threshold - 1) / 13
    return 1 - p_single_fail ** n_flips


def pc_defense_for(target, opp_def):
    """Route an enemy attack's opp_def to the right PC Defense category -
    'Parry/Dodge' lets the target pick whichever's better, same as
    rulebook.md's real rule ("If multiple Defenses are stated, the target
    chooses which to use"). Vulnerable stacks (-1 to Vital/Mental/
    Vigilant Defenses per stack, glossary.md) apply to the Bodily/Mental
    cases only - Dodge and Parry aren't Vulnerable's targets. Harried
    (-1 to Dodge/Parry per stack, glossary.md) is the mirror case - it
    only applies to the Parry/Dodge cases here, same "pure read, the
    real +1 stack is granted at the attack-roll call site" split as
    enemy_defense_for_pc_attack."""
    vulnerable = target.get('vulnerable', 0)
    harried = target.get('harried', 0)
    if opp_def == 'Parry/Dodge':
        return max(target['parry'], target['dodge']) - harried
    if opp_def == 'Dodge':
        return target['dodge'] - harried
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


def _resolve_group_order(indices, entries):
    """Given unit-indices tied on their current Reflex score, returns
    them in final relative order - rulebook.md: "For any ties, those
    creatures make another set of flips until all ties are broken."
    Recurses on sub-groups rather than lumping every re-flip back into
    one global re-sort, so a re-flip only ever resolves order WITHIN the
    tied subgroup - matching the rulebook's own worked example exactly
    (Hilde's re-flipped 15 doesn't leapfrog Felix's already-settled,
    numerically-lower 12; it only decides Hilde vs. the bandits, the
    group she was actually tied with)."""
    if len(indices) == 1:
        return indices
    new_scores = {}
    for i in indices:
        _, u = entries[i]
        flipper = flip_best_of(2) if 'One Eye Behind You' in u.get('passives', ()) else flip()
        new_scores[i] = flipper + u['reflex']
    new_groups = {}
    for i in indices:
        new_groups.setdefault(new_scores[i], []).append(i)
    result = []
    for s in sorted(new_groups, reverse=True):
        group = new_groups[s]
        result.extend(group if len(group) == 1 else _resolve_group_order(group, entries))
    return result


def _roll_initiative(pcs, enemies, trace):
    """Rolls Reflex once for every unit at encounter start - rulebook.md:
    "First, everyone makes a Reflex flip, which is an Insight flip. Each
    creature compares results, and is put into turn order from highest
    to lowest" - and returns a fixed [(side, unit), ...] order for the
    WHOLE fight: Reflex is flipped once to join an encounter, not
    re-rolled every round (rulebook.md's own Action Point paragraph -
    "When you flip Reflex to join an encounter, and again at the end of
    each of your turns, you lose any existing Action Points..." implies
    one join-flip, not a per-round one). PCs' own Reflex is their
    Insight Skill Total (party.py); enemies' is enemy_builder.py's own
    `reflex` (2 + Level - the real encounter-calculator value, not
    invented for this sim). A unit with 'One Eye Behind You' in its own
    `passives` (Sable) has Good Luck on this flip (T011's own Effects
    text), same flip_best_of(2) pattern used everywhere else in this
    file - the technique's other half (discarding a card to manually
    reorder turn order mid-fight) isn't modeled, since it's an
    of-the-moment tactical choice this sim has no basis to make for a
    player."""
    entries = [('party', p) for p in pcs] + [('enemy', e) for e in enemies]
    scores = {}
    for i, (_, u) in enumerate(entries):
        flipper = flip_best_of(2) if 'One Eye Behind You' in u.get('passives', ()) else flip()
        scores[i] = flipper + u['reflex']
    groups = {}
    for i in range(len(entries)):
        groups.setdefault(scores[i], []).append(i)
    order_idx = []
    for s in sorted(groups, reverse=True):
        group = groups[s]
        order_idx.extend(group if len(group) == 1 else _resolve_group_order(group, entries))
    result = [entries[i] for i in order_idx]
    if trace is not None:
        _log(trace, round=0, type='initiative', order=[{'side': side, 'unit': u['name']} for side, u in result])
    return result


def _shift_in_order(order, unit, places):
    """Moves `unit`'s (side, unit) entry `places` positions in the turn
    order - positive `places` delays it (Backfoot: push a hit target
    later), negative advances it (a hypothetical "move yourself earlier"
    variant, tested separately from Backfoot's own delay-the-target
    version - see balance_weights_notes.md). Clamped to the list's own
    bounds. Mutates `order` in place - since `run_fight` iterates a
    `list(order)` snapshot each round (not `order` itself), a shift
    applied mid-round doesn't disturb that round's already-in-progress
    sequence, but does take effect starting next round, which is fixed
    for the rest of the fight same as any other initiative result.
    Returns the actual signed distance moved (0 if `unit` wasn't found,
    or already at the clamped bound), for `_take_pc_turn`'s own log
    annotation."""
    for i, (side, u) in enumerate(order):
        if u is unit:
            entry = order.pop(i)
            new_i = max(0, min(i + places, len(order)))
            order.insert(new_i, entry)
            return new_i - i
    return 0


def _find_extra_target(pc, primary, enemies, movement_on, mode):
    """Finds a second living, distinct-from-`primary` enemy for a
    Whirlwind (`mode='melee'` - any other target within the PC's own
    melee reach) or Ricochet Shot (`mode='adjacent'` - another target
    adjacent to the primary target itself, not to the PC - see the
    Advanced Cost-6 trio's own balance_weights_notes.md pass for why
    these need real position data rather than a flat rate, and why
    Ricochet Shot's condition was reworked from its original
    line-of-fire version, which almost never fired in practice). Without
    `movement_on` there's no position data to check against, so this
    falls back to "any other living enemy" (the same simplification the
    rest of the static-mode model already makes - everything's "in
    range"). Returns the enemy dict or None."""
    others = [e for e in enemies if e['health'] > 0 and e is not primary]
    if not others:
        return None
    if not movement_on:
        return others[0]
    if mode == 'melee':
        reach = effective_range(pc)
        for e in others:
            if _distance(pc['pos'], e['pos']) <= reach:
                return e
        return None
    if mode == 'adjacent':
        for e in others:
            if _distance(primary['pos'], e['pos']) <= T.MELEE_RANGE:
                return e
        return None
    return None


def _take_pc_turn(pc, pcs, enemies, rnd, movement_on, trace, party_log, order=None):
    """One PC's full turn (see module docstring's "How a turn works") -
    strategy (a healer's own heal), Second Wind, movement, then attacks.
    Returns (attacks_made, damage_dealt) for run_fight's own running
    totals. Also runs this PC's own Fleeting decay (glossary.md: 1 stack
    of Crippled/Vulnerable/Bleeding per bearer's own turn) at the end -
    with a real initiative order this genuinely IS "their own turn" now,
    not a once-a-round batch step after every PC's gone.

    `order`: this fight's live turn-order list, passed through only so a
    PC with `turn_order_shift` or `self_turn_order_advance` set (both
    synthetic test fields, not read from any real build yet - see
    balance_weights_notes.md's Backfoot pass) can shift a unit in it via
    `_shift_in_order` on a hit - `turn_order_shift` delays the target
    (Backfoot's own version), `self_turn_order_advance` moves the PC
    itself earlier instead (tested as a separate mechanic)."""
    attacks_made = 0
    damage_dealt = 0

    def _bonus_attack(bonus_target, via_suffix):
        """Resolves one additional weapon attack against `bonus_target`,
        granted for free by a doubling Feature (Whirlwind/Piercing
        Shot/Flurry's own synthetic test fields - see the Advanced
        Cost-6 trio's balance_weights_notes.md pass) - no AP cost, no
        Gambling (a per-attack player choice, not sensible to auto-apply
        to a bonus swing), same hit/damage/Harried/Protected resolution
        as a normal attack otherwise. Mirrors _take_pc_turn's own main
        attack block rather than sharing code with it, to avoid touching
        that well-tested path. Returns the damage dealt."""
        defense = enemy_defense_for_pc_attack(pc, bonus_target)
        resist = enemy_resist_for_pc_attack(pc, bonus_target)
        crippled = pc.get('crippled', 0)
        bad_luck = tactics.defense_has_bad_luck(bonus_target, pc.get('opp_def', 'Parry/Dodge'))
        luck_bonus = tactics.perfect_strike_bonus(pc)
        card = resolve_card(pc.get('good_luck', 0) + luck_bonus, bad_luck)
        roll = pc['skill_total'] - crippled + card
        hit = roll >= defense
        bonus_target['harried'] = bonus_target.get('harried', 0) + 1
        dmg = raw_dmg = protected_absorbed = 0
        if hit:
            raw_dmg = pc['damage'] + (1 if tactics.sift_bonus(pc) else 0)
            dmg = max(0, raw_dmg - resist)
            protected = bonus_target.get('protected', 0)
            if protected > 0 and dmg > 0:
                protected_absorbed = min(dmg, protected)
                bonus_target['protected'] -= protected_absorbed
                dmg -= protected_absorbed
            bonus_target['health'] -= dmg
        if party_log:
            party_log(unit=pc['name'], action='attack', target=bonus_target['name'], roll=roll, defense=defense,
                       hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, protected_absorbed=protected_absorbed,
                       target_hp_after=bonus_target['health'], target_harried_after=bonus_target.get('harried', 0),
                       via=f"{pc['weapon_name']} ({via_suffix})", turn_shift=None)
        return dmg

    if pc['health'] > 0:
        if _has_interrupt_tech(pc):
            # Magehunter (T075) / Parting Shot (T076), synthetic test
            # fields, share one real persistent AP pool (`pc['ap_bank']`)
            # since rulebook.md's AP economy is a single number per PC,
            # not one pool per Interrupt Technique known. Refresh trigger
            # is "when you flip Reflex to join an encounter, AND AGAIN AT
            # THE END of each of your turns" - not at the start of a
            # turn. So a PC's own-turn AP is whatever's left of the pool
            # granted at their *last* turn-end (run_fight's own initial
            # `ap_bank = T.AP_PER_TURN` models the Reflex-flip refresh for
            # their very first turn), minus whatever Interrupts actually
            # spent from that same pool since then (_magehunter_interrupt/
            # _parting_shot_interrupt) - not a blanket "give up a whole
            # attack every turn whether or not the trigger ever fires"
            # cost. If no Interrupt fired, this pool is still the full
            # T.AP_PER_TURN, so a PC who never got a trigger loses nothing
            # relative to a normal PC (see balance_weights_notes.md's
            # re-check of this pass, per the designer's own correction).
            ap = pc['ap_bank'] - tactics.resolve_pc_strategy(pc, pcs, log=party_log)
        else:
            ap = T.AP_PER_TURN - tactics.resolve_pc_strategy(pc, pcs, log=party_log)
        tactics.try_second_wind(pc, log=party_log)  # 0 AP - see tactics.py's own docstring
        targets = [e for e in enemies if e['health'] > 0]
        if targets:
            target = tactics.select_target(pc, targets, movement_on, allies=[p for p in pcs if p['health'] > 0])
            in_range = True
            if movement_on:
                # Blinkstep (T077, synthetic test field, 0 AP, once per
                # encounter): "Shift up to [half your Acrobatics Skill
                # Total] meters" - glossary.md's [Shift] (ordinary
                # movement, just Interrupt-immune and ignores Difficult
                # Terrain, neither of which this simulator models).
                # Applied BEFORE spend_movement_ap, not as a rescue after
                # it - the Technique's real value is covering ground for
                # FREE so AP-funded movement needs less (or none), not
                # "you'd have failed to close the gap otherwise" (rare
                # here - spend_movement_ap already burns up to all 4 AP
                # closing any reachable distance, so it usually succeeds
                # regardless; what it can't do is leave AP left over for
                # an attack this same turn, which is exactly what
                # Blinkstep buys). Only spent when there's an actual gap
                # to close (`not already in range`) - a player wouldn't
                # burn a once-per-encounter charge for nothing - and
                # consumed on use, not just on offer, same rule as every
                # other once-per-encounter field in this file.
                reach = effective_range(pc)
                if pc.get('blinkstep') and _distance(pc['pos'], target['pos']) > reach:
                    shift_dist = pc.get('acrobatics_skill_total', 0) // 2  # rulebook.md: round fractions down
                    if shift_dist > 0:
                        blink_start = pc['pos']
                        pc['pos'] = movement.move_toward(pc['pos'], target['pos'], shift_dist, stop_at=reach)
                        pc['blinkstep'] = False
                        # Logged as its own event (not folded into the
                        # AP-funded move below) so `spaces` on each event
                        # reflects only that phase's own distance, not
                        # both combined under one misleading label.
                        _log(trace, round=rnd, side='party', unit=pc['name'], action='move', pos=pc['pos'],
                             in_range=_distance(pc['pos'], target['pos']) <= reach,
                             spaces=_distance(blink_start, pc['pos']), via='Blinkstep')
                ap_start = pc['pos']
                ap, in_range, moved = spend_movement_ap(pc, target, ap, effective_range(pc))
                if moved:
                    _log(trace, round=rnd, side='party', unit=pc['name'], action='move', pos=pc['pos'],
                         in_range=in_range, spaces=_distance(ap_start, pc['pos']))

            while in_range and ap >= T.ATTACK_AP_COST and target is not None:
                if pc.get('weapon_uses_left') is not None and pc['weapon_uses_left'] <= 0:
                    break  # an Encounter-Technique Weapon (Beornhard's War Magic) out of charges this fight
                substitute = tactics.bottomless_bottles_choice(pc)
                # A Bottled-Fire substitution temporarily overlays this PC's
                # own attack profile with the thrown item's numbers for one
                # iteration, restored right after logging - everything below
                # (defense/resist/roll) reads pc['skill_total'] etc. exactly
                # as it would for a normal weapon attack, so nothing else
                # needs to branch on `substitute`.
                saved_profile = None
                if substitute:
                    saved_profile = (pc['skill_total'], pc['damage'], pc['dmg_type'], pc['opp_def'])
                    pc['skill_total'], pc['damage'], pc['dmg_type'], pc['opp_def'] = (
                        substitute['skill_total'], substitute['damage'], substitute['dmg_type'], substitute['opp_def'])
                # Feint (T074, synthetic test field, once-per-encounter):
                # "Make a weapon attack against the target's Vigilant
                # Defense. Instead of normal effects, if it hits then the
                # target is Harried 3 + [Diamonds] times." Costs 1 AP, not
                # the usual 2 - see balance_weights_notes.md's Martial
                # Techniques pass for why that AP discount needed checking
                # directly rather than assumed away.
                feint_active = bool(pc.get('feint')) and not substitute
                saved_opp_def = None
                feint_stacks = 3
                if feint_active:
                    saved_opp_def = pc['opp_def']
                    pc['opp_def'] = 'Vigilant'
                    # A numeric value overrides the default 3 stacks (a
                    # plain True/1 test field keeps that default) - read
                    # before the charge is consumed below, since pc['feint']
                    # is gone by the time the hit/miss result is known.
                    if isinstance(pc['feint'], (int, float)) and pc['feint'] is not True:
                        feint_stacks = pc['feint']
                    # Charge consumed on use, not on hit - an Encounter
                    # Technique is expended by using it (rulebook.md), a
                    # missed attack doesn't refund the attempt.
                    pc['feint'] = False
                # Cloak and Dagger (T079, synthetic test field, "0 AP -
                # Interrupt (you declare a weapon attack with a
                # close-range weapon that isn't Heavy or two-handed)"):
                # a separate Stealth attack against the target's own
                # Vigilant Defense - if it hits, the target is "unaware"
                # (rulebook.md's [Unaware]: "unable to apply their Parry
                # or Dodge Defense against it"). This does NOT auto-hit -
                # rulebook.md's own base attack rule (line 484) is explicit
                # that a target unable to apply a Defense "is considered
                # to be 8," a real (if usually much lower) number the
                # attack still rolls against, not a guaranteed success.
                # Modeled by overriding `defense` to a flat 8 below, which
                # also correctly feeds into this same attack's own
                # Gambling choice via pc_gamble_count's `defense_override`
                # - a real player who already knows they're facing this
                # much softer Defense would rationally gamble harder,
                # since there's far more room before missing. Unaware's
                # OTHER real effect ("ignores the target's Shallow Health
                # and instead causes them to only lose Deep Health")
                # still can't be modeled - this simulator has no Shallow/
                # Deep Health split at all (a single flat `health` pool
                # everywhere - see the module docstring's own "not
                # modeled" list) - so the measured value is still a
                # floor, just a less understated one than the auto-hit
                # version this was originally (wrongly) built as - see
                # balance_weights_notes.md's own correction. "Good Luck
                # if you discarded a Spade" uses the same guaranteed-
                # favorable-discard simplification as Second Wind's own
                # "assumed a Heart."
                close_range_weapon = not pc.get('attack_range') and pc.get('weapon_name') not in ('Melee', '2H Heavy Melee')
                cloak_dagger_hit = False
                if (pc.get('cloak_and_dagger') and not substitute and not feint_active and close_range_weapon
                        and pc.get('card_uses_left', 0) > 0):
                    # Worth attempting at all? A real player wouldn't
                    # discard a card chasing a target that's already easy
                    # to hit - against an already-Harried-softened target
                    # (this attack's own real Defense, read BEFORE the
                    # Stealth check, so this decision doesn't peek at its
                    # own outcome), the EV-maximizing attack against the
                    # real Defense can already be close to Defense-8's
                    # own ceiling, leaving little for Cloak and Dagger to
                    # add - not enough to be worth a guaranteed Card cost
                    # (2.7, balance_weights_notes.md's own established
                    # rate) against a chance (not certainty) of the
                    # Stealth check itself succeeding. Computed the same
                    # way pc_gamble_count already searches for its own
                    # best `n`, reusing that search rather than a second
                    # copy, and the same flip-2-take-best formula this
                    # project's own Good-Luck-stacking math already uses.
                    eff_skill = pc['skill_total'] - pc.get('crippled', 0)
                    real_defense = enemy_defense_for_pc_attack(pc, target)
                    resist_for_ev = enemy_resist_for_pc_attack(pc, target)
                    sift_for_ev = 1 if tactics.sift_bonus(pc) else 0
                    _, normal_ev = _gamble_search(eff_skill, real_defense, pc['damage'], resist_for_ev, sift_for_ev)
                    _, unaware_ev = _gamble_search(eff_skill, 8, pc['damage'], resist_for_ev, sift_for_ev)
                    stealth_threshold = target['vigilant'] - pc.get('stealth_skill_total', 0)
                    q = _p_flip_at_least(stealth_threshold, n_flips=2)  # guaranteed Good Luck, per the Spade assumption below
                    worth_it = q * (unaware_ev - normal_ev) * 4 - T.CARD_VALUE > 0
                    if worth_it:
                        pc['card_uses_left'] -= 1
                        stealth_card = resolve_card(1, False)  # guaranteed Good Luck, per the Spade assumption above
                        stealth_roll = pc.get('stealth_skill_total', 0) - pc.get('crippled', 0) + stealth_card
                        cloak_dagger_hit = stealth_roll >= target['vigilant']
                        if party_log:
                            party_log(unit=pc['name'], action='stealth_check', target=target['name'],
                                       roll=stealth_roll, defense=target['vigilant'], hit=cloak_dagger_hit,
                                       via='Cloak and Dagger')
                defense = 8 if cloak_dagger_hit else enemy_defense_for_pc_attack(pc, target)
                resist = enemy_resist_for_pc_attack(pc, target)
                # Grenades can't be Gambled on (glossary.md's [Grenade] rule).
                # pc_gamble_count reads the target's current Defense itself
                # (via its own enemy_defense_for_pc_attack call, or the
                # flat 8 override above when Cloak and Dagger landed) -
                # computed here, before this attack's own Harried grant
                # below, so a target already Harried from an earlier
                # attack this round correctly makes gambling look more
                # attractive (lower Defense to clear), but this attack's
                # own upcoming stack doesn't get counted a turn early.
                gambles = 0 if (substitute or feint_active) else pc_gamble_count(
                    pc, target, defense_override=8 if cloak_dagger_hit else None)
                crippled = pc.get('crippled', 0)
                bad_luck = tactics.defense_has_bad_luck(target, pc.get('opp_def', 'Parry/Dodge'))
                luck_bonus = tactics.perfect_strike_bonus(pc)
                card = resolve_card(pc.get('good_luck', 0) + luck_bonus, bad_luck)
                roll = pc['skill_total'] - crippled + card - 2 * gambles  # PCs attack vs. the enemy's opposed Defense (pc['opp_def'])
                attacks_made += 1
                ap -= 1 if feint_active else T.ATTACK_AP_COST
                if pc.get('weapon_uses_left') is not None and not substitute:
                    pc['weapon_uses_left'] -= 1
                hit = roll >= defense
                # rulebook.md: "Regardless of the attack's result, a
                # target who applied their Parry or Dodge Defense
                # against it is Harried once" - a PC's own weapon attack
                # is always opposed by Parry or Dodge (see
                # enemy_defense_for_pc_attack), so this always applies -
                # except a Feint, which targets Vigilant instead, or a
                # landed Cloak and Dagger, whose target is UNABLE to apply
                # Parry or Dodge at all (that's the whole point of
                # Unaware) - so this generic grant doesn't fire for
                # either (Feint's own explicit Harried effect below is
                # separate from this rule).
                if not feint_active and not cloak_dagger_hit:
                    target['harried'] = target.get('harried', 0) + 1
                dmg = 0
                raw_dmg = 0
                protected_absorbed = 0
                turn_shift_note = None
                if feint_active and hit:
                    # "Instead of normal effects" - no damage, Harried N
                    # times instead (feint_stacks, default 3 matching the
                    # CSV's own "3 + [Diamonds]", overridable by setting
                    # pc['feint'] to a number instead of True - see
                    # balance_weights_notes.md's Martial Techniques pass
                    # for the sweep this was built to run). +0.25 for the
                    # suit-pool average, same convention as every other
                    # suit-bonus Feature this session.
                    target['harried'] = target.get('harried', 0) + feint_stacks + 0.25
                elif hit:
                    raw_dmg = pc['damage'] + gambles + (1 if tactics.sift_bonus(pc) else 0)
                    dmg = max(0, raw_dmg - resist)
                    protected = target.get('protected', 0)
                    if protected > 0 and dmg > 0:
                        protected_absorbed = min(dmg, protected)
                        target['protected'] -= protected_absorbed
                        dmg -= protected_absorbed
                    target['health'] -= dmg
                    damage_dealt += dmg
                    if order is not None and pc.get('turn_order_shift'):
                        moved = _shift_in_order(order, target, pc['turn_order_shift'])
                        if moved:
                            turn_shift_note = f"{target['name']} pushed {moved} later in turn order"
                    if order is not None and pc.get('self_turn_order_advance'):
                        moved = _shift_in_order(order, pc, -pc['self_turn_order_advance'])
                        if moved:
                            turn_shift_note = f"{pc['name']} advanced {-moved} earlier in turn order"
                if party_log:
                    via = substitute['via'] if substitute else ('Feint' if feint_active else pc['weapon_name'])
                    party_log(unit=pc['name'], action='attack', target=target['name'], roll=roll, defense=defense,
                               hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, protected_absorbed=protected_absorbed,
                               target_hp_after=target['health'], target_harried_after=target.get('harried', 0),
                               via=via, turn_shift=turn_shift_note)
                if saved_opp_def is not None:
                    pc['opp_def'] = saved_opp_def
                # Unlike most Features on this sheet, none of these three
                # say "if the attack hits" in their own Effects text - the
                # extra attack is its own independent roll, granted on the
                # attempt, not gated on the primary attack landing.
                #
                # Modeled as a once-per-encounter charge (per the designer's
                # correction - these are Encounter abilities, not a
                # persistent per-attack modifier for the whole fight): each
                # field is consumed (set False) the first time it actually
                # fires, so a PC gets exactly one bonus attack per fight,
                # not one every single attack. Whirlwind/Ricochet Shot only
                # consume their charge once a valid second target is
                # actually found - equivalent to "wait for a real
                # opportunity" rather than firing blind on the first swing;
                # Flurry has no target condition, so it just fires on the
                # PC's first attack of the fight.
                if pc.get('bonus_attack_control'):
                    # Calibration control, not a real Technique - an
                    # unconditional once-per-encounter bonus attack is
                    # exactly THE TABEL's own Autoswing definition ("value
                    # of one full extra attack", Locked at 5.5). Run this
                    # alongside whatever's actually being priced, in the
                    # SAME matchup, then scale: 1 Value unit = (this
                    # control's own win-rate delta) / 5.5. That conversion
                    # factor is matchup-specific (a longer/harder fight
                    # gives a bonus attack more room to matter), so
                    # recalibrate per matchup rather than reusing a
                    # constant across different tests - see
                    # balance_weights_notes.md's Advanced Cost-6 trio pass
                    # for a worked example.
                    damage_dealt += _bonus_attack(target, 'Control')
                    pc['bonus_attack_control'] = False
                if pc.get('flurry'):
                    damage_dealt += _bonus_attack(target, 'Flurry')
                    pc['flurry'] = False
                if pc.get('whirlwind'):
                    extra = _find_extra_target(pc, target, enemies, movement_on, 'melee')
                    if extra:
                        damage_dealt += _bonus_attack(extra, 'Whirlwind')
                        pc['whirlwind'] = False
                if pc.get('ricochet_shot'):
                    extra = _find_extra_target(pc, target, enemies, movement_on, 'adjacent')
                    if extra:
                        damage_dealt += _bonus_attack(extra, 'Ricochet Shot')
                        pc['ricochet_shot'] = False
                if saved_profile:
                    pc['skill_total'], pc['damage'], pc['dmg_type'], pc['opp_def'] = saved_profile
                if target['health'] <= 0:
                    target = _retarget(pc, [e for e in enemies if e['health'] > 0], movement_on)
    # Fleeting decay: 1 stack of each per bearer's own turn (glossary.md's
    # [Fleeting] rule), not all stacks at once - Bleeding's decaying
    # stack is what actually deals its 1 damage. Harried is the one
    # exception to "1 stack at a time" - its own glossary.md text says
    # "remove all stacks of Harried you have" at the end of your turn,
    # not decay by 1 like the others.
    if pc['health'] > 0:
        if pc.get('crippled', 0) > 0:
            pc['crippled'] -= 1
        if pc.get('vulnerable', 0) > 0:
            pc['vulnerable'] -= 1
        if pc.get('bleeding', 0) > 0:
            pc['bleeding'] -= 1
            pc['health'] -= 1
        if pc.get('harried', 0) > 0:
            pc['harried'] = 0
        if _has_interrupt_tech(pc):
            # rulebook.md's refresh happens at the END of your own turn
            # - a flat reset to T.AP_PER_TURN (4), discarding whatever
            # was left, not an accumulation - this fresh pool is what's
            # now available for Interrupts until the NEXT end-of-turn
            # refresh (this same assignment, next time this PC's own
            # turn comes around).
            pc['ap_bank'] = T.AP_PER_TURN
    return attacks_made, damage_dealt


def _has_interrupt_tech(pc):
    """Whether `pc` knows any synthetic-test-field Interrupt Technique
    (Magehunter T075, Parting Shot T076) - both share the one real AP
    pool (`pc['ap_bank']`) rather than each getting its own, since
    rulebook.md's AP economy is a single number per PC."""
    return bool(pc.get('magehunter') or pc.get('parting_shot'))


def _magehunter_interrupt(e, pcs, movement_on, party_log):
    """Magehunter (T075): "Make a weapon attack against the target [...]
    a creature within your weapon's range declares a Spell, before it
    is cast" - called from _take_enemy_turn right before an enemy's own
    Melee Spell/Ranged Spell attack resolves, so a real Interrupt: the
    PC's attack lands (and can kill/interrupt the caster) BEFORE the
    enemy's own attack roll happens, not just some other bonus-damage
    add-on after the fact. Any living PC with an unused Magehunter
    charge (`pc['magehunter_charge_used']` not yet set - see below) AND
    at least T.MAGEHUNTER_AP_COST (1) AP left in `pc['ap_bank']` - the
    pool granted at this PC's own last turn-end refresh (or the initial
    Reflex-flip refresh, for their very first turn), NOT a per-turn
    "reserved" flag - within their own weapon range of `e` gets this
    attack, spending 1 AP from that pool AND the charge on use, not on
    hit (same "an Encounter/Interrupt ability is expended by using it"
    rule as Feint).

    Unlike _take_pc_turn's own `_bonus_attack` closure (Whirlwind/
    Flurry/Ricochet Shot - a genuinely free extra swing layered on top
    of an already-resolved primary attack, deliberately no Gambling),
    Magehunter's Interrupt IS a full, independent weapon attack - so it
    keeps Gambling (pc_gamble_count), same as any normal attack.
    Returns the total damage dealt, for run_fight's own party damage
    tally."""
    total_dmg = 0
    for pc in pcs:
        # techniques.csv's own Tags column has Magehunter as
        # "Martial, Encounter" - glossary.md's [Encounter]: "expended
        # when you use them, and you regain their use when the
        # encounter ends" - a real once-per-encounter charge (same
        # rule Whirlwind/Flurry/Ricochet Shot already follow), NOT
        # repeatable every time AP and a valid target line up.
        # `magehunter_charge_used` is a separate flag from `ap_bank` on
        # purpose - the AP this PC's next own turn loses from actually
        # using the Interrupt is real and persists even after the
        # charge itself is spent, so ap_bank keeps tracking regardless.
        if (pc['health'] <= 0 or pc.get('magehunter_charge_used')
                or pc.get('ap_bank', 0) < T.MAGEHUNTER_AP_COST):
            continue
        if e['health'] <= 0:
            break
        reach = effective_range(pc)
        if movement_on and _distance(pc['pos'], e['pos']) > reach:
            continue
        pc['ap_bank'] -= T.MAGEHUNTER_AP_COST
        pc['magehunter_charge_used'] = True
        defense = enemy_defense_for_pc_attack(pc, e)
        resist = enemy_resist_for_pc_attack(pc, e)
        gambles = pc_gamble_count(pc, e)
        crippled = pc.get('crippled', 0)
        bad_luck = tactics.defense_has_bad_luck(e, pc.get('opp_def', 'Parry/Dodge'))
        luck_bonus = tactics.perfect_strike_bonus(pc)
        card = resolve_card(pc.get('good_luck', 0) + luck_bonus, bad_luck)
        roll = pc['skill_total'] - crippled + card - 2 * gambles
        hit = roll >= defense
        e['harried'] = e.get('harried', 0) + 1
        dmg = raw_dmg = protected_absorbed = 0
        if hit:
            raw_dmg = pc['damage'] + gambles + (1 if tactics.sift_bonus(pc) else 0)
            dmg = max(0, raw_dmg - resist)
            protected = e.get('protected', 0)
            if protected > 0 and dmg > 0:
                protected_absorbed = min(dmg, protected)
                e['protected'] -= protected_absorbed
                dmg -= protected_absorbed
            e['health'] -= dmg
            total_dmg += dmg
        if party_log:
            party_log(unit=pc['name'], action='attack', target=e['name'], roll=roll, defense=defense,
                       hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, protected_absorbed=protected_absorbed,
                       target_hp_after=e['health'], target_harried_after=e.get('harried', 0),
                       via=f"{pc['weapon_name']} (Magehunter)", turn_shift=None)
    return total_dmg


def _parting_shot_interrupt(e, pcs, movement_on, party_log):
    """Parting Shot (T076): "Make an attack with a close-range weapon
    against the target [...] a creature within range of a close-range
    weapon you are wielding would move [...] outside your range" -
    called from _take_enemy_turn right before a Kiting enemy's own
    retreat step (`tactics.move_kite`, the only "moves away from its
    target" behavior this simulator has - every other Battle Tactic
    only closes distance, never retreats, so this is Parting Shot's one
    real trigger here) actually moves `e`, checked against `e`'s
    CURRENT position (before that retreat). "Being Pushed" isn't
    modeled (no Push ability exists in this simulator - see
    tunables.ABILITY_COST's own comment on positional effects left
    out).

    Same `ap_bank`/once-per-encounter-charge shape as
    _magehunter_interrupt (`pc['parting_shot_charge_used']`,
    T.PARTING_SHOT_AP_COST), but gated on "close-range weapon"
    specifically (`not pc.get('attack_range')` - party.py only sets
    `attack_range` for a real ranged `Weapon` pick; the blank default,
    2H Heavy Melee, and Unarmed all leave it unset, falling back to
    T.MELEE_RANGE, which IS a close-range weapon for this purpose) -
    a PC with a bow or War Magic doesn't get to punish a retreat this
    way. Returns the total damage dealt, for run_fight's own party
    damage tally."""
    total_dmg = 0
    for pc in pcs:
        if (pc['health'] <= 0 or pc.get('parting_shot_charge_used')
                or pc.get('ap_bank', 0) < T.PARTING_SHOT_AP_COST
                or pc.get('attack_range')):
            continue
        if e['health'] <= 0:
            break
        reach = effective_range(pc)
        if movement_on and _distance(pc['pos'], e['pos']) > reach:
            continue
        pc['ap_bank'] -= T.PARTING_SHOT_AP_COST
        pc['parting_shot_charge_used'] = True
        defense = enemy_defense_for_pc_attack(pc, e)
        resist = enemy_resist_for_pc_attack(pc, e)
        gambles = pc_gamble_count(pc, e)
        crippled = pc.get('crippled', 0)
        bad_luck = tactics.defense_has_bad_luck(e, pc.get('opp_def', 'Parry/Dodge'))
        luck_bonus = tactics.perfect_strike_bonus(pc)
        card = resolve_card(pc.get('good_luck', 0) + luck_bonus, bad_luck)
        roll = pc['skill_total'] - crippled + card - 2 * gambles
        hit = roll >= defense
        e['harried'] = e.get('harried', 0) + 1
        dmg = raw_dmg = protected_absorbed = 0
        if hit:
            raw_dmg = pc['damage'] + gambles + (1 if tactics.sift_bonus(pc) else 0)
            dmg = max(0, raw_dmg - resist)
            protected = e.get('protected', 0)
            if protected > 0 and dmg > 0:
                protected_absorbed = min(dmg, protected)
                e['protected'] -= protected_absorbed
                dmg -= protected_absorbed
            e['health'] -= dmg
            total_dmg += dmg
        if party_log:
            party_log(unit=pc['name'], action='attack', target=e['name'], roll=roll, defense=defense,
                       hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, protected_absorbed=protected_absorbed,
                       target_hp_after=e['health'], target_harried_after=e.get('harried', 0),
                       via=f"{pc['weapon_name']} (Parting Shot)", turn_shift=None)
    return total_dmg


def _take_enemy_turn(e, enemies, pcs, rnd, movement_on, trace, enemy_log, party_log=None):
    """One enemy's full turn (see module docstring's "How a turn
    works"). Returns any damage a Magehunter/Parting Shot Interrupt
    dealt to `e` this turn (0 normally), for run_fight's own party
    damage tally - everything else about a plain enemy turn stays a
    side-effect-only call, same as before."""
    if e['health'] <= 0:
        return 0
    abilities = e.get('abilities', [])
    if 'Durable' in abilities and e.get('protected', 0) < 4:
        e['protected'] = e.get('protected', 0) + 1
    living_pcs = [p for p in pcs if p['health'] > 0]
    if not living_pcs:
        return 0
    interrupt_dmg = 0
    fighting_style = e.get('fighting_style', 'Guarded')
    ap = T.AP_PER_TURN
    target = tactics.select_target(e, living_pcs, movement_on)
    moved = False
    in_range = True
    start_pos = e.get('pos')
    if movement_on:
        # Parting Shot (T076): checked against `e`'s position BEFORE its
        # own retreat step, since the trigger is the creature trying to
        # move away, not having already moved - only Kiting units ever
        # move away from their target at all (tactics.move_kite is the
        # only "retreat" Battle Tactic; everything else only closes
        # distance) - see _parting_shot_interrupt's own docstring.
        if e.get('battle_tactic') == 'Kiting':
            interrupt_dmg += _parting_shot_interrupt(e, pcs, movement_on, party_log)
            if e['health'] <= 0:
                return interrupt_dmg
        ap, in_range, moved = spend_movement_ap(e, target, ap, effective_range(e))
    # Guarded's own stand-still bonus (tactics.defense_has_bad_luck) -
    # set here, at the end of resolving this enemy's own movement, so
    # it's ready for whoever attacks this enemy next (in initiative
    # order, not necessarily "next round") to check - a "held its
    # ground last turn" bonus that lags by however long it takes this
    # enemy's turn to come back around, same idea as before real
    # initiative, just no longer tied to a fixed "one round" gap.
    e['guarded_active'] = (fighting_style == 'Guarded' and not moved)
    if moved:
        _log(trace, round=rnd, side='enemy', unit=e['name'], action='move', pos=e['pos'],
             in_range=in_range, spaces=_distance(start_pos, e['pos']))
    if movement_on and not in_range:
        return interrupt_dmg

    cap = tactics.attack_cap(e)
    attacks_made = 0
    while ap >= T.ATTACK_AP_COST and (cap is None or attacks_made < cap) and target is not None:
        # Magehunter (T075): "a creature within your weapon's range
        # declares a Spell, before it is cast" - checked right before
        # this attack resolves, only for a Spell Action (tunables.
        # ACTIONS' "Melee Spell"/"Ranged Spell") - see
        # _magehunter_interrupt's own docstring. A kill here (e['health']
        # <= 0) ends this enemy's turn immediately, same as any other
        # kill mid-attack-sequence - a dead caster's own attack never
        # goes off.
        if e['action'] in ('Melee Spell', 'Ranged Spell'):
            interrupt_dmg += _magehunter_interrupt(e, pcs, movement_on, party_log)
            if e['health'] <= 0:
                break
        roll = e['accuracy'] + (flip_best_of(2) if fighting_style == 'Aimed Shot' else flip())
        opp_def_val = pc_defense_for(target, e['opp_def'])
        # rulebook.md's Harried trigger (see enemy_defense_for_pc_attack's
        # own comment) - only when this attack was actually opposed by
        # Parry or Dodge, not Bodily/Mental (e.g. a Fire Spell opposed
        # by Dodge alone still counts; Melee Spell/Ranged Spell here are
        # both opp_def='Dodge', so this fires for every Action in
        # tunables.ACTIONS today, but the check stays explicit rather
        # than assuming that never changes).
        if e['opp_def'] in ('Parry/Dodge', 'Dodge'):
            target['harried'] = target.get('harried', 0) + 1
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
                       hit=hit, dmg=dmg, raw_dmg=raw_dmg, resist=resist, target_hp_after=target['health'],
                       target_harried_after=target.get('harried', 0), via=e['action'])
        if target['health'] <= 0:
            target = _retarget(e, [p for p in pcs if p['health'] > 0], movement_on)
    # Harried clears at the end of its own bearer's turn (glossary.md) -
    # this enemy can only have taken damage from its own past turns, not
    # this one (only the acting unit deals damage on its own turn), so
    # e['health'] is still whatever it was on entry if we got this far.
    if e.get('harried', 0) > 0:
        e['harried'] = 0
    return interrupt_dmg


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

    Every round replays the same fixed turn order, rolled once at
    encounter start (`_roll_initiative` - rulebook.md's real Reflex-flip
    rule, ties broken by re-flipping just the tied units), skipping
    whoever's already dead - PCs and enemies interleaved by their own
    Reflex, not "all 4 PCs, then all enemies" like this file used to do.

    `trace`: pass a list (e.g. `trace=[]`) to have this call record what
    happened, round by round, instead of just returning the final tally
    - meant for actually looking at one fight (`narrate_fight.py`), not
    for `simulate()`'s thousands of trials, so it's `None` (skip
    entirely, via `_log`) by default. Events are plain dicts; a
    `round=0, type='initiative'` event (once per fight, before round 1)
    carries the turn order itself (`order`: `[{'side', 'unit'}, ...]`,
    highest Reflex first). Every other event carries `round`; a
    `type='positions'` event (movement mode only,
    once per round, before any of that round's actions) snapshots every
    living unit's `pos`/`health`; everything else carries `side`
    ('party'/'enemy') and `unit`, and is either `action='move'` (this
    unit actually spent AP moving this turn - `pos`, `in_range` says
    whether that got it into range or it's still short and doesn't
    attack this round, `spaces` is the straight-line distance actually
    covered this turn, for reviewing whether a unit's Speed is really
    the bottleneck), `action='attack'` (`target`, `roll`, `defense`,
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
    not just the final post-Resist number. Also carries
    `target_harried_after` - the target's own Harried stack count right
    after this attack (glossary.md's -1 Dodge/Parry per stack; this
    attack's own `defense` already reflects whatever stacks existed
    *before* it, per enemy_defense_for_pc_attack/pc_defense_for's own
    "regardless of the attack's result" trigger). Both `action='attack'` and
    `action='heal'` also carry `via` - the name of whatever actually
    produced this action, for reviewing what a unit's really doing
    round to round: a PC's own `weapon_name` (party.py - the `Weapon`
    cell, or "Melee" for the blank default) or a Card Technique's own
    name ("Bottled Fire"/"Healing Potion"/"Second Wind"/"Healing
    Magic") on the party side, an enemy's own `action` (sample_
    enemies.csv's Action column - "Offensive Melee", "Ranged Weapon",
    ...) on the enemy side. A party-side `action='attack'` event also
    carries `turn_shift` - a plain description string when this hit
    triggered a `turn_order_shift`/`self_turn_order_advance` test field
    (`None` otherwise), for spotting these in a replay. A final
    `type='result'` event carries `winner`."""
    if seed is not None:
        random.seed(seed)
    pcs = make_party(tier, good_luck=good_luck)
    for p in pcs:
        if _has_interrupt_tech(p):
            # rulebook.md: "When you flip Reflex to join an encounter...
            # you lose any existing Action Points and gain 4 Action
            # Points in their place" - the same refresh _take_pc_turn's
            # own end-of-turn step re-applies from here on (see
            # ap_bank's own comment there).
            p['ap_bank'] = T.AP_PER_TURN
    if enemies is not None:
        enemies = [copy.deepcopy(e) for e in enemies]
    else:
        enemies = [copy.deepcopy(e) for e in make_level_encounter(enemy_level, n_enemies)]
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

    # Rolled once at encounter start, fixed for the whole fight (see
    # _roll_initiative's own docstring) - every round replays this same
    # order, skipping whoever's already dead.
    order = _roll_initiative(pcs, enemies, trace)

    def _winner():
        if all(e['health'] <= 0 for e in enemies):
            return 'party'
        if all(p['health'] <= 0 for p in pcs):
            return 'enemies'
        return None

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

        for side, unit in list(order):
            if unit['health'] <= 0:
                continue
            if side == 'party':
                made, dealt = _take_pc_turn(unit, pcs, enemies, rnd, movement, trace, party_log, order)
                pc_attacks += made
                pc_damage_dealt += dealt
            else:
                pc_damage_dealt += _take_enemy_turn(unit, enemies, pcs, rnd, movement, trace, enemy_log, party_log)
            winner = _winner()
            if winner:
                _log(trace, round=rnd, type='result', winner=winner)
                party_hp_pct = (sum(max(0, p['health']) for p in pcs) / sum(p['max_health'] for p in pcs)
                                if winner == 'party' else 0.0)
                return dict(winner=winner, rounds=rnd, party_hp_pct=party_hp_pct,
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
