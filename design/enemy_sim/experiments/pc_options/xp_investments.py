"""What a few more XP buy when the stakes are high (2026-11-10).

Per the designer: take the band's middle builds, give one character 3 or
6 more XP spent one way (a rank, a Stat point, a Battle Maneuver built
around Crippled and the like), and play days hard enough that the party
loses a quarter or more of them. The benchmark is how much each
investment keeps the party from losing.

Days are day_sim's (two fights, care between, the optimizer's --score day
footing), the manual's encounters at the Level with `--extra` more
standard attackers each. Every option plays the same days as the base
(paired seeds). Each character in each middle party takes a turn as the
carrier; an option the character can't legally take (a prereq it misses)
is skipped for that character.

    python3 experiments/pc_options/xp_investments.py --calibrate -L 2   # days lost at +0..+3 Slots
    python3 experiments/pc_options/xp_investments.py -L 2 --extra 2 -n 50
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import sample_enemies as se  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

WEAPON_SKILLS = ("Acrobatics", "Archery", "Brawl", "Melee")
RIDERS = [("Wing Clip", "Crippled"), ("Hamstring", "Slowed"), ("Harrying", "Harried"),
          ("Battering", "Bleeding"), ("Distracting", "Taunted"), ("Half Guard", "Protected on self")]
FEATURE_PREREQ = {"Battering": ("Might", 2), "Distracting": ("Presence", 2)}


def register(level, extra):
    """The manual's encounters at `level`, `extra` more standard attackers
    each, as this run's day mixes."""
    T.ENEMY_LEVEL_UP = 0
    keys = []
    for i, m in enumerate(se.install_manual_mixes(level_into=level, build_level=level)):
        enc = list(se.ENCOUNTERS[level][m])
        ones = [x for x in enc if se.get_enemy(x).get("slots", 1) == 1 and se.get_enemy(x)["kind"] == "attack"]
        se.ENCOUNTERS[level][f"{m} +{extra}"] = enc + [ones[j % len(ones)] for j in range(extra)]
        keys.append(f"{m} +{extra}")
    se.CURRENT_MIXES = tuple(keys)


def raw(build, name):
    return int(build["skillPoints"].get(name, build["statPoints"].get(name, 0)))


def options(build, pc):
    """(label, XP, edit function) for one character. Each edit returns a
    changed copy of the build."""
    out = []
    atk = pc["attack_skill"]
    stat = T.PC_SKILL_STAT[atk]

    def rank(skill):
        r = int(build["skillPoints"][skill]) + 1
        return lambda b: (b["skillPoints"].__setitem__(skill, r), b)[1], r

    f, cost = rank(atk)
    out.append((f"{atk} +1 (Accuracy)", cost, f))
    dsk = max(("Acrobatics", "Brawl"), key=lambda s: party.skill_total(build["statPoints"], build["skillPoints"], s))
    if dsk != atk:
        f, cost = rank(dsk)
        out.append((f"{dsk} +1 (Dodge)", cost, f))
    if atk != "Melee":
        f, cost = rank("Melee")
        out.append(("Melee +1 (Parry)", cost, f))
    s = int(build["statPoints"][stat]) + 1
    out.append((f"{stat} +1 (Stat)", 2 * s, lambda b, s=s: (b["statPoints"].__setitem__(stat, s), b)[1]))
    best = max(raw(build, k) for k in WEAPON_SKILLS)
    for lvl in (1, 2):
        if best < lvl + 1:
            continue
        for feat, what in RIDERS:
            need = FEATURE_PREREQ.get(feat)
            if need and raw(build, need[0]) < need[1]:
                continue
            n = 3 * lvl
            out.append((f"Battle Maneuver L{lvl}: {feat} x{n} ({what})", 3 * lvl,
                        lambda b, lvl=lvl, feat=feat, n=n: (b["techniques"].append(
                            party._entry({"id": "T072", "level": lvl, "features": {feat: n}})), b)[1]))
        out.append((f"Battle Maneuver L{lvl}: Calculated x{lvl} (Good Luck)", 3 * lvl,
                    lambda b, lvl=lvl: (b["techniques"].append(
                        party._entry({"id": "T072", "level": lvl, "features": {"Calculated": lvl}})), b)[1]))
    return out


def cells(level):
    """(party index, seat, label, XP) for every legal option, plus the base."""
    rows = party._rows()
    out = []
    for gi, (gname, names, swaps) in enumerate(g for g in tc.groups(level, ps.MID[level]) if g[0] != "stand-ins"):
        out.append((gi, None, "base", 0))
        for seat, m in enumerate(names):
            build = swaps[m][0]["build"]
            pc = party.make_pc(m, 1, rows=rows, edits=swaps[m][0], row_changes=swaps[m][1])
            for label, xp, f in options(json.loads(json.dumps(build)), pc):
                out.append((gi, seat, label, xp))
    return out


