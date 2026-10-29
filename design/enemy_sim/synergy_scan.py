"""Which pairs are worth more, or less, together than apart? (2026-10-28)

Per the designer: look for combinations with an outsized synergy, on one
character or across the party, so they can be watched for in future
design. A single-item test (technique_pass.py) can't see them.

Synergy for a pair is what the pair is worth on top of the build, less
what each one is worth alone, all three on the same fights (party Health
left at enemy Health x1.75, Level 3, the technique_pass setup):

    synergy = v(A and B) - v(A) - v(B)

Positive: more together. Negative: they get in each other's way (or
cover the same need). What's paired:

- on one character: each host's best single additions by the broad pass
  (technique_pass.csv's "free" reading, Styles counting one at a time),
  in every pair, with one Style at most;
- across the party: each host's two best additions, paired with another
  party member's;
- a short list of pairs already suspected (TARGETED). The War Magic ones
  ("W:...") each rebuild the same copy, so for them the three readings
  (each copy, and the copy with both) matter more than the synergy sum.

    python3 synergy_scan.py -n 500           # everything
    python3 synergy_scan.py --top 6 -n 100   # a quick look
"""
import argparse
import csv
import itertools
import math
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import technique_pass as tp  # noqa: E402
import party  # noqa: E402
import game_data  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
# (host, A, B): each an add spec, a Technique ID or a War Magic copy
# rework ("W:<features>"): Beornhard's first War Magic copy rebuilt.
TARGETED = [
    ("Beornhard (L3)", "W:Lance=1,Sanguine=1,Destructive=1", "W:Lance=1,Reign of Blood=1,Destructive=1"),
    ("Jackal (L3)", "T074", "T129"),        # Feint, then Disciple of the Flowing Hand's Bad Luck
    ("Felix (L3, proposed)", "T074", "T171"),  # Feint and Rending Claws (Harried stackers)
    ("Hilde (L3)", "T019", "T014"),          # Toughened Resolve and Toughened Body
    ("Carrick (L3)", "T019", "T019"),        # Toughened Resolve twice
    ("Hanforth (L3)", "T110", "T086"),       # Lifeline and Bark Turns the Blade
]


def adds_for(host, items):
    """The fit for adding `items` (IDs) to `host`, free; a Style replaces
    the host's own. None if it won't fit."""
    rows = party._rows()
    b = party.read_build(rows[host]["Build"])
    add = [{"id": t, "level": game_data.fixed_level(t) or (game_data.level_range(t) or (1, 1))[0]} for t in items]
    styles = [t for t in items if "Style" in (game_data.techniques()[t].get("Tags") or "")]
    if len(styles) > 1:
        return None
    rem = [{"id": t["id"], "copy": 1} for t in tp.styles_of(b)] if styles else []
    try:
        free, _, bought = party.fit(b, add=add, remove=rem, free=True)
    except party.BuildError:
        return None
    return free


def rework(host, spec):
    """'W:Lance=1,...': the host's first War Magic copy with these Features."""
    rows = party._rows()
    b = party.read_build(rows[host]["Build"])
    feats = {k: int(v) for k, v in (x.split("=") for x in spec[2:].split(","))}
    return feats


