"""What would a min-maxer build? (2026-10-28)

Per the designer: search the legal builds for each archetype at Levels 2
and 3 and keep the ones that do the most for their XP, as a Hall of Fame
for each version of the game (hall_of_fame/), so it shows over time
which mechanics and combinations deliver too much.

An archetype is one of the sample characters: its weapon, armor,
background and row stay as they are (items aren't searched), and
everything an XP buys is open: Stats, Skills, Techniques and their
Levels, a Buildable's Features. A build is legal when it spends its XP
(125 at Level 2, 175 at Level 3, at most 2 left over), no rank is over
the cap (4 at Level 2, 5 at Level 3) or a Stat under 1, every Prereq
Check and Feature prerequisite is met, Feature budgets hold, a Technique
appears once unless it's Buildable or Duplicate, there's one Style at
most, and the sim loads it. A Technique or Feature that needs a choice
(Temper Soulblade, the element and Tormenting Curse Features) is kept
where the sample has it but never added.

The score is the party's Health left in points (losses 0) with the
build in its sample character's place, at enemy Health x1.75 against
the Level's four encounter mixes: the same yardstick as
technique_pass.py. The search is elitist and evolutionary: a small
population, each generation a batch of children made by one to three
moves (shift a rank, add, drop or swap a Technique, rework a Buildable
copy), repaired back to legal by buying prereqs and then trimming or
spending ranks at random, scored on one fixed set of fights. The best
few are then scored again on a fresh set, since the winners of a search
are flattered by the fights they were picked on.

The day score (--score day, 2026-10-29, the designer's pick): the same
search on day_sim.py's morning Health (two fights, the party's healing,
a night's rest, at enemy Health x1.0), so healing and Health a night
count. Morning Health counts a bigger pool in full, so the finalists are
then scored on days in a row before a fight is lost (up to ten, fresh
days), which doesn't, and ranked by that.

    python3 build_optimizer.py --arch Hilde -L 3            # one search
    python3 build_optimizer.py --all -g 60 -n 100           # everything
    python3 build_optimizer.py --hall                       # write hall_of_fame/ from saved results
"""
import argparse
import copy
import csv
import json
import multiprocessing as mp
import os
import pickle
import random
import re
import statistics as st
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T  # noqa: E402
import game_data  # noqa: E402
import techniques as tq  # noqa: E402
import day_sim  # noqa: E402
import threshold  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MULT = 1.75
BUDGET = {2: 125, 3: 175}
FULL_BUDGET = dict(BUDGET)  # what an export says; --combat-budget searches within combat_xp.COMBAT_BUDGET
CAP = {2: 4, 3: 5}
SLACK = 2
VALIDATE_SEED = 50_000
# 'fight' (Health left after one fight) or 'day' (day_sim.py); set by
# --score before the Pool forks.
SCORE = 'fight'
# --score daywin (2026-10-30): the share of days won at enemy Health
# x DAYWIN_X (--at-x), set near where the sample party wins half its days.
# It counts no Health at all, so a bigger pool scores only by winning.
DAYWIN_X = None
DAYS = 10  # the day score's days in a row, at most
# Archetype: the sample character (Level 3 name; Level 2 swaps "(L3" for "(L2"), and its party.
ARCHES = {
    "Hilde": "heavy front-liner", "Browndog": "armored tank", "Jackal": "thrown skirmisher",
    "Carrick": "knife-throwing rogue", "Felix": "unarmed monk", "Enith": "spellblade duelist",
    "Sable": "archer", "Beornhard": "battlemage", "Hanforth": "healer", "Ashleigh": "bard",
}
PARTIES = {
    3: {"S": ["Enith (L3, proposed)", "Felix (L3, proposed)", "Jackal (L3)", "Hanforth (L3)"],
        "U": ["Browndog (L3)", "Ashleigh (L3, proposed)", "Sable (L3, proposed)", "Beornhard (L3)"],
        "H": ["Hilde (L3)", "Carrick (L3)", "Hanforth (L3)", "Beornhard (L3)"]},
    2: {"S": ["Enith (L2, proposed)", "Felix (L2, proposed)", "Jackal (L2)", "Hanforth (L2)"],
        "U": ["Browndog (L2)", "Ashleigh (L2, proposed)", "Sable (L2, proposed)", "Beornhard (L2)"],
        "H": ["Hilde (L2)", "Carrick (L2)", "Hanforth (L2)", "Beornhard (L2)"]},
}
PARTY_OF = {"Enith": "S", "Felix": "S", "Jackal": "S", "Hanforth": "S", "Browndog": "U", "Ashleigh": "U",
            "Sable": "U", "Beornhard": "U", "Hilde": "H", "Carrick": "H"}
