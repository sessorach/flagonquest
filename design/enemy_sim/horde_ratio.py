"""Minion Health ratio check (2026-10-01): Horde at Levels 1-2 with a
half-slot enemy's Health at 1/3, 0.4 or 1/2 of a full enemy's. The
designer's intuition is 1/3 for twice the bodies, possibly up to
1/2 if minions drop too easily. Also counts minion attacks per fight,
since "removed before they matter" is the question.

Usage: python3 horde_ratio.py [trials]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se, tunables as T
from level_baseline import PARTIES


def run(names, level, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp, minion_atk, other_atk = 0, [], [], [], []
    for _ in range(trials):
        tr = []
        enemies = se.build_encounter(se.ENCOUNTERS[level]["Horde"])
        minions = {e["name"] for e in enemies if e.get("slots") == 0.5}
        r = cs.run_fight(1, level, movement=True, enemies=enemies, trace=tr)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        if won:
            hp.append(r["party_hp_pct"])
        atks = [ev for ev in tr if ev.get("side") == "enemy" and ev.get("action") in ("attack", "hex")]
        minion_atk.append(sum(1 for ev in atks if ev["unit"].rstrip("0123456789 ") in minions or ev["unit"] in minions))
        other_atk.append(len(atks) - minion_atk[-1])
    return (100 * wins / trials, st.mean(rounds), 100 * st.mean(hp) if hp else 0,
            st.mean(minion_atk), st.mean(other_atk))


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print("Horde: win% / rounds / party Health left on a win / minion attacks + other enemy attacks per fight")
    for ratio, label in ((1 / 3, "1/3"), (0.4, "0.4"), (0.5, "1/2")):
        T.SLOT_MULTIPLIER[0.5] = ratio
        for level in (1, 2):
            hpmin = se.get_enemy(se.ENCOUNTERS[level]["Horde"][0])["health"]
            cells = []
            for pn, names in PARTIES.items():
                names = names if level == 1 else [n + " (L2)" for n in names]
                w, r, h, ma, oa = run(names, level, trials)
                cells.append(f"{pn}: {w:3.0f}% {r:4.1f}r {h:3.0f}% {ma:4.1f}+{oa:4.1f}a")
            print(f"ratio {label}, Level {level} (minion Health {hpmin}): " + " | ".join(cells), flush=True)
    T.SLOT_MULTIPLIER[0.5] = 1 / 3
