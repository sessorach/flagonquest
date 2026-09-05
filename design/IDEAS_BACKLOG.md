# Ideas backlog

Loose ideas for items, abilities, and other content that came up during
design/balance sessions but weren't acted on immediately — a holding pen,
not a commitment. Move an idea out of this file (delete it here) once
it's actually been drafted into `items.csv`/`techniques.csv` and given a
real writeup in `RULES_DESIGN.md`/`balance_weights_notes.md`; don't leave
a stale duplicate sitting in both places.

## Source material to mine: the dice game's item list

A large batch of items from a separate dice-based tabletop game (its own
Mana/Range-in-spaces/dice-damage system, not this game's AP/meters/card-
flip one) was handed over as inspiration for FlagonQuest items across any
slot — real per-item translation work, not reskinning, since the
underlying mechanics don't map 1:1. Full source list, organized by what
they'd likely translate as once someone sits down with a specific one:

**Consumables** (candidates for Potion/Grenade/Poison, or a Food-adjacent
category): Blade Poison, Blink Potion, Bottled Sunlight, Elixir of Might,
Lucky Coin, Goop Jar, Grave Jar, Healing Potion, Hero's Potion, Mana
Potion (no direct Mana-analogue in this game — would need reframing
around AP/cards/a resource this game actually has), Shockwave Jar, Tile
of Escape, Deadly Poison (+), Earthen Potion (+), Elixir of Precision
(+), Inferno Jar (+), Restoration Potion (+).

**Permanent Consumes**: Tome of Mana Bolt (would need a real spell-
granting mechanic analogue).

**Charms** (likely Ring or Neck candidates — small always-available
triggered effects): Blink Charm, Charm of Ambition, Deflecting Charm,
Gambler's Charm, Goading Charm, Hunter's Handbook, Pillar Talisman,
Repelling Charm, Restoring Charm, Ring of Comets, Ring of the Skull Oath,
Shielding Charm, Thug's Shiv, Thunderstone Bracelet, Weighted Pommel,
Wizard's Earring, Crab Demon Figurine (+), Dryad's Mantle (+), Lifeforce
Shard (+), Regrowth Amulet (+), Shockwave Talisman (+), Vampire's Fang
(+), Venomstone Pendant (+).

**Equipment** (Feet/Held/Torso/Belt candidates mostly, a few Head-shaped
by name but combat-mechanical rather than mental/vision — see the Head
slot note below): Belt of Stanching, Berserker's Helmet, Blazing Boots,
Coward's Shoes, Cursed Mask, Dark Sash, Eagle Claw Bracer, Earthen
Girdle, Flask of the Moon, Flask of the Sun, Gauntlets of Wrath,
Gladiator's Crown, Hermit's Pouch, Lodestone Bracers, Orb of Purity,
Ranger's Bracers, Sandals of Travel, Sanguine Illusionist's Mantle,
[Type]slayer (+), Cape of Needles (+), Cloak of Shifting Sand (+),
Fortress Shield (+), Leyline Orb (+), Sundering Sledge (+), Zephyr
Greaves (+).

Note on the Head-shaped ones specifically (Berserker's Helmet,
Gladiator's Crown, Cursed Mask): these are combat-attack modifiers
(reroll-and-keep mechanics, bonus damage against a prior target), not
mental/vision effects — Head's established lane (`RULES_DESIGN.md:129`).
They'd need real reflavoring to fit this slot rather than a straight
port. Cursed Mask's "choose an enemy, you both reroll certain results"
has a genuine mental/curse-link angle that could become a symmetric
Good-Luck/Bad-Luck effect on wearer and target. Hunter's Handbook's
"learn a fact about an enemy, gain a bonus" has a nice knowledge/analysis
hook, though the attack-bonus half reads more Ring-lane than Head-lane.

## Head slot — candidates not yet drafted

Surfaced while reviewing the existing Head slot Masterwork items against
its established "mental, vision" design lane (`RULES_DESIGN.md:129`):

- **True-seeing lenses/spectacles** — pierces illusions, disguises,
  invisibility specifically, distinct from Mask of Night's darkness-only
  fix. Fills a real gap: nothing in the slot currently handles "vision
  beyond darkness."
- **Circlet of clarity** — resistance to Charm/domination/mind-control-
  style effects. Fills a gap on the mental side: nothing currently
  covers this axis, as distinct from Taunted/Frightened (Cowl of
  Tranquility) or social-Skill buffs (the four Skill hats).
- **Comprehend languages circlet** — understand any spoken/written
  language. Purely mental/utility, untouched so far.
- **Third Eye / detect-magic lens** — see magical auras, identify
  enchanted items/effects at a glance. A different vision-flavored
  knowledge tool than either existing vision item.

## Crown of Glory — capstone redesign, deferred

Original mechanic (once/day, wearer + up to 4 allies each draw a card)
set aside rather than rebalanced — see `balance_weights_notes.md`. Not
just a Level-scaling problem (a "wearer + up to 2×Level allies" formula
fit the numbers cleanly); the real concern is that generic party-wide
card generation doesn't fit Head's "mental, vision" lane at all and
reads more like a capstone-tier effect. Revisit once the rest of the
equipment slots have had a first pass — figure out what a genuinely
capstone-appropriate Head effect looks like, rather than patching the
current mechanic's Level or scaling formula.

## Neck slot — reserved flavor

**Stoic Skullcap**'s name and fluff ("these caps provide the wearer a
sense of calm and clarity when dealing with others, a feeling that
intensifies the more another tries to menace or win them over with raw
charisma") were retired from the Head slot's social-hat consolidation
(see `balance_weights_notes.md`) specifically to be reused for a future
**Neck**-slot item dealing with Pressure directly, once the Neck slot
gets its own pass — matches Neck's "niche, boring, passive utility"
lane (`RULES_DESIGN.md:129`) better than an offensive Skill-buff family
did anyway.

## Alcohol-cost Technique suite

A planned suite of Techniques that use Alcohol as an additional cost,
prompted by revisiting Wizardly Hat of Tam the Tipsy. Real anchors
established while pricing that item, worth reusing when this suite gets
drafted: `Gold = 1.5` raw Value (Locked, `balance_weights.csv`), so
Alcohol's own Value by Level is `1.5 × Level` (1.5, 3.0, 4.5, 6.0, 7.5
for Levels 1-5); and the working (unverified) assumption that a Level-N
Technique effect is worth about the same `Level × 3` a same-Level item
would be. See the Wizardly Hat writeup in `balance_weights_notes.md` for
the full accounting, including why a 2 AP activation cost read as a net
loss at low Levels and why 0 AP reads much better.
