"""A boss encounter without a solo boss (2026-11-06).

Per the designer: maybe the 4-Slot solo boss doesn't hold up, and the
standard boss is an elite (2 Slots) leading standard monsters. Which
shape reads as a boss fight without often beating the party? An elite
plus standard monsters filling 4, 5 or 6 Slots (the party is 4); two
elites plus 0-2 standard monsters; and all-standard encounters at the
same sizes for reference. Elites at today's setting (budget x1, Health
x3) and with twice the budget under the offense-only rule
(big_enemy_options.py --rule offense) at Health x2.5 and x3. Companions
are fixed draws of the manual's standard attackers per Level, the same
across settings. Every party in the middle of its band, plus the low and
high points for the main candidate; 100 fresh fights each.

    python3 experiments/enemies/boss_encounters.py run
    python3 experiments/enemies/boss_encounters.py read --txt results/enemy_stats/boss_encounters.txt
"""
import argparse
import collections
import itertools
import json
import multiprocessing as mp
import os
import random
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402
import big_enemy_options as b  # noqa: E402

ELITES = ["Gravel Ogre", "Elite Sharpshooter", "Storm Magus", "Coven Matriarch", "Black Knight"]
SETS = [(1, 3), (2, 2.5), (2, 3)]
MAIN = (2, 2.5)  # also run at the low and high band points
SIZES = (4, 5, 6)
K = 4  # companion draws per Level and size


def pool():
    out = []
    for n in se.manual_names():
        e = se.get_enemy(f"{n}@3")
        if e.get("slots", 1) == 1 and e["kind"] == "attack":
            out.append(n)
    return out


def draws(level, n, k=K, seed=11):
    """k fixed sets of n standard attackers (distinct monsters)."""
    if n == 0:
        return [()]
    rng = random.Random(seed * 1000 + level * 10 + n)
    p, out = pool(), []
    while len(out) < k:
        d = tuple(sorted(rng.sample(p, n)))
        if d not in out:
            out.append(d)
    return out


def cases():
    out = []
    for L in (1, 2, 3, 4, 5):
        for size in SIZES:
            for comp in draws(L, size):
                out.append(dict(shape="standard", lead="-", level=L, size=size, scale=1, hp=3, enc=list(comp)))
            for e in ELITES:
                for comp in draws(L, size - 2):
                    for s, h in SETS:
                        out.append(dict(shape="elite", lead=e, level=L, size=size, scale=s, hp=h, enc=[e, *comp]))
            for e1, e2 in itertools.combinations([e for e in ELITES if e != "Black Knight"], 2):
                for comp in draws(L, size - 4, k=2):
                    for s, h in SETS:
                        out.append(dict(shape="two elites", lead=f"{e1}+{e2}", level=L, size=size, scale=s, hp=h,
                                        enc=[e1, e2, *comp]))
    return out


def _job(args):
    c, budget, gi, n, seed = args
    b.install()
    b.RULE[0] = "offense"  # only matters when the budget is scaled
    T.ENEMY_LEVEL_UP = 0
    b.setting(2, c["scale"], c["hp"])
    L = c["level"]
    gname, pnames, swaps = tc.groups(L, budget)[gi]
    lvl = min(L, 3)
    se.ENCOUNTERS.setdefault(lvl, {})["_test"] = [f"{x}@{L}" for x in c["enc"]]
    prow = party._rows()
    out = collections.Counter()
    for k in range(n):
        rec, _ = ds.play_day(pnames, swaps, lvl, ("_test",), seed + 1000 * k, prow)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["down"] += f["downs"] > 0
        out["down2"] += f["downs"] > 1
        out["wounded"] += bool(f["wounded"])
        out["rounds"] += f["rounds"]
    return dict(c, budget=budget, party=gname, n=n,
                **{k: out[k] / n for k in ("won", "down", "down2", "wounded", "rounds")})


