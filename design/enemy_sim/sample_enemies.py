"""
Five concrete, one-per-Level sample enemies, built with enemy_builder.py
and tuned (via the per-Level search in combat_sim.py's tuning runs) to
land close to a genuine ~50% on-level win rate against a same-Tier
party - not just picked from the raw Level curve and assumed balanced.
See design/ENEMY_ENCOUNTER_DESIGN.md's "Analysis" section for the
validation grid these produced and what retuning each one needed.

Retuned against the corrected PC baseline in tunables.py (real named
Stat/Skill build, PC_SKILLS_COMBAT variant - see that file's own
comments). The previous roster was tuned against an earlier, effectively
min-maxed PC baseline and became badly overtuned once the PC numbers
were corrected to something more realistic (particularly the Essence/
Resist fix) - Levels 2-5 were landing at 0-2% win rate before this pass.
No single Role/Armor/Defense-tier pattern produced ~50% across all 5
Levels at once, so each Level below was searched and tuned individually
rather than reusing one formula.

These are simulator fixtures for now, not a finished in-game roster -
expect a real "Example Enemies" design doc to supersede this once the
PC/enemy baselines in tunables.py are locked down further.
"""
from enemy_builder import build_enemy


def make_enemy(level):
    if level == 1:
        e = build_enemy("Marsh Viper Scout", 1, 1, "Striker", "Bodily", "Parry/Dodge", "Offensive Melee", "Light")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Flurry'
    elif level == 2:
        e = build_enemy("Ironbranch Skirmisher", 2, 1, "Striker", "Mental", "Bodily", "Ranged Weapon", "Medium")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Skirmisher'
    elif level == 3:
        e = build_enemy("Ironbranch Warden", 3, 1, "None", "Mental", "Bodily", "Defensive Melee", "Unarmored")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Guarded'
    elif level == 4:
        e = build_enemy("Deadbough Priest", 4, 1, "Tank", "Bodily", "Mental", "Melee Spell", "Unarmored")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Guarded'
    elif level == 5:
        e = build_enemy("Deep Coven Matriarch", 5, 1, "Strategist", "Mental", "Bodily", "Melee Spell", "Unarmored")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Guarded'
    else:
        raise ValueError(level)
    return e


if __name__ == "__main__":
    for lvl in range(1, 6):
        e = make_enemy(lvl)
        print(lvl, e['name'], '|', e['role'], '|', e['battle_tactic'], '|', e['fighting_style'],
              '| Acc', e['accuracy'], '| Dmg', e['attack_damage'], e['dmg_type'],
              '| Parry', e['parry'], 'Mental', e['mental'], '| PhysRes', e['physres'], '| HP', e['health'])
