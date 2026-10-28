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

## Start here: `replays/latest/`

The newest replays live in **`replays/latest/`** - one or two typical
fights from the most recent round of design work, as HTML pages you can
open in a browser, plus a `notes.md` saying what changed and how each
fight compares to its matchup's average. `make_replays.py` regenerates
them (older rounds move to `replays/archive/`). `encounter_grid.py` runs
every sample party against every encounter mix in
`sample_enemies.ENCOUNTERS`; `incoming_attacks.py` counts who gets
attacked.

## How the table actually plays: `TABLE_PLAY_NOTES.md`

The designer's notes on how real players fight (who dives in, who hangs
back, how cards get used, how builds spread their XP), the calibration
targets the sim is checked against (fight length, how often someone
goes Down or is Wounded, how often a hit enemy acts again), and the
results so far. `calibrate.py` prints those checks for the sample
parties; every table-play change is a switch in `tunables.py`
(`WOUNDED_RULES`, `RETARGET_RANGE_FIX`, `LINE_OF_SIGHT`, `PLAY_STYLES`)
so `calibrate.py -s NAME=False` shows what one change does on its own.
`play_styles.py` holds the Diver / Skirmisher / Back-liner turn plans
(sample_pcs.csv's Play Style column).

## Pricing effects and Styles: `effect_check.py`

`effect_check.py` puts one buff, debuff or stat change on one PC of
Party A at a time (combat_sim's "Test:" passives) and reads its worth off
a Health ladder, next to THE TABEL's price and THE TABEL's rates times
what the sim counted it doing. `turnorder_single.py` and
`style_compare.py` do the same for Styles. All three score a fight by
the party's Health left in points, losses counting 0. Until 2026-10-21
they scored it as a share of max Health, which made the ladder shrink
its own yardstick and read every other test 2-6 times too high; `--pct`
reproduces those numbers. `-m 1.75` (`--mult 1.75` for the other two)
was the table's toughness for the old Party A. Party A as built
(2026-10-24) needs ×2.0 for THE TABEL's 5-round fights; the defaults
are still 1.75 until the designer picks. Results are in
`design/balance_weights_notes.md`, "Every buff and debuff in the sim".

## Files

One-off studies, each dated in its own docstring and written up in
`balance_weights_notes.md` or `TABLE_PLAY_NOTES.md`. Most still run;
their results describe the sim as it was that day.

- **Bleeding (2026-10-07 to 10-20)**: `bleed_check.py`, `bleed_fate.py`,
  `bleed_points.py`, `bleed_reprice.py`, `bleed_strategy.py`,
  `bleed_vs_damage.py`, `bleed_builds.py`, `bleed_levers.py`,
  `bleed_cashout.py`, `bleed_protected.py`, `spend_pool.py`.
- **Enemies and encounters**: `archetype_compare.py` and
  `ability_compare.py` (price enemy archetypes and ability picks),
  `upgrade_configs.py` (the Upgrade model), `goblin_armor.py`,
  `horde_ratio.py` and `horde_experiments.py` (Horde tuning, 10-01),
  `enemy_toughness.py` (how long a hit enemy lasts; where ×1.75 came
  from), `level_baseline.py`, `margin_sweep.py`, `fight_length.py`.
- **Party behavior**: `party_targeting_compare.py` (targeting modes,
  10-07).

The core files and the regular tools:

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
- **`builds/`** — every sample character's build, as a Builder export
  (`index.html`'s Export file): Stats, Skills, each Technique copy with
  its Level and Features, and the inventory. The designer's exports are
  copied in from `archive/player_builds/`; characters with no export
  (the Baselines, Rook, Wren, the extrapolated `(L2)` rows, the test
  variants) are hand-made in the same format. Each file's `simNotes`
  says where it came from and any edit made to it (Felix's and Enith's
  Features per the designer, the 09-20 exports' "Heavy Armor" read as
  Medium, Maneuver copies listed in the order the sim uses them).
  A **variant** file (2026-10-25) names a `"base"` export and lists only
  what changes, in `party.apply_edits`' format: `"replace"` a copy's
  Level or Features (the Nth copy of an ID, in the export's order),
  `"remove"` or `"add"` a Technique, or change `"stats"`, `"skills"` or
  the `"inventory"`. So when the base export is updated, every variant
  follows it. Every build is checked against techniques.csv's Feature
  Budget and features.csv's costs, Max Copies and Advanced tier when it
  loads; one over budget stops with the copy and its Features.
- **`sample_pcs.csv`** — one row per sample character, holding only what
  an export doesn't: `Build` (the file in `builds/`), `Tier`, `Roster`
  (the "Baseline Tier N" rows `make_party(tier)` uses), `Weapon` (which
  weapon or War Magic the sim attacks with; blank is the 1H Heavy Melee
  default), `Choices` (picks the Builder keeps outside the export, per
  copy in the export's order: "War Magic: Dodge, Vital; Temper
  Soulblade: Fatestealer"), `Unmodeled` (Techniques the row knowingly
  carries unplayed), `Play Style`, `Battle Tactic`, `Bottles Item`,
  `Health` (blank works it out: 5 Shallow and 5 Deep plus techniques.csv's
  and items.csv's Health bonuses; a number overrides it), `Pronouns`, and
  short `Notes`. Each character's longer history is in
  `sample_characters.md`.
- **`techniques.py`** — every Technique the sim knows, by techniques.csv
  ID: what it adds to the sheet (`build`), what it puts on the fight
  dict (`setup`), and what it does in the fight (its hooks). War
  Magic, Battle Maneuver, Spirit Blessing and Healing Magic read each
  copy's Features. War Magic builds every copy from them: Destructive,
  Sanguine, Reign of Blood, Draw Power, the Furrow, Funnel and Nova
  Shapes, the Frigid, Kinetic, Corrupting, Necrotic, Barraging and
  Abjuring riders (a rider that offers Frost or Shadow damage takes
  whichever the target resists least), Piercing Elements and Wild
  Magic; Tormenting Curse with a rider makes a hex. Battle Maneuver
  has every Feature features.csv lists, Viper's Sting and Flurry
  included; Turn Elements and Elemental take their element from
  `Choices`. Spirit Blessing copies built differently each keep their
  own Features (2026-10-26). It adds Steady, Embolden, Retribution,
  River's Might, Touch of Chaos, Elemental Enhancement, Alacrity and
  Steal Fate; Healing Magic adds Purify, Rejuvenate, Guardian Angel,
  Triage, Deep Mending (no effect: the sim keeps one Health pool) and
  Healing Pact, and the healer Styles Field Medic and Lifeward. Force
  Missiles is a 1 AP Technique attack. War Magic's Arcane Chant,
  Glacier (Difficult Terrain, `movement.TERRAIN`) and Channel are in
  since 2026-10-27, so every combat Feature of every Buildable is.
  Out-of-combat IDs are listed in `OUT_OF_COMBAT`; ones that matter in a
  fight but need something the sim doesn't have yet (summons, walls,
  Vigor...) are in `DEFERRED`, with what each one needs. The rest of the
  catalog is in `techniques_more_a.py` (T005-T099) and
  `techniques_more_b.py` (T100-T205), written alongside each other on
  2026-10-27; they register the same way and share one Interrupt AP
  pool for a PC with no `ap_bank`. **An ID, Feature or
  item the sim doesn't know stops the load with its name** — add it
  here (or to `game_data.py` for an item) rather than finding out
  later it was ignored.
- **`enemy_abilities.py`** — the enemy Ability catalog's hooks: Strike
  and Poison riders, Grappling, Devastating, Harrying, Battering,
  Resilient, the 0 AP Actions, Retribution Aura, Action (Parting Shot).
  Build-time numbers stay in `enemy_builder_pcstyle._apply_catalog`.
- **`hooks.py`** — the hook points a Technique, Ability or rule plugs
  into (`POINTS` lists them with what each one's ctx carries), and the
  order handlers run in. combat_sim calls `hooks.run(point, unit, ctx)`
  where it used to test each Technique by name. Since 2026-10-28 an enemy
  attack has two Interrupt points: `attack_targeting` before its flip (a
  PC can move it onto itself, call it off, or change the Defense it
  checks: Lend Bulwark, Arrow Finds Only Mist, Seasons Pass the Forest)
  and `attack_flipped` after it, before it hits or misses (set the
  Defense, or make it a Parry: Swatting Paw, Slithering Hands).
- **`game_data.py`** — reads `scripts/techniques.csv`,
  `scripts/items.csv` and `scripts/features.csv` (names, Health
  bonuses, Feature Budgets and costs), and maps weapon and armor items
  to the sim's tables.
- **`compare_builds.py`** (2026-10-25) — "what if this character had
  that instead?" Runs a party, then the same party with one or more
  characters swapped for a variant row or an inline edit, on the same
  seeds against the same encounters, and prints the change in wins,
  Health left, how often someone goes Down, and fight length, each with
  its 95% margin (paired fight by fight, so the noise the two runs share
  cancels out). Results for the drafted variants are in
  `sample_characters.md`, "Variants". `sweep()` tries many swaps for one
  character against a single base run, for a broad look at modest reps;
  `hanforth_sweep.py`, `beornhard_sweep.py` (2026-10-26) and
  `maneuver_sweep.py` (2026-10-27) are the worked examples: Hanforth's
  Healing Magic, Spirit Blessing and spare XP, Beornhard's War Magic,
  and Hilde's and Browndog's Battle Maneuvers. "Health left" is in
  points since 2026-10-27; the sweeps' write-ups before that are in
  percentage points of the party's max Health (`--pct` reproduces them).
- **`party_tactics.py`** (2026-10-27) — party-wide tactic presets ("all
  in", "cautious", "max range", "hold the line", "bodyguard", "focus
  fire", ...) that hand out Play Styles by role and set targeting; `-t`
  on `calibrate.py`, `compare_builds.py` and the sweeps, or
  `tunables.PARTY_TACTIC`. `tactics_compare.py` runs a party under every
  preset. The Play Styles themselves (Diver, Skirmisher, Back-liner,
  Kiter, Holder, Guardian) are `play_styles.py`'s `PLANNERS`.
- **`encounter.py`** (2026-10-27) — every Encounter use a PC has, in one
  list: each Technique copy's uses with its Level (techniques.csv's for a
  fixed-Level Technique, the export's for a Buildable copy) and its kinds
  (Martial, Discipline, Spell and school, from Tags). `left`/`spend` by
  name, and one rule for which spent use a PC wants back (attacks first,
  then Level, then damage) and when it's worth it (it outranks every
  attack use still in hand). Vigor (Solemn Covenant), Willow Springs
  Back, Placeholder's Alacritous Adaptation and Warmage's Reserves all
  regain through it.
- **Live data** (2026-10-27): the sim reads the game's CSVs every run
  (`game_data.py`, re-read when a file changes): Technique Levels, Tags,
  Health bonuses and Feature budgets, and every weapon's and armor's
  numbers from items.csv (`tunables.WEAPON`/`ARMOR` are built from it;
  only War Magic's Lance is kept by hand). An export the CSVs have moved
  past still plays, by the CSVs, and is listed for a rebuild
  (`party.rebuild_list`, shown by `coverage.py` and SHEETS.md); a
  script's own `edits` that go over a Feature budget still stop.
- **`tech_common.py`** (2026-10-27) — the helpers every Technique file
  shares: attacks made off the attack loop (`_resolve`, `_log_strike`),
  paying cards, healing, reach, the one Interrupt AP pool. A new
  Technique is usually a registration line plus a hook built from these
  and encounter.py (techniques.py's docstring lists them).
- **`PROPOSED_BUILDS.md`** and **`builds/proposed/`** (2026-10-28) — my
  proposed Level 2 and 3 builds for Felix, Enith, Ashleigh and Sable, grown
  from the designer's Level 1 exports, as "(L2, proposed)" / "(L3,
  proposed)" rows. Not the designer's; an export replaces each one.
- **`technique_pass.py`** (2026-10-28) — the broad pass: every modeled
  Technique on up to three Level 3 hosts (taken off whoever knows it,
  added to whoever needs the fewest prereq ranks), read "free" and as
  an XP-matched swap, and every Feature of the four Buildables in a copy
  at a fixed Level. `technique_pass.csv` and `TECHNIQUE_PASS.md`.
- **`coverage.py`** (2026-10-27) — where every techniques.csv ID stands:
  modeled, out of combat or deferred (with the reasons). Exits 1 if one
  is missing or listed twice, so run it after adding Techniques to the
  CSV.
- **`SHEETS.md`** (generated by `sheets.py`, refreshed by
  `make_replays.py`) — every sample character as the sim builds it:
  Stats, Skills and Skill Totals, every Technique copy with its Level and
  Features, items, and the fight numbers. Variants come out resolved.
  The exports themselves are `builds/` (and the designer's originals,
  `archive/player_builds/`).
- **`mechanic_baseline.py`** (2026-10-27) — every Buildable Feature on a
  bare Technique copy, in Value through a Health ladder, next to THE
  TABEL's price for the stacks it landed. Results in
  `TABLE_PLAY_NOTES.md`, "Mechanic baseline". A new study is a list of
  (label, swap) pairs and parties, run through `sweep_main`.
- **`party.py`** — `load_sheet(row)` reads a row and its build;
  `make_pc(name, ..., health=, add_passives=, drop_passives=,
  battle_tactic=)` is the one way to build a character changed for a
  test. `make_party(tier, good_luck=N)` pulls the Roster row x4;
  `get_pc(name)`, `make_party_of(name)`, `make_party_from([names])` and
  `all_pcs()` as before. The Defense, weapon, armor and Card Technique
  formulas are in `_pc_dict`; see its module docstring. For swaps
  (2026-10-28): `xp_spent(build)`, `prereq_needs(build)` (every unmet
  Prereq Check clause, Choice branches included) and `fit(build, add=,
  remove=)`, which buys the prereq ranks a new Technique needs and takes
  the XP back out of `DONORS` (Defense and side Skills) so the total
  lands exactly; `free=True` skips that. `make_pc(edits={"build": b})`
  plays a whole build.
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
  (Hanforth). `target_kiter` (registered as "Kite Hunter") is the
  second — prefers any living enemy whose own `battle_tactic` is
  "Kiting" over anything else, closest among those if more than one,
  for a melee PC (Hilde, say) who wants to reliably end up adjacent to
  a disengaging enemy rather than falling back to plain closest/
  focus-wounded and maybe never getting there — built specifically so
  Parting Shot (T076) has a real priority-targeting option to pair
  with, not just the AI's default pick. **`target_focus_wounded`** is the base party strategy
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
- **`cards.py`** — the cards themselves (2026-10-09, `tunables.CARDS`):
  a 52-card `Deck` per PC and one for the GM, the day's hand and this
  fight's budget (`start_fight`), and the suit for each Skill. How
  players spend the hand (rescues, Gambles behind a card, kill
  top-ups, card Techniques) lives in `combat_sim.py`'s "Real cards"
  section, since it needs the fight. With `CARDS` off, the old
  stand-ins (`flipped_matches`, `chosen_matches`, the flat use
  counters) come back and the old numbers reproduce exactly.
  `card_stats.py` shows where each PC's cards go, per fight.
  TABLE_PLAY_NOTES.md's "Fourth round" has the whole model.
- **`sample_enemies.csv`** — every enemy stat block that's been built for
  a reason, one row per build (Level/Slots/Role/Defense-tier/Action/
  Armor/Battle Tactic/Fighting Style/Abilities/Archetype). The `Roster`
  column tells two kinds apart: the five `TRUE` rows are the validated
  one-per-Level on-level roster; everything else is a `FALSE` reference
  build. The old builder's Generic archetype rows (Neutral, Power-Attack,
  Max-Damage, Ranged Caster, Tank and Minion at every Level), Bog Caster
  and Marsh Viper Scout, which nothing used, moved to
  `archive/sample_enemies_retired_2026-10-25.csv`; only the four old
  Roster rows still use the old builder, since `make_enemy` and every
  default encounter read them. The **Mixed-Style** builds (Hedge Knight,
  Marsh Archer, Skulking Footpad, Fen Warden, Bog Skirmisher) were drafted with deliberately varied Fighting
  Styles rather than defaulting every enemy to Flurry, each row's own
  Notes explains its particular combo and the retuning pass that gave
  them their `DamageBonus`/`AccuracyBonus`/`DefenseBonus`). Bog
  Skirmisher is the newest of the six and the only one that actually
  retreats (`BattleTactic=Kiting`) — added specifically to give
  Parting Shot (T076) and `tactics.target_kiter` ("Kite Hunter") a
  real disengaging target to interact with, since none of the other
  five ever back off from melee; it's a first-cut build (a quick
  4x-clone check, not the multi-pass Powerful Weapon/Spell sweep the
  other four got — see its own Notes) and isn't part of the default
  `MIXED_ROSTER` mix. **`DamageBonus`/
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
  are. `PICK_COST` has the whole Ability catalog (2026-10-25) at
  `ENEMY_ENCOUNTER_DESIGN.md`'s draft costs; `_apply_catalog` does the
  build-time ones (Attunement and Resist by element in
  `resist_by_type`, Elemental Spell/Weapon, Enhanced Range/Reflexes/
  Speed, Improved Support, Devastating's +1) and `combat_sim` plays the
  rest. `ACTIONS` takes Curse, Great Heal and Shielding Nova too.
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
  the old 4x-clone Marsh Viper Scout default, since retired), falling back to the
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
python3 calibrate.py           # the sample parties against the table's calibration targets
python3 calibrate.py -s PLAY_STYLES=False   # ...with one table-play switch turned off
python3 compare_builds.py -L 2 -p B --swap "Beornhard (L2)=Beornhard (L2, Frost)"
                               # one character swapped for a variant row
python3 compare_builds.py -L 2 -p B --edit 'Beornhard (L2)={"replace": [{"id": "T120", "copy": 1, "features": {"Lance": 1, "Frigid": 2}}]}'
                               # ...or for an edit, with no file
```

**Trying a swap.** For a one-off, `--edit` takes the edit as JSON.
For one worth keeping, add a variant file to `builds/` (`"base"` plus
the edits and a `simNotes` line on what changed) and a `sample_pcs.csv`
row pointing at it, copying the base row's Weapon, Play Style and
Choices. A swap that changes a War Magic copy's Defense or a Maneuver's
element changes `Choices` too. Pick an enemy Health multiplier (`-m`)
that gives fights of about five rounds: at the default ×1.75 the Level
2 and 3 parties win in about three, too short for a debuff to pay off.

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
- **Converting a simulated win-rate delta into real Value units.** `+1
  Accuracy` (worth 1.0 Value by THE TABEL's own Locked convention) is
  the right anchor for a *persistent* mechanic tested the same way -
  both run for the whole fight, so their deltas are directly
  comparable. It's the WRONG anchor for a one-time/Encounter-cadence
  mechanic (a once-per-fight bonus attack, a charge-based ability) -
  comparing a single event against a bonus that compounds across every
  attack for the whole fight understates the one-time event badly (see
  balance_weights_notes.md's Advanced Cost-6 trio pass, where this
  actually happened). For anything one-time, use `combat_sim.py`'s
  `bonus_attack_control` field instead: it's an unconditional,
  once-per-encounter bonus attack with no target condition - literally
  THE TABEL's own Autoswing definition ("value of one full extra
  attack", Locked at 5.5). Run it alongside baseline in the SAME
  matchup as whatever's actually being tested, take its own win-rate
  delta, and that calibrates the conversion: `1 Value unit = (control's
  delta) / 5.5`. Apply that same factor to any other one-time
  mechanic's delta from the same matchup to get its Value directly, in
  the same units `balance_weights.csv` already uses. This factor is
  matchup-specific (a longer/harder fight gives one bonus attack more
  room to matter) - recalibrate per matchup, don't reuse a constant
  across different tests.
