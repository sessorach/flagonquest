"""What each Feature-delivered mechanic is worth, broadly (2026-10-27).

Per the designer: a broad pulse on the game's balance across every
Buildable Technique's Features, to see what the weights might need. Each
test character carries one Technique copy with its Feature points left
unspent (the "stripped" base); each test spends them on one Feature,
paired on the same seeds against that base, in two parties where there
are two. The score is effect_check.py's: the party's Health left (losses
count 0), turned into Value by a Health ladder (+2 Health on every PC;
one PC's +1 Health is worth 4, THE TABEL's Health). Next to it, the
stacks the Feature actually landed a fight (counted from the trace, base
subtracted; healing at Health's 4) times THE TABEL's base rate, and the
carrier's own change in damage dealt, so the two can be compared: the
first says what the mechanic did, the second what THE TABEL thinks those
stacks are worth.

Broad, not precise: 100 fights a mix by default, so read differences of
a few Value as noise. Results are in TABLE_PLAY_NOTES.md, "Mechanic
baseline".

    python3 mechanic_baseline.py             # everything, 4 processes
    python3 mechanic_baseline.py -c hilde2 -n 50
    python3 mechanic_baseline.py --csv out.csv
"""
import argparse
import collections
import csv
import math
import os
import re
import statistics as st
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T  # noqa: E401,E402

BM, WM, SB, HM = "T072", "T120", "T104", "T105"

# THE TABEL's base rates (balance_weights.csv's Value column) for the
# stacks the trace counts, per stack, per place or per meter.
RATES = {"Protected": 3, "Bleeding": 4, "Crippled": 1.5, "Slowed": 1.1, "Harried": 1, "Taunted": 2.2,
         "Vulnerable": 1, "Necrotic": 3, "Hasted": 0.55, "Staggered": 1.35, "Outflanked": 1.35, "Pushed": 0.89,
         "Ward": 1.0}
EFFECT_RE = re.compile(r"\b(Protected|Bleeding|Crippled|Slowed|Harried|Taunted|Vulnerable|Necrotic|Hasted|"
                       r"Staggered|Outflanked|Pushed|Ward) \+?(\d+)")

PARTIES = {
    "B2": (["Hilde (L2)", "Browndog (L2)", "Jackal (L2)", "Beornhard (L2)"], 2, 2.75),
    "A2": (["Hilde (L2)", "Browndog (L2)", "Carrick (L2)", "Sable (L2)"], 2, 2.25),
    "D2": (["Browndog (L2)", "Hanforth (L2)", "Felix (L2)", "Beornhard (L2)"], 2, 1.75),
    "H2": (["Hilde (L2)", "Browndog (L2)", "Hanforth (L2)", "Beornhard (L2)"], 2, 2.5),
    "B3": (["Hilde (L3)", "Browndog (L3)", "Jackal (L3)", "Beornhard (L3)"], 3, 2.25),
    "D3": (["Browndog (L3)", "Hanforth (L3)", "Hilde (L3)", "Beornhard (L3)"], 3, 2.25),
}


def bm(copy, feats):
    return {"replace": [{"id": BM, "copy": copy, "features": feats}]}


def wm2(feats):
    """Both of Beornhard (L2)'s Level 2 copies (3 points: Lance + 2)."""
    return {"replace": [{"id": WM, "copy": c, "features": dict({"Lance": 1}, **feats)} for c in (1, 2)]}


def wm4(feats):
    """Beornhard (L3)'s Level 4 copy (6 points)."""
    return {"replace": [{"id": WM, "copy": 3, "features": feats}]}


def one(tid, copy, feats):
    return {"replace": [{"id": tid, "copy": copy, "features": feats}]}


def element(n, copy, tech="Battle Maneuver", kind="Fire"):
    picks = [""] * n
    picks[copy - 1] = kind
    return f"{tech}: " + ", ".join(picks)


