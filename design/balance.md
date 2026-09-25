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

### Every adjustment goes on one side of the ledger: say which, every time

A pricing check compares two numbers. **Target** is what the
Technique or item is owed (its budget). **Value** is what it actually
delivers. Every adjustment belongs on one side with a clear sign, and
getting the side or the sign wrong flips the verdict. This has gone
wrong at least twice: once in the base weapons pass (caught by its own
"direction note") and again in the Martial Schools pass, where an
"unarmored" allowance got subtracted from a Technique's Target when it
should have been added.

- **Something the player gives up raises the Target.** A Condition or
  restriction (both hands empty, unarmored, must be two-handed), a
  narrow Skill that pays off nowhere else (Archery), a Held slot. The
  player accepted a worse deal to use the thing, so it's entitled to
  deliver more. Write it as **"+N to Target."**
- **Something the player gets goes on Value.** Every effect the
  Technique produces. A Skill that also pays off elsewhere (Acrobatics
  feeding Dodge, Brawl feeding Dodge and Parry) is also something the
  player gets, so it *lowers* the Target instead: **"−N to Target."**
- **A cost paid each time it's used comes off Value.** AP, a Card, a
  spent Spell charge, Health: `Net = Value − cost`, then compare Net to
  Target. (Mathematically the same as adding the cost to the Target.
  Pick one and don't do both.)

**The one-line check before writing any adjustment down:** *does this
make the deal better or worse for the player?* Worse for the player
(they give something up, they pay something) means the Technique has
to deliver **more** to be on rate. So the Target goes up, or the cost
comes off Value. Better for the player means the opposite. If an
adjustment ever makes a restricted Technique *easier* to be on rate,
the sign is wrong.

**Situational Techniques are priced at their value when used**, per the
designer: what the Technique is worth in the situation it's built for,
not discounted by how often that situation comes up. Used for Parting
Shot/Heelbiter (an enemy trying to leave), each Spellblade option (as
if it's the best pick for the moment), and Slithering Hands (a second
enemy next to the attacker). A narrow trigger or Condition on an
Encounter Technique pays for an extra feature instead of getting a
number. The exception is an effect whose payoff is still uncertain
*after* you've used it (Necrotic only matters if the target later
heals or has Protected); that one does get discounted.

`balance_weights.csv` rows that are adjustments (not per-unit rates)
state their side explicitly in the Value column ("+2 to the
Technique's own Target", "−1 to the weapon's own Target"). Keep new
rows in that form.

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
  encounter, since a poisoned weapon stays poisoned until it lands a hit
  or the wielder gets a full night's rest — see the Poison note below
  for why this still nets out to `Rate of Use/Encounter = 1`.
- **Scoping window: `Rate` and `Target` have to match, not fight each
  other.** THE TABEL's default is per-*encounter* (`Target = Level × 3`,
  most Techniques/items assumed usable once an encounter). Corrected
  convention for anything that's naturally a per-*day* resource instead
  (Food, and anything else whose real cadence is "once an adventuring
  day" or rarer): **rescope the whole row to a one-day window** —
  `Rate = 1` (it triggers once, within its own one-day window, not a
  fraction of an encounter), and `Target = (Level × 3) × encounters
  between uses` — built directly off the same per-encounter Target
  every other item uses, not a separately-derived daily constant, scaled
  by the standing assumption of **2 encounters per adventuring day**.
  For a once/day item that's `Level × 3 × 2 = Level × 6`; an
  every-other-day item spans 4 encounters between uses, giving
  `Level × 12`. (Corrected from an earlier `Level × 2 × (2/times per
  day)` version — `Level × 4` for once/day — that used its own
  unexplained "2" constant instead of tying back to the per-encounter
  Target everything else in the model is built from; caught reviewing
  the Belt Storage items, see below.) The earlier version of this pass
  also mixed scopes (a per-encounter `Target = Level × 3` left
  untouched, with `Rate` separately discounted by a
  2.5-encounters-per-day conversion) — that double-counts the
  infrequency penalty once on each side of the formula, since the
  point of the wider Target is specifically to *compensate* for not
  getting to use the effect every encounter, not to be discounted again
  on top of that by a shrunken Rate. Sift's own weight (see
  `balance_weights_notes.md`) is *separately* scoped to "how much value
  actually lands within a one-day window" for the same reason — a
  different question from how often the granting item itself can be
  re-triggered.
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

## Reference: Everyday-goods pricing tiers

Pack/Gear and Tool/Kit items (kits, bags, basic consumables, and the
like) sit outside THE TABEL entirely — no combat mechanic to run
through the Value/Target economy, so they were never priced by
formula the way Potions/Grenades/Masterwork items are. Reconstructed
here (2026-09-15) from the Cost values already sitting in `items.csv`
across this session's several Pack/Gear and Tool/Kit passes, rather
than invented fresh — the existing numbers turned out to already fall
into a consistent tier system, just never written down:

| Tier | Gold | What qualifies | Examples |
|---|---|---|---|
| 1 | 1 Gold | Consumable and basic — single-use or otherwise spent/used-up goods needing minimal skill or material investment | Alcohol (Simple), Charcoal, Oil, Basic Conveniences, Quicktorch, Travel Rations, Incense (Simple/Quality), Recreational Drugs (Poor/Quality), Embalming Fluid, Rope, Hammer, Shovel, Small Mirror, Iron Spikes, Tripwire Bells, 10-Foot Pole, Torch, Lantern |
| 2 | 2-3 Gold | Basic but permanent — simple everyday gear that isn't used up, but doesn't grant a real Skill-mechanic benefit either | Basic Clothing, Basic Jewelry, Musical Instrument, Knapsack, Adventurer's Belt, Firestarter, Camping Kit, Pickaxe, Chain, Ladder, Block and Tackle |
| 3a | 3 Gold | A genuine mechanical benefit, but a niche one — comes up in specific, occasional situations rather than gating a core, frequently-used Skill activity | Crowbar (force something open), Manacles (restrain a captive), Grappling Hook (reach an otherwise-unreachable anchor point) |
| 3b | 5 Gold | A genuine mechanical benefit that removes a real Bad Luck penalty on a mainstream, frequently-exercised Skill/School, or a bundle of several minor goods in one purchase | The Craft-School kits (Tailor's/Carving/Smithing/Jeweler's), Climber's/Disguise/Tinker's/Fisher's Kit, Mixology Set |
| 4 | +3 Gold per capacity step | Storage capacity, scaling linearly | Knapsack (3g, step 1) → Backpack (6g, step 2) → Rucksack (9g, step 3) → Survivalist's Pack (12g, step 4) |
| 5 | Roughly doubling per size step | Large transport/vehicles — its own scale, separate from worn/carried gear | Cart, Small (12g) → Cart, Medium (24g) → Wagon, Large (48g) |

Two things worth noting, checked rather than assumed:
- **Tier 1 items don't scale by Level**, with one deliberate exception:
  Incense (Quality, Level 2), Embalming Fluid (Level 2), and
  Recreational Drugs (Quality, Level 3) all still sit at a flat 1
  Gold despite a higher Level — a higher Level here is about
  refinement/quality, not more raw material. Alcohol is the one Tier 1
  item that *does* scale (Cost = Level, 1-5 Gold) — an intentional
  exception tied to its own real quality ladder (Simple through
  Legendary), not a tier violation.
- **Tier 4's "+3 Gold per step" is exact**, not approximate — checked
  against all three bag sizes, not just the first two.
- **Medicinal Supply (2 Gold) doesn't fit any tier above cleanly, and
  that's correct, not an oversight.** Briefly moved to Tier 1 during
  this pass, then reverted once the designer caught it — it's
  consumable like Tier 1, but it's not just a passive good the way
  Charcoal or Oil are: it's a genuine mechanical substitute for cards
  from hand on certain Medicine-related Techniques, real ongoing
  utility a Tier 1 good doesn't have. Sits a notch above Tier 1
  despite being single-use for exactly that reason. Worth checking
  any future "basic consumable" candidate for a similar hidden
  mechanical role before defaulting it to Tier 1 on looks alone.

**Use this table directly when pricing the next everyday good**, the
same way THE TABEL's own weights get reached for on combat items,
rather than re-deriving a number by vibes each time. Expected to keep
growing — the designer's next step is identifying more items/
categories to backfill into this scheme.

**Follow-up, same session: Adventurer's Kit retired, split into three
real items.** Per the designer, Adventurer's Kit's old flavor-text
bundle (mess kit, bedroll, waterskin, utility knife, a rope coil, a
tinderbox) hid two items with genuine standalone value behind one
5 Gold purchase. Split out:
- **Rope** (Tier 1, 1 Gold) — the clearest "consumable" case: gets
  cut, burned through, or left behind, so a player would plausibly buy
  more independent of the rest of the kit.
- **Firestarter** (Tier 2, 2 Gold) — reworded from "Tinderbox, with
  flint and steel" to something deliberately open-ended (flint and
  steel, a fire-bow, oil-soaked tinder, whatever the player wants it
  to be), per the designer's own framing. No mechanical Effects text —
  there's no existing "starting a fire" check in the rulebook to hook
  a bonus into, so it stays pure flavor/logistics, same treatment
  Musical Instrument just got.
- **Camping Kit** (Tier 2, 3 Gold) — everything else (mess kit,
  bedroll, waterskin, utility knife), the "hand-wave the boring
  survival details" bundle Adventurer's Kit always mostly was.

New starting-gear total: 1 + 2 + 3 = 6 Gold (up from the old flat 5),
confirmed fine by the designer — reflects the split items' own real
value rather than the old bundle undercharging for what amounted to
two separate useful goods. `rulebook.md`'s three Character Creation
mentions of Adventurer's Kit updated to name all three replacements;
Belt of the Wayfarer's "produce any item from an Adventurer's Kit"
text updated to reference the new trio — its own Value math is
unaffected, since that clause was already priced at essentially zero
(see `balance_ledger.csv`'s `I222` row).

**Follow-up, same session: grouping Tier 1 items under one shared
recipe.** `crafting_recipes.csv`'s `Applies To` syntax has no way to
match several distinct item Names in one clause (clauses AND, not OR)
— rather than extend it for this one case, followed the same pattern
Armor already uses for "one recipe, several paths" (separate rows
sharing a Name). First group drafted: **Basic Convenience** (Basic
Conveniences, Charcoal, Oil — three `crafting_recipes.csv` rows, same
Name/School/Skill Total/Materials, each with its own `Applies To`),
Alchemy, `Mixology or Survival 2`, 1 material of `Medicinal or Wood`
(an OR-pair rather than forcing one material across genuinely
different goods — Charcoal is wood-derived, Oil/soap read as more
Medicinal, and both are valid). Unified Charcoal's own School from a
Cooking/Survival-only design into this Alchemy-with-an-alternate-skill
shape, matching CR016 Food Item's own precedent for "one School, two
valid Skills" rather than branching School itself the way Weapon/Armor
do.

**Follow-up, same session: classic dungeoneering "basic tool" items
drafted.** Brainstormed against D&D/Pathfinder-style adventuring gear
(10-foot pole, crowbar, manacles, and the like), landing on 15 new
`Pack/Gear`/`Tool/Kit` items split into two families:
- **"Basic Tool" family** (Tier 1/2, flavor-only, same `Craft 3` /
  materials-equal-Cost pattern as Rope/Firestarter/Camping Kit),
  split by material the same way Weapon/Armor split by School — metal
  items via Smithing (Hammer, Shovel, Pickaxe, Chain, Small Mirror,
  Iron Spikes, Lantern, Tripwire Bells), wood items via Carving
  (10-Foot Pole, Ladder, Torch, Block and Tackle). Torch is the plain,
  un-alchemized counterpart to Quicktorch — needs an existing flame or
  a Firestarter to light and doesn't get Quicktorch's 1 AP lighting
  shortcut, so it isn't just a strictly-worse duplicate.
- **Niche-mechanical family** (Crowbar, Manacles, Grappling Hook) —
  each does grant a real mechanical benefit (Good Luck forcing
  something open, an actual restraint effect, a genuine reach-an-
  unreachable-anchor tool), which would put them in Tier 3 by the
  existing definition, but per the designer they gate specific,
  occasional situations rather than a core, frequently-exercised
  Skill the way the mainstream 5 Gold Kits do (Climbing, Disguise,
  Lockpicking, etc.) — priced at 3 Gold instead of 5, and the pricing
  tiers table above split Tier 3 into 3a (3g, niche) and 3b (5g,
  mainstream) to keep tracking both cases. `Craft 4`/3 materials,
  same Smithing-tool shape as the Basic Tool family just one skill
  tier up, matching `Tool/Kit` category alongside the mainstream Kits
  rather than `Pack/Gear`. Grappling Hook explicitly requires a length
  of Rope to reach beyond its own short coil, tying it to the Rope
  item from the Adventurer's Kit split above rather than duplicating
  rope-carrying capacity into the item itself.

Not Masterwork items, so no `balance_ledger.csv` rows — that file
tracks THE TABEL's Value/Target economy, which these Pack/Gear and
Tool/Kit items sit outside of entirely, same as everything else in
this pricing-tiers section.

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
  once/day convention (`Target = Level × 6`, not × 3 — see the Scoping
  window correction below). First priced against Bleeding's tapered
  `value(n)` curve (built for pricing Bleeding dealt *to enemies*,
  where the target might not survive long enough for every stack to
  matter) — that curve caps out at 12, meaning even L2's corrected
  Target of 12 would be mathematically unreachable through stack count
  alone. Corrected per the designer's steer: a player wearing this
  genuinely eats every stack's Health cost eventually (no "might not
  survive to see it" discount the way an enemy has), so prevented
  stacks price at the full linear rate (4/stack, uncapped) instead.
  Re-tuned after the once/day Target correction below (Level × 6, not
  × 4) moved the target it was landing exactly on — bumped from
  preventing 2/4 stacks to **3 at L2** (Value 12, Net 0) and **6 at L4**
  (Value 24, Net 0), landing exactly on Target again both Levels.
- **Dauntless Wrap** (`I068`, L1-5) — grants `[three times the
  enhancement's Level]` stacks of Protected the first time each day the
  wearer would be Downed, before that Health loss lands. Flat once/day
  Protected pricing wildly overshot Target (+5 to +25 across Levels) —
  that rate
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
  clean, linear `Net = −3 × Level` (−3 to −15) once the once/day Target
  correction below is applied (was `Level × 4`, giving `−Level`) — a
  deeper gap than before, but **not re-tuned**: unlike Coat of Knit
  Flesh, this item was already deliberately discounted for genuine
  rarity/leeway per the designer's own call, so the wider gap under the
  corrected Target is left as-is rather than closed by inflating the
  stack count or the frequency assumption.

- **Fitted Armor** (`I177`) — reworked from "-1 Might Requirement" (no
  documented mechanical consequence exists anywhere in `rulebook.md`
  for failing a Might Requirement, so the old text was unpriceable)
  into a flat +1 Physical Resist grant, the Physical sibling of
  Elemental-Resistant Armor. Priced against the designer's steer that
  this specific item should be balanced for who actually buys it — a
  tank/bruiser playstyle, not an average character — taking 50% more
  attacks than the party-average baseline, so Physical Resist's own
  rate scales with the hit-count term (5.0 × 1.5 = 7.5/point). Landed
  on **Level 2** (Target 6, Net +1.5) over Level 3 (Net −1.5): unlike
  Elemental-Resistant Armor's chosen-element bet, this grant carries no
  risk or guesswork — a tank gets full, guaranteed value every fight —
  so it doesn't need the same below-Target discount the riskier picks
  in this cluster get; the item's own self-selection (only the right
  build wants it) already does the limiting work.

