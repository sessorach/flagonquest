"""Turn-order Styles priced on ONE carrier in a normal party (2026-10-06).

style_compare.py's four-copy method distorts these: turn order is
relative, so four copies of Seize the Moment move the whole party to the front at
once, which one character never could (melee 308% vs ranged 70%). Here
the Style sits on one PC of Party A. The Health ladder raises every PC
together (stable targeting, see style_compare.py), and one PC's share
of it is a quarter of the slope. Paired seeds, more fights per mix.

Usage: python3 turnorder_single.py [trials per mix] [Style name ...]"""
import sys, os, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, party, sample_enemies as se
from style_compare import PARTY_A, STYLES, HEALTH_VALUE

STYLE_LEVELS = [("Staggering Blows", 1), ("Seize the Moment", 2), ("Lie in Wait", 1),
                ("Command the Tempo", 3), ("Ambush Predator", 3)]
CARRIERS = ["Hilde (L2)", "Sable (L2)", "Carrick (L2)"]


def build(carrier, style, health, tactic=None, party_names=None):
    rows = {r["Name"]: r for r in party._load_rows()}
    pcs = []
    for i, n in enumerate(party_names or PARTY_A, 1):
        row = dict(rows[n])
        kept = [p.strip() for p in (row.get("Passives") or "").split(",") if p.strip() and p.strip() not in STYLES]
        if n == carrier and style:
            kept.append(style)
        if n == carrier and tactic:
            row["Battle Tactic"] = tactic
        row["Passives"] = ", ".join(kept)
        row["Health"] = str(int(row["Health"]) + health)
        pcs.append(party._pc_dict(row, i, 0))
    return pcs


def run(carrier, style, health, trials):
    cs.make_party = lambda t, good_luck=0: build(carrier, style, health)
    scores = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(trials):
            r = cs.run_fight(1, 2, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[2][mix]),
                             seed=100_000 * mi + k)
            scores.append(100 * r["party_hp_pct"] if r["winner"] == "party" else 0.0)
    return st.mean(scores)


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    only = set(sys.argv[2:])
    base = run(CARRIERS[0], None, 0, trials)
    plus2 = run(CARRIERS[0], None, 2, trials)
    per_pc = (plus2 - base) / 2 / 4  # one PC's +1 Health, in party-score points
    print(f"Party A base {base:.1f}, +2 Health each {plus2:.1f}; one PC's +1 Health = {per_pc:.2f} points", flush=True)
    for carrier in CARRIERS:
        for style, level in STYLE_LEVELS:
            if only and style not in only:
                continue
            score = run(carrier, style, 0, trials)
            value = (score - base) / per_pc * HEALTH_VALUE
            print(f"  {carrier:13} {style:18} L{level}: {score:5.1f} -> {value:+5.1f} Value "
                  f"({100 * value / (level * 3.6):.0f}% of {level * 3.6:.1f})", flush=True)