# A Level 1 Battle Maneuver copy's 3 points, every way.
def maneuver_tests(copy, n_copies, ranged=False):
    tests = [(f, 3, bm(copy, {f: 3}), None) for f in (
        "Lunging", "Wind Slash", "Distracting", "Battering", "Wing Clip", "Harrying", "Hamstring", "Backfoot",
        "Lodestone", "Half Guard", "Blade of Four Fates", "Fleet Step")]
    tests += [("Turn Elements (Fire)", 3, bm(copy, {"Turn Elements": 3}), element(n_copies, copy)),
              ("Calculated", 3, bm(copy, {"Calculated": 1}), None),
              ("Viper's Sting", 3, bm(copy, {"Viper's Sting": 1}), None),
              ("Victorious", 2, bm(copy, {"Victorious": 1}), None),
              ("Elemental (Fire)", 2, bm(copy, {"Elemental": 1}), element(n_copies, copy))]
    return tests


# carrier key: (who, stripped base edits, tunables for every run of it,
#               [parties], [(label, points, edits, Choices or None)])
CARRIERS = {
    "hilde2": ("Hilde (L2)", bm(2, {}), None, ["B2", "A2"], maneuver_tests(2, 2)),
    "browndog2": ("Browndog (L2)", bm(2, {}), None, ["B2", "D2"], maneuver_tests(2, 3)),
    "sable2": ("Sable (L2)", bm(1, {}), None, ["A2"], maneuver_tests(1, 1, ranged=True)),
    "jackal3": ("Jackal (L3)", bm(2, {}), None, ["B3"], maneuver_tests(2, 2, ranged=True)),
    "beornhard2": ("Beornhard (L2)", wm2({}), None, ["B2", "D2"], [
        ("Destructive", 2, wm2({"Destructive": 2}), None),
        ("Frigid", 2, wm2({"Frigid": 2}), None),
        ("Glacier", 2, wm2({"Glacier": 2}), None),
        ("Kinetic", 2, wm2({"Kinetic": 2}), None),
        ("Corrupting (all vs Vital)", 2, wm2({"Corrupting": 2}), "War Magic: Vital, Vital, Vital"),
        ("Necrotic", 2, wm2({"Necrotic": 2}), None),
        ("Barraging", 2, wm2({"Barraging": 2}), None),
        ("Abjuring", 2, wm2({"Abjuring": 2}), None),
        ("Wild Magic", 2, wm2({"Wild Magic": 2}), None),
        ("Sanguine", 1, wm2({"Sanguine": 1}), None),
        ("Arcane Chant, Destructive 1", 2, wm2({"Arcane Chant": 1, "Destructive": 1}), None),
        ("Destructive 1 (half)", 1, wm2({"Destructive": 1}), None),
    ]),
    # Shape setup on, so a Shape copy gets cast (beornhard_sweep.py).
    "beornhard3": ("Beornhard (L3)", wm4({"Lance": 1}), {"SHAPE_SETUP": True}, ["B3", "D3"], [
        ("Destructive 5", 5, wm4({"Lance": 1, "Destructive": 5}), None),
        ("Piercing Elements", 1, wm4({"Lance": 1, "Piercing Elements": 1}), None),
        ("Draw Power", 1, wm4({"Lance": 1, "Draw Power": 1}), None),
        ("Channel", 3, wm4({"Lance": 1, "Channel (Shape)": 1}), None),
        ("Furrow (no Lance)", 3, wm4({"Furrow (Shape)": 1}), None),
        ("Funnel (no Lance)", 3, wm4({"Funnel (Shape)": 1}), None),
        ("Nova (no Lance)", 3, wm4({"Nova (Shape)": 1}), None),
    ]),
    "hanforth2sb": ("Hanforth (L2)", one(SB, 1, {}), None, ["D2", "H2"], [
        ("Shielding", 3, one(SB, 1, {"Shielding": 3}), None),
        ("Step of Air", 3, one(SB, 1, {"Step of Air": 3}), None),
        ("Turn Elements (Fire)", 3, one(SB, 1, {"Turn Elements": 3}), "Spirit Blessing: Fire"),
        ("Retribution", 3, one(SB, 1, {"Retribution": 3}), None),
        ("River's Might", 3, one(SB, 1, {"River's Might": 3}), None),
        ("Touch of Chaos", 3, one(SB, 1, {"Touch of Chaos": 3}), None),
        ("Elemental Enhancement (Fire)", 3, one(SB, 1, {"Elemental Enhancement": 3}), "Spirit Blessing: Fire"),
        ("Steady, Embolden", 2, one(SB, 1, {"Steady": 1, "Embolden": 1}), None),
        ("Quickened, Shielding 2", 3, one(SB, 1, {"Quickened": 1, "Shielding": 2}), None),
    ]),
    "hanforth2hm": ("Hanforth (L2)", one(HM, 1, {}), None, ["D2", "H2"], [
        ("Vitality 2", 4, one(HM, 1, {"Vitality": 2}), None),
        ("Triage, Reach", 4, one(HM, 1, {"Triage": 1, "Reach": 1}), None),
        ("Guardian Angel 4", 4, one(HM, 1, {"Guardian Angel": 4}), None),
        ("Purify 4", 4, one(HM, 1, {"Purify": 4}), None),
        ("Rejuvenate, Vitality 1, Reach", 4, one(HM, 1, {"Rejuvenate": 1, "Vitality": 1, "Reach": 1}), None),
        ("Reach", 1, one(HM, 1, {"Reach": 1}), None),
    ]),
    "hanforth3hm": ("Hanforth (L3)", one(HM, 1, {}), None, ["D3"], [
        ("Vitality 4", 8, one(HM, 1, {"Vitality": 4}), None),
        ("Healing Pact, Vitality 1, Reach", 8, one(HM, 1, {"Healing Pact": 1, "Vitality": 1, "Reach": 1}), None),
        ("Triage, Vitality 2, Reach", 8, one(HM, 1, {"Triage": 1, "Vitality": 2, "Reach": 1}), None),
        ("Guardian Angel 8", 8, one(HM, 1, {"Guardian Angel": 8}), None),
    ]),
}


