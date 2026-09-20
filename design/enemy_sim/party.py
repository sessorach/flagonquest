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
- **Reference builds** (`Roster` FALSE) - named Level 1 characters, one
  leaning into each of the 5 Stats, built to rulebook.md's own Quick
  Creation Reference shape (2 Skills@3, 5@2, 2@1; 1 Stat@3, 2@2, 2@1) and
  verified to cost exactly 57 XP in Skills+Stats (75 total chargen
  budget minus 18 XP/6 Levels of Techniques, which aren't modeled here).
  `get_pc(name)` pulls these by name; `make_party_of(name)` duplicates
  one x4 into a full party, for testing a single build's own attack
  profile against the validated Roster; `make_party_from([names])`
  assembles a custom 4-person mix instead, for testing party
  composition itself (see combat_sim.py's own note on what both showed).
  Melee-attacking: Hilde, Browndog, Carrick, Jackal, Felix (Felix,
  Essence-primary with barely any Melee, reads as a weak attacker
  despite being a coherent character on paper - see the Weapon
  paragraph below for why, and Wren for the same Essence-primary
  concept actually built to attack through Sorcery instead).
  Ranged-attacking (see `Weapon` below): Sable (Archery/Light Bow), Rook
  (Acrobatics/Light Thrown), Wren (Sorcery/War Magic + Lance).
  Support: Beornhard (weak Melee attacker, solid Theurgy - see
  `Support` below).

**`Weapon`** (blank for most rows) switches which Skill/Stat combo
governs a PC's own attack roll, Damage, damage type, opposed Defense,
and attack range - a real capability this sim didn't have originally,
when every PC's attack was hardcoded to Melee/Physical regardless of
build. A blank cell keeps that original 1H Heavy Melee default (Melee
Skill Total, Damage = 4 + Body, Physical, opposed by Parry/Dodge, no
attack_range - falls back to `MELEE_RANGE` under `movement=True`); a
name from `tunables.WEAPON` (`"Light Bow"`, `"Light Thrown"`, `"War
Magic (Lance)"`) switches to that weapon's own real numbers - see
`tunables.WEAPON`'s own comment for the weapon_categories.csv/
features.csv sourcing, including why War Magic's damage is Fire (so it
draws on a target's `elemres`, not `physres` - see combat_sim.
enemy_resist_for_pc_attack) and opposed by Dodge alone rather than
Parry/Dodge. This is fully decoupled from
parry/dodge/bodily/mental/vigilant, which always come from
Melee/Acrobatics/Resilience/Composure/Insight regardless of `Weapon` -
a War Magic caster's Sorcery Skill Total drives their own attack and
Range without touching their (separately tracked) Parry.

**`Support`** (`TRUE`/blank) flags a PC who spends their turn healing
an ally instead of attacking when combat_sim.py's `resolve_support_pc`
decides the party needs it, approximating T105 Healing Magic (Level 1:
discard 1 card, heal 1 Shallow Health + 1 more if that card's a Heart)
- see combat_sim.py's own docstring for the exact heuristic and what it
showed. Doesn't change anything in this file - `support` just gets
threaded onto the PC dict as a plain bool for combat_sim to read.

Every Stat/Skill/Defense formula here is straight from rulebook.md:
- Defense = 8 + [governing Skill Total]
- Weapon Damage = 4 + Body (Heavy 1H Melee formula, weapon_categories.csv)
  unless `Weapon` names a ranged option (see above)
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
              ("Name", "Tier", "Agility", "Body", "Cunning", "Mind", "Essence", "Health", "Roster", "Notes", "Weapon", "Support")}
    parry = 8 + skill_total(stats, skills, "Melee")
    dodge = 8 + skill_total(stats, skills, "Acrobatics")
    bodily = 8 + skill_total(stats, skills, "Resilience")
    mental = 8 + skill_total(stats, skills, "Composure")
    vigilant = 8 + skill_total(stats, skills, "Insight")
    physres = int(stats["Essence"])  # raw Essence, no Skill needed
    health = int(row["Health"])
    speed = 1 + int(stats["Agility"])  # rulebook.md: "Your Speed is equal to 1 + your Agility"

    # The PC's own attack roll: 1H Heavy Melee (Melee Skill Total, no
    # accuracy bonus, Damage 4 + Body, Physical, opposed by Parry/Dodge,
    # no attack_range - falls back to MELEE_RANGE) unless `Weapon` names
    # a ranged option in T.WEAPON, in which case the attacking
    # Skill/accuracy/Damage/Range/dmg_type/opp_def all switch to that
    # weapon's own numbers - see T.WEAPON's own comment for the real
    # rulebook.md/weapon_categories.csv values behind each one. This is
    # deliberately decoupled from parry/dodge/bodily/mental/vigilant
    # above - a caster's Sorcery Skill Total (or an archer's Archery)
    # drives their own attack roll and Range without touching their
    # Melee-based Parry or any other Defense.
    weapon = (row.get("Weapon") or "").strip()
    attack_range = None
    if weapon and weapon in T.WEAPON:
        w = T.WEAPON[weapon]
        atk_skill_total = skill_total(stats, skills, w["skill"]) + w["accuracy"]
        damage = w["damage_base"] + int(stats[w["damage_stat"]])
        dmg_type = w["dmg_type"]
        opp_def = w["opp_def"]
        if "range" in w:
            attack_range = w["range"]
        elif "range_per_body" in w:
            attack_range = w["range_per_body"] * int(stats["Body"])
        elif "range_per_skill" in w:
            attack_range = w["range_per_skill"] * skill_total(stats, skills, w["skill"])
    else:
        atk_skill_total = skill_total(stats, skills, "Melee")
        damage = 4 + int(stats["Body"])
        dmg_type = "Physical"
        opp_def = "Parry/Dodge"

    pc = dict(name=row["Name"] if row["Name"].startswith("Baseline") else f"{row['Name']}{index}",
              parry=parry, dodge=dodge, bodily=bodily, mental=mental, vigilant=vigilant,
              skill_total=atk_skill_total,  # the PC's own attacking Skill Total - see the Weapon block above
              damage=damage, dmg_type=dmg_type, opp_def=opp_def,
              physres=physres, health=health, max_health=health, speed=speed,
              crippled=0, vulnerable=0, bleeding=0, good_luck=good_luck,
              support=(row.get("Support") or "").strip().upper() == "TRUE")
    if attack_range is not None:
        pc["attack_range"] = attack_range
    return pc


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


def make_party_of(name, good_luck=0):
    """4 copies of a single named reference PC (Roster or not) - same
    duplication pattern as make_party(tier), just keyed by name instead
    of Tier. For testing one build's own attack profile (a ranged PC's
    Weapon, say) against the validated Roster without hand-assembling a
    mixed party - monkeypatch combat_sim.make_party to this the same way
    the README's item-balancing checks monkeypatch combat_sim.make_enemy."""
    return make_party_from([name] * 4, good_luck)


def make_party_from(names, good_luck=0):
    """A custom party assembled from named reference rows in whatever mix
    is asked for (e.g. ["Hilde", "Browndog", "Sable", "Beornhard"]) -
    for testing party composition itself, not just one build cloned x4.
    Same monkeypatch-combat_sim.make_party usage as make_party_of."""
    rows = {r["Name"]: r for r in _load_rows()}
    return [_pc_dict(rows[name], i + 1, good_luck) for i, name in enumerate(names)]


def all_pcs():
    return [_pc_dict(row, 1, 0) for row in _load_rows()]


if __name__ == "__main__":
    for p in all_pcs():
        print(p["name"], "| Parry", p["parry"], "| Dodge", p["dodge"], "| Bodily", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])
