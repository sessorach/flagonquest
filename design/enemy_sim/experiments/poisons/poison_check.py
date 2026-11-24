"""What a dose of Poison is worth under the proposed rules (2026-11-24).

The proposal: a poisoned weapon stays poisoned for the scene. Whenever
its attack takes Health off a creature that isn't already suffering the
Poison, the Poison attacks that creature's Vital Defense at Accuracy
3 + its Level; on a hit it gives its stacks, which don't decay in a fight
(they come off hourly). Bloody Poison's Bleeding decays normally.

Two cases, per the designer: the weapon starts the fight poisoned, or
the carrier spends 2 AP on its first turn to poison it. Scored the way
tools/effect_check.py scores everything (paired seeds, party Health
left, a +2 Health ladder for Value), one weapon user at a time as the
carrier.

    python3 experiments/poisons/poison_check.py -n 300
"""
import argparse
import statistics as st
import sys
from types import SimpleNamespace  # noqa: F401
import _paths  # noqa: F401
import combat_sim as cs, hooks, tactics
import effect_check as ec

CARRIERS = ["Hilde", "Carrick", "Sable"]
# name: (effect key, stacks at Level L, lasting?)
POISONS = {
    "Crippling": ("crippled", lambda L: L, True),
    "Slowing": ("slowed", lambda L: L, True),
    "Vulnerability": ("vulnerable", lambda L: 2 * L, True),
    "Bloody": ("bleeding", lambda L: 2 * L, False),
}


def _spec(pc):
    for p in pc.get("passives", ()):
        if p.startswith("Poison:"):
            _, name, level, mode = p.split(":")
            return name, int(level), mode
    return None


@hooks.on("pc_turn_start", order=5)
def _coat(pc, turn):
    s = _spec(pc)
    if not s or pc.get("_coated"):
        return 0
    pc["_coated"] = True
    if s[2] == "ap":
        pc["poison_ap"] = pc.get("poison_ap", 0) + 2
        return 2
    return 0


@hooks.on("pc_damaged_enemy")
def _expose(e, ctx):
    pc = ctx.pc
    s = _spec(pc)
    if not s or not pc.get("_coated") or e["health"] <= 0:
        return
    name, L, _ = s
    key, stacks, lasting = POISONS[name]
    if e.get(key, 0) > 0 and e.get("_poison_" + key):
        return  # already suffering it
    pc["poison_exposures"] = pc.get("poison_exposures", 0) + 1
    defense = e["bodily"] - tactics.def_pen(e, "Vital")
    if cs.flip() + 3 + L < defense:
        return
    n = stacks(L)
    cs._gain(e, key, n)
    e["_poison_" + key] = True
    if lasting:
        e["curse_" + key] = max(e.get("curse_" + key, 0), n)
    pc["poison_hits"] = pc.get("poison_hits", 0) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=300, help="fights per mix")
    ap.add_argument("-m", type=float, default=1.75, help="enemy Health multiplier")
    ap.add_argument("-L", type=int, action="append", help="Poison Levels (default 1 and 2)")
    a = ap.parse_args()
    levels = a.L or [1, 2]
    ec.NAMES[:] = ec.NAMES  # party A: Hilde, Browndog, Carrick, Sable
    variants = [(f"{p} L{L} {m}", f"Poison:{p}:{L}:{m}") for p in POISONS for L in levels for m in ("pre", "ap")]
    cells = []
    for pname, vs in (("A", [v for v in variants if "Vulnerability" not in v[0]]),
                      ("AV", [v for v in variants if "Vulnerability" in v[0]])):
        cells += [(pname, None, "base", a.m, None, 0), (pname, None, "ladder", a.m, None, 2)]
        cells += [(pname, c, label, a.m, spec, 0) for label, spec in vs for c in CARRIERS]
    print(f"{len(cells)} cells, {a.n} fights per mix", file=sys.stderr, flush=True)
    res = ec.run(cells, a.n)
    print(f"Enemy Health x{a.m}, {a.n} fights per mix, {len(ec.MIXES)} mixes. Value per fight "
          f"(THE TABEL units; Target for a Level L Technique is 3L).")
    print(f"{'Poison':<26}{'Value':>7}{'±':>5}  " + "  ".join(f"{c:>8}" for c in CARRIERS))
    for pname in ("A", "AV"):
        base, lad = (pname, None, "base", a.m), (pname, None, "ladder", a.m)
        for label, spec in variants:
            if ("Vulnerability" in label) != (pname == "AV"):
                continue
            vals = [ec.value(res, base, lad, (pname, c, label, a.m)) for c in CARRIERS]
            v = st.mean(x[0] for x in vals)
            se_ = st.mean(x[1] for x in vals) / len(vals) ** 0.5
            print(f"{label:<26}{v:>7.2f}{se_:>5.1f}  " + "  ".join(f"{x[0]:>8.2f}" for x in vals))


if __name__ == "__main__":
    main()
