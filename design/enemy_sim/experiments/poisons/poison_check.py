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
# name: (effect key, stacks at Level L, lasting?), as the items read
# since 2026-11-25. The first runs (2026-11-24) used the old strengths:
# Crippling and Slowing L, Vulnerability and Bloody 2L (--per-level).
POISONS = {
    "Crippling": ("crippled", lambda L: L + 1, True),
    "Slowing": ("slowed", lambda L: L + 1, True),
    "Vulnerability": ("vulnerable", lambda L: L, True),
    "Bloody": ("bleeding", lambda L: 3 * L, False),
}


def _spec(pc):
    for p in pc.get("passives", ()):
        if p.startswith("Poison:"):
            _, name, level, mode, *k = p.split(":")
            return name, int(level), mode, float(k[0]) if k else None
    return None


@hooks.on("pc_turn_start", order=5)
def _coat(pc, turn):
    s = _spec(pc)
    if not s or pc.get("_coated"):
        return 0
    pc["_coated"] = True
    if s[2] == "spell":
        # Beast Venom: a 1 AP spell at the biggest threat against Vital,
        # at the carrier's own Skill Total, on its first turn; no wounding.
        tg = cs._aim_target(turn.enemies, turn.pcs)
        if tg is not None:
            _land(tg, s, cs.flip() + pc["skill_total"])
        return 1
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
    name, L, _, k = s
    key, stacks, lasting = POISONS[name]
    if k is not None:
        stacks = lambda L, k=k: round(k * L)
    if e.get(key, 0) > 0 and e.get("_poison_" + key):
        return  # already suffering it
    if s[2] == "spell":
        return
    _land(e, s, cs.flip() + 3 + L)


def _land(e, s, roll):
    name, L, _, k = s
    key, stacks, lasting = POISONS[name]
    if k is not None:
        stacks = lambda L, k=k: round(k * L)
    if roll < e["bodily"] - tactics.def_pen(e, "Vital"):
        return
    n = stacks(L)
    cs._gain(e, key, n)
    e["_poison_" + key] = True
    if lasting:
        e["curse_" + key] = max(e.get("curse_" + key, 0), n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=300, help="fights per mix")
    ap.add_argument("-m", type=float, default=1.75, help="enemy Health multiplier")
    ap.add_argument("-L", type=int, action="append", help="Poison Levels (default 1 and 2)")
    ap.add_argument("--per-level", action="append", default=[],
                    help="NAME=k: stacks are k times the Level (repeatable); only the already-poisoned case")
    ap.add_argument("--spell", help="Poisons (comma-separated) delivered Beast Venom's way instead")
    a = ap.parse_args()
    levels = a.L or [1, 2]
    ec.NAMES[:] = ec.NAMES  # party A: Hilde, Browndog, Carrick, Sable
    variants = [(f"{p} L{L} {m}", f"Poison:{p}:{L}:{m}") for p in POISONS for L in levels for m in ("pre", "ap")]
    if a.spell:
        variants = [(f"{p} L{L} spell", f"Poison:{p}:{L}:spell") for p in a.spell.split(",") for L in levels]
    elif a.per_level:
        variants = [(f"{p} {k}xL L{L}", f"Poison:{p}:{L}:pre:{k}")
                    for p, k in (x.split("=") for x in a.per_level) for L in levels]
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
