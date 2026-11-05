"""Battle Tactics in the sim, side by side (2026-11-05).

Per the designer: look into Kiting and every Battle Tactic, and say which
stand out. Each manual monster that attacks plays four of itself (the
Slots of a party of four; minions eight, elites two) at Level 3 under
each tactic, against every test party in the middle of the band, fresh
fights. Tactics: Hit Whatever (closest), Assassin (softest), Kiting as
first coded ('always' retreats a move action each turn) and Kiting only
when engaged in melee (KITING_MOVE = 'engaged'). Hold the Line, Vanguard
and Triage aren't modeled: they play as Hit Whatever.

    python3 experiments/enemies/tactic_check.py -o results/enemy_stats/tactic_check.jsonl
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import game_data  # noqa: E402
import sample_enemies as se  # noqa: E402
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

TACTICS = [("Hit Whatever", "always"), ("Assassin", "always"), ("Kiting", "always"), ("Kiting", "engaged")]


def _job(args):
    name, tactic, move, level, gi, n = args
    T.KITING_MOVE = move
    for r in game_data.csv_rows(se._MANUAL_PATH):
        if r["Name"] == name:
            r["BattleTactic"] = tactic
    slots = mc.monsters()[name]["slots"]
    out = mc._job((level, gi, f"{name}:{tactic}:{move}", [name] * int(4 / slots), n, 11))
    out.update(monster=name, tactic=tactic if tactic != "Kiting" else f"Kiting ({move})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=40)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    ms = mc.monsters()
    names = [n for n, m in ms.items() if not m["passive"] and m["slots"] < 4]
    groups = len(tc.groups(a.L, ps.MID[a.L]))
    jobs = [(n, t, mv, a.L, gi, a.n) for n in names for t, mv in TACTICS for gi in range(groups)]
    res = collections.defaultdict(list)
    with mp.Pool(a.j, maxtasksperchild=8) as pool:
        for r in pool.imap_unordered(_job, jobs):
            res[(r["monster"], r["tactic"])].append(r)
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
    cols = ["Hit Whatever", "Assassin", "Kiting (always)", "Kiting (engaged)"]
    print("| Monster | " + " | ".join(cols) + " |")
    print("|---|" + "---|" * len(cols))
    for n in names:
        cells = []
        for c in cols:
            rs = res[(n, c)]
            cells.append(f"{100 * (1 - st.mean(r['won'] for r in rs)):.0f} / {100 * st.mean(r['down'] for r in rs):.0f} / "
                         f"{st.mean(r['rounds'] for r in rs):.1f}")
        print(f"| {n} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
