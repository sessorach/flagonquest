"""
Hook points: where a Technique, an enemy Ability or a rule plugs into a
fight, so combat_sim's turn code doesn't carry a named `if` for each one.

A handler registers for a point with `@on(point, key, order)`. `key` is
the name a unit has to carry for the handler to run - a PC's passive,
Card or Encounter Technique, or an enemy's Ability - or None for a rule
every unit gets. Handlers at one point run in `order`, then in the order
they were registered, so a point's sequence is written down in one place
(the ORDER numbers next to each handler) rather than implied by where
calls happen to sit in combat_sim.

`run(point, unit, ctx)` calls every handler that applies to `unit` and
adds up whatever they return (AP spent, Good Luck, ...; None counts as
0). When ctx has an `ap` field, each handler's return comes off it as
it goes, since those points' handlers return AP spent. `ctx` is a
SimpleNamespace the call site fills with what the point offers - see
POINTS for each one's fields.

Which handlers apply to a unit is worked out once per fight and kept on
the unit (`_hooks`), since a unit's Techniques and Abilities don't
change mid-fight. Tests that add a passive do it before the fight
starts, so they're picked up.
"""
import collections

POINTS = {
    # PC turn. ctx: pcs, enemies, rnd, movement_on, trace, log, ap, order
    "pc_turn_start": "start of a PC's turn, before it moves; returns AP spent",
    "pc_turn_end": "after its attacks and movement; returns AP spent",
    "pc_after_turn": "once the turn is over (turn-order changes); returns nothing",
    # A PC's attack. ctx: target, hit, parried, pool, mv (the Battle
    # Maneuver copy, or None), substitute, rnd, order, notes (log text)
    "attack_luck": "Good Luck on the attack; returns how many",
    "before_attack": "just before the flip (ctx also: mv, repeat); returns extra AP spent. "
                     "pc['_attack_bonus'] set here is extra damage on this attack if it hits",
    "hit_riders": "a hit or a Parry, before damage (ctx.hit / ctx.parried say which)",
    "after_hit": "after a hit's damage has landed",
    "attack_resolved": "after the attack, hit or not, before it's logged (ctx also: dodged, dmg, repeat)",
    "after_attack": "after the attack and its bonus attacks; returns AP spent",
    # Enemy turn. ctx: pcs, enemies, movement_on, log
    "enemy_turn_start": "start of an enemy's turn",
    # An enemy's attack on a PC. ctx: target, prof, dmg, applied (log
    # text), hit, parried
    "enemy_hit_damage": "a hit's damage before it lands; returns the new damage",
    "enemy_hit_riders": "after a hit's damage has landed",
    "enemy_hit_or_parried": "after a hit or a Parry",
    # Reactions. ctx varies; see each call site.
    "pc_damaged_enemy": "a PC's attack took Health off this enemy (unit = the enemy; ctx: pc, dmg)",
    "pc_parried": "this PC Parried an enemy attack (ctx: rnd)",
    "pc_hit": "a damaging enemy attack hit this PC (ctx: attacker, dmg, prof, applied)",
    "fight_start_order": "the turn order's just been rolled (unit = a PC; ctx: order)",
    "attack_declared": "an enemy weapon attack is declared on this PC, before the flip "
                       "(ctx: attacker, prof, pcs, enemies, movement_on, log); returns damage dealt to the attacker",
    "attack_targeting": "an enemy attack (or Hex) at a PC, before its flip; run for the target, then each ally "
                        "(ctx: attacker, prof, target, opp_def, mode, pcs, enemies, movement_on, log). A handler may "
                        "set ctx.target (move it to this PC), ctx.opp_def, ctx.no_harried, or ctx.cancel",
    "attack_flipped": "an enemy attack's flip is made, before it hits or misses (unit = the target; ctx: attacker, "
                      "prof, roll, defense, opp_def, used_parry, mode, pcs, movement_on, log). A handler may set "
                      "ctx.defense, or ctx.parry (the attack is Parried)",
    "pc_would_drop": "this PC is about to be Downed by a Health loss, any source (ctx: loss, notes); "
                     "returns 1 if it stopped the Down (it sets the PC's Health itself)",
    "ally_would_drop": "a hit is about to Down an ally (unit = a PC who might step in; ctx: ally, loss); "
                       "returns 1 if this PC took it on",
    "enemy_left_reach": "an enemy walked or was Pushed out of this PC's reach (ctx: enemy, start, pushed, pcs, log); "
                        "returns damage dealt",
    "pc_left_reach": "a PC walked out of this enemy's reach (ctx: pc, start, pcs, enemies, rnd)",
}

_REG = collections.defaultdict(list)
_SEQ = [0]


def on(point, key=None, order=50):
    if point not in POINTS:
        raise KeyError(f"unknown hook point {point!r}")

    def deco(fn):
        _SEQ[0] += 1
        _REG[point].append((order, _SEQ[0], key, fn))
        _REG[point].sort(key=lambda h: (h[0], h[1]))
        _SHARED.clear()
        return fn
    return deco


def has(unit, key):
    return (key in unit.get("passives", ()) or key in unit.get("techs", ())
            or key in unit.get("abilities", ()))


# Handler lists shared by every unit that knows the same names
# (2026-10-27): a fight makes fresh unit dicts, and building each one's
# lists from _REG was a tenth of a fight's run time.
_SHARED = {}


def handlers(point, unit):
    cache = unit.get("_hooks")
    if cache is None:
        cache = unit["_hooks"] = {}
        unit["_hook_names"] = (frozenset(unit.get("passives", ())) | frozenset(unit.get("techs", ()))
                               | frozenset(unit.get("abilities", ())))
    hs = cache.get(point)
    if hs is None:
        names = unit["_hook_names"]
        key = (point, names)
        hs = _SHARED.get(key)
        if hs is None:
            hs = _SHARED[key] = [fn for _, _, k, fn in _REG[point] if k is None or k in names]
        cache[point] = hs
    return hs


def run(point, unit, ctx=None):
    total = 0
    for fn in handlers(point, unit):
        r = fn(unit, ctx)
        if r:
            total += r
            # Points that spend AP keep the running total on ctx.ap, so
            # each handler sees what the ones before it left.
            if ctx is not None and hasattr(ctx, "ap"):
                ctx.ap -= r
    return total
