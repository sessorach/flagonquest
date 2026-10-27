"""Which Techniques the sim plays (2026-10-27).

Every techniques.csv ID lands in exactly one of techniques.py's lists:
REGISTRY (modeled), OUT_OF_COMBAT (nothing to do in a fight) or DEFERRED
(not modeled yet, with what it would need). This prints the counts, the
deferred ones with their reasons, and anything missing or listed twice,
and exits 1 if there's any of the last two, so a new Technique in the
CSV shows up here before a build trips on it.

    python3 coverage.py          # counts, deferred, problems
    python3 coverage.py --all    # every ID and where it is
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim  # noqa: E402,F401  (sets techniques.cs)
import game_data  # noqa: E402
import techniques as tq  # noqa: E402

LISTS = (("modeled", tq.REGISTRY), ("out of combat", tq.OUT_OF_COMBAT), ("deferred", tq.DEFERRED))


def where(tid):
    return [name for name, d in LISTS if tid in d]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    rows = game_data.techniques()
    counts = {name: 0 for name, _ in LISTS}
    problems = []
    for tid, row in rows.items():
        w = where(tid)
        if len(w) == 1:
            counts[w[0]] += 1
        else:
            problems.append(f"{tid} {row['Name']}: " + (" and ".join(w) if w else "in no list"))
        if a.all:
            print(f"{tid} {row['Name']}: {', '.join(w) or '-'}")
    stray = sorted(set().union(*(d for _, d in LISTS)) - set(rows))
    problems += [f"{tid}: listed, but not in techniques.csv" for tid in stray]
    print(f"{len(rows)} Techniques: " + ", ".join(f"{n} {k}" for k, n in counts.items()))
    print("\nDeferred:")
    for tid, why in sorted(tq.DEFERRED.items()):
        print(f"- {tid} {game_data.technique_name(tid)}: {why}")
    if problems:
        print("\nProblems:")
        print("\n".join("- " + p for p in problems))
        sys.exit(1)
