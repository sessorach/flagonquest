"""Debuff-shrugging picks on an elite (2026-11-06).

Per the designer: after barring Omniguard on elites, look at elites and
debuffs broadly. Two Gravel Ogres (Levels 3-5, every middle-of-band party,
30 fights) with one pick changed at a time: the Ogre's own Sturdy taken
off, or Resilient (shed one of each debuff a turn), Durable (+1 Protected
a turn) or Omniguard (ignore Harried) added with the Ogre's normal points
(the bar switched off for the test). Prices as the catalog's: Resilient
and Sturdy 0, Durable and Omniguard 1.

    python3 experiments/enemies/elite_debuff_picks.py
"""
import collections
import multiprocessing as mp
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import game_data  # noqa: E402
import combat_sim as cs  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

OGRE = next(dict(r) for r in game_data.csv_rows(se._MANUAL_PATH) if r["Name"] == "Gravel Ogre")
BASE = OGRE["PrunedPicks"]
VAR = {"as is (has Sturdy)": BASE,
       "no Sturdy": BASE.replace("; Sturdy", ""),
       "+ Resilient": BASE + "; Resilient",
       "+ Durable": BASE + "; Durable",
       "+ Omniguard": BASE + "; Omniguard",
       "+ Resilient, Durable, Omniguard": BASE + "; Resilient; Durable; Omniguard"}
ORIG_ROW = se._manual_row


def job(a):
    v, L, gi = a
    T.ENEMY_LEVEL_UP = 0
    T.V3_BIG_BARRED = ()

    def row(name):
        r = ORIG_ROW(name)
        if r is not None and name.startswith("Gravel Ogre@"):
            r = dict(r, PrunedPicks=VAR[v])
        return r
    se._manual_row = row
    gname, pn, sw = tc.groups(L, ps.MID[L])[gi]
    make, last = ds._maker(pn, sw, party._rows(), [])
    out = []
    for k in range(30):
        cs.make_party = make
        tr = []
        r = cs.run_fight(1, min(L, 3), movement=True, enemies=se.build_encounter([f"Gravel Ogre@{L}"] * 2),
                         seed=1000 + k, trace=tr)
        att = [e for e in tr if e.get("side") == "party" and e.get("action") == "attack" and "raw_dmg" in e]
        out.append((r["winner"] == "party", r["rounds"], any(p.get("was_downed") for p in last),
                    sum(e["hit"] for e in att), len(att)))
    return v, out


if __name__ == "__main__":
    jobs = [(v, L, gi) for v in VAR for L in (3, 4, 5) for gi in range(8)]
    res = collections.defaultdict(list)
    with mp.Pool(4) as p:
        for v, o in p.imap_unordered(job, jobs):
            res[v].extend(o)
    for v in VAR:
        o = res[v]
        print(f"| {v} | {100 * (1 - st.mean(x[0] for x in o)):.1f}% | {100 * st.mean(x[2] for x in o):.0f}% | "
              f"{st.mean(x[1] for x in o):.1f} | {100 * sum(x[3] for x in o) / sum(x[4] for x in o):.0f}% |")
