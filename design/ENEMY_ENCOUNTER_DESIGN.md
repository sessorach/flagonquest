# Enemy Encounter Design

> **Note (2026-11-03):** the decisions in these notes are summarized in `design/DESIGNER_NOTES.md`. Mentions of `RULES_DESIGN.md` here point to `archive/design_docs_2026-11-03/RULES_DESIGN.md`; `GM_GUIDE_NOTES.md`, `IDEAS_BACKLOG.md` and `PROSE_REVIEW_QUEUE.md` are in `design/todo/`.

A model for building mechanically distinct, intuitive enemies —
reconstructed from `archive/flagonquest_encounter_builder.xlsx`, a
spreadsheet the designer built and actually used at the table, uploaded
this session specifically so its math could get documented here rather
than living only in a personal file. **This document supersedes the
earlier from-scratch "Enemy Stat Block by Level" work** in
`balance_weights_notes.md` and `GM_GUIDE_NOTES.md` — that was a
reasonable first attempt built with no real precedent to check against,
but this spreadsheet turned out to already be a complete, richer,
actually-tested system for the exact same problem. Those earlier
sections are left in place as historical record (not deleted — see
their own superseded-by note), but this document is what to reach for
going forward.

## First principles: enemies play by the players' rules (designer, 2026-11-03)

Read this before any number below; every stat decision answers to it.

- **Enemies use the same logic and mechanics as the players.** The same
  Stats, Skill Totals and Defenses (Defense = 8 + Skill Total), the same
  weapons and armor from the player tables, Parry from the weapon Skill
  and the weapon's Defense, Resist from a Stat plus armor. The few things
  sanded off are there to keep combat quick: no per-encounter abilities
  to track, simple fixed tactics. If an enemy has a big two-hander the
  party can guess it doesn't parry well; sword and board in heavy armor,
  it doesn't dodge well. The mechanics should bear that out.
- **Enemy numbers stay in the players' ballpark.** A damage Stat starts
  around 2 and climbs to 4 by the top Levels, and an archetype can push
  it to the player cap of 5; Accuracy and Defenses run up to the
  players' +10; Health sits near a PC's. No stat goes past what a player
  could have. A goblin shouldn't have more Health than the PC fighting
  it: that breaks the sense that the world hangs together, and players
  read stat blocks by the same yardstick as their own sheet.
- **Legible.** Players should be able to size an enemy up from what it
  visibly is (armor, weapon, a wizard's staff) and be rewarded for
  acting on it: an enemy's five Defenses have a spread, so a weak
  Mental Defense on a brute is worth finding.
- **A canvas, not the painting.** Stat blocks and tactics are simple and
  laid out from the start: an archetype, a main Action, a passive or a
  tweak to that Action, at most a support enemy that spends most turns
  healing or shielding. The party's Techniques are what make a fight
  interesting; the enemy gives them something to work on. A tough
  bruiser that gains Protected every turn is enough: head-on it's a
  slog, debuffed and worn down it falls.
- **Engaging, not a slog.** Enemies shouldn't be bags of Health. Leaning
  a little more dangerous and a little less durable, with fights a bit
  spikier, is fine: parties build to support each other, and carry
  consumables for the bad fight.

Where a balance target and these clash, these win, and the balance gets
found inside them: which stats step up at which Level, how the five
Defenses spread, what an archetype adds.

## Design goals, in the designer's own words

> This was something I could bake the math into, and then use myself to
> help design sensible enemies, without a lot of calculation or work,
> and with some pre-baked stat blocks to create enemies that are
> mechanically separate AND have their strengths and weaknesses
> intuitive with how the game rules work for players... The goal with
> these is to prevent combat from boiling down to melee characters
> clashing and double-attacking until one tips over.

Two goals, and they pull in a specific direction together:

1. **Mechanically separate, intuitively so.** A player facing this
   enemy should be able to tell — from its own in-fiction description,
   not a hidden stat block — roughly what it's good and bad at, the
   same way a heavily armored knight obviously parries well and a
   robed cultist obviously doesn't. The Role/Defense-tiering system
   below is built specifically to make "this enemy is strong here, weak
   there" a real, legible fact rather than every enemy being a
   flat-stat bag of Health.
2. **Break the melee-clash-and-double-attack default.** Left
   unconstrained, the path of least resistance for any enemy is
   "stand in melee, attack twice, repeat" — the same failure mode
   `Fighting Style` and `Battle Tactics` below exist to prevent, by
   giving every enemy a real, different action-economy profile and
   targeting behavior instead of a uniform one.

Every mechanic below should be read against these two goals — they're
not incidental flavor, they're most of why the system is shaped the
way it is.

## Enemy Level and Encounter Slots

**Enemy Level** (1-5) is the same axis as Masterwork/Technique Level —
it sets every base numeric value below via one shared Level-keyed
table (see "The Level-based base stats" below).

**Encounter Slots** is a separate dial: how many "standard enemy"
slots this specific creature counts as in an encounter's budget. Three
values are used in practice: **0.5** (a minion — expect several of
these per encounter), **1** (a standard threat, one enemy = one slot),
**2** (an elite/boss-tier threat worth two standard enemies), plus
**4** for a solo boss (2026-10-07: a whole party's encounter in one
creature, with nine times a standard enemy's Health and Upgrades and two
turns a round, each with its own place in the turn order). Per the
designer, a 4-slot boss is a rare exception that hasn't come up in
their games; 2 Slots is the usual ceiling. This
is a genuinely different axis from Level — a Level 2 minion and a
Level 2 standard enemy share the same base Accuracy/Defense/Damage/
Resist, but scale apart on Health and ability budget (below).

### Health scales non-linearly with Encounter Slots — on purpose

This is the single most important, least obvious piece of the whole
system. Health isn't just `base × Slots`:

```
Health = ROUNDUP(base_health(Level) × slot_multiplier, 0)
slot_multiplier: 1 slot → ×1, 0.5 slots → ×1/3, 2 slots → ×3
```

**0.5 slots gives ⅓ Health, not ½.** This is a deliberate
action-economy tax, not an approximation error — verified against the
live spreadsheet's own worked example (Level 2, 0.5 slots: base Health
8 × ⅓ = 2.67, rounds up to **3** — matches the spreadsheet's own
"Deadbough Root-Tender"/"Deadbough Shade" example rows exactly) and
cross-checked against a second Level-2, 0.5-slot monster in the real
roster ("Deadbough Root-Tender" appears twice with identical stats).
**Why it isn't linear**: two 0.5-slot minions together cost the same
1-slot encounter budget as a single standard enemy, but they get **two
full turns** of actions between them instead of one — a real,
uncosted action-economy advantage a linear ½-Health split wouldn't
account for. The extra discount (⅓ instead of ½) is what keeps a pair
of minions from quietly out-performing one standard enemy of the same
total Health. The 2-slot case (×3, not ×2) works the same logic in
reverse: a single 2-slot enemy only gets *one* turn's worth of
actions despite costing twice the budget, so it needs
disproportionately more Health to make up for the actions it's *not*
getting compared to two separate 1-slot enemies.

**Open question, flagged rather than silently resolved**: the
spreadsheet's own "Deadbough High Priestess" (Level 2, 2 slots) is
recorded with **33 Health**, not the 24 the formula above predicts
(`8 base × 3 = 24`). Every other example in the roster matches the
formula exactly (Level 1/1-slot → 7, Level 2/1-slot → 8, Level
2/0.5-slot → 3, and "Shadow Mender," Level 2/1-slot with **11** Health,
matches base 8 plus the Ability catalog's own "Enhanced Health" bonus
of +3 exactly) — only the one 2-slot example doesn't reconcile cleanly
against the documented formula from this read-through. Worth checking
directly against the live spreadsheet if an exact 2-slot Health number
matters for a specific encounter, rather than trusting this document's
reconstruction of that one case.

## The Level-based base stats

One shared table, Levels 1-5, everything else in this document reads
off it:

| Level | Accuracy (= Good Defense) | Okay Defense | Poor Defense | Damage/Resist | Health (1 slot) | Ability budget |
|---|---|---|---|---|---|---|
| 1 | 4 | 3 | 2 | 1 | 7 | 2 |
| 2 | 6 | 5 | 4 | 2 | 8 | 3 |
| 3 | 7 | 6 | 5 | 3 | 10 | 4 |
| 4 | 8 | 7 | 6 | 4 | 11 | 5 |
| 5 | 9 | 8 | 7 | 4 | 13 | 8 |

