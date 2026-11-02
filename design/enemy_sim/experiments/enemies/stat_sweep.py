"""Enemy base stats per Level, against the table targets (2026-11-02).

Per the designer: Slots stay as they are (a GM counts players, picks
enemies adding up to that many Slots, done). If on-level fights are off,
the enemy baseline per Level is what moves. This nudges every built
enemy's numbers by Level and reads the result the way baseline_check.py
does (the day standard, each fight of the day separately), for:

- Level 1: the sample parties at 75 XP (calibrate.py's Level 1 list);
- Levels 2 and 3: the normalized parties (party_mixes' spread, as in
  baseline_check.py);

plus four stand-ins at each Level. A config is a list of per-Level
nudges, applied to the enemy after it's built (so the roster rows,
archetypes and Abilities stay as they are):

    acc  Accuracy (main and backup attack)
    dmg  Damage on every damaging attack
    def  every Defense (Parry, Dodge, Vital, Mental, Vigilant)
    res  every Resist (Physical and elemental)
    hp   Health per Slot (a minion gets a third, rounded up, like the builder)
    hpx  Health multiplier (applied after hp)
    stk  stacks on a Hex/Shield Ally/Mend (EFFECT_STACKS etc.)

    python3 experiments/enemies/stat_sweep.py -L 1,2,3 -n 50 \\
        "as is=" "L3 dmg-1=3:dmg=-1" "all hp+2=1:hp=2;2:hp=2;3:hp=2"

`--up 1` plays every config one enemy Level up instead (the ladder's
rung): the nudges for the Level the enemy is built at apply.
"""
import argparse
import json
import math
import multiprocessing as mp
import os

import _paths  # noqa: E402,F401 (the simulator's core, a folder or two up)
import day_sim as ds  # noqa: E402
import sample_enemies as se  # noqa: E402
import tunables as T  # noqa: E402
import party_power as pp  # noqa: E402
import party_mixes as pm  # noqa: E402
import build_optimizer as bo  # noqa: E402
import baseline_check as bc  # noqa: E402
import calibrate  # noqa: E402

DEFS = ("parry", "dodge", "bodily", "mental", "vigilant")
L1_PARTIES = ("A", "B", "D", "T", "S", "U")


def parse(spec):
    """'3:dmg=-1,hp=2;2:acc=1' -> {3: {'dmg': -1, 'hp': 2}, 2: {'acc': 1}}."""
    out = {}
    for part in filter(None, (s.strip() for s in spec.split(";"))):
        lv, _, kvs = part.partition(":")
        # "3@Brute": only enemies whose name starts with Brute, at Level 3.
        lv, _, who = lv.partition("@")
        levels = [(int(x), who) if who else int(x) for x in lv.split("/")]
        for kv in filter(None, (s.strip() for s in kvs.split(","))):
            k, _, v = kv.partition("=")
            for L in levels:
                out.setdefault(L, {})[k.strip()] = float(v)
    return out


def _ceil_signed(x):
    return math.ceil(x) if x >= 0 else -math.ceil(-x)


def nudge(e, n):
    if not n:
        return e
    for prof in (e, e.get("backup")):
        if not prof:
            continue
        if prof.get("attack_damage"):
            prof["attack_damage"] = max(1, prof["attack_damage"] + int(n.get("dmg", 0)))
        if "accuracy" in prof:
            prof["accuracy"] += int(n.get("acc", 0))
    for d in DEFS:
        if e.get(d, -99) > -50:
            e[d] += int(n.get("def", 0))
    e["physres"] += int(n.get("res", 0))
    e["elemres"] += int(n.get("res", 0))
    hp = e["max_health"] + _ceil_signed(n.get("hp", 0) * T.SLOT_MULTIPLIER[e.get("slots", 1)])
    hp = max(1, math.ceil(hp * n.get("hpx", 1)))
    e["health"] = e["max_health"] = hp
    if n.get("stk") and e.get("kind") != "attack":
        e["effect_stacks"] = max(1, e["effect_stacks"] + int(n["stk"]))
    return e


_ORIG = {}


def install(nudges):
    get = _ORIG.setdefault("get_enemy", se.get_enemy)

    def get_enemy(name):
        e = get(name)
        nudge(e, nudges.get(e["level"]))
        for key, n in nudges.items():
            if isinstance(key, tuple) and key[0] == e["level"] and e["name"].startswith(key[1]):
                nudge(e, n)
        return e
    se.get_enemy = get_enemy


