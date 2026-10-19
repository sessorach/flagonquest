"""Bleeding against Protected, on both sides (2026-10-19).

Per the designer: try Bleeding a few ways, leaning toward half the stacks
ticking off each turn, with Bleeding on the PCs, the enemies or both, with
and without Protected on the side taking it, and with Protected either
letting Bleeding through, stopping its ticks (the glossary as written) or
stopping stacks from going on (once on, they tick regardless). Bleeding
is likely to hit harder against players than for them, so the point is
to see which rules make that worse.

Every rule is run against the same party with no test Bleeding (base),
and four test riders (tunables.PC_TEST_BLEED / ENEMY_TEST_BLEED):

    pc1 / pc2   every PC hit adds 1 / 2 stacks
    en1 / en2   every enemy hit adds 1 / 2 stacks

each with nobody Durable and with Durable (1 Protected at the start of each
turn, up to 4) on the side taking the Bleeding. A PC's leftover Bleeding
ticks out after the fight (tunables.BLEED_RESOLVE_AFTER), so Health left
and "Down, or after" count it. Warband's Skulking Footpads Poison for 2 a
hit in every version, base included.

    python3 bleed_protected.py grid         # Parties A and T
    python3 bleed_protected.py real         # the Bleeding builds (party X)
    python3 bleed_protected.py dose         # dose size 1-8 against +N damage
    python3 bleed_protected.py grid -n 100  # fewer fights per mix"""
import argparse
import math
import os
import statistics as st
import sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T
from turnorder_single import build

RULES = {
    "tick 1, through": {"BLEED_TICK": 1, "BLEED_PROTECTED": 'through'},
    "tick 1, stops ticks": {"BLEED_TICK": 1, "BLEED_PROTECTED": 'ticks'},
    "tick 1, stops gaining": {"BLEED_TICK": 1, "BLEED_PROTECTED": 'apply'},
    "half, through": {"BLEED_TICK": 'half', "BLEED_PROTECTED": 'through'},
    "half, stops ticks": {"BLEED_TICK": 'half', "BLEED_PROTECTED": 'ticks'},
    "half, stops gaining": {"BLEED_TICK": 'half', "BLEED_PROTECTED": 'apply'},
}
SCENARIOS = {
    "base": {},
    "pc1": {"PC_TEST_BLEED": 1},
    "pc2": {"PC_TEST_BLEED": 2},
    "en1": {"ENEMY_TEST_BLEED": 1},
    "en2": {"ENEMY_TEST_BLEED": 2},
}
PARTIES = {
    "A": ["Hilde", "Browndog", "Carrick", "Sable"],
    "T": ["Browndog", "Hanforth", "Sable", "Beornhard"],
    "X base": ["Hilde", "Felix", "Jackal", "Beornhard"],
    "X bleed": ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"],
}
KEYS = ("BLEED_TICK", "BLEED_PROTECTED", "PC_TEST_BLEED", "ENEMY_TEST_BLEED", "TEST_DURABLE", "TEST_DUMP_STACKS")
DEFAULTS = {k: getattr(T, k) for k in KEYS}


def encounter(mix, mult):
    en = se.build_encounter(se.ENCOUNTERS[1][mix])
    for e in en:
        e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
    return en


def fights(make, settings, n, mult=1.0):
    for k, v in {**DEFAULTS, **settings}.items():
        setattr(T, k, v)
    cs.make_party = make
    return [cs.run_fight(1, 1, movement=True, enemies=encounter(mix, mult), seed=100_000 * mi + k)
            for mi, mix in enumerate(se.CURRENT_MIXES) for k in range(n)]


def party_job(job):
    pname, rule, scen, durable, n = job
    names = PARTIES[pname]
    R = fights(lambda t, good_luck=0: party.make_party_from(names, good_luck),
               {**RULES[rule], **SCENARIOS[scen], "TEST_DURABLE": durable}, n)
    m = lambda key: st.mean(float(r.get(key, 0)) for r in R)
    wins = [r['party_hp_pct'] for r in R if r['winner'] == 'party']
    return job[:4], dict(
        rounds=m('rounds'), loses=100 * st.mean(r['winner'] != 'party' for r in R),
        down=100 * m('pc_downed'), down_after=100 * st.mean(bool(r['pc_downed'] or r.get('pc_downed_after')) for r in R),
        hp=100 * st.mean(wins) if wins else 0.0, landed=m('bleed_dealt'),
        taken=m('pc_bleed_taken') + m('pc_bleed_after'), after=m('pc_bleed_after'),
        blocked_e=m('bleed_blocked'), blocked_p=m('pc_bleed_blocked'))


def dose_job(job):
    rule, durable, mult, carrier, test, size, n = job
    R = fights(lambda t, good_luck=0: build(carrier, test, 0, party_names=PARTIES["A"]),
               {**RULES[rule], "TEST_DURABLE": durable, "TEST_DUMP_STACKS": size}, n, mult)
    return job[:6], st.mean(r.get("bleed_dealt", 0) + r.get("plus_one_dealt", 0) for r in R)


