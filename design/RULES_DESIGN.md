# Designing FlagonQuest's Rules

Companion to `CLAUDE.md`, but for rules/game design decisions rather than
site conventions — a running record of *why* the rules ended up the way
they did, not just what they say. Read this at the start of a rules-design
session to pick up the reasoning where it left off, the same way `CLAUDE.md`
works for the site. Kept as a separate file (not folded into `CLAUDE.md`)
specifically so the rules-overhaul branch and the site-overhaul branch
don't both need to touch the same file before they merge.

This file is never read by the site or by `convert.py` — it's pure internal
reference, not content.

**Standing instruction:** whenever this session's context is about to be
compacted, update this file first with whatever's been settled since the
last update, before the compaction happens.

## Design philosophy established so far

### STANDING RULE — Techniques and items are assumed to break the baseline, and that's fine

This applies to every section of the book, not just one, and should shape how
all future rules text gets written: **the base rules describe the default
case, and Techniques/items are the explicitly-sanctioned place for
exceptions.** Once that's stated up front, it never needs restating at each
individual rule. A movement rule doesn't need "...unless a Technique lets you
jump farther" tacked on; a damage rule doesn't need "...unless an item grants
more" — a reasonable player already infers this once, the same way they infer
that a locked door can be picked without every mention of "door" repeating
that fact. Over-qualifying every base rule with this caveat would make the
book harder to read, not more precise, and is the same "don't write a rule to
explain what doesn't happen" style principle already established below (see
the Social Contests entry), just generalized from one example to the whole
book, per explicit user instruction to "note and double-underline" it as
standing guidance.

Landed by stating it exactly once, where Techniques are first properly
introduced (`## Techniques` in `rulebook.md`, "Your Character" chapter):
"A Technique's rules text can do things the rest of the game doesn't - jump
farther than normal, grant a bigger bonus, override a limitation entirely -
simply by saying so. The rest of this book describes the baseline; Techniques
are what's meant to go beyond it." Applied in commit `ffe0aff`. Practical
effect going forward: don't add hedging caveats to base rules anticipating
what a Technique might override (the Moving section, Social Contests, Pressure
etc. were already written this way without realizing it was a named
principle) — this is now the explicit, citable reason why, not just a
case-by-case style call.

### STANDING RULE — Fire is the deliberately common element

Among the four elemental damage types (Fire, Frost, Brilliant, Shadow),
Fire is intentionally the most common one to encounter — not because
Fire is meant to be mechanically *better*, but specifically so a player
who wants to invest in countering elemental damage has an obvious,
reliable choice to make. This shows up in several places already:
Battle Magic uses Fire as its baseline element, Masterwork items that
deal Fire damage are built one Level lower than the equivalent for
another element, and the actual damage-dealing Grenades default to Fire
at the lower Levels. None of this was written down as an explicit
principle before — surfaced while deriving Resist's balance weight (see
`design/balance_weights_notes.md`), where the designer gave a concrete
rule of thumb: **3 in 4 enemies deal Physical damage only; of the
remaining 1 in 4 that deal an element, Fire is about twice as common as
Frost, Brilliant, or Shadow individually** (working out to roughly
Fire 10%, each other element 5%, of all enemies) — likely trending
higher as characters reach higher Levels and face tougher, more varied
threats.

That's a headcount rule of thumb, though — a later correction narrowed
what actually matters for Resist's math, which is *damage share*, not
enemy count. An elemental-relevant encounter (roughly half of all
encounters, matching the cadence above) isn't just "half the field is
elemental, half is physical" — the elemental-dealing enemy tends to be
the fight's main damage dealer (a mage lobbing fireballs), while the
physical-damage enemies alongside it skew tank/disruptor and contribute
comparatively little. Designer's revised estimate: **when an element is
relevant to a fight, it accounts for roughly two-thirds of that fight's
total damage**, not merely "as much as its share of the enemy count."
Physical Resist is still clearly the better overall pick (it's relevant
in every fight, not just the ones featuring that specific element), but
elemental Resist pays off harder in the fights where it does apply than
the headcount framing alone suggested. See the Resist section of
`design/balance_weights_notes.md` for the recomputed weights this
produces.

The explicit intent, stated directly: there should be real room to
build toward resisting a *specific* element for a known upcoming fight
(a consumable prepared once the party knows what they're up against,
not necessarily a permanent character build), but Fire is the one
worth defaulting to or building around broadly, since it's the one
you're actually likely to run into. Worth keeping in mind for future
content — a new elemental enemy, spell, or Masterwork item should
default to Fire unless there's a specific reason (theme, a Frost-heavy
dungeon, a Shadow-aligned villain) to reach for one of the other three.

### STANDING RULE — Weapon and Implement Masterwork enhancements are meant to overlap heavily

Not an oversight to tidy up — deliberate. Per the designer: a magic
weapon reading as useful to *both* a martial character and a spellcaster
is intentional, for two reasons. First, it widens who a given piece of
loot is actually exciting for — an enchanted blade doesn't have to sit
dead in a spellcaster's inventory just because its bonus reads
combat-flavored. Second, and more importantly, it avoids punishing a
"spellblade"-style hybrid character (someone who both swings a weapon
and casts spells) for wanting one held item to do both jobs, rather than
needing to carry a dedicated weapon *and* a dedicated implement
separately just to have both halves of their kit online. This is
already load-bearing in the base rules, not something Masterwork items
have to individually re-earn: per `glossary.md`'s `[Implement]` entry,
*any* weapon can already be channeled through as an Implement ("If the
Implement is a weapon, the Spell or Discipline counts as an attack with
that weapon for any additional effects"). So a Held weapon enhancement
that reads as combat-flavored (bonus damage-on-hit, a Push, a debuff
proc) is *already* just as usable by a caster funneling spells through
it, and vice versa — worth keeping in mind when archetype-tagging or
designing new Held items: "Weapon" and "Implement" should be treated as
overlapping, not exclusive, categories for the vast majority of Held
Masterwork items, not a hard split.

### STANDING RULE — Equipment slots each have an intended design lane

Surfaced while starting the Masterwork balance pass, checking why a
Neck item (Worry Token) read as an odd fit for a flat Resist bonus (it
turned out not to actually grant one — see below). Found the original
slot philosophy in two archive drafts, `archive/flagonquest_items_2k20.md`
and the updated `archive/flagonquest_items_2k22.md` (which adds Belt and
retitles Hands), never previously carried into the live design docs:

| Slot | Intended lane |
|---|---|
| Head | Mental, vision |
| Hands | Skill-based non-attack actions (lockpicking, surgery, and similar) |
| Feet | Mobility |
| Belt | Carrying items |
| Torso | Direct protection, vitality/healing |
| Held | Weapons and other active-use items requiring an action |
| Neck | Niche, boring, passive utility — deliberately *not* interactive or defensive |
| Ring | A specific active ability, or an augment to a specific skill/ability |

`archive/flagonquest_manifesto_2k19.md`'s "RESIST PLANNING" section ties
Resist specifically to Torso: *"+1 Resist from Torso equipment, MAYBE
+2 for like a Level 5 item."* No archive document ever pairs Resist
with Neck or Ring.

Checking the live catalog against this table caught one real thing and
ruled out another. Real: **Elemental Warding Amulet** (`I208`, Ring)
grants a flat elemental Resist bonus with numbers identical to
Elemental-Resistant Armor's (Torso) — a passive stat clone sitting on
the wrong slot's lane (Ring is meant for *active* abilities, not a
passive number), and redundant with an existing Torso item to boot. See
the Masterwork balance pass below for the redesign that resolved it.
Ruled out: Worry Token doesn't actually grant flat Resist at all — an
earlier broad text search this session matched the word "Resist"
appearing inside one of its six random secret-effect outcomes ("ignores
the target's Physical Resist"), not an actual granted stat. Its real
effect (a charge-based random-benefit charm) already matches Neck's
"boring passive utility" lane correctly; no change needed there. Same
search error also mis-flagged Charcoal (not even a Masterwork item —
its "Resist" hit was a Poison-*Resistance flip*, a saving throw,
unrelated to the Resist stat) and Fortified Armor (which doesn't grant
Resist itself, only conditionally amplifies Resist the wearer already
has from elsewhere) — worth remembering broad substring searches over
`Effects` text need a second look before being trusted as a
categorization, not just a starting point.

### Successes as the universal resolution currency

The game is moving toward one unified idea of "success" behind every flip
— skill checks and attacks alike — rather than attacks having their own
ad hoc rules (a flat `[Hearts]` damage bonus) separate from how skill
checks work. A flip's successes are: 1 base success if it beats the
difficulty, **plus 1 for each full 2 points the result beats the
difficulty by** (already precedented in `Pressure Point Revitalization`'s
"1 extra success for each 2 you beat the difficulty by"), **plus 1 for
each card in the suit pool matching the flip's relevant Skill's suit**,
**plus 1 per Gamble** (see below). On a damaging attack, each success
beyond the first is worth +1 damage, same as the existing Extra Success
rule already says.

**Gambling is a bet made before you see the card, not a spend of margin
you already know you have.** You declare how many times you're Gambling
*before* the flip — each Gamble is a flat -2 to the eventual result, +1
guaranteed success if the flip still succeeds. Because it's declared
blind, it isn't mathematically redundant with the margin-to-successes
conversion above (a naive reading suggests it's an even trade at the same
2-points-per-success rate, and it emphatically is *not* — you're wagering
on a card you haven't flipped yet). A character whose Skill Total
comfortably clears the difficulty is making a low-risk bet; a character
at the edge of their competence is risking the whole attempt to squeeze
out more successes. This is the mechanism that makes Gambling do the
"force players to take chances" job it was originally designed for
(`rulebook.md`, "Gambling and Extra Successes") — it just does it more
precisely once framed this way, and it now applies uniformly to attacks,
not just skill checks.

**Checks that need repeated attempts to accumulate enough successes**
(e.g. picking a lock needing 4 successes total) are allowed to just keep
trying — "unless they mess up badly somehow." **Not yet nailed down:**
what exactly counts as "badly" and what it costs. This is explicitly the
GM's job to set up per-scene (time pressure, a chance of being noticed,
etc.) rather than a hardcoded universal rule, matching how the rest of
the game already leans on GM judgment for scene pacing. Still worth a
firmer default trigger at some point so it doesn't read as hand-wavy in
print.

**Known consequence, not yet resolved:** feeding margin into attack
successes automatically (not just via optional Gambling) is a real
balance change, not just a documentation change — weapon Damage and
enemy Defense values were tuned assuming Extra Success on attacks was
optional and costed. This will need a numbers pass once the formula is
locked, separate from writing the rule itself. (That pass belongs in the
sibling data-focused chat, not here.)

### STANDING RULE — Damage/success bonuses stay routed through the existing systems, never granted flat

Extends "Successes as the universal resolution currency" above from a
core-rule principle to a **content-design** one: a new item or Technique
should never directly grant an Extra Success or a flat bonus to a flip
or to damage. Per the designer, that's "free damage" outside the
systems meant to gate it — the whole point of Extra Success being
earned through Gambling (a real risk/reward trade) or a suit-pool match
(a card-luck/build-synergy payoff) is that it always costs or risks
something, or rewards forethought. A flat grant skips that entirely.
Anything that wants to make an attack land harder or more reliably
should reach for one of the existing levers instead — Good Luck
(better odds on the flip itself), reducing the target's Defense
(Vulnerable and friends), enabling more Gambling (higher Skill Total,
or removing its downside), or a suit-pool assist (Sift, an extra card
in the pool) — all of which still route the actual bonus through the
normal resolution math, preserving the trade-off instead of bypassing
it. Cited directly against a real proposal this session (a Swiftblade
Vial redesign considered granting a direct Extra Success) — rejected
for exactly this reason, redirected toward turn-order adjustment
instead (see below).

### STANDING RULE — Reward cleverness and risk, not raw power

Stated directly by the designer while finalizing Insanity Potion (a
Level 5 capstone deliberately built to be swingy — genuinely stronger
in the right hands and circumstances, offset by a real drawback rather
than a flat number): **a build/item/moment should read as strong
because a player was clever or dared something risky, not because the
math is just bigger than it should be.** Not the same thing as "nothing
should ever be strong" — the opposite, actually: an item is allowed to
land well outside the normal Net band *when the strength comes from the
player's own decision-making or risk tolerance* (reading a fight right,
accepting a real drawback, setting up a combo across multiple sources)
rather than from an unconditional number that's simply too generous for
its Level. The practical test when something reads as strong: is the
power gated behind genuine skill/risk, or would it be exactly as strong
sitting in anyone's hands doing nothing clever at all? The former is
fine even well outside the usual threshold band; the latter is the
"obviously overpowered" failure mode to actually avoid. Directly
informed how Insanity Potion's own Net (−0.15, close to neutral) was
allowed to stand rather than being pushed higher for "capstone flair" —
the item's real power lives in stacking three debuff immunities with a
Speed buff and sustained Bleeding all under one drawback that has to be
accepted to get any of it, not in an inflated top-line number.

