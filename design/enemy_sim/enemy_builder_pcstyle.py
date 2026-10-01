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
ENEMY_HEALTH_BY_LEVEL = {1: 7, 2: 9, 3: 11, 4: 13, 5: 15}
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
# Picks per Level per Encounter Slot, rounded up - the spreadsheet's
# ability counts (tunables.ABILITY_RATE: 2/3/4/5/8). Costs from the
# draft table. Armor is priced from Light, the free baseline. Leftover
# picks become +1 Health each, so every enemy spends its full allotment.
PICK_COST = {
    "Strike (Crippling)": 1, "Strike (Vulnerable)": 1, "Strike (Slowing)": 1,
    "Strike (Frightening)": 1, "Strike (Taunting)": 1, "Poison (Bleeding)": 1,
    "Durable": 2, "Heavy Weapon": 2, "Powerful Weapon": 2, "Powerful Spell": 2,
    "Enhanced Health": 1,  # +1 Health per copy
}
ARMOR_PICKS = {"Unarmored": 0, "Light": 0, "Medium": 1, "Heavy": 2}
# The draft archetypes (the spreadsheet's Roles, evened out to roughly
# 3-4 picks each). Defender stands in for a shield, Bruiser for a
# two-hander; every melee enemy's weapon is a light one-hander otherwise.
ROLE_ADDS = {
    "Defender": {"parry": 2, "dodge": 2},
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
    # Non-damaging main Actions (see ENEMY_ENCOUNTER_DESIGN.md's enemy
    # variety standard) - each enemy using one carries a BackupAction.
    "Hex":             {"acc_mod": 0, "dmg_base": 0, "stat": "mind",            "wd": None, "dmg_type": None,       "opp_def": "Mental",      "range": 2,
                        "kind": "hex"},
    "Shield Ally":     {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "support"},
    "Mend Ally":       {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "heal"},
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


def build_enemy_pcstyle(name, level, slots, action, armor="Light",
                         defense_tiers=None, attack_tier="secondary",
                         health_bonus=0, defense_adj=0, accuracy_adj=0,
                         damage_adj=0, resist_adj=0, abilities=(), main_effect=None, backup_action=None,
                         stat_order=None, role=None):
    """`defense_adj`/`accuracy_adj`/`damage_adj`/`resist_adj`: flat,
    across-the-board sensitivity-testing knobs - NOT a per-archetype
    Ability or a per-build design choice, just a uniform nudge to
    every enemy this function builds, for isolating "what does +1 base
    Defense alone do" from the four real formulas above one at a time
    (health_bonus is the same idea, already present). Keep these at 0
    once a real archetype is settled on - the tiers/action/stat choices
    above are the actual build; these four are a dial for exploring
    around that build, not part of it."""
    tiers = SKILL_TOTAL_BY_LEVEL[level]
    order = [x.strip().lower() for x in (stat_order or DEFAULT_STAT_ORDER)]
    stat = dict(zip(order, PC_STAT_SPREAD_BY_LEVEL[max(0, level - ENEMY_STAT_LAG)]))
    stat["body_or_cunning"] = max(stat["body"], stat["cunning"])
    defense_tiers = defense_tiers or {}
    act = ACTIONS[action]

    def_tiers = SKILL_TOTAL_BY_LEVEL[max(1, level - ENEMY_DEFENSE_LAG)] if ENEMY_DEFENSE_LAG else tiers
    if ENEMY_DEFENSE_LAG and level - ENEMY_DEFENSE_LAG < 1:
        # Below Level 1: one less than Level 1's tiers, same step size.
        def_tiers = {k: v - 1 for k, v in SKILL_TOTAL_BY_LEVEL[1].items()}

    adds = ROLE_ADDS.get(role or "", {})

    def def_total(category):
        tier = defense_tiers.get(category, "poor")
        return 8 + def_tiers[tier] + defense_adj + ENEMY_DEFENSE_SHIFT + adds.get(category, 0)

    # Accuracy is a plain Skill Total (no +8 - that's Defense's own
    # baseline, per party.py's real attack-roll formula), plus the
    # Action's small weapon-proficiency bonus, same shape as
    # tunables.WEAPON's own `accuracy` field.
    accuracy = tiers[attack_tier] + act["acc_mod"] + accuracy_adj + adds.get("acc", 0)
    attack_damage = act["dmg_base"] + stat[act["stat"]] + damage_adj + ENEMY_DAMAGE_BONUS + adds.get("dmg", 0)
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
    health = math.ceil((base_health + health_bonus) * T.SLOT_MULTIPLIER[slots])
    speed = math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"] + adds.get("speed", 0)
    reflex = 2 + level

    # Same Ability-budget formula/check as enemy_builder.build_enemy -
    # this builder skips the synthetic Level curve for Accuracy/Damage/
    # Resist/Defense, but the Ability catalog itself (and its budget)
    # isn't part of that curve, so there's no reason to reinvent it.
    picks = math.ceil(T.ABILITY_RATE[level] * slots)
    picks_used = sum(PICK_COST[a] for a in abilities) + ARMOR_PICKS[armor]
    if picks_used > picks:
        raise ValueError(f"{name}: abilities and armor cost {picks_used} picks, only {picks} available")
    ability_budget, ability_cost = picks * 5, picks_used * 5  # in points, for older scripts' printouts

    # Enhanced Health copies, plus every leftover pick, at +1 Health each.
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
                    accuracy=tiers[attack_tier] + a["acc_mod"] + accuracy_adj + adds.get("acc", 0),
                    attack_damage=a["dmg_base"] + stat[a["stat"]] + damage_adj + ENEMY_DAMAGE_BONUS + adds.get("dmg", 0)
                    if a["dmg_base"] else 0,
                    dmg_type=a["dmg_type"], opp_def=a["opp_def"],
                    attack_range=a["range"] * level + (2 if a["range"] else 0))

    kind = act.get("kind", "attack")
    if kind in ("support", "heal"):
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

    return dict(name=name, level=level, slots=slots, role=role or "None", action=action,
                kind=kind, main_effect=main_effect or {"support": "Protected", "heal": "Health"}.get(kind),
                effect_stacks=effect_stacks, backup=backup, stats=stat,
                accuracy=accuracy, attack_damage=attack_damage, dmg_type=dmg_type,
                opp_def=opp_def, attack_range=attack_range,
                parry=parry, dodge=dodge, bodily=bodily, mental=mental, vigilant=vigilant,
                physres=physres, elemres=elemres,
                health=health, max_health=health, speed=speed, reflex=reflex,
                ability_budget=ability_budget, ability_cost=ability_cost, abilities=list(abilities),
                protected=0, armor=armor)
