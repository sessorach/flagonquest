"""How strong is a party, and what does each member add? (2026-10-30)

The designer's yardstick: the enemy Levels the model already has
(tunables.ENEMY_LEVEL_UP builds every sample enemy that many Levels up
through the same PC-style builder), read as days won (day_sim.py: two
fights, healing, a night's rest). No fractional steps: a party that
still wins 20% of its days a Level up, where others win 5%, is a strong
signal by itself.

Each member's contribution is read against a stand-in: the Baseline
Party Member for that Level (sample_pcs.csv, a plain on-level fighter
with no Techniques), topped up with plain Stats and Skills to the combat
budget (combat_xp.py: 105 / 145 XP of 125 / 175, the designer's
mid-tier focal point, the rest going to life outside fights), so
"contribution" means what a character's own choices add over a plain
fighter with the same combat share.

- `days_won(names, swaps, level, up, n)`: days won, plus how one-sided
  the first fight of each day was.
- `shapley(names, level, up, n)`: every combination of the four with the
  rest swapped for stand-ins (16 readings), each member's Shapley value
  (their average added days won, over every order they could join in)
  and every pair's interaction (positive: worth more together; negative:
  one makes the other partly redundant).
"""
import itertools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party, tunables as T  # noqa: E402
import day_sim  # noqa: E402
import build_optimizer as bo  # noqa: E402

from combat_xp import COMBAT_BUDGET as BUDGET  # 105 / 145: the rest goes to life outside fights
STAND_IN = {L: f"Baseline Tier {L} Party Member" for L in (1, 2, 3, 4, 5)}
# An even rotation, the way a plain fighter would spread XP: the Stats,
# then the Skills a melee fighter's Defenses and attack use.
_STAT_ORDER = ("Agility", "Body", "Essence", "Cunning", "Mind")
_SKILL_ORDER = ("Melee", "Acrobatics", "Resilience", "Insight", "Composure", "Awareness", "Athletics")


def stand_in(level):
    """The Baseline Party Member's build, topped up to BUDGET[level] XP
    with plain Stats and Skills (rank cap 4 at Level 2, 5 at Level 3),
    at most 2 left over."""
    b = party.read_build(party._rows()[STAND_IN[level]]["Build"])
    b = {k: (dict(v) if isinstance(v, dict) else v) for k, v in b.items()}
    cap = {2: 4, 3: 5}[level]
    import combat_xp
    # The budget is combat XP; the Skills it already has outside fights
    # are its life outside them.
    left = BUDGET[level] - combat_xp.split(b)[0]
    order = [("statPoints", s) for s in _STAT_ORDER] + [("skillPoints", s) for s in _SKILL_ORDER]
    progress = True
    while left > 2 and progress:
        progress = False
        for kind, k in order:
            v = int(b[kind][k])
            cost = 2 * (v + 1) if kind == "statPoints" else v + 1
            if v < cap and cost <= left:
                b[kind][k] = v + 1
                left -= cost
                progress = True
    return b


def _members(names, keep, level):
    """`names` with everyone not in `keep` swapped for the stand-in."""
    out, swaps = [], {}
    for i, n in enumerate(names):
        if i in keep:
            out.append(n)
        else:
            out.append(STAND_IN[level])
    return out


def days_won(names, level, up, n, swaps=None, seed=0):
    """Days won (of 4n) with enemies `up` Levels above their own, and the
    first fight of each day: how many ended in two rounds or less with
    nobody Wounded (one-sided), and how many were lost."""
    T.ENEMY_LEVEL_UP = up
    day_sim.set_mult(1.0)
    swaps = dict(swaps or {})
    rows = party._rows()
    si = STAND_IN[level]
    if si in names and si not in swaps:
        b = stand_in(level)
        swaps[si] = ({"build": b}, None)
    try:
        recs = day_sim.run(names, swaps, level, n, seed=seed)
    finally:
        T.ENEMY_LEVEL_UP = 0
    won = sum(not r["lost"] for r in recs)
    first = [r.get("first") for r in recs if r.get("first")]
    trivial = sum(1 for f in first if f["won"] and f["rounds"] <= 2 and not f["wounded"])
    return dict(won=won, days=len(recs), trivial=trivial, first_lost=sum(1 for f in first if not f["won"]),
                fights=len(first))


def _job(args):
    names, keep, level, up, n = args
    return keep, days_won(_members(names, keep, level), level, up, n)


def shapley(names, level, up, n, pool=None):
    """Each member's Shapley value and every pair's interaction, in days
    won (share of days, 0-1), against stand-ins."""
    idx = range(len(names))
    subsets = [frozenset(c) for k in range(len(names) + 1) for c in itertools.combinations(idx, k)]
    jobs = [(names, s, level, up, n) for s in subsets]
    res = dict((pool.map if pool else map)(_job, jobs))
    v = {s: res[s]["won"] / res[s]["days"] for s in subsets}
    N = len(names)
    phi = {}
    for i in idx:
        tot = 0.0
        for s in subsets:
            if i in s:
                continue
            w = math.factorial(len(s)) * math.factorial(N - len(s) - 1) / math.factorial(N)
            tot += w * (v[s | {i}] - v[s])
        phi[names[i]] = tot
    # Shapley interaction index for each pair.
    inter = {}
    for i, j in itertools.combinations(idx, 2):
        tot = 0.0
        for s in subsets:
            if i in s or j in s:
                continue
            w = math.factorial(len(s)) * math.factorial(N - len(s) - 2) / math.factorial(N - 1)
            tot += w * (v[s | {i, j}] - v[s | {i}] - v[s | {j}] + v[s])
        inter[(names[i], names[j])] = tot
    return phi, inter, v, res
