# Balancing FlagonQuest

Aggregate notes on game balance in the broad sense — approaches, recurring
judgment calls, and conclusions from specific balance passes as they
happen. Companion to `design/RULES_DESIGN.md` (which covers rules
*design* decisions — what a mechanic is and why),
`design/flagonquest_balance_notes_model.md` (which explains the value-economy
model in `archive/flagonquest_balance_notes.xlsx` that this file's analysis
leans on), and `design/balance_weights_notes.md` (a narrower, more
skeptical audit of THE TABEL's actual per-mechanic weights — which ones
are really derived, which are just typed in). This file starts mostly
empty and fills in as real balance passes happen — it's meant to be the
current, living version of the kind of self-notes the designer already
kept in the old Manifesto documents (`archive/flagonquest_manifesto_2k19.md`,
`flagonquest_manifesto_v5.md`).

## The value-economy model, in short

Everything is priced against one anchor: 1 value ≈ +1 to a flip (fixed by
Gambling costing 2 for an Extra Success, so an Extra Success = 2 value).
Every mechanic (Damage, a Card, a point of Health, 1 AP, Gold, Good Luck,
a stack of Protected, and so on) has its own value-per-unit relative to
that anchor — see `flagonquest_balance_notes_model.md` for the full
breakdown of Baseline/THE TABEL/BALANCE and exactly how Value, Target, and
Net are computed for a Technique. Masterwork items don't share Techniques'
clean `Level × 3` Target formula, so balancing them is more about relative
comparison against similarly-priced existing entries than a hard
pass/fail number.

## The balance ledger (`design/balance_ledger.csv`)

A running, human-readable record of every item/Technique that's actually
been run through the value model — one row per entry, columns `ID, Name,
Category, Level, Value, Rate of Use/Encounter, Target, Net, Grants,
Notes`. `Grants` is the plain-text breakdown of which THE TABEL mechanics
(and how many units of each) the entry was scored as granting — written
out instead of left implicit, so a later pass can see exactly what fed
the `Value` number without re-deriving it. `Notes` is the important
column: a sentence or two on *how* each estimate was made — which THE
TABEL mechanic an effect got mapped to, any discount applied and why, and
an explicit flag whenever a number is a rough guess rather than a clean
1:1 translation. The `BALANCE` tab in `archive/flagonquest_balance_notes.xlsx`
is this ledger's ancestor and works the same way mechanically (same
`Value`/`Target`/`Net` formulas, see `flagonquest_balance_notes_model.md`)
but has no equivalent "why" column — recovering that reasoning after the
fact was most of the work behind this file's Historical Pricing Logic
section above, which is exactly the gap this ledger exists to stop
recreating.

**Methodology established during the first pass (see Passes completed,
below, for the actual results):**
- **AP cost of using an item** is charged as a negative `1 AP` grant
  (weight 3), not folded into a discount elsewhere. A Potion costs 2 AP
  total to use in combat (1 AP to draw it per the Retrieving Items rule,
  1 AP to drink it per the `[Potion]` tag) — a Grenade costs 2 AP as a
  normal attack action (`Making an Attack` — the model does not also
  charge a separate 1 AP draw cost for Grenades, matching how the
  existing reference rows in the old sheet already priced them). A
  Poison's 2 AP application cost is charged **once**, not once per
  encounter, since a poisoned weapon stays poisoned for up to an hour or
  until it lands a hit — see the Poison note below for why this still
  nets out to `Rate of Use/Encounter = 1`.