- **Fortified Armor** (`I071`) — the "composable amplifier" case: it
  doesn't grant Resist itself, only conditionally boosts whatever
  Resist the rest of the build already has. Reworded its trigger from
  "a red card was flipped" (a stale reference to an older design where
  Hearts/Diamonds paired with bonus successes) to "the attack scored an
  Extra Success" — the current rules tie Extra Successes to matching
  the attacking Skill's own single governing suit, not a fixed
  red/black split, so this both fixes the wording and makes the item
  actually do what it was designed for: soften spikes specifically on
  hits that already dealt bonus damage. Priced at the honest suit-match
  rate (25%) × Physical Resist's rate (5.0) × the same tank assumption
  as Fitted Armor (1.5×): Value 1.875, Net **−7.125**, the deepest gap
  in this cluster. Accepted deliberately, not as a miss — per the
  designer, this is meant to have a higher ceiling than a flat
  expected-value model can price (it's countering burst/spike damage,
  the separately-flagged blind spot in `balance_weights_notes.md`'s
  Resist section, not shaving average damage), and there's real design
  room to expand which enemies can score Extra Successes (e.g. Good
  Luck to hit) going forward. Better to leave this underpowered by the
  model than inflate it to hit a Net the model can't actually justify.

- **Cut Jerkin of the Land** (`I176`) — an almost-exact duplicate of
  **Shawl of the Land** (`I150`, Neck): identical effect text, same
  Level, same Cost, differing only by Shawl's extra "24 hours worn
  continuously" clause. Same shape as Attuned Shroud/Elemental-
  Resistant Armor and Periapt/Armor of Constitutional Integrity earlier
  in this pass — a smaller duplicate, not a differently-priced design.
  Also a better fit for Neck's own design lane ("niche, boring, passive
  utility — deliberately not interactive or defensive") than Torso's
  ("direct protection, vitality/healing"), per the slot-philosophy
  STANDING RULE — so Shawl of the Land was always the more natural home
  for this effect anyway. Zero cross-references, safe to remove
  entirely.

That's the full 11-item Torso Masterwork cluster priced or confirmed
out-of-model. Switched strategy after this: work the remaining
Masterwork items **slot by slot** (Belt, Hands, Other, Feet, Head,
Neck, Ring, Held — smallest to largest), saving an archetype-wide pass
for after every slot's been through the model at least once.

### Belt Masterwork pass — final lineup

6 items, spanning Level 1-4. Storage hadn't been priced against this
model at all before this pass — `rulebook.md`'s Retrieving Items rule
was the key check: a belt pouch is already an "easy" 1-AP location
with no stated mundane capacity limit, so these items were never
saving AP over a normal pouch, they're converting a soft, GM-
adjudicated "sure, you can probably fit that" into a hard mechanical
guarantee. Went through two real structural corrections during review
(both documented in full below) before landing here: **Mendicant's
Cord moved off Belt to Ring** entirely (see its own note further down
this file) — "shift 2 points between Defenses" never fit Belt's
"carrying items" lane, it's Ring's "a specific active ability" lane
almost word-for-word.

**Capacity's real value, and why it's priced per-encounter, not
once/day.** First pass treated capacity as an occasional "crunch"
event (once/day scoped). Corrected per the designer: the actual value
is the everyday convenience of never having to choose what stays in
easy reach vs. the backpack — items that would've cost 2 AP to
retrieve now cost 1, every single fight, not once a day. That's the
same AP-saved-on-retrieval logic Quick Draw Belt already uses, so
capacity is now scoped `Target = Level × 3` like everything else,
capped at **3 genuinely-extra slots** realistically used (`3 × 2.75
[1 AP] × ⅓ [niche crunch frequency] = 2.75`) regardless of nominal
pouch count — more pouches past that point buy flavor, not value.

- **Placeholder's Bottomless Belt** (`I189`, L1, 20 Gold) — *"The belt
  has 20 pouches, each an easily-accessible container that can hold a
  small object such as a Potion or Grenade."* Capacity only. Value
  2.75, Target 3, **Net −0.25**.
- **Smuggler's Belt** (`I106`, L2, 40 Gold) — *"The belt has 8 visible
  pouches... each pouch actually has two separate compartments...
  anyone not familiar with the specific belt will automatically fail
  any attempt to discover the non-visible compartments. For 0 AP, you
  may transfer an item from one of this belt's pouches directly into
  the pouch, pocket, or pack of a willing creature within sight."*
  Pouch count bumped 5→8 for flavor (still under the 3-slot ceiling,
  no separate credit). Secrecy priced as **2× Good Luck** (`2.4` each)
  at the corrected every-other-day frequency — per-encounter baseline
  with 2 encounters/day means "every other day" = 1 occurrence per 4
  encounters = **¼**, not the ⅓ niche-crunch rate: `4.8 × ¼ = 1.2`. The
  remote item-transfer ability is priced flat (1 AP-equivalent, 2.75)
  rather than an assumed per-encounter frequency, since its real value
  is contingent on how many items actually get moved, not how often
  combat happens. `Value = 2.75 + 1.2 + 2.75 = 6.7`, Target 6,
  **Net +0.7**.
- **Sash of Deep Pockets** (`I105`, L3, 60 Gold) — *"This belt's
  pouches can hold up to 20 cubic meters (about the size of a small
  closet) worth of stuff, as long as each item fits through a pouch's
  opening — a little larger than a fist. If the belt is removed,
  everything stored inside immediately falls out."* Bumped from L2 to
  L3 and reworked into "the biggest bag you can wear" — modeled
  against **Placeholder's Spacious Satchel** (`I115`, Other slot, L3,
  60 Gold, 100 cubic meters) at the same price point, scaled down and
  echoing its own phrasing style, since the Satchel stays the
  enormous option and this item's identity is being worn and always
  accessible instead. The "falls out if removed" drawback is the
  countermeasure against using it as a Satchel substitute — a
  narrative/logistics deterrent, not priced as a discount since it
  doesn't touch combat value. `Value = 2.75 (capacity) + 1.833 (2
  large-object slots, unrestricted size now vs. the old 1-meter cap)
  = 4.583`, Target 9, **Net −4.42**.

**Two items modeled on the Quick Draw Technique** (`T039`, fixed
Level 2, Passive: *"It takes you 0 AP to retrieve or store an item,
regardless of location"*) — scoped down to something replaceable gear
can grant without outclassing the permanent Technique it echoes:

- **Quick Draw Belt** (`I220`, L2, 40 Gold) — *"Items you carry can be
  retrieved or stored for 0 AP, regardless of their location."* One
  realistic AP-saving retrieval per encounter, priced against the
  backpack case (2 AP → 0 AP, saves 2 AP = 5.5) since "regardless of
  location" is the whole point. No capacity credit (its text doesn't
  grant pouches). Value 5.5, Target 6, **Net −0.5** — lands at the
  Technique's own Level, confirmed by the designer as intentional
  parity ("literally just the Technique but purchaseable with gold").
- **Hair-Trigger Belt** (`I221`, L4, 80 Gold) — *"As an Interrupt for
  0 AP, you may retrieve any carried item, or swap it for one already
  in your hand, regardless of its location."* Same anchor, but
  Interrupt-timed instead of a normal action — reacting to new
  information rather than committing blind, which is what justifies
  the Level jump. Deliberately **no stated use limit** in the text,
  per the designer — priced against a realistic estimate of 2
  Interrupt-worthy moments per fight (`2 × 5.5 = 11.0`) rather than
  writing a hard cap; a player exceeding that in practice is an earned
  outcome, not something to price against. Target 12, **Net −1.0**.

**Belt of the Wayfarer** (`I222`, L2, 40 Gold, renamed from "Survival
Belt") — *"This belt can produce any
item from an Adventurer's Kit at will, though never more than one of a
given item at a time. Once per day, it can also produce Potions worth
up to 2 Levels total — either two Windrunner's Draughts, or one
Thornskin Elixir. Unused Potions fade by the end of the day."* Mundane
kit items (rope, a torch, a bedroll, and similar — see `I004`) price
at essentially zero, same treatment as Jerkin of the Land's nourishment
effect. The daily Potion budget is a genuine point-spend, not a flat
cap — both options land at exactly the same raw value (`2×3=6` for two
Level-1 Potions, `1×6=6` for one Level 2) since Potion Target scales
linearly with Level, so which option gets picked doesn't change the
price. `Value = 6`, `Target (once/day, Level × 6) = 12`, **Net −6** —
the same `−3 × Level` shape Dauntless Wrap's intentional discount
already established. **Flagged for future expansion**: only two
Potions are currently eligible (a deliberate proof-of-concept-sized
list) — add more non-healing, non-Poison, non-Grenade buff Potions to
the pool as they're created, and consider whether other item types
could eventually round out the daily budget too.

That's the full 6-item Belt slot, Level 1 through 4, with Level 5 open
for a future capstone.

### Hands Masterwork pass — final lineup

8 items, spanning Level 1-3. The archive's original one-liner for this
slot ("skill-based non-attack actions") didn't survive contact with the
real catalog — more than half the existing items were attack-granting
or attack-modifying, not skill utility. **Reslotted Sorcerer's Gloves**
(grants a Sorcery attack) **and Staying Gauntlets** (modifies weapon
attacks to non-lethal) **to Held**, where they actually belong. Working
definition going forward: **"utility built around what your hands can
do — manipulate, create, or access something,"** broader than the
archive's phrasing (a couple of items here aren't tied to a specific
Skill flip at all) but still cleanly excluding anything that grants or
modifies an attack.

**Two new Situational Multiplier conventions came out of pricing this
slot**, both now in `balance_weights.csv`:
- **Trigger frequency, standardized to three fixed tiers** — `1` =
  every encounter (no discount), `1/2` = once/day (real recurring
  demand, not every fight), `1/3` = rarer than daily (niche). Was a
  single ad hoc "~1/3" example before; per the designer, don't
  calculate finer gradations than this — an item that lands
  underpowered at the 1/3 tier needs redesigning, not a more precise
  discount.
- **Narrative Utility items** (`Value = 1/3 × the item's own Target`)
  — for effects the model has no real way to price (exploration/puzzle
  value, not combat). Explicitly a labeled guess, not a derivation —
  formalized so the whole category gets one honest, consistent
  convention instead of a different ad hoc number picked per item.

- **Placeholder's Grasping Gloves** (`I223`, L1) — a scoped-down item
  version of the Tender Telekinesis Technique (`T095`): kept its 2 AP
  cost and fixed the range at 5m (was Skill-Total-scaled) so it
  doesn't outclass the Technique or require the wearer to have
  Sorcery/Theurgy. Narrative Utility item — `Value = 1/3 × 3 = 1`,
  **Net −2**. Deliberately not optimized — a fun, quirky Level-1
  pickup, not a min-max choice.
- **Vanishing Gloves** (`I224`, L1) — once/day, conjures a free
  Smokejar into the wearer's hand. Granting a copy of an
  already-priced Grenade makes this clean to cost directly off that
  item's own Value (6.25) against the once/day Target (6) —
  **Net +0.25**, about as tight a fit as this pass has produced.
- **Armory Gauntlets** (`I075`, L1) — retooled from knightly
  "Armory" theming into a smuggling item: conjures any weapon at will
  (0 AP), undetectable to anyone unfamiliar with this specific pair.
  Conjuring priced as a tier-1 draw-speed saving (2.75, happens nearly
  every fight); concealment priced like Smuggler's Belt's secrecy,
  tier-1/3 (0.8). **Net +0.55**.
- **Deft Gloves** (`I076`, L2) — broadened from "Craft for locks/small
  devices only" to all non-attack Craft flips, per the designer's
  steer, landing it at tier-1/2 (2.4 × 0.5 = 1.2) plus a flat
  tinker's-tools convenience credit (0.5). **Net −4.3**.
- **Field Surgeon's Handwraps** (`I153`, L2) — Good Luck on all
  Medicine, also tier-1/2 since several Techniques call for Medicine
  flips directly (real recurring demand, not a niche trigger).
  **Net −4.8**.
- **Nimble Fingers** (`I225`, L2) — reworked from an active "opposed
  Stealth check" ability into a passive Good Luck bonus on Stealth
  flips made specifically to steal an item unnoticed, matching the
  Deft Gloves/Field Surgeon's pattern. Kept narrow (stealing
  specifically), so tier-1/3 applies: 2.4 × ⅓ = 0.8. **Net −5.2**.
- **Mighty Mitts** (`I077`, L3) — three components: a flat
  no-tools-needed credit (0.5, same shape as Deft Gloves'), narrow
  Good Luck on Might-to-destroy (tier-1/3, 0.8), and a once/day 4-AP
  "act as though you'd spent a minute" burst priced as its own
  flagged guess (1.5) rather than derived. **Net −6.2**.
- **Gloves of Spatial Distortion** (`I154`, L3) — reworked to pass
  objects only, not the wearer (the old text accidentally let the
  wearer teleport through, overlapping with Feet-slot Mobility items).
  Narrative Utility item — `Value = 1/3 × 9 = 3`, **Net −6**.

A "steal an item mid-combat, as part of a successful melee attack"
concept ("Cutpurse's Grip") came up designing this slot but is
deliberately **not** an item — the designer wants it as a Technique
instead, flagged as a Level 5 capstone candidate in `RULES_DESIGN.md`'s
Open questions.

### "Other" Masterwork pass — final lineup

7 items originally, now 6 after a cut. Unlike the 7 worn slots, "Other"
has no archive-established design lane — it's just whatever doesn't
occupy a body slot. Working definition based on the actual catalog:
**carried tools and storage that aren't worn**, distinct from Belt
(worn, carries other items) and Hands (worn, active use).

- **Cut Immaculate Spice Rack** (`I162`) — per the designer, the game
  has few Craft flips for creating items in actual play, making this
  item's cooking-specific Good Luck largely irrelevant. Not a strict
  mechanical duplicate of Placeholder's Wondrous Workspace (Good Luck
  bonus vs. a tool-requirement waiver are genuinely separate benefits,
  same split Deft Gloves already established with its own two
  clauses), but Workspace's universal "any School" coverage already
  absorbs Spice Rack's thematic niche. Zero cross-references, removed
  cleanly.
- **Evertoking Bottle** (`I113`, L1) — surfaced as a real combat item
  on closer read, not the "silly narrative" item it looks like on the
  surface: a smoke cloud (Light Cover, reusing Smokejar's own
  established `Cover(relocation): 1` rate) plus a suit-randomized
  debuff attack (+6 vs. Vital Defense) against anyone who ends their
  turn in it. Expected keyword value averaged across the four suits
  (2.4), the standard on-hit discount (0.5), ~2 realized trigger-
  instances/encounter and the same "can't avoid catching allies" 0.8
  realization AoE Grenades get: `Value = 1 + (2.4 × 0.5 × 2 × 0.8) =
  2.92`, **Net −0.08**. Flagged: the +6 attack bonus is unusually
  generous for Level 1, and this used the standard 50% on-hit discount
  without adjusting for it — may be a real underestimate.
- **Unmovable Bar** (`I163`, L1) — pure anchor-point prop, no Skill
  flip, no combat application. Narrative Utility item: `Value = ⅓ × 3
  = 1`, **Net −2**.
- **Placeholder's Indelible Instrument** (`I164`, L1) — per the
  designer, the most purely narrative item in this batch — no
  plausible tactical use at all, unlike the others' stretch cases.
  Treated as fully out-of-model (same as Travel Rations), not even the
  Narrative Utility token credit: `Value = 0`, **Net −3**.
- **Distant Scroll Cases** (`I114`, L2) — paired long-distance
  item/document-sharing cases, pure logistics with no combat angle.
  Narrative Utility: `Value = ⅓ × 6 = 2`, **Net −4**.
