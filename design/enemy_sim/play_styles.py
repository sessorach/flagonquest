"""
Play styles (2026-10-08): how cautious each PC plays, per the designer's
notes on real tables (TABLE_PLAY_NOTES.md). Tanky characters dive in;
fragile ones hang back and do what they safely can; some sit in between.

- **Diver** - the sim's default turn (tactics.PARTY_TARGETING): goes for
  the best target it can reach and doesn't mind where it ends up.
  `plan_turn` returns None for a Diver, so combat_sim runs its usual turn.
- **Skirmisher** - attacks twice from where it stands if it can; if it's
  standing next to more enemies than it's comfortable with, attacks once
  and steps away. Otherwise moves only as far in as it safely can: a
  melee skirmisher will end next to its own target but not next to a
  second enemy; a ranged one won't end next to any enemy.
- **Back-liner** - keeps BACKLINE_KEEP_AWAY spaces from every enemy if it
  can. Shoots twice when something's in range; with an enemy closing in,
  attacks once and backs off; otherwise approaches only as far as is
  safe, keeping enough AP for one attack. A melee back-liner (Hanforth,
  a healer with fists) only fights hit-and-run: step in, hit once, step
  back out.

Plus RECKLESS_CHANCE of any turn played like a Diver regardless, since
real players get reckless for the fun of it.

Targets are rated by the threat they pose to the party per point of
Health (tactics.enemy_threat), times the damage this PC expects to deal
them, so a Harried target (easier to hit) and a hurt one both rate
higher. That's how "pile onto the Harried one" falls out without a
separate rule.

`plan_turn` only decides; combat_sim._take_pc_turn carries the plan out
(moves, the capped attack loop, the retreat) so every attack still goes
through the one well-tested attack block.
"""
import math
import random
from dataclasses import dataclass, field

import movement
import tactics
import tunables as T

STYLES = ("Diver", "Skirmisher", "Back-liner")


@dataclass
class Plan:
    target: dict = None          # None: no attack this turn
    pre_pos: tuple = None        # where to stand before attacking (None: stay)
    pre_moves: int = 0           # move actions that costs
    max_attacks: int = 2
    retreat: bool = False        # spend leftover AP backing away afterwards
    note: str = ""


def default_style(row_weapon_range, armor, has_shield, support):
    """A blank Play Style cell: healers and long-range shooters hang back,
    short-range shooters and lightly armored melee skirmish, armored or
    shielded melee dives in."""
    if support:
        return "Back-liner"
    if row_weapon_range and row_weapon_range > T.MELEE_RANGE:
        return "Back-liner" if row_weapon_range >= 10 else "Skirmisher"
    if armor in ("Medium", "Heavy") or has_shield:
        return "Diver"
    return "Skirmisher"


def _reach(u):
    return u.get('attack_range') or T.MELEE_RANGE


def _dist(a, b):
    return movement.distance(a, b)


def _adjacent(pos, enemies):
    return [e for e in enemies if _dist(pos, e['pos']) <= T.MELEE_RANGE]


def _within(pos, enemies, radius):
    return [e for e in enemies if _dist(pos, e['pos']) <= radius]


def expected_damage(pc, t):
    """What one plain attack from `pc` is expected to deal `t`: chance to
    hit its current Defense (Harried included) times damage after
    Resist. No Gambling or luck - this is for choosing, not resolving."""
    import combat_sim as cs  # lazy: combat_sim imports this module
    defense = cs.enemy_defense_for_pc_attack(pc, t)
    resist = cs.enemy_resist_for_pc_attack(pc, t)
    skill = pc['skill_total'] - pc.get('crippled', 0)
    p_hit = sum(1 for f in range(1, 14) if skill + f >= defense) / 13
    return p_hit * max(0, pc['damage'] - resist)


def rating(pc, t, allies):
    return tactics.enemy_threat(t, allies) / max(1, t['health']) * expected_damage(pc, t)


def _best(pc, ts, allies):
    return max(ts, key=lambda t: (rating(pc, t, allies), -t['health'])) if ts else None


def _safe_approach(pos, goal, max_spaces, enemies, keep, reach):
    """Step toward `goal` one space at a time, up to `max_spaces`, never
    onto a space within `keep` of an enemy, stopping once within `reach`
    of the goal. Returns (position, spaces moved)."""
    x, y = pos
    moved = 0
    for _ in range(max_spaces):
        if _dist((x, y), goal) <= reach:
            break
        nx, ny = movement._step_toward(x, y, goal[0], goal[1])
        if _within((nx, ny), enemies, keep):
            break
        x, y = movement.clamp((nx, ny))
        moved += 1
    return (x, y), moved


def retreat_pos(pos, enemies, spaces):
    """Back away from the nearest enemy, `spaces` spaces."""
    if not enemies:
        return pos
    nearest = min(enemies, key=lambda e: _dist(pos, e['pos']))
    return movement.move_away(pos, nearest['pos'], spaces)


def plan_turn(pc, targets, allies, ap):
    """The plan for this PC's turn, or None to run the default (Diver)
    turn. `targets` are the living enemies; `ap` is what's left after
    healing/Challenge."""
    style = pc.get('play_style') or "Diver"
    if style == "Diver" or 'pos' not in pc or not targets:
        return None
    if random.random() < T.RECKLESS_CHANCE:
        return None  # a reckless turn: play it like a Diver
    if style == "Skirmisher":
        return _plan_skirmisher(pc, targets, allies, ap)
    if style == "Back-liner":
        return _plan_backliner(pc, targets, allies, ap)
    return None


