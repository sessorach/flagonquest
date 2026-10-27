"""
Minimal 2D battlefield geometry for combat_sim.py's optional movement
mode (run_fight(..., movement=True)) - a bounded ARENA_SIZE x ARENA_SIZE
square (tunables.ARENA_SIZE) of whole spaces, matching the real game:
units move 1 space at a time (no fractional spaces), and 1 Speed buys 1
space of movement in any of the 8 directions - orthogonal or diagonal -
for the same cost, so distance is Chebyshev ("king-move") distance, not
Euclidean. "Space" and "meter" are still the same unit as every other
Range value already in this project (a Range of 19 means 19 spaces
away), just measured in whole steps now instead of a continuous ruler.
Deliberately crude otherwise, matching the rest of this simulator: no
obstacles, no formations, no area effects - just enough to ask "can a
ranged or kiting unit actually stay out of melee reach against a given
Speed/Range matchup," which is what this mode exists to test.
"""
import tunables as T

# Difficult Terrain (glossary.md): {space: degrees}. "To cross a meter of
# space that has Difficult Terrain, a character takes an extra meter of
# Speed for each degree... A character can still move at least 1 space."
# combat_sim resets it each fight; War Magic's Glacier adds to it
# (2026-10-27). Shifts ignore it, and so do the Play Style plans that set
# a PC's spot directly (play_styles), a known shortcut.
TERRAIN = {}


def _cost(cell):
    return 1 + TERRAIN.get(clamp(cell), 0)


def distance(a, b):
    """Chebyshev distance - max(|dx|, |dy|), since a diagonal step
    covers 1 space for the same 1-Speed cost as an orthogonal one (the
    real grid-movement rule, not Euclidean "as the crow flies"). Two
    units are "adjacent" (melee range) exactly when this is 1."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def clamp(pos):
    x, y = pos
    bound = T.ARENA_SIZE
    return (min(max(x, 0), bound), min(max(y, 0), bound))


def _step_toward(x, y, tx, ty):
    """One space, in whichever of the 8 directions actually closes the
    Chebyshev distance to (tx, ty) - diagonal when both axes still
    differ, orthogonal once one axis is already aligned. Greedily
    recomputing this each step (rather than committing to a fixed
    direction up front) is what makes a multi-step move trace the real
    shortest king-move path: diagonal first, then straight the rest of
    the way, never more steps than the Chebyshev distance requires."""
    dx = (tx > x) - (tx < x)
    dy = (ty > y) - (ty < y)
    return x + dx, y + dy


def move_toward(pos, target, speed, stop_at=0):
    """Move up to `speed` whole spaces toward `target`, one space at a
    time, stopping as soon as `stop_at` spaces of it (or closer) -
    checked after every single step, not just at the end, so a unit
    that enters range partway through its move doesn't overshoot. A
    melee unit stops at MELEE_RANGE (1 - adjacent), a ranged unit stops
    as soon as it's within its own attack range instead of closing all
    the way."""
    x, y = pos
    tx, ty = target
    budget, moved = speed, False
    while budget > 0:
        if distance((x, y), (tx, ty)) <= stop_at:
            break
        nx, ny = _step_toward(x, y, tx, ty)
        cost = _cost((nx, ny)) if TERRAIN else 1
        if cost > budget and moved:
            break
        budget -= cost
        x, y, moved = nx, ny, True
    return clamp((x, y))


def move_away(pos, threat, speed):
    """Move up to `speed` whole spaces directly away from `threat`, one
    space at a time - the simplest possible Kiting behavior: no pathing
    around anything (there is nothing else on the battlefield to path
    around), and no check for whether retreating is actually necessary
    this round. Reclamped after every step so a retreat that hits the
    arena edge partway through doesn't get pulled back in-bounds by the
    direction of a step it never actually took - a cornered kiter pinned
    against the wall stays pinned, a real, intended consequence of a
    bounded arena, not a bug to route around."""
    x, y = pos
    hx, hy = threat
    budget, moved = speed, False
    while budget > 0:
        if x == hx and y == hy:
            dx, dy = 1, 0  # can't compute a direction standing exactly on the threat; retreat +x arbitrarily
        else:
            dx = (x > hx) - (x < hx)
            dy = (y > hy) - (y < hy)
        cost = _cost((x + dx, y + dy)) if TERRAIN else 1
        if cost > budget and moved:
            break
        budget -= cost
        x, y, moved = *clamp((x + dx, y + dy)), True
    return (x, y)
