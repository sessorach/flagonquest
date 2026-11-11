"""Squaring the sharpened hit targets on the whole-day model (2026-11-09).

Per the designer (DESIGNER_NOTES, "Targets for how a fight should
feel"): with their resources, PCs hit about two thirds of the time,
enemies about half; a hit lands 2-3 both ways; fight length comes from
how long things live, and that comes last, without big sacks of enemy
Health. Today (11-09 defaults) PCs hit 68-77% and enemies 22-36%. A grid
on the table at every Level, from today's: Accuracy +1 to +4, Damage -1 or
+0, Skill (every Defense) -1 to +1, Health -2 to +2;
tools/combat_stats.py's fights (the manual's encounters, the middle
parties, single fights with potions), 4 a pairing. Read per Level;
then the closest set is checked on the band's whole days.

    python3 experiments/enemies/hit_fit2.py run
    python3 experiments/enemies/hit_fit2.py read
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401
import hit_fit as hf  # noqa: E402
import combat_stats as cst  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402
import sample_enemies as se  # noqa: E402
import statistics as st  # noqa: E402

GRID = dict(accuracy=(1, 2, 3, 4), damage=(-1, 0), skill=(-1, 0, 1), health=(-2, 0, 2))
hf.OUT = os.path.join(_paths.ROOT, "results", "enemy_stats", "hit_fit2.jsonl")


def specs():
    for a, d, s, h in itertools.product(*GRID.values()):
        yield f"accuracy=+{a},damage={d:+d},skill={s:+d},health={h:+d}"


def run(a):
    done = set()
    if os.path.exists(hf.OUT):
        done = {(r["spec"], r["level"], r["gi"]) for r in map(json.loads, open(hf.OUT))}
    jobs = [(spec, L, gi, a.n) for spec in ["accuracy=+0", *specs()] for L in cst.LEVELS
            for gi in range(len([g for g in tc.groups(L, ps.MID[L]) if g[0] != "stand-ins"]))
            if (spec, L, gi) not in done]
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(os.cpu_count(), maxtasksperchild=20) as pool:
        for r in pool.imap_unordered(hf._job, jobs, chunksize=4):
            with open(hf.OUT, "a") as f:
                f.write(json.dumps(r) + "\n")


def score(m):
    """Off the targets: hit chances (two thirds, a half), hit sizes (2-3),
    then fight length and lethality (about 4 rounds, Down about a fifth,
    few fights lost)."""
    out = lambda x, lo, hi: max(0, lo - x, x - hi)
    return (abs(m["pc_hit"] - 0.67) * 10 + abs(m["en_hit"] - 0.50) * 10
            + out(m["pc_dmg"], 2, 3) + out(m["en_dmg"], 2, 3)
            + 0.3 * abs(m["rounds"] - 4) + 3 * abs(m["down"] - 0.2) + 10 * max(0, m["lost"] - 0.03))


def health(spec, level):
    """A standard monster's average Health under `spec`."""
    import enemy_builder_pcstyle as eb
    cst.TABLE[0] = spec
    eb._stats_installed = False
    for L, t in hf.BASE.items():
        eb.ENEMY_TABLE_V3_PRUNED[L] = dict(t)
    cst.install()
    hs = [se.get_enemy(f"{n}@{level}")["max_health"] for n in se.manual_names()]
    hs = [h for h, n in zip(hs, se.manual_names()) if se.get_enemy(f"{n}@{level}")["slots"] == 1]
    return st.mean(hs)


def read(a):
    s = hf.summary()
    lines = []
    for L in cst.LEVELS:
        rows = sorted(((score(m), spec, m) for (spec, lv), m in s.items() if lv == L), key=lambda x: x[0])
        today = [r for r in rows if r[1] == "accuracy=+0"]
        lines += [f"### Level {L}", "",
                  "| Change | Score | PC hit / lands | Enemy hit / lands | Rounds | Down / lost | Health lost | Standard Health |",
                  "|---|---|---|---|---|---|---|---|"]
        for sc_, spec, m in today + rows[:8]:
            lines.append(f"| {spec} | {sc_:.2f} | {100 * m['pc_hit']:.0f}% / {m['pc_dmg']:.1f} | "
                         f"{100 * m['en_hit']:.0f}% / {m['en_dmg']:.1f} | {m['rounds']:.1f} | "
                         f"{100 * m['down']:.0f}% / {100 * m['lost']:.1f}% | {m['hp']:.0f}% | {health(spec, L):.1f} |")
        lines.append("")
    text = "\n".join(lines)
    print(text)
    open(hf.OUT.replace(".jsonl", ".txt"), "w").write(text + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-n", type=int, default=4)
    a = ap.parse_args()
    {"run": run, "read": read}[a.cmd](a)
