"""One budget, and Heavy armor at 6 (2026-11-07).

Per the designer: armor, loadout and picks all come out of the Ability
budget, never out of Health; what's left over can buy Health. Today a
design can overspend into Health (down to 2/3 of the table's), and the
Level's extra points buy picks even when the design already spent past its
points. tunables.V3_ONE_BUDGET stops both: the extra points buy only what
the design leaves room for, and a design that costs more than its Level's
points doesn't build. Under it the Hedge Knight and both priests fit as
designed (they just stop buying an extra pick at Levels 1-2); the three
Heavy designs are a point over at Level 1 with Heavy at 4, three over at 6,
and get trimmed (the trimmed picks go on the end of PrunedExtra, so they
come back if the extra points leave room after Accuracy and Damage):

- one4 (Heavy 4): Warden drops Action (Parting Shot); Sentinel one Dodge +1;
  Warlord Action (Parting Shot), first on its BigPicks instead.
- one6 (Heavy 6): Warden keeps Sturdy and Parting Shot (drops Battering and
  Durable); Sentinel keeps Resist (Fire), Elemental Weapon (Frost),
  Resilient and Sturdy (drops both Dodge +1 and Enhanced Health); Warlord
  keeps Intimidating, with Cleaving and Parting Shot first on its BigPicks.

Read on the manual's fights (manual_check's draws, middle of the band) and
the big-enemy fights (size_check's Black Knights, solo Warlord, Ogres).

    python3 experiments/enemies/one_budget.py
"""
import collections
import multiprocessing as mp
import os
import statistics as st
import sys

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import enemy_builder_pcstyle as eb  # noqa: E402
import sample_enemies as se  # noqa: E402
import manual_check as mc  # noqa: E402
import size_check as sc  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402

HEAVY = ("Ironbranch Warden", "Iron Sentinel", "Brute Warlord")
VARIANTS = {
    "today": dict(heavy=4, one=False, rows={}),
    "one4": dict(heavy=4, one=True, rows={
        "Ironbranch Warden": dict(PrunedPicks="Durable; Sturdy; Strike (Battering)",
                                  PrunedExtra="Dodge +1; Strike (Crippling); Strike (Crippling); Action (Parting Shot)"),
        "Iron Sentinel": dict(PrunedPicks="Resist (Fire); Dodge +1; Enhanced Health; Elemental Weapon (Frost); Resilient; Sturdy",
                              PrunedExtra="Vital/Mental/Vigilant +1; Enhanced Health; Dodge +1"),
        "Brute Warlord": dict(PrunedPicks="Strike (Cleaving); Action (Intimidating)",
                              BigPicks="Action (Parting Shot); {big}"),
    }),
    "one6": dict(heavy=6, one=True, rows={
        "Ironbranch Warden": dict(PrunedPicks="Sturdy; Action (Parting Shot)",
                                  PrunedExtra="Dodge +1; Strike (Crippling); Strike (Crippling); Strike (Battering); Durable"),
        "Iron Sentinel": dict(PrunedPicks="Resist (Fire); Elemental Weapon (Frost); Resilient; Sturdy",
                              PrunedExtra="Vital/Mental/Vigilant +1; Enhanced Health; Dodge +1; Dodge +1"),
        "Brute Warlord": dict(PrunedPicks="Action (Intimidating)",
                              BigPicks="Strike (Cleaving); Action (Parting Shot); {big}"),
    }),
}
SIZE_LABELS = ("Black Knight + two standard", "Two Black Knights", "Solo Brute Warlord",
               "Gravel Ogre + two standard", "Two Gravel Ogres")
_INNER = [None]


def install(v):
    sc.install()
    if _INNER[0] is None:
        _INNER[0] = se._manual_row
    spec = VARIANTS[v]
    eb.ARMOR_HEALTH_V3P["Heavy"] = spec["heavy"]
    T.V3_ONE_BUDGET = spec["one"]

    def manual_row(name):
        r = _INNER[0](name)
        if r is None:
            return r
        over = spec["rows"].get(name.partition("@")[0])
        if over:
            r = dict(r, **{k: x.format(big=r.get("BigPicks", "")) for k, x in over.items()})
        return r
    se._manual_row = manual_row


