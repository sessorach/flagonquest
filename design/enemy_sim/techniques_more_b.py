"""The rest of the Technique catalog, part B (2026-10-27): T100-T205.

Each Technique here is modeled (registered the same way as in
techniques.py), listed in techniques.OUT_OF_COMBAT, or listed in
techniques.DEFERRED with what it would need. combat_sim is `tq.cs` at
fight time (techniques.py's `cs`), not at import.
"""
import techniques as tq
from techniques import technique, hooks, setup_for, OUT_OF_COMBAT, DEFERRED, BuildError  # noqa: F401
