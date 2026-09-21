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

# ---- Armor tiers (armor_categories.csv, the real player-facing table) ----
# One shared table for both sides now - enemies and PCs alike wear real
# armor and get the real armor bonus (see party.py's own Armor
# paragraph for the PC side; enemy_builder.py already used this table).
# Physical Resist only - rulebook.md's Resist rule ("starts equal to
# your Essence") only gets a further boost from Armor for Physical
# damage; elemental Resist (Fire/Frost/Brilliant/Shadow, collapsed into
# one `elemres` pool in this sim) stays Essence-only on both sides, no
# armor contribution, matching armor_categories.csv's own column being
# titled "Physical Resist" specifically. Unarmored is the implicit
# baseline (all zeroes) - armor_categories.csv only lists the three worn
# tiers, each relative to bare skin. This used to be a different,
# enemy-only table anchored one step over Unarmored (to compensate for
# PCs having no armor modeled at all) - now that PCs get the real thing
# too (see party.py), that workaround isn't needed; both sides read off
# this one real table. Note this does shift every enemy that wasn't
# already on Light Armor (all 5 Roster enemies are, so the validated
# grid's own enemy side is unaffected - only Medium/Heavy archetype
# rows, like the Tank archetype, see a small Dodge/Speed change).
ARMOR = {
    "Unarmored": {"dodge": 0, "speed": 0, "physres": 0},
    "Light":     {"dodge": 0, "speed": 0, "physres": 1},
    "Medium":    {"dodge": -1, "speed": 0, "physres": 2},
    "Heavy":     {"dodge": -1, "speed": -1, "physres": 3},
}

# ---- Action Points (rulebook.md's "Actions on a Turn") ----
# "When you flip Reflex to join an encounter, and again at the end of
# each of your turns, you lose any existing Action Points and gain 4
# Action Points in their place." - a flat per-turn budget every unit
# gets, spent on move actions and attacks (see combat_sim.py's
# spend_movement_ap and the Party's/Enemies' turn loops in run_fight).
AP_PER_TURN = 4
# "A move action takes 1 AP to make... this moves you up to your Speed
# in meters. You can always end a move action early." - can be taken
# more than once in a turn, AP allowing, which is exactly how closing a
# longer gap than one Speed's worth of distance works here.
MOVE_AP_COST = 1
# "Most normal actions that involve a bit of effort, like making an
# attack, take 2 AP to do."
ATTACK_AP_COST = 2
# T105 Healing Magic's own techniques.csv row gives it 1 AP specifically
# (not the standard 2 above) - see tactics.strategy_support_healer.
HEALING_MAGIC_AP_COST = 1

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

