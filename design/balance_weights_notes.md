# THE TABEL weights — an audit

Where each of THE TABEL's 19 per-mechanic values actually comes from, one
by one. Companion to `balance.md` (aggregate balance notes and completed
passes) and `flagonquest_balance_notes_model.md` (what the Baseline/THE
TABEL/BALANCE tabs compute) — this file is narrower and more skeptical:
for each weight, does the workbook actually show its derivation, or is it
just typed in? Started because the alchemy balance pass leaned on these
numbers without ever checking where they came from.

**Status key:**
- **Locked** — has a real derivation (a formula, or an explicit reasoned
  line in the workbook) that's been checked and holds up. Safe to keep
  using without revisiting.
- **Pencil** — reasoned out fresh this pass (not from the old workbook),
  agreed provisionally, but not battle-tested against real items yet.
  Comes with the actual math so it can be re-derived if the underlying
  assumptions change.
- **Plausible, not confirmed** — a reasonable reconstruction exists (the
  numbers line up with something real in Baseline), but the workbook
  never states the reasoning outright, so treat it as a good guess, not
  a fact.
- **Unexplained** — no formula, no reasoning line, nothing. A bare
  literal someone typed in.

## Locked

- **Fudge Value = 1.** The anchor itself, by definition — 1 value ≈ +1
  to a flip.
- **Acc/Def = 1.** Not independently derived, doesn't need to be: a flat
  Accuracy or Defense bonus *is* a +1-to-a-flip effect, which is
  literally what Fudge Value means. The most self-evident number in the
  whole table.
- **Health = 4.** `Baseline!C5`, an explicit formula: `Damage(2) ÷
  average hit chance(0.5) = 4` — "if damage is worth 2, and the average
  attack misses half the time, confirmed health loss is twice that."
- **Debuff = 1.** Traces to `Baseline!C17`, "Harried value" = 1.0,
  reasoned explicitly: "Harried reducing defense against 1 attack to
  follow, OR alternate defense being ~1 lower." Harried became the
  calibration point for the whole generic Debuff bucket every other
  stacking status effect (Crippled, Slowed, Vulnerable, Bleeding,
  Necrotic, ...) gets lumped into. Worth remembering this bucket is
  coarse — see the alchemy ledger's notes on Bleeding/Necrotic for where
  that coarseness actually mattered.
- **Gold = 1.5.** Reciprocal of `Baseline!C43`, "Value / Gold ratio" =
  2/3 → 1 ÷ (2/3) = 1.5 exactly. This is a real, checked match, but only
  pushes the question back one level: nothing in the workbook explains
  where 2/3 itself comes from either. Locked as "internally consistent,"
  not as "independently justified from first principles."

## Shallow/Deep HP and Heal — Locked, but easy to get backwards

The `Health` tab has real prose reasoning that never made it into
`flagonquest_balance_notes_model.md`, and the relationship *inverts*
between max-HP and healing — worth its own callout since it's a genuine
trap:

- **More max Deep HP = 4/point.** "1 Max Deep HP is worth 4, it's sort
  of an effective point of healing and it doesn't need to be healed to
  be effective at first, and you save a card."
- **More max Shallow HP = 5/point** — worth *more*, not less, than Deep,
  because it's easier to top back up at rest: "it's a bit easier to heal
  up with end of day healing so it has less of a restraint on your
  cards."
- **Healing Deep Health = 5/point, healing Shallow = 4/point** — the
  *opposite* ranking from the max-HP case, since Deep Health is the
  scarcer resource to actually restore: "Health is worth 4, but if it's
  Deep Health in addition to being a bit restricted we tack like an
  extra 1 value on that."

So: bigger Shallow pool > bigger Deep pool, but healing Deep > healing
Shallow. Both directions are reasoned, just easy to mix up if you're not
looking at the actual quote — flagged here so nobody has to re-derive it
under pressure mid-pass the way the alchemy ledger almost did.

## Pencil (reasoned fresh this pass, not from the old workbook)

- **Good Luck = 2.2.** Rulebook: Good Luck flips an extra card and keeps
  the higher. Exact expectation of 2-card-take-highest, drawing from a
  real 52-card deck (13 ranks × 4 suits, without replacement): **9.196**,
  against a 1-card baseline of 7 exactly — a marginal of **2.196**,
  rounded to 2.2. Checked against 55 actual "Good Luck" grants across
  `items.csv`/`techniques.csv`: only 4 (~7%) grant more than one stack at
  once, so pricing the *first-stack* marginal is the representative case,
  not some blend across the full (steeply diminishing — 2.2 → 1.1 → 0.66
  per successive stack) curve. A flat per-stack rate is already
  structurally generous toward the rare multi-stack grants (it prices
  them linearly, but the real curve is concave), so 2.2 already leans
  slightly generous on its own without needing a separate round-up.
  Lands within ~10% of the model's own Extra-Success anchor (2, fixed by
  Gambling's cost) — a decent independent cross-check.
- **Card (drawn/from hand) = 2.7.** Floor is Good Luck's own marginal
  (2.2): playing a hand card to replace an already-flipped result, on
  your own flip, immediately, is mechanically identical to Good Luck's
  "flip an extra, keep the better" — same expected-value math, just with
  full information instead of blind. Above that floor, a hand card
  carries real option value Good Luck doesn't: timing (save it for
  whichever future flip actually needs it), targeting (spend it on an
  ally instead), and a Suit Pool fallback if it never gets used as a
  replacement at all. That premium isn't a computed number — genuinely a
  judgment call — landed on 2.7 (a ~23% premium over the 2.2 floor) as a
  middle point between the bare floor and the old sheet's unexplained
  3.05.