def key(r):
    return (r["shape"], r["lead"], r["level"], r["size"], r["scale"], r["hp"], "|".join(r["enc"]), r["budget"],
            r["party"])


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {key(r) for r in map(json.loads, open(a.o)) if r}
    jobs = []
    for c in cases():
        L = c["level"]
        pts = [ps.MID[L]]
        if L > 1 and c["shape"] != "two elites" and (c["shape"] == "standard" or (c["scale"], c["hp"]) == MAIN):
            pts = list(tc.POINTS[L])
        for bud in pts:
            for gi, (gname, _, _) in enumerate(tc.groups(L, bud)):
                if key(dict(c, budget=bud, party=gname)) not in done:
                    jobs.append((c, bud, gi, a.n, a.seed))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j, maxtasksperchild=50) as pool_:
        for i, r in enumerate(pool_.imap_unordered(_job, jobs, chunksize=2)):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
            if i % 500 == 0:
                print(i, flush=True)


def pos(r):
    return 1 if r["level"] == 1 else tc.POINTS[r["level"]].index(r["budget"])


def line(rs):
    by_enc = collections.defaultdict(list)
    for r in rs:
        by_enc["|".join(r["enc"]) + str(r["level"])].append(1 - r["won"])
    worst = max(st.mean(v) for v in by_enc.values())
    return (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% | {100 * worst:.0f}% | "
            f"{100 * st.mean(r['down'] for r in rs):.0f}% | {100 * st.mean(r['down2'] for r in rs):.0f}% | "
            f"{100 * st.mean(r['wounded'] for r in rs):.0f}% | {st.mean(r['rounds'] for r in rs):.1f}")


def read(a):
    recs = [json.loads(l) for l in open(a.o) if l.strip()]
    out = []
    head = ("| Shape | Slots | Setting | Lost | Worst encounter | Down | 2+ Down | Wounded | Rounds |\n"
            "|---|---|---|---|---|---|---|---|---|")

    def rows(sel, title, band=1):
        out.append(f"\n### {title}\n\n{head}")
        for size in SIZES:
            for shape in ("standard", "elite", "two elites"):
                for s, h in ([(1, 3)] if shape == "standard" else SETS):
                    rs = [r for r in recs if sel(r) and r["shape"] == shape and r["size"] == size
                          and (r["scale"], r["hp"]) == (s, h) and pos(r) == band]
                    if rs:
                        setting = "-" if shape == "standard" else f"x{s}, Health x{h}"
                        out.append(f"| {shape} | {size} | {setting} | {line(rs)} |")

    no_bk = lambda r: "Black Knight" not in r["lead"]
    rows(no_bk, "Middle of the band, Levels 1-5 (no Black Knight)")
    for L in (1, 2, 3, 4, 5):
        rows(lambda r, L=L: no_bk(r) and r["level"] == L, f"Level {L}, middle of the band (no Black Knight)")
    rows(lambda r: no_bk(r) and r["level"] > 1, "Low band point, Levels 2-5 (no Black Knight)", band=0)
    rows(lambda r: no_bk(r) and r["level"] > 1, "High band point, Levels 2-5 (no Black Knight)", band=2)
    out.append("\n### Each elite leading standard monsters, middle of the band\n")
    out.append("| Elite | Slots | Setting | Lost | Worst encounter | Down | 2+ Down | Wounded | Rounds |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for e in ELITES:
        for size in SIZES:
            for s, h in SETS:
                rs = [r for r in recs if r["shape"] == "elite" and r["lead"] == e and r["size"] == size
                      and (r["scale"], r["hp"]) == (s, h) and pos(r) == 1]
                if rs:
                    out.append(f"| {e} | {size} | x{s}, Health x{h} | {line(rs)} |")
    out.append("\n### Each pair of elites, middle of the band\n")
    out.append("| Elites | Slots | Setting | Lost | Worst encounter | Down | 2+ Down | Wounded | Rounds |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for lead in sorted({r["lead"] for r in recs if r["shape"] == "two elites"}):
        for size in SIZES:
            for s, h in SETS:
                rs = [r for r in recs if r["shape"] == "two elites" and r["lead"] == lead and r["size"] == size
                      and (r["scale"], r["hp"]) == (s, h)]
                if rs:
                    out.append(f"| {lead} | {size} | x{s}, Health x{h} | {line(rs)} |")
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-o", default="results/enemy_stats/boss_encounters.jsonl")
    ap.add_argument("--txt")
    ap.add_argument("-n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=41)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    {"run": run, "read": read}[a.cmd](a)


if __name__ == "__main__":
    main()
