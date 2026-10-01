"""Checks the Upgrade model (2026-10-01): if one Upgrade is worth about
one Health, every way of spending the same allotment should land close
to spending it all on Health. Every full-size enemy in Frontline, Shield
Wall and Warband gets the same Level 2 loadout (6 Upgrades), keeping
its archetype and Action; minions are left as they are. "All Health
+/-2" give a local scale, so a loadout's gap reads in Health terms.

Loadouts (Light Armor unless the loadout buys Medium; casters keep
Unarmored):
- Roster: each enemy's own loadout.
- All Health: 6 x +1 Health.
- Heavy hitter: Heavy Weapon (weapon users) or Powerful Spell (casters),
  plus 4 Health.
- Rider stack: Crippling, Vulnerable, Bleeding, Slowing, plus 2 Health.
- Glass cannon: Heavy Weapon / Powerful Spell plus all four riders, no
  extra Health.
- Turtle: Medium Armor, Durable, plus 3 Health.
A support enemy (Shield Ally) can't use Heavy Weapon on its main Action,
so it puts those 2 Upgrades into Health instead.

Usage: python3 upgrade_configs.py [trials]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se, enemy_builder_pcstyle as eb
from level_baseline import PARTIES

WEAPON_ACTIONS = {"Light Melee", "Ranged Weapon", "Defensive Melee", "Offensive Melee", "Heavy Melee"}
SPELL_ACTIONS = {"Vital Spell", "Ranged Spell", "Melee Spell", "Shadow Bolt", "Vital Fire"}
RIDERS = ["Strike (Crippling)", "Strike (Vulnerable)", "Poison (Bleeding)", "Strike (Slowing)"]
MIXES = ("Frontline", "Shield Wall", "Warband")


def offense_buy(row):
    if row["Action"] in WEAPON_ACTIONS:
        return ["Heavy Weapon"]
    if row["Action"] in SPELL_ACTIONS:
        return ["Powerful Spell"]
    return []  # support: those 2 Upgrades fall through to Health


LOADOUTS = {
    "Roster": None,
    "All Health": lambda row: ([], None, 0),
    "All Health -2": lambda row: ([], None, -2),
    "All Health +2": lambda row: ([], None, 2),
    "Heavy hitter": lambda row: (offense_buy(row), None, 0),
    "Rider stack": lambda row: (RIDERS, None, 0),
    "Glass cannon": lambda row: (offense_buy(row) + RIDERS, None, 0),
    "Turtle": lambda row: (["Durable"], "Medium", 0),
}


def build(names, loadout):
    rows = {r["Name"]: r for r in se._load_rows()}
    enemies = []
    for n in names:
        row = dict(rows[n])
        if loadout and float(row["Slots"]) >= 1:
            abilities, armor, hp = loadout(row)
            row["Abilities"] = "; ".join(abilities)
            row["Armor"] = armor or ("Unarmored" if row["Armor"] == "Unarmored" else "Light")
            row["HealthBonus"] = str(hp)
        enemies.append(se._build_from_row(row))
    return enemies


def run(names, mix, loadout, trials):
    # Glass cannon breaks the Health floor on purpose - it's the loadout
    # that showed the floor was needed.
    eb.HEALTH_FLOOR_FRACTION = 0 if loadout is LOADOUTS["Glass cannon"] else 1 / 3
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp = 0, [], []
    for _ in range(trials):
        r = cs.run_fight(1, 2, movement=True, enemies=build(se.ENCOUNTERS[2][mix], loadout))
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        hp.append(r["party_hp_pct"] if won else 0.0)
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp)


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print("Level 2, every full-size enemy given the loadout. Cells: win% / rounds / expected party Health left")
    scores = {}
    for label, loadout in LOADOUTS.items():
        cells, per = [], []
        for mix in MIXES:
            for pn, names in PARTIES.items():
                w, r, h = run([n + " (L2)" for n in names], mix, loadout, trials)
                cells.append(f"{pn}/{mix[:5]} {w:3.0f}% {r:4.1f}r {h:3.0f}")
                per.append(h)
        scores[label] = st.mean(per)
        print(f"{label:14} avg {scores[label]:5.1f} | " + " | ".join(cells), flush=True)
    slope = (scores["All Health -2"] - scores["All Health +2"]) / 4  # party Health % per enemy Health
    print(f"\nAgainst All Health ({scores['All Health']:.1f}), in enemy-Health terms "
          f"(1 Health = {slope:.1f} points of party Health here; positive = stronger than all-Health):")
    for label in LOADOUTS:
        if label.startswith("All Health"):
            continue
        print(f"  {label:14} {(scores['All Health'] - scores[label]) / slope:+5.1f}")
