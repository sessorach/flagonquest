"""One party under every party tactic (2026-10-27), paired.

Runs the party as built, then under each preset in party_tactics.py (or
the ones named), on the same seeds against the same encounters, and
prints the change in wins, Health left (points), how often someone goes
Down and fight length.

    python3 tactics_compare.py -L 2 -p A
    python3 tactics_compare.py -L 3 -p B -m 2.25 -t cautious -t "max range+focus fire"
"""
import argparse
import re
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calibrate  # noqa: E402
import compare_builds as cb  # noqa: E402
import party_tactics  # noqa: E402
import tunables as T  # noqa: E402


def compare(names, level, specs, n=100, mixes=None):
    """{spec: summary} against the party as built (cb._paired's tuples)."""
    party_tactics.use(None)
    base = cb.run(names, {}, level, n, mixes)
    out = {}
    for spec in specs:
        party_tactics.use(spec)
        try:
            var = cb.run(names, {}, level, n, mixes)
        finally:
            party_tactics.use(None)
        out[spec] = {k: cb._paired(base, var, k) for k in ('win', 'hp', 'down', 'rounds')}
    return base, out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-L", type=int, default=2)
    ap.add_argument("-p", help="a calibrate.py party letter")
    ap.add_argument("--party", help="comma-separated sample_pcs.csv names")
    ap.add_argument("-t", action="append", help="preset(s) to try (default: all)")
    ap.add_argument("-n", type=int, default=100, help="fights per mix")
    ap.add_argument("-m", type=float, default=1.75, help="enemy Health multiplier")
    a = ap.parse_args()
    T.ENEMY_HEALTH_MULT = a.m
    names = [x.strip() for x in re.split(r",(?![^()]*\))", a.party)] if a.party else calibrate.PARTIES[a.L][a.p]
    specs = a.t or [p for p in party_tactics.PRESETS if p != "as built"]
    base, out = compare(names, a.L, specs, a.n)
    print(f"Level {a.L}, {', '.join(names)}; enemy Health x{a.m}; {a.n} fights a mix")
    print(f"As built: wins {100 * st.mean(b['win'] for b in base):.0f}%, Health left "
          f"{st.mean(b['hp'] for b in base):.1f}, someone Down {100 * st.mean(b['down'] for b in base):.0f}%, "
          f"{st.mean(b['rounds'] for b in base):.1f} rounds\n")
    print("| Tactic | Health left | Wins | Someone Down | Rounds |")
    print("|---|---|---|---|---|")
    for spec, sm in sorted(out.items(), key=lambda kv: -kv[1]['hp'][2]):
        hp, win, down, rnd = sm['hp'], sm['win'], sm['down'], sm['rounds']
        print(f"| {spec} | {hp[2]:+.1f} ±{hp[3]:.1f} | {100 * win[2]:+.1f} | {100 * down[2]:+.1f} | {rnd[2]:+.1f} |")
