"""
An alternative to enemy_builder.py's build_enemy() - built off the same
formulas rulebook.md actually gives a PC (party.py's own docstring: "Every
Stat/Skill/Defense formula here is straight from rulebook.md"), instead of
enemy_builder.py's own synthetic Level curve (ACCURACY/DMG_RESIST, a flat
number per Level that a Role modifier and an Action modifier and a Defense-
tier bonus all then stack on top of). That stacking is exactly why this
project kept finding "sharp, hard to control" levers all session - each
layer is its own small swing, and they compound. This file skips the
synthetic curve and builds an enemy the way a PC actually gets built: as a
real Skill Total per Defense (Defense = 8 + Skill Total, party.py's own
formula) and a real weapon-style Damage (base + a governing Stat, same as
party.py's default 1H Heavy Melee = 4 + Body), with Resist coming from a
separate Stat (Essence) entirely - not the same number that also drives
Damage the way DMG_RESIST does in enemy_builder.py.

**SKILL_TOTAL_BY_LEVEL** is design/ENEMY_ENCOUNTER_DESIGN.md's own "What
Skill Total a PC needs to be on-level, per Enemy Level" table (the
"Analysis" section, computed from the real card-flip math: ~54% hit chance
needs Skill Total = Defense - 7) - not a fresh invention, an existing,
already-cross-checked number. Three tiers per Level (poor/secondary/
primary) stand in for "how much this enemy invested in that Skill,"
exactly like a real PC's chargen (rulebook.md's Quick Creation Reference:
2 Skills@3, 5@2, 2@1) leaves most Skills lower than the couple they leaned
into.

**STAT_BASELINE_BY_LEVEL** is read straight off sample_pcs.csv's own
"Baseline Tier N Party Member" rows (make_party(tier)'s validated,
already-calibrated party) - their real Body/Essence Stats, not a guess.
Cross-checking the two tables against each other: Baseline Tier 1's own
Melee Skill Total (Agility 2 + Melee 3 = 5) lands exactly on this table's
Level 1 "secondary" tier (5) - the validated on-level PC baseline already
sits at the "secondary" row, which is the intended reading: an enemy given
uniform "secondary" tiers across the board plays like a mirror-image of
the party's own baseline, not a harder or easier version of it.

**Five independent Defense tiers** (`defense_tiers={"parry":..., "dodge":
..., "bodily":..., "mental":..., "vigilant":...}`, each "primary"/
"secondary"/"poor") replace enemy_builder.py's PrimaryDef/SecondaryDef
pair (which bundles Parry and Dodge into one "Parry/Dodge" category,
moving together always) - a real PC's Melee (Parry) and Acrobatics
(Dodge) are separate Skills that can be raised completely independently
(rulebook.md never bundles them), so this gives the same variety a real
character sheet would have instead of an invented "+2/+1" bonus tacked
onto a flat baseline. Leaving a Defense out of the dict defaults it to
"poor" - a genuine weak point, same as a Skill a PC never invested in.
Vigilant added alongside the original four for the same reason
enemy_builder.py's own tiering grew a fourth category - see
ENEMY_ENCOUNTER_DESIGN.md's Defense tiering section.
"""
import math
import tunables as T

# design/ENEMY_ENCOUNTER_DESIGN.md, "What Skill Total a PC needs to be
# on-level, per Enemy Level" - poor/secondary/primary Defense tiers.
SKILL_TOTAL_BY_LEVEL = {
    1: {"poor": 4, "secondary": 5, "primary": 6},
    2: {"poor": 6, "secondary": 7, "primary": 8},
    3: {"poor": 7, "secondary": 8, "primary": 9},
    4: {"poor": 8, "secondary": 9, "primary": 10},
    5: {"poor": 9, "secondary": 10, "primary": 11},
}

# sample_pcs.csv's "Baseline Tier N Party Member" rows - real Body/Essence,
# not derived. (Agility/Melee aren't needed here since accuracy comes from
# SKILL_TOTAL_BY_LEVEL directly, the same way party.py's Weapon system
# decouples a PC's attack Skill Total from their Parry/Dodge/etc.)
STAT_BASELINE_BY_LEVEL = {
    1: {"body": 2, "essence": 2},
    2: {"body": 2, "essence": 3},
    3: {"body": 3, "essence": 3},
    4: {"body": 4, "essence": 4},
    5: {"body": 4, "essence": 4},
}

# 2026-09-30 projection model, per the designer: enemies built from the
# same Stat spread a real PC has at that Level (chargen's one Stat at 3,
# two at 2, two at 1, then the Tier XP table's Stat share: 28/43/55/64/70
# XP), with the archetype choosing which Stat leads (`StatOrder`). Damage
# comes from that Stat through the players' own weapon/spell table, and
# Resist is Essence plus worn Armor, same as a PC. This is for getting
# projections solid before it gets simplified into a low-baseline-plus-
# archetype-upgrades system for building stat blocks by hand.
PC_STAT_SPREAD_BY_LEVEL = {
    0: [2, 2, 2, 1, 1],  # below chargen - only reached by an enemy's lag at Level 1
    1: [3, 2, 2, 1, 1],
    2: [4, 3, 2, 1, 1],
    3: [4, 4, 2, 2, 1],
    4: [5, 4, 2, 2, 1],
    5: [5, 4, 3, 2, 1],
}

# The party's margin, per the designer: PC-modeled enemies, minus a bit
# so the party is projected to win while spending resources. Both knobs
# are real stats, not fudge factors - an enemy has the Stat spread of a
# PC one Level behind it, and a PC's base Health (10, no Toughened Body).
# Settled from margin_sweep.py (balance_weights_notes.md, "Enemy margin").
ENEMY_STAT_LAG = 1
# Health is the one stat that breaks from player numbers on purpose, per
# the designer: a bit low early, padded more at high Levels. Level 2's 12
# comes from the 2026-09-30 armor-cost round (fights were ending in 3-4
# rounds at 10). Levels 3-5 are penciled until the sample parties go
# past Level 2. ENEMY_HEALTH_BASE, when set, overrides every Level
# (margin_sweep.py and other sweeps use it).
# 2026-10-01 draft rules (option 1): 3 lower at every Level than the
# pre-draft 10/12/14/16/18, to make room for an archetype plus a full
# ability allotment (ENEMY_ENCOUNTER_DESIGN.md, "Draft: the ability
# catalog at 1 pick = 1 Health").
#
# 2026-10-01, per the designer: a bare baseline plus an allotment of
# Upgrades, where +1 Health is one Upgrade among the rest. Each Level's
# baseline + Upgrades total matches the earlier baseline + picks
# (10/12/15/18/23 if everything went to Health), so the split is neutral
# for full-size enemies; Upgrades climb faster than Health so higher
# Levels get more room to stack effects. Levels 3-5 are penciled.
ENEMY_HEALTH_BY_LEVEL = {1: 6, 2: 6, 3: 7, 4: 8, 5: 9}
UPGRADES_BY_LEVEL = {1: 4, 2: 6, 3: 8, 4: 10, 5: 14}
ENEMY_HEALTH_BASE = None
# Flat bonus on every damaging enemy attack, on top of the weapon/spell
# table. Part of the enemy baseline (like Health above), not a player
# rule - tested 2026-09-30 as the designer's "buff enemies' default
# damage by 1" (level_baseline.py --enemy-damage 1).
ENEMY_DAMAGE_BONUS = 0
# Enemy Stats already run one Level behind a PC's; Skill tiers don't, so
# a Level 2 enemy's Primary Defense matches a Level 2 PC specialist's
# (Hedge Knight Parry 18 = Browndog's). Set to 1 to put Defenses one
# Level behind too (accuracy stays on-Level). Off by default; tested via
# level_baseline.py --defense-lag.
ENEMY_DEFENSE_LAG = 0