- **Placeholder's Wondrous Workspace** (`I165`, L2) — universal
  tool/kit-requirement waiver for any crafting School, the same shape
  as Deft Gloves' "counts as tinker's tools" clause but much broader,
  and now the sole tool-substitute item in the catalog. Priced as a
  bigger flat convenience credit than Deft Gloves' narrow version:
  `Value = 2`, **Net −4**.
- **Placeholder's Spacious Satchel** (`I115`, L3) — priced via the
  Storage capacity model (not Narrative Utility), same reasoning as
  Sash of Deep Pockets, since this is a direct storage item: base
  capacity (2.75) plus 3 large-object slots (credited the full 3-slot
  ceiling rather than Sash's 2, since its 100-cubic-meter volume and
  head-sized opening both exceed Sash's numbers): `Value = 2.75 + 3 ×
  0.917 = 5.5`, **Net −3.5**. Doesn't need Sash's "falls out if
  removed" drawback — not being worn is already a real downside on its
  own.

### Feet Masterwork pass — final lineup

9 items, spanning Level 1-5. Surfaced a real gap in the rate table while
pricing this slot: Speed's existing 0.55/point rate only ever priced
*one* move action, correct for a one-shot effect (Push, Difficult
Terrain) but wrong for a bonus that's live the whole encounter. Derived
**Speed (permanent/gear) = 2.54375/point** from the game's own AP
economy (4 AP/turn, 2 AP/attack, 1.5 attacks/turn average) and a
companion **range-breakpoints tool** (`moves_needed(D, Speed) = ceil((D
− 1) / Speed)`) for tuning weapon/ability ranges deliberately against
the "still attacks" (D ≤ 2×Speed+1) vs. "costs the attack" (D ≥
2×Speed+2) line — both now in `balance_weights_notes.md`.

- **Lightfoot Shoes** (`I109`, L1-5) — flat `+Level` Speed, worn
  continuously. First real application of the new permanent-Speed rate:
  `Value = Level × 2.54375`, landing at a flat ~85% of Target every
  Level. Accepted as a modest, real shortfall.
- **Slipstream Sandals** (`I110`, L2) — once/encounter Teleport 3m,
  priced as an attack-enabler (not raw movement) since it only matters
  on the turn it's the deciding factor between closing-and-attacking or
  wasting the turn approaching: `Value = 5.5`, **Net −0.5**.
- **Vaulting Boots** (`I111`, L3) — rebuilt after the running-start rule
  was cut outright (old flip-guarantee wording replaced with a Good
  Luck grant); four components (attack-enabler, fall-safety, vertical-
  Athletics-budget bypass, Good Luck on jump flips): `Value = 9.3`,
  **Net +0.3**.
- **Greaves of the Stalwart Guardian** (`I112`, L2, down from L5) —
  redesigned after `features.csv` showed Push and Slowed are both
  cheapest-tier Basic Features on the game's most generic techniques,
  not niche at all. Two components (immovability, Slowed immunity),
  each realized 25% of fights: `Value = 5.5`, **Net −0.5**.
- **Feathered Sandals** (`I108`, L1) — moved off plain Narrative Utility
  once "ignores up to 10m of fall distance" was read as a real,
  guaranteed-harm anchor (Health's own rate) rather than a stale flip
  reference: `Value = 4.0`, **Net +1.0**.
- **Shadowcat Slippers** (`I155`, L2) — unconditional wall-running,
  same shape as Vaulting Boots' vertical rider but continuously
  available: `Value ≈ 4`, **Net ≈ −2**. Flagged as the least-grounded
  number in this slot — likely still wants a redesign pass.
- **Swim Flippers** (`I107`, L1, renamed from Cobblestone Boots) —
  full-Speed swimming, no penalty; a water-breathing clause was
  considered then moved to Neck (Diver's Necklace) as a different
  slot's job. Plain Narrative Utility: `Value = 1`, **Net −2**.
- **Surestride Boots** (`I188`, L3) — simplified from "ignores 2 degrees
  of Difficult Terrain" to "ignores the effects of," a pure wording
  change (degree 3+ was never worse to a mover than degree 2 already
  is). `Value = 8.25` unchanged, **Net −0.75**.
- **Greaves of the Warlock King** (`I156`, L5) — once/turn Teleport
  `2×Speed` meters, a two-mode engine (cheap AP-saver vs. full
  attack-enabler) landing at 2 uses of each per encounter: `Value =
  16.5`, **Net +1.5**.

### Head Masterwork pass — final lineup

10 items. A quick audit before pricing flagged **Confident Cap** as
running on defunct rules (its old "front"/"Concession" text predates
the Statements/Pressure rework) and three near-duplicate Good-Luck-on-
a-social-Skill hats sharing the same fluff. Consolidated into **three
Level-2 Skill hats plus a new fourth** (Confident Cap→Persuasion, Cap
of Smug Confidence→Presence, Sympathetic Hat→Rapport, Hat of
Disguise→Masquerade, new), each `Value = 2.4 × 0.5 = 1.2`, **Net −4.8**
— pegged to Level 2 over the model's own preferred Level 1 to match
live Hands-slot precedent (Field Surgeon's Handwraps, Deft Gloves,
Nimble Fingers). **Stoic Skullcap retired** from this family (doesn't
map to an offensive Skill buff); its name/flavor reserved for a future
Neck-slot Pressure item.

- **Cowl of Tranquility** (`I057`, L2, down from L1-5) — cut from a
  charge-scaling range (charges scaled `1×Level`, Target `3×Level`, an
  absolute and worsening gap) to a fixed Level 2 with outright Taunted/
  Frightened immunity. `Value = 5.5`, **Net −0.5**.
- **Mask of Night** (`I058`, L1) — negates the wearer's own darkness
  sight penalty, priced off Heavy Cover's Bad-Luck-twice rule: `Value =
  2.2`, **Net −0.8**.
- **Headband of Telepathy** (`I172`, L1) and **Lens of Daybreak**
  (`I059`, L2) confirmed at their existing Narrative-Utility/½-tier
  numbers (**Net −2**, **Net −4.8**) — no changes.
- **Wizardly Hat of Tam the Tipsy** (`I171`, L3) — first real use of
  Gold's own `1.5` rate for pricing a per-use accounting; redesigned
  from a 2-AP-to-drink version that read as a net loss below Level 4 to
  a 0-AP internal-stock version, landing at exactly `Net = 0` for 2
  matched-Level uses/encounter. Flagged, not resolved: the real usage
  ceiling is uncapped in a hard fight.
- **Crown of Glory** (`I061`, L5) — **set aside, not resolved.** Value
  `13.5` against a once/day Target `30` (**Net −16.5**), the largest
  gap in the slot. A Level-scaling fix was worked out but the real
  question — should a Head item generate party-wide cards at all, or
  is this a capstone-tier effect — is left for after the rest of the
  slots have a first pass.
- **Follow-up: three of four remaining Head-slot backlog candidates
  cut, one drafted.** True-Seeing Lenses, Circlet of Clarity, and
  Comprehend Languages Circlet all reached for a mechanic that doesn't
  actually exist in this ruleset (Invisibility/illusion magic, a
  distinct Charm/domination keyword, a language system) and got binned
  in a row — logged in `IDEAS_BACKLOG.md`'s "Reviewed and declined"
  section. **Third Eye** (`I258`, L1, 20 Gold, Brilliant) is the one
  that grounded out in real mechanics: shortens the rulebook's own
  hour-long "examine a Masterwork item" rule to 10 minutes, plus Good
  Luck on identifying unfamiliar magical effects/phenomena, built as a
  weaker cousin of Artisan's Eye (`T046`). Value ~1.0, Net −2.0 (33%
  funded) at Level 1 — same modest tier as the slot's other
  Narrative-Utility-adjacent items. Full derivation in
  `balance_weights_notes.md`'s own writeup, including a documentation
  gap it surfaced in Artisan's Eye worth a look during a future
  Techniques pass.

### Neck Masterwork pass — final lineup

9 items (of 12 drafted; 3 cut). **Choker of Silent Whispers** cut as a
strictly-worse duplicate of Headband of Telepathy on the wrong slot;
**Cape of Many Pockets** cut as a clean duplicate of Belt's existing
Storage items; **Cloak of Faces** cut as a shelved "THE BIN" idea with
no real precedent to price against (an unconditional, undetectable
transformation, unlike every real Masquerade item's beatable disguise
check).

- **Cloak of Caches** (`I063`) and **Diver's Necklace** (`I064`, both
  L1) — plain Narrative Utility, `Value = 1`, **Net −2** each. Diver's
  Necklace directly confirms the Feet slot's own water-breathing call
  (cut from Swim Flippers, "a different slot's job" — this is that
  slot).
- **Shroud of Shadowy Stillness** (`I148`, L1, down from L2) —
  Good-Luck-on-Stealth-while-still, same shape as the Head hats but
  dropped a Level since no existing item pulls it toward L2: `Value =
  1.2`, **Net −1.8**.
- **Watcher's Mantle** (`I149`, L2) — confirmed Narrative Utility,
  `Value = 2`, **Net −4**.
- **Shawl of the Land** (`I150`, L2) — a real anchor for "doesn't need
  to eat" via Travel Rations' own material cost through the Gold rate,
  plus Health's guaranteed-rest bonus: `Value = 5.5`, **Net −0.5**.
  Known, accepted inconsistency: both components are daily-cadence,
  checked against the standard per-encounter Target rather than the
  once/day one this item's own cadence would technically call for.
- **Snowfall Drape** (`I065`, L3, down from L1-5) — redesigned from a
  3-space line (blew past Target even at Level 2) to a Burst 1
  footprint at a fixed 2 degrees of Difficult Terrain: `Value = 8.25`,
  **Net −0.75**.
- **Choker of Defiance** (`I151`, L1-5) — Sift's suit-pool credit
  properly derived for the first time (0.30/card, on top of Sift's own
  0.60/card), reworked to an Interrupt timing with a "use it or lose
  it" locking clause: `Value = 5.4 × Level`, **Net = −0.6 × Level** — a
  clean, consistent 90% funded at every Level.
- **Cloak of One Thousand Feathers** (`I173`, L2) — an uncapped
  fall-glide, repriced as three components (base prevention, tail-risk
  bump, traversal utility) rather than one blown-up fall-damage number
  after a naive extreme-fall framing proved underspecified: `Value =
  6.0`, **Net = 0**, confirmed by the designer.
- **Fate's Grasp** (`I082`, L4, moved here from Ring — swapped with
  Worry Token, see below) — an unconditional, no-charges Sift keyed to
  whatever the wearer already discards or plays from hand. Its daily
  card-spend total is derivable exactly from the Cycles rule (the Draw
  Cycle's `2 × (Cunning + Mind)` income and the Discard Cycle's
  unconditional end-of-day clear mean everything drawn also gets spent
  before the cycle repeats — 12/day at baseline, not a guess), priced
  at Sift's own daily-cadence rate: `Value = 12 × 0.60 = 7.2` at the
  original 1:1 grant, badly underfunded at its original Level 2 (60%).
  Checked every clean integer multiplier ("twice," "three times," "four
  times") against every Level — whenever the multiplier matches the
  Level the ratio is always the same 120% (not a new fit), but "three
  times" paired with **Level 4** gave the tightest fit found, 90%
  funded: `Value = 21.6`, **Net −2.4**. Moved off Ring since its
  automatic, no-decision trigger is Neck's "passive utility" lane, not
  Ring's "active ability" one (`RULES_DESIGN.md`'s slot table).

Swept while drafting this item's own text: **"thrice" retired
project-wide**, replaced with "three times" everywhere it appeared
(`items.csv`, `techniques.csv`, `features.csv`, `rulebook.md`) — per the
designer, it reads as an archaic outlier once the sequence needs "four
times"/"five times" anyway. Wording only, no mechanical changes.

### Ring Masterwork pass — final lineup

15 items originally drafted; 3 cut (Ring of Charming/Assertive/Bold
Statements, Bloodshard Ring, Flamefist's Approach), 1 moved out (Fate's
Grasp, swapped to Neck) — 12 final: Elemental Warding Band, Mendicant's
Cord, Galeforce Loop, Poison Needle, Ring of Pure Elements, Windrider's
Loop, Tactician's Band, Flamebinder's Promise, Heartbinding Band,
Luminous Signet, Focusing Band of [Technique], and Worry Token (swapped
in from Neck). Two items flagged as
possibly mis-tagged before pricing, both confirmed correctly on Ring:
Elemental Warding Amulet (renamed **Elemental Warding Band**) was
always `Slot: Ring` in the source doc, just oddly named; Mendicant's
Cord's original `Slot: Waist` doesn't exist anymore, and Ring's "a
specific active ability" lane fits its Defense-shifting effect better
than Belt's narrow "carrying items" one.

- **Worry Token** (`I211`, L2/4, non-contiguous, moved here from Neck —
  swapped with Fate's Grasp, see above) — its own derivation is
  unchanged by the swap. Reworked from a broken GM-secret random table
  to a suit-keyed Sift (each suit's effect built from that suit's own
  `RULES_DESIGN.md` archetype): `Value = 4.255/charge`, 3 charges at L2
  / 6 at L4, **Net +0.77 / +1.53** — both ~106% funded. Moved to Ring
  since its deliberate charge-spend ("use it now or save it") is Ring's
  "active ability" lane, not Neck's "passive utility" one.

- **Heartbinding Band** (`I084`, L3, up from L2) — spend 1 AP + any
  amount of own Health, an adjacent willing creature heals that much
  Shallow Health (type specified to close a Shallow-pay/Deep-receive
  rate arbitrage the original open wording allowed). In combat, one
  activation is a guaranteed raw loss regardless of magnitude — Heal
  and Health-spend cost cancel exactly, leaving only the flat 1 AP cost
  as debit — kept deliberately as combat-use friction, not a flaw. Real
  value comes from recycling otherwise-wasted overheal out of combat: a
  capped-out full-Health donor's daily Recovery Cycle heal (`= Body`,
  baseline 3) normally goes to waste, and this ring redirects it to
  whoever actually needs it. `Value = 3 × 4 (Healing Shallow) = 12`, an
  exact fit against Level 2's Target — bumped to **Level 3** anyway per
  the designer as deliberate headroom against a clever party exceeding
  the single-donor baseline: `Target = 18`, **Net −6** (67% funded).
- **Flamefist's Approach** (`I086`) — cut. Two powers (a Brawl hit
  grants a free ≤2 AP Sorcery Spell cast; a Sorcery hit within
  `[Meditation Skill Total]` meters grants a free Teleport-to-adjacent)
  were broken into components before pricing finished, but per the
  designer the whole Brawl-enables-Spell/Spell-enables-Brawl-closing
  interplay reads as a better fit for a `[Form]` Technique (a toggled
  combat stance) than a passive Ring. Moved to `IDEAS_BACKLOG.md`
  rather than priced, same call as Bloodshard Ring earlier in this
  slot.
- **Luminous Signet** (`I087`, L4) — same unconditional discard/play
  trigger as Fate's Grasp, but not the same math: timing matters here
  (Hasted decays over ~4 turns, so a stack granted outside combat is
  wasted, unlike Sift's timing-independent bias) and Hasted's rate is
  convex (rising toward ~2.2/stack), so trigger *size* matters, not
  just aggregate volume. Per the designer: 2 allies affected, 4 cards
  in a representative encounter — checked against an initially-floated
  3-4 range, where the convex curve made the difference stark (3 cards:
  55% funded; 4 cards: 92% funded). `Value = Hasted(4)=5.5 × 2 allies =
  11.0`, `Target = 12`, **Net −1.0**. Confirmed at Level 4 rather than
  dropped to fit the 3-card case, deliberately keeping the higher
  `Target` buffer against a clever party pushing trigger sizes past the
  baseline, since the trigger itself is uncapped.
- **Flamebinder's Promise** (`I078`, L1) — a standalone, once/encounter
  fresh attack, priced via the "Pricing a fresh attack from scratch"
  model (Resist placeholder + universal Harried + Autoswing). Its
  damage scales off Mind, which has no established baseline anywhere in
  this document — resolved per the designer by treating the ring as a
  portable Level 1 equivalent of **War Magic** (`T120`), reusing that
  Technique's own reference-table Mind value (3) rather than inventing
  a fresh one: `Value = 1.5`, **Net −1.5**, a modest accepted shortfall.
  Range bumped 5m→6m for flavor — checked against the range breakpoints
  table and confirmed inconsequential (both sit inside the "Short"
  tier, no line crossed).
- **Elemental Warding Band** (`I208`, L1/2) — Ward's already-Locked rate
  reused directly, plus a +15% targeting-flexibility bump for "or a
  willing creature you touch": `Value = 3.13` (L1 Fire) / `6.07` (L2
  Fire), **Net +0.13 / +0.07** (Fire; modestly negative for the other
  three elements). Extending to Level 3-5 was considered and rejected —
  Ward's flat-Resist component caps at 5 stacks while Target keeps
  climbing, a structural mismatch no flat bonus fixes.
- **Mendicant's Cord** (`I209`, L2) — mechanic reworked entirely, from a
  flat 2-point Defense-shift to a Good-Luck/Bad-Luck toggle between
  Harried's and Vulnerable's own Defense groupings. `Value` ranges
  `1.375–4.125` depending on how lopsided the encounter reads — the
  ceiling **cannot reach Target (6) under any circumstance**, a hard
  structural cap, not a judgment call. Accepted anyway per the designer
  — many real encounters are consistently lopsided enough to realize
  well above the pessimistic floor.
- **Ring of Charming, Assertive, or Bold Statements** (`I157`) — cut,
  duplicates the Head hats with no differentiation beyond the slot.
- **Galeforce Loop** (`I083`, L1) — confirmed plain Narrative Utility,
  `Value = 1`, **Net −2**.
- **Poison Needle** (`I085`, L1, down from L3) — same AP-savings shape
  as Quick Draw Belt (saves Poison's 2 AP application cost): `Value =
  5.5`, **Net +2.5**. Prompted the Poison duration rule change ("1
  hour" → "until it exposes a creature or a full night's rest") so a
  loaded dose can't expire unused before it matters.
- **Ring of Pure Elements** (`I158`, L1, down from L3) — same "1 point
  of average soak bypassed" logic as Worry Token's Diamonds branch:
  `Value = 2.0`, **Net −1.0**.
- **Windrider's Loop** (`I187`, L2) — a new Range rate derived
  (`0.55/meter`, reusing Speed's single-instance rate directly, since
  extra Range substitutes for the Move action it would otherwise cost
  to close the gap), bumped from 5m to 10m: `Value = 5.5`, **Net −0.5**.
- **Bloodshard Ring** (`I081`) — cut. The Health-for-damage trade
  worked out to a near-wash once AoE was correctly modeled as applying
  the bonus per target hit (`Net = 2X(N−2)`), but the text has no
  stated usage cap, so it moved to `IDEAS_BACKLOG.md` as a Technique
  idea instead, where a cap can be designed in from the start.
- **Tactician's Band** (`I080`, L2/4, non-contiguous) — the Hand
  Filtering rate (1.66/card) applied directly to a fixed daily charge
  pool; pinned to 7 charges (L2) / 14 charges (L4) after the original
  `5×Level` formula ran a consistent 138%-funded overshoot at every
  Level: **Net −0.38 / −0.76** — ~97% funded at both.
- **Focusing Band of [Technique]** (`I079`, L1-5) — closes out the
  slot. Unlike every other item this pass, its value depends on *which*
  Technique gets bound to it, chosen by the crafter at creation — priced
  via a newly-codified convention (`balance_weights.csv`): a Technique
  is worth `Level × 3` (Encounter cadence) or `Level × 6` (daily
  cadence), the same relationship the once/day item-Target convention
  already uses. Since the ring only activates once/day and persists,
  both cadences land on the identical `Level × 6` total either way —
  collapsing the whole derivation to just the card-discard activation
  cost: `Value = 6L − 2.7`, `Target = 6L`, **flat Net = −2.7 at every
  Level**, exactly the deliberate activation-cost friction the designer
  intended ("the thing that makes it not just a way to buy abilities").
  Rules gap fixed along the way: a Technique with its own choices
  (Feature picks, Free Text) is now explicitly bound to a specific copy
  the creator already knows, locked in at creation, not left open for
  the wearer.

**Ring slot closed out.** Final twelve: Elemental Warding Band,
Mendicant's Cord, Galeforce Loop, Poison Needle, Ring of Pure Elements,
Windrider's Loop, Tactician's Band, Flamebinder's Promise, Heartbinding
Band, Luminous Signet, Focusing Band of [Technique], and Worry Token.

### Held Masterwork pass — final lineup

30 items, the largest single slot by far (more than double the
next-biggest). Working through it lowest-Level to highest.

- **Attacks/turn split into two baselines**, surfaced while pricing
  Claw of Mortality's permanent elemental conversion. The existing
  `1.5 attacks/turn` figure (used throughout this project — Crippled's
  rate, Fitted Armor's tank assumption, Sift's daily cadence) implies
  half of all turns are a double swing; per the designer that's too
  generous for a normal player's own rate, closer to one-or-two turns
  in five. New **`1.25/turn`** baseline added specifically for pricing
  an always-on effect that rides the wielder's own attacks (Range-
  permanent, elemental-conversion-permanent) — the older `1.5/turn`
  stays exactly as-is for aggressive/tank-style scenarios, not
  reopened. See Reaching Weapon below for the resulting recheck.
- **Assassin's Undetectable Arms** (`I088`) — cut, then merged into
  Shadowdraw below rather than left in the backlog. See Shadowdraw.
- **Battering Armament** (`I090`, L1) — Push, decoupled from Speed and
  re-derived this same item: `1 AP / 4-space standard move = 0.6875/
  meter` base, `+30%` tactical premium for forcing an enemy out of
  position, `= 0.89375/meter` (Speed's own rates untouched). Locked in
  at **3m** (exact fit needed 3.357m, not a clean number): `Value =
  2.68`, **Net −0.32** (89% funded). Flagged, not decided: whether this
  should scale Level 1-5 — revisit once the whole Held block is
  assessed after this pass, since a naive linear-meters-per-Level
  scaling gets to unrealistic distances (15m at L5) fast.
- **Legbreaker** (`I213`, Grenade, L2) — rechecked under the new Push
  rate rather than left stale: the old 4m Push would have become 118%
  funded at the new rate, so trimmed to **3m**, restoring a clean fit
  (`Value = 6.18`, **Net +0.18**, 103% funded).
- **Bounty Hunter's Blade** (`I089`, L1) — no Bad Luck on non-lethal
  attacks made with it. Per the designer, meant to read like a same-
  Level Form Technique feeding narrative requirements, not combat
  optimization — priced via the Narrative Utility convention rather
  than a real frequency guess: `Value = 1`, **Net −2**. Confirmed
  as-is.
- **Shadowdraw** (`I091`, L1, renamed from Eager Armament) — merges
  Eager Armament's 0-AP draw with Assassin's Undetectable Arms'
  concealment Good Luck/Bad Luck into one infiltrator-flavored weapon.
  The 0-AP draw isn't a guaranteed once/encounter saving the way Quick
  Draw Belt's is — most characters already carry a weapon drawn — so
  it's scoped to the same ⅓ niche tier as the concealment checks
  (`5.5 × ⅓ = 1.833`), plus the concealment component (`1.53`): `Value
  = 3.36`, **Net +0.36** (112% funded), a clean fit at the original
  Level 1 / 20 Gold.
- **Fatestealer** (`I092`, L1-5) — Downing a creature with this weapon
  instantly kills it (unpriced, GM-dependent) and grants charges spent
  on Sift 2 (better rate, 1.2/charge) or drawing a card (worse rate,
  0.9/charge, left as a deliberate inefficiency). Replaced the flat
  `[Level]`-charges formula with a hand-tuned curve (**1/3/5/6/8**
  charges/Down by Level) to tighten the fit at every Level instead of
  sharing one shortfall shape: Net lands at 60% (L1, confirmed
  acceptable as underpowered), 90% (L2), 100% (L3), 90% (L4), 96% (L5).
  Charge cap raised 5 → 8 to fit the new Level 5 grant.
- **Quartermaster's Blade** (`I186`, L1) — swap the weapon's shape to
  any other weapon as a Move. Genuinely situational/build-dependent
  (mostly useful within one Skill family), no clean anchor — priced via
  the Narrative Utility convention: `Value = 1`, **Net −2**. Confirmed
  as-is; ammo wording flipped to match Armory Gauntlets' precedent
  (conjures its own ammo rather than being denied it).
- **Reaching Weapon** (`I093`, L1-5) — always-on Range increase equal
  to Level. New **Range (permanent) = 3.4375/meter** rate derived —
  scoped by attacks/encounter, not Speed's own moves/encounter
  rescoping, since the bonus applies to every attack rather than just
  movement spent closing distance. [Corrected from an initial
  4.125/meter — see the attacks/turn baseline split below.] Lands at a
  constant **114.6% funded** at every Level (`Value = Level×3.4375` vs.
  `Target = Level×3`); per the designer, confirmed "a little powerful"
  but left as-is — no clean way to trim it without breaking the
  `Range = Level` symmetry, and the overshoot is smaller than Poison
  Needle's already-accepted 183%.
  Wording also cleaned up to match the `[Range]` glossary keyword
  (dropped a now-redundant manually-spelled-out clause); same fix
  applied to Spiritlink Scepter (`I184`, not yet priced this pass).
- **Returning Knives** (`I183`, L1) and **Weapon of Sending** (`I097`,
  L2) — both cut. Per the designer, thrown weapons are meant to be
  treated as an abstracted "you have enough to fight with" collection
  recovered after the encounter, not tracked mid-combat — so
  Returning Knives' "return to hand" premise doesn't solve a real
  problem. Weapon of Sending shares that same clause plus a "throw a
  melee weapon" component now covered by Reaching Weapon (or better
  suited to a future Technique) — cut alongside it.
- **Staying Gauntlets** (`I180`, L1) — cut, superseded by Bounty
  Hunter's Blade (both bypass the Non-Lethal Attacks Bad Luck penalty,
  just triggered differently — one on a declared non-lethal attack,
  this one automatically on any Down).
- **Venomous Weapon** (`I094`, L1-5) — "creates" one Basic Poison dose
  per encounter, auto-exposed for 0 AP. Per the designer, all seven
  Poison flavors are treated as interchangeably "worth" the same
  (they cost the same to craft) rather than pricing off whichever's
  mathematically strongest — Crippling Poison's own already-"naturally
  balanced" formula (`Value = 3×Level`) stands in as the flat baseline.
  **Net = 0 at every Level**, an exact fit.
- **Elemental Bloodletter** (`I181`, L2) — cut. Priced both components
  fully: permanent elemental damage conversion is a real `+15` on its
  own, but the damage→Bleeding clause is a structural `−92` once
  checked against Bleeding's own capped curve versus plain guaranteed
  Health loss — an early elemental-weapon pass that predates the
  Bleeding-taper work and doesn't hold up under it. Binned in favor of
  the Held slot's other elemental-conversion items.
- **Grim Promise** (`I095`, L2) — ignores Wounded/Crippled penalties
  when attacking or parrying. Reused Insanity Potion's own already-
  priced Wounded/Crippled-immunity components directly (`21.8` raw
  stacked), but discounted from Insanity Potion's guaranteed 100%-
  uptime assumption down to the established ⅓ niche tier, since being
  Wounded/Crippled is uncommon for the wielder specifically even though
  the debuffs are common from enemies generally: `Value ≈ 7.27`, **Net
  ≈ +1.27** (121% funded).
- **Sorcerer's Bow** (`I096`) and **Sorcerer's Gloves** (`I178`, cut) —
  both covered a caster's Sorcery/Mind driving a weapon-style attack;
  per the designer, the Bow absorbs the Gloves' role. Priced as build-
  flexibility (Narrative Utility floor `2`) plus a flat `+1.0` premium
  for now covering the Gloves' "no separate weapon needed" niche too,
  `Value = 3.0`. Moved Level 2 → 1, since committing to this weapon
  also forfeits any Archery-gated Techniques — a real cost with no
  clean way to price directly, better reflected by a lower Level than
  an inflated Value. **Net = 0** at Level 1, exact fit.
- **Apprentice's Dueling Catalyst** (`I179`, L1, missed in the original
  stocktake) — cut, obsolete. A holdover from before most weapons
  carried the `[Implement]` tag; now that Bounty Hunter's Blade is
  itself an Implement, its non-lethal Bad Luck removal already covers
  spell attacks channeled through it, per the `[Implement]` rule — no
  separate item needed.
- **Claw of Mortality / Rimefang / Radiant Verdict / Conflagration
  Brand** (`I098`/`I099`/`I227`/`I100`, all L3) — priced as a family:
  weapon-attack damage conversion is the valuable half (Elemental-
  Forged Weaponry's job), so these four lean on debuffs instead, with
  only a small spell-conversion bonus on top (spells default to Fire,
  not Physical, so converting them is a much smaller benefit — derived
  a separate **Fire-baseline** conversion rate, `0.4/attack`, alongside
  a **Fire discount** on the full weapon-conversion rate, both new to
  `balance_weights.csv`). New **continuously-refreshed debuff**
  pricing technique (queueing approximation for always-active debuffs
  like Slowed/Vulnerable; total-stacks-applied for discrete-payout ones
  like Bleeding/Necrotic). Results: Claw of Mortality (Necrotic) 94%
  funded, Rimefang (Slowed, renamed from Claw of Rime) 130%, Radiant
  Verdict (new item, Brilliant/Vulnerable) 121%, Conflagration Brand
  (Bleeding, Fire spell-clause is a deliberate no-op) 139% — a
  consistent family shape rather than four independent misses,
  accepted as-is.
- **Fanged Guard** (`I102`, moved L3 → L2) — Bleeding on a successful
  Parry. First item this pass triggered off Parrying, needing a
  defensive-frequency baseline: `3.75 attempts/encounter × ⅔ (melee) ×
  60% (successful Parry, for a Parry-focused build) = 1.5 successful
  Parries/encounter`, `Value = 6.0`. Original Level 3 was a real
  shortfall (67% funded); Level 2 lands as an exact fit, `Net = 0`.
- **Spiritlink Scepter** (`I184`, L3) — cut, obsolete. Reaching Weapon
  already grants the identical 3-meter Range bonus at Level 3 to ALL
  attacks and abilities, not just Theurgy spells — a strict superset.
- **Valiant Arms** (`I160`, moved L3 → L2) — Good Luck on an attack
  after a 6-meter straight-line charge. A charge-attack mechanic (no
  formal "charge" rule exists elsewhere) — wording tightened
  ("relatively straight line" → "in a straight line," added
  "immediately before the attack"). Priced at `2.5 uses/encounter ×
  2.4 (Good Luck) = 6.0`; original Level 3 was a 67%-funded shortfall,
  Level 2 lands as an exact fit, `Net = 0` — same shape as Fanged Guard.
- **Elemental-Forged Weaponry** (`I101`, L3 or 4) — confirmed as-is,
  no changes. Already priced during the Claw family pass, since this
  item's own existing Level split was the calibration anchor for the
  Fire-discounted weapon-conversion rate. Both options a clean 104%
  funded (Fire at L3, Frost/Brilliant/Shadow at L4).
- **Sanguine Iron Weapon** (`I182`, L4) — Bleeding on any Health-loss-
  causing hit, same discrete-payout mechanic as Conflagration Brand
  without the elemental half. Reused the total-stacks-applied model
  directly: `Value = 12.5`, **Net +0.5** (104% funded). Confirmed
  as-is.
- **Scepter of Evocation** (`I185`, L4) — cut, an earlier draft of the
  same idea that became Thrumming Focus (spend extra AP for Good Luck),
  narrower and pricier for the identical benefit.
- **Thrumming Focus** (`I103`, moved L4 → L2) — spend an extra 1 AP for
  Good Luck. First item this pass to charge the player's own AP per
  use: raw "Good Luck for 1 AP" is a flat loss (`2.4 − 2.75 = −0.35`),
  only usable when the AP would've gone to waste anyway (~11% funded).
  Bumped to **"Good Luck twice"** instead — derived a fresh Good Luck
  stacking curve (exact 52-card combinatorics + scaled Suit Pool
  credit; new `balance_weights.csv` rate) — which flips the trade
  profitable (`3.6 − 2.75 = +0.85`), usable on essentially every
  attack. Checked whether a second activation on the same attack is
  worth it (diminishing returns: `+1.26` marginal against another full
  AP) — it isn't, so rational play self-caps at one per attack with no
  explicit rule needed. `Value = 5.31` at Level 2, **Net −0.69** (89%
  funded).
- **Apocalyptic Staff** (`I104`, L5) — once/encounter, cast War Magic
  (max Level 4) as though known, Features chosen fresh. Wording fixed
  from a broken reference ("Elementalist's Artillery," War Magic's old
  name). Reused the Technique-value convention: `Value = 3×4 = 12`
  against the item's own Level-5 Target (15) — a real, structural
  `Net −3` (80% funded), accepted per the designer for the flexibility
  of a fresh Feature loadout every encounter.
- **Heartseeker** (`I159`, L5) — full redesign. Original "treat any
  card as a Heart" did nothing (no weapon-attack Skill is governed by
  Hearts); per the designer, it used to guarantee max damage back when
  suits added variable damage directly, before the current Extra-
  Success system replaced that. Considered and rejected retuning
  *every* flipped card (Good Luck's both cards feed the Suit Pool,
  which would spiral); redesigned to retune only the *kept* card,
  adding the matching suit alongside its natural one. Priced as a
  guaranteed Extra Success (`+1 Damage`): `Value = 2.0/attack × 6.25 =
  12.5`, **Net −2.5** (83% funded).
- **Placeholder's Speedy Scepter** (`I161`, L5) — 1 AP cheaper
  abilities. Uncapped, this was a real exploit (freeing AP lets a
  turn fund *more* actions, not just cheaper ones — an unbounded
  version could reach ~55 raw). Capped to once/turn, which
  conveniently reproduces the original pricing: `Value = 17.19`, **Net
  +2.19** (114.6% funded, same ratio as Reaching Weapon). Also given a
  special crafting restriction per the designer — base item name must
  start with "S," which among this slot's options means Shield only,
  fitting the "Placeholder's" whimsical-joke-item pattern.
- **Blade of Fortune** (`I210`, L5, renamed from Scaraculpi's Gleaming
  Justice — read as accidentally Italian) — unconditional, permanent
  Good Luck on attacks made with this weapon, no AP cost. Priced the
  same as every other permanent always-on weapon effect this pass:
  `Good Luck (2.4) × 6.25 (own-incidental attacks/encounter) = 15`,
  **Net = 0** at Level 5, an exact fit. Resolves the RULES_DESIGN.md
  flag against Thrumming Focus (`I103`) — that flag predates Thrumming
  Focus's own move down to Level 2 earlier in this pass, so the two now
  read as a sensible cheap-AP-gated vs. pricier-unconditional-permanent
  progression rather than a mismatch.

**Held Masterwork slot pass complete** — all 30 items (`I089`-`I104`,
`I159`-`I161`, `I179`-`I185`, `I227`) across Levels 1-5 confirmed,
reworked, repriced, or cut.

### Baseline Weapons pass — final lineup

The first pass through the 13 core Base Game weapons plus the 3
Goblin Game firearms (`I117`-`I126`, `I130`-`I132`) — the actual base
items every Masterwork enhancement gets built onto, none of which
carry a `Level`/`Target` the way every other item priced so far does.
Full derivation in `balance_weights_notes.md`; headline results:

- **New pricing model for un-Leveled base items**: compare raw
  `Accuracy(1/pt) + Damage(2/pt) + Weapon Defense(1/pt)` directly
  (valid since every weapon shares the same attack cadence), against
  a Target of `baseline(8) + 2 (Archery) − 2 (Acrobatics) + 2
  (two-handed)`. Both Melee weapon pairs (`I117`-`I120`) already fit
  this exactly with zero changes, and the two-handed `+2` is directly
  confirmed by existing data (`Light 2H`'s raw of 10 already equals
  `Light 1H`'s 8, plus the slot cost).
- **New Range-value curve** for a weapon's own inherent engagement
  distance (distinct from every other Range rate, which price a
  *bonus* on top of an existing range): flat 0 below 6m, ramping to
  1.375 by 9m, climbing steeply (`0.515625/m`) from 9-12m, then
  tapering to a quarter of that rate beyond 12m — "past that distance
  it's already the whole battlefield," per the designer.
- **New reload penalty** (`0.8×` on Accuracy/Damage only) for the
  three fire-every-shot firearms — reload doesn't just cost AP, it
  makes double-attacking within a turn mathematically impossible,
  flattening their attack cadence to `5.0/encounter` vs. the `6.25`
  baseline.
- **Light Thrown** (`I121`) Damage `3→2`, **Heavy Thrown** (`I122`)
  Damage `4→3` — kept deliberately generous against their own
  (Acrobatics-discounted) Target, per the designer: Thrown is meant
  to stay a viable flexible/backup pick for non-combat-focused
  archetypes without needing to fully compete with a dedicated
  build's own weapon.
- **Light Bow** (`I123`) Range `15→19`, **Heavy Bow** (`I124`) Range
  `20→17` — swapped into a "precise sniper, longer reach" (Light) vs.
  "hard-hitting, shorter reach" (Heavy) identity, the inverse of the
  naive intuition, since the model's own math wanted Light's lower
  raw stats to need *more* Range credit to hit the same Target.
  Accuracy/Damage deliberately left untouched on both, per the
  designer — only Range was in scope for this fix.
- **Unarmed, Shield, Handgun, Blunderbuss, Musket**: all confirmed
  as-is, no changes needed.

### Baseline Armor pass — three tiers, a genuinely different balance shape than Weapons

Reworked from 2 tiers (Light/Heavy) to 3 (Light/Medium/Heavy), adding
a new `I127` Medium Armor. Full reasoning in `balance_weights_notes.md`
and the two new `RULES_DESIGN.md` notes ("Baseline damage-over-Resist
assumption," "Unarmored as an opt-in archetype choice"); headline
points:

- **Armor's core stat doesn't balance the way Weapons' did.** A
  Weapon's Accuracy/Damage/WD has build-independent value (everyone
  attacks at roughly the same rate), which is what let Light/Heavy
  Weapon pairs balance against a single universal yardstick. Physical
  Resist's *realized* value scales with how many hits the wearer
  actually absorbs — a property of the wearer's build, not the armor
  — so a flat "raw value" comparison under one assumed scenario always
  makes heavier armor look mediocre for an average character while
  understating its value for the dedicated-tank archetype it's
  actually for. Resolved by checking the tiers under two lenses
  (generic party member vs. the already-established `Tank/above-
  average attack draw ×1.5` multiplier) instead of one.
- **Reframed the design goal**: not "no armor tier should be better
  than another" (a single-axis target that doesn't fit this stat), but
  "no tier should be better than another *for the same build*" — a
  squishy character in Heavy Armor should feel like a mistake, a
  dedicated tank in Light Armor should feel like a missed opportunity,
  both true at once rather than one tier dominating.
- **Light Armor stays the untouched baseline** (Resist 1, no
  penalty, Might 3, 4 Gold) — confirmed as the anchor the "average
  attack nets ~2-3 over Resist" assumption is built around.
- **New Medium Armor** (`I127`, Resist 2, Dodge −1 only, Might 4, 6
  Gold) — deliberately took the single-penalty-dimension shape (Dodge,
  not Speed) per the designer: this reads as the pick for a build
  that's already not leaning on Dodge (a Parry-focused or high-output
  "kill them before they hurt you" archetype), where Heavy's *added*
  Speed penalty is what actually gates going further, not raw
  Might/Gold.
- **Heavy Armor's Resist raised 2 → 3** (Speed −1, Dodge −1 both,
  Might 6, 8 Gold unchanged) — fixes the problem that prompted
  revisiting this: the old 2-tier Heavy paid double Light's Gold for
  only ~29% more raw value, a bad deal under *any* build. At Resist 3
  it reads clearly ahead of Medium once a build can actually capitalize
  on the extra Resist (the tank lens), while still a real, feelable
  step down for anyone who can't.
- Gold kept to a simple, cheap linear scale (4/6/8) — deliberately
  *not* used as a meaningful balancing lever, since all Armor is meant
  to stay inexpensive; the real tradeoff lives entirely in the stat
  penalties.
- `crafting_recipes.csv` gained two new Medium Armor recipes
  (Tailoring/Smithing, Craft 4) and all 9 Torso-slot Masterwork items'
  `Base Item Options` now include `I127`. `armor_categories.csv`
  (reference table, not consumed by the live site) updated to match.

**Follow-up**: Might Requirements tightened (Medium `4→5`, Heavy
`6→7`, Light unchanged at 3) — Heavy's 7 sits exactly 1 point past the
character-creation ceiling for a fully-dumped Might Skill Total (Body
3 + Might 3 = 6), so it's unreachable at creation and opens up after a
single Experience rank-up, per the designer's explicit intent. Also
added variable-material Armor upgrade recipes — a lower tier can now
be reinforced into a higher one for just the Total Materials
difference (Light→Medium 2, Medium→Heavy 2, Light→Heavy 4) rather than
only building each tier from scratch. Found and fixed two real bugs
while wiring this up: a CSV-quoting corruption from an unquoted comma
in a recipe name (shifted every later field by one column), and a
genuine precedence bug in `index.html`'s crafting-recipe merge logic
that would have made the new upgrade recipes silently ignore their own
reduced material counts. Full writeup in `balance_weights_notes.md`.

## Open balance work

**Correction (2026-09-13): the Masterwork list is fully closed, not
"~73 items still remaining" as an earlier version of this bullet
claimed.** That claim was written right after the Held slot closed and
assumed every other slot was still open — it wasn't checked against
what had actually already landed. All 9 Masterwork slots (Head, Neck,
Torso, Hands, Ring, Held, Belt, Feet, Other — 91 items total currently
in `items.csv`) have "final lineup" sections above with real Value/
Target/Net math, and every surviving Masterwork item ID has a row in
`balance_ledger.csv` (verified directly, not assumed). Nothing at the
per-item Masterwork level is outstanding.

What genuinely remains, cross-cutting rather than slot-shaped:

- **Is Vital Defense supposed to run lower than Dodge/Parry?** Per the
  designer, Techniques attacking Vital (Ripjaw Gambit, Wasting Claw,
  Plague Fist's Vulnerable setup) are priced on the assumption that an
  enemy's Vital is usually 1-2 below its Dodge/Parry. The roster
  doesn't match right now: the Level 3-5 archetypes have Vital 16-17
  against Dodge/Parry 13-16, since each archetype picks one Defense to
  be Primary and those picked Vital. Worth a look at
  `ENEMY_ENCOUNTER_DESIGN.md`'s Defense tiering and the roster before
  more Vital-targeting Techniques land.

- **Gambling is weapon-attacks-only for damaging attacks: look deeper
  later, with the simulator.** Added to `rulebook.md`'s Gambling
  section on 2026-09-24. The intent is to give weapon users an edge
  over spellcasters on raw damage, but the designer may revise it.
  Worth checking how big that edge actually is. **The combat
  simulator doesn't follow the rule yet**: `combat_sim.py`'s Gambling
  logic runs on every PC attack, War Magic included (Beornhard), so
  casters there have been getting Gambles they shouldn't. Fixing that
  shifts results the Level 1 roster was tuned against, so it wants a
  deliberate pass rather than a quiet patch. Also open: whether
  Discipline attacks like Spirit Bolt count (they aren't tagged
  [Spell]).

- ~~Crafting Schools' XP cost vs. payoff, broadly~~ — **reviewed
  2026-09-15, resolved: no rebalance needed.** Flagged while grouping
  everyday-goods recipes on the assumption that a School's payoff was
  "craft this item instead of buying it retail" — under that framing,
  a 6+ XP School investment (Artisanal Training, 3 XP, + Craft/
  Mixology 2, 3 XP) looked like a bad deal for Tier 1-2 goods worth
  only 1-6 Gold outright.

  That framing was wrong. Per the designer, a School's real payoff is
  **crafting instead of vendoring loot**, not crafting instead of
  buying — `rulebook.md` already states this (materials are worth
  Gold equal to their Level, but "sell for much less except to
  specific tradespeople, and even they are unlikely to pay full
  value"), just without a concrete number. The designer's number: a
  vendor pays roughly **50-75% of a material's Level-equivalent Gold
  value**; crafting instead converts the same material into an item
  worth its **full** value. So the comparison is: find materials as
  loot → sell them at a discount, or craft with them and keep the
  full value.

  Checked this against both ends of the pricing range rather than just
  asserting it holds:
  - **Camping Kit** (3 Gold, 3 materials at Level 1 = 3 Gold raw
    value): vendor sale nets 1.5-2.25 Gold (50-75%); crafting nets the
    full 3 Gold. **Recovers 0.75-1.5 Gold — 25-50% of the material's
    own value.**
  - **A Level 1 Masterwork** (20 materials at Level 1 — confirmed
    exactly `20 × Level` Gold across all 91 Masterwork items in
    `items.csv`, holding precisely at 20/40/60/80/100 through Level
    5): vendor sale nets 10-15 Gold; crafting nets the full 20 Gold.
    **Recovers 5-10 Gold — the same 25-50%.**

  The percentage recovered is identical at every tier — cheap items
  and Masterwork items are proportionally the same deal, just
  different absolute Gold amounts. There's no tier where a School's
  crafting access is a worse deal than another; the real determinant
  of whether a School's fixed XP cost pays off is **how much
  loot-material volume a character actually converts over a
  campaign**, which depends on how the GM paces material loot, not on
  which items that School happens to unlock. That's a GM-pacing
  variable outside the system's control, the same way a situational
  Technique's value depends on how often its trigger condition comes
  up in play — not a design gap to close.

  Kept on the table as an optional idea, not a fix (nothing here is
  broken): a School granting some standing perk beyond crafting access
  itself, so the XP has value from the moment it's spent rather than
  only once a character starts converting loot. Not pursued this pass.

  See `design/GM_GUIDE_NOTES.md` (new) for the loot-planning notes this
  review produced, for an eventual GM-facing guide — `rulebook.md`
  stays player-facing only per its existing scoping note, so this kind
  of "how should a GM actually pace this" guidance doesn't belong
  there.
- **Crafting Skill Total tiers, broadly — reviewed 2026-09-16, fully
  applied.** Follow-up to the Crafting Schools review above, once the
  designer noticed a real gap: Alchemy's Level-scaling formula
  (`Mixology [twice the item's Level]`) put Level 1 at Mixology 2 —
  the *exact same* number as Artisanal Training's own Alchemy prereq
  (also Mixology 2, checked as raw skill ranks per the rulebook's
  Technique-prereq carve-out). So the moment a character paid the real
  cost to unlock Alchemy, their Skill Total already cleared every
  Level 1 recipe in the School with zero further investment. Cooking's
  Food recipe had the identical collision against its own prereq.

  First attempt (`[1 + twice the Level]`, preserving the old slope but
  adding a flat floor) turned out to be unworkable: Skill Total caps
  at 10 (Stat 5 + Skill 5), and the old formula's slope of 2 already
  hit exactly 10 at Level 5 — any positive offset pushes Level 5 past
  the cap into a threshold nothing could ever reach.

  **Landed on unifying Masterwork with a genuine "core progression"
  subset of the Alchemy/Cooking family onto one shared curve — Skill
  Total 4 / 6 / 8 / 9 / 10 across Levels 1-5** (steps of +2, +2, +1,
  +1 — not a single clean line; `min(2 × Level + 2, Level + 5)` as a
  closed form). Replaces Masterwork's old `Craft 5 + Level`
  (6/7/8/9/10) and Alchemy's old `Mixology [twice the Level]`
  (2/4/6/8/10); Level 3 is exactly 8 under both old formulas, so this
  curve was chosen to pass through that shared point — Masterwork's
  already-tuned Levels 3-5 don't move at all, only the low end (1-2)
  comes down. `index.html`'s `parseSkillTotalText` gained a fourth
  pattern for the literal text `"[4/6/8/9/10 by Level]"` (a by-Level
  lookup, not an arithmetic expression like the other two patterns,
  since no single line can hit both endpoints without exceeding the
  cap) — verified in the Playwright sandbox across Levels 1/2/3/5 for
  both Potions and Masterwork items built on different base items.

  **New Archetype-based split, once the designer flagged that not
  every Alchemy-ish good should really be on this curve:**
  - **Progression** (untagged in `Archetype`, the default) — the
    30 Potions/Poisons/Grenades and 5 Food items players actually
    level through. These follow the curve above.
  - **Special** (flagged via `Crafting Notes`, not `Archetype` — this
    is a crafting-mechanics distinction, not the player-facing
    thematic grouping `Archetype` already holds for Potions) —
    **Spirit Quest Ointment** (`I116`) is the one confirmed case,
    found by checking every Potion/Poison/Grenade for a Cost override:
    it's the *only* one with a flat Cost (60 Gold) instead of the
    formula-derived default, real evidence it was never meant to
    follow the generic curve. Still falls through to the generic
    Alchemical Potion recipe for now (Skill Total 8) with a
    `Crafting Notes` flag that it needs its own bespoke recipe — a
    real gap, but a documented one, not a silent one.
  - **Convenience** (`Archetype = "Convenience"`, 14 items: Basic
    Conveniences, Charcoal, Oil, Alcohol ×5, Incense ×2, Embalming
    Fluid, Recreational Drugs ×2, Quicktorch) — reads as a common tool
    rather than a proper Alchemy consumable (Alcohol's own recipe text
    already called it "a simple reagent rather than a proper Potion").
    Pulled off the curve entirely and flattened to **Mixology 3** (or
    `Mixology or Survival 3` for the three with that alternate skill),
    matching Craft's Basic Tool tier exactly rather than sitting at
    the curve's Level 1 floor of 4 — same "everyday goods barely need
    training" tier, just reached via a different Skill. Flattening
    also means a fancier tier (Alcohol, Legendary at Level 5) doesn't
    need more Skill to make, only better/costlier materials — a nicer
    Gold cost doesn't imply a harder recipe for something this basic.
  - **Unarmed Enhancer** (`I001`) — tagged `Archetype = "Masterwork
    Base"` per the designer: mechanically a real weapon-tier item, but
    conceptually more like a piece of clothing (a placeholder base for
    Masterwork unarmed powers, not something with standalone combat
    value at its own tier) — deliberately left off the Weapon curve
    move below and kept at Craft 3, flagged rather than silently
    grouped with either bucket.

  **Also moved, once the tiers were reorganized around Skill Total 7 as
  the new "master craftsperson" ceiling** (see `RULES_DESIGN.md` for
  the anchor reasoning — the strict character-creation cap is Skill
  Total 6, and 7 is one deliberate step past it, not the exact cap):
  - **Weapons** (`CR001`/`CR002`) moved from Craft 3 to **Craft 4**,
    joining the Skill Kits as "properly equipped for adventuring"
    rather than "barely trained."
  - **Medium Armor** (`CR018`-`CR021`) moved from Craft 4 to
    **Craft 5**, filling out a tier that was previously thin (just
    Rucksack and Cart, Medium).
  - **Heavy Armor** (`CR006`/`CR022`/`CR023`) and **Wagon, Large**
    (`CR036`) moved to **Craft 7** (both had briefly landed at Craft 6
    in an earlier pass this same session, since revised) — the two
    "needs real engineering" items, now a genuinely populated tier of
    their own rather than colliding with Survivalist's Pack at 6.

  Full resulting table (everything Craft/Mixology-gated, current as of
  this pass):
  | Skill Total | Contents |
  |---|---|
  | 3 | Light Armor (×3 Schools), Unarmed Enhancer, Basic Clothing/Jewelry, Camping Kit, Knapsack, Adventurer's Belt, Cart (Small), Rope, Firestarter, all 12 Basic Tool items, + the whole Convenience bucket |
  | 4 | Weapons (×2 Schools), Musical Instrument, all 8 Skill Kits, Backpack, Crowbar, Manacles, Grappling Hook, + every Level 1 Progression item |
  | 5 | Medium Armor (×2 Schools + 2 upgrades), Rucksack, Cart (Medium) |
  | 6 | Survivalist's Pack, + every Level 2 Progression item |
  | 7 | Heavy Armor (+2 upgrades), Wagon (Large) |
  | 8 / 9 / 10 | Level 3 / 4 / 5 Progression items only |
- **Crafting Schools themselves, reviewed 2026-09-16 — structure holds
  up, applied one real gap-fill.** Follow-up to the XP-payoff review
  above: is there a better way to structure the six Schools
  (Smithing/Carving/Tailoring/Jewelrymaking/Alchemy/Cooking) given
  players spend real XP to unlock each one? First theory (Jewelrymaking
  is badly underweight — only 2 recipes vs. 11-17 for its Craft-School
  siblings) turned out wrong once checked against a dimension that
  matters just as much: which Schools gatekeep a Masterwork item's
  *base*. Counted every Masterwork item's `Base Item Options` against
  which School can craft that base (deduplicated — a naive per-base-
  item sum wildly overcounts, since a single "any weapon" Masterwork
  item lists 8-9 Held-slot weapon IDs at once):

  | School | Direct recipes | Distinct Masterwork items reachable via a base it can craft | Slots fed |
  |---|---|---|---|
  | Smithing | 21 | 31 | Held, Torso |
  | Carving | 12 | 31 | Held, Torso |
  | Tailoring | 13 | 42 | Belt, Feet, Hands, Head, Torso |
  | Jewelrymaking | 2 | 31 → **48** (see follow-up below) | Head, Neck, Ring → **+ Hands, Feet** |
  | Alchemy | ~55 (Potions/Poisons/Grenades/Convenience) | — (Alchemy items aren't Masterwork bases) | — |
  | Cooking | 5 (Food) | — | — |

  Jewelrymaking reaches the *same* 31 distinct Masterwork items as
  Smithing/Carving despite having almost no direct recipes of its own
  — it's the sole gatekeeper for Basic Jewelry, which 31 Ring/Neck/Head
  Masterwork items build onto, the same role Basic Clothing plays for
  Tailoring (42 items, and the widest slot spread of any School). The
  one real distinction left standing: Jewelrymaking has far less
  **hands-on crafting variety** than its siblings — every one of those
  31 Masterwork items starts from the identical Basic Jewelry recipe,
  where Smithing's 21 direct recipes are each a different crafting
  interaction. A real, softer imbalance, but not a numbers problem —
  not pursued further this pass, since it's about crafting-moment
  variety rather than XP value. Cooking's narrowness (Food only) is
  unaffected by any of this and stays intentional, per the earlier
  Crafting Schools XP-payoff review (its `Mixology or Survival` prereq
  is a deliberately cheap entry point for a Survival-focused character,
  not a gap to fill).

  **Follow-up, same session: Jewelrymaking's slot coverage genuinely
  expanded, not just re-measured.** The designer asked specifically
  whether Jewelrymaking should reach into some of Tailoring's
  accessory slots (Belt, Hands, Head — bracelets, circlets). Checked
  Head first: already works, all 10 Head-slot Masterwork items already
  list both Basic Clothing and Basic Jewelry as valid bases. Then
  checked **Basic Jewelry's own Fluff text**, which already states it
  covers "the Head, Neck, Ring, Hands, and Feet slots" — but zero of
  the 8 Hands-slot or 9 Feet-slot Masterwork items actually listed it
  as a Base Item Option, all Cloth-only. A real gap between documented
  scope and implemented data, not a stretch — added Basic Jewelry as a
  second `Base Item Options` entry to all 17 of those items (verified
  in the Playwright sandbox: the Base Item dropdown now correctly
  offers both choices on, e.g., Deft Gloves and Vaulting Boots).
  Jewelrymaking moves from 31 to **48** reachable Masterwork items and
  from 3 to **5** slots (Head, Neck, Ring, Hands, Feet) — matching
  Tailoring's slot count exactly, using only scope the game already
  claimed rather than inventing new territory. Belt stayed out:
  Basic Jewelry's Fluff doesn't mention it, so extending there would
  need a deliberate edit to that item's own definition first, not just
  a data-completeness fix like Hands/Feet were.

  **Applied: every crafting recipe now has a real School**, closing a
  gap surfaced during this review — five recipes (Musical Instrument,
  Climber's Kit, Disguise Kit, Tinker's Kit, Mixology Set) had a blank
  `School` field, meaning no School check applied to them at all
  (silently, not by documented design, unlike CR017 Masterwork
  Enhancement's *deliberate* blank School). Two were genuinely
  multi-material and split into two School-specific rows, matching the
  Weapon/Armor precedent, rather than picking one arbitrarily:
  - **Musical Instrument** → Carving (Wood/Bone) or Smithing (Metal),
    mirroring Weapon's exact material split.
  - **Disguise Kit** → Tailoring (Cloth, Craft 4) or Alchemy (Medicinal,
    Mixology 4) — already had a dual-Skill "(Craft or Mixology) 4"
    Skill Total; splitting School the same way makes the two paths
    fully parallel instead of one merged row with an ambiguous School.

  The other three read as single-School on inspection: **Climber's
  Kit** and **Tinker's Kit** → Smithing (forged metal hardware is the
  functional part in both — pitons/hooks, picks/springs). **Mixology
  Set** → Smithing too, not Alchemy — building the beakers/vials/stands
  is a metalworking task even though what the finished kit is *for* is
  alchemy, the same "you need a smith to forge the tool, even if the
  tool serves a different trade" logic Jeweler's Kit already follows
  for Jewelrymaking.
- **The Resist-granting-item systemic gap.** Physical Resist and a
  single element's Resist aren't remotely the same value (~5-10× apart
  after a damage-share correction narrowed the original ~7.5-15× gap;
  see `balance_weights_notes.md`), and every existing Resist item
  already checked against the derived weight comes back meaningfully
  negative (Attuned Shroud, Elemental-Resistant Armor, Robes of
  Resilience, Robes of the Elemental Lord — spread across multiple
  already-closed slots). Needs a deliberate decision on whether these
  items need real numeric buffs/Level cuts as a group, not just each
  one individually re-litigated — this is a systemic pattern, not
  isolated undertuning.
- **Correction (2026-09-15): most of the Alchemy-pass findings below are
  already resolved, not still open as this bullet used to claim.**
  Checked directly against `balance_ledger.csv` rather than trusting the
  prose: Revivification Draught was reworked into a deliberate Level-4
  trickle-heal (Net +2.5, an accepted overshoot); Healing Potion got the
  half-AP convention and reverted to its original 2-Health grant (Net
  −0.75, a clean fit); Quartz Tincture was renamed and redesigned into
  Reeler (Net −1.375, accepted below-budget in exchange for identity);
  Poisons had two stacked pricing errors fixed and a follow-up Potency
  pass closing the remaining shortfalls; Hellfire Bomb/Thunderclap-in-
  a-Jar landed within their Level thresholds once the AoE multiplier's
  own realization discount (×1.6, not a bare ×2) was applied. **The
  Food items are now resolved too** (2026-09-15, see the Food bullet
  below for the per-item breakdown) — Power Snack and Hearty Meal land
  a clean/deliberately-under fit, Soul Soup got an asymmetric fix, and
  Muscular Feast was formally accepted as-is. Nothing outstanding
  remains from this Alchemy-pass list.
- **Baseline (non-Masterwork) Weapon and Armor items are now both
  done** (see the Baseline Weapons/Armor passes above). The
  Resist-granting-item systemic gap immediately above is still open,
  though — the Armor pass's two-lens (generic party member/dedicated
  tank) approach may be worth applying to those Masterwork Resist
  items too once that gets picked back up, rather than re-checking
  them against a single flat rate the same way they were first flagged.
- The site-export batch also added 18 non-Masterwork items (`I190`-`I207`)
  that don't need value-model leveling but should get a normal
  price/rarity sanity check alongside the rest — the 4 that are
  Potions/a Grenade (`I204`-`I207`) got that check as part of the
  alchemy pass below; the other 14 (Pack/Gear, Tool/Kit) are flavor/
  utility goods with no combat mechanic to price and don't need one.
- **Material Type and Masterwork Slot × Level coverage — flagged
  2026-09-16, priority corrected same session, still not acted on.**
  Reviewed how evenly the 12 Material Types are spread across every
  recipe/item, and separately how Masterwork content spreads across
  Slot × Level — both in service of "where should new content go."
  First pass measured raw gaps everywhere (see `RULES_DESIGN.md`'s new
  "Where new Masterwork content should go" entry for the corrected
  standing principle this produced): **Level 4-5 completionism isn't
  the goal** — those are endgame tiers most tables never reach, loot is
  naturally abundant by then, and Weapons/Armor are already the
  expected capstone. **Not every Slot needs thematic range either** —
  Feet is deliberately movement-focused and that's fine as-is. The
  actual target is Level 1-3 variety specifically within the four
  Slots built for it: **Held, Torso, Ring, Neck.**

  Re-cut the data to match. Material Type presence within just those
  four Slots at Levels 1-3:
  | Slot | L1 items (materials present) | L2 | L3 |
  |---|---|---|---|
  | Held | 8 (Bone/Brilliant/Fire/Frost/Medicinal/Metal/Shadow/Wood) | 7 (no Fire/Frost) | 8 (no Bone/Metal, has Frost) |
  | Torso | 2 (Bone + all 4 elements via Elemental-Resistant Armor) | 5 (+Medicinal/Metal) | 4 (Bone/Metal + all 4 elements) |
  | Ring | 6 (Brilliant/Fire/Frost/Medicinal/Shadow/Wood) | 6 (Brilliant/Metal/Shadow) | **2 (Bone/Brilliant only — no Fire/Frost/Shadow at all)** |
  | Neck | 4 (Bone/Metal/Shadow/Wood) | 4 (Brilliant/Leather/Metal/Wood) | **2 (Frost + Metal only)** |

  **Ring L3 is the clearest concrete target**: only 2 items
  (Focusing Band of [Technique], Heartbinding Band), and neither
  touches any of the three "hot" elements (Fire/Frost/Shadow) — every
  other Level of Ring has at least one. **Neck L3** is thin on raw
  count (2 items) though it does already have a Frost item
  (Snowfall Drape) — a plain third Neck L3 item, any theme, would help
  regardless of material. **Torso L1** is thinner in count (2) than
  Torso L2 (5), worth a look too, though its 2 existing items already
  cover all 4 elements between them so it's a lower-priority count gap
  rather than a material gap. Held was already the best-covered of the
  four at every Level 1-3, but a real Level 2 Frost gap turned up
  anyway once checked specifically (see the follow-up below) — Held's
  breadth just meant it had less urgency, not zero gaps.

  **Follow-up, same session: two Frost items drafted and priced,
  filling the Ring L3 and Held L2 gaps.**
  - **Numbing Edge** (`I246`, Held, Level 2, 40 Gold) — "When an attack
    with this weapon hits or is Parried, the target gains 2 +
    [Diamonds] additional stacks of Harried." A real, previously-
    unflagged Held L2 Frost gap (checked while drafting this one —
    Held L2 had zero Frost presence at all, unlike L1/L3). Priced
    against the Fanged Guard/Valiant Arms precedent (both L2 Held
    single-effect enchantments, Net=0 at Target=6): ~2.81 hit-or-Parry
    triggers/encounter (3.75 attacks/encounter, an already-established
    figure, × 50% hit chance, + an estimated half of remaining misses
    being specifically Parried) × 2 stacks/trigger × Harried's own
    Locked 1/stack rate, + a `[Diamonds]` suit bonus (per the
    designer's follow-up call to start adding suit synergy to this
    class of effect) = **Value 6.33, Net +0.33 (105% funded)**. Full
    derivation in `balance_ledger.csv`.
  - **Chillstrike Band** (`I247`, Ring, Level 3, 60 Gold) — "Once per
    encounter, for 2 AP, you may make an Acrobatics attack against a
    creature's Dodge Defense within 6 meters. If it hits, the target
    is Slowed 5 + [Spades] times." First drafted as a passive
    forced-movement immunity, reworked per the designer to something
    genuinely *active* for a Ring slot (passive defense reads as
    Neck's lane, not Ring's) — modeled as a portable Level 3 War Magic
    (`T120`) cast with Tormenting Curse (`F061`, converts the spell to
    no-damage in exchange for +3 bonus Feature points) spent on Frigid
    (`F071`, the Slowed-granting Feature), the same "portable War
    Magic" method Flamebinder's Promise already established. Dumping
    the full 7-point Curse budget into Frigid would produce 14+ Slowed
    stacks, wildly past Slowed's own Locked hard cap (4 stacks, Value
    11) — scaled back to 5 base stacks (bumped up from an initial 4
    per the designer, to land closer to Target) + a `[Spades]` suit
    bonus = **Value 10.35, Net +1.35 (115% funded)**. Full derivation
    in `balance_ledger.csv`.

  **Follow-up, same session: two more items drafted and priced,
  filling the Neck L3 count gap and the Torso L1 gap (previously
  empty).** Checked against `RULES_DESIGN.md`'s Suit portfolio table
  per the designer's standing instruction to verify any reviewed
  content against it going forward — neither item ended up touching a
  suit at all (Good Luck's own rate already bakes in its own Suit Pool
  credit; ShallowHeal isn't suit-scaled), so nothing to flag either
  way.
  - **Clarion Cord** (`I248`, Neck, Level 3, 60 Gold) — "At the start
    of each encounter, you and all allies within earshot each have
    Good Luck on their Reflex flip." Went through three revisions
    before landing here. First draft was pure Narrative Utility (no
    combat mechanic) — rejected per the designer as too weak to be
    worth a Level 3 investment. Second draft added a real mechanic but
    as an active "once per encounter, you may call out, choose up to
    four allies" ability — still rejected as reading too active for
    Neck's "not interactive" lane. Reworked to a fully unconditional
    start-of-encounter trigger (no activation, no targeting choice) —
    the same passive shape as Fate's Grasp/Cloak of One Thousand
    Feathers, both already-established "fires automatically" Neck
    items — then narrowed from generic "Good Luck on their first flip"
    to specifically the Reflex (initiative) flip per the designer, for
    a sharper identity: the item version of `T011` One Eye Behind
    You's own self-only "Good Luck on Reflex flips." Finally broadened
    from a capped "up to 3 allies" to "all allies" for simplicity, per
    the designer — priced against a representative party of 4 (wearer
    + 3 allies), the same headcount the capped version already
    assumed, so the Net is unchanged by the simplification: Value = 4
    × Good Luck(2.4) = **9.6, Net +0.6 (107% funded)**. Full derivation
    in `balance_ledger.csv`.
  - **Kindled Wrap** (`I249`, Torso, Level 1, 20 Gold) — "The first
    time each encounter you lose Health, heal 1 Health immediately
    after." Approved as drafted, no revisions. Same always-on-trigger
    shape as Coat of Knit Flesh's own Bleeding-mitigation clause.
    Priced at the inferred ShallowHeal rate (4/point), backed out of
    Healing Potion's (`I043`) own ledger Notes ("ShallowHeal(2)=8") —
    not yet a formally Locked entry in `balance_weights.csv`, flagged
    for a future Locking pass now that it's been reused a second time.
    Value = 1×4 = **4, Net +1 (133% funded)**, comparable to Feathered
    Sandals' own +1.0 Net at Level 1. Full derivation in
    `balance_ledger.csv`.

  **Two real bugs surfaced while drafting these, unrelated to the new
  items themselves:**
  - **`balance_ledger.csv` had genuine pre-existing corruption**: four
    rows (`I095` Grim Promise, `I096` Sorcerer's Bow, `I101-L3`/
    `I101-L4` Elemental-Forged Weaponry) each have an unescaped comma
    in their "Rate of Use/Encounter" field, shifting every later
    column by one — present in git history already, not something
    this session introduced. Worked around it this pass (read/wrote
    via plain list-based `csv.reader`/`csv.writer` instead of the
    Dict variants, which choke on the extra column) rather than fixing
    it, to avoid conflating an unrelated cleanup with this item-adding
    commit — confirmed byte-identical before/after on all four rows.
    Still needs a real fix (re-quote the affected field) whenever
    someone's next in that file.
  - **Harried's suit pairing has an existing inconsistency**: the
    confirmed Suit portfolio table (`RULES_DESIGN.md`) ties Harried to
    Diamonds, but an existing War Magic Feature, Barraging (`F066`),
    reads "Harried X + [Hearts] stacks" instead. Numbing Edge uses
    Diamonds, matching the authoritative table — Barraging's own
    Hearts tie wasn't touched or corrected this pass, just noted.
  - **Follow-up, same session: Crafting School boundaries reviewed and
    fixed before continuing the gap-filling pass.** Per the designer,
    the Cloth/Leather gaps this review surfaced prompted a look at the
    School structure itself first — full writeup in `RULES_DESIGN.md`'s
    new "Crafting Schools — material boundaries and Base Item Option
    coverage, clarified" entry. Short version: Basic Clothing's `Base
    Item Options` was missing from all ten Neck Masterwork items (now
    fixed, `I002,I003`); Basic Clothing/Basic Jewelry's own Effects text
    now states their dual purpose (mundane item and Masterwork base)
    explicitly; Carving got a genuine missing Medium Armor recipe
    (`CR073`/`CR074`, mirroring Tailoring's own fresh+upgrade shape);
    and Bows became Carving-exclusive (Smithing's generic Weapon recipe,
    `CR002`, now excludes them via a new `NameNotContains` `Applies To`
    clause) as Carving's own compensating niche. **The Material Type ×
    Level gap numbers above haven't been re-run yet** — Cloth and
    Leather being a near-interchangeable Tailoring pair may change how
    those two gaps should be read together once this School pass is
    fully settled; picking the gap-filling pass back up is the natural
    next step.
  - **Follow-up, same session: re-ran the gap numbers, bucketed by
    School/Alchemy-type instead of raw Material Type.** The original
    12-Material-Type matrix undercounted real coverage for the two
    paired Schools, since it graded Cloth and Leather (and separately
    Wood and Bone) as two independent gaps each needing their own 3
    items, when a Tailoring or Carving crafter genuinely doesn't care
    which of the pair they end up with. Re-cut into 9 buckets instead
    (one per School for the four mundane pairs/singles, one each for
    the five Alchemy-only Types) and counted an item once if it touches
    *either* member of a pair, at every Level 1-5, across Masterwork +
    Potion/Poison/Grenade:
    | Bucket | L1 | L2 | L3 | L4 | L5 |
    |---|---|---|---|---|---|
    | Metal (Smithing) | 7 | 8 | 3 | 1\* | 1\* |
    | Wood/Bone (Carving) | 12 | 13 | 10 | 7 | 5 |
    | Cloth/Leather (Tailoring) | **2\*** | **2\*** | **2\*** | 0\* | 0\* |
    | Precious (Jewelrymaking) | 4 | **2\*** | **2\*** | 1\* | 1\* |
    | Medicinal (Alchemy) | 6 | 4 | 3 | 2\* | 2\* |
    | Fire (Alchemy) | 9 | 7 | 8 | 3 | 4 |
    | Frost (Alchemy) | 5 | 4 | 8 | **0\*** | 2\* |
    | Brilliant (Alchemy) | 8 | 12 | 8 | 5 | 4 |
    | Shadow (Alchemy) | 11 | 12 | 9 | 4 | 4 |

    **Wood/Bone turns out to have no real gap at all** once merged
    (12/13/10/7/5) — the standalone Leather numbers from the first pass
    were misleading; a Carving-trained crafter was never actually short
    on options. **Cloth/Leather is the one genuine standout**, and a
    much smaller fix than the original unmerged read suggested: it
    needs exactly **one more item at each of L1, L2, and L3** to clear
    the floor (was miscounted as needing 7 Cloth items + 4 Leather
    items separately before the merge — really just 3 items total).
    Its existing L1-3 coverage (Swim Flippers/Bottomless Belt at Feet/
    Belt, Distant Scroll Cases/Watcher's Mantle at Other/Neck,
    Spacious Satchel/Wizardly Hat at Other/Head) also has a real second
    pattern worth acting on: **zero Cloth/Leather items in Held,
    Torso, or Ring at any Level 1-5** — the three "should offer range"
    Slots per `RULES_DESIGN.md`'s standing principle, making one of
    those three the natural target for each of the L1-3 fills rather
    than defaulting to whichever Slot's easiest. **Precious is the only
    other L1-3-relevant gap**, needing one more item each at L2 and L3
    (L1 is already healthy at 4). Metal/Medicinal's own L4-5 thinness
    and Frost's L4 zero stay unaddressed per the standing Level 1-3
    priority principle, same as before. Full working data (per-item
    breakdown feeding this table) in the session's scratch files, not
    committed — regenerable directly from `items.csv` if needed again.
  - **Follow-up: Pillar Ring (`I255`, Level 2, 40 Gold, Precious) fills
    the L2 half of the Precious gap** — the first Precious-material Ring
    item at all (13 existing Ring items, none Precious before this).
    Translated from "Pillar Talisman," one of the Charms in a separate
    dice-based tabletop game's item list handed over as inspiration
    (`IDEAS_BACKLOG.md`'s dice-game section) — conjures a person-sized,
    destructible pillar of force (Total Cover, per `rulebook.md`'s Cover
    and Obscurement section) once per encounter. Full mechanical/value
    derivation in `balance_weights_notes.md`'s own "Pillar Ring" writeup
    (Ring slot, follow-up section) — worth a read for the process alone:
    surfaced that this project has no enemy-stat-block table to gauge
    "what would an on-level attacker's hit look like" against (checked
    the designer's own `archive/flagonquest_balance_notes.xlsx` in full,
    not there either — the designer believes it lives in a different,
    not-yet-located file), caught a real design bug mid-derivation (an
    early Resist formula capped exactly at a maxed attacker's damage,
    making the pillar unbreakable by Levels 4-5), and ended up modeling
    its value around protecting an ally via line-of-sight blocking
    rather than the cheaper "forces a detour" reading, per the
    designer's own steer. Value 6.0, Net 0 (exact fit) at Level 2.
  - **Follow-up: Ring of Comets (`I256`, Level 3, 60 Gold, Precious)
    fills the L3 half of the Precious gap, closing it out entirely
    alongside Pillar Ring.** Also translated from the dice-game Charms
    list (reflavored from a literal falling comet to a gathering blast
    of magic). Built off War Magic's (`T120`) own base with its full
    Level-3 Feature Budget dumped into pure Damage (Destructive, `F062`)
    plus the established Physical-lock bonus, then — per the designer —
    a flat stat baked in rather than scaling off the wearer's Mind: 11
    Physical damage, once per encounter, no attack roll ("hand wave the
    range and to hit... in exchange for it taking a round to set up").
    Full derivation in `balance_weights_notes.md`'s "Ring of Comets"
    writeup (Ring slot, follow-up section) — the interesting part is a
    real correction mid-derivation: a first pass priced this at the
    normal hit-chance-discounted Damage rate, which badly overfunded it
    (140-230% across Levels), before the designer's own diagnosis (a
    guaranteed no-roll hit needs the *guaranteed*-harm rate, 4/point,
    discounted instead by a niche-tier chance the target simply isn't
    there when it lands) landed the math correctly. Value 9.33, Net
    +0.33 (104% funded) at Level 3. **With this, the Precious Material
    Type gap is fully closed (L1-3 all covered).**
  - **Follow-up: Dryad's Mantle (`I257`, Level 2, 40 Gold, Neck) closes
    out the three-item dice-game Charm translation batch.** Picked for
    Neck on mechanical/flavor fit rather than a gap target, since
    Precious was already closed by the other two. Reworked away from
    its original "take the hit, heal 1 after" shape once the designer
    ruled out any healing — an Interrupt that converts the incoming hit
    into a miss entirely, tied to a self-planted sapling anchor, priced
    the same way as Pillar Ring's own protection component (a fully
    avoided hit = 2.25 Health × the guaranteed-harm rate, 4) but at a
    higher ⅔ realization rate per the designer (staying within 10m of a
    self-planted anchor is far more reliable than Pillar Ring's own
    battlefield-geometry dependency). Value 6.0, Net 0 (exact fit) at
    Level 2 — all three translated Charms this pass landed within
    ±0.33 of their Target. Also surfaced a general rule, now in
    `RULES_DESIGN.md`: every Masterwork item should tie to a real Base
    Item Option (Ring → `I003` alone; Neck → `I002,I003` together,
    already the consistent existing practice across all ten other Neck
    items) rather than floating a bespoke Main Material with no
    underlying base — this item's `I002,I003` + Wood now matches that.
  - **Follow-up: Stoic Collar (`I259`, Level 1, 20 Gold, Neck) — "Once
    per encounter, for 1 AP, the party ignores 1 Pressure they would
    otherwise apply this round."** Renamed and moved from Head (where
    it started life as "Stoic Skullcap," a name that stopped making
    sense once it became a Neck item) as part of pricing it properly:
    doing so required building an entirely new **Social Encounter
    Baseline** model from scratch (`balance_weights_notes.md`), the
    social-encounter counterpart to the combat Baseline the old archived
    spreadsheet built, since nothing equivalent existed for pricing
    anything that touches Pressure. The Baseline is a 1-main/3-Support
    party against a 5-round Pressure clock, exact-combinatorics DP
    cross-validated against Monte Carlo, locked at a 57.03% baseline win
    rate. Checking the abstract `Concession/Pressure=2.2` stacking-curve
    math (the first pass, Value≈1.3-2.8) against the real model showed
    it was unreliable in both directions — an always-on version of this
    effect would be wildly overfunded (Value≈15.76, since reducing
    Pressure flips whole rounds across the model's card-rescue
    guaranteed-success line rather than just softening a penalty
    linearly), while the single-use version actually shipped lifts the
    win rate by a modest +5.99pp at its best timing. Landed on Value=3
    as a considered judgment call (the win-rate delta converts
    inconsistently, 2.62-8.78, depending which round's Pressure level is
    assumed) rather than a clean formula output — flagged the same way
    as any Narrative Utility item's honest-guess convention. Target=3
    (L1), Net=0 (exact fit). Also the occasion for renaming "Social
    Contest" to **Social Encounter** throughout the codebase, per the
    designer's own move away from the old "Contest" framing, and for
    drafting the Pressure rule's ignore-vs-remove distinction into
    `rulebook.md` (ignoring softens the Bad Luck but Pressure still
    climbs toward the failure clock; removing actually clears it —
    rarer and stronger) so an item like this can't stall the encounter's
    failure clock indefinitely.
  - **Follow-up, same session: the three Cloth/Leather items drafted and
    priced, closing this gap out (L1/L2/L3 all filled).** Went through
    several redesign rounds — the first drafts for Held (a Leather
    weapon enchantment) and Ring (a leather-cord Crippled-attack) were
    both rejected per the designer as material/lane mismatches (Cloth/
    Leather is Tailoring's domain, not Carving/Smithing's; Ring's own
    lane needs a material with a real jewelry precedent) and moved to
    `IDEAS_BACKLOG.md` rather than forced into slots they didn't belong
    in — a first attempt at a Hands Archery-Good-Luck glove was also
    dropped per the designer's standing preference against direct-
    combat-implication Hands items, and an initial Feet Speed-boost
    idea was dropped for being a plain reskin of Lightfoot Shoes.
    - **Quilted Overcoat** (`I250`, Torso, Level 2, 40 Gold) — "The
      wearer gains a +1 bonus to Physical Resist." `Base Item Options`
      deliberately restricted to `I002` Basic Clothing only (every
      other Torso item also allows the 3 Armor tiers) — the whole
      point is staying compatible with the "Unarmored" Technique
      prereqs already noted in `RULES_DESIGN.md` as a real, intended
      niche. Reuses Robes of Resilience's own Physical Resist rate
      (5.0/point). Value = 5.0, Net -1.0 (83% funded).
    - **Sure-Grip Boots** (`I251`, Feet, Level 1, 20 Gold) — "When
      climbing, the wearer's movement is never limited by their
      Athletics budget, and they have Good Luck on Athletics flips
      made while climbing." A genuine gap in Feet's own roster (covers
      combat wall-running via Shadowcat Slippers, nothing for
      sustained climbing). Reuses Vaulting Boots' own "+2 vertical-
      budget-bypass" flat credit at an assumed ~1.5 climbs/encounter
      (3.0), plus a half-tier Good Luck on climbing Athletics flips
      (1.2) added per the designer to make sure it lands with real
      weight. Value = 4.2, Net +1.2 (140% funded, a deliberate
      designer-requested overshoot).
    - **Dancing Shoes** (`I252`, Feet, Level 1, 20 Gold) — "The wearer
      has Good Luck on flips made to blend in or otherwise seem to
      belong at a formal social event or dance. The wearer is never
      considered inappropriately dressed for such an event, and gains
      no Pressure for it." Half-tier Good Luck on Masquerade (1.2,
      matching Shroud of Shadowy Stillness's own treatment) plus a
      small discounted credit for negating one of `rulebook.md`'s own
      named Pressure sources (being underdressed) — 2.2 × 0.25
      situational chance = 0.55. Value = 1.75, Net -1.25 (58% funded).
    - **Gloves of Misdirection** (`I253`, Hands, Level 1, 20 Gold) —
      "The wearer is treated as though they know Distraction, or an
      extra copy of it if they already know it." Distraction (`T144`)
      is a new Technique this same pass — see below. No activation
      cost or daily gating (unlike Focusing Band of [Technique]), so
      priced at the full, undiscounted Technique-value convention
      (Level × 3 for Encounter cadence). Value = 3, Net = 0 (exact
      fit). Main Materials includes Shadow as a third alternative
      alongside Cloth/Leather, matching the item's stealth theme.
    - **Preserving Larder** (`I254`, Other — no equipment Slot, Level
      3, 60 Gold) — "Only Food materials, rations, or other food items
      can be stored in the bag... the bag can hold 100 cubic meters...
      Food stored within never spoils." The last Cloth/Leather gap
      (Level 3), closing the bucket out entirely. A food-only sidegrade
      to Placeholder's Spacious Satchel (`I115`, also Other slot) —
      same 100-cubic-meter capacity and mouth-size text, narrowed to
      Food materials/rations, plus the no-spoilage clause (Food
      materials genuinely do spoil a week after gathering, per
      `rulebook.md`'s own Material Types section — not an invented
      restriction). **Re-derived** in the follow-up Storage review (see
      `balance_weights_notes.md`'s "Preserving Larder" writeup): the
      Storage-capacity model's AP-saved-on-retrieval logic turned out
      not to fit a Food-only bag at all (nobody retrieves rations
      mid-combat), so per the designer's own steer, this instead prices
      the value of the food it saves from spoiling — a large-beast kill
      (10 Food, Level 1) is worth 10 Gold nominally → 15 raw Value at
      the established `Gold = 1.5` rate, discounted at the standard ⅓
      niche tier (a spoilage-risking windfall isn't an every-fight
      occurrence): `15 × ⅓ = 5.0`. **Value = 5.0, Net -4.0 (56%
      funded)** — in the same band as its Storage-family peers
      (Spacious Satchel 61%, Sash of Deep Pockets 51%). This also
      surfaced a real gap: `rulebook.md` had no base-game guidance for
      how much food a kill yields, only a vague line that turned out to
      live in the Goblin Game chapter specifically — closed by
      generalizing that chapter's own "adult Goblin = 5 Food" anchor
      into a base-game size table (Material Types' Food bullet).
      Distant Scroll Cases (`I114`) was reviewed alongside this and
      left unchanged — its mechanic (sharing a small pocket of space
      across distance, sized for documents) isn't a capacity item
      either, and its existing Narrative Utility pricing already fits.
      **With this item, the Cloth/Leather Material Type bucket is fully
      closed out** — 5/3/3/0/0 across L1-5, no L1-3 gap remaining (see
      the `RULES_DESIGN.md`/`balance.md` re-run entries above for the
      full arc: Quilted Overcoat, Sure-Grip Boots, Dancing Shoes,
      Gloves of Misdirection, and this item).
  - **New Technique, same session: Distraction (`T144`), Level 1,
    Encounter.** Reconstructed from an old, never-carried-forward draft
    found in `archive/flagonquest_site_techniques.md` (per the designer,
    "might have been an older one") — the original was Level 3 with a
    3-skill prereq (Awareness 2, Insight 2, Stealth 3) and a broken/
    truncated suit-bonus clause. Found `T052` Vanish as an almost-exact
    structural sibling already live in the current ruleset (Level 3,
    Encounter, single-skill Stealth 4 prereq, 1 AP, a Stealth-attack-
    against-Instinct-Defense AoE) and used it as the calibration anchor
    rather than reviving the old draft's heavier shape. Final text:
    "Make a Stealth attack against the Instinct Defense of each target
    [within 5m of a chosen point, 10m range]. If it hits, the target is
    distracted for 3 rounds, plus 1 additional round for each Extra
    Success. A creature stops being distracted only if an imminent
    threat or the start of combat draws their attention away — not
    simply by any other distraction. While distracted, a creature has
    Bad Luck on any flips to notice anything other than the
    distraction. A creature already paying close or specific attention
    to something when the attack is made is immune." Prereq: Stealth 2
    (matching Feint's own L1 single-skill-prereq shape, not Vanish's
    heavier L3 gate). Dropped to **Level 1** per the designer's own
    read, confirmed: unlike Vanish, this Technique is explicitly voided
    by the exact situation (a real threat, combat starting) where a
    debuff would normally matter most, so its real utility sits almost
    entirely in the pre-combat/infiltration space — a much narrower
    band than Vanish covers, supporting the lower Level. Duration
    scaling folds suits in through the existing Extra Success system
    rather than a bolted-on `+[Suit]` clause. Range tightened from the
    old draft's 20m to 10m per the designer. Not run through THE
    TABEL's own Value/Target math — per the designer, this one leans
    narrative by design, and Vanish's own precedent was judged a
    sufficient calibration anchor on its own.
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
- **Storage/capacity items reviewed as a family — model weights fixed,
  outlier items repriced.** A real "Storage capacity" model already
  existed (`balance_weights_notes.md`) — cap "genuinely extra slots
  used" at 3, `2.75` base credit (3 × 2.75 AP-equivalent × ⅓ niche
  frequency), `+0.917`/slot for a qualitative large-object
  differentiator — correctly applied to Placeholder's Bottomless Belt,
  Smuggler's Belt, Sash of Deep Pockets, and Placeholder's Spacious
  Satchel (all landing in the normal 51-112% funded range). The real
  gap: **Distant Scroll Cases** (`I114`, 2/6, 33% funded) and
  **Preserving Larder** (`I254`, 3/9, 33% funded) both got priced via
  Narrative Utility instead, despite being genuine capacity items — the
  only two in the whole family sitting well below everyone else's
  funding ratio. Quick Draw Belt/Hair-Trigger Belt (retrieval *speed*,
  modeled directly off Technique T039) and Belt of the Wayfarer
  (on-demand item *production*, a genuine once/day resource) are
  correctly a different thing, not part of this inconsistency.

  Two real model bugs caught reviewing the whole family together, both
  fixed this pass:
  1. `balance_weights_notes.md`'s own Storage section still described
     the Target scope as the old, superseded once/day `Level × 4`
     formula — corrected project-wide to per-encounter `Level × 3`
     (matching what every ledger row actually uses) when the Belt pass
     first ran, but this one paragraph was never updated to match.
     Fixed to say `Level × 3`, with a note explaining the correction.
  2. The `+0.917`/large-object-slot rate had never been given its own
     `balance_weights.csv` row, only prose — added as "Storage capacity
     component (large-object slot)."

  **Also found real pre-existing corruption in `balance_weights.csv`**
  while doing the above (same class of bug as the known
  `balance_ledger.csv` corruption, unrelated to this session's edits):
  10 rows have more columns than the header, meaning a straight
  `csv.reader`/`csv.writer` round-trip silently mangles them. Worked
  around it this pass (a precise text-based line insertion instead of
  a full round-trip, same technique already used for
  `balance_ledger.csv`) rather than fixing it — flagged here for
  whenever someone's next in that file with time to re-quote the
  affected rows properly.

  **Resolved.** Distant Scroll Cases turned out to be correctly priced
  as-is — its mechanic (two cases sharing a small pocket of space
  across distance, for documents specifically) was never really a
  capacity item, just a narrow logistics/communication effect, so
  Narrative Utility is the right convention for it after all. Preserving
  Larder did need repricing, but not by borrowing Spacious Satchel's
  capacity credit directly as first assumed — per the designer, the
  Storage-capacity model's whole AP-saved-on-retrieval basis doesn't
  fit a Food-only bag (nobody retrieves rations mid-combat), so it's
  priced instead on the food it saves from spoiling: a large-beast kill
  (10 Food, Level 1) worth 10 Gold nominally → 15 raw Value at the
  established `Gold = 1.5` rate, discounted at the standard ⅓ niche
  tier, landing at **Value 5.0, Net -4.0 (56% funded)** — see the
  Preserving Larder bullet above and `balance_weights_notes.md`'s own
  writeup for the full derivation. That also closed a real content gap:
  `rulebook.md` had no base-game guidance for how much food a kill
  yields, so the Goblin Game chapter's own "adult Goblin = 5 Food"
  anchor was generalized into a base-game size table on the Food
  Material Type bullet — flagged in `PROSE_REVIEW_QUEUE.md` for a
  later read-through, same as any other rulebook prose edit.

  Also confirmed: **Placeholder's Sneaky Storage** (the "limited
  magical storage" spell the designer recalled) exists only in
  `archive/flagonquest_site_techniques.md` — a cut Level 2 Spell, not
  in the current ruleset. Per the designer, left archived for now;
  logged in `IDEAS_BACKLOG.md` as a candidate for the same
  archive-recovery treatment Distraction (`T144`) got, once there's
  appetite for another pass like that.

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
  `Rate = 1` / `Target = Level × 4` (the once-per-day convention as it
  stood then). **Re-scored again** after the once/day Target formula's
  own follow-up correction (`Level × 6`, not `× 4` — see the Scoping
  window section above): **Hearty Meal** Net −2 (was 0), **Power
  Snack** Net −2.39 (was −0.39, using Sift's own corrected weight, see
  below), **Soul Soup** Net −1.5 (was −1), **Muscular Feast** Net
  −0.733 (was +1.267).

  **Retuned (2026-09-15), per the designer's own framing that Food
  items are start-of-day prep the player carries forward and spends at
  their own discretion, not an instant or forced effect.** Also added a
  new rulebook rule as part of this pass (`rulebook.md`, Food and
  Exhaustion): a character only benefits from the bonus effect of the
  *first* special-effect meal (Power Snack, Hearty Meal, and the like)
  they eat in a day — eating a second still counts as that day's food,
  but grants no further bonus. This makes each Food item's once/day
  Target genuinely mean "your one pick for the day" instead of an
  unenforced assumption, and is what makes leaving Soul Soup's Level 5
  generous (below) safe rather than stackable/abusable.
  - **Power Snack** — added `[Level]` charges of Good Luck, usable on
    any flip before the next rest. Net +0.01, an almost exact fit at
    every Level (both terms scale linearly with Level).
  - **Hearty Meal** — generalized from a Shallow-only heal to a bonus
    on the next Recovery Cycle (the rulebook's own rest-Cycle term),
    inheriting that Cycle's existing Shallow/Deep split choice; priced
    at Deep Heal's rate (5/point) per the "price the rational best
    choice" convention. Net −1.0, deliberately accepted under Target —
    the designer's call, since this reads as strong and generically
    useful enough to be worth the shortfall.
  - **Soul Soup** — grants `[Level]+1` Vigor (see the new Vigor keyword
    in `glossary.md`, also adopted by Solemn Covenant's near-identical
    "Covenant points") instead of `[Level]`, letting it refund a
    Technique one Level above its own. An asymmetric fix in the same
    spirit as Soldier's Salts, but shaped differently since Soul Soup
    has no AP cost to taper away — Net ranges from +3 at Level 1 down
    to −3 at Level 5 (uncapped: the new "only your first special-effect
    meal counts" rule above makes this an exclusive daily pick, so the
    designer was fine leaving the top end generous; the −3 figure is
    also likely conservative, since 6 Vigor can split across two real
    Techniques rather than needing one hypothetical "Level 6" Technique
    the way the simple pricing formula assumes).
  - **Muscular Feast** — left as-is. Its Value doesn't scale linearly
    with Level (Bleeding/Crippled/Slowed each have their own non-linear
    per-stack curves), so no clean multiplier closes the gap without
    overshooting by more than the −0.73 shortfall is worth fixing;
    formally accepted rather than retuned.

  Travel Rations remains out-of-model (no combat mechanic to price).
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
  until it lands a hit or the wielder gets a full night's rest, and
  once a normal attack lands and deals Health loss, the poison
  automatically makes its own attack against Vital Defense). The AP charge double-counted an action the wielder wasn't
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