NEEDS_CHOICE = {"T002", "T003"}
CHOICE_FEATURES = {"Turn Elements", "Elemental", "Elemental Enhancement", "Tormenting Curse"}
BUILDABLES = ("T072", "T120", "T104", "T105")


def row_name(arch, level):
    """The sample character's row in its party (not a variant row)."""
    for n in PARTIES[level][PARTY_OF[arch]]:
        if n.startswith(arch + " ("):
            return n
    raise KeyError(f"no Level {level} row for {arch}")


# ---- The catalog: what can be bought ----

def _tags(tid):
    return game_data.techniques()[tid].get("Tags") or ""


def is_style(tid):
    return "Style" in _tags(tid)


def stackable(tid):
    return "Duplicate" in _tags(tid) or "Buildable" in _tags(tid) or tid in BUILDABLES


def pool():
    """Every modeled Technique the search may add."""
    return sorted(t for t in tq.REGISTRY if t not in NEEDS_CHOICE)


def feature_rows(tid):
    return [r for r in _features_csv() if r["Technique ID"] == tid]


_FCSV = []


def _features_csv():
    if not _FCSV:
        _FCSV.extend(csv.DictReader(open(os.path.join(HERE, "..", "..", "scripts", "features.csv"),
                                         encoding="utf-8-sig")))
    return _FCSV


def random_features(tid, level, rng):
    """A random legal Feature set for a Buildable copy at `level`, using
    up its budget (choice Features left out)."""
    pts, adv = game_data.feature_budget(tid)[level]
    rows = [r for r in feature_rows(tid) if r["Feature Name"] not in CHOICE_FEATURES
            and (adv or r["Tier"] != "Advanced") and r["Feature Name"] != "Bare-Handed"]
    feats = {}
    if tid == "T120" and rng.random() < 0.8:
        feats["Lance"] = 1  # most War Magic attacks want a shape
        pts -= 1
    for _ in range(20):
        ok = [r for r in rows if int(r["Point Cost"] or 0) <= pts and int(r["Point Cost"] or 0) > 0
              and (not r["Max Copies"].strip() or feats.get(r["Feature Name"], 0) < int(r["Max Copies"]))]
        if not ok or pts <= 0:
            break
        r = rng.choice(ok)
        feats[r["Feature Name"]] = feats.get(r["Feature Name"], 0) + 1
        pts -= int(r["Point Cost"])
    return feats


# ---- Legality ----

_ADD_PREREQ = re.compile(r"^\(?([A-Za-z ,]+?)\)?\s+(\d+)$")


def feature_prereqs(build):
    """Unmet Feature prerequisites (features.csv's Additional Prereq, a
    Skill or an "A, B, or C" list and a rank), as prereq_needs gives them."""
    pts = party._points(build)
    out = []
    for t in build["techniques"]:
        for f in t.get("features") or []:
            row = next((r for r in feature_rows(t["id"]) if r["Feature Name"] == f["name"]), None)
            req = (row or {}).get("Additional Prereq", "").strip()
            m = _ADD_PREREQ.match(req)
            if not m:
                continue
            opts = [o.strip() for o in re.split(r",|\bor\b", m.group(1)) if o.strip()]
            n = int(m.group(2))
            if max(pts.get(o, 0) for o in opts) < n:
                out.append((opts, n, f"{f['name']} needs {req}"))
    return out


def problems(build, level):
    out = []
    cap = CAP[level]
    for k, v in build["statPoints"].items():
        if not 1 <= int(v) <= cap:
            out.append(f"{k} {v}")
    for k, v in build["skillPoints"].items():
        if not 0 <= int(v) <= cap:
            out.append(f"{k} {v}")
    spent = sum(party.xp_spent(build))
    if not BUDGET[level] - SLACK <= spent <= BUDGET[level]:
        out.append(f"XP {spent}")
    if party.prereq_needs(build) or feature_prereqs(build):
        out.append("prereqs")
    ids = [t["id"] for t in build["techniques"]]
    if any(ids.count(i) > 1 and not stackable(i) for i in set(ids)):
        out.append("duplicate")
    if sum(1 for i in ids if is_style(i)) > 1:
        out.append("two Styles")
    return out


