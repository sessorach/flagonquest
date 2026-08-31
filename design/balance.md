# Balancing FlagonQuest

Aggregate notes on game balance in the broad sense — approaches, recurring
judgment calls, and conclusions from specific balance passes as they
happen. Companion to `design/RULES_DESIGN.md` (which covers rules
*design* decisions — what a mechanic is and why),
`archive/flagonquest_balance_notes_model.md` (which explains the value-economy
model in `archive/flagonquest_balance_notes.xlsx` that this file's analysis
leans on), and `design/balance_weights_notes.md` (a narrower, more
skeptical audit of THE TABEL's actual per-mechanic weights — which ones
are really derived, which are just typed in; `design/balance_weights.csv`
is the same weights as a fast-lookup index, for reference without
scanning prose). This file starts mostly
empty and fills in as real balance passes happen — it's meant to be the
current, living version of the kind of self-notes the designer already
kept in the old Manifesto documents (`archive/flagonquest_manifesto_2k19.md`,
`flagonquest_manifesto_v5.md`).

## The value-economy model, in short

Everything is priced against one anchor: 1 value ≈ +1 to a flip (fixed by
Gambling costing 2 for an Extra Success, so an Extra Success = 2 value).
Every mechanic (Damage, a Card, a point of Health, 1 AP, Gold, Good Luck,
a stack of Protected, and so on) has its own value-per-unit relative to
that anchor — see `archive/flagonquest_balance_notes_model.md` for the full
breakdown of Baseline/THE TABEL/BALANCE and exactly how Value, Target, and
Net are computed for a Technique. Masterwork items don't share Techniques'
clean `Level × 3` Target formula, so balancing them is more about relative
comparison against similarly-priced existing entries than a hard
pass/fail number.

### Estimating a genuinely hard-to-price effect: triangulate, don't guess once

Most mechanics in this model trace back to a real derivation (a card-math
expectation, a stacking curve built from Baseline's own combat math). But
some effects don't reduce to a clean formula no matter how carefully
you derive one — "ignore Wounded's penalties for the rest of the fight"
is a real example: its actual value depends on how many flips it saves,
how many Defenses it matters for, and whether anyone would've had to
spend a resource fixing the problem instead. There's no single
authoritative number to derive there, just several *reasonable* ways to
look at it.

When that happens, the fix isn't to pick the framing that feels most
rigorous and trust it alone — it's to price the same effect through **two
or more genuinely independent framings**, and take the middle. Independent
means they'd only agree by coincidence if the "true" number were
different — not two versions of the same argument dressed up
differently. For Wounded-immunity (see Insanity Potion below), that
meant: (a) the *direct* cost, estimated flip-by-flip (Bad Luck hitting
roughly one attack and one defensive flip per turn, for a couple of
turns), and (b) the *opportunity* cost — what the party's Healer would've
had to spend fixing the same problem instead (2 AP). Two unrelated ways
of looking at the same effect landing within a few tenths of each other
(8.8 vs 5.5, averaging to 7.15) is a real signal the number's in the
right neighborhood — much stronger evidence than either estimate alone,
and cheap to get once you notice you're eyeballing something rather than
deriving it.

Also worth remembering when several *simultaneous* debuffs get bundled
into one prevention effect: don't just sum each one's "if this happens"
value assuming they all land in the same fight. If an enemy is more
likely to throw *one* debuff type at a target than several at once,
price the group as an average across the plausible ones (same
"GM/enemy decides which applies, not the player" logic Predator's Cry's
Crippled-or-Slowed clause already uses), not a straight sum — otherwise
the estimate quietly assumes a worse (better, for the item) fight than
a real one.

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
`Value`/`Target`/`Net` formulas, see `archive/flagonquest_balance_notes_model.md`)
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
- **"Does the threat even show up" discount — reconsidered: doesn't
  apply to consumable items.** Originally applied at ×0.5 to any item
  whose whole effect is *preventing* a debuff rather than granting
  something directly (Calming Brew, Kiss of the Earth, Predator's Cry,
  Muscular Feast), on the theory that a prevention effect only pays off
  if the enemy was actually about to inflict that debuff. Per the
  designer, that reasoning doesn't actually transfer from Techniques to
  consumables: a Technique is a permanent Experience investment
  competing against every other Technique you could have learned
  instead, genuinely wasted for the rest of the game if its niche never
  comes up — but a Potion/Grenade/Food item costs Gold once and then
  just sits in inventory with zero ongoing cost until the exact moment
  it's actually relevant. Since Bleeding/Crippled/Slowed/Taunted/
  Frightened are all common, frequently-recurring effects rather than
  rare edge cases, any reasonably long campaign eventually makes these
  relevant — "does this ever come up" isn't really the open question
  for a held item the way it is for a learned Technique. **Discount
  removed for consumable items** — all four prevention-type Potions/
  Food recomputed at full, undiscounted value (see Passes Completed
  below). The discount still applies where the underlying logic
  actually holds: a genuinely niche Technique, or a Masterwork item's
  specific mechanic, where there's a real ongoing opportunity cost to a
  permanent investment that might never pay off.
