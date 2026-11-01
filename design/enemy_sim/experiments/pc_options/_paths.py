"""Import path for a script below the simulator folder (2026-11-01).

The simulator's core (combat_sim, party, tactics...) lives in
design/enemy_sim/; the runners in tools/ and the one-off studies in
experiments/<topic>/ import it, and sometimes each other. A script's own
folder is on the path when it runs, so `import _paths` finds this file,
which puts the core, tools/ and every experiments/ folder on the path
too. The same file sits in each of those folders. ROOT is the simulator
folder, for scripts that read builds/, hall_of_fame/ and so on.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(ROOT, "combat_sim.py")):
    ROOT = os.path.dirname(ROOT)
_dirs = [ROOT, os.path.join(ROOT, "tools")]
for _base, _subs, _ in os.walk(os.path.join(ROOT, "experiments")):
    _subs[:] = sorted(d for d in _subs if d != "__pycache__")
    _dirs.append(_base)
# Right after the script's own folder, ahead of installed packages (a pip
# "coverage" mustn't shadow tools/coverage.py).
for _i, _d in enumerate(_dirs, 1):
    if _d not in sys.path:
        sys.path.insert(_i, _d)
