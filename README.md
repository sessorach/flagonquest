# FlagonQuest

FlagonQuest is a browser-based companion site for the FlagonQuest tabletop
RPG — a beer-and-pretzels TTRPG for the modern gamer. It's a technique/item
browser, character builder, and printable character sheet, all in a single
static HTML file with no build step, deployed via GitHub Pages. Game
content (techniques, items, backgrounds, and so on) is maintained as
spreadsheets under `scripts/` and converted to the JSON the site reads via
`scripts/convert.py`.

## Changelog

Notable changes, newest first. Each entry is a summary — see `git log` for
the full commit-by-commit detail behind any of these.

### 2026-09-17 — New Technique (Distraction) and four Cloth/Leather items

- **Distraction** (new Technique, Level 1, Encounter, Stealth 2) — a
  Stealth attack that distracts everyone near a chosen point for a few
  rounds, useful for slipping past guards rather than for a fight.
  Reconstructed from an old, never-finished draft and rebalanced
  against Vanish, its closest sibling in the current ruleset.
- **Quilted Overcoat** (Torso, Level 2, 40 Gold) — +1 Physical Resist,
  built only on Basic Clothing rather than Armor, so it stays
  compatible with "fighting unarmored" builds.
- **Sure-Grip Boots** (Feet, Level 1, 20 Gold) — removes the climbing
  movement cap and grants Good Luck while climbing, filling a real gap
  between the game's combat wall-running items and nothing for
  sustained climbing.
- **Dancing Shoes** (Feet, Level 1, 20 Gold) — Good Luck to blend in
  at a formal event, and never counts as underdressed for one.
- **Gloves of Misdirection** (Hands, Level 1, 20 Gold) — grants a copy
  of the new Distraction Technique.
- All four fill the last of the Cloth/Leather material-type gaps
  identified in the earlier Slot × Level review.

### 2026-09-17 — Crafting recipe cleanup: Main Types wording, Basic Clothing

- Nine crafting recipes (Weapon/Armor via Carving or Tailoring, plus
  Unarmed Enhancer and Musical Instrument) had their Main Materials
  reworded from an ambiguous `Wood, Bone`/`Cloth, Leather` comma-list
  to an explicit `Wood or Bone`/`Cloth or Leather` — matches the intent
  (either material works) rather than the literal "you need one of
  each" reading the rulebook's own Materials rule gives an unjoined
  list.
- Basic Clothing's own recipe now lists Cloth or Leather as its Main
  Types (previously Cloth-only, with Leather buried in Optional) and
  Bone/Metal/Precious as Optional.

### 2026-09-17 — Crafting School boundaries clarified: Neck/Clothing, Carving Medium Armor, Bows

- Basic Clothing is now a valid base item for Neck Masterwork items
  (previously Neck only offered Basic Jewelry, despite several Neck
  items being literal cloaks) — all ten existing Neck items updated.
- Basic Clothing and Basic Jewelry's own descriptions now spell out
  their dual purpose: plain mundane wear on its own, or the base item
  a Masterwork enchantment for the same slot gets built onto.
- Carving can now make Medium Armor (previously stopped at Light,
  while Tailoring and Smithing both reached Medium) — a genuine
  oversight, now fixed with a fresh-build and an upgrade-from-Light
  recipe matching Tailoring's own shape.
- Bows are now Carving-exclusive, giving Carving a real niche of its
  own rather than just trailing Smithing everywhere — matches
  `rulebook.md`'s own long-standing worked example, which already
  assumed a Carving-based bow.

### 2026-09-16 — Two new Masterwork items: Clarion Cord, Kindled Wrap

- **Clarion Cord** (Neck, Level 3, 60 Gold) — a fully passive item: at
  the start of each encounter, the wearer and all allies within
  earshot have Good Luck on their Reflex (initiative) flip.
- **Kindled Wrap** (Torso, Level 1, 20 Gold) — heals 1 Health the
  first time the wearer loses Health each encounter.
- Fills the Neck L3 count gap and the previously-empty Torso L1 slot,
  identified during the same Slot × Level gap review as Numbing Edge
  and Chillstrike Band below.

### 2026-09-16 — Two new Frost Masterwork items: Numbing Edge, Chillstrike Band

- **Numbing Edge** (Held, Level 2, 40 Gold) — a Frost weapon enchantment
  that adds bonus Harried on a hit or a Parried attack, giving the rest
  of the party an opening against a heavily-armored, Parry-reliant
  target.
- **Chillstrike Band** (Ring, Level 3, 60 Gold) — a Frost ring with an
  active, once-per-encounter attack that Slows a target, rather than a
  passive effect (Ring is meant to be something you *do*, not a
  standing buff).
- Both fill real gaps identified while reviewing crafting material
  coverage — Frost had zero representation in either of these
  Slot/Level combinations before now.

### 2026-09-16 — Crafting Skill Total requirements reorganized

- Reworked the Skill Total needed to craft across the board, landing
  on a cleaner tiered table: **3** for genuinely basic goods (Light
  Armor, everyday tools, and simple "convenience" Alchemy goods like
  Alcohol/Charcoal/Oil), **4** for real adventuring gear (Weapons,
  Skill Kits, and your first Level 1 Potion/Poison/Grenade), **5** for
  Medium Armor and bigger packs, **6** for Survivalist's Pack and
  Level 2 Potions, and **7** — a new "master craftsperson" ceiling —
  for Heavy Armor and large Wagons.
- Masterwork items and the core Alchemy/Cooking progression (Potions,
  Poisons, Grenades, Food) now share one Skill Total curve across
  Levels 1-5, fixing a gap where the easiest Alchemy items used to
  require no more Skill than just being allowed to learn Alchemy in
  the first place.
- A handful of "convenience" Alchemy goods (Alcohol, Incense,
  Embalming Fluid, Recreational Drugs, Quicktorch, Basic
  Conveniences/Charcoal/Oil) no longer scale in difficulty with their
  own quality — a fancier bottle of Alcohol costs more Gold, not more
  training.
- Five recipes that had no crafting School requirement at all
  (Climber's Kit, Tinker's Kit, Mixology Set, plus Musical Instrument
  and Disguise Kit, which now offer a choice of two) now correctly
  require one, closing a real gap rather than a documented exception.
