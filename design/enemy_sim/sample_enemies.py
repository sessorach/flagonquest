"""
Loads enemy stat blocks from sample_enemies.csv - a growing collection of
"sample dudes" built with enemy_builder.py, rather than one Python
function per enemy. Two kinds of rows share the file:

- **Roster** (`Roster` column TRUE) - exactly one per Level 1-5, tuned
  (via the per-Level search in combat_sim.py's tuning runs) to land
  close to a genuine ~50% on-level win rate against a same-Tier party.
  `make_enemy(level)` pulls these - see design/ENEMY_ENCOUNTER_DESIGN.md's
  "Analysis" section for the validation grid they produced. All five use
  Light Armor specifically - see that CSV's own Notes column and
  tunables.py's ARMOR comment for why (Light is where the Armor table is
  anchored to the real player-facing armor_categories.csv; testing found
  Unarmored too easy and Medium/Heavy a real wall even with Gambling, so
  they read as a deliberately tougher "elite" pick, not on-level).
- **Reference builds** (`Roster` FALSE) - one-off stat blocks built for a
  specific question (an item-balancing check, a "what does a generic
  fighter look like" ask) that aren't part of the validated roster and
  don't need to be unique per Level. `get_enemy(name)` pulls these by
  name. Includes a Minion archetype at every Level (0.5 Slots, same
  Neutral shape as the Generic Fighter archetype) specifically so
  `build_encounter`/`total_slots` below have a real sub-1-slot enemy to
  compose with - every other row in this file is 1 Slot.

`build_encounter(names)` assembles a custom encounter from any mix of
named rows (Roster or reference, any Level/Slots combination) instead
of `make_enemy(level)`'s single Roster pull - pass its result as
`combat_sim.run_fight`'s own `enemies=` param. `total_slots(enemies)`
sums an encounter's own Slots, for checking a mix against "one slot per
PC" - the default encounter budget (the designer's own framing; not
yet written into ENEMY_ENCOUNTER_DESIGN.md itself).

These are simulator fixtures, not a finished in-game roster - expect an
"Example Enemies" design doc to supersede the Roster rows once the
PC/enemy baselines in tunables.py are locked down further.

**`DamageBonus`/`AccuracyBonus`/`DefenseBonus`** (blank = 0) map straight
to enemy_builder.build_enemy's own `ability_dmg_bonus`/`ability_acc_
bonus`/`ability_def_bonus` params - flat retune knobs for this row's own
attack damage, to-hit Accuracy, and all four defenses (Parry/Dodge/
Bodily/Mental together) respectively, none of which also inflate this
row's own Resist (unlike bumping tunables.DMG_RESIST or ACCURACY
directly, which feed multiple derived stats off the same Level-keyed
number and turned out to be much sharper, less controllable levers
during the Level 1 "mixed Fighting Style" retune - see the 5 Mixed-
Style archetypes' own Notes). Of the three, `DefenseBonus` turned out to
be the cleanest lever for moving win rate and "HP% remaining on a win"
*together* rather than pulling them apart - it changes how fast the
party can kill the enemy, not how hard the enemy hits back, so unlike
Damage/Accuracy it doesn't force the same tradeoff between "wins more"
and "wins by more." Kept distinct from the real `Abilities` catalog
(Powerful Weapon, etc.) since those carry their own in-fiction identity
and tradeoffs (Powerful Weapon costs Accuracy/Parry); these are plain
numeric retune knobs, not a named ability a GM would narrate.

**`ParryTier`/`DodgeTier`/`BodilyTier`/`MentalTier`/`VigilantTier`/
`AttackTier`/`HealthBonus`** are a second, alternative construction
method - enemy_builder_pcstyle.py's build_enemy_pcstyle, wired into
`_build_from_row` whenever `AttackTier` isn't blank (a row with a blank
`AttackTier` still builds the old way, off `Role`/`PrimaryDef`/
`SecondaryDef`/`SecondaryDef2`/`DamageBonus`/`AccuracyBonus`/
`DefenseBonus`, which stay blank/unused on a pcstyle row and vice versa
- the two methods are mutually exclusive per row, not layered). Builds
an enemy the way a PC actually gets built - Defense = 8 + Skill Total,
Damage = a weapon-style base + Stat, Resist = Essence alone - instead
of enemy_builder.py's synthetic Level curve; see build_enemy_pcstyle's
own module docstring for the full formula and why. Each Tier column is
"poor"/"secondary"/"primary" (blank = poor, same "never invested here"
reading as a blank Ability cell) - five independent Defenses instead of
PrimaryDef/SecondaryDef's bundled "Parry/Dodge as one category" (plus
Vigilant, which PrimaryDef/SecondaryDef's own three-category shape
doesn't cover at all - see ENEMY_ENCOUNTER_DESIGN.md's Defense tiering
section). `SecondaryDef2` is the classic-method equivalent - a second
Secondary pick, needed once Vigilant made four categories out of three;
existing rows predating this change leave it blank, which reads as an
extra, currently-unintended weak category until reviewed. `HealthBonus`
(blank = 0) is a small uniform nudge on top of the real Baseline-party
Health for that Level, not part of the formula itself. The 4 default
Level 1 archetypes (Hedge Knight/Marsh Archer/Skulking Footpad/Fen
Warden) use this method now - see their own Notes for the numbers this
landed on, and why (short version: once Harried - glossary.md, -1
Dodge/Parry per stack, previously unmodeled entirely - got wired into
combat_sim.py, the plain ungrounded Skill Total numbers already landed
close to the target win rate/Health-cost shape on their own).
"""
import csv
import os
from enemy_builder import build_enemy
from enemy_builder_pcstyle import build_enemy_pcstyle

