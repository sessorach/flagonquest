# Enemy/combat simulator

Small Python tool for testing whether the enemy-encounter model in
`design/ENEMY_ENCOUNTER_DESIGN.md` actually produces the intended feel
(on-level, then stronger-than, then stretched-thin per Level) — built
to check the design against real Monte Carlo simulation rather than
algebra alone. Full write-up, findings, and the validation grid this
produced are in that document's "Analysis" section; this README is just
usage and a map of the files.

## How a fight works

Turn order is a real Reflex/initiative roll now (rulebook.md's actual
rule: a card flip + Reflex, highest to lowest, ties broken by
re-flipping just the tied units), rolled once at encounter start and
fixed for the whole fight — PCs and enemies interleaved by their own
Reflex, not "all 4 PCs, then all enemies" like this file used to do.

Every unit — PC or enemy — gets `tunables.AP_PER_TURN` (4) Action
Points on its own turn (rulebook.md's real "Actions on a Turn"
economy): moving costs 1 AP per move action (up to Speed meters,
repeatable — spend "as many as required" to close the gap, per the
designer, not an artificial cap), and an attack costs 2 AP, so a unit
that doesn't need to move gets up to 2 attacks. Every "AI" decision
inside that turn — who a unit targets, how it moves, how many attacks
it's willing to make, whether a PC does something other than attack —
lives in `tactics.py` as small named-function registries, not as `if`
branches in `combat_sim.py`'s `run_fight`; "which suit is this card"
assumptions live the same way in `cards.py`. See `combat_sim.py`'s own
module docstring for the full mechanical write-up (Resist by damage
type, Good Luck/Bad Luck, Fighting Style, Card Techniques, initiative)
before making changes — this README stays to usage and a file map.

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
  Magic). **`Heal Cards`**/**`Heal Bonus`** (blank = 1/0, matching the
  original hardcoded numbers) let a Support PC's own Healing Magic (T105)
  build read its real Level (Cost is "Discard [Level] cards") and any
  flat healing-boost feature total (Vitality, say) from the CSV instead
  of one universal amount. **`Heal Range`** (blank = no check) caps how
  far away an ally can be and still get healed, enforced only under
  `movement=True`. **`Passives`** (comma-separated tags, e.g. "Hand of
  Chaos") are always-on Technique effects with no AP/card cost, unlike
  Card Techniques above — see `tactics.sift_bonus`. **`Battle Tactic`**
  reuses the exact same `tactics.TARGETING` registry
  `sample_enemies.csv`'s own BattleTactic column already dispatches
  through — a PC can have a non-default targeting rule too now
  (Hanforth's own "Straggler Hunter") — see `party.py`'s own paragraph
  on all these columns.
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
  `strategy_support_healer`). `target_straggler` (registered as
  "Straggler Hunter") is the first PC-side `TARGETING` entry — goes
  after whichever enemy has the fewest others near it, for a PC who'd
  rather finish off an isolated target than wade into the main clump
  (Hanforth). **`target_focus_wounded`** is the base party strategy
  (the designer's own priority order) for every other PC — whoever's
  hurt worst, tiebroken by which enemy the whole party is collectively
  closest to (`party_reach`, summed distance from every living ally),
  so the party converges on one target from turn 1 instead of each PC
  chasing whatever's nearest to itself alone. `select_target` takes an
  optional `allies` list now — `_take_pc_turn` passes one (the living
  party), `_take_enemy_turn` doesn't, so enemy targeting is untouched.
  "Attack twice if possible" needed no new code — every PC was already
  uncapped. Only visible under `movement=True`: `target_first` (the old
  static-mode default) already focus-fires by list order, so the
  static-mode calibration numbers elsewhere in this doc don't move: win
  97.9% vs 92.1%, downed-rate 46.9% vs 63.7%, tested against the real
  party under movement. Each is a plain `{name: function}` registry keyed off a
  CSV column value — add a new tactic/strategy/style by writing one
  function and registering it, not by adding another `if` branch to
  `combat_sim.py`'s `run_fight`. See its own module docstring before
  adding one. Its **Card Techniques** section (`try_second_wind`/
  `perfect_strike_bonus`/`bottomless_bottles_choice`) covers PC
  techniques whose own cost is "discard a card," not AP — a self-heal
  when Wounded, +2 Good Luck on any weapon attack, and substituting a
  created item for one attack action, each gated by the shared
  `card_uses_left` budget (`sample_pcs.csv`'s own `Card Techniques`
  column above). `sift_bonus` is a related but separate idea — an
  always-on Technique effect with no AP/card cost (`Passives`), Hand of
  Chaos's own flat 1-in-4-chance-of-+1-damage stand-in for real
  suit-pool tracking.
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
  Level 1-5), **Minion** (0.5 Slots, one per Level — see
  `sample_enemies.py`'s own note on why), plus **Mixed-Style** (5 Level 1
  builds — Hedge Knight, Marsh Archer, Skulking Footpad, Bog Caster, Fen
  Warden — drafted with deliberately varied Fighting Styles rather than
  defaulting every enemy to Flurry, each row's own Notes explains its
  particular combo and the retuning pass that gave them their
  `DamageBonus`/`AccuracyBonus`/`DefenseBonus`). **`DamageBonus`/
  `AccuracyBonus`/`DefenseBonus`** (blank = 0) map straight to
  `enemy_builder.build_enemy`'s `ability_dmg_bonus`/`ability_acc_bonus`/
  `ability_def_bonus` params — flat retunes to attack damage, to-hit
  Accuracy, and all four defenses (Parry/Dodge/Bodily/Mental together)
  respectively, none of which also inflate the enemy's own Resist,
  unlike bumping `tunables.DMG_RESIST`/`ACCURACY` directly (which feed
  multiple derived stats off one shared Level-keyed number and turned
  out to be much sharper, harder to control levers during the
  Mixed-Style retune). Of the three, `DefenseBonus` is the one to reach
  for when a win rate and an "HP% remaining on a win" both need to move
  *together* toward a target rather than trading off against each other
  — see those 5 rows' own Notes for the numbers and why. **This whole
  `DamageBonus`/`AccuracyBonus`/`DefenseBonus` retune is currently
  paused** (all three blank) on the 5 Mixed-Style rows — superseded by
  the `ParryTier`/etc. construction below, not deleted (still real
  infrastructure if a future archetype wants that lever instead).
  **`ParryTier`/`DodgeTier`/`BodilyTier`/`MentalTier`/`AttackTier`/
  `HealthBonus`** are `enemy_builder_pcstyle.py`'s own columns — a
  second, real-PC-formula construction method (`_build_from_row` picks
  it over `enemy_builder.build_enemy` whenever `AttackTier` isn't
  blank; see that file's own module docstring for the full Defense =
  8 + Skill Total / Damage = base + Stat / Resist = Essence formula).
  The 4 default Level 1 archetypes (Hedge Knight/Marsh Archer/Skulking
  Footpad/Fen Warden) use this method now, at the plain designer-
  spreadsheet Skill Total numbers, plus one active retune knob -
  **`HealthBonus=2`** (Health 12 at Level 1, up from the real
  Baseline-party's own 10) - landed on after two follow-up passes the
  same session: first swapping the win-rate check from the smoothed
  generic party over to the real drafted one (Hilde/Browndog/Carrick/
  Sable - noticeably stronger fighters on their own, no teamwork
  needed to already beat the generic baseline), then again once the
  party's own base targeting strategy (focus fire on whoever's hurt
  worst, then whichever enemy the whole party's collectively closest
  to - `tactics.target_focus_wounded`) started actually mattering under
  `movement=True`. Current numbers, this row's own real Abilities
  (Durable/Strike (Vulnerable)/Poison (Bleeding), kept as-is - a
  Powerful Weapon/Spell standin was used to sweep the retune itself,
  see below, but isn't what ships): win≈99%, ~5.6 rounds (sd≈1.6 -
  noticeably tighter than any earlier candidate this session, mostly
  thanks to the party no longer scattering its own damage), ~72% party
  Health on a win. Bog Caster (the deliberate double-attacker, still
  excluded from the default 4-mix) stays on the old
  `enemy_builder.build_enemy` construction for now.
- **`enemy_builder_pcstyle.py`** — the second construction method above.
  Builds an enemy the way a PC actually gets built (`party.py`'s own
  formulas) instead of `enemy_builder.py`'s synthetic Level curve:
  `SKILL_TOTAL_BY_LEVEL` is `ENEMY_ENCOUNTER_DESIGN.md`'s own validated
  poor/secondary/primary table (the designer's spreadsheet baseline,
  not a fresh guess), `STAT_BASELINE_BY_LEVEL`/`HEALTH_BASELINE_BY_LEVEL`
  are `sample_pcs.csv`'s real "Baseline Tier N Party Member" Body/
  Essence/Health numbers. `defense_adj`/`accuracy_adj`/`damage_adj`/
  `resist_adj`/`health_bonus` are flat sensitivity-testing knobs (all 0
  on every current row) for isolating what each base number does one at
  a time — not a per-archetype design choice the way the Tier columns
  are.
- **`sample_enemies.py`** — loads the CSV above via `enemy_builder.py`.
  `make_enemy(level)` pulls the single Roster row for that Level;
  `get_enemy(name)` pulls any row by name; `all_enemies()` returns every
  row built. `build_encounter([names])` assembles a custom encounter
  from any mix of named rows (any Level/Slots combination — a Tank plus
  several Minions, say) — pass its result as `combat_sim.run_fight`'s
  own `enemies=` param; `total_slots(enemies)` sums a mix's own Slots,
  for checking it against "one Slot per PC" (the default encounter
  budget, per the designer — not yet written into ENEMY_ENCOUNTER_
  DESIGN.md itself). **`MIXED_ROSTER`**/**`make_level_encounter(level,
  n_enemies=4)`** is what `combat_sim.run_fight` actually calls by
  default now (no explicit `enemies=`) — a real varied 4-archetype mix
  for whichever Levels have one defined in `MIXED_ROSTER` (Level 1 so
  far: Hedge Knight/Marsh Archer/Skulking Footpad/Fen Warden, replacing
  the old 4x-clone Marsh Viper Scout default — still reachable via
  `get_enemy`, just no longer `Roster=TRUE`), falling back to the
  original `n_enemies` clones of `make_enemy(level)` for every other
  Level. Simulator fixtures for now, not a finished in-game roster.