- 17 Hands and Feet Masterwork items (gloves and boots — Deft Gloves,
  Vaulting Boots, and the rest) can now be crafted from either a Basic
  Clothing or a Basic Jewelry base, so a Jewelrymaking-trained
  character can make a bracelet or anklet version instead of always
  needing Tailoring. Basic Jewelry's own description already covered
  Hands and Feet slots; the actual items just hadn't caught up to it.

### 2026-09-15 — 15 new "basic adventuring tool" items added

- Classic dungeoneering gear drafted as real items for the first time
  (10-foot pole, crowbar, manacles, and a dozen others), split into a
  flavor-only "Basic Tool" family (Hammer, Shovel, Pickaxe, Chain,
  Small Mirror, Iron Spikes, Lantern, Tripwire Bells, 10-Foot Pole,
  Ladder, Torch, Block and Tackle — 1-2 Gold) and a niche-mechanical
  family (Crowbar, Manacles, Grappling Hook — 3 Gold, each granting a
  real but situational mechanical benefit). See
  `design/balance.md`'s pricing tiers reference for the full pricing
  rationale.

### 2026-09-15 — Adventurer's Kit retired; Rope, Camping Kit, and Firestarter added

- Adventurer's Kit's old flavor-text bundle (mess kit, bedroll,
  waterskin, knife, rope, tinderbox) is retired in favor of three real
  items: **Rope** (1 Gold, the clearest "you'd buy more of this"
  case), **Firestarter** (2 Gold, reworded from "Tinderbox" into
  something deliberately open-ended — flint and steel, a fire-bow,
  whatever fits), and **Camping Kit** (3 Gold, everything else).
  Starting gear moves from a flat 5 Gold to 6 (1+2+3), reflecting the
  split items' real value. Belt of the Wayfarer's "produce any item
  from an Adventurer's Kit" updated to name all three; its own pricing
  is unaffected, since that clause was already valued at essentially
  zero.
- Also formalized the everyday-goods pricing tiers these fit into as a
  reference chart, and grouped Basic Conveniences/Charcoal/Oil under
  one shared "Basic Convenience" recipe (Alchemy, Mixology or
  Survival) — see `design/balance.md`.

### 2026-09-15 — Masquerade's Bad Luck/Good Luck rule; Musical Instrument un-gated

