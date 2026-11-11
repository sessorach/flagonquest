"""Fitting the hit-chance and hit-size targets (2026-11-08).

Per the designer (firm, DESIGNER_NOTES "Targets for how a fight should
feel"): PCs hit 50-75% of the time, enemies 25-50%, and a hit lands 2-3
on average on both sides; these win over fight length. Today PCs hit
86-93% from Level 2 for 4.8-5.8. A grid on the enemy table at every
Level: Skill (every Defense) +0 to +4, Resist +0 to +3 (the Resist Stat
caps at 5, as a PC's), Health times 0.4 to 1. tools/combat_stats.py's
fights (the manual's encounters, the middle parties), 4 a pairing; the
best per Level is read off afterwards.

    python3 experiments/enemies/hit_fit.py run
    python3 experiments/enemies/hit_fit.py run --wide
    python3 experiments/enemies/hit_fit.py run --set
    python3 experiments/enemies/hit_fit.py read
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import combat_stats as cst  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

SKILL = (0, 1, 2, 3, 4)
RESIST = (0, 1, 2, 3)
HEALTH = (1.0, 0.75, 0.6, 0.5, 0.4)
# Round two (`run --wide`): Levels 3-5, the Resist cap lifted
# (tunables.V3_RESIST_CAP), more Resist and less Health.
WIDE = dict(levels=(3, 4, 5), skill=(2, 3, 4), resist=(3, 4, 5, 6), health=(0.5, 0.4, 0.3, 0.25))
# Round three (`run --set`, designer: monsters of about 8 Health, "two solid
# hits or three more standard ones"; keep the Resist cap): the table's
# Health set to 5-7 (standard monsters then average about 7.5-10 with
# their archetype and leftover points), Skill and Resist as in round one.
SET = dict(skill=(0, 1, 2, 3, 4), resist=(0, 1, 2, 3), health=(5, 6, 7))
OUT = os.path.join(_paths.ROOT, "results", "enemy_stats", "hit_fit.jsonl")


def _job(args):
    spec, level, gi, n = args
    eb.T.V3_RESIST_CAP = 99 if spec.endswith(",wide") else None
    cst.TABLE[0] = spec.replace(",wide", "")
    eb._stats_installed = False
    for L, t in BASE.items():
        eb.ENEMY_TABLE_V3_PRUNED[L] = dict(t)
    r = cst._job((level, gi, n))
    att, fs = r["att"], r["fights"]
    return dict(spec=spec, level=level, gi=gi, pc_att=att.get("pc_att", 0), pc_hit=att.get("pc_hit", 0),
                en_att=att.get("en_att", 0), en_hit=att.get("en_hit", 0),
                pc_dmg=sum(r["pc_hit_dmg"]), en_dmg=sum(r["en_hit_dmg"]), pc_max=r["pc_max"],
                rounds=[f["rounds"] for f in fs], down=[f["down"] for f in fs], lost=[f["lost"] for f in fs],
                hp=[f["hp_lost"] for f in fs])


BASE = {L: dict(t) for L, t in eb.ENEMY_TABLE_V3_PRUNED.items()}


def run(a):
    done = set()
    if os.path.exists(OUT):
        done = {(r["spec"], r["level"], r["gi"]) for r in map(json.loads, open(OUT))}
    jobs = []
    grid = ((WIDE["skill"], WIDE["resist"], WIDE["health"]) if a.wide else
            (SET["skill"], SET["resist"], SET["health"]) if a.set else (SKILL, RESIST, HEALTH))
    for s, r, h in itertools.product(*grid):
        spec = (f"skill=+{s},resist=+{r},health==" + str(h) if a.set else
                f"skill=+{s},resist=+{r},health=*{h}" + (",wide" if a.wide else ""))
        for L in (WIDE["levels"] if a.wide else cst.LEVELS):
            for gi in range(len([g for g in tc.groups(L, ps.MID[L]) if g[0] != "stand-ins"])):
                if (spec, L, gi) not in done:
                    jobs.append((spec, L, gi, a.n))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(os.cpu_count(), maxtasksperchild=20) as pool:
        for r in pool.imap_unordered(_job, jobs, chunksize=4):
            with open(OUT, "a") as f:
                f.write(json.dumps(r) + "\n")


def summary():
    agg = {}
    for r in map(json.loads, open(OUT)):
        k = (r["spec"], r["level"])
        a = agg.setdefault(k, dict(pc_att=0, pc_hit=0, en_att=0, en_hit=0, pc_dmg=0, en_dmg=0, rounds=[], down=[],
                                   lost=[], hp=[], pc_max=r["pc_max"]))
        for x in ("pc_att", "pc_hit", "en_att", "en_hit", "pc_dmg", "en_dmg"):
            a[x] += r[x]
        for x in ("rounds", "down", "lost", "hp"):
            a[x] += r[x]
    out = {}
    for k, a in agg.items():
        out[k] = dict(pc_hit=a["pc_hit"] / max(1, a["pc_att"]), en_hit=a["en_hit"] / max(1, a["en_att"]),
                      pc_dmg=a["pc_dmg"] / max(1, a["pc_hit"]), en_dmg=a["en_dmg"] / max(1, a["en_hit"]),
                      rounds=st.mean(a["rounds"]), down=st.mean(a["down"]), lost=st.mean(a["lost"]),
                      hp=st.mean(a["hp"]))
    return out


def miss(m):
    """How far outside the firm targets (0 inside), in target widths."""
    def out(x, lo, hi):
        return max(0, lo - x, x - hi) / (hi - lo)
    return out(m["pc_hit"], 0.50, 0.75) + out(m["en_hit"], 0.25, 0.50) + out(m["pc_dmg"], 2, 3) + out(m["en_dmg"], 2, 3)


def read(a):
    s = summary()
    if a.set:
        s = {k: m for k, m in s.items() if "health==" in k[0] or k[0] == "skill=+0,resist=+0,health=*1.0"}
    lines = []
    for L in cst.LEVELS:
        rows = sorted(((miss(m), abs(m["down"] - 0.2) + max(0, m["lost"] - 0.03) * 5, spec, m)
                       for (spec, lv), m in s.items() if lv == L), key=lambda x: (round(x[0], 2), x[1]))
        lines += [f"### Level {L}", "",
                  "| Change | Outside targets | PC hit / lands | Enemy hit / lands | Rounds | Down / lost | Health lost |",
                  "|---|---|---|---|---|---|---|"]
        for mi, _, spec, m in [r for r in rows if r[2] == "skill=+0,resist=+0,health=*1.0"] + rows[:8]:
            lines.append(f"| {spec} | {mi:.2f} | {100 * m['pc_hit']:.0f}% / {m['pc_dmg']:.1f} | "
                         f"{100 * m['en_hit']:.0f}% / {m['en_dmg']:.1f} | {m['rounds']:.1f} | "
                         f"{100 * m['down']:.0f}% / {100 * m['lost']:.1f}% | {m['hp']:.0f}% |")
        lines.append("")
    text = "\n".join(lines)
    print(text)
    open(OUT.replace(".jsonl", "_set.txt" if a.set else ".txt"), "w").write(text + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-n", type=int, default=4)
    ap.add_argument("--wide", action="store_true", help="round two: Levels 3-5, the Resist cap lifted")
    ap.add_argument("--set", action="store_true", help="round three: the table's Health set to 5-7")
    a = ap.parse_args()
    {"run": run, "read": read}[a.cmd](a)
