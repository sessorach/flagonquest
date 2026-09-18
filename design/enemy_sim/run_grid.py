"""
Runs the full Party Tier x Enemy Level grid through combat_sim and
prints win rate / average rounds / party HP% remaining on a win. Re-run
this after editing tunables.py or sample_enemies.py to see how a
retuning pass moved the numbers.

Usage: python3 run_grid.py [trials]
"""
import sys
from combat_sim import simulate

trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
grid = {}
for tier in range(1, 6):
    for lvl in range(1, 6):
        grid[(tier, lvl)] = simulate(tier, lvl, trials=trials)

print(f"Win rate (%) — rows=Party Tier, cols=Enemy Level  ({trials} trials/cell)")
print("Tier | " + " | ".join(f"  L{lvl}" for lvl in range(1, 6)))
for tier in range(1, 6):
    row = [f"{grid[(tier, lvl)][0]:5.1f}" for lvl in range(1, 6)]
    print(f"{tier:4d} | " + " | ".join(row))

print()
print("Avg rounds to resolve")
print("Tier | " + " | ".join(f"  L{lvl}" for lvl in range(1, 6)))
for tier in range(1, 6):
    row = [f"{grid[(tier, lvl)][1]:5.1f}" for lvl in range(1, 6)]
    print(f"{tier:4d} | " + " | ".join(row))

print()
print("Party HP% remaining on win")
print("Tier | " + " | ".join(f"  L{lvl}" for lvl in range(1, 6)))
for tier in range(1, 6):
    row = [f"{grid[(tier, lvl)][2]:5.1f}" for lvl in range(1, 6)]
    print(f"{tier:4d} | " + " | ".join(row))
