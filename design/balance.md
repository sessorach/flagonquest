# Balancing FlagonQuest

Aggregate notes on game balance in the broad sense — approaches, recurring
judgment calls, and conclusions from specific balance passes as they
happen. Companion to `design/RULES_DESIGN.md` (which covers rules
*design* decisions — what a mechanic is and why) and
`design/flagonquest_balance_notes_model.md` (which explains the value-economy
model in `archive/flagonquest_balance_notes.xlsx` that this file's analysis
leans on). This file starts mostly empty and fills in as real balance
passes happen — it's meant to be the current, living version of the kind
of self-notes the designer already kept in the old Manifesto documents
(`archive/flagonquest_manifesto_2k19.md`, `flagonquest_manifesto_v5.md`).

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
- **`Rate of Use/Encounter` for anything that's naturally a per-day
  resource, not a per-fight one** (Food, and anything else whose real
  cadence is "once an adventuring day" or rarer) is derived from the
  **2.5-encounters-per-adventuring-day** assumption (roughly 2 combat
  encounters plus enough skill-check/social spend to count as half an
  encounter): a once/day item gets `Rate = 1 / 2.5 = 0.4`; an
  every-other-day item would get `Rate = 1 / 5 = 0.2`. This is a new
  piece of methodology this pass established, not something the old
  sheet's single Food row (Power Snack) used — see the Passes Completed
  entry below for how that changes Power Snack's own number.
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
- **Model gaps** — THE TABEL has no weight for Resist bonuses (Elemental-
  Attuned Tincture, Elemental Warding Amulet-style effects), Hasted
  (Swiftblade Vial), or granting Cover/terrain control at anything but a
  flat per-unit rate (Smokejar, Immaculate Adhesive). Items that lean on
  these got a flagged, rougher approximation rather than a clean
  translation — see each row's own `Notes`.
- **AoE multiplier (×1.5)**, for any Grenade that hits more than one
  creature (Hellfire Bomb, Thunderclap-in-a-Jar) — a genuine guess at the
  average number of effective targets, with no anchor anywhere in THE
  TABEL or the old sheet. This is the single least-confident number-type
  in the whole methodology and worth a gut-check before trusting it on
  a new AoE item.
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
  otherwise-similar AP-gated version.
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

**Findings worth acting on, not just noting:**
- **`I206` Revivification Draught reads as significantly overpowered**
  for its Level — Net +15, sharply higher than every other Level-5 item
  in the batch (Insanity Potion ≈ −19, Swiftblade Vial ≈ −11, and the
  strongest Grenade, Thunderclap-in-a-Jar, only +9). Healing Potion's own
  Level 3 / 2 Health baseline implies roughly 0.67 Health per Level as
  this model's going rate; Revivification's 9 total Health implies ~1.8
  Health per Level, well over double. Worth revisiting the healing
  amount directly, not just the Level.
- **`I043` Healing Potion itself reads as underpowered** for its Level
  (Net −7, one of the weaker Level 3 entries) — worth a look in the
  opposite direction from Revivification, and possibly the two should be
  reconciled against each other directly rather than independently.
- **Poisons read as systematically weak across the board** (Net ranging
  −12 to −14 at a representative Level 3, the worst of any category) —
  this comes from a real structural cost the model doesn't apply to
  anything else: a poison's payoff is contingent on *two* separate rolls
  succeeding (the weapon attack landing, then the poison's own
  Concentration-vs-Vital-Defense flip), where every other consumable
  here only has one contingency layer (or none). This might mean Poisons
  are correctly priced as a niche, situational tool rather than a
  straight damage/debuff item and shouldn't be pushed to hit the same
  Net-≈-0 bar as everything else — or it might mean the double-
  contingency discount is too harsh, or that Poison effects (Potency
  scaling) need a real numbers bump. Flagging the pattern rather than
  picking an answer.
- **`I207` Quartz Tincture** (one of our own newly-drafted items) is
  notably weaker than its Level 4 Grenade peers (Net −6 vs. Sunbeam's +2
  and Hellfire Bomb's +6) — worth a look alongside the Masterwork pass
  as the same drafting batch.
- **Food doesn't fit the shared `Target = Level × 3` formula well at
  all** — every Food item lands solidly negative (−1.4 to −3) purely
  because Food is capped to once/day by rule (`[Food]` tag) and gets
  discounted to `Rate = 0.4` accordingly, not because any of them are
  actually undertuned. The old sheet's own Power Snack row sidestepped
  this by using `Target = 0` and charging the item's Gold cost directly
  instead — worth deciding whether Food should get its own Target
  convention (e.g. `Target = 0`, judged only on whether `Value` clears
  its own Gold cost) rather than being squeezed through the combat-
  encounter formula the rest of the ledger uses.

**Lower-confidence spots, flagged in the ledger but not necessarily
wrong:** the AoE multiplier on Hellfire Bomb/Thunderclap-in-a-Jar; the
Cover/Difficult-Terrain approximation on Smokejar/Immaculate Adhesive;
the Resist-mechanic gap on Elemental-Attuned Tincture; the Hasted-
mechanic gap on Swiftblade Vial; and Insanity Potion's multi-effect
translation overall (the single messiest item in the batch to price).