# ---- Moves ----

def _box(build, name):
    return build["statPoints"] if name in build["statPoints"] else build["skillPoints"]


def _rank(build, name):
    return int(_box(build, name).get(name, 0))


def _cost(build, name, to):
    k = 2 if name in build["statPoints"] else 1
    frm = _rank(build, name)
    return sum(k * r for r in range(frm + 1, to + 1)) if to > frm else -sum(k * r for r in range(to + 1, frm + 1))


def _names(build):
    return list(build["statPoints"]) + list(build["skillPoints"])


def buy_prereqs(build, level):
    for _ in range(40):
        need = party.prereq_needs(build) + feature_prereqs(build)
        if not need:
            return True
        opts, n, _ = need[0]
        if opts is None or n > CAP[level]:
            return False
        opts = [o for o in opts if o in build["statPoints"] or o in build["skillPoints"]]
        if not opts:
            return False
        o = min(opts, key=lambda x: _cost(build, x, n))
        _box(build, o)[o] = n
    return False


def fit_budget(build, level, rng):
    """A sample build cut down to BUDGET[level] (--combat-budget): its
    out-of-combat Techniques go first, then Techniques from the end,
    until the ranks can be trimmed to fit."""
    import combat_xp
    b = copy.deepcopy(build)
    b["techniques"] = [t for t in b["techniques"] if combat_xp.in_fight(t["id"])]
    # Skills that don't come up in a fight are the other 45 (30 at Level 2).
    combat_skills = combat_xp.split(b)[2]
    for k in b["skillPoints"]:
        if k not in combat_skills:
            b["skillPoints"][k] = 0
    while True:
        trial = copy.deepcopy(b)
        if repair(trial, level, rng):
            return trial
        if not b["techniques"]:
            return None
        b["techniques"].pop()


def repair(build, level, rng, keep=()):
    """Back to legal: prereqs bought, then ranks trimmed or bought at
    random until the XP is spent (never trimming below a prereq or a
    rank in `keep`). False if it can't."""
    if not buy_prereqs(build, level):
        return False
    budget = BUDGET[level]
    for _ in range(400):
        spent = sum(party.xp_spent(build))
        if spent > budget:
            cands = [n for n in _names(build) if _rank(build, n) > (1 if n in build["statPoints"] else 0)
                     and n not in keep]
            rng.shuffle(cands)
            for n in cands:
                _box(build, n)[n] = _rank(build, n) - 1
                if not party.prereq_needs(build) and not feature_prereqs(build):
                    break
                _box(build, n)[n] = _rank(build, n) + 1
            else:
                return False
        elif spent < budget - SLACK or (spent < budget and rng.random() < 0.7):
            left = budget - spent
            cands = [n for n in _names(build) if _rank(build, n) < CAP[level] and _cost(build, n, _rank(build, n) + 1) <= left]
            if not cands:
                break
            n = rng.choice(cands)
            _box(build, n)[n] = _rank(build, n) + 1
        else:
            break
    return not problems(build, level)


def _entry(tid, level=None, features=None):
    lv = game_data.fixed_level(tid)
    e = {"id": tid, "name": game_data.technique_name(tid), "level": f"Lv {lv}" if lv else level, "xp": 3 * (lv or level)}
    if features is not None:
        e["features"] = [{"name": k, "count": v} for k, v in features.items()]
    return e


def _random_level(tid, rng):
    lo, hi = game_data.level_range(tid) or (1, 1)
    return rng.randint(lo, min(hi, 4))


