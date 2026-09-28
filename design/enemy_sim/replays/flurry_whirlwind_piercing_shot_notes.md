# Flurry / Whirlwind / Piercing Shot — Advanced Cost-6 trio check

**What was tested**: the three Advanced-tier Feature fields (`flurry`, `whirlwind`,
`piercing_shot` in `combat_sim.py`), each granting a full extra weapon attack -
unconditional and same-target for Flurry, gated on a second target actually
being reachable (melee cleave / line-of-fire) for the other two. See
`balance_weights_notes.md`'s Battle Maneuver pass for the hand-number
derivation and how these compare to the simulated result.

- `flurry_movement_l4x2.html` (winning replay, seed 1) - vs. 2 Level 4 Melee
  Fighters, this PC's best-tested matchup for showing off the mechanic.
- `whirlwind_movement_l4x2.html` (winning replay, seed 3) - same matchup,
  chosen because L4x2's two melee enemies naturally end up clustered near
  each other and the party, giving Whirlwind's melee-cleave condition its
  best odds among everything tested.
- `piercing_shot_movement_l1x4.html` (seed 3) - a different matchup than the
  other two: L4x2's geometry rarely lines two enemies up behind each other
  (~8% of fights), while the more spread-out Level 1 x4 starting layout
  actually gives Piercing Shot's line-of-fire condition much better odds
  (~52% of fights) - worth it here specifically to see the condition firing
  at all, even though Level 1's saturated win rate means the *aggregate*
  value read near zero in the actual balance check.

**Aggregate finding, summarized** (full numbers in `balance_weights_notes.md`):
Flurry is dramatically ahead of every other Feature on this sheet - 3.75x to
10x the value of +1 Accuracy depending on matchup, before even crediting the
fact that in real play it doubles whatever other Features were chosen too
(the sim can't model arbitrary stacked debuffs, so this is a floor, not a
ceiling). Whirlwind is real but composition-dependent, doing much better
against a tight melee cluster than a spread encounter. Piercing Shot's
line-of-fire condition is rare enough in most tested matchups that its
aggregate value reads as noise - close to worthless in practice despite
costing the same 6 points as the other two.
