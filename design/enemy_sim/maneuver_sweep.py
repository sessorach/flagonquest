"""Hilde's and Browndog's Battle Maneuver options, broadly (2026-10-27).

The same broad look as hanforth_sweep.py and beornhard_sweep.py, for the
two front-liners' Battle Maneuvers at 125 and 175 XP: each copy swapped
through the Features, copies merged into a higher-Level one, and
out-of-combat XP (Hilde's Bound Across Mountains, Browndog's Follower)
spent on more Maneuvers. Every swap fits its copy's Feature Budget
(Battle Maneuver: 3, 6, 9 and 12 points at Levels 1-4, Advanced from
Level 3) and spends the XP the build already spends. The sim uses the
copies in sheet order, the first as the opening move. Results are in
TABLE_PLAY_NOTES.md, "Battle Maneuver options".

    python3 maneuver_sweep.py hilde2 0       # Hilde (L2), first party
    python3 maneuver_sweep.py browndog3 1 -n 150
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_builds as cb  # noqa: E402

BM = "T072"
# Every 1-point Basic Feature, three copies' worth on a Level 1 copy.
BASIC = ["Lunging", "Wind Slash", "Distracting", "Battering", "Wing Clip", "Harrying", "Hamstring",
         "Backfoot", "Lodestone", "Half Guard", "Blade of Four Fates", "Fleet Step"]


def bm(copy, feats, level=None):
    r = {"id": BM, "copy": copy, "features": feats}
    if level:
        r["level"] = level
    return r


def new_bm(feats, level=1):
    return {"id": BM, "name": "Battle Maneuver", "level": level, "features": feats}


def element(n_copies, copy, kind="Fire"):
    """The Choices cell for an element on one Maneuver copy."""
    picks = [""] * n_copies
    picks[copy - 1] = kind
    return {"Choices": "Battle Maneuver: " + ", ".join(picks)}


def level1_swaps(copy, n_copies, skip=()):
    """A Level 1 copy (3 points) as each Basic Feature, and the 2- and
    3-point picks."""
    out = [(f"copy {copy}: {f} 3", {"replace": [bm(copy, {f: 3})]}) for f in BASIC if f not in skip]
    out += [
        (f"copy {copy}: Turn Elements 3 (Fire Ward)",
         {"edits": {"replace": [bm(copy, {"Turn Elements": 3})]}, "row": element(n_copies, copy)}),
        (f"copy {copy}: Calculated", {"replace": [bm(copy, {"Calculated": 1})]}),
        (f"copy {copy}: Viper's Sting", {"replace": [bm(copy, {"Viper's Sting": 1})]}),
        (f"copy {copy}: Victorious, Half Guard 1", {"replace": [bm(copy, {"Victorious": 1, "Half Guard": 1})]}),
        (f"copy {copy}: Elemental (Fire), Half Guard 1",
         {"edits": {"replace": [bm(copy, {"Elemental": 1, "Half Guard": 1})]}, "row": element(n_copies, copy)}),
    ]
    return out


def few(copy, names):
    """A short list of Level 1 swaps for a copy that isn't the main one."""
    out = []
    for f in names:
        feats = {f: 1} if f in ("Calculated", "Viper's Sting") else {f: 3}
        out.append((f"copy {copy}: {f}" + ("" if f in ("Calculated", "Viper's Sting") else " 3"),
                    {"replace": [bm(copy, feats)]}))
    return out


def merged(copies, feats, level, label):
    """Several Level 1 copies' XP as one higher-Level copy (fewer uses)."""
    return (label, {"remove": [{"id": BM, "copy": c} for c in sorted(copies)][1:],
                    "replace": [bm(min(copies), feats, level)]})


# Hilde (L2): copy 1 Lunging 3 (her opener), copy 2 Half Guard 3.
HILDE2 = level1_swaps(2, 2, skip=("Half Guard",)) + few(1, ["Calculated", "Viper's Sting", "Wing Clip", "Harrying"]) + [
    merged((1, 2), {"Lunging": 3, "Half Guard": 3}, 2, "both as one Level 2 copy: Lunging 3, Half Guard 3"),
    merged((1, 2), {"Lunging": 3, "Calculated": 1}, 2, "both as one Level 2 copy: Lunging 3, Calculated"),
    merged((1, 2), {"Calculated": 1, "Wing Clip": 3}, 2, "both as one Level 2 copy: Calculated, Wing Clip 3"),
]

# Browndog (L2): copies Lunging 3, Half Guard 3, Lunging 3; Follower (3
# XP) is out of combat.
FOLLOWER = {"id": "T059", "copy": 1}
BROWNDOG2 = level1_swaps(2, 3, skip=("Half Guard",)) + few(3, ["Calculated", "Viper's Sting", "Harrying"]) + [
    merged((2, 3), {"Half Guard": 3, "Lunging": 3}, 2, "copies 2-3 as one Level 2 copy: Half Guard 3, Lunging 3"),
    merged((2, 3), {"Calculated": 1, "Half Guard": 3}, 2, "copies 2-3 as one Level 2 copy: Calculated, Half Guard 3"),
    ("Follower's XP: one more copy, Half Guard 3", {"remove": [FOLLOWER], "add": [new_bm({"Half Guard": 3})]}),
    ("Follower's XP: one more copy, Calculated", {"remove": [FOLLOWER], "add": [new_bm({"Calculated": 1})]}),
]