def _manual(args):
    v, job = args
    install(v)
    return v, mc._job(job)


def _size(args):
    v, job = args
    install(v)
    return v, sc._job(job)


def listing():
    """Each changed monster's picks and Health per Level, every variant."""
    out = []
    for name in ("Hedge Knight", "Warpriest", "Deadbough Priest", *HEAVY, "Black Knight"):
        for v in VARIANTS:
            install(v)
            cells = []
            for L in (1, 2, 3, 4, 5):
                e = se.get_enemy(f"{name}@{L}")
                cells.append(f"L{L} {e['max_health']:g}")
            out.append(f"{name:18s} {v:6s} " + "  ".join(cells))
        install("one6")
        picks, _ = se._pruned_picks(se._manual_row(f"{name}@3"), [])
        out.append(f"{'':18s} one6 picks at L3: {'; '.join(picks)}")
    return "\n".join(out)


if __name__ == "__main__":
    if sys.argv[1:] == ["list"]:
        print(listing())
        sys.exit()
    mjobs, sjobs = [], []
    for L in (1, 2, 3, 4, 5):
        groups = tc.groups(L, ps.MID[L])
        encs = mc.encounters(L, 40, 1)
        for v in VARIANTS:
            for gi in range(len(groups)):
                for e in encs:
                    mjobs.append((v, (L, gi, "|".join(e), list(e), 30, 1)))
        for kind, label, enc in sc.encounters(L):
            if label not in SIZE_LABELS:
                continue
            c = dict(level=L, kind=kind, label=label, enc=enc, minion_hp=round(1 / 3, 3))
            for v in VARIANTS:
                for gi in range(len(groups)):
                    sjobs.append((v, (c, ps.MID[L], gi, 60)))
    res = collections.defaultdict(list)
    touched = ("Hedge Knight", "Warpriest", "Deadbough Priest", *HEAVY)
    with mp.Pool(os.cpu_count(), maxtasksperchild=50) as pool:
        for v, r in pool.imap_unordered(_manual, mjobs, chunksize=4):
            part = ("heavy" if any(n in HEAVY for n in r["enemies"]) else
                    "changed" if any(n in touched for n in r["enemies"]) else "other")
            res[("manual", v, r["level"], part)].append(r)
            res[("manual", v, r["level"], "all")].append(r)
        for v, r in pool.imap_unordered(_size, sjobs, chunksize=2):
            res[("size", v, r["label"])].append(r)
    line = lambda rs: (f"{100 * (1 - st.mean(r['won'] for r in rs)):.1f}% / {100 * st.mean(r['down'] for r in rs):.0f}% / "
                       f"{st.mean(r['rounds'] for r in rs):.1f}" if rs else "-")
    names = {"heavy": "with a Heavy monster", "changed": "with a Hedge Knight or priest (no Heavy)",
             "other": "with none of them", "all": "all"}
    out = ["Lost / Down / Rounds, middle of the band.", "",
           "| Manual fights | Today (Heavy 4, overspend) | One budget, Heavy 4 | One budget, Heavy 6 |",
           "|---|---|---|---|"]
    for L in (1, 2, 3, 4, 5):
        for part in ("all", "heavy", "changed", "other"):
            out.append(f"| Level {L}, {names[part]} | " + " | ".join(line(res[("manual", v, L, part)]) for v in VARIANTS) + " |")
    out += ["", "| Encounter (Levels 1-5) | Today | One budget, Heavy 4 | One budget, Heavy 6 |", "|---|---|---|---|"]
    for label in SIZE_LABELS:
        out.append(f"| {label} | " + " | ".join(line(res[("size", v, label)]) for v in VARIANTS) + " |")
    out += ["", "```", listing(), "```"]
    text = "\n".join(out)
    print(text)
    open(os.path.join(_paths.ROOT, "results/enemy_stats/one_budget.txt"), "w").write(text + "\n")
