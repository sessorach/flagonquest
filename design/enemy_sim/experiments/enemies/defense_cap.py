"""A cap on enemy Defense, like the one on Accuracy (2026-11-06).

Per the designer: no special pricing, keep it simple; is there a purchase
only Defenders make, or a cap like Accuracy's that only bites on the
walls? Variants, each applied to every enemy:

- cap_skill: no Defense Skill above the Level's Skill +2, before
  equipment (Parry's weapon Defense and armor's Dodge on top), clamped.
- cap_total: the same, but Parry's cap includes the weapon's Defense.
- once: Parry and Dodge +1 at most once (extra picks dropped; the
  points go to Health, as unspent points do).
- no_defender: a Defender can't buy Parry and Dodge +1 (likewise).
- cap_total_res: cap_total, and Physical Resist at most the Level's +2.
- def_p1d1 / def_p0d2 / def_p0d1: the Defender archetype's Parry/Dodge
  bumps trimmed, Health added at 1 a point.
- cap_def_p0d2: cap_total with def_p0d2.

Each is read on the walls (two Black Knights, a Black Knight leading
standard monsters, four Iron Sentinels), the manual's other Defenders,
and the Gravel Ogre as a control. `list` prints every manual monster the
caps change.

    python3 experiments/enemies/defense_cap.py run
    python3 experiments/enemies/defense_cap.py list
"""
import argparse
import collections
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import combat_sim as cs  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402
import big_enemy_options as b  # noqa: E402
import boss_encounters as be  # noqa: E402

VARIANTS = ["today", "cap_skill", "cap_total", "once", "no_defender", "cap_total_res",
            "def_p1d1", "def_p0d2", "def_p0d1", "cap_def_p0d2"]
# Archetype retunes (designer, 2026-11-06: maybe the Defender's bumps are
# the culprit): Parry/Dodge moved off, Health on at Parry and Dodge +1's
# price (1 a point).
DEFENDER = {"def_p1d1": dict(parry=1, dodge=1, hp=4), "def_p0d2": dict(parry=0, dodge=2, hp=4),
            "def_p0d1": dict(parry=0, dodge=1, hp=5), "cap_def_p0d2": dict(parry=0, dodge=2, hp=4)}
DEFENDER_TODAY = dict(eb.ROLE_ADDS_V3_ADDITIVE["Defender"])
MODE = ["today"]
ORIG_BUILD, ORIG_RUN = se._build_from_row, cs.run_fight
ORIG_PICKS = None  # big_enemy_options' wrapper, taken once it's installed


def picks(row, abilities):
    p, action = ORIG_PICKS(row, abilities)
    if MODE[0] == "once" and p.count("Parry and Dodge +1") > 1:
        first = p.index("Parry and Dodge +1")
        p = [x for i, x in enumerate(p) if x != "Parry and Dodge +1" or i == first]
    if MODE[0] == "no_defender" and (row.get("Role") or "").strip() == "Defender":
        p = [x for x in p if x != "Parry and Dodge +1"]
    return p, action


def build(row):
    e = ORIG_BUILD(row)
    if MODE[0] in ("cap_skill", "cap_total", "cap_total_res", "cap_def_p0d2") and (row.get("StrongDefense") or "").strip():
        level = int(row["Level"])
        cap = 8 + min(eb.SKILL_CAP, eb.ENEMY_TABLE_V3_PRUNED[level]["skill"]) + 2
        wd = eb.ACTIONS[e["action"]]["wd"] or 0
        if e["parry"] > 0:
            e["parry"] = min(e["parry"], cap + (wd if MODE[0] == "cap_skill" else 0))
        e["dodge"] = min(e["dodge"], cap + T.ARMOR[e["armor"]]["dodge"])
        for d in ("bodily", "mental", "vigilant"):
            e[d] = min(e[d], cap)
        if MODE[0] == "cap_total_res":
            # And Physical Resist no more than 2 over the Level's (armor included).
            e["physres"] = min(e["physres"], min(eb.STAT_CAP, eb.ENEMY_TABLE_V3_PRUNED[level]["resist"]) + 2)
    return e


