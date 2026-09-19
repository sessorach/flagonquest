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
  members — no distinct roles, no Techniques/items).
- **`sample_enemies.py`** — five concrete, one-per-Level enemies,
  already tuned to land close to a genuine on-level fight at their own
  Tier. Simulator fixtures for now, not a finished roster — expect a
  real "Example Enemies" doc to supersede this once the tunables below
  are locked down further.
- **`combat_sim.py`** — the Monte Carlo fight loop (`run_fight`) and
  driver (`simulate`). Models Gambling (PCs punching through high
  Resist) and a subset of the Ability catalog (Enhanced Health,
  Powerful Weapon/Spell, Strike (Crippling)/(Vulnerable), Poison
  (Bleeding), Durable — see `tunables.ABILITY_COST`'s own comment for
  which abilities are wired in and why the rest aren't yet). See its
  module docstring for what's still simplified/not modeled (no real
  Extra Successes from suit-pool matching, Techniques, items,
  positioning, or real initiative).
- **`run_grid.py`** — runs every Party Tier × Enemy Level combination
  and prints win rate / average rounds / party HP% remaining.

## Usage

```
cd design/enemy_sim
python3 run_grid.py           # full 5x5 grid, 3000 trials/cell
python3 run_grid.py 10000     # more trials, slower but less noisy
python3 enemy_builder.py      # cross-check against the live spreadsheet example
python3 sample_enemies.py     # print the 5 sample enemies' stat blocks
```

After editing `tunables.py` (or retuning a build in `sample_enemies.
py`), just re-run `run_grid.py` — no other file needs to change.
