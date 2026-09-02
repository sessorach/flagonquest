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
  Attuned Tincture, Spellblade's Sipper, Elemental Warding Amulet), all
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

### Ward = a rule change (+1 → +2 Resist), plus a diminishing-return duration curve — not a flat number, not a compounding one

Two questions were open here: should Ward scale magnitude per stack
(mirroring Hasted), and what should its actual per-application value be.
Both are now resolved.

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

All Storage pricing rescopes to the once/day convention (`Target =
Level × 4`, `Rate = 1`) rather than per-encounter, and assumes optimal
use throughout (the owner actually carries useful items in the extra
slots, or has something worth hiding when it matters) — the same
"rational player" convention used for elemental Resist picks elsewhere
in this model.

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
