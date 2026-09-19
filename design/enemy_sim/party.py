"""
A deliberately crude stand-in for "a representative party member" at a
given power Tier - built from the real named Stat/Skill breakdown in
tunables.py, not one flat number. Still simplified: all 4 party members
are identical (no distinct roles), no Techniques or items layered on
top, no gear-based Resist bonus (just raw Essence).

Uses PC_SKILLS_COMBAT (the smoothed variant), not PC_SKILLS directly -
see tunables.py's comment on why: PC_SKILLS' real Tier-4 capstone spike
would make enemy calibration swing wildly depending on whether a fight
lands before or after it.

Exposes every Defense category an enemy might actually target (Parry,
Dodge, Bodily, Mental, Vigilant) plus weapon Damage and Resist, all
computed from real rulebook.md formulas:
- Defense = 8 + [governing Skill Total]
- Weapon Damage = 4 + Body (Heavy 1H Melee formula, weapon_categories.csv)
- Resist = raw Essence, no Skill needed (rulebook.md's Calculated
  Statistics: "Resists... starts equal to your Essence")
"""
import tunables as T


def skill_total(tier, skill):
    stat = T.PC_SKILL_STAT[skill]
    return T.PC_STATS[tier][stat] + T.PC_SKILLS_COMBAT[tier][skill]


def make_party(tier):
    st = T.PC_STATS[tier]
    parry = 8 + skill_total(tier, "Melee")
    dodge = 8 + skill_total(tier, "Acrobatics")
    bodily = 8 + skill_total(tier, "Resilience")
    mental = 8 + skill_total(tier, "Composure")
    vigilant = 8 + skill_total(tier, "Insight")
    damage = 4 + st["Body"]  # Heavy 1H Melee formula
    physres = st["Essence"]  # raw Essence, no Skill needed
    health = T.PC_HEALTH[tier]
    return [dict(name=f"PC{i+1}", parry=parry, dodge=dodge, bodily=bodily, mental=mental,
                 vigilant=vigilant, skill_total=parry - 8,  # Melee's own Skill Total, for the PC's own attack roll
                 damage=damage, physres=physres, health=health, max_health=health) for i in range(4)]


if __name__ == "__main__":
    for t in range(1, 6):
        p = make_party(t)[0]
        print(t, "| Parry", p["parry"], "| Dodge", p["dodge"], "| Bodily", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])
