"""A broad pass over every modeled Technique and Feature (2026-10-28).

Shallow on purpose: each test is a few hundred paired fights, enough to
sort what clearly helps from what clearly doesn't, and to say where a
closer look is worth it. The designer asked for it to see how well the
sim can tell what something is worth.

Techniques. Each one goes on up to three Level 3 sample characters, in
their own party: anyone who already knows it (the test takes it off),
then the two who need the fewest prereq ranks for it (party.fit), no
more than MAX_PREREQ_XP, and whose build loads with it (an Unarmed
Technique needs an Unarmed row, ...). A Style replaces the host's own
Style, since you're only ever in one. Two readings for each:
- "free": the Technique on top of the build, with any prereq ranks it
  needs (taken off: just gone). What it's worth.
- "swap": the XP evened out in Defense and other side Skill ranks
  (party.DONORS), the build's total unchanged. Whether a player would
  take it over what they'd give up.

Features. Each Feature of the four Buildables in one copy at a fixed
Level, against the same copy without it: no XP changes hands, so the
difference is the Feature, per point it costs.

Scored as compare_builds does: Health left in points at enemy Health
x1.75, paired on the same seeds, with how often the thing fired (log
lines naming it, per fight). Results go to technique_pass.csv; the
write-up is TECHNIQUE_PASS.md.

    python3 technique_pass.py            # everything, N fights a mix
    python3 technique_pass.py -n 50 --only T07   # a slice

The committed technique_pass.csv is `-n 200` under the default
Assassin reading ('softest'); technique_pass_current.csv is the same
under the old one ('current'), for comparison (its Features predate the
traded-point designs for Spirit Blessing and Beornhard's War Magic).
`--seed 50000` reruns on a fresh set of fights.
"""
import argparse
import csv
import json
import math
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T  # noqa: E402
import game_data  # noqa: E402
import techniques as tq  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LEVEL = 3
MULT = 1.75
MAX_PREREQ_XP = 6
SEED = 0  # --seed: another set of fights, to see how well a reading repeats
BUILDABLES = ("T072", "T120", "T104", "T105")
PARTIES = {
    "S": ["Enith (L3, proposed)", "Felix (L3, proposed)", "Jackal (L3)", "Hanforth (L3)"],
    "U": ["Browndog (L3)", "Ashleigh (L3, proposed)", "Sable (L3, proposed)", "Beornhard (L3)"],
    "H": ["Hilde (L3)", "Carrick (L3)", "Hanforth (L3)", "Beornhard (L3)"],
}
HOSTS = {"Enith (L3, proposed)": "S", "Felix (L3, proposed)": "S", "Jackal (L3)": "S", "Hanforth (L3)": "S",
         "Browndog (L3)": "U", "Ashleigh (L3, proposed)": "U", "Sable (L3, proposed)": "U", "Beornhard (L3)": "U",
         "Hilde (L3)": "H", "Carrick (L3)": "H"}
# Feature probes: (host, which of its copies the probe replaces, the
# probe copy's other Features). The probe takes the place of a copy the
# host already uses (the first Maneuver is the opening move), keeping the
# copy's place so the Choices column's per-copy picks stay lined up.
# A string instead of a dict swaps points of that Feature for the one
# being tested, at the Level's whole budget: Spirit Blessing, where an
# empty copy still gets cast and moves which Blessing the healer casts
# when, so it's measured against a point of Shielding instead. A (dict,
# string) pair does the same on top of the dict's Features: Beornhard's
# War Magic, where a plain Lance copy is one more use of his War Magic
# Weapon but any Feature makes it a Technique attack of its own, which
# the sim spends differently (about -0.35 Health whatever the Feature).
FEATURE_HOSTS = {
    "T072": [("Hilde (L3)", 1, {}), ("Sable (L3, proposed)", 1, {})],
    "T120": [("Beornhard (L3)", 1, ({"Lance": 1}, "Destructive")), ("Enith (L3, proposed)", 3, {"Lance": 1})],
    "T104": [("Hanforth (L3)", 1, "Shielding")],
    "T105": [("Hanforth (L3)", 1, {})],
}
ELEMENT_FEATURES = ("Turn Elements", "Elemental", "Elemental Enhancement")


def short(name):
    # "Shugen School - Arrow Finds Only Mist" logs as "Arrow Finds Only Mist".
    return name.split(" - ", 1)[-1]