_LAST = []
_ORIG = {}


def _make(names, swap=None, ladder=0):
    rows = party._rows()

    def make(tier, good_luck=0):
        pcs = _LAST
        pcs.clear()
        for i, n in enumerate(names, 1):
            if swap and n == swap[0]:
                pc = party.make_pc(n, i, good_luck, rows=rows, edits=swap[1],
                                   row_changes={"Choices": swap[2]} if swap[2] else None)
            else:
                pc = party.make_pc(n, i, good_luck, rows=rows, health=ladder)
            pcs.append(pc)
        return pcs
    return make


def _fights(task):
    """One run: (party key, who or None, edits, Choices, ladder, n, tunables)."""
    pkey, who, edits, choices, ladder, n, tune = task
    names, level, mult = PARTIES[pkey]
    T.ENEMY_HEALTH_MULT = mult
    # A pool process runs many tasks: put back what the last one changed.
    for k, v in _ORIG.items():
        setattr(T, k, v)
    for k, v in (tune or {}).items():
        _ORIG.setdefault(k, getattr(T, k))
        setattr(T, k, v)
    cs.make_party = _make(names, (who, edits, choices) if who else None, ladder)
    hp, stacks, healed = [], collections.Counter(), 0
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(n):
            trace = [] if who else None
            r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                             seed=100_000 * mi + k, trace=trace)
            hp.append(sum(max(0, p['health']) for p in _LAST) if r['winner'] == 'party' else 0)
            for t in trace or ():
                if str(t.get('unit', '')).startswith(who):
                    if t.get('side') == 'party' and t.get('action') == 'attack':
                        stacks['Damage'] += t.get('dmg', 0) or 0
                    for name, num in EFFECT_RE.findall(str(t.get('effects') or '') + ' ' + str(t.get('note') or '')):
                        stacks[name] += int(num)
                    if t.get('action') == 'heal':
                        healed += t.get('amount', 0)
    fights = len(hp)
    return hp, {k: v / fights for k, v in stacks.items()}, healed / fights