- New rule for Masquerade: attempting a disguise with nothing to back
  it up gives Bad Luck, a Disguise Kit clears that penalty for an
  everyday disguise, and a specific prop matched to exactly who you're
  impersonating (a real guard's uniform, not just a costume) grants
  Good Luck instead — settling where the item itself sits relative to
  clever, situational roleplay.
- Musical Instrument was wrongly priced alongside the other Craft-
  School/mechanical skill kits at a uniform 5 Gold — Performance
  doesn't actually require one (singing works fine), so it's flavor
  gear, not a Bad-Luck-avoiding tool. Repriced to 3 Gold, with an
  explicit Effects line saying so.

### 2026-09-15 — Food items retuned; new Vigor keyword

- Closed out the last open finding from the Alchemy balance pass: Power
  Snack, Hearty Meal, and Soul Soup were all under Target once the
  once-per-day Food formula got corrected. All three now grant a
  player-discretion bonus they carry through the day instead of
  something automatic — Power Snack and Hearty Meal add banked Good
  Luck/healing, and Soul Soup gets an asymmetric refund (can refund a
  Technique one Level above its own, capped at Level 5). Muscular Feast
  was formally accepted as slightly under Target rather than retuned.
- New shared glossary term, **Vigor** — the "pay a Technique's own
  Level to refund it" mechanic, previously reinvented under two
  different bespoke names (Soul Soup's "Nutrition points", Solemn
  Covenant's "Covenant points"). Both items now read consistently, and
  any future item using this trick can just say "Vigor."

### 2026-09-15 — Recipes for the remaining Tool/Kit and misc. Pack/Gear items

- All 10 "skill kit" Tool/Kit items (Musical Instrument, Climber's Kit,
  Disguise Kit, Tinker's Kit, Fisher's Kit, and the 5 Craft-School kits)
  are uniformly priced at 5 Gold per the designer, each with a matching
  Craft 4 / 5-material recipe (Metal for every Craft-School kit, per
  the "tools are metal regardless of which School they serve" reasoning
  below; Bone/Metal/Wood, Leather+Metal, Cloth/Medicinal, Metal, and
  Wood+Metal respectively for Musical Instrument/Climber's/Disguise/
  Tinker's/Fisher's). The original design doc had lower figures for
  some of these (3-6 Gold) that had gone unused, but the designer
  confirmed the 5 Gold figure is where these actually landed, not the
  older doc's numbers.
- 8 simple Level 1-3 Pack/Gear consumables (Basic Conveniences, Charcoal,
  Incense × 2 Levels, Oil, Embalming Fluid, Quicktorch, Recreational
  Drugs × 2 Levels) got straightforward one-material recipes — no real
  precedent for these existed, so they're a fresh, deliberately simple
  design rather than a backfill.

### 2026-09-15 — Real recipes for 9 more basic Pack/Gear items

- Carts/Wagon (Small/Medium/Large), the four packs (Knapsack, Backpack,
  Rucksack, Survivalist's Pack), Adventurer's Kit, and Adventurer's Belt
  all moved off the generic "Other Items" reference-only fallback onto
  real recipes — Craft School, Skill Total, and Total Materials all
  sourced from the original design doc and cross-checked against each
  item's current Gold Cost (Total Materials = Cost, same Gold-
  equivalence rate as everything else).

### 2026-09-15 — Alcohol has its own crafting recipe; new Crafting Notes column

- Alcohol (all five Levels) now has a proper Alchemy recipe instead of
  falling to the generic "Other Items" reference-only fallback: Mixology
  [twice the Level], one Medicinal material of its own Level — priced as
  a plain reagent rather than a proper Potion, consistent with Alcohol's
  Cost already being exactly its Level in Gold.
- The Wizardly Hat of Tam the Tipsy's Main Materials changed from just
  Fire (with Alcohol optionally substituting for it) to requiring one
  material each of Fire, Alcohol, and Cloth, now that Alcohol has a real
  recipe to hang that requirement on.
- New optional `items.csv` column, "Crafting Notes" — a crafting-time
  detail that doesn't fit the structured recipe fields and isn't part of
  what the finished item does, so it stays out of Effects and shows only
  in the Crafting tab instead. Placeholder's Speedy Scepter's "base item
  must start with S" restriction and the Wizardly Hat's Alcohol-as-
  material rule both moved here from Effects, where they used to be the
  one bit of crafting-only prose mixed into otherwise pure gameplay text.

### 2026-09-14 — Armor upgrade recipes, tightened Might Requirements

- Armor can now be crafted by reinforcing an existing lower tier
  instead of only building fresh — pay just the Total Materials
  difference between tiers (Light→Medium 2, Medium→Heavy 2,
  Light→Heavy 4) at the same Craft requirement and time. Medium's
  upgrade path is craftable via either Tailoring or Smithing; Heavy's
  upgrade paths stay Smithing-only, matching Heavy's own restriction.
- Might Requirements tightened: Medium `4→5`, Heavy `6→7` (Light stays
  3). Heavy's 7 sits exactly 1 point past the character-creation
  ceiling for a fully-invested Might Skill Total (6), so it's
  deliberately unreachable at creation and opens up after a single
  Experience rank-up.
- Fixed two real bugs found while wiring this up: a CSV-quoting
  corruption from an unquoted comma in a recipe name that silently
  shifted later fields by one column, and a crafting-recipe merge
  precedence bug that would have made the new upgrade recipes ignore
  their own reduced material counts.

### 2026-09-14 — Baseline Weapons and Armor balanced, new 3-tier Armor

- First balance pass through the base (non-Masterwork) Weapon and
  Armor items — `I117`-`I135` Weapons and `I128`/`I129` Armor — which
  carry no Level, so a new pricing model was built instead of reusing
  the Masterwork `Level × 3/6` Target: raw `Accuracy+Damage+Weapon
  Defense` compared against `baseline(8) + 2 (Archery) − 2
  (Acrobatics) + 2 (two-handed)`, plus a new Range-value curve for a
  weapon's own inherent engagement distance and a reload penalty for
  fire-every-shot firearms.
- **Light/Heavy Thrown** Damage trimmed (`3→2`/`4→3`) but kept
  deliberately generous, so Thrown stays a viable flexible/backup
  weapon line for non-combat-focused archetypes.
- **Light/Heavy Bow** ranges swapped (`15→19`/`20→17`) into a
  "precise sniper, longer reach" vs. "hard-hitting, shorter reach"
  identity — Accuracy/Damage left untouched on both.
- **Armor reworked from 2 tiers to 3** — added a new **Medium Armor**
  (Resist 2, Dodge −1 only) between Light (unchanged) and Heavy
  (Resist raised `2→3`, same Speed/Dodge penalties as before). Fixes
  the old 2-tier Heavy Armor paying double Light's Gold for barely
  more value. Might Requirement now gates the jump from Medium to
  Heavy at the Speed penalty specifically, not Gold or raw stats.
- Formalized two standing design assumptions in `RULES_DESIGN.md`: a
  baseline weapon attack should net ~2-3 damage over a Light-Armored
  target's Resist (traced to the original balance spreadsheet, and
  confirmed directly against the actual weapon numbers), and going
  Unarmored is an intentional opt-in archetype choice, not a gap.

### 2026-09-13 — Held cluster closed out

- Worked through all 30 Held Masterwork items, the largest single slot
  by far. Cut six items outright (**Weapon of Sending**, **Staying
  Gauntlets**, **Returning Knives**, **Spiritlink Scepter**, **Scepter
  of Evocation**, **Apprentice's Dueling Catalyst** — mostly superseded
  by another item in the same pass) plus **Elemental Bloodletter**,
  whose damage-to-Bleeding conversion turned out to be a structural net
  loss once checked against Bleeding's own capped curve.
- Derived a second **attacks/turn baseline (`1.25/turn`)** for pricing
  an always-on effect that rides the wielder's own attacks, alongside
  the existing `1.5/turn` figure (kept for aggressive/tank scenarios) —
  surfaced while re-pricing the Held slot's permanent Range and
  elemental-conversion items.
- Priced a 4-item elemental-weapon family together (**Claw of
  Mortality**, **Rimefang**, new item **Radiant Verdict**,
  **Conflagration Brand**), deriving a new **continuously-refreshed
  debuff** pricing technique and a **Fire-baseline elemental-conversion
  rate** for spells (spells default to Fire damage, not Physical, so
  converting them is worth much less than converting a weapon attack).
- **Heartseeker** fully redesigned — its original "treat any card as a
  Heart" mechanic did nothing under the current suit-governance rules
  and dated back to an older variable-damage system. Now grants a
  guaranteed Extra Success via the kept flip card.
- Derived the full **Good Luck stacking curve** (exact card-deck
  combinatorics) to price **Thrumming Focus**'s "spend AP for extra
  Good Luck" mechanic, finding that a second stack on the same attack
  is a net loss — rational play self-caps at one activation without
  needing an explicit rule.
- **Placeholder's Speedy Scepter**'s AP-discount mechanic caught and
  closed as a real exploit before shipping (uncapped, it could fund
  extra actions per turn, not just cheaper ones) — capped to once/turn
  and given a special crafting restriction (base item name must start
  with "S").
- **Blade of Fortune** (renamed from Scaraculpi's Gleaming Justice)
  closes out the slot at an exact-fit Good Luck weapon, resolving a
  design flag that it read stronger than Thrumming Focus's similar
  effect — the two now sit at different Levels with different costs.

### 2026-09-06 — Ring cluster closed out

- Cut two items: **Ring of Charming, Assertive, or Bold Statements**
  (duplicates the Head hats' Good-Luck-on-a-Skill family) and
  **Flamefist's Approach** (its Brawl/Spell interplay was pulled to
  `IDEAS_BACKLOG.md` as a `[Form]` Technique idea instead — a toggled
  combat stance fits the concept better than a passive Ring). A third,
  **Bloodshard Ring**, was already cut earlier this same pass.
- **Fate's Grasp** and **Worry Token** swapped slots (Neck ↔ Ring),
  checked directly against `RULES_DESIGN.md`'s own Neck/Ring design
  lanes: Fate's Grasp's automatic, no-decision Sift trigger is Neck's
  "passive utility" case, Worry Token's deliberate charge-spend is
  Ring's "active ability" one.
- **Fate's Grasp** priced by deriving its daily card-spend total exactly
  from the Cycles rule (Draw Cycle income = Discard Cycle's mandatory
  clear, so nothing carries over day to day) rather than guessing — the
  best-fitting multiplier landed it at Level 4 with "Sift up to three
  times that many cards."
- **Heartbinding Band** reworked to close a real Shallow/Deep healing-
  rate arbitrage (the recipient's free choice of type let a rational
  pair launder cheap Shallow loss into valuable Deep healing) — priced
  instead on a cleaner story: recycling a capped-out donor's otherwise-
  wasted daily rest-healing into healing an ally actually needs.
- **Focusing Band of [Technique]** closes out the slot with a new,
  reusable Technique-value convention (`balance_weights.csv`): a
  Level-N Technique is worth the same `Level × 3`/`Level × 6` a
  same-Level item's own Target represents. Also fixed a real rules gap
  — a Technique with its own choices (Feature picks, Free Text options)
  is now explicitly bound to a specific copy the creator already knows.
- **"Thrice" retired project-wide**, replaced with "three times" across
  every item/technique/feature/rulebook occurrence — reads as an
  archaic outlier once a counting sequence needs "four times"/"five
  times" anyway.
- Backfilled `design/balance_ledger.csv` and `balance.md`'s per-slot
  summaries for the Feet, Head, and Neck clusters, which had full
  writeups in `balance_weights_notes.md` but no matching rows/summaries
  in the other two tracking files — a gap that had opened silently over
  several slots before being caught. Added a standing note (`CLAUDE.md`)
  to keep all three files in sync going forward.

### 2026-09-05 — Neck cluster closed out

- Cut three items: **Choker of Silent Whispers** (a strictly-worse
  reskin of Headband of Telepathy), **Cape of Many Pockets** (duplicates
  existing Belt storage items), and **Cloak of Faces** (found sitting in
  the old design doc's rejected-ideas "bin," never actually meant to
  ship — Hat of Disguise already covers this design space).
- **Snowfall Drape** redesigned around the new **Burst (X)** keyword
  (`glossary.md`, "this space, plus every space within X meters of it")
  — fixed at Level 3, 2 degrees of Difficult Terrain, Burst 1 footprint,
  replacing an uncapped-scaling version that read as overpowered past
  Level 1. Converted several existing area effects (Grenades, a few
  Masterwork items and Techniques) to the same Burst phrasing.
- **Choker of Defiance** reworked: Sift now triggers as an Interrupt
  after a flip (so it can actually feed that flip's suit pool) and
  derives a real suit-pool credit instead of folding it silently into
  Sift's own rate; kept its deliberate "locks until the next Discard
  Cycle" clause to stop free deck-stacking.
- **Cloak of One Thousand Feathers** repriced as three components
  (modest fall-damage prevention, a small uncapped-tail-risk premium,
  and the real headline benefit — solving traversal problems by jumping
  instead of climbing/rappelling) rather than one blown-up number.
- **Worry Token** replaced a broken GM-secret random table with a
  suit-keyed Sift — each of the four suits' effect built from that
  suit's own established identity (`RULES_DESIGN.md`'s Suit portfolio),
  including a new general-purpose **Hand Filtering** balance rate for
  "draw + discard" hand-management mechanics.
- Named the three steps of **A Full Night's Rest** as Cycles (Discard,
  Recovery, Draw), with a default ordering rule for anything that hooks
  into one — surfaced while designing Choker of Defiance's unlock
  condition.
- Added `design/PROSE_REVIEW_QUEUE.md` — a checklist of `rulebook.md`/
  `glossary.md` sections written or edited during an AI-assisted
  session, since there's no way to leave an inline review marker in
  those files.

### 2026-08-31 — Torso cluster closed out; Resist's rate fixed

- Fixed **Resist**'s per-point rate — it was double-discounting hit
  chance (Physical 2.5→5.0, Fire 0.5→1.0, other elements 0.25→0.5 per
  point). Recomputed everything that depends on it: Elemental-Resistant
  Armor, Robes of Resilience, Robes of the Elemental Lord, and Ward's
  flat-Resist component.
- **Fitted Armor** reworked from an undocumented "-1 Might Requirement"
  effect into a flat +1 Physical Resist grant, priced for the
  tank/bruiser build who'd actually equip it.
- **Fortified Armor**'s stale "red card" trigger (a leftover from an
  old bonus-success rule) fixed to "scored an Extra Success," matching
  current mechanics — now correctly softens spike damage instead of
  referencing a rule that no longer exists.