def groups(level):
    si = pp.STAND_IN[level]
    # Level 1's stand-in is the Baseline Tier 1 row as written (75 XP).
    out = [("stand-ins", [si] * 4, {si: ({"build": pp.stand_in(level)}, None)} if level > 1 else {})]
    if level == 1:
        for k in L1_PARTIES:
            out.append((k, calibrate.PARTIES[1][k], {}))
        return out
    norm = pm.normalized(level)
    for trio in bc.parties(level, 8):
        names, swaps = [], {}
        for arch in trio:
            row, b = norm[arch]
            names.append(row)
            swaps[row] = ({"build": b}, bo.choices_for(ds.party._rows()[row], b))
        out.append(("+".join(trio), names, swaps))
    return out


def _job(args):
    label, spec, level, gi, n, up, seed = args
    install(parse(spec))
    T.ENEMY_LEVEL_UP = up
    ds.set_mult(1.0)
    gname, names, swaps = groups(level)[gi]
    recs = ds.run(names, swaps, level, n, seed=seed)
    return label, level, gname, [r.get("per_fight", []) for r in recs]


def summarize(days_by_group):
    party_days = [d for g, days in days_by_group.items() if g != "stand-ins" for d in days]
    s = bc.stats(party_days)
    s["worst"] = min(bc.stats(days)["day"] for g, days in days_by_group.items() if g != "stand-ins")
    s["best"] = max(bc.stats(days)["day"] for g, days in days_by_group.items() if g != "stand-ins")
    s["standins"] = bc.stats(days_by_group["stand-ins"])["day"]
    s["mixes"] = by_mix(days_by_group)
    return s


def by_mix(days_by_group):
    """Fresh first fights only, per mix (the second starts hurt)."""
    out = {}
    for g, days in days_by_group.items():
        if g == "stand-ins":
            continue
        for d in days:
            if d:
                out.setdefault(d[0]["mix"], []).append([d[0]])
    return {m: bc.stats(v)[1] for m, v in out.items()}


def row(label, L, s):
    f1, f2 = s[1], s.get(2, {})
    return (f"{label:26s} L{L} days {s['day']:5.1f}% (worst {s['worst']:3.0f} best {s['best']:3.0f} si {s['standins']:3.0f})"
            f" | F1 lose {f1['lose']:4.1f} Down {f1['down']:3.0f} Wnd {f1['wounded']:3.0f} rds {f1['rounds']:.1f}"
            f" again {f1['again']:2.0f} | F2 lose {f2.get('lose', 0):4.1f} Down {f2.get('down', 0):3.0f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("configs", nargs="+", help="label=spec (spec may be empty)")
    ap.add_argument("-L", default="1,2,3")
    ap.add_argument("-n", type=int, default=50, help="days per mix per party")
    ap.add_argument("--up", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", help="append readings here (jsonl)")
    ap.add_argument("--mixes", action="store_true", help="also each mix's fresh first fights")
    a = ap.parse_args()
    levels = [int(x) for x in a.L.split(",")]
    configs = [c.partition("=")[::2] for c in a.configs]
    jobs = [(lab, spec, L, gi, a.n, a.up, a.seed) for lab, spec in configs for L in levels
            for gi in range(len(groups(L)))]
    res = {}
    with mp.Pool(a.j) as pool:
        for lab, L, g, days in pool.imap(_job, jobs):
            res.setdefault((lab, L), {})[g] = days
    for lab, spec in configs:
        for L in levels:
            s = summarize(res[(lab, L)])
            print(row(lab, L, s), flush=True)
            if a.mixes:
                for m, x in sorted(s["mixes"].items()):
                    print(f"      {m:12s} F1 lose {x['lose']:4.1f} Down {x['down']:3.0f} Wnd {x['wounded']:3.0f} "
                          f"rds {x['rounds']:.1f} again {x['again']:2.0f}")
            if a.o:
                with open(a.o, "a") as f:
                    f.write(json.dumps(dict(label=lab, spec=spec, level=L, up=a.up, n=a.n, stats=s)) + "\n")


if __name__ == "__main__":
    main()
