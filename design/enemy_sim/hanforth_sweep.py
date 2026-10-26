"""Hanforth's options, broadly (2026-10-26).

Groundwork for the Healing Magic and Spirit Blessing pass: a wide range
of swaps on the designer's own 125 and 175 XP Hanforth, each against
the same base run in two parties, at modest reps (a feel for what's
worth what, not a price). Every swap stays inside its copy's Feature
Budget and spends the XP the build already spends; out-of-combat XP
(Minor Oracle, Profession, Dominate Mind) is fair game to move. Results
are in TABLE_PLAY_NOTES.md, "Hanforth's options".

    python3 hanforth_sweep.py 2 0       # Level 2, first party
    python3 hanforth_sweep.py 3 1 -n 150
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_builds as cb  # noqa: E402

HM, SB, LIFELINE = "T105", "T104", "T110"


def hm(feats, level=None):
    """Healing Magic's copy rebuilt."""
    r = {"id": HM, "copy": 1, "features": feats}
    if level:
        r["level"] = level
    return r


def sb(copy, feats, level=None):
    r = {"id": SB, "copy": copy, "features": feats}
    if level:
        r["level"] = level
    return r


def new_sb(feats, level=1):
    return {"id": SB, "name": "Spirit Blessing", "level": level, "features": feats}


def new(tid, name, level):
    return {"id": tid, "name": name, "level": f"Lv {level}"}


OOC_L2 = [{"id": "T191", "copy": 1}, {"id": "T027", "copy": 1}]   # Minor Oracle, Profession: 6 XP
OOC_L3 = OOC_L2 + [{"id": "T068", "copy": 1}]                     # and Dominate Mind: 18 XP
NO_ORACLE = {"Unmodeled": ""}

# (label, swap). A swap is build edits, or {"edits", "row"} when the row
# changes too (Minor Oracle gone from Unmodeled, an element in Choices).
L2 = [
    # Healing Magic, Level 2 (4 points; Vitality 2 as built)
    ("HM: Triage, Reach", {"replace": [hm({"Triage": 1, "Reach": 1})]}),
    ("HM: Vitality 1, Purify, Reach", {"replace": [hm({"Vitality": 1, "Purify": 1, "Reach": 1})]}),
    ("HM: Guardian Angel 2, Vitality 1", {"replace": [hm({"Guardian Angel": 2, "Vitality": 1})]}),
    ("HM: Vitality 1, Guardian Angel 1, Reach", {"replace": [hm({"Vitality": 1, "Guardian Angel": 1, "Reach": 1})]}),
    ("HM: Rejuvenate, Vitality 1, Reach", {"replace": [hm({"Rejuvenate": 1, "Vitality": 1, "Reach": 1})]}),
    # Spirit Blessing, Level 1 (3 points; Shielding 3 as built)
    ("SB: Step of Air 3", {"replace": [sb(1, {"Step of Air": 3})]}),
    ("SB: Step of Air 2, Quickened", {"replace": [sb(1, {"Step of Air": 2, "Quickened": 1})]}),
    ("SB: Shielding 2, Quickened", {"replace": [sb(1, {"Shielding": 2, "Quickened": 1})]}),
    ("SB: Shielding 2, Reach", {"replace": [sb(1, {"Shielding": 2, "Reach": 1})]}),
    ("SB: Shielding 1, Step of Air 1, Quickened", {"replace": [sb(1, {"Shielding": 1, "Step of Air": 1,
                                                                       "Quickened": 1})]}),
    ("SB: Retribution 2, Shielding 1", {"replace": [sb(1, {"Retribution": 2, "Shielding": 1})]}),
    ("SB: Touch of Chaos 3", {"replace": [sb(1, {"Touch of Chaos": 3})]}),
    ("SB: River's Might 3", {"replace": [sb(1, {"River's Might": 3})]}),
    ("SB: Turn Elements 3 (Shadow Ward)", {"edits": {"replace": [sb(1, {"Turn Elements": 3})]},
                                           "row": {"Choices": "Spirit Blessing: Shadow"}}),
    ("SB: Elemental Enhancement 3 (Fire)", {"edits": {"replace": [sb(1, {"Elemental Enhancement": 3})]},
                                            "row": {"Choices": "Spirit Blessing: Fire"}}),
    # Minor Oracle and Profession's 6 XP spent in combat
    ("XP: Lifeline", {"edits": {"remove": OOC_L2, "add": [new(LIFELINE, "Lifeline", 2)]}, "row": NO_ORACLE}),
    ("XP: two more SB Shielding 3", {"edits": {"remove": OOC_L2, "add": [new_sb({"Shielding": 3})] * 2},
                                     "row": NO_ORACLE}),
    ("XP: more SB, Shielding 3 and Step of Air 3",
     {"edits": {"remove": OOC_L2, "add": [new_sb({"Shielding": 3}), new_sb({"Step of Air": 3})]}, "row": NO_ORACLE}),
    ("XP: a Level 2 SB, Shielding 2, Quickened, Reach",
     {"edits": {"remove": OOC_L2, "add": [new_sb({"Shielding": 2, "Quickened": 1, "Reach": 1}, 2)]},
      "row": NO_ORACLE}),
    ("XP: HM to Level 3 (Vitality 4), one more SB Shielding 3",
     {"edits": {"remove": OOC_L2, "replace": [hm({"Vitality": 4}, 3)], "add": [new_sb({"Shielding": 3})]},
      "row": NO_ORACLE}),
    ("XP: HM to Level 3 (Triage, Vitality 2, Reach), one more SB Step of Air 3",
     {"edits": {"remove": OOC_L2, "replace": [hm({"Triage": 1, "Vitality": 2, "Reach": 1}, 3)],
                "add": [new_sb({"Step of Air": 3})]}, "row": NO_ORACLE}),
    ("XP: Toughened Body", {"edits": {"remove": OOC_L2, "add": [new("T014", "Toughened Body", 2)]},
                            "row": NO_ORACLE}),
    # Other trades
    ("Lifeline for Reckoning", {"remove": [{"id": "T111", "copy": 1}], "add": [new(LIFELINE, "Lifeline", 2)]}),
    ("Field Medic and an SB Shielding 3 for Ley-weaving",
     {"remove": [{"id": "T133", "copy": 1}], "add": [new("T189", "Field Medic", 1), new_sb({"Shielding": 3})]}),
]

