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

**Four independent Defense tiers** (`defense_tiers={"parry":..., "dodge":
..., "bodily":..., "mental":...}`, each "primary"/"secondary"/"poor")
replace enemy_builder.py's PrimaryDef/SecondaryDef pair (which bundles
Parry and Dodge into one "Parry/Dodge" category, moving together always) -
a real PC's Melee (Parry) and Acrobatics (Dodge) are separate Skills that
can be raised completely independently (rulebook.md never bundles them),
so this gives the same variety a real character sheet would have instead
of an invented "+2/+1" bonus tacked onto a flat baseline. Leaving a
Defense out of the dict defaults it to "poor" - a genuine weak point, same
as a Skill a PC never invested in.
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
ACTIONS = {
    "Defensive Melee": {"acc_mod": 1, "dmg_base": 3, "stat": "body",    "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Offensive Melee":  {"acc_mod": 0, "dmg_base": 4, "stat": "body",    "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Ranged Weapon":    {"acc_mod": 1, "dmg_base": 3, "stat": "body",    "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Melee Spell":      {"acc_mod": 0, "dmg_base": 2, "stat": "essence", "dmg_type": "Fire",     "opp_def": "Dodge",      "range": 0},
    "Ranged Spell":     {"acc_mod": 0, "dmg_base": 1, "stat": "essence", "dmg_type": "Fire",     "opp_def": "Dodge",      "range": 2},
}


def build_enemy_pcstyle(name, level, slots, action, armor="Light",
                         defense_tiers=None, attack_tier="secondary",
                         health_bonus=0, defense_adj=0, accuracy_adj=0,
                         damage_adj=0, resist_adj=0, abilities=()):
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
    stat = STAT_BASELINE_BY_LEVEL[level]
    defense_tiers = defense_tiers or {}
    act = ACTIONS[action]

    def def_total(category):
        tier = defense_tiers.get(category, "poor")
        return 8 + tiers[tier] + defense_adj

    # Accuracy is a plain Skill Total (no +8 - that's Defense's own
    # baseline, per party.py's real attack-roll formula), plus the
    # Action's small weapon-proficiency bonus, same shape as
    # tunables.WEAPON's own `accuracy` field.
    accuracy = tiers[attack_tier] + act["acc_mod"] + accuracy_adj
    attack_damage = act["dmg_base"] + stat[act["stat"]] + damage_adj
    dmg_type = act["dmg_type"]
    opp_def = act["opp_def"]
    attack_range = act["range"] * level + (2 if act["range"] else 0)

    parry = def_total("parry")
    dodge = def_total("dodge") + T.ARMOR[armor]["dodge"]
    bodily = def_total("bodily")
    mental = def_total("mental")

    # Resist - Essence alone (party.py: "Resist starts equal to your
    # Essence"), completely decoupled from attack_damage above, unlike
    # enemy_builder.py's shared DMG_RESIST curve.
    physres = stat["essence"] + T.ARMOR[armor]["physres"] + resist_adj
    elemres = stat["essence"] + resist_adj

    health = math.ceil((HEALTH_BASELINE_BY_LEVEL[level] + health_bonus) * T.SLOT_MULTIPLIER[slots])
    speed = math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"]
    reflex = 2 + level

    # Same Ability-budget formula/check as enemy_builder.build_enemy -
    # this builder skips the synthetic Level curve for Accuracy/Damage/
    # Resist/Defense, but the Ability catalog itself (and its budget)
    # isn't part of that curve, so there's no reason to reinvent it.
    ability_budget = math.ceil(T.ABILITY_RATE[level] * slots) * 5
    ability_cost = sum(T.ABILITY_COST[a] for a in abilities)
    if ability_cost > ability_budget:
        raise ValueError(f"{name}: abilities cost {ability_cost}, only {ability_budget} available")

    if "Enhanced Health" in abilities:
        health += 3
    if "Powerful Weapon" in abilities:
        attack_damage += 1
        accuracy -= 1
        parry -= 1
    if "Powerful Spell" in abilities:
        attack_damage += 1
        parry = -99

    return dict(name=name, level=level, slots=slots, role="None", action=action,
                accuracy=accuracy, attack_damage=attack_damage, dmg_type=dmg_type,
                opp_def=opp_def, attack_range=attack_range,
                parry=parry, dodge=dodge, bodily=bodily, mental=mental,
                physres=physres, elemres=elemres,
                health=health, max_health=health, speed=speed, reflex=reflex,
                ability_budget=ability_budget, ability_cost=ability_cost, abilities=list(abilities),
                protected=0, armor=armor)