**Good/Okay/Poor Defense** are the three tiers an enemy's Defense
categories get assigned to (see Defense tiering below) — Good equals
Accuracy exactly, Okay is Accuracy−1, Poor is Accuracy−2. **Damage/
Resist** caps out at 4 for both Levels 4 and 5 (doesn't keep climbing)
— a real, deliberate choice in the source data, not a typo across two
rows. **Ability budget** is a *rate*, not the final number — the
enemy's real ability budget is `ROUNDUP(this value × Encounter Slots,
0) × 5` (e.g. Level 2, 0.5 slots: `ROUNDUP(3×0.5,0)×5 = 2×5 = 10`
points to spend from the Ability catalog below).

Two more Level-keyed values, off the same table: **Reflex = 2 + Level**
(4 at Level 2, matching the spreadsheet's live example) and **Speed =
ROUNDUP(Level ÷ 2, 0) + 2** (3 at Level 2).

## Role: the broad archetype, nudging specific stats

Five Roles, each pushing a handful of specific stats up (sometimes
trading one down) — this is the main lever for "this enemy type feels
different from that one" at a glance. Two versions of this table exist
in the source: an earlier, simpler one and a richer, later one that
the live calculator's own worked example actually uses (the example's
chosen Role, "Defensive," only exists by that name in the richer
version) — **the richer version below is the authoritative one**, the
simpler earlier draft is noted after it for context only.

| Role | Modifiers |
|---|---|
| **Tank** | Resist +1 (Physical and all four elemental), Parry +1, Dodge +1 |
| **Striker** | Accuracy +1, Damage +1 |
| **Bruiser** | Damage +1, Resist +1 (Physical and all four elemental), Parry −1, Dodge −1 |
| **Strategist** | Accuracy +1, Bodily Defense +1, Mental Defense +1 |
| **Defensive** | Parry +1, Dodge +1, Bodily Defense +1, Mental Defense +1 |

Tank and Bruiser's Resist +1 is the NPC version of a character raising
Essence: the kind of character who takes that Role would. So it's one
+1 to every Resist, not +1 Physical plus a second +1 to each element.
An earlier version of this table (and the simulator) gave both, which
put a Level 3 Bruiser at 5 elemental Resist. Per the designer, an enemy
below Level 4 shouldn't have the equivalent of a 5 in any base stat, so
no damage bonus or Resist of 5 from stats alone; only Physical Resist
reaches 5 there, by way of armor. Dropping the double count moved the
win-rate grid by 2 points at most, inside the noise.

*(Earlier/simpler draft, superseded by the above but consistent with
it in spirit: Tank = Resist+1/Parry-Dodge+1; Striker = Damage+1/
Accuracy+1; Bruiser = Damage+1/Resist+1/Parry-Dodge−1; Strategist =
Accuracy+1/Parry-Dodge+1/Mental+1; "Backup" = Parry-Dodge+1/Bodily+1/
Mental+1 — the richer version above is a real expansion of this, not a
contradiction: same shape, more generous, and "Backup" renamed
"Defensive" with an added Dodge+1.)*

## Defense tiering: Primary/Secondary/base — the core "intuitive weakness" mechanic

> **Pending rework (2026-09-27):** per the designer, the average enemy
> should have Dodge/Parry 1 higher than Vital/Mental/Vigilant, with room
> to trade stats for higher Defenses and to specialize one Defense
> above the rest at a cost (e.g. a necromancer with very high Vital,
> lower Dodge/Parry). Also (2026-09-28): enemies should threaten the
> party more through mechanics (debuffs) and less through raw numbers.
> See `balance.md`'s Open balance work. The tiering below predates that
> and will change.

The original source spreadsheet gave enemies **three** Defense
categories, not the PC's five — **Parry/Dodge** (combined into one,
unlike PCs who pick between them per-attack), **Bodily** (= Vital
Defense), and **Mental**, with Vigilant Defense left out entirely (a
deliberate simplification there, not an oversight — nothing in that
source system varied it per-enemy).

The GM picked **one Primary Defense** (this enemy's clear strength) and
**one Secondary Defense** (its middling one) out of those three — the
third, un-picked category was this enemy's clear weakness. Concretely,
each Defense's base value (Accuracy + 6, the same base every category
starts from) got a flat **+2 if it's the Primary pick, +1 if
Secondary, +0 otherwise** — reproduced exactly from the live
calculator's own worked example (Level 2, Primary = Parry/Dodge,
Secondary = Mental): Parry/Dodge Defense 17 (base 12 + 2 primary + 3
flat), Bodily Defense 13 (base 12 + 0 + 1 flat, no bonus — the
un-picked category), Mental Defense 14 (base 12 + 1 secondary + 1
flat). This three-category shape is still the historical record of
what the spreadsheet actually specified.

**Extended to four categories, Vigilant included, as of the Martial
Techniques balance pass** (`design/balance_weights_notes.md`) — Feint
specifically targets Vigilant Defense (`8 + Insight Skill Total` per
rulebook.md), and leaving it unmodeled made that Technique's real hit
rate against a typical enemy unanswerable. Vigilant slots into the
same tiering mechanic as Bodily/Mental (base value ±0/+1/+2 by tier),
but **the GM now picks two Secondary Defenses, not one**, keeping the
core "exactly one clear weakness" shape intact across four categories
instead of three (1 Primary + 2 Secondary + 1 un-picked, same as the
old 1 + 1 + 1 did for three) — the alternative (1 Primary + 1
Secondary + 2 un-picked) would give every enemy two legible weaknesses
instead of one, diluting the whole "intuitive weakness" point below.
`enemy_builder.py`'s `build_enemy` takes `secondary_defs` (a pair) now
instead of a single `secondary_def`; existing enemies in
`sample_enemies.csv` that predate this change have their second
Secondary slot left blank (reads as un-picked/weak) until a real design
pass assigns one — flagged there, not silently guessed.

**This is the actual mechanism behind "intuitive strengths and
weaknesses."** A heavily-armored brute with Parry/Dodge as Primary is
legibly bad at resisting Mental effects (Persuasion, Intimidation,
Theurgy targeting the mind) if Mental is left as its un-picked
category — and a player who notices that and leans on a
Composure-targeting approach instead of just swinging harder is being
rewarded for reading the fiction correctly, not for metagaming a
hidden number. Vigilant slots into this the same way: a heavy fighter
who never invested in Insight is legibly exploitable by Feint, the
same "read the fiction, don't metagame a hidden number" reward.

## Battle Tactics and Fighting Style: breaking the melee-clash default

These two pickers exist specifically to serve the second design goal
above — every enemy gets a real, different *targeting* behavior and a
real, different *action-economy* profile, instead of defaulting to
"attack whoever's closest, twice, every turn."

**Battle Tactics** (who this enemy targets):

| Tactic | Behavior |
|---|---|
| Triage | Supports the most wounded ally |
| Hold the Line | Focuses on most aggressive characters |
| Vanguard | Focuses on characters attacking the backline |
| Hit Whatever | Focuses on the closest character |
| Kiting | Focuses closest, but keeps max range |
| Assassin | Goes for weak/isolated characters |

**Fighting Style** (this enemy's action economy):

| Style | Behavior |
|---|---|
| Flurry | Attacks/supports twice if possible |
| Guarded | Attacks/supports once; if it didn't move, attacks against its Dodge/Parry have Bad Luck this turn |
| Aimed Shot | Only attacks once, but it has Good Luck |
| Skirmisher | Only attacks once, but can move up to 3 times |

Note only **one** of the four Fighting Styles (Flurry) is a literal
double-attack — the other three are deliberately built as *alternatives*
to a flat double-attack (extra mobility, a defensive trade-off for
standing still, a Good-Luck-for-fewer-actions trade) precisely so
"attacks twice" isn't the assumed default every enemy reaches for.
Mixing Battle Tactics and Fighting Style picks across an encounter's
roster (a Kiting archer, a Hold-the-Line brute, an Assassin skirmisher
going after the backline) is what actually produces the
"mechanically separate" feel at the table — picking the same
Hit-Whatever/Flurry combination for every enemy in a fight reproduces
exactly the flat, melee-clash default this system exists to avoid.

## Armor

| Armor | Effect |
|---|---|
| Unarmored | — |
| Light | Physical Resist +1 |
| Medium | Physical Resist +2, Dodge −1 |
| Heavy | Physical Resist +3, Dodge −1, Speed −1 |

These are the live PC numbers from `armor_categories.csv`, which the
simulator already uses. The spreadsheet had Medium at Dodge −1, Speed −1
and Heavy at −2/−2. Per the designer (2026-09-30), enemies match live,
and Medium or Heavy Armor costs an ability pick (Heavy is two, Level 3+
only). See the hand-build draft in `GM_GUIDE_NOTES.md`.

## The Ability catalog

Every pickable ability, its point cost, and its effect — reproduced in
full from the source spreadsheet's master reference list. Costs are
paid out of the Level/Slots-derived Ability budget above. Grouped the
same way the source groups them (Combat Ability is the general
catch-all; Combat Action is specifically an attack/support action a
GM assigns as the enemy's actual turn action, separate from picking
abilities).

**Combat Actions** (the enemy's actual attack/support move — pick at
least one; costs are baked into the stat differences below, not a
flat point tag the way Abilities are):
- **Defensive Melee** — Accuracy +1, Damage 3, targets Parry/Dodge,
  Physical, and grants the enemy **+2 to its own Parry Defense** — the
  name is literal, this is the option that makes an enemy noticeably
  harder to Parry against. Verified directly against the live
  spreadsheet's own worked example (Level 2: this action alone is what
  takes Parry Defense from a base 15 up to the shown 17).
- **Offensive Melee** — Damage 4 (a full point higher than Defensive
  Melee), targets Parry/Dodge, Physical, and grants a smaller **+1** to
  the enemy's own Parry Defense — still safer than no bonus at all, just
  a real trade against Defensive Melee's larger one for the extra
  Damage.
- **Ranged Weapon** — Accuracy +1, Damage 3, Range ×3 (scales with
  Level), targets Parry/Dodge, Physical.
- **Melee Spell** — Damage 3, targets Dodge, Fire (default element —
  swap via an Elemental Spell/Weapon ability, below).
- **Ranged Spell** — Damage 2, Range ×2, targets Dodge, Fire.
- **Curse** — no direct damage; targets Dodge, Range ×2. "Target is
  debuffed +2 times" — pure control/debuff action.
- **Great Heal** — Range ×3, no direct combat value. "Target ally
  heals 2 Health."
- **Shield Ally** — Range ×3. "Target ally gains 4 Protected."
- **Shielding Nova** — Range ×3. "Allies in range gain 2 Protected."

**Combat Abilities** (5 points unless noted):
- **Action (Intimidating)** — Range ×2. Target Frightened once (0 AP,
  1/turn).
- **Action (Parting Shot)** — Enemy moves out of melee → free attack
  against them.
- **Action (Taunting)** — Range ×2. Target Taunted once (0 AP, 1/turn).
- **Attunement (Brilliant/Fire/Frost/Shadow)** — +4 Resist to that
  element, −1 Resist to its opposite (Brilliant↔Shadow, Fire↔Frost).
- **Durable** — Turn start → Protected stacks +1 (max 4).
- **Elemental Spell (Brilliant/Frost/Shadow)** — retypes a Spell
  action's damage to that element (no other stat change).
- **Elemental Weapon (Brilliant/Frost/Shadow)** — retypes a Weapon
  attack's damage to that element, at −1 Damage (a real cost for the
  reflavor, unlike Elemental Spell which is free).
- **Enhanced Range** — Range ×2 on the enemy's action.
- **Enhanced Health** — Health +3.
- **Enhanced Reflexes** — Reflex +3.
- **Enhanced Speed** — Speed +1.
- **Improved Support** — Support actions (heals/Protected grants) do
  +50% (round up).
- **Omniguard** (10 points) — Ignore all Harried.
- **Poison (Bleeding/Crippling/Necrotic/Slowing/Vulnerable)** — on a
  landed attack, target gains the named stacks (2 for
  Bleeding/Necrotic, 1 for the others) — targets Bodily specifically
  (a poison/toxin framing, not a weapon-edge one).
- **Powerful Spell** — Damage +1, and sets the enemy's **own** Parry
  Defense to effectively unusable (`K43=-99`) — not something done to
  the target, a trade the enemy itself makes: a caster leaning further
  into raw magical power stops being able to parry at all (fitting
  flavor for a spellcaster with no real weapon training), paid for with
  +1 Damage on their own Spell.
- **Powerful Weapon** — Damage +1, Accuracy −1, Parry −1 (a real
  glass-cannon trade on the weapon attack specifically).
- **Resist (Brilliant/Fire/Frost/Shadow)** — +2 Resist to that element
  alone (the cheaper, non-Attunement way to shore up one Resist).
- **Retribution Aura** — Attacker who damages this NPC gains a stack of
  Bleeding themselves.
- **Shadow Jaunt** — This enemy's movement is Shifting/Teleporting.
- **Strike (Battering)** — Attack is Parried → target still gains a
  Bleeding stack (punishes Parrying specifically).
- **Strike (Cleaving)** (10 points) — Attack can also hit one extra
  adjacent enemy.
- **Strike (Crippling/Necrotic/Slowing/Vulnerable)** — Attack hits →
  target gains that stack (1, or 2 for Necrotic).
- **Strike (Devastating)** — Damage +1; attacks deal their damage as
  Bleeding instead of direct Health loss.
- **Strike (Grappling)** — Attack hits → target is now grappled.
- **Strike (Harrying)** — Attack hits *or* is Parried → target Harried
  once either way.
- **Sturdy** — Flips made to grapple this enemy have Bad Luck; Pushes
  against it are halved (stacks).
- **Resilient** (10 points) — Turn start → remove 1 of each debuff.

**Combat Armor** — see the Armor table above (Unarmored/Light/Medium/
Heavy — these are picked from the same catalog, not a separate system).

**Combat Role**, **Battle Tactics**, **Fighting Style** — see their own
sections above; picked from this same master catalog, just broken out
here for clarity since they're structural picks rather than optional
extras.

**Wired into the combat simulator**: all of it, since 2026-10-25, through
`enemy_builder_pcstyle.py` (`PICK_COST` at the draft costs below, and
`ACTIONS` for Curse, Great Heal and Shielding Nova). A few readings the
sim had to pick: Curse lands 2 stacks of its MainEffect and Great Heal
and Shielding Nova 2 each, at the catalog's own numbers, not the Level
tables the sim's Hex, Shield Ally and Mend Ally use. Enhanced Range
doubles a ranged action and does nothing for a melee one. Poison
riders land on any hit, as Poison (Bleeding) always has. Cleaving's
extra target is another PC next to the attacker. Grappling uses the
rulebook's Grapple rules on both sides; a grappled PC who can't fight
from inside it (two-handed weapon, a bow or spell, a cautious play
style) spends 2 AP to try to break free, and the enemy contests with
its attack's Accuracy. Intimidating and Taunting need no roll. The old
`enemy_builder.build_enemy` still knows only the spreadsheet subset in
`tunables.ABILITY_COST`.

Testing this against `sample_enemies.py`'s roster turned up two things
worth knowing before picking abilities for a real enemy:
- **Powerful Weapon can backfire** on an enemy whose Primary Defense is
  Parry/Dodge specifically — its own -1 Parry from the ability directly
  undercuts that investment, and in one test raised the party's win
  rate from 14.7% to 28.1% rather than lowering it. The +1 Damage
  didn't make up for handing the party easier hits (and more
  Gambling room) on every one of their own turns.
- **Strike (Vulnerable) has no live target right now** — none of the
  five Combat Actions above actually target a PC's Bodily or Mental
  Defense (they all route to Parry/Dodge or Dodge), and Vulnerable only
  lowers Vital/Mental/Vigilant. It's correctly wired, just inert until
  a Bodily/Mental-targeting Action exists to pair it with.

## The point-buy economy behind all of this

Every axis above (Accuracy, Defense, Damage, Resist, Health,
Abilities) is really an **escalating-cost point-buy currency**, the
same "each additional point costs more than the last" shape PC
Stat/Skill costs already use (`rulebook.md`'s Spending Experience) —
not a flat per-point rate. The full marginal-cost tables from the
source (1-indexed by point number):

- **Accuracy/Defense**: 1, 2, 2, 3, 4, 4, 5, 6, 8, 10 (cost of the 1st
  through 10th point respectively)
- **Damage/Resist**: 2, 4, 6, 8, 10 (cost of the 1st through 5th
  point — this axis moves in bigger steps, matching Damage/Resist's
  own Level table topping out at 4 rather than climbing every Level)
- **Health**: 5 XP per point, flat (no escalation on this one axis)
- **Abilities**: 5 XP per "ability point" at the 1-point tier, scaling
  up to 30 XP by the 6-point tier (`2×2.5` at the base, `×[2,3,4,5,6]`
  for successive tiers)

These costs feed a **per-Level total budget**, reconciled against a
**loot/Gold discount** — the source assumes a total 350 Gold handed
out per creature across a notional "15 Levels" of treasure (i.e.
`350 ÷ 15 × Level` Gold, converted to an XP-equivalent at a rate of
Gold ÷ 7), and **subtracts that XP-equivalent from the enemy's own raw
stat-point subtotal** before converting to a final budget. The
reasoning: an enemy that drops real loot is *also* handing the party
power on top of whatever their own stats do, so their own stat budget
should be a little smaller to compensate — treasure and threat are
priced against the same currency, not two unrelated systems. After
that discount, the remainder is divided by a flat **"XP Combat
Impact" of ⅔** (not every point of raw stat-budget converts 1:1 into
something that actually matters in a fight) to reach the **final
per-Level enemy budget**:

| Level | Final per-Level enemy stat-point budget |
|---|---|
| 1 | 63.5 |
| 2 | 123.5 |
| 3 | 174 |
| 4 | 221 |
| 5 | 279.5 |

This is the number a GM building a brand-new enemy from raw points
(rather than using the Level-based base-stat table as a starting point
and just layering Role/Abilities on top, the faster path most of the
worked examples actually use) would be budgeting against.

**An earlier, simpler draft of this same reconciliation** exists in the
source too (a separate "NPC Enemy Rules" sheet) — it assumed a flat
**70% of a PC's XP goes toward combat-relevant stats** (the other 30%
elsewhere, matching this project's own later, independently-derived
observation that PC XP doesn't all go to combat) and a flat "value of
one enemy ability" of 3.5, producing a broadly similar but not
identical per-Level budget (58.75 / 107.86 / 158.63 / 230.36 / 256.79).
The two don't reconcile exactly — worth knowing this project went
through at least two passes at this same economic question before
landing on the fuller version above, not a sign either pass is wrong,
just that the fuller version is the one that ended up wired into the
live calculator and the real worked examples.

## Worked examples, from the source's own roster

Fourteen real enemies exist in the source spreadsheet's "Monster List"
tab, already built with this system. A representative few:

- **Deadbough Root-Tender** (Level 2, 0.5 slots — a minion): Health 3,
  Reflex 4, Other Resist 2, Physical Resist 3 (Light Armor), Parry
  17/Dodge 15/Bodily 13/Mental 14, Speed 3. Battle Tactics: Hold the
  Line. Fighting Style: Flurry. Action: Defensive Melee (Close Range,
  Accuracy +7 vs. Parry/Dodge, Damage 5 Physical). Abilities: Strike
  (Battering), Action (Parting Shot).
- **Deadbough High Priestess** (Level 2, 2 slots — this roster's one
  elite/boss-tier example): Health 33 (see the flagged Health-formula
  discrepancy above), Physical Resist 5, Fire Resist 5, Parry 17,
  Battle Tactics: Hit Whatever, Fighting Style: Aimed Shot, Action:
  Ranged Spell (Range 14m, Accuracy +6 vs. Mental, Damage 5 Fire).
- **Venomwolf** (Level 1, 1 slot): Health 7, Speed 5 (fast — no armor,
  a beast rather than an armored humanoid), Battle Tactics: Hit
  Whatever, Fighting Style: Skirmisher, Action: Defensive Melee
  (Accuracy +6 vs. Parry/Dodge, Damage 4 Physical), Ability: Poison
  (Slowing).
- **Shadow Mender** (Level 2, 1 slot): Health 11 (base 8 + Enhanced
  Health's +3 — the one roster example that cleanly demonstrates the
  Health-ability-bonus math), Battle Tactics: Triage, Action: Great
  Heal, Ability: Improved Support (+50% healing).

Full roster (name, Level, slots) for reference: Deadbough Root-Tender
(2, 0.5, ×2 — the same design used twice), Deadbough Smolderer (2, 1),
Deadbough Shade (2, 0.5), Deadbough High Priestess (2, 2), Deadbough
Sniper (2, 1), Ironbranch Shielder (2, 1), Ironbranch Controller (2,
1), Venomwolf (1, 1), Bitewolf (1, 1), Wither Weaver (2, 1), Shadow
Mender (2, 1), Otherworld Slasher (2, 1), Bandit Firemage (1, 1),
Bandit Raider (1, 1) — see `archive/flagonquest_encounter_builder.xlsx`
directly (`Monster List` tab) for every stat on each.

## Analysis: does this actually produce 5 discrete power tiers?

Per the designer's own stated goal, checked directly against the real
numbers rather than assumed: **the party should start roughly on-level
with a given Enemy Level, grow clearly stronger than it, then move to
the next Level and feel stretched thin again — five distinct,
felt steps, not a fine-grained treadmill that always keeps combat
"balanced."**

### The base stat curve is deliberately gentle — almost flat

Level-to-Level deltas on the four core axes:

| | L1→2 | L2→3 | L3→4 | L4→5 |
|---|---|---|---|---|
| Accuracy/Defense | +2 | +1 | +1 | +1 |
| Damage/Resist | +1 | +1 | +1 | **+0** |
| Health | +1 | +2 | +1 | +2 |
| **Ability budget** | +1 | +1 | +1 | **+3** |

Three of the four axes barely move after the opening Level 1→2 jump.
**Damage/Resist caps at Level 4 outright** — a Level 5 enemy hits no
harder and resists no better than a Level 4 one; only Health (+2) and
Ability budget (a near-doubling, +3 on a base of 5) keep growing into
Level 5. Converting to hit-chance terms: reaching a clearly "stronger
than" feel (~70%+ hit chance) or "stretched thin" feel (~35%) from an
"on-level" baseline (~54%, the card-average-7 case) needs roughly a
±2-2.5 point Skill Total gap — bigger than almost every one of these
Level-to-Level steps.

**Conclusion: the 5-tier feel is not something the base stat curve
produces on its own.** It has to come from two other places instead:

1. **The Ability catalog, used deliberately per tier** — this is the
   one axis that genuinely breaks the gentle-growth pattern (the
   Level 4→5 near-doubling), and it's the axis a GM directly controls
   per-encounter. A Level 5 fight should feel different from a Level 1
   one mostly because of *what it can do* (more elemental variety,
   real utility like Omniguard/Resilient a Level 1-2 budget can't
   afford, stacked debuffs), not because its Accuracy is 5 points
   higher. Lean on this axis, not on inflating base stats, whenever a
   tier needs to feel like a genuine step up.
2. **When the GM chooses to introduce the next Level into the
   story** — since PC growth is continuous (XP earned session by
   session) but Enemy Level is quantized into 5 discrete bins, holding
   a region's Enemy Level fixed while the party keeps earning XP
   *automatically* produces the on-level → outgrown arc, with no extra
   engineering needed on the enemy-math side. The discreteness lives in
   the GM's pacing decision (this region is Level 2 content; the party
   moves to Level 3 content at the next real story beat), not in the
   numbers themselves.

This isn't a flaw in the system — flat stat escalation avoiding a raw
numbers arms race is consistent with this project's own standing
design rule (`RULES_DESIGN.md`: "Reward cleverness and risk, not raw
power") — but it does mean the discreteness has to be an active choice
each time a new Level's content gets built, not something to expect
"for free" from the formula.

### What Skill Total a PC needs to be on-level, per Enemy Level

Computed directly from the real Defense numbers (card-flip math: for
roughly 54% hit chance, `PC Skill Total = Defense − 7`, since the
average card is 7), across all three Defense tiers an enemy might use:

| Enemy Level | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| vs. a Poor-tier Defense | 4 | 6 | 7 | 8 | 9 |
| vs. a Secondary-tier Defense | 5 | 7 | 8 | 9 | 10 |
| vs. a Primary-tier Defense | 6 | 8 | 9 | 10 | 11 |

Cross-checked against the earlier (superseded) session's own PC
Skill-Total-by-tier reconstruction (6/7/8/9/10, anchored on the
chargen ceiling / skilled-NPC-ceiling / adventurer-tier Skill Total
meanings) — it lines up closely with the Secondary-tier row above (off
by exactly 1 at Tier 1). That reconstruction's *shape* held up under
this real cross-check; what it couldn't verify was the XP timeline
next to it.

### A rough XP anchor — explicitly a planning estimate, not a verified rate

**This project has no documented XP-per-session or XP-per-milestone
rate anywhere** (`rulebook.md` only says Experience comes "as you
reach goals and milestones") — so no total-XP number can be *derived*
the way the Skill Total table above was. What follows is a labeled
estimate for planning purposes only, built by anchoring to the one
real data point that exists (`rulebook.md`'s own worked chargen
example: reaching Skill Total 6 via 1 Stat at rank 3 + 1 Skill at rank
3 costs 18 XP, which is 24% of the full 75 XP chargen budget) and
extending that same ratio outward using the real, escalating Skill/Stat
XP-cost formulas — **assuming a party keeps investing roughly as
broadly as chargen does** (not funneling an ever-growing share into
pure combat as they level; some Awareness, social Skills, Techniques,
crafting, etc. the whole way through):

| Enemy Level | Low estimate (vs. Poor Defense) | Mid estimate (vs. Secondary) | High estimate (vs. Primary) |
|---|---|---|---|
| 1 | 46 | **67** | 75 |
| 2 | 75 | **92** | 117 |
| 3 | 92 | **117** | 150 |
| 4 | 117 | **150** | 192 |
| 5 | 150 | **192** | 242 |

Read the **Mid** column as the working estimate if one number is
needed ("a party feels ready for Level 3 content around 117 total
Experience earned"); the Low/High columns show how much that number
moves depending which Defense tier "on-level" is measured against, to
keep from presenting false precision. **Notably lower than the
previous session's own guessed 75/125/175/225/275 schedule at every
tier past the first** (e.g. Level 5: 192 here vs. 275 guessed before —
a real, meaningful correction, not just a re-derivation landing in the
same place) — the earlier schedule's flat +50/tier shape had no real
anchor behind it at all; this one at least starts from a verified data
point, even though the *extension* past that point is still an
assumption, not a fact. **The single biggest lever in this table is
the "combat-XP-share stays ~24%" assumption** — a party that
specializes *harder* into combat as it levels (skipping non-combat
Skills more and more) would hit each Skill Total threshold on *less*
total XP than shown; a party that diversifies *more* (heavy Technique
or Crafting investment) would need *more*. Revisit this table if actual
play shows parties consistently feel on-level with a given Enemy Level
well before or after the total XP they've actually earned matches it.

### Empirical validation: Monte Carlo combat simulation

The algebra above checks out, but it can't see everything — multiple
enemies, multiple rounds, and how a GM's actual Role/Action/Armor/
Defense-tier choices compound together. Built a small combat simulator
(`design/enemy_sim/`) to test the "5 discrete tiers" hypothesis
directly: 4 party members (per the PC power-per-Tier numbers above)
against 4 copies of a same-Level enemy, fought out thousands of times
with real card flips, tracking win rate, rounds to resolve, and party
Health remaining. See `design/enemy_sim/README.md` for the tool itself;
this section is the finding.

**First pass, enemies picked straight off the base Level curve, no
special tuning**: wildly inconsistent on-level win rates — 47%, 8.5%,
0%, 55%, 9.6% across Levels 1-5, when the target was ~50% at every
Level. Diagnosis, confirmed by tracing the actual numbers: **individual
build choices swing real difficulty far more than raw Level does.** The
first "Level 3" test enemy (a Tank with Primary Defense on Parry/Dodge
*and* Medium Armor *and* Defensive Melee's own +2 Parry bonus, all
stacking onto the same stat) came out needing 5 hits to drop instead of
the ~2 the flat per-Level curve implies — genuinely elite-tier tough
while still nominally "just Level 3." Caught a real gap in the
simulator too along the way: it wasn't giving PCs any Physical Resist
at all, inflating difficulty everywhere (worst against double-attack
Fighting Styles) until fixed.

**Second pass — the PC side itself got replaced.** The abstract
"Skill Total by Tier" estimate this section's algebra used above (and
the party.py that originally fed the simulator) was replaced with a
real, named Stat/Skill build per Tier — an actual character (favorite
Skill, a defensive core, broad utility Skills, real Stats), verified
XP-exact against `rulebook.md`'s own chargen worked example rather than
an abstract number. See `design/enemy_sim/tunables.py`'s `PC_SKILLS`/
`PC_STATS` for the build and its own comments for the full derivation
and every correction that went into it — most consequentially, PC
Weapon Damage uses **Body** (not Agility, `weapon_categories.csv`) and
PC Resist is **raw Essence with zero Skill investment needed**
(rulebook.md) — the latter had been badly under-modeled, making PCs
read as far too fragile before the fix. This is a real, meaningful
correction to the PC baseline, not a re-derivation landing in the same
place — the corrected numbers are generally weaker (more realistically
spread) than the earlier abstract estimate, especially on Resist.

That correction broke the previous roster outright — Levels 2-5
collapsed to 0-2% win rate against the new, weaker PC numbers, the same
order-of-magnitude problem the first pass diagnosed, just from the
opposite direction (enemies now overtuned, not undertuned). A first
retuning pass (searched per Level, since no single Role/Defense-tier
"formula" worked across all 5 Levels at once - a build tuned for
Levels 3/5 made 1/2/4 nearly unloseable applied unchanged) landed a
clean-looking diagonal, but two further fixes were needed before the
numbers could be trusted.

**Third pass — giving enemies the real player Armor system surfaced two
real gaps, not just a tuning nuance.** The designer asked for enemies to
use the same Light/Medium/Heavy Armor choice players do (`enemy_
builder.py`'s `ARMOR` table is a deliberate simplification of the real
`armor_categories.csv`, anchored so Light matches it exactly - see
`tunables.py`'s own comment). Testing it found:

1. **PCs had no counter-play modeled against high Physical Resist at
   all.** `rulebook.md`'s damage rule is a flat subtraction (`damage -
   Resist`), and a Medium/Heavy-armored enemy's Resist can rival a PC's
   whole weapon Damage - meaning normal attacks dealt exactly 0 net
   damage, forever, against nothing more exotic than a Level 2 enemy in
   Heavy Armor. The real counter is Gambling (rulebook.md: declare N
   Gambles before a flip, each is -2 to the roll but grants +1 Extra
   Success - and +1 damage - if it still hits) - not modeled at all
   before this. Added `combat_sim.pc_gamble_count`: a PC gambles enough
   to make a hit deal net damage when a normal hit would deal none
   (since a real player facing a guaranteed zero has nothing to lose by
   trying), and gambles once more opportunistically when it's already a
   safe bet.
2. **The 10-round cap was quietly masking the real win/loss split.**
   A build that read as "10% win rate" turned out to be a near-even
   201-vs-211 split once allowed to actually resolve - 1588 of 2000
   trials had been hitting the cap as an unresolved "draw," not a loss,
   and draws don't count toward win rate. Raised `run_fight`'s default
   `max_rounds` from 10 to 30. This also explains the previous pass's
   own flagged "Levels 2-5 run slower, more draws" finding - it wasn't
   a symptom of the Level curve, it was the round cap cutting close,
   slow-grinding fights short before they could resolve.

With both fixes in place, retesting confirmed **Light Armor specifically
is the tier that reads as "on-level"** - Unarmored is too easy, and
Medium/Heavy remain a real wall (0-12% win rate) even with smart
Gambling, reading as a legitimately tougher "elite" encounter rather
than an on-level fight. All five sample enemies below use Light Armor
for this reason, not an arbitrary pick:

| Enemy | Level | Role | Primary/Secondary Defense | Action | Armor | Battle Tactics | Fighting Style |
|---|---|---|---|---|---|---|---|
| Marsh Viper Scout | 1 | Striker | Bodily / Parry/Dodge | Offensive Melee | Light | Hit Whatever | Flurry |
| Ironbranch Skirmisher | 2 | Bruiser | Parry/Dodge / Mental | Ranged Spell | Light | Hit Whatever | Flurry |
| Ironbranch Warden | 3 | Bruiser | Bodily / Mental | Ranged Weapon | Light | Assassin | Guarded |
| Deadbough Priest | 4 | None | Bodily / Mental | Melee Spell | Light | Assassin | Flurry |
| Deep Coven Matriarch | 5 | Striker | Mental / Bodily | Ranged Spell | Light | Assassin | Guarded |

**The resulting Party Tier × Enemy Level grid** (win rate %, 1500
trials/cell, `design/enemy_sim/run_grid.py`, `max_rounds=30`):

| Tier | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| 1 | **46.3** | 0.0 | 0.0 | 0.0 | 0.0 |
| 2 | 98.6 | **49.0** | 0.0 | 0.0 | 0.0 |
| 3 | 100.0 | 99.3 | **52.3** | 0.0 | 0.0 |
| 4 | 100.0 | 100.0 | 100.0 | **50.9** | 39.3 |
| 5 | 100.0 | 100.0 | 100.0 | 44.3 | **42.3** |

Zero draws anywhere in this grid (every cell now resolves to an actual
win or loss within 30 rounds) - the cleanest, most trustworthy version
of this diagonal yet, every on-level cell within ~8 points of 50% and
lockout above one's own Tier now *fully* clean (0.0%, not just close).
One soft spot: Tier 5 vs. Level 4 (44.3%) reads slightly *weaker* than
Tier 4 vs. Level 4 (50.9%), when a stronger party should do at least as
well - most likely noise from the PC build's own per-Skill growth not
being perfectly monotonic tier-to-tier (`PC_SKILLS_COMBAT`), not a
grid-construction bug; left as-is rather than force-tuned, same
reasoning as always: the underlying baselines are still expected to
move.

**Caveat carried over from the tuning process itself**: reaching that
clean diagonal took real, deliberate build choices per enemy - it
didn't fall out of the base Level curve automatically, and didn't fall
out of one reusable build pattern either. The underlying PC-Tier/
enemy-Level baselines in `design/enemy_sim/tunables.py` are themselves
expected to move as the PC and enemy models get worked on more (per the
designer). Re-run `python3 run_grid.py` after any tunables change to
see where the diagonal lands - and when interpreting a *low* win rate
from any future run, check the raw party/enemies/draw counts
(`simulate()`'s 4th return value) before assuming it means "this build
loses" rather than "this build is just slow to resolve."

**This table is now known stale** (found while retuning Level 1's
Mixed-Style roster, 2026-09-21): several mechanical additions landed in
`combat_sim.py` after this grid was generated (Card Techniques, the
real Armor/AP economy, real initiative order), and nobody re-ran
`run_grid.py` afterward to check the diagonal still held. It doesn't -
most on-level cells now read 95-100%, not ~50%, when actually measured.
Only Level 1 has been re-tuned against this since (see `sample_
enemies.csv`'s Mixed-Style rows and `tunables.HEALTH_BASE[1]`) - Levels
2-5 still reflect the stale numbers in this table and need the same
treatment before trusting them again.

## Superseded sources in the same workbook — historical only

Three more tabs in the source workbook explore the same problems from
different, ultimately-abandoned angles. Kept in the archive copy for
the record, not modeled here:

- **NPC Combatant** — a different, incomplete draft built around a
  single "Combat Proficiency" score (0-10ish) rather than Level, with
  a "pick 2 Focused Stats"/"pick 2 Focused Defenses" structure and full
  non-combat Skill Totals (Stealth, Masquerade, Awareness, Insight,
  Acrobatics, Athletics) derived from that one score. Contains broken
  formulas (`#VALUE!`/`#N/A` cells) — clearly an earlier or parallel
  exploration that didn't get finished, not a working alternate system.
- **Social Contests** and **Social References** — the *old*,
  pre-Pressure-rework Social Contest system's own NPC-builder
  counterpart (Demerits, Intent/Debate/Mental Defense, Compelling/
  Logical/Forceful Statement types, "front member" positioning, Social
  Edges like "All-Rounder"/"Home Turf"). Fully superseded by the
  current Statement/Support/Pressure rules and this session's own
  Social Encounter Baseline (`balance_weights_notes.md`) — consistent
  with the "Concessions"/"front" terminology already flagged as defunct
  in `IDEAS_BACKLOG.md`. Not a source to reconcile the new Social
  Encounter Baseline against; purely historical.

## Planned next steps

Per the designer: the PC and enemy baseline models (`design/enemy_sim/
tunables.py`) are still being actively worked on and expected to
change. Once those settle, this project will want real **"Example PC
Builds"** and **"Example Enemies"** documents in `design/` — a proper,
game-ready roster, not just `enemy_sim/sample_enemies.py`'s simulator
fixtures. Revisit this section once the tunables are locked down rather
than starting that work against numbers still in flux.


## Enemy variety standard (2026-09-30)

Per the designer: earlier drafts suffered from generic stat blocks, so
enemies should have mechanical breadth while staying simple to run.

- **No activated abilities.** An enemy has one thing it does: its main
  **Action**. Attackers attack; support enemies Protect or heal an ally;
  debuffers attack a Defense (usually Mental) for no damage and land a
  big stack of one debuff. Support and debuffer enemies carry a
  **backup attack** for when there's nothing useful to buff or debuff.
  Plus its **Fighting Style** (Flurry / Guarded / Aimed Shot /
  Skirmisher) and **Battle Tactic** (nearest, the most hurt, kiting).