def run(names, who, edits, n, watch=None, row_changes=None):
    """Per-fight results for `names`, `who` built with `edits` (None: as
    is), and how many log lines named `watch` per fight."""
    rows = party._rows()
    last = []

    def make(tier, good_luck=0):
        last[:] = [party.make_pc(m, i, good_luck, rows=rows, edits=edits if m == who else None,
                                 row_changes=row_changes if m == who else None)
                   for i, m in enumerate(names, 1)]
        return last
    cs.make_party = make
    out, fires = [], 0
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(n):
            tr = [] if watch else None
            r = cs.run_fight(1, LEVEL, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[LEVEL][mix]),
                             seed=100_000 * mi + k + SEED, trace=tr)
            won = r['winner'] == 'party'
            out.append((sum(max(0, p['health']) for p in last) if won else 0, won, r['rounds']))
            if watch:
                fires += sum(1 for e in tr if e.get('side') == 'party' and e.get('unit', '').startswith(who.split(' (')[0])
                             and watch in f"{e.get('via', '')} {e.get('note', '')} {e.get('effects', '')}")
    return out, fires / len(out)


def paired(base, var):
    d = [v[0] - b[0] for b, v in zip(base, var)]
    w = [float(v[1]) - float(b[1]) for b, v in zip(base, var)]
    return st.mean(d), 1.96 * st.stdev(d) / math.sqrt(len(d)), 100 * st.mean(w)


_BASE = {}


def base_run(party_key, n):
    if (party_key, n) not in _BASE:
        _BASE[(party_key, n)] = run(PARTIES[party_key], None, None, n)[0]
    return _BASE[(party_key, n)]


def choices_for(row, build):
    """The row's Choices, less any Technique the build no longer has."""
    have = {game_data.technique_name(t["id"]) for t in build["techniques"]}
    picks = party._choices(row.get("Choices"))
    kept = {k: v for k, v in picks.items() if k in have}
    if kept == picks:
        return None
    return {"Choices": "; ".join(f"{k}: {', '.join(v)}" for k, v in kept.items())}


def styles_of(build):
    return [t for t in build["techniques"] if "Style" in (game_data.techniques()[t["id"]].get("Tags") or "")]


def plan_technique(tid):
    """The hosts and builds for one Technique: [(host, mode, free build,
    swap build, notes)], and why other hosts were passed over."""
    rows = party._rows()
    name = game_data.technique_name(tid)
    is_style = "Style" in (game_data.techniques()[tid].get("Tags") or "")
    lo, _ = game_data.level_range(tid) or (1, 1)
    knowers, others, skipped = [], [], []
    for host in HOSTS:
        b = party.read_build(rows[host]["Build"])
        copies = [i for i, t in enumerate(b["techniques"]) if t["id"] == tid]
        try:
            if copies:
                rem = [{"id": tid, "copy": 1}]
                free, notes, _ = party.fit(b, remove=rem, free=True)
                swap, snotes, _ = party.fit(b, remove=rem, cap=LEVEL + 2)
                party.make_pc(host, rows=rows, edits={"build": free}, row_changes=choices_for(rows[host], free))
                knowers.append((host, "take off", free, swap, snotes, 0))
                continue
            add = [{"id": tid, "level": game_data.fixed_level(tid) or lo}]
            rem = [{"id": t["id"], "copy": 1} for t in styles_of(b)] if is_style else []
            free, notes, bought = party.fit(b, add=add, remove=rem, free=True)
            if bought > MAX_PREREQ_XP:
                skipped.append(f"{host}: prereqs cost {bought} XP")
                continue
            swap, snotes, _ = party.fit(b, add=add, remove=rem, cap=LEVEL + 2)
            party.make_pc(host, rows=rows, edits={"build": free})  # loads?
            relevant = {s.strip() for s in (game_data.techniques()[tid].get("Relevant Skills") or "").split(",")}
            match = 0 if party.make_pc(host, rows=rows)["attack_skill"] in relevant else 1
            mode = "add" + (f", replacing {', '.join(game_data.technique_name(r['id']) for r in rem)}" if rem else "")
            others.append((host, mode, free, swap, list(dict.fromkeys(notes + snotes)), (bought, match)))
        except party.BuildError as e:
            skipped.append(f"{host}: {e}")
    others.sort(key=lambda o: o[5])
    picked = knowers[:2] + others[:3 - min(2, len(knowers))]
    return name, picked, skipped


