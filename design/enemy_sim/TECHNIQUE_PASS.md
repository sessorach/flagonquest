# The broad pass: every Technique and Feature (2026-10-28)

A shallow test of everything the sim plays, to see how well it can tell
what a Technique or Feature is worth. Every modeled Technique went on up
to three Level 3 sample characters, and every Feature of the four
Buildables went into one of a host's own copies. `technique_pass.py`
runs it (about 20 minutes on four cores); the numbers are in
`technique_pass.csv`.

The short version:

- **Each reading is precise and repeats.** Run again on a fresh set of
  fights, 30 Techniques came back with a correlation of 0.98, every
  difference inside its margin, and no sign flipped.
- **What a Technique is worth depends a lot on who has it.** Two hosts
  for the same Technique agree only loosely (0.41 for non-Styles).
  Mostly that's real: an Unarmed Style on a swordsman, a gap-closer on a
  back-liner.
- **One sim rule was swamping Health-changing Techniques.** Assassin
  enemies went for the lowest current Health, so at full Health they all
  picked whoever was first in the party list, and a point off one PC's
  max Health (Grim Resolve) sent every Assassin at that PC instead. Felix
  with Grim Resolve read +7.5; it's +1.6 with the tie broken properly.
  The pass uses the fixed reading; it's a switch, not the default yet
  (see "Your call" below).
- **XP cost barely predicts value** (correlation 0.24). Most Techniques
  (64 of 116) stay within half a point of Health even on their best
  host; 49 clear +0.5 somewhere; 3 are below -0.5 everywhere.
- **Some standouts:** Warmage's Reserves, Toughened Resolve, Lifeline and
  Brace pay well for their XP. Sanguine on its own costs a caster's
  party 6.6 Health a fight. Feint still never pays.

## How it was run

- **Parties and fights**: Level 3, each host in its own party (S: Enith,
  Felix, Jackal, Hanforth; U: Browndog, Ashleigh, Sable, Beornhard; H:
  Hilde, Carrick, Hanforth, Beornhard), the four Level 3 encounter
  mixes, enemy Health x1.75 so fights run about five rounds, 200 fights a
  mix (800 a reading). Scored as compare_builds does: the party's Health
  left in points (losses 0), paired fight by fight on the same seeds.
  Margins are 95%.
- **Hosts**: anyone who already knows the Technique (the test takes it
  off), then the two who need the fewest prereq ranks for it, no more
  than 6 XP of them (`party.fit`). A host whose build won't load with it
  is skipped (an Unarmed Technique needs an Unarmed row). Six Techniques
  found no host: Solemn Perseverance, Solemn Covenant, Pressure Point
  Revitalization, The Gatekeeper, Slithering Hands (Brawl 5 and Insight 4)
  and The Grizzly Awakens.
- **Two readings**: "free" (the Technique on top, with any prereq ranks
  it needs) and "swap" (the XP evened out in Defense and side Skill
  ranks, `party.DONORS`, so the build's total doesn't change). Both are
  in the CSV; the tables below use "free".
- **Styles**: you're only in one, so a Style replaces the host's own. The
  tables give it against no Style at all: the reading plus what the
  replaced Style was worth to that host when taken off.
- **Features**: one Feature in one of the host's own copies at a fixed
  Level, against the same copy without it, so no XP changes hands. One
  copy of it, and three when it's a 1-point Feature with no cap.
  Battle Maneuver goes in place of a plain copy (the host's opening
  Maneuver), War Magic on a Lance copy, Healing Magic on a plain copy.
  Spirit Blessing is traded for a point of Shielding instead: an empty
  Blessing still gets cast, and moved which Blessing Hanforth cast when.
- **Fires a fight**: log lines naming it, so a passive that changes
  numbers (a Defense, a Health bonus) shows 0 even when it works.

Two mistakes of mine, caught before this write-up: the first full run had
every Feature's sign backwards (base minus variant), and the 20-fight
smoke test was too noisy to read. Both are fixed; the Feature numbers
were checked by hand against fresh runs.

## New in the sim for this

