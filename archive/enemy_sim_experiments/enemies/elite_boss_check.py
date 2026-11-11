"""Bigger enemies with bigger budgets (2026-11-06).

Per the designer (option 1): an elite or solo boss gets its Ability
budget scaled by its size (tunables.V3_SLOT_BUDGET), each point costing
its Health over that scale, so one that spends nothing keeps its Health,
and spends the extra on mechanics. Levels 3-5, every test party in the
middle of the band, fresh fights. The boss and elites get the pick lists
below at each scale (in-process patches; the manual is unchanged).

    python3 experiments/enemies/elite_boss_check.py > results/enemy_stats/elite_boss_check.txt
"""
import collections
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

BOSS_X2 = "; Strike (Crippling); Strike (Crippling); Strike (Frightening); Strike (Frightening); Accuracy +1; Durable"
BOSS_X4 = BOSS_X2 + ("; Damage +1; Powerful Weapon; Strike (Battering); Resilient; Accuracy +1; "
                     "Enhanced Speed; Omniguard")
OGRE_X2 = "; Accuracy +1; Damage +1; Durable"
MATRIARCH_X2 = ("; Accuracy +1; Strike (Vulnerable); Strike (Vulnerable); Enhanced Reflexes; "
                "Parry and Dodge +1; Parry and Dodge +1")
# (label, encounter, {monster: extra picks}, {slots: budget scale})
# Round 2: the bigger budgets paid for with a smaller Health multiple
# (the boss's V3_SOLO_HEALTH, an elite's V3_ELITE_HEALTH): ("_hp", n).
CASES2 = [
    ("Solo boss, budget x2, Health x5", ["Brute Warlord"], {"Brute Warlord": BOSS_X2}, {4: 2, "_hp": 5}),
    ("Solo boss, budget x2, Health x4", ["Brute Warlord"], {"Brute Warlord": BOSS_X2}, {4: 2, "_hp": 4}),
    ("Solo boss, budget x2, Health x3", ["Brute Warlord"], {"Brute Warlord": BOSS_X2}, {4: 2, "_hp": 3}),
    ("Solo boss, budget x4, Health x4", ["Brute Warlord"], {"Brute Warlord": BOSS_X4}, {4: 4, "_hp": 4}),
    ("Solo boss, budget x4, Health x3", ["Brute Warlord"], {"Brute Warlord": BOSS_X4}, {4: 4, "_hp": 3}),
    ("Solo boss, budget x4, Health x2", ["Brute Warlord"], {"Brute Warlord": BOSS_X4}, {4: 4, "_hp": 2}),
    ("Two Gravel Ogres, budget x2, Health x2.5", ["Gravel Ogre"] * 2, {"Gravel Ogre": OGRE_X2}, {2: 2, "_hp": 2.5}),
    ("Two Gravel Ogres, budget x2, Health x2", ["Gravel Ogre"] * 2, {"Gravel Ogre": OGRE_X2}, {2: 2, "_hp": 2}),
]
CASES3 = [
    ("Solo boss, budget x2, Health x3.5", ["Brute Warlord"], {"Brute Warlord": BOSS_X2}, {4: 2, "_hp": 3.5}),
    ("Two Gravel Ogres, budget x2, Health x2.5", ["Gravel Ogre"] * 2, {"Gravel Ogre": OGRE_X2}, {2: 2, "_hp": 2.5}),
    ("Coven Matriarch + two Brutes, budget x2, Health x2.5", ["Coven Matriarch", "Brute", "Brute"],
     {"Coven Matriarch": MATRIARCH_X2}, {2: 2, "_hp": 2.5}),
]
CASES = [
    ("Solo boss, budget x1", ["Brute Warlord"], {}, {}),
    ("Solo boss, budget x2", ["Brute Warlord"], {"Brute Warlord": BOSS_X2}, {4: 2}),
    ("Solo boss, budget x4", ["Brute Warlord"], {"Brute Warlord": BOSS_X4}, {4: 4}),
    ("Two Gravel Ogres, budget x1", ["Gravel Ogre"] * 2, {}, {}),
    ("Two Gravel Ogres, budget x2", ["Gravel Ogre"] * 2, {"Gravel Ogre": OGRE_X2}, {2: 2}),
    ("Coven Matriarch + two Brutes, x1", ["Coven Matriarch", "Brute", "Brute"], {}, {}),
    ("Coven Matriarch + two Brutes, x2", ["Coven Matriarch", "Brute", "Brute"],
     {"Coven Matriarch": MATRIARCH_X2}, {2: 2}),
]


def _job(args):
    ci, level, gi, n = args
    label, enc, extra, scale = CASES[ci]
    scale = dict(scale)
    hp = scale.pop("_hp", None)
    if hp is not None:
        if 4 in scale:
            T.V3_SOLO_HEALTH = hp
        else:
            T.V3_ELITE_HEALTH = hp
    T.V3_SLOT_BUDGET = scale
    for r in game_data.csv_rows(se._MANUAL_PATH):
        if r["Name"] in extra:
            r["PrunedPicks"] += extra[r["Name"]]
    out = mc._job((level, gi, label, enc, n, 41))
    out.update(label=label)
    if gi == 0:
        e = se.get_enemy(f"{enc[0]}@{level}")
        out["health"] = e["max_health"]
    return out


def main():
    import sys
    if "round2" in sys.argv:
        CASES[:] = CASES2
    if "round3" in sys.argv:
        CASES[:] = CASES3
    jobs = [(ci, L, gi, 60) for ci in range(len(CASES)) for L in (3, 4, 5)
            for gi in range(len(tc.groups(L, ps.MID[L])))]
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(_job, jobs):
            res[(r["label"], r["level"])].append(r)
    print("| Fight | Level | Health of the big one | Lost (worst party) | Down | Wounded | Rounds |")
    print("|---|---|---|---|---|---|---|")
    for label, *_ in CASES:
        for L in (3, 4, 5):
            rs = res[(label, L)]
            hp = next(r["health"] for r in rs if "health" in r)
            print(f"| {label} | {L} | {hp} | {100 * (1 - st.mean(r['won'] for r in rs)):.0f}% "
                  f"({100 * (1 - min(r['won'] for r in rs)):.0f}%) | {100 * st.mean(r['down'] for r in rs):.0f}% | "
                  f"{100 * st.mean(r['wounded'] for r in rs):.0f}% | {st.mean(r['rounds'] for r in rs):.1f} |")


if __name__ == "__main__":
    main()
