"""Horde follow-ups (2026-10-01), all at Level 2 with every party and
half-slot minions at 1/2 Health:

1. Horde with its minions starting in ambush, right next to the party.
2. Horde with a second Ember Caster in place of the Bog Hexer.
3. Both together.
4. A controlled minion test: the hardest mix (Shield Wall) and Frontline,
   each as-is and as a "minion version", where every enemy is split into
   two half-slot copies of itself (same stats and archetype, half-slot
   Health and picks). Everything else is the same. Minion versions also
   run at 1/3 Health, the old ratio, for reference.

Usage: python3 horde_experiments.py [trials]"""
import sys, os, copy, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se, tunables as T
from level_baseline import PARTIES

L2 = lambda xs: [x + " (L2)" for x in xs]


def minion_of(name):
    """A half-slot copy of a named enemy row. Abilities that don't fit the
    smaller pick budget are dropped from the end of the list."""
    row = dict(next(r for r in se._load_rows() if r["Name"] == name))
    row["Slots"] = "0.5"
    abilities = [a.strip() for a in row["Abilities"].split(";") if a.strip()]
    while True:
        row["Abilities"] = "; ".join(abilities)
        try:
            return se._build_from_row(row)
        except ValueError:
            if not abilities:
                raise
            abilities.pop()


def full(names):
    return lambda: se.build_encounter(names)


def minions(names):
    return lambda: [minion_of(n) for n in names for _ in (0, 1)]


def ambush(builder):
    def build():
        es = builder()
        for e in es:
            if e.get("slots") == 0.5:
                e["ambush"] = True
        return es
    return build


H = se.ENCOUNTERS[2]["Horde"]
H2 = [n if n != "Bog Hexer (L2)" else "Ember Caster (L2)" for n in H]
SW, FL = se.ENCOUNTERS[2]["Shield Wall"], se.ENCOUNTERS[2]["Frontline"]
VARIANTS = [
    ("Horde as is", full(H), 0.5),
    ("Horde, minions ambush", ambush(full(H)), 0.5),
    ("Horde, 2nd caster for the Hexer", full(H2), 0.5),
    ("Horde, 2nd caster + ambush", ambush(full(H2)), 0.5),
    ("Shield Wall", full(SW), 0.5),
    ("Shield Wall, minion version (1/2)", minions(SW), 0.5),
    ("Shield Wall, minion version (1/3)", minions(SW), 1 / 3),
    ("Frontline", full(FL), 0.5),
    ("Frontline, minion version (1/2)", minions(FL), 0.5),
    ("Frontline, minion version (1/3)", minions(FL), 1 / 3),
]


def run(names, build, trials):
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    wins, rounds, hp, atk = 0, [], [], []
    for _ in range(trials):
        tr = []
        r = cs.run_fight(1, 2, movement=True, enemies=build(), trace=tr)
        won = r["winner"] == "party"
        wins += won
        rounds.append(r["rounds"])
        if won:
            hp.append(r["party_hp_pct"])
        atk.append(sum(1 for ev in tr if ev.get("side") == "enemy" and ev.get("action") in ("attack", "hex")))
    return 100 * wins / trials, st.mean(rounds), 100 * st.mean(hp) if hp else 0, st.mean(atk)


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print("Level 2. Cells: win% / rounds / party Health left on a win / enemy attacks per fight")
    for label, build, ratio in VARIANTS:
        T.SLOT_MULTIPLIER[0.5] = ratio
        cells = []
        for pn, names in PARTIES.items():
            w, r, h, a = run(L2(names), build, trials)
            cells.append(f"{pn}: {w:3.0f}% {r:4.1f}r {h:3.0f}% {a:4.1f}a")
        print(f"{label:36} " + " | ".join(cells), flush=True)
    T.SLOT_MULTIPLIER[0.5] = 0.5