- **Interrupts on an enemy's attack** (`hooks.py`): `attack_targeting`
  before its flip (move it onto another PC, call it off, or change the
  Defense it checks) and `attack_flipped` after the flip, before it hits
  or misses. With them: Swatting Paw, Arrow Finds Only Mist, Slithering
  Hands, Lend Bulwark and Seasons Pass the Forest. Turn the Tables still
  needs PC grapples. When to spend each is my rule, in
  TABLE_PLAY_NOTES.md's "Attack Interrupts".
- **Storm of Blades**, for a striker with a one-handed weapon in each
  hand (your offer). Repeating a plain swing is the same as a second
  swing, so it only pays when it repeats a Maneuver or a Technique strike;
  it changed little on any host (+0.1 at best).
- **`party.fit`**: XP-matched swaps with prereq checks, which the pass
  uses for every host.
- Coverage is 126 of 205 modeled, 44 out of combat, 35 deferred.

## How well the sim can tell

**Repeatability.** 30 Techniques at random (68 host readings) rerun on a
different 800 fights: correlation 0.98, every difference within the
combined margins, and all 29 readings bigger than ±0.3 kept their sign.
The median margin is ±0.3 Health. So at this depth a reading is a fact
about that host in that party.

**Across hosts.** Two hosts for the same Technique correlate 0.28 (0.41
for non-Styles), up from 0.02 and 0.08 before the Assassin fix. What's
left is mostly fit: Spirit Hands is +2.7 on Felix and 0 on Hanforth
(his weapon isn't Unarmed), Feint is -0.2 to -1.4 depending on who
follows up, Lifeline is +3.0 on the healer and 0 on Jackal. A Technique's
value is a property of the Technique and the character together.

**The Assassin tie.** Every Level 3 mix has two to four enemies with the
Assassin tactic, which reads "go for whoever's already hurt worst". The
sim took that as the least current Health, so at the start of a fight
(nearly everyone on 10) the tie went to whoever was listed first:
Enith in Party S. Anything that took a point off another PC's max Health
moved every Assassin onto that PC. Felix's party scored +6.4 with Felix
on 9 Health instead of 10, and +0.3 on 11. `tunables.ASSASSIN_READS =
'hurt'` reads the share of Health lost instead, with ties going to the
squishiest-looking and then chance: Felix on 9, 10 and 11 then score
within noise of each other. Readings that moved most: Grim Resolve,
Toughened Resolve, Raise Spirits, Dread Reputation, Lifeline. The rest
of the catalog barely moved (0.89 between the two runs).
`technique_pass_current.csv` has the pass under the current default.

**Yardsticks.** What plain ranks buy each host, in the same units:

| On each host | Health left | XP |
|---|---|---|
| +1 rank of the main attack Skill | +0.3 to +1.5 (Jackal +1.5, Carrick +1.2, Hilde +1.0) | 5-6 |
| +1 rank of Resilience | +0.0 to +0.5 | 3-5 |
| +1 max Health | +0.7 to +4.8 (Carrick +4.8, Jackal +3.0, Hanforth +1.8) | - |

So a rank buys roughly 0.05 to 0.25 Health per XP, and anything that
keeps Carrick or Jackal standing pays more than anything else.

**XP cost.** Across 116 Techniques, Level (XP cost) correlates 0.24 with
the average value and 0.09 with the best host's. Average value per XP by
Level: Level 1 -0.01, Level 2 +0.05, Level 3 +0.07, Level 4 +0.03.

## Techniques

"Best host per XP" is the best host's reading divided by the
Technique's XP (three times its Level); "(has it)" means the reading is
that host's own copy taken off.

### The most for their XP (not Styles)

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Warmage's Reserves | 2 | +1.28 | Beornhard (has it) +7.7; Enith +0.0; Jackal +0.0 | 2.9 |
| Toughened Resolve | 3 | +0.89 | Carrick +8.0; Browndog (has it) +3.9; Ashleigh +3.8 | 0.0 |
| Lifeline | 2 | +0.50 | Hanforth +3.0; Felix +2.6; Jackal +0.0 | 0.6 |
| Brace | 1 | +0.41 | Browndog (has it) +1.2; Felix +0.4; Enith +0.3 | 0.8 |
| One Eye Behind You | 2 | +0.34 | Sable (has it) +2.1; Felix +0.8; Enith -0.8 | 0.0 |
| Grim Resolve | 2 | +0.27 | Felix +1.6; Hanforth +1.5; Jackal (has it) -2.4 | 0.0 |
| Bladeslinging | 1 | +0.24 | Enith +0.7; Browndog +0.0; Sable +0.0 | 0.0 |
| Reckoning | 2 | +0.23 | Hanforth (has it) +1.4; Felix +0.3; Jackal -1.4 | 1.2 |
| Blinkstep | 2 | +0.20 | Jackal +1.2; Carrick +0.5; Ashleigh -0.2 | 0.8 |
| Swallow Skims the Water | 3 | +0.20 | Felix (has it) +1.8 | 1.9 |
| Gainsay | 1 | +0.18 | Beornhard (has it) +0.5; Enith +0.5; Felix +0.0 | 0.7 |
| Land's Bounty | 2 | +0.15 | Hanforth +0.9; Sable -0.0 | 0.3 |
| Willow Springs Back | 3 | +0.14 | Felix (has it) +1.3 | 2.3 |
| Lantern Gutters in the Wind | 4 | +0.14 | Felix +1.7 | 0.8 |
| Circling Vulture | 4 | +0.13 | Felix +1.6 | 0.4 |
| Bark Turns the Blade | 2 | +0.11 | Hanforth +0.7; Jackal +0.3; Felix -0.2 | 0.0 |
| Optimize Blood | 3 | +0.11 | Carrick +1.0 | 0.0 |
| Second Wind | 2 | +0.11 | Browndog (has it) +0.6; Hilde (has it) +0.4; Felix +0.3 | 0.3 |
| Sickness Takes the Flock | 2 | +0.10 | Hilde +0.6; Hanforth +0.4; Felix (has it) +0.4 | 1.0 |
| Old Growth Digs Deep | 4 | +0.10 | Felix +1.2 | 0.8 |
| Skin of Stone | 3 | +0.10 | Carrick +0.9; Browndog +0.6; Ashleigh +0.1 | 0.3 |
| Hand Rings the Bell | 2 | +0.09 | Hilde +0.5; Hanforth +0.4; Felix +0.2 | 0.7 |

### The least (not Styles)

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Spectral Spiderwebs | 2 | -0.09 | Sable -0.6; Hanforth -0.9 | 0.7 |
| Feint | 1 | -0.06 | Enith -0.2; Felix -1.1; Jackal -1.4 | 0.7 |
| Great Wind Scatters the Leaves | 4 | -0.05 | Felix -0.6 | 1.3 |
| Bottomless Bottles | 4 | -0.05 | Jackal (has it) -0.5 | 0.0 |
| Raise Spirits | 4 | -0.04 | Ashleigh (has it) -0.4 | 0.0 |
| Sap Seals the Wound | 4 | -0.03 | Felix -0.3 | 0.0 |
| Cloak of Awe | 3 | -0.02 | Hanforth -0.2 | 1.2 |
| Shattering Slam | 2 | -0.02 | Felix -0.1 | 0.7 |
| Arrow Finds Only Mist | 3 | -0.01 | Felix -0.1 | 0.2 |
| Gust of Wind | 1 | -0.01 | Hanforth (has it) -0.0; Enith -0.1; Felix -1.7 | 1.1 |
| Chainbreaker | 2 | -0.01 | Felix -0.0 | 0.1 |
| Bell Tolls a Dirge | 2 | -0.00 | Jackal -0.0; Felix -0.3; Hanforth -1.1 | 0.7 |
| Perfect Strike | 2 | -0.00 | Sable (has it) -0.0; Carrick (has it) -0.1; Enith -0.2 | 0.0 |
| Temper Soulblade | 1 | +0.00 | Enith (has it) +0.0 | 0.0 |

### Styles, against no Style

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Disciple of the Flowing Hand | 3 | +0.35 | Jackal +3.1; Hanforth +1.4; Felix +0.8 | 0.0 |
| Spirit Hands | 3 | +0.30 | Felix +2.7; Hanforth +0.0 | 0.0 |
| Placeholder's Lengthy Ley-weaving | 2 | +0.28 | Hanforth (has it) +1.7; Beornhard +0.0; Enith -0.3 | 0.0 |
| Seize the Moment | 2 | +0.27 | Hilde +1.6; Jackal +0.9; Hanforth +0.1 | 0.0 |
| Overchanneling | 2 | +0.26 | Beornhard (has it) +1.5; Felix -0.3; Enith -0.4 | 0.0 |
| Earthen Mantle Approach | 3 | +0.25 | Hilde +2.3 | 0.0 |
| Hands of Defilement | 3 | +0.25 | Felix +2.2; Hanforth +0.0 | 0.9 |
| Intimidating Presence | 2 | +0.23 | Hilde +1.4; Ashleigh +0.1; Browndog -0.8 | 5.2 |
| Hand of Chaos | 2 | +0.20 | Felix +1.2; Enith (has it) +0.9; Hanforth +0.4 | 0.0 |
| Eagle Eyes | 1 | +0.18 | Jackal (has it) +0.5; Carrick +0.3; Ashleigh +0.2 | 0.0 |
| Furious Rage | 2 | +0.18 | Enith +1.1; Browndog +0.3; Hilde (has it) +0.2 | 0.0 |
| Aura of Death | 1 | +0.17 | Enith +0.5; Felix +0.2; Beornhard +0.0 | 5.2 |
| Rending Claws | 2 | +0.16 | Enith +1.0; Felix +0.9; Jackal +0.2 | 6.9 |
| Doubleshot | 4 | +0.15 | Carrick +1.9; Jackal +0.5 | 0.0 |
| Ambush Predator | 3 | +0.14 | Felix +1.3; Carrick +0.3 | 0.0 |
| Lifeward | 3 | +0.14 | Hanforth +1.2; Ashleigh +0.0 | 0.0 |
| Crashing Wave Approach | 3 | +0.13 | Hilde +1.1; Browndog +1.0; Enith +0.6 | 4.6 |
| Command the Tempo | 3 | +0.12 | Browndog +1.1; Ashleigh +0.3 | 0.0 |
| Indomitable Phalanx | 2 | +0.12 | Hilde +0.7; Browndog +0.6; Enith +0.4 | 0.0 |
| Suppressing Fire | 3 | +0.11 | Carrick +1.0; Sable (has it) +1.0; Jackal +0.8 | 4.8 |
| Inexhaustible Guardian | 2 | +0.10 | Browndog (has it) +0.6; Enith +0.2; Hilde +0.2 | 0.0 |
| Boughs Unbroken | 2 | +0.10 | Felix (has it) +0.6; Hanforth +0.2; Beornhard +0.0 | 0.0 |
| Lend Bulwark | 2 | +0.10 | Hilde +0.6; Browndog +0.3; Enith +0.3 | 0.3 |
| Exploit the Opening | 3 | +0.10 | Enith +0.9; Felix +0.8; Hanforth +0.4 | 0.0 |
| Earthen Fist Posture | 1 | +0.08 | Jackal +0.2; Felix -0.0; Enith -0.1 | 0.0 |
| Forward! | 1 | +0.08 | Ashleigh +0.2; Browndog -0.1; Hilde -0.1 | 2.7 |
| Field Medic | 1 | +0.07 | Hanforth +0.2; Ashleigh +0.0; Carrick +0.0 | 0.0 |
| Eternal Riposte | 2 | +0.06 | Felix +0.4; Enith +0.3; Hanforth +0.3 | 1.3 |
| Furious Swipes | 3 | +0.06 | Felix +0.5; Hanforth +0.0 | 3.8 |
| Lie in Wait | 1 | +0.04 | Enith +0.1; Felix -0.5; Jackal -1.7 | 0.0 |
| Lead by Example | 2 | +0.03 | Hilde +0.2; Enith +0.1; Browndog +0.1 | 0.0 |
| Follow Through | 1 | +0.03 | Hanforth +0.1; Felix +0.1; Enith -0.0 | 0.1 |
| Lawman's Hand | 2 | +0.03 | Felix +0.2; Carrick (has it) +0.1; Enith +0.0 | 0.0 |
| Storm of Blades | 3 | +0.02 | Enith +0.1; Carrick +0.1; Jackal -0.1 | 0.0 |
| Twin Spell | 3 | +0.01 | Enith +0.1; Beornhard +0.0 | 0.0 |
| Dread Reputation | 3 | +0.01 | Ashleigh +0.1; Browndog -1.8 | 3.3 |
| Deadeye's Shadow | 2 | +0.01 | Ashleigh +0.0; Carrick +0.0; Jackal -0.9 | 2.2 |
| Commander's Gambit | 4 | +0.00 | Ashleigh +0.0 | 0.0 |
| Infinite Coiling | 2 | +0.00 | Beornhard +0.0; Felix +0.0; Hanforth +0.0 | 0.0 |
| Drunken Brawling | 2 | +0.00 | Ashleigh +0.0; Carrick +0.0; Jackal +0.0 | 0.0 |
| Grasping Earth | 2 | +0.00 | Enith +0.0; Hanforth +0.0 | 0.0 |

### Never did anything on any host

- **Temper Soulblade** (Enith's Fatestealer): no effect in these fights.
- **Bolstering Refrain**: needs three hurt allies, one Wounded; it seldom
  happens in these fights.
- **Striking Constrictor** and **Infinite Coiling**: need a PC who keeps
  a grapple; Felix plays Skirmisher, so he doesn't.
- **Drunken Brawling**: went to back-liners (the hosts that fit its
  prereqs cheapest), who don't move through melee.
- **Grasping Earth**: needs Difficult Terrain, and no host made any (a
  Glacier caster in the party would).

These say more about hosts and my play rules than about the Techniques.

## Features, per point

### Battle Maneuver (in place of a plain copy (the host's opening Maneuver))

| Feature | Level | Hilde, per point | Sable, per point |
|---|---|---|---|
| Half Guard | 1 | +0.74 ±0.29 | +1.25 ±0.26 |
| Half Guard x3 | 1 | +0.59 ±0.13 | +1.04 ±0.13 |
| Fleet Step | 1 | +1.47 ±0.54 | +0.10 ±0.19 |
| Backfoot | 1 | +0.99 ±0.35 | +0.58 ±0.42 |
| Fleet Step x3 | 1 | +0.87 ±0.21 | +0.04 ±0.07 |
| Ascended Blade | 3 | +0.42 ±0.16 | +0.41 ±0.17 |
| Elemental | 1 | +0.42 ±0.16 | +0.41 ±0.17 |
| Backfoot x3 | 1 | +0.41 ±0.12 | +0.32 ±0.14 |
| Turn Elements | 1 | +0.45 ±0.19 | +0.27 ±0.15 |
| Wing Clip | 1 | +0.38 ±0.25 | +0.22 ±0.13 |
| Harrying | 1 | +0.12 ±0.12 | +0.42 ±0.23 |
| Turn Elements x3 | 1 | +0.38 ±0.10 | +0.16 ±0.06 |
| Wing Clip x3 | 1 | +0.30 ±0.10 | +0.21 ±0.08 |
| Calculated | 1 | +0.14 ±0.10 | +0.34 ±0.13 |
| Flurry | 3 | +0.25 ±0.07 | +0.15 ±0.07 |
| Lunging | 1 | +0.33 ±0.36 | +0.00 ±0.00 |
| Viper's Sting | 1 | +0.18 ±0.15 | +0.15 ±0.11 |
| Whirlwind | 3 | +0.07 ±0.04 | +0.24 ±0.08 |
| Hamstring x3 | 1 | +0.05 ±0.03 | +0.24 ±0.15 |
| Lunging x3 | 1 | +0.29 ±0.17 | +0.00 ±0.00 |
| Harrying x3 | 1 | +0.05 ±0.04 | +0.20 ±0.08 |
| Battering | 1 | +0.05 ±0.06 | +0.18 ±0.12 |
| Victorious | 1 | +0.21 ±0.09 | +0.00 ±0.06 |
| Blade of Four Fates x3 | 1 | -0.05 ±0.19 | +0.24 ±0.19 |
| Lodestone | 1 | -0.14 ±0.46 | +0.32 ±0.45 |
| Lodestone x3 | 1 | -0.04 ±0.17 | +0.21 ±0.17 |
| Battering x3 | 1 | +0.05 ±0.05 | +0.09 ±0.06 |
| Hamstring | 1 | +0.04 ±0.03 | +0.06 ±0.29 |
| Distracting x3 | 1 | +0.04 ±0.08 | +0.04 ±0.15 |
| Distracting | 1 | +0.13 ±0.24 | -0.06 ±0.43 |
| Wind Slash | 1 | +0.04 ±0.22 | +0.00 ±0.00 |
| Wind Slash x3 | 1 | +0.01 ±0.07 | +0.00 ±0.00 |
| Bare-Handed | 1 | +0.00 ±0.00 | +0.00 ±0.00 |
| Ricochet Shot | 3 | +0.00 ±0.00 | +0.00 ±0.01 |
| Blade of Four Fates | 1 | -0.07 ±0.47 | -0.01 ±0.47 |

### War Magic (added to a Lance copy)

| Feature | Level | Beornhard, per point | Enith, per point |
|---|---|---|---|
| Abjuring | 2 | +0.55 ±0.38 | +0.31 ±0.14 |
| Wild Magic x3 | 3 | +0.35 ±0.15 | +0.28 ±0.14 |
| Destructive x3 | 3 | +0.39 ±0.11 | +0.20 ±0.12 |
| Abjuring x3 | 3 | +0.35 ±0.14 | +0.22 ±0.07 |
| Destructive | 2 | +0.34 ±0.26 | -0.12 ±0.28 |
| Frigid x3 | 3 | +0.10 ±0.12 | +0.03 ±0.08 |
| Wild Magic | 2 | +0.27 ±0.44 | -0.14 ±0.39 |
| Piercing Elements x3 | 3 | +0.07 ±0.10 | +0.04 ±0.11 |
| Frigid | 2 | -0.10 ±0.31 | +0.17 ±0.12 |
| Nova (Shape) | 3 | +0.04 ±0.11 | +0.01 ±0.02 |
| Barraging x3 | 3 | -0.01 ±0.10 | +0.03 ±0.04 |
| Necrotic x3 | 3 | -0.04 ±0.09 | +0.04 ±0.04 |
| Funnel (Shape) | 3 | +0.00 ±0.12 | -0.02 ±0.03 |
| Corrupting x3 | 3 | -0.07 ±0.10 | +0.03 ±0.04 |
| Channel (Shape) | 3 | -0.07 ±0.10 | +0.01 ±0.04 |
| Furrow (Shape) | 3 | -0.05 ±0.10 | -0.01 ±0.01 |
| Necrotic | 2 | -0.15 ±0.27 | +0.07 ±0.11 |
| Arcane Chant x3 | 3 | -0.10 ±0.10 | +0.00 ±0.00 |
| Draw Power x3 | 3 | -0.10 ±0.10 | +0.00 ±0.00 |
| Barraging | 2 | -0.20 ±0.29 | +0.08 ±0.10 |
| Reign of Blood x3 | 3 | -0.10 ±0.10 | -0.03 ±0.13 |
| Kinetic x3 | 3 | -0.19 ±0.13 | +0.01 ±0.06 |
| Corrupting | 2 | -0.24 ±0.29 | +0.02 ±0.09 |
| Piercing Elements | 3 | -0.25 ±0.30 | +0.03 ±0.30 |
| Glacier x3 | 3 | -0.28 ±0.14 | +0.03 ±0.06 |
| Arcane Chant | 2 | -0.26 ±0.29 | +0.00 ±0.00 |
| Draw Power | 3 | -0.30 ±0.30 | +0.00 ±0.00 |
| Glacier | 2 | -0.42 ±0.38 | +0.12 ±0.14 |
| Kinetic | 2 | -0.43 ±0.36 | +0.06 ±0.14 |
| Reign of Blood | 2 | -0.26 ±0.29 | -0.35 ±0.37 |
| Sanguine | 2 | -6.59 ±0.68 | -1.42 ±0.38 |

### Spirit Blessing (for a point of Shielding)

| Feature | Level | Hanforth, per point |
|---|---|---|
| Elemental Enhancement | 1 | +0.13 ±0.28 |
| Alacrity | 3 | -0.02 ±0.21 |
| Mass Blessing | 3 | -0.08 ±0.17 |
| Turn Elements | 1 | -0.15 ±0.23 |
| Quickened | 1 | -0.16 ±0.30 |
| Guided Hand | 3 | -0.18 ±0.15 |
| Touch of Chaos | 1 | -0.25 ±0.34 |
| Reach | 1 | -0.29 ±0.37 |
| Retribution | 1 | -0.30 ±0.27 |
| Steal Fate | 3 | -0.32 ±0.14 |
| Embolden | 1 | -0.39 ±0.21 |
| Step of Air | 1 | -0.40 ±0.23 |
| Steady | 1 | -0.42 ±0.22 |
| River's Might | 1 | -0.45 ±0.40 |

### Healing Magic (added to a plain Healing Magic copy)

| Feature | Level | Hanforth, per point |
|---|---|---|
| Guardian Angel | 1 | +1.31 ±0.29 |
| Triage | 2 | +0.51 ±0.11 |
| Guardian Angel x3 | 2 | +0.43 ±0.11 |
| Vitality | 2 | +0.32 ±0.10 |
| Purify | 1 | +0.17 ±0.08 |
| Reach | 1 | +0.11 ±0.26 |
| Purify x3 | 2 | +0.06 ±0.04 |
| Reach x3 | 2 | +0.05 ±0.09 |
| Deep Mending | 3 | +0.00 ±0.00 |
| Healing Pact | 3 | +0.00 ±0.00 |
| Rejuvenate x3 | 2 | -0.20 ±0.10 |
| Rejuvenate | 1 | -0.44 ±0.26 |

What stands out:

- **Sanguine** costs Beornhard's party 6.6 Health a fight and 15 points
  of win rate (Enith's 1.4): it adds 3 damage and turns the whole hit
  into Bleeding, which pays out too slowly in five-round fights. Unless
  the caster also cashes it with Reign of Blood, it's a trap.
- **Battle Maneuver**: Half Guard (+0.7 and +1.3 per point) and Fleet
  Step on Hilde (+1.5) lead; Backfoot, Ascended Blade and Elemental are
  solid. Ricochet Shot, Wind Slash and Lodestone do little.
- **War Magic**: Abjuring, Destructive and Wild Magic pay modestly, about
  +0.2 to +0.5 per point (the three-copy readings are the steadiest);
  the Shapes add about nothing on either host,
  since their extra targets seldom line up.
- **Spirit Blessing**: nothing beats a point of Shielding for Hanforth;
  Elemental Enhancement comes closest.
- **Healing Magic**: Guardian Angel (+1.3 for one point), then Triage and
  Vitality; Rejuvenate reads -0.4.

## Your call

- **The Assassin reading.** `'hurt'` (share of Health lost, ties to the
  squishiest-looking, then chance) reads the tactic's own description
  better and takes a big artifact out of anything that changes Health.
  Making it the default would move every baseline a little (the
  calibrate parties, the replays). Say if you want it.
- **The play rules behind the never-fires.** Bolstering Refrain's
  trigger, who keeps a grapple, Fatestealer.
- **Sanguine.** Worth a look in the rules, or a note that it wants Reign
  of Blood alongside.

## Next, if you want it

- Deeper runs (1,000+ fights a mix) on anything you want to price
  precisely; at this depth ±0.3 Health is the floor.
- Level 2 hosts for the Level 1-2 Techniques, which only got Level 3
  characters here.
- Hosts picked by archetype for the ones that went to poor fits
  (Drunken Brawling on a brawler, Grasping Earth with a Glacier caster).
