# Enemy/combat simulator

A Monte Carlo simulator for FlagonQuest's combat: the sample characters
(built from real Builder exports) against enemies built the way the
design says to, on a small 2D arena with real cards. It checks the enemy
design in `design/ENEMY_ENCOUNTER_DESIGN.md` and prices character
options; the decisions it fed are in `design/DESIGNER_NOTES.md`. This
README is a map and a how-to; each file's docstring says what it does
and why.

Tidied 2026-11-11: finished studies went to
`archive/enemy_sim_experiments/` (they name the settings they ran on, and
won't run as they are); the old enemy builders (v1, v2, the earlier v3s)
are gone, so every enemy builds through `enemy_builder.py`.

## Start here

- **`replays/latest/`**: one or two typical fights from the latest round
  of work as HTML pages, and a `notes.md` on what changed.
  `tools/make_replays.py "what changed"` writes them (the previous round
  moves to `replays/archive/`).
- **`TABLE_PLAY_NOTES.md`**: how real tables play (who dives in, how
  cards get spent) and the targets the sim is checked against.
- **`MONSTER_MANUAL.md`**: every monster as a stat block (generated from
  `monster_manual.csv` by `tools/monster_manual.py`; edit the CSV).
- **`SHEETS.md`**: every sample character resolved (generated from
  `builds/`; edit the builds).

## Layout

- **This folder**: the simulator itself and its data.
- **`tools/`**: the runners used again and again (below).
- **`experiments/<topic>/`**: one-off studies while they're live; when a
  study is done, fold it into a tool or archive it.
- **`results/`**: result tables; **`hall_of_fame/`**: optimizer runs;
  **`builds/`**: the Builder exports and their variants.

Run scripts from this folder by path (`python3 tools/calibrate.py`). A
script in a subfolder starts with `import _paths` (it puts the core,
`tools/` and the experiments folders on the path) and reads data through
`_paths.ROOT`. `SIM_SET="NAME=value,..."` sets any tunable for one run,
workers included (it splits on commas, so a dict goes in a string form
where the tunable allows it).

## The core

| File | What it is |
|---|---|
| `combat_sim.py` | The fight: turn order, AP, movement, attacks, cards, effects. `run_fight(tier, level, enemies=..., movement=True, trace=[])`. |
| `tactics.py` | What a unit does on its turn: targets, movement, how many attacks. |
| `play_styles.py` | How cautiously each PC plays (Diver, Skirmisher, Back-liner...). |
| `party_tactics.py` | Whole-party presets (`-t cautious` on the tools). |
| `cards.py` | Decks, hands and the day's card budget. |
| `day_sim.py` | A whole day: two fights, care between them, a night's rest. |
| `party.py` | Builds the sample characters from `sample_pcs.csv` and `builds/`. |
| `techniques.py`, `techniques_more_a.py`, `techniques_more_b.py`, `tech_common.py` | Every Technique by its techniques.csv ID. |
| `encounter.py` | Encounter-use tracking. |
| `hooks.py` | Where a Technique or enemy Ability plugs into a fight. |
| `enemy_builder.py` | Turns a monster's picks into a stat block: the Level table, archetypes, prices. |
| `sample_enemies.py` | Enemies by name (`"Gravel Ogre@3"`, or a `sample_enemies.csv` row), what each buys, and the encounters the tools play. |
| `enemy_abilities.py` | The enemy Abilities in a fight. |
| `game_data.py` | Reads the game's live CSVs (`scripts/*.csv`): the sim never copies a game fact. |
| `tunables.py` | Every number still subject to revision, and the switches. |
| `combat_xp.py` | How much of a build's XP goes to fights. |
| `threshold.py`, `movement.py`, `resume.py`, `sheets.py`, `narrate_fight.py`, `replay_html.py` | The toughest beatable fight; arena geometry; restart-safe runs; `SHEETS.md`; one narrated fight; its HTML page. |

## The tools

| Tool | What it answers |
|---|---|
| `calibrate.py` | The sample parties against the table's targets (fight length, Down, Wounded). |
| `table_check.py` | The band check: days won at the bottom, middle and top of each Level's XP band. |
| `bands.py` | The band parties and their builds (`--check` that the stored builds still match). |
| `combat_stats.py` | Hit chances, hit sizes, rounds and lethality on the manual, per Level. |
| `manual_check.py` | Every manual monster in fights; each one's share of the difficulty. |
| `size_check.py` | Every enemy size (minions to the solo boss) on the defaults. |
| `reprice.py` | What each enemy Ability is worth, against its price. |
| `monster_manual.py` | Writes `MONSTER_MANUAL.md`. |
| `effect_check.py` | Every buff and debuff, priced; `--day --extra N` over whole days with extra Slots. |
| `xp_investments.py` | What a few more XP buy at high stakes (ranks, Stats, Battle Maneuvers); `--trace` follows a Maneuver's stacks. |
| `compare_builds.py` | One character swapped for a variant, paired. |
| `tactics_compare.py` | One party under each party tactic. |
| `technique_pass.py`, `synergy_scan.py` | Every Technique and Feature, alone and in pairs. |
| `build_optimizer.py`, `scorecard.py`, `party_mixes.py`, `party_power.py` | What a min-maxer builds; how strong builds and parties are. |
| `heal_swap.py`, `durability_swap.py` | Healing Magic and durability against their alternatives. |
| `coverage.py` | That every Technique is modeled, out of combat, or deferred. |
| `make_replays.py` | The latest replays. |

## The standard fights

- **Enemies**: the monster manual's encounters, eight drawn per Level by
  the variety rules (`sample_enemies.CURRENT_MIXES`, "Manual 1".. "Manual
  8"). `SIM_SET="ENCOUNTER_SOURCE='roster'"` plays the old roster's four
  mixes instead.
- **Parties**: the band parties (`bands.groups`), usually the middle of
  the band (`bands.MID`); Level 1 plays the six sample parties.
- **A day, not a fight**: `day_sim` plays two fights with the day's card
  budget. A fight run on its own gets fewer cards than a day's first
  fight, so check which a number came from before comparing.
- **Higher stakes**: an extra standard attacker or two per encounter
  (`effect_check --extra`, `xp_investments --extra`) makes days
  threatening without changing the enemies.

## Common commands

```
python3 tools/calibrate.py -L 2                    # the sample parties against the table's targets
python3 tools/table_check.py -n 100                # the band check, every Level
python3 tools/combat_stats.py                      # hit chances and lethality on the manual
python3 tools/effect_check.py --day --extra 1      # every effect over whole, threatening days
python3 tools/xp_investments.py -L 2 --extra 1     # what extra XP buys
python3 tools/compare_builds.py -L 2 -p B --swap "Beornhard (L2)=Beornhard (L2, Frost)"
python3 narrate_fight.py 1 1 3 --party Hilde,Browndog,Sable,Beornhard --html out.html
SIM_SET="DEBUFF_ABUSE=True" python3 tools/xp_investments.py ...   # any tool, a tunable changed
```

A one-off build edit: `compare_builds.py --edit 'Name={"replace": [...]}'`
(`party.apply_edits`' format). One worth keeping: a variant file in
`builds/` (`"base"` plus the edits and a `simNotes` line) and a
`sample_pcs.csv` row copying the base row's Weapon, Play Style and
Choices.

## Changing the simulator

- New behavior goes behind a `tunables.py` switch, and the old path is
  proved unchanged: run the tools on fixed seeds before and after with
  the switch off and compare the outputs exactly (parallel tools write
  lines in any order, so sort them first).
- A Technique or enemy Ability goes in `techniques*.py` /
  `enemy_abilities.py` at a `hooks.py` point; an export naming something
  the sim doesn't know stops the load on purpose.
- A rules fact is read through `game_data.py`, never copied.
- Keep it short: the simplest code that does the job, and fold or archive
  a finished study rather than keeping a near-copy.
