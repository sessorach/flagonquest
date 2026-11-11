"""Average and spread of the combat numbers on the monster manual (2026-11-08).

Per the designer: hit chance, chance to be hit, damage dealt and taken,
round length, overall lethality, and how much they vary. Every party in
the middle of its band against the manual's own encounters
(manual_check's draws, no solo boss), Levels 1-5, fresh single fights,
traced. `--prev` plays the table without the 2026-11-08 harder hits
(enemy_builder_pcstyle.V3_HARD_HITS) for comparison, on the same seeds.

Per attack: hit chance (a hit is a hit even when Resist takes it all), and
what a hit lands after Resist and Protected. Per fight: rounds, party
Health lost (a share of its max), damage the party takes and deals a
round, PCs dropped to 0, and whether someone went Down or the fight was
lost. Spread: the standard deviation and the 10th-90th percentile range.

    python3 tools/combat_stats.py                 # today's table
    python3 tools/combat_stats.py --prev          # without the harder hits
    python3 tools/combat_stats.py --table "skill=+3,health=*0.5" --name try1
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import combat_sim as cs  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import bands  # noqa: E402

LEVELS = (1, 2, 3, 4, 5)
K_ENC = 24
PREV = [False]
TABLE = [""]


def install():
    if getattr(eb, "_stats_installed", False):
        return
    eb._stats_installed = True
    for t in eb.ENEMY_TABLE_V3_PRUNED.values():
        if PREV[0]:
            for k, d in eb.V3_HARD_HITS.items():
                t[k] -= d
        # --table "skill=+3,resist=+2,health=*0.5": every Level's row changed.
        for part in filter(None, TABLE[0].split(",")):
            k, _, v = part.partition("=")
            t[k] = (max(1, round(t[k] * float(v[1:]))) if v.startswith("*") else int(v[1:]) if v.startswith("=")
                    else t[k] + int(v))


def _job(args):
    level, gi, n = args
    install()
    T.ENEMY_LEVEL_UP = 0
    gname, names, swaps = [g for g in bands.groups(level, bands.MID[level]) if g[0] != "stand-ins"][gi]
    encs = [e for e in mc.encounters(level, K_ENC, 1)
            if not any(se.get_enemy(f"{x}@{level}").get("slots", 1) == 4 for x in e)]
    rows = party._rows()
    cs.make_party = lambda tier, good_luck=0: [
        party.make_pc(m, i, good_luck, rows=rows, edits=swaps.get(m, (None, None))[0],
                      row_changes=swaps.get(m, (None, None))[1]) for i, m in enumerate(names, 1)]
    pc_max = st.mean(p["max_health"] for p in cs.make_party(1))
    att = collections.Counter()
    pc_hit_dmg, en_hit_dmg, fights = [], [], []
    for ei, enc in enumerate(encs):
        for k in range(n):
            trace = []
            r = cs.run_fight(1, min(level, 3), movement=True,
                             enemies=se.build_encounter([f"{x}@{level}" for x in enc]),
                             seed=1_000_000 * gi + 1_000 * ei + k, trace=trace)
            taken = dealt = 0
            dropped = set()
            for t in trace:
                if t.get("action") != "attack":
                    continue
                side = t.get("side")
                if side == "party":
                    att["pc_att"] += 1
                    if t.get("hit"):
                        att["pc_hit"] += 1
                        pc_hit_dmg.append(t.get("dmg", 0))
                        dealt += t.get("dmg", 0)
                elif side == "enemy":
                    att["en_att"] += 1
                    if t.get("hit"):
                        att["en_hit"] += 1
                        en_hit_dmg.append(t.get("dmg", 0))
                        taken += t.get("dmg", 0)
                        if t.get("target_hp_after", 1) <= 0:
                            dropped.add(t.get("target"))
            rounds = max(1, r["rounds"])
            fights.append(dict(rounds=r["rounds"], lost=r["winner"] != "party", down=bool(r["pc_downed"]),
                               wounded=bool(r.get("pc_wounded")), hp_lost=100 * (1 - r["party_hp_pct"]),
                               taken=taken / rounds, dealt=dealt / rounds, dropped=len(dropped),
                               again=r["acts_again_any"]))
    return dict(level=level, gi=gi, pc_max=pc_max, att=dict(att), pc_hit_dmg=pc_hit_dmg, en_hit_dmg=en_hit_dmg,
                fights=fights)


def spread(xs, fmt="{:.1f}"):
    xs = sorted(xs)
    p = lambda q: xs[min(len(xs) - 1, int(q * len(xs)))]
    return (f"{fmt.format(st.mean(xs))} (sd {fmt.format(st.pstdev(xs))}; "
            f"{fmt.format(p(0.1))}-{fmt.format(p(0.9))})")


def report(res):
    out = ["Every party in the middle of its band, the manual's encounters; mean (standard deviation; "
           "10th-90th percentile).", ""]
    for L in LEVELS:
        rs = [r for r in res if r["level"] == L]
        att = collections.Counter()
        for r in rs:
            att.update(r["att"])
        pch = [d for r in rs for d in r["pc_hit_dmg"]]
        enh = [d for r in rs for d in r["en_hit_dmg"]]
        fs = [f for r in rs for f in r["fights"]]
        pc_max = st.mean(r["pc_max"] for r in rs)
        out += [f"### Level {L} ({len(fs)} fights; an average PC has {pc_max:.1f} Health)", "",
                "| | Value |", "|---|---|",
                f"| PC hit chance | {100 * att['pc_hit'] / att['pc_att']:.0f}% |",
                f"| Chance an enemy attack hits a PC | {100 * att['en_hit'] / att['en_att']:.0f}% |",
                f"| A PC hit lands | {spread(pch)} |",
                f"| An enemy hit lands | {spread(enh)}; {100 * st.mean(enh) / pc_max:.0f}% of a PC; "
                f"{100 * sum(1 for d in enh if d == 0) / len(enh):.0f}% land 0 |",
                f"| Party deals a round (attacks) | {spread([f['dealt'] for f in fs])} |",
                f"| Party takes a round (attacks) | {spread([f['taken'] for f in fs])} |",
                f"| Rounds | {spread([f['rounds'] for f in fs])} |",
                f"| Party Health lost (% of max) | {spread([f['hp_lost'] for f in fs], '{:.0f}')} |",
                f"| PCs dropped to 0 a fight | {spread([f['dropped'] for f in fs], '{:.2f}')} |",
                f"| A hit enemy acts again | {100 * sum(f['again'][0] for f in fs) / max(1, sum(f['again'][1] for f in fs)):.0f}% |",
                f"| Someone Down / Wounded / fight lost | {100 * st.mean(f['down'] for f in fs):.0f}% / "
                f"{100 * st.mean(f['wounded'] for f in fs):.0f}% / {100 * st.mean(f['lost'] for f in fs):.1f}% |",
                ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=10, help="fights per encounter per party")
    ap.add_argument("--prev", action="store_true", help="the table without the harder hits")
    ap.add_argument("--table", default="", help='changes to every Level\'s row: "skill=+3,resist=+2,health=*0.5"')
    ap.add_argument("--name", help="results file name (results/enemy_stats/<name>.txt)")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    PREV[0], TABLE[0] = a.prev, a.table
    jobs = [(L, gi, a.n) for L in LEVELS
            for gi in range(len([g for g in bands.groups(L, bands.MID[L]) if g[0] != "stand-ins"]))]
    with mp.Pool(a.j) as pool:
        res = list(pool.imap_unordered(_job, jobs))
    text = report(res)
    print(text)
    name = a.name or ("combat_stats_prev" if a.prev else "combat_stats")
    open(os.path.join(_paths.ROOT, "results", "enemy_stats", name + ".txt"), "w").write(text + "\n")


if __name__ == "__main__":
    main()
