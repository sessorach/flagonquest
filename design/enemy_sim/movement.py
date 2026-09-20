"""
Minimal 2D battlefield geometry for combat_sim.py's optional movement
mode (run_fight(..., movement=True)) - a bounded ARENA_SIZE x ARENA_SIZE
square (tunables.ARENA_SIZE), continuous (float) coordinates, not a
snapped grid ("spaces" here just means meters, matching every other
Range value already in this project). Deliberately crude, matching the
rest of this simulator: no obstacles, no formations, no area effects -
just enough to ask "can a ranged or kiting unit actually stay out of
melee reach against a given Speed/Range matchup," which is what this
mode exists to test.
"""
import math
import tunables as T


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def clamp(pos):
    x, y = pos
    bound = T.ARENA_SIZE
    return (min(max(x, 0), bound), min(max(y, 0), bound))


def move_toward(pos, target, speed, stop_at=0.0):
    """Move up to `speed` meters toward `target`, stopping `stop_at`
    meters short of it rather than walking on top of it - a melee unit
    stops at MELEE_RANGE (roughly adjacent), a ranged unit stops as soon
    as it's within its own attack range instead of closing all the way."""
    d = distance(pos, target)
    need = max(0.0, d - stop_at)
    if need <= 0 or d == 0:
        return pos
    step = min(speed, need)
    t = step / d
    return clamp((pos[0] + (target[0] - pos[0]) * t, pos[1] + (target[1] - pos[1]) * t))


def move_away(pos, threat, speed):
    """Move up to `speed` meters directly away from `threat` - the
    simplest possible Kiting behavior: no pathing around anything (there
    is nothing else on the battlefield to path around), and no check for
    whether retreating is actually necessary this round. A cornered
    kiter pinned against the arena edge stays pinned - a real, intended
    consequence of using a bounded arena, not a bug to route around."""
    d = distance(pos, threat)
    if d == 0:
        dx, dy = 1.0, 0.0  # can't compute a direction standing exactly on the threat; retreat +x arbitrarily
    else:
        dx, dy = (pos[0] - threat[0]) / d, (pos[1] - threat[1]) / d
    return clamp((pos[0] + dx * speed, pos[1] + dy * speed))
