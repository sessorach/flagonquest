"""
Loads PC stat blocks from sample_pcs.csv - real named Stat/Skill builds
(all 5 Stats, all 25 Skills, matching index.html's own STAT_SKILLS),
not one abstract number per Tier. Same Roster/reference split as
sample_enemies.csv:

- **Roster** (`Roster` column TRUE) - exactly one per Tier 1-5, "Baseline
  Tier N Party Member." This is `tunables.py`'s old PC_SKILLS_COMBAT (the
  smoothed variant) migrated into full character-sheet form - see
  ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the derivation, and
  the smoothing rationale (avoids PC_SKILLS' real Tier-4 capstone spike
  swinging enemy calibration depending on whether a fight lands before or
  after it). `make_party(tier)` pulls this row and duplicates it x4 -
  still 4 identical party members, no distinct roles, no Techniques or
  items layered on top, no gear-based Resist bonus (just raw Essence).
- **Reference builds** (`Roster` FALSE) - named Level 1 characters (Hilde,
  Browndog, Carrick, Jackal, Felix), one leaning into each of the 5
  Stats, built to rulebook.md's own Quick Creation Reference shape (2
  Skills@3, 5@2, 2@1; 1 Stat@3, 2@2, 2@1) and verified to cost exactly 57
  XP in Skills+Stats (75 total chargen budget minus 18 XP/6 Levels of
  Techniques, which aren't modeled here). `get_pc(name)` pulls these by
  name.

**A real limitation worth stating plainly**: combat_sim.py's PC attack
roll only ever uses the party member's Melee Skill Total - there's no
modeling yet of a spellcaster attacking through Sorcery/Theurgy instead,
or a social-leaning character contributing anything other than melee
damage. Felix (Essence-primary, barely any Melee) will read as a weak
attacker in the current sim despite being a perfectly coherent character
on paper - that's a gap in combat_sim's model, not a mistake in Felix's
build. Fine for now since the Roster rows (what the validated grid
actually uses) are melee-competent by design; matters if a reference
build ever gets plugged into a real fight.

Every Stat/Skill/Defense formula here is straight from rulebook.md:
- Defense = 8 + [governing Skill Total]
- Weapon Damage = 4 + Body (Heavy 1H Melee formula, weapon_categories.csv)
- Resist = raw Essence, no Skill needed (rulebook.md's Calculated
  Statistics: "Resists... starts equal to your Essence")
- Speed = 1 + Agility (rulebook.md's Calculated Statistics) - only used
  by combat_sim.py's optional movement mode (run_fight(..., movement=
  True), see movement.py); ignored entirely otherwise.
"""
import csv
import os
import tunables as T

_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_pcs.csv")


def _load_rows():
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def skill_total(stats, skills, skill):
    stat = T.PC_SKILL_STAT[skill]
    return int(stats[stat]) + int(skills[skill])


def _pc_dict(row, index, good_luck):
    stats = {s: row[s] for s in ("Agility", "Body", "Cunning", "Mind", "Essence")}
    skills = {k: v for k, v in row.items() if k not in
              ("Name", "Tier", "Agility", "Body", "Cunning", "Mind", "Essence", "Health", "Roster", "Notes")}
    parry = 8 + skill_total(stats, skills, "Melee")
    dodge = 8 + skill_total(stats, skills, "Acrobatics")
    bodily = 8 + skill_total(stats, skills, "Resilience")
    mental = 8 + skill_total(stats, skills, "Composure")
    vigilant = 8 + skill_total(stats, skills, "Insight")
    damage = 4 + int(stats["Body"])  # Heavy 1H Melee formula
    physres = int(stats["Essence"])  # raw Essence, no Skill needed
    health = int(row["Health"])
    speed = 1 + int(stats["Agility"])  # rulebook.md: "Your Speed is equal to 1 + your Agility"
    return dict(name=row["Name"] if row["Name"].startswith("Baseline") else f"{row['Name']}{index}",
                parry=parry, dodge=dodge, bodily=bodily, mental=mental, vigilant=vigilant,
                skill_total=parry - 8,  # Melee's own Skill Total, for the PC's own attack roll
                damage=damage, physres=physres, health=health, max_health=health, speed=speed,
                crippled=0, vulnerable=0, bleeding=0, good_luck=good_luck)


def make_party(tier, good_luck=0):
    """4 copies of the Roster row for this Tier. `good_luck`: how many
    stacks of Good Luck every PC has on their own attack roll (rulebook.md:
    each stack flips one extra card, keep the highest) - 0 by default, a
    param specifically so combat_sim's good-luck-value experiment can turn
    it on without a second copy of this function."""
    for row in _load_rows():
        if row["Roster"].strip().upper() == "TRUE" and int(row["Tier"]) == tier:
            return [_pc_dict(row, i + 1, good_luck) for i in range(4)]
    raise ValueError(f"no Roster row for Tier {tier}")


def get_pc(name, good_luck=0):
    for row in _load_rows():
        if row["Name"] == name:
            return _pc_dict(row, 1, good_luck)
    raise KeyError(f"no sample_pcs.csv row named {name!r}")


def all_pcs():
    return [_pc_dict(row, 1, 0) for row in _load_rows()]


if __name__ == "__main__":
    for p in all_pcs():
        print(p["name"], "| Parry", p["parry"], "| Dodge", p["dodge"], "| Bodily", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])
