"""A scorecard for builds at the same combat XP (2026-10-30, proof of concept).

The designer's goals, each read off days played (day_sim.py) with the
counters tunables.TRACK_SHARES turns on:

- Choices about equally useful per XP: every build here spends the same
  combat XP (combat_xp.COMBAT_BUDGET), so its contribution (days won one
  enemy Level up with three party_power stand-ins, minus four stand-ins)
  compares directly. Per-XP outliers: more than twice or under half the
  median contribution.
- No player useless: contribution under -10 points.
- Nobody forces the GM to redo the numbers: a party that wins half its
  days one Level up (GM pressure), or wins half its first fights at its
  own Level in two rounds with nobody Wounded (walkovers).
- No eclipsing: two builds together worth 10 points less than each alone
  says (the pair interaction, with two stand-ins).
- Extremes: over half the party's damage, or over 40% of the hits taken
  with under one Down in ten days.

Builds: for each archetype in --runs (build_optimizer.py --start
normalized results), the normalized start and the search's best. Every
job is seeded the same, so differences between builds aren't fight luck.

    python3 scorecard.py -L 3 -n 500 --runs hall_of_fame/runs_levelup -o out.json
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import random
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party, tunables as T  # noqa: E402
import day_sim  # noqa: E402
import build_optimizer as bo  # noqa: E402
import party_power as pp  # noqa: E402
import resume  # noqa: E402

FLAGS = dict(gm_pressure=0.5, walkover=0.5, dead_weight=-10, carry=20, eclipse=-10, dmg_share=0.5,
             hits_share=0.4, downs_per_10=1.0)
KEYS = ("dmg_out", "heal_out", "dmg_in", "hits_in", "downed")


def play(args):
    """Days with `seats` (row name, build or None for a stand-in)."""
    seats, level, up, n, seed = args
    rows = party._rows()
    si = pp.STAND_IN[level]
    names, swaps = [], {si: ({"build": pp.stand_in(level)}, None)}
    for name, b in seats:
        if b is None:
            names.append(si)
        else:
            names.append(name)
            swaps[name] = ({"build": b}, bo.choices_for(rows[name], b))
    T.TRACK_SHARES = True
    T.ENEMY_LEVEL_UP = up
    day_sim.set_mult(1.0)
    try:
        recs = day_sim.run(names, swaps, level, n, seed=seed)
    finally:
        T.ENEMY_LEVEL_UP = 0
    first = [r["first"] for r in recs if r.get("first")]
    out = dict(won=sum(not r["lost"] for r in recs), days=len(recs),
               trivial=sum(1 for f in first if f["won"] and f["rounds"] <= 2 and not f["wounded"]),
               fights=len(first), seats=[{k: 0 for k in KEYS} for _ in names])
    for r in recs:
        for tot, sl in zip(out["seats"], r.get("slots") or ()):
            for k in KEYS:
                tot[k] += sl[k]
    return out


def builds(runs, level):
    """{arch: {"normalized": build, "optimized": build}} and each one's row.
    `runs`: one or more result folders (searches from different starts or
    seeds); the optimized build is the best validated across all of them
    (every search validates on the same fresh days), and the normalized one
    the start of a --start normalized search."""
    out = {}
    for arch in bo.ARCHES:
        res = []
        for d in runs:
            path = os.path.join(d, f"{arch.lower()}_l{level}.json")
            if os.path.exists(path):
                res += [dict(r, run=d) for r in json.load(open(path))]
        if not res:
            continue
        best = max(res, key=lambda r: r["validated"])
        norm = next((r["start_build"] for r in res if r.get("start") == "normalized"), None)
        if norm is None:
            continue
        out[arch] = dict(row=best["name"], normalized=norm, optimized=best["build"],
                         search=dict(validated=best["validated"], start=best.get("start"), run=best["run"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=500, help="day_sim.run's n (it plays 4n days)")
    ap.add_argument("--runs", required=True, help="result folder(s), comma-separated")
    ap.add_argument("--parties", type=int, default=6, help="random four-archetype parties, besides the top four")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    bo.START = "normalized"  # choices_for clears a dropped Unmodeled Technique
    L, n = a.L, a.n
    B = builds(a.runs.split(","), L)
    archs = sorted(B)
    stand = [(None, None)] * 4

    def seat(arch, kind):
        return (B[arch]["row"], B[arch][kind])
    jobs = {}
    for up in (0, 1):
        jobs[("base", up)] = (stand, L, up, n, 0)
        for arch in archs:
            for kind in ("normalized", "optimized"):
                jobs[("single", arch, kind, up)] = ([seat(arch, kind)] + stand[:3], L, up, n, 0)
    # Two Levels up too: one up, the strongest builds win nearly every day
    # alone, and a pair can't add what each adds (the 100% ceiling).
    jobs[("base", 2)] = (stand, L, 2, n, 0)
    for arch in archs:
        jobs[("single", arch, "optimized", 2)] = ([seat(arch, "optimized")] + stand[:3], L, 2, n, 0)
    for x, y in itertools.combinations(archs, 2):
        for up in (1, 2):
            jobs[("pair", x, y, up)] = ([seat(x, "optimized"), seat(y, "optimized")] + stand[:2], L, up, n, 0)
    part = resume.Partial(a.o + ".partial")
    todo = [k for k in jobs if list(k) not in part]
    with mp.Pool(a.j) as pool:
        for k, v in zip(todo, pool.imap(play, [jobs[k] for k in todo])):
            part.add(list(k), v)
    R = {tuple(json.loads(k)): v for k, v in part.got.items()}

    def rate(k):
        return R[k]["won"] / R[k]["days"]
    # The parties: the four best optimized builds by contribution, and a few
    # random four-archetype mixes.
    contrib = {arch: rate(("single", arch, "optimized", 1)) - rate(("base", 1)) for arch in archs}
    top = sorted(archs, key=lambda x: -contrib[x])[:4]
    rng = random.Random(1)
    mixes = ([tuple(sorted(top))] + [tuple(sorted(rng.sample(archs, 4))) for _ in range(a.parties)]
             if len(archs) >= 4 else [])
    pjobs = {}
    for m in dict.fromkeys(mixes):
        for up in (0, 1):
            pjobs[("party",) + m + (up,)] = ([seat(x, "optimized") for x in m], L, up, n, 0)
    todo = [k for k in pjobs if list(k) not in part]
    with mp.Pool(a.j) as pool:
        for k, v in zip(todo, pool.imap(play, [pjobs[k] for k in todo])):
            part.add(list(k), v)
    R = {tuple(json.loads(k)): v for k, v in part.got.items()}

    base_up, base_own = rate(("base", 1)), rate(("base", 0))
    card = {}
    for arch in archs:
        for kind in ("normalized", "optimized"):
            up_k, own_k = ("single", arch, kind, 1), ("single", arch, kind, 0)
            own = R[own_k]
            seat0 = own["seats"][0]
            tot = {k: sum(s[k] for s in own["seats"]) for k in KEYS}
            c = dict(up=rate(up_k), own=rate(own_k), contribution=100 * (rate(up_k) - base_up),
                     up2=rate(("single", arch, kind, 2)) if kind == "optimized" else None,
                     contribution_own=100 * (rate(own_k) - base_own),
                     walkover=own["trivial"] / own["fights"],
                     dmg_share=seat0["dmg_out"] / max(1, tot["dmg_out"]),
                     heal_share=seat0["heal_out"] / max(1, tot["heal_out"]),
                     hits_share=seat0["hits_in"] / max(1, tot["hits_in"]),
                     downs_per_10=10 * seat0["downed"] / own["days"])
            card[f"{arch}/{kind}"] = c
    med = st.median(card[f"{x}/optimized"]["contribution"] for x in archs)
    pairs, pairs2 = {}, {}
    for x, y in itertools.combinations(archs, 2):
        for up, d in ((1, pairs), (2, pairs2)):
            d[f"{x}+{y}"] = 100 * (rate(("pair", x, y, up)) - rate(("single", x, "optimized", up))
                                   - rate(("single", y, "optimized", up)) + rate(("base", up)))
    parties = {}
    for k in pjobs:
        if k[-1] == 1:
            m = k[1:-1]
            own = R[("party",) + m + (0,)]
            tot = {kk: sum(s[kk] for s in own["seats"]) for kk in KEYS}
            parties["+".join(m)] = dict(up=rate(k), own=rate(("party",) + m + (0,)),
                                        walkover=own["trivial"] / own["fights"],
                                        dmg_share={x: s["dmg_out"] / max(1, tot["dmg_out"]) for x, s in zip(m, own["seats"])},
                                        hits_share={x: s["hits_in"] / max(1, tot["hits_in"]) for x, s in zip(m, own["seats"])},
                                        downs_per_10={x: 10 * s["downed"] / own["days"] for x, s in zip(m, own["seats"])})
    flags = []
    for key, c in card.items():
        if c["up"] >= FLAGS["gm_pressure"]:
            flags.append((key, "GM pressure", f"wins {100 * c['up']:.0f}% one Level up with three stand-ins"))
        if c["contribution"] < FLAGS["dead_weight"]:
            flags.append((key, "doesn't pull weight", f"{c['contribution']:+.0f} points"))
        if c["contribution"] > FLAGS["carry"]:
            flags.append((key, "carries", f"{c['contribution']:+.0f} points"))
        if med > 0 and (c["contribution"] > 2 * med or c["contribution"] < med / 2):
            flags.append((key, "per-XP outlier", f"{c['contribution']:+.0f} vs median {med:+.0f}"))
        if c["walkover"] >= FLAGS["walkover"]:
            flags.append((key, "walkovers", f"{100 * c['walkover']:.0f}% of first fights"))
        if c["dmg_share"] > FLAGS["dmg_share"]:
            flags.append((key, "extreme: damage", f"{100 * c['dmg_share']:.0f}% of the party's damage"))
        if c["hits_share"] > FLAGS["hits_share"] and c["downs_per_10"] < FLAGS["downs_per_10"]:
            flags.append((key, "extreme: soaks", f"{100 * c['hits_share']:.0f}% of hits, {c['downs_per_10']:.1f} Downs per 10 days"))
    for k, v in pairs2.items():
        if v <= FLAGS["eclipse"]:
            flags.append((k, "eclipse (two Levels up)", f"{v:+.0f} points together"))
    for k, p in parties.items():
        if p["up"] >= FLAGS["gm_pressure"]:
            flags.append((k, "GM pressure (party)", f"wins {100 * p['up']:.0f}% one Level up"))
        if p["walkover"] >= FLAGS["walkover"]:
            flags.append((k, "walkovers (party)", f"{100 * p['walkover']:.0f}% of first fights"))
        for x in k.split("+"):
            if p["dmg_share"][x] > FLAGS["dmg_share"]:
                flags.append((k, "extreme: damage (party)", f"{x} {100 * p['dmg_share'][x]:.0f}%"))
            if p["hits_share"][x] > FLAGS["hits_share"] and p["downs_per_10"][x] < FLAGS["downs_per_10"]:
                flags.append((k, "extreme: soaks (party)", f"{x} {100 * p['hits_share'][x]:.0f}% of hits"))
    out = dict(level=L, days_per_job=R[("base", 1)]["days"], base=dict(up=base_up, own=base_own,
               walkover=R[("base", 0)]["trivial"] / R[("base", 0)]["fights"]),
               base_up2=rate(("base", 2)), median_contribution=med, card=card, pairs=pairs, pairs_two_up=pairs2,
               parties=parties, flags=flags,
               builds={x: B[x] for x in archs})
    with open(a.o, "w") as f:
        json.dump(out, f, indent=1)
    part.finish()
    print(f"stand-ins: {100 * base_own:.0f}% own Level, {100 * base_up:.0f}% one up")
    for key, c in sorted(card.items(), key=lambda kv: -kv[1]["contribution"]):
        print(f"{key:24s} up {100 * c['up']:3.0f}%  own {100 * c['own']:3.0f}%  contrib {c['contribution']:+4.0f}  "
              f"dmg {100 * c['dmg_share']:3.0f}%  heal {100 * c['heal_share']:3.0f}%  hits {100 * c['hits_share']:3.0f}%  "
              f"downs/10 {c['downs_per_10']:.1f}  walkover {100 * c['walkover']:.0f}%")
    for f in flags:
        print("FLAG", *f)


if __name__ == "__main__":
    main()