def install(mode):
    global ORIG_PICKS
    b.install()
    if ORIG_PICKS is None:
        ORIG_PICKS = se._pruned_picks
    MODE[0] = mode
    eb.ROLE_ADDS_V3_ADDITIVE["Defender"] = dict(DEFENDER.get(mode, DEFENDER_TODAY))
    se._pruned_picks, se._build_from_row = picks, build


ENCS = {
    "Two Black Knights": lambda L: [["Black Knight"] * 2],
    "Black Knight + standard": lambda L: [["Black Knight", *c] for c in be.draws(L, 2)],
    "Four Iron Sentinels": lambda L: [["Iron Sentinel"] * 4],
    "Four Hedge Knights": lambda L: [["Hedge Knight"] * 4],
    "Four Ironbranch Wardens": lambda L: [["Ironbranch Warden"] * 4],
    "Eight Shieldbearers": lambda L: [["Shieldbearer"] * 8],
    "Two Gravel Ogres (control)": lambda L: [["Gravel Ogre"] * 2],
}


def _job(args):
    mode, name, L, gi, n = args
    install(mode)
    T.ENEMY_LEVEL_UP = 0
    b.setting(2, 1, 3)
    caps = []

    def rf(*a, **k):
        r = ORIG_RUN(*a, **k)
        caps.append(r)
        return r
    cs.run_fight = rf
    gname, pn, sw = tc.groups(L, ps.MID[L])[gi]
    out = []
    for enc in ENCS[name](L):
        se.ENCOUNTERS.setdefault(min(L, 3), {})["_t"] = [f"{x}@{L}" for x in enc]
        for k in range(n):
            del caps[:]
            rec, _ = ds.play_day(pn, sw, min(L, 3), ("_t",), 41 + 1000 * k, party._rows())
            r, f = caps[0], rec["per_fight"][0]
            out.append((r["winner"] == "party", r["winner"] == "draw", f["downs"] > 0, r["rounds"], r["pc_attacks"],
                        r["pc_damage_dealt"]))
    return mode, name, out


def run(a):
    jobs = [(m, n, L, gi, a.n) for m in (a.only.split(",") if a.only else VARIANTS) for n in ENCS for L in (2, 3, 4, 5)
            for gi in range(len(tc.groups(L, ps.MID[L])))]
    res = collections.defaultdict(list)
    with mp.Pool(a.j, maxtasksperchild=40) as pool:
        for m, n, o in pool.imap_unordered(_job, jobs, chunksize=2):
            res[(m, n)].extend(o)
    lines = ["| Encounter | Variant | Lost (draws) | Down | Rounds | Damage per attack |", "|---|---|---|---|---|---|"]
    for n in ENCS:
        for m in VARIANTS:
            o = res.get((m, n))
            if not o:
                continue
            lines.append(f"| {n} | {m} | {100 * (1 - st.mean(x[0] for x in o)):.1f}% ({100 * st.mean(x[1] for x in o):.0f}%) | "
                         f"{100 * st.mean(x[2] for x in o):.0f}% | {st.mean(x[3] for x in o):.1f} | "
                         f"{sum(x[5] for x in o) / sum(x[4] for x in o):.2f} |")
    text = "\n".join(lines)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def listing(a):
    keys = ("parry", "dodge", "bodily", "mental", "vigilant", "max_health")
    for L in (1, 3, 5):
        install("today")
        base = {n: se.get_enemy(f"{n}@{L}") for n in se.manual_names()}
        for m in VARIANTS[1:]:
            install(m)
            for n in se.manual_names():
                e = se.get_enemy(f"{n}@{L}")
                d = {k: e[k] - base[n][k] for k in keys if e[k] != base[n][k]}
                if d:
                    print(f"L{L} {m:12s} {n:20s} " + ", ".join(f"{k} {base[n][k]}->{e[k]}" for k in d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "list"))
    ap.add_argument("-n", type=int, default=50)
    ap.add_argument("--txt", default="results/enemy_stats/defense_cap.txt")
    ap.add_argument("--only", help="variants to run (comma-separated)")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    {"run": run, "list": listing}[a.cmd](a)


if __name__ == "__main__":
    main()