def _moves_for(spaces, speed):
    return math.ceil(spaces / speed) if spaces > 0 else 0


def _plan_skirmisher(pc, targets, allies, ap):
    reach, speed, here = _reach(pc), max(1, tactics._speed(pc)), pc['pos']
    melee = reach <= T.MELEE_RANGE
    limit = 1 if melee else 0  # enemies it'll end its turn next to
    in_reach = [t for t in targets if _dist(here, t['pos']) <= reach]
    if in_reach:
        t = _best(pc, in_reach, allies)
        if len(_adjacent(here, targets)) > limit:
            return Plan(target=t, max_attacks=1, retreat=True, note="attack, then step away")
        return Plan(target=t, max_attacks=2, note="double attack from here")
    # One move, then one attack, ending somewhere comfortable.
    options = []
    for t in targets:
        dest = movement.move_toward(here, t['pos'], speed, stop_at=reach)
        if _dist(dest, t['pos']) <= reach and len(_adjacent(dest, targets)) <= limit:
            options.append((rating(pc, t, allies), t, dest))
    if options and ap >= T.MOVE_AP_COST + T.ATTACK_AP_COST:
        _, t, dest = max(options, key=lambda o: (o[0], -o[1]['health']))
        return Plan(target=t, pre_pos=dest, pre_moves=1, max_attacks=1, note="move in, attack once")
    # Nothing safe to hit this turn: close in as far as is comfortable.
    t = _best(pc, targets, allies)
    keep = 0 if melee else T.MELEE_RANGE
    dest, spaces = _safe_approach(here, t['pos'], speed * (ap // T.MOVE_AP_COST), targets, keep, reach)
    if melee and len(_adjacent(dest, targets)) > limit:
        dest, spaces = here, 0
    return Plan(target=None, pre_pos=dest, pre_moves=_moves_for(spaces, speed), max_attacks=0,
                note="close in, nothing safe to hit")


def _plan_backliner(pc, targets, allies, ap):
    reach, speed, here = _reach(pc), max(1, tactics._speed(pc)), pc['pos']
    if reach <= T.MELEE_RANGE:
        return _plan_hit_and_run(pc, targets, allies, ap, speed, here)
    keep = T.BACKLINE_KEEP_AWAY
    in_reach = [t for t in targets if _dist(here, t['pos']) <= reach]
    threatened = bool(_within(here, targets, keep))
    if threatened:
        if in_reach:
            return Plan(target=_best(pc, in_reach, allies), max_attacks=1, retreat=True,
                        note="attack, then back off")
        dest = retreat_pos(here, targets, speed)
        after = [t for t in targets if _dist(dest, t['pos']) <= reach]
        return Plan(target=_best(pc, after, allies), pre_pos=dest, pre_moves=1, max_attacks=1,
                    retreat=True, note="back off, then attack")
    if in_reach:
        return Plan(target=_best(pc, in_reach, allies), max_attacks=2, note="double attack from here")
    # Approach just far enough to shoot, never within `keep` of an enemy,
    # keeping 2 AP for one attack.
    max_moves = max(0, (ap - T.ATTACK_AP_COST) // T.MOVE_AP_COST)
    options = []
    for t in targets:
        dest, spaces = _safe_approach(here, t['pos'], speed * max_moves, targets, keep, reach)
        if _dist(dest, t['pos']) <= reach:
            options.append((rating(pc, t, allies), t, dest, spaces))
    if options:
        _, t, dest, spaces = max(options, key=lambda o: (o[0], -o[3]))
        return Plan(target=t, pre_pos=dest, pre_moves=_moves_for(spaces, speed), max_attacks=1,
                    note="edge into range, attack once")
    t = _best(pc, targets, allies)
    dest, spaces = _safe_approach(here, t['pos'], speed * (ap // T.MOVE_AP_COST), targets, keep, reach)
    return Plan(target=None, pre_pos=dest, pre_moves=_moves_for(spaces, speed), max_attacks=0,
                note="edge closer, nothing safe to hit")


def _plan_hit_and_run(pc, targets, allies, ap, speed, here):
    adjacent = _adjacent(here, targets)
    if adjacent:
        return Plan(target=_best(pc, adjacent, allies), max_attacks=1, retreat=True, note="hit, then step back")
    if ap >= 2 * T.MOVE_AP_COST + T.ATTACK_AP_COST:
        options = []
        for t in targets:
            dest = movement.move_toward(here, t['pos'], speed, stop_at=T.MELEE_RANGE)
            if _dist(dest, t['pos']) <= T.MELEE_RANGE and len(_adjacent(dest, targets)) <= 1:
                options.append((rating(pc, t, allies), t, dest))
        if options:
            _, t, dest = max(options, key=lambda o: (o[0], -o[1]['health']))
            return Plan(target=t, pre_pos=dest, pre_moves=1, max_attacks=1, retreat=True,
                        note="step in, hit, step back")
    return Plan(target=None, max_attacks=0, note="hold back")
