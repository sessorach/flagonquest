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
"""
import csv
import os
from enemy_builder import build_enemy

_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_enemies.csv")


def _load_rows():
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _build_from_row(row):
    e = build_enemy(
        row["Name"],
        int(row["Level"]),
        float(row["Slots"]),
        row["Role"],
        row["PrimaryDef"] or None,
        row["SecondaryDef"] or None,
        row["Action"],
        row["Armor"],
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