- **Jerkin of the Land** cut as a duplicate of Shawl of the Land
  (Neck) — this completes the full 9-item Torso Masterwork cluster.
- `balance_weights.csv` gained "Derived From" tracking and a
  Situational Multipliers section, to catch this kind of
  double-discount before it happens again.

### 2026-08-30 — Torso Masterwork pass

- Tagged all 103 Masterwork items with an **Archetype** reference
  column, and recorded the equipment slot-design philosophy (Torso =
  protection, Neck = boring passive utility, Ring = active ability,
  etc.) as a standing rule.
- Recorded **War Magic** (T120) as a damage-baseline reference
  (Level 2-4 builds) to sanity-check Resist items against real hits.
- Trimmed the Torso flat-Resist cluster: cut **Attuned Shroud**
  (duplicate of Elemental-Resistant Armor), reworked **Robes of the
  Elemental Lord** into the Level 5 capstone (+3, up from +2).
- Fixed the stale **"Bodily Defense"** term to **"Vital Defense"**
  everywhere it was still live (items.csv, convert.py, index.html).
- Cut **Periapt of Constitutional Integrity** (Neck), a duplicate of
  Armor of Constitutional Integrity (Torso); widened the survivor's
  trigger to "Poison, Disease, or similar bodily threat."
- Priced **Lifeforce Plate** (refills Protected when you're at 0),
  **Coat of Knit Flesh** (reworked into a once-per-day Bleeding
  prevention, which also exposed and fixed a stale Bleeding glossary
  rule), and **Dauntless Wrap** (Protected on the hit that would Down
  you, discounted for how rarely that actually comes up).

### 2026-08-29 — Buff-Potion cluster finished, Ward redesigned

- **Good Luck**'s value corrected (2.2→2.4, crediting both cards in a
  Good Luck flip toward the Suit Pool); **Energizing Brew** and
  **Essential Ointment** simplified and lost their AP costs.