def mutate(build, level, rng):
    b = copy.deepcopy(build)
    move = rng.choice(["shift", "shift", "add", "add", "drop", "swap", "rework"])
    keep = ()
    if move == "shift":
        n = rng.choice(_names(b))
        if _rank(b, n) >= CAP[level]:
            return None
        _box(b, n)[n] = _rank(b, n) + 1
        keep = (n,)
    elif move in ("add", "swap"):
        if move == "swap" and b["techniques"]:
            b["techniques"].pop(rng.randrange(len(b["techniques"])))
        tid = rng.choice(POOL)
        ids = [t["id"] for t in b["techniques"]]
        if tid in ids and not stackable(tid):
            return None
        if is_style(tid):
            b["techniques"] = [t for t in b["techniques"] if not is_style(t["id"])]
        if tid in BUILDABLES:
            lv = _random_level(tid, rng)
            b["techniques"].append(_entry(tid, lv, random_features(tid, lv, rng)))
        else:
            b["techniques"].append(_entry(tid, None if game_data.fixed_level(tid) else _random_level(tid, rng)))
    elif move == "drop":
        if not b["techniques"]:
            return None
        b["techniques"].pop(rng.randrange(len(b["techniques"])))
    elif move == "rework":
        copies = [i for i, t in enumerate(b["techniques"]) if t["id"] in BUILDABLES
                  and not any(f["name"] in CHOICE_FEATURES for f in t.get("features") or [])]
        if not copies:
            return None
        i = rng.choice(copies)
        tid = b["techniques"][i]["id"]
        lv = _random_level(tid, rng) if rng.random() < 0.4 else party.tech_level(b["techniques"][i])
        b["techniques"][i] = _entry(tid, lv, random_features(tid, lv, rng))
    if not repair(b, level, rng, keep):
        return None
    return b


POOL = []


# ---- Scoring ----

def choices_for(row, build):
    have = {game_data.technique_name(t["id"]) for t in build["techniques"]}
    picks = party._choices(row.get("Choices"))
    kept = {k: v for k, v in picks.items() if k in have}
    if kept == picks:
        return None
    return {"Choices": "; ".join(f"{k}: {', '.join(v)}" for k, v in kept.items())}


def score(args):
    """Mean party Health left (losses 0) with `build` in `name`'s place;
    None if it doesn't load."""
    name, build, level, key, n, seed = args
    T.ENEMY_HEALTH_MULT = MULT
    rows = party._rows()
    names = PARTIES[level][key]
    row = choices_for(rows[name], build) if build else None
    edits = {"build": build} if build else None
    try:
        party.make_pc(name, rows=rows, edits=edits, row_changes=row)
    except (party.BuildError, KeyError, ValueError) as e:
        return None
    if SCORE == 'day':
        recs = day_sim.run(names, {name: (edits, row)} if build else {}, level, n, seed=seed)
        return st.mean(r["morning"] for r in recs)
    if SCORE == 'daywin':
        day_sim.set_mult(DAYWIN_X)
        recs = day_sim.run(names, {name: (edits, row)} if build else {}, level, n, seed=seed)
        return st.mean(0 if r["lost"] else 1 for r in recs)
    last = []

    def make(tier, good_luck=0):
        last[:] = [party.make_pc(m, i, good_luck, rows=rows, edits=edits if m == name else None,
                                 row_changes=row if m == name else None) for i, m in enumerate(names, 1)]
        return last
    cs.make_party = make
    out = []
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(n):
            r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                             seed=100_000 * mi + k + seed)
            out.append(sum(max(0, p["health"]) for p in last) if r["winner"] == "party" else 0)
    return st.mean(out)


def _key(build):
    return json.dumps([sorted(build["statPoints"].items()), sorted(build["skillPoints"].items()),
                       sorted(json.dumps(t, sort_keys=True) for t in build["techniques"])])


