"""Prices Styles on the sample PCs (2026-10-01). Each Style goes on one
PC (the carrier) and is measured against that same PC without it, on a
ladder of extra carrier Health (+2/+4). THE TABEL prices 1 Health at 4
Value, so a Style's worth comes out in Value and can be checked against
the Style budget: Level x 3.6 per encounter (Level x 3 with the 1.2x
Style premium; balance.md).

A party of four copies of the carrier, all carrying the Style, against
the four current Level 2 mixes. The measure is the
party's expected Health left (losses count as 0), so it covers both "did
they win" and "what did it cost".

Unpaired runs were too noisy for this (2026-10-01: one PC's +2 Health
read as worse than +0), so every variant now uses the same seeds.

Usage: python3 style_compare.py GROUP [trials]
GROUP: hilde, carrick, browndog, beornhard (or all)"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se

HEALTH_VALUE = 4
STYLE_BUDGET_PER_LEVEL = 3.6
L2 = lambda xs: [x + " (L2)" for x in xs]
PARTY_A = L2(["Hilde", "Browndog", "Carrick", "Sable"])
PARTY_D = L2(["Browndog", "Hanforth", "Felix", "Beornhard"])

# group: (party, carrier, [(Style, its Level)]). The carrier's own Styles
# are stripped for the base, so a Style it already has gets priced too.
GROUPS = {
    "hilde": (PARTY_A, "Hilde (L2)", [("Furious Rage", 2), ("Lawman's Hand", 2)]),
    "carrick": (PARTY_A, "Carrick (L2)", [("Hand of Chaos", 2)]),
    "browndog": (PARTY_A, "Browndog (L2)", [("Inexhaustible Guardian", 2), ("Indomitable Phalanx", 2)]),
    "beornhard": (PARTY_D, "Beornhard (L2)", [("Overchanneling", 2)]),
    # Turn-order Styles (2026-10-06). 'Staggering Blows' is a test-only
    # passive (Stagger once on a hit) checking the per-place weight. These
    # four-copy groups distort turn order; see turnorder_single.py.
    "turnorder_melee": (PARTY_A, "Hilde (L2)", [("Staggering Blows", 1), ("Seize the Moment", 2), ("Lie in Wait", 1),
                                                 ("Command the Tempo", 3), ("Ambush Predator", 3)]),
    "turnorder_ranged": (PARTY_A, "Sable (L2)", [("Staggering Blows", 1), ("Seize the Moment", 2), ("Lie in Wait", 1),
                                                  ("Command the Tempo", 3), ("Ambush Predator", 3)]),
}
STYLES = {"Furious Rage", "Bleeding Strikes", "No Parry", "Plus One Damage", "Lawman's Hand", "Hand of Chaos", "Inexhaustible Guardian",
          "Indomitable Phalanx", "Overchanneling", "Staggering Blows", "Seize the Moment", "Lie in Wait",
          "Command the Tempo", "Ambush Predator"}


def make_party(names, carrier, passives_add=(), health=0):
    rows = {r["Name"]: r for r in party._load_rows()}
    pcs = []
    for i, n in enumerate(names, 1):
        row = dict(rows[n])
        if n == carrier:
            kept = [p.strip() for p in (row.get("Passives") or "").split(",") if p.strip() and p.strip() not in STYLES]
            row["Passives"] = ", ".join(kept + list(passives_add))
            row["Health"] = str(int(row["Health"]) + health)
        pcs.append(party._pc_dict(row, i, 0))
    return pcs


def run(names, carrier, passives_add, health, trials):
    cs.make_party = lambda t, good_luck=0: make_party(names, carrier, passives_add, health)
    scores = []
    # Paired seeds: every variant replays the same fights (same starting
    # gap, initiative, card flips until the Style first changes
    # something), so the comparison isn't swamped by fight-to-fight luck.
    # One PC's Style only moves the party's result by a point or two,
    # about the size of that luck across a few thousand unpaired fights.
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(trials):
            r = cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                             seed=100_000 * mi + k)
            scores.append(100 * r["party_hp_pct"] if r["winner"] == "party" else 0.0)
    return st.mean(scores)


def price(group, trials):
    # Four copies of the carrier, every one carrying the Style. With one
    # carrier in a mixed party, the Style moved results by about as much
    # as fight-to-fight luck, and the Health ladder wasn't even
    # monotonic: one PC's Health changes who Challenge protects, who
    # Assassins chase and who gets healed, so paired fights split apart
    # from turn 1. Four copies give four times the signal, and raising
    # every PC's Health together keeps the targeting order intact.
    _, carrier, styles = GROUPS[group]
    names = [carrier] * 4
    base = run(names, carrier, (), 0, trials)
    plus1 = run(names, carrier, (), 1, trials)
    plus2 = run(names, carrier, (), 2, trials)
    slope = (base - plus2) / 2  # party-Health points per +1 Health on every PC
    print(f"4x {carrier}: base {base:.1f}, +1 Health each {plus1:.1f}, +2 Health each {plus2:.1f} "
          f"(1 Health per PC = {-slope:.2f} points)", flush=True)
    for style, level in styles:
        score = run(names, carrier, (style,), 0, trials)
        health_eq = (score - base) / -slope  # per PC
        value = health_eq * HEALTH_VALUE
        target = level * STYLE_BUDGET_PER_LEVEL
        print(f"  {style:24} L{level}: {score:.1f} -> {health_eq:+.2f} Health = {value:+.1f} Value "
              f"(target {target:.1f}, {100 * value / target:.0f}%)", flush=True)


if __name__ == "__main__":
    group = sys.argv[1] if len(sys.argv) > 1 else "all"
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    for g in (GROUPS if group == "all" else [group]):
        price(g, trials)