L3 = [
    # Healing Magic, Level 3 (8 points, Advanced open; Vitality 4 as built)
    ("HM: Triage, Vitality 2, Reach", {"replace": [hm({"Triage": 1, "Vitality": 2, "Reach": 1})]}),
    ("HM: Healing Pact, Vitality 1, Reach", {"replace": [hm({"Healing Pact": 1, "Vitality": 1, "Reach": 1})]}),
    ("HM: Vitality 3, Guardian Angel 2", {"replace": [hm({"Vitality": 3, "Guardian Angel": 2})]}),
    ("HM: Vitality 2, Guardian Angel 2, Reach, Purify",
     {"replace": [hm({"Vitality": 2, "Guardian Angel": 2, "Reach": 1, "Purify": 1})]}),
    ("HM: Triage, Vitality 1, Guardian Angel 2, Reach",
     {"replace": [hm({"Triage": 1, "Vitality": 1, "Guardian Angel": 2, "Reach": 1})]}),
    # Spirit Blessing, two Level 1 copies (Shielding 3 both, as built)
    ("SB: second copy Step of Air 3", {"replace": [sb(2, {"Step of Air": 3})]}),
    ("SB: second copy Shielding 2, Quickened", {"replace": [sb(2, {"Shielding": 2, "Quickened": 1})]}),
    ("SB: both Shielding 2, Quickened", {"replace": [sb(1, {"Shielding": 2, "Quickened": 1}),
                                                     sb(2, {"Shielding": 2, "Quickened": 1})]}),
    ("SB: second copy Touch of Chaos 3", {"replace": [sb(2, {"Touch of Chaos": 3})]}),
    ("SB: second copy Retribution 2, Shielding 1", {"replace": [sb(2, {"Retribution": 2, "Shielding": 1})]}),
    ("SB: second copy Elemental Enhancement 3 (Fire)",
     {"edits": {"replace": [sb(2, {"Elemental Enhancement": 3})]}, "row": {"Choices": "Spirit Blessing: , Fire"}}),
    # Out-of-combat XP (Minor Oracle 3, Profession 3, Dominate Mind 12) spent in combat
    ("XP 6: Lifeline", {"edits": {"remove": OOC_L2, "add": [new(LIFELINE, "Lifeline", 2)]}, "row": NO_ORACLE}),
    ("XP 12: HM to Level 4 (Vitality 5, Reach), SB L3 Guided Hand 2, Quickened",
     {"remove": [{"id": "T068", "copy": 1}], "replace": [hm({"Vitality": 5, "Reach": 1}, 4)],
      "add": [new_sb({"Guided Hand": 2, "Quickened": 1}, 3)]}),
    ("XP 12: SB L3 Guided Hand 2, Quickened, SB L1 Step of Air 3",
     {"remove": [{"id": "T068", "copy": 1}],
      "add": [new_sb({"Guided Hand": 2, "Quickened": 1}, 3), new_sb({"Step of Air": 3})]}),
    ("XP 12: SB L3 Mass Blessing, Shielding 3, SB L1 Shielding 3",
     {"remove": [{"id": "T068", "copy": 1}],
      "add": [new_sb({"Mass Blessing": 1, "Shielding": 3}, 3), new_sb({"Shielding": 3})]}),
    ("XP 12: SB L3 Alacrity, Shielding 3, SB L1 Shielding 3",
     {"remove": [{"id": "T068", "copy": 1}],
      "add": [new_sb({"Alacrity": 1, "Shielding": 3}, 3), new_sb({"Shielding": 3})]}),
    ("XP 12: HM to Level 4 (Healing Pact, Vitality 3), SB L3 Mass Blessing, Shielding 3",
     {"remove": [{"id": "T068", "copy": 1}], "replace": [hm({"Healing Pact": 1, "Vitality": 3}, 4)],
      "add": [new_sb({"Mass Blessing": 1, "Shielding": 3}, 3)]}),
    ("XP 12: Lifeline, Toughened Body",
     {"remove": [{"id": "T068", "copy": 1}], "add": [new(LIFELINE, "Lifeline", 2), new("T014", "Toughened Body", 2)]}),
    ("XP 18: Lifeline, SB L3 Mass Blessing, Shielding 3, SB L1 Step of Air 3",
     {"edits": {"remove": OOC_L3, "add": [new(LIFELINE, "Lifeline", 2), new_sb({"Mass Blessing": 1, "Shielding": 3}, 3),
                                          new_sb({"Step of Air": 3})]}, "row": NO_ORACLE}),
    # Styles in place of Ley-weaving (6 XP)
    ("Field Medic for Ley-weaving (3 XP spare unspent)",
     {"remove": [{"id": "T133", "copy": 1}], "add": [new("T189", "Field Medic", 1)]}),
    ("Lifeward for Ley-weaving and Minor Oracle",
     {"edits": {"remove": [{"id": "T133", "copy": 1}, {"id": "T191", "copy": 1}],
                "add": [new("T190", "Lifeward", 3)]}, "row": NO_ORACLE}),
]

# (names, enemy Health multiplier) per Level: Party D, and a second party
# with a different front line.
PARTIES = {
    2: [(["Browndog (L2)", "Hanforth (L2)", "Felix (L2)", "Beornhard (L2)"], 1.75),
        (["Hilde (L2)", "Browndog (L2)", "Hanforth (L2)", "Beornhard (L2)"], 2.5)],
    3: [(["Browndog (L3)", "Hanforth (L3)", "Hilde (L3)", "Beornhard (L3)"], 2.25),
        (["Hilde (L3)", "Hanforth (L3)", "Jackal (L3)", "Beornhard (L3)"], 2.0)],
}

if __name__ == "__main__":
    cb.sweep_main(__doc__, {2: ("Hanforth (L2)", L2), 3: ("Hanforth (L3)", L3)}, PARTIES)