def search(arch, level, gens, n, kids, popsize, seed, pool_, ckpt=None):
    """`ckpt`: a file the search saves itself to after every generation
    and picks up from, so a restart costs one generation at most and the
    result is the same as an unbroken run."""
    rng = random.Random(seed)
    name = row_name(arch, level)
    key = PARTY_OF[arch]
    start = party.read_build(party._rows()[name]["Build"])
    start = {k: copy.deepcopy(v) for k, v in start.items()}
    if sum(party.xp_spent(start)) > BUDGET[level]:
        start = fit_budget(start, level, rng)
    base = pool_.apply(score, ((name, None, level, key, n, 0),))
    seen = {}
    pop = [(base, start)]
    seen[_key(start)] = base
    first = 0
    if ckpt and os.path.exists(ckpt):
        with open(ckpt, "rb") as f:
            st_ = pickle.load(f)
        first, pop, seen, base = st_["gen"], st_["pop"], st_["seen"], st_["base"]
        rng.setstate(st_["rng"])
        print(f"  picking up {arch} L{level} after generation {first}", flush=True)
    t0 = time.time()
    for g in range(first, gens):
        children = []
        for _ in range(kids * 3):
            if len(children) >= kids:
                break
            parent = max(rng.sample(pop, min(2, len(pop))), key=lambda p: p[0])[1]
            c = parent
            for _ in range(rng.choice((1, 1, 2, 3))):
                c2 = mutate(c, level, rng)
                if c2 is not None:
                    c = c2
            if c is parent or _key(c) in seen:
                continue
            seen[_key(c)] = None
            children.append(c)
        scores = pool_.map(score, [(name, c, level, key, n, 0) for c in children])
        for c, s in zip(children, scores):
            seen[_key(c)] = s
            if s is not None:
                pop.append((s, c))
        pop = sorted(pop, key=lambda p: -p[0])[:popsize]
        print(f"  {arch} L{level} gen {g + 1}/{gens}: best {pop[0][0]:.2f} (base {base:.2f}), "
              f"{len(seen)} tried, {time.time() - t0:.0f}s", flush=True)
        if ckpt:
            with open(ckpt + ".tmp", "wb") as f:
                pickle.dump(dict(gen=g + 1, pop=pop, seen=seen, base=base, rng=rng.getstate()), f)
            os.replace(ckpt + ".tmp", ckpt)
    # The finalists, scored again on fresh fights (with the sample itself).
    finals = pop[:max(popsize, 6)]
    val = pool_.map(score, [(name, b, level, key, 3 * n, VALIDATE_SEED) for _, b in finals]
                    + [(name, None, level, key, 3 * n, VALIDATE_SEED)])
    base_val = val[-1]
    out = [dict(arch=arch, level=level, name=name, search=s, validated=v, base_search=base, base_validated=base_val,
                build=b) for (s, b), v in zip(finals, val[:-1]) if v is not None]
    if SCORE == 'day':
        # Days in a row, on fresh days, for the finalists and the sample.
        builds = [r["build"] for r in out] + [None]
        days = pool_.map(score_days, [(name, b, level, key, 3 * n, VALIDATE_SEED) for b in builds])
        for r, d in zip(out, days):
            r.update(days=d, base_days=days[-1], score="day", mult=day_sim.MULT)
        return sorted(out, key=lambda r: -r["days"])
    if SCORE == 'daywin':
        for r in out:
            r.update(score="daywin", at_x=DAYWIN_X)
    return sorted(out, key=lambda r: -r["validated"])


def day_threshold(args):
    """The toughest day (enemy Health multiplier) the party wins half
    the time with `build` in `name`'s place (threshold.py): the ranking
    the designer picked, 2026-10-30, since it counts no resource."""
    name, build, level, key, n, seed = args
    rows = party._rows()
    row = choices_for(rows[name], build) if build else None
    swaps = {name: ({"build": build}, row)} if build else {}

    def rate(m):
        day_sim.set_mult(m)
        recs = day_sim.run(PARTIES[level][key], swaps, level, n, seed=seed)
        return sum(not r["lost"] for r in recs), len(recs)
    return threshold.find(rate, 0.5, 6.0)[0]


def rescore(runs_dir, n, pool_):
    """Adds the toughest day (`day_x`, the sample's `base_day_x`) to every
    entry in `runs_dir`'s results and ranks each file by it. A file
    already rescored is skipped, so a restart picks up where it stopped."""
    for path in sorted(os.listdir(runs_dir)):
        if not path.endswith(".json"):
            continue
        full = os.path.join(runs_dir, path)
        res = json.load(open(full))
        if not res or all("day_x" in r for r in res):
            continue
        r0 = res[0]
        key = PARTY_OF[r0["arch"]]
        jobs = [(r0["name"], r["build"], r0["level"], key, n, VALIDATE_SEED) for r in res]
        jobs.append((r0["name"], None, r0["level"], key, n, VALIDATE_SEED))
        xs = pool_.map(day_threshold, jobs)
        for r, x in zip(res, xs):
            r.update(day_x=x, base_day_x=xs[-1], day_x_n=n)
        res.sort(key=lambda r: -r["day_x"])
        with open(full + ".tmp", "w") as f:
            json.dump(res, f, indent=1)
        os.replace(full + ".tmp", full)
        print(f"{path}: toughest day x{res[0]['day_x']:.2f} vs the sample's x{xs[-1]:.2f}", flush=True)


