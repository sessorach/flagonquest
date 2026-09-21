# Stagger / Outflank, magnitude 4 — L4×2 under movement (positioning on)

**What was tested**: the two committed Features (Backfoot's Stagger, Fleet Step's
Outflank — see `balance_weights_notes.md`'s Backfoot pass) at shift magnitude 4,
given to Hilde, against 2 Level 4 Melee Fighters — the clearest 2-enemy matchup
found for this mechanic, and run with `movement=True` per the now-default
convention (see this folder's own README section). Seed 2 for both, chosen
because it's one of the few where the shift actually fires (many seeds don't,
when the target's already at the position the push would clamp to — see
`turn_shift` in the log).

- `stagger_movement_l4x2_shift4.html` — enemy-delay: on a hit, pushes the
  *target* 4 places later in turn order.
- `outflank_movement_l4x2_shift4.html` — self-advance: on a hit, moves *Hilde*
  4 places earlier instead.

Both replays happen to be losses in this specific seed (this matchup's
aggregate win rate is only ~37-46% even with the bonus on, so that's a fair,
non-cherry-picked sample, not a curated win) — the point of saving these is to
see the `turn_shift` annotation actually firing in the log and to have a real
movement-mode fight to reference, not to showcase a highlight-reel win.

**Aggregate numbers for this exact matchup** (2000 trials, movement=True):
Stagger=4 → 44.75% win / 8.16 rounds / 65.25% HP-on-win vs. a 24.85% baseline;
Outflank=4 → 37.55% win / 8.56 rounds / 60.74% HP-on-win, same baseline. Matches
the finding already written up: Stagger clearly outperforms Outflank against a
scarce/tough enemy composition like this one.

**Superseded**: `backfoot_enemy_delay_shift2.html`/`backfoot_self_advance_shift2.html`
in this same folder are the original static-mode (no positioning) replays from
before `movement=True` became the default — kept for the record since they're
referenced in the balance notes' initial pass, but any *new* illustrative
replay should use movement mode like this one does.
