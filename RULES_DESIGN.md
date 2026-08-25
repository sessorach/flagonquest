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

### Crafting simplification (in progress — decided, not yet written into `rulebook.md` or the CSVs)

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

**Explicitly not yet done, by user instruction ("let's just make notes
... then we can bulk update those later"):**
- `rulebook.md`'s `#### Materials` section still describes the old
  Base/Extra framing and needs a full rewrite once this is finalized.
- The "base item" paragraph drafted earlier in this file (fold
  Materials/Tools/Time into one pass, skip it if you already own a
  suitable item) needs revising to match the Main/Optional model instead
  of a "combine two lists" framing, per the point above.
- `crafting_recipes.csv` (all 17 rows, especially CR001–CR011's Slots
  shape) and every Masterwork/Weapon/Armor/etc. item in `items.csv` with
  its own Total/Base/Extra Materials override still need migrating to
  the new formula — a bulk data-layer pass, explicitly deferred, likely
  belongs in the sibling data-focused chat unless raised here again with
  explicit authorization (same boundary as the Stance→Form rename).
- Not yet touched at all: Tools (Tools/Workspace/Recipe) and Time — no
  indication either needs to change under this model, but not
  re-verified against it either.

**Concise baseline recipe format, drafted per explicit request ("draft up
what a concise version of these creation rules as a baseline might look
like") — still just a draft, not applied to `rulebook.md`:**

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

## Open questions / TODO

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

## Notes to self (compaction aid)

- **Verify, don't assert, on crafting math specifically** — user
  instruction, in response to the Materials-formula work: "don't make
  any mistakes... add a note to yourself to not make any mistakes in the
  future." When a worked example involves arithmetic (the Main-floor/
  Optional-cap split, or anything similar), actually compute it and
  check the result is internally consistent (Main ≥ half, Optional ≤
  half, they sum to Total) before presenting it as an example — don't
  write plausible-looking numbers and trust they work out. (The
  Cost ÷ Level-rounds-to-0 risk this note originally pointed at turned
  out to be based on a misunderstanding — Cost ÷ Level is a design-time
  authoring guideline, not something the live rule computes — so it's
  resolved, not just flagged. Leaving that correction in the Crafting
  section as the example of exactly the kind of thing this note exists
  to catch: I stated a mechanic with more confidence than I'd actually
  verified it, and it took the user's correction to catch it, not my own
  check.)
- Full 25-skill list with governing Stat lives in `index.html`'s
  `STAT_SKILLS` (~line 488), not in the rulebook prose itself as a single
  table — cross-check there, not from memory, if the skill list ever
  seems off.
- Skill descriptions (flavor + mechanical blurb) are `####` headers under
  each Stat's `###` section in `rulebook.md`, roughly lines 13–151.
- "The Suit Pool" section (`rulebook.md` ~line 255) and "Gambling and
  Extra Successes" (~line 219) are the two sections that will need the
  heaviest rewrite once the successes formula is finalized.
- Common Effects keyword definitions (Bleeding, Crippled, Frightened,
  Harried, Hasted, Necrotic, Protected, Slowed, Taunted, Vulnerable,
  Ward) are in `glossary.md` under "# Common Effects", ~line 121–176.
  `[Stance]` rules tag is ~line 113.
- `parse_markdown_sections` in `convert.py` (~line 596) treats every
  non-blank, non-heading line in `rulebook.md`/`glossary.md` as literal
  rendered body text — no HTML-comment stripping exists. Never leave
  draft/review markers inside those files; draft in chat first, commit
  clean.
- Workflow established this session: draft rules prose in chat, matching
  voice per `CLAUDE.md`'s Rulebook/Glossary prose guidance, get
  confirmation, then commit — one focused commit per section. No
  in-file review markers. Git diffs/commits are the review record.
- Data-layer changes (CSV edits, technique rebalancing, new keyword
  mechanics with real numbers) are explicitly out of scope for this
  branch/chat — handled in a sibling chat. This session sticks to
  `rulebook.md`, `glossary.md`, and `convert.py`'s mini-syntaxes if the
  overhaul touches those.
- Branch: `claude/flagonquest-rules-overhaul`, deliberately separate from
  the concurrent site/UI branch (`claude/flagonquest-webpage-579utb`) —
  the two merge once both are ready.
