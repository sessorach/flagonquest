"""Healing Magic against the other ways to heal, on the optimized builds (2026-10-31).

The designer's question: Healing Magic shows up on most optimized builds
as a Level 1 splash (3 XP). How does it stand up to Second Wind and the
other healing, and would a build without it want some other healing?

For each optimized build in a scorecard.py result: the build as it is;
with every healing Technique below taken off (no healing); and with its
healing swapped for each option in turn (or the option added, if it has
none), at the same total XP (party.fit: prereq ranks bought, the rest
paid from or put back into the combat Skills in DONORS). Each plays with
three stand-ins one enemy Level up, as the scorecard does, same seeds for
every variant. Results in points against the build as it is, and on the
odds (log-odds), which still reads near 100%.

    python3 heal_swap.py -L 3 -n 500 --scorecard hall_of_fame/runs_levelup/scorecard_l3_run1.json -o out.json
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import party  # noqa: E402
import game_data  # noqa: E402
import build_optimizer as bo  # noqa: E402
import resume  # noqa: E402
import scorecard as sc  # noqa: E402

# The healing options, as Builder entries (the fixed-Level ones take their
# own Level). Healing Magic as the searches take it: Level 1, one Feature.
OPTIONS = {
    "Healing Magic (Guardian Angel)": {"id": "T105", "level": 1, "features": {"Guardian Angel": 1}},
    "Healing Magic (Reach)": {"id": "T105", "level": 1, "features": {"Reach": 1}},
    "Second Wind": {"id": "T012"},
    "Bolstering Refrain": {"id": "T066"},
    "Lay On Hands": {"id": "T020"},
    "Sap Seals the Wound": {"id": "T093"},
    "Thief Empties the Vessel": {"id": "T159"},
}
HEALING = {"T105", "T012", "T066", "T020", "T093", "T159", "T055"}
# Where the XP comes from (the highest rank first) or goes back to: every
# combat Skill and Stat but the build's attack Skill and its Stat. Skills
# pay first (pay()): taking a 5 Stat down to pay 3 XP costs the build far
# more than the option it's paying for (the first try did, 2026-10-31, and
# made every option look worse than no healing at all).
DONORS = ("Resilience", "Composure", "Insight", "Might", "Acrobatics", "Melee", "Brawl", "Archery", "Sorcery",
          "Theurgy", "Meditation", "Agility", "Body", "Mind", "Cunning", "Essence")
CAP = {2: 4, 3: 5}


def variants(build, level, row):
    """{label: build or the reason it can't be built}."""
    have = [t for t in build["techniques"] if t["id"] in HEALING]
    # apply_edits counts copies per ID.
    seen, rm = {}, []
    for t in build["techniques"]:
        if t["id"] in HEALING:
            seen[t["id"]] = seen.get(t["id"], 0) + 1
            rm.append({"id": t["id"], "copy": seen[t["id"]]})
    out = {"as is": build}
    import tunables as T
    sk = party.make_pc(row, 1, edits={"build": build}, row_changes=bo.choices_for(party._rows()[row], build))["attack_skill"]
    donors = tuple(d for d in DONORS if d not in (sk, T.PC_SKILL_STAT.get(sk)))
    skills = tuple(d for d in donors if d not in build["statPoints"])

    def pay(**kw):
        try:
            return party.fit(build, donors=skills, cap=CAP[level], **kw)[0]
        except party.BuildError:
            return party.fit(build, donors=donors, cap=CAP[level], **kw)[0]
    names = ", ".join(sorted({game_data.technique_name(t["id"]) for t in have})) or "none"
    try:
        out["no healing"] = pay(remove=rm) if rm else None
    except party.BuildError as e:
        out["no healing"] = str(e)
    for label, entry in OPTIONS.items():
        try:
            out[label] = pay(add=[entry], remove=rm)
        except party.BuildError as e:
            out[label] = str(e)
    # One that doesn't load (a Feature budget, say) is reported, not played.
    rows = party._rows()
    for label, b in out.items():
        if isinstance(b, dict):
            try:
                party.make_pc(row, 1, rows=rows, edits={"build": b}, row_changes=bo.choices_for(rows[row], b))
            except (party.BuildError, KeyError, ValueError) as e:
                out[label] = str(e)
    return out, names


def _logit(p, days):
    p = min(max(p, 0.5 / days), 1 - 0.5 / days)
    return math.log(p / (1 - p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-n", type=int, default=500)
    ap.add_argument("--scorecard", required=True)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    ap.add_argument("-o", required=True)
    a = ap.parse_args()
    bo.START = "best"
    card = json.load(open(a.scorecard))
    L, n = a.L, a.n
    stand = [(None, None)] * 3
    jobs, table = {}, {}
    for arch, B in sorted(card["builds"].items()):
        vs, names = variants(B["optimized"], L, B["row"])
        table[arch] = dict(healing=names, variants={})
        for label, b in vs.items():
            if isinstance(b, dict):
                jobs[(arch, label)] = ([(B["row"], b)] + stand, L, 1, n, 0)
            else:
                table[arch]["variants"][label] = dict(error=b or "nothing to take off")
    part = resume.Partial(a.o + ".partial")
    todo = [k for k in jobs if list(k) not in part]
    with mp.Pool(a.j) as pool:
        for k, v in zip(todo, pool.imap(sc.play, [jobs[k] for k in todo])):
            part.add(list(k), v)
    R = {tuple(json.loads(k)): v for k, v in part.got.items()}
    for arch in table:
        base = R[(arch, "as is")]
        b_rate = base["won"] / base["days"]
        for label in [k[1] for k in jobs if k[0] == arch]:
            r = R[(arch, label)]
            rate = r["won"] / r["days"]
            table[arch]["variants"][label] = dict(
                up=rate, points=100 * (rate - b_rate),
                odds=_logit(rate, r["days"]) - _logit(b_rate, base["days"]),
                downs_per_10=10 * r["seats"][0]["downed"] / r["days"],
                heal_share=r["seats"][0]["heal_out"] / max(1, sum(s["heal_out"] for s in r["seats"])))
    with open(a.o, "w") as f:
        json.dump(dict(level=L, days=R[next(iter(jobs))]["days"], builds=table), f, indent=1)
    part.finish()
    for arch, t in table.items():
        print(f"{arch} (has: {t['healing']}): as is {100 * t['variants']['as is']['up']:.0f}%")
        for label, v in t["variants"].items():
            if label == "as is":
                continue
            if "error" in v:
                print(f"    {label:32s} can't: {v['error']}")
            else:
                print(f"    {label:32s} {100 * v['up']:3.0f}%  {v['points']:+4.0f} points  {v['odds']:+.2f} log-odds")


if __name__ == "__main__":
    main()