- **AP dropped entirely for consumables meant to be drunk ahead of
  time.** A follow-up to the prevention discount above, for the same
  three items (Calming Brew, Kiss of the Earth, Predator's Cry) — AP
  only exists as a resource *in combat* (confirmed during the Social
  Contests/Exploration rework), and these are long-duration (1 hour, or
  "this encounter") consumables clearly meant to be downed during
  downtime, before initiative is even rolled, not mid-fight instead of
  an attack. Dropped the `AP:-2` charge from their Value entirely.
  Their wording was also extended to remove existing stacks of the
  prevented effect, not just future ones (matching Calming Brew's
  original phrasing) — this makes them usable reactively too, in a
  genuine emergency, without needing a second, separately-priced
  "reactive" version of the item: drinking one mid-fight instead of
  ahead of time still costs the normal AP to retrieve and consume it in
  the moment, which is already a real, unmodeled cost baked into actual
  play — the base Value doesn't need to discount for that case
  separately, since a player who uses it reactively is already paying
  for it in AP they wouldn't have spent if they'd planned ahead.
  Originally didn't extend to Healing Potion — flagged at the time as a
  related but distinct problem, since a reactive-only heal doesn't have
  a "drink it ahead of time" mode the way a preventive effect does. See
  the half-AP convention immediately below for how that ultimately got
  resolved instead.
- **Half AP for items with genuinely mixed combat/non-combat use** — a
  third AP treatment, distinct from both of the above, for an item that
  doesn't cleanly sit at either extreme. Healing Potion is the case that
  motivated this: unlike the prevention trio above (overwhelmingly
  pre-fight prep) it's also genuinely used reactively mid-fight, but
  unlike a Grenade (always in-combat) a lot of its real use is just
  topping off Health during downtime, where AP doesn't exist as a
  resource at all. Charging the full `AP:-2` assumes it's always
  reactive; dropping AP entirely (the prevention-item treatment)
  assumes it's never used that way — neither extreme is honest for an
  item that's genuinely both. Splitting the difference: charge **half
  the standard AP cost** (2.75, one AP's value, instead of the full
  5.5), on the read that roughly half of real use is in-combat and half
  is downtime. Healing Potion: ShallowHeal(2)=8, −2.75 = Value 5.25,
  Net −0.75 at Level 2 — a clean fit, restoring its original 2-Health
  grant rather than needing to inflate it to 3 the way a full AP charge
  required. Worth reaching for on any future item with this same
  genuinely-mixed-use shape, rather than defaulting to the full or zero
  treatment out of habit.
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
  guess — see Passes Completed below. **Follow-up:** resolved with a
  ×0.8 realization discount on top of the 2x assumption (net 1.6x) —
  see `balance_weights_notes.md`'s AoE multiplier section.
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

## Reference: War Magic damage baseline

`War Magic` (`T120`) is the designer's own go-to comparison point for
"what does a damaging spellcaster's attack actually look like" — a
Buildable Sorcery Spell (base: *"deals 2 + [your Mind] Fire damage"*
on a hit), capped at **Level 4, not 5** (Feature Budget `1:1, 2:3,
3:4/adv, 4:6/adv`). Worked out two builds per Level (a maximum-damage
dump and a "damaging but strategic" build trading some damage for
range/alt-type/debuffs), using representative Mind values (3/4/5 at
Levels 2/3/4 respectively — no "Baseline Stat" convention exists
elsewhere yet, so treat these as illustrative, not authoritative):

| Level | Mind | Max single-target damage | Strategic build |
|---|---|---|---|
| 2 | 3 | **8** Fire (`Destructive ×3`) | **6** Frost + Slowed 2+[Spades] + range (`Frigid ×1, Lance, Destructive ×1`) |
| 3 | 4 | **10** Fire (`Destructive ×4`) | **7** Shadow + Vulnerable 2+[Diamonds] + range + Good Luck (`Destructive ×1, Corrupting ×1, Lance, Piercing Elements`) |
| 4 | 5 | **13** Fire (`Destructive ×6`) | **9** Shadow + Vulnerable 2+[Diamonds] + Harried + range + Good Luck (`Destructive ×2, Corrupting ×1, Barraging ×1, Lance, Piercing Elements`) |

Rough shape: pure damage climbs 8 → 10 → 13; the "does other things
too" build trades a chunk of that for utility and sits at 6 → 7 → 9 —
a fairly steady, moderate curve, not explosive scaling. War Magic can't
reach Brilliant damage (no Feature offers it — Frost and Shadow are
the only alternates to its Fire baseline), so this benchmark only
covers Fire/Frost/Shadow directly.

**Use case**: a same-Level rough sanity check for whether a Resist
item is actually blunting a representative hit by a noticeable amount,
independent of the Value/Target economy — see the Torso Masterwork
pass below for the first real application of this.

### Torso Masterwork pass — flat-Resist items

First real application of the War Magic baseline above. All four
flat-Resist Torso items read as catastrophic against `Target = Level x
3` — but cross-checked against a real representative hit, each one is
actually blunting **10-25% of a same-Level attack**, a genuine felt
effect the raw Net doesn't convey. Decided, per the designer: accept
these below Target rather than inflate the flat bonus further (which
risks the same eventual-immunity problem that ruled out scaling Ward's
flat bonus this session), and keep the "choose one element permanently
at crafting" design as-is — a real, informed bet the player commits to,
not something to soften into a re-pickable choice. Two allowances feed
into how generous a design to land on: Masterwork items broadly can run
a bit hotter than a strict Target comparison implies, since you can
only equip one per slot; Robes specifically (can't be worn as real
armor, explicitly sacrificing base armor's own protection) get an
additional bump on top of that.

Trimmed from four items to three, since two were genuinely redundant
rather than differently-priced:
- **Cut Attuned Shroud** (`I066`) — a strict subset of Elemental-
  Resistant Armor (flat +2 one element vs. that item's own L1 +1/L2
  +2 same element), not a different design, just a smaller duplicate.
- **Kept Elemental-Resistant Armor** (L1 +1 / L2 +2, one chosen
  element) as the accessible option — Net −2.0/−4.0, 12.5%/25% off a
  same-Level hit.
- **Kept Robes of Resilience** (L3, +1 to all five Resists) as the
  mid-tier generalist — Net −1.5, 10% off a same-Level hit but across
  every damage type at once, a versatility premium the single-hit
  percentage doesn't capture.
- **Reworked Robes of the Elemental Lord** into the L5 capstone: +3 to
  Fire/Frost/Brilliant/Shadow (up from +2), explicit "robe, not armor"
  framing — Net −7.5, ~23% off a same-Level hit (using War Magic's
  L4 benchmark as a floor, since it caps before reaching Level 5).

**Resist double-discount correction (later in the same pass):**
Resist's own per-point rate was found to double-discount the hit
chance — it multiplied an already-landed-hit count by Damage's own
hit-gated rate (2), when a point of Resist against a landed hit
prevents a *guaranteed* point of Health loss and should price at the
guaranteed rate (4) instead. Every Resist rate doubled as a result
(Physical 2.5→5.0, Fire 0.5→1.0, Frost/Brilliant/Shadow 0.25→0.5 each)
— see `balance_weights_notes.md`'s Resist section for the full
derivation. The three Nets above are the corrected numbers (previously
−2.5/−5.0, −5.25, −11.25) — the War Magic percentage-reduction
cross-checks are unaffected, since those describe Resist points against
raw damage, not this model's Value/Net accounting. This also ripples
through Ward's flat-Resist component (Elemental-Attuned Tincture,
Spellblade's Sipper, Elemental Warding Amulet — all recomputed in the
ledger); Elemental-Attuned Tincture in particular now overshoots its
Target by more than its Level's usual tolerance (Net +2.0 against a
~0.975 band) and may need a follow-up trim, unlike the others which
either landed closer to on-target or stayed within their usual accepted
band.

