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
- **Speed = 0.6/point** (Agility 3, i.e. Speed 4, agreed as the
  representative baseline for most movement). Not a mechanic THE TABEL
  currently has a row for at all, despite real items granting flat Speed
  (Feathered Sandals, Slipstream Sandals, and others) — added here since
  Push and Difficult Terrain both turn out to be priced off of it.
  Derivation: 1 Move action costs 1 AP and covers up to Speed meters, so
  the value of +1 Speed is the AP saved covering the same ground —
  `(1 AP's value) ÷ (Speed + 1) = 3 ÷ 5 = 0.6`.
- **Push = 0.6/meter.** Directly Speed's own per-point rate — a Push is
  forced movement, priced the same as any other meter of movement.
- **Difficult Terrain = 0.6/degree.** Same rate as Push and Speed: 1
  degree costs exactly 1 extra meter of Speed to cross 1 meter of the
  terrain, so it's priced in the same currency. Difficult Terrain still
  carries an extra wrinkle Push doesn't, though — it's usually granted as
  a *zone* effect ("the space gains N levels of Difficult Terrain") that
  can affect more than one creature crossing it, inheriting the same
  AoE-estimation uncertainty flagged for Hellfire Bomb/Thunderclap in
  the alchemy ledger, on top of the per-degree rate itself.
- **Resist — a different value per damage type, not one shared rate.**
  THE TABEL never had a Resist row at all, despite 7 current Masterwork
  items granting it. This is explicitly out of scope for base weapon/armor
  Resist — those are "designed to fit the assumptions" directly and don't
  get run through this model — it's only for *bonus* Resist a Masterwork
  item or consumable grants on top of that.

  Resist prevents 1 point of damage on *every* future hit of that type
  for as long as it's active (not a one-shot like Protected), so its
  value is `Damage's own weight (2, mirroring granting vs. preventing a
  contingent point of harm) × how many hits of that type actually land`.
  "How many hits of that type land" needed two inputs with no existing
  derivation, both taken directly from the designer's own stated rule of
  thumb rather than derived: **enemy type mix** — 3 in 4 enemies are
  Physical-only, 1 in 4 deal an element, and among those, Fire is twice
  as common as Frost, Brilliant, or Shadow individually (Fire 10% of all
  enemies, each other element 5%) — and **total hits landed per player
  per encounter**, worked out from Baseline's own existing combat math
  (10 enemy-rounds/fight × 1.5 attacks/round, split across a 4-player
  party, at 50% hit chance ≈ **1.875 hits/player/encounter, any type**)
  rather than a new guess.

  Combining those: **Physical Resist ≈ 2.8/point**, **Fire Resist ≈
  0.375/point**, **Frost/Brilliant/Shadow Resist ≈ 0.19/point each** —
  Physical is worth roughly **15×** a single element, confirming the
  designer's own intuition sharply, not just directionally. Checked
  against the 4 existing chosen-element/elemental Resist items already
  in the catalog (assuming Fire is chosen where there's a choice, since
  a rational player would): **every one reads meaningfully underpowered
  for its Level** — Attuned Shroud −2.25, Elemental-Resistant Armor
  −2.6 to −5.25 depending on Level, Robes of Resilience −5.25, Robes of
  the Elemental Lord −13.1. This is a real, consistent pattern, not
  noise from one bad row — flagging it for the actual Masterwork pass
  rather than fixing it here, same as the alchemy pass did with Poisons:
  it might mean these items are genuinely overpriced/over-leveled for
  what they deliver, or it might mean a pure expected-hits model is
  missing something real about Resist's value (burst/spike protection
  in a single big hit, not just average damage over time) — worth
  deciding deliberately rather than defaulting to "buff everything."

## Plausible, not confirmed — the numbers line up with something real,
## but the workbook never says so

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

## What's still open

Every weight that started this audit unresolved (Sift, Push, Difficult
Terrain, Resist) now has a Pencil derivation, and Damage and Autoswing
are fully Locked. The AoE multiplier used on area-effect Grenades
(Hellfire Bomb, Thunderclap-in-a-Jar) is also confirmed — the designer
balances these assuming **2 enemies hit** (deliberately bad value
against 1, above-rate against 3+) — but plugging that in surfaces a real
finding, not just a settled number: see `balance.md`'s Passes Completed
entry. What's left, if anyone wants to push further:
- Sift's ~0.60/card figure is calibrated to a once-per-day window
  specifically — a Technique that grants Sift on a different trigger
  (e.g. a combat-conditional one, which is how the design intentionally
  keeps Sift from being freely spammable — an unconditional, on-demand
  Sift really would be strong, given how gently its value decays under
  repeated use) would need the same simulation re-run for its own actual
  window, not a reused constant.
- Difficult Terrain's AoE/zone-effect scope now has the same "2 enemies"
  assumption to use as Grenade AoE (already applied to Smokejar/
  Immaculate Adhesive in the alchemy ledger), but check whether those
  two rows' own numbers hold up the same way Hellfire Bomb/Thunderclap's
  didn't once the confirmed multiplier is actually applied carefully.
- The Resist finding — every existing elemental-Resist item reading
  underpowered — is a real pattern to act on during the Masterwork pass,
  not a loose end in the weight itself. The weight's own derivation is
  solid (built entirely from already-Locked/confirmed pieces: Damage's
  weight, Baseline's own combat-frequency math, and the designer's
  directly-stated enemy-type mix); what's undecided is what to *do*
  about the items it exposes as under-tuned.
- Protected's 75% discount and 1 AP's "plausible, not confirmed"
  reconstruction (2.75 vs. the sheet's 3 — still an open decision, not
  yet locked either way) are still open, not settled the way Good Luck/
  Card/Pressure/Sift/Push/Difficult Terrain/Damage/Resist/Autoswing now
  are.