def job_technique(args):
    tid, n = args
    name, picked, skipped = plan_technique(tid)
    out = []
    rows = party._rows()
    for host, mode, free, swap, notes, _ in picked:
        key = HOSTS[host]
        base = base_run(key, n)
        row = choices_for(rows[host], free)
        try:
            fv, fires = run(PARTIES[key], host, {"build": free}, n, watch=short(name), row_changes=row)
            sv, _ = run(PARTIES[key], host, {"build": swap}, n, row_changes=row)
        except party.BuildError as e:
            out.append(dict(kind="technique", id=tid, name=name, host=host, party=key, mode=mode,
                            notes=f"doesn't load: {e}"))
            continue
        # paired(a, b) is b minus a. Taking it off, the reading is what
        # knowing it is worth: the build as is, minus the build without it.
        if mode == "take off":
            f, s = paired(fv, base), paired(sv, base)
            _, fires = run(PARTIES[key], host, None, n, watch=short(name))
        else:
            f, s = paired(base, fv), paired(base, sv)
        out.append(dict(kind="technique", id=tid, name=name, host=host, party=key, mode=mode,
                        level=game_data.fixed_level(tid) or (game_data.level_range(tid) or (1, 1))[0],
                        style="Style" in (game_data.techniques()[tid].get("Tags") or ""),
                        free=round(f[0], 2), free_margin=round(f[1], 2), free_wins=round(f[2], 1),
                        swap=round(s[0], 2), swap_margin=round(s[1], 2), swap_wins=round(s[2], 1),
                        fires=round(fires, 2), notes="; ".join(notes)))
    if not picked:
        out.append(dict(kind="technique", id=tid, name=name, host="", notes="no host: " + " | ".join(skipped)))
    return out


def feature_probes():
    """(Buildable, host, Level, base Features, Feature, copies) for every
    Feature: one copy of it, and three when it's a 1-point Feature with no
    cap, at the lowest Level whose budget takes it (Level 3 for
    Advanced)."""
    out = []
    for tid, hosts in FEATURE_HOSTS.items():
        budget = game_data.feature_budget(tid)
        rows = [r for r in csv.DictReader(open(os.path.join(HERE, "..", "..", "scripts", "features.csv"),
                                               encoding="utf-8-sig")) if r["Technique ID"] == tid]
        for host, copy_no, core in hosts:
            if isinstance(core, (str, tuple)):
                fixed, swap_from = core if isinstance(core, tuple) else ({}, core)
                fixed_cost = sum(int(next(r["Point Cost"] for r in rows if r["Feature Name"] == k)) * v
                                 for k, v in fixed.items())
                for r in rows:
                    fname, cost = r["Feature Name"], int(r["Point Cost"] or 0)
                    if fname == swap_from or fname in fixed:
                        continue
                    # The lowest Level with room for the fixed Features, the
                    # tested one and a point of swap_from (Advanced: Level 3).
                    lvl = next((L for L, (pts, adv) in sorted(budget.items())
                                if pts >= fixed_cost + cost + 1 and (adv or r["Tier"] != "Advanced")), None)
                    if lvl is None:
                        continue
                    base = dict(fixed, **{swap_from: budget[lvl][0] - fixed_cost})
                    out.append((tid, host, copy_no, lvl, base, fname, 1, cost))
                continue
            core_cost = sum(int(next(r["Point Cost"] for r in rows if r["Feature Name"] == k)) * v
                            for k, v in core.items())
            for r in rows:
                fname, cost = r["Feature Name"], int(r["Point Cost"] or 0)
                if fname in core:
                    continue
                cap = int(r["Max Copies"]) if r["Max Copies"].strip() else None
                for k in ((1, 3) if cost == 1 and cap is None else (1,)):
                    need = core_cost + cost * k - int(r["Bonus Points"] or 0) * k
                    lvl = next((L for L, (pts, adv) in sorted(budget.items())
                                if pts >= need and (adv or r["Tier"] != "Advanced")), None)
                    if lvl is None:
                        continue
                    out.append((tid, host, copy_no, lvl, core, fname, k, cost))
    return out


