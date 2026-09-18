# Enemy Encounter Design

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
**2** (an elite/boss-tier threat worth two standard enemies). This
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
| **Tank** | Resist +1, Parry +1, Dodge +1, and all four elemental Resists (Fire/Frost/Brilliant/Shadow) +1 |
| **Striker** | Accuracy +1, Damage +1 |
| **Bruiser** | Damage +1, Resist +1, Parry −1, Dodge −1, and all four elemental Resists +1 |
| **Strategist** | Accuracy +1, Bodily Defense +1, Mental Defense +1 |
| **Defensive** | Parry +1, Dodge +1, Bodily Defense +1, Mental Defense +1 |

*(Earlier/simpler draft, superseded by the above but consistent with
it in spirit: Tank = Resist+1/Parry-Dodge+1; Striker = Damage+1/
Accuracy+1; Bruiser = Damage+1/Resist+1/Parry-Dodge−1; Strategist =
Accuracy+1/Parry-Dodge+1/Mental+1; "Backup" = Parry-Dodge+1/Bodily+1/
Mental+1 — the richer version above is a real expansion of this, not a
contradiction: same shape, more generous, and "Backup" renamed
"Defensive" with an added Dodge+1.)*

## Defense tiering: Primary/Secondary/base — the core "intuitive weakness" mechanic

Enemies use **three** Defense categories, not the PC's five —
**Parry/Dodge** (combined into one, unlike PCs who pick between them
per-attack), **Bodily** (= Vital Defense), and **Mental**. Vigilant
Defense isn't modeled for enemies at all — a deliberate simplification,
not an oversight (nothing in the source system varies it per-enemy).

The GM picks **one Primary Defense** (this enemy's clear strength) and
**one Secondary Defense** (its middling one) out of those three — the
third, un-picked category is this enemy's clear weakness. Concretely,
each Defense's base value (Accuracy + 6, the same base every category
starts from) gets a flat **+2 if it's the Primary pick, +1 if
Secondary, +0 otherwise** — reproduced exactly from the live
calculator's own worked example (Level 2, Primary = Parry/Dodge,
Secondary = Mental): Parry/Dodge Defense 17 (base 12 + 2 primary + 3
flat), Bodily Defense 13 (base 12 + 0 + 1 flat, no bonus — the
un-picked category), Mental Defense 14 (base 12 + 1 secondary + 1
flat).

**This is the actual mechanism behind "intuitive strengths and
weaknesses."** A heavily-armored brute with Parry/Dodge as Primary is
legibly bad at resisting Mental effects (Persuasion, Intimidation,
Theurgy targeting the mind) if Mental is left as its un-picked
category — and a player who notices that and leans on a
Composure-targeting approach instead of just swinging harder is being
rewarded for reading the fiction correctly, not for metagaming a
hidden number.

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
| Unarmored | Dodge +1, Speed +1 |
| Light | Physical Resist +1 |
| Medium | Physical Resist +2, Dodge −1, Speed −1 |
| Heavy | Physical Resist +3, Dodge −2, Speed −2 |

Same Resist-for-mobility trade-off shape as the PC armor tiers
(`weapon_categories.csv`/`armor_categories.csv`), applied to enemies
directly rather than reinvented.

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