- **Concession/Pressure = 2.2 (matches Good Luck).** Current rules:
  "party has Bad Luck on Statements equal to their current Pressure" —
  Pressure literally *is* imposed Bad Luck, not a separate mechanic. Bad
  Luck flips an extra card and keeps the *lower* one. Checked the
  combinatorics: `E[min of 2 draws]` = 4.804, and `7 − 4.804 = 2.196` —
  **exactly** the same magnitude as Good Luck's own marginal (2.196), not
  approximately — the uniform 1–13 distribution is symmetric around 7, so
  the harm from taking-the-worst-of-2 and the benefit from
  taking-the-best-of-2 are identical by construction. The old sheet's
  `=5/2` (2.5) was close but had no stated reasoning; this pass replaces
  it with the same number as Good Luck, on a real derivation rather than
  a coincidence of proximity.

## Plausible, not confirmed — the numbers line up with something real,
## but the workbook never says so

- **Autoswing = 5.5.** Exactly equals `Baseline!C16 + C17` (4.5 + 1.0),
  i.e. "value of character attack damage" + "Harried value" — the *full*
  average value of one typical attack, hit-chance discount and all.
  Reads as pricing Autoswing not as "remove the ~50% hit-chance discount"
  (which would only add back the discounted half, ~4.5) but as "this
  attack's entire payoff, as if from scratch, is now guaranteed" — closer
  to granting a whole extra guaranteed attack's worth of value than to a
  smaller "convert existing attack to always-hit" adjustment. Also see
  `balance.md`'s note on dropping Autoswing credit from current Grenades
  entirely, since current rules confirm they still roll to hit — this
  finding doesn't change that call, it just explains where 5.5 itself
  would have come from if it were ever needed again for something that
  genuinely does auto-hit.
- **Damage = 2.** Matches `Baseline!C4`'s stated assumption almost
  exactly: "Average weapons deal 2 over soak of equivalent type." Reads
  as a direct, if slightly informal, translation — "the typical weapon's
  damage-over-resist is about 2, so let's set the per-point Damage weight
  to 2" — which technically conflates a per-unit rate with one example's
  observed total, but the two numbers happen to coincide since typical
  weapon Damage values are small (single digits), so the conflation
  doesn't obviously break anything in practice.
- **1 AP = 3.** Two independent paths from Baseline both land on
  **2.75**, not 3: (a) per-attack value (5.5, see Autoswing above) ÷ 2 AP
  per attack = 2.75; (b) baseline turn value (8.25) ÷ AP actually spent
  attacking in a turn (1.5 attacks × 2 AP = 3 AP) = 2.75. 3 reads as a
  modest round-up from that ~2.75 figure — the same "nudge slightly
  generous over the derived number" pattern as Good Luck's old 2.5 over
  its real ~2.2, just smaller here (3 vs 2.75 is a ~9% bump, not the ~14%
  bump 2.5-over-2.2 would have been).
- **Protected = 3** (`=4×75%` in the sheet). Health's own value is 4, and
  Protected's current rule prevents exactly 1 Health loss per stack,
  fully guaranteed once it actually triggers — so a naive read would
  price it at the full 4, same as Health. The 75% discount most likely
  accounts for `[Fleeting]`: a stack of Protected clears at the end of
  your turn if unused, so a granted stack doesn't always get spent
  against an actual hit before it expires. That's a real mechanical
  reason a discount belongs here — but the *specific* 75%/25% split isn't
  computed or stated anywhere, just asserted.

## Unexplained — no formula, no reasoning, lowest priority to chase further

- **Sift = 0.64.** The hardest of the three to reconstruct, for a real
  reason: Sift's current rule (look at X cards, send *each one* to the
  bottom or discard, then shuffle) doesn't actually improve your very
  next draw's expected value at all — you're not choosing to keep a good
  card on top, you're removing all X viewed cards from the near-term
  draw order regardless, and whatever was card X+1 becomes your new next
  draw, which is just as random as before. Its real value has to come
  from second-order effects (routing bad cards to the bottom vs. the
  discard pile changes *when* they cycle back into play), which is
  genuinely harder to price with a flat per-unit rate than anything else
  in the table. 0.64 might be nothing more than "clearly worth less than
  a full card, pick a small number" — no evidence either way. Would need
  an actual deck-cycling simulation to pin down properly, not just
  algebra.
- **Push = 0.5.** Current rule just says "forcibly moved a certain
  distance" — no fixed magnitude, that's set per-effect. One guess: a
  Push is usually a one-time repositioning rather than a persistent
  per-turn hindrance the way a Debuff stack or a degree of Difficult
  Terrain is, so valuing it at half of those (which both sit at 1) could
  reflect that it doesn't keep paying out turn after turn. Unconfirmed.
- **Difficult Terrain = 1.** Same weight as generic Debuff, no stated
  reason why they should match. Plausibly just "another generic
  battlefield hindrance, treat it the same as Debuff by default" rather
  than an independent derivation.

## What's still open

Sift, Push, and Difficult Terrain are the three genuinely unresolved
weights left — everything else in THE TABEL now has either a real
derivation, a plausible reconstruction, or (for Good Luck/Card/
Pressure) a fresh one built this pass. None of the three above are
urgent: they show up rarely in the alchemy ledger (only Smokejar and
Immaculate Adhesive leaned on Difficult Terrain, both already flagged as
low-confidence translations) and none look likely to swing a Net verdict
on their own. Worth a real pass if a future balance run leans on them
more, but not blocking anything right now.