### Turn-order adjustment — a mechanic to lean into more, first value derivation

Several existing Techniques already let a creature's position in the
turn order shift, but each was designed independently with no shared
value behind it: `Backfoot` (Battle Maneuver Feature, Basic/1pt) pushes
a *target* back "by up to X + [Spades] times" on a hit; `Alacrity`
(Spirit Blessing Feature, Advanced/2pt) lets the target move up "by up
to 2," flat, no scaling; `One Eye Behind You` lets you discard a card
to move yourself "by up to [half Insight Skill Total]"; `Heroic
Inspiration` offers "adjust position by 1" as one of three
interchangeable choices alongside "Protected twice" or a Taunted/
Frightened cleanse. None of these were priced against THE TABEL — they
predate the value-economy work entirely, so their relative magnitudes
aren't a reliable calibration point (Heroic Inspiration bucketing "shift
by 1" alongside "Protected twice," worth 6 on its own, is suggestive of
original design instinct but not verified).

Per the designer, this is a mechanic they want to lean into more —
"a fun tactical thing," enabling one character to capitalize on another's
setup (a debuff landed, an enemy about to go down) by acting inside a
window that would otherwise close before their natural turn comes up.
That's the same fundamental shape Harried's own value already covers:
a temporary window whose benefit accrues to *whichever attack happens
to land inside it* — Harried's per-stack rate was derived assuming
"on average, one extra attack benefits" from a window it opens. Turn-
order adjustment doesn't open a window itself; it lets you choose *who*
gets to use one that's already open (from Harried, Vulnerable, a
kill-race, or simply denying an enemy the chance to react before your
side reshapes the board) — a related but distinct kind of tactical
edge from a direct numeric buff. **Confirmed Pencil value: 1.0 per
place shifted**, roughly half of Good Luck's revised marginal (2.4) —
reasoning it as "sometimes decisive, often marginal" in the same spirit
as the discount Good Luck's own Suit Pool credit needed, since a shift
only pays off when there's an actual timing-sensitive window to
exploit, unlike Good Luck which improves the flip it's attached to
every single time. Linear for now, deliberately left uncapped — per the
designer, worth seeing how it actually reads once used across a few
more items/Techniques before deriving a cap from first principles,
rather than guessing one now. Worth revisiting the moment a design
would need double-digit places to hit its budget (a first warning sign
this session: an early draft of Swiftblade Vial's redesign needed ~9
places paired with modest Hasted to hit its Level-4 budget alone — far
past any existing precedent's scale, which is what pushed the final
version toward a smaller shift paired with more Hasted instead). Now
in `balance_weights.csv`/`balance_weights_notes.md`.

### Suits: an emerging identity per suit, not a strict grid

Each suit (♥ Hearts / ♣ Clubs / ◆ Diamonds / ♠ Spades) is being built out
as a full portfolio: a cluster of Skills, an Offensive identity, a
Defensive identity, and eventually a Social identity once the social
contest redesign happens. The goal isn't a perfectly even split — the
user is explicitly fine with asymmetry as long as each suit ends up
*roughly as useful* as the others overall, just not necessarily useful in
the same way.

**The game's own existing Element correspondence turned out to be the
most reliable tie-breaker**, more reliable than tarot/Jungian-function
correspondence alone: Hearts↔Brilliant, Clubs↔Fire, Diamonds↔Shadow,
Spades↔Frost (`rulebook.md`'s five damage types + the original brainstorm
sheet's "Element (Game)" row). This splits into two dualities — elemental
(Fire/Frost: active force vs. passive control) and spiritual
(Brilliant/Shadow: abundance of spirit vs. its absence/concealment) — and
resolved several placements flavor text alone couldn't (Stealth as
Shadow/concealment → Diamonds; Theurgy's supportive magic as
Brilliant/abundance → Hearts, leaving Sorcery alone in Clubs as the
Fire-coded direct-damage skill).

**Concrete mechanical ties beat lore-only arguments when both are
available.** Example: Insight stayed in Spades not because of a Jungian
Thinking/Intuition argument (which actually argued against it) but
because Insight determines the Reflex flip that sets Turn Order, and Turn
Order is already a Spades-flavored defensive concept. Similarly,
Presence stayed in Hearts because the social rules already group it with
Rapport as "Charismatic statements" (as opposed to Persuasion's
"Strategic" category) — even though Presence's own dictionary-style
description ("intimidating," "commanding") arguably reads closer to
Clubs. **Flagged as the least certain call in the whole table** — worth
a gut check later.

Current Skill → Suit table (see "Open questions" for the one flagged
uncertainty):

| Suit | Skills |
|---|---|
| ♥ Hearts | Rapport, Performance, Survival, Theurgy, Presence *(uncertain)* |
| ♣ Clubs | Brawl, Athletics, Resilience, Might, Meditation, Sorcery |
| ◆ Diamonds | Craft, Composure, Masquerade, Streetwise, Mixology, Acrobatics, Stealth |
| ♠ Spades | Melee, Archery, Awareness, Insight, Persuasion, Academics, Medicine |

**Sorcery is the renamed Elementalism** — if the old name turns up
anywhere (old notes, a stray CSV mention), it should be updated.

**A skill-count-even split doesn't imply an equally-useful split, and
that's fine.** Tallying how often each skill actually gets used across
`techniques.csv`/`items.csv`'s `Relevant Skills` column (weighting by
real content, not just raw skill count) gives Clubs 82 / Hearts 60 /
Diamonds 55 / Spades 46 — Hearts has the *fewest* skills (5) but the
*second-highest* usage, entirely on the strength of Theurgy being the
single most-used skill in the game. Skill count and practical usefulness
are different axes; don't assume they need to track together.

**Suit portfolio so far** (✓ = confirmed real against `glossary.md`, — =
open):

| Suit | Offensive | Defensive |
|---|---|---|
| ♥ Hearts | Frightened, Taunted | Brilliant Ward; healing effects scale off Hearts (roughly half of `Healing:TRUE` techniques already check "if the discarded card was a Heart" — see `Second Wind`, `Lay On Hands`) |
| ♣ Clubs | Bleeding, Crippled | Fire Ward, Hasted, Shift |
| ◆ Diamonds | Harried, Vulnerable, Necrotic | Shadow Ward; **no defensive keyword yet** |
| ♠ Spades | Slowed, Pushing, Difficult Terrain | Frost Ward, Protected |

`(Fire/Frost/Brilliant/Shadow) Ward` is one glossary entry with four
elemental variants, not a Hearts-exclusive effect — every suit already
gets its own Ward for free via the Element correspondence above.

