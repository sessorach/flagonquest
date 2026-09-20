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

# ---- Movement mode (combat_sim.run_fight(..., movement=True)) ----
# A bounded square arena, in meters ("space" and "meter" are the same
# unit throughout this project - see weapon/spell Range values). 20x20
# was picked as a representative mid-size arena, not derived from
# anything - a real Range value at Level 5 (Heavy Bow: 17m, Ranged
# Spell: 12m) can span most of it, while Level 1's shorter ranges (5-6m)
# leave real room for a kiter to actually use the space.
ARENA_SIZE = 20
# How close two units need to be for a melee Action (attack_range == 0
# from enemy_builder's own formula) to actually connect - not literally
# 0, since two approaching units stopping exactly on top of each other
# isn't a sensible reading of "Close Range." Not derived from a real
# rulebook.md number (no such number exists); picked as a small,
# plausible "within striking distance" buffer.
MELEE_RANGE = 2

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
# PC stat blocks moved to sample_pcs.csv (real named Stat/Skill builds -
# all 5 Stats, all 25 Skills, matching index.html's STAT_SKILLS) - see
# party.py's own module docstring for the Roster/reference-build split
# and ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the original
# derivation and every correction that went into the Roster numbers.
# This used to be four dicts here (PC_SKILLS, PC_STATS, PC_SKILLS_COMBAT,
# PC_HEALTH) - migrated out once real character sheets existed to hold
# them properly, same reasoning as sample_enemies.py's own CSV move.
# The PC_SKILLS_COMBAT-vs-PC_SKILLS smoothing rationale (avoiding a real
# player's Tier-4 "capstone" spike from swinging enemy calibration
# depending on which side of it a fight lands) still applies - it's
# baked directly into the Roster rows now rather than kept as a second
# parallel table.

# Which Stat governs each named PC Skill (index.html's STAT_SKILLS) -
# still needed by party.py to compute Skill Totals from the CSV's raw
# Stat/Skill columns, so it stays here rather than moving to the CSV
# itself (a structural fact, not a tunable number).
PC_SKILL_STAT = {
    "Melee": "Agility", "Acrobatics": "Agility", "Stealth": "Agility", "Archery": "Agility", "Brawl": "Agility",
    "Resilience": "Body", "Awareness": "Body", "Might": "Body", "Athletics": "Body", "Presence": "Body",
    "Persuasion": "Cunning", "Insight": "Cunning", "Streetwise": "Cunning", "Survival": "Cunning", "Masquerade": "Cunning",
    "Composure": "Mind", "Craft": "Mind", "Medicine": "Mind", "Academics": "Mind", "Mixology": "Mind",
    "Meditation": "Essence", "Performance": "Essence", "Rapport": "Essence", "Sorcery": "Essence", "Theurgy": "Essence",
}

# ---- TODO: PC power budget from loot - not modeled yet ----
# The designer's own point: PCs get a small power bump from the loot they
# find (items/gear), same idea as ENEMY_ENCOUNTER_DESIGN.md's enemy-side
# "loot/Gold discount" (350 Gold total across 15 notional Levels, Gold÷7
# XP-equivalent, subtracted from the enemy's own stat budget before
# pricing - see that doc's "per-Level total budget" section). Nothing on
# the PC/Roster side accounts for this yet - the Roster rows in
# sample_pcs.csv are bare Stats/Skills/Health only, no items layered on
# top, so this simulator currently reads PCs as somewhat weaker than a
# real, geared party would be at the same Tier. Deferred per the
# designer ("if it's a bit of a tricky calculation, put a note to do it
# later and just worry about the sim for now") rather than guessed at
# here - when this gets picked up, the enemy-side Gold÷7 XP-equivalent
# rate is the natural starting point for converting loot into the same
# kind of stat-budget bump.
