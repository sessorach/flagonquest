"""Every size on the defaults, minions included (2026-11-06).

Per the designer: one size table (points and Health by Slots; the 4-Slot
solo boss's two turns the one special case; no extra Health for an elite
leading a boss fight), tested across the board. Sizes now: minion (0.5)
the Level's points and a third of the Health, standard (1), elite (2)
twice the points and 2.5 times the Health, solo boss (4) twice the points,
4 times the Health and two turns. Minions also at 0.4 and 0.5 of the
Health. Besides the manual's elites, three test-only ones built the
manual's way (BigPicks, offense only): an Elite Sharpshooter, a Storm
Magus and a Black Knight, a Defender in Heavy armor, to see whether the
Defense cap holds on a big Defender. Companions are fixed draws per
Level. Every party in the middle of its band (and at the low and high
points on the defaults), Levels 1-5, 60 fresh fights each, results to a
jsonl a rerun resumes.

    python3 experiments/enemies/size_check.py run
    python3 experiments/enemies/size_check.py read --txt results/enemy_stats/size_check.txt
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import random
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import game_data  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import bands  # noqa: E402

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


BASE = dict(BackupAction="", MainEffect="", WeakDefense="", Concept="test only")
TEST_ELITES = {
    "Elite Sharpshooter": dict(BASE, Slots="2", Role="Striker", Action="Heavy Bow", Armor="Light",
                               StrongDefense="Dodge", BattleTactic="Assassin",
                               PrunedPicks="Accuracy +1; Enhanced Range; Strike (Vulnerable); Strike (Vulnerable)",
                               PrunedExtra="Strike (Crippling); Strike (Crippling)",
                               BigPicks="Accuracy +1; Damage +1; Strike (Crippling); Strike (Crippling); "
                                        "Strike (Vulnerable); Strike (Vulnerable); Enhanced Reflexes; Accuracy +1"),
    "Storm Magus": dict(BASE, Slots="2", Role="Strategist", Action="Ranged Spell", Armor="Unarmored",
                        StrongDefense="Mental", BattleTactic="Hit Whatever",
                        PrunedPicks="Powerful Spell; Accuracy +1; Strike (Frightening); Strike (Frightening)",
                        PrunedExtra="Strike (Vulnerable); Strike (Vulnerable)",
                        BigPicks="Strike (Frightening); Strike (Frightening); Accuracy +1; Strike (Vulnerable); "
                                 "Strike (Vulnerable); Enhanced Range; Attunement (Fire); Enhanced Reflexes; Accuracy +1"),
    "Black Knight": dict(BASE, Slots="2", Role="Defender", Action="Heavy Weapon and Shield", Armor="Heavy",
                         StrongDefense="Vital", BattleTactic="Hold the Line",
                         # Omniguard dropped 2026-11-06: elites can't take it.
                         PrunedPicks="Strike (Taunting); Strike (Taunting); Sturdy",
                         PrunedExtra="Dodge +1",
                         BigPicks="Accuracy +1; Damage +1; Strike (Crippling); Strike (Crippling); Action (Taunting); "
                                  "Strike (Battering); Accuracy +1"),
}
ELITES = ["Gravel Ogre", "Coven Matriarch", "Elite Sharpshooter", "Storm Magus", "Black Knight"]
MINION_HP = [1 / 3, 0.4, 0.5]
_ORIG_ROW = se._manual_row


def install():
    if getattr(se, "_size_check", False):
        return
    se._size_check = True

    def manual_row(name):
        base, _, level = name.partition("@")
        if base in TEST_ELITES:
            return dict(TEST_ELITES[base], Name=name, Level=level, AttackTier="primary", Abilities="",
                        HealthBonus="", FightingStyle="None", PrunedAction=TEST_ELITES[base]["Action"],
                        Roster="FALSE")
        return _ORIG_ROW(name)
    se._manual_row = manual_row


def minions():
    return [n for n in se.manual_names() if se.get_enemy(f"{n}@3").get("slots") == 0.5]


def minion_draws(level, n, k=4, seed=13):
    rng = random.Random(seed * 1000 + level * 10 + n)
    pool, out = minions(), []
    fixed = [tuple([m] * n) for m in pool] if n == 8 else []
    out += fixed
    while len(out) < len(fixed) + k:
        d = tuple(sorted(rng.choice(pool) for _ in range(n)))
        if d not in out:
            out.append(d)
    return out


def encounters(L):
    out = []
    for comp in draws(L, 4):
        out.append(("standard", "Four standard", [*comp]))
    for d in minion_draws(L, 8):
        out.append(("minion", "Eight minions", [*d]))
    for d, comp in zip(minion_draws(L, 4), draws(L, 2)):
        out.append(("minion", "Four minions + two standard", [*d, *comp]))
    for d, comp in zip(minion_draws(L, 2), draws(L, 3)):
        out.append(("minion", "Two minions + three standard", [*d, *comp]))
    for e in ELITES:
        for comp in draws(L, 2):
            out.append(("elite", f"{e} + two standard", [e, *comp]))
        if e != "Coven Matriarch":  # two supports: no attacker at all
            out.append(("elite", f"Two {e}s", [e, e]))
        for d, comp in zip(minion_draws(L, 2, k=2), draws(L, 1, k=2)):
            out.append(("elite+minion", f"{e} + two minions + one standard", [e, *d, *comp]))
    for pair in (("Gravel Ogre", "Coven Matriarch"), ("Gravel Ogre", "Elite Sharpshooter"),
                 ("Elite Sharpshooter", "Storm Magus")):
        out.append(("elite", f"{pair[0]} + {pair[1]}", list(pair)))
    if L >= 3:
        out.append(("solo", "Solo Brute Warlord", ["Brute Warlord"]))
    return out


LEVELS = [1, 2, 3, 4, 5]


KINDS = []  # empty: every kind


def cases():
    out = []
    for L in LEVELS:
        for kind, label, enc in encounters(L):
            if KINDS and kind not in KINDS:
                continue
            hps = MINION_HP if "minion" in kind else [MINION_HP[0]]
            for h in hps:
                out.append(dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(h, 3)))
    return out


EXTRA = [None]


def _job(args):
    c, budget, gi, n = args
    install()
    if EXTRA[0] is not None:
        T.V3_PRUNED_EXTRA = EXTRA[0]
    T.ENEMY_LEVEL_UP = 0
    T.V3_MINION_HEALTH = c["minion_hp"]
    L = c["level"]
    gname, pn, sw = bands.groups(L, budget)[gi]
    se.ENCOUNTERS.setdefault(min(L, 3), {})["_t"] = [f"{x}@{L}" for x in c["enc"]]
    rows = party._rows()
    out = collections.Counter()
    for k in range(n):
        rec, _ = ds.play_day(pn, sw, min(L, 3), ("_t",), 41 + 1000 * k, rows)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["down"] += f["downs"] > 0
        out["down2"] += f["downs"] > 1
        out["rounds"] += f["rounds"]
    pos = 1 if L == 1 else bands.POINTS[L].index(budget)
    return dict(c, pos=pos, party=gname, **{k: out[k] / n for k in ("won", "down", "down2", "rounds")})


def key(r):
    return (r["level"], r["label"], "|".join(r["enc"]), r["minion_hp"], r["pos"], r["party"])


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {key(r) for r in map(json.loads, open(a.o)) if r}
    jobs = []
    for c in cases():
        L = c["level"]
        pts = [bands.MID[L]] if L == 1 or c["minion_hp"] != round(MINION_HP[0], 3) else list(bands.POINTS[L])
        for b in pts:
            pos = 1 if L == 1 else bands.POINTS[L].index(b)
            for gi, (gname, _, _) in enumerate(bands.groups(L, b)):
                if (L, c["label"], "|".join(c["enc"]), c["minion_hp"], pos, gname) not in done:
                    jobs.append((c, b, gi, a.n))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j, maxtasksperchild=50) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=2)):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
            if i % 500 == 0:
                print(i, flush=True)


def read(a):
    recs = [json.loads(l) for l in open(a.o) if l.strip()]
    labels = list(dict.fromkeys(r["label"] for r in sorted(recs, key=lambda r: r["level"])))
    out = ["| Encounter | Minion Health | Lost (worst draw) | Down | 2+ Down | Rounds | By Level: lost / Down | Low / high band lost |",
           "|---|---|---|---|---|---|---|---|"]
    for label in labels:
        for h in sorted({r["minion_hp"] for r in recs if r["label"] == label}):
            rs = [r for r in recs if r["label"] == label and r["minion_hp"] == h]
            mid = [r for r in rs if r["pos"] == 1]
            if not mid:
                continue
            by_enc = collections.defaultdict(list)
            for r in mid:
                by_enc[(r["level"], "|".join(r["enc"]))].append(1 - r["won"])
            byL = " ".join(f"L{L} {100 * (1 - st.mean(r['won'] for r in mid if r['level'] == L)):.0f}/"
                           f"{100 * st.mean(r['down'] for r in mid if r['level'] == L):.0f}"
                           for L in (1, 2, 3, 4, 5) if any(r["level"] == L for r in mid))
            lo = [r for r in rs if r["pos"] == 0]
            hi = [r for r in rs if r["pos"] == 2]
            band = (f"{100 * (1 - st.mean(r['won'] for r in lo)):.0f}% / {100 * (1 - st.mean(r['won'] for r in hi)):.0f}%"
                    if lo and hi else "-")
            has_minion = any("minion" in r["kind"] for r in rs)
            out.append(f"| {label} | {f'{h:.2f}' if has_minion else '-'} | "
                       f"{100 * (1 - st.mean(r['won'] for r in mid)):.1f}% ({100 * max(st.mean(v) for v in by_enc.values()):.0f}%) | "
                       f"{100 * st.mean(r['down'] for r in mid):.0f}% | {100 * st.mean(r['down2'] for r in mid):.0f}% | "
                       f"{st.mean(r['rounds'] for r in mid):.1f} | {byL} | {band} |")
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-o", default="results/enemy_stats/size_check.jsonl")
    ap.add_argument("--txt")
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("-L", default="1,2,3,4,5", help="Levels to run")
    ap.add_argument("--kinds", default="", help="encounter kinds to run (standard, minion, elite, elite+minion, solo)")
    ap.add_argument("--extra", help="the Level extra points, '1:0/2:2/3:4/4:4/5:4'")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    LEVELS[:] = [int(x) for x in a.L.split(",")]
    KINDS[:] = [k for k in a.kinds.split(",") if k]
    if a.extra:
        EXTRA[0] = {int(L): int(n) for L, n in (x.split(":") for x in a.extra.split("/"))}
    {"run": run, "read": read}[a.cmd](a)


if __name__ == "__main__":
    main()
