"""Prices one enemy ability pick (5 points) the same way archetype_compare.py
prices archetypes: the pick goes onto every enemy in the Level 2 Frontline,
Shield Wall and Warband mixes (Horde is left out until the baseline
settles, per the designer), against parties A, B and D. Each result is read
off a Health ladder (every enemy at -2/+2/+4/+6 Health), so a pick reads as
"worth about N Health per enemy".

The pick is added on top of whatever the enemy already has, without the
budget check, since the question is what one more pick is worth. Loadout
upgrades are priced as a pick here, without the Health trade Medium Armor
currently uses on the roster.

Usage: python3 ability_compare.py [trials]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se
from archetype_compare import health_equivalent


def add_ability(name):
    def mod(e):
        e["abilities"] = list(e.get("abilities", [])) + [name]
    return mod


def health(n):
    def mod(e):
        e["health"] += n
        e["max_health"] = e["health"]
    return mod


def heavy_weapon(e):
    # Powerful Weapon: Damage +1, Accuracy -1, Parry -1 (on the damaging
    # attack, the main Action or the backup).
    for prof in (e, e.get("backup")):
        if prof and prof.get("attack_damage"):
            prof["attack_damage"] += 1
            prof["accuracy"] -= 1
    e["parry"] -= 1


def armor_step(physres, dodge, speed):
    def mod(e):
        e["physres"] += physres
        e["dodge"] += dodge
        e["speed"] += speed
    return mod


VARIANTS = {
    "Plain": lambda e: None,
    "Health -2": health(-2),
    "Health +2": health(2),
    "Health +4": health(4),
    "Health +6": health(6),
    "Strike (Crippling)": add_ability("Strike (Crippling)"),
    "Strike (Vulnerable)": add_ability("Strike (Vulnerable)"),
    "Strike (Slowing)": add_ability("Strike (Slowing)"),
    "Strike (Frightening)": add_ability("Strike (Frightening)"),
    "Strike (Taunting)": add_ability("Strike (Taunting)"),
    "Poison (Bleeding)": add_ability("Poison (Bleeding)"),
    "Durable": add_ability("Durable"),
    "Enhanced Health (+3)": health(3),
    "Heavy Weapon": heavy_weapon,
    # One armor step up: Light -> Medium (Physical Resist +1, Dodge -1).
    "Medium Armor (step)": armor_step(1, -1, 0),
}

MIXES = ("Frontline", "Shield Wall", "Warband")
L2 = lambda xs: [x + " (L2)" for x in xs]
PARTIES = {"A": L2(["Hilde", "Browndog", "Carrick", "Sable"]),
           "B": L2(["Rook", "Jackal", "Wren", "Hanforth"]),
           "D": L2(["Browndog", "Hanforth", "Felix", "Beornhard"])}


def run(names, mix, mod, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp = 0, [], []
    for _ in range(trials):
        enemies = se.build_encounter(se.ENCOUNTERS[2][mix])
        for e in enemies:
            mod(e)
        r = cs.run_fight(1, 2, movement=True, enemies=enemies)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        hp.append(r["party_hp_pct"] if won else 0.0)
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp)


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    results = {}
    print(f"One more ability pick on every enemy, Level 2. {trials} fights per cell. Fighting Styles "
          f"{'on' if se.FIGHTING_STYLES_ENABLED else 'off'}.")
    print("Cells: win% / rounds / expected party Health left (losses count as 0)")
    for name, mod in VARIANTS.items():
        cells, scores = [], []
        for pn, names in PARTIES.items():
            for mix in MIXES:
                w, r, h = run(names, mix, mod, trials)
                cells.append(f"{pn}/{mix[:5]} {w:3.0f}% {r:4.1f}r {h:3.0f}")
                scores.append(h)
        results[name] = st.mean(scores)
        print(f"{name:22} avg {results[name]:5.1f} | " + " | ".join(cells), flush=True)

    ladder = [(0, results["Plain"])] + [(d, results[f"Health {d:+d}"]) for d in (-2, 2, 4, 6)]
    print("\nWorth, in Health per enemy (from the ladder):")
    for name in VARIANTS:
        if name.startswith("Health") or name == "Plain":
            continue
        print(f"  {name:22} {health_equivalent(results[name], ladder):+5.1f}")
