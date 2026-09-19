"""
Five concrete, one-per-Level sample enemies, built with enemy_builder.py
and tuned (via the per-Level search in combat_sim.py's tuning runs) to
land close to a genuine ~50% on-level win rate against a same-Tier
party - not just picked from the raw Level curve and assumed balanced.
See design/ENEMY_ENCOUNTER_DESIGN.md's "Analysis" section for the
validation grid these produced and what retuning each one needed.

All five now use Light Armor specifically - not an arbitrary pick.
Light is where enemy_builder.py's Armor tiers are anchored to the real
player-facing armor_categories.csv (a Light-armored PC and a Light-
armored enemy read as comparably tough); Unarmored/Medium/Heavy are a
deliberate simplification of that same real system extrapolated around
that anchor, for faster stat-block building (see tunables.py's own
comment on ARMOR). Testing confirmed Unarmored reads as too easy and
Medium/Heavy as a real wall (Physical Resist stacking with the enemy's
own innate Resist can exceed a PC's whole weapon Damage, per
rulebook.md's flat damage-minus-Resist rule) even with PCs now Gambling
smartly to punch through (`combat_sim.pc_gamble_count`) - Medium/Heavy
enemies are a legitimate design option for a deliberately tougher
"elite" fight, just not what a same-Tier 4v4 validates as on-level.

Retuned against the corrected PC baseline in tunables.py (real named
Stat/Skill build, PC_SKILLS_COMBAT variant - see that file's own
comments). No single Role/Defense-tier/Action pattern produced ~50%
across all 5 Levels at once, so each Level below was searched and tuned
individually rather than reusing one formula.

These are simulator fixtures for now, not a finished in-game roster -
expect a real "Example Enemies" design doc to supersede this once the
PC/enemy baselines in tunables.py are locked down further.
"""
from enemy_builder import build_enemy


def make_enemy(level):
    if level == 1:
        e = build_enemy("Marsh Viper Scout", 1, 1, "Striker", "Bodily", "Parry/Dodge", "Offensive Melee", "Light")
        e['battle_tactic'] = 'Hit Whatever'; e['fighting_style'] = 'Flurry'
    elif level == 2:
        e = build_enemy("Ironbranch Skirmisher", 2, 1, "Bruiser", "Parry/Dodge", "Mental", "Ranged Spell", "Light")
        e['battle_tactic'] = 'Hit Whatever'; e['fighting_style'] = 'Flurry'
    elif level == 3:
        e = build_enemy("Ironbranch Warden", 3, 1, "Bruiser", "Bodily", "Mental", "Ranged Weapon", "Light")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Guarded'
    elif level == 4:
        e = build_enemy("Deadbough Priest", 4, 1, "None", "Bodily", "Mental", "Melee Spell", "Light")
        e['battle_tactic'] = 'Assassin'; e['fighting_style'] = 'Flurry'
    elif level == 5:
        e = build_enemy("Deep Coven Matriarch", 5, 1, "Striker", "Mental", "Bodily", "Ranged Spell", "Light")
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
