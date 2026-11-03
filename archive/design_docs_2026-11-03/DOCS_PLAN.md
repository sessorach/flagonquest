# Design docs: reorganization plan (draft, 2026-11-03)

Per the designer: the design documents are the record of every decision
and of what the designer has said matters, and they need to be legible:
well organized and fairly concise. Nothing is to be lost. This is the
proposed plan; nothing below has been rewritten yet. Delete this file
once the work is done.

## The safety net first

1. **Snapshot.** Copy every design doc as it stands into
   `archive/design_docs_2026-11-03/`, untouched. The live docs can then be
   cut down to the decisions and their short reasons, with the full
   derivations a click away (and in git).
2. **File the orphans.** About a dozen decisions live only in
   `PROSE_REVIEW_QUEUE.md`, a checklist the designer prunes. Move each into
   `RULES_DESIGN.md` before anything else (Athletics movement budget, only
   weapon attacks can be Gambled, Masquerade disguise rule, only the first
   special meal a day counts, Main Types without "or", food harvest
   yields, Vigor, Repeat, Opportunity Attack and Negated, Range adjacency,
   Fleeting/Frightened/Taunted in social encounters, the Play rewrite).

## The documents, after

| File | What it is | Comes from |
|---|---|---|
| `design/README.md` (new) | One page: what each doc is for, which to read first | new |
| `DESIGNER_NOTES.md` (new) | The designer's own thinking, distilled: the manifestos and archive notes, plus principles stated in chat | archive manifestos, items docs, old site text |
| `RULES_DESIGN.md` | Rules decisions by game system, not by date | itself, plus orphans from the prose queue |
| `GM_GUIDE_NOTES.md` | GM advice: loot and Materials, social encounters, judgment calls | itself (its enemy-building draft moves to the enemy doc) |
| `balance.md` | Pricing principles, the current weights in prose, reference models, open questions | balance.md plus the live parts of balance_weights_notes |
| `balance_derivations.md` | Appendix: item and Technique derivations by slot and School, sim measurements by date, superseded versions | balance_weights_notes.md, reorganized |
| `ENEMY_ENCOUNTER_DESIGN.md` | Principles, standing decisions, the current model and tables, archetypes, abilities, building encounters, targets, open questions, short history | itself, plus the GM guide's enemy draft |
| `enemy_sim/TABLE_PLAY_NOTES.md` | How the table plays, the sim's play rules, calibration targets, a short findings log | itself (first third) |
| `enemy_sim/PC_BALANCE_NOTES.md` (new) | PC-build balance work: yardsticks, scorecards, Technique option sweeps | TABLE_PLAY_NOTES second half, sample_characters variants |
| `enemy_sim/README.md` | Usage and file map only | itself, history trimmed |
| `IDEAS_BACKLOG.md`, `PROSE_REVIEW_QUEUE.md` | Unchanged in purpose, contradictions fixed | themselves |

## Shape of a rewritten doc

- **Principles first,** each in a line or two, with who said it and when.
- **Current decisions next,** grouped by topic, each with its short reason
  and a pointer to where it was worked out.
- **Open questions** gathered in one place.
- **History last,** each superseded pass cut to a few lines: what it
  tried, what it found, what replaced it.
- Current names throughout ("formerly X" where it helps).

## Contradictions to settle while editing

- Fight length: about 3 rounds (10-08), 4-5 (11-02), 3.5-4.3 accepted
  with v3 (11-03). Record the latest, with the older targets as history.
- Spell Gambling: "only weapon attacks can be Gambled" (prose queue,
  balance.md) vs the older success rules in RULES_DESIGN.
- IDEAS lists potions the designer already cut, and "heals ignore
  Necrotic", which breaks "no counters to counters".
- Enemy doc: "Health is the one stat that breaks from player numbers"
  (09-30) vs the first principles (11-03); Fighting Styles described as
  live though they're off.

## Order of work

1. Snapshot, orphans, `design/README.md`, `DESIGNER_NOTES.md`.
2. `ENEMY_ENCOUNTER_DESIGN.md` (freshest, and the v3 direction).
3. `RULES_DESIGN.md` and `GM_GUIDE_NOTES.md`.
4. `balance.md` and `balance_derivations.md`.
5. The sim notes.

One commit per document, so each can be read and reverted on its own.
