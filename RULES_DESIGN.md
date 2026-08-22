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

## Open questions / TODO

- Presence: Hearts (current) vs. Clubs — genuinely contested, see above.
- Diamonds still has no defensive keyword/mechanic identity.
- The "bad fail" trigger for accumulating multi-attempt checks (lockpicking-style) isn't defined.
- Scope of the generalized `Ritual Magic`-style card-contribution mechanic, and whether/how it becomes Stance-gated.
- Renaming "Stance" — leaning toward "Form" (over "Style", which is also live in the data as flavor text for several existing Stances, e.g. "Shugen Style"), not yet applied anywhere.
- Social Mechanics portfolio row and the social/exploration rules overhaul generally — explicitly deferred until the core successes/suit fundamentals are done.

## Things considered and deliberately not done

- Reviving Embolden/Bolstered as literal mechanics — see above, superseded by simpler existing rules (case-by-case GM ruling; healing-clears-Wounded).
- Letting the *target* of a healing effect spend their own cards as a general pattern (only `Pressure Point Revitalization` does this, deliberately kept unique).

## Notes to self (compaction aid)

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
