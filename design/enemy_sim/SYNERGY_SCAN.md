# Synergy scan (2026-10-30)

Per the designer: look for combinations with an outsized synergy, on one
character or across the party, so they can be watched for in future
design. `synergy_scan.py` reads, for each pair, what the pair is worth
on top of the build less what each is worth alone, all on the same
days (day_sim.py's morning Health, enemy Health ×1.0, Level 3, 500 days
per first-fight mix):

    synergy = v(A and B) - v(A) - v(B)

Positive: worth more together. Negative: they get in each other's way,
or cover the same need. The pairs (599 in all, `synergy_scan.csv`):

- **On one character (521):** each host's best single additions from the
  Level 3 deep pass (TECHNIQUE_PASS.md, "By the day"), every pair of them.
- **Across the party (72):** each host's two best additions, against
  another party member's.
- **Suspected (6):** Sanguine with Reign of Blood, Feint with Disciple of
  the Flowing Hand and with Rending Claws, Toughened Resolve with
  Toughened Body and with itself, Lifeline with Bark Turns the Blade.

## What it found

**Nothing outsized.** Most pairs add up: 463 of 599 are within their
margin (median ±0.28 morning Health), and about 30 of the 599 would land
outside theirs by chance alone. Of the 136 outside, 104 are negative: two things competing for
the same cards, the same AP or the same missing Health. The biggest
positive synergy outside the suspected pairs is +1.4 Health, against
single Techniques worth up to +7.

Positive:

| Host | Pair | Alone | Together | Synergy |
|---|---|---|---|---|
| Ashleigh (L3) | Second Wind + Lifeline | +2.36, +1.39 | +5.11 | +1.36 ± 0.23 |
| Sable (L3) | Second Wind + Lifeline | +1.47, +0.74 | +3.28 | +1.07 ± 0.19 |
| Felix (L3) | Lifeline + Second Wind | +4.14, +0.62 | +5.51 | +0.76 ± 0.30 |
| Ashleigh (L3) | Firefly Leaves the Hand + One Eye Behind You | +0.74, +0.72 | +2.63 | +1.17 ± 0.43 |
| Hilde (L3) | One Eye Behind You + Solemn Pact | +1.72, +0.34 | +3.11 | +1.05 ± 0.62 |
| Hanforth (L3) | Brace + Blinkstep | +0.67, +0.05 | +1.65 | +0.94 ± 0.28 |
| Ashleigh (L3) | Lay On Hands + Toughened Resolve | +7.27, +4.12 | +12.22 | +0.83 ± 0.25 |

Negative:

| Host | Pair | Alone | Together | Synergy |
|---|---|---|---|---|
| Ashleigh (L3) | Lay On Hands + Bolstering Refrain | +7.27, +3.59 | +7.28 | -3.58 ± 0.33 |
| Ashleigh (L3) | Lay On Hands + Second Wind | +7.27, +2.36 | +7.92 | -1.72 ± 0.23 |
| Carrick (L3) | Toughened Resolve + Bark Turns the Blade | +5.19, +1.27 | +4.97 | -1.50 ± 0.56 |
| Carrick (L3) | Toughened Resolve, twice | +5.19 each | +9.07 | -1.32 ± 0.64 |
| Felix (L3) | Lantern Gutters in the Wind + Old Growth Digs Deep | +1.38, +1.31 | +1.36 | -1.33 ± 0.38 |
| Ashleigh (L3) | Lay On Hands + Lifeline | +7.27, +1.39 | +7.45 | -1.21 ± 0.35 |

- **Lifeline and self-healing.** The one repeated positive: a Lifeline
  holder who can heal itself (Second Wind) keeps the shared pool going.
  The same idea as Lifeline on a big pool (hall_of_fame/v1.2/HALL.md),
  one step further. Small, but on the watch list.
- **Healing saturates.** There's only so much missing Health after a
  fight: a second healing Technique on the same character adds little
  (Lay On Hands with Bolstering Refrain is worth Lay On Hands alone).
- **A second Toughened Resolve is worth less than the first** on Carrick
  (+5.19, then +3.88), and Toughened Resolve with Toughened Body just
  adds up on Hilde (+0.01). So stacking doesn't snowball by this score;
  the optimizer stacks it because each copy is a good buy on its own.
- **Encounter Techniques that want the same AP** cost each other a
  little: Felix's three Martial Disciplines (Lantern Gutters in the
  Wind, Old Growth Digs Deep, Circling Vulture) lose about 1.3 per pair.
- **Across the party, nothing.** None of the 72 cross-party pairs is
  outside its margin on the positive side; the average is -0.25.
- **The suspected pairs:** Reign of Blood rescues about half of what
  Sanguine costs Beornhard (+3.7 together), but the pair is still a loss
  (-3.5); Sanguine is down for its overhaul anyway. Feint with Disciple
  of the Flowing Hand (+1.1) brings Feint to about even, no more. Feint
  with Rending Claws: nothing.

The scan uses morning Health, which counts a bigger pool in full; in a
synergy that mostly cancels, since the pool is counted in the singles
too.