def job_feature(args):
    (tid, host, copy_no, lvl, core, fname, k, cost), n = args
    rows = party._rows()
    b = party.read_build(rows[host]["Build"])
    key = HOSTS[host]
    spec = {"id": tid, "copy": copy_no, "level": lvl}
    spec_core = next((c for h, n, c in FEATURE_HOSTS[tid] if h == host), None)
    swap_from = spec_core if isinstance(spec_core, str) else spec_core[1] if isinstance(spec_core, tuple) else None
    var_f = dict(core, **{fname: k})
    if swap_from:
        # Points of swap_from traded for this Feature, the budget kept.
        var_f[swap_from] = core[swap_from] - cost * k
        if var_f[swap_from] <= 0:
            del var_f[swap_from]
    base_b = party.apply_edits(b, {"replace": [dict(spec, features=dict(core))]})
    var_b = party.apply_edits(b, {"replace": [dict(spec, features=var_f)]})
    row = None
    if fname in ELEMENT_FEATURES:
        # Fire, for the copy the probe replaces: the element enemies here use.
        picks = party._choices(rows[host].get("Choices"))
        tname = game_data.technique_name(tid)
        mine = picks.get(tname, [])
        mine = (mine + [""] * copy_no)[:max(len(mine), copy_no)]
        mine[copy_no - 1] = "Fire"
        picks[tname] = mine
        row = {"Choices": "; ".join(f"{t}: {', '.join(v)}" for t, v in picks.items())}
    rec = dict(kind="feature", id=tid, name=f"{game_data.technique_name(tid)}: {fname}" + (f" x{k}" if k > 1 else ""),
               host=host, party=key, level=lvl, points=cost * k,
               mode=f"for {cost * k} point(s) of {swap_from}" if swap_from else "added")
    try:
        base, _ = run(PARTIES[key], host, {"build": base_b}, n, row_changes=row)
        var, fires = run(PARTIES[key], host, {"build": var_b}, n, watch=fname, row_changes=row)
    except party.BuildError as e:
        return [dict(rec, notes=f"doesn't load: {e}")]
    d = paired(base, var)  # var minus base
    per = d[0] / (cost * k) if cost * k else None
    return [dict(rec, free=round(d[0], 2), free_margin=round(d[1], 2), free_wins=round(d[2], 1),
                 per_point=None if per is None else round(per, 2), fires=round(fires, 2),
                 notes="fires: log lines mentioning the Feature")]


def _init(seed=0, overrides=()):
    global SEED
    T.ENEMY_HEALTH_MULT = MULT
    SEED = seed
    for o in overrides:
        k, _, v = o.partition("=")
        try:
            v = json.loads(v)
        except ValueError:
            pass
        setattr(T, k, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=100, help="fights per mix")
    ap.add_argument("--only", help="IDs starting with this")
    ap.add_argument("--features", action="store_true", help="the Feature probes only")
    ap.add_argument("--techniques", action="store_true", help="the Techniques only")
    ap.add_argument("-j", type=int, default=os.cpu_count(), help="processes")
    ap.add_argument("-o", default=os.path.join(HERE, "technique_pass.csv"))
    ap.add_argument("--seed", type=int, default=0, help="offset every fight's seed (50000: a fresh set)")
    ap.add_argument("--ids", help="comma-separated IDs (Techniques only)")
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE")
    a = ap.parse_args()
    _init(a.seed, a.s)
    ids = [t for t in sorted(tq.REGISTRY) if t not in BUILDABLES and (not a.only or t.startswith(a.only))
           and (not a.ids or t in a.ids.split(","))]
    jobs = []
    if not a.features:
        jobs += [(job_technique, (t, a.n)) for t in ids]
    if not a.techniques:
        jobs += [(job_feature, (p, a.n)) for p in feature_probes() if not a.only or p[0].startswith(a.only)]
    results = []
    if a.ids:
        a.techniques = True
        jobs = [j for j in jobs if j[0] is job_technique]
    with mp.Pool(a.j, initializer=_init, initargs=(a.seed, a.s)) as pool:
        for i, res in enumerate(pool.imap_unordered(_call, jobs), 1):
            results += res
            if i % 20 == 0:
                print(f"{i}/{len(jobs)}", flush=True)
    keys = ["kind", "id", "name", "host", "party", "mode", "level", "style", "points", "free", "free_margin",
            "free_wins", "swap", "swap_margin", "swap_wins", "per_point", "fires", "notes"]
    results.sort(key=lambda r: (r["kind"], r["id"], r.get("name", ""), r.get("host", "")))
    with open(a.o, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in keys})
    print(f"wrote {a.o}: {len(results)} rows")


def _call(job):
    fn, args = job
    return fn(args)


if __name__ == "__main__":
    main()
