# Backfoot-style turn-order shift, magnitude 2 — Level 1 fair-fight check

**What was tested**: two variants of a `turn_order_shift`-style ability given to
Hilde (front-line melee), at a shift magnitude of 2, in the standard Level 1
fair fight (Hilde/Browndog/Carrick/Sable vs. the 4-archetype Level 1 Roster).
Compared against a `+1 Accuracy` anchor (defined as 1.0 Value) and a plain
baseline, 4000 trials each. See `balance_weights_notes.md`'s Backfoot pass for
the full writeup and the earlier Level 3×3 numbers this follows up on.

- `backfoot_enemy_delay_shift2.html` — **enemy-delay** variant (Backfoot's
  actual mechanic): on a hit, pushes the *target* 2 places later in turn
  order. Seed 2, chosen because it actually shows the shift firing (many
  seeds don't, when the target's already near the back of the order and the
  push clamps to 0 movement — see `turn_shift` in the combat log).
- `backfoot_self_advance_shift2.html` — **self-advance** variant (not a real
  Technique yet, tested as a separate hypothesis): on a hit, moves *Hilde
  herself* 2 places earlier instead. Seed 1.

**Finding**: at Level 1's current calibration, the standard fair fight is
nowhere near fair — it's already ~99.9% party win rate, fully saturated, so
win-rate deltas can't show anything here. Rounds-to-win and HP-on-win (the
only metrics with headroom) showed a real, measurable movement for
self-advance (rounds down ~0.1-0.15, roughly the same ballpark as +1
Accuracy's own rounds effect) but only noise-level movement for enemy-delay.
Read: **self-advance seems to help more reliably than enemy-delay at this
Tier**, but the effect for either is small relative to how lopsided the fight
already is — this matchup just doesn't have many close calls left for
turn-order nuance to swing. The earlier Level 3×3 check (a genuinely
contested ~56% matchup) is still the more informative dataset for sizing
Backfoot's actual Value/point; this Level 1 pass is here mainly to confirm
*that* the saturation is real, not to replace it.
