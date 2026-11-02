"""Normalized builds at the edges of each Level's XP band (2026-11-02).

Per the designer: Level N enemies are for PCs within 25 XP of that
Level's schedule (Level 2: 100-150 total XP, Level 3: 150-200), so the
bottom of a band should feel some friction and the top should be
comfortable. The combat share follows combat_xp's two points (105 of
125, 145 of 175: 20 and 30 XP outside fights), straight-line in total
XP, so the band edges are 85/125 combat at Level 2 and 125/165 at
Level 3. Each archetype's own export at that Level is brought to the
budget by combat_xp.normalize, the same rule as builds/normalized/.

    python3 experiments/enemies/band_builds.py          # writes the four sets
    python3 experiments/enemies/band_builds.py --check  # the stored mid-band set still comes out the same
"""
import argparse
import json
import os
import sys

import _paths  # noqa: E402,F401
import party  # noqa: E402
import combat_xp  # noqa: E402
import build_optimizer as bo  # noqa: E402

EDGES = {2: (85, 125), 3: (125, 165)}


def combat_budget(total_xp):
    """Combat XP for a total: 20 outside fights at 125, 30 at 175."""
    return total_xp - (20 + (total_xp - 125) / 5)


def build_at(arch, level, budget):
    name = bo.row_name(arch, level)
    um = {x.strip() for x in (party._rows()[name].get("Unmodeled") or "").split(",") if x.strip()}
    b = party.read_build(party._rows()[name]["Build"])
    saved = combat_xp.COMBAT_BUDGET[level]
    combat_xp.COMBAT_BUDGET[level] = budget
    try:
        return combat_xp.normalize(b, level, party.make_pc(name)["attack_skill"], um)[0]
    finally:
        combat_xp.COMBAT_BUDGET[level] = saved


def path(arch, level, budget):
    return os.path.join(_paths.ROOT, "builds", "normalized", f"{arch.lower()}_l{level}_c{budget}.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        bad = 0
        for level, budget in combat_xp.COMBAT_BUDGET.items():
            for arch in bo.ARCHES:
                new = build_at(arch, level, budget)
                old = party.read_build(path(arch, level, budget))
                same = all(new[k] == old.get(k) for k in ("statPoints", "skillPoints", "techniques"))
                bad += not same
                print(f"{arch} L{level}: {'same' if same else 'DIFFERENT'}")
        sys.exit(bad)
    for level, budgets in EDGES.items():
        for budget in budgets:
            for arch in bo.ARCHES:
                b = build_at(arch, level, budget)
                c = combat_xp.split(b)[0]
                with open(path(arch, level, budget), "w") as f:
                    json.dump(b, f, indent=1)
                print(f"{arch} L{level} c{budget}: {c} combat XP")


if __name__ == "__main__":
    main()