def run_grid(parties, n):
    jobs = []
    for p in parties:
        for rule in RULES:
            for scen in SCENARIOS:
                conds = ((None, 'enemies', 'pcs') if scen == "base"
                         else (None, 'enemies') if scen.startswith("pc") else (None, 'pcs'))
                jobs += [(p, rule, scen, d, n) for d in conds]
    with Pool() as pool:
        res = dict(pool.map(party_job, jobs))
    for p in parties:
        for side, cond in (("no Protected", None), ("Durable on whoever's bled", "x")):
            print(f"\n== Party {p}, {side}")
            print("| Rule | Base: rounds / HP left / Down, or after | PCs 1 a hit: rounds / HP / landed | PCs 2 a hit "
                  "| Enemies 1 a hit: HP / Down, or after / taken | Enemies 2 a hit |")
            print("|---|---|---|---|---|---|")
            for rule in RULES:
                cells = []
                base_pc = res[(p, rule, "base", None if cond is None else 'enemies')]
                base_en = res[(p, rule, "base", None if cond is None else 'pcs')]
                # The base cell: no Durable, or rounds with Durable enemies
                # and HP / Down with Durable PCs, what each side compares to.
                cells.append(f"{base_pc['rounds']:.2f} / {base_en['hp']:.1f} / {base_en['down_after']:.0f}%")
                for scen in ("pc1", "pc2"):
                    r = res[(p, rule, scen, None if cond is None else 'enemies')]
                    cells.append(f"{r['rounds'] - base_pc['rounds']:+.2f} / {r['hp'] - base_pc['hp']:+.1f} / "
                                 f"{r['landed']:.2f}" + (f" ({r['blocked_e']:.2f} stopped)" if r['blocked_e'] else ""))
                for scen in ("en1", "en2"):
                    r = res[(p, rule, scen, None if cond is None else 'pcs')]
                    cells.append(f"{r['hp'] - base_en['hp']:+.1f} / {r['down_after'] - base_en['down_after']:+.0f} / "
                                 f"{r['taken'] - base_en['taken']:.2f}" + (f" ({r['blocked_p'] - base_en['blocked_p']:.2f} stopped)" if r['blocked_p'] else ""))
                print(f"| {rule} | " + " | ".join(cells) + " |", flush=True)
    return res


def run_real(n):
    jobs = [(p, rule, "base", d, n) for p in ("X base", "X bleed") for rule in RULES for d in (None, 'enemies')]
    with Pool() as pool:
        res = dict(pool.map(party_job, jobs))
    for d, label in ((None, "no Protected"), ('enemies', "Durable enemies")):
        print(f"\n== Bleeding builds (party X), {label}: rounds / loses / Down, or after / HP left / Bleeding landed")
        print("| Rule | X base | X bleed |")
        print("|---|---|---|")
        for rule in RULES:
            c = []
            for p in ("X base", "X bleed"):
                r = res[(p, rule, "base", d)]
                c.append(f"{r['rounds']:.2f} / {r['loses']:.1f}% / {r['down_after']:.0f}% / {r['hp']:.1f} / {r['landed']:.2f}"
                         + (f" ({r['blocked_e']:.2f} stopped)" if r['blocked_e'] else ""))
            print(f"| {rule} | " + " | ".join(c) + " |", flush=True)
    return res


SIZES = (1, 2, 3, 5, 8)


def run_dose(n):
    configs = [(rule, None, 1.0) for rule in ("tick 1, through", "half, through")]
    configs += [(rule, 'enemies', 1.0) for rule in RULES]
    configs += [(rule, None, 1.75) for rule in ("tick 1, through", "half, through")]
    jobs = [(rule, d, m, c, t, s, n) for rule, d, m in configs for c in ("Hilde", "Sable")
            for t in ("Bleeding Dump", "Damage Dump") for s in SIZES]
    with Pool() as pool:
        res = dict(pool.map(dose_job, jobs))
    print("\n== One dose of N stacks on the carrier's first hit: extra points landing a fight, Hilde / Sable,"
          " and the share of +N damage on the same hit")
    print("| Rule | Durable enemies | Enemy Health | " + " | ".join(f"{s} stack{'s' if s > 1 else ''}" for s in SIZES) + " |")
    print("|---|---|---|" + "---|" * len(SIZES))
    for rule, d, m in configs:
        cells = []
        for s in SIZES:
            b = [res[(rule, d, m, c, "Bleeding Dump", s)] for c in ("Hilde", "Sable")]
            tw = [res[(rule, d, m, c, "Damage Dump", s)] for c in ("Hilde", "Sable")]
            cells.append(" / ".join(f"{x:.2f}" for x in b) + " (" + " / ".join(
                f"{100 * x / y:.0f}%" if y else "-" for x, y in zip(b, tw)) + ")")
        print(f"| {rule} | {'yes' if d else 'no'} | x{m} | " + " | ".join(cells) + " |", flush=True)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=("grid", "real", "dose"))
    ap.add_argument("-n", type=int, default=400, help="fights per mix")
    ap.add_argument("-p", action="append", help="parties for the grid (default A and T)")
    a = ap.parse_args()
    if a.what == "grid":
        run_grid(a.p or ["A", "T"], a.n)
    elif a.what == "real":
        run_real(a.n)
    else:
        run_dose(a.n)