- **Every enemy puts something on the fight:** a debuff on the party (an
  on-hit rider from its Ability budget, or a debuffer's whole Action) or
  a buff on its allies. On-hit riders so far, 5 points each: Crippling,
  Vulnerable, Bleeding (Poison, 2 stacks), Slowing, Frightening,
  Taunting. Durable (self-Protected each turn) is the buff option.
- **More attack types:** Shadow casters against Vital Defense, Fire
  casters against Dodge, debuffers against Mental, alongside the melee
  and ranged weapon attackers against Parry/Dodge.
- **Enemies don't know the party's Defenses.** Targeting is position
  (nearest) or visible wounds (the most hurt), never "who's easiest to
  hit." A Taunted enemy goes for its Taunter.
- **How the designer builds a fight** (2026-09-30): usually two stat
  blocks, three for a complicated one, and rarely four different enemies.
  At most one enemy that doesn't attack (a healer or a debuffer). Two or
  more non-attackers made the old Chapel mix drag. A basic fight might be
  bruisers that Slow on a hit to bog down the party's front line, plus a
  damage caster in the back throwing spells at Vital. A complicated one
  might be minions plus a damage caster and a debuffer. Enemy groups are
  meant to stay simpler than the party. The sim's current mixes
  (`sample_enemies.CURRENT_MIXES`) follow this:

  | Mix | Enemies |
  |---|---|
  | Frontline | 2 Brutes + 2 Grave Callers |
  | Shield Wall | 2 Hedge Knights + 2 Marsh Archers |
  | Warband | a Brute + 2 Footpads + a Warpriest |
  | Horde | 4 Goblin minions + an Ember Caster + a Bog Hexer |

- **Debuff/buff size:** a debuffer's Hex or a support's Shield Ally
  lands `EFFECT_STACKS` = 3 at Levels 1-2, 4 at 3-4, 5 at 5, priced to
  trade roughly evenly with an enemy hit (~2 net Health, ~8 value).

In the simulator: `enemy_builder_pcstyle.ACTIONS` gains **Vital Spell**
(Shadow vs Bodily), **Hex** (no damage, vs Mental, `MainEffect`
stacks) and **Shield Ally** (Protected on the most-hurt ally), each
non-attack Action with a `BackupAction`. New archetypes: Brute,
Warpriest, Grave Caller, Bog Hexer, Mire Witch (Levels 1-3), grouped
into three mixes per Level in `sample_enemies.ENCOUNTERS` (Classic,
Warband, Coven). PCs now feel Slowed (Speed), Frightened and Taunted
(Bad Luck), and Browndog's Challenge Taunts the enemy nearest the
party's most fragile member. `encounter_grid.py` runs the comparison.


## Projection model: enemies built like players (2026-09-30)

For getting projections solid before simplifying into a hand-buildable
"low baseline, archetypes add" system (the designer's original
spreadsheet shape, where upgrades like a Heavy weapon or Medium/Heavy
armor come out of an ability-point budget). In the simulator today an
enemy is built from real player rules: the Stat spread of a PC one
Level behind it, ordered by archetype; damage from the players' weapon
and spell table; Resist from Essence plus the players' armor table;
Health 10, a PC's base without Toughened Body; Defenses and accuracy
from the Level's Skill Total tiers. Protect and heal Actions can't miss,
so they grant what an average enemy attack delivers (2 at Levels 1-3).
Full numbers and the sweep that settled the margin:
`balance_weights_notes.md`, "Enemy margin".

**The hand-build version (draft, 2026-09-30)** lives in
`GM_GUIDE_NOTES.md`, "Enemy stat blocks by hand". It keeps the
spreadsheet's structure: a Level baseline, one archetype (the
spreadsheet's Roles) on top, then a fixed number of ability picks. The
numbers are moving over to match the simulator.

The designer's rules for it:

- **XP anchor.** Level N matches a midpoint player of that tier: Level
  1 ≈ 75 XP, Level 2 ≈ 125 XP, then up 50 per Level.
- **Costs.** An overall gain costs an ability pick: better armor, a
  heavier weapon, an on-hit debuff. A trade is a free choice or comes
  with the archetype: a shield (Defender), a two-hander (Bruiser),
  Defense tiers, the main Action.
- **Weapons.** Enemies start from light-weapon numbers: a one-hander, a
  Light Bow, or a spell.
- **Health.** It's the only stat that breaks from player numbers. It's
  low early and padded late: penciled at 8/10/12/15/18.
- **Ability values.** We'll settle what one pick is worth later, at a
  size that keeps the math clean without getting granular.

Still to do in the simulator: build the sample roster the hand-build
way, and calibrate the baseline table until the fights land on target
(most or all fights won, about 5 rounds). At Level 2, the hand-built
heavy hitters currently come out about 1 damage lower and 1-2 Resist
tougher than the projection model's.

### Archetype comparison (2026-09-30)

`enemy_sim/archetype_compare.py` applies each archetype's adds to every
enemy in the Level 2 Classic, Warband and Horde mixes. It runs those
against parties A and B, 400 fights per matchup.

The measure is the party's expected Health left (losses count as 0).
Each archetype is then priced against a ladder of plain enemies with
−2/+2/+4 Health, so the result reads as "worth about N Health per
enemy". Plain enemies leave the party 62% of its Health on average.

| Archetype | Adds | Health left | Worth (Health per enemy) |
|---|---|---|---|
| Defender | Parry +1, Dodge +1, Resist +1 | 30% | +6.8 (past the ladder's end, extrapolated) |
| Backup (Resist) | Parry +1, Dodge +1, Mental +1, Resist +1 | 31% | +6.6 (extrapolated) |
| Bruiser | Damage +1, Resist +1, Parry −1, Dodge −1 | 43% | +3.6 |
| Striker | Accuracy +1, Damage +1 | 45% | +2.9 |
| Backup | Parry +1, Dodge +1, Vital +1, Mental +1 | 49% | +1.9 |
| Strategist (Dodge) | Accuracy +1, Dodge +1, Mental +1 | 53% | +1.3 |
| Strategist | Accuracy +1, Vital +1, Mental +1 | 58% | +0.6 |
| Striker (glass) | Accuracy +1, Damage +1, Resist −1 | 63% | −0.2 |
| Skirmisher | Speed +1, Dodge +1, Accuracy +1, Resist −1 | 65% | −0.5 |
| Ambusher | Reflex +3, Accuracy +1, Parry −1, Dodge −1 | 66% | −0.9 |

Rough per-stat values, backed out of the rows above:

| Stat | Worth (Health per enemy) |
|---|---|
| Resist +1 | ~3-5 |
| Damage +1 | ~2.4 |
| Parry/Dodge +1 | ~1.9 |
| Accuracy +1 | ~0.5 |
| Reflex +3 | ~0.5 |
| Vital and Mental | about 0 |

Resist is by far the biggest lever, for the same reason fights ran long
earlier: at Level 2, Resist already eats most of each hit, so one more
point takes a large share of what's left.

Caveats:

- **Vital/Mental** read as 0 only because the sample parties barely
  attack them. Nothing targets Vital, and only Browndog's Challenge
  targets Mental.
- **Speed** is undersold. The 20m arena leaves most enemies in reach
  already, and Dodge +1 only helps an enemy whose Dodge is its better
  defense.
- **Defender and Backup (Resist)** run past the +4 Health end of the
  ladder, so their prices are extrapolated.
- **Resist's price** depends on the PC damage baseline. It will move if
  the +1-to-all-weapons change goes in.

**Round 2, revised set** (`archetype_compare.py 400 --revised`). Plain
enemies and the Health ladder reproduced within about 1 point of round
1.

| Archetype | Adds | Health left | Worth | Rounds (typical) |
|---|---|---|---|---|
| Defender (shield) | Parry +2, Dodge +2 | 36.5% | +4.8 (just past the ladder) | 7-14 |
| Backup (Resist) | Resist +1, Vital +1, Mental +1 | 42.0% | +3.5 | 6-14 |
| Bruiser | Damage +1, Resist +1, Parry −1, Dodge −1 | 42.5% | +3.4 | 5-10 |
| Striker | Accuracy +1, Damage +1 | 45.1% | +2.7 | 4.5-8.5 |
| Backup (+Accuracy) | Parry +1, Dodge +1, Vital +1, Mental +1, Accuracy +1 | 45.7% | +2.6 | 5.5-11.5 |
| Skirmisher | Speed +1, Dodge +1, Accuracy +1 | 50.0% | +1.7 | 5-9 |
| Strategist (Dodge) | Accuracy +1, Dodge +1, Mental +1 | 52.5% | +1.4 | 5-9 |

The spread narrowed from −0.9 to +6.8 down to +1.4 to +4.8. The
second point of Parry/Dodge is worth more than the first: +1 was about
1.9 Health, +2 is about 4.8. Each point cuts a bigger share of the hits
still landing.

Skirmisher and Strategist sit low for the reasons in the caveats above
(Speed, Mental and Vital are barely exercised). They shouldn't be buffed
off this number alone.

Defensive archetypes (Defender, Backup with Resist) stretch fights well
past the 5-round target. Offensive ones hold or shorten them. That's
worth a GM note: a room full of Defenders makes a slog, not just a
harder fight.

**Round 3, with Party D and the new mixes** (`archetype_compare.py 300
--revised`, parties A, B and D against Frontline, Shield Wall, Warband
and Horde).

Party D (Browndog, Hanforth with Reckoning, Felix as a Shugen monk,
Beornhard splitting War Magic between Dodge and Vital) makes about 8 of
its ~35 attacks per fight against Vital or Mental, so those Defenses
count for something now. Plain enemies leave the party 71% of its Health
on average. That's higher than rounds 1-2, because the new mixes are
easier (see below).

| Archetype | Worth, round 3 | Round 2 (parties A and B only) |
|---|---|---|
| Bruiser | +4.4 | +3.4 |
| Striker | +3.7 | +2.7 |
| Backup (Resist) | +3.5 | +3.5 |
| Defender (shield) | +3.3 | +4.8 |
| Backup (+Accuracy) | +2.7 | +2.6 |
| Skirmisher | +2.3 | +1.7 |
| Strategist (Dodge) | +1.9 | +1.4 |

The spread is now +1.9 to +4.4. Defender dropped, because many of Party
D's attacks skip Parry/Dodge entirely. The offensive archetypes rose,
because extra damage matters more against the softer new mixes.

The defensive archetypes still stretch fights the most: Party D against
Warband and Shield Wall runs 12-19 rounds with Defender or Backup
(Resist).

**The new mixes aren't even with each other.** Shield Wall (two Hedge
Knights in free Heavy Armor plus two archers) beats party A about 78% of
the time. Frontline, Warband and Horde are 95-100% party wins in 3-5
rounds. It's armor again: Shield Wall is the only mix with Physical
Resist 5 enemies. Applying the hand-build's loadout costs to the roster
(Heavy Armor only at Level 3+, Medium Armor for a pick) is the obvious
next lever.

### Armor costs and Health by Level (2026-09-30)

Enemies now pay for armor:
- **Heavy Armor:** Level 3+ only, 10 ability points.
- **Medium Armor:** traded for 2 Health until ability values settle.
  It keeps the live penalties (−1 Dodge, no Speed penalty), same as
  players.

That took Shield Wall from a wall (party A: 22%) to a hard fight (81%
at Health 10). With less armor around, Level 2 fights at Health 10 ended
in 3-4 rounds, so enemy Health became a per-Level table,
`ENEMY_HEALTH_BY_LEVEL`:

| Level | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Health | 10 | 12 | 14 (penciled) | 16 (penciled) | 18 (penciled) |

`level_baseline.py 300` results, every party against every current mix:

- **Level 1 at 10:** Frontline, Warband and Horde are 85-100% wins in
  3.5-7 rounds, and the party keeps 74-89% of its Health. Shield Wall is
  61-91% wins in 6-14 rounds. At 8, everything is shorter (about 3-5
  rounds) and easier, so 10 stays.
- **Level 2 at 12:** Frontline and Warband are 94-100% wins in about
  4-7 rounds. Horde is 100% in 3.4-4.6. Party Health left is 63-88%.
  Shield Wall is 66% (party A) to 96% in 5-10 rounds, keeping 49-86%.
- **What's still off:** outside Shield Wall, fights are about the right
  length, but the party barely spends resources. Enemies only get 5-12
  attacks off per fight. Horde's 4-Health minions mostly die before
  swinging, and Aimed Shot casters attack once a turn. The next lever is
  enemy offense in the softer mixes, not more Health.

**Enemy damage +1 test** (`level_baseline.py 300 --enemy-damage 1
--current-only`, Health 10/12). Wins, then party Health left on a win,
without → with the +1:

| Level 2 mix | Wins | Party Health left |
|---|---|---|
| Frontline | 94-99% → 81-92% | 63-74% → 51-65% |
| Warband | 96-100% → 88-97% | 68-88% → 59-85% |
| Horde | 100% → 96-100% | 83-87% → 77-81% |
| Shield Wall | 66-96% → 40-84% | 49-86% → 42-75% |

Rounds barely moved (about 4-6, Shield Wall 6-10).

- **At Level 2** it puts Frontline and Warband about where the designer
  wants them: most fights won, and the party spends a real share of
  its Health.
- **Shield Wall gets too hard** for the all-weapon party A (40%).
- **Horde stays easy**, because its minions still die before they
  swing.
- **At Level 1** it's too much. Party D wins Frontline 59%, and Shield
  Wall drops to 33-78%.

This points at a per-Level damage bonus (0 at Level 1, +1 at Level 2),
the same "low early" shape as Health. Not applied yet.

### Fighting Styles off, and the Defense lag test (2026-09-30)

Per the designer, Fighting Styles are off for now
(`sample_enemies.FIGHTING_STYLES_ENABLED`). They were meant to stop fights
being piles of double attacks, but the baseline needs more enemy offense,
not less. Guarded on a stand-still tank was also the uncosted combination
behind Shield Wall. With Guarded's stand-still bonus switched off, party
A's Shield Wall win rate went from 64% to 98%. The other pieces mattered
much less (archers' Aimed Shot/targeting 92%, shield 89%, Durable 87%,
Light Armor 81%).

**Why a Level 2 enemy has Parry 18:** enemy Stats run one Level behind a
PC's, but Skill tiers don't. A Level 2 enemy's Primary Defense matches a
Level 2 PC specialist's: Hedge Knight Parry 18 = Browndog's Agility 4 +
Melee 4 + Shield 2. `ENEMY_DEFENSE_LAG = 1` puts Defenses one Level
behind too (Hedge Knight Parry 16). Accuracy stays on-Level either way.

`level_baseline.py 300 --current-only`, Fighting Styles off, Health
10/12:

| Level 2 mix | Styles off | Styles off + Defense lag |
|---|---|---|
| Frontline | 88-97% wins, 4.0-5.2 rounds, 51-68% Health left | 97-100%, 3.0-4.1 rounds, 56-73% |
| Warband | 96-100%, 4.5-5.6 rounds, 59-85% | 100%, 3.4-4.2 rounds, 70-88% |
| Horde | 100%, 3.4-4.7 rounds, 82-88% | 100%, 3.0-3.9 rounds, 86-91% |
| Shield Wall | 68-87%, 5.3-7.3 rounds, 37-71% | 93-99%, 3.7-4.9 rounds, 50-79% |

**Level 1, styles off:** 70-100% wins in 3.5-8 rounds. Party D (Level 1
Felix is a fresh, thin build) is the one that struggles, at 70-76%
against Frontline and Shield Wall.

- **Styles off alone** lands Frontline and Warband near the target
  (most fights won, about 5 rounds, real Health spent). It brings Shield
  Wall back from 40% to 68% for party A. Enemies get more attacks off
  (Frontline 11-18 a fight, up from 7-13).
- **Adding the Defense lag** makes everything too short and too easy.
  It stays off.
- **Horde is still easy.** Its minions die before they swing, which
  needs a structural fix rather than a stat change.
- **Enemy damage +1** was tested before styles came off. With styles
  off it's likely no longer needed; it stays off.

### Pricing an ability pick, and archetypes with styles off (2026-10-01)

`ability_compare.py 300` and `archetype_compare.py 300 --revised`, both
on the same scale: Level 2, Fighting Styles off, parties A, B and D
against Frontline, Shield Wall and Warband (Horde left out until the
baseline settles). The added pick or archetype goes on every enemy, and
"worth" is read off a −2/+2/+4/+6 Health ladder. Enhanced Health (+3
Health) reads +3.1, so the scale checks out.

| One ability pick | Worth (Health per enemy) |
|---|---|
| Enhanced Health (+3) | +3.1 |
| Heavy Weapon | +1.9 |
| Durable | +1.6 |
| Poison (Bleeding) | +1.3 |
| Medium Armor (one step from Light) | +1.1 |
| Strike (Crippling) | +1.0 |
| Strike (Frightening) | +0.7 |
| Strike (Vulnerable) | +0.5 |
| Strike (Slowing) | +0.3 |
| Strike (Taunting) | +0.2 |

| Archetype | Styles off | Styles on (round 3) |
|---|---|---|
| Bruiser | +6.8 | +4.4 |
| Striker | +6.5 | +3.7 |
| Backup (Resist) | +4.1 | +3.5 |
| Defender (shield) | +4.0 | +3.3 |
| Backup (+Accuracy) | +3.7 | +2.7 |
| Skirmisher | +2.8 | +2.3 |
| Strategist (Dodge) | +2.6 | +1.9 |

- **Picks are cheap and uneven.** Most on-hit riders are worth well
  under 1 Health. The sim's PCs shrug off Slowed and Taunted, so those
  may be undersold. Enhanced Health is worth three riders.
- **The roster overcharges Medium Armor.** It's worth about 1.1, but the
  roster trades it for 2 Health.
- **Archetypes are worth 3-7 picks each**, and offense got much more
  valuable with styles off: Striker and Bruiser nearly doubled, since
  every enemy now attacks twice a turn.
- **What it means for the budget:** the current target is hit at
  baseline + about one pick (~1 Health). An archetype plus two more
  picks would add roughly +4 to +9.

### Draft: the ability catalog at 1 pick = 1 Health (2026-10-01)

**Status: draft for the designer to review.** The spreadsheet charged a
flat 5 points (one pick) for almost everything, and 10 for Omniguard,
Strike (Cleaving) and Resilient. Here each ability is re-costed in
picks, where one pick is worth about 1 Health per enemy on the
`ability_compare.py` scale (Level 2, Fighting Styles off). "Measured"
rows come from that test. "Estimate" rows aren't modeled in the sim
yet and are reasoned from the nearest measured thing; test before
trusting them.

**Rules behind the costs** (the designer's: an overall gain costs a
pick, a trade is a free choice):
- A pick's worth is about 1 Health. Anything worth well under that gets
  more stacks rather than a fractional cost, so every pick is a whole
  number.
- Leftover picks can always go to +1 Health each (Enhanced Health,
  re-scaled).
- Trades and reflavors (choosing the element of a spell) cost nothing.

| Ability | Spreadsheet | Measured / estimate | Draft cost | Draft change |
|---|---|---|---|---|
| **On-hit riders** | | | | |
| Strike (Crippling) | 5 | 1.0 measured | 1 pick | — |
| Poison (Bleeding), 2 stacks | 5 | 1.3 measured | 1 pick | — |
| Strike (Vulnerable) | 5 | 0.5 measured | 1 pick | 2 stacks instead of 1 |
| Strike (Slowing) | 5 | 0.3 measured | 1 pick | 2 stacks; Slowed is likely undersold, since sim PCs barely move |
| Strike (Frightening) | new in sim | 0.7 measured | 1 pick | — |
| Strike (Taunting) | new in sim | 0.2 measured | 1 pick | 2 stacks; Taunted is likely undersold, same reason |
| Strike (Necrotic), Poison (Crippling/Necrotic/Slowing/Vulnerable) | 5 | estimate, like the riders above | 1 pick | same stack rules as the matching Strike |
| Strike (Harrying) | 5 | estimate ~1 | 1 pick | — |
| Strike (Battering) | 5 | estimate ~1 | 1 pick | — |
| Strike (Grappling) | 5 | estimate 1-2, positional | 1 pick | test later |
| Strike (Devastating) | 5 | estimate ~2 (+1 damage, as Bleeding) | 2 picks | — |
| Strike (Cleaving) | 10 | estimate ~2 | 2 picks | — |
| **Defense and durability** | | | | |
| Enhanced Health | 5 (+3 Health) | 3.1 measured | 1 pick | **+1 Health per pick** (any number of times) |
| Durable | 5 | 1.6 measured | 2 picks | — |
| Medium Armor (from Light) | separate armor pick | 1.1 measured | 1 pick | replaces the roster's 2-Health trade |
| Heavy Armor (from Light) | separate armor pick | estimate ~2 (two steps, Speed −1) | 2 picks, Level 3+ | — |
| Resist (one element, +2) | 5 | estimate ~1; Resist +1 to all is worth ~4 | 1 pick | — |
| Attunement (+4 one element, −1 opposite) | 5 | estimate 1-2 | 1 pick | — |
| Omniguard (ignore Harried) | 10 | estimate ~2; every PC weapon attack Harries | 2 picks | — |
| Resilient (shed 1 of each debuff a turn) | 10 | estimate ~2 | 2 picks | — |
| Retribution Aura | 5 | estimate ~1 | 1 pick | — |
| Sturdy | 5 | estimate under 1, niche | 1 pick | — |
| **Offense** | | | | |
| Heavy Weapon (was Powerful Weapon) | 5 | 1.9 measured | 2 picks | renamed |
| Powerful Spell (+1 damage, no Parry) | 5 | estimate ~2.5; casters rarely Parry | 2 picks | — |
| Elemental Spell | 5 | a reflavor | free | — |
| Elemental Weapon (−1 damage) | 5 | a trade | free | — |
| Enhanced Range | 5 | estimate ~1 | 1 pick | — |
| Improved Support (+50% heals/Protected) | 5 | estimate 1-2 | 1 pick | test with a support enemy |
| **Movement and timing** | | | | |
| Enhanced Speed (+1) | 5 | estimate under 1 (Skirmisher's Speed barely registered) | 1 pick | — |
| Enhanced Reflexes (+3) | 5 | ~0.5 (from the Ambusher test) | 1 pick | — |
| Shadow Jaunt | 5 | estimate ~1, positional | 1 pick | — |
| Action (Parting Shot) | 5 | estimate ~1 | 1 pick | — |
| Action (Intimidating / Taunting), 0 AP at range | 5 | estimate ~1; no hit needed | 1 pick | — |

The main Actions stay free picks, as they were on the spreadsheet: the
attacks, Curse/Hex, Great Heal, Shield Ally and Shielding Nova.

**Archetypes in the same currency.** Measured with styles off, they're
worth 2.6-6.8 picks. The draft evens them at about 3-4 each. The two
offensive ones keep their Damage +1 but lose the extra freebie riding
on it (Striker's Accuracy, Bruiser's Resist):

| Archetype | Draft | Measured worth (current version) |
|---|---|---|
| Defender | Parry +2, Dodge +2 | 4.0 |
| Backup | Resist +1, Vital +1, Mental +1 | 4.1 |
| Striker | Damage +1 (drops Accuracy +1) | 6.5 with Accuracy; untested without |
| Bruiser | Damage +1, Parry −1, Dodge −1 (drops Resist +1) | 6.8 with Resist; untested without |
| Skirmisher | Speed +1, Dodge +1, Accuracy +1 | 2.8 |
| Strategist | Accuracy +1, Dodge +1, Mental +1 | 2.6 |

**What the baseline gives up.** Today's target is hit at baseline + 1
pick, with no archetype. The spreadsheet's structure (an archetype worth
~3.5, plus 3 picks at Level 2) adds ~5.5 Health-worth per enemy on top
of that. Two ways to make room:
- **Keep the spreadsheet's pick counts (2/3/4/5/8)** and trim the
  baseline by ~5.5 Health-worth at Level 2. Health alone would mean 12
  → ~7, which undoes the padding, so a mix is likelier: Health 12 → 9
  and every Defense −1.
- **Keep this baseline** and cut the allotment to the archetype plus 1
  pick at Level 2. That's the smallest change, but it leaves little
  room for variety.

### The roster under the draft rules (2026-10-01)

Option 1 applied: baseline Health 7/9/11/13/15, every Defense −1, the
draft archetypes on every enemy, abilities and armor bought with picks
(2/3/4/5/8 per slot) at the draft costs, and leftover picks as +1 Health
each. Melee enemies swing a light one-hander. Defender stands in for a
shield and Bruiser for a two-hander, and Heavy Weapon is a 2-pick buy.

At Level 2, per enemy:

| Enemy | Archetype | Picks |
|---|---|---|
| Hedge Knight | Defender | Medium Armor, Taunting, +1 Health |
| Brute | Bruiser | Heavy Weapon, Crippling |
| Warpriest | Backup | Medium Armor, Frightening, +1 Health |
| Marsh Archer | Striker | Vulnerable, +2 Health |
| Footpad | Skirmisher | Bleeding, +2 Health |
| Grave Caller, Ember Caster | Striker | Vulnerable, +2 Health |
| Bog Hexer | Strategist | +3 Health |
| Goblin | Striker, 2 picks | Slowing, +1 Health |

`level_baseline.py 300 --current-only` (Fighting Styles off), against
the styles-off baseline from before the draft:

| Level 2 mix | Before the draft | Draft rules |
|---|---|---|
| Frontline | 88-97% wins, 4.0-5.2 rounds, 51-68% Health left | 83-90%, 3.5-4.6 rounds, 52-62% |
| Warband | 96-100%, 4.5-5.6 rounds, 59-85% | 94-97%, 4.7-5.9 rounds, 58-84% |
| Shield Wall | 68-87%, 5.3-7.3 rounds, 37-71% | 38-87%, 5.0-5.5 rounds, 35-65% |
| Horde | 100%, 3.4-4.7 rounds, 82-88% | 99-100%, 3.3-4.5 rounds, 81-84% |

**Level 1 (Health 7):** Frontline and Warband are 79-100% wins but
short, at 2.5-4.9 rounds. Shield Wall is 71-92% in 4.4-6 rounds.

- **The conversion mostly holds.** Frontline and Warband land about
  where they were, so baseline − (Health 3 + Defense 1) + archetype +
  full picks comes out close to the old balance point.
- **Shield Wall got harder for the weapon parties** (party A 38%, B
  65%). The Hedge Knights still reach Parry 18, and the archers now hit
  harder (Striker +1 Damage, 2 stacks of Vulnerable).
- **Level 1 fights are on the short side** at Health 7. The Level 1 trim
  may want to be smaller than Level 2's.

**Follow-up: Defender variants and Level 1 Health** (`level_baseline.py
300 --current-only --defender ... --health 1:N`).

Shield Wall at Level 2, party wins A / B / C / D:

| Defender | A | B | C | D |
|---|---|---|---|---|
| Draft (Parry/Dodge +2) | 38% | 65% | 87% | 76% |
| Parry +2 only | 40% | 72% | 89% | 83% |
| Tank (Parry/Dodge +1, Resist +1) | 30% | 58% | 71% | 64% |

Level 1, enemy Health:
- **7:** fights run 2.5-4.9 rounds.
- **8:** 69-100% wins in 2.8-6.4 rounds.
- **9:** party D drops to 57-62% against Frontline and Shield Wall.

Applied: **Defender = Parry +2** (a shield's own numbers) and **Level 1
Health 8**. The Defender barely moves Shield Wall. Its difficulty for
party A is the matchup: an all-weapon party into Parry 18 and Medium
Armor, while two Striker archers hit back. The archers' Vulnerable is
wasted there, since nothing in the mix attacks Vital or Mental. Open
question: accept Shield Wall as the hard counter to a weapon party, or
make its archers Skirmishers.

**Shield Wall is staying as a counter-fight** (designer, 2026-10-01). At
Level 2, every party with any elemental damage wins it most of the time:

| Party | Elemental damage | Shield Wall wins |
|---|---|---|
| B | Wren's Fire War Magic, Jackal's Bottled Fire | 72% |
| C | Beornhard's Fire War Magic | 89% |
| D | Beornhard's Fire, Felix's Brilliant strikes | 83% |
| A | none (all weapons) | 40% |

A fight that counters a lopsided party is fine and encourages variety,
so the sim shouldn't tune around party A's result. The way to cover this
in the sim is to model weapon-based elemental options (elemental
strikes and the like) when they come up, not to soften the mix.


### Horde and the minion Health ratio (2026-10-01)

`horde_ratio.py 300`: Horde (4 Goblin minions, an Ember Caster, a Bog
Hexer) at Levels 1-2, all four parties, with half-slot minions at 1/3,
0.4 or 1/2 of a full enemy's Health. Under the draft rules a Level 2
minion comes to 4 / 5 / 6 Health.

| Level 2 Horde | 1/3 (Health 4) | 0.4 (Health 5) | 1/2 (Health 6) |
|---|---|---|---|
| Party wins | 98-100% | 98-100% | 96-100% |
| Rounds | 3.3-4.4 | 3.8-5.2 | 4.2-5.4 |
| Party Health left | 81-84% | 76-85% | 70-79% |
| Minion attacks per fight (all four) | 0.7-2.3 | 1.2-3.3 | 2.0-4.0 |

The minion attack counts are the real finding. Goblins average 2-5 move
actions per fight between them, so most die in their first turn or two,
often before reaching anyone. Almost any PC hit kills a 4-Health minion,
and the party gets free shots while they close in. At 1/3, twice the
bodies buys almost no extra actions, which is what the slot rule is
supposed to pay for. Switching them from Assassin to nearest-target
targeting helped only a little (party D: 2.0 → 4.1 attacks).

**Applied: half-slot minions at 1/2 Health** (`tunables.SLOT_MULTIPLIER`),
the top of the designer's 1/3-1/2 range. Minion attacks roughly double,
and fights run about a round longer and cost more, but Horde stays
easy. What's left is structural: the minions still drop before acting,
and the Hexer doesn't attack, so most of Horde's damage comes from one
caster. Candidates to test: start the minions closer (an ambush), or
swap the Hexer for a second damage caster.

**Horde experiments** (`horde_experiments.py 300`, Level 2, all four
parties). Wins, rounds, and party Health left on a win:

| Variant | Wins | Rounds | Health left |
|---|---|---|---|
| Horde as is (minions at 1/2) | 97-99% | 4.1-5.6 | 71-78% |
| Horde, minions ambush | 93-98% | 4.3-5.7 | 65-71% |
| Horde, 2nd Ember Caster for the Hexer | 79-92% | 4.0-5.5 | 46-61% |
| Horde, 2nd caster + ambush | 67-83% | 3.9-5.5 | 46-50% |
| Shield Wall | 36-89% | 4.6-5.3 | 34-66% |
| Shield Wall, minion version (1/2) | 0-28% | 3.3-4.9 | 21-50% |
| Shield Wall, minion version (1/3) | 15-54% | 3.6-4.7 | 28-50% |
| Frontline | 82-93% | 3.4-4.7 | 53-60% |
| Frontline, minion version (1/2) | 5-29% | 3.5-4.9 | 27-43% |
| Frontline, minion version (1/3) | 57-75% | 3.2-4.1 | 45-51% |

A "minion version" splits every enemy into two half-slot copies of
itself: same stats and archetype, half-slot Health and picks.

- **The controlled test reverses the earlier read.** Split into
  minions, real enemies get much harder. At 1/2 Health, Frontline drops
  from 82-93% party wins to 5-29%. Even at 1/3, both mixes are harder as
  minions than as full enemies. Twice the bodies means twice the
  attacks at full damage, and a minion with real Resist (a Hedge
  Knight's Medium Armor) doesn't die to one hit.
- **So Horde's goblins were weak for their own reasons**, not because
  of the slot rule: Light Armor, Resist 1-2, and a Hexer that doesn't
  attack. Half-slot picks also round up (2 picks each at Level 2, so 4
  per slot against a full enemy's 3), which makes minions a little more
  generous still.
- **The Horde fix is composition.** Swapping the Hexer for a second
  Ember Caster puts it on target: 79-92% wins in 4-5.5 rounds, with the
  party keeping about half its Health. The ambush start adds a little
  on top; it's a GM tool, not a default.

**Round 2 of the Horde experiments** (after the designer's go-ahead):
minions back at 1/3 Health, half-slot picks rounded down (1 pick at
Level 2), and Horde's Hexer swapped for a second Ember Caster.

| Variant (Level 2) | Wins | Rounds | Health left |
|---|---|---|---|
| Horde (2 casters) | 90-99% | 3.0-4.2 | 60-73% |
| Horde, minions ambush | 83-96% | 2.7-4.5 | 56-66% |
| Frontline | 82-92% | 3.5-4.5 | 52-60% |
| Frontline, minion version | 73-90% | 3.0-4.2 | 53-60% |
| Shield Wall | 38-89% | 4.6-5.5 | 34-66% |
| Shield Wall, minion version | 23-64% | 3.6-4.5 | 33-53% |

- **Melee minions are now about even with the enemy they replace.**
  Frontline split into minions lands within a few points of full
  Frontline.
- **Ranged minions are still stronger.** Shield Wall's split doubles
  the archers. Halving a back-line shooter's Health matters less than
  doubling its shots, because the party has to walk past the front line
  to reach it. GM rule of thumb: minions work best as front-line fodder,
  and a pack of minion archers is a hard fight.
- **The 1/4 bracket was a no-op at Level 2.** 9 × 1/4 rounds up to 3,
  the same as 9 × 1/3, so those rows only show run-to-run noise.
- **Horde is easier than Frontline but in range.** Most fights won,
  with the party spending about a third of its Health, but the fights
  are short, at 3-4 rounds.

**Goblins with Medium Armor: tested and reverted** (`goblin_armor.py
300`). At Levels 1-2 a goblin's one pick would buy Medium Armor in
place of Strike (Slowing). Horde before → after:

| Level | Wins | Party Health left | Goblin attacks per fight (all four) |
|---|---|---|---|
| 1 | 81-100% → 90-100% | 65-74% → 61-73% | 0.8-2.3 → 0.8-2.8 |
| 2 | 89-99% → 91-99% | 59-73% → 60-74% | 0.6-2.1 → 0.6-2.1 |

There was no consistent effect, just a few points either way by party.

- **One hit still kills.** A 3-Health goblin dies to nearly every hit.
  The extra point of Resist only saves it from the weakest physical
  hits (Sable's 5-damage bow now leaves it at 1 Health).
- **Elemental hits ignore armor anyway.**
- **Level 1 Felix's 4-damage punches got worse** against them, which is
  why party D dipped.

It also cost the goblins their Slowing, against the "every enemy puts
something on the fight" standard, so the roster keeps Light Armor +
Slowing.

Horde as it stands: 89-99% party wins, the party spends about a third
of its Health, and fights run 3-4 rounds. The goblins work as a speed
bump that soaks the party's attacks for a round or two while the casters
fire. A minion that survives a hit would need about 6 Health at Level 2,
the 1/2 ratio, which made minion versions of normal enemies far too
strong. If the designer wants sturdier fodder, it likely needs its own
minion trade-off (more Health, weaker attack), not more armor.

### Baseline + Upgrades (2026-10-01)

Per the designer: a bare baseline plus an allotment of **Upgrades**,
where +1 Health is one Upgrade among the rest. Upgrades climb faster
than baseline Health, so higher Levels get more room to customize and
stack effects:

| Level | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Baseline Health | 6 | 6 | 7 | 8 | 9 |
| Upgrades | 4 | 6 | 8 | 10 | 14 |

Each Level's baseline + Upgrades matches the earlier baseline + picks,
so all 45 roster enemies build identically. Minions get a third of the
Upgrades, rounded up like their Health. At these numbers a pair of
minions still gets fewer than the one enemy they stand in for (Level 2:
2 × 2 = 4 against 6). The `level_baseline.py` rerun matched the
previous baseline within noise. Levels 3-5 are penciled.

**Does the model hold?** `upgrade_configs.py 200`: every full-size
enemy in Frontline, Shield Wall and Warband gets the same Level 2
loadout (6 Upgrades, archetype and Action kept), against parties A-D.
Each result is read against all-Health on a ±2 Health scale (1 enemy
Health ≈ 3.9 points of party Health here; noise about ±0.3):

| Loadout | vs all-Health | Rounds |
|---|---|---|
| Roster (each enemy's own role-fitted picks) | +1.5 stronger | 3.4-6.2 |
| Heavy hitter (Heavy Weapon / Powerful Spell, +4 Health) | +0.1 | 3.4-5.4 |
| Turtle (Medium Armor, Durable, +3 Health) | −0.2 | 3.5-6.6 |
| Rider stack (4 riders, +2 Health) | −0.4 | 2.7-5.2 |
| Glass cannon (offense buy + 4 riders, no extra Health) | −1.8 weaker | 2.3-4.1 |

- **Generic loadouts come out even,** so the costs are about right.
  Stacked riders don't snowball.
- **Glass cannon is weaker than its price.** At 6 Health an enemy drops
  in one or two hits before its effects pay off; the 1:1 rate breaks
  down at the bottom of the Health range. Proposed fix: a Health floor
  of a third of the Upgrades (2 at Level 2).
- **Role-fitted loadouts run about 1.5 Health above their price**
  (Taunting on the shield tank, Medium Armor on the front line,
  Bleeding on skirmishers; most visible in Warband). That's a reward for
  building to the enemy's job, worth a GM-guide note rather than a fix.
- **Upgrades set fight length.** Offense-heavy loadouts shorten fights
  to 2-4 rounds; Health and Turtle stretch them toward 5-6.

### Codified hand-build rules (2026-10-01)

Per the designer: replace every remaining judgment call with a pick
from a list or a lookup, so the GM only decides what the enemy is and
how it spends its Upgrades. The step-by-step version is in
`GM_GUIDE_NOTES.md` ("The process"). What changed from the hand-picked
roster:

- **Attack tier:** the roster had about half its enemies at Primary,
  picked case by case. Now everyone attacks at Primary
  (`CODIFIED_ATTACK_TIER`). Secondary for everyone was tested first and
  came out softer than the hand-built roster at Level 2.
- **Defenses:** the roster spent 3 tier-steps per enemy, placed by
  hand. Now Parry is always Secondary, every other Defense is Poor, and
  one Strong Defense (Dodge, Vital, Mental or Vigilant) is Primary. It's
  the same 3 steps, but Parry sits one above Dodge (two for a melee
  weapon), so Bruiser, Heavy Weapon and Powerful Spell cost defense.
- **Damage Stat and Resist:** the roster used a hand-ordered Stat list.
  Now they come from the main Action's type: weapon (High damage, Low
  Resist), spell or Hex (High, Mid), support (Mid, High). Any Action
  works with any archetype.

`level_baseline.py 300 --current-only`, Level 2 party wins:

| Mix | Hand-picked roster | Codified, Attack at Secondary | Codified, Attack at Primary (adopted) |
|---|---|---|---|
| Frontline | 81-91% | 89-97% | 82-91% |
| Warband | 93-97% | 94-99% | 94-99% |
| Horde | 91-98% | 89-100% | 78-97% |
| Shield Wall | 43-91% | 85-98% | 72-93% |

With Attack at Primary, the codified rules land on the hand-built
numbers. The exception is Shield Wall, which is now a milder counter to
the all-weapon party (72% against 43%): the codified Hedge Knight has 1
less Parry and Resist than the hand-picked one. A GM who wants the old
wall can spend Upgrades on Durable or a second rider.

### Base stats against the measured party (2026-11-02)

Per the designer: Slots stay as they are (count the players, pick
enemies adding up to that many Slots), so if on-level fights are off,
the per-Level baseline is what moves. A broad first pass, nothing
changed yet. `experiments/enemies/stat_sweep.py` nudges every built
enemy's numbers by Level (or one enemy's, `3@Brute:`) and plays the day
standard (two fights, care between) against the measured on-level
parties: Level 1 the six sample parties at 75 XP, Levels 2-3 eight
normalized parties (105 / 145 combat XP) spread over party_mixes'
ranking, 400 days each. Readings are in `results/enemy_stats/`. The
targets are the 2026-10-08 ones (TABLE_PLAY_NOTES.md): about three
rounds, the party basically never loses, someone Down less than once in
three fights, someone Wounded about every other fight, a hit enemy acts
again about half the time. "F1" below is the day's first fight, fresh.

**Where it stands.** Level 1 and 2 are close; Level 3 isn't.

| Level | Days won | F1 lost | F1 Down | F1 Wounded | Rounds | Acts again |
|---|---|---|---|---|---|---|
| 1 | 94% | 0.3% | 20% | 58% | 2.9 | 23% |
| 2 | 91% | 0.9% | 24% | 59% | 3.1 | 25% |
| 3 | 65% | 5.7% | 49% | 79% | 3.3 | 33% |

**Why Level 3.** The measured party barely gets tougher from Level 1 to
3 (Level 1 is the sample builds, 2-3 the normalized ones): average
Physical Resist 3.3 / 4.4 / 4.3, Health 10.0 / 10.5 / 10.9, the main
Defenses up about 1 a Level. Enemies gain +1 Accuracy, +1 every
Defense, +1 Damage (the damage Stat's step in the lagged spread), +1
Resist on about half the roster and 2-3 Health, every Level. The
party's offense keeps up with the enemy's defense; its defense doesn't
keep up with the enemy's offense.

**One stat at a time** (every Level, days won):

| | L1 | L2 | L3 |
|---|---|---|---|
| as is | 94 | 91 | 65 |
| Damage −1 / +1 | 100 / 78 | 99 / 75 | 83 / 42 |
| Resist −1 / +1 | 98 / 83 | 95 / 82 | 74 / 48 |
| Health −2 / +2 | 98 / 85 | 96 / 84 | 75 / 51 |
| Accuracy −1 / +1 | 98 / 91 | 95 / 87 | 73 / 55 |
| Defense −1 / +1 | 97 / 91 | 94 / 88 | 68 / 59 |
| Hex / Shield stacks −1 | 95 | 92 | 65 |

Damage moves the most; it also moves Down and Wounded the most. Health
is the only knob that moves fight length and "acts again" (+2 Health:
+0.5 rounds, +10 points of acts again), and it costs survival.

**Matching the feel per Level.** From a grid of Damage × Health ×
Accuracy, the same table feel needs about 1 less enemy Damage at Level 2
and 2 less at Level 3: enemy Damage flat from Level 1 to 3, the way the
party's Resist and Health are. Two families:

| Table | Level | Days won | F1 Down | F1 Wounded | Rounds | Acts again |
|---|---|---|---|---|---|---|
| A: Damage −1 at L2, −2 at L3 | 2 | 99% | 8% | 38% | 3.0 | 25% |
| | 3 | 97% | 13% | 50% | 3.0 | 31% |
| C: A, plus +4 Health per Slot and −1 Accuracy at every Level (L1 also −1 Damage) | 1 | 96% | 15% | 51% | 4.0 | 43% |
| | 2 | 97% | 13% | 47% | 3.9 | 41% |
| | 3 | 91% | 19% | 57% | 3.9 | 46% |
| E: −1 Accuracy and Defense from L2 up, −1 Damage from L3 up, Grave Caller −1 Damage | 2 | 98% | 14% | 47% | 2.9 | 23% |
| | 3 | 93% | 19% | 58% | 3.0 | 30% |

"About three rounds" and "acts again about half the time" pull against
each other: acts again only climbs with enemy Health, and the Health
that gets it to 45% makes fights about four rounds.

**One and two Levels up.** Every table above makes the next Level a
cliff. Days won with enemies one Level up / two up:

| Table | L1 | L2 | L3 |
|---|---|---|---|
| as is | 8 / 0 | 14 / 0 | 7 / 0 |
| A | 29 / 0 | 73 / 5 | 54 / 0 |
| C | 7 / 0 | 48 / 1 | 32 / 0 |
| E | 27 / 0 | 62 / 4 | 44 / 0 |

(For Level 3's rungs, Levels 4-5 took Level 3's nudges.) Taking parts of
the Level 2→3 step off one at a time, under A, Level 2 parties: days
won one up goes 73% → Resist −1 89%, Health −3 89%, Defense −1 82%,
Accuracy −1 81%. Level 1→2 is the steepest:
`SKILL_TOTAL_BY_LEVEL` steps +2 there (4/5/6 → 6/7/8) and +1 after.

**Mixes and archetypes.** Fresh first fights at Level 3 under A:
Frontline (two Brutes, two Grave Callers) Down 31%, Horde 14%, Shield
Wall 7%, Warband 2%. Frontline's danger is the Grave Caller: −1 Damage
on it alone takes Frontline to 5% Down (the Brute alone, 16%). Its
Vital Spell goes after Vital Defense with Shadow damage, and the party's
Vital Defense and elemental Resist (about 3, against 4.4 Physical) are
its weakest numbers, so a spell at the same Damage hits more often and
harder than a weapon. Horde's acts again sits at 10-19% at every Level:
its minions drop to one hit. Warband is mild because its Warpriest
spends turns Protecting rather than attacking.

**Open for the designer.** Which damage curve (A's flat Damage, or E's
smoothed Skill step plus a smaller Damage cut); whether fights should
run three rounds or four (acts again); how steep one enemy Level should
be (now it's a cliff in every table); and whether spells aimed at Vital
or Mental need a price or a damage trade.

### Draft base table v2 (2026-11-02)

Per the designer: land structurally on the original table (one row per
Level, everything read off it), roughly following a PC's progression
with some abstraction, ratcheting up where the party needs a challenge;
by Level 5 some archetypes reach the PC caps (+10 to an attack or
Defense Skill Total, 5 in a damage or Resist Stat), since they're
facing PCs at about 275 XP. Level N enemies are for PCs within 25 XP of
that Level's schedule (Level 1: 75-100, Level 2: 100-150, Level 3:
150-200, and so on), so a party at the bottom of a band should feel
friction and one at the top should be comfortable. Fights should run
about 4-5 rounds on average. A party that hits a rare bad fight has its
consumables to fall back on (not modeled yet), so an occasional acute
loss is fine.

`tunables.ENEMY_TABLE = 'v2'` builds the codified rows from
`enemy_builder_pcstyle.ENEMY_TABLE_V2`; `'v1'` plays byte-identical to
before (fixed-seed calibrate and day_sim runs). v2 is the default since
later the same day (designer: "the new one we're working off of"). In
PC terms, Defense = 8 + the Skill Total:

(As first drafted; the kit pass below set the final numbers: Attack
6-10 and Health moved into Upgrades.)

| Level | Attack | Defense: Strong / Parry / other | Stat: High / Mid / Low | Damage | Health | Upgrades |
|---|---|---|---|---|---|---|
| 1 | 5 | 13 / 12 / 11 | 2 / 2 / 1 | −1 | 12 | 4 |
| 2 | 6 | 14 / 13 / 12 | 3 / 2 / 1 | −1 | 14 | 6 |
| 3 | 7 | 15 / 14 / 13 | 3 / 3 / 1 | −1 | 15 | 8 |
| 4 | 8 | 16 / 15 / 14 | 4 / 4 / 2 | −1 | 16 | 10 |
| 5 | 9 | 17 / 16 / 15 | 4 / 4 / 2 | −1 | 13 | 14 |

High/Mid/Low are the damage and Resist Stats by the main Action's
category, as before (weapon: damage High, Resist Low; spell: High, Mid;
support: Mid, High). Damage is on every damaging attack, on top of the
weapon or spell; Health is per Slot, before HealthBonus and Upgrades.
Level 5's base Health is under Level 4's on purpose: its 14 Upgrades
(against 10) keep the total climbing, and by then the party has mostly
capped out (below).

XP here is always composite, what a PC has spent on everything, the
designer's unit. A PC plays at its combat share, `combat_xp.combat_for`:
the line through the 2026-10-30 points (105 of 125, 145 of 175),
0.8 × composite + 5, about 83%. XP trickles in steadily (early on about
5 XP per adventuring day, or every other day, after a handful of fights
and other challenges), so a party spends roughly five to ten adventuring
days in each half of a band, and a few XP either way rarely shows at
the table.

How it got here, against v1 (2026-11-02 sweeps, `stat_sweep.py` with
`SIM_SET="ENEMY_TABLE='v2'"`):

- Attack and every Defense step +1 per Level (v1 jumped +2 from Level 1
  to 2, then +1); the High Stat is 1 lower at Levels 3 and 5 (v1:
  2/3/4/4/5). That alone put the middle of each band where Level 1
  already was, at about three rounds.
- For 4-5 rounds (designer), base Health about doubles (v1: 6/6/7/8/9),
  paid for with 1 less Damage and 1 less Attack at every Level. More
  Health is the only thing that lengthens fights, and each +2 Health
  per Slot cost about 4-12 points of days won at Levels 2-3 until
  Damage and Attack came down. It also brings "a hit enemy acts again" to
  about half, the other October target.
- Attacks aimed at Vital, Mental or Vigilant get no separate price
  (designer): an attack that's harder to defend against gives up about
  1 Accuracy, priced the same as one that only targets Dodge, and the
  spell Actions already pay it (Accuracy +0 and 2 + Stat, against a
  light weapon's +1 and 3 + Stat, and no Parry), like a player's War
  Magic. An earlier draft took 1 Damage off them for the Grave Caller;
  that's gone.

At Level 5, with a weapon's or archetype's +1 and gear, some enemies
reach the caps: Accuracy 10-11, a Defender's Parry 19, a Striker's or
Bruiser's damage Stat 5, a Backup's Resist Stat 5. Attack is one under
the PC progression at every Level (5 to 9, not 6 to 10); that's the
price of the longer fights.

**Across the band** (`experiments/enemies/table_check.py`; days won /
F1 Down / F1 Wounded / rounds / acts again; normalized parties at the
band's bottom, middle and top, `band_builds.py`; Level 1 is the sample
parties at 75 XP, the bottom of its band; Levels 4-5 below):

| Level | Composite XP (combat) | v1 | v2 |
|---|---|---|---|
| 1 | 75 | 94% / 20 / 58 / 2.9 / 23 | 93% / 22 / 59 / 4.7 / 53 |
| 2 | 100 (85), bottom | 45% / 59 / 85 / 4.1 / 37 | 35% / 64 / 86 / 6.7 / 65 |
| 2 | 125 (105), middle | 91% / 24 / 59 / 3.1 / 25 | 96% / 16 / 49 / 4.5 / 53 |
| 2 | 150 (125), top | 98% / 14 / 46 / 2.8 / 24 | 100% / 5 / 30 / 3.9 / 49 |
| 3 | 150 (125), bottom | 16% / 76 / 93 / 5.4 / 47 | 45% / 54 / 83 / 6.9 / 68 |
| 3 | 175 (145), middle | 65% / 49 / 79 / 3.3 / 33 | 92% / 20 / 58 / 4.3 / 55 |
| 3 | 200 (165), top | 88% / 29 / 62 / 2.9 / 27 | 100% / 5 / 27 / 3.7 / 49 |

The middle of every band lands together (92-96% of days, someone Down
in about a fifth of fresh fights, Wounded in about half, 4.3-4.7
rounds). The bottom of the band is a hard day, and harder than with
short fights: a party that's behind grinds through about seven rounds.
The top is easy. Parties at 150 XP win nearly every day against Level
2 enemies and about half against Level 3: that's the tier step.

Doubling base Health changes what an Upgrade is worth: +1 Health is
now a smaller share of an enemy's toughness, so the 1 Upgrade = 1
Health pricing of the ability catalog wants a recheck under v2.

**Levels 4-5.** No character exists past Level 3, so the same eight
parties' Level 3 exports were grown to each point by the normalizing
rule (more ranks in the attack Skill and Stat, Essence and the Defense
Skills, rank cap 5; `band_builds.GROWN_FROM`), against the Level 3
mixes built Levels higher. They keep their Level 3 Techniques, so
they're a floor on a real Level 4-5 character. Most run out of ranks
to buy at 220-245 combat XP (about 270-300 composite), the designer's
"capping out by about 275". Plain stand-ins (Stats and Skills only)
played much stronger than real parties (Level 3 middle: 100% of days
and 2% Down, against 92% and 20%), so they're no longer the check.

| Level | Composite XP (combat) | v1 | v2 |
|---|---|---|---|
| 4 | 200 (165), bottom | 34% / 62 / 87 / 4.6 / 50 | 52% / 51 / 81 / 6.4 / 70 |
| 4 | 225 (185), middle | 78% / 35 / 72 / 3.7 / 44 | 95% / 18 / 53 / 4.8 / 65 |
| 4 | 250 (205), top | 94% / 23 / 62 / 3.5 / 42 | 100% / 13 / 42 / 4.7 / 63 |
| 5 | 250 (205), bottom | 22% / 71 / 92 / 6.7 / 62 | 95% / 24 / 57 / 5.4 / 68 |
| 5 | 275 (225), middle | 26% / 67 / 91 / 6.6 / 61 | 96% / 22 / 53 / 5.3 / 67 |
| 5 | 300 (245), top | 29% / 65 / 90 / 6.4 / 61 | 97% / 21 / 51 / 5.3 / 67 |

Level 4's middle lands with the others. Level 5 needed less base Health
(17 played 6.5 rounds and 90% of days; 13 is the table's), and its band
is flat: the grown characters have capped, so the bottom and top play
alike. A real Level 5 character would have spent on Techniques instead
of ranks it can't buy, so Level 5 is the least certain row; checking it
properly needs Level 4-5 sample characters.

### The v2 kit: archetypes, Abilities and armor (2026-11-02)

Per the designer, with v2 as the new ground: a check pass over the
pieces a GM builds an enemy from, so they're in line with each other.
`experiments/enemies/kit_check.py` puts each one on every full-size
enemy in the four mixes (rebuilt through the builder, so an Ability's
Upgrades come out of the enemy's Health as on a real stat block), against
the eight normalized parties in the middle of the band at Levels 2 and 3,
fresh fights on paired seeds, about 1,900 fights a reading. The score is
party Health lost (a loss counts 100), turned into enemy Health per Slot
with the slope of "every enemy +2 Health". A Role is free, so it reads
as what it's worth; an Ability or armor pays its Upgrades in Health, so
it reads as worth minus cost and about 0 is fair. Enhanced Health (1
Upgrade for 1 Health) reads exactly 0, the sanity check. Noise is about
±0.5.

**What the first pass found, on the v2 table as drafted:**

- +1 Damage was worth 7-9 enemy Health on its own, so Striker (+1
  Damage) and Bruiser (+1 Damage, −1 Parry and Dodge) read 6-9, against
  1-2.5 for Defender, Backup, Skirmisher and Strategist. Bonuses to Vital
  and Mental were worth almost nothing: the parties rarely attack them.
  +1 Resist was worth about 3 Health and a round.
- Retribution Aura read +20-25 for 1 Upgrade. Every PC hit that damages
  the enemy gives the attacker a stack of Bleeding, and with twice the
  enemy Health there are twice the hits. On melee attackers only it
  read +2.5-4.
- Poison (Bleeding) read +9-10 for 1 Upgrade: 2 stacks a hit is about
  +2 damage past Resist, and leftover stacks tick out after the fight.
  At 1 stack it read +3.4-4.5.
- Necrotic riders and Grappling +2, Attunement +2-4, Enhanced Range
  +1-3, Medium Armor +2.4 for 1 Upgrade and Heavy +3.9 for 2, Powerful
  Spell +1-2, Heavy/Powerful Weapon +0.7-1.5. Resilient and Omniguard came out
  about −1 for their 2 Upgrades, Sturdy and Shadow Jaunt about −1 for 1.
  The plain riders (Crippling, Vulnerable, Slowing, Frightening,
  Taunting, Harrying, Battering) sat within ±0.7.

Repricing those left a Level 1 enemy with no room: 4 Upgrades and a
floor of 2 for Health. So v2 moves Health into Upgrades at the same
total (an all-Health enemy is unchanged), and the kit prices every pick
at its measured worth:

| Level | Attack | Defense: Strong / Parry / other | Stat: High / Mid / Low | Damage | Health | Upgrades |
|---|---|---|---|---|---|---|
| 1 | 6 | 13 / 12 / 11 | 2 / 2 / 1 | −1 | 8 | 8 |
| 2 | 7 | 14 / 13 / 12 | 3 / 2 / 1 | −1 | 10 | 10 |
| 3 | 8 | 15 / 14 / 13 | 3 / 3 / 1 | −1 | 11 | 12 |
| 4 | 9 | 16 / 15 / 14 | 4 / 4 / 2 | −1 | 12 | 14 |
| 5 | 10 | 17 / 16 / 15 | 4 / 4 / 2 | −1 | 11 | 16 |

| Role | v1 | v2 |
|---|---|---|
| Defender | Parry +2 | Parry +2, Resist +1 |
| Backup | Resist +1, Vital +1, Mental +1 | Resist +1, Parry +1, Dodge +1, Vital +1, Mental +1 |
| Striker | Damage +1 | Damage +1, Accuracy −2 |
| Bruiser | Damage +1, Parry −1, Dodge −1 | Damage +1, Resist +1, Accuracy −3 (see the next section) |
| Skirmisher | Speed +1, Dodge +1, Accuracy +1 | Speed +1, Dodge +2, Accuracy +1 |
| Strategist | Accuracy +1, Dodge +1, Mental +1 | Accuracy +2, Mental +1 |

| Upgrades | v1 | v2 |
|---|---|---|
| Poison (Bleeding) | 1 (2 stacks) | 5 (1 stack) |
| Retribution Aura | 1 | 4 (melee attackers only) |
| Strike/Poison (Necrotic), Strike (Grappling), Strike (Devastating) | 1, 1, 2 | 3 |
| Heavy Weapon, Powerful Weapon, Powerful Spell | 2 | 3 |
| Enhanced Range | 1 | 3 |
| Attunement (any element) | 1 | 3 |
| Resist (any element), Enhanced Reflexes | 1 | 2 |
| Durable, Omniguard, Resilient | 2 | 1 |
| Medium / Heavy Armor | 1 / 2 | 3 / 6 |
| everything else | unchanged | unchanged |

The roster rows keep their picks; all 50 rows in sample_enemies.csv
still build. With Strikers giving up Accuracy, Attack went back up by 1
to follow the PC progression (6 to 10, the cap at Level 5).

**After** (`kit_check.py` on the final kit): the Roles read 2.7-3.9
Health at Level 2 and 2.7-5.7 at Level 3 (Striker and Bruiser still at
the top there, Defender and Backup each add about a round). Every
Ability and armor is within ±1.1 of fair except Enhanced Range at Level 2
(+1.6), Powerful Spell and Poison (Bleeding) at Level 3 (+1.9, +1.7),
and Retribution Aura and Strike (Devastating) at Level 2 (−1.4, −1.3).
Some readings now come from fewer enemies: at the new prices an enemy
that already carries armor or two picks can't fit another 3-5 Upgrades.

**The baseline on the final kit** (`table_check.py`; days won / F1 Down /
F1 Wounded / rounds / acts again, middle of each band):

| Level | Composite XP | Middle | Bottom (days won) | Top (days won) |
|---|---|---|---|---|
| 1 | 75 | 96% / 14 / 47 / 4.5 / 49 | — | — |
| 2 | 125 | 98% / 11 / 41 / 4.5 / 53 | 43% | 100% |
| 3 | 175 | 97% / 13 / 44 / 4.0 / 51 | 61% | 100% |
| 4 | 225 | 99% / 10 / 37 / 4.5 / 61 | 67% | 100% |
| 5 | 275 | 99% / 12 / 36 / 5.1 / 65 | 99% | 99% |

Every Level now plays alike in the middle of its band, at 4-5 rounds,
a little on the easy side of the October targets (Wounded in 36-47% of
fights against "about every other one"). The bottom of each band is a
hard day; Level 5's is flat because the grown characters have capped.

**Left for the designer:** whether the middle should be a notch harder
(Wounded nearer half); whether 5 Upgrades is the right home for
Poison (Bleeding) or it wants a different shape (the Bleeding weights
are next in the effect-weights pass anyway); and whether Retribution
Aura's "melee attackers only" reads right in the fiction.

### Archetypes and what enemy damage is worth (2026-11-02)

The designer: Striker is a trade, but Bruiser (Striker plus −1 Parry and
Dodge) looks strictly worse; why does the sim value enemy damage so
highly? `kit_check.py` with a probe Role on every full-size enemy, one
stat at a time (Health per Slot / change in fights where someone goes
Down, Level 2 and 3):

| Change | Level 2 | Level 3 |
|---|---|---|
| Damage +1 | +9.4 / +15 pts | +12.6 / +20 pts |
| Damage −1 | −5.5 / −4 | −8.2 / −5 |
| Resist +1 | +2.2 / +3 (+0.7 rounds) | +2.6 / +3 |
| Accuracy +1 / −1 / −2 | +1.2 / −1.1 / −2.5 | +1.4 / −1.6 / −3.3 |
| Parry +1, Dodge +1 (each) | +0.3, +0.7 | +0.5, +0.2 |
| Vital or Mental +1 | 0 | 0 |
| Speed +1 | +0.5 | +0.3 |

Why damage: the margin is thin. The current mixes' attacks average 5.6
damage against the parties' 4.4 Physical / 3.2 elemental Resist, so a
hit nets about 1.5 before extra successes, and +1 Damage is +63% of
everything an enemy deals. The other way round, PC weapons net about 3
a hit past enemy Resist, so +1 enemy Resist takes about a third off the
party's damage (worth 2-3 Health and most of a round). Parry and Dodge
count for little because an enemy defends with the better of the two, so
raising one moves only some attacks; Vital and Mental count for nothing
because these parties almost never target them. So +1 Damage is worth
about eight points of Accuracy, and an archetype carrying it has to pay
in Accuracy: 2 points does (they compound, fewer hits means fewer extra
points), 3 is too much (Striker at −3 read +1.0/+1.6).

Bruiser was Striker plus −1 Parry/Dodge, worth about −0.5 Health, so it
was strictly worse, as the designer saw. It's now the tough, clumsy
hitter, the original table's shape: Damage +1, Resist +1, Accuracy −3.
Candidates tried (Level 2 / Level 3, Health):

| Bruiser | L2 | L3 | rounds |
|---|---|---|---|
| Damage +1, Accuracy −2, Parry −1, Dodge −1 (old) | +3.2 | +5.0 | −0.1 |
| Resist +2, Parry −1, Dodge −1 | +4.4 | +5.3 | +1.4 |
| Damage +1, Resist +1, Accuracy −3, Parry −1, Dodge −1 | +2.5 | +3.8 | +0.4 |
| **Damage +1, Resist +1, Accuracy −3** (adopted) | **+3.4** | **+4.8** | **+0.7** |

The six now (Health; L2 / L3): Defender +3.9 / +4.5, Backup +3.4 /
+3.9, Striker +3.9 / +5.7, Bruiser +3.4 / +4.8, Skirmisher +3.7 / +2.7,
Strategist +2.7 / +3.1. Each is a distinct shape: Defender and Backup
lengthen fights by a round or more, Bruiser by most of one, Striker and
Strategist not at all. Striker sits a little high at Level 3 and
Skirmisher a little low (Dodge is worth less there); noise is about
±0.5.

The middle of each band on the adopted set (`table_check.py`, days won /
F1 Down / F1 Wounded / rounds): Level 1 97% / 13 / 45 / 4.7, Level 2
99% / 8 / 37 / 4.6, Level 3 97% / 10 / 41 / 4.1, Level 4 98% / 8 / 34 /
4.6, Level 5 99% / 8 / 32 / 5.3. The Brute, the roster's Bruiser, got a
little easier, so this is a notch further on the easy side.

### Toward PC-like enemy stats (2026-11-03)

The designer, overnight: can enemies get 4-5 round fights and the
on-level challenge without so much Health, with numbers closer to what
PCs end up with? Why did the two come out so different? Nothing changed
in the builder; these are readings.

**Where they differ** (middle of each band; PCs are the parties
`table_check.py` plays, enemies the average full-size enemy in the four
mixes; PC Accuracy is the attack Skill Total before a weapon's +1,
enemy Accuracy is the whole attack, archetype included):

| Level | PC Health | Enemy Health | PC Resist (P/E) | Enemy Resist | PC Damage | Enemy Damage | PC Acc | Enemy Acc | PC / enemy best Parry-Dodge |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 10.0 | 13.4 | 3.4 / 2.1 | 2.7 / 1.8 | 5.2 | 4.6 | 6.1 | 5.1 | 13.8 / 13.1 |
| 2 | 10.1 | 17.1 | 4.4 / 3.2 | 2.8 / 1.9 | 5.4 | 5.5 | 8.0 | 6.1 | 15.1 / 14.1 |
| 3 | 10.7 | 19.1 | 4.4 / 3.1 | 3.4 / 2.1 | 6.0 | 5.6 | 9.0 | 7.1 | 15.7 / 15.1 |
| 4 | 10.7 | 22.1 | 5.9 / 4.6 | 4.4 / 3.1 | 6.7 | 6.6 | 10.7 | 8.1 | 17.5 / 16.1 |
| 5 | 10.7 | 23.1 | 6.3 / 5.0 | 4.4 / 3.1 | 6.7 | 6.6 | 10.7 | 9.1 | 17.9 / 17.1 |

Enemies are built big and soft: about twice the PCs' Health, 1-2 less
Resist, a little less Accuracy (mostly the roster's Strikers paying 2 for
their Damage). The reason is the margins. A PC's hit nets about 3 past
enemy Resist and an enemy's about 1.5 past the PCs', so each point of
Resist is a large share of a hit. With the PCs' Resist and enemy
Resist 1-2 lower, the party's damage per round was high, so fights only
reached 4-5 rounds with lots of enemy Health. Enemy Resist can stand in
for Health: +1 Resist cuts the party's damage by about a third.

**The sweeps** (`experiments/enemies/progression_sweep.py`, nudges on
v2 at every Level, the middle of each band, 60 days per mix per party;
`progression_rank.py` scores them against the targets: about 95% of
days, someone Down in about a fifth of fresh fights, Wounded about half,
4-5 rounds, acts again about half). Two grids, 48 configs: Resist +0/+1/
+2, Health ×1.0 to ×0.5, Damage +0/+1, Accuracy +0/+1. What held:

- Less Health alone shortens fights (×0.65: about 3 rounds, nearly
  every day won, someone Down in 2-3% of fights) and makes them easier; Damage +1 alone makes them harder (76-86% of days).
- Resist +1, Health ×0.65 and Damage +1 together (enemy Damage then
  matches the player formula exactly, no −1) keep Levels 2, 4 and 5 on
  target at about two-thirds of v2's Health, with enemy Resist at the
  PCs' level.
- Level 1 (the sample parties, lower damage) wants Damage left at −1 and
  Health ×0.75; Level 3 wants Health ×0.75 and Accuracy +1 rather than
  Damage +1. Resist +2 anywhere made the bottom of the band much harder
  (Level 3: 28% of days).

**The best set across the bands** ("PC-like per Level": Resist +1 at
every Level; Level 1 Health ×0.75; Level 2 Health ×0.65, Damage +1;
Level 3 Health ×0.75, Accuracy +1; Levels 4-5 Health ×0.65, Damage +1).
Days won (worst party) / F1 Down / F1 Wounded / rounds / acts again:

| Level | Composite XP | v2 | PC-like per Level |
|---|---|---|---|
| 1 | 75 | 97% (95) / 12 / 45 / 4.7 / 54 | 95% (91) / 12 / 43 / 4.9 / 51 |
| 2 | 100 | 45% (20) / 53 / 77 / 6.8 / 68 | 38% (10) / 54 / 77 / 6.1 / 57 |
| 2 | 125 | 99% (98) / 8 / 38 / 4.6 / 57 | 94% (82) / 14 / 45 / 4.1 / 43 |
| 2 | 150 | 100% / 2 / 17 / 4.0 / 51 | 99% / 6 / 29 / 3.4 / 38 |
| 3 | 150 | 63% (32) / 39 / 70 / 6.7 / 67 | 51% (16) / 45 / 74 / 7.1 / 64 |
| 3 | 175 | 97% (88) / 9 / 41 / 4.1 / 52 | 94% (78) / 11 / 44 / 3.9 / 46 |
| 3 | 200 | 100% / 2 / 15 / 3.5 / 47 | 100% / 2 / 16 / 3.2 / 40 |
| 4 | 200 | 70% (38) / 35 / 67 / 6.1 / 68 | 59% (22) / 42 / 70 / 5.3 / 57 |
| 4 | 225 | 99% (95) / 8 / 32 / 4.6 / 64 | 93% (75) / 17 / 45 / 3.9 / 51 |
| 4 | 250 | 100% / 3 / 19 / 4.5 / 62 | 99% / 8 / 34 / 3.8 / 49 |
| 5 | 275 | 99% (98) / 7 / 32 / 5.3 / 67 | 96% (85) / 15 / 47 / 4.4 / 53 |

Its enemies, against the PCs above: Health 10.5 / 11.7 / 14.6 / 15.0 /
15.1 (v2: 13-23), Resist 3.7 / 3.8 / 4.4 / 5.4 / 5.4 Physical (PCs: 3.4-6.3), Damage 4.6 /
6.5 / 5.6 / 7.6 / 7.6, Accuracy 5.1 / 6.1 / 8.1 / 8.1 / 9.1.

What it costs:

- **A wider spread between parties.** With higher enemy Resist a
  low-damage party loses a bigger share of its damage: the worst party
  in the middle of the band wins 75-85% of days at Levels 2-5, against
  88-98% under v2. That's the "weak builds stand out" the yardstick wanted, but a
  harder floor too.
- **Shorter fights,** 3.9-4.9 rounds against v2's 4.1-5.3, and acts again
  at the low end (43-53%).
- **A harder bottom of the band** at Levels 2-4 (38-59% of days).
- **The kit prices assumed v2's Health.** With a third less Health an
  Upgrade of Health is a bigger share of an enemy, and a Resist or Damage
  bonus moves more; the archetype and Ability prices would want
  rechecking under it.
- **It isn't regular yet.** Damage and Health go back and forth by
  Level, partly because Level 1 is the sample parties (less damage) and
  Levels 4-5 are grown characters. A table version would smooth it:
  Resist +1 throughout, enemy Damage on the player formula from Level 2,
  Health about 11 / 12 / 14 / 15 / 15 per full-size enemy.

### v3: enemies built the way PCs are (2026-11-03)

Per the designer's first principles (top of this document), with the
original spreadsheet re-read: its Design sheet already priced an enemy's
stats in player XP and landed on the player schedule (Total XP rating
64 / 124 / 174 / 221 / 280 at Levels 1-5), and its NPC Enemy Rules sheet
had Damage and Resist 2 / 3 / 4 / 5 / 5 and Health 5-13. Its Roles were
plain bumps. Where v1 and v2 drifted (big Health, low Resist, damage
below the player formula, Accuracy trades) was in chasing fight length
after the fact. v3 goes back to the shape and finds the balance inside
it. `tunables.ENEMY_TABLE = 'v3'`, the default since the designer
adopted it (with the trim and archetypes in "v3 adopted" below).

**How a v3 enemy is built** (`enemy_builder_pcstyle.build_enemy_v3`):

- **Skill**: the weapon Skill Total. With a melee weapon in hand, Parry
  = 8 + Skill + the weapon's Defense, as for a PC; casters and archers
  can't Parry (a support with a backup mace Parries at its Weak tier).
- **Defenses**: the Strong Defense (the row's StrongDefense) = 8 + Skill;
  one Weak Defense = 8 + Skill − 4, by default what that kind of enemy
  visibly neglects (a fighter's Mental, a caster's Vital, a support's
  Dodge; a row can name its own in WeakDefense); the rest Average, 8 +
  Skill − 2 (`tunables.V3_DEF_GAP`). Armor moves Dodge as for a PC.
- **Accuracy**: a Skill Total one under Skill, plus the weapon's or
  spell's own Accuracy (+1 light weapons, +0 heavy weapons and spells);
  archetypes that attack well raise it back.
- **Damage**: the player weapon and spell table (light 3, 1H heavy 4,
  2H heavy 5, spells 2) + the damage Stat.
- **Resist**: the Resist Stat + armor (Light +1, Medium +2, Heavy +3
  Physical).
- **Health** per Slot; minions a third (rounded up), a 2-Slot elite
  three times.
- **Caps**: Stats 5, Skill Totals 10, as for a PC.
- Abilities aren't priced yet under v3 (an enemy has the ones on its
  row; v2's repricing and its 1-stack Bleeding don't apply). That's the
  next pass.

**The table** (each stat steps up at its own Levels so two don't jump at
once; Defenses as 8 + Skill Total):

| Level | Skill (Parry, Strong) | Accuracy | Defense: Strong / Average / Weak | Damage Stat | Resist Stat | Health per Slot (minion) | Speed | Reflex |
|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 4 | 13 / 11 / 9 | 2 | 2 | 10 (4) | 3 | 3 |
| 2 | 6 | 5 | 14 / 12 / 10 | 3 | 3 | 11 (4) | 3 | 4 |
| 3 | 7 | 6 | 15 / 13 / 11 | 3 | 3 | 13 (5) | 4 | 5 |
| 4 | 8 | 7 | 16 / 14 / 12 | 4 | 4 | 15 (5) | 4 | 6 |
| 5 | 9 | 8 | 17 / 15 / 13 | 4 | 4 | 15 (5) | 5 | 7 |

What that comes to before archetype and armor: a light-weapon fighter
at Level 1 hits at +5 for 5 with Parry 14; at Level 5, +9 for 7 with
Parry 18. A 2H heavy weapon hits for 2 more at 1 less Accuracy and has
no weapon Defense on its Parry. A caster hits at +4 / +8 for 4 / 6,
can't Parry, and has the Weak Vital Defense.

**Against the PCs** (middle of each band; PC Accuracy is the attack
Skill Total before the weapon's own +1):

| Level | PC / enemy Accuracy | PC best Parry-Dodge / enemy Strong | PC / enemy Resist Stat | PC / enemy Damage | PC / enemy Health |
|---|---|---|---|---|---|
| 1 | 6.1 / 4 | 13.8 / 13 | 3.4 / 2 (+armor) | 5.2 / 5 | 10.0 / 10 |
| 2 | 8.0 / 5 | 15.1 / 14 | 4.4 / 3 | 5.4 / 6 | 10.1 / 11 |
| 3 | 9.0 / 6 | 15.7 / 15 | 4.4 / 3 | 6.0 / 6 | 10.7 / 13 |
| 4 | 10.7 / 7 | 17.5 / 16 | 5.9 / 4 | 6.7 / 7 | 10.7 / 15 |
| 5 | 10.7 / 8 | 17.9 / 17 | 6.3 / 4 | 6.7 / 7 | 10.7 / 15 |

(PC Resist is the whole Resist, armor included; an enemy's is its Stat
plus its armor, so a Light-armored enemy is about 1 under the party.)

**The archetypes** (bumps, capped at the player maximums; values from
`kit_check.py` under v3, enemy Health per Slot at Levels 2 / 3, and the
change in fights where someone goes Down):

| Archetype | Adds | Worth | Plays |
|---|---|---|---|
| Defender | Resist +1, Parry +1, Dodge +1 | 2.1 / 2.0 | +1 round |
| Striker | Damage +1, Accuracy +1, Resist −1 | 1.7 / 3.2 | spikier (+6-12 Down) |
| Bruiser | Damage +1, Resist +1, Parry −1, Dodge −1, Speed −1 | 2.6 / 3.5 | spikier and longer |
| Strategist | Accuracy +2, Dodge +1, Mental +1 | 1.8 / 2.5 | |
| Skirmisher | Accuracy +2, Dodge +1, Speed +1 | 2.4 / 3.0 | |
| Backup | Resist +1, Dodge +1, Vital +1, Mental +1 | 1.8 / 1.7 | +1 round |

With the original bumps unchanged (Striker Damage +1 and Accuracy +1;
Bruiser Damage +1, Resist +1, Parry/Dodge −1; Strategist Accuracy +1,
Parry/Dodge +1, Mental +1; Backup Parry/Dodge +1, Vital +1, Mental +1)
they read 3.1-4.8 for Striker and Bruiser and 0.2-1.4 for Strategist and
Backup: Parry and Dodge +1 are worth about 0.1-0.2 Health (an enemy
defends with the better of the two, and the parties mostly attack one),
Vital and Mental +1 nothing against these parties, +1 Accuracy about 1,
+1 Resist about 1.4 and most of a round, +1 Damage about 2-3. Under v3
damage no longer dwarfs the rest (under v2 +1 Damage was worth eight
Accuracy; now about two and a half), because enemy hits now get well
past the party's Resist, so +1 is a smaller share of them. So no
archetype has to pay Accuracy for Damage: Striker pays by being lightly
built, Bruiser by being heavy and slow.

**The Level 3 roster under v3:**

| Enemy | Archetype | Action + Abilities | Armor | Acc | Damage | Parry | Dodge | Vital | Mental | Vigilant | Resist (P / E) | Health | Speed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Brute | Bruiser | Light Melee + Heavy Weapon, Strike (Crippling) | Medium | 6 | 8 Physical | 14 | 11 | 15 | 11 | 13 | 6 / 4 | 13 | 3 |
| Hedge Knight | Defender | Light Melee + Strike (Taunting) | Heavy | 7 | 6 Physical | 17 | 13 | 15 | 11 | 13 | 7 / 4 | 13 | 3 |
| Skulking Footpad | Skirmisher | Light Melee + Poison (Bleeding) | Light | 9 | 6 Physical | 16 | 16 | 13 | 11 | 13 | 4 / 3 | 13 | 5 |
| Marsh Archer | Striker | Ranged Weapon + Strike (Vulnerable) | Light | 8 | 7 Physical | — | 15 | 13 | 11 | 13 | 3 / 2 | 13 | 4 |
| Grave Caller | Striker | Vital Spell + Strike (Vulnerable) | Unarmored | 7 | 6 Shadow | — | 13 | 11 | 15 | 13 | 2 / 2 | 13 | 4 |
| Warpriest | Backup | Shield Ally (backup mace) + Strike (Frightening) | Medium | 3 | 6 Physical | 12 | 11 | 14 | 16 | 13 | 6 / 4 | 13 | 4 |
| Goblin Cutthroat (minion) | Striker | Light Melee + Strike (Slowing) | Light | 8 | 7 Physical | 16 | 15 | 13 | 11 | 13 | 3 / 2 | 5 | 4 |

**How it plays** (`table_check.py -t v3`; days won (worst party) / F1
Down / F1 Wounded / rounds / acts again):

| Level | Composite XP | v3 | v2 (for reference) |
|---|---|---|---|
| 1 | 75 | 91% (83) / 17 / 52 / 3.8 / 38 | 97% (95) / 12 / 45 / 4.7 / 54 |
| 2 | 100 | 42% (10) / 52 / 78 / 5.3 / 53 | 45% (20) / 53 / 77 / 6.8 / 68 |
| 2 | 125 | 93% (74) / 15 / 44 / 3.9 / 41 | 99% (98) / 8 / 38 / 4.6 / 57 |
| 2 | 150 | 99% / 6 / 29 / 3.3 / 37 | 100% / 2 / 17 / 4.0 / 51 |
| 3 | 150 | 48% (12) / 47 / 77 / 6.0 / 56 | 63% (32) / 39 / 70 / 6.7 / 67 |
| 3 | 175 | 93% (72) / 15 / 48 / 3.5 / 39 | 97% (88) / 9 / 41 / 4.1 / 52 |
| 3 | 200 | 100% / 5 / 25 / 3.0 / 34 | 100% / 2 / 15 / 3.5 / 47 |
| 4 | 200 | 63% (21) / 38 / 70 / 5.2 / 55 | 70% (38) / 35 / 67 / 6.1 / 68 |
| 4 | 225 | 93% (75) / 16 / 48 / 3.9 / 50 | 99% (95) / 8 / 32 / 4.6 / 64 |
| 4 | 250 | 100% / 8 / 35 / 3.8 / 49 | 100% / 3 / 19 / 4.5 / 62 |
| 5 | 275 | 96% (87) / 14 / 48 / 4.3 / 51 | 99% (98) / 7 / 32 / 5.3 / 67 |

The middle of every band lands on the October targets (Down in about
one fight in six, Wounded about every other one), at 3.5-4.3 rounds:
spikier and a little shorter than v2, which the designer accepted for
PC-like numbers. Weaker parties feel it more (worst party 72-87% in the
middle). A hit enemy acts again 38-51% of the time.

**How the schedule was found** (`progression_sweep.py --table v3`,
`results/enemy_stats/v3*.jsonl`): a 32-config grid of damage −1/0,
Resist +0/+1, Accuracy −1/0, Health +0/+2 and Defense gap 1/2, read Level
by Level (each Level's parties meet only its enemies), then three whole
schedules across the bands. The designer's damage schedule (2, 3 at
Level 2, 4 at Level 4) held at every Level once base Accuracy sat one
under Skill; moving the damage steps later made Level 4 too easy.
Health more than about 2 over the table made Level 1 too hard; +1 Resist
across the board did the same. The Defense gap made little difference
between 1 and 2; 2 keeps the spread legible.

**Open:** abilities under v3 (prices against these numbers, in picks or
Health); whether 3.5-4 rounds is close enough to "4-5"; Levels 4-5 are
still checked against grown Level 3 characters.

### v3 adopted: trimmed base, bigger archetypes, Abilities priced in Health (2026-11-03)

The designer adopted v3 the same day, with two changes: "trim back a
slight bit of the baseline stat block and add that power budget into the
archetypes" so enemies feel distinct, then "start ironing out the
Ability budget and balancing, at least in terms of Health", with a second
look at each price once the balance weights are reviewed. v3 is the
simulator default; `tunables.V3_VERSION = 1` plays the first v3 (the
table above and its archetypes) for the numbers recorded under it.

**The trimmed table**: every Level loses 1 Skill (so every Defense and
Parry) and 1 Accuracy.

| Level | Skill (Parry, Strong) | Accuracy | Defense: Strong / Average / Weak | Damage Stat | Resist Stat | Health per Slot (minion) |
|---|---|---|---|---|---|---|
| 1 | 4 | 3 | 12 / 10 / 8 | 2 | 2 | 10 (4) |
| 2 | 5 | 4 | 13 / 11 / 9 | 3 | 3 | 11 (4) |
| 3 | 6 | 5 | 14 / 12 / 10 | 3 | 3 | 13 (5) |
| 4 | 7 | 6 | 15 / 13 / 11 | 4 | 4 | 15 (5) |
| 5 | 8 | 7 | 16 / 14 / 12 | 4 | 4 | 15 (5) |

Speed and Reflex are unchanged. Built from the table, the enemies match
the runs that played the trim as a nudge, except at Level 5, where the
Skill 10 cap now applies as written (four Defenses 1 higher).

**The archetypes** (`kit_check.py`, enemy Health per Slot at Levels
2 / 3, and the change in rounds):

| Archetype | Adds | Worth | Rounds |
|---|---|---|---|
| Defender | Resist +1, Parry +2, Dodge +2 | 3.6 / 2.8 | +2.4 / +1.7 |
| Striker | Damage +1, Accuracy +2, Resist −1 | 2.8 / 4.4 | −0.2 |
| Bruiser | Damage +1, Resist +1, Vital +2, Parry −1, Dodge −1, Speed −1 | 2.9 / 3.5 | +0.7 / +0.6 |
| Strategist | Accuracy +3, Dodge +1, Mental +2, Vigilant +2 | 2.5 / 3.6 | +0.3 / +0.2 |
| Skirmisher | Speed +2, Dodge +2, Accuracy +2 | 2.4 / 3.3 | +0.4 / +0.3 |
| Backup | Resist +1, Parry +1, Dodge +2, Vital +2, Mental +2 | 3.1 / 2.5 | +2.0 / +1.4 |

Bruiser first had Resist +2: 6.8 / 9.1 and over two extra rounds, so it
took Vital +2 instead (a hard body to poison).

**What each Ability is worth** (`kit_check.py --bare`: every full-size
enemy in the four mixes stripped of its Abilities, then given just the
one, if it can take it; eight normalized parties in the middle of the
band, 2,000 fights a reading on paired seeds). An Ability only some
enemies can take (Powerful Spell on the two casters, Enhanced Range on
the ranged ones) is spread over all fourteen in the raw reading, so each
reading is divided by the share that took it. The v2 kit's readings
weren't, which undercounted those Abilities there. Health per Slot at
Levels 2 / 3, for the enemy that has it:

- **About nothing** (under half a Health): the one-stack riders (Strike
  or Poison Crippling, Vulnerable, Slowing; Strike Frightening,
  Taunting), Resilient, Action (Intimidating); Sturdy and Shadow Jaunt
  read exactly 0 (the parties don't grapple, Push or chase).
- **About 1:** Necrotic riders 1.4 / 1.0, Harrying 0.7, Devastating
  0.3 / 1.4 (its damage arrives as Bleeding, which Protected stops),
  Heavy or Powerful Weapon 0.7 / 1.2, Durable 1.2 / 0.9, Omniguard
  0.6 / 0.4, Enhanced Speed 0.4 / 0.7, Parting Shot 0.8 / 1.4, Action
  (Taunting) 0.4 / 0.7, Resist (Fire) 1.0 / 1.4, Medium Armor over
  Light 1.2 / 1.0, Enhanced Health 0.8 / 0.9 (it's +1 Health: the sanity
  check).
- **About 2:** Battering 1.2 / 1.8, Cleaving 1.7 / 1.8, Enhanced
  Reflexes 1.3 / 3.1, Heavy Armor over Light 2.1 at Level 3.
- **More:** Grappling 2.7 / 3.6, Powerful Spell 2.2 / 5.1, Enhanced
  Range 4.5 / 3.1, Attunement (Fire) 3.6 / 4.0 (against the parties
  that use War Magic's Fire).
- **As written, too much for one Ability:** Poison (Bleeding) 4.6 / 6.2
  (2 stacks a hit) and Retribution Aura 10.6 / 19.2 (every attacker
  takes Bleeding, every hit). In the v2 kit's shapes (1 stack; melee
  attackers only) they read 2.4 / 3.4 and 1.7 / 3.0, and v3 now plays
  them that way (`tunables.V3_KIT_SHAPES = 'v2'`). Both shapes are still
  the designer's call.

Unarmored gives back about 1 against Light. The roster's own Abilities,
taken all together, are worth about 1 Health an enemy.

**The draft prices** (`enemy_builder_pcstyle.ABILITY_HEALTH_V3`,
`tunables.V3_ABILITY_PRICES`): every enemy gets 1 Health per Slot of
Abilities and armor free on top of the table (`V3_ABILITY_ALLOWANCE`,
about what the roster's come to); what it spends past that comes off
its Health, what it leaves is Health, and at most a third of the
table's Health can go.

| Health | Abilities |
|---|---|
| 0 | the one-stack Strike and Poison riders (Crippling, Vulnerable, Slowing, Frightening, Taunting), Resilient, Sturdy, Shadow Jaunt, Action (Intimidating), Elemental Spell or Weapon (reflavors) |
| 1 | Strike or Poison (Necrotic), Strike (Harrying), Strike (Devastating), Heavy or Powerful Weapon, Durable, Omniguard, Enhanced Health, Enhanced Speed, Improved Support, Action (Parting Shot), Action (Taunting), Resist (an element), Medium Armor |
| 2 | Strike (Battering), Strike (Cleaving), Enhanced Reflexes, Retribution Aura, Heavy Armor |
| 3 | Strike (Grappling), Poison (Bleeding), Powerful Spell, Enhanced Range, Attunement (an element) |
| −1 | Unarmored (gives one back) |

A 0 means the sim reads it as about nothing against the sample parties,
not that it's worthless: some are situational (Sturdy, Shadow Jaunt),
and the one-stack debuffs are the ones to check against the balance
weights first, since the sim may undervalue them.

**Checked with the prices on** (`results/enemy_stats/v3_abilities_priced*`):
every Ability reads within about ±0.6 of fair, except Grappling and
Enhanced Reflexes at Level 3 (+1.2, +1.1, a little cheap there) and
Heavy Armor at Level 2 (+2.9; Heavy is for Level 3 and up). Powerful
Spell, Attunement and Enhanced Range first went in at 4 and read −2.3,
−1.2 and −1.1, so they came down to 3 (Powerful Spell read +0.8 / +2.3
at 2). Improved Support can't be read here: one Warpriest in fourteen
enemies, and moving its price by 1 didn't move the reading.

**How it plays** (`progression_sweep.py --table v3`, middle of each
band; days won (worst party) / F1 Down / F1 Wounded / rounds / acts
again):

| Level | Composite XP | Adopted, unpriced | Priced (allowance 1) |
|---|---|---|---|
| 1 | 75 | 95.4% (90) / 13 / 45 / 3.6 / 36 | 95.2% (90) / 13 / 42 / 3.7 / 38 |
| 2 | 125 | 95.6% (85) / 12 / 41 / 3.7 / 39 | 94.5% (83) / 13 / 40 / 3.7 / 40 |
| 3 | 175 | 95.3% (80) / 13 / 44 / 3.4 / 38 | 94.5% (78) / 14 / 43 / 3.3 / 37 |
| 4 | 225 | 95.8% (82) / 13 / 43 / 3.8 / 49 | 95.2% (82) / 15 / 44 / 3.8 / 50 |
| 5 | 275 | 97.4% (91) / 12 / 44 / 4.1 / 50 | 97.1% (88) / 13 / 44 / 4.0 / 51 |

Pricing barely moves the roster: the Unarmored casters gain 2 Health,
the Footpad pays 2 for Poison (Bleeding), and the rest are within 1 of
where they were.

**Open:** each price against the balance weights (the zeros first);
Poison (Bleeding)'s and Retribution Aura's shapes; Improved Support
needs a test with more supports in it; whether 1 Health is the right
allowance; Heavy Armor's Level 3 floor isn't enforced under v3 yet.

### How much budget can go into on-hit debuffs (2026-11-04)

The designer: a bigger allowance with the option to spend it on Health
is the same thing as v3's 1 point plus a Health trade. What matters is
that enemies should apply debuffs and have mechanics as a standard
thing, not be pure Health sponges. So pull some other power budget back
to fit them in, and see how much each Level can bear before the missing
stats distort the fights.

`experiments/enemies/debuff_budget.py` gives every full-size enemy in
the four mixes (not the minions) a package of on-hit Abilities on top of
its own. Every package starts with two free riders (Strike (Crippling),
Strike (Slowing)) and adds, in order, Strike (Necrotic) (1), Strike
(Harrying) (1), Poison (Necrotic) (1), Poison (Bleeding) (3) and Strike
(Battering) (2), at the v3 prices. The package is paid for either from
Health, as a v3 enemy normally pays, or from a stat, with its Health put
back. The Health floor is off so the ladder can run past what a GM
could build. Middle of each band, day standard; days won (worst party) /
F1 Down / F1 Wounded / rounds / acts again:

| Package (paid with) | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|---|---|---|---|---|---|
| as built | 95 (90) / 13 / 42 / 3.7 / 38 | 95 (83) / 13 / 40 / 3.7 / 40 | 95 (78) / 14 / 43 / 3.3 / 37 | 95 (82) / 15 / 44 / 3.8 / 50 | 97 (88) / 13 / 44 / 4.0 / 51 |
| free riders only | 94 (88) / 14 / 43 / 3.8 / 39 | 93 (75) / 14 / 41 / 3.9 / 41 | 93 (74) / 14 / 44 / 3.4 / 38 | 94 (76) / 16 / 45 / 3.9 / 51 | 95 (81) / 13 / 45 / 4.2 / 52 |
| 1 (Health) | 94 (88) / 14 / 40 / 3.5 / 33 | 93 (75) / 15 / 39 / 3.6 / 36 | 93 (72) / 14 / 42 / 3.2 / 33 | 93 (76) / 16 / 43 / 3.7 / 47 | 94 (80) / 14 / 44 / 3.9 / 47 |
| 2 (Health) | 95 (87) / 14 / 39 / 3.1 / 27 | 93 (73) / 15 / 37 / 3.3 / 31 | 93 (68) / 14 / 41 / 3.0 / 29 | 92 (75) / 17 / 43 / 3.5 / 43 | 94 (80) / 14 / 44 / 3.6 / 43 |
| 3 (Health) | 97 (92) / 12 / 35 / 2.8 / 21 | 95 (75) / 14 / 34 / 3.0 / 26 | 95 (75) / 13 / 39 / 2.8 / 25 | 93 (77) / 16 / 42 / 3.3 / 38 | 96 (88) / 13 / 42 / 3.4 / 38 |
| 6 (Health) | 100 (99) / 6 / 25 / 2.0 / 3 | 98 (88) / 10 / 26 / 2.2 / 10 | 97 (79) / 13 / 34 / 2.2 / 13 | 95 (78) / 17 / 42 / 2.7 / 26 | 96 (85) / 16 / 42 / 2.8 / 25 |
| 8 (Health) | 100 / 6 / 22 / 1.7 / 0 | 100 (99) / 5 / 18 / 1.8 / 0 | 99 (95) / 8 / 23 / 1.7 / 3 | 97 (89) / 14 / 36 / 2.3 / 15 | 98 (92) / 11 / 34 / 2.3 / 15 |
| 2 (Damage −1) | 96 (92) / 10 / 32 / 3.9 / 39 | 97 (87) / 10 / 32 / 3.9 / 41 | 97 (87) / 8 / 32 / 3.4 / 39 | 98 (94) / 7 / 30 / 3.8 / 51 | 99 (95) / 4 / 26 / 4.1 / 51 |
| 3 (Damage −1) | 96 (91) / 11 / 33 / 3.9 / 39 | 96 (79) / 12 / 33 / 3.9 / 42 | 97 (86) / 9 / 32 / 3.4 / 39 | 97 (93) / 7 / 31 / 3.8 / 51 | 99 (95) / 4 / 27 / 4.1 / 51 |
| 6 (Damage −1) | 89 (75) / 18 / 46 / 3.9 / 40 | 89 (60) / 18 / 43 / 3.9 / 42 | 92 (68) / 17 / 44 / 3.4 / 39 | 92 (75) / 19 / 47 / 3.9 / 51 | 91 (75) / 16 / 47 / 4.2 / 51 |
| 2 (Accuracy −1, Resist −1) | 98 (95) / 10 / 33 / 3.1 / 28 | 98 (91) / 11 / 31 / 3.1 / 31 | 96 (80) / 12 / 36 / 2.9 / 31 | 97 (87) / 12 / 34 / 3.3 / 42 | 98 (92) / 10 / 36 / 3.4 / 43 |
| 3 (Damage −1, Accuracy −1) | 99 (96) / 7 / 28 / 3.8 / 38 | 98 (90) / 8 / 27 / 3.8 / 41 | 98 (91) / 7 / 26 / 3.3 / 38 | 99 (95) / 5 / 23 / 3.8 / 51 | 100 (98) / 3 / 21 / 4.0 / 51 |
| 6 (3 Health, 3 for Damage −1) | 98 (94) / 9 / 32 / 2.8 / 21 | 97 (86) / 12 / 31 / 3.0 / 26 | 96 (83) / 10 / 35 / 2.7 / 26 | 96 (86) / 13 / 39 / 3.2 / 38 | 97 (88) / 11 / 37 / 3.3 / 38 |

What it says:

- **Paid from Health, the debuffs about earn their keep, but the fights
  shrink.** Days won barely move through 3 Health, but each Health spent
  takes about a quarter of a round off and 4-6 points off "acts again".
  Past about 3 rounds and 30% acts again, the enemy drops before its
  debuffs have time to matter, and fights get easier: at 6 Health, Level
  1 is 2 rounds and a hit enemy almost never acts again. Before that
  line, Levels 1-3 (10-13 Health) bear about 2 Health of debuffs (Level
  3 starts shortest, 1-2), and Levels 4-5 (15 Health) about 3, a fifth
  of the table's Health or a little less.
- **Paid from Damage, the fight keeps its length.** −1 Damage Stat leaves
  rounds and acts again where they were at every Level, because the
  enemy keeps all its turns and puts some of what it would have dealt
  into debuffs. It's worth more than the 1 Health per point the first
  guess gave it: 2 or 3 points of debuffs for −1 Damage is soft (96-99%
  of days, Down 4-12%), 6 points is a notch hard (88-92%, Down 16-19%,
  Wounded 43-47%). The fair trade is about 4-5 points of debuffs for −1
  Damage, the same at every Level.
- **Accuracy and Resist are poorer currencies.** −1 each for 2 points of
  debuffs is soft and shortens the fights (Resist is Health by another
  name).
- **The free riders aren't quite free.** Two of them on every enemy cost
  the party 1-2 points of days won: together they're worth something
  like half a Health to a Health, not 0.

So the way to give every enemy debuffs as standard without making it a
sponge, or a glass cannon that dies before they matter, is to pay for
them with Damage: one less on the Damage Stat schedule buys a package of
about 4-5 points (the two free riders plus Necrotic and Harrying and
then some, or Poison (Bleeding)), keeping the 4-round shape. Health can
still buy a point or two on top, within the limits above.

Caveats: the package leans on Necrotic and Bleeding, which act like
damage; the pure control debuffs (Crippled, Slowed, Vulnerable,
Frightened, Taunted) read small in the sim, which may undervalue them
(the balance-weights review). Enemies stacking the same debuff from two
sources (Strike and Poison (Necrotic)) is in the package; a GM would more
often pick different ones. Minions were left as they are.

### What each stat is worth, and which ones set fight length (2026-11-04)

The designer: are cuts to "survivability" the ones that make fights
shorter? The aim is a pruned baseline, with the power moved into the
archetypes and an Ability budget, nearly everything additive. Each stat
moved by 1 on every full-size enemy (`kit_check.py`, `nudge:` variants,
v3 as adopted, paired seeds, 2,000 fights a reading; enemy Health per
Slot, and the change in rounds), Levels 2 / 3:

| Change | Worth (Health) | Rounds |
|---|---|---|
| Damage −1 / +1 | −3.4 / −4.1, +3.9 / +4.2 | −0.2, +0.2 |
| Accuracy −1 / +1 | −1.9 / −2.0, +2.0 / +2.2 | −0.1, +0.1 |
| Parry and Dodge −1 | −0.9 / −0.3 | −0.3 / −0.2 |
| Vital, Mental, Vigilant −1 | about 0 | 0 |
| Resist −1 / +1 | −1.7 / −1.4, +4.1 / +3.2 | −0.7 / −0.5, +1.5 / +1.3 |
| Health −1 (from the debuff test) | −1 | about −0.25 |

Yes: what keeps an enemy standing (Health, Resist, and the Defense the
party attacks, Parry or Dodge) sets the fight's length, about a quarter
to a half round per Health of worth. What it hits with (Damage,
Accuracy) barely moves the length, about 0.05 rounds per Health of
worth. So a baseline pruned in offense keeps fights at their length,
and the budget it frees can buy offense back (+1 Damage for about 4,
+1 Accuracy for about 2) or go into debuffs and mechanics. Vital and
Mental are worth nothing against the sample parties, who rarely target
them; they'll matter against a party that does. +1 Resist is worth
more than −1 costs and adds over a round, so it's the one stat to hand
out carefully.

### The pruned v3: a thin baseline, archetypes and Abilities that add (2026-11-04)

The designer: "prune back some of the enemy baseline power, and then put
it in the Ability budget they can spend to further specialize." The
baseline is thin, the archetype carries a good share of the power, and
Abilities add the rest. Very few things take numbers away (heavier
armor is the example). If the baseline's damage comes down, the budget
has to be able to buy it back. Trim both Damage and Accuracy, and make
the archetypes additive. `tunables.V3_VERSION = 3`; v3 as adopted stays
the default until the designer picks.

**The pruned table**: the Damage Stat 1 / 2 / 2 / 3 / 3 and Accuracy one
lower (2 / 3 / 4 / 5 / 6). Health, Resist, Defenses, Speed and Reflex as
v3, since those set a fight's length ("What each stat is worth"). The
budget goes from 1 to 7 per Slot (`V3_PRUNED_ALLOWANCE`): the old 1,
plus 4 for the Damage Stat and 2 for the Accuracy the table gave up.
Unspent points are Health, as before. An enemy that buys back Damage +1
and Accuracy +1 is the old enemy.

**Additive archetypes** (`ROLE_ADDS_V3_ADDITIVE`; worth in enemy Health
per Slot at Level 2, against enemies that bought their stats back):

| Archetype | Adds | Worth |
|---|---|---|
| Defender | Resist +1, Parry +2, Dodge +2 | 3.1, adds about 1-1.5 rounds |
| Striker | Damage +1, Speed +1 | 3.4 |
| Bruiser | Damage +1, Health +1, Vital +2 | 3.3 |
| Strategist | Accuracy +2, Dodge +1, Mental +2, Vigilant +2 | 2.7 |
| Backup | Resist +1, Parry +1, Dodge +2, Vital +2, Mental +2 | 2.9, adds about a round |
| Skirmisher | Speed +2, Dodge +2, Accuracy +1 | 2.4 |

Striker and Bruiser lost their cuts (Striker's Resist −1; Bruiser's
Parry, Dodge and Speed −1). Striker is now the mobile hitter, Bruiser
the tough one. Accuracy is worth more on the pruned base, so Strategist
(+3) and Skirmisher (+2) read 4 Health and came down 1 each. Bruiser as
Health and Vital alone read about 1. Level 3 reads higher for the
damage archetypes (Striker and Bruiser about 5.5, the rest 3-4.7), on a
noisier slope (`results/enemy_stats/v3_pruned_roles*.txt`).

**The catalog, grouped** (Health per Slot; any v3 can use the stat
Abilities):

*Equipment.* What the enemy carries. These are the only things that
take a number away, the way gear does for a PC.

| Ability | Price | Notes |
|---|---|---|
| Unarmored / Light / Medium / Heavy Armor | −1 / 0 / 1 / 2 | Dodge and Speed as for a PC; Heavy is Level 3 and up |
| Heavy Weapon (also Powerful Weapon) | 1 | Damage +1, Accuracy −1, Parry −1. The two are the same in the sim and should be one entry: a two-handed weapon, as a PC's |
| Powerful Spell | 3 | a caster's focus: Damage +1, can't Parry |
| Enhanced Range | 3 | a longbow or a long reach: Range ×2 |
| Elemental Weapon / Elemental Spell | 0 | an enchanted weapon or a spell's element (the weapon at −1 Damage) |

*Stats.* Plain additions, each can be taken more than once up to the
player caps.

| Ability | Price | Notes |
|---|---|---|
| Damage +1 | 4 | the pruned base's buy-back |
| Accuracy +1 | 2 | the other buy-back |
| Guard +1 | 1 | Parry and Dodge +1; adds a quarter-round |
| Resist +1 | 4 | adds over a round; hand it out carefully |
| Enhanced Health | 1 | Health +1 (the catalog text says +3; the sim plays +1) |
| Enhanced Speed / Enhanced Reflexes | 1 / 2 | Speed +1 / Reflex +3 |

*On a hit.* Strike and Poison riders: one-stack Crippling, Vulnerable,
Slowing, Frightening, Taunting 0; Necrotic, Harrying, Devastating 1;
Battering, Cleaving 2; Grappling, Poison (Bleeding) 3.

*Toughness.* Durable, Omniguard, Resist (an element) 1; Retribution Aura
2; Attunement (an element) 3; Resilient, Sturdy 0.

*Actions and movement.* Action (Parting Shot), Action (Taunting),
Improved Support 1; Action (Intimidating), Shadow Jaunt 0.

**The roster spending its budget** (`sample_enemies.csv` PrunedPicks,
`tunables.V3_PRUNED_ROSTER`). Three ways, against v3 as adopted:

- *buyback*: every enemy buys back Damage +1 and Accuracy +1, the old
  enemies with the new archetypes.
- *picks*: the current roster redesigned to spend the budget on
  mechanics. Brute: Battering and Grappling. Hedge Knight: Action
  (Taunting), Omniguard, Harrying, Accuracy +1. Footpad: Parting Shot,
  Enhanced Reflexes, Harrying. Marsh Archer: Enhanced Range, Accuracy
  +1, Slowing, Harrying. Grave Caller: Powerful Spell, Accuracy +1,
  Strike and Poison (Necrotic). Ember Caster: Powerful Spell, Accuracy
  +1, Crippling, Attunement (Fire). Warpriest: Improved Support,
  Durable, Harrying, Action (Intimidating), Accuracy +1. All of these
  keep their row's own Abilities; minions and the other rows buy back.
- *mixed*: the same enemies buy back Damage +1 and take Necrotic and
  Harrying on a hit.

Middle of each band; days won (worst party) / F1 Down / F1 Wounded /
rounds / acts again:

| Level | v3 as adopted | buyback | picks | mixed |
|---|---|---|---|---|
| 1 | 95 (90) / 13 / 42 / 3.7 / 38 | 94 (90) / 14 / 47 / 3.9 / 41 | 91 (84) / 20 / 50 / 5.0 / 48 | 94 (88) / 15 / 41 / 3.9 / 41 |
| 2 | 95 (83) / 13 / 40 / 3.7 / 40 | 97 (93) / 11 / 39 / 3.8 / 43 | 96 (90) / 14 / 37 / 4.6 / 48 | 97 (88) / 13 / 36 / 3.9 / 43 |
| 3 | 95 (78) / 14 / 43 / 3.3 / 37 | 96 (85) / 12 / 39 / 3.5 / 40 | 96 (82) / 10 / 35 / 3.9 / 45 | 96 (85) / 10 / 35 / 3.4 / 41 |
| 4 | 95 (82) / 15 / 44 / 3.8 / 50 | 97 (90) / 12 / 38 / 3.9 / 53 | 97 (86) / 10 / 31 / 4.4 / 59 | 97 (90) / 10 / 32 / 3.9 / 53 |
| 5 | 97 (88) / 13 / 44 / 4.0 / 51 | 99 (93) / 10 / 37 / 4.2 / 55 | 97 (92) / 8 / 29 / 5.1 / 60 | 99 (95) / 8 / 33 / 4.2 / 54 |

- **The prune holds.** With the stats bought back, every Level plays
  about as v3 did, a little softer (the weakest party does better),
  mostly from Striker giving up its 2 Accuracy.
- **Spending the budget on mechanics lengthens fights** to 4-5 rounds
  (3.9-5.1) and a hit enemy acts again 45-60% of the time. That's the
  first table to land on the designer's 4-5 rounds. Toughness picks
  (Omniguard, Durable, Grappling, Reflexes) keep enemies up; less damage
  per hit keeps the party up longer too.
- **It's uneven across Levels.** Level 1 gets harder (91% of days,
  someone Down in a fifth of fights; Level 1 parties have the least to
  answer debuffs with), Levels 3-5 softer (Down 8-10%, Wounded 29-35%).
- **Mixed plays like buyback**, a notch softer at Levels 3-5.

**Open:** whether *picks* is the shape to tune toward. If so, Levels 3-5
want a little more offense (a budget of 8 there, or Accuracy back on
the table from Level 3) and Level 1 a little less. Should Heavy and
Powerful Weapon merge into one equipment entry, and should it be a PC's
two-hander (Damage +2, Accuracy −1, no weapon Defense)? Should the
catalog's Enhanced Health be +1 or +3?

### Building an enemy on paper: loadouts, stacking effects, the budget by Level (2026-11-04)

The designer's direction for the pruned v3, round two:

- **It has to work on paper.** The game is meant to be a book, like any
  tabletop game. Building an enemy should be a series of "pick from this
  list" steps, penciled in and tallied at the end. Once the numbers are
  settled, simplify the builder back down to that. A "monster manual" of
  varied stat blocks is the test of it.
- **The weapon is a loadout, not an Ability.** An enemy in melee is
  presumed to carry a sword and shield. The choices are heavy versus
  light and two-handed versus a shield, alongside bows and spells. The
  loadout is what the enemy does with its turn. Powerful Weapon and
  Powerful Spell become plain extra damage, bought once.
- **Some Abilities once, some again and again.** Damage +1 (the buy-back)
  and Powerful Weapon or Spell once. Stats, defense bonuses and on-hit
  effects can be bought repeatedly. On-hit stacks stop at 3-4 ("anything
  more than that is probably egregious"); an archer that lands 3
  Crippled should swing the fight, and the players can wait it out or
  pack a counter.
- **The budget is the lever.** If a Level's enemies come out weak against
  what the players get there, give them more points to spend.

**The steps** (`V3_VERSION = 3`; the sim's `sample_enemies.csv` rows
PrunedAction / PrunedPicks / PrunedExtra):

1. Level and Slots: the base table (the pruned v3 table above).
2. Archetype: its bumps (additive, above).
3. Loadout (the Action), and armor.
4. Strong and Weak Defense.
5. Spend the Ability budget: 6 / 7 / 9 / 9 / 9 points at Levels 1-5, per
   Slot. Unspent points are Health.

**Loadouts** (worth per enemy in Health against Sword and Shield,
`kit_check.py` `action:` variants on the melee enemies; the numbers are
the PC weapon table's):

| Loadout | Accuracy | Damage | Parry (weapon Defense) | Price |
|---|---|---|---|---|
| Sword and Shield (default) | +1 | 3 | +2 (shield) | 0 |
| Heavy Weapon and Shield | +0 | 4 | +2 | 1 (read 1.3) |
| Light Two-Handed | +1 | 4 | +1 | 2 (read 4.5) |
| Two-Handed Weapon | +0 | 5 | +0 | 2 (read 3.7) |
| Bow / Heavy Bow | +1 / +0 | 3 / 4 | none | 0 / 1 |
| Melee, Ranged or Vital Spell | +0 | 2 | none | 0 |
| Support (Shield Ally, Mend Ally...) with a backup weapon | | | | 0 |

Gear is priced under what it measured (designer, 2026-11-04). At its
measured 4, a two-hander cost the same as Damage +1 and gave up the
shield's Parry besides, so it only made sense alongside Damage +1. Players
get the same kit for a nominal Might investment, so better kit should be a
cheap upgrade for an enemy too, even if it comes out a little better on
paper: two-handers 2, the heavy one-hander and heavy bow 1. With the
Brute's two-hander 2 points cheaper, every Level plays a point or so
harder: 94 / 95 / 90 / 93 / 92% of days won, Down 14-18%, Wounded 40-46%,
4.3-5.2 rounds, acts again 43-60 (`v3p_tune.txt`, "gear cheaper").

A quick pass on the kit itself (same budget, `v3p_tune.txt`): with heavy
kit free, every sword-and-shield enemy on a heavy weapon and shield and
the archer on a heavy bow cost the party 4-7 points of days won at every
Level (86-90%, Down about a fifth), so those two went back to 1. Every
melee enemy on a two-hander at 2 left days about where they were (91-96%)
with Down a few points up and fights 0.7 rounds shorter (no shield, 2
Health spent), so 2 stands.

**Is Accuracy worth more to a debuff-heavy enemy?** In principle yes (an
effect only lands on a hit), but not in the sim yet. Accuracy +1 reads
2.1 / 3.7 Health on the bought-back roster and 1.5 / 1.9 on the
redesigned one (`v3p_acc_*.txt`). The light effects read small a stack,
and an enemy that didn't buy its Damage back hits for less, so each
extra hit carries less. If the balance-weights pass values the effects
higher, Accuracy rises with them. Damage +1 reads 3.4-5.6 on either.

**On-hit effects, a stack a pick, up to 4** (worth per enemy, Levels
2 / 3, at 1 / 2 / 4 stacks):

| Effect | 1 stack | 2 stacks | 4 stacks | Price a stack |
|---|---|---|---|---|
| Crippled | 0.3 / 0.2 | 0.9 / 0.5 | 2.5 / 1.8 | ½ |
| Vulnerable | 0.1 / 0.3 | 0.3 / 0.7 | 0.6 / 1.5 | ½ |
| Slowed | 0.0 / 0.1 | 0.1 / 0.4 | 0.2 / 0.8 | ½ |
| Frightened | 0.2 / 0.2 | 0.3 / 0.2 | 0.3 / 0.2 | ½ |
| Taunted | 0.2 / 0.4 | 0.2 / 0.4 | 0.2 / 0.4 | ½ |
| Necrotic | 0.6 / 0.7 | 1.4 / 1.1 | 2.0 / 1.6 | ½ |
| Harried | 0.8 / 1.0 | 1.5 / 1.6 | 2.3 / 2.4 | 1 |
| Bleeding (Poison) | 2.3 / 3.2 | 3.5 / 5.1 | — | 2½ |

Crippled grows faster than a stack at a time, which fits the designer's
read that a big stack should swing a fight. Frightened and Taunted do
all they do with one stack in the sim (whoever is Frightened or Taunted
is, however many stacks), so a second stack only lasts longer. The
light effects read small in the sim, which may undervalue them; that's
for the balance-weights pass.

**Other Abilities** (prices for the pruned v3,
`enemy_builder_pcstyle.ABILITY_HEALTH_V3P`):

- *Once:* Damage +1 (4), Powerful Weapon (4; +1 Damage on weapon
  attacks, read 4.4), Powerful Spell (3; +1 on spells, read 2.6),
  Enhanced Range (3), Attunement (3), Improved Support, Durable,
  Omniguard, Resist (an element), Action (Parting Shot), Action
  (Taunting) (1 each), Retribution Aura, Battering, Cleaving, Enhanced
  Reflexes (2), Grappling (3).
- *Again and again, up to the player caps:* Accuracy +1 (2), Parry and
  Dodge +1 (1), Vital/Mental/Vigilant +1 (1), Resist +1 (4),
  Enhanced Health (1), Enhanced Speed (1).
- *Armor:* Unarmored −1, Light 0, Medium 1, Heavy 2.

**The roster on paper**, as redesigned (the extra points at Levels 3-5
go to Accuracy +1 first):

| Enemy | Archetype | Loadout, armor | Picks |
|---|---|---|---|
| Brute | Bruiser | Two-Handed Weapon, Light (Medium at 3) | Accuracy +1, Crippling ×2 |
| Hedge Knight | Defender | Sword and Shield, Medium (Heavy at 3) | Accuracy +1, Taunting ×2, Action (Taunting), Omniguard, Harrying |
| Skulking Footpad | Skirmisher | Sword and Shield, Light | Poison (Bleeding), Accuracy +1, Parting Shot, Slowing ×2 |
| Marsh Archer | Striker | Bow, Light | Accuracy +1, Enhanced Range, Crippling ×2, Vulnerable ×2 |
| Grave Caller | Striker | Vital Spell, Unarmored | Powerful Spell, Accuracy +1, Necrotic ×2, Vulnerable ×2 |
| Ember Caster | Striker | Ranged Spell, Unarmored | Powerful Spell, Accuracy +1, Attunement (Fire) |
| Warpriest | Backup | Shield Ally (mace backup), Medium | Improved Support, Durable, Accuracy +1, Frightening ×2, Harrying |

At Level 3 that comes to (Accuracy before the weapon's own +1 is in the
Acc column already):

| Enemy | Acc | Damage | Parry | Dodge | Vital | Mental | Resist (P / E) | Health | Speed |
|---|---|---|---|---|---|---|---|---|---|
| Brute | 6 | 8 | 14 | 11 | 16 | 10 | 5 / 3 | 13 | 4 |
| Hedge Knight | 7 | 5 | 18 | 13 | 14 | 10 | 7 / 4 | 12 | 3 |
| Skulking Footpad | 8 | 5 | 16 | 16 | 12 | 10 | 4 / 3 | 14 | 6 |
| Marsh Archer | 7 | 6 | — | 14 | 12 | 10 | 4 / 3 | 13 | 5 |
| Grave Caller | 6 | 6 Shadow | — | 12 | 10 | 14 | 3 / 3 | 14 | 5 |
| Ember Caster | 6 | 6 Fire | — | 12 | 10 | 14 | 3 / 3 | 13 | 5 |
| Warpriest | 6 (mace) | 5 | 12 | 11 | 14 | 16 | 6 / 4 | 13 | 4 |

**Tuning the budget** (`pruned_tune.py`, middle of each band; days won
(worst party) / F1 Down / F1 Wounded / rounds / acts again):

| Level | 7 points | extra on the row's own picks | extra on offense first |
|---|---|---|---|
| 1 | 91 (80) / 19 / 47 / 4.9 / 44 | −1: 94 (87) / 17 / 45 / 4.5 / 41 | |
| 2 | 95 (90) / 13 / 39 / 4.6 / 47 | | |
| 3 | 96 (80) / 8 / 34 / 4.1 / 44 | +1: 89 (69) / 11 / 36 / 4.6 / 45 | +2: 91 (66) / 15 / 45 / 4.2 / 46 |
| 4 | 97 (87) / 10 / 32 / 4.6 / 57 | +1: 92 (77) / 12 / 34 / 5.1 / 59 | +2: 94 (80) / 14 / 41 / 4.6 / 57 |
| 5 | 95 (73) / 8 / 34 / 5.0 / 57 | +1: 90 (68) / 11 / 36 / 5.5 / 59 | +2: 92 (72) / 13 / 44 / 5.1 / 58 |

(Level 1 at 7 points is from the run before Necrotic and Bleeding were
repriced; the rest are after. +4 and +6 on offense went too far: 74-82%
of days, Down about a fifth to a third.)

- **At 7 points, Levels 3-5 were soft inside a fight** (Down 8-10%,
  Wounded about a third) while winning 95-97% of days.
- **Extra points on the rows' own mechanics lengthen fights** (to 5-5.5
  rounds) and cost the party days faster than they raise the stakes in
  a fight: more Crippled and better defenses grind.
- **Extra points on offense first** raise Down and Wounded to target
  without lengthening fights. Two points (Accuracy +1) at Levels 3-5
  land every reading near its target; the day rate sits a couple of
  points under 93 at Levels 3 and 5, and the weakest party feels it.
- **Level 1 plays best a point lighter** (6 points).

So the budget runs **6 / 7 / 9 / 9 / 9** (`tunables.V3_PRUNED_EXTRA`).
In practice the extra at Levels 3-5 is the Accuracy the base table gave
up, which says a pruned enemy at those Levels should usually buy its
Accuracy back.

The designer made the pruned v3 the default on 2026-11-04
(`tunables.V3_VERSION = 3`). The prices are measured against the sample parties and
get their review against the balance weights next, the light on-hit
effects first. Levels 4-5 are still read against grown Level 3
characters.

**Across each band, as the default** (`table_check.py -t v3 -n 60`,
`results/enemy_stats/v3p_table_check.txt`; days won (worst party) / F1
Down / F1 Wounded / rounds / acts again):

| Level | Bottom | Middle | Top |
|---|---|---|---|
| 1 | — | 94 (87) / 18 / 45 / 4.6 / 43 | — |
| 2 | 32 (10) / 61 / 80 / 6.4 / 60 | 95 (90) / 14 / 40 / 4.8 / 49 | 100 (98) / 4 / 21 / 3.7 / 44 |
| 3 | 36 (10) / 53 / 78 / 6.2 / 65 | 90 (64) / 16 / 46 / 4.3 / 48 | 100 (98) / 4 / 19 / 3.3 / 39 |
| 4 | 48 (11) / 44 / 72 / 5.8 / 64 | 93 (79) / 14 / 42 / 4.7 / 59 | 99 (93) / 8 / 32 / 4.6 / 56 |
| 5 | 89 (69) / 18 / 50 / 5.2 / 60 | 92 (72) / 14 / 46 / 5.2 / 60 | 92 (68) / 13 / 42 / 5.1 / 60 |

The middle of every band is close: 90-95% of days, Down 14-18%,
Wounded 40-46%, 4.3-5.2 rounds, acts again 43-60%. Level 3 is the
hardest of them (90%, the weakest party 64%). The bottom of each band is
harsher than v3 as adopted on 11-03 (a third of days at Levels 2-3
against 42-48%), the top as comfortable. Level 5 is flat across its band
because its parties are the Level 3 characters grown, which reach the caps;
that's the yardstick running out, not the enemies.

### A little more dangerous: the budget against weak and strong parties (2026-11-04)

The designer: project it slightly more dangerous for the party, since real
players will build for synergy, coordinate, and have their items, and
even a strong party in the sim shouldn't win every day. Weak against
strong is the eight test parties in the middle of each band (`bc.parties`:
picked across all 210 four-character mixes the optimizer ranked, weakest
to strongest), so the best of them is the strongest mix known.
`pruned_tune.py`, every Level's budget raised together, extra on offense
first (`results/enemy_stats/v3p_danger.txt`):

| Budget (Levels 1-5) | Days won, average | weakest party | strongest | second strongest | Down | Wounded | Rounds |
|---|---|---|---|---|---|---|---|
| 6 / 7 / 9 / 9 / 9 | 90-95% | 30-90% | 99-100% | 96-99% | 14-18% | 40-46% | 4.3-5.2 |
| 7 / 8 / 10 / 10 / 10 | 82-90% | 27-69% | 98-100% | 89-98% | 18-21% | 44-51% | 4.9-5.7 |
| 8 / 9 / 11 / 11 / 11 | 79-89% | 22-77% | 95-100% | 90-99% | 19-24% | 47-53% | 4.9-5.9 |
| 9 / 10 / 12 / 12 / 12 | 70-80% | 15-60% | 91-100% | 85-95% | 23-29% | 52-60% | 5.2-6.2 |
| 10 / 11 / 13 / 13 / 13 | 71-75% | 11-52% | 88-100% | 80-95% | 31-33% | 56-65% | 4.6-6.0 |

(Level 1's weakest is a sample party built far under the others.)

- **One composition shrugs it off.** Hilde, Sable and Hanforth with Felix
  or Carrick win 98-100% of days at every budget tried, while the next
  best drop to 85% at Level 3 by +3. Raising the enemies can't make that
  party lose without crushing everyone else (the average at 70-75%). It's
  a party-side outlier for the PC balance pass, not an enemy setting.
- **Synergy is mostly the sum of the parts.** Over all 210 mixes
  (`hall_of_fame/runs_levelup/mixes_l*.json`, from the optimizer's runs
  on an older enemy table), adding up each character's own worth explains
  95% of the differences between parties; pairs add or take little
  beyond that. Sable, Hilde, Hanforth and Carrick are the strongest
  members, Ashleigh and Enith the weakest. The sim's characters don't
  coordinate the way players do, which is the designer's point.
- **+1 everywhere** (7 / 8 / 10 / 10 / 10) is the default since: the
  average party wins 82-90% of days, someone is Down in about a fifth
  of fights and Wounded in about half, and every strong party but the
  outlier loses a day now and then. Fights run a little long, 4.9-5.7
  rounds.

### The monster manual in fights (2026-11-05)

The designer, after reviewing the draft manual: trim the hexes and put
their budget elsewhere (Hex stacks 2 / 2 / 3 / 3 / 4 at Levels 1-5, and
the Hex loadout gives 2 points back), and limit the poison stackers,
since poisons outlast the fight (a Poison effect stops at 2 picks). Then
a broad test: `experiments/enemies/manual_check.py` draws 40 encounters
a Level from the manual by the encounter rules (Slots equal to the
party's four, two stat blocks usually, three sometimes, at most one
enemy that doesn't attack, the solo boss alone from Level 3), and every
test party in the middle of the band fights each one fresh 60 times
(`results/enemy_stats/manual_check.txt`).

| Level | Manual: lose / Down / Wounded / rounds / acts again | The four old mixes |
|---|---|---|
| 1 | 12% / 26% / 46% / 6.5 / 50% | 5% / 27% / 53% / 5.3 / 46% |
| 2 | 6% / 14% / 31% / 6.8 / 57% | 4% / 18% / 42% / 6.0 / 52% |
| 3 | 8% / 17% / 40% / 6.4 / 56% | 5% / 19% / 49% / 5.9 / 49% |
| 4 | 5% / 13% / 31% / 6.5 / 62% | |
| 5 | 5% / 14% / 33% / 6.2 / 62% | |

(Fresh single fights, so these read harder on losses and longer than the
day standard's numbers elsewhere.) On average the manual plays close to
the four mixes the table was tuned on, a little longer and, at Level 1,
a little deadlier. Hilde, Sable and Hanforth's party is still the
strongest at every Level (lose 0.5-2%, Down 5-9%).

**Each monster's share** (an encounter's reading, against its Level's
average, fitted to the share of the encounter's Slots each monster
fills; read as "a whole encounter of this monster", in points of fights
lost or with someone Down, and in rounds):

| Monster | Down | Lose | Rounds |
|---|---|---|---|
| Ironbranch Warden | +57 | +56 | +10 |
| Brute Warlord (solo) | +54 | +59 | +10 |
| Iron Sentinel | +46 | +49 | +17 |
| Crossbow Sniper | +27 | +2 | −1 |
| Grave Caller | +21 | −10 | −4 |
| Marsh Archer | +17 | −6 | −2 |
| Mind Lash Adept | +15 | −8 | −4 |
| ... the middle (Goblin Cutthroat to Thornhide Brute) | +9 to −7 | | |
| Warpriest | −20 | +9 | +8 |
| Shade Stalker | −23 | −14 | −3 |
| Fen Warden | −23 | −12 | −3 |
| Mire Witch | −24 | −5 | −4 |
| Bog Skirmisher | −24 | −13 | −1 |
| Deadbough Priest | −27 | +11 | +6 |
| Bog Hexer | −30 | −5 | 0 |
| Curse Weaver | −43 | −13 | −7 |
| Field Medic | −55 | −26 | −2 |

What it says:

- **Stacked defense is worth far more than its parts.** The two heavy
  walls (Heavy Armor, a shield's Parry, Parry and Dodge bought on top,
  Durable, Resilient, Sturdy) are the strongest monsters by a distance:
  fights against three of them run 15 rounds or more and the party
  loses a third to all of the time. Each +1 to Parry or Dodge read about
  half a Health alone, but piled on one body the party's hit chance
  falls off a cliff. That's the first effect to reprice: a Defense
  bought on top of armor and a shield should cost more, or the stat
  picks stop at once each.
- **Ranged Assassins with Vulnerable spike.** Crossbow Sniper, Grave
  Caller, Marsh Archer and the Mind Lash Adept put someone Down far more
  often (+15 to +27) without winning more fights: they focus the
  softest PC and open them up.
- **Kiting makes an enemy nearly harmless.** Every Kiting monster sits
  near the bottom. Four Bog Skirmishers put someone Down in 0% of fights
  Kiting, 3% Hitting Whatever and 30% as Assassins; Shade Stalkers 1%,
  17% and 30% (Level 3, 60 fights a party). As the sim plays it, a
  kiter spends its turns moving away and spreads its damage thin. That's
  either the sim's Kiting or the tactic itself, and worth deciding
  before any kiter is priced.
- **Supports and hexers trade Downs for length.** The healers and the
  Warpriest cut Downs (they don't attack) but make fights longer and
  lose the party more of them (+9 to +11). The trimmed hexers and the
  Curse Weaver now do little: −30 and −43 on Downs, about even on
  losses. The Field Medic is the weakest monster in the book (a
  Kiting healer whose heals don't cover what its party loses).
- **The solo boss is a boss.** The Brute Warlord alone downs someone in
  about 70% of fights and wins a third of them at Levels 3-5.

**Open, before the wide PC-against-enemy test:** price stacked defense
(or cap the stat picks); decide Kiting; give the healers and hexers
something back; and whether the solo boss should be as dangerous as it
is.

**Monster Defenses without any Defense picks, against the PCs**
(2026-11-05, the designer's question: with the Strong and Weak Defense and
the weapon's Parry alone, how close do monsters get to player numbers?
Every manual monster with Parry and Dodge +1, Vital/Mental/Vigilant +1
and Resist picks taken out, against every distinct PC in the test parties
in the middle of the band; average and range,
`results/enemy_stats/v3p_defense_vs_pcs.txt`):

| Level | | Better of Parry / Dodge | Vital | Mental | Physical Resist |
|---|---|---|---|---|---|
| 1 | PCs | 13.4 (12-16) | 11.4 (10-13) | 11.3 (10-13) | 3.3 (2-4) |
| | monsters | 12.3 (10-16) | 10.5 (8-14) | 10.4 (8-14) | 3.4 (2-6) |
| 2 | PCs | 14.9 (12-16) | 12.7 (11-14) | 12.3 (12-13) | 4.4 (3-6) |
| | monsters | 13.3 (11-17) | 11.5 (9-15) | 11.4 (9-15) | 4.4 (3-7) |
| 3 | PCs | 15.9 (12-19) | 14.2 (13-15) | 12.9 (12-14) | 4.3 (4-5) |
| | monsters | 14.3 (12-18) | 12.5 (10-16) | 12.4 (10-16) | 4.4 (3-7) |
| 4 | PCs | 17.8 (14-20) | 15.3 (13-17) | 13.3 (12-15) | 5.9 (5-6) |
| | monsters | 15.3 (13-19) | 13.5 (11-17) | 13.4 (11-17) | 5.4 (4-8) |
| 5 | PCs | 18.1 (15-20) | 16.2 (15-18) | 16.0 (15-18) | 6.3 (6-8) |
| | monsters | 16.3 (14-20) | 14.5 (12-18) | 14.4 (12-18) | 5.4 (4-8) |

Without picks the average monster sits 1-2 under the average PC on its
best Defense and its Vital and Mental (2-2.5 at Levels 4-5, where the
PCs are grown Level 3 characters), with about the same Physical Resist,
and the ranges overlap: a shield-carrying Defender matches the best PC
Parry (18 at Level 3). That corrects the walls reading above. The
Ironbranch Warden and Iron Sentinel bought only one or two Defense picks
between them (Parry 19-20 built, 18 without); what sets them apart is
Physical Resist 7 at Level 3 from Heavy Armor and the Defender's +1, above
any PC's (4-5), on top of a shield Defender's Parry. Physical weapons do
little to them, so the fight grinds. The thing to price is heavy armor on
a Defender, more than the Defense picks.

**What armor is worth on the pruned base** (2026-11-05, the designer: how
to price Heavy against Medium and Unarmored; `kit_check.py`, every
full-size enemy in the four mixes put in each armor, then also made a
Defender, Levels 2 / 3, `results/enemy_stats/v3p_armor.txt`; readings
put back into worth by adding the price paid, and compared with Light):

| Armor | Worth against Light, any enemy | Rounds | On a Defender | Rounds |
|---|---|---|---|---|
| Unarmored (Resist +0) | −1.7 / −1.8 | −0.8 / −0.5 | | |
| Light (Resist +1) | 0 | 0 | 0 | 0 |
| Medium (Resist +2, Dodge −1) | +2.4 / +1.1 | +1.5 / +0.4 | +3.7 / +2.5 | +2.6 / +1.0 |
| Heavy (Resist +3, Dodge −1, Speed −1) | +4.9 / +3.7 | +3.6 / +1.9 | +7.8 / +6.1 | +5.9 / +3.6 |

So the steps are about 2 Health each (Unarmored about −2, Medium +2,
Heavy +4, against the current −1 / 1 / 2), and they compound on a
Defender: its Resist +1 and Parry/Dodge +2 on top of Heavy Armor are
worth about 7 against Light, and add 4-6 rounds. That's the walls.

**Armor at −2 / 0 / 2 / 4** (the designer's test, 2026-11-05;
`results/enemy_stats/v3p_armor_prices.txt`, `manual_check_armor.txt`).
The roster, middle of each band (days won (worst / best party) / Down /
Wounded / rounds), against the same budget at the old armor prices:

| Level | Armor −2 / 0 / 2 / 4 | Armor −1 / 0 / 1 / 2 |
|---|---|---|
| 1 | 90 (79 / 98) / 22 / 51 / 5.0 | 90 (79 / 98) / 21 / 49 / 5.1 |
| 2 | 87 (73 / 100) / 19 / 44 / 5.4 | 86 (68 / 100) / 19 / 44 / 5.6 |
| 3 | 85 (55 / 100) / 19 / 48 / 4.6 | 82 (53 / 100) / 19 / 49 / 4.9 |
| 4 | 86 (65 / 100) / 19 / 46 / 5.1 | 85 (69 / 100) / 18 / 47 / 5.4 |
| 5 | 85 (69 / 99) / 20 / 50 / 5.4 | 82 (63 / 99) / 20 / 51 / 5.7 |

The roster barely moves (a point or three easier at Levels 3 and 5, fights
a little shorter): its armored enemies lose a Health or two and the
unarmored casters gain one. In the manual's broad test, encounters lose
the party 1.5-2 points fewer fights at every Level (10 / 4 / 5 / 3 / 4%),
and the walls come down but stay on top: the Ironbranch Warden from +57
to +42 on Downs and +56 to +40 on losses, the Iron Sentinel from +46 to
+33 and +49 to +37, and from +17 to +14 rounds. The unarmored ranged
Assassins rise a little (Grave Caller +21 to +29 on Downs). Pricing armor
at its worth helps the walls by about a quarter; what's left is the
Defender's own Resist +1 on top of Heavy Armor.

**The Defender's Resist +1 swapped for Health** (the designer, 2026-11-05:
"+1 Health, or maybe +2, play with those numbers"). Priced against the
other archetypes on the pruned base (`results/enemy_stats/v3p_defender.txt`,
worth in Health per Slot at Levels 2 / 3, extra rounds): the others read
1.7-3.6, about 2.6 on average. The Defender with Resist +1 read 4.5 / 3.3
and +3-4 rounds; with Health +1 1.3 / 1.2; +2 2.0 / 1.8; +3 2.7 / 2.6 and
+2-3 rounds. So Health +3 sits at the average and still makes the Defender
the archetype that lengthens fights.

In the manual's broad test (with armor at −2 / 0 / 2 / 4), the walls fall
back among the ordinary threats (Down / lose / rounds, a whole encounter
against the average):

| | Resist +1 | Health +3 | Health +2 |
|---|---|---|---|
| Ironbranch Warden | +42 / +40 / +8 | +25 / +21 / +5 | +18 / +16 / +4 |
| Iron Sentinel | +33 / +37 / +14 | +15 / +17 / +8 | +10 / +14 / +7 |
| Hedge Knight | −3 / +7 / +4 | −6 / +2 / +2 | −7 / +1 / +1 |
| Encounters lost, Levels 1-5 | 10 / 4 / 5 / 3 / 4% | 6 / 2 / 3 / 2 / 3% | 5 / 1 / 3 / 2 / 3% |

With Health +3 the Ironbranch Warden sits next to the ranged Assassins
(+22 to +32 on Downs) rather than above them; the solo boss is the only
outlier left. The roster, middle of each band, wins 89-91% of days with
Health +3 (85-90% with Resist +1), Down 17-21%, Wounded 42-50%, 4.3-5.3
rounds (`v3p_defender_band.txt`), a few points easier than the "notch
more dangerous" setting, since the Shield Wall's Hedge Knights were part
of what made it so.

**Health +3 is the default** (designer's call to play with the numbers;
it's the one priced like the rest).

**A point more budget at Levels 2-5** (the designer's test, 2026-11-05),
to win back the danger the Defender's Health +3 took off. Budget 7 / 9 /
11 / 11 / 11; the roster, middle of each band (days won (worst / best
party) / Down / Wounded / rounds / acts again):

| Level | 7 / 9 / 11 / 11 / 11 | 7 / 8 / 10 / 10 / 10 |
|---|---|---|
| 1 | 91 (83 / 98) / 21 / 50 / 4.7 / 49 | 91 (83 / 98) / 21 / 50 / 4.7 / 49 |
| 2 | 92 (83 / 100) / 19 / 48 / 4.5 / 52 | 91 (78 / 100) / 17 / 42 / 5.0 / 53 |
| 3 | 87 (55 / 100) / 21 / 52 / 4.5 / 51 | 89 (60 / 100) / 19 / 48 / 4.3 / 49 |
| 4 | 87 (60 / 100) / 20 / 47 / 5.2 / 63 | 89 (67 / 100) / 19 / 46 / 5.0 / 62 |
| 5 | 86 (65 / 99) / 21 / 51 / 5.6 / 64 | 89 (71 / 99) / 19 / 49 / 5.3 / 62 |

Levels 3-5 are back at the notch-more-dangerous setting (86-87% of days,
Down a fifth, Wounded about half); Level 2 barely moves (its second extra
point buys Accuracy +1, and the Shield Wall's Hedge Knights pay for their
Medium Armor). In the manual's broad test encounters lose the party
2 / 4 / 2 / 3% at Levels 2-5 (from 1.5 / 3 / 1.7 / 2.6%), and the order of
the monsters doesn't change. The strongest party still wins 99-100% of
days. This is the default.

### Battle Tactics in the sim (2026-11-05)

The designer: look into Kiting, and all the tactics, and say which stand
out. How the sim plays them (`tactics.py`, `combat_sim.spend_movement_ap`):

- **Hit Whatever** goes for the closest PC (with movement on).
- **Assassin** goes for the softest: the PC hurt worst for their size,
  then the lightest armor (`tunables.ASSASSIN_READS = 'softest'`).
- **Kiting** goes for the closest PC and, every turn, spends one move
  action stepping straight away from them, whether anyone is near or not.
  At 4 AP that leaves one attack a turn where everyone else makes two.
- **Hold the Line, Vanguard and Triage aren't modeled:** they play as Hit
  Whatever. (Supports pick whom to help by their own rule.)

`experiments/enemies/tactic_check.py`: every attacking manual monster,
four of itself (eight minions, two elites) at Level 3, under each tactic,
against every test party in the middle of the band, 40 fresh fights each.
Kiting is played as coded ('always') and with a test rule that backs off
only from a PC already in melee reach, otherwise closing to range and
attacking like anyone else (`tunables.KITING_MOVE = 'engaged'`). Fights
lost / with someone Down (%) / rounds:

| Monster | Hit Whatever | Assassin | Kiting (always) | Kiting (engaged) |
|---|---|---|---|---|
| Hedge Knight | 0 / 3 / 7.1 | 1 / 18 / 7.6 | 0 / 0 / 8.4 | 0 / 0 / 8.4 |
| Ironbranch Warden | 32 / 49 / 12.8 | 29 / 59 / 12.7 | 5 / 3 / 11.7 | 6 / 6 / 12.3 |
| Iron Sentinel | 43 / 59 / 16.1 | 40 / 73 / 16.6 | 6 / 1 / 16.8 | 7 / 2 / 16.8 |
| Shieldbearer | 0 / 7 / 5.9 | 2 / 36 / 6.5 | 0 / 0 / 6.9 | 0 / 0 / 7.0 |
| Marsh Archer | 0 / 11 / 4.0 | 0 / 54 / 4.3 | 0 / 0 / 4.2 | 0 / 10 / 4.3 |
| Crossbow Sniper | 0 / 18 / 3.8 | 0 / 59 / 4.3 | 0 / 3 / 4.3 | 0 / 18 / 4.0 |
| Glaive Dancer | 0 / 8 / 3.4 | 0 / 25 / 3.5 | 0 / 0 / 3.9 | 0 / 0 / 3.9 |
| Executioner | 0 / 8 / 3.4 | 0 / 14 / 3.4 | 0 / 0 / 4.0 | 0 / 0 / 4.0 |
| Grave Caller | 7 / 48 / 3.7 | 8 / 70 / 3.8 | 0 / 8 / 3.9 | 2 / 40 / 4.1 |
| Ember Caster | 2 / 42 / 4.2 | 4 / 62 / 4.2 | 1 / 4 / 4.5 | 1 / 32 / 4.6 |
| Cinder Adept | 3 / 21 / 4.9 | 5 / 42 / 4.7 | 0 / 2 / 4.6 | 0 / 14 / 4.8 |
| Mind Lash Adept | 11 / 53 / 3.9 | 11 / 71 / 3.9 | 0 / 5 / 3.9 | 2 / 43 / 4.4 |
| Goblin Cutthroat | 0 / 20 / 3.6 | 0 / 54 / 3.7 | 0 / 0 / 4.0 | 0 / 0 / 4.0 |
| Brute | 2 / 13 / 4.5 | 1 / 36 / 4.5 | 0 / 0 / 4.4 | 0 / 0 / 4.5 |
| Thornhide Brute | 3 / 12 / 4.4 | 1 / 30 / 4.4 | 0 / 0 / 4.6 | 0 / 0 / 4.7 |
| Gravel Ogre | 0 / 11 / 4.3 | 0 / 17 / 4.4 | 0 / 0 / 5.1 | 0 / 0 / 5.1 |
| Warleader | 0 / 1 / 4.0 | 0 / 13 / 4.2 | 0 / 0 / 4.7 | 0 / 0 / 4.7 |
| Fen Warden | 0 / 7 / 3.6 | 0 / 5 / 3.6 | 0 / 0 / 4.3 | 0 / 0 / 4.3 |
| Skulking Footpad | 0 / 5 / 3.4 | 0 / 18 / 3.5 | 0 / 0 / 4.3 | 0 / 0 / 4.3 |
| Shade Stalker | 1 / 24 / 5.1 | 2 / 34 / 4.7 | 0 / 2 / 4.7 | 0 / 14 / 5.0 |
| Bog Skirmisher | 1 / 4 / 6.3 | 0 / 35 / 5.8 | 0 / 0 / 5.4 | 1 / 5 / 6.9 |
| Hunting Hound | 4 / 23 / 4.2 | 1 / 42 / 3.9 | 0 / 0 / 4.1 | 0 / 0 / 4.1 |

What stands out:

- **Kiting as coded makes anything nearly harmless.** Someone goes Down in
  0-8% of fights against every monster, and even the walls' losses drop
  from 32-43% to 5-6%. Half the attacks, all of them at the front line.
- **Kiting backing off only when engaged** puts the ranged monsters and
  casters back where they'd be as Hit Whatever, a little under (Grave
  Caller Down 40% against 48, Ember Caster 32 against 42, Mind Lash Adept
  43 against 53, Crossbow Sniper 18 against 18). It's a ranged tactic:
  a melee monster that backs off from melee does nothing either way.
- **Assassin is the strongest tactic by a distance, on Downs.** Against
  Hit Whatever it puts someone Down two to five times as often with
  almost every monster (Marsh Archer 11% to 54%, Goblin Cutthroat 20% to
  54%, Brute 13% to 36%, Shieldbearer 7% to 36%), while losses barely
  move. Hit Whatever spends itself on whoever stands closest, usually
  the armored front; Assassin picks off the soft back line. As a free
  pick it's worth more than most Abilities.
- **The walls win on durability, not tactics:** 29-43% losses under Hit
  Whatever or Assassin alike.

**Open:** play Kiting as "back off when engaged" (what the table's
"keeps max range" suggests); whether Assassin should cost something, or
be the tactic the GM reaches for on purpose; and modeling Hold the Line
(the most aggressive PC) and Vanguard (whoever is attacking the back
line), so they stop reading as Hit Whatever.

**Kiting when engaged, Hold the Line and Vanguard, as the default**
(designer, 2026-11-05: switch Kiting to engaged and model the other two;
"none of these should conflict with good tactics like double-tapping",
they're a quick reference so GMs can run the game smoothly). A tactic
only picks the target: every enemy still moves and attacks twice as
any enemy does.

- **Kiting** backs off only from a PC in melee reach; otherwise it closes
  to range and attacks like anyone else (`tunables.KITING_MOVE = 'engaged'`).
- **Hold the Line** attacks the PC who has dealt its side the most damage
  this fight; the closest on a tie or before anyone has.
- **Vanguard** attacks the PC who has dealt the most damage to its side's
  back line this fight (ranged attackers, healers, hexers); the closest
  on a tie or before anyone has.

The four mixes the table was tuned on use none of the three, and play
byte-identically. `tactic_check.py --mixed`: each monster fills half the
Slots beside two Ember Casters (two Hedge Knights for the Ember Caster),
only its own tactic changing, Level 3, every test party, 40 fresh fights
(`results/enemy_stats/tactic_check_mixed.txt`; fights lost / with someone
Down (%) / rounds):

| Monster | Hit Whatever | Assassin | Kiting | Hold the Line | Vanguard |
|---|---|---|---|---|---|
| Hedge Knight | 3 / 20 / 4.8 | 2 / 20 / 4.6 | 1 / 5 / 5.1 | 2 / 20 / 4.5 | 4 / 21 / 4.9 |
| Ironbranch Warden | 5 / 22 / 5.5 | 4 / 25 / 5.5 | 3 / 4 / 6.2 | 4 / 20 / 5.4 | 6 / 23 / 5.4 |
| Iron Sentinel | 12 / 26 / 8.1 | 8 / 29 / 7.6 | 1 / 2 / 8.4 | 9 / 33 / 8.2 | 13 / 37 / 8.5 |
| Shieldbearer | 1 / 13 / 4.2 | 1 / 17 / 4.2 | 0 / 1 / 4.2 | 1 / 15 / 4.2 | 2 / 18 / 4.4 |
| Marsh Archer | 0 / 18 / 3.8 | 2 / 34 / 3.8 | 0 / 17 / 3.8 | 2 / 22 / 3.7 | 2 / 22 / 3.7 |
| Crossbow Sniper | 0 / 22 / 3.5 | 1 / 41 / 3.7 | 0 / 22 / 3.6 | 0 / 28 / 3.5 | 0 / 28 / 3.5 |
| Glaive Dancer | 1 / 19 / 3.6 | 1 / 23 / 3.6 | 0 / 3 / 3.7 | 1 / 19 / 3.6 | 1 / 19 / 3.6 |
| Executioner | 1 / 20 / 3.6 | 0 / 22 / 3.6 | 0 / 3 / 3.8 | 1 / 19 / 3.7 | 1 / 18 / 3.6 |
| Grave Caller | 4 / 44 / 3.9 | 6 / 44 / 4.0 | 2 / 42 / 4.0 | 3 / 40 / 3.9 | 3 / 40 / 3.9 |
| Ember Caster | 2 / 17 / 4.6 | 3 / 17 / 4.5 | 2 / 16 / 4.9 | 1 / 11 / 4.3 | 2 / 12 / 4.4 |
| Cinder Adept | 5 / 30 / 4.7 | 8 / 44 / 5.1 | 3 / 26 / 4.8 | 13 / 34 / 5.8 | 14 / 35 / 5.7 |
| Mind Lash Adept | 3 / 37 / 4.1 | 2 / 36 / 3.8 | 3 / 37 / 4.2 | 3 / 32 / 4.0 | 3 / 32 / 4.0 |
| Goblin Cutthroat | 3 / 25 / 3.8 | 2 / 32 / 3.8 | 0 / 1 / 3.6 | 1 / 24 / 3.7 | 2 / 30 / 3.8 |
| Brute | 1 / 23 / 3.9 | 2 / 28 / 4.0 | 0 / 2 / 3.9 | 3 / 20 / 4.0 | 3 / 22 / 4.0 |
| Thornhide Brute | 1 / 23 / 3.9 | 3 / 27 / 4.0 | 0 / 3 / 4.1 | 1 / 22 / 3.9 | 1 / 23 / 3.9 |
| Gravel Ogre | 2 / 19 / 3.8 | 1 / 23 / 3.8 | 0 / 1 / 4.2 | 1 / 16 / 3.8 | 2 / 17 / 3.8 |
| Warleader | 1 / 18 / 3.8 | 0 / 15 / 3.6 | 0 / 2 / 4.0 | 2 / 17 / 3.9 | 2 / 18 / 3.9 |
| Fen Warden | 2 / 23 / 3.7 | 2 / 17 / 3.9 | 1 / 5 / 3.8 | 2 / 22 / 3.8 | 2 / 21 / 3.9 |
| Skulking Footpad | 1 / 18 / 3.6 | 1 / 25 / 3.6 | 0 / 2 / 3.8 | 2 / 21 / 3.7 | 2 / 23 / 3.7 |
| Shade Stalker | 2 / 32 / 4.4 | 2 / 34 / 4.1 | 2 / 23 / 4.4 | 1 / 23 / 3.8 | 1 / 23 / 3.8 |
| Bog Skirmisher | 1 / 12 / 4.5 | 1 / 18 / 4.5 | 1 / 10 / 4.9 | 2 / 14 / 4.4 | 2 / 14 / 4.4 |
| Hunting Hound | 2 / 27 / 3.8 | 3 / 31 / 3.9 | 0 / 1 / 3.6 | 2 / 30 / 3.9 | 2 / 30 / 3.8 |

- **Hold the Line and Vanguard play close to Hit Whatever** (a few points
  either way): they change who gets hit, not how hard. The Iron Sentinel
  covering the casters downs someone more (Vanguard 37%, Hit Whatever
  26%), and the Cinder Adept loses the party more fights going after its
  hardest hitters (13-14% against 5%).
- **Kiting is for ranged monsters.** Played when engaged, archers and
  casters read about as Hit Whatever (Marsh Archer 17% Down against 18%,
  Grave Caller 42% against 44%); a melee monster that backs off from
  melee does next to nothing (1-5% Down).
- **Assassin's edge is smaller beside other attackers** but still the
  largest (Marsh Archer 34% against 18%, Crossbow Sniper 41% against 22%).

**GM quick reference** (whom an enemy attacks; it still moves and attacks
as normal):

| Tactic | Attacks | Note |
|---|---|---|
| Hit Whatever | the closest PC | the default; spends itself on the front line |
| Hold the Line | whoever has hurt its side most this fight | closest until someone has |
| Vanguard | whoever has hurt its back line most this fight | closest until someone has |
| Kiting | the closest PC, stepping back first if one is in melee reach | ranged enemies only |
| Assassin | the softest PC: the most hurt for their size, then the lightest armor | the deadliest: two to five times the Downs of Hit Whatever |
| Triage | (supports) the ally that most needs it | |

### What a hexer is for (2026-11-05)

The designer: review the hexers; re-evaluate what their job in the
ecosystem is supposed to be. How the sim plays one: its Hex is an attack
at Mental that lands its stacks on a hit and deals nothing; it Hexes
whoever lacks a full stack (by its tactic) and swings its backup only
once everyone has one. The effects are all Fleeting: a Hex of 3 Crippled
is −3 to attacks for one turn, −2 the next, −1 the one after. Vulnerable
lowers only Vital, Mental and Vigilant, which most attacks don't target;
Slowed costs movement, which matters little in these fights.

`experiments/enemies/hexer_check.py`: a basic fight at Level 3, three of
a working monster (Brutes, or Grave Callers aiming at Vital) and a
fourth, against every test party in the middle of the band, 60 fresh
fights each (`results/enemy_stats/hexer_check.txt`). The fourth is
another of the three, a hexer as built, or a hexer changed one way: a
different effect, the old stack counts, a curse that lasts the fight
(`tunables.HEX_PERSIST`), one that also lands on every PC within 3 m of
its target (`HEX_AREA`), or the Bog Hexer as a caster whose damaging
spell carries Crippling four times instead of a Hex:

| Fight | Lost | Down | Wounded | Rounds |
|---|---|---|---|---|
| Brute x4 | 1.2% | 15% | 51% | 4.4 |
| Brute x3 + Bog Hexer (Crippled) | 0.0% | 3% | 27% | 4.5 |
| Brute x3 + Bog Hexer, old stacks | 0.2% | 4% | 28% | 5.0 |
| Brute x3 + Bog Hexer, Harried | 0.2% | 4% | 30% | 4.1 |
| Brute x3 + Bog Hexer, Vulnerable | 0.0% | 2% | 26% | 4.0 |
| Brute x3 + Bog Hexer, Frightened | 0.0% | 2% | 26% | 4.2 |
| Brute x3 + Mire Witch (Slowed) | 0.0% | 3% | 26% | 4.2 |
| Brute x3 + Curse Weaver (Vulnerable) | 0.2% | 4% | 30% | 3.9 |
| Brute x3 + Ember Caster (attacker) | 0.8% | 16% | 50% | 4.0 |
| Brute x3 + Bog Hexer, lasting | 0.6% | 4% | 29% | 4.7 |
| Brute x3 + Bog Hexer, spreading | 0.4% | 5% | 32% | 5.4 |
| Brute x3 + Bog Hexer, lasting and spreading | 0.4% | 6% | 35% | 5.1 |
| Brute x3 + Bog Hexer as a Crippling caster | 3.5% | 18% | 51% | 5.0 |
| Grave Caller x4 | 6.0% | 77% | 89% | 3.7 |
| Grave Caller x3 + Bog Hexer (Crippled) | 1.9% | 34% | 60% | 4.0 |
| Grave Caller x3 + Bog Hexer, old stacks | 1.9% | 34% | 60% | 4.4 |
| Grave Caller x3 + Bog Hexer, Harried | 0.0% | 33% | 59% | 3.5 |
| Grave Caller x3 + Bog Hexer, Vulnerable | 1.2% | 38% | 65% | 3.7 |
| Grave Caller x3 + Bog Hexer, Frightened | 0.0% | 33% | 59% | 3.6 |
| Grave Caller x3 + Mire Witch (Slowed) | 1.0% | 35% | 59% | 3.7 |
| Grave Caller x3 + Curse Weaver (Vulnerable) | 1.5% | 36% | 61% | 3.5 |
| Grave Caller x3 + Ember Caster (attacker) | 7.7% | 65% | 84% | 3.8 |
| Grave Caller x3 + Bog Hexer, lasting | 3.5% | 34% | 60% | 4.4 |
| Grave Caller x3 + Bog Hexer, spreading | 2.3% | 35% | 60% | 4.5 |
| Grave Caller x3 + Bog Hexer, lasting and spreading | 3.3% | 37% | 62% | 4.7 |
| Grave Caller x3 + Bog Hexer as a Crippling caster | 6.7% | 42% | 70% | 4.9 |

- **A hexer adds next to nothing, whatever it hexes with.** Swapping one
  of four Brutes for any hexer takes Downs from 15% to 2-4% and Wounded
  from 51% to about 27%: the fight plays like three Brutes. The effect
  doesn't matter (Crippled, Harried, Vulnerable, Frightened, Slowed all
  land within a couple of points), nor do the old stack counts.
- **Even lasting and spreading curses barely help** (Downs 4-6%), though
  they make fights longer (up to 5.4 rounds).
- **Vulnerable beside Vital attackers is the one pairing that shows**,
  and only a little (Grave Callers 38% Down with it, 33-35% with the
  others).
- **Debuffs on a damaging spell work.** The same budget as a caster whose
  hits Cripple four times plays like an attacker (18% Down, the most
  fights lost of any fourth, and longer fights). A hexer's turn is worth
  far less than the damage it gives up.

The sim may undervalue control, since its PCs don't play around a debuff
the way players feel one; the balance-weights pass is where that gets
checked.

**Ways to give the hexer a job** (for the designer):

1. **Debuff casters instead of Hexes:** a hexer is a caster whose spells
   carry stacked on-hit effects (the Mind Lash Adept and the Crippling
   caster above). Simple, already in the catalog, and it plays.
2. **Hexers as cheap spice:** keep the no-damage Hex but make a hexer a
   half-Slot add-on (minion-sized), so it costs a fight little and the
   table still gets the flavor.
3. **A stronger Hex:** something bigger than stacks that fade, such as
   Bad Luck on the target's attacks for a round, or the Hex as an area
   effect at full strength. New rules to write and test.

**Accuracy +1 bought more than once** (2026-11-05, the designer: how
strong is it, and does it eclipse the PCs? `kit_check.py` `nudge:acc=1-4`
on every full-size enemy in the four mixes, pruned default, Levels 2 / 3;
`results/enemy_stats/v3p_acc_stack.txt`; worth in Health per Slot, change
in fights with someone Down):

| Accuracy | Worth | Down |
|---|---|---|
| +1 | 1.7 / 2.3 | +6 / +6 |
| +2 | 3.4 / 4.8 | +12 / +13 |
| +3 | 5.4 / 7.4 | +18 / +19 |
| +4 | 7.3 / 9.9 | +24 / +24 |
| (Damage +1) | 4.1 / 4.7 | +15 / +15 |

Each point is worth about the same as the last (1.7-2.0 Health at Level
2, 2.3-2.6 at Level 3) and adds about 6 points of Downs: no runaway, a
touch under its price of 2 at Level 2 and a touch over at Level 3. Two
points of Accuracy are worth about one of Damage. The ceiling is the
player's: a Skill Total of 10 plus the weapon's own Accuracy. As built the
most accurate monster sits at about the PCs' average (Mire Witch: 9 at
Level 3 against the PCs' 9, best 10), the average monster 2-3 under. Even
a monster spending its whole budget on Accuracy (with the Strategist's
+2) only reaches the best PC's number (Level 1: 7 against 8; Level 3: the
cap, against the best PC's 10).

**Decided** (designer, 2026-11-05): Accuracy +1 stays repeatable, with a
note that it can't raise an enemy's Accuracy before its weapon's own above
10, the player's cap. Buys to reach it: at Level 1 eight (six for a
Strategist), more than any budget holds; at Level 3 four for a Strategist
(8 of 11 points); at Level 5 two for a Strategist, three for a Skirmisher,
four for anyone else.

**Hexers as debuff casters** (designer, 2026-11-05: a hexer is an enemy
that spends more of its budget on debuffing and Accuracy). The three are
rebuilt as Strategists on a damaging spell with two stacked on-hit
effects and Accuracy bought twice or three times: the Bog Hexer (Ranged
Spell; Crippled 4, Slowed 2 on a hit), the Mire Witch (Vital Spell;
Slowed 4, Necrotic 4) and the Curse Weaver (the Mind Spell at Mental;
Vulnerable 4, Frightened 4). No cap on a hit's total stacks beyond 4 an
effect, for now. The no-damage Hex leaves the regular manual. Same fight
as before (`hexer_check.py v2`, `results/enemy_stats/hexer_check_v2.txt`):

| Fight | Lost | Down | Wounded | Rounds |
|---|---|---|---|---|
| Brute x4 | 1.2% | 15% | 51% | 4.4 |
| Brute x3 + Bog Hexer (caster: Crippled 4, Slowed 2) | 1.5% | 17% | 51% | 4.9 |
| Brute x3 + Mire Witch (caster: Slowed 4, Necrotic 4) | 0.2% | 13% | 50% | 4.3 |
| Brute x3 + Curse Weaver (caster: Vulnerable 4, Frightened 4) | 0.2% | 11% | 50% | 3.9 |
| Brute x3 + Ember Caster (attacker) | 0.8% | 16% | 50% | 4.0 |
| Grave Caller x4 | 6.0% | 77% | 89% | 3.7 |
| Grave Caller x3 + Bog Hexer (caster: Crippled 4, Slowed 2) | 5.8% | 49% | 72% | 4.6 |
| Grave Caller x3 + Mire Witch (caster: Slowed 4, Necrotic 4) | 2.5% | 45% | 72% | 4.1 |
| Grave Caller x3 + Curse Weaver (caster: Vulnerable 4, Frightened 4) | 3.7% | 64% | 86% | 3.8 |
| Grave Caller x3 + Ember Caster (attacker) | 7.7% | 65% | 84% | 3.8 |

Each now plays like an attacker beside the Brutes (Downs 11-17% against
15% for a fourth Brute), and the Curse Weaver's Vulnerable pays off beside
the Vital-attacking Grave Callers (64% against 65% for another caster).

**The solo boss's size** (designer, 2026-11-05: swingier and more
dangerous than usual, but it shouldn't often beat the whole party). The
Brute Warlord alone, with a 4-Slot enemy's Health at each multiple of a
standard enemy's (`boss_check.py`, `results/enemy_stats/boss_check.txt`;
fights lost, with the worst party's in brackets):

| Health (× a standard enemy) | Level | Lost (worst party) | Down | Wounded | Rounds |
|---|---|---|---|---|---|
| 9 | 3 | 56% (98%) | 66% | 69% | 12.9 |
| 9 | 4 | 57% (100%) | 67% | 69% | 15.0 |
| 9 | 5 | 70% (100%) | 72% | 73% | 17.9 |
| 8 | 3 | 43% (85%) | 61% | 66% | 11.3 |
| 8 | 4 | 39% (87%) | 59% | 63% | 12.4 |
| 8 | 5 | 64% (100%) | 69% | 70% | 16.4 |
| 7 | 3 | 27% (58%) | 51% | 60% | 9.0 |
| 7 | 4 | 22% (58%) | 44% | 54% | 9.2 |
| 7 | 5 | 48% (92%) | 61% | 66% | 13.8 |
| 6 | 3 | 9% (23%) | 35% | 50% | 6.2 |
| 6 | 4 | 8% (33%) | 24% | 38% | 6.2 |
| 6 | 5 | 23% (63%) | 43% | 54% | 9.3 |
| 5 | 3 | 2% (10%) | 19% | 38% | 4.2 |
| 5 | 4 | 1% (3%) | 12% | 28% | 4.4 |
| 5 | 5 | 5% (17%) | 21% | 38% | 5.3 |

At 9 (as first built) the boss won 56-70% of fights over 13-18 rounds.
At 6 it loses the party 8-9% of fights at Levels 3-4 with someone Down in
a quarter to a third, over about 6 rounds: dangerous and swingy, rarely
a wipe. Level 5 reads harder (23%) on parties that are Level 3 characters
grown to the caps. `tunables.V3_SOLO_HEALTH = 6` (the pruned v3 only).
