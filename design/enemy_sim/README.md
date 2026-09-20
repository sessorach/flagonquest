# Enemy/combat simulator

Small Python tool for testing whether the enemy-encounter model in
`design/ENEMY_ENCOUNTER_DESIGN.md` actually produces the intended feel
(on-level, then stronger-than, then stretched-thin per Level) — built
to check the design against real Monte Carlo simulation rather than
algebra alone. Full write-up, findings, and the validation grid this
produced are in that document's "Analysis" section; this README is just
usage.

## Files

- **`tunables.py`** — every number that's still subject to revision: the
  enemy Level curve, Role/Armor/Action modifiers, and the Ability
  catalog subset. **Edit this file when the enemy model changes** — the
  other files implement the *shape* of the formulas and shouldn't need
  touching for a pure numbers retune. PC stat blocks used to live here
  too (`PC_STATS`/`PC_SKILLS_COMBAT`/`PC_HEALTH`) — moved to
  `sample_pcs.csv` once real character sheets existed to hold them
  properly; only `PC_SKILL_STAT` (a structural fact, not a tunable
  number) stayed behind.
- **`enemy_builder.py`** — turns a Level/Slots/Role/Defense-tier/Action/
  Armor/Abilities pick into a full enemy stat block, matching
  `archive/flagonquest_encounter_builder.xlsx`'s own formulas exactly
  (`python3 enemy_builder.py` re-runs the cross-check against the
  spreadsheet's own live worked example).
- **`sample_pcs.csv`** — real named PC Stat/Skill builds (all 5 Stats,
  all 25 Skills, matching `index.html`'s `STAT_SKILLS`), same
  Roster/reference split as the enemy CSV below: the `TRUE` "Baseline
  Tier N Party Member" rows are what `party.py`'s `make_party(tier)`
  actually uses (4 identical copies, the smoothed PC_SKILLS_COMBAT
  variant migrated from `tunables.py`); the `FALSE` rows are named
  reference characters — melee: Hilde, Browndog, Carrick, Jackal, Felix
  (one leaning into each of the 5 Stats); ranged (via the `Weapon`
  column, see below): Sable (Light Bow), Rook (Light Thrown), Wren (War
  Magic + Lance) — all built to rulebook.md's own Quick Creation
  Reference shape and verified to cost exactly 75 XP including
  Techniques. **Worth knowing**: a blank `Weapon` cell still means
  `combat_sim.py`'s PC attack only uses Melee — a non-melee, no-`Weapon`
  reference character like Felix reads as weak in a real fight
  regardless of how coherent the build is on paper; that's `Weapon`
  not being set for that character, not a limit of the sim anymore
  (see Wren for the same Essence-primary concept actually built to
  attack through Sorcery).
- **`party.py`** — loads `sample_pcs.csv`. `make_party(tier, good_luck=N)`
  pulls the Roster row and duplicates it x4 (still 4 identical party
  members, no distinct roles, no Techniques/items, no gear-based Resist);
  `good_luck=N` gives every PC N stacks of Good Luck on their own attack
  roll, for testing a mechanic's value empirically (see `combat_sim.py`'s
  note below). `get_pc(name)` pulls any row by name; `make_party_of(name)`
  duplicates one row x4 into a full party (for testing one build's own
  attack profile against the Roster - see `combat_sim.py`'s note on
  the three `Weapon`-based ranged builds); `all_pcs()` returns every
  row built. A row's `Weapon` cell (blank by default) switches which
  Skill/Stat drives that PC's own attack roll, Damage, and attack range
  away from the 1H Heavy Melee default - `tunables.WEAPON` has the real
  weapon_categories.csv/features.csv numbers behind each option, fully
  decoupled from Parry/Dodge/etc.
- **`sample_enemies.csv`** — every enemy stat block that's been built for
  a reason, one row per build (Level/Slots/Role/Defense-tier/Action/
  Armor/Battle Tactic/Fighting Style/Abilities/Archetype). The `Roster`
  column tells two kinds apart: the five `TRUE` rows are the validated
  one-per-Level on-level roster (tuned to land close to a genuine ~50%
  win rate at their own Tier); everything else is a `FALSE` reference
  build tagged with an `Archetype` label. Five archetypes exist at every
  Level 1-5 (25 rows total) — **Neutral** (no Role/Defense-tier skew),
  **Power-Attack** (Bruiser Role), **Max-Damage** (Striker Role +
  Powerful Weapon — every damage lever this sim has wired, at the cost
  of accuracy and Parry), **Ranged Caster** (Strategist Role, Ranged
  Spell, Powerful Spell — a backline caster that's given up on melee
  defense), and **Tank** (Tank Role, Heavy Armor, Durable + Enhanced
  Health — a real wall on purpose). Add a row here instead of writing a
  one-off script whenever a stat block gets built for a reason worth
  keeping around.
- **`sample_enemies.py`** — loads the CSV above via `enemy_builder.py`.
  `make_enemy(level)` pulls the Roster row for that Level (what
  `combat_sim.py` uses for the grid); `get_enemy(name)` pulls any row by
  name; `all_enemies()` returns every row built. Simulator fixtures for
  now, not a finished in-game roster — expect an "Example Enemies" doc
  to supersede the Roster rows once the tunables are locked down
  further.
- **`combat_sim.py`** — the Monte Carlo fight loop (`run_fight`) and
  driver (`simulate`). PCs attack whichever of the enemy's Parry/Dodge
  is worse for the enemy (`enemy_defense_for_pc_attack`, matching
  rulebook.md's "the target chooses which Defense to use" rule — this
  used to be hardcoded to Parry alone, which broke badly against the
  Ranged Caster archetype's -99 Parry trick before it was fixed). Also
  models Gambling (PCs punching through high Resist), Good Luck
  (`good_luck=N` on `simulate`/`run_fight`, applied to every PC — see
  the module's own note on why "every PC, every attack, all fight"
  reads very differently from the per-flip Value the balance model
  prices, and how to isolate just one PC instead), and a subset of the
  Ability catalog (Enhanced Health, Powerful Weapon/Spell, Strike
  (Crippling)/(Vulnerable), Poison (Bleeding), Durable — see
  `tunables.ABILITY_COST`'s own comment for which abilities are wired
  in and why the rest aren't yet). See its module docstring for what's
  still simplified/not modeled (Extra Successes from suit-pool
  matching, Techniques, items, real initiative — positioning has a
  first pass now, see `movement.py` below).
- **`movement.py`** — geometry helpers (`distance`, `move_toward`,
  `move_away`) for `combat_sim.py`'s optional `movement=True` mode: a
  bounded `tunables.ARENA_SIZE`-square arena, continuous coordinates, no
  obstacles or formations. `run_fight(..., movement=True)` starts PCs
  and enemies on opposite sides, and each unit has to close into its own
  effective range (`combat_sim.effective_range`) before it can attack
  that round — a Kiting unit (`sample_enemies.csv`'s `BattleTactic`
  column) retreats along the straight line away from its nearest threat
  instead of closing. Built to test the Speed-vs-Range question
  directly: can a backline caster's range actually keep it out of melee?
  See `combat_sim.py`'s module docstring for what that showed.
  `movement=False` (the default everywhere else in this README) is
  untouched by any of this — it's still the exact behavior the
  win-rate grid below was validated against.
- **`run_grid.py`** — runs every Party Tier × Enemy Level combination
  and prints win rate / average rounds / party HP% remaining.

## Usage

```
cd design/enemy_sim
python3 run_grid.py           # full 5x5 grid, 3000 trials/cell
python3 run_grid.py 10000     # more trials, slower but less noisy
python3 enemy_builder.py      # cross-check against the live spreadsheet example
python3 sample_enemies.py     # print every stat block in sample_enemies.csv
python3 party.py              # print every stat block in sample_pcs.csv
```

Testing one specific build against another (an item-balancing check, an
archetype comparison) without touching the Roster: monkeypatch
`combat_sim.make_enemy` (or `combat_sim.make_party`) to return
`sample_enemies.get_enemy("name")` (or `party.make_party_of("name")`,
4 copies of one reference PC) instead — see any of the Ring-item
pricing checks in `design/balance_weights_notes.md` for a worked
example. Add `movement=True` to either `run_fight(...)` or
`simulate(...)` to run that same matchup on the 2D arena instead of the
default list-order-focus-fire model — this is how the three `Weapon`
ranged builds (Sable/Rook/Wren) got tested against the Roster, see
`combat_sim.py`'s own note on the result.

After editing `tunables.py` (a pure numbers retune) or a Roster row in
`sample_enemies.csv`/`sample_pcs.csv`, just re-run `run_grid.py` — no
other file needs to change.
