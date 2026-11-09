"""Weak / Average / Strong cells, per application, from the effect_check
CSVs. Debuffs: Weak = on the first hit, ordinary fights (Level 1 mixes at
x1.75); Average = aimed at the biggest threat, ordinary fights; Strong =
aimed at the boss, the best of the dangerous fights. Offense-side effects
are scaled by THE TABEL's +1 Accuracy / +1 Damage over what those measure
in the ordinary fights."""
import csv, math, statistics as st
from collections import defaultdict
S = "/tmp/claude-0/-home-user-flagonquest/e6747bdc-fa39-5126-8ea2-8c3b178a4574/scratchpad/ec_manual"
f = float
import os
PREFIX = os.environ.get("CELLS_PREFIX", "")
RENAME = {"full2": "all"} if PREFIX else {}
def load(fn, party=None):
    g = defaultdict(list)
    try:
        rows = list(csv.DictReader(open(f"{S}/{PREFIX}{RENAME.get(fn, fn)}.csv")))
    except FileNotFoundError:
        return g
    for r in rows:
        if r["mix"] == "all" and (party is None or r["party"] == party):
            g[r["test"]].append(r)
    return g
D = {k: load(k, "A") for k in ("full2", "danger_standard", "danger_level2", "danger_chief", "danger_ogre",
                               "fill_ogre", "fill_durable", "nofocus_std", "nofocus_level2", "nofocus_chief",
                               "nofocus_ogre")}
D["full2_175"] = defaultdict(list)
for t, rs in load("full2", "A").items():
    D["full2_175"][t] = [r for r in rs if r["mult"] == "1.0"]
DV = {"full2": load("full2", "AV"), "fill_standard": load("fill_standard", "AV"), "fill_ogre": load("fill_ogre", "AV")}
for t, rs in list(DV["full2"].items()):
    DV["full2"][t] = [r for r in rs if r["mult"] == "1.0"]

def per_app(src, test, only=None, total=False):
    rs = src.get(test, [])
    if only:
        rs = [r for r in rs if r["carrier"] in only]
    if not rs:
        return None
    v = st.mean(f(r["value"]) for r in rs)
    if total:
        return v
    a = st.mean(f(r["applied"]) for r in rs)
    return v / a

def wmean(pairs):
    pairs = [(v, w) for v, w in pairs if v is not None]
    return sum(v * w for v, w in pairs) / sum(w for _, w in pairs) if pairs else None

def _anchor(test):
    v = per_app(D["full2_175"], test, total=True)
    return v
_acc, _dmg = _anchor("Accuracy +1"), _anchor("Damage +1")
print(f"anchors measured: +1 Accuracy {_acc}, +1 Damage {_dmg}")
ACC = 5.49 / (_acc if PREFIX and _acc else 2.45)
DMG = 10.97 / (_dmg if PREFIX and _dmg else 5.36)
print(f"offense factors: Accuracy-like x{ACC:.3f}, Damage-like x{DMG:.3f}")
DANGER = [("L2", "danger_level2"), ("Chief", "danger_chief"), ("Ogre", "danger_ogre")]

def debuff(eff, conv=1.0, aim_src=None, strong_srcs=None, only_aim=None, weak_srcs=None, n_list=(1, 4)):
    out = {}
    for n in n_list:
        w = wmean([(per_app(src, f"{eff} {n}, first hit"), wt) for src, wt in (weak_srcs or [(D["full2_175"], 2), (D["danger_standard"], 1)])])
        a = per_app(aim_src or D["danger_standard"], f"{eff} {n} on the boss, first turn", only_aim)
        best = None
        for name, src in (strong_srcs or [(n_, D[s]) for n_, s in DANGER]):
            v = per_app(src, f"{eff} {n} on the boss, first turn", only_aim)
            if v is not None and (best is None or v > best[0]):
                best = (v, name)
        allv = {name: per_app(src, f"{eff} {n} on the boss, first turn", only_aim) for name, src in (strong_srcs or [(n_, D[s]) for n_, s in DANGER])}
        out[n] = (w * conv if w is not None else None, a * conv if a is not None else None,
                  (best[0] * conv, best[1]) if best else None, {k: (v * conv if v is not None else None) for k, v in allv.items()})
    return out

def show(name, res):
    for n, (w, a, s, allv) in res.items():
        fmt = lambda x: "-" if x is None else f"{x:.2f}"
        print(f"{name:12} x{n}: weak {fmt(w):>6}  avg {fmt(a):>6}  strong {fmt(s[0]) if s else '-':>6} ({s[1] if s else ''})   "
              + "  ".join(f"{k} {fmt(v)}" for k, v in allv.items()))

show("Crippled", debuff("crippled"))
show("Slowed", debuff("slowed"))
show("Bad Luck", debuff("badluck"))
show("Frightened", debuff("fright"))
show("Taunted(BD)", debuff("taunt", only_aim=["Browndog"]))
show("Bleeding", debuff("bleeding", DMG))
show("Harried(raw)", debuff("harried", ACC))
if D["nofocus_std"]: show("Harried", debuff("harried", ACC, aim_src=D["nofocus_std"],
                       strong_srcs=[(n_, D["nofocus_" + s.split("_")[1]]) for n_, s in DANGER],
                       weak_srcs=[(D["nofocus_std"], 1)]))
show("Vulnerable", debuff("vulnerable", ACC, aim_src=DV["fill_standard"], strong_srcs=[("Ogre", DV["fill_ogre"])],
                          weak_srcs=[(DV["full2"], 2), (DV["fill_standard"], 1)]))
show("Necrotic", debuff("necrotic", DMG, aim_src={}, strong_srcs=[("Durable Ogre", D["fill_durable"])],
                        weak_srcs=[(D["full2_175"], 1)]))
# Taunt on a hit, Browndog only
for n in (1, 4):
    print(f"Taunt {n} on Browndog's hits: full2 {per_app(D['full2_175'], f'taunt {n}, first hit', ['Browndog']):.2f}"
          f" dstd {per_app(D['danger_standard'], f'taunt {n}, first hit', ['Browndog']):.2f}"
          f"; all carriers full2 {per_app(D['full2_175'], f'taunt {n}, first hit'):.2f} dstd {per_app(D['danger_standard'], f'taunt {n}, first hit'):.2f}")
for n in (1, 4):
    print(f"Fright {n} aimed, Hilde+Browndog: " + "  ".join(
        f"{nm} {per_app(D[s], f'fright {n} on the boss, first turn', ['Hilde', 'Browndog']):.2f}" for nm, s in [("ord", "danger_standard")] + DANGER))
