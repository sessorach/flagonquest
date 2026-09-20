# Enemy/combat simulator

Small Python tool for testing whether the enemy-encounter model in
`design/ENEMY_ENCOUNTER_DESIGN.md` actually produces the intended feel
(on-level, then stronger-than, then stretched-thin per Level) — built
to check the design against real Monte Carlo simulation rather than
algebra alone. Full write-up, findings, and the validation grid this
produced are in that document's "Analysis" section; this README is just
usage and a map of the files.

## How a fight works

Every unit — PC or enemy — gets `tunables.AP_PER_TURN` (4) Action
Points a turn (rulebook.md's real "Actions on a Turn" economy): moving
costs 1 AP per move action (up to Speed meters, repeatable — spend "as
many as required" to close the gap, per the designer, not an artificial
cap), and an attack costs 2 AP, so a unit that doesn't need to move
gets up to 2 attacks. Every "AI" decision inside that turn — who a unit
targets, how it moves, how many attacks it's willing to make, whether a
PC does something other than attack — lives in `tactics.py` as small
named-function registries, not as `if` branches in `combat_sim.py`'s
`run_fight`; "which suit is this card" assumptions live the same way in
`cards.py`. See `combat_sim.py`'s own module docstring for the full
mechanical write-up (Resist by damage type, Good Luck/Bad Luck,
Fighting Style) before making changes — this README stays to usage and
a file map.

## Files

- **`tunables.py`** — every number that's still subject to revision:
  the enemy Level curve, Role/Armor/Action modifiers, the AP economy
  (`AP_PER_TURN`/`MOVE_AP_COST`/`ATTACK_AP_COST`/`HEALING_MAGIC_AP_COST`),
  and the Ability catalog subset. **Edit this file when the enemy or AP
  model changes** — the other files implement the *shape* of the
  formulas and shouldn't need touching for a pure numbers retune.
  `ARMOR` is the real `armor_categories.csv` table, shared by both
  sides now (enemies and PCs both get real worn-Armor Resist/Dodge/
  Speed effects, not two different tables).
- **`enemy_builder.py`** — turns a Level/Slots/Role/Defense-tier/Action/
  Armor/Abilities pick into a full enemy stat block, matching
  `archive/flagonquest_encounter_builder.xlsx`'s own formulas exactly
  (`python3 enemy_builder.py` re-runs the cross-check against the
  spreadsheet's own live worked example).
- **`sample_pcs.csv`** — real named PC Stat/Skill builds (all 5 Stats,
  all 25 Skills, matching `index.html`'s `STAT_SKILLS`), same
  Roster/reference split as the enemy CSV below: the `TRUE` "Baseline
  Tier N Party Member" rows are what `party.py`'s `make_party(tier)`
  actually uses (4 copies, the smoothed PC_SKILLS_COMBAT variant
  migrated from `tunables.py`); the `FALSE` rows are named reference
  characters — melee: Hilde, Browndog, Carrick, Felix (one leaning into
  each of the 4 physical Stats, Cunning covered by Carrick's Acrobatics
  lean); ranged/utility (via `Weapon`, see below): Sable (Light Bow),
  Rook (Light Thrown), Jackal (Light Thrown + Bottomless Bottles), Wren
  (War Magic + Lance); caster (via `Weapon`): Beornhard (War Magic +
  Lance, an Encounter-Technique attack, see `Weapon Uses` below) — all
  built to rulebook.md's own Quick Creation Reference shape and verified
  to cost exactly 75 XP including Techniques. Hilde/Browndog/Carrick/
  Jackal/Beornhard are player-drafted, real JSON exports from
  `index.html` (not this project's own reference-build convention), and
  replaced this project's own earlier versions of those same five names
  — a row's own Notes says so and gives the full derivation. A row's
  `Armor` cell (`Unarmored`/`Light`/`Medium`/`Heavy`, blank =
  `Unarmored`) is the real `tunables.ARMOR` table — see each row's own
  Notes for why that tier was picked (usually whether the build's Might
  Skill Total actually clears that armor's real Might Requirement).
  **Worth knowing**: a blank `Weapon` cell still means a PC's attack
  only uses Melee/Physical — a non-melee, no-`Weapon` reference
  character like Felix reads as weak in a real fight regardless of how
  coherent the build is on paper; that's `Weapon` not being set for
  that character, not a limit of the sim (see Wren for the same
  Essence-primary concept built to attack through Sorcery instead, with
  Fire damage). `Pronouns` (blank unless specified) is reference-only —
  useful for consistent rulebook prose, read by nothing in the sim
  itself.
  **`Card Techniques`** (comma-separated tags — "Second Wind", "Perfect
  Strike", "Bottomless Bottles", "Warmage's Reserves") names which of
  `tactics.py`'s Card Techniques (see its own section below) this PC
  has — a technique whose real cost is "discard a card" rather than AP,
  drawing on a shared per-fight budget (`card_uses_left`, `party.py`'s
  `hand_size // 3` — "say 1/3 of" a full hand, the designer's own quick-
  check framing). **`Weapon Uses`** (blank = unlimited, the default) is
  the separate idea of a PC whose own `Weapon` is itself an Encounter
  Technique with a limited number of known copies (Beornhard's 3x War
  Magic) — see `party.py`'s own paragraph on both columns.
- **`party.py`** — loads `sample_pcs.csv`. `make_party(tier, good_luck=N)`
  pulls the Roster row and duplicates it x4; `get_pc(name)` pulls any
  row by name; `make_party_of(name)` duplicates one row x4; `make_party_
  from([names])` assembles a custom 4-person mix from any named rows,
  for testing party composition itself; `all_pcs()` returns every row
  built. See its own module docstring for exactly how `Weapon`/`Armor`/
  `Support` each change a built PC dict.
- **`tactics.py`** — the pluggable "AI" every unit's turn is dispatched
  through: `select_target`/`TARGETING` (who a unit attacks), `move_unit`/
  `MOVEMENT_TACTICS` (how it moves), `attack_cap`/`ATTACK_CAP` (an enemy
  Fighting Style's own action-economy rule — Guarded/Aimed Shot/
  Skirmisher deliberately cap at 1 attack for their own compensating
  bonus, Flurry and every PC are uncapped), `defense_has_bad_luck` (a
  Guarded enemy that held its ground last turn imposes Bad Luck on
  attacks against its Parry/Dodge), and `resolve_pc_strategy`/
  `PC_STRATEGIES` (what a PC does instead of attacking — currently just
  `strategy_support_healer`). Each is a plain `{name: function}`
  registry keyed off a CSV column value — add a new tactic/strategy/
  style by writing one function and registering it, not by adding
  another `if` branch to `combat_sim.py`'s `run_fight`. See its own
  module docstring before adding one. Its **Card Techniques** section
  (`try_second_wind`/`perfect_strike_bonus`/`bottomless_bottles_choice`)
  covers PC techniques whose own cost is "discard a card," not AP — a
  self-heal when Wounded, a Good Luck bonus on a Gambled attack, and
  substituting a created item for one attack action, each gated by the
  shared `card_uses_left` budget (`sample_pcs.csv`'s own `Card
  Techniques` column above).
- **`cards.py`** — the one place "which suit is this card" gets decided:
  `flipped_matches(suit)` (a genuinely random flipped card, a 1-in-4
  roll) vs. `chosen_matches(suit)` (a discarded/played card, chosen by
  the player from their hand — always true, a deliberate stand-in for a
  cost that's a small slice of a full hand). `tactics.
  strategy_support_healer` uses `chosen_matches('Hearts')` for Healing
  Magic's own Hearts-discard bonus; a future suit-keyed mechanic
  reaches for this instead of a fresh `random.random() < 0.25`.
- **`sample_enemies.csv`** — every enemy stat block that's been built for
  a reason, one row per build (Level/Slots/Role/Defense-tier/Action/
  Armor/Battle Tactic/Fighting Style/Abilities/Archetype). The `Roster`
  column tells two kinds apart: the five `TRUE` rows are the validated
  one-per-Level on-level roster; everything else is a `FALSE` reference
  build tagged with an `Archetype` label — **Neutral**, **Power-Attack**,
  **Max-Damage**, **Ranged Caster**, **Tank** (one of each at every
  Level 1-5), plus **Minion** (0.5 Slots, one per Level — see
  `sample_enemies.py`'s own note on why).
- **`sample_enemies.py`** — loads the CSV above via `enemy_builder.py`.
  `make_enemy(level)` pulls the Roster row for that Level; `get_enemy
  (name)` pulls any row by name; `all_enemies()` returns every row
  built. `build_encounter([names])` assembles a custom encounter from
  any mix of named rows (any Level/Slots combination — a Tank plus
  several Minions, say) — pass its result as `combat_sim.run_fight`'s
  own `enemies=` param; `total_slots(enemies)` sums a mix's own Slots,
  for checking it against "one Slot per PC" (the default encounter
  budget, per the designer — not yet written into ENEMY_ENCOUNTER_
  DESIGN.md itself). Simulator fixtures for now, not a finished in-game
  roster.
- **`combat_sim.py`** — the Monte Carlo fight loop (`run_fight`) and
  driver (`simulate`). See its own module docstring for the full
  mechanical write-up: the AP economy, Resist-by-damage-type on both
  sides (`enemy_resist_for_pc_attack`/`pc_resist_for_enemy_attack`),
  Good Luck/Bad Luck (`resolve_card`), Gambling, the Ability catalog
  subset, and what's still simplified/not modeled.
- **`movement.py`** — geometry helpers (`distance`, `move_toward`,
  `move_away`) for `combat_sim.py`'s optional `movement=True` mode: a
  bounded `tunables.ARENA_SIZE`-square arena, continuous coordinates, no
  obstacles. The party starts in a compact 2x2 block
  (`combat_sim._party_formation`), enemies spread down the y-axis,
  front lines a random `tunables.START_GAP_RANGE` (5-10m) apart by
  default (`run_fight(..., start_gap=N)` for a fixed distance instead).
  `movement=False` (the default) skips positions/movement entirely —
  every unit is always "in range" — but still uses the same AP economy
  for attacks (see "How a fight works" above); it does **not** replay
  the exact old pre-AP-economy numbers anymore, since that economy is
  what changed.
- **`run_grid.py`** — runs every Party Tier × Enemy Level combination
  and prints win rate / average rounds / party HP% remaining.
- **`narrate_fight.py`** — runs ONE seeded fight with `run_fight(...,
  trace=[])` and renders it as a round-by-round ASCII position map plus
  a readable combat log, instead of just an aggregate win rate — good
  for actually looking at what a fight does, or sanity-checking a new
  tactic/strategy by reading its log. `--party name1,name2,name3,name4`
  swaps in a custom party (`party.make_party_from`); `--encounter
  "Name 1,Name 2,..."` swaps in a custom enemy mix
  (`sample_enemies.build_encounter`); `--static` runs `movement=False`
  instead; `--json out.json` dumps the raw trace; **`--html out.html`
  writes a real, self-contained graphical replay page** (battle map +
  combat log) you can open in any browser, no server or network needed
  — the easiest way to just look at one fight. See its own module
  docstring for the full CLI.
- **`replay_html.py`** — the HTML/CSS/JS template `narrate_fight.py
  --html` fills in; `render_html(trace, result, arena_size)` is
  importable directly if something else wants the same rendering from
  its own trace.

## Usage

```
cd design/enemy_sim
python3 run_grid.py           # full 5x5 grid, 3000 trials/cell
python3 run_grid.py 10000     # more trials, slower but less noisy
python3 enemy_builder.py      # cross-check against the live spreadsheet example
python3 sample_enemies.py     # print every stat block in sample_enemies.csv
python3 party.py              # print every stat block in sample_pcs.csv
python3 narrate_fight.py 1 1 3 --party Hilde,Browndog,Sable,Beornhard --html out.html
                               # narrate one seeded fight, and save a graphical replay to open yourself
```

Testing one specific build against another (an item-balancing check, an
archetype comparison, a custom Slots mix) without touching the Roster:
monkeypatch `combat_sim.make_enemy` (or `combat_sim.make_party`) to
return `sample_enemies.get_enemy("name")` (or `party.make_party_of
("name")` / `party.make_party_from([names])`) instead, or pass
`run_fight(..., enemies=sample_enemies.build_encounter([names]))`
directly for a one-off custom encounter — see any of the Ring-item
pricing checks in `design/balance_weights_notes.md` for a worked
monkeypatch example. Add `movement=True` to either `run_fight(...)` or
`simulate(...)` to run that same matchup on the 2D arena instead of the
default (no positions, but still AP-based) model.

After editing `tunables.py` (a pure numbers retune) or a Roster row in
`sample_enemies.csv`/`sample_pcs.csv`, just re-run `run_grid.py` — no
other file needs to change.

**A real recalibration is due.** The win-rate grid this file's Roster
enemies were tuned against assumed PCs with no worn Armor and exactly 1
attack a turn - both fixed (see combat_sim.py's own module docstring),
which swings the grid hard toward the party (an on-level fight that
used to read ~50% now reads closer to 100% at Tier 1-3). The Roster
enemies themselves haven't been retuned to match yet - that's a real
balance pass, not a mechanics fix, so it's deliberately left for the
designer to pick up rather than done unilaterally here.
