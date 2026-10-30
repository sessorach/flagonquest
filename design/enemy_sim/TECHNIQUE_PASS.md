# The broad pass: every Technique and Feature (2026-10-28)

A shallow test of everything the sim plays, to see how well it can tell
what a Technique or Feature is worth. Every modeled Technique went on up
to three Level 3 sample characters, and every Feature of the four
Buildables went into one of a host's own copies. `technique_pass.py`
runs it (about 20 minutes on four cores); the numbers are in
`technique_pass.csv`.

The short version:

- **Each reading is precise and repeats.** Rerun on a fresh set of
  fights, 30 Techniques came back with a correlation of 0.98, every
  difference inside its margin, and no sign flipped.
- **What a Technique is worth depends a lot on who has it.** Two hosts
  for the same Technique agree only loosely (0.37 for non-Styles).
  Mostly that's fit: an Unarmed Style on a swordsman, a gap-closer on a
  back-liner.
- **The Assassin tactic was swamping anything that changes Health.** It
  went for the least current Health, so at full Health every Assassin
  picked whoever was first in the party list, and a point off one PC's
  max Health sent them all at that PC. Per the designer it now reads
  "softest target" off the lightest armor (the default since this pass);
  Toughened Resolve went from +0.4 to +8.1 depending on the host to +3.8
  to +4.2 on all three.
- **XP cost barely predicts value** (correlation 0.30). Most Techniques
  (60 of 116) stay within half a point of Health even on their best
  host; 52 clear +0.5 somewhere; 4 are below -0.5 everywhere.
