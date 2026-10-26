"""What if this character had that instead? (2026-10-25)

Runs a party, then the same party with one or more characters swapped,
on the same seeds against the same encounters, and prints the difference
with its 95% margin (paired, fight by fight, so the noise both runs share
cancels out).

A swap is either another sample_pcs.csv row (a variant build, e.g.
"Beornhard (L2, Frost)") or an edit to the character's build in
party.apply_edits' format, given as JSON:

    python3 compare_builds.py -L 2 -p B --swap "Beornhard (L2)=Beornhard (L2, Frost)"
    python3 compare_builds.py -L 2 --party "Hilde (L2),Browndog (L2),Jackal (L2),Beornhard (L2)" \\
        --edit 'Beornhard (L2)={"replace": [{"id": "T120", "copy": 1, "features": {"Lance": 1, "Frigid": 2}}]}'

`-p` takes a calibrate.py party letter, `--party` any names. Enemy
Health is x1.75 by default (`-m`), the effect check's table toughness,
so fights aren't foregone wins and a difference has room to show; `-m 1`
for as-built enemies. `-s NAME=VALUE` overrides a tunable, as in
calibrate.py.

From a script: compare(names, swaps, level, n) returns the two runs'
per-fight results and the summary; sweep(names, who, variants, level, n)
tries many swaps for one character against one base run (2026-10-26,
hanforth_sweep.py uses it), and sweep_table prints them.
"""
import argparse
import ast
import json
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T, tactics  # noqa: E402
import calibrate  # noqa: E402


def _builder(names, swaps):
    """A make_party stand-in: each name built as itself, or as its swap -
    a row name (str), a dict of build edits, or {"edits": ..., "row": ...}
    when a row column changes too (a Choices pick for a new element)."""
    rows = party._rows()

    def make(tier, good_luck=0):
        pcs = []
        for i, n in enumerate(names, 1):
            swap = swaps.get(n)
            if isinstance(swap, str):
                pc = party.make_pc(swap, i, good_luck, rows=rows)
            elif swap and ("edits" in swap or "row" in swap):
                pc = party.make_pc(n, i, good_luck, rows=rows, edits=swap.get("edits"), row_changes=swap.get("row"))
            elif swap:
                pc = party.make_pc(n, i, good_luck, rows=rows, edits=swap)
            else:
                pc = party.make_pc(n, i, good_luck, rows=rows)
            pcs.append(pc)
        return pcs
    return make


def run(names, swaps, level, n, mixes=None):
    cs.make_party = _builder(names, swaps)
    out = []
    for mi, mix in enumerate(mixes or se.CURRENT_MIXES):
        for k in range(n):
            r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                             seed=100_000 * mi + k)
            out.append(dict(win=r['winner'] == 'party', hp=100 * r['party_hp_pct'] if r['winner'] == 'party' else 0,
                            down=bool(r['pc_downed']), rounds=r['rounds']))
    return out


def _paired(base, var, key):
    d = [float(v[key]) - float(b[key]) for b, v in zip(base, var)]
    mean = st.mean(d)
    margin = 1.96 * (st.stdev(d) / math.sqrt(len(d))) if len(d) > 1 else 0.0
    return st.mean(float(b[key]) for b in base), st.mean(float(v[key]) for v in var), mean, margin


def compare(names, swaps, level=2, n=300, mixes=None):
    base = run(names, {}, level, n, mixes)
    var = run(names, swaps, level, n, mixes)
    return base, var, {k: _paired(base, var, k) for k in ('win', 'hp', 'down', 'rounds')}


def sweep(names, who, variants, level=2, n=100, mixes=None):
    """Many swaps for one character (`who`), each against the same base
    run, for a broad look rather than a precise one: `variants` is a list
    of (label, swap) in _builder's swap formats. Returns the base run's
    means and [(label, summary)]."""
    base = run(names, {}, level, n, mixes)
    out = []
    for label, swap in variants:
        var = run(names, {who: swap}, level, n, mixes)
        out.append((label, {k: _paired(base, var, k) for k in ('win', 'hp', 'down', 'rounds')}))
    means = {k: st.mean(float(b[k]) for b in base) for k in ('win', 'hp', 'down', 'rounds')}
    return means, out