Three items now span L1/2 → L3 → L5, a fair spread without needing a
fourth. None of the remaining Torso items lean on flat Resist, so this
same fix doesn't automatically apply — they got their own pass instead:

- **Armor of Constitutional Integrity** (`I069`) — cut its exact-duplicate
  Neck-slot twin (Periapt of Constitutional Integrity, `I175`), kept
  this one as the sole grantor. Net −1.4, a modest, accepted shortfall.
- **Lifeforce Plate** (`I072`) — refills the wearer to 1 (L3) or 2 (L5)
  stacks of Protected whenever they're at 0. Priced off an estimated
  ~2.5 "relevant empty moments per encounter" (broader than the strict
  1.875-hits anchor, since its trigger also catches incidental chip
  damage, not just a guaranteed major hit — see
  `balance_weights_notes.md`'s Lifeforce Plate section for the full
  comparison against the stricter framing). L3 Net −1.5, L5 Net exactly
  0.

- **Coat of Knit Flesh** (`I070`) — reworked from a per-turn "remove
  stacks of Bleeding" cleanse into a clean once-per-day prevention (the
  first N stacks of Bleeding the wearer would ever gain in a day are
  ignored outright), after the original wording turned out ambiguous
  against Bleeding's own "lose 1 Health when a stack decays" rule —
  read literally, the item's own removal could have triggered that same
  Health loss. Also prompted a general glossary reword tying the Health
  cost explicitly to natural decay, not removal by any means (see
  `scripts/glossary.md`'s Bleeding entry). Rescoped under this file's
  once/day convention (`Target = Level × 4`, not × 3). First priced
  against Bleeding's tapered `value(n)` curve (built for pricing
  Bleeding dealt *to enemies*, where the target might not survive long
  enough for every stack to matter) — that curve caps out at 12,
  meaning L4's Target of 16 was mathematically unreachable through
  stack count alone. Corrected per the designer's steer: a player
  wearing this genuinely eats every stack's Health cost eventually
  (no "might not survive to see it" discount the way an enemy has), so
  prevented stacks price at the full linear rate (4/stack, uncapped)
  instead. Landed exactly on Target both Levels: **N=2 at L2** (Value
  8, Net 0), **N=4 at L4** (Value 16, Net 0).