def _paired(base, var):
    d = [v - b for b, v in zip(base, var)]
    return st.mean(d), 1.96 * st.stdev(d) / math.sqrt(len(d))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-c", action="append", help="carrier key(s); default all")
    ap.add_argument("-n", type=int, default=100, help="fights per mix")
    ap.add_argument("-j", type=int, default=4, help="processes")
    ap.add_argument("--only", help="run only Features whose label contains this")
    ap.add_argument("--csv")
    a = ap.parse_args()
    carriers = {k: v for k, v in CARRIERS.items() if not a.c or k in a.c}
    if a.only:
        carriers = {k: v[:4] + ([t for t in v[4] if a.only in t[0]],) for k, v in carriers.items()}
    pkeys = sorted({p for c in carriers.values() for p in c[3]})
    tasks = {}
    for p in pkeys:
        tasks[("asbuilt", p)] = (p, None, None, None, 0, a.n, None)
        tasks[("ladder", p)] = (p, None, None, None, 2, a.n, None)
    for ck, (who, base_edits, tune, plist, tests) in carriers.items():
        for p in plist:
            tasks[("base", ck, p)] = (p, who, base_edits, None, 0, a.n, tune)
            for label, pts, edits, choices in tests:
                tasks[("test", ck, p, label)] = (p, who, edits, choices, 0, a.n, tune)
    keys = list(tasks)
    with Pool(a.j) as pool:
        out = dict(zip(keys, pool.map(_fights, [tasks[k] for k in keys], chunksize=1)))
    per_value = {}
    for p in pkeys:
        slope, _ = _paired(out[("asbuilt", p)][0], out[("ladder", p)][0])
        per_value[p] = 32 / slope  # Value per point of Health left (8 PC-Health points = 32 Value)
    rows = []
    for ck, (who, _, _, plist, tests) in carriers.items():
        print(f"\n### {who} ({ck})\n")
        print("| Feature | Points | " + " | ".join(f"{p}: Value (±)" for p in plist) +
              " | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |")
        print("|---|---|" + "---|" * len(plist) + "---|---|---|---|")
        for label, pts, _, _ in tests:
            vals, cells, priced, landed, dealt = [], [], [], [], []
            for p in plist:
                bhp, bst, bheal = out[("base", ck, p)]
                thp, tst, theal = out[("test", ck, p, label)]
                d, m = _paired(bhp, thp)
                v, mv = d * per_value[p], m * per_value[p]
                vals.append(v)
                cells.append(f"{v:+.1f} ±{mv:.1f}")
                delta = {k: tst.get(k, 0) - bst.get(k, 0) for k in set(tst) | set(bst)}
                delta = {k: x for k, x in delta.items() if abs(x) >= 0.05}
                dmg = delta.pop('Damage', 0)
                dealt.append(dmg)
                priced.append(sum(x * RATES[k] for k, x in delta.items()) + 4 * (theal - bheal))
                landed.append(", ".join(f"{k} {x:+.1f}" for k, x in sorted(delta.items(), key=lambda kv: -abs(kv[1])))
                              + (f", healed {theal - bheal:+.1f}" if abs(theal - bheal) >= 0.05 else ""))
                rows.append(dict(carrier=ck, who=who, party=p, feature=label, points=pts, value=round(v, 2),
                                 margin=round(mv, 2), tabel=round(priced[-1], 2), damage=round(dmg, 2),
                                 landed=landed[-1]))
            mean = st.mean(vals)
            print(f"| {label} | {pts} | " + " | ".join(cells) + f" | {mean / pts:+.1f} | {landed[0] or '-'} | "
                  f"{priced[0]:+.1f} | {dealt[0]:+.1f} |")
    print("\nValue per point of Health left: " + ", ".join(f"{p} {v:.1f}" for p, v in per_value.items()))
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
