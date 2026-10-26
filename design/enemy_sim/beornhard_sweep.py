"""Beornhard's War Magic options, broadly (2026-10-26).

The same broad look as hanforth_sweep.py, for the designer's own 125
and 175 XP Beornhard: other Features on his War Magic copies, the
Defense they're learned against, and his other Techniques' XP traded
for more War Magic (or Force Missiles). Every swap fits its copy's
Feature Budget (War Magic: 1, 3, 4 and 6 points at Levels 1-4, Advanced
from Level 3) and spends the XP the build already spends. Results are
in TABLE_PLAY_NOTES.md, "Beornhard's War Magic options".

    python3 beornhard_sweep.py 2 0       # Level 2, first party
    python3 beornhard_sweep.py 3 1 -n 150
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_builds as cb  # noqa: E402

WM = "T120"


def wm(copy, feats, level=None):
    r = {"id": WM, "copy": copy, "features": feats}
    if level:
        r["level"] = level
    return r


def both(feats):
    """The two Level 2 copies (copies 1 and 2 at both Levels) rebuilt."""
    return [wm(1, feats), wm(2, feats)]


def new_wm(feats, level):
    return {"id": WM, "name": "War Magic", "level": level, "features": feats}


def drop(tid):
    return {"id": tid, "copy": 1}


def vital(n):
    """Every War Magic copy learned against Vital, `n` copies."""
    return {"Choices": "War Magic: " + ", ".join(["Vital"] * n)}


L, D = "Lance", "Destructive"
FORCE = {"id": "T121", "name": "Force Missiles", "level": "Lv 1"}

# Level 2: copies 1-2 are Level 2 Lance + Destructive 2 (3 points), copy 3
# the Level 1 Lance that's his weapon. All against Dodge.
L2 = [
    # Both Level 2 copies rebuilt (3 points each)
    ("WM: Lance, Destructive 1, Frigid 1", {"replace": both({L: 1, D: 1, "Frigid": 1})}),
    ("WM: Lance, Frigid 2", {"replace": both({L: 1, "Frigid": 2})}),
    ("WM: Lance, Destructive 1, Kinetic 1", {"replace": both({L: 1, D: 1, "Kinetic": 1})}),
    ("WM: Lance, Corrupting 2, all vs Vital", {"edits": {"replace": both({L: 1, "Corrupting": 2})}, "row": vital(3)}),
    ("WM: Lance, Destructive 1, Corrupting 1, all vs Vital",
     {"edits": {"replace": both({L: 1, D: 1, "Corrupting": 1})}, "row": vital(3)}),
    ("WM: Lance, Necrotic 2", {"replace": both({L: 1, "Necrotic": 2})}),
    ("WM: Lance, Barraging 2", {"replace": both({L: 1, "Barraging": 2})}),
    ("WM: Lance, Destructive 1, Barraging 1", {"replace": both({L: 1, D: 1, "Barraging": 1})}),
    ("WM: Lance, Sanguine, Destructive 1", {"replace": both({L: 1, "Sanguine": 1, D: 1})}),
    ("WM: Lance, Wild Magic 2", {"replace": both({L: 1, "Wild Magic": 2})}),
    ("WM: Lance, Destructive 1, Wild Magic 1", {"replace": both({L: 1, D: 1, "Wild Magic": 1})}),
    ("WM: Lance, Abjuring 2", {"replace": both({L: 1, "Abjuring": 2})}),
    ("WM: Destructive 3, no Lance", {"replace": both({D: 3})}),
    ("WM: one copy Frigid 2, one Destructive 2", {"replace": [wm(1, {L: 1, "Frigid": 2})]}),
    ("WM: as built, all vs Vital", {"edits": {}, "row": vital(3)}),
    ("WM: a Tormenting Curse hex, Lance, Frigid 5", {"replace": [wm(2, {"Tormenting Curse": 1, L: 1, "Frigid": 5})]}),
    # Other Techniques' XP into War Magic
    ("XP: Shadow Jaunt for a Level 1 Lance", {"remove": [drop("T097")], "add": [new_wm({L: 1}, 1)]}),
    ("XP: Overchanneling for a Level 2 Lance, Destructive 2",
     {"remove": [drop("T140")], "add": [new_wm({L: 1, D: 2}, 2)]}),
    ("XP: Warmage's Reserves for a Level 2 Lance, Destructive 2",
     {"remove": [drop("T124")], "add": [new_wm({L: 1, D: 2}, 2)]}),
    ("XP: Overchanneling for Force Missiles and a Level 1 Lance",
     {"remove": [drop("T140")], "add": [FORCE, new_wm({L: 1}, 1)]}),
    ("XP: Shadow Jaunt for Force Missiles", {"remove": [drop("T097")], "add": [FORCE]}),
]

# Level 3: copies 1-2 as at Level 2; copy 3 is Level 4 (6 points,
# Advanced): Destructive 2, Draw Power, Furrow.
L3 = [
    # The Level 4 copy rebuilt
    ("WM4: Lance, Destructive 3, Piercing Elements, Draw Power",
     {"replace": [wm(3, {L: 1, D: 3, "Piercing Elements": 1, "Draw Power": 1})]}),
    ("WM4: Lance, Destructive 5", {"replace": [wm(3, {L: 1, D: 5})]}),
    ("WM4: Lance, Destructive 3, Wild Magic 2", {"replace": [wm(3, {L: 1, D: 3, "Wild Magic": 2})]}),
    ("WM4: Lance, Piercing Elements, Destructive 2, Barraging 2",
     {"replace": [wm(3, {L: 1, "Piercing Elements": 1, D: 2, "Barraging": 2})]}),
    ("WM4: Funnel, Destructive 3", {"replace": [wm(3, {"Funnel (Shape)": 1, D: 3})]}),
    ("WM4: Nova, Destructive 3", {"replace": [wm(3, {"Nova (Shape)": 1, D: 3})]}),
    ("WM4: Furrow, Frigid 2, Destructive 1", {"replace": [wm(3, {"Furrow (Shape)": 1, "Frigid": 2, D: 1})]}),
    ("WM4: Furrow, Necrotic 1, Destructive 2", {"replace": [wm(3, {"Furrow (Shape)": 1, "Necrotic": 1, D: 2})]}),
    ("WM4: Furrow, Destructive 3", {"replace": [wm(3, {"Furrow (Shape)": 1, D: 3})]}),
    # The two Level 2 copies rebuilt
    ("WM2: both Lance, Frigid 2", {"replace": both({L: 1, "Frigid": 2})}),
    ("WM2: both Lance, Destructive 1, Wild Magic 1", {"replace": both({L: 1, D: 1, "Wild Magic": 1})}),
    ("WM2: both Lance, Destructive 1, Barraging 1", {"replace": both({L: 1, D: 1, "Barraging": 1})}),
    ("WM: as built, all vs Vital", {"edits": {}, "row": vital(3)}),
    # XP moved
    ("XP: the Level 4 copy at Level 3 (Lance, Destructive 2, Piercing) and a Level 1 Lance",
     {"replace": [wm(3, {L: 1, D: 2, "Piercing Elements": 1}, 3)], "add": [new_wm({L: 1}, 1)]}),
    ("XP: Wall of Shadows for a Level 2 Lance, Destructive 2",
     {"remove": [drop("T123")], "add": [new_wm({L: 1, D: 2}, 2)]}),
    ("XP: Gainsay for a Level 1 Lance", {"remove": [drop("T122")], "add": [new_wm({L: 1}, 1)]}),
    ("XP: Wall of Shadows and Gainsay for a Level 3 Lance, Destructive 2, Piercing",
     {"remove": [drop("T123"), drop("T122")], "add": [new_wm({L: 1, D: 2, "Piercing Elements": 1}, 3)]}),
    ("XP: Overchanneling for a Level 2 Lance, Destructive 2",
     {"remove": [drop("T140")], "add": [new_wm({L: 1, D: 2}, 2)]}),
    ("XP: Shadow Jaunt for Force Missiles", {"remove": [drop("T097")], "add": [FORCE]}),
]

PARTIES = {
    2: [(["Hilde (L2)", "Browndog (L2)", "Jackal (L2)", "Beornhard (L2)"], 2.75),
        (["Browndog (L2)", "Hanforth (L2)", "Felix (L2)", "Beornhard (L2)"], 1.75)],
    3: [(["Hilde (L3)", "Browndog (L3)", "Jackal (L3)", "Beornhard (L3)"], 2.25),
        (["Browndog (L3)", "Hanforth (L3)", "Hilde (L3)", "Beornhard (L3)"], 2.25)],
}

if __name__ == "__main__":
    cb.sweep_main(__doc__, {2: ("Beornhard (L2)", L2), 3: ("Beornhard (L3)", L3)}, PARTIES)
