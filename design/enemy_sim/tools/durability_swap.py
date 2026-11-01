"""Lifeline and Toughened Resolve on and off, under four yardsticks (2026-11-01).

The designer's question: are max Health and Lifeline as strong as the
optimizer says, or is the yardstick flattering them? Two things in the
yardstick favor them: scoring a build next to three stand-ins (plain
fighters do the damage, so keeping them alive is all that's missing), and
enemy Levels that add Health but not damage (one Level up from Level 3
adds none). So each optimized build plays:

- `S1`: with three stand-ins, one enemy Level up (the scorecard's reading);
- `S1+`: the same with every enemy attack dealing 1 more damage
  (tunables.ENEMY_DAMAGE_ADJ, about the next damage step a Level brings);
- `P2`: in six parties of three other optimized builds, two Levels up
  (one up, those parties win nearly every day);
- `P2+`: the same with the extra damage.

and the same with Lifeline taken off, one or every Toughened Resolve taken
off, one more Toughened Resolve, or Lifeline added, at the same total XP
(heal_swap.payer: the difference paid from or put back into the combat
Skills first). Every variant of a build plays the same parties and seeds.

    python3 tools/durability_swap.py -L 3 -n 500 --scorecard hall_of_fame/runs_levelup/scorecard_l3_run2.json -o out.json
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import random
import sys

import _paths  # noqa: E402,F401 (the simulator's core, a folder or two up)
import build_optimizer as bo  # noqa: E402
import heal_swap as hs  # noqa: E402
import resume  # noqa: E402
import scorecard as sc  # noqa: E402

LIFELINE, RESOLVE = "T110", "T019"
PARTIES = 6
CONTEXTS = {"S1": (1, {}), "S1+": (1, {"ENEMY_DAMAGE_ADJ": 1}),
            "P2": (2, {}), "P2+": (2, {"ENEMY_DAMAGE_ADJ": 1})}


def _copies(build, tid):
    """apply_edits' remove entries for every copy of `tid`."""
    return [{"id": tid, "copy": i + 1} for i in range(sum(t["id"] == tid for t in build["techniques"]))]


def variants(build, level, row):
    pay = hs.payer(build, level, row)
    life, res = _copies(build, LIFELINE), _copies(build, RESOLVE)
    tries = {}
    if life:
        tries["no Lifeline"] = dict(remove=life)
    if res:
        tries["1 fewer Toughened Resolve"] = dict(remove=res[-1:])
    if len(res) > 1:
        tries["no Toughened Resolve"] = dict(remove=res)
    if life and res:
        tries["neither"] = dict(remove=life + res)
    tries["1 more Toughened Resolve"] = dict(add=[{"id": RESOLVE}])
    if not life:
        tries["add Lifeline"] = dict(add=[{"id": LIFELINE}])
    out = {"as is": build}
    for label, kw in tries.items():
        try:
            out[label] = pay(**kw)
        except Exception as e:  # party.BuildError, mostly a prereq over the cap
            out[label] = str(e)
    return hs.check_loads(out, row), dict(lifeline=len(life), resolve=len(res))


def parties_for(arch, others, k=PARTIES):
    """`k` fixed trios of other archetypes, the same for every variant."""
    rng = random.Random(sum(map(ord, arch)))
    pool = sorted(o for o in others if o != arch)
    return [tuple(sorted(rng.sample(pool, 3))) for _ in range(k)]


def logit(won, days):
    p = min(max(won / days, 0.5 / days), 1 - 0.5 / days)
    return math.log(p / (1 - p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=500, help="day_sim.run's n for the stand-in readings (4n days)")
    ap.add_argument("--party-n", type=int, default=250, help="the same for each party reading")
    ap.add_argument("--scorecard", required=True)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    bo.START = "best"
    card = json.load(open(a.scorecard))
    L = a.L
    B = card["builds"]
    stand = [(None, None)] * 3
    jobs, table = {}, {}
    for arch in sorted(B):
        vs, have = variants(B[arch]["optimized"], L, B[arch]["row"])
        trios = parties_for(arch, B)
        table[arch] = dict(have=have, parties=trios, variants={})
        for label, b in vs.items():
            if not isinstance(b, dict):
                table[arch]["variants"][label] = dict(error=b)
                continue
            me = (B[arch]["row"], b)
            for ctx, (up, over) in CONTEXTS.items():
                if ctx.startswith("S"):
                    jobs[(arch, label, ctx, "")] = ([me] + stand, L, up, a.n, 0, over)
                else:
                    for t in trios:
                        jobs[(arch, label, ctx, "+".join(t))] = ([me] + [(B[x]["row"], B[x]["optimized"]) for x in t],
                                                                 L, up, a.party_n, 0, over)
    part = resume.Partial(a.o + ".partial")
    todo = [k for k in jobs if list(k) not in part]
    with mp.Pool(a.j) as pool:
        for k, v in zip(todo, pool.imap(sc.play, [jobs[k] for k in todo])):
            part.add(list(k), {x: v[x] for x in ("won", "days")})
    R = {tuple(json.loads(k)): v for k, v in part.got.items()}

    def reading(arch, label, ctx):
        ks = [k for k in R if k[:3] == (arch, label, ctx)]
        won, days = sum(R[k]["won"] for k in ks), sum(R[k]["days"] for k in ks)
        return dict(rate=won / days, logit=logit(won, days), days=days)
    for arch, t in table.items():
        labels = sorted({k[1] for k in jobs if k[0] == arch}, key=lambda s: (s != "as is", s))
        for label in labels:
            t["variants"][label] = {ctx: reading(arch, label, ctx) for ctx in CONTEXTS}
        base = t["variants"]["as is"]
        for label in labels:
            for ctx in CONTEXTS:
                v = t["variants"][label][ctx]
                v["points"] = 100 * (v["rate"] - base[ctx]["rate"])
                v["odds"] = v["logit"] - base[ctx]["logit"]
    with open(a.o, "w") as f:
        json.dump(dict(level=L, contexts={k: dict(up=u, overrides=o) for k, (u, o) in CONTEXTS.items()},
                       builds=table), f, indent=1)
    part.finish()
    for arch, t in table.items():
        print(f"{arch} (Lifeline {t['have']['lifeline']}, Toughened Resolve {t['have']['resolve']})")
        for label, v in t["variants"].items():
            if "error" in v:
                print(f"    {label:28s} can't: {v['error']}")
                continue
            print(f"    {label:28s} " + "  ".join(
                f"{ctx} {100 * v[ctx]['rate']:3.0f}%" + ("" if label == "as is" else f" ({v[ctx]['points']:+.0f})")
                for ctx in CONTEXTS))


if __name__ == "__main__":
    main()
