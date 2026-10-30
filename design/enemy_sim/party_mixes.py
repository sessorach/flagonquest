"""Every party of four from the ten archetypes, at the same combat XP (2026-10-30).

Per the designer: try every mix, keep the stronger ones and move them on.
Round 1 plays all 210 parties of the normalized builds
(builds/normalized/, combat_xp.COMBAT_BUDGET) at their own enemy Level
and one up, with scorecard.py's counters. Round 2 takes the five
strongest parties and five from the middle (the most even ones, by how
close the four members' damage shares are) and plays every lineup of
each with stand-ins swapped in (16 a party, one Level up): each member's
Shapley value and each pair's interaction (party_power.shapley_values).
Then the flags (scorecard.FLAGS).

    python3 party_mixes.py -L 3 -n 250 -o mixes_l3.json
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party  # noqa: E402
import build_optimizer as bo  # noqa: E402
import combat_xp  # noqa: E402
import party_power as pp  # noqa: E402
import resume  # noqa: E402
import scorecard as sc  # noqa: E402

TOP, MIDDLE = 5, 5


def normalized(level):
    out = {}
    for arch in bo.ARCHES:
        path = os.path.join(bo.HERE, "builds", "normalized", f"{arch.lower()}_l{level}_c{combat_xp.COMBAT_BUDGET[level]}.json")
        out[arch] = (bo.row_name(arch, level), party.read_build(path))
    return out


def run_jobs(part, jobs, j):
    todo = [k for k in jobs if list(k) not in part]
    with mp.Pool(j) as pool:
        for k, v in zip(todo, pool.imap(sc.play, [jobs[k] for k in todo])):
            part.add(list(k), v)
    return {_tup(json.loads(k)): v for k, v in part.got.items()}


def _tup(x):
    return tuple(_tup(y) for y in x) if isinstance(x, list) else x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=250, help="day_sim.run's n (it plays 4n days)")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    L, n = a.L, a.n
    B = normalized(L)
    archs = sorted(B)
    mixes = list(itertools.combinations(archs, 4))
    part = resume.Partial(a.o + ".partial")
    jobs = {}
    for up in (0, 1):
        jobs[("base", up)] = ([(None, None)] * 4, L, up, n, 0)
        for m in mixes:
            jobs[("mix",) + m + (up,)] = ([B[x] for x in m], L, up, n, 0)
    R = run_jobs(part, jobs, a.j)

    def rate(k):
        return R[k]["won"] / R[k]["days"]
    table = []
    for m in mixes:
        own = R[("mix",) + m + (0,)]
        tot = sum(s["dmg_out"] for s in own["seats"])
        shares = [s["dmg_out"] / max(1, tot) for s in own["seats"]]
        table.append(dict(party=list(m), up=rate(("mix",) + m + (1,)), own=rate(("mix",) + m + (0,)),
                          walkover=own["trivial"] / own["fights"], dmg_share=dict(zip(m, shares)),
                          hits_share={x: s["hits_in"] / max(1, sum(t["hits_in"] for t in own["seats"]))
                                      for x, s in zip(m, own["seats"])},
                          downs_per_10={x: 10 * s["downed"] / own["days"] for x, s in zip(m, own["seats"])}))
    table.sort(key=lambda r: -r["up"])
    # Each archetype across every party it's in: its average days won one up.
    by_arch = {x: st.mean(r["up"] for r in table if x in r["party"]) for x in archs}
    # Round 2: the strongest, and the most even of the middle third.
    top = table[:TOP]
    third = len(table) // 3
    middle = sorted(table[third:2 * third], key=lambda r: st.pstdev(r["dmg_share"].values()))[:MIDDLE]
    picked = top + middle
    jobs = {}
    for r in picked:
        m = tuple(r["party"])
        for k in range(5):
            for keep in itertools.combinations(range(4), k):
                seats = [B[m[i]] if i in keep else (None, None) for i in range(4)]
                key = ("lineup", tuple(sorted(m[i] for i in keep)), 1)
                jobs[key] = (seats, L, 1, n, 0)
    R = run_jobs(part, jobs, a.j)
    rounds2 = []
    for r in picked:
        m = tuple(r["party"])
        v = {frozenset(keep): rate(("lineup", tuple(sorted(m[i] for i in keep)), 1))
             for k in range(5) for keep in itertools.combinations(range(4), k)}
        phi, inter = pp.shapley_values(v, 4)
        gain = v[frozenset(range(4))] - v[frozenset()]
        rounds2.append(dict(party=list(m), kind="top" if r in top else "middle", up=r["up"], gain=100 * gain,
                            shapley={m[i]: 100 * x for i, x in phi.items()},
                            pairs={f"{m[i]}+{m[j]}": 100 * x for (i, j), x in inter.items()}))
    F = sc.FLAGS
    flags = []
    for r in table:
        k = "+".join(r["party"])
        if r["up"] >= F["gm_pressure"]:
            flags.append((k, "GM pressure", f"wins {100 * r['up']:.0f}% one Level up"))
        if r["walkover"] >= F["walkover"]:
            flags.append((k, "walkovers", f"{100 * r['walkover']:.0f}% of first fights"))
        for x in r["party"]:
            if r["dmg_share"][x] > F["dmg_share"]:
                flags.append((k, "extreme: damage", f"{x} {100 * r['dmg_share'][x]:.0f}%"))
            if r["hits_share"][x] > F["hits_share"] and r["downs_per_10"][x] < F["downs_per_10"]:
                flags.append((k, "extreme: soaks", f"{x} {100 * r['hits_share'][x]:.0f}% of hits"))
    for r in rounds2:
        k = "+".join(r["party"])
        for x, c in r["shapley"].items():
            if c < F["dead_weight"]:
                flags.append((k, "doesn't pull weight", f"{x} {c:+.0f}"))
            if c > F["carry"] or (r["gain"] > 0 and c > r["gain"] / 2):
                flags.append((k, "carries", f"{x} {c:+.0f} of the party's {r['gain']:+.0f}"))
        for p, c in r["pairs"].items():
            if c <= F["eclipse"]:
                flags.append((k, "eclipse", f"{p} {c:+.0f}"))
    out = dict(level=L, days_per_job=R[("base", 1)]["days"], base=dict(up=rate(("base", 1)), own=rate(("base", 0))),
               by_arch=by_arch, mixes=table, round2=rounds2, flags=flags)
    with open(a.o, "w") as f:
        json.dump(out, f, indent=1)
    part.finish()
    print(f"stand-ins: {100 * out['base']['own']:.0f}% own Level, {100 * out['base']['up']:.0f}% one up")
    print("one Level up, averaged over the 84 parties each archetype is in:")
    for x in sorted(archs, key=lambda x: -by_arch[x]):
        print(f"  {x:10s} {100 * by_arch[x]:.0f}%")
    for r in table[:5] + table[-3:]:
        print(f"{'+'.join(r['party']):40s} up {100 * r['up']:3.0f}%  own {100 * r['own']:3.0f}%  walkover {100 * r['walkover']:.0f}%")
    for r in rounds2:
        print(r["kind"], "+".join(r["party"]), f"gain {r['gain']:+.0f}",
              " ".join(f"{x} {c:+.0f}" for x, c in r["shapley"].items()))
    for f in flags:
        print("FLAG", *f)


if __name__ == "__main__":
    main()