# 2026-09-30, per the designer: gear that's an overall gain costs the
# enemy something, the way it costs a player XP (the Might to wear it).
# Heavy Armor is Level 3+ only and paid from the Ability budget (two
# picks). Medium Armor is paid with a trade for now, until ability
# values get worked out: -2 Health, about what +1 Physical Resist less
# 1 Dodge came to in archetype_compare.py (ENEMY_ENCOUNTER_DESIGN.md).
HEAVY_ARMOR_MIN_LEVEL = 3

# ---- 2026-10-01 draft rules: one ability pick = about 1 Health ----
# Every Defense one lower than the Level's Skill tier (the other half of
# option 1's baseline trim, alongside Health above).
ENEMY_DEFENSE_SHIFT = -1
# Upgrade costs (UPGRADES_BY_LEVEL above is the allotment). Armor is
# priced from Light, the free baseline. Unspent Upgrades become +1 Health
# each, so every enemy spends its full allotment.
PICK_COST = {
    "Strike (Crippling)": 1, "Strike (Vulnerable)": 1, "Strike (Slowing)": 1,
    "Strike (Frightening)": 1, "Strike (Taunting)": 1, "Poison (Bleeding)": 1,
    "Durable": 2, "Heavy Weapon": 2, "Powerful Weapon": 2, "Powerful Spell": 2,
    "Enhanced Health": 1,  # +1 Health per copy
    # The rest of the catalog (2026-10-25), at ENEMY_ENCOUNTER_DESIGN.md's
    # draft costs ("Draft: the ability catalog at 1 pick = 1 Health").
    # Most are estimates the draft says to test before trusting.
    "Strike (Necrotic)": 1, "Strike (Harrying)": 1, "Strike (Battering)": 1, "Strike (Grappling)": 1,
    "Strike (Devastating)": 2, "Strike (Cleaving)": 2,
    "Poison (Crippling)": 1, "Poison (Necrotic)": 1, "Poison (Slowing)": 1, "Poison (Vulnerable)": 1,
    "Omniguard": 2, "Resilient": 2, "Retribution Aura": 1, "Sturdy": 1,
    "Enhanced Range": 1, "Improved Support": 1, "Enhanced Speed": 1, "Enhanced Reflexes": 1,
    "Shadow Jaunt": 1, "Action (Parting Shot)": 1, "Action (Intimidating)": 1, "Action (Taunting)": 1,
}
ELEMENTS = ("Brilliant", "Fire", "Frost", "Shadow")
OPPOSITE = {"Brilliant": "Shadow", "Shadow": "Brilliant", "Fire": "Frost", "Frost": "Fire"}
for _el in ELEMENTS:
    PICK_COST[f"Resist ({_el})"] = 1
    PICK_COST[f"Attunement ({_el})"] = 1
    PICK_COST[f"Elemental Spell ({_el})"] = 0  # a reflavor
    PICK_COST[f"Elemental Weapon ({_el})"] = 0  # a trade: -1 Damage
ARMOR_PICKS = {"Unarmored": 0, "Light": 0, "Medium": 1, "Heavy": 2}
# At least this share of the Upgrades has to stay as +1 Health (rounded
# up: 2 of 6 at Level 2). Spending everything on effects left a 6-Health
# enemy that dropped before its effects paid off - weaker than its price
# (upgrade_configs.py, "Glass cannon"). Set to 0 to test past it.
HEALTH_FLOOR_FRACTION = 1 / 3

# Codified hand-build rules (2026-10-01). Damage Stat and Resist come from
# the main Action's category, as positions in the Stat spread (0 = High,
# 1 = Mid, 3 = Low): fighters put their best Stat into damage and their
# worst into Resist, casters keep Mid Resist, supports lead with Resist.
CATEGORY_STATS = {"weapon": (0, 3), "spell": (0, 1), "support": (1, 0)}
STRONG_DEFENSE_CHOICES = ("Dodge", "Vital", "Mental", "Vigilant")
# Every codified enemy attacks at this Skill tier. Primary, because
# Secondary came out softer than the hand-built roster (which had about
# half its enemies attacking at Primary); with Primary, Level 2 lands
# back on the hand-built numbers (level_baseline.py, 2026-10-01).
CODIFIED_ATTACK_TIER = "primary"


def action_category(action):
    a = ACTIONS[action]
    if a.get("kind") in ("support", "heal", "nova"):
        return "support"
    if a.get("kind") == "hex" or a["dmg_type"] not in (None, "Physical"):
        return "spell"
    return "weapon"
# The draft archetypes (the spreadsheet's Roles, evened out to roughly
# 3-4 picks each). Defender stands in for a shield, Bruiser for a
# two-hander; every melee enemy's weapon is a light one-hander otherwise.
ROLE_ADDS = {
    # A shield's real numbers. Parry/Dodge +2 and the spreadsheet's Tank
    # (Parry/Dodge +1, Resist +1) both tested worse against Shield Wall.
    "Defender": {"parry": 2},
    "Backup": {"res": 1, "bodily": 1, "mental": 1},
    "Striker": {"dmg": 1},
    "Bruiser": {"dmg": 1, "parry": -1, "dodge": -1},
    "Skirmisher": {"speed": 1, "dodge": 1, "acc": 1},
    "Strategist": {"acc": 1, "dodge": 1, "mental": 1},
}
DEFAULT_STAT_ORDER = ["body", "agility", "essence", "cunning", "mind"]

# sample_pcs.csv's own Baseline Health by Tier - the PC-equivalent
# starting point build_enemy_pcstyle's own `health_bonus` param adds on
# top of, rather than a fresh guess.
HEALTH_BASELINE_BY_LEVEL = {1: 10, 2: 13, 3: 13, 4: 14, 5: 14}