- **Dauntless Wrap** (`I068`, L1-5) — grants `[thrice the enhancement's
  Level]` stacks of Protected the first time each day the wearer would
  be Downed, before that Health loss lands. Flat once/day Protected
  pricing wildly overshot Target (+5 to +25 across Levels) — that rate
  assumes stacks realized gradually across a normal fight, not a single
  guaranteed lump delivered at the one moment it's certain to help.
  Discounted per the designer's own framing instead: there's no
  guarantee a given day even produces a hit that would Down the
  wearer specifically, and when one does, the fight was probably
  already going badly — this only ever helps in a losing situation, so
  it deserves real leeway rather than being priced as a guaranteed win.
  Landed on roughly once every 3 adventuring days as the realized
  trigger rate (comparable order of rarity to the established
  Poison-frequency convention, scaled to a per-day cadence). Result: a
  clean, linear `Net = −Level` across the whole range (−1 to −5) —
  fits the same accepted-below-Target band as the rest of this cluster.

Still open: Fortified Armor, Fitted Armor, and Jerkin of the Land —
three Torso items still unpriced, one of them (Fortified Armor)
needing its own non-standard "composable amplifier" treatment since it
doesn't grant Resist itself, only conditionally amplifies whatever
Resist is already present.

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
- **Resolved: Fleeting effects and the same-turn-grant snag.** Fleeting
  effects decay 1 stack at the end of the affected creature's own turn.
  Turned out topping off an *existing* stack was never actually broken —
  decay removes 1 from the whole pool, not 1 per source, so pre-existing
  stacks already absorb that turn's -1 regardless of anything gained the
  same turn. The real bug was narrower: a Fleeting effect going from
  **0 stacks to some**, on the affected creature's own turn (the common
  case: any self-buff), has nothing pre-existing to absorb the -1, so it
  eats directly into the brand-new grant. Past fix was an ad hoc "+1 free
  stack" baked into specific grants (e.g. Brace) — worked for the 0-stack
  case, but over-corrected by 1 whenever the target already had stacks,
  and had to be manually remembered per item. **Fixed at the rule
  level**, scoped to exactly the broken case: a Fleeting effect skips its
  next decay after going from 0 to positive, then decays normally from
  there — see `scripts/glossary.md`'s `[Fleeting]` entry and
  `RULES_DESIGN.md`'s "Applied so far" for the full writeup. This means
  every item/technique's stated stack count was already being priced as
  if fully delivered (nothing in this session's math ever discounted for
  the bug), so **no existing pricing needs revisiting** — the rule fix
  just makes that assumption actually true going forward.

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
- **Spirit Quest Ointment (`I116`) is deliberately out-of-model too**,
  same reasoning as Travel Rations — a 24-hour ritual with no combat
  mechanic at all (full Experience respec, once a full night's rest
  follows), it exists purely to establish that respeccing is a real,
  sanctioned thing a character can do, not to be priced against a
  combat Target. Confirmed rather than left unexamined: its recipe
  already carries a deliberate "token cost to prevent abuse," per the
  designer — `Total Materials: 15` (vs. the generic Alchemical Potion
  fallback's 2) and an explicit `Cost: 60 Gold` override, both already
  set on the item itself rather than inheriting `crafting_recipes.csv`'s
  shared fallback. 60 Gold at Level 3 lands in the same range as a full
  permanent Masterwork enhancement of the same Level (Robes of
  Resilience, also 60 Gold) — a real, meaningful gate for something as
  impactful as a full respec, not a token in the "basically free"
  sense. No change needed.
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
  multiplier itself. **Follow-up:** the multiplier itself did end up
  getting revisited after all — a real, previously-uncosted downside
  (AoE is unconditional and can't avoid catching allies, and is harder
  to land a clean multi-enemy hit with than aiming at one target) turned
  into a ×0.8 realization discount on the 2x assumption, net 1.6x. Both
  items land within their Level threshold at that rate without touching
  their raw Damage/Debuff numbers at all — see
  `balance_weights_notes.md`'s AoE multiplier section.
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

  **Follow-up pass, closing out the remaining shortfalls**: Vulnerability,
  Harrying, and Psychosis Poison all bumped from 1× to 2× Potency,
  matching Bloody Poison's own already-accepted precedent. Root cause
  was the same across all three: Crippling Poison lands exactly on
  Target at 1× Potency because Crippled's own per-stack rate (1.5) is
  high enough to get there at that multiplier, but Vulnerable's rate
  (1) and Harried's continuously-active-via-Poison rate (also 1, reusing
  Vulnerable's formula) can't reach Target the same way at 1× — a lower-
  rate keyword needing a bigger multiplier, not a poison-specific flaw.
  Vulnerability and Harrying now land at Net +3 (an accepted overshoot,
  the same magnitude as Bloody Poison's own +2.75); Psychosis lands at
  +0.9, a genuinely clean fit. Slowing Poison was deliberately left at
  1× — it already carries its own extra realization discount (Slowed's
  value depends on movement actually being contested, unlike a flat
  attack/defense penalty), and bumping it would have overshot by roughly
  +4.2, more than any of the others.

  **Standing convention, stated by the designer while reviewing this
  pass: Poisons can reasonably carry a wider balance berth than other
  item categories, and the low end of their Level range matters more
  than the ceiling.** Two reasons given: Poisons are single-target,
  narrower in impact than an AoE Grenade or a self-buff Potion by
  nature, so a stronger-than-Target application doesn't swing a fight
  the way an equivalently-overshooting party-wide buff would; and the
  archetype that leans hardest on Poisons — a dedicated alchemist —
  realistically gets more mileage from applying them steadily at
  whatever Level they can currently make than from chasing the biggest
  possible Potency on rare, maxed-out applications. Practical effect:
  when a Poison flavor's own curve makes hitting Target exactly
  impossible at a clean integer Potency multiplier, prefer erring
  toward a stronger low-Level fit over a perfectly-centered one that
  reads weak at Level 1-2 — the overshoot at Level 5 matters less than
  it would for most other categories.
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
