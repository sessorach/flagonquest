"""On-level fights with an extra Slot or two (2026-11-10), per the designer:
is that a better threatening fight than a Level up? The effect_check party
(Hilde, Browndog, Carrick, Sable, Level 1) against the eight Level 1 manual
encounters, each with one or two more standard attackers from the same
encounter; single fights and a day's first fight, 250 fights a cell.

    python3 experiments/enemies/extra_slots.py
"""
import sys, statistics as st
from multiprocessing import Pool

import _paths, combat_sim as cs, sample_enemies as se, party

NAMES = ["Hilde", "Browndog", "Carrick", "Sable"]
N = 250

def mix_plus(m, extra):
    enc = list(se.ENCOUNTERS[1][m])
    ones = [x for x in enc if se.get_enemy(x).get("slots", 1) == 1 and se.get_enemy(x)["kind"] == "attack"]
    return enc + [ones[i % len(ones)] for i in range(extra)]

def job(a):
    m, extra, day = a
    rows = party._rows()
    cs.make_party = lambda tier, good_luck=0: [party.make_pc(n, i, good_luck, rows=rows) for i, n in enumerate(NAMES, 1)]
    out = []
    for k in range(N):
        r = cs.run_fight(1, 1, movement=True, enemies=se.build_encounter(mix_plus(m, extra)), seed=k, day_fight=day)
        out.append((r["winner"] != "party", r["rounds"], 100 * r["party_hp_pct"], bool(r["pc_downed"])))
    return (extra, day), out

jobs = [(m, x, d) for m in se.CURRENT_MIXES for x in (0, 1, 2) for d in (None, 1)]
res = {}
with Pool() as p:
    for key, out in p.imap_unordered(job, jobs):
        res.setdefault(key, []).extend(out)
print("| Slots | Fight | Lost | Someone Down | Rounds | Party Health left |")
print("|---|---|---|---|---|---|")
for x in (0, 1, 2):
    for d in (None, 1):
        o = res[(x, d)]
        print(f"| {4 + x} | {'single' if d is None else 'day, fight 1'} | {100 * st.mean(a for a, *_ in o):.1f}% | "
              f"{100 * st.mean(c for *_, c in o):.0f}% | {st.mean(b for _, b, *_ in o):.1f} | {st.mean(h for _, _, h, _ in o):.0f}% |")
print("Encounters (+2):")
for m in se.CURRENT_MIXES:
    print(" ", m, mix_plus(m, 2))