- **Standouts:** Warmage's Reserves, Toughened Resolve, Brace, Lifeline
  and Gainsay pay well for their XP. Sanguine on its own costs a
  caster's party 5 Health a fight. Feint still never pays.

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
  Level, so no XP changes hands. Battle Maneuver goes in place of a plain
  copy (the host's opening Maneuver), Healing Magic on a plain copy, and
  Enith's War Magic on a Lance copy, each against the same copy without
  it (one copy of the Feature, and three for a 1-point one with no cap).
  Spirit Blessing and Beornhard's War Magic are traded instead, for a
  point of Shielding and a point of Destructive: an empty Blessing still
  gets cast, and a plain Lance copy is one more use of Beornhard's War
  Magic Weapon while any Feature makes it a separate Technique attack, so
  "against nothing" measured the bookkeeping, not the Feature.
- **Fires a fight**: log lines naming it, so a passive that changes
  numbers (a Defense, a Health bonus) shows 0 even when it works.

Mistakes of mine, caught before this write-up: the first full run had
every Feature's sign backwards, the 20-fight smoke test was too noisy to
read, and one rerun ran under the old Assassin rule because I changed
the setting while it started. All fixed; the Feature numbers were
checked by hand on fresh runs.

## New in the sim for this

- **Interrupts on an enemy's attack** (`hooks.py`): `attack_targeting`
  before its flip (move it onto another PC, call it off, or change the
  Defense it checks) and `attack_flipped` after the flip, before it hits
  or misses. With them: Swatting Paw, Arrow Finds Only Mist, Slithering
  Hands, Lend Bulwark and Seasons Pass the Forest. Turn the Tables still
  needs PC grapples.
- **Interrupts happen before their trigger** (per the designer:
  "techniques are priced assuming they give players an opportunity to do
  something before the triggering action happens"). Every modeled one
  was checked: Gainsay, Magehunter, Bark Turns the Blade, Lifeline, Raise
  Spirits, Arrow Finds Only Mist and Lend Bulwark all resolve first, and
  an attacker Downed by one never attacks. Mind and Body Unbroken used to
  catch the Down after it landed, and missed Bleeding; it's now at a
  `pc_would_drop` point, before the Health comes off, from any source.
- **Storm of Blades**, for a striker with a one-handed weapon in each
  hand. Repeating a plain swing is the same as a second swing, so it only
  pays when it repeats a Maneuver or a Technique strike; it changed
  little on any host.
- **`party.fit`**: XP-matched swaps with prereq checks.
- Coverage is 126 of 205 modeled, 44 out of combat, 35 deferred.

## How well the sim can tell

**Repeatability.** 30 Techniques at random (68 host readings) rerun on a
different 800 fights: correlation 0.98, every difference within the
combined margins, and all 29 readings bigger than ±0.3 kept their sign.
(That check ran under the old Assassin rule; it's a property of the
method.) The median margin is ±0.3 Health. So at this depth a reading is
a fact about that host in that party.

**Across hosts.** Two hosts for the same Technique correlate 0.20 (0.37
for non-Styles), up from 0.02 and 0.08 under the old Assassin rule. What's
left is mostly fit: Spirit Hands is +1.9 on Felix and 0 on Hanforth (his
weapon isn't Unarmed), Feint is -0.1 to -1.8 depending on who follows
up, Lifeline is +2.0 on the healer and -0.2 on Jackal. A Technique's
value belongs to the Technique and the character together.

**The Assassin tactic.** Every Level 3 mix has two to four Assassins.
The old rule went for the least current Health, so at the start of a
fight (nearly everyone on 10) the tie went to whoever was listed first,
and a point off any other PC's max Health moved every Assassin onto that
PC: Felix's party scored +6.4 with Felix on 9 Health instead of 10. Now
(`ASSASSIN_READS = 'softest'`, the default): hurt worst first, then the
lightest armor, then chance. It made the Level 1-2 calibrate parties
rougher (someone Wounded 36-47% -> 55-76%), Level 3 about the same.
Against the old-rule pass (`technique_pass_current.csv`), readings
correlate 0.78; the ones that moved most change max Health (Grim
Resolve, Toughened Resolve), then several Styles on Felix and Jackal.

**Yardsticks.** What plain ranks buy each host, in the same units:

| On each host | Health left | XP |
|---|---|---|
| +1 rank of the main attack Skill | +0.3 to +1.3 (Felix +1.3, Jackal +1.3, Carrick +1.1) | 5-6 |
| +1 rank of Resilience | +0.1 to +0.3 | 3-5 |
| +1 max Health | +0.7 to +1.4 | - |

So a rank buys roughly 0.05 to 0.25 Health per XP. (Under the old
Assassin rule one more max Health read +4.8 on Carrick: the same tie.)

**XP cost.** Across 116 Techniques, Level (XP cost) correlates 0.30 with
the average value and 0.13 with the best host's. Average value per XP by
Level: Level 1 -0.02, Level 2 +0.04, Level 3 +0.06, Level 4 +0.04, so
about half a main-attack rank's worth per XP.

## Techniques

"Best host per XP" is the best host's reading divided by the
Technique's XP (three times its Level); "(has it)" means the reading is
that host's own copy taken off.

### The most for their XP (not Styles)

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Warmage's Reserves | 2 | +1.02 | Beornhard (has it) +6.1; Enith +0.0; Jackal +0.0 | 2.6 |
| Toughened Resolve | 3 | +0.47 | Carrick +4.2; Ashleigh +3.8; Browndog (has it) +3.8 | 0.0 |
| Brace | 1 | +0.35 | Browndog (has it) +1.1; Enith +0.7; Felix +0.6 | 0.8 |
| Lifeline | 2 | +0.33 | Hanforth +2.0; Felix +1.4; Jackal -0.2 | 0.5 |
| Gainsay | 1 | +0.32 | Beornhard (has it) +1.0; Enith +0.3; Felix +0.0 | 0.7 |
| Reckoning | 2 | +0.31 | Hanforth (has it) +1.9; Felix -0.6; Jackal -0.9 | 1.2 |
| One Eye Behind You | 2 | +0.26 | Sable (has it) +1.5; Felix +0.6; Enith -0.6 | 0.0 |
| Bladeslinging | 1 | +0.20 | Enith +0.6; Browndog +0.0; Sable +0.0 | 0.0 |
| Swallow Skims the Water | 3 | +0.18 | Felix (has it) +1.7 | 1.8 |
| Bark Turns the Blade | 2 | +0.18 | Hanforth +1.1; Jackal +0.6; Felix +0.2 | 0.0 |
| Circling Vulture | 4 | +0.16 | Felix +2.0 | 0.3 |
| Land's Bounty | 2 | +0.16 | Hanforth +0.9; Sable -0.0 | 0.3 |
| Lantern Gutters in the Wind | 4 | +0.15 | Felix +1.8 | 0.8 |
| Blinkstep | 2 | +0.14 | Jackal +0.9; Carrick +0.4; Ashleigh -0.1 | 0.7 |
| Old Growth Digs Deep | 4 | +0.13 | Felix +1.5 | 0.7 |
| Willow Springs Back | 3 | +0.12 | Felix (has it) +1.1 | 2.1 |
| Swatting Paw | 3 | +0.12 | Felix +1.1 | 0.6 |
| Sickness Takes the Flock | 2 | +0.11 | Hilde +0.7; Hanforth +0.3; Felix (has it) +0.2 | 1.0 |
| Force Missiles | 1 | +0.11 | Beornhard +0.3; Enith +0.1; Felix -0.1 | 1.6 |
| Seasons Pass the Forest | 2 | +0.11 | Felix +0.7 | 0.2 |
| Mind and Body Unbroken | 4 | +0.11 | Felix +1.3 | 0.0 |
| Optimize Blood | 3 | +0.10 | Carrick +0.9 | 0.0 |

### The least (not Styles)

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Raise Spirits | 4 | -0.07 | Ashleigh (has it) -0.8 | 0.0 |
| Great Wind Scatters the Leaves | 4 | -0.06 | Felix -0.7 | 1.3 |
| Spectral Spiderwebs | 2 | -0.05 | Sable -0.3; Hanforth -0.7 | 0.7 |
| Bottomless Bottles | 4 | -0.05 | Jackal (has it) -0.6 | 0.0 |
| Shattering Slam | 2 | -0.04 | Felix -0.2 | 0.6 |
| Cloak of Awe | 3 | -0.03 | Hanforth -0.3 | 1.1 |
| Feint | 1 | -0.03 | Enith -0.1; Jackal -0.9; Felix -1.8 | 0.7 |
| Cloak of Command | 3 | -0.02 | Hanforth -0.2 | 1.1 |
| Arrow Finds Only Mist | 3 | -0.02 | Felix -0.2 | 0.2 |
| Perfect Strike | 2 | -0.01 | Enith -0.1; Sable (has it) -0.2; Carrick (has it) -0.4 | 0.0 |
| Gaze of Pale Moonlight | 2 | -0.01 | Jackal -0.0; Felix -0.2; Hanforth -0.3 | 0.7 |
| Gust of Wind | 1 | -0.00 | Enith -0.0; Hanforth (has it) -0.2; Felix -1.9 | 1.0 |
| Wall of Shadows | 2 | -0.00 | Beornhard (has it) -0.0; Felix -0.2; Jackal -0.4 | 0.5 |
| Chainbreaker | 2 | -0.00 | Felix -0.0 | 0.2 |

### Styles, against no Style

| Technique | Level | Best host per XP | Hosts: Health left | Fires a fight (most) |
|---|---|---|---|---|
| Placeholder's Lengthy Ley-weaving | 2 | +0.34 | Hanforth (has it) +2.1; Enith +0.0; Beornhard +0.0 | 0.0 |
| Seize the Moment | 2 | +0.27 | Hilde +1.6; Jackal +0.7; Hanforth +0.4 | 0.0 |
| Overchanneling | 2 | +0.27 | Beornhard (has it) +1.6; Felix -0.9; Enith -1.0 | 0.0 |
| Earthen Mantle Approach | 3 | +0.25 | Hilde +2.3 | 0.0 |
| Eagle Eyes | 1 | +0.22 | Jackal (has it) +0.7; Carrick +0.3; Ashleigh +0.1 | 0.0 |
| Spirit Hands | 3 | +0.21 | Felix +1.9; Hanforth +0.0 | 0.0 |
| Disciple of the Flowing Hand | 3 | +0.19 | Jackal +1.7; Felix +1.7; Hanforth +1.3 | 0.0 |
| Hands of Defilement | 3 | +0.19 | Felix +1.7; Hanforth +0.0 | 0.9 |
| Intimidating Presence | 2 | +0.17 | Hilde +1.0; Ashleigh +0.1; Browndog -0.9 | 4.9 |
| Command the Tempo | 3 | +0.17 | Browndog +1.5; Ashleigh +0.3 | 0.0 |
| Hand of Chaos | 2 | +0.15 | Felix +0.9; Hanforth +0.3; Enith (has it) +0.2 | 0.0 |
| Boughs Unbroken | 2 | +0.15 | Felix (has it) +0.9; Hanforth +0.3; Beornhard +0.1 | 0.0 |
| Rending Claws | 2 | +0.14 | Felix +0.8; Jackal +0.5; Enith +0.3 | 5.3 |
| Indomitable Phalanx | 2 | +0.14 | Hilde +0.8; Browndog +0.6; Enith +0.5 | 0.0 |
| Doubleshot | 4 | +0.13 | Carrick +1.6; Jackal +0.4 | 0.0 |
| Suppressing Fire | 3 | +0.12 | Carrick +1.1; Sable (has it) +1.0; Jackal +0.9 | 5.9 |
| Crashing Wave Approach | 3 | +0.11 | Hilde +1.0; Browndog +0.6; Enith +0.4 | 4.5 |
| Ambush Predator | 3 | +0.10 | Felix +0.9; Carrick +0.8 | 0.0 |
| Lifeward | 3 | +0.10 | Hanforth +0.9; Ashleigh +0.0 | 0.0 |
| Eternal Riposte | 2 | +0.09 | Felix +0.6; Enith +0.4; Hanforth +0.1 | 1.2 |
| Lend Bulwark | 2 | +0.09 | Browndog +0.5; Hilde +0.5; Enith +0.0 | 0.3 |
| Exploit the Opening | 3 | +0.06 | Felix +0.5; Hanforth +0.2; Enith +0.2 | 0.0 |
| Furious Rage | 2 | +0.06 | Enith +0.3; Browndog +0.3; Hilde (has it) +0.3 | 0.0 |
| Inexhaustible Guardian | 2 | +0.05 | Browndog (has it) +0.3; Enith +0.3; Hilde +0.2 | 0.0 |
| Forward! | 1 | +0.05 | Ashleigh +0.2; Browndog +0.0; Hilde -0.2 | 2.5 |
| Lead by Example | 2 | +0.05 | Enith +0.3; Browndog +0.1; Hilde +0.1 | 0.0 |
| Field Medic | 1 | +0.05 | Hanforth +0.2; Ashleigh +0.0; Carrick +0.0 | 0.0 |
| Aura of Death | 1 | +0.05 | Felix +0.1; Enith +0.1; Beornhard +0.0 | 4.0 |
| Furious Swipes | 3 | +0.04 | Felix +0.4; Hanforth +0.0 | 3.1 |
| Lawman's Hand | 2 | +0.03 | Carrick (has it) +0.2; Felix +0.1; Enith +0.0 | 0.0 |
| Deadeye's Shadow | 2 | +0.02 | Ashleigh +0.1; Carrick -0.1; Jackal -1.0 | 3.2 |
| Follow Through | 1 | +0.02 | Hanforth +0.1; Felix +0.0; Enith -0.0 | 0.1 |
| Twin Spell | 3 | +0.01 | Enith +0.1; Beornhard +0.0 | 0.0 |
| Storm of Blades | 3 | +0.01 | Carrick +0.1; Enith +0.1; Jackal -0.3 | 0.0 |
| Commander's Gambit | 4 | +0.01 | Ashleigh +0.1 | 0.0 |
| Dread Reputation | 3 | +0.01 | Ashleigh +0.1; Browndog -1.6 | 3.3 |
| Infinite Coiling | 2 | +0.00 | Beornhard +0.0; Felix +0.0; Hanforth +0.0 | 0.0 |
| Drunken Brawling | 2 | +0.00 | Ashleigh +0.0; Carrick +0.0; Jackal +0.0 | 0.0 |
| Earthen Fist Posture | 1 | +0.00 | Felix +0.0; Enith -0.0; Jackal -0.2 | 0.0 |
| Grasping Earth | 2 | +0.00 | Enith +0.0; Hanforth +0.0 | 0.0 |
| Lie in Wait | 1 | -0.22 | Felix -0.7; Jackal -0.9; Enith -1.2 | 0.0 |

### Never did anything on any host

- **Temper Soulblade** (Enith's Fatestealer): no effect in these fights.
- **Striking Constrictor** and **Infinite Coiling**: need a PC who keeps
  a grapple; Felix plays Skirmisher, so he doesn't.
- **Drunken Brawling**: went to back-liners (the hosts that fit its
  prereqs cheapest), who don't move through melee.
- **Grasping Earth**: needs Difficult Terrain, and no host made any (a
  Glacier caster in the party would).

These say more about hosts and my play rules than about the Techniques.

## Features, per point

### Battle Maneuver (in place of a plain copy, the host's opening Maneuver)

| Feature | Level | Hilde, per point | Sable, per point |
|---|---|---|---|
| Fleet Step | 1 | +1.33 ±0.54 | +0.06 ±0.20 |
| Half Guard | 1 | +0.66 ±0.26 | +0.54 ±0.19 |
| Backfoot | 1 | +0.67 ±0.38 | +0.52 ±0.39 |
| Half Guard x3 | 1 | +0.55 ±0.13 | +0.56 ±0.11 |
| Fleet Step x3 | 1 | +0.90 ±0.21 | +0.03 ±0.07 |
| Turn Elements | 1 | +0.44 ±0.20 | +0.49 ±0.18 |
| Wing Clip | 1 | +0.47 ±0.29 | +0.26 ±0.17 |
| Ascended Blade | 3 | +0.30 ±0.16 | +0.38 ±0.14 |
| Elemental | 1 | +0.30 ±0.16 | +0.38 ±0.14 |
| Turn Elements x3 | 1 | +0.43 ±0.11 | +0.24 ±0.08 |
| Backfoot x3 | 1 | +0.31 ±0.12 | +0.30 ±0.13 |
| Harrying | 1 | +0.15 ±0.13 | +0.42 ±0.19 |
| Wing Clip x3 | 1 | +0.28 ±0.11 | +0.20 ±0.08 |
| Viper's Sting | 1 | +0.25 ±0.15 | +0.19 ±0.11 |
| Flurry | 3 | +0.22 ±0.07 | +0.16 ±0.07 |
| Lunging x3 | 1 | +0.38 ±0.16 | +0.00 ±0.00 |
| Calculated | 1 | +0.08 ±0.07 | +0.28 ±0.13 |
| Harrying x3 | 1 | +0.06 ±0.05 | +0.22 ±0.07 |
| Lunging | 1 | +0.28 ±0.31 | +0.00 ±0.00 |
| Hamstring | 1 | +0.02 ±0.02 | +0.24 ±0.27 |
| Victorious | 1 | +0.21 ±0.09 | +0.03 ±0.07 |
| Whirlwind | 3 | +0.06 ±0.04 | +0.18 ±0.08 |
| Hamstring x3 | 1 | +0.02 ±0.03 | +0.21 ±0.14 |
| Blade of Four Fates x3 | 1 | -0.06 ±0.22 | +0.21 ±0.21 |
| Blade of Four Fates | 1 | -0.05 ±0.48 | +0.19 ±0.55 |
| Battering | 1 | -0.00 ±0.02 | +0.11 ±0.11 |
| Battering x3 | 1 | +0.02 ±0.05 | +0.07 ±0.05 |
| Lodestone | 1 | -0.18 ±0.43 | +0.24 ±0.44 |
| Bare-Handed | 1 | +0.00 ±0.00 | +0.00 ±0.00 |
| Ricochet Shot | 3 | +0.00 ±0.00 | -0.00 ±0.01 |
| Lodestone x3 | 1 | -0.13 ±0.16 | +0.12 ±0.17 |
| Wind Slash x3 | 1 | -0.04 ±0.08 | +0.00 ±0.00 |
| Distracting x3 | 1 | -0.03 ±0.06 | -0.04 ±0.15 |
| Wind Slash | 1 | -0.12 ±0.23 | +0.00 ±0.00 |
| Distracting | 1 | -0.09 ±0.17 | -0.26 ±0.44 |

### War Magic (Beornhard: for a point of Destructive on a Lance copy; Enith: added to a Lance copy)

| Feature | Level | Beornhard, per point | Enith, per point |
|---|---|---|---|
| Abjuring | 2 | +0.19 ±0.30 | +0.29 ±0.12 |
| Destructive x3 | 3 | - | +0.20 ±0.11 |
| Abjuring x3 | 3 | - | +0.17 ±0.05 |
| Wild Magic x3 | 3 | - | +0.14 ±0.14 |
| Piercing Elements x3 | 3 | - | +0.09 ±0.09 |
| Glacier x3 | 3 | - | +0.05 ±0.07 |
| Barraging x3 | 3 | - | +0.03 ±0.04 |
| Furrow (Shape) | 4 | +0.01 ±0.09 | +0.00 ±0.01 |
| Arcane Chant x3 | 3 | - | +0.00 ±0.00 |
| Corrupting x3 | 3 | - | +0.00 ±0.04 |
| Draw Power x3 | 3 | - | +0.00 ±0.00 |
| Necrotic x3 | 3 | - | +0.00 ±0.02 |
| Kinetic x3 | 3 | - | -0.01 ±0.03 |
| Reign of Blood x3 | 3 | - | -0.02 ±0.09 |
| Frigid x3 | 3 | - | -0.03 ±0.05 |
| Channel (Shape) | 4 | -0.12 ±0.06 | +0.02 ±0.03 |
| Destructive | 2 | - | -0.06 ±0.22 |
| Funnel (Shape) | 4 | -0.19 ±0.10 | +0.00 ±0.03 |
| Frigid | 2 | -0.29 ±0.21 | +0.05 ±0.09 |
| Piercing Elements | 3 | -0.29 ±0.19 | +0.04 ±0.23 |
| Draw Power | 3 | -0.28 ±0.13 | +0.00 ±0.00 |
| Nova (Shape) | 4 | -0.30 ±0.08 | +0.01 ±0.01 |
| Arcane Chant | 2 | -0.34 ±0.25 | +0.00 ±0.00 |
| Necrotic | 2 | -0.42 ±0.22 | -0.02 ±0.06 |
| Glacier | 2 | -0.59 ±0.33 | +0.14 ±0.15 |
| Barraging | 2 | -0.48 ±0.24 | -0.01 ±0.09 |
| Corrupting | 2 | -0.45 ±0.22 | -0.05 ±0.08 |
| Wild Magic | 2 | -0.22 ±0.41 | -0.29 ±0.40 |
| Reign of Blood | 2 | -0.45 ±0.22 | -0.20 ±0.27 |
| Kinetic | 2 | -0.78 ±0.32 | +0.01 ±0.05 |
| Sanguine | 2 | -5.14 ±0.61 | -1.13 ±0.33 |

### Spirit Blessing (for a point of Shielding)

| Feature | Level | Hanforth, per point |
|---|---|---|
| Elemental Enhancement | 1 | -0.03 ±0.23 |
| Mass Blessing | 3 | -0.13 ±0.13 |
| Quickened | 1 | -0.14 ±0.29 |
| Alacrity | 3 | -0.17 ±0.18 |
| Guided Hand | 3 | -0.17 ±0.12 |
| Reach | 1 | -0.18 ±0.28 |
| Touch of Chaos | 1 | -0.18 ±0.29 |
| Turn Elements | 1 | -0.18 ±0.16 |
| Step of Air | 1 | -0.25 ±0.18 |
| Retribution | 1 | -0.26 ±0.19 |
| Steal Fate | 3 | -0.31 ±0.10 |
| Embolden | 1 | -0.32 ±0.16 |
| Steady | 1 | -0.32 ±0.17 |
| River's Might | 1 | -0.68 ±0.33 |

### Healing Magic (added to a plain Healing Magic copy)

| Feature | Level | Hanforth, per point |
|---|---|---|
| Guardian Angel | 1 | +1.21 ±0.30 |
| Triage | 2 | +0.51 ±0.10 |
| Guardian Angel x3 | 2 | +0.43 ±0.11 |
| Vitality | 2 | +0.34 ±0.12 |
| Purify | 1 | +0.16 ±0.13 |
| Reach | 1 | +0.10 ±0.23 |
| Purify x3 | 2 | +0.02 ±0.03 |
| Reach x3 | 2 | +0.02 ±0.07 |
| Healing Pact | 3 | +0.01 ±0.01 |
| Deep Mending | 3 | +0.00 ±0.00 |
| Rejuvenate x3 | 2 | -0.26 ±0.10 |
| Rejuvenate | 1 | -0.56 ±0.24 |

What stands out:

- **Sanguine** costs Beornhard's party 5.1 Health a fight against a
  point of Destructive, and 10 points of win rate (Enith's 1.1): under
  the current Bleeding rule it turns the whole hit into Bleeding that
  pays out over the target's next turns, some after it's Down or the
  fight is over. Down for an overhaul (designer, 2026-10-28).
- **Battle Maneuver**: Half Guard (+0.5 to +0.7 per point on both),
  Backfoot, Turn Elements and Wing Clip lead; Fleet Step is +1.3 on Hilde
  and nothing on Sable. Ricochet Shot, Wind Slash, Distracting and
  Lodestone do little.
- **War Magic**: on Beornhard, nothing beats a point of Destructive
  except Abjuring (+0.2) and Furrow (even); the Shapes add about nothing
  for Enith either. Destructive, Abjuring and Wild Magic pay modestly on
  Enith (+0.1 to +0.3 per point).
- **Spirit Blessing**: nothing beats a point of Shielding for Hanforth.
- **Healing Magic**: Guardian Angel (+1.2 for one point), then Triage and
  Vitality; Rejuvenate reads -0.6.

## Next, if you want it

- Deeper runs (1,000+ fights a mix) on anything you want to price
  precisely; at this depth ±0.3 Health is the floor.
- Level 2 hosts for the Level 1-2 Techniques, which only got Level 3
  characters here.
- Hosts picked by archetype for the ones that went to poor fits
  (Drunken Brawling on a brawler, Grasping Earth with a Glacier caster).

## By the day, every host (Level 3, 2026-10-30)

The deep pass: every modeled Technique added, free, to every Level 3
sample it fits, read by day_sim.py's morning Health (two fights, healing,
a night's rest, enemy Health ×1.0), 1,000 days per first-fight mix. A
Style counts against the host's own Style. `technique_pass_day_l3.csv`
has every reading (726); below, each Technique's mean over its hosts,
best and worst per XP (XP = three times its Level), next to the 10-28
single-fight pass (the top three hosts only, so the host sets differ).

| Technique | Lv | Hosts | Morning Health, roster mean | Per XP | Range over hosts | One fight (10-28 pass) |
|---|---|---|---|---|---|---|
| Lay On Hands | 4 | 1 | +7.33 ± 0.29 | +0.61 | +7.3 to +7.3 | +0.03 |
| Toughened Resolve | 3 | 3 | +4.77 ± 0.14 | +0.53 | +4.0 to +5.3 | +3.95 |
| Bolstering Refrain | 3 | 1 | +3.68 ± 0.24 | +0.41 | +3.7 to +3.7 | -0.01 |
| One Eye Behind You | 2 | 8 | +1.84 ± 0.16 | +0.31 | -0.8 to +3.8 | +0.50 |
| Lifeline | 2 | 7 | +1.77 ± 0.11 | +0.29 | +0.7 to +3.8 | +1.05 |
| Magehunter | 1 | 10 | +0.60 ± 0.07 | +0.20 | +0.2 to +1.4 | +0.03 |
| Second Wind | 2 | 8 | +1.05 ± 0.06 | +0.17 | +0.0 to +2.2 | +0.39 |
| Great Old Oak School - Bark Turns the Blade | 2 | 7 | +0.95 ± 0.10 | +0.16 | -0.4 to +2.2 | +0.64 |
| Disciple of the Flowing Hand | 3 | 7 | +1.37 ± 0.13 | +0.15 | +0.8 to +2.0 | +1.58 |
| Shugen School - Swallow Skims the Water | 3 | 1 | +1.35 ± 0.40 | +0.15 | +1.4 to +1.4 | +1.66 |
| Mind and Body Unbroken | 4 | 1 | +1.66 ± 0.29 | +0.14 | +1.7 to +1.7 | +1.27 |
| Brace | 1 | 10 | +0.40 ± 0.04 | +0.13 | +0.1 to +0.8 | +0.77 |
| Bear School - Swatting Paw | 3 | 1 | +1.17 ± 0.29 | +0.13 | +1.2 to +1.2 | +1.07 |
| Earthen Mantle Approach | 3 | 1 | +1.17 ± 0.29 | +0.13 | +1.2 to +1.2 | +2.26 |
| Warmage's Reserves | 2 | 4 | +0.75 ± 0.08 | +0.12 | +0.0 to +3.0 | +2.04 |
| ... | | | | | | |
| Grim Resolve | 2 | 8 | -0.44 ± 0.15 | -0.07 | -0.9 to +0.1 | -0.25 |
| Demon School - Bell Tolls a Dirge | 2 | 7 | -0.53 ± 0.06 | -0.09 | -1.6 to -0.0 | -0.26 |
| Gust of Wind | 1 | 10 | -0.28 ± 0.06 | -0.09 | -0.9 to +0.2 | -0.70 |
| Reckoning | 2 | 7 | -0.56 ± 0.12 | -0.09 | -2.3 to +2.0 | +0.11 |
| Raise Spirits | 4 | 1 | -1.45 ± 0.34 | -0.12 | -1.4 to -1.4 | -0.80 |
| Feint | 1 | 10 | -0.59 ± 0.08 | -0.20 | -1.8 to +0.2 | -0.93 |
| Challenge | 1 | 10 | -0.91 ± 0.10 | -0.30 | -1.7 to -0.1 | -0.41 |
| Lie in Wait | 1 | 9 | -2.11 ± 0.14 | -0.70 | -3.3 to -1.0 | -0.92 |

- **The two passes mostly agree** (rank correlation 0.81 across 116
  Techniques), except on healing between fights.
- **Healing jumps.** Lay On Hands (+7.3, from about nothing in one fight)
  and Bolstering Refrain (+3.7) are the biggest movers; Second Wind,
  One Eye Behind You and Lifeline gain too. Lay On Hands is any kind of
  Health, a card a cast, after every fight: the one host it fits
  (Level 4 prereq) spends a spare hand on it every night. It's on the
  watch list alongside healing in general (hall_of_fame/v1.2/HALL.md).
- **Morning Health still counts a pool in full.** Toughened Resolve's
  +4.77 is mostly its own 4 Health; the toughest-day reading puts a copy
  at about 0.4-0.6% per XP, an ordinary buy (TABLE_PLAY_NOTES.md, "Two
  kinds of measure").
- **Bottom of the list:** Lie in Wait (-2.1), Raise Spirits (-1.5),
  Challenge (-0.9) and Feint (-0.6), the same four as in the single-fight
  pass. The first three read worse by the day; Feint a little better.
  Reckoning drops from about even to -0.6.
- Hosts per Technique: median 5; a one-host reading is that character
  alone.

### Level 2 (2026-10-30)

The same pass on the Level 2 samples (`technique_pass_day_l2.csv`, 674
readings, 102 Techniques that fit someone at Level 2). It ranks them much
as Level 3 does (rank correlation 0.88). Top and bottom, roster means:

| Technique | Lv | Hosts | Morning Health | Per XP | At Level 3 |
|---|---|---|---|---|---|
| Toughened Resolve | 3 | 1 | +4.41 ± 0.17 | +0.49 | +4.77 |
| Bolstering Refrain | 3 | 1 | +2.63 ± 0.15 | +0.29 | +3.68 |
| Bottomless Bottles | 4 | 1 | +3.12 ± 0.34 | +0.26 | +0.71 |
| Brace | 1 | 9 | +0.45 ± 0.03 | +0.15 | +0.40 |
| Lifeline | 2 | 5 | +0.88 ± 0.09 | +0.15 | +1.77 |
| Second Wind | 2 | 7 | +0.60 ± 0.04 | +0.10 | +1.05 |
| ... | | | | | |
| Raise Spirits | 4 | 1 | -1.32 ± 0.19 | -0.11 | -1.45 |
| Feint | 1 | 10 | -0.36 ± 0.05 | -0.12 | -0.59 |
| Challenge | 1 | 9 | -0.47 ± 0.06 | -0.16 | -0.91 |
| Lie in Wait | 1 | 10 | -1.10 ± 0.09 | -0.37 | -2.11 |

- Most things are worth less at Level 2 than at Level 3, losses
  included. Lifeline and Second Wind roughly halve; so does Lie in
  Wait's cost. I haven't looked into why.
- Bottomless Bottles (Jackal's) goes the other way: four times as much
  at Level 2 as at Level 3. Not looked into either.
- Lay On Hands doesn't fit anyone at Level 2 (Level 4 prereq), so it's
  missing here.