- **Scoping window: `Rate` and `Target` have to match, not fight each
  other.** THE TABEL's default is per-*encounter* (`Target = Level × 3`,
  most Techniques/items assumed usable once an encounter). Corrected
  convention for anything that's naturally a per-*day* resource instead
  (Food, and anything else whose real cadence is "once an adventuring
  day" or rarer): **rescope the whole row to a one-day window** —
  `Rate = 1` (it triggers once, within its own one-day window, not a
  fraction of an encounter), and `Target = Level × 2 × (2 / times used
  per day)` — for a once/day item that's `Level × 4`; an every-other-day
  item would use `times per day = 0.5`, giving `Level × 8`. The earlier
  version of this pass mixed scopes (a per-encounter `Target = Level × 3`
  left untouched, with `Rate` separately discounted by a
  2.5-encounters-per-day conversion) — that double-counts the
  infrequency penalty once on each side of the formula, since the
  point of the wider Target is specifically to *compensate* for not
  getting to use the effect every encounter, not to be discounted again
  on top of that by a shrunken Rate. All 5 Food rows in the ledger were
  re-scored under the corrected version — see Passes Completed below for
  how that changed Power Snack, Hearty Meal, Muscular Feast, and Soul
  Soup's numbers. Sift's own weight (see `balance_weights_notes.md`) is
  *separately* scoped to "how much value actually lands within a
  one-day window" for the same reason — a different question from how
  often the granting item itself can be re-triggered.
- **"Does the threat even show up" discount (×0.5)**, for any item whose
  whole effect is *preventing* a debuff rather than granting something
  directly (Calming Brew, Kiss of the Earth, Predator's Cry, Muscular
  Feast) — a prevention effect only pays off if the enemy was actually
  about to inflict that debuff, which won't happen every single
  encounter it's carried into, unlike a Grenade's own effect which pays
  off the moment it's used.
- **The "refund a Technique use" trick**, for items whose whole effect is
  handing back the use of an Encounter Technique (Soldier's Salts,
  Fighter's Friend, Soul Soup) — THE TABEL has no mechanic for this, so
  a refund is priced at the refunded Technique's own `Target` budget
  (`Level × 3`), on the assumption the player gets that Technique's full
  value back out of it. A clean trick, but it assumes the player actually
  has a good Technique of that Level sitting unused to refund — its real
  value swings a lot with what's actually in the build.
- **Model gaps** — THE TABEL has no weight for Cover/terrain control at
  anything but a flat per-unit rate (Smokejar, Immaculate Adhesive).
  Items that lean on this got a flagged, rougher approximation rather
  than a clean translation — see each row's own `Notes`. Resist and
  Hasted were also gaps when this pass ran (Elemental-Attuned Tincture,
  Elemental Warding Amulet, Swiftblade Vial all used rough guesses) but
  have since been properly derived — see `balance_weights_notes.md`.
  Elemental-Attuned Tincture's Value in this ledger still reflects the
  old guess (1 Protected-equivalent) and hasn't been recomputed against
  the real Resist weight yet.
- **AoE multiplier — confirmed at ×2, not the original ×1.5 guess.**
  The designer's actual balancing assumption for area-effect Grenades
  (Hellfire Bomb, Thunderclap-in-a-Jar) is "2 enemies hit" — deliberately
  bad value if only 1 target is caught, above-rate if 3+ are. Applying
  the real number surfaced a genuine finding rather than just fixing a
  guess — see Passes Completed below.
- **Dropped the old sheet's "Autoswing" credit on Grenades.** The 4
  existing reference rows (Bottled Fire, Bonemelter, Sunbeam, Hellfire
  Bomb) each carried a flat Autoswing bonus (a 💯-tagged mechanic worth
  5.5, meant for genuinely guaranteed-hit effects — see the "Elementalism
  can't autoswing" line in `flagonquest_manifesto_v5.md`, implying other
  attack types *can*). Current rules text is explicit that Grenades still
  roll a normal attack against Dodge Defense (`Making an Attack`, the
  `[Grenade]` glossary tag) — nothing about them auto-hits. This reads as
  a stale holdover from an older draft where Grenades may genuinely have
  auto-hit, not something that still applies, so it was **not** carried
  forward for any row in this pass, including recomputing the 4 existing
  reference items fresh without it (see Passes Completed for how their
  numbers shifted).

## Historical Masterwork/magic-item pricing logic (from the old site)

Pulled from `archive/flagonquest_site_other.md` (the old Google Sites
export's "DM Notes" and "System Mk 2" sections) while looking for the
usage-frequency assumptions behind Masterwork pricing. Two passes, from
different eras — kept both since the later one's derivation explains
*why* the current flat `Level × 20` pricing looks the way it does, even
though neither era's actual numbers are what's live today.

**Earlier pass — Common/Uncommon/Rare/Extraordinary tiers ("DM Notes").**
Masterwork items priced 6/12/24/48 Gold across four power tiers, each
with a rough Technique-Level equivalent:
- **Common** — minor, convenient power ("a weapon that turns into other
  weapon types"), roughly mimics a Level 1 ability with restrictions.
- **Uncommon** — real passive mechanical benefit (inherent Pushes,
  always-on weapon/armor bonuses), roughly a Level 2 ability with
  little restriction.
- **Rare** — a substantial, constant bonus (temp HP every fight,
  extended spell range) — powerful enough to stop trying to mimic
  specific abilities, but called "Level 4-ish" if it did.
- **Extraordinary** — "the dumpster for everything that's disgustingly
  good" — top tier, minimal restraint.

Assumed a character ends up with **~7 magic items total** (1
Extraordinary + 1 Rare + 2 Uncommon + 3 Common), and set a broader Gold
benchmark: **1200 Gold ≈ "the average magic item a party could
realistically afford to buy."**

**Later, more refined pass — the actual per-use derivation ("System Mk
2").** This is the part that looks like the real ancestor of the
current design philosophy:
1. Assumed consumable spending of ~1.5 Gold/session (1 Healing
   Potion/session + 1 tricky-fight consumable every other session), and
   ~1.5 fights/session — working out to **roughly 1 Gold of consumable
   value "spent" per fight**.
2. Asked: how many times would a character need to *use* a static
   magic item for its passive benefit to match that same per-fight
   value? Picked **12 uses** as the benchmark ("because it's
   convenient").
3. Item price = (per-fight consumable value) × 12 — sanity-checked
   against Fortifying Concoction: 6 Gold ≈ 12 uses of "2 temp Health
   for a scene," so a Level 2 item priced at 6 Gold should deliver
   about that much passive benefit.
4. Produces a Level-based pricing ladder: **Level 2 = 6G, Level 3 =
   12G, Level 4 = 24G, Level 5 = 36G** (a later note revises the top
   end from the earlier pass's 48 down to 36).

**Takeaway.** The throughline across both old passes, and into the
current flat `Level × 20` Masterwork pricing, is consistent: **a
Masterwork item's value is calibrated against a consumable of the same
Level, used repeatedly (the old math landed on ~12 times) rather than
once.** The current system dropped the granular Gold-tier/use-count
bookkeeping in favor of round numbers, but the underlying assumption —
Masterwork items are priced like Techniques of their Level because
they're assumed to get used enough over time to be worth it, same as
the user confirmed when this file was started — looks unchanged. Worth
keeping in mind for the upcoming Masterwork balance pass: if a
drafted item's power doesn't obviously look like it'd get used ~12
times per relevant span (session, or however "makes par" ends up being
defined for the current system), that's a signal its Level or its
actual effect may need adjusting, not just its raw Value-model number.

## Open balance work

- **The full Masterwork list, 103 items total** (`items.csv` `I057`-`I115`
  pre-existing, plus `I148`-`I165`, `I168`-`I189`, and `I208`-`I211`
  newly drafted across three gap-fill passes — see `RULES_DESIGN.md`'s
  "Old-docs review," "Site export gap-fill," and "Final Masterwork
  completeness/dedup sweep" entries) needs to be run through the value
  model to get properly statted and leveled — this is the next planned
  pass, and the gap-fill work feeding it is now done. `I210` Scaraculpi's
  Gleaming Justice (unconditional Good Luck on all attacks, no action
  cost) is flagged in RULES_DESIGN.md as a first candidate worth
  sanity-checking, since it's stronger than `I103` Thrumming Focus's
  otherwise-similar AP-gated version. **Expect Resist-granting items to
  read as underpowered across the board** — Physical Resist and a single
  element's Resist aren't remotely the same value (~5-10× apart after a
  damage-share correction narrowed the original ~7.5-15× gap; see
  `balance_weights_notes.md`), and every existing Resist item already
  checked against the derived weight comes back meaningfully negative
  (Attuned Shroud, Elemental-Resistant Armor, Robes of Resilience, Robes
  of the Elemental Lord). Decide deliberately whether that means these
  items need real numeric buffs/Level cuts, not just each one
  individually — this is a systemic pattern, not isolated undertuning.
- The site-export batch also added 18 non-Masterwork items (`I190`-`I207`)
  that don't need value-model leveling but should get a normal
  price/rarity sanity check alongside the rest — the 4 that are
  Potions/a Grenade (`I204`-`I207`) got that check as part of the
  alchemy pass below; the other 14 (Pack/Gear, Tool/Kit) are flavor/
  utility goods with no combat mechanic to price and don't need one.

## Passes completed

### Alchemy-craftable set — Potions, Grenades, Poisons, Food (38 items)

First real pass through the value model, run as a smaller test case
before tackling the much larger and more varied Masterwork list — every
`Category: Potion/Grenade/Poison/Food` row in `items.csv`. Full row-by-
row results, including every `Grants` breakdown and `Notes` estimate, are
in `design/balance_ledger.csv`; methodology (AP costs, the 2.5-encounter
conversion, the prevention discount, the refund trick, the AoE
multiplier, and dropping "Autoswing") is above. Poisons `I050`-`I056`
were each evaluated at a representative Level 3 (Potency 3), since their
actual Level is inherited from whichever Level of `I049` Basic Poison
they're crafted onto rather than being fixed.

**Findings worth acting on, not just noting** *(Net figures below are
current as of the 1 AP / AoE-multiplier corrections above — updated from
the values first reported when this pass landed)*:
- **`I206` Revivification Draught reads as significantly overpowered**
  for its Level — Net +15.5, sharply higher than every other Level-5
  item in the batch (Insanity Potion ≈ −18.5, Swiftblade Vial ≈ −10, and
  the strongest Grenade, Thunderclap-in-a-Jar, +19.5 — though that one's
  now its own flagged AoE finding, see below, not a fair comparison
  point anymore). Healing Potion's own Level 3 / 2 Health baseline
  implies roughly 0.67 Health per Level as this model's going rate;
  Revivification's 9 total Health implies ~1.8 Health per Level, well
  over double. Worth revisiting the healing amount directly, not just
  the Level.
- **`I043` Healing Potion itself reads as underpowered** for its Level
  (Net −6.5, one of the weaker Level 3 entries) — worth a look in the
  opposite direction from Revivification, and possibly the two should be
  reconciled against each other directly rather than independently.
- **Poisons read as systematically weak across the board** (Net ranging
  roughly −11.5 to −13.75 at a representative Level 3, the worst of any
  category) — this comes from a real structural cost the model doesn't
  apply to anything else: a poison's payoff is contingent on *two*
  separate rolls succeeding (the weapon attack landing, then the
  poison's own Concentration-vs-Vital-Defense flip), where every other
  consumable here only has one contingency layer (or none). This might
  mean Poisons are correctly priced as a niche, situational tool rather
  than a straight damage/debuff item and shouldn't be pushed to hit the
  same Net-≈-0 bar as everything else — or it might mean the double-
  contingency discount is too harsh, or that Poison effects (Potency
  scaling) need a real numbers bump. Flagging the pattern rather than
  picking an answer.
- **`I207` Quartz Tincture** (one of our own newly-drafted items) is
  notably weaker than its Level 4 single-target peer Sunbeam (Net −5.5
  vs. +2.5) — worth a look alongside the Masterwork pass as the same
  drafting batch.
- **Food's Target formula was fixed after this pass first landed** — the
  original version mixed a per-encounter `Target = Level × 3` with a
  separately-discounted per-day `Rate`, double-counting the infrequency
  penalty (see the corrected methodology above). Re-scored under
  `Rate = 1` / `Target = Level × 4` (the once-per-day convention), the
  category reads much healthier: **Hearty Meal lands exactly at Net 0**,
  **Power Snack at −0.39** (using Sift's own corrected weight, see
  below), **Soul Soup at −1**, and only **Muscular Feast stays notably
  weak at −3** (likely more about the prevention-contingency discount
  than the day/encounter scoping this time). Travel Rations remains
  out-of-model (no combat mechanic to price).
- **Sift was undervalued in the old sheet, but not for the reason it
  first looked like.** THE TABEL's 0.64 turned out to have no traceable
  derivation at all (see `balance_weights_notes.md`); simulating the
  actual mechanic (Sift lets you discard cards ≤7 and reshuffle the rest
  back in — verified that "sent to the bottom" cards actually get
  reshuffled randomly, not kept in a fixed low-priority spot) gives a
  **true long-run value of ~1.62/card**, but only ~0.60/card actually
  lands within a single adventuring day (~18 draws, estimated from
  Baseline's own attack-frequency numbers) — which is the correct window
  to use for something like Power Snack that resets daily. The old
  0.64 turns out to be close to the *right* per-day number almost by
  coincidence, not by the reasoning that produced it.
- **The AoE multiplier is now confirmed at ×2 (the designer balances
  area Grenades assuming 2 enemies hit), and applying it honestly
  exposes a real problem, not just a corrected guess.** Hellfire Bomb
  and Thunderclap-in-a-Jar jump to Net +14.5 and +19.5 — far above every
  other item in the batch, including same-Level single-target Grenades
  (Sunbeam +2.5). Both use the *same* raw per-target Damage as their
  single-target peers, then get doubled on top for the AoE credit —
  which is very likely the actual issue: **an AoE item's raw per-target
  numbers should probably be set lower than a same-Level single-target
  item's from the start**, since the ×2 credit is already baked into how
  it's meant to be priced. Worth trimming the raw Damage/Debuff numbers
  on these two specifically during the real pass, not re-litigating the
  multiplier itself.
- **1 AP locked at 2.75 (down from the old sheet's 3), and the whole
  ledger recomputed against it** — every AP-costed row (all 32 Potions/
  Grenades/Poisons, each at `AP:-2`) shifts by a uniform +0.5 to both
  Value and Net, since only the AP term changed. Confirmed on real
  reasoning, not just Baseline's arithmetic: 1 AP's value is priced as
  the opportunity cost of *not* spending it on an attack instead — AP is
  deliberately scarce (very few things grant it directly) and quantized
  (an attack always costs a full 2 AP, never a fraction), so `(value of
  one attack) ÷ 2` is the direct, correct reading of what any other
  AP-costed effect needs to beat. See `balance_weights_notes.md` for the
  full reasoning.

**Lower-confidence spots, flagged in the ledger but not necessarily
wrong:** the Cover/Difficult-Terrain approximation on Smokejar/
Immaculate Adhesive (now at least using the same confirmed "2 enemies"
assumption, but not double-checked the way Hellfire Bomb/Thunderclap
were); and Insanity Potion's multi-effect translation overall (the
single messiest item in the batch to price, still). The Resist-mechanic
gap on Elemental-Attuned Tincture and the Hasted-mechanic gap on
Swiftblade Vial are both now resolved — see "Full ledger sync" below.

- **Full ledger sync against every corrected weight from the
  buffs/debuffs pass** — every row using a Common Effects keyword with
  its own new curve (Bleeding, Crippled, Vulnerable, Necrotic, Hasted,
  Slowed, Taunted, Frightened), plus the Good Luck/Card/Difficult
  Terrain rate corrections and Elemental-Attuned Tincture's real
  Resist/Ward math, got recomputed. Headline findings: Acidic Flask
  flips from -4.5 to +2.5 (Bleeding's real curve is much higher than
  the old flat weight at 4 stacks); Thunderclap-in-a-Jar's already-
  flagged AoE overpower finding gets worse under the same correction,
  +19.5 → +26.5, now the single most overpowered item in the ledger.
  Full detail in `balance_ledger.csv`'s own per-row Notes.
- **Poisons were carrying two stacked pricing errors — both fixed.**
  Every Poison row had `AP:-2` baked into its Value, priced as if
  applying the poison cost an action every time it triggered, *and* a
  separate ×0.5 "poison-landing" discount on top of that, treating the
  weapon's own to-hit roll and the poison's own Concentration-vs-Vital-
  Defense roll as two independently-multiplying ~50% gates.

  Both turned out wrong, confirmed with the designer against the real
  rule (`glossary.md`'s `[Poison]` entry — applying a Poison is a
  **one-time, out-of-combat setup action**; the weapon stays poisoned
  for up to an hour and, once a normal attack lands and deals Health
  loss, the poison automatically makes its own attack against Vital
  Defense). The AP charge double-counted an action the wielder wasn't
  spending on the poison at the moment it pays off — that attack
  already pays its own AP and deals its own separately-priced Damage.
  The extra ×0.5 double-counted the *same* contingency a different way:
  per the designer, the whole chain (weapon hits → poison's own
  Concentration-boosted roll) is contingent on "the one attack," not
  two separate coin flips — the same single-contingency treatment a
  Grenade's own on-hit Debuff grant already gets, with no extra
  discount layered on top of the curve.

  Dropping both moves every row up substantially — Bloody Poison and
  Necrotic Poison now read *overpowered* (+2.75, +4.5) rather than
  underpowered, since Bleeding's and Necrotic's own curves are strong
  enough that a single undiscounted application clears the Level×3
  Target on their own. The rest (Crippling -1.5, Vulnerability -4,
  Harrying -6, Slowing -6.25, Psychosis -5.7) remain below Target,
  purely as a function of their own keyword's curve value at this
  stack count now, not any remaining pricing artifact. Necrotic Poison
  keeps its own separate situational-realization discount (×0.75 — does
  the target ever actually heal or gain Protected while the
  slower-decaying stacks last, a genuinely different question from
  "did the poison attack land") and Psychosis Poison keeps its own
  future-hit proc-trigger discount (×0.5 — does a *later* hit land to
  actually fire the effect) — both are real, separate contingencies
  from the poison-landing one that got removed, not further instances
  of the same error.

  Separately, the designer raised (but hasn't committed to) an idea to
  change Poison's own duration rule from "1 hour" to "until your next
  long rest," specifically to avoid the feel-bad of a pre-applied
  Poison expiring unused before a fight — noted here as an open idea,
  not implemented; see `RULES_DESIGN.md`'s open questions.
- **The refund-trick pricing method got a real premium, and the family
  it prices got reshuffled.** "Regain the use of a Technique" has no
  THE TABEL mechanic of its own, so it's priced as if it directly grants
  a second use of the refunded Technique — worth that Technique's own
  Target (`Level × 3`). On its own, that pins Value to *exactly* equal
  Target, leaving zero margin to ever clear an item's own AP cost —
  true of every item using this trick, and why Soldier's Salts and
  Fighter's Friend both landed at precisely `−(2 AP's value)` regardless
  of their own Level (Soul Soup, the AP-free Food version of the same
  trick, was fine for the same reason). Fixed with a **×1.5 premium** on
  the refund's own baseline, same "flexibility is worth something extra"
  reasoning Card's premium over Good Luck's bare floor already uses —
  choosing exactly when to get a second use out of your best Technique
  has real tactical value beyond just "another instance of a fixed
  number." Applied uniformly to all four refund-trick items, not just
  the two that were flagged, since it's a change to the underlying
  convention.

  The premium alone doesn't fully solve it, though — the AP tax is a
  fixed cost (2.75 × 2 = 5.5) against a Target that scales with Level,
  so it eats a much bigger share of a low-Level item's budget than a
  high-Level one's. Checking every (potion Level, refunded Technique
  Level) pair found the "break-even" gap between the two shrinks from
  +1 at low Levels down to 0 by Level 4 — not a flat rule, a real taper.
  Used that to reshuffle the two existing items and add a third:
  **Soldier's Salts** re-Leveled from 2 to 1 (unchanged otherwise — it
  wasn't underpowered, it was costed a Level too high for what it does),
  **Fighter's Friend** re-Leveled from 4 to 3, and a new item,
  **Battlemaster's Brew**, fills the vacated Level 4/refund-4 slot.
  Final family: Soldier's Salts (L1, refund L2, Net +0.5), Fighter's
  Friend (L3, refund L3, Net −1), Battlemaster's Brew (L4, refund L4,
  Net +0.5), Soul Soup (Food L1, refund L1, Net +0.5).
