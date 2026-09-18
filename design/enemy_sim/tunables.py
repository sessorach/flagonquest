"""
Every number in the enemy/party model that's still subject to revision —
edit this file when the PC or enemy baselines change, not enemy_builder.py
or party.py. Those two files implement the *shape* of the formulas (how
Level/Role/Armor/Defense-tier combine); this file is *what the numbers
currently are*, kept separate specifically so re-tuning doesn't require
touching mechanics code.

Enemy-side curves are a direct port of archive/flagonquest_encounter_
builder.xlsx's "Design" and "Encounter References" tabs (verified against
its own live worked example — see enemy_builder.py's __main__ block).
PC-side curves are this project's own estimate (see design/
ENEMY_ENCOUNTER_DESIGN.md's "Analysis" section for the derivation) and
are the piece most likely to move as the PC/enemy models get revisited.
"""

# ---- Enemy Level curve (Design sheet) ----
ACCURACY = {1: 4, 2: 6, 3: 7, 4: 8, 5: 9}
DMG_RESIST = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}
HEALTH_BASE = {1: 7, 2: 8, 3: 10, 4: 11, 5: 13}
ABILITY_RATE = {1: 2, 2: 3, 3: 4, 4: 5, 5: 8}

# ---- Encounter Slots -> Health multiplier (non-linear, action-economy tax) ----
SLOT_MULTIPLIER = {1: 1, 0.5: 1 / 3, 2: 3}

# ---- Armor tiers (Combat Armor catalog) ----
ARMOR = {
    "Unarmored": {"dodge": 1, "speed": 1, "physres": 0},
    "Light":     {"dodge": 0, "speed": 0, "physres": 1},
    "Medium":    {"dodge": -1, "speed": -1, "physres": 2},
    "Heavy":     {"dodge": -2, "speed": -2, "physres": 3},
}

# ---- Role archetypes (Combat Role catalog, richer/authoritative version) ----
ROLE_MODS = {
    "None":       {},
    "Tank":       {"resist": 1, "parry": 1, "dodge": 1, "elem_all": 1},
    "Striker":    {"accuracy": 1, "damage": 1},
    "Bruiser":    {"damage": 1, "resist": 1, "parry": -1, "dodge": -1, "elem_all": 1},
    "Strategist": {"accuracy": 1, "bodily": 1, "mental": 1},
    "Defensive":  {"parry": 1, "dodge": 1, "bodily": 1, "mental": 1},
}

# ---- Combat Actions (own direct Accuracy/Damage/Parry contributions) ----
ACTIONS = {
    "Defensive Melee": {"accuracy": 1, "damage": 3, "parry": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Offensive Melee":  {"accuracy": 0, "damage": 4, "parry": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Ranged Weapon":    {"accuracy": 1, "damage": 3, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Melee Spell":      {"accuracy": 0, "damage": 3, "dmg_type": "Fire", "opp_def": "Dodge", "range": 0},
    "Ranged Spell":     {"accuracy": 0, "damage": 2, "dmg_type": "Fire", "opp_def": "Dodge", "range": 2},
}

# ---- PC power per Tier (1-5) ----
# "Mid" column from ENEMY_ENCOUNTER_DESIGN.md's Analysis section: the Skill
# Total needed for ~54% hit chance against a Secondary-tier enemy Defense
# at that same Level. The single number this session's own from-scratch
# reconstruction, not extracted from the spreadsheet - most likely to be
# revised as the PC/enemy models get worked on further.
SKILL_TOTAL = {1: 5, 2: 7, 3: 8, 4: 9, 5: 10}

# PC's own weapon-relevant Stat, for weapon Damage formulas. Reuses the
# enemy's own "grenade base stat 3-5 by Level" convention as a deliberate
# simplification (both sides scaling off the same on-Level Stat curve) -
# see ENEMY_ENCOUNTER_DESIGN.md for the reasoning and its caveats.
WEAPON_STAT = {1: 3, 2: 3, 3: 4, 4: 5, 5: 5}

# PC Health per Tier: chargen's real floor (10 = 5 Shallow + 5 Deep) plus
# growth shaped like the enemy's own Health curve above (relative, not
# independently derived - flagged as an estimate in the design doc).
PC_HEALTH = {t: 10 + (HEALTH_BASE[t] - HEALTH_BASE[1]) for t in range(1, 6)}
