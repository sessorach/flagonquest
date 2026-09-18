"""
A deliberately crude stand-in for "a representative party member" at a
given power Tier - one Skill Total, one Defense, one Damage, one Resist,
one Health, shared identically by all 4 party members. No real character
sheet, no distinct roles (tank/striker/healer), no Techniques or items.
The numbers themselves live in tunables.py; this file just turns a Tier
into a party of 4 identical PCs using them.
"""
import tunables as T


def make_party(tier):
    skill_total = T.SKILL_TOTAL[tier]
    stat = T.WEAPON_STAT[tier]
    defense = 8 + skill_total
    damage = 4 + stat  # Heavy 1H Melee formula
    physres = stat + 1  # established Fresh-attack Resist placeholder convention: Stat+1 for Physical
    health = T.PC_HEALTH[tier]
    return [dict(name=f"PC{i+1}", skill_total=skill_total, defense=defense,
                 damage=damage, physres=physres, health=health, max_health=health) for i in range(4)]


if __name__ == "__main__":
    for t in range(1, 6):
        p = make_party(t)[0]
        print(t, '| SkillTotal', p['skill_total'], '| Defense', p['defense'],
              '| Damage', p['damage'], '| PhysRes', p['physres'], '| Health', p['health'])
