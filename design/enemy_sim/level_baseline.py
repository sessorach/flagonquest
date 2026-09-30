"""How the Level 1 and Level 2 baselines look: every sample party against
every current mix (sample_enemies.CURRENT_MIXES) at its own Level, with
enemy Health per ENEMY_HEALTH_BY_LEVEL, plus alternatives. Target, per
the designer: the party wins most or all fights, spends resources
(Health left well under full), and fights last about 5 rounds.

Usage: python3 level_baseline.py [trials] [--enemy-damage N] [--defense-lag] [--current-only]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se, enemy_builder_pcstyle as eb

PARTIES = {"A": ["Hilde", "Browndog", "Carrick", "Sable"], "B": ["Rook", "Jackal", "Wren", "Hanforth"],
           "C": ["Hilde", "Browndog", "Beornhard", "Hanforth"], "D": ["Browndog", "Hanforth", "Felix", "Beornhard"]}


def run(names, level, mix, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp, attacks = 0, [], [], []
    for _ in range(trials):
        tr = []
        r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]), trace=tr)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        if won:
            hp.append(r["party_hp_pct"])
        attacks.append(sum(1 for ev in tr if ev.get("side") == "enemy" and ev.get("action") in ("attack", "hex")))
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp) if hp else 0, st.mean(attacks)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    trials = int(args[0]) if args else 300
    if "--enemy-damage" in sys.argv:
        eb.ENEMY_DAMAGE_BONUS = int(sys.argv[sys.argv.index("--enemy-damage") + 1])
        args = [a for a in args if a != str(eb.ENEMY_DAMAGE_BONUS)]
        trials = int(args[0]) if args else 300
        print(f"Enemy damage bonus: +{eb.ENEMY_DAMAGE_BONUS}")
    if "--defense-lag" in sys.argv:
        eb.ENEMY_DEFENSE_LAG = 1
        print("Enemy Defenses one Level behind")
    print(f"Fighting Styles: {'on' if se.FIGHTING_STYLES_ENABLED else 'off'}")
    print("Cells: win% / rounds / party Health left on a win / enemy attacks per fight")
    only = "--current-only" in sys.argv
    for level, healths in ((1, (8, 10)), (2, (10, 12))):
        if only:
            healths = (eb.ENEMY_HEALTH_BY_LEVEL[level],)
        for h in healths:
            eb.ENEMY_HEALTH_BASE = h
            print(f"\nLevel {level} parties vs Level {level} mixes, enemy Health {h}"
                  + (" (current)" if eb.ENEMY_HEALTH_BY_LEVEL[level] == h else ""))
            for pn, names in PARTIES.items():
                names = names if level == 1 else [n + " (L2)" for n in names]
                cells = []
                for mix in se.CURRENT_MIXES:
                    w, r, hpl, a = run(names, level, mix, trials)
                    cells.append(f"{mix[:5]:5} {w:3.0f}% {r:4.1f}r {hpl:3.0f}% {a:4.1f}a")
                print(f"  {pn}: " + " | ".join(cells), flush=True)
    eb.ENEMY_HEALTH_BASE = None
