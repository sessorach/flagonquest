# Enemy/combat simulator

Small Python tool for testing whether the enemy-encounter model in
`design/ENEMY_ENCOUNTER_DESIGN.md` actually produces the intended feel
(on-level, then stronger-than, then stretched-thin per Level) — built
to check the design against real Monte Carlo simulation rather than
algebra alone. Full write-up, findings, and the validation grid this
produced are in that document's "Analysis" section; this README is just
usage.

## Files

- **`tunables.py`** — every number that's still subject to revision:
  the enemy Level curve, Role/Armor/Action modifiers, and the PC
  power-per-Tier curve. **Edit this file when the PC/enemy models
  change** — the other files implement the *shape* of the formulas and
  shouldn't need touching for a pure numbers retune.
- **`enemy_builder.py`** — turns a Level/Slots/Role/Defense-tier/Action/
  Armor pick into a full enemy stat block, matching
  `archive/flagonquest_encounter_builder.xlsx`'s own formulas exactly
  (`python3 enemy_builder.py` re-runs the cross-check against the
  spreadsheet's own live worked example).
- **`party.py`** — a crude "representative PC" per power Tier (one
  Skill Total/Defense/Damage/Resist/Health, shared by all 4 party
  members — no distinct roles, no Techniques/items). `make_party(tier,
  good_luck=N)` can give every PC N stacks of Good Luck on their own
  attack roll, for testing a mechanic's value empirically (see
  `combat_sim.py`'s note below).
- **`sample_enemies.csv`** — every enemy stat block that's been built
  for a reason, one row per build (Level/Slots/Role/Defense-tier/
  Action/Armor/Battle Tactic/Fighting Style/Abilities). Two kinds share
  the file, told apart by the `Roster` column: the five `TRUE` rows are
  the validated one-per-Level on-level roster (tuned to land close to a
  genuine ~50% win rate at their own Tier); everything else is a `FALSE`
  reference build made for a specific question (a generic Level 2
  fighter for an item-balancing check, say) and isn't tied to a
  particular Level. Add a row here instead of writing a one-off script
  whenever a stat block gets built for a reason worth keeping around.
- **`sample_enemies.py`** — loads the CSV above via `enemy_builder.py`.
  `make_enemy(level)` pulls the Roster row for that Level (what
  `combat_sim.py` uses for the grid); `get_enemy(name)` pulls any row by
  name; `all_enemies()` returns every row built. Simulator fixtures for
  now, not a finished in-game roster — expect an "Example Enemies" doc
  to supersede the Roster rows once the tunables below are locked down
  further.
- **`combat_sim.py`** — the Monte Carlo fight loop (`run_fight`) and
  driver (`simulate`). Models Gambling (PCs punching through high
  Resist), Good Luck (`good_luck=N` on `simulate`/`run_fight`, applied
  to every PC — see the module's own note on why "every PC, every
  attack, all fight" reads very differently from the per-flip Value the
  balance model prices, and how to isolate just one PC instead), and a
  subset of the Ability catalog (Enhanced Health, Powerful Weapon/
  Spell, Strike (Crippling)/(Vulnerable), Poison (Bleeding), Durable —
  see `tunables.ABILITY_COST`'s own comment for which abilities are
  wired in and why the rest aren't yet). See its module docstring for
  what's still simplified/not modeled (Extra Successes from suit-pool
  matching, Techniques, items, positioning, real initiative).
- **`run_grid.py`** — runs every Party Tier × Enemy Level combination
  and prints win rate / average rounds / party HP% remaining.

## Usage

```
cd design/enemy_sim
python3 run_grid.py           # full 5x5 grid, 3000 trials/cell
python3 run_grid.py 10000     # more trials, slower but less noisy
python3 enemy_builder.py      # cross-check against the live spreadsheet example
python3 sample_enemies.py     # print every stat block in sample_enemies.csv
```

After editing `tunables.py` (a pure numbers retune) or `sample_enemies.
csv` (a Roster row's build), just re-run `run_grid.py` — no other file
needs to change.