**Embolden and Bolstered are deliberately cut, not gaps to fill.**
Embolden (a specific counter to Taunted/Frightened) was cut because
GM-adjudicated case-by-case handling does that job better. Bolstered
(countered Wounded's penalties) was cut because Wounded now just clears
on any healing. Their absence from Hearts/Diamonds' defensive portfolio
is intentional, not unfinished.

**Archetypes that fall out of the current table**, cross-checked against
actual technique clusters in `techniques.csv`:
- **Clubs** — splits fairly evenly between a direct-magic blaster
  (Sorcery) and a martial powerhouse (Meditation/Brawl/Resilience/Might).
  Broad appeal: very different builds both want Clubs.
- **Hearts** — support caster (Theurgy) plus the social face
  (Presence/Rapport/Performance). Has the clearest "why hand me cards"
  hook of any suit now that healing-scales-with-Hearts is confirmed
  real and common.
- **Diamonds** — no single dominant skill; spread across
  Craft/Composure/Masquerade/Streetwise/Stealth. Reads as the
  generalist/skill-monkey suit (artificer, rogue, con-artist, scout).
- **Spades** — the precise-combatant/analyst suit (Melee/Archery plus
  Insight/Academics/Medicine). Persuasion is thin in current content
  (only 1 use) but that's a content gap, not evidence against its suit
  placement.

### Card-sharing as a deliberate design throughline

The user wants the suit system to encourage players to hand each other
cards mid-session — "my build leans Diamonds, hand me your Diamonds."
Two existing mechanisms already support this without new rules:

1. **The base "Play" rule** (`rulebook.md`, "Your Hand and Playing
   Cards") already lets any player pitch a card from their hand into
   *any* flip made by them or a willing ally — replacing a flipped card
   or just adding its suit to the pool. Already fully general.
2. **`Ritual Magic`** (T099) already lets a willing ally discard cards
   to pay *your* Spell costs, "as though you had discarded them
   yourself" — this is closer to what the user wants than the
   alternative considered and rejected below, since it's the ally
   paying your cost rather than the target spending their own hand.

**Considered and rejected:** letting more techniques (e.g. `Healing
Magic`) let the *target* spend their own cards, the way `Pressure Point
Revitalization` (Medicine 5) already uniquely does. Rejected because the
user doesn't want patients spending their own cards for their own
healing as a general pattern — `Pressure Point Revitalization` keeps that
as its own specific, unique mechanic rather than it becoming common.

**Emerging direction instead:** generalize `Ritual Magic`'s pattern
("a willing ally may pay your cost/contribute to your effect") beyond
just Spells, and possibly turn it into a Stance-equivalent (see below) so
it can't freely stack with other similarly strong always-on enablers if
its scope broadens. Not yet decided how far the scope extends.

### Crafting simplification (applied)

**Deliberately no check for crafting itself, and this is settled, not
open.** No failure consequence for a crafting check makes sense: losing
time just drags out an already-slow, low-stakes activity, losing
materials is too punishing for something this deliberate, and given how
long crafting already takes, Gambling/spending cards would make a check
close to a formality anyway. More importantly, the actual uncertainty
in getting an item already happened upstream — the checks to find the
materials, survive the fight that dropped them, or talk your way into a
recipe. Materials are essentially loot; crafting is what turns loot into
targeted value. Gating that behind its own roll would be re-rolling dice
on something the fiction already resolved — the same "don't stack
redundant risk on something already resolved" instinct behind not
double-dipping Pressure with Extra Successes, or cutting the old flat
Hearts damage bonus once suit-matching covered the same ground.

**The actual problem is that the book currently documents the wrong
formula for how Materials work, and there isn't just one formula to
begin with.** `crafting_recipes.csv` has two incompatible shapes:
"Slots" (a small fixed count split into Primary/Leeway, e.g. a Carving
weapon's "2 Wood/Bone, 1 Cloth/Leather") governs Weapons, Armor, Basic
Clothing, Basic Jewelry, and Medicinal Supply — the items players craft
most — while "Value" (Total Materials count, Base Material Type ≥1,
Extra Material Type capped at half) governs only the five generic
fallback recipes for open-ended, Level-scaling categories (Masterwork,
Potions, Poisons, Grenades, Food). The rulebook's `#### Materials`
section only documents Value, meaning it never actually explains the
mechanic behind the majority of real recipes, including the book's own
worked example (Enith's blade uses Slots-shape numbers the prose never
introduces). Separately, `convert.py`'s docstring references "the
rulebook's per-slot default" base item (e.g. "basic clothing or basic
jewelry") for when `Base Item Options` is left blank — that default is
never actually stated anywhere in `rulebook.md`, just assumed to exist.

**Decided replacement: one universal formula, everywhere, no more
two-shape split.**
- **Correction from the previous entry: Cost ÷ Level is a design-time
  authoring guideline, not a live rule the book states or players
  compute.** Total Materials is just a plain number a recipe states
  outright, the same way it already states Level and School — nothing
  in the rulebook derives it from Cost at read-time. Cost ÷ Level (at 1
  Gold per Level of material value) is only *why* Masterwork recipes
  land on a flat 20 when authoring them (Level × 20 Gold pricing was
  chosen specifically so 20 materials at the item's own Level produces
  that price) — it's the reasoning behind picking Masterwork's number,
  not something every recipe follows. Basic items (weapons, armor, etc.)
  get their own directly-authored Total Materials number based on other
  factors entirely (one-handed vs. two-handed, etc.), unrelated to this
  formula. This resolves the Cost-vs-Level edge case flagged below —
  there's no live division happening, so nothing can round to 0.
- **Every recipe just states Total Materials as a number.** Masterwork
  recipes will typically land on 20 (per the design principle above);
  basic items get whatever number fits their own design factors. The
  rulebook's job is explaining how to *use* that number (Main/Optional
  split below), not where it came from.
- **Main Type must be at least half of Total Materials, rounded down
  per the global rounding rule; Optional Type can fill the rest, up to
  half.** This is mathematically identical to the old Base
  (≥1)/Extra (≤half) framing — same rule, restated as a symmetric floor
  instead of an awkward floor-of-1-plus-a-cap. Directly matches the
  worked "fire sword: 20 total, at least 10 Fire, up to 10 Metal, so 14
  Fire + 6 Metal is fine" framing.
- **This also quietly resolves the base-item flexibility problem**
  without needing a separate "combine two material lists" mechanic (the
  fold-it-into-one-crafting-pass idea from the base-item discussion
  above is now superseded by this): an enhancement just names its own
  Main Type, and the underlying item's normal Type serves as the
  Optional Type, inside the same shared Total Materials pool — a fire
  sword and a fire bow are the same enhancement recipe, just with
  Optional satisfied by Metal vs. Wood respectively. No union of two
  separate lists needed.
- Converting the existing fixed-slot recipes (Weapons/Armor/Clothing/
  Jewelry) to this shape loosens them slightly (e.g. a Carving weapon
  could go all-Wood/Bone instead of being forced into exactly 1
  Cloth/Leather) — a deliberate, welcome side effect of "let players mix
  and match based on what they have," not a bug to guard against.
- `Base Item Options` (specific item IDs, e.g. `I128,I129` reused across
  several Torso Masterwork items) stays a separate, complementary
  mechanic from Main/Optional Types — it's an equip-time concern (which
  specific already-owned item can carry this enhancement's stat bonuses
  on the Character Sheet), not a crafting-time material concern. No
  conflict between the two, they answer different questions.

**Original numbers restored from `archive/flagonquest_content_original.docx`**
(saved into the repo per explicit user request, "it would be nice to
maintain copies of the original work to reference" — the first
Word-doc source added to `archive/`, alongside its existing CSV/HTML
drafts). The doc's own pricing table and per-category recipe stats
confirmed: Masterwork flat 20 materials at the item's own Level
(20 Gold/Level pricing × 1 Gold/Level material value cancels out to a
constant 20, never scaling with Level), Alchemy (Potions/Poisons/
Grenades) flat 2 (2 Gold/Level, same cancellation), Food flat 2 (its
own entry, same 2×Level pricing despite being Cooking School not
Alchemy), Medicinal Supply/Basic Clothing/Basic Jewelry unchanged from
current data (already matched the doc exactly). Weapons/Armor/Tools
were **not** reverted to the doc's own Gold-derived approach for those
categories — that was superseded by a later, deliberate redesign (the
Primary/Leeway fixed-slot system, per README's own "Crafting materials
framework" changelog entry) that's kept, just reformatted into Total/
Main/Optional terms with the same numbers.

**Final correction to "Total Materials = Cost ÷ Level" as a live
formula: it isn't one, anywhere, not even for Weapons/Armor.** Every
craftable item just states its own Total Materials directly — "we'll
likely just make new recipes for everything... it'll just be their
base price in gold, but we can standardize it." For Weapons/Armor/
Tools this meant literally copying each item's own Cost (Gold, minus
the word "Gold") into its own Total Materials column — verified
against real `items.csv` data first, and every existing Cost already
matched the user's stated category costs exactly (1H melee/bow-adjacent
3, 2H melee 6, thrown 5, bows 6 as two-handed, shields 3, light armor
4, heavy armor 8) — so this was a mechanical copy, not new authoring.
Unarmed and Improvised are confirmed not craftable (no recipe at all);
Unarmed Enhancer keeps its own flat 3.

**Applied across every layer, in order, each verified before the
next:**
1. `convert.py` — `CRAFTING_RECIPE_MAP`/`ITEM_MAP` dropped Kind/
   Primary/Leeway entirely, renamed Base/Extra Materials to Main/
   Optional Materials; removed the now-obsolete Kind-shape validation
   block. Ran clean, zero validation errors.
2. `crafting_recipes.csv` — all 17 rows rebuilt on the new columns;
   Weapon/Armor/Tools recipes leave Total Materials blank on purpose
   (it's always item-overridden now) but keep their Main/Optional Types.
3. `items.csv` — Weapon/Armor Total Materials set from each item's own
   Cost (14 rows, mechanical script, matched expectations exactly);
   Masterwork items' Optional Materials cleared (1 row had a stray
   value) since it's now derived from the chosen base item, not stated
   per-item.
4. `index.html`'s Crafting tab — `resolveRecipeRequirements`/
   `craftingMaterialsEligibility`/`craftingGroup`/the render ternary all
   collapsed from two branches to one. `recipesForItem` fixed to merge
   an item's own overrides with the matching recipe row(s) *field by
   field* rather than all-or-nothing — a latent pre-existing bug found
   during the survey (an item with only some columns overridden was
   silently losing the rest). The base-item picker went from
   reference-only to actually functional: picking a base item now feeds
   its own Main Type in as the Masterwork item's Optional Type, via a
   new `resolveBaseItemMainTypes` helper — needed because a base item
   like Light Armor doesn't have one fixed Type of its own, it's
   craftable via three different Schools each with a different material,
   so the helper takes the union across all of them. Caught and fixed a
   real bug here too: my first pass tried to read `baseItem.main_materials`
   directly, which is blank for anything (like Armor) whose Type lives
   on the recipe table, not the item — the Playwright screenshot showed
   the Optional Type missing before this was caught. Removed
   `itemGoldValue`/`parseGoldNumber` as dead code once the Gold-derived
   token was gone entirely.
5. Verified via the CLAUDE.md-documented Playwright sandbox workflow
   (local testsite/, React/ReactDOM/Babel/qrcode-generator vendored via
   `npm install` since the CDN proxy blocks unpkg.com directly but
   allows the npm registry) across a Weapon (item-override + recipe
   merge), a Masterwork item (base-item-driven Optional Type, including
   live-switching between two base items and watching the Materials
   line update), a Potion, and a Food item with a pre-existing per-item
   override — all rendered correctly, no new console errors.
6. `rulebook.md`'s `#### Materials`/`#### Time`/Examples rewritten to
   match (the "base item" paragraph drafted earlier in this file turned
   out not to need revision — the Main/Optional model was already
   compatible with it once written).

**Concise baseline recipe format** (this is what actually shipped, in
both `rulebook.md` and the data):

> Gather a number of materials equal to the item's Total Materials. Every
> material used must be at least the item's Level.
>
> A recipe lists Main material Types and, if it has any, Optional
> material Types. At least half your materials (rounded down) must be
> Main Types; the rest can be Optional Types instead, up to half.
>
> Masterwork items are built onto a base item (see "base item," above).
> Rather than listing their own Optional Types, a Masterwork entry lists
> only its own Main Type — usually just one — and the chosen base item's
> own Main Type becomes this item's Optional Type instead. A
> Fire-aligned weapon enhancement always lists Fire as its Main Type;
> built onto a Metal-based sword, Metal becomes its Optional Type, or
> Wood if it's built onto a Carving-based bow instead.
>
> Example: Enith wants to forge a blade wreathed in shadow. She settles
> on Elemental-Forged Weaponry, a Level 3 Masterwork enhancement (Main
> Type: Shadow, Total Materials 20), built onto a Metal-based sword as
> her base item, giving Metal as her Optional Type. She needs at least
> 10 Shadow-aligned materials, and can round out the rest with up to 10
> Metal — she spends 10 Shadow-aligned scraps (including a Level 5 one
> saved from a shade she put down last week) and 10 Level 3 Metal
> ingots, all Level 3 or higher.

Verified against that worked example: Total 20, half = 10, 10 Shadow
(Main) + 10 Metal (Optional) = 20. Checked with an actual calculation,
not asserted — see the standing note below on why that matters here
specifically.

**Previously flagged risk (Cost ÷ Level rounding to 0 for low-Cost
items) is now moot, not just unresolved** — resolved by the correction
above: Total Materials is never computed from Cost at rule-time, so
there's no division that could round to a degenerate 0. Noting this so
a future pass doesn't waste time re-chasing it.

**Follow-on: `#### Time` simplified to two flat baselines.** A fresh
review of Tools/Time (after Materials landed) surfaced two things: the
old intro sentence claimed Time varied by "item type, relevant Skill,
materials, and creation School" when the actual rule only ever varied
by two of those, and Food/Cooking had no stated crafting time at
all — neither the "Alchemy items" 1-hour bucket nor the Craft-School
8/4-hour bucket covered it, a gap that predates this session, not
something the Materials migration introduced. Separately, that
migration itself introduced a live inconsistency worth naming even
though it wasn't the thing being fixed: Materials now differentiates
by weapon/armor size (Light 1H needs 3, Heavy 2H needs 6) where it
didn't before, but Time stayed one flat 8-hour bucket for all of
them — before, both were flat, so at least they agreed with each
other; now only one scales with size.

Resolved by collapsing to two categories, explicitly framed as a
baseline rather than a precise rule: clothing/armor/weapons/similar
equipment (including Masterwork, no longer needing its own separate
sentence) take 8 hours; Alchemy and Food consumables take 1 hour and
can be batched (any number of the same item at once). This directly
answers the Food gap (now explicitly in the consumable bucket) and the
overclaim (two buckets, not four factors) — and sidesteps the
weapon-size-vs-Time mismatch by making the numbers openly GM-adjustable
rather than pretending a fixed rule already accounts for it. Applied
in commit `0799328`.

