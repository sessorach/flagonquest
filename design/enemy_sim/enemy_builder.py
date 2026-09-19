"""
Implements the enemy stat-block formulas from archive/flagonquest_
encounter_builder.xlsx (see design/ENEMY_ENCOUNTER_DESIGN.md for the
full write-up). All the actual numbers live in tunables.py - this file
is just the shape of how they combine, and shouldn't need editing when
the baseline curves get retuned.
"""
import math
import tunables as T


def build_enemy(name, level, slots, role, primary_def, secondary_def, action, armor="Light",
                 ability_dmg_bonus=0, ability_parry_delta=0, abilities=()):
    acc_base = T.ACCURACY[level]
    dmg_resist = T.DMG_RESIST[level]
    health = math.ceil(T.HEALTH_BASE[level] * T.SLOT_MULTIPLIER[slots])
    ability_budget = math.ceil(T.ABILITY_RATE[level] * slots) * 5

    ability_cost = sum(T.ABILITY_COST[a] for a in abilities)
    if ability_cost > ability_budget:
        raise ValueError(f"{name}: abilities cost {ability_cost}, only {ability_budget} available")

    role_mod = T.ROLE_MODS[role]
    act = T.ACTIONS[action]
    accuracy = acc_base + role_mod.get("accuracy", 0) + act.get("accuracy", 0)
    attack_damage = dmg_resist + act["damage"] + role_mod.get("damage", 0) + ability_dmg_bonus
    dmg_type = act["dmg_type"]
    opp_def = act["opp_def"]
    attack_range = act.get("range", 0) * level + (2 if act.get("range", 0) else 0)

    # base Defense = Accuracy + 6 (spreadsheet's own baseline) + 1 (flat modifier)
    base_def = acc_base + 6 + 1

    def tier_bonus(cat):
        if cat == primary_def: return 2
        if cat == secondary_def: return 1
        return 0

    parry = base_def + tier_bonus("Parry/Dodge") + role_mod.get("parry", 0) + act.get("parry", 0) + ability_parry_delta
    dodge = base_def + tier_bonus("Parry/Dodge") + role_mod.get("dodge", 0) + T.ARMOR[armor]["dodge"]
    bodily = base_def + tier_bonus("Bodily") + role_mod.get("bodily", 0)
    mental = base_def + tier_bonus("Mental") + role_mod.get("mental", 0)

    resist = dmg_resist + role_mod.get("resist", 0)
    physres = resist + T.ARMOR[armor]["physres"]
    elemres = resist + role_mod.get("elem_all", 0)

    speed = math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"]
    reflex = 2 + level

    # Static abilities (flat stat modifiers) apply immediately; dynamic
    # ones (an on-hit debuff, Durable's per-turn Protected regen) are
    # just recorded on the enemy dict for combat_sim.py's round loop to
    # check - see tunables.ABILITY_COST's own comment for which is which.
    if "Enhanced Health" in abilities:
        health += 3
    if "Powerful Weapon" in abilities:
        attack_damage += 1
        accuracy -= 1
        parry -= 1
    if "Powerful Spell" in abilities:
        attack_damage += 1
        parry = -99  # own Parry effectively unusable, matching the source spreadsheet's convention

    return dict(name=name, level=level, slots=slots, role=role, action=action,
                accuracy=accuracy, attack_damage=attack_damage, dmg_type=dmg_type,
                opp_def=opp_def, attack_range=attack_range,
                parry=parry, dodge=dodge, bodily=bodily, mental=mental,
                physres=physres, elemres=elemres,
                health=health, max_health=health, speed=speed, reflex=reflex,
                ability_budget=ability_budget, ability_cost=ability_cost, abilities=list(abilities),
                protected=0, armor=armor)


if __name__ == "__main__":
    # Cross-check against the live spreadsheet's own worked example
    # (Level 2, 0.5 slots, no Role, Primary=Parry/Dodge, Secondary=Mental,
    # Defensive Melee, Light Armor) - every number below should match:
    # Accuracy(attack roll bonus)=7, Parry=17, Dodge=15, Bodily=13,
    # Mental=14, PhysRes=3, OtherRes=2, Health=3, Damage=5 Physical.
    e = build_enemy("Deadbough Root-Tender", 2, 0.5, "None", "Parry/Dodge", "Mental", "Defensive Melee", "Light")
    for k in ['accuracy', 'attack_damage', 'parry', 'dodge', 'bodily', 'mental', 'physres', 'elemres', 'health']:
        print(k, e[k])