- **`combat_sim.py`** — the Monte Carlo fight loop (`run_fight`) and
  driver (`simulate`). `_roll_initiative`/`_resolve_group_order` roll a
  real Reflex-based turn order once at encounter start (rulebook.md's
  actual rule, ties re-flipped), interleaving PCs and enemies rather
  than resolving one side's whole turn before the other's;
  `_take_pc_turn`/`_take_enemy_turn` are one unit's own turn, called in
  that fixed order every round. See its own module docstring for the
  full mechanical write-up: the AP economy, Resist-by-damage-type on both
  sides (`enemy_resist_for_pc_attack`/`pc_resist_for_enemy_attack`),
  Good Luck/Bad Luck (`resolve_card`), Gambling, Card Techniques, the
  Ability catalog subset, and what's still simplified/not modeled.
  **Harried** (glossary.md: -1 Dodge/Parry per stack, gained by anyone
  who defends with Parry or Dodge against an attack, "regardless of the
  attack's result" - rulebook.md; cleared at the bearer's own turn end)
  is now modeled too - a real, previously-missing rule (it isn't an
  Ability, so the original Ability-catalog wiring pass never covered
  it), not a tuning choice. `enemy_defense_for_pc_attack`/
  `pc_defense_for` read the current penalty; `_take_pc_turn`/
  `_take_enemy_turn` grant the +1 stack (only at the real attack-roll
  call site, not `pc_gamble_count`'s own odds check) and clear it at
  turn end. The effect size is large - Tier 1 vs Level 1 alone moved
  from ~36% win/~7.6 rounds to ~91%/~5.8 once it's on, and every trace/
  replay now shows a target's current Harried count next to each attack
  (`narrate_fight.py`/`replay_html.py`, `target_harried_after` in the
  trace). `_take_pc_turn`'s own grant is ordered *after* `pc_gamble_count`
  reads the target's Defense for this same attack - so a PC's gambling
  decision reflects the target's Harried count from *earlier* attacks
  this round, not a stack this attack is about to add on top of itself
  (that ordering was backwards at first - caught and fixed while
  checking the designer's own question about whether gambling already
  accounted for a target getting easier to hit as the round wears on;
  it does, now correctly).
- **`movement.py`** — geometry helpers (`distance`, `move_toward`,
  `move_away`) for `combat_sim.py`'s optional `movement=True` mode: a
  bounded `tunables.ARENA_SIZE`-square arena of whole spaces — the real
  grid-movement rule (the designer's own clarification): no fractional
  spaces, and a diagonal step costs the same 1 Speed as an orthogonal
  one, so `distance` is Chebyshev ("king-move"), not Euclidean. Used to
  be continuous float coordinates; `tunables.MELEE_RANGE` is now a real
  1 (adjacent), not an invented buffer. The party starts in a compact 2x2 block
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

## Testing conventions for ad hoc balance checks

For a quick "roughly how much is this worth" check (a proposed Feature
fix, a new Ability idea) rather than a real calibration pass, default
to these unless told otherwise - keeps a check fast and cheap instead
of burning tokens on precision the question doesn't need:

- **A few thousand trials, not tens of thousands.** Enough to see the
  shape (is it bigger/smaller/flat relative to the comparison point),
  not to pin down the exact percentage. 1500-4000 trials/config is
  usually plenty; only reach for more if the effect you're checking is
  genuinely small and a first pass came back too noisy to read. When
  movement mode's own extra cost (see below) forces a choice, trim
  trials before dropping positioning, not the other way around.
- **`movement=True` by default, not the static/no-position model.**
  Checked head to head at the real starter party vs. Level 3 x3
  (balance_weights_notes.md's Backfoot pass): static reads 57% win,
  movement reads 18.6% - closing distance, kiting, and Speed all cost
  the party a lot that the static model just doesn't charge for. That's
  not a minor rounding difference, it's a different fight, so any check
  run static-only risks measuring a mechanic's value in a combat model
  that doesn't look like real play. Only skip positioning for a quick
  sanity check (e.g. confirming a formula/annotation actually fires),
  never for a check whose numbers are meant to inform an actual balance
  decision.
- **Starter party (Hilde/Browndog/Carrick/Sable) is the default party**,
  but don't default to only the standard Level 1 Roster fight the way
  earlier passes did - it's saturated near 100% even under movement (no
  headroom for a delta to show), and the party's real starting Tier is
  worth checking across more than one enemy composition anyway. Try a
  small spread of Levels/enemy counts (a 1-enemy fight, a 2-3 enemy
  mix, maybe a mixed-Level pair via `sample_enemies.build_encounter`)
  and note which ones actually produced a readable signal - a check
  that came back too noisy or too saturated at some Level is itself
  worth recording (so the next person doesn't re-run the same dead
  end), but don't spend trials chasing a matchup that isn't informative
  just to have coverage everywhere.
- **Save an illustrative replay when a check is worth reviewing later.**
  `replays/` (this folder) holds a handful of `narrate_fight.py --html`
  outputs from specific mechanic checks, gitignored-sized-permitting
  (each is a self-contained page, typically well under 100KB) - not
  every test run, just the ones worth coming back to. Use `--vs-average`
  so the replay's own banner shows how that one seeded fight compares to
  the aggregate for its matchup, and check the combat log for the
  `turn_shift` annotation (or any other test-specific field) actually
  showing up on the events it should. A short paired `.md` note next to
  each saved replay (what was being tested, what the aggregate numbers
  came back as) is worth more later than the replay alone - the replay
  shows one fight, the note is what makes it findable and meaningful
  months later.