def sweep_table(means, results):
    """Markdown rows, best Health change first."""
    lines = [f"Base: wins {100 * means['win']:.0f}%, Health left {means['hp']:.1f}, "
             f"someone Down {100 * means['down']:.0f}%, {means['rounds']:.1f} rounds", "",
             "| Swap | Health left | Wins | Someone Down | Rounds |", "|---|---|---|---|---|"]
    for label, sm in sorted(results, key=lambda r: -r[1]['hp'][2]):
        hp, win, down, rnd = sm['hp'], sm['win'], sm['down'], sm['rounds']
        lines.append(f"| {label} | {hp[2]:+.1f} ±{hp[3]:.1f} | {100 * win[2]:+.1f} | {100 * down[2]:+.1f} | "
                     f"{rnd[2]:+.1f} |")
    return "\n".join(lines)


def sweep_main(doc, variants, parties):
    """The command line a sweep study shares (hanforth_sweep.py,
    beornhard_sweep.py): `variants` {level: (who, [(label, swap)])},
    `parties` {level: [(names, enemy Health multiplier)]}."""
    ap = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("level", type=int, choices=sorted(variants))
    ap.add_argument("party", type=int, help="index into the Level's parties")
    ap.add_argument("-n", type=int, default=100, help="fights per mix")
    ap.add_argument("--only", help="run only swaps whose label contains this")
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE")
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        setattr(T if hasattr(T, k) else tactics, k, v)
    names, mult = parties[a.level][a.party]
    T.ENEMY_HEALTH_MULT = mult
    who, vs = variants[a.level]
    vs = [v for v in vs if not a.only or a.only in v[0]]
    means, results = sweep(names, who, vs, a.level, a.n)
    print(f"Level {a.level}, {', '.join(names)}; enemy Health x{mult}; {a.n} fights a mix"
          + (f"; {', '.join(a.s)}" if a.s else "") + "\n")
    print(sweep_table(means, results))


def report(summary):
    lines = []
    for key, label, scale in (('win', 'wins', 100), ('hp', 'Health left', 1), ('down', 'someone Down', 100),
                              ('rounds', 'rounds', 1)):
        b, v, d, m = summary[key]
        unit = '%' if scale == 100 else ''
        lines.append(f"  {label:13s} {b * scale:6.1f}{unit} -> {v * scale:6.1f}{unit}   "
                     f"change {d * scale:+.1f}{unit} (+/- {m * scale:.1f})")
    return "\n".join(lines)


def _parse_swaps(swap_args, edit_args):
    swaps = {}
    for s in swap_args:
        name, _, other = s.partition("=")
        swaps[name.strip()] = other.strip()
    for e in edit_args:
        name, _, js = e.partition("=")
        swaps[name.strip()] = json.loads(js)
    return swaps


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-L", type=int, default=2, help="Level of the party and the encounters")
    ap.add_argument("-p", help="a calibrate.py party letter")
    ap.add_argument("--party", help="comma-separated sample_pcs.csv names")
    ap.add_argument("--swap", action="append", default=[], help='"Name=Other row"')
    ap.add_argument("--edit", action="append", default=[], help='"Name={json edits}"')
    ap.add_argument("-n", type=int, default=300, help="fights per mix")
    ap.add_argument("-m", type=float, default=1.75, help="enemy Health multiplier (default 1.75)")
    ap.add_argument("--mixes", help="comma-separated encounter names (default: the four standard mixes)")
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE")
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        setattr(T if hasattr(T, k) else tactics, k, v)
    T.ENEMY_HEALTH_MULT = a.m
    names = [x.strip() for x in a.party.split(",")] if a.party else calibrate.PARTIES[a.L][a.p]
    swaps = _parse_swaps(a.swap, a.edit)
    unknown = [n for n in swaps if n not in names]
    if unknown:
        raise SystemExit(f"not in the party: {unknown}")
    mixes = [x.strip() for x in a.mixes.split(",")] if a.mixes else None
    _, _, summary = compare(names, swaps, a.L, a.n, mixes)
    print(f"Level {a.L}, {', '.join(names)}; enemy Health x{a.m}; {a.n} fights a mix")
    for name, swap in swaps.items():
        print(f"  {name} -> {swap if isinstance(swap, str) else json.dumps(swap)}")
    print(report(summary))
