"""Horde with Medium-armored goblins (2026-10-01, per the designer). At
Levels 1-2 a goblin's one pick would buy Medium Armor instead of Strike
(Slowing); Level 3 has room for both. Tested and reverted: it made no
consistent difference (a 3-Health goblin still dies to almost any hit),
and it cost the goblins their Slowing rider. The roster keeps Light
Armor + Slowing; this script builds the Medium version in memory so the
comparison can be rerun. Health is the same either way, since the pick
gets spent both times.

Usage: python3 goblin_armor.py [trials]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se
from level_baseline import PARTIES


def with_medium(enemies):
    """Level 1-2 goblins spend their pick on Medium Armor (Physical
    Resist +1, Dodge -1 over Light) instead of Strike (Slowing)."""
    for e in enemies:
        if e["name"].startswith("Goblin") and e["armor"] == "Light" and e["level"] < 3:
            e["armor"] = "Medium"
            e["physres"] += 1
            e["dodge"] -= 1
            e["abilities"] = [a for a in e["abilities"] if a != "Strike (Slowing)"]
    return enemies


def run(names, level, mutate, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp, gob = 0, [], [], []
    for _ in range(trials):
        tr = []
        r = cs.run_fight(1, level, movement=True, enemies=mutate(se.build_encounter(se.ENCOUNTERS[level]["Horde"])),
                         trace=tr)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        if won:
            hp.append(r["party_hp_pct"])
        gob.append(sum(1 for ev in tr if ev.get("side") == "enemy" and ev.get("action") == "attack"
                       and str(ev.get("unit", "")).startswith("Goblin")))
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp) if hp else 0, st.mean(gob)


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print("Horde. Cells: win% / rounds / party Health left on a win / goblin attacks per fight (all four)")
    for level in (1, 2):
        for label, mutate in (("Light + Slowing (roster)", lambda es: es), ("Medium Armor (tested)", with_medium)):
            cells = []
            for pn, names in PARTIES.items():
                names = names if level == 1 else [n + " (L2)" for n in names]
                w, r, h, g = run(names, level, mutate, trials)
                cells.append(f"{pn}: {w:3.0f}% {r:4.1f}r {h:3.0f}% {g:4.1f}g")
            print(f"Level {level}, goblins {label:25} " + " | ".join(cells), flush=True)
