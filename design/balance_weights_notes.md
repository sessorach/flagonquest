# THE TABEL weights — an audit

Where each of THE TABEL's 19 per-mechanic values actually comes from, one
by one. Companion to `balance.md` (aggregate balance notes and completed
passes), `archive/flagonquest_balance_notes_model.md` (what the Baseline/THE
TABEL/BALANCE tabs compute), and `balance_weights.csv` (a fast-lookup
index of the current value/status for every weight derived below, for
reference without scanning this file's prose) — this file is narrower and
more skeptical: for each weight, does the workbook actually show its
derivation, or is it just typed in? Started because the alchemy balance
pass leaned on these numbers without ever checking where they came from.

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

**Before combining two weights (or applying a situational multiplier
from `balance_weights.csv`'s Situational Multipliers section) to derive
a new number, check both source rows' `Discount Baked In` columns
first.** If either one already reflects a probability discount (hit
chance, realization, frequency), don't apply that same dimension again
on top of it. This is exactly the bug the Resist correction below was
born from: Resist's formula multiplied an already-landed-hit count
(hit chance already resolved) by Damage's own rate (hit chance *also*
baked in) — the same discount counted twice. `balance_weights.csv` now
carries a `Derived From` column precisely so a check like that is a
quick lookup, not a re-derivation from scratch.

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
- **Damage = 2.** Confirmed directly: it's Health(4) × average hit
  chance(0.5) exactly — the same formula that derives Health, just run
  in reverse. Also confirmed on intent, not just arithmetic: Damage
  prices a *contingent* point of harm (an attack that has to land, ~50%
  baseline), always **before** Resist — Resist is a separate, later
  reduction applied at the point damage resolves, not something baked
  into the granting item's own value. **A guaranteed point of harm that
  bypasses the attack roll entirely prices at the full Health rate (4),
  not Damage's discounted rate (2)** — same idea as pricing it as
  negative Shallow Health. Two different weights for "a point of harm,"
  depending on whether a roll stands between it and the target; picking
  the wrong one is the most likely way to mis-score a new item.
- **Autoswing = 5.5.** Confirmed directly: not a "hit-chance discount
  removed" mechanic at all (the earlier "guaranteed hit" reading was
  wrong) — it's the bundled credit for a Technique or item that *grants
  an attack as part of a larger effect* (Battle Maneuver's base "make a
  weapon attack," before any chosen Features add more on top, is the
  live example — this weight is not a leftover with nothing depending
  on it). Equals `Baseline!C16 + C17` exactly: the value of one typical
  attack (damage, discounted for the normal ~50% hit chance) plus the
  Harried stack any attack applies against a target who Parries or
  Dodges it — "basically just the value of an attack... plus a stack of
  Harried," in the designer's own words. Doesn't change the earlier call
  to drop this credit from current Grenades (they don't grant a *bundled
  extra* attack, the Grenade *is* the attack, already priced through
  Damage directly).
- **1 AP = 2.75** (down from the old sheet's unexplained 3). Confirmed
  on the underlying logic, not just the arithmetic: "AP is a restriction
  on everything you can do in combat... very few things grant AP
  directly, as is intended; so this value is used to basically just say,
  how valuable does this need to be considering I could just attack" —
  in the designer's own words. That's a direct statement of the
  opportunity-cost framing: 1 AP's value is what you gave up by *not*
  spending it toward another attack. Attacks come in whole 2-AP chunks
  (you can't attack a fraction of a time — a turn free of movement needs
  can go all-in on 2 attacks, which is exactly why ranged characters who
  don't need to close distance can be so consistent), so the rate is
  `(value of one attack, 5.5) ÷ (its AP cost, 2) = 2.75` — the most
  direct reading of "what does 1 AP cost me if I spend it elsewhere
  instead of attacking." The whole alchemy ledger (every Potion/
  Grenade/Poison, all costed at `AP:-2`) has been recomputed under this
  — a uniform +0.5 Value/Net shift across 32 rows, since only the AP
  term changed.
- **Protected = 3** (`= 4 × 75%`), promoted from "asserted" to confirmed.
  First had to resolve a real mechanical ambiguity: the rule text
  ("prevent 1 Health loss for each stack... then remove that many
  stacks") could be read as burning *all* current stacks on the first
  Health-loss event regardless of size, or as banking the unused
  remainder. Confirmed by the designer: it's the latter — a Health-loss
  event only consumes `min(stacks, incoming loss)`, leaving the rest for
  a future hit, and it applies to *any* Health loss (Bleeding ticks
  included, not just attacks). That makes Protected behave like a real
  banked shield, not a use-it-or-lose-it burst. Simulated the actual
  mechanic across a full 5-round encounter (Baseline's own enemy taper/
  attack-rate, ~2.25 avg damage/hit, 0.5 hit chance) at three targeting
  assumptions — how much of the party's total incoming hit volume lands
  on the Protected-holder specifically:
  - Generic/untargeted (1/4 share, same as any other party member):
    49-61% of granted stacks' value realized, depending on stack count.
  - Moderately focused (1/2 share — roughly double an average party
    member's hits, matching a tank/Taunt-adjacent build): 74-84%.
  - Fully taunted (100% share): 93-97%.

  Real grants run 1-4 stacks per use (Brace = 3, Fortifying Concoction =
  4, Strength from the Slain = 3, Skin of Stone scales with Meditation),
  and per the designer's own recollection — "I was estimating a
  character using Protected would take more hits than average, in the
  same vein of assuming some synergy or strategy" — the intended
  baseline was the moderately-focused case, which lands at 74-84% across
  that realistic stack range: an almost exact match to the workbook's
  original 75%. The number holds up under an actual simulation of the
  real (bank-partial) mechanic, not just an asserted split.

## Shallow/Deep HP and Heal — Locked, but easy to get backwards

The `Health` tab has real prose reasoning that never made it into
`archive/flagonquest_balance_notes_model.md`, and the relationship *inverts*
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

  ### Correction: Good Luck = 2.4, crediting the Suit Pool

  The 2.196 above only prices the numeric "keep the higher card" benefit
  and misses a second real effect: per the Suit Pool rule ("any cards
  flipped for Good or Bad Luck... combine to determine the total suit
  pool"), **both** cards drawn for a Good Luck flip count toward the
  suit pool, not just the kept higher one. With 2 cards drawn without
  replacement from a 52-card deck, `P(at least one matches a given
  suit) = 1 − (39/52)(38/51) ≈ 44.1%`, versus 25% (13/52) for a single
  card — a **+19.1 percentage point** jump in the odds of an Extra
  Success from a suit match. Since Extra Success is the model's own
  Locked anchor (2 value, fixed by Gambling), that's worth
  `0.191 × 2 ≈ 0.38` additional expected value per flip, *if* the flip
  is one where Extra Successes actually matter.

  They don't always: Extra Successes only do something on flips that
  "call for more than a bare pass" — attacks (bonus damage) and
  extended-effort checks — not a plain pass/fail check, where a suit
  match is wasted. There's no way to derive the real split precisely,
  so this applies a **50% discount** to the raw 0.38 credit (the same
  kind of judgment call as Card's premium below, or Harried's "on
  average one extra attack benefits" reasoning) — `0.38 × 0.5 = 0.19`.

  **Good Luck = 2.196 + 0.19 = 2.39, rounded to 2.4.**

  This barely moves the 51 existing single-instance Good Luck grants
  (Technique-level, usually exactly one flip), but matters more for
  long-duration grants covering many flips over their active window
  (e.g. Liquid Charisma) — those get re-priced as `(relevant flip
  count) × 2.4`, not a flat per-grant bump.

  Two follow-ups this surfaces but doesn't resolve:
  - **Pressure/Bad Luck (2.2, mirrored off Good Luck)** should, by the
    same logic, move the *other* way: both cards from a Bad Luck flip
    also feed the *target's own* suit pool, so the same probability
    bump partially offsets the imposed penalty rather than adding to
    it. Not re-priced here — flagged for a dedicated pass.
  - **Card (2.7)** is floored on Good Luck's old marginal, and a hand
    card played for a flip also joins that flip's suit pool the same
    way, so its floor likely deserves the same bump (~2.9). Not applied
    here since nothing downstream needed it yet.
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
- **Turn-order adjustment = 1.0/place shifted.** New this pass — several
  existing Techniques already shift a creature's position in turn order
  (`Backfoot`, `Alacrity`, `One Eye Behind You`, `Heroic Inspiration`),
  but none were ever priced against THE TABEL. The mechanic doesn't
  create a beneficial window on its own; it lets you choose *who* gets
  to act inside one that's already open (a debuff just landed, an enemy
  about to go down, denying an enemy a reaction before the board
  reshapes) — the same fundamental shape Harried's own value already
  covers, where the payoff depends on whichever attack happens to land
  inside the window, not a guaranteed numeric swing. Priced as a
  judgment call at roughly half of Good Luck's revised marginal (2.4),
  reasoning it as "sometimes decisive, often marginal" — Good Luck
  improves the flip it's attached to every single time, a turn-order
  shift only pays off when an exploitable window actually exists.
  Deliberately left **linear and uncapped** for now — a real cap almost
  certainly exists once a shift is large enough to guarantee "first in
  the round" for a typical party+encounter size, but per the designer,
  worth seeing how the flat rate reads across a few more real items/
  Techniques before deriving one from first principles rather than
  guessing. Guaranteed: Yes (nothing gates the shift itself on a flip).
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
- **Sift = 0.60/card** (down from a naive first pass at 1.62 — see
  below for why the two differ). Sift's rule ("look at X cards, send
  each to the bottom of your deck or the discard, then shuffle") looked
  like it shouldn't do anything at first — you're not choosing to keep a
  good card on top, every viewed card gets moved. The key detail: "then
  shuffle your deck" means a card sent to the bottom doesn't stay there,
  it gets reshuffled randomly back in. So the real choice per card is
  binary — discard it (removed until the discard pile eventually
  reshuffles back in) or let it rejoin the deck at random — which is
  exactly the "stack the deck" mechanism: discard the low cards
  (confirmed by simulation that "discard ≤ 7" is within noise of
  optimal, matching the stated player heuristic exactly), keep the high
  ones circulating. Simulating that (500k trials, discarding ≤7 and
  reshuffling the rest) gives a **true long-run value of ~1.62/card** —
  the total bonus delivered across every future draw until the
  post-Sift deck is fully exhausted, which holds constant (1.61–1.62)
  regardless of how deep into the deck you already are, and only decays
  gently under repeated back-to-back use (1.62 → 1.42/card by the 5th
  consecutive application, thanks to each rank having 4 copies in a real
  deck — much gentler than Good Luck's stacking curve).

  But 1.62 is a *lifetime-of-the-deck* number, and THE TABEL's default
  scoping is per-encounter (or per-day for daily-cadence effects, see
  `balance.md`'s corrected Target convention) — not "eventually, however
  many days that takes." Rescoping to what actually lands within one
  adventuring day (~18 draws — 1.5 attacks/turn × 5 rounds × ~1.55
  combats/day from Baseline, plus Reflex/defensive/misc flips) gives
  **~0.60/card**, verified by simulation rather than estimated. That's
  the number to actually use in the ledger for anything gated to a
  daily cadence; a Sift effect with a different natural window (e.g.
  gated to a specific in-combat condition) would need this same
  simulation re-run for whatever window applies to it instead — this
  isn't a universal constant the way Damage or Health are.
- **Hand Filtering (draw + discard) = 1.66/card.** New this pass,
  surfaced while designing Worry Token's (Neck) Spades effect: "draw 1
  card, then discard the worse of it and your current worst hand card."
  Not the same mechanism as Sift (there's no reason to ever choose
  "bottom" over "discard" once a card is already sitting in your hand
  and known to be bad — Sift's bottom-vs-discard choice only matters for
  an unseen top-of-deck card you're trying to bias for the future), so
  this gets its own rate rather than reusing Sift's.

  The real question is what a "hand card" is actually worth holding for
  future use, and per the designer, that isn't a flat average across
  1-13: below rank 9, a card only really serves as generic
  Technique-discard fuel, and any card works equally well for that — so
  gaining "another" sub-9 card has no marginal value at all, since you
  already have plenty of interchangeable fuel. Only rank 9+ is a card a
  player would actually hold and look for a chance to sub into a flip.
  That's `5/13` of draws (ranks 9-13, 4 copies each, 20 of 52 cards).

  Below that threshold, drawing and discarding is a pure wash — you'd
  just discard the useless draw and keep your hand exactly as it was,
  no cost either way. At/above it, you get a card worth holding — but
  its value isn't simply "the rank-9-13 average (11) minus the 7
  baseline" (a naive +4), since you don't just blindly sub it into your
  *next* flip regardless — you keep whichever is higher, the held card
  or your natural flip, same "keep the max" logic as Good Luck/Card. So
  the real marginal value is `E[max(held card, natural flip)] − 7`,
  computed exactly against a real 52-card deck (the held card removed
  from the pool) for each possible held rank:

  | Held card | E[max(held, natural flip)] |
  |---|---|
  | 9 | 9.78 |
  | 10 | 10.47 |
  | 11 | 11.24 |
  | 12 | 12.08 |
  | 13 | 13.00 |

  Averaging across the 5 equally-likely held ranks (conditional on
  clearing the ≥9 bar) gives **11.31**, so the marginal value of holding
  a known rank-9-13 card is `11.31 − 7 = 4.31` — a touch above the naive
  +4, since a held 9 or 10 still occasionally rides along "for free" on
  a better natural flip rather than ever actively costing you anything.

  **Full rate: `Value = (5/13) × 4.31 ≈ 1.66/card`.** This is a general,
  reusable benchmark for any "draw + discard" hand-filtering mechanic,
  not just Worry Token — record it in `balance_ledger.csv`'s `Grants`
  column as `HandFiltering:N` (N = cards drawn-and-filtered), same
  convention as `Card:N`/`GoodLuck:N`. Re-derive the threshold/marginal
  if a mechanic ever changes the "won't sub in below rank X" cutoff or
  the card range itself.
- **Speed = 0.55/point** (Agility 3, i.e. Speed 4, agreed as the
  representative baseline for most movement). Not a mechanic THE TABEL
  currently has a row for at all, despite real items granting flat Speed
  (Feathered Sandals, Slipstream Sandals, and others) — added here since
  Push and Difficult Terrain both turn out to be priced off of it.
  Derivation: 1 Move action costs 1 AP and covers up to Speed meters, so
  the value of +1 Speed is the AP saved covering the same ground —
  `(1 AP's value) ÷ (Speed + 1) = 2.75 ÷ 5 = 0.55`. (Corrected from an
  earlier pass's 0.6 — that used 1 AP's *old*, pre-correction value of 3;
  nobody re-ran this formula after 1 AP itself got Locked at 2.75. Caught
  during the buff/debuff review below, since Hasted/Slowed both mirror
  this rate.)
- **Push = 0.55/meter.** Directly Speed's own per-point rate — a Push is
  forced movement, priced the same as any other meter of movement.
- **Difficult Terrain — non-linear, hard-capped at 2 degrees (Agility
  3/Speed 4 baseline), not 0.55/degree.** The original derivation
  treated each degree as flatly adding 1 extra meter of Speed cost,
  priced at Speed's own per-point rate — but that misses the rule's
  actual floor: "a character can still move at least 1 space [crossing
  Difficult Terrain]... no matter how many degrees of Difficult Terrain
  there are" (`glossary.md`). A move action covers `floor(Speed /
  (1 + degrees))` meters, minimum 1 — at the Speed-4 baseline that
  bottoms out at exactly 1 meter/move action once degrees reach 2, and
  stays there for any higher degree, the same hard-cap shape every
  stacking Debuff-bucket keyword below ended up with. Re-derived as the
  AP-equivalent cost of covering the same ground a free move action
  would have: `value(degrees) = (Speed ÷ throughput(degrees) − 1) ×
  1 AP's value (2.75)`.

  | Degrees | Meters/move action | Value |
  |---|---|---|
  | 0 | 4 | 0 |
  | 1 | 2 | 2.75 |
  | 2 | 1 | 8.25 |
  | 3+ | 1 | 8.25 (capped) |

  **Guaranteed: Yes** — unlike Damage or Push, nothing gates this on an
  attack roll; a placed hazard just sits there, so no hit-chance
  discount applies. Whether a given creature actually crosses it during
  the encounter is a separate, item-specific question — same shape as
  Necrotic's own "does the trigger condition come up" uncertainty —
  handled through each granting item's own Rate of Use, not folded into
  the weight itself. Difficult Terrain is still usually granted as a
  *zone* effect that can catch more than one creature, so the per-degree
  Value above gets multiplied by however many creatures the item's own
  estimate assumes get caught — same AoE-estimation uncertainty flagged
  for Hellfire Bomb/Thunderclap, now compounded with a curve that can
  swing by 3x between one degree and the next, so that creature-count
  estimate matters more here than it did under the old linear rate.
- **Resist — a different value per damage type, not one shared rate.**
  THE TABEL never had a Resist row at all, despite 7 current Masterwork
  items granting it. This is explicitly out of scope for base weapon/armor
  Resist — those are "designed to fit the assumptions" directly and don't
  get run through this model — it's only for *bonus* Resist a Masterwork
  item or consumable grants on top of that.

  Resist prevents 1 point of damage on *every* future hit of that type
  for as long as it's active (not a one-shot like Protected), so its
  value is `4 (the guaranteed-harm rate, matching Health's own — see the
  correction note below) × how many hits of that type actually land`.
  "How many hits of that type land" needed two inputs with no existing
  derivation: **how often each damage type shows up**, and **total hits
  landed per player per encounter** — worked out from Baseline's own
  existing combat math (10 enemy-rounds/fight × 1.5 attacks/round, split
  across a 4-player party, at 50% hit chance ≈ **1.875 hits/player/
  encounter, any type**) rather than a new guess.

  The first input went through a real correction. The initial pass used
  the designer's *enemy headcount* rule of thumb directly as a stand-in
  for damage share: 3 in 4 enemies Physical-only, 1 in 4 elemental, Fire
  twice as common as Frost/Brilliant/Shadow individually (Fire 10% of
  all enemies, each other element 5%). On review, that overstates
  Physical and understates the elements — an elemental-relevant fight
  isn't split evenly by headcount, because the elemental-damage enemy
  tends to be the fight's actual main damage dealer (a mage lobbing
  fireballs), while the physical enemies alongside it skew tank/
  disruptor and contribute comparatively little. Corrected model, per
  the designer: an encounter is elemental-relevant about half the time
  (unchanged), Fire is twice as likely as each other element *within*
  that half (unchanged), but *within* a relevant encounter, that element
  now accounts for **two-thirds of the fight's total damage**, not just
  its headcount share. Averaged across all encounters (elemental and
  not), that resolves to exact clean fractions: **Physical 2/3 of all
  damage, Fire 2/15, Frost/Brilliant/Shadow 1/15 each** (down from
  Physical's old 3/4, up from Fire's old 1/10 and the others' old 1/20).

  Combining those with the same formula (using the corrected guaranteed-
  harm rate of 4, not the hit-gated Damage rate of 2 — see the double-
  discount correction below): **Physical Resist = 5.0/point**, **Fire
  Resist = 1.0/point**, **Frost/Brilliant/Shadow Resist = 0.5/point
  each**. Physical is worth **5×** Fire and **10×** a non-Fire element —
  still clearly the better overall pick (per the designer: "that doesn't
  mean physical resist isn't still better" — it's relevant in *every*
  fight, not just the ones featuring that specific element).

  **Correction: Resist was double-discounting the hit-chance, exactly
  the bug the Damage-weight clarification below exists to prevent.**
  The formula above originally used `Damage's own weight (2, mirroring
  granting vs. preventing a contingent point of harm)` as the
  per-hit-landed multiplier — but "hits landed" (the 1.875 figure) is
  *already* a landed-hit count, with the 50% hit-chance discount baked
  in at derivation time (see below). Damage's own weight of 2 is
  *also* a hit-chance-discounted rate. Multiplying an already-landed-hit
  count by an already-discounted per-point rate discounts the same miss
  chance twice. Caught by the designer directly: once an attack has
  landed, a point of Resist prevents a *guaranteed* point of Health
  loss, priced at the guaranteed rate (4) — not Damage's contingent rate
  (2), which is for uncertain-whether-it-hits situations "hits landed"
  has already resolved. Every Resist rate above doubles cleanly as a
  result (the share and hit-count terms are untouched, only the
  multiplier changes) — previously Physical 2.5, Fire 0.5,
  Frost/Brilliant/Shadow 0.25 each.

  This ripples through every already-priced Resist-granting item in the
  Torso Masterwork pass — see `balance_ledger.csv` and `balance.md`'s
  Torso pass section for the corrected Nets (Elemental-Resistant Armor,
  Robes of Resilience, Robes of the Elemental Lord) — and through Ward,
  whose flat-Resist component inherits this rate directly (Elemental-
  Attuned Tincture, Spellblade's Sipper, Elemental Warding Band), all
  recomputed in the same pass. The open question about *why* Resist
  read as underpowered even before this fix still stands, separately: it
  might mean these items are genuinely under-leveled for what they
  deliver, or it might mean a pure expected-hits model is missing
  something real about Resist's value (burst/spike protection in a
  single big hit, not just average damage over time) — worth revisiting
  now that the more mundane double-discount explanation is resolved.

  This same correction feeds directly into **Ward** (Fire/Frost/
  Brilliant/Shadow Ward) — see its own writeup below in the Debuff
  bucket section for the full derivation, including a rule change (the
  flat bonus doubled from +1 to +2 Resist) made alongside this fix. The
  burst/spike-protection blind spot flagged just above applies to Ward
  too, since it inherits Resist's rate directly — still genuinely open,
  unlike Ward's other two questions (magnitude scaling, per-application
  value) which are now resolved.

  **Clarification, caught during the Potion buff-cluster pass (and the
  origin of the Resist fix above):** the `2` in "Damage's own weight (2,
  mirroring granting vs. preventing a contingent point of harm)" is
  already the price of a *hit-gated* point of damage — it has the ~50%
  on-hit discount baked directly into the rate itself, not applied
  separately at the aggregate "how many hits land" step. A
  **guaranteed, unconditional** point of harm (no attack roll gating it
  at all) prices at double that — **4**, matching Health's own full rate
  (same reasoning Bleeding's guaranteed per-tick Health loss uses to
  justify pricing at 4, not 2). Don't discount the `2` rate a second
  time for "this only matters on a hit" — that's already priced in.
  (First got this wrong pricing Warmage's Draft's elemental-conversion
  effect — walked it back once caught there, but didn't retroactively
  check Resist's own formula for the same mistake until the designer
  flagged it directly while reviewing a new Torso item.)

## Pricing a fresh attack from scratch (Grenades, Battle Magic, and similar) — Resist placeholder + universal Harried + Autoswing as cost

Distinct from the Locked "Damage is priced before Resist" rule above —
that rule governs *modifying* an existing attack (Extra Success and
similar), where a real weapon's own baseline already implicitly clears
Resist. A standalone attack built from scratch (a Grenade, or a spell
like Battle Magic) has no such implicit weapon baseline, so it needs a
different anchor:

- **Resist placeholder**: assume the target's relevant Resist equals the
  granting character's own investment in the matching stat — **Body 3**
  (the same representative baseline used everywhere else this session)
  for a fixed/non-scaling item, or the caster's actual stat for
  something that scales with it. Physical damage assumes the full
  baseline (**4** = Body 3 + 1 armor); elemental damage skips the armor
  term (**3** = Body 3 alone) — the same "+1 elemental credit, assuming
  ~1 Physical Resist from armor that elemental typically bypasses"
  convention as before, just expressed as a smaller subtraction rather
  than a bonus addition. `margin = raw Damage − Resist placeholder`,
  priced at Damage's own rate (2/point) — **not** discounted again for
  hit chance, since Damage's own weight already has that baked in.
- **Universal Harried credit**: any attack against Dodge/Parry applies
  Harried once, "regardless of the attack's result" (`rulebook.md`) — so
  a fresh attack gets **+1**, flat and guaranteed (not hit-gated), same
  as Autoswing already bundles into its own definition for a *granted*
  attack.
- **Autoswing (5.5) subtracted as the flat opportunity cost** of not
  just attacking normally instead — this replaces a flat AP charge for
  anything that's genuinely a stand-in attack (not doubled for AoE,
  since you only gave up *one* attack regardless of how many targets the
  substitute effect hits).
- **AoE doubles the margin** (not the raw Damage before subtracting the
  Resist placeholder), and doubles the universal Harried credit too
  (each assumed target rolls their own Defense) — but does **not**
  double Autoswing, which stays a flat, single opportunity cost.

Confirmed against the full Grenade batch (see `balance_ledger.csv`, IDs
I028-I036 and I207) — every item in that category was recomputed under
this model this pass. Any bespoke debuff a fresh attack grants on top of
Damage still uses its own per-keyword curve from the Debuff bucket
below, discounted ×0.5 if it's delivered via that same attack roll
(guaranteed value once landed, same convention as everywhere else) —
separate from Damage's own already-baked-in discount, and never applied
to Autoswing.

### Harried = 1/stack, linear, hard-capped at 6 — no multi-turn accrual, decays all-at-once

"For each stack of this, you suffer a -1 penalty to Dodge and Parry
Defense. At the end of your turn, remove all stacks of Harried you
have" (`glossary.md`) — structurally closer to Vulnerable than to
Crippled/Bleeding (both push the *attacker's* hit chance toward 100% by
knocking down a Defense; Vulnerable hits Vital/Mental/Instinct, Harried
hits Dodge/Parry), so it shares Vulnerable's exact saturation point: a
flat -N zeroes the gap to 100% against the baseline ~53.8% hit chance
at **6 stacks**.

But the decay itself is genuinely different from every other keyword in
this bucket — a flat magnitude that lasts until the *afflicted
creature's own next turn ends*, then wipes entirely, not a 1-per-turn
taper. More stacks buy **zero extra duration**, only a deeper Defense
penalty during one fixed window — so there's no multi-turn window to
sum over, and none of Crippled/Vulnerable's peak-then-decline per-stack
shape (that shape is an artifact of their multi-turn accrual, which
doesn't apply here).

That window realistically covers about **1 follow-up attack on
average**, per the designer — "any time someone applies Harried that
one extra attack gets to benefit from it... sometimes it's 2, sometimes
they're the last person to attack" — which matches the original
Debuff=1 single-stack calibration exactly (Baseline's own "reducing
defense against 1 attack to follow"). With no multi-turn accrual to
bend the curve, this stays **linear** straight to the cap:

| Stacks | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
|---|---|---|---|---|---|---|---|
| Value | 1 | 2 | 3 | 4 | 5 | 6 | 6 (capped) |

Checked against the two current Grenades granting *bonus* Harried on
top of the universal on-attack credit: Thunderclap-in-a-Jar's 4
post-AoE stacks and Quartz Tincture's 2 stacks are both well under the
6-stack cap, so this curve doesn't actually change either item's
existing numbers — it's numerically identical to the flat rate they
were already using in that range. What it does resolve: confirms
there's a real ceiling (value 6, or 3 once halved for the standard
on-hit contingency) on how much *any* item can extract from Harried
alone. That's well short of what a whole item's budget needs even at
Level 1-2, so a genuinely "Harried-forward" item (Quartz Tincture's
planned redesign) still needs a real Damage or other component to carry
most of its budget, with Harried as a secondary, flavorful lever rather
than the primary one — not a flaw in the curve, just a hard limit on
what a defense-penalty-only mechanic can be worth on its own.

## Pricing a menu of stacking-debuff Features — assume reasonable concentration, not a uniform spread

A distinct question from any single keyword's own curve above: several
Techniques (Battle Maneuver `T072`, War Magic `T120`, Social Maneuver
`T057`, and any future one shaped the same way) hand the player a pool
of Feature points to freely divide across a menu of options, several of
which stack the *same* keyword the harder you invest in them (Battle
Maneuver's Hamstring grants Slowed X + suit, where X is however many
points went in). Pricing that menu by checking "what's 1 point worth in
isolation" understates it — per the designer, a player looking at this
menu doesn't spread evenly across every option, they see an attack that
can Slow someone and put a *real* number of points there, because
that's the obvious, intuitive move, not a min-maxed one. **Price the
menu assuming that — a player concentrating a reasonable few points
into one synergistic option — not a uniform 1-point-per-feature spread,
and not a maximally-optimized dump into whichever single option has the
highest ceiling either.**

Concretely, using the ×0.5 hit-discount from the fresh-attack model
above plus each keyword's own `value(n)` curve (n = points spent + an
assumed 0.25 expected suit bonus), realized Value per point spent looks
like this at a few different concentration levels:

| Feature (keyword) | 1 pt | 2 pt | 3 pt | 4 pt | 6 pt |
|---|---|---|---|---|---|
| Wing Clip (Crippled) | 1.12 | 1.41 | 1.75 | 2.06 | 2.38 |
| Hamstring (Slowed) | 0.82 | 1.03 | 1.28 | 1.48 | 1.39 |
| Battering (Bleeding) | 2.50 | 2.12 | 1.71 | 1.39 | 0.98 |
| Distracting (Taunted) | 1.38 | 1.24 | 1.19 | 1.17 | 1.10 |
| Harrying (Harried) | 0.62 | 0.56 | 0.54 | 0.53 | 0.50 |

**These shapes aren't interchangeable, and "concentrate" doesn't mean
the same thing for each one** — this is the real payoff of checking
each keyword's own curve instead of applying one flat multiplier:
- **Crippled/Slowed/Taunted compound** (continuously-active,
  multi-turn-window keywords) — per-point value *rises* with
  concentration, up to each one's own saturation point (Slowed peaks
  around 4 points, right where its own hard cap sits; Crippled keeps
  climbing all the way past 7). A player who wants to invest in one of
  these is *rewarded* for going a few points deep rather than spreading
  thin.
- **Bleeding tapers the opposite way** — its own stacking cap (~12
  total, geometric taper past 2 stacks) means concentration actively
  *hurts* per-point efficiency. The intuitive move here is the
  shallow one (1-2 points), not a deep dump.
- **Harried stays flat and low regardless of concentration** — it has
  no compounding shape to reward investment in the first place (a
  previously-known limit, see its own section above), so no amount of
  "reasonable concentration" rescues Harrying's own per-point rate.

**Working target: ~1.0 realized Value per Feature point**, landing
roughly in the middle of what a player reasonably investing 2-4 points
into one compounding option (Crippled, Slowed, Taunted) actually
realizes — not the isolated 1-point number, and not the fully-optimized
ceiling either. Use this table (or the same method applied to whichever
keyword is actually in question) as the working check for any Feature's
own point cost, rather than assuming every Cost-1 Feature is
interchangeable — Harrying's flat ~0.5-0.6 across the board and
Battering's inverted taper are both real, keyword-driven deviations
from the target, not review misses to force back to 1.0 by re-costing
alone.

## Cover — priced as the cost of avoiding it, not the raw penalty

Heavy Cover "gives Bad Luck twice on attacks against Dodge or Parry, as
well as flips to see you" (`rulebook.md`). Bad Luck's single-instance
value is already Locked at 2.2 (worst-of-2-draws card math); Heavy
Cover's "twice" is the marginal value of a *second* application on top —
worst-of-3-draws instead of worst-of-2, same real 52-card-deck math:
`E[min of 3] = 3.706`, against the same 7 baseline, giving **3.29/
instance** (up from 2.2, but not dramatically — most of Bad Luck's own
bite is already in the first application).

That per-instance number is a **ceiling, not the actual price**. Heavy
Cover from a persistent zone effect (a smoke cloud, not a one-shot
attack) applies to *every* attack and *every* perception flip against
the covered target for as long as the zone lasts — eating that
repeatedly, every turn, for a whole encounter is obviously worse than
just repositioning once to get a clean shot/view. A rational target
always takes the cheaper option, so the value the party actually
extracts is **the cost of that one relocation**, not the underlying
penalty's own math — same "compulsion with an escape hatch, priced at
whichever is cheaper" logic as Taunted/Frightened above, just with
movement as the escape hatch instead of a different attack target.

There's no formal in-system rule for "cost to route around an obstacle
of size X," so the relocation cost is a judgment call per use case (same
footing as Card's premium-over-Good-Luck's-floor) — priced in AP-
equivalent terms (1 AP = 2.75) based on how disruptive the specific
zone's size/duration realistically is. Confirmed against Smokejar (a
wide, ~3-meter-radius cloud that lingers for the whole scene): the
designer's own estimate is **at least one enemy loses 2 move actions**
repositioning to stay in effective range, so **5.5** (2 × 2.75) is the
number used there — comfortably under the 3.29-per-instance ceiling
(and its per-turn repeated cost, which is far higher still), consistent
with "so strong it basically never actually applies." A smaller or
shorter-lived Cover zone would need a smaller relocation estimate, the
same way Sift's value changes with its actual usage window.

## AoE multiplier — 2x enemies-hit assumption, ×0.8 realization discount, net 1.6x

The designer balances area-effect Grenades (Hellfire Bomb,
Thunderclap-in-a-Jar) assuming **2 enemies hit** — deliberately bad
value against a single target, above-rate against 3+ — a real,
confirmed calibration point, not re-litigated here. But taking that at
full, undiscounted face value ignores a genuine tactical cost pure
single-target damage doesn't have: an area effect is unconditional (it
can't be aimed to skip an ally standing in the blast) and inherently
harder to land a clean 2-enemy cluster with than simply pointing a
weapon at one chosen target. That's a real downside with no cost
attached anywhere in the model, the same kind of gap a realization
discount already fixed for Protected (the ideal scenario doesn't always
materialize in play).

**Applied as a ×0.8 realization discount on top of the 2x
assumption — net 1.6x** — to the AoE-doubled portion of Value only
(Damage margin, any debuff curves, the universal Harried credit).
Autoswing stays a flat, undiscounted subtraction regardless, same
reasoning as always: it's the opportunity cost of not just attacking
instead, unrelated to how the throw itself plays out.

```
Value = (DamageComponent + DebuffComponent + Harried_universal) × 1.6
        − Autoswing (undiscounted)
```

Checked against both AoE Grenades that existed at the time — both were
flagged overpowered under the old undiscounted 2x, and both landed
cleanly within their Level threshold at 1.6x, independently (not fit to
match, a genuine confirmation the number is in the right neighborhood):
Hellfire Bomb Net +0.1, Thunderclap-in-a-Jar Net +0.175 (at the time —
see the correction below for why Thunderclap's own number has moved
since).

### Correction: curves need `curve(N) × 2`, not `curve(2N)`, for AoE debuffs

The "AoE-doubled portion" language above was ambiguous about *how* to
double a non-linear debuff curve, and the first two AoE items to use
one (Thunderclap's Bleeding and bonus Harried) picked the wrong reading:
doubling the *stack count* fed into one curve evaluation
(`curve(2N)`), rather than evaluating the curve once per target and
doubling *that* (`curve(N) × 2`). These are only equivalent for a
linear mechanic (Damage's margin, the flat universal Harried credit) —
for anything with a shaped curve, they diverge, because the curve
represents the value delivered to **one** target, and AoE means that
same experience happens to two **independent** targets, not one target
receiving a doubled dose.

Which direction this moves a given item's Value depends on the shape
of that specific curve near the stack count in question:
- **Crippled/Slowed** (rising marginal value approaching their caps —
  higher starting stacks buy more turns at the capped per-turn
  contribution before decaying below it) were being **over-credited**
  by the old method: concentrating a doubled stack count on one
  hypothetical target extracts more value from a still-climbing curve
  than genuinely splitting the same total across two independent
  targets.
- **Bleeding** (the opposite shape — a geometric taper past 2 stacks,
  diminishing not rising) was being **under-credited**: spreading a
  small stack count across two independent targets, each getting the
  full un-tapered value, beats concentrating it on one target where
  the back half of the stacks fall into the taper.
- **Harried** (linear straight to its cap) is unaffected as long as
  neither the base grant nor its doubled reading crosses the cap —
  true for every current item using it.

Fixed at the point of use rather than retroactively auditing every
prior AoE computation in isolation — see Thunderclap-in-a-Jar's own
recomputation in `balance_ledger.csv` for the corrected numbers, and
apply `curve(N) × 2` (not `curve(2N)`) to any future AoE item using a
shaped debuff curve.

## What's still open

Every weight that started this audit unresolved (Sift, Push, Difficult
Terrain, Resist) now has a Pencil derivation, and Damage, Autoswing, and
1 AP are fully Locked. What's left, if anyone wants to push further:
- Sift's ~0.60/card figure is calibrated to a once-per-day window
  specifically — a Technique that grants Sift on a different trigger
  (e.g. a combat-conditional one, which is how the design intentionally
  keeps Sift from being freely spammable — an unconditional, on-demand
  Sift really would be strong, given how gently its value decays under
  repeated use) would need the same simulation re-run for its own actual
  window, not a reused constant.
- Difficult Terrain's own per-degree rate is now resolved too (see the
  non-linear, hard-capped derivation above, replacing the old flat
  0.55/degree) — it still uses the same "2 enemies" AoE/zone-effect
  scope assumption as Grenade AoE for how many creatures a given item's
  zone catches, and that creature-count estimate now matters more than
  it used to, since the per-degree curve itself can swing 3x between
  1 and 2 degrees.
- The Resist finding — every existing elemental-Resist item reading
  underpowered — is a real pattern to act on during the Masterwork pass,
  not a loose end in the weight itself. The weight's own derivation is
  solid (built entirely from already-Locked/confirmed pieces: Damage's
  weight, Baseline's own combat-frequency math, and the designer's
  directly-stated enemy-type mix); what's undecided is what to *do*
  about the items it exposes as under-tuned.

Protected's 75% discount (the last core THE TABEL weight with no
confirmed reasoning behind it) is now resolved too — see the Locked
section above. Every core weight has either a real derivation, a
confirmed designer intent, or a fresh Pencil one built and reasoned
through this pass. What's left is the buff/debuff bucket's own
per-keyword curves, below.

## The Debuff bucket, broken out — per-keyword curves (Pencil)

THE TABEL's generic `Debuff = 1` bucket lumps every stacking status
effect (Bleeding, Crippled, Frightened, Harried, Hasted, Necrotic,
Slowed, Taunted, Vulnerable — the "Common Effects" glossary keywords)
into one flat per-stack rate. Going through them individually instead —
these are **not flat rates**, most of them are genuinely non-linear in
stack count, for real mechanical reasons specific to each one, not a
shared curve applied uniformly.

**General principle, stated by the designer:** a build that specifically
opts into and stacks one of these is expected to have other abilities
synergizing with it — the numbers below assume *moderate* synergy (the
mechanic gets built around a little), not the theoretical maximum-power
combo. This is why the compounding curves below aren't flattened down to
match a flat, incidental-use rate.

**Two survival assumptions do most of the work here**, both grounded in
the same design fact: the party's baseline strategy is to focus-fire
down one enemy at a time, which cuts directly against any effect that
needs its *target* to keep existing for its value to land.
- **Bleeding/Necrotic-shaped effects** (resolve via a discrete event when
  a stack decays, one stack per turn) get a **hard-ish cap**: real play
  experience says only ~1-2 stacks of Bleeding actually get a chance to
  resolve per enemy before it dies. Modeled as a geometric taper — full
  value for the first 2 stacks, each stack beyond that worth half the
  previous one — rather than a hard cutoff, so it degrades gracefully
  instead of creating a cliff.
- **Crippled/Vulnerable-shaped effects** (a continuously-active modifier
  that applies in full to everything relevant while any stacks remain,
  decaying 1/turn) get a **2-turn realistic-survival window** instead —
  shorter than their full theoretical decay-to-zero, same focus-fire
  logic, but these compound differently under stacking (see below) since
  concentrating stacks makes *every* remaining turn in that window hit
  harder, not just adding one more discrete future tick.

### Bleeding = 4/stack, capped (geometric taper beyond 2)

Removed 1 stack per turn (the standard Fleeting decay), each removal
causing 1 guaranteed Health loss — no roll involved once applied, so it
prices at Health's full rate (4), the same "guaranteed harm bypasses the
attack roll" rule that governs Damage vs. Health elsewhere in this
audit. `value(n) = 4 × min(n, 2) + 4 × Σ 0.5^k` for stacks beyond 2 —
asymptotically caps at **12 total**, no matter how large n gets:

| Stacks | 1 | 2 | 3 | 4 | 6 | 10 | 20 (max-Level Bloody Poison, ingested) |
|---|---|---|---|---|---|---|---|
| Value | 4 | 8 | 10 | 11 | 11.75 | ≈12 | ≈12 |

A 20-stack application (the extreme case — Bloody Poison's ingested
variant at max Potency) reads as worth about 3 realistic stacks, not 20
— by design, so an ability can't just pile on Bleeding for unbounded
scaling. This is the standout finding from the whole breakout: Bleeding
has been scored at the generic Debuff rate (1) everywhere in the current
data (16 mentions across items/techniques) — a 4× miss even before the
stacking cap is applied.

**Correction: the taper is an enemy-targeting assumption, not a
universal one.** The cap exists because Bleeding is normally something
the party inflicts on an *enemy* — a target whose continued presence in
the fight is genuinely uncertain (it might die to other damage, or the
encounter might just end, before every stack finishes decaying), so
stacking past ~2 buys a shrinking chance of ever actually cashing out.
That uncertainty doesn't apply the same way to a **player character**
carrying Bleeding — the wearer is the one still standing at the table
for the whole encounter (and the rest of the day), so every stack they
pick up really does eventually tick down and cost Health, without the
"might not live to see it" discount. Pricing an effect that removes or
prevents Bleeding **from a player** (Coat of Knit Flesh, or anything
like it in the future) should use the full linear rate — 4/stack,
uncapped — not this tapered `value(n)` curve, which stays reserved for
pricing Bleeding as something the party deals out.

### Crippled = 1.5/stack base, 4-turn window, hard-capped at 42

"-1 to your own attacks" per stack — reduces the *afflicted creature's
own* future attack rolls, all current stacks apply to every attack made
while any remain (not one discrete event per stack, unlike Bleeding).
At Baseline's 1.5 attacks/turn, a single stack is worth 1.5 (not 1 —
the earlier "same as Harried" guess undercounted this).

Revised twice more this session. First, the survival window widened
from 2 turns to **4**, matching a second real tactical pattern besides
simple focus-fire death: a creature Crippled hard enough stops being a
threat and gets *left alive on purpose* while the party deals with
bigger problems first, so the debuff keeps paying off for longer than
"it dies in 2 turns" assumes — the same "establish it turn 1, it runs
the remaining 4 of a 5-round Baseline encounter" logic used everywhere
else in this pass now.

Second, and more importantly: the curve needed an actual **ceiling**,
not just a wide window. A flat -N penalty against the flip mechanic
(baseline ~53.8% hit chance, uniform 1-13 flip) hits **0% at exactly 7
stacks** — the attack mathematically cannot land past that, so a stack
count beyond 7 is pure waste on whichever turn already has 7+ up.
Capping each turn's contribution at 7 (not the *starting* stack count,
the *current* one that turn, since decay still runs 1/turn) gives a
real hard ceiling instead of the old formula's smooth-but-unbounded
convergence:

| Stacks | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12+ |
|---|---|---|---|---|---|---|---|---|---|---|
| Value | 1.5 | 4.5 | 9 | 15 | 21 | 27 | 33 | 37.5 | 42 | 42 |
| Per-stack | 1.5 | 2.25 | 3 | 3.75 | 4.2 | 4.5 | 4.71 | 4.69 | 4.2 | falling |

Per-stack value actually *peaks* right at the saturation point (n=7,
~4.71/stack) and *declines* past it, since extra stacks just get wasted
on turns where the cap's already hit — a genuinely different shape from
every other keyword in this bucket, and a clean, mechanically-grounded
one: the formula's own ceiling lines up exactly with the point the game
mechanics themselves stop caring about more stacks, not an arbitrary
survival-window guess.

### Vulnerable = 1/stack base, 4-turn window, hard-capped at 24

"-1 to Vital/Mental/Instinct Defense" per stack — same shape as
Crippled (continuously-active, 1/turn Fleeting decay), calibrated to a
different base rate: these three Defenses see real use but are
individually rarer than Dodge/Parry, which is explicitly *why*
Vulnerable hits all three at once, to land on par with Harried's
single-Defense relevance. Same two revisions as Crippled, mirrored on
the *defender's* side of the same flip mechanic: 4-turn window, and a
hard cap at exactly **6 stacks** — that's where a baseline ~53.8%
attacker's hit chance against this target reaches 100%, so nothing past
6 makes an attack any more likely to land:

| Stacks | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10+ |
|---|---|---|---|---|---|---|---|---|
| Value | 1 | 3 | 6 | 10 | 14 | 18 | 23 | 24 |
| Per-stack | 1 | 1.5 | 2 | 2.5 | 2.8 | 3 | 2.875 | falling |

Same peak-then-decline shape as Crippled, just at a lower absolute
ceiling (24 vs. 42) since Vulnerable's base rate (1) is Harried's own
narrower incoming-threat rate rather than the target's full attack
output.

### Necrotic = 3/stack when it actually resolves, but priced through Rate of Use, not a stacking curve

Necrotic doesn't fit the same non-linear-stacking treatment as the other
three, because its two real uses in play aren't gated by focus-fire
survival or decay compounding — they're gated by whether the target ever
does the one specific thing Necrotic punishes at all. Per the designer:

- **Player-applied, vs. an enemy that heals or shields itself.** "Either
  tank characters or heal/support ones will apply Protected to people
  likely to be focused by attacks, and the point is that Necrotic
  cancels those out before the attack deals damage." That cancellation
  ("at any time if you have stacks of both Necrotic and Protected,
  remove 1 stack of each") is unconditional — no attack roll, no hit
  chance, it just fires the instant both are present. So *when it
  resolves*, 1 stack of Necrotic is worth exactly what the Protected
  stack it deletes was worth: **3** (Protected's own Locked value).
  Same logic against a straight self-heal: it blocks 1 point of
  whatever Heal weight applies (4 Shallow / 5 Deep), landing in the same
  ballpark. Call it **3/stack**, Protected's rate, as the representative
  number for this role.
- **Enemy-applied, vs. a player's own healing.** Here the designer's
  framing is different: "players will know they have Necrotic, so it's
  more of a hedge against them healing until it goes away." A player who
  sees the stacks won't feed a heal into them and eat the block — they
  wait the (generic 1/turn Fleeting) decay out. So the mechanical
  "block 1 Health of a heal" clause rarely actually fires; what actually
  happens is closer to a **stacks-count-many turns of denied access to
  healing** (can't clear Wounded penalties, can't top back up) — a
  tempo-denial effect, not a Health-point-denial one. Nothing else in
  THE TABEL prices "delay X for N turns" directly, so this role doesn't
  reduce to a clean per-stack number the way the other three did.

The honest way to handle this: price Necrotic at **3/stack for when it
resolves** (Guaranteed: Yes — no attack-roll gate, unlike Damage/Push),
same as Bleeding, but don't try to build a stacking curve for it — its
contingency isn't "does the target survive/keep attacking," it's "does
the target's specific trigger condition ever come up at all," which
varies per use case (every-few-fights for the anti-Protected/anti-heal
role, per the designer's own estimate) rather than following a
mechanical decay shape. That belongs in each Necrotic-granting item's
own **Rate of Use** column in `balance_ledger.csv` — same place Sift's
and Food's own realistic-cadence discount already lives — not in a
second universal weight. If a Necrotic item's computed Net reads low
under a conservative "every few fights" rate, the designer's own
preferred fix is bumping how often enemy Protected-users/healers show
up in encounter design, not inflating the per-stack weight.

### Taunted / Frightened = 2.2/stack, linear — not a taper or a compound

Structurally different from all four keywords above: both gate on
"**while you have any stacks**" — the compulsion (Bad Luck on some set
of actions) doesn't get stronger with more stacks, it's a flat on/off
switch. Extra stacks buy nothing but *duration* against the generic
1/turn Fleeting decay both use unconditionally (no "if unused" carve-out
the way Protected has). So unlike Bleeding/Necrotic's taper or
Crippled/Vulnerable's compounding, this one is genuinely **linear**:
`value(n) = n × (per-turn value)`.

Pricing the per-turn value: both effects are a compulsion with a
built-in escape hatch — comply with the redirect, or eat Bad Luck on
the disallowed action. Bad Luck's own card math is already Locked at
**2.2**, exactly mirroring Good Luck/Pressure (worst-of-2 is symmetric
to best-of-2). That sets a hard **ceiling**, not just a floor: a
rational target never accepts an outcome that costs more than 2.2 in
expected value, since eating the Bad Luck penalty is always sitting
right there as the cheaper alternative once things get worse than that.
So whichever an enemy actually picks, the value the party extracts per
turn can't exceed ~2.2 — the mechanic's own escape hatch caps itself.

Both land at the same **2.2/stack, linear** number, but the two clauses
differ in how *tight* that ceiling actually is in practice — a real
usage distinction worth keeping straight even though the value is
identical:
- **Taunted** restricts *any non-friendly action that doesn't target
  the taunter* — there's no free escape route, so complying (attack the
  taunter) or defying (eat Bad Luck on literally anything else hostile)
  are the only two options. The 2.2 ceiling is usually actually
  realized. This is genuine whole-field control: every attacker who
  complies gets funneled onto one target, protecting the rest of the
  party at once — matching the designer's read of Taunted as a
  foundational tanking tool. Realizing the full value still needs the
  taunter to actually be a viable target to attack (no worse than
  eating Bad Luck) — a squishy character self-Taunting to bait a
  killing blow wouldn't realize this the same way a real tank build
  would.
- **Frightened** only restricts *actions targeting the frightener
  specifically* — attacking anyone else costs the enemy nothing at all.
  So its 2.2 ceiling is loose and often *not* realized outside a
  1-enemy-remaining fight or a genuinely no-good-alternate-target
  situation; most of the time a Frightened creature just walks away and
  attacks someone else for free. It's a narrower tool — protects one
  specific relationship (usually yourself, or whoever cast it), not the
  field — even though the underlying per-turn math is identical to
  Taunted's.

Same realistic-window caveat as Bleeding/Crippled applies to the
*linear* stacking itself, just aimed at a different failure mode:
stacks beyond however many rounds the fight (or the taunter, if it's
the Taunted creature's own survival that matters) realistically has
left are wasted, since there's no more time left for the "any stacks"
trigger to matter. Baseline's own 5-round encounter length is the
natural ceiling to check a big grant against, same as it was for the
survival-window keywords above.

### Hasted = 0.55/stack base, rising toward ~2.2/stack; Slowed = 1.1/stack base, hard-capped at 17.6

A late catch during review: both were originally waved off as "flat
continuously-active modifiers, no decay event to make them non-linear" —
that reasoning was wrong. They *are* continuously-active with the same
generic 1/turn Fleeting decay Crippled/Vulnerable use, applying full
current magnitude to Speed every turn they're up. That's exactly the
shape that made Crippled/Vulnerable compound, not the shape that keeps
Harried/Ward flat (Harried clears *all* stacks at end of turn instead of
decaying 1-at-a-time; Ward's "+1 Resist while any stacks" is boolean the
same way Taunted/Frightened are, not magnitude-scaling). Same formula as
Crippled/Vulnerable — `value(n) = rate × Σ(stacks remaining each turn of
the survival window)` — with the base rate corrected alongside Speed's
own fix above (0.55/point, not the stale 0.6).

The two get *different* windows, though, because what caps them is
different:
- **Slowed** (debuff, applied to an enemy) got the same second revision
  Crippled/Vulnerable did: a 4-turn window (not 2 — a heavily-Slowed
  creature that can't reposition or flee is also a "left alive on
  purpose" case, same logic as Crippled), and a hard cap, since Speed
  saturates too — zero is zero, a creature that already can't move
  doesn't get more immobile. Capped at **4 stacks**, matching the
  session's own baseline Speed (Agility 3 → Speed 4).

  A third revision doubled the base rate itself. Speed's own 0.55/point
  is priced against *one* movement need per turn — but a Slowed
  creature realistically needs to cover ground twice in a typical turn
  (reposition, then act, or simply that a single Move action's worth of
  distance rarely covers everything a turn wants), and both movement
  needs get hit by the exact same flat -1 penalty. That's a direct
  doubling at the rate level, not a change to the window or the cap —
  those are about how long the effect stays relevant and where Speed
  physically bottoms out, neither of which depends on how many times
  per turn the penalty actually bites: **1.1/stack**, not 0.55/stack.

  | Stacks | 1 | 2 | 3 | 4 | 5 | 6 | 8+ |
  |---|---|---|---|---|---|---|---|
  | Value | 1.1 | 3.3 | 6.6 | 11 | 14.3 | 16.5 | 17.6 |
  | Per-stack | 1.1 | 1.65 | 2.2 | 2.75 | 2.86 | 2.75 | falling |

  Hard ceiling at 17.6 (double the pre-revision 8.8), now in the same
  ballpark as Vulnerable's own ceiling (24) rather than sitting well
  below it — matching the read that Slowed had been underrated relative
  to the other three. Peak per-stack still lands right at the cap
  (n=4, 2.75/stack). A target with higher Agility needs proportionally
  more stacks to zero out (the cap is target-Speed-dependent, same
  "representative baseline" caveat as everywhere else Agility 3 gets
  used), and the same caveat as before still applies on top: realization
  also depends on whether movement is actually contested in a given
  fight — an enemy that just stands and swings never feels it, unlike
  an Accuracy/Defense penalty that bites on every attack roll regardless
  of scenario.
- **Hasted** (buff, applied to your own side) doesn't have a "target
  might die" cap — the party doesn't get whittled down like enemies do
  in the Baseline model, so the real limit is just how much of the fight
  is left when it's cast. Per the designer: "sometimes longer,
  realistically you're using it early on into a fight and getting a good
  3-4 turns out of it if you apply enough" — a 4-turn window:

  | Stacks | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
  |---|---|---|---|---|---|---|---|---|
  | Value | 0.55 | 1.65 | 3.3 | 5.5 | 7.7 | 9.9 | 14.3 | 18.7 |
  | Per-stack | 0.55 | 0.83 | 1.1 | 1.375 | 1.54 | 1.65 | 1.79 | 1.87 |

  Converges toward 2.2/stack (4 × 0.55), unbounded — unlike Slowed,
  Hasted has no saturation point to cap against (Speed climbing has no
  probabilistic ceiling the way hit chance does), so it keeps this
  smooth per-stack convergence rather than the hard wall Slowed's own
  revision added.

### Speed (permanently-worn) = 2.54375/point — the single-instance rate was never re-scoped for gear

Same class of gap as the Hasted/Slowed correction above, caught while
pricing the Feet slot. Speed's 0.55/point rate (`balance_weights.csv`)
was derived from a single move action's AP savings — it prices *one
use*, the same basis Push and Difficult Terrain correctly use, since
those really are one-shot effects. But several Feet items grant a
*permanent, continuously-active* Speed bonus (Lightfoot Shoes and
others), live for the whole encounter the same way Resist or
Hasted/Slowed are — and unlike those two, Speed's rate never got the
"sum across every turn it's up" treatment.

**Deriving how many move actions that permanent bonus actually pays out
over an encounter**, from the game's own AP economy rather than a
guess: a player turn is 4 AP (`rulebook.md:436`), an attack costs 2 AP
(`rulebook.md:438`), and Baseline's own established average is 1.5
attacks/turn (already used for the Resist and card-draw derivations
above). Since attacks come in whole numbers, that average isn't a
smooth "1.5 attacks, 1 AP left over every turn" — it's a blend of two
turn shapes:

- **Half of turns**: a well-positioned or ranged character spends the
  full 4 AP on 2 attacks — 0 AP left for movement.
- **The other half**: 1 attack (2 AP) leaves 2 AP, split — per the
  designer — roughly **85/15** between moving twice (both leftover AP
  spent on a second move action) and moving once (the last AP wasted,
  or spent on a 1-AP utility technique/Interrupt instead of a second
  move).

Average moves/turn = 0.5 × 0 (double-attack turns) + 0.5 × (0.85×2 +
0.15×1) = 0.925. Over Baseline's 5-round encounter: **4.625
moves/encounter**.

`Value = 0.55 (single-instance rate) × 4.625 = 2.54375/point` — this is
Speed's rate for anything **permanently worn or continuously active**
(gear, a passive technique bonus). Push and Difficult Terrain stay on
the original 0.55/point single-instance rate, since they're genuinely
one-shot — this correction only applies to an effect that's live for
the whole fight, the same distinction Hasted/Slowed drew from
Taunted/Frightened above.

Worked check against Lightfoot Shoes (flat `+Level` Speed, Feet slot,
`Target = Level × 3`):

| Level | Value (Level × 2.54375) | Target | Net |
|---|---|---|---|
| 1 | 2.54 | 3 | −0.46 |
| 2 | 5.09 | 6 | −0.91 |
| 3 | 7.63 | 9 | −1.37 |
| 4 | 10.18 | 12 | −1.82 |
| 5 | 12.72 | 15 | −2.28 |

Lands at a flat ~85% of Target every Level — a modest, consistent
shortfall rather than the catastrophic one the uncorrected
single-instance rate implied (was −2.45 to −12.25 across the same
Levels). Worth the same kind of "accept below Target" allowance the
Torso Resist items got, on its own grounds this time — see the Torso
Masterwork pass note above on why that precedent doesn't transfer
wholesale (Resist's allowance came from a felt-value cross-check
finding a gap the raw economy missed; Speed's 0.55 base rate already
*is* the felt-value number, so there's no equivalent hidden gap here —
this is a real, if modest, shortfall being knowingly accepted, not a
pricing-model blind spot like Resist's was).

### Range breakpoints — how far a Speed 4 (Agility 3) attacker can close and still act

A companion tool to the Speed correction above, for tuning weapon/ability
ranges deliberately rather than by feel: given a distance `D` and a
would-be closer's Speed, the moves needed to *cross* it isn't `D /
Speed` — closing a gap only means covering ground down to melee range
(1m, "close range" per `glossary.md`), not all the way to 0. Corrected:

`moves_needed(D, Speed) = ceil((D − 1) / Speed)`

(An earlier pass here divided the raw distance by Speed directly,
missing the −1; caught by cross-checking the grenade/thrown-weapon
range below, which the uncorrected formula misclassified — see the
worked check further down.)

Since a standard turn is 4 AP and a standard attack costs 2 AP,
**closing the gap and still attacking the same turn requires
`moves_needed ≤ 2`** — the same 2-move ceiling the Speed correction
above derived directly from Baseline's own attack economy (half of
turns spend the full 4 AP on 2 attacks; the rest split 2 AP between
movement and either a second move or something else). Solving that
ceiling for `D` gives the single most useful number here:

**The "still attacks" ceiling is `D ≤ 2×Speed + 1`; the "costs you the
attack" floor is `D ≥ 2×Speed + 2`.** At the session's baseline Speed
4, that's **9m vs. 10m exactly** — the line where a target goes from
"reachable and punishable this turn" to "reachable only by giving up
the attack." This is the breakpoint worth designing weapon/ability
ranges around most deliberately, more than the outer full-turn edge
below: it's the first point where range actually buys the wielder
something (a free turn without melee retaliation), not just a
theoretical "eventually out of reach."

The rest of the tiers, at baseline Speed 4:

| Breakpoint | AP story | Distance | Meaning |
|---|---|---|---|
| **Melee/Reach** | Weapon-defined, not movement-derived | 1m ("close range," per `glossary.md`) | Already in range; not a movement question |
| **Short** | 1 move (1 AP) | up to 5m | Closable for the cheapest possible action |
| **Medium** | 2 moves + attack (4 AP, full turn) | up to 9m | Closable **and still punishable** in melee this turn |
| *(the 10m line)* | 3 moves (3 AP), 0 AP left for an attack | 10m–13m | Costs the wielder's attack to close — "most of a turn," per the designer |
| **Long** | 4 moves, 0 AP left (full turn) | 14m–17m | Closable in one turn, but the whole turn — no attack, no AP to spare |
| **Extreme** | \>4 moves | \>17m | Can't be closed in a single turn at all |

These aren't snap points every range value has to land on exactly —
they're landmarks to test a proposed range against: does crossing it
cost an attacker their attack that turn, their whole turn, or is it
simply out of reach for a turn entirely?

**Cross-checked against the weapons already in `items.csv`** (Body's
own baseline is 3, per the Fresh-attack Resist placeholder note above,
so `3 × Body` = 9m):

| Weapon | Range | Moves needed (Speed 4) | Tier |
|---|---|---|---|
| Melee (any) | Close (1m) | 0 | Melee/Reach |
| Thrown weapons / Bombs | 3 × Body (9m) | 2 | Medium — sits exactly at the "still attacks" ceiling |
| Handgun | 10m | 3 | First weapon past the ceiling — costs the attack |
| Light Bow / Blunderbuss | 15m | 4 | Long, right at the edge — 0 AP left over |
| Heavy Bow / Musket | 20m | 5 | Extreme — can't be closed in one turn |

Reads as more intentional than gut-estimated, on inspection, and
sharper than the uncorrected pass made it look: thrown weapons/Bombs
land exactly on the "still punishable in melee" line rather than past
it, Handgun is the *first* weapon that reliably buys a full turn of
safety from a baseline-Speed melee attacker, and Light Bow/Blunderbuss
sit right at the outer edge of what a single committed turn can cross
at all — a clean progression that already tracks the breakpoints
without having been designed against them explicitly.

**This shifts with the closer's actual Speed**, which matters most for
calibrating against non-baseline creatures (a fast monster, a Hasted
ally) rather than the player-facing weapon numbers themselves: a Speed
5 closer brings the Handgun's 10m back under the 2-move "still attacks"
line (`ceil((10−1)/5) = 2`), and even Heavy Bow/Musket's 20m only takes
4 moves at Speed 5-6 (`ceil((20−1)/5) = 4`, `ceil((20−1)/6) = 4`) —
still the full turn, but no longer safely uncrossable the way it is at
baseline. Worth checking any new range value against a faster baseline
too (Speed 5-6), not just the default 4, before calling it safely in a
given tier.

### Slipstream Sandals = 5.5 — a once/encounter movement item priced as an attack-enabler, not raw movement

Once/encounter, 0 AP, Teleport 3 meters (Feet, Level 2). The first pass
priced this against Push's marginal per-meter rate (`3 × 0.55 = 1.65`)
and flagged it as probably wrong — Push's rate prices incremental
Speed, appropriate for an on-hit rider, but this is a single
once-per-encounter effect with a completely different use pattern: per
the designer, "you only use them if you need the extra to hit a
breakpoint" — this item does nothing on a turn where you were already
in range, and does nothing if you're too far out for even the extra 3m
to matter. Its entire value lives in the turns where it's exactly the
difference between closing-and-attacking and wasting the turn just
approaching.

**Model: `Value = (value of landing the attack it enables) × (how
often it's actually the deciding factor)`.** The payoff side uses the
same AP-cost basis as everywhere else in this document rather than a
weapon-specific damage number (this is a generic item, not tied to any
one weapon): landing an attack costs 2 AP, so its value is `2 × 2.75 =
5.5`. Per the designer, a player who takes this item is assumed to
find a way to use it to good effect basically every fight — **frequency
= 100%** — so `Value = 5.5`.

`Target = 6` (Level 2 × 3). **Net = −0.5** — effectively at Target, no
additional rider needed.

**Why 3 meters specifically**, not some other distance: anchored to
Slowed's own already-derived rate (`balance_weights.csv` row "Slowed"),
not a hand-wavy "some obstacle." Slowed reduces Speed by 1/stack,
hard-capped at 4 stacks — at baseline Speed 4, 4 stacks zeroes movement
out completely. 3 meters is exactly *one stack short* of that full
cap: the item guarantees your one crucial move still gets through even
under near-maximal Slowed, without fully trivializing a fully-capped
Slowed. A deliberate, checkable design constraint ("Slowed-cap minus
one") rather than an arbitrary flavor number — worth reusing as a
reference point for any future item whose whole point is "still lets
you act despite a debuff."

**This is also a direct, concrete application of the range breakpoints
above**: spending the teleport plus a normal turn's 2 leftover move
actions covers `3 + 2×4 = 11m` before the attack's 2 AP, which
functionally extends the "still attacks" ceiling from 9m to 12m for
one turn per encounter — a Feet item literally moving the breakpoint
line rather than granting movement in the abstract.

Same "attack-enabler, priced via the AP-cost basis, discounted by how
often it's the deciding factor" model checked against Vaulting Boots
and Greaves of the Warlock King below, since both are also
once-per-encounter/turn movement effects rather than continuously
active ones.

### Vaulting Boots = 9.3 — rebuilt after the running-start rule was cut outright

Once/encounter, 1 AP, jump up to 10m in any direction (Feet, Level 3).
The first pass split this into an attack-enabler component (5.5, same
basis as Slipstream Sandals) plus a **flip-guarantee** component
(2.75, `50% × 5.5`), reasoning that the item's own wording ("without
requiring a running start or a flip") implied a mundane jump this size
would normally need a flip with a real chance of failure, and that
guaranteeing success was worth crediting.

**Per the designer, the running-start mechanic wasn't just stale
here — it's gone from the game entirely.** There used to be a rule
requiring you to cover a certain amount of ground before you could
long-jump (combining move actions' Speed toward one big jump/climb/
swim, per `rulebook.md:456-470` — Felix's chasm example is the clearest
illustration), cut outright for being more complicated than it was
worth. `rulebook.md`'s Moving section still describes it and needs a
rewrite to match — a separate rules-text pass, not done here.

The item itself is simplified to match, replacing the old flip-related
wording with a **Good Luck** grant instead of an outright guarantee —
you can still be asked for a flip on an unusually complicated jump, you
just get help on it:

> Once per encounter you may spend 1 AP to make a jump up to 10 meters
> in any direction. You have Good Luck on any flips related to the
> jump, and if you fall as part of the jump you ignore up to 10 meters
> of distance for the purpose of determining fall damage.

(`items.csv` `I111`, regenerated into `data/items.json`. The original
draft still referenced an "Acrobatics flip to avoid falling damage" —
per the designer, fall damage is a flat calculation now, not a flip,
so the wording is trimmed to just "determining fall damage.")

Repricing component by component:

- **Attack-enabler**: unchanged, `5.5`.
- **Fall-safety**: unchanged flat credit, `1`.
- **Vertical-jump flexibility**: the Athletics budget's standing 2-per-
  space vertical cost (`rulebook.md:456`, untouched by the running-start
  cut — a separate mechanic) means a mundane 10m *vertical* climb/jump
  needs a budget of 20 (Athletics Skill Total ≥ 40), a bar most
  characters never clear, versus 10 for the same distance horizontally.
  A flat "10m, any direction, no check" item bypasses that gate
  entirely in the harder direction, not just the easy one — a modest
  flat rider, one step above fall-safety's own +1 given it's bypassing
  a budget most characters can't reach at all: **+2**.
- **Good Luck on jump-related flips**: Good Luck's own established rate
  is `2.4/instance` (`balance_weights.csv`). Since most jumps under the
  simplified rules won't call for a flip at all — this only matters on
  the rare complicated case — it's priced at the **1/3 "rarer than
  daily, narrow single-use-case" tier**: `2.4 × ⅓ = 0.8`.

`Value = 5.5 + 1 + 2 + 0.8 = 9.3`. `Target = 9` (Level 3 × 3). **Net =
+0.3** — lands close to Target on its own, no accept-below-Target
allowance needed this time.

### Greaves of the Warlock King = 16.5 — a two-mode once/turn engine, not a single flat rate

Once/turn, 1 AP, Teleport `2 × Speed` meters (Feet, Level 5) — 8m at
baseline Speed 4. Unlike the once/encounter items above, this is
repeatable up to 5 times across a Baseline encounter, so "how often
does it matter" isn't a single yes/no — it's two distinct payoffs
depending on the gap it's used against:

- **Gap ≤ 9m** (already inside the normal "still attacks" range):
  doesn't enable anything new, just does the same job for less AP — 1
  AP instead of the 2 AP ordinary movement would cost to close the
  same ground. Backpack-precedent AP-savings: `1 AP saved × 2.75 =
  2.75/use`.
- **Gap 10-13m** (the "costs the attack" zone from the range
  breakpoints above): 1 AP on the 8m teleport, 1 remaining move action
  covers up to 4 more meters, 2 AP left for the attack — `8 + 4 + 1
  (melee range) = 13m`, exactly the full width of that zone. Full
  attack-enabler value: `5.5/use`.

Per the designer: a player who takes this item finds ways to make the
extra margin count, landing at **2 rescue uses + 2 cheap-saver uses
per encounter** — a player expanding what they can do with a
repeatable tool, same framing as Slipstream Sandals' "will find a way
to get value every fight," just split across two use-modes instead of
one.

`Value = 2×5.5 + 2×2.75 = 11 + 5.5 = 16.5`. `Target = 15` (Level 5 ×
3). **Net = +1.5**.

### Greaves of the Stalwart Guardian = 5.5 — redesigned down to Level 2 after Push/Slowed turned out to be common, not niche

Originally Level 5, three components (immovability, ignore 3 degrees
of Difficult Terrain, 5 charges/encounter to negate a stack of
Slowed), landing at a guessed ≈15.55 against Target 15 — flagged from
the start as the most guesswork in the batch. Reworked from scratch:

- **Difficult Terrain dropped entirely.** Its own rate is hard-capped
  at degree 2 (`0/2.75/8.25/8.25` for degrees 0/1/2/3+) — the rule
  itself floors movement throughput at 1m/action once terrain hits
  degree 2, so degree 3 is no worse than degree 2 to a mover. Ignoring
  3 degrees protects no more than Surestride Boots' 2 already does, and
  duplicating Surestride's whole job on a second item added nothing.
  Per the designer, this also lets the item concentrate its full budget
  on one coherent "unshakeable" identity instead of splitting across a
  third, unrelated axis.
- **Slowed-negation replaced with outright immunity**, dropping the
  5-charges tracked-resource mechanic (hard to price rigorously — no
  clean anchor, and "you choose which stack to block" added real but
  unquantifiable strategic value) for something that reads clean
  against Slowed's own established curve.
- **No knockdown/recovery credit.** Prone isn't a mechanic in this
  game — "unwillingly knocked over" is flavor for how the forced-
  movement immunity manifests, not a separate priced component.

**Frequency was the real correction, and it went the opposite
direction from the first guess.** Initially assumed Push/Shift/
Teleport effects were rare, based on `\bpush\b` across `techniques.csv`
finding only one hit (Spellblade, `T100` — itself flagged as "not
priced against this model at all yet," so not a trustworthy magnitude
reference either). That search missed `features.csv` entirely: Push
and Slowed are both cheapest-tier **Basic** Features on the two most
generic, broadly-available Buildable techniques in the catalog —
**Lodestone** (`F010`, Battle Maneuver, 1 point — Push `2×[X+Spades]`
meters on hit/Parry) and **Kinetic** (`F070`, War Magic, 1 point — Push
up to `[4×X]+Spades` meters on hit), with **Hamstring** (`F008`) and
**Frigid** (`F071`) doing the same for Slowed. Any ordinarily-built
martial or caster enemy could plausibly carry one — not niche at all.

Per the designer: rather than pricing each trigger as its own
independent ½-tier event (which implies *something* relevant in 75% of
fights, `1 − 0.5×0.5`), the two triggers split one shared "about half
of fights feature either a Push- or a Slow-relevant threat" — 25% each
if split evenly, no signal either is more common than the other:

- Immovability: representative hit ≈ `8m × 0.55/meter = 4.4` (still a
  constructed placeholder — Spellblade's own number is unreliable,
  and neither Lodestone nor Kinetic resolve to one fixed "typical"
  distance since both scale with X and a suit flip), realized 25% of
  fights: `4.4 × 0.25 = 1.1`.
- Slowed immunity: full cap `17.6`, realized 25% of fights: `17.6 ×
  0.25 = 4.4`.

`Value = 1.1 + 4.4 = 5.5`. Per the designer, a reactive, niche item
shouldn't be pushed to fit a bigger Level than it earns — **dropped to
Level 2** (`Target = 6`) rather than stretched to justify staying at
Level 5. **Net = −0.5**, the same modest-shortfall shape as Surestride
Boots' own −0.75.

Effects text simplified to match (`items.csv` `I112`, regenerated into
`data/items.json`): "You cannot be unwillingly knocked over, Pushed,
Shifted, Teleported, or otherwise moved unless they wish to be. You
are immune to Slowed." Cost dropped from 100 Gold (Level 5) to 40 Gold,
matching this slot's flat Level × 20 Gold convention.

### Feathered Sandals = 4.0 — moved off Narrative Utility once fall damage turned out to be a real, guaranteed-harm anchor

Originally priced as plain Narrative Utility (`Value = ⅓ × 3 = 1`, Net
−2), on the reasoning that it had "no clean AP/frequency anchor" — but
its own wording was stale first: "automatically succeeds on flips to
avoid damage when falling 10 meters or less" describes a fall-damage
flip that doesn't exist anymore (fall damage is a flat calculation:
reduce distance by Essence or half Acrobatics Skill Total, lose Health
for the rest — same correction already made to Vaulting Boots).
Reworded to match, and made unconditional rather than gated to a
specific ability (`items.csv` `I108`): "The wearer ignores up to 10
meters of distance for the purpose of determining fall damage, from
any fall."

Once it's read as "ignores 10m of distance" rather than "avoids a
flip," the old "no clean anchor" reasoning stops being true — this
prevents *guaranteed* Health loss (no attack roll involved, same shape
as Resist), which is exactly what Health's own guaranteed-harm rate
(4/point) already prices. No baseline Essence or Acrobatics Skill
Total exists anywhere in this document the way baseline Speed (4) or
Body (3) do, so a representative case has to be constructed rather
than derived: a **6m fall** (a real, moderate, plausible fall — not an
extreme case) against a **baseline reduction of 3** (matching the
"baseline stat = 3" pattern used for Body/Agility elsewhere).
Unmitigated damage `= max(0, 6−3) = 3`; with the item, effective
distance drops to 0, fully negating it. `Prevented = 3 × 4 = 12` raw.

Checked `features.csv`/`techniques.csv` for anything that forces a
fall as a combat consequence, the same way Push/Slowed got checked —
found nothing (`Bound Across Mountains`/`Falling Tumble` both just let
you substitute a different stat into the existing reduction formula,
not create new fall scenarios). Unlike Push/Slowed, there's no reason
to think falling is more common than it looks, so it stays on the
**⅓ "rarer than daily, niche" tier**: `12 × ⅓ = 4.0`.

`Target = 3` (Level 1). **Net ≈ +1.0**. The 6m/reduction-3 case is a
constructed placeholder, not a firm derivation the way Speed's rate
or Slowed's curve are — flagged as a first stab, open to a different
representative fall if a better anchor turns up later.

### Shadowcat Slippers = 4 — the softest number of the batch, likely still wants a redesign pass

Wall-running, unconditional, for the whole encounter. Structurally the
same shape as Vaulting Boots' vertical-jump flexibility rider (+2,
bypassing the Athletics budget's 2-per-space vertical cost — the same
steep bottleneck) — but continuously available rather than gated to
one guaranteed use, the same permanent-vs-single-use distinction that
required multiplying Speed's rate by moves/encounter for Lightfoot
Shoes.

Unlike that derivation, this one isn't built on a hard per-meter or
per-move rate — Vaulting Boots' own +2 was already a soft, constructed
flat credit, not a firm number. Multiplying a soft flat guess by an
assumed frequency compounds uncertainty rather than resolving it, so
treat this accordingly: assuming roughly **2 meaningful uses/encounter**
where vertical mobility actually matters (same order of magnitude as
Greaves of the Warlock King's own "2 uses" figure), `Value ≈ 2 × 2 =
4`. `Target = 6` (Level 2). **Net ≈ −2** — better than the original
Narrative Utility −4, but this is the least-grounded number of the
three Feet-slot items revisited this pass. Probably wants the same
kind of redesign conversation Greaves of the Stalwart Guardian got,
rather than being treated as settled.

Per the designer, the wording was ambiguous about whether wall-running
happened at the wearer's normal Speed or something slower — clarified
rather than changed (`items.csv` `I155`, regenerated into
`data/items.json`): "The wearer can run up walls and other vertical
surfaces at their full Speed, but must end their turn on a stable
surface or fall." This was already the assumption behind the Value
derivation above, so it doesn't move the number.

### Swim Flippers (formerly Cobblestone Boots) = 1 — renamed and simplified, Net unchanged

The original mechanic (full-Speed underwater walking, no buoyancy) was
checked against the same vertical-budget-bypass lens that helped
Vaulting Boots/Shadowcat Slippers and didn't hold up: swimming only
costs 1/space from the Athletics budget — the same gentle *horizontal*
rate as jumping, nothing like vertical's steep 2/space wall. Most
reasonably-built characters can likely already swim at full Speed
without this item, so there was no real bypass value to price beyond
Narrative Utility's flat credit.

First redesigned to add a no-need-to-breathe-underwater guarantee, then
walked back — per the designer, water-breathing belongs to a different
slot's job, not this one. Settled (`items.csv` `I107`, regenerated into
`data/items.json`): "The wearer may swim with no penalty, at their full
Speed." A plain swim-Speed item, renamed off the old "walk the
seafloor, immune to buoyancy" framing since that's an oddly specific
niche for a boot enchantment, on the "Leather" material tag flippers
actually call for rather than the old "Metal."

Still no clean economic anchor (swim distance isn't gated by AP spend
or hit chance any more than the old buoyancy effect was), so it stays
on the plain **Narrative Utility** formula: `Value = ⅓ × 3 = 1`.
`Target = 3` (Level 1). **Net = −2**, unchanged from the original
Cobblestone Boots throughout every version of this item — the formula
is Level-based, not effect-based, so this was always going to land
here regardless of which specific water-themed flavor it settled on.

### Surestride Boots = 8.25 — simplified to "ignore all," Net unchanged

Was "ignores 2 levels of Difficult Terrain," the cleanest, most
directly-derived number in the whole Feet slot — Difficult Terrain's
own rate hard-caps at degree 2 (`0/2.75/8.25/8.25` for degrees
0/1/2/3+), so ignoring 2 degrees already sat at the full capped value,
`Value = 8.25` with no construction or guesswork needed.

Per the designer, simplified to "ignores all Difficult Terrain"
(`items.csv` `I188`, regenerated into `data/items.json`) — Difficult
Terrain beyond degree 2 doesn't exist in a meaningfully different way
mechanically (the rule itself floors movement throughput at 1m/action
once terrain hits degree 2, so degree 3+ was never worse to a mover
than degree 2 already was, the same reasoning that let Greaves of the
Stalwart Guardian's "ignore 3 degrees" get cut without losing anything
real). Ignoring "all" therefore grants exactly the same practical
protection "ignore 2" already did — a pure wording simplification, not
a power change. `Value` stays `8.25`, `Target = 9` (Level 3 × 3),
**Net = −0.75**, unchanged.

**Wording updated again** during the immunity/prevention phrasing
standardization pass below: "ignores all Difficult Terrain" →
"ignores the effects of Difficult Terrain," matching the "ignores the
effects of X" template for non-stacking mechanics. Still no power
change — same `Value = 8.25`, `Net = −0.75`.

## Head slot — first pass

### Confident Cap, Cap of Smug Confidence, Stoic Skullcap, Sympathetic Hat — consolidated from four defensive items into three offensive Skill hats

Started as a quick value-model sanity check across all ten Head Masterwork
items, which flagged these four as needing attention before pricing —
`I060`/`I168` share near-word-for-word fluff ("simple but impressively
crafted, designed in an understated fashion but woven with silver
threading...") under different names, the exact same gap-fill-batch
duplication pattern that produced Attuned Shroud in the Torso pass.

**Confident Cap turned out to be worse than a duplicate — its whole
mechanic is built on defunct rules.** Its text ("Whenever you are in
the front in a social contest and your party would gain a Concession...")
references "front" and "Concession," neither of which exist in the
current Social Contests rules (`rulebook.md:579-629`): the actual
system is Statements (a Presence/Rapport/Persuasion flip against
Mental/Instinct Defense) and Pressure (an accumulating Bad Luck stack
on Statements) — already noted elsewhere in this document ("Pressure
literally *is* imposed Bad Luck, not a separate mechanic"). Confident
Cap was the most antiquated item found in the Head slot audit.

**Redesigned as three Level 1 items, one per social Skill** (Presence,
Persuasion, Rapport), each granting Good Luck on that Skill's flips
**outside of a social contest** — a single flat-difficulty check,
Support, or any other narrative use, rather than the contested
Statement itself. Worded to avoid the term "Statement" entirely
(per the designer, that framing is being reworked into something else,
not yet reflected in `rulebook.md`) — scoping instead to "other than
those made as part of a social contest," which stays correct regardless
of what the contest-check ends up being called.

Repurposed existing IDs/flavor rather than creating new ones, matching
each hat's fluff to the Skill it already suited best:

- **`I060` Confident Cap → Persuasion** ("every expert negotiator can
  be seen sporting one"). Fluff trimmed — the original justified two
  different effects via "the styling of the hats varies," which no
  longer applies now that the family is split one-Skill-per-hat.
- **`I168` Cap of Smug Confidence → Presence** (the more generic of
  the four fluff-wise; kept largely as-is).
- **`I170` Sympathetic Hat → Rapport** ("helps attune the emotions of
  the wearer with those around them... understand the feelings that
  drive others") — already read as Rapport almost exactly as written,
  no rework needed.
- **`I169` Stoic Skullcap → retired**, doesn't map cleanly to an
  offensive Skill-buff (its flavor — resisting *others'* persuasion —
  is defensive, not offensive). Per the designer, its name/flavor is
  reserved for a future Neck-slot item that deals with Pressure
  directly, not reused here. Row deleted from `items.csv`.

**Pricing**, identical shape for all three: Good Luck's own rate (2.4)
at the **½ "genuine recurring demand"** tier — the standardized tiers
doc's own worked example for exactly this case ("a Skill Good Luck
tied to genuine recurring demand, e.g. Techniques that call for
Medicine flips"). `Value = 2.4 × 0.5 = 1.2`.

Checked against real precedent before finalizing the Level: three
existing Hands-slot items already do this exact "Good Luck on one
Skill's flips" shape — Field Surgeon's Handwraps (`I153`, Level 2,
unconditional Good Luck on Medicine), Deft Gloves (`I076`, Level 2,
Good Luck on Craft plus a tool-replacement clause — nearly identical
in structure to these hats), and Nimble Fingers (`I225`, Level 2,
Good Luck on Stealth for theft specifically). All three sit at Level
2, not Level 1 — and while the derived `Value = 1.2` actually fits
Level 1's `Target = 3` (`Net = −1.8`) better than Level 2's `Target =
6` (`Net = −4.8`) under this model, those three items predate this
balance pass and were never run through it (the same risk `balance.md`'s
Open balance work section already flags across the untouched
Masterwork list generally). Per the designer, pegged to **Level 2**
anyway for consistency with what's already live, rather than trusting
the model over existing precedent here — `Target = 6`, **Net = −4.8**
for all three. `items.csv` `I060`/`I168`/`I170` updated (Level 1→2,
Cost 20→40 Gold), regenerated into `data/items.json`. Field Surgeon's
Handwraps/Deft Gloves/Nimble Fingers themselves are flagged as
candidates to re-examine once the Hands slot gets its own pass.

### Hat of Disguise = 1.2 — a new fourth Skill hat, same family as the three above

New item (`I226`), added rather than found during the audit — a D&D-
"Hat of Disguise"-style pitch, checked against real support before
drafting: Masquerade (`rulebook.md:272`) is disguising yourself and
acting in character, already backed by a mundane Disguise Kit
(`I015`) and several Masquerade-focused Techniques (Practiced Persona,
Ventriloquy, Air of Mystery, One of Many Faces). Confirmed Masquerade
targets Insight Defense and isn't one of the three Skills a Statement
uses (Presence/Rapport/Persuasion) — a genuinely separate mechanic,
not a fourth flavor of the same thing.

"The wearer has Good Luck on Masquerade flips, and does not need a
Disguise Kit to attempt a disguise." Same pricing shape as the three
social hats: `Value = 2.4 (Good Luck) × 0.5 (½ tier) = 1.2`. Pegged to
**Level 2** for the same reason as the other three (matching existing
Hands-slot precedent over the model's own preferred Level 1 — see
above): `Target = 6`, **Net = −4.8**, matching the other three
exactly. The
"no Disguise Kit needed" clause is left unpriced — kits are cheap and
common, so this is a flavor-consistent convenience (the classic "the
hat alone handles it" trope) rather than a real value swing, the same
call made for Difficult Terrain's "ignore 2" vs. "ignore all" not
moving Surestride Boots' price.

### Cowl of Tranquility = 5.5 — cut from a Level 1-5 range down to a fixed Level 2, charges converted to outright immunity

Was `1-5`, "starts each encounter with `[Level]` charges," negate a
stack of Taunted or Frightened per charge. Checked `features.csv` the
same way Push/Slowed got checked for Greaves of the Stalwart Guardian:
**Taunted is just as common** — "Distracting" (`F004`, Battle
Maneuver, Basic, 1 point) inflicts it on hit/Parry, the same
universal-technique-Basic-feature pattern as Push/Slowed — but no
Frightened-inflicting feature was found (only `F043` Embolden, which
*removes* it), so Frightened doesn't get the same confidence boost.

**The structural problem**: charges scale `1× Level`, but Target
scales `3× Level`, and per the designer a single relevant attack only
ever grants 1-2 stacks — realistic usage caps out low regardless of
how many charges a higher Level buys, so the shortfall only gets worse
with Level, not better (unlike Lightfoot Shoes' proportional gap, this
one is absolute and flat while Target keeps climbing). No Level fixes
this on its own; it needed the same "right-size the Level, don't
stretch the effect" move Greaves of the Stalwart Guardian got.

**Solved for the charge count a fixed Level 2 (`Target = 6`) would
need**: `charges × 2.2 (Taunted/Frightened's own rate) × 0.5 (½
"genuine recurring demand" tier, matching the Head slot's social hats
above) = Target` → `charges ≈ 5.45`. 5 charges lands at `Value = 5 ×
2.2 × 0.5 = 5.5`, `Net = −0.5` — but per the designer, 5 charges
already covers realistic Taunted/Frightened exposure in a fight so
completely that tracking them as a resource is pointless theater —
functionally equivalent to outright immunity. Simplified to match,
same move as Greaves of the Stalwart Guardian's Slowed-charges → Slowed
immunity, and Surestride Boots' "ignore 2" → "ignore all": a wording
simplification once the charge count already covers the realistic
ceiling, not a power change. `Value` stays `5.5`, `Net` stays `−0.5`.

`items.csv` `I057`, regenerated into `data/items.json`: fixed at
**Level 2** (was `1-5`), Cost fixed at 40 Gold (was Level × 20 via
`Value Per Level`, no longer applicable to a fixed-Level item),
Effects simplified to: "You cannot gain stacks of Taunted or
Frightened." (Wording updated again in the standardization pass below
— was "You are immune to Taunted and Frightened" at first.)

### Immunity/prevention wording standardized across items.csv and techniques.csv

Audited every "immune to"/"cannot gain"/"ignored instead"-style clause
in both files — four genuinely different patterns had accumulated:
full unconditional immunity ("You are immune to X"), count-limited
prevention ("the next/first N stacks... instead you don't" vs. "...are
ignored instead" — two different verbs for the same mechanic), a
hedged partial immunity (Pranic Nourishment's "effectively immune,"
deliberately not full since it still allows intoxication), and
Difficult Terrain's own non-stacking "ignores" phrasing.

Per the designer, standardized to two templates:

- **Full immunity to a stacking debuff**: "cannot gain stacks of X."
  Applied to Cowl of Tranquility (`I057`) and Greaves of the Stalwart
  Guardian (`I112`), both "You are immune to X" → "You cannot gain
  stacks of X."
- **Full immunity to a non-stacking mechanic**: "ignores the effects
  of X." Applied to Surestride Boots (Difficult Terrain, see above)
  and Corrupted Blood (`T090`, Technique) — poison isn't stack-based
  (Concentration/Potency instead), so "cannot gain stacks of" doesn't
  literally apply; "You are immune to this poison" → "You ignore the
  effects of this poison" fits the non-stacking template instead.
- **Count-limited prevention**: "ignore the first N stacks of X you
  would gain," replacing both older verbs. Applied to Muscular Feast
  (`I026`), Kiss of the Earth (`I204`), Predator's Cry (`I205`), and
  Coat of Knit Flesh (`I070`) — the latter's old "...are ignored
  instead" was the specific inconsistency that started this audit.
  Any trailing mechanical clauses (Muscular Feast's "choose which
  stacks to prevent" for simultaneous effects; Kiss of the
  Earth's/Predator's Cry's "if you already have stacks, remove them
  and count them against the total") are unchanged — only the lead-in
  verb moved.

Pranic Nourishment (`T085`) deliberately left alone — it's genuinely
partial (doesn't prevent intoxication), not a full-immunity case
either template fits.

No pricing changes from any of this — every edit here is a wording-
only pass, not a mechanical one. All regenerated into `data/items.json`
and `data/techniques.json`.

### Mask of Night = 2.2 — priced off Heavy Cover's Bad-Luck-twice rule

Level 1. "When the mask is in place it grants its wearer perfect
vision in darkness, negating any penalty to sight due to a lack of
light. Smoke or anything else that physically obscures sight is not
negated, however."

Real anchor: total darkness counts as Heavy Cover (`rulebook.md:512`),
which gives Bad Luck twice on "flips to see you" *and* on attacks
against Dodge/Parry. This item negates the wearer's own side of that —
their sight-related flips while in darkness — not the
attacker's-difficulty-seeing-them side, which is a different
beneficiary this item doesn't touch. `Value = 2 × 2.2 (Bad Luck's
rate, mirrors Good Luck) × 0.5 (½ "genuine recurring demand" tier,
same as the social hats and Cowl of Tranquility above) = 2.2`. `Target
= 3` (Level 1). **Net = −0.8**.

### Headband of Telepathy = 1 — confirmed as-is, no numeric anchor exists or is being sought

Level 1. "The wearer can communicate telepathically with one creature
they can see within 20 meters, for the rest of the scene." Pure
Narrative Utility, `Value = ⅓ × 3 = 1`, `Net = −2`, same formula as
Feathered Sandals originally and Swim Flippers. Per the designer,
confirmed deliberately rather than reworked further — this is a "gut
feeling, niche, and that's fine" item, not one meant to ever get a
harder numeric anchor. Left as Level 1 with no changes.

### Lens of Daybreak = 1.2 — confirmed at the ½ tier, same as Mask of Night

Level 2. "The wearer has Good Luck on Awareness flips that
specifically involve sight." Per the designer, sight-based Awareness
checks are genuinely common (spotting stealthing enemies, general
perception) — but the value per success is soft/narrative ("succeeding
on them can give the party great ways to move forward") rather than a
guaranteed hard payoff, so this confirms the ½ "genuine recurring
demand" tier rather than pushing to the full "every encounter" one —
matches Mask of Night's own reasoning exactly, just for a different
sight-related trigger. `Value = 2.4 (Good Luck) × 0.5 = 1.2`. `Target =
6` (Level 2). **Net = −4.8** — the biggest shortfall of the Head slot
items reviewed so far, since Awareness-specifically-sight is a
narrower Skill-use than Mask of Night's broader darkness-negation.

### Wizardly Hat of Tam the Tipsy = a real per-use accounting, using Gold's own established rate for the first time

Level 3. "Whenever the wearer drinks Alcohol, they may regain the use
of an Encounter Technique with a Level equal to or lower than the
Alcohol's own Level." No established rate exists for "the value of
regaining an Encounter Technique use" — Techniques generally haven't
been run through this Value/Target model at all (Spellblade's own
writeup flags it as unpriced). Per the designer, this item predates a
planned suite of Alcohol-cost Techniques and stays as a fun legacy
item for now rather than getting formalized — but the accounting
below is worth keeping for whenever that suite gets priced, since it
establishes real anchors this document didn't have before.

**Gold has an established conversion this document hadn't used until
now**: `Gold = 1.5` (Locked, `balance_weights.csv`, "reciprocal of
Baseline's Value/Gold ratio"). Alcohol (`I195`-`I199`, 1-5 Gold across
Levels 1-5) is therefore worth `1.5 × Level` in raw Value with no
construction needed. A technique-refresh's own value has no established
anchor, so — per the designer's working assumption, not a verified
fact — it's treated as worth the same `Level × 3` a same-Level item
would be, on the reasoning that a Level-N technique should deliver
comparable power to a Level-N item. That gives a clean, level-invariant
finding: **a technique refresh is worth exactly double what that
Level's Alcohol costs** (`3N` vs. `1.5N`), so net benefit per matched-
Level use is just Alcohol's own Value again (`1.5 × Level`).

**First pass (2 AP to drink, matching a Potion's cost) read badly.**
Subtracting the 2 AP opportunity cost (`2 × 2.75 = 5.5`, the same
"AP has a real, comparable-value alternative — an attack" basis the
attack-enabler items use) alongside Alcohol's own cost:

| Level | Technique value (3N) | Alcohol cost (1.5N) | AP cost | Net/use |
|---|---|---|---|---|
| 1 | 3.0 | 1.5 | 5.5 | −4.0 |
| 2 | 6.0 | 3.0 | 5.5 | −2.5 |
| 3 | 9.0 | 4.5 | 5.5 | **−1.0** |
| 4 | 12.0 | 6.0 | 5.5 | +0.5 |
| 5 | 15.0 | 7.5 | 5.5 | +2.0 |

At the hat's own Level, triggering it was a net *loss* compared to
just attacking that turn — only break-even to positive at Level 4-5
Alcohol/technique pairs. More uses didn't accumulate toward Target the
normal way, since each individual use below Level 4 was itself
negative.

**Redesigned per the designer**: the hat holds its own Alcohol supply
(up to twelve doses) and drinking from that stock costs **0 AP** as
part of using it — removing the AP-opportunity-cost term entirely.
Net benefit per matched-Level use reverts to `1.5 × Level` (1.5, 3.0,
**4.5**, 6.0, 7.5 for Levels 1-5) — positive at every Level now, not
just 4+. At Level 3, **2 uses in a single encounter exactly hits
Target** (`2 × 4.5 = 9`, `Net = 0`) — clean, though every use is
scoped to *within* one encounter specifically, never between them
(an Encounter Technique refreshes for free at the next encounter
regardless, so recovering one between fights is worthless — the
ability only ever does something real when it recovers a technique
already burned earlier in the *same* fight).

Flagged, not resolved: with 0 AP cost and a dozen-dose reserve, the
real ceiling on uses/encounter isn't anything this item controls
anymore — it's just however many Encounter Techniques the wearer
knows and burns in one hard fight. A character cycling through 3-4
Techniques in a tough encounter could plausibly trigger this 3+ times
(`Value` 13.5+, `Net` +4.5 or more), meaningfully over Target. Left
as-is per the designer rather than fixed now, since this stays a
legacy item pending the future Technique suite, not something being
actively rebalanced today.

Effects text updated to match (`items.csv` `I171`, regenerated into
`data/items.json`): "The hat can hold up to twelve doses of Alcohol,
and drinking Alcohol stored this way costs 0 AP. Whenever the wearer
drinks Alcohol, they may regain the use of an Encounter Technique with
a Level equal to or lower than the Alcohol's own Level."

### Crown of Glory — set aside, not resolved

Level 5. "Once per day, for 0 AP, the wearer may have themselves and
up to 4 allies who can see them each draw a card." Priced at `Value =
5 × 2.7 (Card) = 13.5` against the once/day `Target = Level × 6 = 30`,
**Net = −16.5** — the largest raw gap in the Head slot. A "wearer +
up to `2 × Level` allies" scaling formula was worked out as a possible
fix (lands Net from +2.1 at Level 1 down to −0.3 at Level 5 — a tight
fit), but per the designer, the deeper concern isn't the Level-scaling,
it's whether a Head-slot item should be generating extra cards at all
— generic party-wide card generation reads as more of a capstone-tier
effect than a normal equipment-slot one. Set aside rather than fixed;
the designer wants to work out the rest of the slot first, then
revisit what a new capstone-appropriate design should look like here,
rather than patch the current mechanic's numbers.

### Third Eye = ~1.0, follow-up pass — three of four backlog candidates resolved by checking what actually exists to hook into

Level 1, 20 Gold, Brilliant. Last of four Head-slot candidates sitting
in `IDEAS_BACKLOG.md` since the original Head-slot pass. The other
three (True-Seeing Lenses, Circlet of Clarity, Comprehend Languages
Circlet) all got cut outright on the same root problem, caught one
after another: each reached for a mechanic — Invisibility/illusion
magic, a distinct Charm/domination keyword, a language system — that
simply doesn't exist anywhere in this ruleset, so there was nothing
real for the item to interact with. Worth remembering as a pattern:
check whether the thing an item claims to detect/pierce/resist is an
actual live mechanic before drafting it, not after.

This one grounds out in two real things. Per the designer, built as a
weaker, universally-accessible cousin of **Artisan's Eye** (`T046`,
Level 3 Technique, gated behind Craft/Mixology/Survival 4 + Academics
2) rather than a duplicate of it:

1. **Reduces the baseline "examine a Masterwork item for an hour" rule**
   (`rulebook.md`'s Equipment section) down to 10 minutes. Pure
   downtime convenience, no combat relevance — the model has no real
   way to price this (same reasoning as the Narrative Utility
   convention, though this is one component of a two-part item rather
   than the item's whole basis).
2. **Good Luck on any flip made to identify or make sense of an
   unfamiliar magical effect or phenomenon** — broadened per the
   designer from an initial Academics-only draft, since Sorcery or
   Theurgy will often be the actually-relevant Skill depending on what's
   being identified, not just Academics. Standard niche-tier Good Luck:
   `2.4 × ⅓ = 0.8`.

Combined estimate **~1.0 Value**, `Target = 3` (Level 1), **`Net ≈
−2.0` (33% funded)** — the same modest tier as Cloak of Caches/Diver's
Necklace/Watcher's Mantle, consistent with a flavorful niche-utility
item rather than a combat-relevant one.

**Flagged, not fixed**: Artisan's Eye's own Effects text references
"as though you had flipped a 13 to analyze it," but no "analyze" check
is documented anywhere in `rulebook.md` — the only baseline rule found
is a plain, rollless "examine for an hour" line. This suggests Artisan's
Eye's real value-add is purely collapsing that hour down to instant,
not removing some failure chance that may never have existed in the
first place. Worth a look whenever Techniques get their own review pass.

## Neck slot — first pass

### Cloak of Caches, Diver's Necklace = 1 each — plain Narrative Utility

Both Level 1, no combat mechanic to anchor to, same formula as
Feathered Sandals originally and Swim Flippers: `Value = ⅓ × 3 = 1`,
`Target = 3`, **Net = −2** each.

- **Cloak of Caches**: produces mundane adventuring gear (rope, flint
  and steel, a bowl, twine, and similar) on demand, one of each at a
  time.
- **Diver's Necklace**: breathe water perfectly.

Diver's Necklace is worth noting as a direct confirmation of an
earlier call: Swim Flippers (Feet slot) originally had a
water-breathing clause added, then cut per the designer since "that
would be a different slot's job" — this is that slot, already live
with exactly that effect, at exactly this Narrative Utility price.

**Choker of Silent Whispers cut entirely** (`I062`, removed from
`items.csv`, regenerated into `data/items.json`) — checked against
Headband of Telepathy (Head, also Level 1) and found to be a strictly
*worse* version of the same idea rather than a genuine alternative:
half the range (10m vs. 20m), a single message instead of a standing
"rest of the scene" channel, and a visible tell Headband of Telepathy
doesn't have ("will be able to tell... if they see the wearer
whispering"). Per the designer, this kind of remote-communication
effect belongs on Head, not Neck — Headband of Telepathy is the
correct version of the idea, this was a redundant, strictly-inferior
reskin of it on the wrong slot.

### Shroud of Shadowy Stillness = 1.2 — dropped to Level 1

Same Good-Luck-on-a-Skill shape as the Head hats: "While wearing the
shroud and not moving, the wearer becomes very hard to perceive, and
has Good Luck on Stealth flips as long as they remain still." `Value =
2.4 × 0.5 (½ tier) = 1.2`, unchanged. Per the designer, dropped from
Level 2 to **Level 1** rather than matching the Head hats' Level-2 peg
— unlike those, there's no existing same-shape item elsewhere in the
catalog pulling this one toward Level 2, so it stays on the model's
own preferred fit: `Target = 3`, **Net = −1.8**. `items.csv` `I148`
updated (Level 2→1, Cost 40→20 Gold), regenerated into
`data/items.json`.

### Watcher's Mantle = 2 — confirmed at Level 2, wording clarified

No combat mechanic — pure Narrative Utility, `Value = ⅓ × 6 = 2`,
`Target = 6` (Level 2), **Net = −4**. Per the designer, confirmed at
this Level/tier rather than dropped to Level 1 like Shroud of Shadowy
Stillness — "never sleep, rest on your own schedule" reads as enough
of a step up from the Level 1 utility items to stay where it is.

Wording clarified rather than the mechanic changed (`items.csv` `I149`,
regenerated into `data/items.json`): the old "worn the mantle
continuously for a full day" was ambiguous about whether that meant a
literal 24-hour timer or specifically passing through a night's rest.
Now explicit: "This only begins functioning after the wearer has worn
the mantle through a full night's rest, without receiving its benefits
during that rest" — the mantle needs one full rest cycle to activate,
during which its own benefits don't apply yet.

### Shawl of the Land = 5.5 — a real anchor for "doesn't need to eat," not just Narrative Utility

Two components. The **+1 Health from a full night's rest** piece uses
Health's own guaranteed-harm rate (4/point, the same basis as Feathered
Sandals' fall-safety re-derivation) directly: `Value = 1 × 4 = 4`.

The **"doesn't need to eat or drink"** piece got a real anchor instead
of the usual Narrative Utility fallback: Travel Rations (`I023`, the
plain, no-bonus Level 1-5 Food item — "enough food for a single person
for an entire day," nothing else) needs `Total Materials: 1` with no
type specified, and this project's own crafting convention is "a
material is baseline worth its Level in Gold" (`convert.py:339`). At
Level 1 that's **1 Gold** — through the established `Gold = 1.5` rate,
**1.5 raw Value**. Per the designer, that's the credit for this piece:
the value of the basic Level 1 food item this shawl makes unnecessary.

`Value = 4 + 1.5 = 5.5`. `Target = 6` (Level 2). **Net = −0.5** — a
clean, close fit.

Wording clarified the same way as Watcher's Mantle (`items.csv` `I150`,
regenerated into `data/items.json`): "worn continuously for 24 hours"
→ "This only begins functioning after the wearer has worn the shawl
through a full night's rest, without receiving its benefits during
that rest."

**Known inconsistency, kept deliberately.** Both components here are
daily-cadence (once/rest), not per-encounter — under the once/day
`Target = Level × 6` convention used elsewhere (Crown of Glory,
Choker of Defiance below), this should really be checked against
`Target = 12`, not the standard `Target = 6`, which would make it read
as badly undervalued rather than a clean −0.5 fit. Per the designer,
left as-is anyway — Shawl of the Land is accepted as a deliberate
exception to the once/day Target convention rather than rescoped to
match it, since compared against the standard per-encounter Target the
number already lands well. Worth remembering if this item ever gets
revisited: the −0.5 Net is real only under the standard Target, not
the once/day one this item's own cadence would technically call for.

### Cape of Many Pockets — cut, duplicates existing Belt items

Level 3. "The cape has 12 pouches, each an easily-accessible container
that can hold an object no larger than 1 meter in any dimension.
Stored items are weightless and cannot be damaged." Checked against
Belt's own lane ("carrying items," `RULES_DESIGN.md:129`) and found
to be a clean duplicate, not just a thematic overlap — two existing
Belt items already do this exact job: **Placeholder's Bottomless
Belt** (`I189`, Level 1, 20 pouches for small objects — the same
"many pouches" shape, more pouches, a third the Level) and **Sash of
Deep Pockets** (`I105`, Level 3, 20 cubic meters of capacity-gated
storage — bigger and more flexible at the same Level). Nothing about
Cape of Many Pockets carved out real space between those two. Per the
designer, cut entirely rather than ported to Belt, since Belt already
covers this ground better. Removed from `items.csv` (`I174`),
regenerated into `data/items.json`.

### Snowfall Drape = 8.25 — redesigned to a fixed Level 3, fixed 2 degrees, Burst 1 footprint

Originally Level 1-5, "leave snow in the first 3 spaces you move from
that action. Those spaces each gain `[Level]` degrees of Difficult
Terrain." Difficult Terrain's own rate is non-linear and hard-capped at
degree 2 (`0/2.75/8.25/8.25` for degrees 0/1/2/3+, per the Speed-4
baseline derivation above) — so this had the same plateau shape Cowl of
Tranquility had before its fix, except landing the opposite way: priced
per-creature-caught against a "clever player really bogging down
enemies" framing (2-4 creatures caught across an encounter), even the
most conservative case already blew past Target at Level 2 and got
worse at every Level above it. Reworked from scratch rather than patched:

- **Footprint changed from a 3-space line to Burst 1**, centered on the
  space the wearer moved from (see the new `Burst (X)` keyword,
  `glossary.md`) — a deliberate nerf as well as a terminology cleanup.
  A straight 3-meter line forces a full 3-meter crossing on anyone
  walking its length; Burst 1 is a circle of diameter 2m, so the
  worst-case straight-through crossing drops to 2 meters.
- **Degrees fixed at 2**, no longer scaling with Level — Level 3-5
  bought nothing extra under the old `[Level]` scaling anyway, since
  degree hard-caps at 2, so tying the item's own Level to that number
  was always going to either underdeliver (Level 1) or plateau
  (Level 2+). Fixed magnitude, Level now just sets where it sits
  against Target.
- **Crossing cost is stepped, not linear** — a single move action
  already covers up to Speed (4m baseline) for free, so terrain cost
  only bites once the ground covered exceeds what one action would
  normally take: crossing 1m of degree-2 terrain costs the same 1
  action a clear-ground move would (0 extra); crossing the full 2m
  diameter costs 2 actions against a normal 1 (**1 extra action**,
  `Value = 1 AP's value (2.75)`). No partial-action credit for "half a
  space" — the cost is 0 or 2.75 per space actually crossed, nothing
  between.
- **Priced at 3 creatures caught, each crossing the full diameter**:
  `Value = 3 × 2.75 = 8.25`. Against `Target = 9` (Level 3), **Net =
  −0.75** — a clean fit, and a more defensible creature-count than the
  old line-footprint's "chokepoint catches everyone forced through,"
  since a round Burst can be approached (and partially dodged) from any
  direction rather than only blocking one lane.

`items.csv` (`I065`) updated: Level `1-5` → fixed `3`, Cost blank/`Value
Per Level: 20` → fixed `60 Gold` (matching the existing 20-Gold/Level
convention), Effects reworded to "Once per encounter, when you move,
you may ruffle the cloak and leave snow in Burst 1 of the space you
moved from. Those spaces each gain 2 degrees of Difficult Terrain that
last for the encounter." Regenerated into `data/items.json`.

### Choker of Defiance = 5.4×Level — Sift's suit-pool credit derived, locking clause kept

Originally `[twice Level]` charges, "spend X charges to Sift X cards and
add their suits to the suit pool" before a flip. Reworked in three ways:

- **Timing moved to an Interrupt after a flip** — it adds the sifted
  cards' suits to *that flip's* suit pool, so it needs to resolve
  before the flip's effects land, same window `Play` from hand already
  uses to feed a suit pool reactively. "Before making a flip" didn't
  actually support that.
- **Suit-pool credit properly derived**, not folded silently into
  Sift's plain 0.60/card rate (which only covers the "stack the deck"
  future-draw benefit, not this). Per the designer's correction, each
  matching-suit card grants its *own* Extra Success (not just "does at
  least one match" — the model Good Luck's 2.4 correction used), so the
  right measure is **expected number of matches**, linear via
  expectation: each card is an independent 13/52 = ¼ chance to match a
  given suit, worth `¼ × 2 (Extra Success) × 0.5 (not every flip cares)
  = 0.25/card` at the naive floor. Bumped to **0.30/card** (designer's
  judgment call, same shape as Card's premium over Good Luck's own
  floor) to credit suits sometimes triggering more than a plain Extra
  Success. Combined per-card value: `0.60 (stack the deck) + 0.30
  (suit pool) = 0.90/card`.
- **Locking clause kept deliberately** (not dropped even though a flat
  charge cap alone would have worked) — spending a charge locks the
  choker until it unlocks during the Discard Cycle of the wearer's next
  full night's rest, at which point the wearer shuffles their discard
  pile into their deck. Destroying it is the only way to remove it
  early. Per the designer: this stops a clever player from using it to
  freely stack the deck for the next adventuring day — "use it or lose
  it."

**Pricing**: `2 × Level` charges, each spending 1 to Sift 3 cards:
`Value = 2 × Level × 3 × 0.90 = 5.4 × Level`. Against the once/day
`Target = Level × 6` (confirmed: this is exactly `Level × 3`
per-encounter × the standing 2-encounters/day assumption, not a
separate constant), **Net = −0.6 × Level** — a clean, consistent 90%
funded at every Level 1-5, not just one sweet spot. `items.csv` (`I151`)
Effects updated, regenerated into `data/items.json`.

### Cloak of One Thousand Feathers = 6.0 — three components, not one blown-up fall-damage number

Level 2, 40 Gold. "Whenever the wearer would fall, instead they glide —
moving 5 meters toward the ground and 5 meters horizontally, as they
choose — ignoring any effects of falling from a height regardless of
distance. This takes no action to do." Structurally different from
Feathered Sandals (`Value = 4.0`, ignores *up to* 10m): this has no cap
at all, and the rulebook's own fall rule has no ceiling either, so a
naive "construct a representative extreme fall and price the full
guaranteed-harm prevention" approach could land almost anywhere
depending on how tall a fall gets picked — tried a 20m case first
(`Net ≈ +16.67` at Level 2), which only showed the question was
underspecified, not that the item was actually that strong.

Per the designer: the big-fall framing has it backwards. Falls large
enough to matter as *damage prevented* are rare and not really the
point; the real benefit is the **opportunity** the item creates — jump
off something as a deliberate way to solve a traversal problem (skip
climbing down, rappelling, or finding a longer route) — plus the
diagonal glide (5m down *and* 5m horizontal, wearer's choice) meaning
the movement isn't wasted the way a straight fall would be. Repriced as
three separate components instead of one number:

- **Base fall-damage prevention**, anchored to the same modest,
  plausible case Feathered Sandals used (not an extreme height, per the
  designer's framing above) — 6m fall, baseline reduction 3:
  `(6−3) × 4 (Health's guaranteed-harm rate) × ⅓ (niche tier) = 4.0`.
- **Uncapped tail-risk bump**: a small premium over Feathered Sandals'
  own 10m cap, since a fall beyond that is unlikely but does still fully
  resolve here where Feathered Sandals wouldn't help at all. Kept
  deliberately modest per the designer's read that this isn't the main
  event: **+1.0**.
- **Movement/traversal utility**: the actual headline benefit — no
  combat-mechanic anchor, so priced at the same Narrative Utility
  niche-convenience rate used elsewhere this pass (Cloak of Caches,
  Diver's Necklace: `⅓ × 3 = 1`): **+1.0**.

`Value = 4.0 + 1.0 + 1.0 = 6.0`. Against `Target = 6` (Level 2), **Net =
0** — confirmed by the designer. No changes to `items.csv` (`I173`) —
Level, Cost, and Effects text were already correct; only the pricing
derivation needed resolving.

### Cloak of Faces — cut, was never meant to be in the main list

Level 5, 100 Gold. "Placed over the face of a recently-deceased
humanoid, after a full round the cloak steals the corpse's face...
after wearing the cloak for a full day, the wearer becomes attuned to
it... for 2 AP, the wearer may raise the hood and replace their face
with any face the cloak has stolen — this actually changes their
features, not an illusion." Per `RULES_DESIGN.md`'s "explicit judgment
calls" note from the original drafting pass: this item was sitting in
the old design doc's "THE BIN" (a rejected-ideas dump), not the main
item list, and only got drafted into `items.csv` by a broad "draft up
entries for all of those items" instruction that didn't distinguish the
bin from the real list — flagged at the time as possibly intentionally
shelved, never resolved either way until now.

Mechanically it would have been a real outlier too: every existing
Masquerade-family effect (Practiced Persona, One of Many Faces, Hat of
Disguise) is a disguise check — Good Luck on it, or an auto-success —
still beatable by an opposed Insight check. This was an unconditional,
undetectable-by-any-check actual transformation, with no real precedent
to price against. Per the designer: bin it — Hat of Disguise is the
right analogue for this design space already, and Cloak of Faces was
"just a fun idea that didn't pan out." Removed from `items.csv`
(`I152`), regenerated into `data/items.json`. Nine items remain in the
Neck slot: Cloak of Caches, Diver's Necklace, Snowfall Drape, Shroud of
Shadowy Stillness, Watcher's Mantle, Shawl of the Land, Choker of
Defiance, Cloak of One Thousand Feathers, and Worry Token — the last of
which is still open (see next).

### Worry Token = suit-keyed Sift, Level 2/4

Originally a GM-secret random table (3 charges/day, "more often than not
nothing happens," otherwise one of six effects — a flat +2 to "the
second flip within 2 hours," a vague social nudge, a confusingly-timed
Defense bonus, plus three usable ones: heal, ignore Physical Resist,
draw a card after 6 hours). Reworked from scratch — the vague/broken
effects had no real anchor, and GM-fiat selection doesn't fit a game
this card-driven.

**Resolution mechanism**: spend 1 charge to Sift 1 card, and the suit
determines the effect — reusing the established `Sift` mechanic
directly (Sift's own 0.60/card value applies to every activation,
regardless of which branch fires) rather than inventing a new reveal
mechanism. Each suit's effect is built from that suit's own established
identity (`RULES_DESIGN.md`'s Suit portfolio table and archetype notes),
not an arbitrary pick:

- **♥ Hearts — heal 1 Shallow Health (4.0).** Hearts' clearest
  "why hand me cards" hook is already healing-scales-with-Hearts
  (confirmed real per the archetype notes); Health only comes in whole
  points, so this is the smallest possible unit, not an attempt to match
  the other three branches' magnitude.
- **♣ Clubs — you are Hasted three times (3.3, 3-stack rate).** Clubs'
  established defensive identity ("Fire Ward, Hasted, Shift"). Bumped
  from an original 1-stack proposal (0.55) to 3 stacks specifically to
  close the gap with Hearts' fixed 4.0, since Hasted (unlike Health) can
  flex to hit a target magnitude.
- **◆ Diamonds — your next two attacks this encounter deal Shadow
  damage instead of their normal type (4.0).** Diamonds' own element is
  Shadow (established suit↔element mapping), so this is the "generic
  elemental conversion" every suit gets for free. Priced off an assumed
  **average 1 point of Physical soak per hit** (the designer's own
  estimate) — bypassing it is worth `1 × 2 (Damage's hit-gated rate,
  Locked) = 2.0/attack`, `× 2 attacks = 4.0`. Scoped to "this encounter"
  (not "this hour") to match the other three branches' combat framing.
- **♠ Spades — draw 2 cards, then discard 2 from your hand (3.32, using
  the new Hand Filtering rate above, linear for 2 cards).** Checked
  against `RULES_DESIGN.md`'s suit archetype notes before finalizing:
  Spades is explicitly "the precise-combatant/**analyst** suit," a
  direct match for calculated hand-filtering — a stronger fit than
  Diamonds' "generalist/skill-monkey" archetype, which was briefly
  considered instead before this check.

**Pricing**: `Value/charge = 0.60 (base Sift, every activation) +
avg(4.0, 3.3, 4.0, 3.32) = 0.60 + 3.655 = 4.255`. Following
`items.csv`'s existing non-contiguous-Level convention (same shape as
Coat of Knit Flesh's `Level: 2, 4`): **3 charges at Level 2** (`Value =
12.77` against `Target = 12`, **Net = +0.77**) and **6 charges at Level
4** (`Value = 25.53` against `Target = 24`, **Net = +1.53**) — both
land at the same ~106%-funded ratio, since charges and Target both
scale directly with Level. `items.csv` (`I211`) updated: Level `2` →
`2, 4`, Cost `40 Gold` → blank/`Value Per Level: 20` (matching the
20-Gold/Level convention), Effects rewritten for the suit-keyed
mechanic. Regenerated into `data/items.json`.

**Later swapped to Ring** (see Fate's Grasp below, priced right after
this) — Worry Token's own math is untouched by the swap, only its Slot
field moved.

**The rule itself changed.** Scaling magnitude per stack (Hasted's
shape) was considered and rejected: Resist reduces damage 1-for-1 per
point with no upper bound, so an unbounded per-stack scale would let a
character with enough Ward stacks become functionally immune to a
damage type for as long as the buff lasts — several existing effects
already grant enough stacks to make that a real risk, and trivializing
a fight built around a specific element is exactly the failure mode to
avoid. Instead, per the designer: **Ward's flat bonus doubles, from +1
to +2 Resist**, keeping the boolean "any stacks → this flat bonus"
shape — stacks still only ever buy *duration*, never a growing wall.
`scripts/glossary.md` and the regenerated `data/*.json` now say +2.

**The value derivation**, now that the magnitude is fixed: unlike
Taunted/Frightened's flat 2.2/turn (a per-flip penalty with no
encounter-timing dependency), Ward's payoff rides on Resist's own
already-derived rate, which is an *encounter-aggregate* built from
Baseline's round-by-round taper (enemies active, and therefore hits
landing, are front-loaded — round 1 sees roughly 9× round 5's hit
volume). Ward decaying 1/turn while covering the *early*, hit-dense
rounds is worth a lot more per stack than the same stack count spent
covering the quiet tail — the opposite shape from Hasted/Slowed's
compounding, and different again from Taunted/Frightened's flat
linear rate. Assuming (same logic as Hasted, a proactive buff on your
own side) it's applied at the start of a fight against a known or
suspected threat, so stack 1 covers round 1, stack 2 extends into
round 2, and so on:

| Stacks (rounds covered) | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Fire — Value | 0.72 | 1.28 | 1.68 | 1.92 | 2.00 |
| Fire — Per-stack | 0.72 | 0.64 | 0.56 | 0.48 | 0.40 |
| Frost/Brilliant/Shadow — Value | 0.36 | 0.64 | 0.84 | 0.96 | 1.00 |
| Frost/Brilliant/Shadow — Per-stack | 0.36 | 0.32 | 0.28 | 0.24 | 0.20 |

(Doubled straight through following the Resist double-discount
correction above — the curve's shape is untouched, only the per-point
rate it's built on changed.) Both cap at exactly `2 × Resist's own
per-point rate` (2.0 Fire, 1.0 others) at 5 stacks — a full Baseline
encounter's worth of coverage,
matching the same realistic-window cap every other keyword in this
bucket uses. Genuinely **diminishing** returns per stack, the third
distinct shape in this whole bucket (alongside Bleeding/Necrotic's
capped taper and Crippled/Vulnerable/Hasted/Slowed's compounding) —
worth stacking up to cover a fight's opening, but each additional
stack buys less than the last, exactly the opposite incentive from the
immunity-risk shape that got rejected.

### Dryad's Mantle = 6.0, follow-up pass — an avoided hit priced the same way as Pillar Ring's protection, at a higher realization rate

Level 2, 40 Gold, Neck. The third and final dice-game Charm
translated this pass (same source as Pillar Ring/Ring of Comets
above) — picked for Neck on mechanical/flavor fit rather than a
Material Type gap, since Precious was already closed out by the other
two.

**Mechanic**, once per encounter for 1 AP: plant a sapling in an
empty space within 10 meters; while within 10 meters of it, Interrupt
an attack that would hit you, for 0 AP, to Shift into its space,
remove it, and the attack misses instead. Reworked from the original
"still take the hit, heal 1 Health after" — per the designer, no heal
at all, which meant the mechanic needed to actually resolve *something*
in exchange, not just lose its only payoff. Landed on the stronger
escape-valve reading (the attack never lands, rather than landing and
then getting patched up) since a Technique-style Interrupt on "would
hit you" naturally sits *before* the triggering action's effects
resolve (`rulebook.md`'s own Interrupt rule), and because a pure
reposition-after-eating-a-hit version would have nothing left to price
at all once the heal was gone.

**Value**: same anchor as Pillar Ring's own protection component — a
fully avoided hit is worth the old balance spreadsheet's descriptive
"Average Health lost per hit: 2.25" × Health's guaranteed-harm rate
(4) = 9.0. Per the designer, this fires in about **⅔ of combat
encounters** — notably more reliable than Pillar Ring's own ⅓ niche
tier, since staying within 10 meters of a sapling you planted yourself
is a much easier bar to clear than the battlefield geometry Pillar
Ring's line-of-sight protection depends on: `9.0 × ⅔ = 6.0`. `Target =
6` (Level 2), **`Net = 0`** — an exact fit, the third of these three
translated Charms to land exactly on Target.

**Base Item Options set to `I002,I003`** (Basic Clothing or Basic
Jewelry), not a bespoke standalone material — per the designer, every
Masterwork item should tie back to a real Base Item, with its own
flavor Main Materials layered on top rather than floating free. This
wasn't a new rule invented for this item: every one of the 10 other
existing Neck items already uses exactly this pattern (`I002,I003`
together), letting the physical form — cloak or necklace — stay the
crafter's choice rather than something the designer pre-decides per
item. This item just hadn't been checked against that existing
convention until the designer raised it explicitly; Main Materials
`Wood` (sapling/nature flavor) sits on top of that base, same as
Shawl of the Land's own Wood or Clarion Cord's own Precious already do.

## Social Encounter Baseline — the combat Baseline's counterpart, built from scratch

Surfaced while trying to price Stoic Collar (below): unlike combat,
which has real numeric anchors throughout (`rulebook.md`'s own worked
examples, `50% avg hit chance`, `1.875 hits/player/encounter`, etc.),
Social Contests — retermed **Social Encounters** going forward, per the
designer's own move away from the old "Contest" framing — had nothing
equivalent. `rulebook.md` deliberately leaves successes-needed and
Pressure's accrual rate to GM judgment, so pricing anything that
touches Pressure meant constructing a representative baseline from
scratch, the same project the old archived spreadsheet's `Baseline` tab
did for combat. Everything below is a new, explicit estimate — not
derived from existing rules text the way combat's numbers were — and
should be revisited if actual play shows it's off.

**Why build this at all, rather than eyeball Pressure item pricing the
way Narrative Utility items get a labeled guess:** Pressure interacts
with itself nonlinearly (Bad Luck stacking, a hard failure threshold,
Support's success chance collapsing as it stacks) in a way that no
flat per-point rate can capture honestly. The first attempt at pricing
Stoic Collar's mechanic using just the already-Locked `Concession/
Pressure = 2.2/point` rate landed on a plausible-looking but untested
number — building the actual round-by-round model is what caught that
it was wrong by a wide margin once checked against real dynamics (see
Stoic Collar's own writeup below).

### The assumptions, and why each one was picked

- **Party composition**: one character built for social checks (+6
  Skill Total) leading Statements, three others Supporting (+4 each).
  Not derived from anything — the designer's own estimate of "a
  reasonably-built party, not a specialist min-max," picked as the
  representative case to price against rather than either extreme.
- **Difficulty 13**, giving the main character success on a card **≥7**
  and Supporters success on **≥9**. **Known discrepancy, flagged rather
  than silently resolved**: `rulebook.md`'s actual Supporting rule uses
  a **flat difficulty of 11** for every Support check, regardless of
  what's being supported — not derived from the specific Statement's
  own difficulty the way this baseline assumes. Under the real rule, a
  +4 Supporter would succeed on **≥7** (`11−4`), meaningfully easier
  than the ≥9 this baseline uses. This baseline keeps the designer's
  own stated numbers as given (a deliberate simplification for this
  exercise), but real play following the literal Supporting rule should
  see Support hold up better than everything below suggests — worth
  reconciling in a future pass, either by adjusting this baseline or by
  reconsidering whether Support really should scale with the specific
  check's difficulty for Social Encounters specifically.
- **5 successes needed**, 1 per successful Statement plus 1 per Extra
  Success (suit-pool match). Per the designer, representing a
  "prolonged, not one-off" Encounter — the kind that actually calls for
  tracking Pressure at all, as opposed to the single-check case
  `rulebook.md` says most social interactions resolve as.
- **Pressure +1 after every round**, applying its Bad Luck to **both**
  the Statement and every Support check made that round. Per the
  designer, this needs its own `rulebook.md` clarification (added
  below) — the current text only says Pressure hits "Statements," and
  a Support check is textually a separate flip, not a Statement itself.
- **Fail at Pressure 5** (checked against fail-at-4 too; 5 fits the
  designer's own described shape — "some parties finish in 2 checks
  with good luck, others drag to 4" — much better, since fail-at-4
  leaves almost no room for a 4-round encounter to still be winnable).
- **All cards drawn from a Good/Bad Luck flip count toward the Suit
  Pool**, not just the one used for the pass/fail result — per the
  designer: "if they have 2x good luck and flip 3 clubs... they'd get 4
  total successes." This is a real interpretation of the existing Extra
  Success rule (`rulebook.md`'s Making an Attack section: "an Extra
  Success for each card in your suit pool matching") that isn't
  currently spelled out for the multi-card Good/Bad Luck case — also
  flagged for a `rulebook.md` clarification, though not yet added
  (affects every Good/Bad Luck check in the game, combat included, so
  it's a bigger, separate change than this pass's scope).
- **Card-spending rescue, assumed available "most of the time."** Per
  the designer, a party is assumed to have a suitable card free for
  their main Statement-maker more often than not. Modeled precisely as
  two cases: **net Good Luck or neutral** (Support successes ≥
  Pressure) — *any* failure is rescuable, since failing there means
  zero of the drawn cards cleared the difficulty, and one more
  (assumed-high) card always fixes that — so this case becomes a
  **guaranteed success** under the assumption. **Net Bad Luck**
  (Pressure > Support successes) — only rescuable if *exactly one*
  drawn card was the spoiler; two or more low cards can't be fixed by
  swapping just one, so this stays probabilistic:
  `P(success) = (7/13)^n + n·(6/13)·(7/13)^(n−1)`, `n` = cards drawn.
  This assumption turned out to be the single biggest lever in the
  whole model — see the isolation check below.

### Methodology: exact combinatorics, not Monte Carlo

Every number below comes from an exact dynamic-program over the
distribution of "successes so far," advancing one round at a time
(convolving in that round's exact successes-gained distribution,
itself computed via closed-form order statistics on the uniform 1-13
deck — `P(max of n ≥ T) = 1-((T-1)/13)^n`, `P(min of n ≥ T) =
((14-T)/13)^n`), rather than sampling. Cross-checked against a
200,000-trial Monte Carlo run of the same rules (before the difficulty
tweak/card-rescue were added) — 8.32% exact vs. 8.3% simulated for the
same configuration, confirming the exact model is correct.

### The locked baseline: 57% win rate

Final configuration (party +6/+4, difficulty 13, 5 successes, Pressure
every round hitting Statement + all 3 Supports, fail at Pressure 5,
card-rescue assumed available):

| Round | Pressure | Support success % | E[successful Supports] | Main flip success % | E[successes this round] | Cumulative win % |
|---|---|---|---|---|---|---|
| 1 | 0 | 38.5% | 1.15 | 100.0% | 1.54 | 0.02% |
| 2 | 1 | 14.8% | 0.44 | 86.8% | 1.22 | 4.36% |
| 3 | 2 | 5.7% | 0.17 | 59.7% | 1.01 | 29.04% |
| 4 | 3 | 2.2% | 0.07 | 38.5% | 0.76 | 47.32% |
| 5 | 4 | 0.8% | 0.03 | 24.3% | 0.54 | **57.03%** (43.0% loss) |

**57.03%** sits where the designer wanted it — "closer to 50% than
75%," within the originally-stated 50-66% target band. Note this was
reached by testing several configurations (successes needed 3/4/5,
Pressure every round vs. every-other-round) before landing here; the
other tested combinations ran from 6.7% (harshest: every round, 5
successes, no card-rescue, support needing 10+) up to 98.7%
(gentlest: Pressure only every other round, full card-rescue) — see
git history for the intermediate passes if any of those numbers are
useful reference points later.

**The isolation check that mattered most**: with the exact same
difficulty tweak but card-rescue turned off, the same configuration
only wins 9.72% of the time — confirming the card-spending assumption,
not the difficulty numbers, is what does most of the work getting this
into a sane range. Any future change to how freely available cards are
assumed to be should expect a large swing in these numbers, not a
minor one.

### Stoic Collar = ~3, priced against the real Social Encounter Baseline instead of the abstract Pressure curve

Level 1, 20 Gold, Neck (`I2XX` — see item entry). Retired from the Head
slot's social-hat consolidation as "Stoic Skullcap," renamed since a
skullcap can't be a Neck item (that name only made sense back when
this was Head). Once per encounter, for 1 AP: ignore 1 Pressure the
party would otherwise apply this round.

**First pass used the abstract stacking-curve math** (`Concession/
Pressure = 2.2`, the multi-stack Good/Bad Luck table from Thrumming
Focus's own derivation) and landed on a plausible-sounding
`Value ≈ 1.3-2.8` depending on the exact wording tried. Once the actual
Social Encounter Baseline existed to check against, this turned out to
be unreliable in both directions:

- An **always-on** "ignore N Pressure every round" version, run through
  the real model, comes out wildly overfunded — `ignore 1` alone lifts
  the baseline's 57.03% win rate to **78.48%** (+21.45pp), pricing out
  at raw Value **~15.76** (weighted by how often each round is actually
  reached, using the same stacking-curve rate across all 4 checks/round
  it touches) — far past what any reasonable Level should carry.
- A **single-use, one-round** version (the one actually shipped) lifts
  the win rate by **+5.99pp** at its best timing (round 2 or 4) — a
  real, modest effect, not nothing, but nowhere near the always-on
  version's power.

**Why the always-on version blew up**: the card-rescue assumption in
the Baseline makes any round with "net Good Luck or neutral" (Support
successes ≥ Pressure) an automatic success. Reducing Pressure doesn't
just soften a linear penalty here — past a certain point it flips
rounds across that guaranteed-success line entirely, which the flat
per-point stacking curve has no way to see. This is the same
spiral-breaking dynamic noted in the Baseline's own card-rescue
isolation check, just showing up again from the item-pricing side.

**Landed on Value ≈ 3** for the single-use version as a considered
judgment call, not a clean formula output: converting the win-rate
delta into raw Value the same way as the always-on case (stacking-curve
harm removed × 4 checks that round) gives inconsistent numbers
depending on which round is assumed (`2.62` at round 4's Pressure
level, `8.78` at round 2's) despite both producing the *same* empirical
win-rate delta in the exact model — a sign the simple per-check-harm
approximation doesn't cleanly capture a one-time rescue's real
value the way it captures the always-on case's per-round tax. Given
that spread, `Value = 3` was picked as a defensible middle ground
rather than over-trusting either endpoint: `Target = 3` (Level 1),
`Net ≈ 0`. Flagged as a labeled judgment call, same as any Narrative
Utility item's own honest-guess convention — revisit if actual play
suggests this reads stronger or weaker than intended.

### Correction: Ward reimagined as flat Resist + a self-limiting absorption charge

Even after the +1→+2 fix above, Ward still read as chronically
underpowered — every existing Resist-granting item (this element's own
Masterwork gear included) came back meaningfully negative against its
own Target. Raising the flat Resist bonus further was already ruled
out (see above: unbounded magnitude risks eventual immunity to a whole
damage type). The fix instead adds a **second, self-limiting**
component rather than a bigger first one: each Ward stack can now also
directly absorb 1 Health loss from that damage type — the exact same
mandatory-substitution rule Protected uses (`glossary.md`'s Protected
entry was tightened to the same "instead" wording this pass, value
unchanged), just restricted to one damage type. This can't
create an immunity risk the way scaling the flat bonus would, since
it's consumed on use, not a permanent multiplier — the same reason
Protected itself was always safe to price at a real rate.

**Pricing the new component**: Protected's own rate is Locked at
3/stack (blocks any Health loss, unconditionally). A type-restricted
version only fires against one damage type — scaled by the same
damage-share logic Resist's own derivation already established:
*within a fight where that element is actually relevant* (the assumed
context for any item built around a known threat), roughly two-thirds
of incoming damage is that element. `(2/3) × 3 ≈ 2.0/stack`, uniform
across all four elements — the Fire-vs-other asymmetry lives entirely
in *whether* a fight becomes elemental-relevant at all (already
resolved to yes by the item's own premise), not in how concentrated
the damage is once it does. This is an **additive approximation**, not
a full joint-probability model — a stack that gets consumed early by
absorbing a hit can no longer also be sitting there extending the flat
Resist bonus's own duration, so treating the two components as
independently additive is mildly generous. Not worth a more exact
model yet given this is a first pass; revisit if it reads too strong
in play.

**Ripple**: this makes Ward's *universal* definition stronger, not
just a special case for one item. First estimated this at "7
Masterwork items, 12 Techniques" — a stale count from an earlier,
imprecise substring search that was actually matching "Resist," not
the Ward keyword itself. Grepping for `\bWard\b` directly found the
real scope is much smaller: only **Warmage's Draft** (fixed in this
same pass — see `balance_ledger.csv`, its own 5-stack Ward grant went
from Net 0.0 to roughly +10 before the trim) and **Spellblade** (`T100`,
a Technique, not priced against this model at all yet) actually grant
Ward. The larger set of items that looked like they should be affected
(Attuned Shroud, Elemental-Resistant Armor, Fortified Armor, Robes of
Resilience, Robes of the Elemental Lord, Charcoal, Elemental Warding
Amulet, Worry Token) grant a flat Resist stat bonus directly, not
Ward — unaffected by this change, and still the separate systemic
issue flagged in `balance.md`'s Open balance work.

Checked against the only two things in the catalog that currently grant
Ward: **Spellblade** (`[3×X]+1+[Hearts]` stacks — 4 to 17 at Level 1
depending on the card flip) massively over-grants relative to the
5-stack realistic ceiling, so most of a typical cast is already wasted
overkill under this model, independent of the rule change — a real
finding for whenever Spellblade itself gets balanced. **Elemental-
Attuned Tincture** grants Ward "that lasts for 1 hour" instead of a
stack count — a full hour comfortably outlasts a single 5-round
encounter, so that item doesn't decay mid-fight the way a normal
stacked grant does; it should just be priced at the flat full-encounter
rate (2.0 Fire / 1.0 others, doubled per the Resist correction above)
with no duration discount, not run through the stacking table above.

### Lifeforce Plate — refill-frequency framing, not a new per-stack rate

Lifeforce Plate (`I072`, Masterwork Torso) doesn't grant Protected
directly — it refills the wearer to 1 stack (Level 3) or tops back up
to 2 stacks (Level 5) whenever they'd otherwise be sitting at 0 or
under. Protected's own per-stack rate (3, Locked) isn't in question
here; the only real unknown is *how often* "the wearer has no/too few
stacks" actually comes up in a real fight — a refill-frequency
question, not a new mechanic to price from scratch.

Two framings were considered:

- **Strict**: reuse Resist's own "1.875 hits/player/encounter" anchor
  (10 enemy-rounds/fight × 1.5 attacks/round ÷ 4 players × 50% hit
  chance) as the refill count, treating every one of those hits as an
  instance where this item's Protected was up and got consumed. This
  collapses to Value = 1.875 × stacks × 3 — L3: 5.625 (Net −3.375), L5:
  11.25 (Net −3.75).
- **Broad** (adopted): Lifeforce Plate's actual trigger ("0 stacks of
  Protected") is looser than Resist's "a guaranteed major hit" —
  it also catches incidental chip damage, not just the big swing that
  anchor was built around. Estimated at ~2.5 "relevant empty moments"
  per encounter instead. Value = 2.5 × stacks × 3 — L3: 7.5 (Net −1.5),
  L5: 15 (Net exactly 0).

Went with the broader read: the item's own wording doesn't gate on
"took a hit," it gates on "currently has 0 stacks," which is a wider
net than 1.875 was ever meant to capture. Landed with L3 still a bit
under Target and L5 an exact fit — both accepted, consistent with the
rest of this Torso cluster's below-budget Masterwork allowance.

### Storage capacity — priced as AP saved on a realistic-use cap, not raw pouch count

First applied to the Belt slot's three Storage items (Sash of Deep
Pockets, Smuggler's Belt, Placeholder's Bottomless Belt) — reusable for
any other Storage-archetype item (7 total in the catalog). `rulebook.md`'s
Retrieving Items rule is the key fact: a belt pouch is already an "easy"
1-AP location, with no stated mundane capacity limit, so a Storage item
isn't saving AP over a normal pouch — it's converting a soft,
GM-adjudicated "sure, you can probably fit that" into a hard mechanical
guarantee. That means raw pouch count (5, 12, or 20 across the three
Belt items) isn't the right thing to price directly: a character rarely
wants more than a handful of consumables in easy reach beyond what a
normal belt already plausibly holds, so pouches past that point buy
headroom against GM pushback, not new mechanical value.

**Model**: cap the "genuinely extra slots used" at **3** regardless of
an item's nominal pouch count, value each at the AP saved retrieving
from it (1 AP, 2.75/point per `1 AP,2.75,...` in `balance_weights.csv`),
realized at the niche/rare trigger frequency (⅓, the new Situational
Multiplier) — a capacity crunch big enough to matter isn't an everyday
occurrence. `Value(capacity) = 3 × 2.75 × ⅓ = 2.75`, the same for every
Storage item regardless of pouch count, unless it has a real qualitative
differentiator worth pricing separately (Sash of Deep Pockets' pouches
fit 1-meter objects, not just small ones — credited 1 more slot at the
same rate, +0.917). A Level difference (Bottomless Belt's L1 vs. the
other two's L2) is the correct way to differentiate otherwise-similar
Storage items, not inflating the capacity component itself.

**Secrecy** (Smuggler's Belt): its "automatically fails to discover"
guarantee modeled as Good Luck-tier (2.4, a near-certain success — not
a modest edge) on a Stealth-adjacent concealment check, at the same ⅓
frequency: `2.4 × ⅓ = 0.8`, additive on top of the capacity component.

All Storage pricing scopes per-encounter (`Target = Level × 3`, `Rate
= 1`), same as everything else in this model, and assumes optimal use
throughout (the owner actually carries useful items in the extra
slots, or has something worth hiding when it matters) — the same
"rational player" convention used for elemental Resist picks elsewhere
in this model. [Corrected from an earlier once/day scoping (`Target =
Level × 4`) — see `balance.md`'s Belt Masterwork pass: capacity's real
value is the everyday convenience of freeing up 1-AP-reach slots every
single fight, not an occasional once-a-day crunch, so it belongs on
the same per-encounter footing as the rest of THE TABEL, not its own
daily window. This paragraph originally went stale after that
correction landed elsewhere and was never updated to match — caught
reviewing the full Storage item family together.]

**Large-object slot rate, now its own row.** The "+1 slot at the same
per-slot rate" mentioned above (Sash of Deep Pockets' 1-meter-object
pouches, Spacious Satchel's full 3-slot credit) is `2.75 / 3 = 0.917`
per slot — previously only stated in this prose, now also given its
own `balance_weights.csv` row ("Storage capacity component
(large-object slot)") since it's been reused across multiple items
without ever being formally tabulated.

### Preserving Larder = 5.0 — a money-saved-from-spoilage anchor, not the capacity model

Level 3, "Other" (no equipment Slot). Reviewed alongside the rest of
the Storage family per the designer's request, and it turned out *not*
to fit the capacity model above at all, rather than just needing its
placeholder Narrative Utility pricing (`Value = 3`, PENCILED IN)
swapped for the real thing. The capacity model's whole basis is AP
saved on retrieval — converting a belt pouch's soft "sure, you can
probably fit that" into a hard guarantee, scoped per-encounter because
that convenience recurs every fight. None of that holds for a bag that
can only ever hold Food: nobody is digging for rations mid-combat, so
there's no AP-retrieval story to price here at all, borrowed from
Spacious Satchel or otherwise.

**Per the designer**, the item's real value is what it saves the party
from *wasting* — food that would otherwise spoil a week after
gathering (`rulebook.md`'s Material Types section) gets preserved
instead, either to actually eat later or, less directly, to not need
to re-gather. That's the same shape as Shawl of the Land's own
"doesn't need to eat" credit (Neck slot, above): a real Gold number run
through the established `Gold = 1.5` conversion (`balance_weights.csv`,
"reciprocal of Baseline's own Value/Gold ratio"), rather than the usual
Narrative Utility fallback.

That needed a real number for "how much food does a kill actually
yield," which `rulebook.md` didn't have at the base-game level — only
a vague "larger kills have many more units, depending on their size"
line, and that line lives in the Goblin Game chapter specifically (its
own concrete anchor, "an adult Goblin has 5 Food worth of meat," is
scoped to that supplement, not Base Game). Generalized the Goblin
anchor into a base-game size table instead of inventing new numbers:
a rodent/fish/bird/insects-sized kill is good for 1 Food, a
person-sized kill for about 5 (reusing the Goblin figure directly),
and a larger beast (boar, elk, bear) for 10 or more. `scripts/
rulebook.md`'s Food bullet updated to match, regenerated into
`data/rulebook.json`.

**The math**: a large-beast kill (10 Food, Level 1 by default — most
mundane game is Level 1 baseline per "higher-quality materials can be
hard to find") is worth 10 Gold nominally (Materials are worth Gold
equal to their own Level) → `10 × 1.5 = 15` raw Value at the Gold
rate. A windfall big enough to actually risk spoiling waste — more
food than the party can eat or otherwise use inside the one-week
clock — isn't an every-fight or even every-day occurrence, so this
takes the standard **⅓ niche tier**, same as Smuggler's Belt's Secrecy
or Shadowdraw's concealment: `15 × ⅓ = 5.0`.

`Value = 5.0`, `Target = 9` (Level 3, unchanged), **`Net = −4.0` (56%
funded)** — lands in the same band as its Storage-family peers
(Spacious Satchel 61%, Sash of Deep Pockets 51%), not forced to fit,
just landing there. `design/balance_ledger.csv`'s `I254` row updated
to match.

**Distant Scroll Cases (`I114`) reviewed alongside this and left
unchanged.** Its own mechanic — two cases sharing a small pocket of
space across arbitrary distance, sized for documents specifically, not
a bag's worth of gear — was never really a capacity item either; it's
a narrow logistics/communication effect, correctly priced via
Narrative Utility already (`Value = ⅓ × 6 = 2`, `Net = −4`, 33%
funded). No change needed.

### Trigger frequency tiers, standardized — and a labeled-guess convention for Narrative Utility items

Surfaced pricing the Hands Masterwork slot, where several items needed
a "how often does this actually trigger" discount with no combat-
frequency anchor to lean on (unlike Resist's own 1.875-hits/encounter
derivation). The ad hoc "~⅓, niche" example used loosely across
earlier passes (Poisons, Dauntless Wrap, Storage capacity, secrecy
checks) is now **three fixed tiers**, per the designer — deliberately
no finer gradations than this:

- **1 (every encounter)** — something used almost every fight (an
  Encounter-style power, or a draw-speed saving that happens each
  combat, e.g. Armory Gauntlets' weapon-conjure). No discount.
- **½ (once/day)** — real, roughly-daily regularity, but not every
  single fight (a Skill Good Luck tied to genuine recurring demand —
  Field Surgeon's Handwraps' Medicine, once the designer pointed out
  several Techniques actually call for Medicine flips; Deft Gloves'
  broadened Craft).
- **⅓ (rarer than daily)** — the old catch-all "niche" bucket:
  Poisons, Dauntless Wrap's Down-threatening hit, Lifeforce Plate's
  "empty moments," a narrow single-use-case Skill bonus (Nimble
  Fingers' steal-specifically), someone actually searching you
  (Smuggler's Belt/Armory Gauntlets' secrecy).

Don't try to calculate a more precise rate for "comes up every other
day" or similar in-between cadences — per the designer, an item that
lands underpowered at the ⅓ tier needs redesigning, not a fancier
discount. That's a deliberate simplicity choice: these frequencies
were never going to be measured precisely anyway, so a small fixed set
beats an ever-growing pile of one-off fractions.

**Narrative Utility items** — a second, separate convention for
effects the model genuinely has no way to price at all (exploration/
puzzle value, not combat): `Value = ⅓ × the item's own Target`.
Explicitly **not** a derived discount the way the frequency tiers are
— it's a flat, labeled guess, formalized only so the whole category
(Placeholder's Grasping Gloves, Gloves of Spatial Distortion) gets one
honest, consistent number instead of a different ad hoc pick per item.
Any item using this convention should say so plainly in its own
pricing note, the same way every other flagged judgment call in this
file gets called out rather than presented as more rigorous than it
is.

## Ring slot — first pass

15 items. Two flagged as possibly mis-tagged before pricing started —
checked against the archive source docs (`archive/flagonquest_site_other.md`):
**Elemental Warding Band** (`I208`, then "Elemental Warding Amulet")
was always `Slot: Ring` in the original doc despite its amulet/pendant
flavor text — not mis-tagged, just oddly named. Renamed and reflavored
to actually describe a ring. **Mendicant's Cord** (`I209`) was
originally `Slot: Waist`, an old slot that doesn't exist anymore — most
likely folded into the modern Belt, but Belt's established design lane
(`RULES_DESIGN.md:129`) is narrowly "carrying items," while Ring's is "a
specific active ability, or an augment to a specific skill/ability" —
a much better fit for Mendicant's Cord's active Defense-shifting effect.
Left on Ring; the stale "sash" fluff still needs a rewrite when that
item comes up.

### Elemental Warding Band = 2.72-5.28 (Fire) / 2.36-4.64 (other) — reused Ward's already-Locked rate directly

Level `1, 2`, `20/40 Gold`. "When this enhancement is created, choose
Fire, Frost, Brilliant, or Shadow. Once per encounter, you may grant 1
stack of Ward of the chosen type (2 stacks if Level 2) to yourself or a
willing creature you touch." Renamed from "Elemental Warding Amulet"
and reflavored to describe an actual ring (see the slot-check note
above) — no mechanical change from that alone.

Quick to price since Ward's rate is already fully Locked from the
Torso pass — no new derivation needed, just look up the table:

| Stacks | Fire (flat Resist + absorption) | Frost/Brilliant/Shadow |
|---|---|---|
| 1 (Level 1) | `0.72 + 2.0 = 2.72` | `0.36 + 2.0 = 2.36` |
| 2 (Level 2) | `1.28 + 4.0 = 5.28` | `0.64 + 4.0 = 4.64` |

Against the standard once/encounter `Target = Level × 3` (Level 1 = 3,
Level 2 = 6): **Net −0.28 Fire / −0.64 other** (Level 1), **Net −0.72
Fire / −1.36 other** (Level 2) — all four cases modestly under budget,
same shape as most other Pencil items in this pass.

**Added "or a willing creature you touch"** per the designer, for
flexibility (buff an ally instead of only yourself) — doesn't change
Ward's own raw value, but carries real option value the same way
Card's premium over Good Luck's floor does (timing/targeting
flexibility). Applied a modest, explicitly-judgment-call **+15%**
bump rather than a derived number: `2.72 × 1.15 ≈ 3.13` (Fire, Level
1), landing almost exactly on Target — a side benefit of the change,
not a target forced backward into the math.

**Considered extending to Level 5** (continuing the existing "stacks =
Level" pattern) — verified this doesn't hold up:

| Level | Stacks | Value (Fire) | Value (other) | Target | Net (Fire) | Net (other) |
|---|---|---|---|---|---|---|
| 3 | 3 | 7.68 | 6.84 | 9 | −1.32 | −2.16 |
| 4 | 4 | 9.92 | 8.96 | 12 | −2.08 | −3.04 |
| 5 | 5 | 12.00 | 11.00 | 15 | −3.00 | −4.00 |

The gap widens every Level rather than staying flat, because Ward's
flat-Resist component has diminishing per-stack returns that cap at 5
stacks, while Target keeps climbing a flat +3/Level regardless — a
structural mismatch, not something a flat bonus could patch. Per the
designer: kept capped at Level 1-2 as originally structured, rather
than stretched to a range that doesn't actually scale. `items.csv`
(`I208`) updated (Name, Fluff, Effects), regenerated into
`data/items.json`.

### Mendicant's Cord = 1.375-4.125 (context-dependent), Level 2 accepted below budget — Good Luck/Bad Luck instead of point-shifting

Level 2, 40 Gold. Originally "As a Move, you may touch yourself or a
willing adjacent creature and shift up to 2 points from one of their
Defenses to another — the raised Defense can't end up higher than the
lowered one's new value." Reworked entirely — moving discrete Defense
points didn't feel good to the designer, and the underlying value
question (is the reallocation actually useful) is the same either way,
so a cleaner mechanic was worth finding rather than pricing the
original as-is.

**New mechanic**: "On your turn, for 0 AP, you may choose either your
Dodge and Parry Defenses or your Vital, Mental, and Instinct Defenses.
Until you do this again, attacks against the chosen group have Bad
Luck, and attacks against the other group have Good Luck." Self-only
(the "or a willing adjacent creature" targeting was cut). The two
groups match Harried's and Vulnerable's own established Defense
pairings exactly (`glossary.md`: Harried hits "Dodge and Parry
Defense," Vulnerable hits "Vital, Mental, and Instinct Defenses") —
reusing an existing split rather than inventing a new one, and
simplifying what was originally going to be a "pick one Defense from
each group" sub-choice down to just picking which whole group gets
hardened.

**Pricing**: Good Luck and Bad Luck are priced identically (`2.2`
each), so protecting one group while weakening the other nets to
`Value = 2.2 × D`, where `D` = the net number of extra hits landing on
the protected group versus the weakened one over the encounter — a
direct consequence of Bad Luck/Good Luck's symmetry, not a new
derivation. Using the established `1.875 hits/player/encounter`
baseline (the same one Resist's own derivation uses) as the ceiling on
total hits, `D` maxes out at 1.875 (every single hit lands on the
protected group) — meaning the absolute best case is `Value = 2.2 ×
1.875 = 4.125`.

That ceiling **cannot reach Level 2's Target (6)** under any
circumstance, not just an unlucky one — a hard structural cap from the
encounter's own combat math, not a judgment call. Realistic cases
range from `≈1.375` (a genuinely mixed encounter, no reliable read,
using Resist's own Physical/elemental damage-share split — 2/3 vs
1/3 — as the read-accuracy proxy) up to close to the `4.125` ceiling
(a well-read, consistently lopsided encounter — a tank correctly
clocking "this room is all melee" and staying toggled that way the
whole fight). Per the designer: accepted at Level 2 anyway, on the
same "identity over hitting the exact number" basis as Acidic
Flask/Reeler earlier in this pass — many real encounters *are*
consistently lopsided rather than an even mix, so the realized value
skews well above the pessimistic blended estimate even though it can
never fully close the gap.

**Reflavored as an actual ring** while keeping the name: mendicant
orders (Franciscans, most notably) are historically defined by a
knotted cord/cincture worn as a vow-symbol, so "Mendicant's Cord" as a
name already has a real anchor independent of which slot it's worn on
— reworked to a ring shaped like a small knotted cord rather than
inventing an unrelated ring concept. The sacrifice-based mechanic
(harden one thing at the cost of another) also fits a mendicant's
core ethos — voluntary sacrifice in one place for protection
elsewhere — better than the original flat point-shift did. `items.csv`
(`I209`) updated: Name kept, Fluff and Effects rewritten, Base Item
Options corrected from `I002` (Basic Clothing, a leftover from the old
"Waist" slot) to `I003` (Basic Jewelry, matching Ring/Neck's
established convention). Regenerated into `data/items.json`.

### Mendicant's Cord, follow-up — the "genuinely mixed encounter" case may not be reachable yet

Checked directly against `design/enemy_sim/`'s real enemy-Action catalog
(not just the pricing math above): none of the five Combat Actions
(`tunables.ACTIONS`) target Bodily or Mental Defense — Defensive Melee/
Offensive Melee/Ranged Weapon all route to Parry/Dodge, Melee Spell/
Ranged Spell route to Dodge. Checked the full catalog in this doc's own
"Combat Actions" section too, not just the simulator's subset — Curse
and the three support actions don't target Bodily/Mental either. So
right now, *every* enemy attack targets the Dodge & Parry group, which
means choosing that group to protect is never a wrong guess — the
"genuinely mixed encounter, no reliable read" case the `1.375` floor
above assumes may not actually be possible under the current Action
catalog, not just uncommon.

Ran the actual card math on it (a generic Level 2 fighter, Accuracy 6,
against a Tier 2 PC's Parry/Dodge of 14): hit chance without Luck is
46.1%, drops to 21.3% with Bad Luck applied (a −24.8 point swing) —
confirming the protection is real and large, just currently guaranteed
rather than a genuine gamble. Not re-pricing off this alone — a future
Combat Action that does target Bodily/Mental (or a PC-facing ability
that does) would restore the intended risk, and the item's accepted
shortfall already leans on real play being lopsided anyway. Worth
revisiting if the Action catalog ever grows a Bodily/Mental option, or
if the gap is judged with intent instead.

### Ring of Charming, Assertive, or Bold Statements — cut, duplicates the Head hats

Level 1, 20 Gold. "Once per encounter, the wearer may gain Good Luck
on a Statement made using Rapport (if Charming), Persuasion (if
Assertive), or Presence (if Bold)." Same shape as Confident Cap/Cap of
Smug Confidence/Sympathetic Hat (Head) — Good Luck on a specific
social Skill, chosen at creation — with no real differentiation beyond
the slot. Per the designer, cut entirely rather than kept alongside an
already-established equivalent family. Removed from `items.csv`
(`I157`), regenerated into `data/items.json`.

### Galeforce Loop = 1 — plain Narrative Utility

Level 1, 20 Gold. Once/encounter flavor gust (snuffs torches, scatters
paper, disperses smoke, untraceable to the wearer) — no combat
mechanic. Same formula as Cloak of Caches/Diver's Necklace/Choker of
Silent Whispers: `Value = ⅓ × 3 = 1`, `Target = 3`, **Net = −2**.
Confirmed as-is, no changes needed.

### Poison Needle = 5.5, moved from Level 3 to Level 1 — same AP-savings shape as Quick Draw Belt

Originally Level 3, 60 Gold. "The wearer can spend a full minute to
place a dose of poison inside the ring, where it can remain
indefinitely. When the wearer declares an attack with a weapon, as an
Interrupt for 0 AP they may apply the poison in the ring to that
weapon." This saves exactly Poison's own application cost (2 AP,
charged once per encounter since a poisoned weapon persists) —
`Value = 2 × 2.75 = 5.5`, the *identical* derivation shape as Quick
Draw Belt (also "saves 2 AP once/encounter," also landing at 5.5).
Quick Draw Belt is Level 2 (Target 6, Net −0.5); at Level 3 (Target 9)
this same 5.5 landed at **Net −3.5**, a much bigger gap for
mechanically the same shape. At **Level 1** (Target 3), **Net = +2.5**
— a real overshoot, but the same ballpark as other accepted Level-1
overshoots this pass (Feathered Sandals +1.0, Immaculate Adhesive
+1.125), and closer to Quick Draw Belt's own per-Level fit than Level
3 ever was.

Checked whether "2 combats/day" changes this (the designer's framing,
assuming the ring gets used once per fight) — it doesn't: `Value = 5.5`
and `Target = Level × 3` are both already scoped per-encounter, the
same convention Quick Draw Belt uses, so the number of combats in a
day doesn't change the per-encounter comparison (multiplying by
combats/day would double-count what the per-encounter convention
already accounts for).

There's a real, unquantified flexibility premium on top that wasn't
folded into the number above: the designer's framing is "hold a more
conditional poison and choose exactly when to apply it" rather than
committing to one poison type blind, well before a fight — the same
"timing/targeting/optionality" shape as Card's premium over Good
Luck's floor. Left unquantified since the base case already clears
Level 1's Target comfortably without it (`+2.5`) — this only makes the
Level-1 placement more generously justified, not something that needed
deriving to clear a bar it was already clearing.

**Poison duration changed from "1 hour" to "until a full night's
rest"** as part of this (`glossary.md`'s `[Poison]` entry) — resolves a
previously-flagged, undecided open question (`RULES_DESIGN.md`: a
Poison applied too early under the old 1-hour window risked expiring
unused before it ever mattered). This specific item is exactly why it
came back up: Poison Needle's whole point is holding a loaded dose
indefinitely and applying it at the perfect reactive moment, which the
1-hour window worked directly against. Also fixed two stale "up to an
hour" references in `balance.md` that predated this change.

`items.csv` (`I085`) updated: Level 3 → 1, Cost 60 → 20 Gold.
Regenerated into `data/items.json`.

### Ring of Pure Elements = 2.0, moved from Level 3 to Level 1 — same conservative estimate as before, just a better-fitting Level

Originally Level 3, 60 Gold. "Once per encounter, when the wearer
makes a damaging spell attack, they may have it deal its damage as
Fire, Frost, Brilliant, or Shadow instead of its normal type." Same
"average 1 point of soak bypassed" assumption used for Worry Token's
Diamonds branch: `Value = 1 × 2 (Damage's hit-gated rate) = 2.0`. At
Level 3 (Target 9) this was a **Net ≈ −7** gap; at **Level 1** (Target
3), **Net = −1.0** — a much closer fit, and still a conservative
estimate, since no premium was added for choosing among all four
elements rather than one fixed type (unquantified upside, same
reasoning as Poison Needle's flexibility premium above — the base case
is close enough to Target without it). `items.csv` (`I158`) updated:
Level 3 → 1, Cost 60 → 20 Gold. Regenerated into `data/items.json`.

### Windrider's Loop = 5.5, bumped from 5m to 10m Range — new Range rate derived, reusing Speed directly

Level 2, 40 Gold. "Once per encounter, when making a weapon attack,
the wearer may increase that weapon's Range by 10 meters" (was 5m). No
existing rate for Range anywhere in this document, so derived fresh —
cleanly, since the real alternative to "attack from X meters farther
away" is "spend a Move action closing that same distance first, then
attack." Extra Range substitutes directly for movement, so it prices
identically to Speed's own single-instance rate (`0.55/meter`, already
used for one-shot movement effects like Push/Difficult Terrain): **Range
(single-instance) = 0.55/meter**, added to `balance_weights.csv`.

At the original 5m: `Value = 5 × 0.55 = 2.75` (exactly 1 AP's own raw
value, which tracks — this effectively saves the Move action you'd
otherwise spend before attacking). Against Level 2's Target (6), **Net
= −3.25**, a big gap in the same "clearly mis-Leveled" shape as Poison
Needle and Ring of Pure Elements.

Unlike Ward, Range has **no diminishing-returns curve** — the rate is
flat per meter with no cap, so a few different fixes were all
genuinely viable (worked through with the designer): stretch it to a
full Level 1-5 range at `5 × Level` meters (a clean ~91-92%-funded fit
at every Level, since both Value and Target stay purely linear); keep
Level 2 fixed and bump to `~11m` once/encounter; or keep 5m but allow
two uses/encounter (`Value = 2 × 2.75 = 5.5`). Per the designer: kept
as a single fixed Level 2 item, bumped to **10m** once/encounter —
`Value = 10 × 0.55 = 5.5`, **Net = −0.5**, a clean fit, same number the
"twice per encounter at 5m" option would have landed on, just via a
simpler single-larger-bonus mechanic instead.

One thing deliberately left unquantified: extra Range is sometimes
worth *more* than the movement it substitutes for, specifically when
moving isn't an option at all (surrounded, restrained, shooting across
a genuine gap). Real situational upside, same shape as Cloak of One
Thousand Feathers' unquantified traversal bonus — not folded in since
the base case already lands close to Target without it. `items.csv`
(`I187`) updated (5m → 10m). Regenerated into `data/items.json`.

### Bloodshard Ring — cut, no clean usage cap to price against

Level 2, 40 Gold. "Before making a spell attack that deals damage, the
wearer may spend X Health. If they do, the spell attack deals its
damage as Fire, and deals an extra X damage. If the spell attack only
has one target, then instead it deals an extra [twice X] damage."
Worked through in detail — the raw Health-for-damage trade turns out
close to a wash rather than a trap once AoE is correctly modeled as
applying the bonus *per target hit*: `Net = 2X(N−2)` for N targets,
break-even at 1-2 targets, genuinely profitable at 3+. The flat "deals
its damage as Fire" conversion adds a consistent `~2.0` on top (same
"1 point of average soak bypassed" logic as Ring of Pure Elements),
independent of target count.

Cut rather than priced, though — the text has no stated usage cap at
all ("before making a spell attack" reads as usable on every qualifying
attack), which makes it impossible to price cleanly without a realistic
per-encounter usage-frequency assumption the model has no way to
supply on its own. Per the designer, moved to `IDEAS_BACKLOG.md` as a
Technique idea instead, where a usage cap can be designed in from the
start rather than left open-ended. Removed from `items.csv` (`I081`),
regenerated into `data/items.json`.

### Tactician's Band = charges × 1.66, pinned to Level 2/4 at 7/14 charges — direct reuse of Hand Filtering

Originally Level 1-5, "`[five times Level]` charges per day, each:
expend a charge, discard a card from your hand, and draw a card." This
mechanic *is* the Hand Filtering primitive verbatim — no new derivation
needed, just apply the already-codified rate (`1.66/card`) directly.
Since the charge pool is a fixed daily allotment (not an ambiguous
realistic-usage-frequency question the way Sift's own rate needed
rescoping for), the total Value is just `charges × 1.66`, compared
against the once/day Target convention (`Level × 6`).

At the original `5 × Level` charges, `Value = 8.3 × Level` against
`Target = 6 × Level` — **Net = +2.3 × Level**, a consistent 138%-funded
overshoot at every Level, not a rounding-level gap. Per the designer,
pinned to a non-contiguous Level `2, 4` (`items.csv`'s existing
convention, same shape as Coat of Knit Flesh/Elemental Warding Band) —
but pinning the Level alone doesn't fix the ratio, since `Value` and
`Target` both scale identically with Level regardless of which ones are
offered. Landed on **7 charges (Level 2) / 14 charges (Level 4)**
instead (not `4×Level`'s 8/16, a close-but-not-quite fit): `7 × 1.66 =
11.62` against `Target = 12` (**Net = −0.38**), `14 × 1.66 = 23.24`
against `Target = 24` (**Net = −0.76**) — ~97% funded at both, the
closest fit found for this item. `items.csv` (`I080`) updated: Level
`1-5` → `2, 4`, Effects reworded to the fixed 7/14 charge counts
(matching Coat of Knit Flesh's "X (if Level N) or Y (if Level M)"
phrasing). Regenerated into `data/items.json`.

### Flamebinder's Promise = 1.5 — priced as a portable Level 1 War Magic, not the generic fresh-attack model's own guessed baseline

Level 1, 20 Gold. "Once per encounter, for 2 AP, the wearer may throw a
ball of fire at a nearby creature. This is an Acrobatics attack against
the Dodge Defense of a target within 5 meters, dealing 3 + [Mind] Fire
damage." A standalone, once/encounter, from-scratch attack — exactly
the shape the **"Pricing a fresh attack from scratch"** model above was
built for (Resist placeholder, priced at Damage's rate; a flat
Universal Harried credit; Autoswing subtracted as the opportunity cost
of spending the 2 AP on this instead of a normal attack).

The one real snag: the damage scales off the wearer's own **Mind**, and
no baseline Mind value has ever been established in this document —
`balance.md`'s own War Magic reference explicitly flags "no Baseline
Stat convention exists" for Mind, using illustrative 3/4/5 values tied
to *War Magic's own Level* (a Buildable Technique), which doesn't map
directly onto a fixed-Level item. **Per the designer, resolved by
treating this ring as a portable Level 1 equivalent of War Magic
(`T120`) itself** — War Magic is this project's own established
"what does a spellcaster's attack actually look like" reference point,
so reusing its own baseline directly is more grounded than constructing
a fresh Mind assumption from nothing. War Magic is itself an
Encounter-tagged Technique (2 AP, once/encounter) with the same base
line, "2 + [your Mind] Fire damage" against Dodge or Vital Defense,
melee range only ("An adjacent creature") — confirming the same
once/encounter, 2-AP cadence this ring already uses, just delivered via
Acrobatics instead of Sorcery Spell and with a fixed range instead of
melee-only. Mind **3** (the lowest value War Magic's own reference
table tabulates, at "Level 2") is used as the representative baseline —
the closest already-established anchor, not a fresh guess, though still
flagged as a judgment call rather than a firm fact, being the first
item this document has ever priced with a Mind-scaling formula.

- Raw Damage = 3 + 3 (Mind) = 6 Fire.
- Resist placeholder (elemental, skips the armor term) = 3 → `margin =
  6 − 3 = 3`, priced at Damage's own rate (2/point): **6**.
- Universal Harried credit (attack vs. Dodge Defense) = **+1**.
- Autoswing subtracted as the flat opportunity cost = **−5.5**.

`Value = 6 + 1 − 5.5 = 1.5`. `Target = 3` (Level 1). **Net = −1.5** — a
modest, accepted shortfall, the same shape as several other items this
pass that land close-but-under Target rather than needing a Level or
magnitude change.

**Range bumped from 5m to 6m**, per the designer, purely for flavor —
checked against the range breakpoints table (`balance_weights_notes.md`
above) and confirmed inconsequential either way: both 5m and 6m sit
well inside the "Short" tier's own 1-move-closable range, nowhere near
the 9m "still attacks" ceiling or the 10m "costs the attack" floor, so
the bump crosses no breakpoint and carries no separate Value credit
under this model (a fresh-attack effect's inherent Range isn't
separately priced the way Windrider's Loop's Range *rider* on an
existing weapon was). `items.csv` (`I078`) updated (5m → 6m).
Regenerated into `data/items.json`.

### Flamebinder's Promise, follow-up — the Resist placeholder (3) was a Bruiser-shaped guess, not a generic one

Checked against `design/enemy_sim/`'s Level 1 enemy model, built two
ways: a neutral fighter (no Role, no Defense-tier pick) and a
Bruiser-Role "power-attack" one. The Bruiser's ElemRes comes out to
**3** — matching this item's own placeholder almost exactly — but the
neutral fighter's ElemRes is only **1**, since Resist is small enough
at Level 1 that a single Role-derived point swings it by a lot in
relative terms:

| | Enemy ElemRes | Value | Net |
|---|---|---|---|
| Neutral fighter | 1 | 5.5 | +2.5 (183% funded) |
| Bruiser (power-attack) fighter | 3 | 1.5 | −1.5 (50% funded, matches the derivation above) |

So the original `3` wasn't a bad guess — it happens to land right on
the Bruiser case — but it isn't the generic one either, and this item's
Value swings harder on that choice than most (Ring of Comets, checked
the same way, only moved from 104% to 89% funded across the same two
builds — a linear-margin formula like this one doesn't get the same
cushioning a step-function one like Pillar Ring's "hits to destroy"
does). Not re-pricing off this alone — flagged here since it's a real
example of how much a pricing placeholder can move once a concrete
enemy model exists to check it against, worth keeping in mind for any
other item whose derivation leans on a guessed Resist value.

### Fate's Grasp = Sift, keyed to a daily card-spend total derived from the Cycles rule — moved to Neck, Level 4

Originally Level 2, 40 Gold, no Fluff written yet. "Whenever you discard
or play cards from your hand, after that effect is resolved, you may
Sift up to that many cards." No charge cap at all — fires every single
time a card leaves the hand via discard or play, for the rest of the
game.

**Why this isn't just a reuse of Sift's existing 0.60/card rate applied
blind.** That rate is explicitly calibrated to a once-per-day window
(~18 draws/adventuring-day); a Technique or item granting Sift on a
*different* trigger needs the same simulation re-run for its own actual
window, not a reused constant (see "What's still open" above — this is
exactly the case it flagged). Two questions had to be answered fresh:
how many cards actually get discarded/played from hand per day, and
whether 0.60/card is even the right rate to apply to each one.

**The daily card-spend total is derivable exactly, not guessed.** The
Draw Cycle gives `2 × (Cunning + Mind)` cards each day (`rulebook.md`'s
Cycles rule) — **12** at the "baseline stat = 3" convention already
used throughout this pass (Body, Agility, and now Cunning/Mind). The
Discard Cycle then unconditionally discards *whatever's left* in hand
before the next day's draw. Because of that, every card that enters
hand over a full day-night cycle also *leaves* it before the cycle
repeats — played, discarded as some ability's cost, or swept by the
Discard Cycle itself — with nothing carrying over. So "cards discarded
or played from hand per day" isn't a rough estimate, it's mechanically
**exactly equal to** the Draw Cycle's own daily income: 12/day at
baseline. (Flips themselves don't touch this count at all — a flip
draws straight off the top of the deck, per `rulebook.md`'s Skill
Checks section; "hand" cards are a wholly separate resource, fed only
by the Draw Cycle and whatever else explicitly draws to hand.)

**0.60/card is still the right rate**, despite the different trigger —
the discount is about how many future flips remain in the day for a
Sift's bias to pay off, not about what causes the Sift to fire. Since
Fate's Grasp's triggers land at roughly typical points across a normal
day (not bunched at the very end where few flips remain to benefit),
the same daily-cadence rate applies.

`Value = 12 × 0.60 = 7.2` at the original 1:1 ("Sift up to that many
cards"). Against the once/day `Target = Level × 6`: **Net = −4.8** at
the original Level 2 (`Target = 12`, 60% funded) — a real shortfall,
not a rounding one.

**Explored scaling the multiplier up instead of just dropping the
Level**, checking every clean integer multiplier ("twice," "three
times," "four times" the cards spent) against Levels 1-5:

| Multiplier | Value | Best-fitting Level | Net | % funded |
|---|---|---|---|---|
| ×1 (original) | 7.2 | L1 (`Target` 6) | +1.2 | 120% |
| ×2 ("twice") | 14.4 | L2 (`Target` 12) | +2.4 | 120% |
| ×3 ("three times") | 21.6 | **L4 (`Target` 24)** | **−2.4** | **90%** |
| ×4 ("four times") | 28.8 | L5 (`Target` 30) | −1.2 | 96% |

Whenever the multiplier equals the Level, the ratio is always the same
120% — not a new fit, just the same one repeating, since Value and
Target both scale by that shared number. The one genuine standout among
clean multipliers is **×3 at Level 4: 90% funded**, tighter than any
Level 2 or Level 3 pairing available — in the same close-but-under
range as Surestride Boots (−0.75) and Windrider's Loop (−0.5). Per the
designer: **locked in at Level 4, "Sift up to three times that many
cards."** `Value = 21.6`, `Target = 24`, **Net = −2.4**.

**Moved from Ring to Neck**, swapped with Worry Token (above) — checked
directly against `RULES_DESIGN.md`'s own slot table (Neck: "niche,
boring, passive utility — deliberately not interactive"; Ring: "a
specific active ability, or an augment to a specific skill/ability").
Fate's Grasp has no charges, no timing decision, no AP cost — it just
fires automatically off whatever the wearer is already doing, the
textbook Neck case. Worry Token is a deliberate charge-spend with a
real "use it now or save it" decision each time, the textbook Ring
case. `items.csv` (`I082`) updated: Slot `Ring` → `Neck`, Level `2` →
`4`, Cost `40 Gold` → `80 Gold` (Level × 20, matching this pass's flat
Masterwork convention), Effects reworded for the ×3 multiplier.
`items.csv` (`I211` Worry Token) updated: Slot `Neck` → `Ring` only —
its own Value/Target/Net derivation above is untouched by the swap.
Both regenerated into `data/items.json`.

**"Thrice" retired project-wide, replaced with "three times."** Swept
while writing this item's own effects text — per the designer, "thrice"
reads as an archaic outlier once the counting sequence goes past
"twice" and starts needing "four times"/"five times" anyway, where
"twice" itself has no plainer two-word alternative competing with it.
Every existing "thrice" across `items.csv` (Dauntless Wrap, Worry
Token's Clubs branch), `techniques.csv` (Solemn Perseverance, Strength
from the Slain), `features.csv` (Wild Magic), and `rulebook.md`
(Experience cost, the Carrick Gambling example) was swept to "three
times" in this same pass, so there's no lingering mixed usage. No
mechanical changes from any of these — wording only. `CLAUDE.md`'s own
documented convention updated to match.

### Heartbinding Band = 12 (recycled overheal, not rate-arbitrage) — Level 3

Originally Level 2, 40 Gold. "The wearer may spend 1 AP, place their
hand (the one with the ring) on an adjacent willing creature, and
spend any amount of Health. That creature then heals that much
Health." Two real problems surfaced before landing on a final number.

**A genuine Shallow/Deep rate arbitrage existed in the original
wording.** `rulebook.md`'s healing rule lets the recipient freely
choose Shallow or Deep for any healing received "unless the effect
specifies one type" — and Healing Deep (5/point, Locked) is worth more
than Healing Shallow (4/point, Locked), while spending Health as a
flat cost prices at the plain guaranteed rate (4/point, the same basis
Bloodshard Ring's Health cost used). A rational pair could pay from
Shallow and receive as Deep, generating `+1/point` out of the rate
mismatch alone, before any tactical value. **Closed by specifying the
type**: `items.csv` now reads "...heals that much **Shallow** Health,"
which the recipient no longer gets to override.

**With the arbitrage closed, a single in-combat activation is a
guaranteed raw loss, and that's intentional.** Healing Shallow (4) and
the flat Health-spend cost (4) cancel exactly, leaving only the 1 AP
cost (2.75, same opportunity-cost basis Wizardly Hat's first-pass "2 AP
to drink" version used) as pure debit: `Value = 4 − 4 − 2.75 = −2.75`
per activation, regardless of how much Health is moved in one action
(the AP cost is flat per activation, not per point). Per the designer:
**kept deliberately** as a combat-use penalty — this ring isn't meant
to be spammed mid-fight, the AP cost is the friction that enforces
that.

**The real value comes from a different mechanism: recycling
otherwise-wasted overheal, not the Shallow/Deep rate mismatch.**
Outside combat, AP isn't a binding resource (per this document's
existing "AP doesn't exist outside combat" precedent), so the 1 AP
cost stops mattering. A character already sitting at full Health gets
nothing from their own Recovery Cycle heal (`Heal = Body`, capped at
max Health) — that healing is simply wasted every day it happens to a
capped-out character. This ring lets the party redirect that
would-be-wasted heal to whoever actually needs it instead, converting
healing that would otherwise vanish into real Value the party wouldn't
have had. Using the Recovery Cycle's own formula directly (`Body`,
baseline 3) as the recycled amount: `Value = 3 × 4 (Healing Shallow,
Locked) = 12` — an exact fit against Level 2's once/day `Target = 12`
(`Net = 0`), not a coincidence, since both numbers come straight from
already-established rates/formulas rather than being tuned to match.

**Per the designer, bumped to Level 3 anyway** (`Target = 18`, `Net =
−6`, 67% funded) as a deliberate margin against a clever party pushing
past the single-donor baseline this estimate assumes (more than one
capped-out donor, more than one beaten-up recipient, in the same day)
— explicitly accepted as "a rulebreaking type of item," priced with
real headroom rather than right at the exact-fit line. `items.csv`
(`I084`) updated: Level `2` → `3`, Cost `40 Gold` → `60 Gold` (Level ×
20, matching this pass's flat Masterwork convention), Effects reworded
to specify Shallow Health. Regenerated into `data/items.json`.

### Flamefist's Approach — cut, pulled to the backlog as a Form Technique instead

Level 4, 80 Gold. Two powers (Brawl hit grants a free ≤2 AP Sorcery
Spell cast; Sorcery hit within `[Meditation Skill Total]` meters grants
a free Teleport-to-adjacent), each once/encounter, both uncappable by
discarding a card. Broken into components before pricing started —
Power 1 as a conditionally-hit-gated Autoswing (`5.5 × 0.5` for the
triggering Brawl attack's own hit chance, on top of whatever's already
baked into Autoswing's 5.5), Power 2 as an attack-enabler in the same
family as Slipstream Sandals/Windrider's Loop (the `[Meditation Skill
Total]` term turned out to just be the *range gate* for triggering,
not the teleport distance itself — the destination is always
"adjacent," so this isn't an unanchored-Skill-Total problem the way
Flamebinder's Promise's Mind scaling was), plus the discard-a-card
escape valve priced as its own component (a card's own value, 2.7,
spent to unlock an extra use).

Per the designer: cut before finishing the derivation — the whole
Brawl-hit-enables-Spell / Spell-hit-enables-Brawl-closing interplay
reads as a more natural fit for a **`[Form]` Technique** (a stance
entered/left at the start of a turn, per `glossary.md`) than a passive
Ring — the concept is "a martial-arts/spellcasting hybrid combat
style," which a Form's own toggled, turn-scoped nature suits better
than an always-on item ever could. Moved to `IDEAS_BACKLOG.md` rather
than priced, same call as Bloodshard Ring earlier in this slot.
Removed from `items.csv` (`I086`), regenerated into `data/items.json`.

### Luminous Signet = 11.0, confirmed at Level 4 — same trigger as Fate's Grasp, a genuinely different derivation

Level 4, 80 Gold. "Whenever you discard or play cards from your hand,
all allies in Burst 5 of you are each Hasted [cards discarded/played]
times." Same unconditional, uncapped discard/play trigger as Fate's
Grasp, but not the same math — three real differences kept this from
being a copy of that derivation:

- **Timing matters here, unlike for Fate's Grasp.** Sift's bias pays
  off no matter when it's granted; Hasted decays over roughly a 4-turn
  window, so a stack granted outside combat is essentially wasted
  before the next fight starts. Fate's Grasp's `12/day` (from the Draw
  Cycle's daily income) isn't the right volume here — this needed a
  per-*encounter* estimate of in-combat card-spend specifically, not a
  daily aggregate.
- **Hasted's curve is convex** (`balance_weights.csv`: `0.55/stack`
  base, rising toward `~2.2/stack`, unbounded), so trigger *size*
  matters, not just total cards spent — three separate 1-card triggers
  deliver less than one 3-card trigger, even though both are "3 stacks
  total."
- **This is AoE**, needing the same kind of realistic-count assumption
  Grenade AoE uses (settled on 2 enemies hit, not the theoretical max).

Per the designer: **2 allies** affected (not the wearer), and **4
cards** discarded/played in a representative encounter — checked
against both ends of an initially-floated 3-4 range:

| Cards/trigger | Hasted value/ally (table above) | × 2 allies | vs. L4 `Target = 12` |
|---|---|---|---|
| 3 | 3.3 | 6.6 | Net −5.4 (55% funded) |
| 4 | 5.5 | 11.0 | **Net −1.0 (92% funded)** |

The convex curve makes the two ends of that range land very
differently — going from 3 to 4 cards jumps 55%→92% funded, not a
proportional bump, purely because Hasted's per-stack rate itself rises
at higher stack counts. **Confirmed at Level 4** rather than dropped to
fit the 3-card case at Level 3 — per the designer, deliberately keeping
this Level (and its correspondingly higher `Target`) rather than a
lower one, since the trigger itself is uncapped and a clever party
pushing trigger sizes past the 4-card baseline (playing several cards
at once for a bigger single application) is exactly the kind of
escalation a lower Level's smaller `Target` buffer would handle worse.
`Value = 11.0`, `Target = 12` (Level 4 × 3, the standard per-encounter
convention, not once/day — this is a combat-only effect, unlike Fate's
Grasp's daily one). **Net = −1.0.** No changes to `items.csv` — Level,
Cost, and Effects text were already correct; only the pricing
derivation needed resolving.

### Focusing Band of [Technique] = 6L − 2.7, flat Net −2.7 at every Level — closes out the Ring slot

Level 1-5, 20 Gold/Level. "When this ring is created, the creator
chooses a Technique they know, which must be the same Level as this
ring. The wearer may discard a card at any time in order to 'learn'
the chosen Technique until they get a full night's rest or take the
ring off. During this time they are treated as though they know the
Technique, or an extra copy of it if it's an Encounter or Duplicate
Technique." Unlike every other item this pass, its value depends
entirely on *which* Technique gets bound to it — a genuinely different
pricing problem, needing a real anchor for "what is a Technique worth"
rather than a mechanical derivation of its own.

**The anchor, formalized per the designer**: a Level-N Technique is
worth the same `Level × 3` a same-Level item's own per-encounter
`Target` represents (first used informally for Wizardly Hat of Tam the
Tipsy's Alcohol/technique-refresh accounting, now codified in
`balance_weights.csv` as **Technique value (Encounter cadence) = 3/
Level**) — and a Technique designed to deliver its value once per day
rather than refreshing per-encounter is worth **twice** that, `6/
Level` (**Technique value (daily cadence)**), matching the once/day
item-Target convention's own `Level × 3 × 2 encounters/day` logic
exactly.

**Both cadences land on the same number here, for a structural
reason**: this ring only activates once per day (discard a card,
persists until the next rest or removing the ring — re-discarding
while already active does nothing new). If bound to an *Encounter*
Technique, the wearer gets to use it once per encounter, every
encounter, for the rest of that day — `Level × 3` per encounter × ~2
encounters/day (Baseline's own standing assumption) = `Level × 6`
total daily value. If bound to a Technique with genuine daily cadence,
it's already worth `Level × 6` on its own by the convention above. So
whichever type of Technique the ring is bound to, its total daily
value comes out to the same `Level × 6` — which is exactly the once/day
`Target = Level × 6` convention this item should be checked against.

**Per the designer: the card-discard activation cost is the entire
intended balancing lever here** — "the thing that makes it not just a
way to buy abilities is the card cost to use the item." With the
Technique's own value and the item's Target cancelling out by
construction (both `Level × 6`), the whole derivation collapses to just
that one cost: `Value = 6L − 2.7` (2.7, the established Card
drawn/hand rate) against `Target = 6L`, giving a **flat Net = −2.7 at
every Level 1-5** — not a shortfall that grows or shrinks with Level,
just the deliberate, constant activation friction the designer
intended.

| Level | Value | Target | Net |
|---|---|---|---|
| 1 | 3.3 | 6 | −2.7 |
| 2 | 9.3 | 12 | −2.7 |
| 3 | 15.3 | 18 | −2.7 |
| 4 | 21.3 | 24 | −2.7 |
| 5 | 27.3 | 30 | −2.7 |

**One real rules gap fixed while pricing this**: the original text
never addressed what happens for a Technique with its own internal
choices (a Buildable technique's Feature picks, or a Free Text option
like a chosen School/Profession) — a real ambiguity, since a smartly-
built copy of a Buildable Technique is worth far more than a generic
one, and the model's own flat `Level × 3`/`Level × 6` anchor implicitly
assumes one specific, already-realized version of the Technique, not
an open choice the wearer gets to make fresh. Per the designer,
resolved: the ring is bound to match a *specific copy* of the Technique
the creator already knows, its choices locked in at creation, not left
open for the wearer to pick their own. `items.csv` (`I079`) updated to
add this clarifying sentence. Regenerated into `data/items.json`.

**Ring slot closed out.** Final roster: Elemental Warding Band,
Mendicant's Cord, Galeforce Loop, Poison Needle, Ring of Pure Elements,
Windrider's Loop, Tactician's Band, Flamebinder's Promise, Heartbinding
Band, Luminous Signet, Focusing Band of [Technique], and Worry Token
(swapped in from Neck) — 12 live items, 3 cut (Ring of Charming/
Assertive/Bold Statements, Bloodshard Ring, Flamefist's Approach), 1
moved out (Fate's Grasp, swapped to Neck).

### Pillar Ring = 6.0, follow-up pass — the Ring slot's first Precious item, and a new value model for terrain control

Level 2, 40 Gold, Precious. Closes a real gap noted during the Precious
Material Type review: 13 Ring items existed spanning Levels 1-5, and
not one used Precious as a Main Material. Translated from "Pillar
Talisman," one of the Charms in a separate dice-based tabletop game's
item list handed over as inspiration (`IDEAS_BACKLOG.md`'s "Source
material to mine: the dice game's item list" section) — the original
placed a wall-like obstacle with no Health, destructibility, or combat
stats at all, just a placement restriction (adjacent to at most one
existing wall) as its only balancing lever.

**Mechanic**, once per encounter for 1 AP: conjure a person-sized
pillar of magical force in an unoccupied space within 10 meters,
blocking sight and attacks through it like a wall — mechanically
**Total Cover** (`rulebook.md`'s Cover and Obscurement section: "makes
attacks against Dodge or Parry, as well as flips to see you,
impossible"), the first item in the catalog to grant it directly
rather than relying on terrain the GM places. Per the designer, the
adjacent-to-a-wall restriction was dropped once the pillar became
destructible instead — a real HP pool is a better anti-abuse lever
than a placement rule, and it opens up the item's use anywhere instead
of only near existing terrain.

**Toughness**, borrowed directly from Wall of Ice's (`T126`)
Health/Resist/destruction structure (`4 Health, [Mind] Resist... When
a space loses all Health, that section is destroyed`), scaled down to
a single segment since this is an accessory's once-per-encounter
effect, not a multi-segment Spell: **4 Health, Resist = 2 + Level**,
flat. No enemy-stat-block table exists in this project yet to gauge
"what would an on-level attacker's hit look like" against (checked —
searched all 15 tabs of `archive/flagonquest_balance_notes.xlsx`, the
designer's own balance notes, nothing there either); used the closest
real precedent instead, the Equipment tab's own note that "Grenades
assume a base stat of 3-5, based on Level: 1-2 assume 3, 3 assumed 4,
4-5 assumes 5" as the on-level-enemy Body proxy, checked against a
Heavy One-Handed Melee Weapon's `4 + [Body]` damage:

| Level | Enemy Body (grenade convention) | Attack dmg | Resist (2+L) | Net/hit | Hits to destroy |
|---|---|---|---|---|---|
| 1 | 3 | 7 | 3 | 4 | 1 (too fragile) |
| 2 | 3 | 7 | 4 | 3 | 2 |
| 3 | 4 | 8 | 5 | 3 | 2 |
| 4 | 5 | 9 | 6 | 3 | 2 |
| 5 | 5 | 9 | 7 | 2 | 2 |

Levels 2-5 land exactly on the designer's own target ("an average
enemy should take two attacks to clear it") with no further tuning;
Level 1 breaks the pattern (one-shot), so the item is fixed at Level 2
rather than spanning the usual 1-5 range. (An earlier draft of this
formula — Resist capped at 9 — hit the exact ceiling of a maxed Heavy
1H's damage, 4+5=9, making the pillar *literally* unbreakable by
Levels 4-5; caught by checking the worst case explicitly rather than
trusting the formula's shape, and fixed by lowering the growth rate
before landing on the cleaner 2+Level version above.) The pillar also
has a flat **8 Parry and Dodge Defense** against attacks made to
destroy it — not a new number, just `rulebook.md`'s own baseline for a
target applying no Defense ("Making an Attack": *"The target may
choose not \[or be unable\] to apply any Defenses against an attack,
in which case it is considered to be 8"*) restated explicitly on the
card, since a stationary pillar obviously isn't dodging — so hitting
it is close to guaranteed, and the real question is whether an attacker
commits the 2 attacks (or a Gamble) it takes to actually bring it down.

**Value**, per the designer's own framing (confirmed over forcing a
detour): the pillar's real job is blocking line of sight to protect an
ally, not just making enemies walk the long way around — though a
chokepoint can make that detour cost real AP too, as upside, not the
primary case being priced. Modeled as blocking **~2 attacks' worth of
harm** before it stops mattering (destroyed, the ally repositions, or
the fight moves on) — symmetric with the 2-hits-to-destroy figure
above, since either the enemy spends ~2 attacks breaking through, or
the cover denies them ~2 attacks' worth of offense instead. Each fully
blocked hit is valued at the old balance spreadsheet's own descriptive
(not double-discounted, unlike the archived "character attack value"
figure which bakes hit-chance in twice) "Average Health lost per hit:
2.25" × Health's guaranteed-harm rate (4) = 9.0/hit; two of those =
18.0 uncapped. That's the "if it always lands perfectly" number, far
too high to take at face value — real use depends on there being
actual terrain to exploit, the ally choosing to stand behind it, and
the attack being a Dodge/Parry one specifically (spell attacks against
Vital/Mental/Vigilant see straight through cover per the rulebook, per
its own text). Standard **⅓ niche tier**, same as Secrecy/Concealment:
`18.0 × ⅓ = 6.0`.

`Value = 6.0`, `Target = 6` (Level 2), **`Net = 0`** — an exact fit,
and landing on the same Level the designer's own gut-feel called for
independently of the math ("this is going to be about a level 2 or 3
ring... it will inconvenience people a little bit if they try to break
it").

### Ring of Comets = 9.33, follow-up pass — a War Magic build priced as a guaranteed hit, not an attack roll

Level 3, 60 Gold, Precious — the second of the dice-game Charms (same
source as Pillar Ring above), and the other half of the Ring slot's
Precious gap fix (L2 Pillar Ring, L3 this). Reflavored per the
designer from a literal falling comet to a gathering blast of magic —
the name stays (poetic enough on its own), but the Effects text no
longer describes an actual sky object.

**Mechanic**, once per encounter for 1 AP: choose a point within 10
meters, and at the start of your next turn it detonates, dealing flat
damage to anyone still standing in that space — no attack roll at all.
Per the designer: "hand wave the range and to hit... in exchange for
it taking a round to set up." Built directly off War Magic's (`T120`)
own base ("2 + [your Mind] Fire damage") with its full Feature Budget
dumped into Destructive (`F062`, Basic, 1 point = +1 damage, repeatable)
— at Level 3 that's 4 points, +4 damage — plus the already-established
+1 bonus for locking the damage type to Physical instead of leaving it
open. Per the designer's latest steer, the `[Mind]` term was dropped
entirely in favor of **baking in a flat stat** rather than scaling with
the wearer's own investment: `2 (base) + 4 (Level 3 budget) + 1
(Physical lock) + 4 (baked-in stat) = 11 Physical damage`. 4 was chosen
over 3 specifically because it lands closer to Target (see below) — not
an arbitrary pick.

**Two real corrections mid-derivation**, both caught by taking "hand
wave... to hit" at its literal word rather than treating it as still a
normal attack roll underneath:

1. **Damage rate.** A first pass used the standard hit-chance-
   discounted rate (2/point, the same one weapons/Grenades use) plus a
   flat Harried credit, on the reasoning that a normal attack roll's
   own baked-in ~50% miss chance was doing similar work to "they might
   not be there." Per the designer, that's the wrong model — there's no
   roll here at all, so this is a genuine guaranteed hit whenever the
   target's actually present, which is exactly the case
   `balance_weights.csv`'s own Damage row calls out: *"a guaranteed
   point of harm that skips the attack roll uses Health's rate (4)
   instead."* No Harried credit either, since Harried only triggers when
   a real Defense gets applied against an actual attack — nothing like
   that happens here.
2. **Realization tier.** The corrected math (4/point, no Harried) came
   out badly overfunded on its own (140-230% across Levels 1-4) — not a
   subtle miss, a real sign the "guaranteed hit" framing was letting the
   item keep value it hadn't actually earned. Per the designer's own
   diagnosis: the delay is exactly why it isn't really guaranteed in
   practice — "an enemy is just going to step out of the way." A full
   round of telegraph is enough warning that most aware, on-level
   enemies do relocate, making "still standing there" the less common
   outcome, not a coin flip — the standard **⅓ niche tier**, not the ½
   tier a first pass tried, which still left it well over Target.

**Final math**: Resist placeholder for a fixed (non-scaling) Physical
item stays the standard `Body 3 + 1 armor = 4` (the baked-in 4 is the
*item's* own chosen power level, not a stand-in for a tougher assumed
enemy, so it doesn't get to also inflate its own target's toughness).
`margin = 11 − 4 = 7`, `Value = 7 × 4 (guaranteed-harm rate) × ⅓ (niche
tier) = 9.33`. `Target = 9` (Level 3), **`Net = +0.33` (104% funded)** —
about as close to an exact fit as this model produces. (At a baked-in
stat of 3 instead: `Value = 8.0`, `Net = −1.0`, 89% funded — still
reasonable, just a worse fit than 4.)

## Held slot — first pass

30 items, the largest single slot.

### Assassin's Undetectable Arms — cut, pulled to the backlog as a concealment accessory power

Level 1, 20 Gold. "Regardless of its type or construction, some feature
or enhancement of the weapon allows it to be concealed on your person.
Furthermore, you have Good Luck on any flip to keep it hidden, and
anyone attempting to search you for it or detect it has Bad Luck on the
associated flip." A narrative/skill-challenge item — closest existing
precedent is Smuggler's Belt's own "Secrecy" component (Good Luck-tier
concealment at the ⅓ "rarer than daily" niche tier, and "someone
actually searching you" is literally that tier's own canonical
example). Partial pricing sketch before the cut: `(2.4 Good Luck + 2.2
Bad Luck) × ⅓ = 1.53` against either Target convention, a real
shortfall (51% funded per-encounter, 26% funded once/day) — and that's
before even accounting for the item's other implied component (that a
weapon normally *can't* be concealed at all without this enhancement),
which was never resolved.

Per the designer: this reads better as a **narrative/skill-challenge
concealment power** that would work better folded into another item as
an accessory effect than priced and shipped standalone at Level 1.
Moved to `IDEAS_BACKLOG.md` rather than priced — flagged for a future
Held item (or another slot) that wants a concealment hook alongside its
main effect, not a fresh derivation from scratch when that day comes.
Removed from `items.csv` (`I088`), regenerated into `data/items.json`.

### Push decoupled from Speed and re-derived = 0.89375/meter — Battering Armament = 3m, Level 1

Level 1, 20 Gold. "When an attack with this weapon hits or is Parried,
the target is Pushed 1 meter in a direction of your choice." Priced at
the existing Push rate (0.55/meter, reused directly from Speed's own
single-instance rate), `Value = 0.55`, **Net = −2.45** against Level 1's
`Target = 3` — only 18% funded, the largest shortfall found so far this
pass on a single-component item.

**Push's own rate got re-derived from scratch, decoupled from Speed
entirely**, rather than patched item-by-item. The old rate reused
Speed's single-instance derivation (`1 AP(2.75) / (baseline Speed+1 =
5)`) wholesale — but per the designer, Push deserves its own anchor:
**a standard move is 4 spaces**, not Speed's own baseline-plus-one
figure, and Push's real value is more than a raw AP-equivalent of
lost movement — forcing an enemy out of position (breaking their
formation, isolating them from allies, shoving them somewhere
disadvantageous) is a real, additional tactical benefit a plain
"undo my displacement" framing doesn't capture. `Value = 1 AP(2.75) / 4
= 0.6875/meter` base, **+30% tactical premium** (a modest, explicitly
judgment-call bump, same convention as Elemental Warding Band's own
+15% targeting-flexibility bump) `= 0.89375/meter`. **Speed's own rates
(single-instance 0.55, permanent 2.54375) are untouched** — this
correction is scoped to Push alone, not a wholesale Speed re-derivation.
`balance_weights.csv` updated.

At the new rate, Level 1's `Target = 3` needs **3.357m** for an exact
fit — not a clean number, and half-spaces aren't a thing. **Locked in
at 3m** (`Value = 2.68`, **Net = −0.32**, 89% funded) over 3.5m (104%
funded), the closest clean distance under the target. `items.csv`
(`I090`) updated (1m → 3m). Regenerated into `data/items.json`.

**Flagged for later, not decided now**: whether Battering Armament
should scale Level 1-5 instead of staying fixed at Level 1. A naive
`3m × Level` scaling holds a perfectly constant 89.4%-funded ratio at
every Level (Push has no diminishing curve to fight, unlike Ward/
Hasted), but the raw distances get large fast — 15m at Level 5 reads as
a lot for a single melee hit's shove, well past every other Push/
movement effect priced this pass (Slipstream Sandals topped out at 3m,
Windrider's Loop's Range at 10m). If it scales, it likely wants
something other than raw linear meters-per-Level (the same "cap it and
scale a secondary component instead" move Snowfall Drape and Cowl of
Tranquility made once *their* linear scaling stopped making sense), not
a decision to make in isolation — revisit once the whole Held block
gets assessed after this pass, alongside any other single-Level items
that might want the same look.

### Legbreaker rechecked under the new Push rate — trimmed 4m → 3m

Level 2 Grenade, previously `Value = 5.7`, `Net = −0.3` (95% funded),
using the old Push rate: `margin(8) + 4m×0.55(2.2) + Harried(1) −
Autoswing(5.5) = 5.7`. Under the new 0.89375/meter rate, the same 4m
Push jumps to `4×0.89375 = 3.575`, pushing `Value` to `7.075` against
`Target = 6` — **Net = +1.075, 118% funded**, a real overshoot, not
noise. Per the designer, rechecked rather than left stale: trimmed the
Push distance to **3m** (`3×0.89375 = 2.68125`), landing at `Value =
6.181`, **Net = +0.18** (103% funded) — a clean fit, restoring the same
close-to-Target shape the original 4m/old-rate version had. `items.csv`
(`I213`) updated (4m → 3m). Regenerated into `data/items.json`.

### Bounty Hunter's Blade = Narrative Utility, confirmed as-is — Level 1

"Non-lethal attacks with this don't have Bad Luck," removing the
rulebook's Non-Lethal Attacks penalty (`rulebook.md:530`) specifically
on non-lethal attacks made with this weapon. The naive read is real
combat math (Bad Luck's own established 2.2 rate) — but the value
swings wildly depending on an assumed frequency with no real anchor: a
clean-ish fit around 1 non-lethal attack/encounter (2.2 ≈ Target 3),
badly overfunded on a full non-lethal build (~7.5 own-attacks/encounter
baseline × 2.2 ≈ 16.5).

Per the designer: this item is meant to be comparable to a same-Level
Form Technique — a way to feed mostly narrative requirements (a bounty
hunter needing a target alive), not a combat-optimization pick — and
isn't meant to be evaluated well at all. Priced via the Narrative
Utility convention instead of the frequency guess: `Value = ⅓ × 3 = 1`,
`Net = 1 − 3 = −2`. Confirmed as-is, no item text changes needed.

### Shadowdraw = 3.36, merged from Eager Armament + Assassin's Undetectable Arms — Level 1

Eager Armament ("drawing the weapon from any location within reach only
takes 0 AP") started down the same path as Quick Draw Belt — priced
against the backpack case (2 AP saved = 5.5), once/encounter. First
draft landed at `Net +2.5` (matching Poison Needle's own accepted
Level-1 overshoot), on the read that the weapon's normally-concealed
fluff makes it the hard-to-reach case.

**Corrected before locking in**: that once/encounter framing carries an
implicit assumption the designer flagged — most characters already
have their weapon drawn or in easy reach when a fight starts, so a
generic "saves 2 AP every encounter" claim doesn't actually hold for
this item the way it does for Quick Draw Belt's general-purpose
version. The 0-AP draw only pays off in the specific scenes where the
wielder chose to go around visibly unarmed and a fight then breaks out
— the same ⅓ "rarer than daily, niche" trigger already governing
concealment checks, not a guaranteed once/encounter event.

That reframing pointed straight at merging Eager Armament with
**Assassin's Undetectable Arms** (`I088`, cut earlier this pass — see
its writeup above): both items are really the same underlying weapon
(one hidden and hard to draw, one designed to draw for free from
wherever it's kept), and Assassin's Undetectable Arms' own concealment
component was already priced at the ⅓ niche tier and looking for a
home. Renamed to **Shadowdraw**, merging both effects:

- **0 AP draw**, now correctly scoped to the ⅓ niche tier (not every
  encounter): `5.5 × ⅓ = 1.833`.
- **Concealment Good Luck/Bad Luck** (Assassin's Undetectable Arms'
  own Smuggler's Belt-precedent math, unchanged): `1.53`.

`Value = 1.833 + 1.53 = 3.36`, `Target (L1, per-encounter) = 3`, `Net =
+0.36` (112% funded) — a clean fit at the original Level 1 / 20 Gold,
no Level bump needed. Main Material swapped Wood → Shadow to match the
concealment half. Assassin's Undetectable Arms' `IDEAS_BACKLOG.md`
entry removed — resolved into this item rather than left pulled.

### Fatestealer = hand-tuned 1/3/5/6/8 charge curve, Level 1-5

"When an attack with this weapon Downs a creature, that creature is
instantly killed and the weapon gains up to `[enhancement's Level]`
charges" (capped 5, lost on a full night's rest). Spend charges: 1 →
Sift 2 cards, or 3 → draw a card.

Three pieces:

- **"Instantly killed" on Down** — real mechanical insurance (the
  rulebook's Downed state, `rulebook.md:366`, explicitly isn't death —
  "not at risk of dying immediately, but this may change depending on
  the circumstances"), but genuinely GM/scenario-dependent (how often
  does an enemy actually threaten to come back?). No clean anchor —
  left unpriced, same as several other flagged-but-unquantified clauses
  this pass.
- **Charge economy** — 1 charge → Sift 2 = `2 × 0.60 = 1.2/charge`; 3
  charges → draw 1 = `2.7 / 3 = 0.9/charge`. Per the designer, left as-
  is deliberately even though Sift is strictly the better trade (a
  rational player never takes the draw option) — a real, accepted
  inefficiency rather than a bug to fix.
- **Charge generation frequency** — no existing anchor for "how many
  enemies does the wielder personally Down." Per the designer: someone
  building around this weapon handles more than an average character,
  landing on **~1.5 Downs/encounter** as the working baseline (2/day
  at the high end was also discussed) — `× 2 encounters/day` (the
  established convention) = **3 Downs/day**.

**Flat-`Level` formula replaced with a hand-tuned curve** rather than
left as one shared shortfall shape across every Level. Solving
`Value = 3 × chargesPerDown × 1.2` against `Target = 6 × Level` for an
exact fit gives `chargesPerDown ≈ 1.667 × Level`; rounded to clean
integers and anchored on the designer's own `L2=3`/`L4=6` picks, with
`L3=5` filled in by exact-fit interpolation (lands precisely on
`Net=0`) and `L5=8` chosen over `9` to stay at or under Target rather
than overshoot it:

| Level | Charges/Down | Value | Target | Net | Funded |
|---|---|---|---|---|---|
| 1 | 1 | 3.6 | 6 | −2.4 | 60% |
| 2 | 3 | 10.8 | 12 | −1.2 | 90% |
| 3 | 5 | 18.0 | 18 | 0 | 100% |
| 4 | 6 | 21.6 | 24 | −2.4 | 90% |
| 5 | 8 | 28.8 | 30 | −1.2 | 96% |

Levels 2-5 land in a tight 90-100% band; Level 1 stays at 60%,
confirmed by the designer as acceptable — "Level 1 can be a bit
underpowered." Charge cap raised **5 → 8** to match the new Level 5
grant (a single Down at Level 5 would otherwise exceed the old cap and
waste 3 charges immediately). `items.csv` (`I092`) Effects text
rewritten to state the per-Level curve explicitly rather than a
`[Level]` formula, since it's no longer a clean multiple. Regenerated
into `data/items.json`.

### Quartermaster's Blade = Narrative Utility, confirmed as-is — Level 1

"As a Move, change the weapon's shape to that of any other single
weapon, including shields." No clean anchor: `weapon_categories.json`'s
profiles genuinely differ (Accuracy/Damage/Defense, plus different
governing Skills), but the practical value is mostly confined to
swapping within one Skill family (a Melee character can freely move
between 1H/2H Light/Heavy and Shield; swapping to a Bow/Thrown/Unarmed
profile only helps if that Skill is also trained) — genuinely
situational and build-dependent rather than a fixed number, without
picking an arbitrary "which swap, how often" scenario.

Per the designer: priced via the Narrative Utility convention rather
than constructing a representative case. `Value = ⅓ × 3 = 1`, `Net = 1
− 3 = −2`. One wording fix alongside the confirmation (not the pricing):
the original text denied ammunition outright if the weapon turned
ranged ("does not create ammunition") — flipped to match Armory
Gauntlets' own precedent (`I075`, "may also conjure ammunition for it
as part of an attack"), so the effect reads flat across every weapon
type instead of carving out a ranged-specific exception. `items.csv`
(`I186`) updated. Regenerated into `data/items.json`.

### Reaching Weapon = Level×4.125, confirmed overfunded but left as-is — Level 1-5, new Range (permanent) rate derived

"Attacks made with this weapon, and abilities used with it, have their
Range increased by [Level] meters," always on. Unlike Windrider's
Loop's once/encounter Range bump, this is a permanent bonus — the same
gap `balance_weights.csv`'s Range row already flagged for itself
("a permanently-worn Range bonus would need the same single-instance-
to-permanent rescoping Speed itself needed").

**First framing tried and set aside**: reuse Speed's own permanent
rescoping directly (`single-instance × moves/encounter`), on the theory
that Range substitutes for movement the same way Speed does. Rejected
on reflection — Speed's `4.625 moves/encounter` multiplier counts *all*
movement (retreating, repositioning, chasing), but Range only
substitutes for the fraction of that spent specifically closing
distance to attack. Tried scoping it down via the established ½/⅓
realization tiers instead (`half of moves/encounter are attack-closing`
→ `1.271875/meter`), but that produced a very different verdict (42%
funded at every Level) than the full-reuse alternative (85% funded) —
too wide a swing to settle on either number without a firmer anchor.

**Reframed, and this is the version used**: per the designer, since the
weapon is always-on, its Range bonus should be scoped by how many
*attacks* happen per encounter, not by movement at all — every attack
made with the weapon benefits from the extra reach, so the multiplier
is the established `attacks/encounter` figure (**7.5**, `1.5/turn × 5
rounds`), applied to the existing single-instance Range rate rather
than inventing a new discount:

`Range (permanent)/meter = 0.55 (single-instance) × 7.5 (attacks/
encounter) = 4.125/meter` — added to `balance_weights.csv`.

Solving for the break-even point (`Target/4.125 = 3L/4.125 ≈ 0.727×L`)
shows the item's own `[Level]`-meters formula already grants *more*
than the break-even amount at every Level:

| Level | Meters | Value | Target | Net | Funded |
|---|---|---|---|---|---|
| 1 | 1 | 4.125 | 3 | +1.125 | 137.5% |
| 2 | 2 | 8.25 | 6 | +2.25 | 137.5% |
| 3 | 3 | 12.375 | 9 | +3.375 | 137.5% |
| 4 | 4 | 16.5 | 12 | +4.5 | 137.5% |
| 5 | 5 | 20.625 | 15 | +5.625 | 137.5% |

A constant 137.5%-funded overshoot at every Level, since both sides
scale linearly with Level — no per-Level curve needed (unlike
Fatestealer), just one consistent ratio. Per the designer: confirmed
"a little powerful," but left as-is — there's no clean way to trim
this without breaking the tidy `Range = Level` symmetry, and the
overshoot is smaller than Poison Needle's already-accepted 183%.

**Wording also cleaned up** while in this text: the item predated the
`[Range]` glossary keyword (`glossary.md:39`, "if something increases
an effect's Range by X, you may choose any point within X meters... to
target creatures that are X meters farther away than usual"), so it
still manually spelled out the "choose any point within X meters for
non-ranged effects" clause the keyword now covers generically.
Simplified to match Windrider's Loop's already-clean phrasing
("increase that weapon's Range by 10 meters," no follow-up sentence).
Found and fixed the same stale pattern on **Spiritlink Scepter**
(`I184`, Held, Level 3, not yet reached in this pass) while checking
for consistency — same fix, no pricing change, will get its own full
pass when the Held slot reaches Level 3. `items.csv` (`I093`, `I184`)
updated. Regenerated into `data/items.json`.

### Returning Knives + Weapon of Sending — both cut, thrown-weapon "return" mechanic dropped

Returning Knives (`I183`, Level 1) — "when the weapon is thrown as part
of an attack, at the start of the wielder's next turn it returns to
their hand" — looked at first like it solved a real problem: a Held-
slot Masterwork weapon is presumably the wielder's primary attack, and
throwing it away would seem to leave them disarmed until it's
retrieved.

Per the designer: that premise doesn't hold. Thrown weapons are meant
to be treated as an abstracted "you have enough of these to fight
with" collection, recovered as a batch after the encounter — not
tracked square-by-square mid-combat, since that bookkeeping isn't
interesting or worth balancing around. Under that design call, there's
no real in-combat cost this item is removing in the first place — cut
rather than priced.

**Weapon of Sending** (`I097`, Level 2) shares the identical "returns
to hand" clause, so it loses the same rationale. Its other component —
letting a weapon that couldn't normally be thrown be thrown as an
Acrobatics attack — was originally added "for fun," but per the
designer, Reaching Weapon already covers the underlying need (extended
threat range instead of needing to throw at all), and a genuine
throw-a-melee-weapon option is better suited to a Technique if it's
ever wanted. Cut alongside Returning Knives.

Both removed from `items.csv`. Regenerated into `data/items.json`
(213 → 211 rows).

### Staying Gauntlets — cut, superseded by Bounty Hunter's Blade

"Weapon attacks made by the wearer that would Down a creature instead
render them unconscious rather than killing them." Landed in almost
exactly the same spot as **Bounty Hunter's Blade** (`I089`, just
confirmed via the Narrative Utility convention): both remove the
practical cost/risk of the Non-Lethal Attacks Bad Luck penalty
(`rulebook.md:530`), just triggered differently — Bounty Hunter's
Blade on a declared non-lethal attack, this one automatically whenever
a weapon attack would Down a creature. Per the designer: redundant
with an item already confirmed in the list rather than a distinct
niche — cut rather than priced. Removed from `items.csv`. Regenerated
into `data/items.json` (211 → 210 rows).

### Venomous Weapon = flat Level×3, exact fit — Level 1-5, all Poison flavors treated as interchangeable

"When created, a Basic Poison is chosen, with a Concentration of
+[3+Level] and a Potency of Level" — the exact same formula Basic
Poison (`I049`) itself uses, auto-exposed the first time each encounter
this weapon causes Health loss or Bleeding. Per the designer's framing:
this is basically a weapon that "creates" one poison dose per fight.

**First pass considered and set aside**: since the wielder locks in one
flavor permanently at creation, price off whichever of the seven
already-priced flavors (`I050`-`I056`) is mathematically strongest —
Vulnerability/Harrying Poison, cleanly linear at `Value = 4×Level`,
`Net = +1×Level` (133% funded), no stack cap to run into. Set aside per
the designer: all seven flavors cost the same to craft and should be
treated as "worth" the same regardless of their own internal balance
(which genuinely varies, from Slowing Poison's real shortfall to
Vulnerability/Harrying's accepted overshoot) — re-litigating which
flavor a min-maxer would pick isn't the point of pricing this item.

**Used instead**: Crippling Poison's own formula stands in as the flat
baseline, since it's the one already called "naturally balanced" in its
own writeup — `Value = 3×Potency×2 = 3×Level`, exactly matching
`Target = 3×Level` at every Level. Venomous Weapon delivers that same
value for free, once per encounter:

| Level | Value | Target | Net |
|---|---|---|---|
| 1 | 3 | 3 | 0 |
| 2 | 6 | 6 | 0 |
| 3 | 9 | 9 | 0 |
| 4 | 12 | 12 | 0 |
| 5 | 15 | 15 | 0 |

An exact fit at every Level — no per-Level curve needed. Wording
clarified (not the pricing): the trigger now explicitly states it costs
**0 AP** to auto-expose the target, closing a gap where the text could
otherwise be read as still owing the glossary's normal 2 AP Poison-
application cost (`glossary.md:105`) on top of the automatic trigger.
Flavor choice stays fixed at creation, per the designer, unchanged.
`items.csv` (`I094`) updated. Regenerated into `data/items.json`.

### Elemental Bloodletter — cut, an early elemental-weapon pass that doesn't hold up under the Bleeding-taper model

"When the weapon is created, choose Fire, Frost, Brilliant, or Shadow —
it deals its damage as that type instead of Physical. Whenever an
attack with it would cause a creature to lose Health, they instead
gain that many stacks of Bleeding." Two components, priced fully per
the designer's request before deciding what to do with the result.

**Component 1 — permanent damage-type conversion**. Ring of Pure
Elements already priced a *once/encounter* version of this idea at
`1 point of average soak bypassed × Damage's rate (2/point) = 2.0`.
Worry Token's Diamonds branch and Spellblade's Sipper both confirm the
formula scales linearly with how many attacks it covers (`×2 attacks
= 4.0`, `×4 attacks = 8`, respectively). Elemental Bloodletter's
version is permanent — every attack, all encounter — so using the
established `attacks/encounter = 7.5` baseline: `Value = 1 × 2 × 7.5 =
15`. A real, strong number on its own.

**Component 2 — damage→Bleeding conversion**. Checked against Bleeding's
own established capped curve (`value(n)`, asymptotically capping near
12) versus what the same points would be worth as guaranteed Health
loss instead (Health's own rate, `4/point`, uncapped). At a
representative weapon hit (baseline stat=3, e.g. 1H Light Melee's
`3+[Body]` → 6 damage): `value(6) = 11.75` vs. `6 × 4 = 24` as plain
Health loss — a per-hit **loss of −12.25**. This isn't sensitive to the
exact representative number either: it holds for any hit above ~2
damage, and gets worse as weapon damage increases, since Bleeding's
curve caps near 12 while raw guaranteed Health loss keeps scaling
linearly. Scaled the same way as Component 1 (every attack, ×7.5):
**−91.875**.

**Combined**: `15 − 91.875 ≈ −77` against Target 6 — not a "landed low"
number, a structural finding: as literally worded, the Bleeding clause
makes the wielder's own attacks actively worse than doing nothing
extra, on essentially every hit. Per the designer: this reads like an
early pass at an elemental weapon from before the Bleeding-taper work
existed in this project, and doesn't hold up now that it does. Binned
rather than redesigned, in favor of the existing elemental-conversion
options already in the Held slot (Elemental-Forged Weaponry, Claw of
Mortality, Claw of Rime, Conflagration Brand — none yet priced this
pass, but all structurally simpler). Removed from `items.csv`.
Regenerated into `data/items.json` (210 → 209 rows).

### Grim Promise = 7.27, reusing Insanity Potion's Wounded/Crippled components at the ⅓ niche tier — Level 2

"When attacking or parrying with this weapon, the wielder ignores any
penalties from being Wounded or Crippled." Reused Insanity Potion's
(`I048`) own already-established Wounded/Crippled-immunity components
directly as raw per-instance figures, rather than re-deriving from
scratch:

- **Wounded's Bad Luck** on attack/parry flips — Insanity Potion's own
  "flip-based" sub-estimate is already scoped to exactly this (not all
  flips broadly): `~2 turns × (1 attack + 1 defense flip) × Bad Luck
  (2.2) = 8.8`.
- **Wounded's separate −2 Defense penalty** on Parry specifically (a
  distinct modifier from Bad Luck, not covered above): `~2 turns × 1
  parry/turn × 2 points × Defense's rate (1) = 4`.
- **Crippled's removal**: since Crippled's only effect is "−1 to
  attacks" (nothing else, per the glossary), ignoring it while
  attacking is full Crippled immunity — Insanity Potion's own
  representative case, `3 stacks, 4-turn window = 9`.

Stacked raw: `8.8 + 4 + 9 = 21.8` — 363% over Level 2's Target (6) if
taken at face value. But Insanity Potion's own figures assumed
**guaranteed, 100%-uptime Wounded+Crippled**, since that item inflicts
both conditions on the drinker itself as a built-in drawback — a
completely different premise from a normal wielder's baseline
likelihood of actually being Wounded or Crippled during a given fight.

Per the designer: Wounded and Crippled are relatively uncommon
specifically **for the wielder**, even though similar debuffs are
common from enemies in general (i.e., the debuffs themselves come up
with regularity against the party as a whole, but landing on this one
character specifically is rarer) — mapping onto the established ⅓
"rarer than daily, niche" realization tier rather than treating it as
guaranteed. `Value = 21.8 × ⅓ ≈ 7.27`, `Target (L2) = 6`, `Net ≈ +1.27`
(121% funded) — a modest overshoot in line with several other
accepted overshoots this pass. No item text changes needed.

### Sorcerer's Bow = 3.0, moved to Level 1 — Sorcerer's Gloves cut, absorbed into the Bow

Sorcerer's Bow ("uses Sorcery as its relevant Skill, damage based on
Mind instead of Cunning") is a build-flexibility item, not a numeric
buff — the underlying Bow-category stats (`weapon_categories.json`)
stay identical; only which Skill/Stat drives them changes. Same shape
as Quartermaster's Blade's weapon-flexibility (priced via the Narrative
Utility convention, since the real gain depends entirely on the
wielder's own build — how lopsided their Mind-vs-Cunning gap is, which
the model has no way to know): `Value = ⅓ × 6 = 2` as a floor.

**Sorcerer's Gloves** (`I178`, same Level, "throw a bolt of energy...
Sorcery attack... 3+[Mind] Physical damage") covered a related but
distinct niche — a generic Sorcery-driven attack that doesn't require
holding any weapon at all. Per the designer: the Bow should absorb this
role rather than keeping both items around. Cut Sorcerer's Gloves,
folded a flat **+1.0** premium into Sorcerer's Bow for now covering
that niche too (no clean way to price the "no separate weapon needed"
convenience harder than a flat premium, same judgment-call shape as
other flexibility bumps this pass): `Value = 2 + 1.0 = 3.0`.

**Moved Level 2 → 1**: per the designer, committing to this weapon's
Skill/Stat also means giving up any Archery-gated Techniques the
wielder might otherwise want — a real opportunity cost with no clean
way to price directly (the same rabbit hole as everything else this
pass), better reflected by sitting at a lower Level than by inflating
Value to chase Level 2's Target. At Level 1 (Target 3, Cost 20 Gold):
`Net = 0` — an exact fit, cleaner than the Level 2 version's 50%-funded
gap. `items.csv` (`I096` Level/Cost updated, `I178` removed).
Regenerated into `data/items.json` (209 → 208 rows).

### Apprentice's Dueling Catalyst — cut, obsolete now that Bounty Hunter's Blade is an Implement

"Spell attacks made using this as an Implement that would Down a
creature instead render them unconscious rather than killing them."
Wasn't in the original Held stocktake — caught while surveying what
was left after closing out Level 1/2.

Per the designer: this is a holdover from before most weapons carried
the `[Implement]` tag, when a spellcaster needed a dedicated item to
guarantee non-lethal spell attacks since their weapon Implement
couldn't cover that ground too. Now that Bounty Hunter's Blade (`I089`)
is itself tagged Implement, the `[Implement]` rule (`glossary.md:97`,
"the Spell or Discipline counts as an attack with that weapon for any
additional effects") already makes its non-lethal Bad Luck removal
apply to any spell attack channeled through it as well — no separate
item needed. Removed from `items.csv`. Regenerated into `data/items.json`
(208 → 207 rows).

### Attacks/turn split into two baselines — 1.25 (own, incidental) vs. 1.5 (aggressive/tank), Reaching Weapon rechecked

Surfaced while pricing Claw of Mortality's permanent elemental-conversion
component, which reused Range (permanent)'s own `attacks/encounter`
scaling (`7.5`, derived from `1.5 attacks/turn × 5 rounds`) — the same
figure used throughout this project for combat-frequency math (Crippled's
per-stack rate, Fitted Armor's tank assumption, Sift's daily cadence,
the Skill-vs-Technique meditation's daily-attack figures). Surveyed
every elemental-conversion item in the pool (Ring of Pure Elements,
Spellblade's Sipper, Elemental-Forged Weaponry, Claw of Mortality/Rime,
Conflagration Brand) to check whether the permanent, full-attacks/
encounter scaling had any real precedent — it didn't; every item priced
*so far* used an explicit, capped window (1 attack, or 4 attacks), and
nobody had actually validated the formula at the full permanent baseline
before Elemental Bloodletter/Claw of Mortality tried it.

Per the designer: `1.5 attacks/turn` (implying half of all turns are a
double-swing) reads too generous for a normal player's own attack rate
— realistically closer to **one, maybe two turns out of five** seeing a
double swing, not half. Solving `attacks/turn = 2p + 1×(1−p)` for
`p ≈ 0.25` (roughly 1 in 4 turns doubles): **`1.25/turn`**.

**Critical distinction, not a blanket revision**: this doesn't replace
the older `1.5/turn` figure everywhere — that figure stays exactly as
it was for anything modeling an **aggressive or tank-style combatant**
taking/making more hits than a normal player optimizing their own
turns (Crippled's own per-stack rate, Fitted Armor's "tank takes 1.5×
hits" assumption, Sift's daily-cadence estimate, and the earlier
Skill-vs-Technique meditation's daily-attack figures) — per the
designer, "a tank putting themself in the position to take more hits"
is a genuinely different scenario from "a player doing what they can
to make more attacks." Those derivations aren't reopened by this
correction. The new **`1.25/turn` ("own, incidental")** baseline is
specifically for pricing an always-on item effect that rides every
attack the *wielder personally makes* — Range-permanent, elemental-
conversion-permanent, and anything else in that same shape. Added both
as distinct rows to `balance_weights.csv`.

`attacks/encounter (own, incidental) = 1.25 × 5 = 6.25` (down from
7.5). Downstream effects:

- **Range (permanent)**: `0.55 × 6.25 = 3.4375/meter` (down from
  4.125).
- **Elemental Conversion (permanent)**: `2 (Damage's hit-gated rate ×
  1 soak bypassed) × 6.25 = 12.5` for a full-uptime case (down from 15).
  Added as its own row to `balance_weights.csv`, generalizing the
  "1 soak bypassed × Damage's rate" formula for a permanent, not just
  fixed-window, conversion.

**Reaching Weapon rechecked** (already committed/pushed under the old
rate): `Value = Level × 3.4375`, still a consistent overshoot at every
Level but down from 137.5% to **114.6% funded**. Same designer call as
before — left as-is rather than trimmed, no clean way to reel it in
without breaking the `Range = Level` symmetry. `balance_ledger.csv`
rows updated (`I093-L1` through `L5`); no `items.csv` text change
needed, only the rate/Value/Net.

### Claw of Mortality / Rimefang / Radiant Verdict / Conflagration Brand — the elemental-Held-weapon family, priced together

Surfaced while pricing Claw of Mortality's spell-conversion clause,
which needed the new `attacks/turn` split above. Rather than price the
four Level 3 "weapon debuff + spell-conversion" items one at a time,
worked through them as a family so their relative strength lines up on
purpose rather than by accident. Confirmed the family's actual design
intent first, per the designer: **damage conversion is the valuable
half for weapon attacks specifically**, and these four items exist to
give spellcasters something useful out of the same slot too — via
debuffs, not damage conversion, since spells are already elemental
most of the time and converting an already-elemental spell to a
*different* element is a much smaller benefit than converting a
Physical weapon attack.

**Two separate elemental-conversion baselines derived**, since "what
does this attack default to" differs by attack type:

- **Weapon attacks default to Physical.** Converting one to an element
  bypasses the real, large gap between Physical Resist's rate (5.0)
  and an elemental Resist rate (1.0 Fire, 0.5 Frost/Brilliant/Shadow)
  — the original `1 point of soak bypassed × Damage's rate(2) = 2`
  formula holds at full strength for Frost/Brilliant/Shadow. **Fire
  gets a discount**: it's the most common elemental damage type (per
  the designer, and matching Fire Resist's own rate being double the
  other three — enemies more often carry some), so converting *to*
  Fire specifically bypasses less. Calibrated directly off Elemental-
  Forged Weaponry's own existing Level 3 (Fire) / Level 4 (other three)
  split rather than re-deriving from Resist-rate arithmetic: solving
  for what value/attack lands Fire's own Level-3 Target at the same
  ~104%-funded ratio the other three hit at Level 4 gives **`1.5/
  attack`** for Fire, `2/attack` for the rest. Added to
  `balance_weights.csv` as *Elemental Conversion, weapon (Physical
  baseline)*. This also confirmed Elemental-Forged Weaponry (`I101`,
  not otherwise touched this pass) was already correctly designed —
  its existing Level split just never had the underlying rate written
  down.
- **Spells default to Fire**, not Physical (per the designer, matching
  Sorcery's own flavor text — "shooting fireballs"). A conversion
  scoped to spell/non-weapon attacks (the shape all four family items
  use) is really Fire → [other element], a much smaller resist gap.
  Scaled the original soak-bypass credit proportionally to the
  established Resist rates (`Fire's rate ÷ Physical's rate = 1.0 ÷ 5.0
  = 0.2`) rather than assuming the full 1-point credit: `value/attack =
  0.2 × Damage's rate(2) = 0.4`. Added to `balance_weights.csv` as
  *Elemental Conversion, spell (Fire baseline)*. At full spell-uptime
  (`attacks/encounter`, own-incidental baseline, 6.25): **`0.4 × 6.25 =
  2.5`**. A conversion *to* Fire specifically is a complete no-op under
  this rule (spells are already Fire by default) — flagged for
  Conflagration Brand below.

**Checked whether a debuff could stack on top of the full weapon-
conversion value**: no room — weapon-conversion alone already
saturates the Target at either Level (104% both ways), so there's no
budget left without bumping the Level. Confirms the current split is
correct: Elemental-Forged Weaponry stays the pure-conversion item, this
family stays debuff-focused with only the small spell-bonus on top.

**New debuff-pricing technique**: none of these four items apply their
debuff as a one-shot lump — they refresh it on *every* weapon hit,
continuously, for the whole fight. That needed a different model than
this project's existing lump-application curves (which assume all
stacks land at once and decay together). Set up as: `hits/turn = 1.25
(own-incidental attacks/turn) × 0.5 (avg hit chance) = 0.625`, `×5
rounds = 3.125 total stacks applied/encounter`. Then split by keyword
shape:

- **Discrete-payout debuffs** (Bleeding, Necrotic — resolve via one
  event when a stack decays, no interaction between simultaneous
  stacks): `total stacks applied × the keyword's own per-stack rate`
  directly, since individual 1-stack applications mostly resolve well
  clear of any stacking taper before the next one lands.
- **Continuously-active debuffs** (Slowed, Vulnerable, Crippled,
  Taunted/Frightened — penalty applies for as long as any stacks
  remain): a queueing approximation, since arrivals (0.625/turn) run
  below the 1/turn decay rate and the stack count settles into a low
  equilibrium rather than climbing to the stacking cap and holding
  there. `average active stacks = arrival/(decay−arrival) = 0.625 ÷
  0.375 ≈ 1.67`, then `value = avg active stacks × per-stack rate × 5
  rounds`. Flagged explicitly as a simplified (M/M/1-style) queueing
  approximation, directionally solid but not exact to the decimal.
  Assumes each weapon is the sole source of its own debuff — no
  stacking with a duplicate copy or another item/Technique granting
  the same keyword, since that's a different character's pricing
  problem, not this one's. Both added to `balance_weights.csv` as one
  combined *Continuously-refreshed debuff* row.

**Family results** (Level 3, Target 9 each):

| Item | Element | Debuff (weapon) | Spell bonus | Total | Net | Funded |
|---|---|---|---|---|---|---|
| Claw of Mortality | Shadow | Necrotic ×2/hit, full tier: `2×3×1=6.0` | +2.5 | 8.5 | −0.5 | 94% |
| Rimefang (renamed from Claw of Rime) | Frost | Slowed ×1/hit, queueing: `1.67×1.1×5≈9.2` | +2.5 | 11.7 | +2.7 | 130% |
| Radiant Verdict (new) | Brilliant | Vulnerable ×1/hit, queueing: `1.67×1×5≈8.35` | +2.5 | 10.85 | +1.85 | 121% |
| Conflagration Brand | Fire | Bleeding ×1/hit, total-applied: `3.125×4=12.5` | +0 (no-op) | 12.5 | +3.5 | 139% |

Necrotic's rare-trigger nature genuinely caps how much it can carry
even under the most generous realization tier, landing Claw of
Mortality a bit short (94%) — structural, not a mistake. The other
three cluster in a 120–140% band, consistent enough across the family
to read as an intentional "this whole cluster runs a bit hot" choice
rather than three separate misses — accepted as-is rather than trimmed
individually, per the designer. Conflagration Brand's dead Fire spell
clause is deliberately left as a no-op (its own choice, not swapped to
a different element) — the item compensates by having Bleeding alone
carry the item's entire budget, ending up the strongest of the four,
which reads as a fair trade for the wasted clause.

**Radiant Verdict** (`I227`) is a new item, not previously in
`items.csv` — fills the family's missing Brilliant slot. Held, Level 3,
60 Gold, Main Material Brilliant, same Base Item Options as its three
siblings. **Claw of Rime renamed to Rimefang** (`I099`) — same
mechanics, new name (and a new Fluff paragraph, since the original had
none) to read as distinct from Claw of Mortality rather than a second
"Claw of X." `items.csv` updated (`I098` untouched mechanically,
`I099` renamed, `I100` untouched, `I227` added). Regenerated into
`data/items.json` (207 → 208 rows).

### Fanged Guard = 6.0, moved to Level 2 for an exact fit

"When the weapon is used to successfully Parry an attack from an
adjacent creature, that creature gains a stack of Bleeding." First
item this pass triggered off Parrying rather than attacking, needing a
defensive-frequency baseline instead of the offensive `attacks/turn`
one. Per the designer: a rational build for this item is a melee
defender specifically leaning into Parry Defense, planning to use it
against virtually every attack they face — `incoming attack attempts/
encounter (3.75, the established figure) × ⅔ (assumed melee share of
attacks against them) × 60% (assumed successful-Parry rate for a
Parry-focused build) = 1.5 successful Parries/encounter`. Bleeding
priced as a discrete-payout debuff (undiscounted per-stack rate, same
treatment as the Claw family): `Value = 1.5 × 4 = 6.0`.

Originally Level 3 (`Target 9`, `Net −3.0`, 67% funded) — a real
shortfall. Moved to **Level 2** instead (`Target 6`, `Cost 40 Gold`):
`Net = 0`, an exact fit. `items.csv` (`I102`) updated (Level 3→2, Cost
60→40 Gold; mechanic/wording unchanged). Regenerated into
`data/items.json`.

### Spiritlink Scepter — cut, obsolete since Reaching Weapon covers the same ground

"Theurgy spells cast using this as an Implement have their Range
increased by 3 meters." Already the same permanent-Range mechanic
Reaching Weapon uses, just scoped narrower (Theurgy spells only,
instead of all attacks and abilities). Since Reaching Weapon already
grants the identical 3-meter bonus at Level 3 with no such
restriction, per the designer this item is now strictly obsolete —
cut rather than priced (would have landed at `Value = 10.3125`, `Net =
+1.3125`, 114.6% funded, identical to Reaching Weapon's own accepted
overshoot, but there's no reason to keep a narrower duplicate around).
Removed from `items.csv`. Regenerated into `data/items.json` (208 →
207 rows).

### Valiant Arms = 6.0, moved to Level 2 for an exact fit

"When this weapon is used to make an attack, if the wielder moved at
least 6 meters in a straight line immediately before the attack, they
have Good Luck on the attack." A charge-attack mechanic — no formal
"charge" rule exists in the rulebook, per the designer, this item is
that idea informally. Wording tightened alongside pricing: "relatively
straight line" → "in a straight line," and added "immediately before
the attack" to fix the timing (move-then-attack, same turn).

Per the designer, a mobile build could pull this off roughly every
other attack without much tradeoff — **2-3 times/fight**; used 2.5 as
the working middle: `Value = 2.5 × 2.4 (Good Luck) = 6.0`.

Originally Level 3 (`Target 9`, `Net −3.0`, 67% funded) — moved to
**Level 2** instead (`Target 6`, `Cost 40 Gold`): `Net = 0`, an exact
fit, same shape as Fanged Guard's own move this pass. `items.csv`
(`I160`) updated (wording, Level 3→2, Cost 60→40 Gold). Regenerated
into `data/items.json`.

### Elemental-Forged Weaponry = confirmed as-is, both Levels clean fits

"When the weapon is made, Fire is chosen; if the enhancement is Level
4, Frost, Brilliant, or Shadow may be chosen instead. Attacks with
this weapon deal their damage as that type, instead of their usual
type." The pure weapon-conversion item — no debuff, unlike the Claw
family. Already priced during that same family pass, since this item's
own existing Level 3 (Fire)/Level 4 (any of the other three) split was
the actual calibration anchor for the new Fire-discounted weapon-
conversion rate, not something derived independently here.

`Value (Fire, L3) = 1.5/attack × 6.25 (own-incidental attacks/
encounter) = 9.375`, `Target = 9`, `Net = +0.375` (104% funded).
`Value (Frost/Brilliant/Shadow, L4) = 2/attack × 6.25 = 12.5`, `Target
= 12`, `Net = +0.5` (104% funded). Both clean fits — confirmed as-is,
no text or pricing changes needed.

### Sanguine Iron Weapon = 12.5, confirmed as-is

"Whenever an attack with the weapon causes the target to lose Health,
they also gain a stack of Bleeding." Same mechanic as Conflagration
Brand's Bleeding clause (discrete-payout, continuously reapplied on
every hit) minus the elemental-conversion half, at Level 4 instead of
3. Reused the total-stacks-applied model directly: `3.125 stacks/
encounter × 4/stack = 12.5`, `Target (L4) = 12`, `Net = +0.5` (104%
funded) — a clean fit, no changes needed.

### Scepter of Evocation — cut, superseded by Thrumming Focus

"A spell that would normally cost 2 or fewer AP may instead be cast
for 4 AP. If it is, Good Luck on any attacks made as part of the
spell." Same underlying idea as Thrumming Focus (`I103`, same Level,
same slot): pay extra AP for Good Luck. Per the designer, this reads
as an earlier draft of that same idea — narrower (only spells already
costing ≤2 AP) and pricier (+2 AP, not +1) for the identical benefit,
with Thrumming Focus's own wording ("spend an extra 1 AP for any
action involving an attack with this weapon") already the cleaner,
more general version. Cut rather than priced. Removed from
`items.csv`. Regenerated into `data/items.json` (207 → 206 rows).

### Thrumming Focus = 5.31, bumped to "Good Luck twice" and moved to Level 2

"The wielder may spend an extra 1 AP for any action involving an
attack with this weapon. If they do, that attack has Good Luck twice
instead of once." Originally just "Good Luck" — checked the raw trade
first, since this is the first item this pass to charge the *player's
own AP* per use rather than a flat activation tax: `Good Luck (2.4) −
1 AP (2.75) = −0.35`, a flat loss every single use. That means a
rational player only ever activates it in the narrow case where the AP
would otherwise go completely unused — modeled via the same 85/15
split Speed's own permanent-rescoping already uses for "moving once, 1
AP idle": `~0.56 turns/encounter`, `Value ≈ 1.35`, only **11% funded**.

**Bumped to "Good Luck twice"** (flip 3, take highest) instead of
raising the frequency assumption, per the designer. Needed a fresh
derivation — no existing rate for stacked Good Luck. Computed exact
`E[max of N]` from the 52-card deck (13 ranks, 4 copies each) via
combinatorics, marginal over the 7-baseline, plus a Suit Pool credit
scaled proportionally to Good Luck's own `+0.19` for 2 cards (`~0.095/
card`):

| Flips | Raw marginal | +Suit Pool | Total |
|---|---|---|---|
| 2 (Good Luck) | 2.196 | +0.19 | 2.4 (matches Good Luck exactly) |
| 3 (twice) | 3.294 | +0.285 | 3.6 |
| 4 (thrice) | 3.950 | +0.38 | 4.33 |
| 5 (four times) | 4.385 | +0.475 | 4.86 |

Added to `balance_weights.csv` as *Good Luck (stacked, flip N take
highest)*.

At "twice" (flip 3), the trade flips to genuinely profitable: `3.6 −
2.75 = +0.85` — a rational player now uses it on essentially every
attack, not just spare-AP turns. **Checked whether a second activation
on the same attack is worth it** (per the designer's own "what if it
stacks twice a turn" question): flip 5 (`4.86`) over flip 3 (`3.6`) is
only `+1.26` marginal, against another full `2.75` AP — a net loss.
Diminishing returns kill the second activation; rational play caps at
one per attack regardless of whether the rules permit more, so the
item's wording doesn't need an explicit stacking cap — natural optimal
play already self-limits.

Priced at full uptime (`own-incidental attacks/encounter`, 6.25), net
of the AP cost paid per use (not a one-time Potion-style tax, since
it's spent every time): `Value = 6.25 × (3.6 − 2.75) = 5.31`.
Originally Level 4 (`Target 12`, `Net −6.69`, 44% funded) — moved to
**Level 2** (`Target 6`, `Cost 40 Gold`): `Net = −0.69` (89% funded), a
much closer fit. `items.csv` (`I103`) updated (wording, Level 4→2,
Cost 80→40 Gold). Regenerated into `data/items.json`.

### Apocalyptic Staff = 12, 80% funded and accepted for the Feature flexibility

"Once per encounter, the wielder may choose a version of the War Magic
(Level 4) Sorcery Spell Technique, selecting any Features as though
they were learning it, and cast it as though they knew it." The
original text referenced "Elementalist's Artillery (Level 4) battle
magic Technique" — a broken reference, no such Technique exists.
Confirmed with the designer: that was War Magic's (`T120`) old name, a
Buildable Encounter Sorcery Spell capped at Level 4 (`Level Min 1 /
Max 4`, base "2+[Mind] Fire damage," up to 6 basic/advanced Feature
points at Level 4). Wording updated to the current name.

Reuses the already-established Technique-value convention from
Focusing Band of [Technique]: `Technique value (Encounter cadence)/
Level = 3`. At War Magic's max Level (4): `Value = 3 × 4 = 12`. The
item itself is Level 5 (`Target = 15`) while the Technique it borrows
caps at Level 4 — a real, structural gap: `Net = -3` (80% funded).

Per the designer: accepted as-is, not adjusted further — the
flexibility of choosing Features fresh each encounter (rather than
being locked into one fixed loadout the way actually learning the
Technique would be) is worth the shortfall. `items.csv` (`I104`)
updated (wording only). Regenerated into `data/items.json`.

### Heartseeker = 12.5, redesigned around a guaranteed Extra Success

"When the wielder makes an attack with this weapon, they may treat any
card flipped for it as a Heart" — broken as written. Extra Successes
require matching the *attacking Skill's own governing suit*
(`rulebook.md:181`), and no weapon-attack Skill is governed by Hearts
(Melee and Archery are both Spades, Brawl is Clubs) — the original
text did nothing for its own stated purpose.

Per the designer: this used to guarantee max damage back when suits
added a variable 0-3 damage bonus directly. That mechanic was replaced
by the current Extra-Success-adds-damage system, so this needed a real
redesign, not just a suit swap.

**First version considered and rejected**: retune *every* card flipped
for the attack to match, not just the one kept. Since Good Luck's both
flipped cards feed the Suit Pool, this would guarantee-match *both*
cards on every single attack — a real spiral, compounding a growing
Suit Pool advantage across a whole fight, not just a one-off tension
removal. Caught before pricing it.

**Redesigned instead**: scope the retuning to only the card actually
*kept* for the attack's flip, and have it **add** the matching suit
alongside its natural one (not replace it) — so the discarded Good
Luck card keeps its own real suit, closing the spiral entirely, while
the attack itself still gets a guaranteed Extra Success. New wording:
"the card they keep for that attack's flip counts as matching
whichever suit governs the Skill used for the attack, in addition to
its normal suit if different."

Priced as a guaranteed Extra Success: `+1 Damage` (the rulebook's own
worked example), at Damage's rate (`2/point`, already hit-chance-
discounted) = `2.0/attack`. Full uptime (`own-incidental attacks/
encounter`, 6.25, since this is a permanent always-on effect on every
attack): `Value = 2.0 × 6.25 = 12.5`. `Target (L5) = 15`, `Net = -2.5`
(83% funded) — a clean fit, no Level/Cost change needed. `items.csv`
(`I159`) updated (mechanic rewritten). Regenerated into
`data/items.json`.

### Placeholder's Speedy Scepter = 17.19, capped once/turn, restricted to Shield

"Abilities used with this cost 1 less AP, to a minimum of 1 AP."
First-pass pricing used the standard permanent-effect treatment
(single-instance rate × own-incidental attacks/encounter): `1 AP saved
(2.75) × 6.25 = 17.1875`, `Target (L5) = 15`, `Net = +2.19` (114.6%
funded) — same ratio Reaching Weapon and Spiritlink Scepter both
landed at.

**Caught before locking in**: as originally worded (uncapped), this is
a real exploit. Freeing up AP doesn't just save value on a fixed
number of actions — it lets the wielder fit *more* actions into the
same turn. Normally 4 AP/turn funds 2 actions (2 AP each); at 1 AP
each (minimum), the same 4 AP could fund 4 actions. Each of those
*extra* actions is worth a full action's value (Autoswing, `5.5`), not
just the AP saved (`2.75`) — an uncapped version could theoretically
reach something like `2 extra actions/turn × 5.5 × 5 rounds ≈ 55`,
wildly beyond anything else priced this pass.

**Capped to once per turn** to close this — conveniently, that
reproduces the original single-instance-per-attack framing almost
exactly (6.25 ≈ 5 rounds, allowing for occasional double-attack turns),
so the pricing didn't need to change: `Value = 17.1875`, `Net = +2.19`
(114.6% funded), unchanged from the first pass, just now correctly
bounded by the wording.

**Special crafting restriction added**, per the designer: can only be
applied to a base item whose name begins with "S." Checked this
slot's own Base Item Options list (`I117`-`I126`) — only **Shield**
qualifies. `Base Item Options` restricted to just `I126` as a result.
No dedicated schema field exists for a special per-item crafting
requirement like this (checked `convert.py`'s docstring — the only
existing mechanism is the plain Base Item Options list), so this is
documented directly in the item's own Effects text rather than adding
a new column for what's a one-off rule. Fits the established
"Placeholder's" joke-naming pattern already used elsewhere in this
project (Placeholder's Grasping Gloves, Placeholder's Indelible
Instrument — deliberately whimsical items, not meant to be optimized)
— a "Speedy Scepter" that can only ever actually be built as a Shield.
`items.csv` (`I161`) updated (wording, Base Item Options). Regenerated
into `data/items.json`.

### Blade of Fortune (formerly Scaraculpi's Gleaming Justice) = 15, exact fit

"The wielder has Good Luck on attacks made with this weapon" —
unconditional, permanent, no AP cost. Renamed from Scaraculpi's
Gleaming Justice per the designer (read as accidentally Italian for a
fantasy weapon name; "Sword of Glory" and "Blessed Edge" were also
floated — landed on **Blade of Fortune**).

Priced the same way as every other permanent always-on weapon effect
this pass: single-instance rate × own-incidental attacks/encounter.
`Good Luck (2.4) × 6.25 = 15`, `Target (L5) = 15`, `Net = 0` — an
exact fit, no Level/Cost/Effects changes needed beyond the name.

This also resolves the sanity-check flag `RULES_DESIGN.md` raised when
this item was first drafted: it's a strictly stronger, unconditional
version of Thrumming Focus's (`I103`) AP-gated single Good Luck, both
originally sitting at higher Levels than made sense side by side. That
flag predates Thrumming Focus's own repricing earlier in this pass,
which moved it down to Level 2 (see above) — with Thrumming Focus now
a cheap, AP-gated Level 2 item and Blade of Fortune a pricier,
unconditional, permanent Level 5 one, the two read as a sensible
progression rather than a mismatch. No further action needed on that
flag.

`items.csv` (`I210`) updated (name only). Regenerated into
`data/items.json`.

**This closes out the Held Masterwork slot pass** — every item across
`I089`-`I104`, `I159`-`I161`, `I179`-`I185`, `I227` (Levels 1-5) has
now been confirmed, reworked, repriced, or cut.

### Baseline Weapons pass — a new model for `Category: Weapon` items, no Level/Target of their own

The first pass through the 13 core baseline weapons plus the 3 Goblin
Game firearms (`I117`-`I126`, `I130`-`I132`) — the actual base items
every Masterwork enhancement gets built onto. None of these carry a
`Level`, so unlike everything priced so far there's no `Level × 3/6`
Target to check against. The only meaningful check is *internal*: do
weapons in the same tier cost roughly the same, does Accuracy/Damage/
Weapon Defense trade off sensibly, does Gold scale with power.

**The raw model.** A weapon's "budget" is `Accuracy(1/pt) + Damage
(2/pt) + Weapon Defense(1/pt)`, using the same locked rates as
everywhere else. Comparing raw budgets directly (not multiplied by
attacks/encounter) is valid here specifically because every weapon
shares the same underlying attack cadence — the multiplier is common
to all of them and cancels out in a weapon-to-weapon ranking. Light/
Heavy `1H`/`2H` Melee (`I117`-`I120`) turned out to already be
perfectly matched pairs under this model with zero changes needed —
Light trades Accuracy+WD for Damage relative to Heavy, both landing on
identical totals (8, 10) — confirming the raw model wasn't inventing
anything, just describing what was already there.

**Held-slot opportunity cost = 2, anchored to Shield.** Per the
designer: "the value of a one-handed weapon is lower because you can
use something else in the other hand... my baseline for that is
someone choosing to use a shield for an extra +2 parry defense." This
single number validates itself beautifully against existing data:
`Light 2H Melee's raw (10) = Light 1H's raw (8) + 2` exactly, same for
Heavy (10=8+2) — both pairs were already priced correctly before this
model ever touched them. It also explains Shield itself: a sword-and-
board build (`Light 1H`, 8, + Shield's own +2) totals 10, the *same*
combined value as a two-hander, just redistributed toward defense
instead of damage.

**Target formula: `baseline(8) + 2 (Archery) − 2 (Acrobatics) + 2
(two-handed)`.** Established through a long back-and-forth — see the
full exchange in this project's session history for the complete
reasoning — but the durable result:

- **Archery: +2.** The only combat Skill that feeds zero Defenses and
  has no other listed use at all (`rulebook.md`: *"Marksmanship with
  bows and similar ranged weaponry. It can be used to attack with
  these weapons"* — nothing else). A character investing in it gets
  strictly less back per point than Melee (feeds Parry) or Acrobatics
  (feeds Dodge, fall-damage reduction, general checks). The full
  theoretical gap (a 3-point "primary focus" skill investment × the
  Defense rate) is discounted down to a flat +2 rather than credited
  in full.
- **Acrobatics: −2.** Mirrors Archery exactly, in the opposite
  direction. Two distinct arguments converge here: Acrobatics is
  broader in absolute utility than even Melee's own skill (Dodge +
  fall damage + general checks, vs. Melee's Parry-only), *and* — the
  sharper point — most builds invest *some* Acrobatics for Dodge
  regardless of weapon choice, so a Thrown build's offensive
  investment substantially overlaps with spending it was going to make
  anyway, a genuine marginal-cost efficiency distinct from the
  breadth argument. Per the designer, this is deliberately generous:
  Thrown weapons are meant to read as a flexible, viable backup choice
  for non-combat-focused archetypes (a Rogue, or a spellcaster who's
  run out of spells) without needing to compete on raw power with a
  dedicated build's weapon — "them being usable as melee weapons is
  fine, then they're just worse melee weapons, but they have a real
  upside in being so flexible."
- **Two-handed: +2.** The Held-slot opportunity cost above, applied as
  an *increase to the entitled budget* (the weapon is allowed more raw
  power), not a credit added after the fact that lets it get away with
  less raw power — confirmed against the crucial direction-check: Light
  2H Melee's raw (10) already equals `8+2`, an empirical fact that
  fixed which of the two mathematically-equivalent-looking readings was
  correct before Archery's own sign got decided.
- **Important direction note**, since it was easy to get backwards:
  "budget increased by two" means the weapon is *entitled to more raw
  power*, not that a credit lets it need *less*. Confirmed unambiguously
  from the two-handed case (a known fact, not something being solved
  for) before applying the same direction to Archery/Acrobatics.

**Accuracy stays capped at +1** for every weapon except Unarmed's own
+2 (a deliberate, singular exception, per the designer) — all of this
pass's budget corrections went into Damage (and Range) instead, never
into pushing Accuracy higher.

**A units note, worth remembering the next time a Range-like mechanic
needs pricing**: Accuracy/Damage/WD are *per-event* stats (their value
scales with how often the triggering event — an attack made, an attack
parried — happens over an encounter); the Range value below is a
*per-turn/per-encounter* quantity that does NOT compound with attack
frequency at all — it's about the structure of the fight, not how often
the wielder swings. They're only safely addable because the Range
credit is deliberately expressed in the same "attack-value-equivalent"
units (via the `5.5`-per-attack conversion) before being summed with
the per-event stats — a translation step, not a coincidence. This is
also exactly why the firearms' reload penalty (below) correctly applies
only to the per-event Accuracy+Damage sum and never touches the Range
term: reload reduces how often you attack, which has no bearing on how
delayed the enemy's approach is.

**Reload penalty (firearms) = 0.8×, on the per-event stats only.**
Per the designer: a reload-gated weapon needs 1 AP to reload after
every shot but the last. The real constraint isn't the AP cost itself
— it's that firing twice in one turn would cost `2+1+2=5 AP`, more
than a turn allows, a hard deterministic ceiling (not a probability)
on ever double-attacking. That flattens the firearms' own-incidental
rate to a flat `1.0/turn × 5 = 5.0/encounter`, vs. the `1.25/turn ×
5 = 6.25` baseline everything else gets — a `5.0/6.25 = 0.8×`
multiplier, applied only to `Accuracy+Damage`, never to Range.

**Range value — the longest derivation in this pass**, through
several iterations before landing:

1. First pass treated Range as a small flat "avoided melee's closing
   tax" credit (~1.4), same for every ranged weapon regardless of
   actual meters — this under-priced how much a Bow's real reach is
   worth and forced almost all of the Archery+two-handed budget
   compensation into Damage, which would have made Heavy Bow's Damage
   literally exceed Heavy 2H Melee's — exactly the "tactically better
   *and* straight-up more damage" outcome the designer explicitly did
   not want.
2. Corrected to price Range as **guaranteed extra double-attack
   turns**: `moves_needed(D, Speed 4) = ceil((D−1)/4)` from the Feet
   pass's own breakpoint work determines how many turns the enemy needs
   to close; a "safe turn" (the enemy hasn't arrived yet) is worth
   `(2 attacks guaranteed − 1.25 baseline expectation) × 5.5 = 4.125`.
3. Final shape, a single continuous curve rather than discrete tiers,
   per the designer's own worked proposal ("if each move is 4 meters,
   1 meter of range is 1/8 of a safe turn"):
   - **0 below 6m** — no real tactical benefit that close.
   - **Ramps to 1.375 by 9m** — restores credit for "avoiding
     repositioning to chase a target," which a hard cliff at a single
     threshold was missing entirely; per the designer, "even a few
     points of range can be valuable like that."
   - **+0.515625/meter from 9-12m** (reaching 2.922 at 12m) — the
     steep "denies the enemy's whole turn" zone, `(D−9)/8` safe turns.
   - **Tapers to 1/4 rate (+0.129/meter) beyond 12m** — per the
     designer, past this distance a fight is already "the entire
     battlefield," so further range shouldn't keep adding value at
     the same steep rate.
4. A separate "counters enemy ranged fighters" value stream (return
   fire during the approach instead of eating free hits) was
   considered and explicitly dropped — per the designer, this should
   symmetrically apply to enemy stat blocks too once those get their
   own balance pass, so it nets to roughly zero for *this* pass's
   purposes and isn't worth pricing into player weapons now.

**Final changes locked in this pass:**

- **Light Thrown** (`I121`): Damage `3+[Cunning] → 2+[Cunning]`. Range
  (`3×Body`) unchanged. `Value = Acc(1)+Dmg(4)+Range(9m,1.375) =
  6.375`, `Target = 6` (8−2 Acrobatics), `Net = +0.375` (106% funded).
- **Heavy Thrown** (`I122`): Damage `4+[Body] → 3+[Body]`. `Value =
  0+Dmg(6)+1.375 = 7.375`, `Target = 6`, `Net = +1.375` (123% funded)
  — deliberately left generous rather than trimmed further, per the
  designer's explicit "err on the side of over-valuing their
  capabilities" for this weapon line's flexibility.
- **Light Bow** (`I123`): Range `15 → 19`. Accuracy/Damage untouched
  (`+1`/`3`), per the designer — only Range was to move. `Value =
  1+6+3.825 = 10.825`, `Target = 12` (8+2 Archery+2 two-handed),
  `Net = −1.175` (90% funded).
- **Heavy Bow** (`I124`): Range `20 → 17` — swapped with Light Bow
  into a "hard-hitting, shorter reach" identity (the inverse of
  Light's "precise sniper, longer reach"), since the model's own math
  wanted Light's lower raw stats to need *more* Range credit than
  Heavy's to hit the same Target, inverting the naive intuition that
  "Heavy" should also mean "longer ranged." `Value = 0+8+3.567 =
  11.567`, `Target = 12`, `Net = −0.433` (96% funded).
- **Unarmed** (`I125`), **Shield** (`I126`): confirmed as-is, no
  changes — see the model notes above for why each sits deliberately
  below the 1H attacker baseline.
- **Handgun/Blunderbuss/Musket** (`I131`/`I130`/`I132`): confirmed
  as-is, no changes — all land within 88-106% funded once the reload
  penalty and Range curve are both applied, close enough given the
  designer's own "long range is too context-sensitive to land a
  perfectly balanced number" allowance. Blunderbuss is the loosest fit
  (88%) but carries its own unpriced Good Luck(≤5m)/Bad Luck(10-15m)
  clause likely closing some of that gap.

`items.csv` (`I121`-`I124`) updated. Regenerated into `data/items.json`.

### Baseline Armor pass — 3 tiers, a genuinely different balance shape than Weapons

The second and final piece of the Baseline items work, after Weapons
above — `I128`/`I129` (Light/Heavy Armor) plus a new `I127` Medium
Armor, reworking the old 2-tier system into 3.

**Why this couldn't reuse the Weapons model directly.** Every Weapon
stat (Accuracy, Damage, Weapon Defense) has build-independent value —
everyone attacks at roughly the same cadence, so comparing raw budgets
directly was valid. Physical Resist doesn't work that way: its
*realized* value scales with how many hits the wearer actually
absorbs, a property of the wearer's build, not the armor. This project
already has a rate for exactly this case (`Tank / above-average attack
draw`, `×1.5` example, `balance_weights.csv`) — a flat single-scenario
raw-value comparison will always make heavier armor look like a
mediocre trade for an "average" character while understating its real
value for the dedicated-tank archetype it's actually built for.

**Resolved by checking every tier under two lenses** rather than one —
generic party member (baseline hit-draw) and dedicated tank (`×1.5` on
the Resist component only, since Speed/Dodge penalties are flat costs
that don't scale with how tanky the build is):

| Tier | Resist | Speed | Dodge | Generic value | Tank value | Tank/Generic |
|---|---|---|---|---|---|---|
| Light | 1 | 0 | 0 | 5.0 | 7.5 | 1.50× |
| Medium | 2 | 0 | −1 | 9.0 | 14.0 | 1.56× |
| Heavy | 3 | −1 | −1 | 11.46 | 18.96 | 1.65× |

Heavy reads as a mediocre, easily-skippable trade under the generic
lens — deliberately, since that's not who it's for. Under the tank
lens it pulls further ahead than Light does (1.65× vs. 1.50×), because
it has more Resist for the multiplier to amplify against the same flat
penalty cost — the mechanical shape behind "dedicated tanks really
synergizing with higher Resist provide real value," not just a vibe.

**Reframed the design goal.** Not "no tier should be better than
another" (a single-axis target that doesn't fit a build-dependent
stat), but **"no tier should be better than another *for the same
build*"** — a genuine two-way tension: a squishy character in Heavy
Armor should feel like a real mistake (paying Speed/Dodge costs for
Resist they'll never draw enough hits to cash in), and a dedicated
tank in Light Armor should *also* feel like a missed opportunity
(leaving Resist value on the table their build was built to
capitalize on). Both being true at once is success, not a sign the
tiers are failing to converge on one "best" answer.

**The tier shape**: Light = no penalty, Medium = one penalty
dimension, Heavy = both — matching "somewhat more flexible" (Medium)
vs. "more pronounced" (Heavy) directly. Checked which single stat
Medium should sacrifice: Dodge (`raw 9.0`) vs. Speed (`raw 7.46`) leave
different raw totals since Dodge's rate (1/pt) is cheaper than Speed's
(2.54375/pt) — meaning a genuine free choice between the two would have
a dominant strategy (always take Dodge), not a real decision. Fixed
Medium's penalty at Dodge specifically instead, per the designer:
"you really only start picking up heavier armor once you're planning
on either using Parry or just killing dudes faster than they hurt
you... a Barbarian archetype might go Medium since their Dodge isn't
very good regardless... but the Speed penalty starts biting so they
don't go all the way to Heavy unless they're more of an actual Tank
type." Speed specifically gates the jump to Heavy, not Might or Gold.

**Final changes:**

- **Light Armor** (`I128`): confirmed as-is, untouched — the anchor
  tier everything else compares against, and also the anchor for the
  "average attack nets ~2-3 over Resist" assumption (see
  `RULES_DESIGN.md`'s new note) — baseline weapons at zero Stat
  investment already land almost exactly on this against Light
  Armor's Resist.
- **Medium Armor** (`I127`, new): Resist 2, Speed 0, Dodge −1, Might
  Req 4, 6 Gold. `Value = 9.0` generic, `14.0` under the tank lens.
- **Heavy Armor** (`I129`): Physical Resist `2 → 3` (Speed −1/Dodge
  −1/Might 6/Cost 8g unchanged). `Value = 11.46` generic, `18.96`
  tank-lens — directly fixes the problem that prompted revisiting this
  at all: the old 2-tier Heavy paid double Light's Gold for only ~29%
  more raw value (`10.0−2.54−1=6.46` at the old Resist 2), a bad deal
  under any build, not just the wrong one.
- **Gold kept to a simple 4/6/8 linear scale**, deliberately not used
  as a real balancing lever — per the designer, all Armor should stay
  inexpensive; the actual tradeoff lives entirely in the stat
  penalties, not the price tag.
- **Unarmored** (`I002` Basic Clothing) and the Might Requirement
  gating (Light 3, Medium 4, Heavy 6, unchanged/interpolated) both
  confirmed as-is — see `RULES_DESIGN.md`'s "Unarmored as an opt-in
  archetype choice" note. Might Requirement gates access to the higher
  tiers rather than buying extra budget, the same rule established for
  Weapons' Heavy variants.
- `crafting_recipes.csv` gained `CR018`/`CR019` (Medium Armor via
  Tailoring/Smithing, Craft 4) and all 9 Torso-slot Masterwork items'
  `Base Item Options` now include `I127` alongside `I128`/`I129`/`I002`.
  `armor_categories.csv` (a small unconsumed reference table, per
  `convert.py`'s own comment) updated to a matching 3-row AC001-AC003.

`items.csv` (`I127` new, `I129` Resist changed), `crafting_recipes.csv`,
`armor_categories.csv` updated. Regenerated into `data/*.json`.
Verified in a sandboxed Playwright pass (Items tab search/add for all
three tiers, Crafting tab's Medium Armor recipe dropdown) — no console
errors, all three tiers and the new recipe render correctly.

### Armor follow-up — variable-material upgrade recipes, tightened Might Requirements

A quick follow-up pass on the 3-tier Armor system above, prompted by
wanting Armor's crafting to support upgrading an existing suit into a
higher tier rather than only building each tier from scratch, plus a
deliberate tightening of the Might Requirement gates.

**Might Requirement: Light 3 (unchanged), Medium 4→5, Heavy 6→7.**
Might is governed by the Body Stat (`STAT_SKILLS.Body` in `index.html`
includes Might), so Might's Skill Total = Body Stat points + Might
Skill points. At character creation, the absolute ceiling for a
character who fully dumps into it (Body as their one 3-rank primary
Stat, Might as one of their two 3-rank primary Skills) is `3+3=6`. Per
the designer: "I don't want heavy to be available at character
creation, but shortly after" — **Heavy's Might Req 7 sits exactly 1
point past that creation-time ceiling**, so it's mathematically
unreachable at creation and opens up after a single Experience-funded
Body or Might rank-up. Medium's 5 is reachable at creation but needs a
real, non-token investment (e.g. a 2-rank secondary Stat + 3-rank
primary Skill, or the reverse) — not something every build clears by
accident the way Light's 3 is.

**Variable-material Armor upgrade recipes** — a suit of Armor can now
be built by reinforcing an existing lower tier instead of only from
scratch, paying just the Total Materials *difference* between tiers
(Light=4, Medium=6, Heavy=8, so Light→Medium=2, Medium→Heavy=2,
Light→Heavy=4) at the same Craft requirement and crafting time as
building the target tier fresh. Per the designer, kept simple as plain
additional recipe rows (the same pattern already used for a School
choice) rather than a new rulebook rule — no new mechanic for players
to learn, just more entries in the same picker:

| Recipe | School | Craft | Materials |
|---|---|---|---|
| Medium ← Light (Tailoring) | Tailoring | 4 | 2 |
| Medium ← Light (Smithing) | Smithing | 4 | 2 |
| Heavy ← Medium | Smithing only | 5 | 2 |
| Heavy ← Light | Smithing only | 5 | 4 |

Medium's upgrade path got both Schools (mirroring its own fresh-build
duality), per the designer; Heavy's upgrade paths stay Smithing-only
either way, matching Heavy's own fresh-build restriction — reinforcing
into plate is a metalworking job regardless of what the base armor
was built from.

**Two real bugs found and fixed while wiring this up, not just data
entry:**

1. **A genuine CSV-quoting corruption** — `CR020`/`CR021`'s Name field
   (`Armor - Medium (Upgrade from Light, Tailoring)`) contains an
   unquoted comma, which silently shifted every field after it by one
   column (the Description ended up in the School column, etc.).
   Exactly the failure mode `CLAUDE.md` warns about hand-editing CSVs
   outside a tool that understands quoting — caught by actually
   checking the converted JSON output before trusting it, not by
   assuming the edit worked. Fixed by quoting the Name field properly.
2. **A real precedence bug in `index.html`'s `recipesForItem`** — the
   merge logic let an item's own `total_materials` *always* win over a
   recipe's, which happened to work for every existing recipe (they
   all leave Total Materials blank at the recipe level, relying on the
   item's default) but would have made these new upgrade recipes
   silently ignore their own reduced material counts and just show the
   item's full fresh-build number — defeating the entire point of the
   feature without any visible error. Fixed by flipping the precedence
   specifically for Total Materials: a recipe's own value now wins
   when set, falling back to the item's default otherwise — fully
   backward compatible, since every pre-existing recipe still leaves
   it blank. Also fixed the crafting picker's option labels, which
   used only the recipe's School name (`via Tailoring`) — two recipes
   sharing a School (a tier's fresh-build and upgrade recipes) would
   have rendered as identical, indistinguishable dropdown options.
   Now falls back to the recipe's own parenthesized name suffix
   whenever more than one variant shares a School.

`items.csv` (Might Req changes), `crafting_recipes.csv` (4 new
recipes, `CR020`-`CR023`), `armor_categories.csv` (Might Req updated),
and `index.html` (the two fixes above) all updated. Regenerated into
`data/*.json`. Re-verified in the sandboxed Playwright pass: all three
Armor tiers' full recipe picker (fresh + upgrade variants) render with
correct, distinguishable labels and correct Materials counts for every
option, Might Requirements display correctly on all three tiers, no
console errors.

### Vigor = 4.5/point — a reusable Technique-refund pool

Vigor (`glossary.md` Keyword) is a spendable pool that recovers an
expended Encounter Technique: spend Vigor equal to that Technique's own
Level to regain a use of it. Introduced this pass to unify two items/
techniques that had independently reinvented the exact same mechanic
under different names — Soul Soup's "Nutrition points" and Solemn
Covenant's (`T022`) "Covenant points" — but it's written up here as its
own weight, not just a rename, because the underlying math turns out to
reduce to a clean, flat, reusable per-point rate.

**Derivation.** The refund-trick family (Soldier's Salts/Fighter's
Friend/Battlemaster's Brew/Soul Soup, see `balance.md`) already
established that outright refunding a Technique of Level N is worth
`1.5 × (N × 3)` = `4.5N` — the refunded Technique's own `Target` budget
(`Level × 3`), plus a ×1.5 premium for the flexibility of choosing
*which* Technique and *when*. Spending Vigor to recover a Level-N
Technique costs exactly N Vigor, so the value realized per point spent
is `4.5N ÷ N` = **4.5**, independent of N. This isn't a coincidence to
re-derive per item — it's a property of the refund-trick formula itself
being linear in Level, the same way `1 AP`'s rate (2.75) falls straight
out of Autoswing's, not a fresh judgment call each time it's used.

Confirmed against Soul Soup's own worked numbers at every Level (not
just asserted): Level 1 grants 2 Vigor for Value 9 (4.5/point exactly);
Level 3 grants 4 Vigor for Value 18 (4.5/point exactly); the pattern
holds at every Level since both the grant formula (`[Level]+1`) and the
refund-trick Value formula are linear in Level.

**Use this rate directly for any future "recover a Technique" design**,
the same way Good Luck (2.4) or Card (2.7) are reached for directly
rather than re-deriving the underlying card math each time: price a
new Vigor-granting item/technique as `(Vigor granted) × 4.5`, no need
to work back through the refund-trick formula unless the design itself
changes (e.g. a different premium, or a mechanic that isn't a flat
pay-Level-in-Vigor spend).

**One caveat, not yet fully priced in either direction:** Vigor is a
genuine spendable *pool*, not a single redemption — a character holding
6 Vigor can split it across two separate Technique refunds (a Level 5 +
a Level 1, or two Level 3s) rather than needing one hypothetical
"Level 6" Technique the flat rate implicitly assumes when granted in a
single lump sum near a Technique-Level ceiling. That flexibility is
real value the flat 4.5/point rate doesn't capture, so treat 4.5/point
as a reasonable floor for a Vigor grant sized well within the 1-5
Technique-Level range, and a likely-conservative floor for a grant
large enough that splitting it matters (see Soul Soup's own Level 5
case in `balance.md`, granted uncapped for exactly this reason).


## Enemy Stat Block by Level — revised around the designer's own past XP-tier methodology

**In turn superseded by `design/ENEMY_ENCOUNTER_DESIGN.md`.** The
designer then found the actual spreadsheet this XP-tier recollection
was describing (`archive/flagonquest_encounter_builder.xlsx`) — a
complete, already-tested point-buy system (Role archetypes,
Primary/Secondary Defense tiering, Battle Tactics/Fighting Style
pickers, a full Ability catalog, real worked examples), well past what
this section reconstructed from memory alone. Left below as the record
of that reconstruction attempt, not because it's still the thing to
build enemies from.

**Supersedes the first-draft version of this section** (see git history
for the original, `1e172e5`..`cf8470b` if it's still needed for
reference). That draft built enemy Stat/Skill Total purely from the
"grenade base stat 3-5 by Level" convention with no real anchor for
Skill Total specifically. The designer then recalled having actually
built this before, with a real methodology: draft what a same-XP-tier
PC's stats would realistically look like (accounting for XP that goes
to non-combat Skills, not just combat ones), then give enemies a slight
stat discount off that, plus a separate spare budget for special
abilities. This section rebuilds around that — genuinely better
grounded, since it starts from the actual character-progression math
instead of a combat-only proxy. `Primary Stat`, `Resist`, and `Health`
below are **unchanged** from the first draft (they weren't derived from
a PC baseline to begin with — see their own reasoning below); `Skill
Total`, `Defense`, and the new `Ability Budget` column are the
genuinely new parts this revision adds.

### Tiers are XP-based, not Level-based

Per the designer's own recollection: **75 XP for Tier 1** (this
project's actual chargen budget, `rulebook.md`), **+50 XP per tier
after that** — 75/125/175/225/275 for Tiers 1-5. This is a different
axis than the existing Technique/Masterwork Level 1-5 scale (which
tracks *item* power, not *character* power) — the two happen to share a
1-5 range and roughly correspond in practice, but aren't the same
measurement. "Level" in the rest of this table means "Tier" in this
sense going forward.

### Step 1: what would a same-tier PC's Skills/Stats/Techniques spend actually look like

Verified against `rulebook.md`'s own worked chargen example first,
since it's the one real data point that exists for this: "2 Skills at 3
ranks, 5 Skills at 2 ranks, 2 Skills at 1 rank; 1 Stat at 3 ranks, 2
Stats at 2 ranks, 2 Stats at 1 rank each; 6 total Levels' worth of
Techniques." Actual XP cost of that exact spread (Skill cumulative cost
to rank N is `N(N+1)/2`, Stat is double that, Technique is `3×Level`,
all per `rulebook.md`'s Spending Experience section):

`Skills: 2×6 + 5×3 + 2×1 = 29. Stats: 1×12 + 2×6 + 2×2 = 28. Techniques: 6×3 = 18. Total: 75.`

Confirms exactly — 29+28+18 = 75, matching the stated 75 XP chargen
budget and the "6 total Levels' worth of Techniques" line precisely.
Ratio: **Skills ~39% / Stats ~37% / Techniques ~24%.**

**Per the designer, Techniques should take a growing share at higher
tiers** (a mature character's identity leans more on its ability kit
than raw stats by that point), Skills/Stats a shrinking one. Modeled as
Techniques' share climbing **+6 percentage points per tier** from that
24% anchor, with the remaining Skills/Stats split kept at the same
~51:49 ratio chargen's own example uses:

| Tier | XP | Techniques (XP) | Skills (XP) | Stats (XP) |
|---|---|---|---|---|
| 1 | 75 | 18 (24%) | 29 | 28 |
| 2 | 125 | 38 (30%) | 44 | 43 |
| 3 | 175 | 63 (36%) | 57 | 55 |
| 4 | 225 | 94 (42%) | 67 | 64 |
| 5 | 275 | 132 (48%) | 73 | 70 |

**This Skills-XP figure covers a whole character, not just their combat
Skill(s)** — per the designer's own framing, "players didn't just spend
XP on combat stats, some are other things like Awareness and social
stuff." A real same-tier PC (or a same-tier NPC contact/ally the GM
wants to gauge, not just an enemy) plausibly has meaningful Persuasion,
Streetwise, Academics, or whatever else alongside their combat kit —
this table doesn't try to model that breadth explicitly (it's out of
scope for a *combat* stat block, and the Social Encounter Baseline
above already covers the social-encounter case separately), but it's
worth keeping in mind reading the numbers below: they represent a
PC's *best* combat investment specifically, not their whole sheet.

### Step 2: the representative PC's combat Skill Totals

**Main Skill Total** (their best combat Skill + its governing Stat,
the "specialize" choice): `6 / 7 / 8 / 9 / 10` across Tiers 1-5 — a
clean +1/tier climb that lands exactly on real anchors already
established elsewhere in this project: Tier 1 = 6 (the exact chargen
ceiling, `3+3`, matching the real chargen example's own top skill+stat
pick), Tier 2 = 7 (`RULES_DESIGN.md`'s "skilled ordinary craftsperson"
ceiling), Tier 5 = 10 (the absolute Skill Total cap, `5+5` — the same
ceiling the separate Masterwork/Alchemy crafting-difficulty curve also
tops out at).

**Secondary Skill Total** (whichever other combat-relevant Skill+Stat
covers a different Defense — Dodge/Vital/Mental/Vigilant aren't all
governed by the same Skill as a character's main weapon): `Main − 2` —
`4 / 5 / 6 / 7 / 8`. The `−2` offset isn't arbitrary: it's exactly what
chargen's own worked example gives for a plausible second-best
pick (one of the "2 ranks" Skills + a "2 ranks" Stat = Skill Total 4,
against the top pick's 6).

### Step 3: the enemy discount

Per the designer, **a percentage discount, landing on ~85%** (splitting
the stated 85-90% range) applied to both Skill Total lines, rounding to
the nearest whole number (ties round down, in the enemy's *weaker*
direction, consistent with the discount's own purpose):

| Tier | PC Main | Enemy Main (×0.85) | Gap | PC Secondary | Enemy Secondary (×0.85) | Gap |
|---|---|---|---|---|---|---|
| 1 | 6 | 5 | 1 | 4 | 3 | 1 |
| 2 | 7 | 6 | 1 | 5 | 4 | 1 |
| 3 | 8 | 7 | 1 | 6 | 5 | 1 |
| 4 | 9 | 8 | 1 | 7 | 6 | 1 |
| 5 | 10 | 8 | 2 | 8 | 7 | 1 |

**The gap grows on its own at Tier 5** (2, versus a flat 1 everywhere
else) — not a separate rule bolted on, just what a flat percentage
naturally does once the PC number itself gets big enough (10×0.85=8.5,
rounding down). This matches the designer's own stated expectation
("bigger absolute gap at high tiers") without needing a sliding
percentage.

**Enemy Defense = 8 + Enemy Skill Total** (identical formula to PCs, no
new rule) — Main-line Defense `13/14/15/16/16`, Secondary-line
`11/12/13/14/15`. **Enemy Accuracy** uses the same discounted Skill
Total directly (flip a card + Enemy Skill Total vs. the target's
Defense) — the discount applies uniformly to the enemy's own offense
and defense both, not just one side.

### Primary Stat, Resist, Health — unchanged from the first draft, and why they don't get the new discount

These three were never derived from a PC-tier baseline in the first
place, so this revision doesn't touch them:

- **Primary Stat** (`3/3/4/5/5`) is the "grenade base stat 3-5 by
  Level" convention — already an **enemy-facing** number by its own
  original citation ("the on-level-*enemy* Body proxy"), not a PC
  number that needs a further discount applied on top. Applying the new
  85% discount here too would double-discount an already-enemy-scoped
  figure.
- **Resist** (Physical `4/4/5/6/6`, Elemental `3/3/4/5/5`) reuses the
  already-Locked Fresh-attack Resist placeholder convention
  (`Stat + 1` for Physical, `Stat` alone for elemental) directly off
  Primary Stat above — unaffected by this revision for the same reason.
- **Health** (flat **6** at every Tier, Standard tier) is unchanged
  too: it comes from `2 hits × (Heavy 1H Melee Damage − Physical
  Resist)`, both of which key off Primary Stat, not the newly-revised
  Skill Total. Net/hit still works out flat at 3 (`7−4, 7−4, 8−5, 9−6,
  9−6`), so Health stays flat at 6 — see the original derivation
  (below the fold in git history) if the full walkthrough is needed;
  the Minion/Standard/Elite/Boss tier multipliers (×0.5 / ×1 / ×2 /
  ×3-4) are also unchanged.

### Step 4: the ability budget

Per the designer, this should be **a literal XP number, spent like
Technique costs** — a GM can pick real Techniques (`3×Level` XP each)
off the existing catalog within budget, or reskin a couple, rather than
inventing a parallel enemy-only ability system. Uses the **undiscounted**
Techniques-XP figure from Step 1's table directly (`18/38/63/94/132`) —
the ability budget isn't stat power being compared apples-to-apples
against a PC's own combat stats, so it doesn't need the same 85% cut;
treat it as a ceiling, not an obligation to spend all of it, and not
every ability needs to be combat-relevant (a signature non-combat trait
fits just as well as an attack technique, same as it would for a PC).

### Full Tier 1-5 reference table (Standard tier)

| Tier (XP) | Primary Stat | Main / Secondary Skill Total | Main / Secondary Defense | Physical / Elemental Resist | Heavy 1H Damage | Health | Ability budget (XP) |
|---|---|---|---|---|---|---|---|
| 1 (75) | 3 | 5 / 3 | 13 / 11 | 4 / 3 | 7 | 6 | 18 |
| 2 (125) | 3 | 6 / 4 | 14 / 12 | 4 / 3 | 7 | 6 | 38 |
| 3 (175) | 4 | 7 / 5 | 15 / 13 | 5 / 4 | 8 | 6 | 63 |
| 4 (225) | 5 | 8 / 6 | 16 / 14 | 6 / 5 | 9 | 6 | 94 |
| 5 (275) | 5 | 8 / 7 | 16 / 15 | 6 / 5 | 9 | 6 | 132 |

Same tier system as before for Health (Minion ×0.5, Standard ×1, Elite
×2, Boss ×3-4) and for Boss's own Skill Total bump (Main/Secondary +2,
capped at the absolute Skill Total ceiling of 10 — using the new
Standard-tier numbers above, that's `7/5` at Tier 1 up to `10/9` at
Tier 5), plus the same encounter-shape reference (4 Standard-tier
enemies vs. a 4-player party, ~5 rounds) — none of that changed by this
revision.

### Known limitations, carried over and updated

- **The Skills-XP figure includes non-combat investment by design**
  (see Step 1) — this table still only outputs *combat* numbers. It
  doesn't attempt to quantify a same-tier NPC's social/utility Skills;
  use the Social Encounter Baseline above for that side of things.
- **The Tier-to-Skills/Stats/Techniques ratio curve (Step 1) is a
  clean, chosen shape** (+6pp/tier to Techniques' share, matching
  chargen's own ratio otherwise), not something independently
  verified against actual higher-tier play — there's no documented
  "how does a real character's spend evolve past chargen" curve
  anywhere else in this project to check it against.
- **The 85% enemy discount is applied only to Skill Total/Defense/
  Accuracy, not Primary Stat/Resist/Health** — a deliberate choice
  (see the "unchanged" section above), not an oversight, since those
  three were already enemy-scoped rather than PC-derived.
- **Non-combat enemies aren't what this table is for** — same caveat
  as before; use the Social Encounter Baseline for a social antagonist.
- **The Boss tier's Health multiplier and Skill Total bump are still a
  judgment call**, not derived the way the rest of this table is —
  flagged the same way any Narrative Utility item's honest-guess
  convention is.

## Feint (T074) and the Martial Techniques pass — Vigilant Defense modeled, a real Gambling AI bug found, and a standing lesson on how to price moment-specific effects

Feint ("Make a weapon attack against the target's Vigilant Defense.
Instead of normal effects, if it hits then the target is Harried
3 + [Diamonds] times", 1 AP, Level 1, Encounter) looked badly
underpriced on a first pass (~0.43 Value against a 5.5 budget — see
"the budget" derivation below) and ended up **confirmed fine as
written** once the simulator's own modeling caught up to what the
Technique actually does. Three real findings came out of chasing that
gap down, all worth keeping for future work, not just this one
Technique.

### Vigilant Defense is now modeled for enemies

`ENEMY_ENCOUNTER_DESIGN.md`'s Defense tiering used to cover only three
categories (Parry/Dodge, Bodily, Mental) — Vigilant was explicitly
left out of the original spreadsheet, "a deliberate simplification,
not an oversight," per that doc's own prior text. That made Feint's
real hit rate against a typical enemy unanswerable, since it's the
one Technique in the catalog that specifically targets Vigilant.
Extended to four categories (1 Primary + **2** Secondary picks now,
not 1, to keep the "exactly one clear weakness" shape intact — see
that doc's own updated section for the full reasoning), wired into
both `enemy_builder.py` (now takes `secondary_defs`, a pair) and
`enemy_builder_pcstyle.py` (a fifth independent tier), and into
`combat_sim.py`'s `enemy_defense_for_pc_attack` (`pc['opp_def'] ==
'Vigilant'`, no Harried subtraction — Harried is Dodge/Parry only).
Existing `sample_enemies.csv` rows leave their new `SecondaryDef2`/
`VigilantTier` blank until a real design pass assigns them, flagged
rather than guessed.

### A real bug in `pc_gamble_count`, not just Feint's own math

Checking Feint's value meant checking what happens once a target's
Defense is cratered by several Harried stacks and a teammate attacks
it next — and that surfaced a genuine simulator bug, independent of
Feint: `pc_gamble_count`'s "plenty of Skill Total to spare" branch
used to gamble until the *average* card (7) would still clear
Defense, which is exactly a 50/50 shot on that maxed-out attempt, not
the "safe bet... can usually Gamble freely" rulebook.md actually
describes. Confirmed empirically before the fix: a follow-up attack
against a 7-stack-Harried target had a *lower* hit rate (53.0%) than
a normal, unbuffed attack in the same fights (74.4%) — the old
heuristic was spending the crater on marginal extra damage instead of
on actually landing the hit.

**The real fix wasn't a tighter constant, it was solving the actual
optimization problem.** Card values are uniform 1-13, so
`P(hit | n gambles)` is exactly linear in `n`, which makes
`E[net damage] = P(hit|n) × (successes on a hit)` a single-peaked
(concave) function of `n` — there's one true EV-maximizing gamble
count, not a threshold to eyeball. `pc_gamble_count` now evaluates
every candidate `n` from 0 up to the point even a 13 can't hit, and
picks whichever maximizes expected *net* damage (post-Resist) — one
unified pass instead of the old two separate hand-tuned branches
(Resist-wall vs. normal). Worked out analytically, the EV-optimal
count is `n* = (S - D + 12) / 4` (roughly *half* what the old "average
card clears" heuristic gambled for the same margin), landing at a hit
chance around **half of your zero-gamble hit chance, not a flat
50/50** — but the actual code just searches directly rather than
trusting a closed form at every edge case, since a real Resist wall
shifts which `n` pays off in a way the plain formula doesn't reflect
on its own.

**This is a standing rule for any future Gambling-adjacent balance
check, not just Feint**: when evaluating whether a target's cratered
Defense is worth exploiting, don't assume "gamble until it's still
likely to hit" — compute the actual EV-maximizing count (or just run
`pc_gamble_count`'s own logic, which now does this correctly), since
the naive threshold either over- or under-commits depending on how
big the margin is.

After the fix, the same follow-up-attack check read 79.4% hit rate
(now *above* the 72.4% normal-attack control, matching intuition) at
9.21 average raw damage when it hits — a real, large improvement, not
just a smaller number.

### Measure the moment, not just the aggregate win-rate delta

Even with the Gambling fix, Feint's value measured against the
**whole-fight win-rate delta** (the same method used for Backfoot/
Stagger/Outflank and the Advanced Cost-6 trio) stayed noisy and
inconclusive — bouncing between roughly -2 and +2 Value across a
sweep of Harried-stack counts, indistinguishable from zero at
reasonable trial counts. That's not because Feint has no value; it's
because **the whole-fight win-rate delta is the wrong tool for a
mechanic whose value is concentrated in one specific follow-up
moment, not spread evenly across a whole fight.** A single ~4.6-net-
damage swing is real and substantial in the moment it happens, but
it's a drop in the bucket against everything else a 20+-round,
4-enemy fight decides on — diluted into noise by the aggregate
metric, even though the underlying effect is large and reliable.

**The fix: measure the specific moment directly against a matched
control**, not the whole fight's outcome. Isolated the actual
follow-up attack(s) against the Feinted target, compared their
expected *net* damage (post-Resist, not raw) against a same-fight
control attack against a different, non-Feinted target:

- **One follow-up** (whichever party member attacks the Feinted
  target next): 79.4% hit / 5.78 avg net damage when hit = **4.59
  expected**, vs. control's 72.4% / 2.54 = **1.84 expected**. Delta =
  **2.75 net damage**. Converted at the *guaranteed* rate (4/point,
  Health's own rate — not the hit-discounted 2/point, since the delta
  is already probability-weighted, so discounting it again would
  double-count): **Value ≈ 11.0** for that one follow-up alone.
- Feint only lands on a trackable follow-up in **46.0%** of fights
  (the rest of the time there's no living second attacker on that
  target soon enough) — blending that in: `0.460 × 11.0 ≈ 5.0`,
  landing almost exactly on the budget below.
- **Two follow-ups** (crediting a second party member attacking the
  same still-Harried target, which the decay rule — clears at the
  *bearer's own* turn end, not after one attack — genuinely allows):
  follow-up #2 only shows up in 57.1% of Feint-landings (the target
  or turn order doesn't always cooperate), so its own delta (+1.18 net
  damage) gets weighted by that incidence: `2.75 + (0.571 × 1.18) ≈
  3.42` net damage per landing, **Value ≈ 13.7** once Feint lands at
  all, **≈ 6.3** fully unconditional (`0.460 × 13.7`).

**The budget it's being checked against**: for a 1 AP, Level 1
Encounter Technique, the designer's own call was to price it against
Autoswing (5.5, "value of one full extra attack") rather than the
generic `3 × Level` Technique-value rate — reasoning that a Technique
this cheap, replacing a whole attack action, should be judged against
what a full extra attack is worth, not the flatter per-Level curve.
**Verdict: Feint's real value (≈5.0-6.3, crediting one or two
follow-ups) meets or exceeds that 5.5 budget — left as-is, no change,
Cost still 1 AP.** The earlier "badly underpriced" read was an
artifact of the Gambling bug and the wrong pricing metric, not a real
problem with the Technique.

**Standing lesson for future balance checks**: if a mechanic's payoff
is concentrated in a specific follow-up action or narrow window
(cratering Defense for an ally, a one-shot setup effect, anything
that reads as "this enables something else" rather than "this
directly deals with the outcome") — measure that specific moment's
expected value against a matched control, the way this pass did,
rather than trusting the whole-fight win-rate delta to surface it.
The aggregate metric is the right tool for something whose value is
genuinely spread across the whole fight (Stagger, Flurry, straight
Damage/debuff Features); it's the wrong tool for something whose
value lives in one narrow, specific moment - Backfoot/Stagger already
showed composition-dependence is real, and this pass adds "diluted
into noise by fight length" as a second, distinct way the aggregate
metric can mislead.

## Magehunter (T075) — a real Interrupt-window model, corrected after a real AP-timing bug in the first pass

T075 Magehunter (Level 1, "1 AP - Interrupt (a creature within your
weapon's range declares a Spell, before it is cast)"): "Make a weapon
attack against the target. You may use a Technique instead, as long
as it has you make a weapon attack against the target and takes no
more than 2 AP to use." combat_sim.py had no concept of Interrupts at
all before this pass — every turn was processed atomically per-unit,
so there was no way to let a PC act on an enemy's turn. This needed
real interrupt-timing logic, not another `_bonus_attack`-style
synthetic flag layered onto the PC's own turn (Whirlwind/Flurry/
Feint's pattern).

**First pass got the AP-refresh timing backwards.** rulebook.md's own
text: "When you flip Reflex to join an encounter, and AGAIN AT THE
END of each of your turns, you lose any existing Action Points and
gain 4 Action Points in their place." The first version of this model
read that as "reserve AP at the *start* of every turn, just in case" —
`_take_pc_turn` unconditionally cut a Magehunter PC's own-turn budget
from 4 AP to 2 (giving up a whole attack) on EVERY turn, whether or
not an Interrupt ever actually fired. That's not what the rule says:
the refresh happens at the *end* of a turn, as a flat, unconditional
reset to 4 AP — completely independent of whether that AP ever gets
tapped for an Interrupt. A PC who never gets a valid trigger loses
*nothing* relative to a normal PC, because that AP was just going to
sit idle and get reset again regardless — there's no "reservation" to
pay for up front. The designer caught this directly: "they don't have
to spend the action point until basically the trigger happens...
they're not spending it ahead of time" — and predicted the technique
should land close to on-budget (~3 Value, the Level 1 Technique-value
anchor), with a real floor of "no net loss" even in a fight with zero
casters, since the idle AP was never going to do anything else anyway.

**The corrected model** (`combat_sim.py`): a real persistent counter,
`pc['ap_bank']`, replaces the old boolean `magehunter_ready` flag.
Initialized to `T.AP_PER_TURN` (4) once at encounter start (the
Reflex-flip refresh, in `run_fight`). On a Magehunter PC's own turn,
`_take_pc_turn` spends from `ap_bank` as that turn's starting AP
(normal 2-attack turns whenever nothing's been spent from it since
the last refresh) rather than a fixed 4; at the END of that turn,
`ap_bank` unconditionally resets to a fresh 4, matching the rule's
own "flat reset, not an accumulation" shape. `_magehunter_interrupt`
(called from `_take_enemy_turn` whenever `e['action']` is a Spell
Action, before that attack resolves) now checks/spends real AP
(`T.MAGEHUNTER_AP_COST`, 1 — its own printed cost, not
`T.ATTACK_AP_COST`) from that same pool, and can fire more than once
in the same window if enough is left (several casters triggering
before the PC's next turn). The interrupt attack itself is unchanged
from the first pass — full weapon-attack math, Gambling included, a
kill ends the enemy's turn before its own attack resolves (still
confirmed directly: 52/500 seeded trials against a low-Health lone
caster killed it before its own attack fired).

**Re-tested the same three matchups, plus a genuine zero-caster
control** (`movement=True`, Autoswing-`bonus_attack_control`
calibration in the same matchup each time):

| Matchup | Baseline win% | Magehunter win% | Δ | Autoswing control Δ | Value |
|---|---|---|---|---|---|
| Level 1 mixed roster (1 of 4 enemies casts) | 65.12 | 63.54 | -1.58 | +6.35 | -1.37 |
| 4× Fen Warden (all Melee Spell, saturated ~95%) | 95.47 | 96.17 | +0.70 | +0.42 | +9.06 |
| 5× Fen Warden (all Melee Spell, unsaturated ~59%) | 59.87 | 65.63 | +5.77 | +8.25 | +3.84 |
| 4× all-weapon, zero casters (Hedge Knight/Marsh Archer/Skulking Footpad) | 46.02 | 46.30 | +0.28 | n/a | ~0 (control) |

The zero-caster control lands almost exactly on the predicted floor —
+0.28 points, noise-level, confirming a PC with no valid Interrupt
target loses nothing.

**Second correction: Magehunter is also tagged `[Encounter]`.**
techniques.csv's own `Tags` column reads "Martial, Encounter" for
T075, not just "Martial" - missed in the table above, which let the
Interrupt fire every time AP and a valid trigger lined up, all fight
long. glossary.md's `[Encounter]` definition is explicit: "Encounter
abilities are expended when you use them, and you regain their use
when the encounter ends" - a real once-per-encounter charge, the same
rule Whirlwind/Flurry/Ricochet Shot already follow elsewhere in this
file. Fixed with a separate `pc['magehunter_charge_used']` flag,
checked alongside (not instead of) `ap_bank` in `_magehunter_interrupt`
- the charge gates whether the Interrupt can fire again at all, while
`ap_bank` keeps tracking the real AP cost of the one use that already
happened (that cost doesn't disappear just because the charge is
spent - it still reduces whichever future turn it lands before).

With a true single use per fight, the table above's win-rate deltas
mostly collapse back toward noise (5× Fen Warden retested: +5.77 pts
→ -1.45 pts; mixed roster: -1.58 pts → -2.40 pts) - one attack, once,
somewhere across a ~10-round, ~47-attack fight is exactly the
"diluted into noise by fight length" trap this project's own Feint
pass already named (see that section above). Switched to the same fix
that pass used: measure the moment directly instead of trusting the
aggregate delta. Instrumented the 5× Fen Warden matchup (4000 trials,
trace-scanning for the one `(Magehunter)`-tagged attack event per
fight) to isolate exactly what one use is worth:

- **Fires in 100% of fights** in this all-caster matchup (a valid
  trigger always comes up somewhere in ~10 rounds).
- **41.7% hit rate**, averaging **1.371 net damage per use**
  (unconditional on hit - EV-maximizing Gambling, per
  `pc_gamble_count`, trades hit rate for bigger hits when it pays,
  same as any other attack).
- **Kills the target outright in 5.8% of uses** - a real elimination
  (the rest of that enemy's turns for the whole fight, not just one
  prevented attack), not fully priced into the raw damage average
  above.
- The matchup's own overall party-attack average (`dpa`) is **1.206**
  net damage/attack - so the raw swap alone (1.371 vs. 1.206) is worth
  about **+0.165 net damage per use**, converted at the guaranteed
  rate (4/point, since both numbers are already probability-weighted
  averages, not a fresh hit-chance to discount again) - **≈0.66
  Value** from the swap alone, before crediting the 5.8% kill-rate's
  own elimination value, which isn't cleanly separable with this
  measurement but is real and additive.

**Verdict: Magehunter is a small, close-to-fair, genuinely single-use
Interrupt - not the strong positive the multi-use bug produced, and
not the strong negative the AP-pre-reservation bug produced either.**
The raw swap-only estimate (≈0.66 Value) plus a non-trivial 5.8%
outright-kill chance land it in reasonable range for a cheap (1 AP)
Level 1 Technique, even if it's more modest than the flat `3 × Level`
anchor a repeatable ability would be judged against - a true
once-per-encounter Interrupt is a smaller thing than the multi-use
version this pass spent two iterations accidentally modeling. No
Cost/Effects change - leaving Magehunter as written. Three real bugs
in one Technique's simulator model (AP-refresh timing, then the
missed Encounter tag) is worth remembering as its own lesson: an
Interrupt/Encounter-tagged ability needs BOTH the real AP-economy
check (ap_bank) AND the Encounter once-per-fight charge check before
its numbers mean anything - checking Tags against glossary.md's own
keyword definitions is as load-bearing as getting the AP math right.

## Parting Shot (T076) — same Interrupt shape as Magehunter, built with both lessons already applied

T076 Parting Shot (Level 1, Martial + Encounter, "1 AP - Interrupt (a
creature within range of a close-range weapon you are wielding would
move or be Pushed outside your range)"): "Make an attack with a
close-range weapon against the target." Same trigger family as
Magehunter (T075) - an off-turn preemptive weapon attack - just keyed
on a creature trying to disengage instead of casting a Spell, so it
reuses the same `ap_bank`/once-per-encounter-charge infrastructure
Magehunter's two corrections above already built, rather than
repeating either mistake.

**What "move outside your range" means in this simulator.** Only one
Battle Tactic ever moves a unit AWAY from its target at all -
`tactics.move_kite` ("Kiting" - always exactly 1 retreat action per
turn, no check for whether retreating is actually necessary). Every
other tactic only closes distance. So Parting Shot's real trigger here
is narrow and specific: a Kiting enemy that's currently within a
close-range-weapon PC's reach, right before its own retreat step
executes. "Being Pushed" isn't modeled at all (no Push ability exists
in this simulator - see tunables.ABILITY_COST's own comment on
positional effects left out).

**Built** (`combat_sim.py`): `pc['parting_shot']` (synthetic test
field) shares `pc['ap_bank']` with Magehunter via a new
`_has_interrupt_tech(pc)` helper (both draw from the same real AP
pool, since rulebook.md's AP economy is one number per PC, not one
per Technique known) and gets its own `pc['parting_shot_charge_used']`
Encounter charge from the start - no repeat of either bug this
Technique's own sibling needed two passes to find.
`_parting_shot_interrupt`, called from `_take_enemy_turn` right before
`spend_movement_ap` executes a Kiting unit's retreat (checked against
the enemy's position BEFORE that move, not after), gates on "close-
range weapon" specifically (`not pc.get('attack_range')` - party.py
only sets `attack_range` for a real ranged `Weapon` pick, so the blank
default/2H Heavy Melee/Unarmed all qualify, a Light Bow/War Magic PC
doesn't).

**Tested** against a 12× "Generic Level 1 Ranged Caster" (Kiting,
`Roster=FALSE` reference build - the only sample_enemies.csv rows that
use Kiting at all; 12 gives a fair ~51% unsaturated baseline, since
these untuned reference builds are individually weak) and a zero-Kiter
control:

| Matchup | Baseline win% | Parting Shot win% | Δ | Autoswing control Δ | Value |
|---|---|---|---|---|---|
| 12× Kiting Ranged Caster | 51.30 | 53.87 | +2.57 | +1.77 | +7.98 |
| 4× non-Kiting (Hedge Knight/Marsh Archer/Skulking Footpad) | 44.95 | 45.30 | +0.35 | n/a | ~0 (control) |

Same no-trigger floor as Magehunter's own zero-caster control - a PC
with nothing worth interrupting loses nothing. Moment-level detail on
the Kiting matchup (4000 trials, trace-scanning for the one
`(Parting Shot)`-tagged event per fight): **fires in 100% of fights**
(a Kiting enemy always ends up adjacent to *some* melee PC at some
point over ~11 rounds), **67.3% hit rate**, **2.732 average net
damage per use** (unconditional on hit) against this matchup's own
**2.681 party-wide dpa** - a close-to-even raw swap, same shape as
Magehunter's. The real difference is the kill rate: **23.9% of uses
kill the target outright** (vs. Magehunter's 5.8%), because these
particular reference-build casters are individually low-Health - a
much bigger share of Parting Shot's value here comes from outright
eliminating a weak straggler mid-retreat than from the raw damage
swap, which is presumably also why the aggregate win-rate delta reads
cleanly positive here (+2.57 vs. Autoswing's own +1.77) rather than
collapsing into the same noise Magehunter's rarer 5.8%-kill case did.

**One real caveat worth flagging directly, not just a simulator
footnote: none of the current default Level 1 roster uses Kiting.**
MIXED_ROSTER's four archetypes (Hedge Knight, Marsh Archer, Skulking
Footpad, Fen Warden) all either close distance or hold position -
none of them ever retreat from melee. Against the actual default
encounter mix a table is likely to run, Parting Shot's trigger
condition may simply never come up at all, landing it at the ~0 floor
in practice rather than anywhere near the +7.98 this pass measured -
that number describes Parting Shot's ceiling against a
disengage-happy enemy (a skirmisher, a hit-and-run archer, anything
actually built to kite), not its typical case with the roster as it
stands today. Worth the designer's own call on whether that's fine
(a situational Technique that rewards facing the right enemy type,
same shape as Magehunter rewarding facing casters) or whether the
roster should grow a real Kiting archetype for Techniques like this
one to actually matter against.

**Verdict: built correctly the first time, thanks to the AP-timing and
Encounter-tag lessons Magehunter's two corrections already paid for.**
No Cost/Effects change. The main open question isn't the Technique's
own math - it's whether the current enemy roster gives it anything to
trigger against at all.

### Follow-up: a real Kiting archetype (Bog Skirmisher), and Parting Shot on Hilde specifically

Picked up directly from the open question above - answered it by
adding a real Kiting archetype and testing Parting Shot on the PC
who'd actually want it.

**Bog Skirmisher** (new `sample_enemies.csv` row, `Archetype=Mixed-
Style`, `Roster=FALSE`): Level 1, 1 Slot, Ranged Weapon (Physical -
distinct from Fen Warden's Melee Spell and Bog Caster's Ranged Spell,
so the mix reads as three genuinely different threats, not two spell
casters and a third), `BattleTactic=Kiting`, `FightingStyle=Aimed
Shot` (not Guarded - Kiting always spends its one move action
retreating, so Guarded's own stand-still Bad Luck bonus would never
actually trigger on a unit that always moves; pairing Kiting with
Guarded would waste half the Fighting Style), `AttackTier=Primary`,
`DodgeTier=Secondary`/rest Poor, `HealthBonus=0` (not the other five's
+2 - a deliberate identity choice: this archetype's survivability is
supposed to come from staying out of reach, not raw Health, so it
should die fast once actually caught), Abilities `Strike
(Vulnerable);Powerful Weapon`. Built with `enemy_builder_pcstyle.py`,
same construction as its siblings. **Not calibrated to the same rigor
as the other four** - a quick 4x-clone check against the real drafted
party (Hilde/Browndog/Carrick/Sable, `movement=True`) landed at
win=100%, ~5.0 rounds, ~86% party Health on a win, well short of the
other four's ~72% target - Kiting alone doesn't hold up to a focused
melee-heavy party in this simulator's bounded 20×20 arena (it gets
cornered and caught fast, then dies quickly with `HealthBonus=0`), so
a lone Kiter reads as considerably weaker than its stand-and-fight
siblings at the same nominal Level. Good enough to give Parting Shot
something real to interact with; not folded into the default
`MIXED_ROSTER` mix, and would want a fuller retune pass first if it
ever should be.

**`target_kiter`** (`tactics.py`, registered as "Kite Hunter") - a new
PC-side `TARGETING` entry, the second after Hanforth's "Straggler
Hunter": prefers any living enemy whose own `battle_tactic` is
"Kiting" over anything else, closest among those if more than one.
Built so a melee PC who wants to punish a disengaging enemy actually
goes after it, instead of falling back to plain closest/focus-wounded
and maybe never ending up adjacent to the one target Parting Shot
cares about.

**Tested on Hilde specifically** (2H Heavy Melee - a close-range
weapon, Parting Shot's own requirement - Body-primary duelist, real
drafted-party member), in the real drafted party
(Hilde/Browndog/Carrick/Sable) against the full 4-archetype mix plus
two Bog Skirmishers (`['Hedge Knight', 'Marsh Archer', 'Skulking
Footpad', 'Fen Warden', 'Bog Skirmisher', 'Bog Skirmisher']` - a fair
~55% unsaturated matchup, `movement=True`, 4000 trials):

| Setup | Win% | Δ | Autoswing control Δ | Value |
|---|---|---|---|---|
| Baseline (no Parting Shot) | 54.73 | - | - | - |
| Parting Shot, default targeting | 61.25 | +6.53 | - | - |
| Parting Shot + Kite Hunter targeting | 61.35 | +6.62 | +9.08 | 4.02 |

**Value ≈ 4.02** - close to the `3 × Level` Technique-value anchor,
and a real, well-powered aggregate reading this time (unlike Magehunter's
own moment-diluted-into-noise problem) - because Parting Shot's
per-use value here is both high AND frequent enough not to get lost
in a ~10-round fight (see the moment-level numbers below).

**Does "Kite Hunter" targeting actually help?** Checked directly
(3000 trials, trace-scanning for the `(Parting Shot)` event):

- Default targeting: fires in **73.7%** of fights, 62.8% hit rate,
  3.139 avg net damage/use, **38.0% outright-kill rate**.
- Kite Hunter targeting: fires in **81.3%** of fights (+7.6 points -
  a real, if modest, improvement in trigger reliability), 62.7% hit
  rate, 3.136 avg net damage/use, **33.5% kill rate**.

Kite Hunter targeting does what it says - more fights end with Hilde
actually adjacent to a Bog Skirmisher when it tries to retreat - but
the overall win-rate delta barely moves (+6.53 → +6.62), and the
per-use kill rate is slightly *lower* despite firing more often. The
likely reason: chasing the Kiter specifically sometimes means engaging
a still-full-Health Bog Skirmisher before the rest of the party has
softened it up, trading some of `target_focus_wounded`'s own
focus-fire efficiency for a more reliable (but not necessarily
better-timed) trigger. Both average net damage per use (~3.14) come in
well above this matchup's own party-wide dpa (1.392, more than double)
- Parting Shot always targets the softest defense in the mix by
design (Bog Skirmisher's Poor/Secondary tiers), so a triggered use
reads as a much better-than-average attack regardless of which
targeting rule got Hilde there.

**Verdict: Parting Shot is a real, on-budget pick once the roster
actually has something for it to punish** - Value ≈ 4.02 against a
mix that includes even just two Kiting enemies alongside the normal
four, a fair, well-powered, non-noisy reading. Kite Hunter targeting
is a genuine, if modest, improvement to trigger reliability (+7.6
points fire rate) rather than a large swing in outcome - worth having
as an option for a player who's specifically built around punishing
disengage (Hilde's own concept fits it well), not a required pairing.
The open question from the base Parting Shot section still stands for
whoever's *not* running Kite Hunter or facing a Bog-Skirmisher-style
threat: against the actual default `MIXED_ROSTER` (still 0 Kiting
archetypes), Parting Shot remains at its ~0 floor.

## Blinkstep (T077) — free pre-attack movement, measured value below its own anchor, but the simulator can only see one of its uses

T077 Blinkstep (Level 2, Martial + Encounter, 0 AP): "Shift up to [half
your Acrobatics Skill Total] meters." glossary.md's `[Shift]`: ordinary
movement, except nobody may take an Interrupt action against it and it
ignores Difficult Terrain - neither of those two exceptions is
modeled in this simulator (no enemy Interrupt exists to dodge, no
terrain system exists at all), so what's measurable here is narrower
than the Technique's real scope - flagged up front, not as an
afterthought, since it matters for reading the number below.

**A real field was missing to model this at all**: no PC dict exposed
raw Acrobatics Skill Total anywhere - only `dodge` (`8 +` it, *after*
Armor's own Dodge modifier folds in), which isn't the same number for
anyone not in Unarmored/Light Armor. Hilde specifically wears Medium
Armor (-1 Dodge) - reading Shift distance off `dodge - 8` would have
quietly undercounted her own Acrobatics by 1 meter of Shift. Added
`acrobatics_skill_total` to `party.py`'s own `_pc_dict`, captured
before the Armor modifier applies, alongside the existing `dodge`/
`parry`/etc. fields.

**Built** (`combat_sim.py`, `pc['blinkstep']` synthetic test field,
once-per-encounter charge): applied *before* `spend_movement_ap`, not
as a rescue after it - `spend_movement_ap` already spends up to all 4
AP closing any reachable gap on its own (so it usually succeeds
regardless of Blinkstep), meaning the real value here isn't "you'd
have failed to reach otherwise" but "you get there using less AP, or
none at all, leaving more for an attack this same turn" - the
Technique's own real value proposition. Only spent when there's an
actual gap left to close (a player wouldn't burn a once-per-encounter
charge for nothing), `// 2` per rulebook.md's own "round fractions
down" rule, logged as its own trace event separate from any
AP-funded movement that follows so `spaces` on each event reflects
only that phase's own distance.

**Tested on Hilde** (Acrobatics Skill Total 4 → Shift 2m; her real
Prereq is Acrobatics 3, raw skill points, which her actual build
doesn't meet - same "test the mechanic regardless of whether this
PC's own canonical build qualifies" convention as Magehunter/Parting
Shot's earlier passes), real drafted party, `movement=True`:

| Matchup | Baseline win% | Blinkstep win% | Δ | Autoswing control Δ | Value |
|---|---|---|---|---|---|
| Default Lvl1 mix (saturated ~99%) | 99.23 | 99.52 | +0.28 | +0.17 | 9.35 (untrustworthy - saturated) |
| 4-archetype + Hedge Knight + Marsh Archer (unsaturated ~49%) | 48.60 | 53.10 | +4.50 | +8.68 | 2.85 |
| 4-archetype + Hedge Knight (~88%, noisier) | 87.58 | 90.12 | +2.53 | +3.43 | 4.06 |

The clean ~49% matchup is the one to trust; the saturated one is
noise (same "often-saturated Level 1×4" trap the README already
flags), the ~88% one sits in between the other two and shouldn't be
weighted equally against the clean reading. Decomposed on the clean
matchup (3000 trials): total party attacks/fight barely moves
(48.52 → 48.81) but total damage/fight rises more (63.61 → 65.98) -
consistent with "occasionally buys a 2nd attack a turn earlier than
it would've otherwise landed" rather than a large volume change.

**Verdict: measured Value ≈ 2.85-4.06, below the `3 × Level` = 6
anchor for a Level 2 Technique - but read this as a floor, not a
final number.** Unlike Magehunter's two real bugs (a modeling error
each time, fully explaining the wrong numbers), there's no known
error here to fix - the mechanic does what it says, freeing AP for an
earlier attack when there's a gap to close. What's missing is
everything this simulator was never going to be able to measure:
Shift's own Interrupt-immunity (dodging a Parting-Shot-style punish -
no enemy in this catalog has one yet, so there's nothing to test
against), ignoring Difficult Terrain (no terrain system exists at
all), and every purely positional use (avoiding a flank, escaping a
bad spot, repositioning while doing something else with your AP) that
doesn't reduce to "closed the gap for an attack." Same category of
gap ENEMY_ENCOUNTER_DESIGN.md's own Ability catalog already
acknowledges for Sturdy/Shadow Jaunt/Retribution Aura - positional
effects this project's model just can't fully price. No Cost/Effects
change - the measured shortfall isn't confident enough to act on
given how much of the Technique's real value this pass couldn't see.

## Perfect Strike (T078) — already implemented (quietly active this whole session), now actually priced

T078 Perfect Strike (Level 2, Martial, "0 AP - Interrupt (you declare
a weapon attack)", Cost "Discard a card"): "You have Good Luck on the
weapon attack, then choose one: have Good Luck a second time on the
attack; or add the discarded card to the attack's suit pool." Unlike
every other Technique this Martial-cluster pass has built from
scratch, this one already had a working `tactics.perfect_strike_bonus`
implementation - part of the original Card Techniques infrastructure,
not something this pass added - but it had never actually been priced
against a control. Carrick and Sable (both real drafted-party members)
have "Perfect Strike" in their own canonical `Card Techniques` column,
so it's been quietly firing in *every* drafted-party test this whole
session (Parting Shot, Blinkstep, ...) without a dedicated check of
its own.

**Implementation matches the Effects text**, modeling the "Good Luck a
second time" branch specifically (not the suit-pool alternative, which
this sim can't represent - same "pick the branch this simulator can
actually model" convention as every other Choice-shaped Effect this
project has hit): `+2` Good Luck stacks on one attack (flip 3, take
highest), consuming one `card_uses_left` charge
(`hand_size // 3` - Carrick's own Cunning 2 + Mind 2 gives 2 uses),
shared with Second Wind's same budget.

**A/B tested on Carrick** (4x-clone, `make_party_of` - the established
pattern for isolating one PC build's own attack profile) against a
clean ~51% unsaturated matchup (`['Hedge Knight', 'Marsh Archer',
'Skulking Footpad', 'Fen Warden', 'Hedge Knight']`, `movement=True`,
6000 trials), Autoswing-`bonus_attack_control` applied to all 4 PCs
in the control run (since all 4 clones share Carrick's own Perfect
Strike):

| Setup | Win% | Δ |
|---|---|---|
| No Perfect Strike (stripped) | 26.47 | - |
| Perfect Strike (Carrick's real build) | 50.30 | +23.83 |
| Autoswing control (all 4 PCs) | 49.37 | +22.90 |

A genuinely large swing either way - Perfect Strike alone very nearly
doubles this matchup's win rate. Converting through the ratio (both
deltas reflect all 4 PCs' worth of effect, so the 4s cancel):
`Value ≈ (23.83 / 22.90) × 5.5 ≈ 5.72` per PC for the whole fight's
worth of Perfect Strike (Carrick's 2 charges).

**But this number is inflated, and there's an already-Locked way to
check it directly.** Perfect Strike's base effect - "Good Luck, then
Good Luck a second time" - is exactly the already-priced "Good Luck
(stacked, flip 3 take highest)" rate from the Thrumming Focus pass:
**3.6 Value**, not a fresh derivation. Its Cost ("Discard a card") is
also already priced: **Card (drawn/hand) = 2.7**, the same rate this
project already treats a card-discard activation cost as a real,
netted charge against (see the Bloodfire Signet Ring's own "Value =
6L − 2.7" derivation). **Net Value per use = 3.6 − 2.7 = 0.9** - a
small, positive per-use value, ×2 uses for Carrick specifically
(`hand_size // 3`) ≈ **1.8 total per-fight Value**, well below the raw
5.72 the aggregate win-rate delta suggested.

**Why the gap**: this simulator's `card_uses_left` is an isolated
counter, not a real hand - spending a charge on Perfect Strike doesn't
reduce anything else a card could have paid for (Gambling, another
Card Technique, a future turn's own flexibility). A real player's
discard is a genuine opportunity cost across their whole hand; this
sim's aggregate win-rate delta can't see that cost at all, so it
measures Perfect Strike as if the discard were free - the same
structural blind spot Blinkstep's own section just flagged for
position, now showing up for cards instead. **The hand-derived 0.9/use
figure (built from two already-Locked/Pencil rates that already
account for the discard cost properly) is the one to trust here, not
the raw simulator delta** - the inverse of most of this pass's other
findings, where the simulator caught something hand-math missed;
here hand-math catches something the simulator structurally can't.

**Verdict: Perfect Strike is a small, positive, on-target Technique
(≈0.9 Value/use, ≈1.8/fight for a typical Cunning/Mind budget like
Carrick's) - no Cost/Effects change.** Standing methodological note
for whenever Second Wind/Bottomless Bottles/Warmage's Reserves (the
other three Card Techniques sharing this same `card_uses_left`
machinery) get their own dedicated check: expect the same inflation
if priced by aggregate win-rate delta alone - net out Card (2.7)
against whatever the simulator measures, the same way this pass did,
rather than trusting the raw delta.

## Cloak and Dagger (T079) — corrected twice: a rules bug, then an arithmetic slip, before landing on a real, situational Technique

T079 Cloak and Dagger (Level 3, Martial, "0 AP - Interrupt (you declare
a weapon attack with a close-range weapon that isn't Heavy or
two-handed)", Cost "Discard a card"): "Make a Stealth attack against
the Vigilant Defense of a target of the weapon attack (Good Luck if
you discarded a Spade). If it hits, that target is unaware of the
attack." rulebook.md's own `[Unaware]` rule has TWO real effects: the
target "cannot apply their Parry or Dodge Defense" AND "that attack
ignores the target's Shallow Health and instead causes them to only
lose Deep Health." **Per the designer's own call**, only the first
half is modeled here - the Deep-Health half would need a real
two-pool Health system across the whole simulator, not just this one
Technique, so it's explicitly flagged as unmeasured rather than
approximated. Every number below is still a floor on the Technique's
real value for that reason.

**First pass got the rule itself wrong.** "Cannot apply their Parry
or Dodge Defense" was built as a full auto-hit - but rulebook.md's own
base attack rule is explicit (line 484): "The target may choose not
(or be unable) to apply any Defenses against an attack, in which case
it is considered to be **8**." Not a guaranteed success - a real
(usually much lower) Defense the attack still rolls against.

**Second pass got the arithmetic wrong on top of that.** Comparing the
simulator's own raw win-rate-delta reading (≈3.9 Value/charge) against
Autoswing (5.5), the write-up "credited back" the Card cost (2.7) by
*adding* it - `3.9 + 2.7 = 6.6 > 5.5, overpowered`. Backwards: the raw
3.9 was already a gross figure (the simulator's `card_uses_left` is an
isolated counter, nothing else gets worse from spending it, so no cost
was ever subtracted), and the fair comparison nets the cost by
*subtracting* it, giving ≈1.2 - below Autoswing, not above it. The
designer's own request to just crunch the math directly, rather than
trust another simulator read, is what surfaced the first error.

**The actual hand math, using the same EV-maximizing-Gambling logic
already established for `pc_gamble_count`:** the target's real
Dodge/Parry Defense in the roster ranges 12-14; Unaware routes it to a
flat 8 instead. For Hanforth (Skill Total 6, Damage 5, Stealth Skill
Total 3, vs PhysRes 3) against the roster's real Vigilant Defense (12,
uniform across all four base archetypes):

- Stealth check odds: Good Luck (flip 2, take best) vs threshold 9 →
  **q = 0.621**.
- EV-maximizing attack, normal Defense: 12→1.385 (n=1), 13→1.154
  (n=1), 14→0.923 (n=0).
- EV-maximizing attack, Unaware (Defense 8): **2.462** (n=2) - fixed,
  doesn't depend on the normal Defense.
- Net Value per *attempt* = `q × (unaware_ev − normal_ev) × 4 −
  2.7` (Card cost, THE TABEL's own established rate):

| Target Defense | Expected net Value per attempt |
|---|---|
| 12 | **−0.02** (not worth attempting) |
| 13 | **+0.55** |
| 14 | **+1.12** |

A situational Technique by design, not a flat bonus - worth roughly
Perfect Strike's own tier (0.9/use) against the roster's toughest
targets, and correctly worth nothing (or slightly negative) against
anything easier. This is the number to trust, not a fresh simulator
read - same reasoning as Perfect Strike's own write-up: the aggregate
win-rate delta doesn't reliably reconstruct a value this conditional
on which specific target a PC happens to face turn to turn.

**Rebuilt to match, in three pieces** (`combat_sim.py`):
1. `defense = 8 if cloak_dagger_hit else enemy_defense_for_pc_attack(...)`
   - a real (if soft) roll, not an override to `hit = True`.
2. `pc_gamble_count` gained a `defense_override` param, so Gambling
   re-optimizes against the Defense-8 floor once Unaware lands - more
   headroom before missing means a rational player gambles harder.
   `_gamble_search` factors the shared EV search out of
   `pc_gamble_count` so both it and the new check below (3) use one
   search, not two that could drift apart.
3. **The PC now only attempts Cloak and Dagger when it's actually
   worth the card** - a new gate computes the exact expression above
   (`q × (unaware_ev − normal_ev) × 4 − T.CARD_VALUE`, `T.CARD_VALUE`
   the same established 2.7) before spending a charge, using
   `_p_flip_at_least` (the same flip-2-take-best formula this
   project's Good-Luck-stacking math already established) for `q`.
   Without this the original (Defense-8-corrected but still greedy)
   version burned charges on already-easy targets for negative
   expected value - a real, separate bug from the auto-hit mistake,
   not just a design nicety.

**Directly validated against the hand math**: instrumented the gate's
live decisions against Hanforth's real stats mid-fight - it accepts
*exactly* Defense 13-14 and rejects Defense ≤12, matching the
sensitivity table above to the number. The code now implements the
same EV-maximizing logic worked out by hand, not an approximation of
it.

**Verdict: Cloak and Dagger is not overpowered - the "auto-hit,
overtuned" read was wrong twice over, first on the rule, then on the
arithmetic.** Net Value per use lands at ≈0.55-1.12 against the
roster's toughest targets (in line with Perfect Strike's own tier for
a Technique one Level higher), and the Technique correctly isn't worth
using at all against an easy target - exactly the shape a "cracks
tough marks" Rogue tool should have, not a flat bonus. No Cost/Effects
change. Standing lesson alongside Perfect Strike's own: for a Card
Technique specifically, the aggregate win-rate delta is the wrong
primary instrument (the simulator can't see the card's own opportunity
cost, and here also can't cleanly reconstruct a value this
target-dependent) - hand-derive from already-Locked/Pencil rates first,
treat the simulator read as a rough cross-check, not the other way
around.

## Bear School - Boulder Toss (T081) — hand math only, no simulator changes, framing decides the verdict entirely

T081 Bear School - Boulder Toss (Level 2, Martial + Encounter, "0 AP -
Interrupt (you hit with an attack to grapple a creature)", Condition
"Your hands are empty"): "End the grapple and throw the target up to
[half your Might Skill Total] meters in a straight line. If thrown
into a sturdy object, the target strikes it (3 + [your Body] Physical
damage to both). If thrown through a creature's space, make a Might
attack against that creature's Dodge; if it hits they are struck for
the same damage." Almost the entire payoff depends on battlefield
positioning (an obstacle, a second creature in the throw's line) that
this simulator has no representation of at all - no terrain system, no
line-of-throw resolution against arbitrary enemy positions. Building
that properly would be a real project of its own (real obstacle
density plus multi-target line resolution), well beyond this pass's
scope, so **this Technique is priced by hand only - no simulator
changes, no `combat_sim.py` edits.** The designer's own call, given
how position-dependent the effect is.

**The one clean rules fact, no assumption needed**: Grapple (rulebook.
md's own Combat Maneuver) is "Make an Unarmed weapon attack against
your target's Dodge or Parry Defense" - the *exact same roll* as a
normal Unarmed attack against the same target (same Skill, same
Defense-choice rule), and it deals **no damage of its own** - a hit
just establishes the grapple, nothing else. So the entire question is
a pure payload comparison at identical hit odds: is "end the grapple
and throw" worth more than the guaranteed weapon damage you gave up by
not just attacking? No AP/card cost to net out either - Boulder Toss
itself is 0 AP, and the Grapple attempt already costs the same 2 AP a
normal attack would, so this is a straight opportunity-cost comparison
between two uses of the same attack action, not an activation-cost
question the way Perfect Strike/Cloak and Dagger were.

**First framing: attempt it opportunistically, hoping a good throw
target exists.** Worked example (Body 3, Brawl 3, Might 3, Agility 2,
Cunning 1 - meets both Prereqs, Brawl 3 and Might 2, with headroom):
Unarmed Skill Total 7, Damage 5; Might Skill Total 6, Boulder Toss
damage 6 (net 3 after PhysRes 3). Assumed odds (stated, not a rules
fact - a battlefield-density guess): P(a usable obstacle happens to be
in throw range) 35%, P(a second creature happens to be in the exact
throw line) 15%.

| Target Defense | Normal attack EV | Boulder Toss EV | Delta |
|---|---|---|---|
| 12 | 1.615 | 0.919 | **-0.70** |
| 13 | 1.385 | 0.817 | **-0.57** |
| 14 | 1.154 | 0.714 | **-0.44** |

Negative across the whole roster's Defense range, and stays negative
even at a generous 50% obstacle assumption (only -0.10 at Defense 14)
- doesn't cross into positive territory until obstacle odds climb well
past what a "maybe there's something nearby" read should assume.
Structurally this makes sense: the raw damage bump (+1 over a normal
hit, 6 vs. 5) is real but small, stacked behind a SECOND layer of risk
(the obstacle/bystander has to actually be there) on top of the
grapple itself landing - two dice to roll instead of one, for a small
bonus if both come up.

**Second framing, per the designer's own correction: a player who sets
this up deliberately** - maneuvers so there's a wall (or equivalent
obstacle) roughly behind the target *before* ever attempting the
Grapple, rather than grappling first and hoping. This makes the
"worst case" (a wall strike) a near-guarantee once the grapple lands,
not a battlefield-density coin flip - the only real remaining
uncertainty is whether a second enemy *also* happens to be in the
throw's exact line before the wall (upside on top of the guaranteed
floor, not something even a deliberate player fully controls).

| Target Defense | Normal attack EV | Boulder Toss EV (guaranteed wall + 25% bystander upside) | Delta | Value |
|---|---|---|---|---|
| 12 | 1.615 | 2.396 | **+0.78** | **+3.12** |
| 13 | 1.385 | 2.130 | **+0.75** | **+2.98** |
| 14 | 1.154 | 1.864 | **+0.71** | **+2.84** |

Solidly positive across the whole Defense range (holds across a
15-35% bystander-odds spread, never crossing back to negative) - beats
a normal attack by 50-80% in expected damage, since the floor is now a
guaranteed hit (net 3) instead of a coin flip on whether *anything*
connects at all. Converted to Value at the guaranteed rate (4/point,
since the delta is already probability-weighted through both the
grapple-hit chance and the bystander-hit chance): **≈2.8-3.1 Value
from damage alone**, roughly half the `3 × Level` = 6 anchor for a
Level 2 Technique - and that's still *before* crediting the free 3m
forced repositioning on top (denying a target's own positioning,
potential hazard synergy, the tempo cost of needing to close distance
back in), which is real, additive value this project's damage-based
framework still has no way to price (same category as Blinkstep's
non-attack Shift uses and Cloak and Dagger's Deep-Health half).

**Verdict: on-budget, likely comfortably so once the reposition value
is accounted for - no Cost/Effects change.** The two framings above
aren't really in tension - they're the same Technique played two
different ways, and the gap between them (-0.44 to +0.78 delta,
depending entirely on whether the player set up the throw first) is
itself the interesting finding: Boulder Toss is a genuine skill-
expression Technique, not a flat bonus - a player who treats Grapple
as "attack, then hope" gets a real, measurable worse deal than just
attacking normally, while one who plays it as "maneuver first, then
grapple into a guaranteed payoff" comes out clearly ahead even before
the free movement is counted. That's a coherent design shape for a
"grab and throw" tool built around battlefield awareness, not
something to flatten into a single number.

## Demon School - Plague Fist (T083) — hand math against THE TABEL's own Vulnerable/Necrotic weights, plus a real independent bug caught along the way

T083 Plague Fist (Level 2, Martial + Discipline + Encounter, "2 AP",
Prereqs "Brawl 3, Meditation 2"): "Make an Unarmed weapon attack which
deals its damage as Shadow. If the attack hits, before damage is dealt,
the target gains [half your Meditation Skill Total] + [Spades] stacks
of Necrotic, then [half your Meditation Skill Total] + [Diamonds]
stacks of Vulnerable." Per the designer's steer, this one's priced by
hand against THE TABEL's own already-Pencil'd Vulnerable/Necrotic
weights - no simulator mechanic built, no `combat_sim.py` changes for
Plague Fist itself (the "run the sim" treatment is for weird/messy
cases; this one reduces cleanly to existing per-stack rates).

**One real bug found first, and fixed independently of Plague Fist's
own pricing.** `enemy_defense_for_pc_attack`'s Vigilant branch was
returning `target['vigilant']` with no Vulnerable subtraction at all -
glossary.md is explicit that Vulnerable is "-1 penalty to Vital,
Mental, **and Vigilant** Defenses" per stack, and `pc_defense_for`
already applied it to the enemy-attacks-PC direction's Bodily/Mental
cases, but the reverse direction's Vigilant case was missing entirely.
Harmless until now - nothing granted an enemy Vulnerable before Plague
Fist - but a real, pre-existing gap, not something new introduced here.
Fixed (now reads `target['vigilant'] - vulnerable`) and verified via a
clean `import combat_sim`; committed alongside this write-up since it's
correct regardless of how Plague Fist itself ends up priced, and
directly relevant to two Martial siblings in this same cluster (Feint,
Cloak and Dagger) that also target Vigilant.

**The clean rules facts**: Unarmed's own attack roll and Defense choice
don't change - Plague Fist is the same to-hit roll as a normal Unarmed
attack, just with its damage type swapped to Shadow and two status
effects tacked on "if the attack hits, before damage is dealt." Same
2 AP an Unarmed attack already costs, so like Boulder Toss this is a
straight opportunity-cost question: what does Plague Fist buy you over
just attacking, at identical hit odds, with no separate AP/card cost to
net out.

**Damage-type swap (Shadow vs. Physical)**: the roster's enemies run
`physres=3` (Light Armor's own Physical Resist bonus) but `elemres=2`
(bare Essence, no armor contribution) - a real, unconditional +1 net
damage per hit just from the type swap, gated by the same attack roll
as a plain Unarmed hit (no extra roll needed). Priced the same way
Boulder Toss's own delta was: compute both EVs (already probability-
weighted through the shared hit chance), take the delta, convert at the
guaranteed 4/point rate.

**Vulnerable/Necrotic stacks**: worked-example build (Body 3, Agility
2, Cunning 1, Mind 1, Essence 3, Brawl 3, Meditation 3 - meets both
Prereqs with some headroom on Meditation, same "not bare minimum"
convention as Boulder Toss's own example): Unarmed Skill Total 7
(Agility 2 + Brawl 3 + weapon's own +2 accuracy), Damage 5, Meditation
Skill Total 6 (Essence 3 + Meditation 3), so half-Meditation-ST = 3.
Suit clauses use this project's own established 0.25 expected-value
convention (`balance_weights_notes.md`'s own "assumed 0.25 expected
suit bonus" - a 1-in-4 chance per suit), so expected stacks = 3.25 for
both Necrotic and Vulnerable. Vulnerable's own value is priced off THE
TABEL's already-Locked lump-application curve (Value(3)=6, Value(4)=10
- see "Vulnerable = 1/stack base..." above), weighted by the 75%/25%
split between landing exactly 3 vs. 4 stacks: `0.75×6 + 0.25×10 = 7.0`
per landed hit, then multiplied by the attack's own hit chance (same
roll delivers both the damage and the stacks, so no separate discount
needed beyond that one P(hit)).

| Target Defense | P(hit) | Damage-swap Value | Vulnerable EV | Core Value (damage + Vulnerable) | Necrotic ceiling (situational) |
|---|---|---|---|---|---|
| 12 | 0.692 | 2.77 | 4.85 | **7.62** | 6.75 |
| 13 | 0.615 | 2.46 | 4.31 | **6.77** | 6.00 |
| 14 | 0.538 | 2.15 | 3.77 | **5.92** | 5.25 |

Against the `3 × Level` = 6 anchor for a Level 2 Encounter Technique,
Core Value alone already lands at roughly 100-127% of budget across the
roster's real Defense range - **before** Necrotic is counted at all.
At the Prereq-minimum build instead (Meditation Skill Total 4, half = 2,
expected stacks 2.25, Vulnerable EV off `0.75×3 + 0.25×6 = 3.75`/hit),
Core Value drops to 4.17-5.37 - back in the normal on-budget range. So
like Boulder Toss, Plague Fist's real value is build-dependent, but for
a different reason: not a framing choice, just how much Meditation the
character actually invested beyond the bare Prereq.

**Necrotic's own honest treatment**: per THE TABEL's already-established
convention (see "Necrotic = 3/stack..." above), 3/stack is priced for
when it actually resolves (blocks a Protected stack or a self-heal),
not discounted again for whether that trigger ever comes up - that
situational discount belongs in the encounter design, not the per-stack
rate. Against this project's own tested roster, that's **effectively
zero** - no enemy in the simulator ever heals or carries Protected
(same "zero measurable combat effect" finding this project already
reached for Necrotic generally), so the 5.25-6.75 ceiling in the table
above is real only against a healer/Protected-granting enemy archetype,
which the roster doesn't currently field. Flagged, not counted toward
the Core Value verdict.

**One more unpriced upside, same category as Boulder Toss's reposition
value or Cloak and Dagger's Deep-Health half**: Vulnerable's -1 to
Vigilant stacks with any ally also attacking Vigilant that fight (Feint,
Cloak and Dagger - both Martial siblings in this same cluster), and
THE TABEL's own per-stack Vulnerable pricing already prices the
Defense-drop in isolation, not this kind of party-level compounding.
Real value, not captured in the Core Value number above.

**Verdict: reads hot, not "massively over-grants."** Core Value alone
(2.77-4.85 range depending on Defense, before Necrotic or the Vigilant-
synergy upside) sits at roughly 100-130% of the Level 2 budget for a
headroom build, and comfortably on-budget for a bare-minimum-Prereq one
- a real but modest overshoot, the same shape as Boulder Toss's
"positive but not runaway" reading rather than Spellblade's flagged
"massively over-grants" territory. No Cost/Effects change recommended;
worth a light trim (dropping the Shadow-type swap, or capping the
Necrotic/Vulnerable formula at `[half your Meditation Skill Total]`
alone with no suit bonus) only if a future pass wants to pull it fully
back to the anchor, not urgent on its own.
