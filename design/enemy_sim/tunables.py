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

# ---- Armor tiers ----
# Not a literal copy of the player-facing armor_categories.csv (which
# gives every bonus relative to bare skin) - deliberately relative to an
# assumed baseline of an enemy already wearing some armor (per the
# designer: "a baseline of them having 1 armor"), i.e. Light's own
# numbers here (dodge/speed +0, physres +1) ARE that baseline. Unarmored
# then reads as trading that armor away for +1 Dodge/+1 Speed; Medium/
# Heavy read as layering on more Physical Resist at a cost to Dodge and
# Speed, same shape as the real player table's own tradeoff, just
# anchored one step over so an enemy's resulting stat block still lands
# close to what a similarly-built PC would have (verified against
# party.py's PC physres, which is raw Essence with no armor modeled).
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

# ---- Ability catalog: the subset wired into the simulator ----
# The full Ability catalog (ENEMY_ENCOUNTER_DESIGN.md's "The Ability
# catalog" section) has ~30 entries; only the ones with a single, clean
# numeric effect that this simulator's simplified round loop can
# actually represent are implemented here - flat stat modifiers, an
# on-hit debuff with one real number attached (Crippled's -1 to
# attacks, Vulnerable's -1 to Vital/Mental/Vigilant Defenses, Bleeding's
# 1 damage per decaying stack), and Durable's Protected regen. Left out
# for now: anything needing Speed/initiative (Slowed, Enhanced Speed -
# no turn-order model here), healing (Necrotic - no PC healing action
# exists in this sim), Harried/targeting-choice effects (Omniguard,
# Action abilities, Frightened/Taunted), multi-target hits (Strike
# (Cleaving)), and anything positional (Sturdy, Shadow Jaunt,
# Retribution Aura). Costs match the real catalog exactly, for the
# budget-validation check in enemy_builder.build_enemy.
ABILITY_COST = {
    "Enhanced Health": 5,
    "Powerful Weapon": 5,
    "Powerful Spell": 5,
    "Strike (Crippling)": 5,
    "Strike (Vulnerable)": 5,
    "Poison (Bleeding)": 5,
    "Durable": 5,
}

# ---- PC power per Tier (1-5) ----
# A real named Stat/Skill build per Tier (75/125/175/225/275 total XP -
# the designer's own chargen-then-+50/tier schedule), not an abstract
# Skill Total number - see ENEMY_ENCOUNTER_DESIGN.md's Analysis section
# for the full derivation and every correction that went into this.
# Every tier's total XP is exact (verified against rulebook.md's real
# Skill/Stat cost formulas: N(N+1)/2 for Skills, N(N+1) for Stats,
# leftover after Skills+Stats rolls into Techniques).
#
# Shape: one favorite Skill (Melee) leads throughout - starts at rank 3
# (chargen's own "push your best skill" pattern, Skill Total ~5) and
# hits its rank-5 cap by Tier 4 (a "capstone" push for late Techniques).
# The other 3 Defense-relevant Skills (Acrobatics/Resilience/Composure),
# one social Skill (Persuasion), and Insight (Vigilant Defense) form a
# "core" tier that rounds out through Tiers 2-3. Eight more Skills
# (Awareness/Craft/Streetwise/Athletics/Might/Medicine/Survival/Stealth)
# get real, if modest, investment too - "spread wide," not a short list
# that maxes out and stops. Essence is prioritized on the Stat side
# specifically because Resist = raw Essence with zero Skill investment
# needed (rulebook.md) - the single most XP-efficient survivability
# stat in the game, previously badly under-prioritized.
PC_SKILLS = {
    1: {"Melee": 3, "Acrobatics": 2, "Resilience": 2, "Composure": 2, "Persuasion": 2, "Insight": 2,
        "Awareness": 2, "Craft": 0, "Streetwise": 0, "Athletics": 0, "Might": 1, "Medicine": 1, "Survival": 1, "Stealth": 1},
    2: {"Melee": 3, "Acrobatics": 3, "Resilience": 3, "Composure": 3, "Persuasion": 2, "Insight": 2,
        "Awareness": 2, "Craft": 2, "Streetwise": 2, "Athletics": 2, "Might": 1, "Medicine": 1, "Survival": 1, "Stealth": 1},
    3: {"Melee": 4, "Acrobatics": 4, "Resilience": 3, "Composure": 3, "Persuasion": 3, "Insight": 3,
        "Awareness": 2, "Craft": 2, "Streetwise": 2, "Athletics": 2, "Might": 2, "Medicine": 2, "Survival": 2, "Stealth": 2},
    4: {"Melee": 5, "Acrobatics": 4, "Resilience": 4, "Composure": 4, "Persuasion": 4, "Insight": 3,
        "Awareness": 3, "Craft": 2, "Streetwise": 1, "Athletics": 2, "Might": 2, "Medicine": 2, "Survival": 2, "Stealth": 2},
    5: {"Melee": 5, "Acrobatics": 4, "Resilience": 4, "Composure": 4, "Persuasion": 4, "Insight": 4,
        "Awareness": 3, "Craft": 3, "Streetwise": 3, "Athletics": 3, "Might": 2, "Medicine": 2, "Survival": 2, "Stealth": 2},
}
PC_STATS = {
    1: {"Agility": 2, "Essence": 2, "Body": 2, "Cunning": 2, "Mind": 1},
    2: {"Agility": 3, "Essence": 3, "Body": 2, "Cunning": 2, "Mind": 2},
    3: {"Agility": 3, "Essence": 3, "Body": 3, "Cunning": 3, "Mind": 3},
    4: {"Agility": 4, "Essence": 4, "Body": 4, "Cunning": 3, "Mind": 3},
    5: {"Agility": 4, "Essence": 4, "Body": 4, "Cunning": 4, "Mind": 4},
}

