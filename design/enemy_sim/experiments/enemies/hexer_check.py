"""What a hexer adds to a fight, and other jobs it could have (2026-11-05).

Per the designer: review the hexers and what their job in the ecosystem
should be. A basic fight at Level 3, three of a working monster plus one
fourth, against every test party in the middle of the band, fresh fights.
The fourth is another of the working monster (the reference), a manual
hexer as built, or a hexer changed one way: a different effect, the old
stack counts, or a Hex that also deals its backup's damage. Patches are
in-process only; the manual is unchanged.

    python3 experiments/enemies/hexer_check.py > results/enemy_stats/hexer_check.txt
"""
import collections
import json
import multiprocessing as mp
import os
import statistics as st
import sys

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import game_data  # noqa: E402
import sample_enemies as se  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import manual_check as mc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

LEVEL = 3
OLD_STACKS = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5}
# (label, team, fourth, patch): patch edits the fourth's manual row
VARIANTS = []
for team in ("Brute", "Grave Caller"):
    VARIANTS += [
        (f"{team} x4", team, team, {}),
        (f"{team} x3 + Bog Hexer (Crippled)", team, "Bog Hexer", {}),
        (f"{team} x3 + Bog Hexer, old stacks", team, "Bog Hexer", {"_stacks": "old"}),
        (f"{team} x3 + Bog Hexer, Harried", team, "Bog Hexer", {"MainEffect": "Harried"}),
        (f"{team} x3 + Bog Hexer, Vulnerable", team, "Bog Hexer", {"MainEffect": "Vulnerable"}),
        (f"{team} x3 + Bog Hexer, Frightened", team, "Bog Hexer", {"MainEffect": "Frightened"}),
        (f"{team} x3 + Mire Witch (Slowed)", team, "Mire Witch", {}),
        (f"{team} x3 + Curse Weaver (Vulnerable)", team, "Curse Weaver", {}),
        (f"{team} x3 + Ember Caster (attacker)", team, "Ember Caster", {}),
        # Other jobs: a curse that lasts the fight, one that spreads to PCs
        # within 3 m of its target, both, and a caster whose damaging
        # spells carry the debuff instead of a Hex.
        (f"{team} x3 + Bog Hexer, lasting", team, "Bog Hexer", {"_persist": True}),
        (f"{team} x3 + Bog Hexer, spreading", team, "Bog Hexer", {"_area": 3}),
        (f"{team} x3 + Bog Hexer, lasting and spreading", team, "Bog Hexer", {"_persist": True, "_area": 3}),
        (f"{team} x3 + Bog Hexer as a Crippling caster", team, "Bog Hexer",
         {"Action": "Ranged Spell", "BackupAction": "", "MainEffect": "",
          "PrunedPicks": "Accuracy +1; Accuracy +1; Enhanced Range; Shadow Jaunt; Strike (Crippling); "
                         "Strike (Crippling); Strike (Crippling); Strike (Crippling)"}),
    ]


def _job(args):
    label, team, fourth, patch, gi, n = args
    for r in game_data.csv_rows(se._MANUAL_PATH):
        if r["Name"] == fourth:
            for k, v in patch.items():
                if not k.startswith("_"):
                    r[k] = v
    T.HEX_PERSIST = bool(patch.get("_persist"))
    T.HEX_AREA = patch.get("_area", 0)
    if patch.get("_stacks") == "old":
        eb.HEX_STACKS_V3P.update(OLD_STACKS)
    out = mc._job((LEVEL, gi, label, [team] * 3 + [fourth], n, 21))
    out["label"] = label
    return out


def main():
    groups = len(tc.groups(LEVEL, ps.MID[LEVEL]))
    jobs = [(l, t, f, p, gi, 60) for l, t, f, p in VARIANTS for gi in range(groups)]
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(_job, jobs):
            res[r["label"]].append(r)
    print("| Fight | Lost | Down | Wounded | Rounds |\n|---|---|---|---|---|")
    for l, *_ in VARIANTS:
        rs = res[l]
        print(f"| {l} | {100 * (1 - st.mean(r['won'] for r in rs)):.1f}% | {100 * st.mean(r['down'] for r in rs):.0f}% | "
              f"{100 * st.mean(r['wounded'] for r in rs):.0f}% | {st.mean(r['rounds'] for r in rs):.1f} |")


if __name__ == "__main__":
    main()