# Hilde (L3): copy 1 Lunging 3, copy 2 Level 3 (Whirlwind, Victorious,
# Ascended Blade: 9 points), copy 3 Half Guard 3, copy 4 Lunging 3;
# Bound Across Mountains (6 XP) is out of combat.
BOUND = {"id": "T007", "copy": 1}
HILDE3 = [(f"Level 3 copy: {label}", {"replace": [bm(2, feats)]}) for label, feats in (
    ("Flurry, Calculated", {"Flurry": 1, "Calculated": 1}),
    ("Flurry, Wing Clip 3", {"Flurry": 1, "Wing Clip": 3}),
    ("Flurry, Lunging 3", {"Flurry": 1, "Lunging": 3}),
    ("Whirlwind, Calculated, Half Guard 1", {"Whirlwind": 1, "Calculated": 1, "Half Guard": 1}),
    ("Whirlwind, Battering 4", {"Whirlwind": 1, "Battering": 4}),
    ("Whirlwind, Harrying 4", {"Whirlwind": 1, "Harrying": 4}),
    ("Whirlwind, Wing Clip 4", {"Whirlwind": 1, "Wing Clip": 4}),
    ("Whirlwind, Viper's Sting, Half Guard 1", {"Whirlwind": 1, "Viper's Sting": 1, "Half Guard": 1}),
    ("Calculated, Wing Clip 3, Harrying 3", {"Calculated": 1, "Wing Clip": 3, "Harrying": 3}),
    ("Calculated, Viper's Sting, Lunging 3", {"Calculated": 1, "Viper's Sting": 1, "Lunging": 3}),
)] + [
    ("Level 3 copy: Whirlwind, Victorious, Elemental (Fire)",
     {"edits": {"replace": [bm(2, {"Whirlwind": 1, "Victorious": 1, "Elemental": 1})]}, "row": element(4, 2)}),
] + few(3, ["Calculated", "Wing Clip", "Harrying", "Battering"]) + [
    ("Bound Across Mountains' XP: a Level 2 copy, Calculated, Half Guard 3",
     {"remove": [BOUND], "add": [new_bm({"Calculated": 1, "Half Guard": 3}, 2)]}),
    ("Bound Across Mountains' XP: two more copies, Half Guard 3 and Calculated",
     {"remove": [BOUND], "add": [new_bm({"Half Guard": 3}), new_bm({"Calculated": 1})]}),
]

# Browndog (L3): copies Lunging 3, Half Guard 3, Lunging 3, as at Level 2.
BROWNDOG3 = [
    merged((1, 2, 3), {"Whirlwind": 1, "Calculated": 1, "Lunging": 1}, 3,
           "all three as one Level 3 copy: Whirlwind, Calculated, Lunging 1"),
    merged((1, 2, 3), {"Flurry": 1, "Calculated": 1}, 3, "all three as one Level 3 copy: Flurry, Calculated"),
    merged((1, 2, 3), {"Flurry": 1, "Lunging": 3}, 3, "all three as one Level 3 copy: Flurry, Lunging 3"),
    merged((1, 2, 3), {"Calculated": 3}, 3, "all three as one Level 3 copy: Calculated 3"),
    ("copies 2-3 and Follower's XP as one Level 3 copy: Flurry, Half Guard 3",
     {"remove": [FOLLOWER, {"id": BM, "copy": 3}], "replace": [bm(2, {"Flurry": 1, "Half Guard": 3}, 3)]}),
    ("copies 2-3 and Follower's XP as one Level 3 copy: Whirlwind, Half Guard 3, Lunging 1",
     {"remove": [FOLLOWER, {"id": BM, "copy": 3}],
      "replace": [bm(2, {"Whirlwind": 1, "Half Guard": 3, "Lunging": 1}, 3)]}),
] + few(2, ["Calculated", "Wing Clip", "Harrying", "Battering", "Backfoot", "Fleet Step"]) + [
    ("Follower's XP: one more copy, Half Guard 3", {"remove": [FOLLOWER], "add": [new_bm({"Half Guard": 3})]}),
    ("Follower's XP: one more copy, Calculated", {"remove": [FOLLOWER], "add": [new_bm({"Calculated": 1})]}),
]

PARTY_B = {2: ["Hilde (L2)", "Browndog (L2)", "Jackal (L2)", "Beornhard (L2)"],
           3: ["Hilde (L3)", "Browndog (L3)", "Jackal (L3)", "Beornhard (L3)"]}
PARTY_A = {2: ["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"],
           3: ["Hilde (L3)", "Browndog (L3)", "Carrick (L3)", "Sable (L2)"]}
MULT = {2: (2.75, 2.25), 3: (2.25, 2.0)}
PARTIES = {f"{who}{lvl}": [(PARTY_B[lvl], MULT[lvl][0]), (PARTY_A[lvl], MULT[lvl][1])]
           for who in ("hilde", "browndog") for lvl in (2, 3)}
VARIANTS = {"hilde2": ("Hilde (L2)", HILDE2), "browndog2": ("Browndog (L2)", BROWNDOG2),
            "hilde3": ("Hilde (L3)", HILDE3), "browndog3": ("Browndog (L3)", BROWNDOG3)}

if __name__ == "__main__":
    cb.sweep_main(__doc__, VARIANTS, PARTIES)