_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_enemies.csv")


def _load_rows():
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _build_from_row(row):
    # AttackTier non-blank picks enemy_builder_pcstyle's real-PC-formula
    # construction (Defense = 8 + Skill Total, Damage = base + Stat,
    # Resist = Essence alone) over enemy_builder.build_enemy's synthetic
    # Level curve - see enemy_builder_pcstyle.py's own module docstring
    # for why. ParryTier/DodgeTier/BodilyTier/MentalTier/VigilantTier
    # (blank = "poor", same "a Skill you never invested in" reading as a
    # blank Ability cell) replace PrimaryDef/SecondaryDef's bundled
    # "Parry/Dodge as one category" for these rows - five independent
    # Defenses, not four.
    if (row.get("AttackTier") or "").strip():
        e = build_enemy_pcstyle(
            row["Name"],
            int(row["Level"]),
            float(row["Slots"]),
            row["Action"],
            row["Armor"],
            defense_tiers={
                "parry": (row.get("ParryTier") or "poor").strip().lower(),
                "dodge": (row.get("DodgeTier") or "poor").strip().lower(),
                "bodily": (row.get("BodilyTier") or "poor").strip().lower(),
                "mental": (row.get("MentalTier") or "poor").strip().lower(),
                "vigilant": (row.get("VigilantTier") or "poor").strip().lower(),
            },
            attack_tier=row["AttackTier"].strip().lower(),
            health_bonus=int(row["HealthBonus"]) if row.get("HealthBonus", "").strip() else 0,
            abilities=[a.strip() for a in row["Abilities"].split(";") if a.strip()],
        )
    else:
        # SecondaryDef/SecondaryDef2: up to two Secondary picks now that
        # Vigilant makes four categories (see ENEMY_ENCOUNTER_DESIGN.md's
        # Defense tiering section) - blank entries filtered out, so a row
        # with only SecondaryDef set (every pre-Vigilant row) still works
        # exactly as before, just with Vigilant itself reading as a
        # second, currently-unintended weak category until a real design
        # pass assigns it a proper pick.
        secondary_defs = tuple(v for v in (row["SecondaryDef"], row.get("SecondaryDef2", "")) if v)
        e = build_enemy(
            row["Name"],
            int(row["Level"]),
            float(row["Slots"]),
            row["Role"],
            row["PrimaryDef"] or None,
            secondary_defs,
            row["Action"],
            row["Armor"],
            ability_dmg_bonus=int(row["DamageBonus"]) if row.get("DamageBonus", "").strip() else 0,
            ability_acc_bonus=int(row["AccuracyBonus"]) if row.get("AccuracyBonus", "").strip() else 0,
            ability_def_bonus=int(row["DefenseBonus"]) if row.get("DefenseBonus", "").strip() else 0,
            abilities=[a.strip() for a in row["Abilities"].split(";") if a.strip()],
        )
    e["battle_tactic"] = row["BattleTactic"]
    e["fighting_style"] = row["FightingStyle"]
    return e


