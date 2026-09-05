# Prose review queue

`rulebook.md`/`glossary.md` sections written or edited during an
AI-assisted session, so a later full read-through can find them without
combing the whole book looking for what changed. This is a checklist,
not a permanent record — **delete an entry once you've reviewed it**
(git history is the permanent record; `git log -p -- scripts/rulebook.md
scripts/glossary.md` or the commit hash(es) noted below gets you the
exact diff for any entry here). Backfilled once, covering every commit
on `claude/flagonquest-rules-overhaul` since it branched from `main`
(back through `2914efb`) — new entries append going forward per
`CLAUDE.md`'s note.

Ordered by where each section falls in the book (top to bottom), not by
when it was touched, so a front-to-back read-through can just check
things off in order.

## rulebook.md

- **`# Quick Start Guide`** (new section) — added, leading the book with
  a one-page overview before Character Creation. Commit `e2156ca`.
- **`## Spending Experience`** — moved next to Character Creation, fixed
  an XP-cost ambiguity, documented the 5-rank Stat/Skill cap, then
  simplified that cap note. Commits `d01e193`, `3cd85d9`, `45215d0`.
- **`### Learning Techniques`** — moved along with the Basics/Character
  Creation reorder. Commit `697cc2e`.
- **`## Building a Character`** — reordered next to Spending Experience.
  Commit `d01e193`.
- **`## Calculated Statistics`** / **`### Moving`** — movement reworked
  into a shared Athletics budget, reach clarified, a rounding rule
  added; the running-start rule later removed. Commits `6e038d4`,
  `2914efb`.
- **`# The Basics`** — promoted to lead section (after Quick Start/
  Character Creation) as part of the reorder. Commit `697cc2e`.
- **`### Successes`** — split out from the old combined Gambling/Extra
  Success section; suit-matching folded in as an Extra Success source.
  Commits `e668e91`, `e2156ca`.
- **`### Gambling`** — reframed as a bet declared before the flip, not a
  GM-gated option, as part of the same split. Commit `e2156ca`.
- **`### Supporting`** — reframed away from a skill-deficit fallback.
  Commit `038f203`.
- **`### The Suit Pool`** — added the Skill→Suit bullet list and a
  matching-suit example; Hearts' flat attack-damage bonus dropped in
  favor of suit-matching generally. Commits `e668e91`, `8fe1b09`.
- **Every `#### <Skill>` entry under Stats and Skills** (all 25 skills,
  `Acrobatics` through `Theurgy`) — each gained a trailing sentence
  naming its governing suit, for redundancy alongside the Suit Pool
  list. Commit `e668e91`.
- **`#### Persuasion`** — additionally touched by the Social Contests
  rework (its "governed by" framing adjusted alongside Presence/Rapport
  becoming the fixed Statement skills). Commit `78ec143`.
- **`## Techniques`** — gained "Techniques can override the baseline
  rules" line; Prerequisites sentence's missing subject fixed; reordered
  alongside Spending Experience. Commits `d01e193`, `ffe0aff`, `6eb02a5`.
- **`## A Full Night's Rest`** — clarified that "once per day" resets on
  the next full night's rest, not a literal 24-hour clock; later the
  three resting steps renamed to Cycles (Discard/Recovery/Draw) with a
  default ordering rule for Cycle-hooking effects. Commits `0e23cd2`,
  `93efdc2`.
- **`## Food and Exhaustion`** — moved to Health and Resources,
  generalized beyond Exploration (no longer travel-scoped). Commit
  `14930ef`.
- **`# Adventuring`** — intro sentence's stale "combat/exploration/
  social all share turns and AP" claim fixed to correctly scope turns/AP
  to combat only. Commit `6eb02a5`.
- **`### Making an Attack`** — fleshed out as a check like any other;
  Hearts' flat damage bonus removed in favor of general suit-matching.
  Commits `8fe1b09`, `a847d86`.
- **`## Traveling and Exploration`** / **`### Legs of a Journey`** /
  **`### Scout`** / **`### Search`** / **`### Pushing the Pace`** —
  reworked around one check per leg, generalized Pushing the Pace.
  Commits `a08b24e`, `14930ef`.
- **`## Social Challenges`** / **`### Social Contests`** /
  **`### Pressure`** — social contests replaced with an extended check
  plus the new Pressure mechanic (no more separate team-check subsystem,
  Concessions, or front/back positioning). Commit `78ec143`.
- **`#### Disrespect`** (Results of a Social Contest) — fixed a
  reference to "Persuasion, Diplomacy, or Intimidate" (the latter two
  aren't Skills in this game) to the three real social Skills. Commit
  `6eb02a5`.
- **`#### Materials`** / **`#### Time`** (Creating Items) — rewritten for
  the unified crafting formula, then Time simplified into two
  GM-adjustable baseline buckets. Commits `413f9b3`, `0799328`.
- **`## Examples`** (Creating Items) — rewritten alongside the
  Materials/Time changes; also touched during the Quick Start Guide add.
  Commits `e2156ca`, `413f9b3`.

## glossary.md

- **`#### Burst (X)`** (new entry, `# Keywords`) — added to name "this
  space, plus every space within X meters of it" for area effects, used
  going forward instead of ad hoc "adjacent to"/"within X meters of"
  phrasing. Commit `4ab9a21`.
- **`#### [Form]`** (Rules Tags) — renamed from `[Stance]`. Commit
  `4016fe0`.
- **`#### Bleeding [Fleeting]`** — Coat of Knit Flesh's interaction
  reworked into a once-per-day prevention; wording tightened to scope
  the prevention to natural decay specifically, not removal by any
  means. Commit `290a5d0`.
- **`#### Protected [Fleeting]`** — wording tightened for a mandatory
  "instead" substitution (no rules change), as part of the Ward rework
  below. Commit `106d064`.
- **`#### (Fire/Frost/Brilliant/Shadow) Ward [Fleeting]`** — reimagined
  as a flat +2 Resist bonus (up from +1) plus a self-limiting typed
  Protected-style absorption charge per stack, avoiding the immunity
  risk a further flat-bonus raise would have created. Commits `ed66572`,
  `106d064`.
- **`#### [Fleeting]`** (Rules Tags) — fixed a same-turn-grant snag: a
  Fleeting effect now skips its next decay when going from 0 stacks to
  some, instead of losing a stack the instant it's granted. Commit
  `5e103d2`.
- **`#### Pressure`** (Common Terms) — added alongside the Social
  Contests rework. Commit `78ec143`.
