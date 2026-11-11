"""The on-level baseline against the table targets (2026-11-02).

Per the designer: on-level fights should be won almost always, with
some threat, so a build that trivializes them or still goes Down
stands out. The targets (TABLE_PLAY_NOTES.md, 2026-10-08): about three
rounds (five at most), the party basically never loses, someone goes
Down less than once in every few fights, someone is Wounded about every
other fight, a hit enemy acts again about half the time.

This plays the day standard (day_sim: two fights, care in between) at
the parties' own Level, for a spread of the normalized parties
(builds/normalized/) picked from party_mixes.py's own-Level ranking,
and reports each fight of the day separately, since the second starts
hurt. `SIM_SET` tries a lever for one run.

    python3 experiments/yardsticks/baseline_check.py -L 3 -n 100
    SIM_SET="ENEMY_HEALTH_MULT=0.8" python3 experiments/yardsticks/baseline_check.py -L 3 -n 100
"""
import argparse
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401 (the simulator's core, a folder or two up)
import day_sim as ds  # noqa: E402
import party_mixes as pm  # noqa: E402
import party_power as pp  # noqa: E402
import build_optimizer as bo  # noqa: E402
import sample_enemies as se  # noqa: E402

_ORIG = {}
PICKS = 12  # parties, evenly spread over party_mixes' own-Level ranking


def parties(level, k=PICKS):
    d = json.load(open(os.path.join(_paths.ROOT, "hall_of_fame", "runs_levelup", f"mixes_l{level}.json")))
    ranked = sorted(d["mixes"], key=lambda m: m["own"])
    idx = sorted({round(i * (len(ranked) - 1) / (k - 1)) for i in range(k)})
    return [tuple(ranked[i]["party"]) for i in idx]


def _job(args):
    trio, level, n, seed, trim = args
    for mix in se.CURRENT_MIXES:
        # Workers run several jobs, so trim from the untouched list.
        base = _ORIG.setdefault((level, mix), list(se.ENCOUNTERS[level][mix]))
        se.ENCOUNTERS[level][mix] = trim_mix(base) if trim == "all" else list(base)
    if trim in ("first", "second"):
        # One fight of the day a Slot smaller: drop the same enemies
        # trim_mix would, from the encounter already built.
        which = 1 if trim == "first" else 2
        run_fight = _ORIG.setdefault("run_fight", ds.cs.run_fight)

        def trimmed(*a, **kw):
            if kw.get("day_fight") == which:
                names = trim_mix([e["name"] for e in kw["enemies"]])
                kept = []
                for e in kw["enemies"]:
                    if e["name"] in names:
                        names.remove(e["name"])
                        kept.append(e)
                kw["enemies"] = kept
            return run_fight(*a, **kw)
        ds.cs.run_fight = trimmed
    elif "run_fight" in _ORIG:
        ds.cs.run_fight = _ORIG["run_fight"]
    norm = pm.normalized(level)
    if trio == "stand-ins":
        si = pp.STAND_IN[level]
        names, swaps = [si] * 4, {si: ({"build": pp.stand_in(level)}, None)}
    else:
        names, swaps = [], {}
        for arch in trio:
            row, b = norm[arch]
            names.append(row)
            swaps[row] = ({"build": b}, bo.choices_for(ds.party._rows()[row], b))
    ds.set_mult(ds.MULT)
    recs = ds.run(names, swaps, level, n, seed=seed)
    return trio, [r.get("per_fight", []) for r in recs]


def trim_mix(names):
    """One enemy Slot fewer: the last full-Slot enemy, or two Minions."""
    out = list(names)
    minions = [n for n in out if "Goblin Cutthroat" in n]
    if len(minions) >= 2:
        for _ in range(2):
            out.remove(minions[0])
    else:
        out.pop(0)
    return out


def stats(days):
    out = {}
    for f in (1, 2):
        fights = [d[f - 1] for d in days if len(d) >= f]
        if not fights:
            continue
        won = [x for x in fights if x["won"]]
        # A hit enemy's first hit, as calibrate.py's "after first hit".
        ag = [sum(x["again_first"][i] for x in fights) for i in (0, 1)]
        out[f] = dict(n=len(fights), lose=100 * (1 - len(won) / len(fights)),
                      rounds=st.mean(x["rounds"] for x in won) if won else 0,
                      long=100 * sum(x["rounds"] > 5 for x in won) / max(1, len(won)),
                      down=100 * sum(x["downs"] > 0 for x in fights) / len(fights),
                      downs=st.mean(x["downs"] for x in fights),
                      wounded=100 * sum(x["wounded"] for x in fights) / len(fights),
                      again=100 * ag[0] / max(1, ag[1]))
    out["day"] = 100 * sum(len(d) == 2 and d[1]["won"] for d in days) / len(days)
    return out


def line(label, s):
    parts = [f"{label:42s} days won {s['day']:5.1f}%"]
    for f in (1, 2):
        if f in s:
            x = s[f]
            parts.append(f"F{f}: lose {x['lose']:4.1f}% rds {x['rounds']:.1f} (>5 {x['long']:2.0f}%) "
                         f"Down {x['down']:3.0f}% Wnd {x['wounded']:3.0f}% again {x['again']:3.0f}%")
    return " | ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=100, help="days per mix per party (4n days)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--trim", choices=("none", "all", "first", "second"), default="none",
                    help="fights one enemy Slot smaller: every one, or only the day's first or second")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", help="write the readings here (json)")
    a = ap.parse_args()
    groups = ["stand-ins"] + parties(a.L)
    with mp.Pool(a.j) as pool:
        res = pool.map(_job, [(g, a.L, a.n, a.seed, a.trim) for g in groups])
    out, every = {}, []
    for trio, days in res:
        label = trio if isinstance(trio, str) else "+".join(trio)
        out[label] = stats(days)
        if trio != "stand-ins":
            every += days
        print(line(label, out[label]), flush=True)
    out["all normalized"] = stats(every)
    print(line("ALL NORMALIZED (pooled)", out["all normalized"]))
    if a.o:
        json.dump(dict(level=a.L, trim=a.trim, readings=out), open(a.o, "w"), indent=1)


if __name__ == "__main__":
    main()