# Weapon-style Damage (base + governing Stat) per Action, matching
# tunables.WEAPON's own shape (party.py's real ranged/spell options) -
# `stat` is always "body" here (this simulator's enemies don't model a
# Cunning-based ranged option yet, unlike Sable's real Light Bow) except
# Spell actions, which draw on Essence the same way party.py's War Magic
# draws on Mind (a caster's own casting Stat, not raw muscle).
# Each Action's attack uses the players' own weapon/spell numbers
# (tunables.WEAPON / weapon_categories.csv, War Magic's 2 + Mind for
# spells): `acc_mod` is the weapon's Accuracy, `dmg_base` + `stat` its
# Damage, `wd` the Weapon Defense it adds to Parry (Defensive Melee is a
# light blade plus a Shield, so it Parries with the Shield's +2).
ACTIONS = {
    "Defensive Melee": {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Offensive Melee": {"acc_mod": 0, "dmg_base": 4, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Light Melee":     {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Heavy Melee":     {"acc_mod": 0, "dmg_base": 5, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Ranged Weapon":   {"acc_mod": 1, "dmg_base": 3, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Melee Spell":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Dodge",       "range": 0},
    "Ranged Spell":    {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Dodge",       "range": 2},
    "Vital Spell":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Bodily",      "range": 2},
    "Shadow Bolt":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Dodge",       "range": 2},
    "Vital Fire":      {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Bodily",      "range": 2},
    # Loadouts for the pruned v3 (designer, 2026-11-04): an enemy in melee
    # is presumed to carry a sword and shield; the toggles are heavy versus
    # light and two-handed versus a shield. The numbers are the PC weapon
    # table's (items.csv), Parry taking the better weapon Defense in hand
    # (the shield's 2).
    "Sword and Shield":       {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Heavy Weapon and Shield": {"acc_mod": 0, "dmg_base": 4, "stat": "body",          "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Light Two-Handed":       {"acc_mod": 1, "dmg_base": 4, "stat": "body_or_cunning", "wd": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Two-Handed Weapon":      {"acc_mod": 0, "dmg_base": 5, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Bow":                    {"acc_mod": 1, "dmg_base": 3, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Heavy Bow":              {"acc_mod": 0, "dmg_base": 4, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    # The monster manual's Mental attacker (2026-11-04, new for the
    # designer's review): a spell like the Vital Spell, at Mental Defense.
    "Mind Spell":             {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Mental",      "range": 2},
    # Non-damaging main Actions (see ENEMY_ENCOUNTER_DESIGN.md's enemy
    # variety standard) - each enemy using one carries a BackupAction.
    "Hex":             {"acc_mod": 0, "dmg_base": 0, "stat": "mind",            "wd": None, "dmg_type": None,       "opp_def": "Mental",      "range": 2,
                        "kind": "hex"},
    "Shield Ally":     {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "support"},
    "Mend Ally":       {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "heal"},
    # The catalog's other main Actions (2026-10-25), at its own numbers:
    # Curse "Target is debuffed +2 times" (Dodge, Range x2), Great Heal
    # "Target ally heals 2 Health" (Range x3), Shielding Nova "Allies in
    # range gain 2 Protected" (Range x3). `stacks` overrides the Level
    # tables below; none of the three is priced against the others yet.
    "Curse":           {"acc_mod": 0, "dmg_base": 0, "stat": "mind",            "wd": None, "dmg_type": None,       "opp_def": "Dodge",       "range": 2,
                        "kind": "hex", "stacks": 2},
    "Great Heal":      {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 3,
                        "kind": "heal", "stacks": 2},
    "Shielding Nova":  {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 3,
                        "kind": "nova", "stacks": 2},
}

# How many stacks a Hex lands on a hit, or how much Protected a Shield
# Ally grants, by Level. Priced to trade roughly evenly with a damaging
# attack: an L1-2 enemy hit nets ~2 Health (~8 value), about what 3
# stacks of Slowed/Frightened/Protected or 2-3 of Crippled are worth.
EFFECT_STACKS = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5}

# Shield Ally / Mend Ally never miss, so they're priced against what an
# attacker's action actually delivers on average (hit chance included),
# not against a hit: see GUARANTEED_STACKS' calibration note in
# balance_weights_notes.md.
GUARANTEED_STACKS = {1: 2, 2: 2, 3: 2, 4: 3, 5: 3}


# ---- Draft base table v2 (2026-11-02, tunables.ENEMY_TABLE = 'v2') ----
# Per the designer: shaped like the original table (one row per Level,
# everything read off it), roughly following a PC's progression with some
# abstraction, so by Level 5 some archetypes reach the PC caps (+10 to an
# attack or Defense Skill Total, 5 in a damage or Resist Stat). Level N is
# for PCs within 25 XP of that Level's schedule (Level 2: 100-150 total).
# Levels 1-3 come from the 2026-11-02 sweep against the measured parties
# (ENEMY_ENCOUNTER_DESIGN.md, "Base stats against the measured party");
# Levels 4-5 are extended to the caps and only checked against stand-ins.
# Only the codified rows (StrongDefense) read it.
#   attack: the attack Skill Total (every codified enemy attacks at it)
#   defense: Skill Totals for the Strong / Parry / every other Defense
#            (Defense = 8 + this, no ENEMY_DEFENSE_SHIFT on top)
#   stats: High / Mid / Low (damage and Resist by the main Action's
#          category, CATEGORY_STATS)
#   damage: on every damaging attack, on top of the weapon or spell
#   health: base Health per Slot (replaces ENEMY_HEALTH_BY_LEVEL)
#   upgrades: Upgrades per Slot (replaces UPGRADES_BY_LEVEL)
# The designer wants fights of about 4-5 rounds (2026-11-02): roughly
# twice v1's Health (base plus Upgrades), paid for with 1 less Damage.
# Attack follows the PC progression to the cap of 10 at Level 5.
ENEMY_TABLE_V2 = {
    1: dict(attack=6, defense=(5, 4, 3), stats=(2, 2, 1), damage=-1, health=8, upgrades=8),
    2: dict(attack=7, defense=(6, 5, 4), stats=(3, 2, 1), damage=-1, health=10, upgrades=10),
    3: dict(attack=8, defense=(7, 6, 5), stats=(3, 3, 1), damage=-1, health=11, upgrades=12),
    4: dict(attack=9, defense=(8, 7, 6), stats=(4, 4, 2), damage=-1, health=12, upgrades=14),
    # Level 5's Health total (base + Upgrades) sits just over Level 4's:
    # the party has mostly capped out by then (2026-11-02, Level 3
    # characters grown to 205-245 combat XP played 6.5-round fights at 17).
    5: dict(attack=10, defense=(9, 8, 7), stats=(4, 4, 2), damage=-1, health=11, upgrades=16),
}
# The v2 kit (2026-11-02, experiments/enemies/kit_check.py): every
# Ability and armor priced at what it's worth in enemy Health against the
# measured parties (1 Upgrade = 1 Health, as the catalog intends), and the
# Roles evened out to about 3-5 Health each. Health moved into Upgrades
# above (same total for an all-Health enemy) so a Level 1 enemy can still
# afford a fairly priced pick.
PICK_COST_V2 = dict(PICK_COST, **{
    "Poison (Bleeding)": 5,       # 1 stack a hit (STRIKE_RIDERS_V2); 2 stacks were worth ~10
    "Retribution Aura": 4,        # melee attackers only (enemy_abilities); every attacker was worth ~20-25
    "Strike (Necrotic)": 3, "Poison (Necrotic)": 3,
    "Strike (Grappling)": 3,
    "Strike (Devastating)": 3,
    "Heavy Weapon": 3, "Powerful Weapon": 3, "Powerful Spell": 3,
    "Enhanced Range": 3, "Enhanced Reflexes": 2,
    "Attunement (Brilliant)": 3, "Attunement (Fire)": 3, "Attunement (Frost)": 3, "Attunement (Shadow)": 3,
    "Resist (Brilliant)": 2, "Resist (Fire)": 2, "Resist (Frost)": 2, "Resist (Shadow)": 2,
    "Durable": 1, "Omniguard": 1, "Resilient": 1,
})
ARMOR_PICKS_V2 = {"Unarmored": 0, "Light": 0, "Medium": 3, "Heavy": 6}
ROLE_ADDS_V2 = {
    "Defender": {"parry": 2, "res": 1},
    "Backup": {"res": 1, "parry": 1, "dodge": 1, "bodily": 1, "mental": 1},
    # +1 Damage is worth about 9-13 enemy Health on its own (enemy hits
    # net about 1.5 past the party's Resist, so it's +60%): 2 Accuracy pays
    # for it. Bruiser is the tough, clumsy hitter (the original table's
    # shape): with -1 Parry/Dodge instead it was Striker minus 0.5 Health.
    "Striker": {"dmg": 1, "acc": -2},
    "Bruiser": {"dmg": 1, "res": 1, "acc": -3},
    "Skirmisher": {"speed": 1, "dodge": 2, "acc": 1},
    "Strategist": {"acc": 2, "mental": 1},
}
# No separate price for attacks aimed at Vital, Mental or Vigilant
# (designer, 2026-11-02): an attack that's harder to defend against gives
# up about 1 Accuracy, priced the same as one that only targets Dodge, and
# the spell Actions already pay it (Accuracy +0 and 2 + Stat, against a
# light weapon's +1 and 3 + Stat, and no Parry), like War Magic.


def _v2():
    return getattr(T, "ENEMY_TABLE", "v1") == "v2"


# ---- v3: enemies built the way PCs are (2026-11-03) ----
# Per the designer (ENEMY_ENCOUNTER_DESIGN.md, "First principles"): the
# same Stats, Skill Totals, weapons and armor as the players, numbers in
# the players' ballpark, archetypes as plain bumps up to the player caps,
# and a spread of Defenses players can read and exploit. Read when
# tunables.ENEMY_TABLE = 'v3', for the codified rows.
#   skill:    the weapon Skill Total: Parry (with a melee weapon) and the
#             Strong Defense, a PC's focus
#   accuracy: the attack's Skill Total, one under `skill` (archetypes that
#             attack well raise it back, designer 2026-11-03)
#   damage:   the damage Stat (a PC's Body/Cunning/Mind for its attack)
#   resist:   the Resist Stat (a PC's Essence), plus armor
#   health:   Health per Slot
# Each stat steps up at its own Levels so two don't jump at once (2026-11-03
# schedule sweeps, ENEMY_ENCOUNTER_DESIGN.md "v3"): damage at 2 and 4,
# Resist at 2 and 4, Health at 2, 3 and 4 (a PC has about 10-11).
ENEMY_TABLE_V3 = {
    1: dict(skill=4, accuracy=3, damage=2, resist=2, health=10),
    2: dict(skill=5, accuracy=4, damage=3, resist=3, health=11),
    3: dict(skill=6, accuracy=5, damage=3, resist=3, health=13),
    4: dict(skill=7, accuracy=6, damage=4, resist=4, health=15),
    5: dict(skill=8, accuracy=7, damage=4, resist=4, health=15),
}
# The first v3 (2026-11-03 morning), one more Skill and Accuracy at every
# Level, with the smaller archetypes (ROLE_ADDS_V3_FIRST). The designer
# trimmed the base and moved the power into the archetypes the same day:
# tunables.V3_VERSION = 1 plays this one, for the recorded numbers.
ENEMY_TABLE_V3_FIRST = {L: dict(r, skill=r["skill"] + 1, accuracy=r["accuracy"] + 1)
                        for L, r in ENEMY_TABLE_V3.items()}
# The original spreadsheet's Roles (Design sheet) as bumps, evened out
# against the measured parties (2026-11-03, kit_check.py under v3: each
# worth about 2-3 enemy Health). Accuracy only ever goes up: Striker pays
# for Damage and Accuracy by being lightly built, Bruiser by being heavy
# and slow. Defender is the spreadsheet's Tank; Skirmisher the roster's
# mobile one.
ROLE_ADDS_V3_FIRST = {
    "Defender": {"res": 1, "parry": 1, "dodge": 1},
    "Striker": {"dmg": 1, "acc": 1, "res": -1},
    "Bruiser": {"dmg": 1, "res": 1, "parry": -1, "dodge": -1, "speed": -1},
    "Strategist": {"acc": 2, "dodge": 1, "mental": 1},
    "Backup": {"res": 1, "dodge": 1, "bodily": 1, "mental": 1},
    "Skirmisher": {"speed": 1, "dodge": 1, "acc": 2},
}
# The pruned v3 (designer, 2026-11-04: "prune back some of the enemy
# baseline power, and then put it in the Ability budget they can spend to
# further specialize"). Offense comes off, not survivability: Damage and
# Accuracy set little of a fight's length, Health, Resist and Defenses
# most of it (ENEMY_ENCOUNTER_DESIGN.md, "What each stat is worth"). The
# Damage Stat and Accuracy are one lower; the budget (V3_PRUNED_ALLOWANCE)
# buys them back (Damage +1, Accuracy +1) or goes into Abilities.
# tunables.V3_VERSION = 3.
ENEMY_TABLE_V3_PRUNED = {L: dict(r, damage=r["damage"] - 1, accuracy=r["accuracy"] - 1)
                         for L, r in {
    1: dict(skill=4, accuracy=3, damage=2, resist=2, health=10),
    2: dict(skill=5, accuracy=4, damage=3, resist=3, health=11),
    3: dict(skill=6, accuracy=5, damage=3, resist=3, health=13),
    4: dict(skill=7, accuracy=6, damage=4, resist=4, health=15),
    5: dict(skill=8, accuracy=7, damage=4, resist=4, health=15),
}.items()}
# In pencil (designer, 2026-11-08): a flatter curve at Levels 2-5. Skill
# (every Defense) -1 at Levels 2-5 and Resist -1 at 2-4, splitting the
# step from 4 to 5; the cut paid back as Health (as Ability points it
# bought offense first and cut fights short); and the Accuracy +1 every
# monster bought from Level 2 is in the table, its 2 points off the
# budget (V3_PRUNED_EXTRA). experiments/enemies/flat_table.py.
V3_FLAT_TABLE = {2: dict(skill=-1, resist=-1, health=3, accuracy=1), 3: dict(skill=-1, resist=-1, health=2, accuracy=1),
                 4: dict(skill=-1, resist=-1, health=1, accuracy=1), 5: dict(skill=-1, health=1, accuracy=1)}
# Then harder hits (designer, 2026-11-08, in pencil): enemy hits landed
# 0.7-1.6 Health after PC Resist, so Damage +2 at every Level, paid in
# Accuracy -1 and Health -3: fewer hits, each two to three times as big
# (experiments/enemies/hard_hits.py).
V3_HARD_HITS = dict(damage=2, accuracy=-1, health=-3)
ENEMY_TABLE_V3_PRUNED = {L: {k: v + V3_FLAT_TABLE.get(L, {}).get(k, 0) + V3_HARD_HITS.get(k, 0) for k, v in r.items()}
                         for L, r in ENEMY_TABLE_V3_PRUNED.items()}
# The hit-target candidate (tunables.V3_HIT_FIT; hit_fit.py's closest fits
# Level by Level, the Resist cap kept): Skill and Resist up, Health set so
# a standard monster averages about 8, and a point less enemy Damage at
# Levels 1 and 3 (their hits landed 3.2-3.5).
V3_HIT_FIT_TABLE = {1: dict(resist=1, health=6, damage=-1), 2: dict(skill=3, resist=2, health=6),
                    3: dict(skill=3, resist=3, health=5, damage=-1), 4: dict(skill=4, resist=2, health=7),
                    5: dict(skill=3, resist=1, health=7)}
if getattr(T, "V3_HIT_FIT", False):
    for _L, _c in V3_HIT_FIT_TABLE.items():
        for _k, _d in _c.items():
            ENEMY_TABLE_V3_PRUNED[_L][_k] = _d if _k == "health" else ENEMY_TABLE_V3_PRUNED[_L][_k] + _d
# Archetypes for the pruned v3: only additions (designer, 2026-11-04: "very
# few things should reduce numbers", heavier armor the one example). Each
# about 2.5-3.5 enemy Health at Level 2 (kit_check.py, V3_PRUNED_ROSTER =
# 'buyback'; results/enemy_stats/v3_pruned_roles*.txt). Level 3 reads
# higher for the damage ones (about 5.5), on a noisier slope. Striker is
# the mobile hitter, Bruiser the tough one; Strategist and Skirmisher came
# down 1 Accuracy each, since Accuracy is worth more on the pruned base.
# "hp" is Health per Slot.
ROLE_ADDS_V3_ADDITIVE = {
    # Resist +1 swapped for Health +3 (designer, 2026-11-05): on Heavy Armor
    # it made walls that physical weapons barely hurt. Health +3 reads about
    # the other archetypes' average (2.6 Health), Resist +1 3.3-4.5.
    "Defender": {"parry": 2, "dodge": 2, "hp": 3},
    "Striker": {"dmg": 1, "speed": 1},
    "Bruiser": {"dmg": 1, "hp": 1, "bodily": 2},
    "Strategist": {"acc": 2, "dodge": 1, "mental": 2, "vigilant": 2},
    "Backup": {"res": 1, "parry": 1, "dodge": 2, "bodily": 2, "mental": 2},
    "Skirmisher": {"speed": 2, "dodge": 2, "acc": 1},
}
# The archetypes on the trimmed base (designer, 2026-11-03: "trim back a
# slight bit of the baseline and add that power budget into the
# archetypes", so enemies feel more distinct; adopted the same day). Each
# is worth about 2.5-4.5 enemy Health against the measured parties
# (kit_check.py, results/enemy_stats/v3_bigroles_values.txt).
ROLE_ADDS_V3 = {
    "Defender": {"res": 1, "parry": 2, "dodge": 2},
    "Striker": {"dmg": 1, "acc": 2, "res": -1},
    # Resist +2 read 7-9 Health and over two extra rounds (2026-11-03): +1,
    # and a hard-to-poison body instead.
    "Bruiser": {"dmg": 1, "res": 1, "bodily": 2, "parry": -1, "dodge": -1, "speed": -1},
    "Strategist": {"acc": 3, "dodge": 1, "mental": 2, "vigilant": 2},
    "Backup": {"res": 1, "parry": 1, "dodge": 2, "bodily": 2, "mental": 2},
    "Skirmisher": {"speed": 2, "dodge": 2, "acc": 2},
}
STAT_CAP, SKILL_CAP = 5, 10
# Draft v3 Ability prices in enemy Health per Slot (2026-11-03): each
# Ability's measured worth on enemies stripped of theirs, per enemy that
# can take it, Levels 2-3 averaged and rounded (kit_check.py --bare,
# results/enemy_stats/v3_abilities*.txt), with Poison (Bleeding) and
# Retribution Aura in their v2 shapes (tunables.V3_KIT_SHAPES). A 0 is an
# Ability the sim reads as about nothing against the sample parties
# (situational, or a debuff the sim may undervalue): left for the
# balance-weights review, not a verdict. Armor is priced from Light.
# Checked with the prices on (results/enemy_stats/v3_abilities_priced*):
# Powerful Spell, Attunement and Enhanced Range came down from 4 to 3
# (Powerful Spell read -2.3 / -1.1 at 4 and +0.8 / +2.3 at 2). Improved
# Support can't be read here: one Warpriest in fourteen enemies, and a
# price change of 1 didn't move it. It stays at 1 until a support-heavy
# test.
ABILITY_HEALTH_V3 = {
    "Strike (Crippling)": 0, "Strike (Vulnerable)": 0, "Strike (Slowing)": 0,
    "Strike (Frightening)": 0, "Strike (Taunting)": 0,
    "Strike (Necrotic)": 1, "Strike (Harrying)": 1, "Strike (Devastating)": 1,
    "Strike (Battering)": 2, "Strike (Cleaving)": 2, "Strike (Grappling)": 3,
    # New 2026-11-08, priced at what reprice.py measured: Area Attack about
    # 4.6 Health at every Level; a Push about nothing (-0.4 to -0.7, as a
    # melee or a ranged rider): the sim has no ledges or hazards to push into.
    "Area Attack": 5, "Strike (Shoving)": 0,
    "Poison (Crippling)": 0, "Poison (Slowing)": 0, "Poison (Vulnerable)": 0,
    "Poison (Necrotic)": 1, "Poison (Bleeding)": 3,
    "Heavy Weapon": 1, "Powerful Weapon": 1, "Powerful Spell": 3,
    "Durable": 1, "Omniguard": 1, "Resilient": 0, "Sturdy": 0, "Shadow Jaunt": 0,
    "Retribution Aura": 2,
    "Enhanced Health": 1, "Enhanced Speed": 1, "Enhanced Reflexes": 2, "Enhanced Range": 3,
    "Improved Support": 1,
    "Action (Parting Shot)": 1, "Action (Intimidating)": 0, "Action (Taunting)": 1,
}
for _el in ELEMENTS:
    ABILITY_HEALTH_V3[f"Resist ({_el})"] = 1
    ABILITY_HEALTH_V3[f"Attunement ({_el})"] = 3
    ABILITY_HEALTH_V3[f"Elemental Spell ({_el})"] = 0
    ABILITY_HEALTH_V3[f"Elemental Weapon ({_el})"] = 0
ARMOR_HEALTH_V3 = {"Unarmored": -1, "Light": 0, "Medium": 1, "Heavy": 2}
# The pruned v3's armor (designer, 2026-11-05): each step measured about 2
# Health on the pruned base (ENEMY_ENCOUNTER_DESIGN.md, "What armor is
# worth on the pruned base"), twice the price above. Heavy went to 6
# (designer, 2026-11-07): fights with a Heavy monster ran 1-3 rounds
# longer and were lost far more often at Levels 1 and 5
# (experiments/enemies/heavy_armor_price.py, one_budget.py).
ARMOR_HEALTH_V3P = {"Unarmored": -2, "Light": 0, "Medium": 2, "Heavy": 6}
# Stat Abilities (2026-11-04, for the pruned v3; any v3 can take them):
# each is that bump, at its measured worth ("What each stat is worth"),
# and can be taken more than once up to the player caps.
# "Dodge +1" (2026-11-06) is the paper-defenses name for Parry and Dodge
# +1: with tunables.V3_PAPER_DEFENSES nothing raises Parry, so both read
# as Dodge alone.
STAT_ABILITIES = {"Damage +1": ("dmg",), "Accuracy +1": ("acc",), "Parry and Dodge +1": ("parry", "dodge"),
                  "Dodge +1": ("dodge",),
                  "Vital/Mental/Vigilant +1": ("bodily", "mental", "vigilant"), "Resist +1": ("res",)}
ABILITY_HEALTH_V3.update({"Damage +1": 4, "Accuracy +1": 2, "Parry and Dodge +1": 1, "Dodge +1": 1,
                          "Vital/Mental/Vigilant +1": 1, "Resist +1": 4})
# The pruned v3's pick rules (designer, 2026-11-04): a few Abilities once
# only, the stats and the on-hit effects as often as you like up to a cap
# (the player caps for stats; 4 stacks of one effect on a hit, "anything
# more than that is probably egregious"). Everything else once.
# The pruned v3's prices (2026-11-04, kit_check.py --bare on the pruned
# base with the stats bought back; results/enemy_stats/v3p_kit*.txt). A
# rider is one stack a pick. The light effects read small a stack (Crippled
# about 0.3 rising to 0.5 by the fourth, Vulnerable 0.2-0.4, Slowed 0.1-
# 0.2; Frightened and Taunted about 0.3 for the first and nothing after),
# so they're half a point a stack ("two stacks a point"). Necrotic and
# Harried read 0.6-0.9 a stack, Necrotic about 0.5, Bleeding 2-2.75. Powerful Weapon and
# Spell are now plain +1 Damage (4.4 and 2.6 on the enemies that use
# them). The loadouts are priced from Sword and Shield.
ABILITY_HEALTH_V3P = dict(ABILITY_HEALTH_V3, **{
    "Strike (Crippling)": 0.5, "Strike (Slowing)": 0.5, "Strike (Vulnerable)": 0.5,
    "Strike (Frightening)": 0.5, "Strike (Taunting)": 0.5,
    "Poison (Crippling)": 0.5, "Poison (Slowing)": 0.5, "Poison (Vulnerable)": 0.5,
    "Powerful Weapon": 4, "Powerful Spell": 3,
    # Re-measured with the Health floor off (v3p_kit2): Necrotic about 0.5
    # a stack, Bleeding 2-2.75.
    "Strike (Necrotic)": 0.5, "Poison (Necrotic)": 0.5, "Poison (Bleeding)": 2.5,
})
# Gear is priced under what it measured (designer, 2026-11-04): at 4 a
# two-hander cost the same as Damage +1 and gave up the shield's Parry
# besides, so it only made sense alongside Damage +1. Players get the same
# kit for a nominal Might, so better kit should be a cheap upgrade for an
# enemy too, even if it comes out a little better on paper. Measured:
# heavy one-hander and shield 1.3, two-handers 3.7-4.5, against Sword and
# Shield.
# Quick pass (v3p_tune.txt): with heavy kit free, every Level lost 4-7
# points of days won (it's a real +1 Damage for -1 Accuracy), so the heavy
# one-hander and heavy bow went back to 1. Two-handers at 2 on every melee
# enemy left days about where they were (fights 0.7 rounds shorter).
LOADOUT_HEALTH_V3P = {"Sword and Shield": 0, "Heavy Weapon and Shield": 1, "Light Two-Handed": 2,
                      "Two-Handed Weapon": 2, "Bow": 0, "Heavy Bow": 1, "Hex": -2}
# Accuracy +1 can be bought again and again, but can't take an enemy's
# Accuracy before its weapon's own above 10, the player's Skill Total cap
# (designer, 2026-11-05; profile() clamps it at SKILL_CAP).
REPEATABLE_V3 = {"Accuracy +1", "Parry and Dodge +1", "Dodge +1", "Vital/Mental/Vigilant +1", "Resist +1",
                 "Enhanced Health", "Enhanced Speed"}
RIDER_CAP_V3 = 4
# Poisons last past the fight, so a Poison effect stops at 2 picks
# (designer, 2026-11-05).
POISON_CAP_V3 = 2
# Hexes trimmed a stack at every Level for the pruned v3 (designer,
# 2026-11-05: "trim down the hexes a bit and move their power budget
# elsewhere"), and the Hex loadout gives 2 points back to spend.
HEX_STACKS_V3P = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4}
# The Weak Defense when a row doesn't name one: what that kind of enemy
# visibly neglects (a fighter's Mental, a caster's Vital, a support's
# Dodge), skipping its Strong Defense.
WEAK_DEFAULT = {"weapon": ("mental", "vigilant"), "spell": ("bodily", "vigilant"), "support": ("dodge", "vigilant")}


def build_enemy_v3(name, level, slots, action, armor, strong_defense, role=None, abilities=(),
                   main_effect=None, backup_action=None, weak_defense=None):
    version = getattr(T, "V3_VERSION", 2)
    t = {1: ENEMY_TABLE_V3_FIRST, 2: ENEMY_TABLE_V3, 3: ENEMY_TABLE_V3_PRUNED}[version][level]
    roles = {1: ROLE_ADDS_V3_FIRST, 2: ROLE_ADDS_V3, 3: ROLE_ADDS_V3_ADDITIVE}[version]
    adds = dict(roles.get(role or "", {}))
    if version == 3 and role == "Defender" and getattr(T, "V3_DEFENDER_PARRY_TO_HEALTH", False):
        # The Defender's +2 Parry moved to Health (designer, 2026-11-06):
        # under the Defense cap a shield already takes its Parry there, so
        # the bump would be paid for and wasted. Priced as Parry and Dodge +1
        # is (1 Health for both, so 1 for the Parry half of two points).
        adds["hp"] = adds.get("hp", 0) + adds.pop("parry", 0) // 2
    if version == 3:
        barred = set(getattr(T, "V3_BIG_BARRED", ())) & set(abilities) if slots >= 2 else set()
        if barred:
            raise ValueError(f"{name}: {', '.join(sorted(barred))} can't be taken by an elite or solo boss")
        for ab in set(abilities):
            n = abilities.count(ab)
            rider = ab.startswith("Strike (") or ab.startswith("Poison (")
            if n > 1 and not rider and ab not in REPEATABLE_V3:
                raise ValueError(f"{name}: {ab} can only be taken once")
            cap = POISON_CAP_V3 if ab.startswith("Poison (") else RIDER_CAP_V3
            if rider and n > cap:
                raise ValueError(f"{name}: {ab} taken {n} times, more than {cap}")
    # Stat Abilities (the pruned v3's buy-backs), as archetype-style bumps.
    for ab, key in STAT_ABILITIES.items():
        for _ in range(abilities.count(ab)):
            for k in key:
                adds[k] = adds.get(k, 0) + 1
    paper = version == 3 and getattr(T, "V3_PAPER_DEFENSES", False)
    if paper:
        # Paper defenses (designer, 2026-11-06): Parry is the Level's Skill
        # plus the main weapon's Defense, nothing else; archetypes and
        # Abilities never raise it.
        adds.pop("parry", None)
    act = ACTIONS[action]
    cat = action_category(action)
    skill = min(SKILL_CAP, t["skill"])
    dmg_stat = min(STAT_CAP, t["damage"] + adds.get("dmg", 0))
    res_stat = min(getattr(T, "V3_RESIST_CAP", None) or STAT_CAP, t["resist"] + adds.get("res", 0))
    gap = T.V3_DEF_GAP
    strong = strong_defense.lower().replace("vital", "bodily")
    weak = (weak_defense or "").lower().replace("vital", "bodily") or next(
        d for d in WEAK_DEFAULT[cat] if d != strong)
    tier = {d: skill - gap for d in ("dodge", "bodily", "mental", "vigilant")}
    tier[strong] = skill
    if weak != strong:
        tier[weak] = skill - 2 * gap

    def defense(d):
        return 8 + min(SKILL_CAP, tier[d] + adds.get(d, 0))
    # Parry, as for a PC: the weapon's Skill plus the weapon's Defense, so
    # only with a melee weapon in hand (the main Action's, or the backup's
    # at the Weak tier, the way a caster's mace is an afterthought).
    if act["wd"] is not None:
        parry = 8 + min(SKILL_CAP, skill + adds.get("parry", 0)) + act["wd"]
    elif backup_action and ACTIONS[backup_action]["wd"] is not None and not paper:
        # (Paper defenses: a caster's or healer's fallback weapon is an
        # afterthought and gives no Parry; it defends with Dodge.)
        parry = 8 + min(SKILL_CAP, skill - 2 * gap + adds.get("parry", 0)) + ACTIONS[backup_action]["wd"]
    else:
        parry = -99
    stat = {k: dmg_stat for k in ("body", "cunning", "mind", "agility", "body_or_cunning")}
    stat["essence"] = res_stat

    def profile(action_name):
        a = ACTIONS[action_name]
        main = action_name == action
        sk = t["accuracy"] if main else t["accuracy"] - 2 * gap
        return dict(action=action_name, accuracy=min(SKILL_CAP, sk + adds.get("acc", 0)) + a["acc_mod"],
                    attack_damage=a["dmg_base"] + stat[a["stat"]] if a["dmg_base"] else 0,
                    dmg_type=a["dmg_type"], opp_def=a["opp_def"],
                    attack_range=a["range"] * level + (2 if a["range"] else 0))
    main = profile(action)
    accuracy, attack_damage = main["accuracy"], main["attack_damage"]
    if version == 3 and ("Powerful Weapon" in abilities or "Powerful Spell" in abilities):
        # The pruned v3: plain +1 Damage on that kind of attack, no trade
        # (the weapon itself is the loadout now); the backup's below.
        want = "Powerful Spell" if action_category(action) == "spell" else "Powerful Weapon"
        if want in abilities and act["dmg_base"]:
            attack_damage += 1
    elif "Powerful Weapon" in abilities or "Heavy Weapon" in abilities:
        attack_damage += 1
        accuracy -= 1
        parry -= 1
    if "Powerful Spell" in abilities and version != 3:
        attack_damage += 1
        parry = -99
    kind = act.get("kind", "attack")
    effect_stacks = act["stacks"] if "stacks" in act else (
        GUARANTEED_STACKS[level] if kind in ("support", "heal") else
        HEX_STACKS_V3P[level] if version == 3 and kind == "hex" else EFFECT_STACKS[level])
    if kind != "attack" and not backup_action:
        raise ValueError(f"{name}: a {action} enemy needs a BackupAction to fall back on")
    backup = profile(backup_action) if backup_action else None
    if version == 3 and backup and backup["attack_damage"]:
        want = "Powerful Spell" if action_category(backup_action) == "spell" else "Powerful Weapon"
        if want in abilities:
            backup["attack_damage"] += 1
    if kind != "attack":
        attack_damage = 0
    base_health = t["health"]
    if getattr(T, "V3_ABILITY_PRICES", False):
        # Every enemy gets V3_ABILITY_ALLOWANCE Health's worth of Abilities
        # and armor on top of the table; what it spends past that comes off
        # its Health, what it leaves is Health. No more than a third of the
        # table's Health can go (v2's lesson: a glass cannon drops before
        # its effects pay).
        prices = ABILITY_HEALTH_V3P if version == 3 else ABILITY_HEALTH_V3
        cost = sum(prices[a] for a in abilities) + (ARMOR_HEALTH_V3P if version == 3 else ARMOR_HEALTH_V3)[armor]
        if version == 3:
            cost += LOADOUT_HEALTH_V3P.get(action, 0)
        allowance = (T.V3_PRUNED_ALLOWANCE + getattr(T, "V3_PRUNED_EXTRA", {}).get(level, 0)
                     if version == 3 else T.V3_ABILITY_ALLOWANCE)
        # A big enemy's budget scales (V3_SLOT_BUDGET, 2026-11-06 test): k
        # times the points, each costing 1/k of its Health per point, so an
        # enemy that spends nothing keeps the Health it had.
        k = T.V3_SLOT_BUDGET.get(slots, 1) if version == 3 else 1
        base_health += (allowance * k - cost) / k
        if version == 3 and getattr(T, "V3_ONE_BUDGET", False):
            if cost > allowance * k:
                raise ValueError(f"{name}: Abilities, loadout and armor cost {cost} of its {allowance * k} points")
        elif base_health < max(1, math.ceil(t["health"] * getattr(T, "V3_HEALTH_FLOOR", 2 / 3))):
            raise ValueError(f"{name}: Abilities and armor cost {cost} Health, more than a third of its {t['health']}")

    def cap_def(value):
        # The Defense cap (designer, 2026-11-06), like Accuracy's: no Defense
        # above 8 + the Level's Skill + V3_DEFENSE_CAP before gear; armor's
        # Dodge penalty goes on after. Archetype bumps and stat picks stack up
        # to it, not past it. Parry is checked with its weapon in: under
        # V3_PAPER_DEFENSES it is Skill plus weapon and never reaches it.
        cap = getattr(T, "V3_DEFENSE_CAP", None)
        if version != 3 or cap is None or value <= 0:
            return value
        return min(value, 8 + min(SKILL_CAP, t["skill"]) + cap)
    # A solo boss (4 Slots) in the pruned v3 has V3_SOLO_HEALTH times a
    # standard enemy's Health (designer, 2026-11-05), not the older 9.
    mult = (T.V3_SOLO_HEALTH if version == 3 and slots == 4 else
            getattr(T, "V3_ELITE_HEALTH", 3) if version == 3 and slots == 2 else
            getattr(T, "V3_MINION_HEALTH", 1 / 3) if version == 3 and slots == 0.5 else T.SLOT_MULTIPLIER[slots])
    health = math.ceil((base_health + adds.get("hp", 0)) * mult - 1e-9) + abilities.count("Enhanced Health")
    enemy = dict(name=name, level=level, slots=slots, role=role or "None", action=action,
                 kind=kind, main_effect=main_effect or {"support": "Protected", "heal": "Health",
                                                        "nova": "Protected"}.get(kind),
                 effect_stacks=effect_stacks, backup=backup, stats=stat,
                 accuracy=accuracy, attack_damage=attack_damage, dmg_type=act["dmg_type"],
                 opp_def=act["opp_def"], attack_range=main["attack_range"],
                 parry=cap_def(parry), dodge=cap_def(defense("dodge")) + T.ARMOR[armor]["dodge"],
                 bodily=cap_def(defense("bodily")), mental=cap_def(defense("mental")),
                 vigilant=cap_def(defense("vigilant")),
                 physres=res_stat + T.ARMOR[armor]["physres"], elemres=res_stat,
                 health=health, max_health=health,
                 speed=math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"] + adds.get("speed", 0),
                 reflex=2 + level, ability_budget=0, ability_cost=0, abilities=list(abilities),
                 protected=0, armor=armor, weak_defense=weak)
    _apply_catalog(enemy, abilities)
    return enemy


def build_enemy_pcstyle(name, level, slots, action, armor="Light",
                         defense_tiers=None, attack_tier="secondary",
                         health_bonus=0, defense_adj=0, accuracy_adj=0,
                         damage_adj=0, resist_adj=0, abilities=(), main_effect=None, backup_action=None,
                         stat_order=None, role=None, strong_defense=None, weak_defense=None):
    """`defense_adj`/`accuracy_adj`/`damage_adj`/`resist_adj`: flat,
    across-the-board sensitivity-testing knobs - NOT a per-archetype
    Ability or a per-build design choice, just a uniform nudge to
    every enemy this function builds, for isolating "what does +1 base
    Defense alone do" from the four real formulas above one at a time
    (health_bonus is the same idea, already present). Keep these at 0
    once a real archetype is settled on - the tiers/action/stat choices
    above are the actual build; these four are a dial for exploring
    around that build, not part of it."""
    if strong_defense and getattr(T, "ENEMY_TABLE", "v1") == "v3":
        return build_enemy_v3(name, level, slots, action, armor, strong_defense, role=role,
                              abilities=abilities, main_effect=main_effect, backup_action=backup_action,
                              weak_defense=weak_defense)
    tiers = SKILL_TOTAL_BY_LEVEL[level]
    act = ACTIONS[action]
    if strong_defense:
        # The codified hand-build rules (GM_GUIDE_NOTES.md, "Enemy stat
        # blocks by hand"): no per-enemy judgment calls. Attack is always
        # the Secondary tier; Parry is always Secondary and every other
        # Defense Poor, except the one Strong Defense, which is Primary;
        # Damage Stat and Resist come from the main Action's category.
        if strong_defense not in STRONG_DEFENSE_CHOICES:
            raise ValueError(f"{name}: Strong Defense must be one of {STRONG_DEFENSE_CHOICES}")
        attack_tier = CODIFIED_ATTACK_TIER
        defense_tiers = {"parry": "secondary", strong_defense.lower().replace("vital", "bodily"): "primary"}
        spread = PC_STAT_SPREAD_BY_LEVEL[max(0, level - ENEMY_STAT_LAG)]
        dmg_col, res_col = CATEGORY_STATS[action_category(action)]
        dmg_val, res_val = spread[dmg_col], spread[res_col]
        if _v2():
            hml = dict(zip((0, 1, 3), ENEMY_TABLE_V2[level]["stats"]))
            dmg_val, res_val = hml[dmg_col], hml[res_col]
        stat = {k: dmg_val for k in ("body", "cunning", "mind", "agility", "body_or_cunning")}
        stat["essence"] = res_val
    else:
        order = [x.strip().lower() for x in (stat_order or DEFAULT_STAT_ORDER)]
        stat = dict(zip(order, PC_STAT_SPREAD_BY_LEVEL[max(0, level - ENEMY_STAT_LAG)]))
        stat["body_or_cunning"] = max(stat["body"], stat["cunning"])
    defense_tiers = defense_tiers or {}

    def_tiers = SKILL_TOTAL_BY_LEVEL[max(1, level - ENEMY_DEFENSE_LAG)] if ENEMY_DEFENSE_LAG else tiers
    if ENEMY_DEFENSE_LAG and level - ENEMY_DEFENSE_LAG < 1:
        # Below Level 1: one less than Level 1's tiers, same step size.
        def_tiers = {k: v - 1 for k, v in SKILL_TOTAL_BY_LEVEL[1].items()}

    adds = (ROLE_ADDS_V2 if strong_defense and _v2() else ROLE_ADDS).get(role or "", {})

    def def_total(category):
        tier = defense_tiers.get(category, "poor")
        if strong_defense and _v2():
            v2 = dict(zip(("primary", "secondary", "poor"), ENEMY_TABLE_V2[level]["defense"]))
            return 8 + v2[tier] + defense_adj + adds.get(category, 0)
        return 8 + def_tiers[tier] + defense_adj + ENEMY_DEFENSE_SHIFT + adds.get(category, 0)

    def attack_total(tier):
        if strong_defense and _v2():
            return ENEMY_TABLE_V2[level]["attack"]
        return tiers[tier]

    v2_damage = ENEMY_TABLE_V2[level]["damage"] if strong_defense and _v2() else 0


    # Accuracy is a plain Skill Total (no +8 - that's Defense's own
    # baseline, per party.py's real attack-roll formula), plus the
    # Action's small weapon-proficiency bonus, same shape as
    # tunables.WEAPON's own `accuracy` field.
    accuracy = attack_total(attack_tier) + act["acc_mod"] + accuracy_adj + adds.get("acc", 0)
    attack_damage = act["dmg_base"] + stat[act["stat"]] + damage_adj + ENEMY_DAMAGE_BONUS + adds.get("dmg", 0) + v2_damage
    dmg_type = act["dmg_type"]
    opp_def = act["opp_def"]
    attack_range = act["range"] * level + (2 if act["range"] else 0)

    parry = def_total("parry") + (act["wd"] or 0)
    dodge = def_total("dodge") + T.ARMOR[armor]["dodge"]
    bodily = def_total("bodily")
    mental = def_total("mental")
    vigilant = def_total("vigilant")  # Feint's target - see ENEMY_ENCOUNTER_DESIGN.md's Defense tiering section

    # Resist - Essence alone (party.py: "Resist starts equal to your
    # Essence"), completely decoupled from attack_damage above, unlike
    # enemy_builder.py's shared DMG_RESIST curve.
    physres = stat["essence"] + T.ARMOR[armor]["physres"] + resist_adj + adds.get("res", 0)
    elemres = stat["essence"] + resist_adj + adds.get("res", 0)

    if armor == "Heavy" and level < HEAVY_ARMOR_MIN_LEVEL:
        raise ValueError(f"{name}: Heavy Armor is Level {HEAVY_ARMOR_MIN_LEVEL}+ only")
    base_health = ENEMY_HEALTH_BASE if ENEMY_HEALTH_BASE is not None else ENEMY_HEALTH_BY_LEVEL[level]
    if strong_defense and _v2():
        base_health = ENEMY_TABLE_V2[level]["health"]
    health = math.ceil((base_health + health_bonus) * T.SLOT_MULTIPLIER[slots])
    speed = math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"] + adds.get("speed", 0)
    reflex = 2 + level

    # Same Ability-budget formula/check as enemy_builder.build_enemy -
    # this builder skips the synthetic Level curve for Accuracy/Damage/
    # Resist/Defense, but the Ability catalog itself (and its budget)
    # isn't part of that curve, so there's no reason to reinvent it.
    # Upgrades scale by Encounter Slots the same way Health does (1/3 for
    # a half-slot minion, x3 for a 2-slot boss), rounded up like Health.
    # At these allotments a pair of minions still gets fewer Upgrades than
    # the one full enemy they stand in for (Level 2: 2 x 2 = 4 against 6).
    kit_v2 = bool(strong_defense and _v2())
    upgrades = ENEMY_TABLE_V2[level]["upgrades"] if kit_v2 else UPGRADES_BY_LEVEL[level]
    cost, armor_cost = (PICK_COST_V2, ARMOR_PICKS_V2) if kit_v2 else (PICK_COST, ARMOR_PICKS)
    picks = math.ceil(upgrades * T.SLOT_MULTIPLIER[slots])
    picks_used = sum(cost[a] for a in abilities) + armor_cost[armor]
    if picks_used > picks:
        raise ValueError(f"{name}: abilities and armor cost {picks_used} Upgrades, only {picks} available")
    health_floor = math.ceil(picks * HEALTH_FLOOR_FRACTION)
    if picks - picks_used < health_floor:
        raise ValueError(f"{name}: {picks_used} of {picks} Upgrades on effects leaves fewer than {health_floor} for Health")
    ability_budget, ability_cost = picks * 5, picks_used * 5  # in points, for older scripts' printouts

    # Enhanced Health copies, plus every unspent Upgrade, at +1 Health each.
    # Applied after the slot multiplier, so a minion's leftover picks
    # still count in full.
    health += abilities.count("Enhanced Health") + (picks - picks_used)
    if "Powerful Weapon" in abilities or "Heavy Weapon" in abilities:
        attack_damage += 1
        accuracy -= 1
        parry -= 1
    if "Powerful Spell" in abilities:
        attack_damage += 1
        parry = -99

    def _profile(action_name):
        a = ACTIONS[action_name]
        return dict(action=action_name,
                    accuracy=attack_total(attack_tier) + a["acc_mod"] + accuracy_adj + adds.get("acc", 0),
                    attack_damage=a["dmg_base"] + stat[a["stat"]] + damage_adj + ENEMY_DAMAGE_BONUS + adds.get("dmg", 0)
                    + v2_damage if a["dmg_base"] else 0,
                    dmg_type=a["dmg_type"], opp_def=a["opp_def"],
                    attack_range=a["range"] * level + (2 if a["range"] else 0))

    kind = act.get("kind", "attack")
    if "stacks" in act:
        effect_stacks = act["stacks"]
    elif kind in ("support", "heal"):
        effect_stacks = GUARANTEED_STACKS[level]
    else:
        effect_stacks = EFFECT_STACKS[level]
    if kind != "attack" and not backup_action:
        raise ValueError(f"{name}: a {action} enemy needs a BackupAction to fall back on")
    if kind == "hex" and not main_effect:
        raise ValueError(f"{name}: a Hex enemy needs a MainEffect (the debuff it lands)")
    backup = _profile(backup_action) if backup_action else None
    if kind != "attack":
        attack_damage = 0

    enemy = dict(name=name, level=level, slots=slots, role=role or "None", action=action,
                 kind=kind, main_effect=main_effect or {"support": "Protected", "heal": "Health",
                                                        "nova": "Protected"}.get(kind),
                 effect_stacks=effect_stacks, backup=backup, stats=stat,
                 accuracy=accuracy, attack_damage=attack_damage, dmg_type=dmg_type,
                 opp_def=opp_def, attack_range=attack_range,
                 parry=parry, dodge=dodge, bodily=bodily, mental=mental, vigilant=vigilant,
                 physres=physres, elemres=elemres,
                 health=health, max_health=health, speed=speed, reflex=reflex,
                 ability_budget=ability_budget, ability_cost=ability_cost, abilities=list(abilities),
                 protected=0, armor=armor)
    _apply_catalog(enemy, abilities)
    return enemy


def _apply_catalog(e, abilities):
    """The catalog's build-time numbers (the rest play out in combat_sim):
    Attunement "+4 Resist to that element, -1 Resist to its opposite",
    Resist "+2 Resist to that element alone", Elemental Spell/Weapon
    retypes the attack (Weapon "at -1 Damage"), Enhanced Range "Range x2
    on the enemy's action", Enhanced Reflexes +3, Enhanced Speed +1,
    Improved Support "+50% (round up)" on heals and Protected grants,
    and Strike (Devastating)'s "Damage +1". Per-element Resist sits in
    `resist_by_type`, on top of the one `elemres` pool."""
    for a in abilities:
        if a.startswith("Attunement ("):
            el = a[len("Attunement ("):-1]
            rbt = e.setdefault("resist_by_type", {})
            rbt[el] = rbt.get(el, 0) + 4
            rbt[OPPOSITE[el]] = rbt.get(OPPOSITE[el], 0) - 1
        elif a.startswith("Resist ("):
            el = a[len("Resist ("):-1]
            rbt = e.setdefault("resist_by_type", {})
            rbt[el] = rbt.get(el, 0) + 2
        elif a.startswith("Elemental Spell (") or a.startswith("Elemental Weapon ("):
            el = a[a.index("(") + 1:-1]
            spell = a.startswith("Elemental Spell")
            for prof in (e, e.get("backup")):
                if not prof or not prof.get("attack_damage"):
                    continue
                is_spell = action_category(prof["action"]) == "spell"
                if is_spell == spell:
                    prof["dmg_type"] = el
                    if not spell:
                        prof["attack_damage"] -= 1
        elif a == "Enhanced Range" and e.get("attack_range"):
            e["attack_range"] *= 2
        elif a == "Enhanced Reflexes":
            e["reflex"] += 3
        elif a == "Enhanced Speed":
            e["speed"] += 1
        elif a == "Improved Support" and e["kind"] in ("support", "heal", "nova"):
            e["effect_stacks"] = math.ceil(e["effect_stacks"] * 1.5)
        elif a == "Strike (Devastating)":
            for prof in (e, e.get("backup")):
                if prof and prof.get("attack_damage"):
                    prof["attack_damage"] += 1