**Follow-on: per-recipe-type review, starting with Basic Gear and
Weapons.** With the unified Total/Main/Optional shape in place, went
through the recipes type-by-type checking each one's Main/Optional
lists are reasonably standardized (roughly 1-2 Main alternatives, 2-3
Optional alternatives, per the user's own Masterwork-fire-sword
example of what counts as "plenty of flexibility while staying
simple"). Flagged Medicinal Supply as a categorization outlier (Alchemy
School, flat Total 2, single-use "spend it" item — reads more like a
Consumable than Basic Gear) and recommended folding it into a later
Alchemy/Consumables pass rather than acting on it now — not yet done.
Flagged two Basic Gear rows exceeding the 2-3-Optional guideline:
Armor - Light (Smithing) (4 Optional Types) and Basic Clothing (4
Optional Types, but deliberately kept as-is — it's the maximally
generic catch-all slot item, an intentional exception). Trimmed CR005
(Armor - Light (Smithing))'s Optional Materials from `Cloth, Leather,
Wood, Bone` down to `Cloth, Leather`, matching its Carving/Tailoring
siblings. Applied in commit `6cb6066`.

Then reviewed Weapons specifically: asked whether Carving vs. Smithing
were ever restricted to different weapon subtypes. The original design
doc (`archive/flagonquest_content_original.docx`) said Bows could only
be made via Carving, not Smithing — but the *current* `crafting_recipes.csv`
never actually enforced that: CR001 (Carving)'s description carried
the restriction as prose ("Bows can only be made this way"), while
both CR001 and CR002 (Smithing) used the identical unrestricted
`Applies To: Category:Weapon`, and the `Applies To` mini-syntax
(`matchesRecipeApplies` in `index.html`) only supports ANDed inclusion
clauses (`Category:X`/`Name:X`/`NameContains:X`) — no exclusion/NOT
operator exists, so the restriction couldn't have been enforced as
written even if intended. Rather than adding a NOT-clause to fix the
mismatch, the user decided the restriction itself isn't worth keeping
— there's enough fantasy justification for a metal bow/crossbow, and
no balance reason to keep Smithing from making every weapon type. Fix
was just to drop the stale "Bows can only be made this way" sentence
from CR001's description; no `Applies To`/schema/index.html change
needed, since both rows were already unrestricted in practice.

Then Armor: the doc's *"Heavy armor can only be made using Smithing"*
restriction turned out to already be correctly enforced — CR006 is the
only Heavy Armor recipe, no Carving/Tailoring variant exists for it —
so nothing needed fixing there, unlike Bows. But comparing the three
Light Armor variants' Optional Materials against the doc surfaced a
real inconsistency: CR003 (Carving) and CR004 (Tailoring) both list
all three non-Main material categories as Optional (e.g. CR004: Main
Cloth/Leather, Optional Wood/Bone/Metal), but CR005 (Smithing) had
been trimmed to only `Cloth, Leather` during the Basic Gear pass —
dropping Wood/Bone. At the time that trim looked like a reasonable
"tighten an overly-long Optional list" cleanup (see above), but
revisiting it here against Armor specifically as a set, it broke the
3-way symmetry the other two rows already had. Asked the user whether
Wood/Bone belonged there; the design intent turned out to be that
Cloth/Leather and Wood/Bone are treated as full material analogues in
this system — both are "harvested from creatures" style materials
that are broadly interchangeable in crafting — so the correct shape is
full 3-way symmetry (every School's Optional list includes the other
two Schools' Main types) rather than the shorter list. Reverted CR005
back to `Cloth, Leather, Wood, Bone`, and extended the same fix to
CR006 (Armor - Heavy (Smithing)) for consistency — it shares the same
Main (Metal) and the same Smithing School as CR005, so there's no
reason for it to have a shorter Optional list just because it's the
Heavy variant.

Circled back to Weapons with that same principle: CR001/CR002 only
granted `Cloth, Leather` as Optional (per the doc's literal wording,
which never mentions Metal or Wood/Bone as Weapon extras). Explicit
design direction from the user: err toward more material flexibility
generally, since a player already has to invest in a Craft skill and a
small technique just to unlock a creation School in the first place —
the recipes themselves can afford to be permissive. Applied full
symmetry to match Armor's shape: CR001 (Carving, Main Wood/Bone) now
lists Optional `Cloth, Leather, Metal`; CR002 (Smithing, Main Metal)
now lists Optional `Cloth, Leather, Wood, Bone`.

**Alchemy and Consumables pass.** Checked Medicinal Supply against the
doc's own dedicated entry for it — School Alchemy, Skill Total
Mixology 3, Total Materials 2, Main Medicinal, Optional Cloth — and
CR012 already matched exactly, no fix needed there. Two real changes
came out of this pass instead:

1. **Medicinal Supply reclassified as a Consumable.** Its
   `item.category` is `Pack/Gear` (a real inventory-slot distinction,
   left alone), but `craftingGroup()` in `index.html` — the Crafting
   tab's group-filter chips (Base/Masterwork/Alchemy/Food) — was purely
   `item.category`-driven, so it fell into "Base" alongside Weapons/
   Armor/Clothing despite being crafted via the Alchemy School under
   Alchemy's own flat-2 rule. Added a name-based exception (`item.name
   === "Medicinal Supply"` → `"Alchemy"`) so it now filters correctly
   alongside Potions/Poisons/Grenades — confirmed by toggling the
   Alchemy filter chip and checking Medicinal Supply appears while
   Basic Clothing (Base) and Travel Rations (Food) don't. Also
   physically reordered it in `crafting_recipes.csv` to sit right
   before the Alchemical Potion/Poison/Grenade/Food block (swapped
   with "Other Items," which stayed with Basic Gear since it isn't
   itself a consumable) — the two rows just traded IDs (CR011 ↔ CR012)
   and file position; nothing outside the CSV/JSON referenced the old
   numbering (checked — only a stale index.html comment mentioned
   `CR001`/`CR002` by name, unrelated to these two).

2. **Restored the doc's level-scaling Skill Total for Alchemy/Food.**
   The doc states `Skill Total: Mixology [twice the item's Level]` for
   Alchemy (Potions/Poisons/Grenades) and `Mixology or Survival [twice
   the item's Level]` for Food — a genuine, deliberate scaling formula,
   not a typo (Masterwork's own doc entry uses the same idea in a
   different form: `Craft 5 + [the item's Level]`). The live recipes
   had flattened this to `Mixology 3` / `Mixology or Survival 3` at
   some point before this session, with no record of why — most likely
   folded in during the same earlier "similar kind of review" pass that
   produced the Kind/Value-vs-Slots split this whole Crafting overhaul
   replaced. User confirmed: restore the doc's scaling, it looks like
   it got flattened by mistake in that bulk update.

   Unlike the Cost/Materials formulas (a *design-time-only* principle,
   deliberately never written as a live rule — see above), this is a
   genuine live gameplay requirement that scales with which Level the
   item is actually being built at, the same category of thing as a
   Prereq Check's `[Level]` threshold or a Technique's `[Level]`-bracket
   effect text — so it's written as live bracket text
   (`Mixology [twice the item's Level]`) and resolved in `index.html`,
   not pre-flattened into per-item numbers. Extended `parseSkillTotalText`
   to recognize that exact bracket pattern and resolve it against
   `item.levels` — but only when the item has exactly one fixed Level;
   a Level-range item (Travel Rations' "Level 1-5," Basic Poison's
   "Level 1-5") can't produce one number here any more than an
   unresolved technique Level can for a Prereq Check threshold, so it
   falls back to `null` (no computed badge, the raw bracket text still
   displays) rather than guessing — same "flag readiness, don't guess"
   rule used everywhere else this pattern shows up. Didn't attempt to
   parse Food's two-skill `"Mixology or Survival [...]"` form — that
   was already unparseable under the old flat `"Mixology or Survival 3"`
   text too (the regex only ever matched a single `\w+`), so leaving it
   as display-only text is the existing baseline, not a new regression.

   Verified in the Playwright sandbox: Healing Potion (Level 3) shows
   `Mixology 6`, Insanity Potion and Thunderclap-in-a-Jar (Level 5) both
   show `Mixology 10`, Bottled Fire (Level 2) shows `Mixology 4` — all
   correctly `2 × Level`. Basic Poison and the seven named Poison
   sub-types (Bloody/Crippling/Necrotic/Vulnerability/Harrying/
   Psychosis/Slowing) correctly show the raw unresolved bracket text
   with no Skill badge, since they either have a Level range or (the
   seven sub-types) no Level at all — worth noting that gap predates
   this change and isn't something this pass introduced: those seven
   are really just flavor options under "Basic Poison" (per the doc,
   "Choose a Basic Poison" from that list) rather than independently
   Level'd craftable items, so the missing badge there is arguably more
   correct than the flat "Mixology 3" badge they used to show.

**STANDING RULE — Optional Materials shouldn't repeat an item's own
Main Type.** Asked the user to sanity-check that most Alchemy/Food
items really do reduce to "one Main ingredient + a blanket Optional
list to pad with." Mostly true, with two real findings: Energizing
Brew (a Potion) had no Main Type at all — a plain data gap, unlike the
Poison sub-types' *intentional* absence — and several Grenades whose
own Main is Fire (Bottled Fire, Smokejar, Hellfire Bomb,
Thunderclap-in-a-Jar) sit under CR015, whose recipe-level Optional
list is `Medicinal, Fire` — meaning Fire is redundantly listed on both
sides for those four. User's ruling, stated as a general principle
going forward: **if an Optional entry duplicates something already in
an item's own Main, drop it from Optional — it does nothing there.**
The Main≥half/Optional≤half split already lets a player use up to
100% Main-Type materials on their own, so re-listing a Main Type under
Optional never unlocks anything extra; it's purely a cosmetic
redundancy, confirmed by how `craftingMaterialsEligibility` in
`index.html` already unions `mainTypes` and `optionalTypes` into one
allowed set — dropping the duplicate doesn't change what's craftable,
only how the requirement reads.

Applied immediately: gave Energizing Brew (`I037`) a Main Type of
`Medicinal` (per the user's #1 answer), and since that now duplicates
CR013's recipe-level Optional (`Medicinal`), added a per-item Optional
override of `None` (the same "explicit empty" convention Travel
Rations already uses) to drop the redundancy the fix itself created.
Noticed Basic Poison (`I049`) already had this exact same redundancy
independently (its own Main is `Medicinal`, same as CR014's Optional)
— pre-existing, not something either fix introduced — and applied the
identical `None` override there too, since it's the same pattern the
user just ruled on. Confirmed via `craftingMaterialsEligibility`'s
union logic that this is a display-only cleanup for both, not a
behavior change (Basic Poison's craftable pool was always "100%
Medicinal" either way).

**Resolved.** Shown the Grenade table above, the user reconsidered
keeping Fire as a blanket Optional at all — on reflection, "Alchemy
has Medicinal as a glue type" (i.e. the one shared padding material
across every Alchemy/Consumable recipe), Acidic Flask should keep its
own unique flexibility as a cheap-materials outlet via its Main
OR-list rather than needing Fire in Optional too, and any real
elemental-material variety belongs in future Masterwork/Alchemy
additions rather than being baked into Grenade's Optional list. So
rather than the narrower per-item fix considered above (dropping Fire
only from the four Fire-Main items' own Optional), simplified further:
dropped Fire from CR015's Optional Materials entirely, leaving just
`Medicinal` — now identical in shape to Potion (CR013) and Poison
(CR014). No per-item overrides needed anywhere, since the redundancy
this whole sub-thread started from no longer exists at the source.
Alchemy/Consumables recipes are now uniform: every one of Potion,
Poison, and Grenade has `Medicinal` as its sole Optional padding
material, and Food alone keeps a second Optional Type (`Bone`)
alongside Medicinal, deliberately, since Food is meant to be more
flexible than the others (managing it is expected to be a lighter
concern for most parties than needing a broad Alchemy stockpile).

**Masterwork overview pass.** By far the least-finished recipe type —
much bigger gaps than anything found in Weapons/Armor/Alchemy/Food.
Surveyed all 60 Masterwork items against the doc's own Masterwork
section and found three real structural holes, one of which is now
fixed:

1. **Skill Total: 0/60 items had one stated — now fixed.** The doc's
   rule, `Craft 5 + [the item's Level]`, had genuinely never been
   applied anywhere (not at the CR017 recipe level, not per-item).
   User confirmed it's intentional and just never made it into the
   CSV. Applied it to CR017 as live bracket text (same "genuine
   gameplay formula, not a design-time-only Cost/Materials thing"
   reasoning as Alchemy/Food's Level-scaling Skill Total) and extended
   `parseSkillTotalText` with a third pattern —
   `^(\w+)\s+(\d+)\s*\+\s*\[the item's Level\]$` — resolved the same
   "only when the item has exactly one fixed Level" way as the
   `[twice the item's Level]` pattern. Also gave Spirit Quest Ointment
   (`I116`) its own `Mixology 5 + [the item's Level]` override, since
   it's the one Masterwork item with a non-Craft School (Alchemy) —
   Jewelrymaking (the other three School-overridden items use
   Carving/Tailoring/Jewelrymaking) is Craft-governed same as
   Smithing/Carving/Tailoring, per the existing Artisanal Training
   Prereqs mapping, so it didn't need an exception; only Alchemy/
   Cooking Schools use Mixology/Survival instead. Verified in the
   Playwright sandbox: Mask of Night (Lv1) → Craft 6, Confident Cap
   (Lv3) → Craft 8, Crown of Glory (Lv5) → Craft 10, Spirit Quest
   Ointment (Lv3) → Mixology 8 (correctly Mixology, not Craft), and
   Level-range items (Cowl of Tranquility, Lifeforce Plate, Tactician's
   Band, Dauntless Wrap) correctly show the raw unresolved formula text
   with no badge rather than guessing.

2. **Base Item Options: only 23/60 (38%) have any set — not yet
   fixed.** Not randomly missing — maps cleanly by Slot. Held
   (weapons, 17/17) is complete. Torso (armor) is 6/9, and even those
   6 only reference Light/Heavy Armor, missing the doc's "or basic
   clothing" half. Every other Slot — Head (0/5), Neck (0/4), Ring
   (0/10), Hands (0/3), Feet (0/6), Belt (0/2) — has never had Base
   Item Options touched at all, despite the doc stating a clean,
   simple per-slot rule for every one of them (Head: clothing or
   jewelry; Neck/Ring: jewelry; Hands/Feet/Belt: clothing). The 4
   "Other"-slot items (Evertoking Bottle, Distant Scroll Cases,
   Placeholder's Spacious Satchel, Spirit Quest Ointment) fall outside
   any doc-defined slot section entirely — bespoke items that need
   individual review rather than a blanket per-slot rule.

3. **School: only 4/60 stated (the same 4 "Other" items) — not yet
   fixed.** The doc's rule ("same as base item") was never built as a
   dynamic resolution the way Optional Type was
   (`resolveBaseItemMainTypes`) — so even the 23 items with a working
   base-item picker still show no School.

Also noted: Total Materials is solid (flat 20 across 59/60 items,
matching the established design principle), with Spirit Quest
Ointment's 15 as the one outlier — not yet asked about, flagged for a
later pass. Every one of the 60 items does have its own Main Type
stated (no Energizing-Brew-style gap there).

Sequencing agreed with the user: Skill Total first (done, above), then
Base Item Options by Slot (mechanical fill-in for Head/Neck/Ring/
Hands/Feet/Belt following the doc's clean rule; fix Torso's missing 3
items and add the missing Basic Clothing option to all 9), then the 4
bespoke "Other" items individually last.

**Spirit Quest Ointment moved out of Masterwork entirely.** Before
even reaching the "Other" items in that sequencing, the user decided
it was never really a Masterwork enhancement to begin with — a
one-time-use ritual item (spend 24 hours, reassign all Experience),
not a permanent worn/held upgrade like the rest of the category — and
reclassified it as a Potion instead, explicitly accepting it as "a
special-rule consumable that breaks the pattern" going forward rather
than trying to force it to fit either category's mold. Category
Masterwork → Potion, Slot cleared (Potions don't have one), School and
Skill Total cleared so it now inherits CR013's standard Alchemy
School and `Mixology [twice the item's Level]` formula (resolves to
Mixology 6 at its Level 3, down from the Masterwork-formula Mixology 8
it had for about one commit) — its outlier Total Materials (15, not
Potion's flat 2) and three-Type Main (`Brilliant, Shadow, Medicinal`)
both stay, since those are exactly the "breaks the pattern"
specialness the user wants kept. Gave it an explicit Optional
Materials override of `None`, since Medicinal — CR013's blanket
Optional — is already one of its own Main Types (the same
redundancy-avoidance standing rule from the Alchemy/Consumables pass).

That surfaced a real, separate bug while verifying: `parseTypesList`
in `index.html` didn't special-case the literal text `"None"` the way
`parseSkillTotalText`/`parseSchoolList` already special-case `"Varies"`
— so an explicit `None` Optional override parsed as one literal Type
named `"None"` instead of resolving to no Optional Types at all,
rendering as a stray "or up to half None" in the Crafting tab. This
silently affected every existing `None` user (Travel Rations, Basic
Poison, Energizing Brew — all from this same session) too, not just
Spirit Quest Ointment; fixed by making `parseTypesList` resolve `None`
to `null`, same as a blank cell. Re-verified all four in the
Playwright sandbox — none show the stray text anymore, and Spirit
Quest Ointment now correctly groups under the Alchemy filter chip
(confirmed absent from Masterwork's).

**Base Item Options filled in, by Slot, following the doc's rules.**
Before filling anything in, found the validation would have blocked
most of it: `convert.py`'s Base Item Options check required an *exact*
Slot match between a base item and the item referencing it, but Basic
Clothing (`I002`) and Basic Jewelry (`I003`) both have a blank Slot of
their own (deliberately — they're meant to cover several slots, not
tied to one), so referencing either from a Head/Ring/Neck/Feet/Hands/
Belt item would have failed that check. Fixed the validation first: a
base item with no Slot of its own is now treated as a wildcard (skips
the match check); an item that *does* carry a real Slot (actual
Weapon/Armor pieces) still has to match exactly, preserving the
existing Held/Torso behavior.

With that fixed, filled in Base Item Options for every Masterwork item
outside Held (already complete) and the 3 "Other" bespoke items (still
deferred), straight from the doc's per-slot rule: Head → Basic
Clothing or Basic Jewelry (`I002,I003`); Neck and Ring → Basic Jewelry
only (`I003`); Hands, Feet, and Belt → Basic Clothing only (`I002`);
Torso → armor or basic clothing (`I128,I129,I002`) — this also fixed
Torso's two outstanding gaps at once, since it both filled in the 3
items that had nothing (Attuned Shroud, Robes of Resilience, Robes of
the Elemental Lord) and added the missing Basic Clothing option to the
6 that already had Light/Heavy Armor. 39 rows touched in total, `python3
convert.py` came back with zero validation warnings, and spot-checked
one item per slot in the Playwright sandbox (Mask of Night, Bloodshard
Ring, Cobblestone Boots, Smuggler's Belt, Elemental-Resistant Armor,
Attuned Shroud) — every base-item picker and its resolved Optional
Type show correctly, no page errors.

Base Item Options coverage across Masterwork is now complete except
the 3 "Other" items, which the doc never defines a slot rule for and
still need individual review. School's dynamic resolution (the doc's
"same as base item" rule, never built the way Optional Type's
`resolveBaseItemMainTypes` was) remains the one open structural gap
from the original overview.

**Old-docs review, drafted into the current data (pending the user's
balance-pass review).** The user pulled four more old design documents
(`archive/flagonquest_manifesto_2k19.md`, `flagonquest_manifesto_v5.md`,
`flagonquest_items_2k20.md`, `flagonquest_items_2k22.md` — converted
from `.docx` via `mammoth`, which preserves headings/lists/bold far
better than the earlier XML-regex fallback) specifically to check for
old Techniques and Masterwork items that never made it into the
current data. Two background research agents cross-referenced both
doc pairs against `techniques.csv`/`items.csv`/`rulebook.md`/this file
and found: 8 old Techniques with no current analogue (mostly one
connected idea — a card-discard resource loop built around the
now-defunct Focus resource, which predates the current card economy),
18 candidate Masterwork items with no current analogue, and a handful
of still-open rules ideas (a GM difficulty-by-Level table, enemy/
encounter design guidance, and an Adventuring Goods gap above the
current "Cart, Small"). The Techniques and general rules ideas are
left for the user to decide on — only the Masterwork items and the
Adventuring Goods gap were actionable data work, so those got drafted
in now, at the user's request, as `I148`-`I167`.

All 18 Masterwork items follow the just-established per-slot Base Item
Options rule rather than what each old write-up individually stated —
several of the old Neck items said "Base Item: Basic clothing," but
Neck items now uniformly resolve to Basic Jewelry only (`I003`) per
the doc-derived rule applied in the previous pass, and that took
priority over the old per-item text. The 3 "Other"-slot items
(Immaculate Spice Rack, Unmovable Bar, Placeholder's Indelible
Instrument, Placeholder's Wondrous Workspace — actually 4, see below)
get no Base Item Options at all, matching the existing 3 "Other" items
that still need their own individual review.

A few explicit judgment calls the user should check in the balance
pass:
- **Cloak of Faces** was sitting in the old doc's "THE BIN" section (a
  rejected-ideas dump), not the main item list — drafted in per "draft
  up entries for all of those items," but flagged here as possibly
  intentionally shelved rather than overlooked.
- **Ring of Pure Elements** merges two versions of the same idea: 2k20's
  fuller "Signet of the Elementalist King" (choose Fire/Frost/Brilliant/
  Shadow/Physical once per encounter, plus a since-defunct "spend Focus
  to bypass the limit" clause) and 2k22's simpler, later "Ring of Pure
  Elements" (fixed to Brilliant only, no choice). Drafted as the fuller
  4-element choice mechanic (dropping Physical and the Focus clause) at
  2k22's more conservative Level 3, rather than either version verbatim
  — a real synthesis call, not a straight port.
- **Greaves of the Warlock King** (free Teleport twice Speed, 1 AP,
  once/turn) is notably stronger than the current Slipstream Sandals
  (flat 3m, once/encounter) — already flagged in the original summary,
  carried through into the draft as-is rather than pre-nerfed, since
  that's exactly the kind of thing to catch in a balance pass rather
  than silently soften before the user even sees it.
- **Placeholder's Wondrous Workspace**'s old mechanic ("counts as any
  item creation toolkit, each counting as two Level 2 materials of any
  type") referenced the old Gold-token materials system this project
  already moved away from. Simplified to "fulfills the tool or Skill
  Kit requirement for any creation School" — same intent, no live
  formula. Given School: Smithing explicitly (matching what the old doc
  stated) rather than inheriting CR017's "same as base item," since it
  has no Base Item at all to inherit from.
- **Choker of Defiance**, **Ring of Charming/Assertive/Bold Statements**,
  and **Placeholder's Speedy Scepter** had no stated Material Type in
  the old docs at all — assigned Precious to all three as a reasonable
  generic "worked magic item" material, purely a placeholder judgment
  call pending the user's own preference.
- The 4 "Other"-slot items got a slightly wider Main Materials list
  than their old-doc "Material Types" line, specifically because they
  have no Base Item Options and therefore no Optional Type ever
  resolves for them (same situation as the pre-existing 3 "Other"
  items) — a single narrow Main Type would leave them with no
  crafting flexibility at all.

**Cart, Medium / Wagon, Large — added, with a real balance catch.**
The old doc priced Cart, Medium at 12 Gold and Wagon, Large at 24 —
but the *current* "Cart, Small" (`I012`) already costs 12 Gold flat,
meaning importing the old numbers verbatim would have made "Medium"
cost the same as "Small," with no progression at all. Rescaled using
the same doubling-per-tier convention already established elsewhere
in this project (Light/Heavy Armor: 4/8 Gold; 1H/2H Weapons: 3/6 Gold)
— Small stays 12, Medium becomes 24, Large becomes 48 — which also
happens to preserve the old doc's own internal Medium:Large ratio
(12:24 = 1:2, same as the new 24:48). Added in the same blank-
Materials-fields style as the existing Cart, Small (no School/Skill
Total/Total Materials/Main Materials populated — matches how Small
Cart isn't hooked into the Crafting tab's auto-matching at all, and
presumably falls under CR011 "Other Items"' reference-only guidance
at the table instead).

All 20 new rows (`I148`-`I167`) verified in the Playwright sandbox —
spot-checked a range of cases (a fixed-Level Neck item resolving
Craft+Level and its Optional Type from Basic Jewelry, a Level-range
item correctly showing unresolved Skill Total text, a Held item
correctly listing every weapon base-item option, an "Other"-slot item
with no Optional Type suffix since it has no base item, and the
School-override item showing "Smithing" instead of "—") — all correct,
zero page errors, and the one comma-containing name (Ring of Charming,
Assertive, or Bold Statements) round-tripped through CSV quoting fine.

**Site export gap-fill — 22 more Masterwork items, 18 non-Masterwork
items, `I168`-`I207`.** Same idea as the docx-derived batch above, but
sourced from `archive/flagonquest_site_items.md` (the old Google Sites
export) instead — two background agents cross-referenced its
Masterwork sections and everything else against the then-current
206-row `items.csv`. One of the two agents got interrupted mid-run by
the user; resuming it via a fresh `Agent` call (rather than properly
`SendMessage`-continuing the original) accidentally left two parallel
agents running the same Masterwork extraction — turned out to be a
lucky mistake, since the original had actually finished successfully
in the background (its result just hadn't landed yet) and the
duplicate surfaced 6 additional genuine gaps the first pass missed
(Cape of Many Pockets, Periapt of Constitutional Integrity, Jerkin of
the Land, Returning Knives, Spiritlink Scepter, Scepter of Evocation),
so both results got merged rather than the duplicate being wasted
work. Note for next time: use `SendMessage` to resume a specific
agent, not a fresh `Agent` call — this worked out, but was luck, not
the right mechanism.

Real, recurring old-design pattern worth naming: several of the new
gaps are the *same power offered on an alternate slot's base item* —
Jerkin of the Land (Torso) duplicates the already-drafted Shawl of the
Land (Neck)'s no-food/water effect; Periapt of Constitutional
Integrity (Neck) duplicates the existing Armor of Constitutional
Integrity (Torso, `I069`); Cape of Many Pockets (Neck) duplicates the
existing Sash of Deep Pockets (Belt, `I105`). The old site apparently
offered players a slot choice for some powers rather than fixing them
to one slot. Kept all of these as separate items rather than treating
them as pure duplicates, since the old design intent was clearly "same
power, pick your preferred slot" — worth deciding explicitly in the
balance pass whether that's a pattern to keep going forward or a
one-off relic to consolidate.

Scope trimmed from what the agents found: dropped Wand, Orb of the
Weave, Signet of Technical Prowess (+ its Tactician's Band
Power-boost variant), and Mitts of the Great Beast. The first three
depend on mechanics that don't exist in the current rules at all
(a generic Technique "Power score," a spell-emulation-via-fixed-stats
subsystem, a "commit" resource) — real redesign work, not a
translation job, so left as a future design question rather than
force-drafted. Mitts of the Great Beast was flagged by its own
finding agent as likely just an early draft of the already-existing
Mighty Mitts (`I077`, same Hands/Level 3 slot, same "Good Luck on
Might" idea) — excluded as a probable duplicate rather than drafted
alongside it. Also excluded, from the non-Masterwork side: the 7
"reflip cards" tier-6/8 Potions from the older "Alchemical Goods" page
(Bottled Wit, Extra Heartbeat, Placeholder's Profound Potion, Steady
Heart, Strongbrew, Coursing River, Quickmend Potion) — the newer
"Alchemical Items" page's own potion list already dropped every one of
these, meaning the designer had already deliberately cut them in a
later revision, not merely never gotten around to porting them; and
the entire dice-based/Mana-resource "Items" page sub-list (Mana
Potion, Elixir of Might, Dragon Rum, Shockwave Jar, Inferno Jar,
Bottled Sunlight, plus a ~25-item batch of charm/ring items) — a
structurally distinct older ruleset predating the current card system,
flagged by its own finding agent as not straightforwardly portable.

Terminology translations applied while drafting (old Stat/Skill/Defense
names don't match current ones — checked `index.html`'s `STAT_SKILLS`
and `rulebook.md` directly rather than guess): old "Elementalism"
Skill → current **Sorcery**; old "Argument Defense"/"Suspicion
Defense" (no current equivalent) → **Instinct Defense**/**Mental
Defense against Statements** respectively, matching how Persuasion
targets Instinct and Presence/Rapport target Mental; old "Willpower"/
"Focus"/"Mana" spends → dropped entirely, no current equivalent
resource; old "Off-Balance" effect (Quartz Tincture) → substituted
**Harried** (an existing debuff), not a literal port. Also caught and
fixed a **real pre-existing bug** from the earlier docx-derived batch
while doing this: `Ring of Charming, Assertive, or Bold Statements`
(`I157`) referenced fictional "Maneuvering/Debate/Forceful Statement"
subtypes that never existed in the current rules (Statements are just
a flip using Presence, Rapport, or Persuasion, no further subtyping) —
fixed to gate on those three Skills directly instead.

**A second redundancy sweep, and a clarified scope for the standing
rule.** Verifying the new batch in Playwright surfaced the same
Main/Optional-redundancy pattern from the Alchemy/Consumables pass
(`Kiss of the Earth`, `Predator's Cry`, `Revivification Draught` all
had `Medicinal` in both their own Main and CR013's inherited Optional;
`Windrider's Loop` and `Placeholder's Bottomless Belt` likewise
duplicated their single base item's own resolved Optional Type) — all
five trimmed. Running the same check retroactively across *all*
existing Masterwork rows turned up two more, both pre-existing bugs
from the earlier docx batch (`Choker of Defiance` and the just-fixed
`Ring of Charming...`, both placeholder-Main'd as `Precious`, which
collided with Ring/Neck's own resolved Optional of `Precious` via
Basic Jewelry) — reassigned both to `Metal` instead.

Doing this sweep clarified the standing rule's actual scope, which
hadn't been made explicit before: it applies cleanly to **single-base-
item slots** (Neck/Ring resolve to Basic Jewelry's `Precious` only;
Hands/Feet/Belt resolve to Basic Clothing's `Cloth` only — one fixed
Optional, no player choice involved, so an overlap is unconditionally
redundant). It does **not** apply the same way to **multi-base-item
slots** (Head chooses between Basic Clothing/Basic Jewelry; Torso
between Light Armor/Heavy Armor/Basic Clothing; Held between 9 weapon
types) — there, Optional is resolved *per whichever base the player
actually picks*, so a Main Type overlapping with the *union* only
overlaps for some picks, not all. Several already-shipped Torso items
already have this shape (Dauntless Wrap, Coat of Knit Flesh, Fortified
Armor, Robes of Resilience) and weren't touched — Jerkin of the Land
and Fitted Armor (both Torso, both new) and Headband of Telepathy
(Head, new) have the same overlap-with-the-union shape and were left
alone too, matching that established precedent rather than
retroactively "fixing" something that was never actually broken.

**Final Masterwork completeness/dedup sweep — 4 more items, `I208`-`I211`,
plus 3 pre-existing bugs surfaced along the way.** Before starting the
Masterwork balance pass, ran a dedicated agent to cross-check the full
99-item Masterwork list (59 pre-existing + the 22 docx-derived + the 18
site-export-derived) against every archived source doc one more time,
specifically hunting for (a) items still genuinely missing and (b)
accidental duplicates between the docx-derived and site-export-derived
batches, since those were drafted by different agents in different
sessions with no way to see each other's work.

Found 5 candidate-missing items, all buried in a scrap-dump section
titled "MASTEROWKRK ITEMS OF WONDER AND MYSTERY" in `site_other.md`/
`site_techniques.md` — a lower-priority file the original site-export
pass hadn't fully mined. 4 were portable and got drafted:
- **Elemental Warding Amulet** (`I208`, Ring, Level 1-2) — a Ring version
  of `I067` Elemental-Resistant Armor's exact mechanic (+1/+2 Resist to
  a chosen element, scaling with Level). Straight "same power, different
  slot" port, no new numbers invented.
- **Mendicant's Cord** (`I209`, Belt, Level 2) — touch yourself or a
  willing adjacent creature and shift up to 2 points from one Defense to
  another (can't push the raised one above the lowered one's new value).
  A genuinely novel mechanic, no current analogue.
- **Scaraculpi's Gleaming Justice** (`I210`, Held, Level 5) — unconditional
  Good Luck on all attacks with the weapon, no action cost. Stronger than
  `I103` Thrumming Focus's AP-gated version of the same benefit, but the
  old doc places it at Level 5 (this system's top tier) and other Level 5
  items are similarly strong (`I104` Apocalyptic Staff gives a free
  Level-4 spell once per encounter) — ported at face value, flagged here
  as a first candidate to sanity-check once the balance pass actually runs.
- **Worry Token** (`I211`, Neck, Level 2) — a 3-charge daily trinket with
  a GM-secret random-effect table (mostly "nothing happens," occasionally
  a minor heal/flip bonus/Defense bonus/Resist-ignore/card draw). Ported
  close to verbatim; it's an unusual mechanic for this catalog (no other
  item hides its effect from the player) but nothing about it needed
  redesigning, just translating "Armor Soak" → "Physical Resist."

**Shield of Supplies excluded** — its own source text is just "U" (an
unfilled placeholder marker) followed by two open questions ("Holds like
an Adventurer's Kit? Can dismiss items and they can be re-grabbed from
the shield?"). Unlike the other 4, this was never actually a decided
mechanic to translate, just a stub idea — same exclusion basis as Wand/
Orb of the Weave/Signet of Technical Prowess from the earlier pass
(needs real design work, not translation). Elemental Staff and Invoker's
Scepter, also in the same scrap dump, were confirmed to fall under the
already-documented Willpower/spell-commit incompatibility that justified
excluding Wand/Orb, plus Invoker's Scepter has no effect ever written
for it at all.

**Bugs found and fixed while cross-checking:**
- `I169` Stoic Skullcap and `I170` Sympathetic Hat (both Head, Level 2)
  had ended up with byte-identical Effects text ("+1 bonus to Mental
  Defense against Statements"). Root cause: the two old items used
  different old Defense names — Stoic Skullcap's source already said
  "Mental Defense during social contests" (no translation needed);
  Sympathetic Hat's said "Suspicion Defense," which the established
  Argument/Suspicion → Instinct/Mental translation rule (see the
  terminology-translations note above) correctly maps to "Mental
  Defense against Statements" too. The two old Defenses genuinely
  collapse onto the same current one — this isn't a translation error,
  it's current rules being simpler than old ones (old had a 3-way
  Defense split for Statement subtypes; current only has 2). Since a
  same-slot, mechanically-identical pair is still redundant as a
  catalog entry regardless of why, re-differentiated Sympathetic Hat
  instead of leaving the collision: its own fluff text ("attune the
  emotions of the wearer with those around them... helps them
  understand the feelings that drive others") is about reading other
  people, not resisting persuasion — and a different old-era source
  line (an Insight Skill blurb: "determines your Reflex bonus as well
  as your Suspicion Defense") independently backs Insight, i.e. current
  **Instinct Defense**, as the better-fitting translation for this
  specific item. Changed to "+1 bonus to Instinct Defense."
- `I073` Robes of Resilience used the old term "Soak" instead of
  current "Resist" in its Effects text (bonus value itself, +1, was
  already correct against source) — fixed the wording only.
- `I074` Robes of the Elemental Lord read "+3 bonus to Fire, Frost, and
  Shadow Resists" — checked against its own source
  (`site_items.md` line 2254, the more-current-looking of two listings,
  since it already used "Resist"/"Brilliant" rather than the other
  listing's older "Soak"/"Spirit"), which says "+2 bonus to Fire,
  Frost, **Brilliant**, and Shadow Resists." Current data had both an
  inflated bonus (+3 vs +2) and a missing element (no Brilliant) —
  fixed to match source. Predates this project's two item-gap-fill
  sessions, so it's an older transcription slip, not something either
  drafting pass introduced.

Total Masterwork count is now 103 (`I057`-`I115`, `I148`-`I165`,
`I168`-`I189`, `I208`-`I211`), confirmed no ID gaps/typos and
`Base Item Options` internally consistent across all of them. This is
the full list going into the balance pass.

## Applied so far

- `rulebook.md`: `### Gambling and Extra Successes` split into `### Successes`
  (base success + suit-match Extra Successes only — the margin-based
  "+1 per full 2 points over the difficulty" idea was considered and
  explicitly cut, so Gambling and suit-matching are the *only* sources
  of Extra Success) and `### Gambling` (reframed as a bet declared
  before the flip, not a GM-gated option). `### The Suit Pool` got the
  Skill→Suit bullet list plus a matching-suit example. Every Skill's
  `#### ` description in "Stats and Skills" got a trailing sentence
  naming its governing suit, for redundancy alongside the Suit Pool list.
- Resolved the "does Hearts keep a universal attack-damage bonus" fork from
  earlier: no. The flat `[Hearts]` damage rule is fully removed from
  `Making an Attack` — attack damage now comes only from the general
  Successes rule (base success, Gambling, and whichever suit governs the
  Skill/weapon used), same as any other flip. This is a deliberate choice
  to let Hearts' combat role stay minimal in favor of its healing/support
  identity, made with full awareness that (per the technique audit
  earlier) only one technique in the game (`Earthquake`) will ever grant
  Hearts a damage-relevant suit match. Also generalized the Extra-Success
  damage bonus to "all damaging attacks" rather than "weapon attacks"
  only, clearing up an inconsistency the old rule had.
- Style notes from this pass, apply going forward: keep explanations
  concise, frame rules positively (state what a thing *is*/*does* rather
  than what it isn't), and lean on the site's existing formatting tools —
  bullets for real enumerated lists, more headers for navigability, and
  break a mechanic's illustration into its own "Example:" paragraph
  (the site auto-italicizes text that starts with "Example:" via
  `renderBlock`, so no manual emphasis markup is needed in the source).
  Also don't reach for a semicolon or a dash-set-off aside as a
  reflex. This supplements CLAUDE.md's existing `- ` aside convention
  rather than overriding it: a dash is still the right call when a
  passage genuinely calls for one, and semicolons and other varied
  punctuation are fine too when they're doing real work, not something
  to avoid outright. Sentences don't need to stay short and
  comma-joined either — natural variety in sentence length and
  structure is good. The actual bar is whether a passage reads
  naturally or feels jarring, not a hard rule against any specific
  mark. When unsure, default to the plainer phrasing and only reach
  for a dash/semicolon if it's clearly the better fit. Given that, the
  already-applied sections (Successes, Gambling, The Suit Pool)
  probably don't need a wholesale retrofit — revisit a specific line
  only if it actually reads awkwardly, not just because it uses a dash.
  Sharpened further during the social contest rewrite: don't write a
  rule to explain what *doesn't* happen just to set up a design note
  about what a future Technique might do. Techniques already
  implicitly can do anything the base rule doesn't cover — stating
  that out loud (an early Social Contests draft had "Extra Successes
  don't reduce Pressure on their own - that's Technique territory")
  is filler, not information. If a design note is worth preserving,
  it belongs here in this file, not in the rulebook prose.

- `rulebook.md`'s `### Supporting` section was reframed: it used to
  read as a fallback for characters who "don't have a good Skill,"
  which came across as dismissive. It's now framed as how the whole
  party stays engaged in a scene together, and explicitly encourages
  reaching for Support whenever you don't have something else going
  on, rather than sitting out. No AP cost is mentioned deliberately —
  Supporting isn't meant to be a formal combat action; Techniques that
  need to interact with it that way spell out their own AP cost, and
  otherwise it falls under the general "most miscellaneous actions are
  2 AP" guidance plus GM judgment.

- `rulebook.md`'s top-level chapter order changed: `# The Basics` now
  comes first (was second, after `# Your Character`), so a new reader
  hits core mechanics before character-building detail. Two short
  primer paragraphs were added to Basics' intro, right after the "what
  is a TTRPG" paragraph, so Skill Checks doesn't presuppose knowledge
  of Skill Total or the card deck that used to come from reading
  Character first: a minimal Stats+Skills-combine-into-Skill-Total
  blurb (explicitly deferring full detail to "the 'Your Character'
  section, later in this book" — named in quotes so it doesn't read as
  literally addressing the player's own character), and an expanded
  version of the existing one-line card-deck mention that now also
  states the 4 suits by name. `# Your Character` (Stats and Skills,
  Techniques, Spending Experience) moved as a whole, unchanged block,
  to sit right after Basics and before `# Health and Resources`.
  Nothing else in the book's order changed.

- Fixed the "does the 75 starting Experience cover Techniques too"
  ambiguity found in the "just for fun" gap review: `## Spending
  Experience` (with its `### Learning Techniques` child) moved from
  `# Your Character` to sit directly above `## Building a Character`
  in `# Character Creation`, and that section's XP bullet now reads
  "Spend 75 Experience to buy Stats, Skills, and Techniques for your
  character" instead of only mentioning Stats and Skills. Also
  confirmed via the Quick Creation walkthrough's own numbers (29 for
  Skills + 28 for Stats + 18 for 6 Technique Levels = 75 exactly) that
  Techniques coming out of the same pool was always the intent, just
  previously unstated.
- Scoping note from the same review: this rulebook is player-facing
  only, not a GM's guide. A GM-side difficulty or ruling being left
  vague (e.g. the group Stealth check's difficulty) isn't a gap by
  itself, the same way "the GM determines the difficulty" already
  works everywhere else — only flag something as a real gap if it's
  about a player's own choices (character building, an action they
  take themselves) rather than GM adjudication this book was never
  going to spell out.

- Major reorder from the "new reader" pacing review: `rulebook.md` now
  opens with a new `# Quick Start Guide` (one-sentence-each bullets
  covering Stats/Skills/Skill Total, flips, suits, Extra Successes at
  a glance, Techniques, Health, Action Points), then `# Character
  Creation` moved to sit right after it (previously last in the whole
  book), then `# The Basics` and everything else in their prior
  order. The idea: worst case, a brand-new player reads the Quick
  Start Guide for the gist, builds a character right away since
  Character Creation is now impossible to miss, and picks up the full
  rules for everything else as they go rather than needing to read
  linearly before playing. Character Creation's own intro sentence was
  flipped to match ("comes first so it's easy to find," rest of the
  book explains everything else in detail) — it used to say the
  opposite ("comes last since it leans on... the rest of the book").
- As part of the same pass, `### Successes` in The Basics was cut way
  down: dropped the exact formula and its worked example, kept only
  "some flips need more than a bare pass, usually for extended effort
  like a tough attack, here's the two ways to earn Extra Successes,
  Adventuring covers exactly how." `### Gambling` kept its rule
  paragraph as-is but dropped Hilde's combat example (which
  presupposes Making an Attack, not yet covered this early) — Carrick's
  lockpicking example stayed since it's a self-contained skill check.
  **Follow-up not yet done:** Adventuring (`Making an Attack`) needs to
  actually gain the fuller Successes treatment this trim promised —
  right now the full mechanical detail that used to live in The Basics
  isn't duplicated anywhere else yet, just referenced as "covered
  later."

- `Making an Attack` now pays off the promise The Basics makes:
  explicitly calls an attack "a check" using the same vocabulary as
  Skill Checks/Successes ("flip a card, add your Skill Total, compare
  to the difficulty"), spells out the full success math inline (1 for
  hitting, +1 Extra Success per Gamble, +1 per matching-suit card)
  instead of a bare cross-reference, and adds a worked example (Jackal,
  spear attack, Gambling once). The explicit design point behind this:
  combat has its own pacing bolted on (AP costs, turn order, the
  declare/flip/resolve steps) but the actual resolution mechanic
  underneath an attack is identical to any other check, not a separate
  minigame the way attack rolls/saves can feel bolted onto a different
  d20 subsystem in something like D&D. Combat Maneuvers (Shove,
  Grapple, Non-Lethal) didn't need their own edits since they already
  just say "make a [Skill] attack" and inherit this automatically.
  Checked for other stale "(see X, above/below)" cross-references left
  over from the various reorders this session — none found outside
  Goblin Game, where they were already valid.

- **Ward's flat bonus doubled, +1 → +2 Resist** (`glossary.md`'s Common
  Effects entry for Fire/Frost/Brilliant/Shadow Ward). Surfaced from a
  balance pass that found Ward underpriced (see
  `design/balance_weights_notes.md`'s Ward writeup) and a design goal to
  make it hit harder. Considered making it scale magnitude per stack the
  way Hasted does (+1 Resist *per stack* instead of a flat bonus while
  any stacks remain) and explicitly rejected it: Resist has no upper
  bound on how much damage it can prevent, so unbounded per-stack
  scaling would let a character who stacks enough Ward become
  functionally immune to a damage type for as long as the buff lasts —
  several existing effects already grant enough stacks to make that a
  real risk, and trivializing a fight built around a specific element is
  exactly the failure mode to avoid. Doubling the flat bonus instead
  keeps the existing "any stacks → this bonus" shape (stacks still only
  ever buy duration, never a growing wall) while making a single
  application meaningfully stronger.
- **Fleeting effects don't decay on the turn they go from 0 stacks to
  some** (`glossary.md`'s `[Fleeting]` entry). Surfaced during the buff-
  Potion balance pass: since decay is a flat "remove 1 from the whole
  pool," not "remove 1 per source," a creature that already has at least
  1 stack of a Fleeting effect is completely unaffected by gaining more
  of it the same turn — the pool's own pre-existing stacks already
  absorb that turn's -1, so topping off a stack you already have was
  never actually broken. The bug only bites the 0→N case: a *freshly*
  granted Fleeting effect (most commonly a self-buff cast on your own
  turn, since that's the same turn its own end-of-turn decay fires) has
  nothing pre-existing to absorb the -1, so it eats directly into the
  brand-new grant — gain 1 Protected, immediately lose it to 0; gain 3,
  immediately down to 2. Past fix for this was ad hoc, baking a "+1 free
  stack" into specific grants (Brace, e.g.) — mostly worked, but doesn't
  know about pre-existing stacks, so it silently over-corrects by 1 in
  the (never-actually-broken) topping-off case, and has to be manually
  remembered and reapplied to every new Fleeting-granting effect. Fixed
  at the rule level instead, scoped to exactly the case that's broken:
  a Fleeting effect skips the next decay after going from 0 to a
  positive count, then decays normally from there on — no new
  bookkeeping needed (still just one stack counter per effect; the only
  check is "was this at zero right before the grant?"), and every
  existing "+1 free stack" item-level patch becomes safe to remove as a
  follow-up cleanup, not required to keep working around this anymore.
- **Ward reimagined: flat Resist + a self-limiting absorption charge**
  (`glossary.md`'s `(Fire/Frost/Brilliant/Shadow) Ward [Fleeting]`
  entry). Surfaced fixing Elemental-Attuned Tincture — even after the
  +1→+2 fix above, every Resist-granting item in the catalog still read
  as underpowered, and raising the flat bonus further was already ruled
  out (unbounded magnitude risks eventual immunity to a whole damage
  type). Instead of a bigger first component, Ward now gets a second,
  self-limiting one: each stack can also directly absorb 1 Health loss
  from that damage type, on top of the existing "+2 Resist while any
  stacks remain." Self-limiting because it's consumed on use, not a
  permanent multiplier — no immunity risk, the same reason Protected
  itself was always safe to price at a real rate. New Ward text: "While
  you have any stacks of this, you have +2 Resist against the specified
  type of damage. If you would lose Health to that damage type from
  something other than a cost, remove up to that many stacks instead."
  See `balance_weights_notes.md` for the value derivation (2.0/stack
  for the absorption piece, reusing Protected's 3/stack rate scaled by
  Resist's own damage-share fraction).

  Applying this exposed one more thing worth tightening while in there:
  **Protected's own wording** ("prevent 1 Health loss... then remove
  that many stacks") reads more like a description of an outcome than
  a hard rule — reworded to a direct, mandatory substitution: "If you
  would lose Health to something other than a cost, remove up to that
  many stacks of Protected instead." One sentence, no "may," value
  unchanged — Ward's new absorption clause mirrors this exact phrasing
  rather than cross-referencing Protected, per the designer's explicit
  call to keep rules text short and self-contained rather than layering
  "same as X, except Y" cross-references.

  **Ripple, checked and resolved:** first flagged this as affecting "7
  Masterwork items and 12 Techniques," a stale count carried over from
  an early, imprecise substring search (it was matching "Resist," not
  "Ward" — corrected after actually grepping for the keyword). The real
  scope is much smaller: only **Warmage's Draft** (this session's own
  Potion, fixed in the same pass — see `balance_ledger.csv`) and
  **Spellblade** (`T100`, a Technique not yet priced against this model
  at all, so nothing to fix there yet) grant Ward. The much larger set
  of items that read as "Resist-granting" and underpowered (Attuned
  Shroud, Elemental-Resistant Armor, Fortified Armor, Robes of
  Resilience, Robes of the Elemental Lord, Charcoal, Elemental Warding
  Amulet, Worry Token) grant a flat Resist stat bonus directly, not the
  Ward keyword — they're unaffected by this change and remain the
  separate, still-open systemic issue already flagged in `balance.md`.

## Open questions / TODO

- **Poison duration — "1 hour" vs. "until your next long rest."**
  Surfaced during the balance pass on Poisons (see `balance.md`'s
  "Poisons were charging AP twice" entry): applying a Poison is meant
  to happen before a fight, but the current 1-hour duration means a
  Poison applied too early can expire unused before it ever gets to
  matter — a real feel-bad at the table. Changing it to last until the
  wielder's next long rest would remove that risk, at the cost of
  making less narrative sense (a poison coating that just doesn't
  degrade for a full adventuring day). Raised, not decided — the
  designer flagged it as "possible" rather than committing to it.
- Presence: Hearts (current) vs. Clubs — genuinely contested, see above.
- Diamonds still has no defensive keyword/mechanic identity.
- ~~The "bad fail" trigger for accumulating multi-attempt checks~~ —
  resolved: this is deliberately left to GM fiat, not a formula. Fits
  the player-facing-only scoping note above; no rules text needed.
- ~~"Stance" → "Form" data-layer gap~~ — resolved: renamed across all
  14 Form-tagged techniques in `techniques.csv` (Tags, Action, plus
  the two in-text mentions — Furious Rage's "While in this Stance:",
  Overchanneling's flavor text), matching the `glossary.md` rename.
  Also converted `Ritual Magic` (T099) itself to a Form (added the
  tag, changed Action to "Passive (Form)"). This crossed the
  data/CSV boundary that was otherwise reserved for the sibling
  chat — the user explicitly asked for it here since it was a
  mechanical rename/tagging change, not new design.
- Scope of the generalized `Ritual Magic`-style card-contribution
  mechanic beyond Spells (still open — the Form conversion above is
  just the mechanical piece, not this broader design question).
- Social contests reworked: no longer a separate team-check subsystem
  with Concessions, front/back positioning, and Charismatic/Strategic
  statement types. A social contest is now just an extended check like
  any other — the GM sets a target number of successes, and a
  Statement (Presence/Rapport/Persuasion, 2 AP implied rather than
  stated since AP only matters in combat) is a normal check against
  the target's Mental or Instinct Defense. **New fixed Defense mapping,
  not a player choice:** Persuasion targets Instinct Defense, Presence
  and Rapport both target Mental Defense — justified by the Suit
  assignments already locked in (Persuasion is the lone Spades skill
  among the three; Presence/Rapport are both Hearts), and by each
  Skill's own rulebook description (Persuasion explicitly covers
  lying, matching Instinct/Insight's "sixth sense" for something being
  off; Presence/Rapport both work on a target's resolve, matching
  Mental/Composure's "staying power in social situations"). Intent is
  a simple baseline players can read NPCs against, with Techniques
  later adding the ability to target the other Defense for a specific
  character build — not built into the base rule.

  Introduced **Pressure**, replacing Concessions: a GM-tracked value
  representing circumstances stacking against the party during a
  contest (a bad disguise, a story straining under scrutiny, simply
  taking too long), applied as Bad Luck on Statements equal to the
  current total. Deliberately not tied to a strict per-round formula —
  "taking too long" only "may" add Pressure, at the GM's pace, matching
  the same GM-fiat treatment as the accumulating-check "bad fail"
  trigger. High enough Pressure is the GM's cue to end the check in
  failure outright. This is also where social-specialist Techniques
  are meant to live down the line (mitigating Pressure, ignoring it
  from specific circumstances) — deliberately not previewed in the
  rulebook text itself, per the style note above.

  `Ending the Contest` and `Results of a Social Contest` (Win Over /
  Disrespect / Agreement) were left almost untouched — they describe
  outcomes, which don't depend on how the party got there. Also fixed
  a stale cross-reference this surfaced: Persuasion's own Skill
  description used to say it "determines your Strategic statements,"
  a term that no longer exists — now says it "targets Instinct Defense
  in a social contest." `glossary.md`'s `Concession` entry was swapped
  for a `Pressure` one.

  Traveling and Exploration reworked: see below.

- **Traveling and Exploration** rewritten from genuinely unfinished
  draft text (literal placeholder fragments like "resolve movement
  last?", "Uh flat difficulty of 11...") that also contradicted the new
  AP-only-in-combat rule by describing hour-long AP-based travel rounds.
  Landed on a leg-based structure after reviewing parallels from other
  systems (point-crawl/leg abstraction generally, Forbidden Lands'
  per-watch concurrent actions, Blades in the Dark's montage-scene
  instinct, PbtA's multi-track failure consequences) — closest model is
  Forbidden Lands' watch: one check per character per leg, no retries
  until the next leg, no fixed real-time round length (GM paces legs the
  same way Pressure isn't tied to a strict per-round formula).

  New structure: `### Legs of a Journey` (GM sets how much ground a leg
  covers based on terrain/danger; one action + one check per character
  per leg, no retries; failed checks are GM-adjudicated as either
  "nothing happens" or "the party fails to avoid a brewing
  complication" — deliberately not a formula, same GM-fiat treatment as
  the "bad fail" trigger and Pressure), `### Scout` (flat difficulty 11,
  matching Support's precedent as a reliably-usable baseline — reveals
  info about *both* the leg currently being traveled and a clue about
  the next one, per explicit correction: "would make more sense if it
  revealed information about the next stretch of journey, including the
  one being traveled... tips players off about anything they might run
  into as they travel"), `### Search` (GM-set difficulty, varies more
  by context; dropped the old "learn why you failed" retry-flavored
  line since it assumed a retry loop that no longer exists), `### Stealth`
  (unchanged in substance, just points at the existing group-check rule
  under Encounter Basics rather than inventing a new one), and a new
  `### Pushing the Pace` (the whole party must agree; trades away every
  character's leg action — no Scout/Search/Stealth that leg — in
  exchange for covering more ground, and removes the "nothing happens"
  half of the failure spread: any brewing complication lands unmitigated
  with no roll). `Move` dropped entirely as a discrete action, since it
  only existed to be AP-gated before. `### Food and Exhaustion` left
  untouched (already uses real hours/days, not AP). Applied to
  `rulebook.md` (commit `a08b24e`); `Pushing the Pace` came from
  directly answering "what would be some good rules... that would allow
  for the party to move faster at some sort of drawback," picking the
  option (narrowing the existing nothing-happens/complication split,
  combined with the lost-action opportunity cost) that added no new
  mechanic rather than a Bad-Luck-flavored or Exhaustion-cost
  alternative also considered.

  A comparison pass afterward ("how is the exploration looking?") flagged
  one seam: `### Food and Exhaustion` was still nested inside Traveling
  and Exploration, running on a literal 24-hour clock while legs are a
  GM-paced, variable-length abstraction — every comparison system ties
  its consequence-clock to its travel-pacing unit directly, and this
  didn't. Resolved by generalizing it rather than reconciling the two
  clocks: it's not wilderness-specific in the first place (1 Food item
  covers a day, applies whether the party's in a dungeon, a city, or on
  the road), so it moved out of Exploration entirely and became its own
  `## Food and Exhaustion` section in `# Health and Resources`, right
  after `## A Full Night's Rest` (thematically adjacent — both are about
  what happens if you skip a night's sleep) and before `## Costs and
  Commitment`. Reworded only the opening framing sentence ("usually,
  while staying in town, exhaustion isn't much of a concern... while
  traveling the wilderness" → "this rarely comes up in town... but it
  matters anywhere they're not") to stop scoping the *rule* to
  wilderness travel while keeping the same in-practice implication that
  it mainly bites away from easy supply access; the actual mechanics
  (24-hour rest window, 1 Food/4L water per day, -2 penalty, GM-judged
  death after a prolonged stretch) are untouched. Checked Goblin Game's
  `## Food System` (its override of "a full day's nutrition") for a
  stale reference to the old location — it doesn't name one, so no
  follow-up needed there. Exploration's own scope is now just the leg
  structure and its four actions (Scout/Search/Stealth/Pushing the
  Pace), with no resource-tracking mixed in. Applied in commit `14930ef`.

- **Full-book broad review** (base game only — Goblin Game and Creating
  Items were explicitly excluded from scope: Creating Items' complexity is
  a known, deferred simplification project, not a bug hunt target, and
  Goblin Game is a supplement, not part of "the base game" this review
  covered). Read the whole of `rulebook.md` fresh and found two real,
  concrete issues plus a small grammar slip, all fixed in commit `6eb02a5`:
  - The `# Adventuring` intro sentence still claimed combat, exploration,
    and social intrigue "all share the same basic structure of taking
    turns and spending Action Points" — stale from before this session's
    AP-only-in-combat principle landed (Legs of a Journey has no turns/AP
    at all; Social Contests explicitly dropped its AP mention). Reworded
    to correctly scope turns/AP to combat and note the other two have
    their own pacing, without re-claiming a shared structure that no
    longer exists.
  - `#### Disrespect` (Results of a Social Contest) referenced "Persuasion,
    Diplomacy, or Intimidate flips" — Diplomacy and Intimidate aren't
    Skills in this game at all, a leftover from some earlier, more
    D&D-flavored draft that predates the finalized 25-Skill list. Fixed
    to the three actual social Skills: Persuasion, Presence, or Rapport.
    This section was explicitly left untouched during the Social
    Contests rework ("describe outcomes, which don't depend on how the
    party got there"), so it's an old bug the rework didn't introduce or
    catch, only this later full-read did.
  - `## Techniques`'s Prerequisites sentence was missing its subject
    ("To learn a Technique, must have..." → "...you must have...").
  - Verified clean (no changes needed): all 25 Skills' inline "governed
    by [Suit]" sentences cross-checked against The Suit Pool's table —
    fully consistent, no drift. Exploration and Social Contests read
    cleanly with no stray AP/old-mechanic references beyond the intro
    sentence above.
  - Noted but explicitly out of scope per user instruction: Goblin
    Game's Food System never states outright that it *replaces* the base
    game's Food-and-Exhaustion penalty for Goblins (only that it
    "overhauls" food requirements) — Goblin Traits' "Hungry" bullet
    implies replacement but nothing says so explicitly, unlike Gems'
    explicit "treat every mention of Gold as Gems" override. Left alone
    since Goblin Game is out of scope for this pass; worth revisiting
    whenever Goblin Game content is back in scope.

## Things considered and deliberately not done

- Reviving Embolden/Bolstered as literal mechanics — see above, superseded by simpler existing rules (case-by-case GM ruling; healing-clears-Wounded).
- Letting the *target* of a healing effect spend their own cards as a general pattern (only `Pressure Point Revitalization` does this, deliberately kept unique).

*(Session workflow notes, file-location facts, and standing verification
habits used to live in a "Notes to self" section here — moved to
`CLAUDE.md` instead, since this file is meant to stay a clean decision
record rather than mixing in process notes. See `CLAUDE.md`'s "Quick
reference" section and Git workflow.)*
