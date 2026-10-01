"""Prices the hand-build enemy archetypes (GM_GUIDE_NOTES.md, "Enemy stat
blocks by hand") against each other. Each variant applies one archetype's
flat adds to every enemy in a few Level 2 mixes. A Health ladder (every
enemy at -2/+2/+4 Health) gives a common scale, so each archetype reads as
"worth about N Health per enemy".

The measure is the party's expected Health left: its Health left on a win,
times the win rate. Losses count as zero, so it captures both "did they
win" and "what did it cost them".

Usage: python3 archetype_compare.py [trials] [--revised]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se

# Keys: acc, dmg, parry, dodge, vital, mental, res, speed, reflex, health.
ARCHETYPES = {
    "Plain": {},
    # Health ladder, the common scale.
    "Health -2": {"health": -2},
    "Health +2": {"health": 2},
    "Health +4": {"health": 4},
    # The spreadsheet's Roles, as drafted.
    "Defender": {"parry": 1, "dodge": 1, "res": 1},
    "Bruiser": {"dmg": 1, "res": 1, "parry": -1, "dodge": -1},
    "Striker": {"acc": 1, "dmg": 1},
    "Strategist": {"acc": 1, "vital": 1, "mental": 1},
    "Backup": {"parry": 1, "dodge": 1, "vital": 1, "mental": 1},
    # Suggested adjustments and additions.
    "Striker (glass)": {"acc": 1, "dmg": 1, "res": -1},
    "Strategist (Dodge)": {"acc": 1, "dodge": 1, "mental": 1},
    "Backup (Resist)": {"parry": 1, "dodge": 1, "mental": 1, "res": 1},
    "Skirmisher": {"speed": 1, "dodge": 1, "acc": 1, "res": -1},
    "Ambusher": {"reflex": 3, "acc": 1, "parry": -1, "dodge": -1},
}

# Second round, aiming every archetype at roughly Striker's worth (+3):
# Resist off the Defender and Backup (it's the dominant stat, see
# ENEMY_ENCOUNTER_DESIGN.md), Skirmisher without its Resist -1, Ambusher
# cut. Striker and Bruiser stay in as reference points.
REVISED = {
    "Plain": {},
    "Health -2": {"health": -2},
    "Health +2": {"health": 2},
    "Health +4": {"health": 4},
    "Health +6": {"health": 6},
    "Striker": {"acc": 1, "dmg": 1},
    "Bruiser": {"dmg": 1, "res": 1, "parry": -1, "dodge": -1},
    "Defender (shield)": {"parry": 2, "dodge": 2},
    "Skirmisher": {"speed": 1, "dodge": 1, "acc": 1},
    "Backup (+Accuracy)": {"parry": 1, "dodge": 1, "vital": 1, "mental": 1, "acc": 1},
    "Backup (Resist)": {"res": 1, "vital": 1, "mental": 1},
    "Strategist (Dodge)": {"acc": 1, "dodge": 1, "mental": 1},
}

# Horde is left out until the baseline settles (per the designer), so
# these prices sit on the same scale as ability_compare.py's.
MIXES = ("Frontline", "Shield Wall", "Warband")
L2 = lambda xs: [x + " (L2)" for x in xs]
PARTIES = {"A": L2(["Hilde", "Browndog", "Carrick", "Sable"]),
           "B": L2(["Rook", "Jackal", "Wren", "Hanforth"]),
           # Party D attacks Vital and Mental too (Felix's Shugen strikes,
           # Hanforth's Reckoning, Beornhard's War Magic split, Browndog's
           # Challenge), so those Defenses get priced properly.
           "D": L2(["Browndog", "Hanforth", "Felix", "Beornhard"])}


def apply(e, adds):
    for prof in (e, e.get("backup")):
        if not prof:
            continue
        prof["accuracy"] += adds.get("acc", 0)
        if prof.get("attack_damage"):
            prof["attack_damage"] += adds.get("dmg", 0)
    e["parry"] += adds.get("parry", 0)
    e["dodge"] += adds.get("dodge", 0)
    e["bodily"] += adds.get("vital", 0)
    e["mental"] += adds.get("mental", 0)
    e["physres"] += adds.get("res", 0)
    e["elemres"] += adds.get("res", 0)
    e["speed"] += adds.get("speed", 0)
    e["reflex"] += adds.get("reflex", 0)
    e["health"] += adds.get("health", 0)
    e["max_health"] = e["health"]
    return e


def run(names, mix, adds, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp = 0, [], []
    for _ in range(trials):
        enemies = [apply(e, adds) for e in se.build_encounter(se.ENCOUNTERS[2][mix])]
        r = cs.run_fight(1, 2, movement=True, enemies=enemies)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        hp.append(r["party_hp_pct"] if won else 0.0)
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp)


def health_equivalent(score, ladder):
    """Linear interpolation of `score` (expected Health left) on the
    Health ladder's (health_delta, score) points. Harder = lower score =
    more Health-equivalent."""
    pts = sorted(ladder, key=lambda p: p[0])
    for (h0, s0), (h1, s1) in zip(pts, pts[1:]):
        lo, hi = min(s0, s1), max(s0, s1)
        if lo <= score <= hi and s0 != s1:
            return h0 + (score - s0) * (h1 - h0) / (s1 - s0)
    # Outside the ladder: extrapolate off the nearest end segment.
    (h0, s0), (h1, s1) = (pts[0], pts[1]) if score > pts[0][1] else (pts[-2], pts[-1])
    return h0 + (score - s0) * (h1 - h0) / (s1 - s0)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    trials = int(args[0]) if args else 300
    if "--revised" in sys.argv:
        ARCHETYPES = REVISED
    results = {}
    print(f"Level 2 parties vs Level 2 mixes, every enemy given the archetype. {trials} fights per cell.")
    print("Cells: win% / rounds / expected party Health left (losses count as 0)")
    for name, adds in ARCHETYPES.items():
        cells, scores = [], []
        for pn, names in PARTIES.items():
            for mix in MIXES:
                w, r, h = run(names, mix, adds, trials)
                cells.append(f"{pn}/{mix[:4]} {w:3.0f}% {r:4.1f}r {h:3.0f}")
                scores.append(h)
        results[name] = st.mean(scores)
        print(f"{name:20} avg {results[name]:5.1f} | " + " | ".join(cells), flush=True)

    ladder = [(0, results["Plain"])] + [(d, results[f"Health {d:+d}"]) for d in (-2, 2, 4, 6) if f"Health {d:+d}" in results]
    print("\nWorth, in Health per enemy (from the ladder):")
    for name in ARCHETYPES:
        if name.startswith("Health") or name == "Plain":
            continue
        print(f"  {name:20} {health_equivalent(results[name], ladder):+5.1f}")