def score_days(args):
    """Mean days won in a row (up to DAYS) with `build` in `name`'s place."""
    name, build, level, key, n, seed = args
    rows = party._rows()
    row = choices_for(rows[name], build) if build else None
    swaps = {name: ({"build": build}, row)} if build else {}
    recs = day_sim.run(PARTIES[level][key], swaps, level, n, days=DAYS, seed=seed)
    return st.mean(r["days"] for r in recs)


def current_version():
    for r in csv.DictReader(open(os.path.join(HERE, "..", "..", "scripts", "versions.csv"), encoding="utf-8-sig")):
        if r["Current"].strip().lower() == "yes":
            return r["Version"]
    return "unknown"


def _content(build):
    return json.dumps([sorted((k, int(v)) for k, v in build["statPoints"].items()),
                       sorted((k, int(v)) for k, v in build["skillPoints"].items() if int(v)),
                       sorted((t["id"], party.tech_level(t), json.dumps(sorted((f["name"], f["count"]) for f in t.get("features") or [])))
                              for t in build["techniques"])])


def _techs(build):
    """A build's Techniques, Levels and Features, without its ranks."""
    return json.dumps(sorted((t["id"], party.tech_level(t), json.dumps(sorted((f["name"], f["count"])
                                                                              for f in t.get("features") or [])))
                             for t in build["techniques"]))


def finalists(runs_dirs, keep=2):
    """The best `keep` builds per archetype and Level that beat their
    sample, from one or more runs' results (merged by file name). Once
    rescored, all are ranked by the toughest day (rescore()); each pick
    after the first must differ from the ones before it in its
    Techniques, not just a rank, so the Hall shows different builds."""
    if isinstance(runs_dirs, str):
        runs_dirs = [runs_dirs]
    merged = {}
    for d in runs_dirs:
        for path in sorted(os.listdir(d)):
            if path.endswith(".json"):
                for r in json.load(open(os.path.join(d, path))):
                    r.setdefault("score", "fight")
                    merged.setdefault(path[:-5], []).append(r)
    out = {}
    for key, res in sorted(merged.items()):
        if all("day_x" in r for r in res):
            res = sorted(res, key=lambda r: -r["day_x"])
        seen, picks = set(), []
        for r in res:
            if "day_x" in r:
                beats = r["day_x"] > r["base_day_x"]
            elif "days" in r:
                beats = r["days"] > r["base_days"]
            else:
                beats = r["validated"] > r["base_validated"]
            t = _techs(r["build"])
            if t in seen or not beats:
                continue
            seen.add(t)
            picks.append(r)
        if picks:
            out[key] = picks[:keep]
    return out