# Combat-calibration variant of PC_SKILLS, used by party.py instead of the
# table above. PC_SKILLS above is deliberately non-monotonic in feel - a
# real player's journey has a Tier-4 "capstone" spike where their favorite
# Skill jumps to its rank-5 cap all at once. But the enemy Level curve
# (ACCURACY/DMG_RESIST/HEALTH_BASE above) climbs smoothly, so calibrating
# enemies against the spiky version makes Level 4 swing from "brutal" to
# "trivial" depending on whether a given fight lands before or after that
# spike - not a useful target to tune against. This variant reverts just
# the Tier-4 Melee spike (rank 4, not 5 - the push happens by Tier 5
# instead), giving a smooth +1 Skill Total/tier line for Melee specifically,
# with the freed Tier-4 XP spent on Acrobatics instead (same total XP
# either way, verified exact). Everything else is identical to PC_SKILLS -
# only Melee's growth curve differs, since it's the only Skill with an
# explicit capstone tweak. PC_SKILLS itself is the one to read for a real
# example build (see ENEMY_ENCOUNTER_DESIGN.md's "Hilde" writeup); this is
# purely an enemy-balancing convenience.
import copy as _copy
PC_SKILLS_COMBAT = _copy.deepcopy(PC_SKILLS)
PC_SKILLS_COMBAT[4]["Melee"] = 4
PC_SKILLS_COMBAT[4]["Acrobatics"] = 5

# Which Stat governs each named PC Skill above (index.html's STAT_SKILLS).
PC_SKILL_STAT = {
    "Melee": "Agility", "Acrobatics": "Agility", "Stealth": "Agility",
    "Resilience": "Body", "Awareness": "Body", "Might": "Body", "Athletics": "Body",
    "Persuasion": "Cunning", "Insight": "Cunning", "Streetwise": "Cunning", "Survival": "Cunning",
    "Composure": "Mind", "Craft": "Mind", "Medicine": "Mind",
}

# PC Health per Tier: chargen's real floor (10 = 5 Shallow + 5 Deep) plus
# whichever tier of the real Toughened Body/Resolve/Spirit technique
# family (T014/T019/T023, gated on raw Resilience-or-Composure rank
# 3/4/5) this build's own raw skill ranks actually qualify for - a
# genuine technique lookup, not an invented growth curve. This build's
# Resilience/Composure never reach raw rank 5 (breadth wins out over
# that last point of specialization), so Toughened Spirit never comes
# into play - Health tops out at 14, not 15.
PC_HEALTH = {1: 10, 2: 13, 3: 13, 4: 14, 5: 14}