def make_enemy(level):
    for row in _load_rows():
        if row["Roster"].strip().upper() == "TRUE" and int(row["Level"]) == level:
            return _build_from_row(row)
    raise ValueError(f"no Roster row for Level {level}")


def get_enemy(name):
    for row in _load_rows():
        if row["Name"] == name:
            return _build_from_row(row)
    raise KeyError(f"no sample_enemies.csv row named {name!r}")


def all_enemies():
    return [_build_from_row(row) for row in _load_rows()]


# The new Level 1 baseline (replacing 4x Marsh Viper Scout - now a
# reference build only, Roster=FALSE, still available via get_enemy):
# one of each of 4 of the 5 Mixed-Style archetypes (Hedge Knight, Marsh
# Archer, Skulking Footpad, Fen Warden), retuned against a real drafted
# party - see those 4 rows' own Notes for the calibration numbers. Bog
# Caster (the deliberate double-attacker) is left out of the default
# mix on purpose, kept as a separate flavor pick for a GM who wants that
# harsher read. Only Level 1 has an entry so far ("we'll check out the
# rest at a later point," per the designer) - every other Level still
# falls back to make_level_encounter's own old behavior below.
MIXED_ROSTER = {
    1: ["Hedge Knight", "Marsh Archer", "Skulking Footpad", "Fen Warden"],
}


def make_level_encounter(level, n_enemies=4):
    """What combat_sim.run_fight builds by default when no explicit
    `enemies=` is given - MIXED_ROSTER's own mix for this Level, if
    it's got one sized to match `n_enemies` (a real varied encounter,
    not clones of one archetype); otherwise the original behavior,
    `n_enemies` copies of make_enemy(level). A caller asking for some
    other `n_enemies` at a MIXED_ROSTER Level (a smaller test fight,
    say) still gets the old single-archetype-clone behavior, since the
    mix itself is a fixed-size set, not something to trim or repeat."""
    names = MIXED_ROSTER.get(level)
    if names and len(names) == n_enemies:
        return build_encounter(names)
    return [make_enemy(level) for _ in range(n_enemies)]


def build_encounter(names):
    """A custom encounter assembled from named reference rows in
    whatever Level/Slots mix is asked for - e.g. build_encounter(
    ["Generic Level 1 Tank", "Generic Level 1 Minion", "Generic Level 1
    Minion"]) for a 2-slot Tank plus two 0.5-slot Minions (a 3-slot
    encounter). Pass the result as combat_sim.run_fight's own
    `enemies=` param (it takes any list of already-built enemy dicts,
    not just N copies of one make_enemy(level) call) - see total_slots
    to check the mix against "one slot per PC," the default encounter
    budget (the designer's own framing - see this file's own module
    docstring; ENEMY_ENCOUNTER_DESIGN.md doesn't spell this rule out
    yet)."""
    return [get_enemy(name) for name in names]


def total_slots(enemies):
    """Sum of an encounter's own Slots values, for checking a
    build_encounter mix against "one slot per PC" (4 for a 4-PC party,
    made up however - four 1-slot enemies, two 1-slot plus four
    0.5-slot, one 2-slot plus two 1-slot, ...)."""
    return sum(e.get("slots", 1) for e in enemies)


if __name__ == "__main__":
    for e in all_enemies():
        print(e["level"], e["name"], "|", e["role"], "|", e["battle_tactic"], "|", e["fighting_style"],
              "| Acc", e["accuracy"], "| Dmg", e["attack_damage"], e["dmg_type"],
              "| Parry", e["parry"], "Mental", e["mental"], "| PhysRes", e["physres"], "| HP", e["health"])