def edited(level, gi, seat, label):
    gname, names, swaps = [g for g in tc.groups(level, ps.MID[level]) if g[0] != "stand-ins"][gi]
    swaps = dict(swaps)
    if seat is not None:
        m = names[seat]
        rows = party._rows()
        pc = party.make_pc(m, 1, rows=rows, edits=swaps[m][0], row_changes=swaps[m][1])
        build = json.loads(json.dumps(swaps[m][0]["build"]))
        f = dict((lb, fn) for lb, _, fn in options(build, pc))[label]
        b = f(build)
        party.load_sheet(rows[m], b, strict=False)  # stops on an export the sim can't load
        swaps[m] = ({"build": b}, swaps[m][1])
    return gname, names, swaps


def job(args):
    level, extra, cell, mi, k0, k1, seed = args
    register(level, extra)
    gi, seat, label, xp = cell
    gname, names, swaps = edited(level, gi, seat, label)
    rows = party._rows()
    out = []
    for k in range(k0, k1):
        rec, _ = ds.play_day(names, swaps, level, ds.day_mixes(mi, k), seed + 100_000 * mi + k, rows)
        out.append((bool(rec["lost"]), 0 if rec["lost"] else rec["fights"][-1]))
    return cell, out


def run(level, extra, n, cell_list, seed=0):
    jobs = [(level, extra, c, mi, k, min(n, k + 25), seed) for c in cell_list for mi in range(T.MANUAL_MIXES)
            for k in range(0, n, 25)]
    res = collections.defaultdict(list)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for i, (cell, out) in enumerate(pool.imap_unordered(job, jobs, chunksize=4)):
            res[cell] += out
            if i % 200 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)
    return res


def calibrate(a):
    base = [c for c in cells(a.L) if c[2] == "base"]
    for x in range(0, 4):
        res = run(a.L, x, a.n, base)
        lost = [d for c in base for d, _ in res[c]]
        print(f"Level {a.L}, +{x} Slots: days lost {100 * st.mean(lost):.1f}% "
              f"(per party: {', '.join(f'{100 * st.mean(d for d, _ in res[c]):.0f}' for c in base)})", flush=True)


def report(a, res, cl):
    base = {c[0]: res[c] for c in cl if c[2] == "base"}
    rows = collections.defaultdict(list)
    for c in cl:
        if c[2] == "base":
            continue
        b, t = base[c[0]], res[c]
        dl = 100 * (st.mean(d for d, _ in b) - st.mean(d for d, _ in t))  # points of days lost saved
        dh = st.mean(h for _, h in t) - st.mean(h for _, h in b)
        rows[c[2]].append((dl, dh, c[3], c))
    base_lost = 100 * st.mean(d for v in base.values() for d, _ in v)
    lines = [f"Level {a.L}, +{a.extra} Slots, {a.n} days a mix ({8 * a.n} a carrier); base days lost "
             f"{base_lost:.1f}%. Saved: points of days lost the investment takes off (higher is better), "
             "averaged over every carrier who can take it; per XP divides by its cost.", "",
             "| Investment | XP | Carriers | Days-lost points saved | Per XP | Health left after fight 2 | Best carrier |",
             "|---|---|---|---|---|---|---|"]
    order = sorted(rows.items(), key=lambda kv: -st.mean(x[0] for x in kv[1]) / max(1, st.mean(x[2] for x in kv[1])))
    for label, xs in order:
        dl, dh, xp = st.mean(x[0] for x in xs), st.mean(x[1] for x in xs), st.mean(x[2] for x in xs)
        best = max(xs, key=lambda x: x[0])
        gname = [g for g in tc.groups(a.L, ps.MID[a.L]) if g[0] != "stand-ins"][best[3][0]][1][best[3][1]]
        lines.append(f"| {label} | {xp:.1f} | {len(xs)} | {dl:+.1f} | {dl / xp:+.2f} | {dh:+.1f} | {gname} {best[0]:+.1f} |")
    text = "\n".join(lines)
    print(text)
    out = os.path.join(_paths.ROOT, "results", f"xp_investments_L{a.L}_x{a.extra}.txt")
    open(out, "w").write(text + "\n")
    json.dump([[list(c), res[c]] for c in cl], open(out.replace(".txt", ".json"), "w"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=2)
    ap.add_argument("--extra", type=int, default=2)
    ap.add_argument("-n", type=int, default=50, help="days a mix")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--list", action="store_true", help="just list the cells")
    a = ap.parse_args()
    if a.calibrate:
        calibrate(a)
    elif a.list:
        for c in cells(a.L):
            print(c)
    else:
        cl = cells(a.L)
        print(len(cl), "cells", flush=True)
        report(a, run(a.L, a.extra, a.n, cl), cl)