- Four new buff Potions rounding out Levels 1-4: **Windrunner's
  Draught**, **Thornskin Elixir**, **Spellblade's Sipper** (see Ward
  below), **Fatebinder's Cordial**.
- Fixed a **Fleeting** timing bug where a freshly-granted effect
  immediately lost a stack to that same turn's decay.
- **Swiftblade Vial** reworked (Hasted eight times, turn-order
  adjustment by up to 3, Good Luck handed fully to Fatebinder's
  Cordial); turn-order adjustment given its first real value.
- **Ward** redesigned: flat +2 Resist plus a self-limiting typed-
  Protected absorption charge per stack. Fixed **Elemental-Attuned
  Tincture** and rebalanced **Spellblade's Sipper** (renamed from
  Warmage's Draft) around the stronger Ward.
- **Insanity Potion** finalized: sustained Bleeding on hit/Parry
  instead of a stale "treat any card as a Heart" clause.
- **Vulnerability, Harrying, and Psychosis Poison** bumped to twice
  their Potency, closing the last real gaps in the Poison lineup.
- Added an **Archetype** reference column (Potions/Grenades/Poisons/
  Food) for informal balance groupings.

### 2026-08-27 — Grenade and Potion families rebalanced

- **Healing-item family** restructured into a clean Level 1-4 ladder
  (Fortifying Concoction, Healing Potion, Calming Brew/Kiss of the
  Earth/Predator's Cry, Revivification Draught); Level 5 left open for
  a future capstone.
- **Oozejar** added (Level 4, debuff-only Grenade); fixed an AoE
  debuff-pricing bug affecting non-linear debuffs on multi-target items
  (balance-model only, no player-facing number changes).
- Two new Grenades: **Legbreaker** (Push) and **Harrowing Ichor**
  (Frightened).
- **Prevention Potions** (Calming Brew, Kiss of the Earth, Predator's
  Cry) no longer cost AP, now also clear existing stacks of what they
  prevent, and settled into a Level 3-4 spread.
- **Grenades rebalanced**: several damage bumps, suit-based scaling
  added to every debuff-granting Grenade, Quartz Tincture renamed
  Reeler, Hellfire Bomb/Thunderclap-in-a-Jar's AoE math corrected.
- **Refund-Potion family** reshuffled (Soldier's Salts to Level 1,
  Fighter's Friend to Level 3) and a new **Battlemaster's Brew**
  (Level 4) added.

### 2026-08-26 — Ward's Resist bonus doubled

- Fire/Frost/Brilliant/Shadow Ward now grants **+2 Resist** against its
  specified damage type while any stacks remain (up from +1). Surfaced
  during a balance audit that found Ward underpriced relative to Resist;
  a per-stack scaling version (like Hasted's +1 Speed/stack) was
  considered and rejected since Resist has no upper bound, and letting
  Ward stack toward it would risk a character becoming immune to a
  damage type mid-fight — doubling the flat bonus keeps that ceiling in
  place while making a single application meaningfully stronger.

### 2026-08-25 — Unified crafting recipes onto one Materials formula

- Crafting recipes used to come in two incompatible shapes — a fixed
  Primary/Leeway slot count for Weapons/Armor/Tools, and a Gold-price-
  derived Total/Base/Extra Materials formula for Masterwork/Alchemy/
  Potions/Poisons/Grenades/Food — and the rulebook only ever documented
  the second one, so it never actually explained how the majority of
  real recipes worked. Replaced both with a single rule: every recipe
  states its own Total Materials directly, at least half must be a Main
  Type, up to half can be an Optional Type instead.
- Restored the original numbers from the project's original design
  document (now archived at `archive/flagonquest_content_original.docx`
  for reference): Masterwork a flat 20 materials at the item's own
  Level, Alchemy and Food a flat 2, Weapons/Armor/Tools mirroring their
  own Gold Cost directly (they're Level 1 by default).
- Masterwork items now name only their own Main Type — their Optional
  Type comes from whichever base item is chosen at craft time, so the
  same enhancement works whether it's built onto a Metal sword or a
  Wood bow without needing to state every possible material by hand.
  The Crafting tab's base-item picker went from a reference-only
  preview to something that actually feeds into the materials check.
- If you already own a suitable item to enhance, you can skip gathering
  its Optional-Type materials and enhance that item directly instead of
  crafting a fresh one just to sacrifice into the enhancement.

### 2026-08-23 – 2026-08-24 — Social Contests and Exploration reworked

- **Social Contests** are no longer a separate team-check subsystem with
  Concessions, front/back positioning, and Charismatic/Strategic
  statement types — a social contest is now just an extended check like
  any other, with a new fixed Defense mapping (Persuasion targets
  Instinct Defense; Presence and Rapport both target Mental Defense).
  **Pressure** replaces Concessions: a GM-tracked value representing
  circumstances stacking against the party, applied as Bad Luck on
  Statements equal to its current total.
- **Traveling and Exploration** rewritten around **Legs of a Journey** —
  one action and one check per character per leg, no retries. New
  **Scout** and **Search** actions, and a new **Pushing the Pace**
  option (the whole party trades away their leg actions to cover more
  ground, at the cost of no roll to avoid a brewing complication).
  `Move` dropped as a discrete action, since it only existed to be
  AP-gated under the old rules.
- **Food and Exhaustion** moved out of Exploration into its own section
  under Health and Resources — it was never actually wilderness-
  specific (1 Food item covers a day regardless of where the party is),
  just nested somewhere that implied it was.

### 2026-08-19 — Hand-editable printed Character Sheet

- Printed Stats & Skills now show filled/empty dots (●●●○○) instead of
  a plain number — raising a Stat or Skill later just means filling in
  one more dot with a pen, instead of erasing and rewriting a digit.
- Printed Derived Stats (Speed, the five Defenses, the five Resists,
  Reflex, Cards Per Day, Resting Health) and the Skill Total badge now
  print in a light gray, thin weight instead of solid black — since
  those are computed from Stats & Skills, a pencil correction after
  raising a dot reads clearly against the faint original instead of
  fighting a bold printed digit for the same visual weight. Screen
  view is unaffected either way — both are print-only.

### 2026-08-19 — Mobile design tokens, print fix, Choice Effects fix

- Mobile gets its own small set of design tokens now (separate from,
  but matching, the desktop text sizes) — the foundation for handling
  mobile-specific layout going forward, since this is a tabletop
  companion app a lot of players run from a phone at the table, not
  just a smaller desktop. The two-column Stats & Skills grid added
  earlier today is the first thing built against it, and its own
  numbers were tightened a bit further as part of that.
- Fixed the Character Sheet's Health/Fullness/Hunger Debt trackers
  clipping when printed — the heart/food/bone icons don't render
  reliably across print engines. A printed sheet now shows the current
  number plus a row of blank boxes to check off by hand instead.
- A technique with per-copy options (like Profession) no longer shows
  every possible option on the Character Sheet just because one copy
  hasn't had its option picked yet — the Sheet now only ever shows
  what's actually been chosen. The Builder still shows the full list
  while a pick is pending, since that's still useful there for
  comparing options.
- Techniques with Choice Effects data (like Profession) no longer show
  a redundant "Copy 1: Sailor" line under the effect text on the
  Character Sheet — the effect text already says what was picked.
  Techniques whose choice doesn't carry its own effect text (like
  Artisanal Training's School) still show that line, since it's the
  only record of the pick.

### 2026-08-19 — Two-column stat grid on wider phones; small UI polish

- The Character Sheet's Stats & Skills grid can now show two boxes per
  row on a wide-enough phone or phablet instead of always stacking one
  per row — the read-only view doesn't need the extra width the
  editable Builder version's steppers do, so it can afford to fit more.
  It self-adjusts to whatever actually fits rather than a fixed
  breakpoint, so a narrower phone still gets the familiar single column
  instead of anything overflowing or a skill name getting squeezed.
- A custom material's "Level" label no longer sits next to its own
  "Lv N" badge once it's collapsed — that was saying the same thing
  twice; it still shows while actively editing, next to the bare
  +/− stepper, where it's the only thing saying what the number means.
- A custom material's Edit and Done buttons are now one toggle in a
  fixed spot (bottom-left) instead of Edit sitting in the header right
  next to the delete (✕) button and Done appearing across the tile in
  the opposite corner once editing started.

### 2026-08-18 — Bigger, more consistent text; small mobile bump

- Bumped the site's base text sizes up a notch across the board —
  Effects/Special/Fluff text, buttons, notes, labels — since everything
  read a bit small, especially on a phone.
- Stat numbers now stand out more: Skill Total's glowing badge, the
  Derived Stats numbers (Speed, Defenses, Resists, ...), and every
  technique/item/background/material's own name are all a consistent,
  more prominent size now, instead of each having drifted to its own
  slightly-different one over time.
- Tags and Relevant Skills chips (the quick-glance rules info on a
  technique's card) are bigger and a bit bolder too, so they read as
  the "important, scannable" info they are instead of blending into
  the background.
- Unified two spots that showed the same "big bold XP total" number at
  different sizes depending on which tab you were on.
- On top of all that, narrow screens (phones) now get one more small
  proportional bump, so mobile reads noticeably easier without needing
  a completely separate mobile layout.
- Same idea for colors, not just text: the card/box background+border
  look used everywhere (technique/item/background cards, Stats & Skills
  and Derived Stats blocks, XP tiles, both full-screen modals) and the
  amber "granted bonus" badge look (an item's flat stat bonus, a
  material's type tags) had each been retyped by hand at a dozen-plus
  spots, occasionally drifting slightly. Pulled into shared constants
  so they can't drift apart again — no visual change, just one
  definition instead of many.

### 2026-08-18 — Fullness tracker

- **Fullness** (Goblin Game) now has its own tracker on the Character
  Sheet, right next to Health — 🍖/🍽️ pips instead of hearts, only shown
  when the Goblin Game supplement is enabled, with a small divider on
  the pip row itself marking where Too Full starts. Spacious Gut and
  Gorger correctly raise the max (15 → 20 → 25) and, for Spacious Gut,
  the Too Full threshold (10 → 15) too, with a "Too Full" badge (Bad
  Luck on Reflex/Awareness) when you're over it. Fullness can also go
  negative from missing meals — a "Hunger Debt" pip row below tracks
  that down to -30 (in steps of 5, so it stays a handful of clickable
  icons instead of thirty), with its own divider and "Starving" badge
  at -10.

### 2026-08-17 — Choice-based prereqs, Grants Technique

- **Artisanal Training** and **Profession** now use a real dropdown to
  pick their School/Profession when you learn them, instead of a plain
  free-text note — the same mechanism as Soulblade's weapon-type picker.
  Artisanal Training's prereq badge now correctly checks Craft/Mixology/
  Survival based on which School you picked, instead of showing no
  badge at all.
- **Profession**'s full original text — each of the ten options'
  specific Good Luck benefit and prereq (Apothecary, Artisan, Busker,
  Fisher, Gatherer, Grifter, Merchant, Sailor, Tactician, Theologian) —
  had gone missing from the data at some point; restored it, and wired
  up its prereq badge the same way as Artisanal Training's. Several
  options (Apothecary, Artisan, Fisher, Merchant, Sailor) need more than
  one skill at once, which needed a small extension to the Prereq Check
  syntax to express.
- **Profession**'s and (going forward) any similar technique's card now
  narrows down to just the option(s) you've actually picked instead of
  always showing the full list — pick Apothecary and only its benefit
  and prereq show, learn a second copy for Sailor too and both show,
  side by side — but that list reappears in full while any copy is
  still sitting on its default "Choose a ___…" (e.g. adding a second
  copy), so there's always a way to compare the remaining options
  instead of them vanishing the moment the first copy is picked. The
  old catch-all "Building" column (Feature-built
  techniques' behind-the-scenes build instructions) has been renamed to
  the more general "Builder Notes" and picked up a short explainer on
  Profession/Artisanal Training's cards about how this narrowing works.
  Profession's "each time you learn this, choose one of the following"
  line moved into that same Builder Notes explainer, so the read-only
  Character Sheet — where the choice is already made — no longer shows
  a leftover "choose one of the following" ahead of the one option you
  actually picked.
- **Extensive Background** now has its own dropdown to pick an
  additional Background you qualify for, and correctly shows a green
  "Prereqs: None — ✓ Met" badge instead of no badge. The extra
  Background you pick shows up on the Character Sheet alongside your
  normal two.
- **Creator** and **Professional** backgrounds now automatically grant
  you Artisanal Training / Profession the moment you select them — free
  of XP, with their own School/Profession dropdown, but not manually
  removable (deselect the background to remove the granted technique
  instead). The Builder's XP totals, and single-character Export/
  Import, correctly treat these as free and don't double them up.

### 2026-08-17 — Prereq summary panel, share-link cleanup

- The Builder's prereq summary panel is now labeled "Prereq Checker."
- The URL no longer mirrors the current build in a `#build=...` hash
  during normal use — that only ever served refresh persistence, which
  character slots/localStorage already handle.
- Share links are now much shorter (a typical build's link is roughly a
  third of its old length) — same data, just packed more efficiently
  instead of as a quoted-key JSON object. Older links still open fine.
- Added a **"Show QR code"** button next to Copy share link — pops up
  the current build's share link as a scannable code, so someone else
  at the table can open it on their phone without typing a URL.
- "Copy share link" no longer puts the link in the address bar either —
  it only ever copies to the clipboard now (falling back to a native
  copy-this-text prompt if that's blocked).
- **Character switching overhauled**: the header's character dropdown
  plus separate "+ New"/"Duplicate" buttons are now one "Manage
  Characters" button that opens a list of every character with
  Switch/Duplicate/Delete on each, drag-to-reorder, and a "New
  Character" row at the end of the list. Also removed "Clear build"
  from the Builder tab — Delete (or just starting a new character)
  covers that now.
- The Rulebook/Glossary header's Techniques link now says `?tab=
  techniques` when you hover it, matching the tab's actual name
  (it used to read `?tab=browse`, an old internal name). The `?tab=`
  query string also disappears from the address bar right after it
  lands you on the right tab, instead of sitting there — stale — once
  you switch to a different one.
- **Builder tab tidy-up**: Export/Import/Share/QR code are now a small
  button grid to the right of the Character name/Concept fields
  (wrapping below them on narrow screens) instead of a full-width row
  underneath. Backup/Restore all characters, and the localStorage
  warning note, moved into the Manage Characters overlay — they act on
  every character in the browser, not just the one open here. The
  Sources header is bolder and brighter than its neighbors now, since
  it's the one section that starts collapsed.
- Fixed wrapped header/Builder-row elements landing off-center on
  narrow-but-not-mobile screens (roughly 500-900px) — a real
  double-checked layout issue, not just an eyeballing quirk: two items
  sharing a line and then centered as a *pair* still reads as lopsided
  when one of them (the page title) is a much wider box than its
  visible text. Each piece now gets its own row below the breakpoint
  where they'd otherwise unevenly pair up.
- Code cleanup pass after this stretch of changes: pulled the QR/
  Manage-Characters overlays' identical backdrop, Escape-key handling,
  and × button styling into shared helpers instead of two copies drifting
  apart, and swept for dead code/stale docs left over from the changes
  above. No visible behavior change.

### 2026-08-14 — Rulebook cleanup, material pricing

- Removed Jokers from the rulebook — the deck is now a standard 52-card
  deck throughout.
- Materials are now priced at their Level in Gold instead of a flat 1
  Gold regardless of grade.
- Formatting pass on the Rulebook: parallel-sentence clusters bulleted,
  worked examples italicized/indented.
- Header brand and tab nav stay centered on mobile once wrapped.
- **Crafting browser overhaul**: one row per item with a School picker
  instead of a duplicate row per School; recipes gained a Kind switch
  (Slots or Value) so generic fallback recipes now cover Potions,
  Poisons, Grenades, Food, and un-authored Masterwork items; Masterwork
  base-item choices get a real picker; Artisanal Training can grant
  School training; filters are now independent checkboxes/chips.
- Two new Goblin Game techniques, **Spacious Gut** and **Gorger**
  (raise max Fullness, change what happens when Too Full; Gorger
  requires Spacious Gut). Techniques gained a **Supplement** column,
  gated by Sources like items/backgrounds already were.
- **Goblin Game Food System**: new Rulebook chapter on Fullness, daily
  food needs, **Too Full**, the five Food Material varieties, and the
  Meal recipe. Rulebook/Glossary chapters can now be supplement-tagged
  and filtered via a tab row when more than one supplement exists.
- More Goblin Game content from the full player doc: Goblin Traits,
  Gems, **Bingus**/**Golden Bingus**, The Great Game, Deeds — added to
  the Glossary where relevant.
- Rulebook/Glossary header links navigate in place instead of opening a
  new tab.
- Techniques gained an **Excluded By** column for when a different
  enabled supplement makes a technique nonsensical — hides Pranic
  Nourishment and Land's Bounty and swaps in a Goblin Game version of
  Street Runner once Goblin Game is enabled.
- Header is pinned again on desktop at the compact single-row width;
  still scrolls away normally on narrower/wrapped layouts.
- Exported files are named after their contents (`<character
  name>-<date>.json`, `FlagonQuest-export-<date>.json`) instead of
  generic filenames.
- Land's Bounty's Difficult Terrain now scales with Mind ("up to
  [Mind] levels") instead of a flat single level.
- **Supporting** now has real rules: a flat difficulty 11 check that
  grants Good Luck on success, moved next to Skill Checks and Gambling.
- Character Creation moved to the end of the Rulebook's chapter list.
- Standardized repeated-count phrasing ("twice"/"thrice"/"four times")
  across the Rulebook, techniques, items, and features.
- Food-created items now spoil a week after being made, matching raw
  Food materials (previously just a day).
- **Site-wide consistency pass**: fixed a glossary tooltip bug with
  multi-paragraph entries, a broken Travel Rations price, several
  unfinished Rulebook sentences, and straight quotes/apostrophes
  standardized to curly; deduped a few copy-pasted style helpers in
  the code with no visible effect.
- **Consistency pass, round two**: split out **Basic Travel Ration** as
  a plain store-bought Pack/Gear item, distinct from the craftable
  Food-category version; rewrote Rapport's blurb ahead of the Social
  rework; unified `Relevant Skills`/`relevant_skills` naming across
  techniques and items; split `backgrounds.csv`/`features.csv` into
  `Description (Fluff)`/`Effects` columns; filled in three stub
  Rulebook spots; renamed Character Creation's opening section to
  "Building a Character."
- **Automatic prereq checking**: techniques with a machine-checkable
  `Prereq Check` show a red/green "✓ Met"/"✗ Not met" badge on their
  Prereqs line while browsing, evaluated against the current build
  (140 of 143 techniques; the rest stay plain text where the syntax
  can't express them).
- **Fixed a live bug**: the Feature-builder (Battle Maneuver, War
  Magic, Healing Magic, Spirit Blessing, Social Maneuver) was silently
  ignoring its own point budgets after its prose-scraping fallback
  broke; now driven by a real `Feature Budget` data column instead.
- Rulebook/Glossary header nav can jump straight to a specific Builder
  tab (`index.html?tab=items`, etc.) instead of always landing on the
  Character Sheet.
- **Artisanal Training and Soulblade get real pickers**: School and
  weapon type are now dropdowns instead of free text.
- **Builder prereq summary panel**: a new panel between the XP tracker
  and Stats & Skills grid lists every Skill/Stat/Technique the current
  build requires, collapsed to the highest threshold, with the same
  red/green Met badge as the per-technique Prereq Check line.

### 2026-08-11 — Crafting materials framework

- New **Material** item category for crafting resources, tagged with one
  or more Material Types (Metal, Wood, Fire, and so on) — seeded a
  starter catalog of the 12 canonical Types.
- **Custom materials**: a lightweight builder (name, Level, toggle any
  number of Types) for GM-granted special materials that aren't in the
  data file, e.g. one that's both Metal and Fire.
- Materials get their own section on the Items tab and Character Sheet,
  separate from the gear grid.
- **Crafting browser** (draft): a collapsible section on the Items tab
  listing every item with a resolvable recipe, showing whether the
  current character is trained/skilled enough and has the materials for
  it, with a filter for either or both. Recipes now explicitly declare
  which items they cover (`crafting_recipes.csv`'s new "Applies To"
  column) instead of relying on eyeballing text, and Masterwork items'
  base-item requirement (if any) is shown for reference. No craft action
  yet — this is the eligibility browser, not the spend-materials step.
- Weapons/Armor/Tools recipes rebuilt around fixed **Primary/Leeway
  material slots** (e.g. 2 Metal + 1 Cloth/Leather) instead of the
  Gold-derived Base/Extra percentage split, with a separate recipe row
  per crafting School (Carving vs. Smithing, etc.) so the browser shows
  each way to make an item on its own line. Masterwork/Alchemy items
  keep the original Gold-value formula, since materials being worth
  their Level in Gold is what lets that side scale without hand-authored
  recipes.
- Items tab: **Keyword** and **Supplement** filters are checkbox
  multi-selects now, so you can show e.g. both Base Game and Goblin Game
  at once instead of picking one at a time; the custom item and material
  builders moved to sit side by side under the search bar, above the
  inventory grid.
- Catalog materials now carry a **Level** (1–5), editable per stack —
  picking a different Level splits a unit off into its own stack instead
  of reclassifying the whole pile, so you can hold e.g. both Level 1 and
  Level 3 Metal at once; crafting eligibility checks each stack's Level
  against the item being made.
- Custom material builder reworked to match the buildable-technique
  pattern: a fresh one opens straight into the name/Level/Type form, and
  "Done" collapses it down to look like a stock material tile (name, Lv
  badge, only the Types you turned on) — "Edit" reopens the form. Also
  fixes the name field clipping outside the tile.

### 2026-08-04 — Health tracking

- Character Sheet's Health box now tracks current Shallow/Deep Health, not
  just the max: a heart-pip readout you can click directly, plus a
  −/+ stepper for one-at-a-time changes.
- Hitting 0 Shallow Health auto-flags **Wounded**: a badge on the Health
  box, an automatic −2 applied to Speed and all five Defenses (called out
  in red on each), and a reminder to also apply Bad Luck to flips by hand.

### 2026-08-03 — Character management, flavor text, content sources

- **Duplicate** a character into a new slot; **Backup/Restore all**
  characters at once (everything lives in browser storage only, so this is
  the only way to back up more than one at a time).
- Removing a technique or item now shows a brief "Removed X — Undo" toast.
- Restored the full original flavor text for 66 techniques that had been
  condensed down to a single line somewhere before this repo's history —
  cross-checked against the source content document.
- **Sources** panel on the Builder tab: toggle which supplements (Base
  Game, Goblin Game) show up when picking new content, without touching
  anything already in a build.
- Un-stuck the header bar (scrolls away normally instead of staying
  pinned); Rulebook/Glossary nav links now wrap together as a pair.

### 2026-08-02 — Goblin Game content, combat math, item filters

- 14 new Goblin Game clan Backgrounds (Bloody Banner, Rockbiters,
  Black-Ear, Dampfoot, Firebug, Fardown, Troll-Food); Backgrounds and
  Techniques sections are drag-reorderable on the Character Sheet.
- Advanced filters on the Items tab (Slot, keyword, Supplement);
  Techniques default-sorted by Level then name.
- Permanent max-Health bonuses from techniques (Toughened Body/Resolve/
  Spirit) now flow through to the sheet automatically.
- Accuracy/Defenses/Reflex consistently use Skill **Total** (stat + skill
  points), not just the raw skill value; Unarmed requires a free hand.
- Custom weapon builder for freeform items; Goblin Game firearms and bomb
  variants added.
- Auto-calculated Parry Defense and weapon damage; dual-mode Thrown
  weapons (melee + thrown stats together); drag-reorder inventory.
- Masterwork base-item picker with per-level pricing; custom items with
  their own stats and stacked powers.

### 2026-08-01 — Items, Backgrounds, multiple characters

- Items and Backgrounds pickers added, with equip/parry tracking.
- Character **slots** — the browser can hold more than one character, with
  a switcher in the header.
- Print layout overhaul: compact header box, pinned footer, alternating
  row shading that actually survives most browsers' print settings.

### 2026-07-29 – 2026-07-31 — Foundation

- Initial build-out: technique browser and search, the Builder/Character
  Sheet split, Stats & Skills point-buy with XP budget, Feature-built
  techniques (Battle Maneuvers, Spells, etc.) with their point budgets,
  share links, the Rulebook and Glossary pages, and the site's branding
  and print styling.
