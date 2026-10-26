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

# (file stem, party names, encounter Level, sample_enemies.ENCOUNTERS key),
# plus optionally a run_fight result key that must be above 0 in the
# picked fight, to show something that doesn't happen every fight.
MATCHUPS = [
    ("partyS_L1_vs_L1_frontline", ["Enith", "Felix", "Jackal", "Hanforth"], 1, "Frontline"),
    ("partyU_L1_vs_L1_shield_wall", ["Browndog", "Ashleigh", "Sable", "Beornhard"], 1, "Shield Wall"),
    ("partyT_L1_vs_L1_warband", ["Browndog", "Hanforth", "Sable", "Beornhard"], 1, "Warband"),
    # The Bleeding builds together (sample_pcs.csv's "(Bleed)" rows).
    ("bleed_party_L1_vs_L1_frontline", ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"], 1,
     "Frontline"),
    # Bleeding appliers with the two cash-outs (2026-10-16): Felix's Open
    # the Wound and Beornhard's Reign of Blood.
    ("cash_party_L1_vs_L1_frontline", ["Hilde (Bleed)", "Felix (Cash)", "Jackal (Bleed)", "Beornhard (Cash)"], 1,
     "Frontline", "cashed"),
    # Both sides bleeding (2026-10-19): the Bleeding builds against
    # Warband's Skulking Footpads, who Poison for 2 Bleeding a hit.
    ("bleed_party_L1_vs_L1_warband", ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"], 1,
     "Warband", "pc_bleed_taken"),
    # A dangerous fight (2026-10-21): Frontline at 1.5 times the slots,
    # led by a 2-slot Brute Chief, the kind of fight control is for.
    ("partyA_L1_vs_chief_frontline", ["Hilde", "Browndog", "Carrick", "Sable"], 1, "Chief's Frontline"),
    # The designer's 175 XP builds (2026-10-24), all four: Strength from
    # the Slain, Hilde's Level 3 Battle Maneuver, Exert Pressure, Jackal's
    # Wind Slash Maneuvers, Beornhard's Destructive War Magic.
    ("partyB_L3_vs_L3_frontline", ["Hilde (L3)", "Browndog (L3)", "Jackal (L3)", "Beornhard (L3)"], 3, "Frontline"),
    # Every Technique on the sheets (2026-10-25): Hanforth's Lifeline,
    # Spirit Blessing, Gust of Wind and ranged Reckoning, with Rook's and
    # Sable's Blinkstep and Parting Shot, against the Level 2 Solo Boss.
    # The designer's own Hanforth (L2) doesn't take Lifeline (10-26); this
    # shows the variant that does.
    ("partyD2_L2_vs_solo_boss", ["Browndog (L2)", "Rook (L2)", "Sable (L2)", "Hanforth (L2, Lifeline)"], 2,
     "Solo Boss", "lifeline_taken"),
    # Variant builds (2026-10-25, sample_characters.md "Variants"): the
    # Frost Beornhard Slowing what he hits, and the two Level 3 swaps that
    # helped, Hilde's Flurry and Beornhard's Piercing Elements.
    ("partyB_L2_frost_vs_L2_warband", ["Hilde (L2)", "Browndog (L2)", "Jackal (L2)", "Beornhard (L2, Frost)"], 2,
     "Warband"),
    ("partyB_L3_flurry_piercing_vs_L3_frontline",
     ["Hilde (L3, Flurry)", "Browndog (L3)", "Jackal (L3)", "Beornhard (L3, Piercing)"], 3, "Frontline"),
    # Hanforth's own 175 XP build (2026-10-26).
    ("partyD_L3_vs_L3_frontline", ["Browndog (L3)", "Hanforth (L3)", "Hilde (L3)", "Beornhard (L3)"], 3,
     "Frontline"),
]


def _use_party(names):
    cs.make_party = lambda tier, good_luck=0: party.make_party_from(names, good_luck)


def _pick_seed(level, encounter, avg_rounds, win_pct, tries=300, need=None):
    want = "party" if win_pct >= 50 else "enemies"
    best = None
    for seed in range(1, tries + 1):
        r = cs.run_fight(1, level, seed=seed, movement=True, enemies=se.build_encounter(encounter))
        if r["winner"] != want or (need and not r.get(need, 0) > 0):
            continue
        gap = abs(r["rounds"] - avg_rounds)
        if best is None or gap < best[0]:
            best = (gap, seed)
    return best[1] if best else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summary", help="one line on what changed this round")
    ap.add_argument("--trials", type=int, default=1000)
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE, for this round's replays")
    args = ap.parse_args()
    for kv in args.s:
        k, v = kv.split("=", 1)
        try:
            v = __import__("ast").literal_eval(v)
        except (ValueError, SyntaxError):
            pass
        setattr(T, k, v)

    if os.path.isdir(LATEST) and os.listdir(LATEST):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        os.makedirs(ARCHIVE, exist_ok=True)
        shutil.move(LATEST, os.path.join(ARCHIVE, stamp))
    os.makedirs(LATEST, exist_ok=True)

    notes = [f"# Latest replays ({datetime.date.today()})", "", args.summary, ""]
    if args.s:
        notes += ["Settings: " + ", ".join(args.s), ""]
    for stem, names, level, enc_key, *need in MATCHUPS:
        need = need[0] if need else None
        _use_party(names)
        encounter = se.ENCOUNTERS[level][enc_key]
        win_pct, avg_rounds, avg_hp, _, _ = cs.simulate(1, level, trials=args.trials, movement=True,
                                                        enemies=se.build_encounter(encounter))
        seed = _pick_seed(level, encounter, avg_rounds, win_pct, need=need)
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
                  f"{avg_hp:.0f}% HP left on a win"]
        if need:
            notes += [f"- Picked from fights with {need} above 0"]
        notes += [""]
    with open(os.path.join(LATEST, "notes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(notes))
    print("\n".join(notes))


if __name__ == "__main__":
    main()
