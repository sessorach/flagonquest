"""
Five concrete, one-per-Level sample enemies, built with enemy_builder.py
and tuned (via the search in combat_sim.py's tuning runs) to land close
to a genuine ~50% on-level win rate against a same-Tier party - not just
picked from the raw Level curve and assumed balanced. See design/
ENEMY_ENCOUNTER_DESIGN.md's "Analysis" section for the validation grid
these produced and what retuning each one needed.

These are simulator fixtures for now, not a finished in-game roster -
expect a real "Example Enemies" design doc to supersede this once the
PC/enemy baselines in tunables.py are locked down further.
"""
from enemy_builder import build_enemy


def make_enemy(level):
    if level == 1:
        e = build_enemy("Marsh Viper Scout", 1, 1, "Striker", "Parry/Dodge", "Bodily", "Offensive Melee", "Light")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Skirmisher'
    elif level == 2:
        e = build_enemy("Ironbranch Skirmisher", 2, 1, "Striker", "Parry/Dodge", "Mental", "Offensive Melee", "Light")
        e['battle_tactic'] = 'Hit Whatever'; e['fighting_style'] = 'Flurry'
    elif level == 3:
        e = build_enemy("Ironbranch Warden", 3, 1, "Defensive", "Parry/Dodge", "Bodily", "Offensive Melee", "Light")
        e['battle_tactic'] = 'Hold the Line'; e['fighting_style'] = 'Guarded'
    elif level == 4:
        e = build_enemy("Deadbough Priest", 4, 1, "Tank", "Mental", "Bodily", "Ranged Spell", "Medium")
        e['battle_tactic'] = 'Vanguard'; e['fighting_style'] = 'Guarded'
    elif level == 5:
        e = build_enemy("Deep Coven Matriarch", 5, 1, "Tank", "Mental", "Bodily", "Ranged Spell", "Light",
                         ability_dmg_bonus=1)
        e['battle_tactic'] = 'Vanguard'; e['fighting_style'] = 'Flurry'
    else:
        raise ValueError(level)
    return e


if __name__ == "__main__":
    for lvl in range(1, 6):
        e = make_enemy(lvl)
        print(lvl, e['name'], '|', e['role'], '|', e['battle_tactic'], '|', e['fighting_style'],
              '| Acc', e['accuracy'], '| Dmg', e['attack_damage'], e['dmg_type'],
              '| Parry', e['parry'], 'Mental', e['mental'], '| PhysRes', e['physres'], '| HP', e['health'])
