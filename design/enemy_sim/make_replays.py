"""
Writes the "latest" replays for a round of design work: 1-2 seeded
fights as self-contained HTML pages in `replays/latest/`, plus a
`notes.md` saying what changed and how each shown fight compares to
the matchup's average. Per the designer: every round of sim/design work
should leave a replay or two there to look over, so this is the one
command to run at the end of each round.

Picks a "typical" fight for each matchup rather than a random one: a
party win whose length is closest to the matchup's own average (a loss
if the matchup is mostly losses), so the replay shows what the numbers
describe.

Usage:
    python3 make_replays.py "what changed this round" [--trials N]
Edit MATCHUPS below to change which fights get shown. The previous
round's `latest/` is moved to `replays/archive/<date-time>/` first.
"""
import argparse
import datetime
import os
import shutil

import combat_sim as cs
import tunables as T
import party
import sample_enemies as se
from replay_html import render_html

HERE = os.path.dirname(os.path.abspath(__file__))
LATEST = os.path.join(HERE, "replays", "latest")
ARCHIVE = os.path.join(HERE, "replays", "archive")

# (file stem, party names, encounter Level, sample_enemies.ENCOUNTERS key)
MATCHUPS = [
    ("partyS_L1_vs_L1_frontline", ["Enith", "Felix", "Jackal", "Hanforth"], 1, "Frontline"),
    ("partyU_L1_vs_L1_shield_wall", ["Browndog", "Ashleigh", "Sable", "Beornhard"], 1, "Shield Wall"),
    ("partyT_L1_vs_L1_warband", ["Browndog", "Hanforth", "Sable", "Beornhard"], 1, "Warband"),
]


def _use_party(names):
    cs.make_party = lambda tier, good_luck=0: party.make_party_from(names, good_luck)


def _pick_seed(level, encounter, avg_rounds, win_pct, tries=300):
    want = "party" if win_pct >= 50 else "enemies"
    best = None
    for seed in range(1, tries + 1):
        r = cs.run_fight(1, level, seed=seed, movement=True, enemies=se.build_encounter(encounter))
        if r["winner"] != want:
            continue
        gap = abs(r["rounds"] - avg_rounds)
        if best is None or gap < best[0]:
            best = (gap, seed)
    return best[1] if best else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summary", help="one line on what changed this round")
    ap.add_argument("--trials", type=int, default=1000)
    args = ap.parse_args()

    if os.path.isdir(LATEST) and os.listdir(LATEST):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        os.makedirs(ARCHIVE, exist_ok=True)
        shutil.move(LATEST, os.path.join(ARCHIVE, stamp))
    os.makedirs(LATEST, exist_ok=True)

    notes = [f"# Latest replays ({datetime.date.today()})", "", args.summary, ""]
    for stem, names, level, enc_key in MATCHUPS:
        _use_party(names)
        encounter = se.ENCOUNTERS[level][enc_key]
        win_pct, avg_rounds, avg_hp, _, _ = cs.simulate(1, level, trials=args.trials, movement=True,
                                                        enemies=se.build_encounter(encounter))
        seed = _pick_seed(level, encounter, avg_rounds, win_pct)
        trace = []
        result = cs.run_fight(1, level, seed=seed, movement=True, trace=trace, enemies=se.build_encounter(encounter))
        result["vs_average"] = {"trials": args.trials, "win_pct": win_pct, "avg_rounds": avg_rounds,
                                "avg_hp_on_win": avg_hp}
        with open(os.path.join(LATEST, stem + ".html"), "w", encoding="utf-8") as f:
            f.write(render_html(trace, result, T.ARENA_SIZE))
        this_hp = f", {result['party_hp_pct'] * 100:.0f}% party HP left" if result["winner"] == "party" else ""
        notes += [f"## {stem}.html",
                  f"- Party: {', '.join(names)}",
                  f"- Enemies: Level {level} {enc_key} ({', '.join(encounter)})",
                  f"- This fight (seed {seed}): {result['winner']} won in {result['rounds']} rounds{this_hp}",
                  f"- Matchup average over {args.trials} fights: {win_pct:.1f}% wins, {avg_rounds:.1f} rounds, "
                  f"{avg_hp:.0f}% HP left on a win", ""]
    with open(os.path.join(LATEST, "notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(notes))
    print("\n".join(notes))


if __name__ == "__main__":
    main()