def write_hall(runs_dir, flavor, version, sub=""):
    """hall_of_fame/v<version>/: each finalist as a Builder export (the
    sample's export with the searched Stats, Skills and Techniques, and its
    flavor name and concept), named <archetype>_l<Level>_<rank>.json."""
    folder = os.path.join(HERE, "hall_of_fame", f"v{version}", sub)
    os.makedirs(folder, exist_ok=True)
    written = []
    for key, picks in finalists(runs_dir).items():
        for i, r in enumerate(picks, 1):
            name = r["name"]
            sample = party.read_build(party._rows()[name]["Build"])
            b = copy.deepcopy(sample)
            for k in ("statPoints", "skillPoints", "techniques"):
                b[k] = r["build"][k]
            fl = flavor.get(f"{key}_{i}", {})
            b["charName"] = fl.get("name", f"{r['arch']} (Level {r['level']}, optimized #{i})")
            b["charConcept"] = fl.get("concept", "")
            b["xpBudget"] = FULL_BUDGET[r["level"]]
            b["exportedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            if "days" in r:
                how = (f"Days won in a row (up to {DAYS}) {r['days']:.2f} against the sample's {r['base_days']:.2f}; "
                       f"morning Health {r['validated']:.2f} against {r['base_validated']:.2f}, on fresh days "
                       f"(day_sim.py, enemy Health x{r['mult']})")
            else:
                how = (f"Party Health left {r['validated']:.2f} against the sample's {r['base_validated']:.2f} on "
                       f"fresh fights (enemy Health x{MULT})")
            if "day_x" in r:
                how = (f"Toughest day it wins half the time: enemy Health x{r['day_x']:.2f}, against the sample's "
                       f"x{r['base_day_x']:.2f} ({100 * (r['day_x'] / r['base_day_x'] - 1):+.0f}%). " + how)
            found = {"day": "Health in the morning (day_sim.py)",
                     "daywin": f"days won at enemy Health x{r.get('at_x')}"}.get(r.get("score"),
                                                                                "Health left after one fight")
            how += f". Found by the search on {found}"
            b["simNotes"] = [f"Hall of Fame v{version}: build_optimizer.py's #{i} for {r['arch']} ({ARCHES[r['arch']]}), "
                             f"Level {r['level']}, in {name}'s place in party {PARTY_OF[r['arch']]}. {how}. "
                             "Items, background and row are the sample's."]
            out = os.path.join(folder, f"{key}_{i}.json")
            with open(out, "w") as f:
                json.dump(b, f, indent=1, ensure_ascii=False)
                f.write("\n")
            written.append(out)
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch", action="append", help="archetype(s) (a sample character's first name)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("-L", type=int, action="append", help="Level(s): 2, 3")
    ap.add_argument("-g", type=int, default=40, help="generations")
    ap.add_argument("-n", type=int, default=100, help="fights per mix for each score")
    ap.add_argument("-k", type=int, default=24, help="children a generation")
    ap.add_argument("-p", type=int, default=6, help="population")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", default=os.path.join(HERE, "hall_of_fame", "runs"))
    ap.add_argument("--hall", action="store_true", help="write hall_of_fame/v<version>/ from the runs in -o")
    ap.add_argument("--score", choices=("fight", "day", "daywin"), default="fight",
                    help="Health left after one fight, day_sim.py's morning Health (then days in a row), "
                         "or the share of days won at --at-x")
    ap.add_argument("--at-x", type=float, help="--score daywin: the enemy Health multiplier to play the days at")
    ap.add_argument("--rescore", action="store_true",
                    help="add the toughest day (threshold.py) to every result in -o and rank by it; -n is days a mix")
    ap.add_argument("--combat-budget", action="store_true",
                    help="search within combat_xp.COMBAT_BUDGET (95 / 130 XP), the rest assumed spent outside fights")
    ap.add_argument("--hall-sub", default="", help="a subfolder of hall_of_fame/v<version>/ for --hall")
    ap.add_argument("--redo", action="store_true", help="search again even if -o already has a result")
    ap.add_argument("--flavor", help="a JSON of names and concepts, keyed <archetype>_l<Level>_<rank>")
    a = ap.parse_args()
    if a.rescore:
        with mp.Pool(a.j) as pool_:
            rescore(a.o, a.n, pool_)
        return
    if a.hall:
        flavor = json.load(open(a.flavor)) if a.flavor else {}
        for p in write_hall(a.o.split(","), flavor, current_version(), a.hall_sub):
            print(p)
        return
    global SCORE, DAYWIN_X
    if a.combat_budget:
        import combat_xp
        BUDGET.update(combat_xp.COMBAT_BUDGET)
    SCORE = a.score
    DAYWIN_X = a.at_x
    if SCORE == "daywin" and not DAYWIN_X:
        ap.error("--score daywin needs --at-x")
    POOL[:] = pool()
    archs = list(ARCHES) if a.all else a.arch
    levels = a.L or [3, 2]
    os.makedirs(a.o, exist_ok=True)
    with mp.Pool(a.j) as pool_:
        for level in levels:
            for arch in archs:
                path = os.path.join(a.o, f"{arch.lower()}_l{level}.json")
                # A long run that gets cut off picks up where it stopped.
                if os.path.exists(path) and not a.redo:
                    print(f"{arch}, Level {level}: already in {a.o}", flush=True)
                    continue
                print(f"{arch} ({ARCHES[arch]}), Level {level}", flush=True)
                ckpt = path[:-5] + ".ckpt"
                res = search(arch, level, a.g, a.n, a.k, a.p, a.seed, pool_, ckpt=ckpt)
                with open(path, "w") as f:
                    json.dump(res, f, indent=1)
                if os.path.exists(ckpt):
                    os.remove(ckpt)
                if res:
                    print(f"  best validated {res[0]['validated']:.2f} vs the sample {res[0]['base_validated']:.2f}"
                          + (f"; days in a row {res[0]['days']:.2f} vs {res[0]['base_days']:.2f}" if "days" in res[0]
                             else ""), flush=True)


if __name__ == "__main__":
    main()