def evaluate(args):
    host, label, items, n = args
    key = tp.HOSTS[host]
    rows = party._rows()
    if any(i.startswith("W:") for i in items):
        b = party.read_build(rows[host]["Build"])
        feats = {}
        for i in items:
            feats.update({k: max(feats.get(k, 0), v) for k, v in rework(host, i).items()})
        lvl = 3 if sum(feats.values()) > 3 else 2
        build = party.apply_edits(b, {"replace": [{"id": "T120", "copy": 1, "level": lvl, "features": feats}]})
    else:
        build = adds_for(host, items)
        if build is None:
            return host, label, None
    try:
        res = tp.run(tp.PARTIES[key], host, {"build": build}, n, row_changes=tp.choices_for(rows[host], build))[0]
    except party.BuildError:
        return host, label, None
    return host, label, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=500)
    ap.add_argument("--top", type=int, default=12, help="best single additions per host to pair")
    ap.add_argument("--cross", type=int, default=2, help="additions per host for cross-party pairs")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("--pass-csv", default=os.path.join(HERE, "technique_pass.csv"))
    ap.add_argument("-o", default=os.path.join(HERE, "synergy_scan.csv"))
    a = ap.parse_args()
    tp._init()
    rows = list(csv.DictReader(open(a.pass_csv)))
    best = {}
    for r in rows:
        if r["kind"] == "technique" and r["mode"].startswith("add") and r["free"] not in ("", None):
            best.setdefault(r["host"], []).append((float(r["free"]), r["id"]))
    for h in best:
        best[h] = [t for v, t in sorted(best[h], reverse=True) if v > 0]
    jobs = {}

    def want(host, items):
        label = "+".join(sorted(items))
        jobs[(host, label)] = (host, label, tuple(items), a.n)
        return label
    pairs = []
    for host, ts in best.items():
        top = ts[:a.top]
        for t in top:
            want(host, [t])
        for x, y in itertools.combinations(top, 2):
            pairs.append(("same", host, None, x, y))
            want(host, [x, y])
    # Across the party: A on one member, B on another (scored as two edits).
    cross = []
    for key, members in tp.PARTIES.items():
        hosted = [(m, t) for m in members if m in best for t in best[m][:a.cross]]
        for (h1, x), (h2, y) in itertools.combinations(hosted, 2):
            if h1 != h2:
                cross.append((key, h1, h2, x, y))
    for host, x, y in TARGETED:
        for it in ([x], [y], [x, y] if x != y else [x, x]):
            want(host, it)
        pairs.append(("targeted", host, None, x, y))
    base_keys = {tp.HOSTS[h] for h in best} | {tp.HOSTS[h] for h, _, _ in TARGETED}
    print(f"{len(jobs)} single-character readings, {len(cross)} cross pairs", flush=True)
    with mp.Pool(a.j, initializer=tp._init) as pool:
        bases = dict(zip(sorted(base_keys), pool.map(_base, [(k, a.n) for k in sorted(base_keys)])))
        res = {}
        for i, (host, label, r) in enumerate(pool.imap_unordered(evaluate, list(jobs.values())), 1):
            res[(host, label)] = r
            if i % 50 == 0:
                print(f"{i}/{len(jobs)}", flush=True)
        cross_res = pool.map(_cross, [(c, a.n) for c in cross])

    def val(host, items):
        r = res.get((host, "+".join(sorted(items))))
        if r is None:
            return None
        return tp.paired(bases[tp.HOSTS[host]], r)
    out = []
    for kind, host, _, x, y in pairs:
        vx, vy = val(host, [x]), val(host, [y])
        vxy = val(host, [x, y] if x != y else [x, x])
        if None in (vx, vy, vxy):
            continue
        syn = [vxy_i - a_i - b_i for vxy_i, a_i, b_i in zip(_diffs(bases, host, res, [x, y] if x != y else [x, x]),
                                                            _diffs(bases, host, res, [x]),
                                                            _diffs(bases, host, res, [y]))]
        out.append(dict(kind=kind, party=tp.HOSTS[host], host=host, other="", a=x, b=y, a_name=_n(x), b_name=_n(y),
                        a_alone=round(vx[0], 2), b_alone=round(vy[0], 2), together=round(vxy[0], 2),
                        synergy=round(st.mean(syn), 2), margin=round(1.96 * st.stdev(syn) / math.sqrt(len(syn)), 2)))
    for (key, h1, h2, x, y), (rx, ry, rxy) in zip(cross, cross_res):
        if None in (rx, ry, rxy):
            continue
        base = bases.get(key) or _base((key, a.n))
        dx = [v[0] - b[0] for v, b in zip(rx, base)]
        dy = [v[0] - b[0] for v, b in zip(ry, base)]
        dxy = [v[0] - b[0] for v, b in zip(rxy, base)]
        syn = [c - p - q for c, p, q in zip(dxy, dx, dy)]
        out.append(dict(kind="cross", party=key, host=h1, other=h2, a=x, b=y, a_name=_n(x), b_name=_n(y),
                        a_alone=round(st.mean(dx), 2), b_alone=round(st.mean(dy), 2), together=round(st.mean(dxy), 2),
                        synergy=round(st.mean(syn), 2), margin=round(1.96 * st.stdev(syn) / math.sqrt(len(syn)), 2)))
    out.sort(key=lambda r: -abs(r["synergy"]))
    with open(a.o, "w", newline="") as f:
        w = csv.DictWriter(f, list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {a.o}: {len(out)} pairs")


def _n(x):
    return x if x.startswith("W:") else game_data.technique_name(x)


def _diffs(bases, host, res, items):
    r = res[(host, "+".join(sorted(items)))]
    return [v[0] - b[0] for v, b in zip(r, bases[tp.HOSTS[host]])]


def _base(args):
    key, n = args
    return tp.run(tp.PARTIES[key], None, None, n)[0]


def _cross(args):
    """A on h1, B on h2, both, in their party: per-fight results."""
    (key, h1, h2, x, y), n = args
    rows = party._rows()
    bx, by = adds_for(h1, [x]), adds_for(h2, [y])
    if bx is None or by is None:
        return None, None, None
    names = tp.PARTIES[key]

    def go(edits):
        last = []

        def make(tier, good_luck=0):
            last[:] = [party.make_pc(m, i, good_luck, rows=rows, edits={"build": edits[m]} if m in edits else None,
                                     row_changes=tp.choices_for(rows[m], edits[m]) if m in edits else None)
                       for i, m in enumerate(names, 1)]
            return last
        tp.cs.make_party = make
        out = []
        for mi, mix in enumerate(tp.se.CURRENT_MIXES):
            for k in range(n):
                r = tp.cs.run_fight(1, tp.LEVEL, movement=True,
                                    enemies=tp.se.build_encounter(tp.se.ENCOUNTERS[tp.LEVEL][mix]), seed=100_000 * mi + k)
                won = r["winner"] == "party"
                out.append((sum(max(0, p["health"]) for p in last) if won else 0, won, r["rounds"]))
        return out
    try:
        return go({h1: bx}), go({h2: by}), go({h1: bx, h2: by})
    except party.BuildError:
        return None, None, None


if __name__ == "__main__":
    main()