# ---- PC ranged attack options (sample_pcs.csv's `Weapon` column) ----
# A PC row with a blank Weapon uses the original hardcoded default (1H
# Heavy Melee: Melee Skill Total, no accuracy bonus, Damage = 4 + Body,
# no attack_range - falls back to MELEE_RANGE via combat_sim.
# effective_range) - every pre-existing PC row still does this, so this
# table only needs entries for the ranged options actually in use.
# Numbers are real weapon_categories.csv/rulebook.md values, not
# invented for the simulator:
# - Light Bow: Accuracy +1, Damage 3 + [Cunning], Skill Archery - Range
#   19m from the actual craftable item (items.csv I123 "Light Bow", the
#   one PCs actually carry), not weapon_categories.csv WC007's more
#   abstract 15m category value - items.csv is the more specific source
#   for a real equipped item, so it wins per this project's own
#   data-over-prose/data-over-abstraction principle. Sable (Deadeye)'s
#   Notes flags this correction.
# - Light Thrown (WC005): Accuracy +1, Damage 3 + [Cunning], Range
#   "Close, or 3 x Body" - modeled as the ranged option (3 x Body), the
#   whole point of a thrown weapon's own scaling being worth testing
#   here; Skill "Acrobatics or Melee" - Acrobatics chosen (Dodge's own
#   governing Skill, an agile-skirmisher lean).
# - War Magic (Lance) - War Magic (T120) itself is Range "An adjacent
#   creature"; its own Lance feature (features.csv F064) reads "Increase
#   the Range of the spell attack by [Sorcery Skill Total] meters" - so
#   a War Magic build that's taken Lance has Range == Sorcery Skill
#   Total exactly, per the designer's own framing. No Accuracy bonus (a
#   Spell attack roll, not a weapon-category one); Damage 2 + [Mind]
#   straight from T120's own Effects text (the spell's damage stat is
#   Mind, distinct from Essence, which governs the Sorcery Skill Total
#   that resolves the attack roll and this Range - the two track
#   separately here the same way melee's own Skill Total (Agility) and
#   Damage stat (Body) already do). `dmg_type` selects which of the
#   target's own Resist pools the hit is reduced by (see combat_sim.
#   enemy_resist_for_pc_attack) - Fire for War Magic, matching T120's own
#   Effects text ("...Fire damage"), Physical for both real weapons
#   (matching tunables.ACTIONS' own Physical/Fire split for the enemy
#   side of the same Actions). `opp_def` selects which of the target's
#   Defenses the attack roll is opposed by - "Parry/Dodge" (the
#   target's own choice, rulebook.md's real rule for a weapon attack)
#   for both real weapons; War Magic's own rule reads "against the
#   target's Defense (Dodge or Vital, chosen when you learn this)" - a
#   one-time pick at chargen, not a per-attack target choice like
#   Parry/Dodge - Dodge was picked here to match how tunables.ACTIONS
#   already resolves the enemy side's own Melee/Ranged Spell (opp_def
#   "Dodge", no Bodily/Vital option modeled).
WEAPON = {
    "Light Bow":         {"skill": "Archery",    "accuracy": 1, "damage_base": 3, "damage_stat": "Cunning", "range": 19,
                           "dmg_type": "Physical", "opp_def": "Parry/Dodge"},
    "Light Thrown":      {"skill": "Acrobatics",  "accuracy": 1, "damage_base": 3, "damage_stat": "Cunning", "range_per_body": 3,
                           "dmg_type": "Physical", "opp_def": "Parry/Dodge"},
    "War Magic (Lance)": {"skill": "Sorcery",     "accuracy": 0, "damage_base": 2, "damage_stat": "Mind",    "range_per_skill": 1,
                           "dmg_type": "Fire", "opp_def": "Dodge"},
    # 2H Heavy Melee (weapon_categories.csv WC004): Accuracy +0, Damage
    # 5 + [Body] (one higher than the 1H Heavy Melee default every blank
    # `Weapon` cell already gets), Skill Melee, no attack_range (falls
    # back to MELEE_RANGE like the blank default) - the only real
    # difference from leaving `Weapon` blank is the +1 Damage.
    "2H Heavy Melee":    {"skill": "Melee",       "accuracy": 0, "damage_base": 5, "damage_stat": "Body",
                           "dmg_type": "Physical", "opp_def": "Parry/Dodge"},
    # Unarmed (weapon_categories.csv WC009): Accuracy +2, Damage
    # 2 + [Body or Cunning], Skill Brawl - for a Brawl-built PC (Hanforth)
    # who doesn't actually invest in Melee, so the blank-Weapon default
    # (Melee Skill Total) would badly understate them; "Body or Cunning"
    # picked per-PC as whichever's actually higher (Hanforth's own
    # Cunning) rather than hardcoded, same "pick the one that matches
    # the build" call Light Thrown's own Acrobotics-vs-Melee choice
    # already makes - see party.py's own handling.
    "Unarmed":           {"skill": "Brawl",       "accuracy": 2, "damage_base": 2, "damage_stat": None,
                           "dmg_type": "Physical", "opp_def": "Parry/Dodge"},
}

# ---- Movement mode: party formation and start distance ----
# A 2x2 block, "for simplicity's sake" per the designer, rather than the
# single-file line the enemies still use (_start_positions in
# combat_sim.py) - real formation/facing isn't modeled at all, this is
# just enough that the party's 4 positions aren't identical. spacing=2
# keeps the block tight (roughly MELEE_RANGE-sized) without stacking
# every PC on one exact point.
PARTY_FORMATION_SPACING = 2
# The party's and enemies' front lines start a random distance apart in
# this range (meters) each fight, centered in the arena - "spaced out
# slightly but not opposite ends," per the designer, replacing the
# original fixed 16m corner-to-corner start this mode shipped with.
# run_fight's own `start_gap` param can override this with a fixed
# distance instead, for a controlled before/after comparison.
START_GAP_RANGE = (5, 10)

# ---- TODO: PC power budget from loot - partially resolved, not fully ----
# The designer's own point: PCs get a small power bump from the loot they
# find (items/gear), same idea as ENEMY_ENCOUNTER_DESIGN.md's enemy-side
# "loot/Gold discount" (350 Gold total across 15 notional Levels, Gold÷7
# XP-equivalent, subtracted from the enemy's own stat budget before
# pricing - see that doc's "per-Level total budget" section). Real worn
# Armor (see ARMOR above and party.py's own Armor paragraph) is now
# modeled and closes part of this gap - a PC's Physical Resist is no
# longer bare Essence alone. Still missing: every other kind of gear
# (weapons beyond the base weapon_categories.csv options already modeled
# via `Weapon`, Masterwork items, Techniques) - deferred per the
# designer's original framing, same as before. If this gets picked up
# further, the enemy-side Gold÷7 XP-equivalent rate is still the natural
# starting point for whatever's still missing.
