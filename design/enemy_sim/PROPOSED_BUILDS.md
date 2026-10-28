# Proposed builds: Felix, Enith, Ashleigh and Sable at Levels 2 and 3

Proposals for the four characters who only have Level 1 exports (2026-10-28,
for the designer to look over and tweak). Each one grows from your own
Level 1 build, so they read like the same characters levelling up; the Level
1 builds stay as you made them. They're in the sim as rows named
"(L2, proposed)" and "(L3, proposed)" (`sample_pcs.csv`, files in
`builds/proposed/`), so `compare_builds.py --swap` and the party scripts run
them like any other row, and SHEETS.md shows each one resolved. When you've
settled one, rebuild it in the Builder and export it; the export replaces the
proposal.

This is the second pass. The first one put nearly all the new XP into
fighting, and you pointed out players don't level like that. This pass spends
10-20% of the new XP on things that fit the character's Level 1 side
interests: a ribbon Technique or a few out-of-combat Skill ranks. The
first pass is in git (commit 111436b) if you want to compare.

How they were made:

- **XP**: exactly 125 (Level 2) and 175 (Level 3), by the rulebook's costs (a
  Skill rank costs its new rank, a Stat point twice its new rank, a Technique
  three times its Level).
- **Rank cap**: 4 at Level 2 and 5 at Level 3, the most your own Level 2 and 3
  exports go to (the rulebook only states the 3 at creation).
- **Checked**: every Prereq Check, every Feature budget, and that the sim
  loads it. Stats get about a third of the new XP.
- **Out of combat**: 13-18% of each build's total XP, against 3-34% in yours
  (about 11% on average at Level 3). Numbers below.
- **One Style each**: the glossary's "you may only be in one Style at a time".
  The sim doesn't enforce that yet (it plays every Style a character knows),
  so where a character switches Styles, the one she doesn't fight in is in the
  row's Unmodeled column.

## Felix (Monk, unarmed)

Level 2: Sickness Takes the Flock (Vulnerable and Necrotic on a target) and
Hand Rings the Bell (his Slowing strike against Mental), plus Pranic
Nourishment, which fits a monk who meditates instead of sleeping. Body and
Essence up for his punch and Meditation.

**Felix (L2, proposed)** (44 Stats + 45 Skills + 36 Techniques = 125 XP)

- Stats: Agility 3, Body 3 (+1), Cunning 1, Mind 2, Essence 3 (+1)
- Skills: Acrobatics 2 (+2), Brawl 4 (+1), Stealth 2, Awareness 2 (+1), Might 1, Resilience 3 (+2), Insight 2, Composure 2 (+1), Meditation 4 (+1), Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2) **new**; Pranic Nourishment (L2) **new**; Shugen School - Hand Rings the Bell (L2) **new**
- In a fight: Health 10, Parry 16, Dodge 15, Vital 14, Mental 12, Vigilant 11, Speed 4, Reflex 3; Unarmed attack 9 for 5 Physical

Level 3: Swallow Skims the Water teleports him next to a target and strikes
its Mental Defense, and Willow Springs Back spends AP he has left at the end
of a turn to get an Encounter use back. Stealth 3 and Shadow's Path build on
the Stealth 2 he started with (he's a cat), in place of Toughened Body and
Meditation 5, so he stays at 10 Health.

**Felix (L3, proposed)** (60 Stats + 55 Skills + 60 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 3, Cunning 1, Mind 2, Essence 4 (+1)
- Skills: Acrobatics 2, Brawl 5 (+1), Stealth 3 (+1), Awareness 2, Might 2 (+1), Resilience 3, Insight 2, Composure 2, Meditation 4, Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2); Pranic Nourishment (L2); Shugen School - Hand Rings the Bell (L2); Shugen School - Swallow Skims the Water (L3) **new**; Great Old Oak School - Willow Springs Back (L3) **new**; Shadow's Path (L2) **new**
- In a fight: Health 10, Parry 18, Dodge 17, Vital 14, Mental 12, Vigilant 11, Speed 5, Reflex 3; Unarmed attack 11 for 5 Physical

Alternatives: Bark Turns the Blade (a 2 AP Interrupt when he's hit) instead of
Pranic Nourishment leaves his party 1.2 percentage points more of its
Health a fight. Spirit
Hands (Level 3 Style) instead of Boughs Unbroken.

## Enith (Duelist, your Warlock stand-in)

Level 2: Spellblade, which spends her War Magic uses on weapon hits (Bleeding
[3 x Level]), and Magehunter (an Interrupt on enemy casters). For the side:
Persuasion 3, a rank of Survival (she's a Settler), and Placeholder's
Wizardly Witchlight.

**Enith (L2, proposed)** (44 Stats + 51 Skills + 30 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 1, Cunning 3 (+1), Mind 2, Essence 3 (+1)
- Skills: Acrobatics 3 (+1), Melee 3 (+1), Stealth 1, Awareness 1, Might 2, Resilience 1, Insight 4 (+1), Persuasion 3 (+1), Survival 1 (+1), Academics 2 (+1), Composure 2, Sorcery 4 (+1)
- Techniques: Soulblade (L1: Light One-Handed Melee Weapon); Temper Soulblade (L1: Fatestealer); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2) **new**; Magehunter (L1) **new**; Placeholder's Wizardly Witchlight (L1) **new**
- In a fight: Health 10, Parry 15, Dodge 14, Vital 10, Mental 12, Vigilant 15, Speed 4, Reflex 7; 1H Light Melee attack 7 for 6 Physical

Level 3: a Level 3 War Magic copy built for damage (Lance, Destructive 3) and
Toughened Body, plus Academics, Stealth and Survival. In the first pass the
damage copy beat a third hex (Corrupting 4 with Piercing Elements) by +10.7%
wins (±3.2) at enemy Health x1.75; the hex is a fine pick if you want her
purely as the controller.

**Enith (L3, proposed)** (60 Stats + 70 Skills + 45 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 1, Cunning 3, Mind 2, Essence 4 (+1)
- Skills: Acrobatics 3, Melee 4 (+1), Stealth 2 (+1), Awareness 1, Might 2, Resilience 1, Insight 4, Persuasion 3, Survival 2 (+1), Academics 3 (+1), Composure 3 (+1), Sorcery 5 (+1)
- Techniques: Soulblade (L1: Light One-Handed Melee Weapon); Temper Soulblade (L1: Fatestealer); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2); Magehunter (L1); Placeholder's Wizardly Witchlight (L1); War Magic (L3: Lance, Destructive 3) **new**; Toughened Body (L2) **new**
- In a fight: Health 13, Parry 17, Dodge 15, Vital 10, Mental 13, Vigilant 15, Speed 5, Reflex 7; 1H Light Melee attack 9 for 6 Physical

Worth knowing: Body 1 and Resilience 1 leave her Vital Defense at 10, the
lowest of anyone at Levels 2 and 3. Feint is out (see the findings below).

## Ashleigh (Leader, bard)

Level 2: Heroic Inspiration (party-wide Protected) and Cry of Victory
(Frightens nearby enemies when she Downs one), plus Profession as a Busker,
which is what a bard does between adventures. Essence for Performance, Body
for Presence, Agility for her thrown weapon.

**Ashleigh (L2, proposed)** (48 Stats + 44 Skills + 33 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 3 (+1), Cunning 1, Mind 1, Essence 4 (+1)
- Skills: Acrobatics 3 (+1), Stealth 1, Awareness 1, Might 1, Presence 4 (+1), Resilience 2 (+1), Insight 2 (+1), Composure 2, Performance 4 (+1), Rapport 3
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2) **new**; Profession (L1: Busker) **new**; Cry of Victory (L2) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 13, Mental 11, Vigilant 11, Speed 4, Reflex 3; Light Thrown attack 7 for 3 Physical, range 9

Level 3: Bolstering Refrain (heals up to [half Performance] allies), Rally to
Victory (Level 4: allies Sift and swap out low cards) and A Perfectly Good
Explanation, a social Technique for the party's talker, in place of Insight
and Composure ranks. Essence 5 makes Performance 10.

**Ashleigh (L3, proposed)** (62 Stats + 53 Skills + 60 Techniques = 175 XP)

- Stats: Agility 3, Body 3, Cunning 2 (+1), Mind 1, Essence 5 (+1)
- Skills: Acrobatics 3, Stealth 1, Awareness 1, Might 1, Presence 4, Resilience 2, Insight 2, Composure 2, Performance 5 (+1), Rapport 4 (+1)
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2); Profession (L1: Busker); Cry of Victory (L2); Bolstering Refrain (L3) **new**; Rally to Victory (L4) **new**; A Perfectly Good Explanation (L2) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 13, Mental 11, Vigilant 12, Speed 4, Reflex 4; Light Thrown attack 7 for 4 Physical, range 9

Alternatives: Forward! (her Style, Hasted to nearby allies) instead of
Profession; it fired 1.7 times a fight in the first pass, but I haven't
measured it on its own.

## Sable (Deadeye, bow)

Level 2: a Battle Maneuver (Calculated and Wing Clip 3: Good Luck, then
Crippled on a hit) and Blinkstep (a free Shift, to keep her distance), plus
Stealth 3 and Shadow's Path in place of Toughened Body. Agility and Cunning up
for the bow.

**Sable (L2, proposed)** (42 Stats + 47 Skills + 36 Techniques = 125 XP)

- Stats: Agility 4 (+1), Body 1, Cunning 3 (+1), Mind 1, Essence 2 (+1)
- Skills: Acrobatics 3 (+1), Archery 4 (+1), Stealth 3 (+1), Athletics 1 (+1), Awareness 2, Might 2, Resilience 3 (+1), Insight 3, Persuasion 2, Composure 2
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3) **new**; Blinkstep (L2) **new**; Shadow's Path (L2) **new**
- In a fight: Health 10, Parry 13, Dodge 15, Vital 12, Mental 11, Vigilant 14, Speed 5, Reflex 6; Light Bow attack 9 for 6 Physical, range 19

Level 3: Suppressing Fire (Style: every bow shot Cripples the target, hit or
miss), and a second Maneuver with Ricochet Shot (an extra target next to the
first). She'd switch from Hand of Chaos to Suppressing Fire, so the sim plays
that one. Survival 3 for tracking, in place of Insight and Acrobatics ranks.

**Sable (L3, proposed)** (60 Stats + 61 Skills + 54 Techniques = 175 XP)

- Stats: Agility 5 (+1), Body 1, Cunning 4 (+1), Mind 1, Essence 2
- Skills: Acrobatics 3, Archery 5 (+1), Stealth 3, Athletics 1, Awareness 3 (+1), Might 2, Resilience 3, Insight 3, Persuasion 2, Survival 3 (+3), Composure 2
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3); Blinkstep (L2); Shadow's Path (L2); Suppressing Fire (L3) **new**; Battle Maneuver (L3: Ricochet Shot, Calculated, Wing Clip) **new**
- In a fight: Health 10, Parry 14, Dodge 16, Vital 12, Mental 11, Vigilant 15, Speed 6, Reflex 7; Light Bow attack 11 for 7 Physical, range 19
- The sim leaves out: Hand of Chaos (she fights in her other Style)

Alternatives: Wisdom of the Woods (needs Survival 3, which she now has) is
the next ribbon on her list. Deadeye's Shadow (Level 2 Style: Taunts on her hits) would test
whether an archer can draw attacks, but she's on 10 Health at the back.

## Next to your builds

Share of each build's XP spent out of combat: Skills no combat Technique of
theirs uses, and Techniques the sim doesn't play. Every Stat point counts as
combat, so these run a bit low.

| Character | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Hilde | 7% | 8% | 13% |
| Browndog | 16% | 5% | 3% |
| Jackal | 7% | 10% | 7% |
| Beornhard | 3% | 4% | 3% |
| Hanforth | 4% | 10% | 15% |
| Carrick | 39% | 34% | 25% |
| Felix | 11% | 13% (was 8%) | 15% (was 6%) |
| Enith | 16% | 14% (was 10%) | 13% (was 7%) |
| Ashleigh | 20% | 14% (was 7%) | 16% (was 5%) |
| Sable | 16% | 18% (was 13%) | 14% (was 6%) |

How they fight at Level 3 (attack is Skill Total for damage; Beornhard's
War Magic Lance is 9 for 10):

| Character | Health | Parry | Dodge | Vital | Mental | Vigilant | Speed | Reflex | Attack |
|---|---|---|---|---|---|---|---|---|---|
| Hilde | 13 | 17 | 13 | 16 | 12 | 13 | 5 | 5 | 9 for 10 |
| Browndog | 14 | 19 | 13 | 16 | 13 | 12 | 4 | 4 | 9 for 8 |
| Jackal | 10 | 13 | 17 | 14 | 14 | 14 | 5 | 6 | 10 for 6 |
| Beornhard | 10 | none | 14 | 14 | 15 | 13 | 4 | 5 | 9 for 8 |
| Hanforth | 10 | 16 | 15 | 14 | 14 | 15 | 4 | 7 | 8 for 7 |
| Carrick | 10 | 13 | 16 | 14 | 13 | 15 | 5 | 7 | 9 for 6 |
| Felix (proposed) | 10 | 18 | 17 | 14 | 12 | 11 | 5 | 3 | 11 for 5 |
| Enith (proposed) | 13 | 17 | 15 | 10 | 13 | 15 | 5 | 7 | 9 for 6 |
| Ashleigh (proposed) | 10 | 12 | 14 | 13 | 11 | 12 | 4 | 4 | 7 for 4 |
| Sable (proposed) | 10 | 14 | 16 | 12 | 11 | 15 | 6 | 7 | 11 for 7 |

And at Level 2 (Beornhard's Lance is 8 for 9):

| Character | Health | Parry | Dodge | Vital | Mental | Vigilant | Speed | Reflex | Attack |
|---|---|---|---|---|---|---|---|---|---|
| Hilde | 13 | 15 | 12 | 15 | 12 | 12 | 4 | 4 | 7 for 9 |
| Browndog | 10 | 16 | 12 | 15 | 12 | 12 | 3 | 4 | 6 for 8 |
| Jackal | 10 | 12 | 15 | 13 | 14 | 12 | 4 | 4 | 8 for 4 |
| Beornhard | 10 | none | 13 | 13 | 14 | 11 | 3 | 3 | 8 for 7 |
| Hanforth | 10 | 15 | 14 | 13 | 13 | 13 | 4 | 5 | 7 for 7 |
| Carrick | 10 | 12 | 15 | 12 | 12 | 14 | 4 | 6 | 8 for 5 |
| Felix (proposed) | 10 | 16 | 15 | 14 | 12 | 11 | 4 | 3 | 9 for 5 |
| Enith (proposed) | 10 | 15 | 14 | 10 | 12 | 15 | 4 | 7 | 7 for 6 |
| Ashleigh (proposed) | 10 | 12 | 14 | 13 | 11 | 11 | 4 | 3 | 7 for 3 |
| Sable (proposed) | 10 | 13 | 15 | 12 | 11 | 14 | 5 | 6 | 9 for 6 |

What stands out:

- **Mine are spikier than yours.** Felix and Sable hit at 11 by Level 3, and
  none of yours goes past 10. Felix's Parry 18 and Dodge 17 are near the top
  too. But their other Defenses are lower: Vital, Mental and Vigilant
  average 12.4 across my four at Level 3 against 13.9 across your six, and
  Enith's Vital 10 and Felix's Vigilant 11 and Reflex 3 are the lowest on the
  table. That's mostly the Stats, not this pass: your Level 3s spread 15-18
  Stat points with nothing below 2, while mine put 13-14 into one or two
  Stats and leave a 1 somewhere (Felix's Cunning, Enith's Body, Ashleigh's
  Mind, Sable's Body and Mind). Taking a Stat from 4 to 5 costs 10 XP, the
  same as taking a 1 to 3. The
  out-of-combat XP cost about a point on one or two Defenses each (Sable's
  Vigilant, Ashleigh's Mental and Vigilant, Enith's Vital and Dodge).
- **Less Health.** Your Level 3 front-liners bought Toughened Body (Hilde 13,
  Browndog 14); of mine only Enith has it now.
- **Ashleigh has the weakest block** (7 for 4, Mental 11), as a support
  character might. Jackal is the closest of yours, and Ashleigh trails her on
  every line but Health, where they tie.

If you'd rather they look like yours, the next step would be to take a point
off each one's top Stat and spread it into the 1s, keeping the side
interests where they are.

## How they do in the sim

Your two Level 1 test parties, at Levels 2 and 3 (200 fights a mix, the
calibrate settings). Party S is Enith, Felix, Jackal and Hanforth; Party U is
Browndog, Ashleigh, Sable and Beornhard. Jackal, Hanforth, Browndog and
Beornhard are your own builds.

| Party | Rounds | Losses | Someone Down | Someone Wounded |
|---|---|---|---|---|
| S, Level 1 (your builds) | 3.9 | 2.1% | 37% | 76% |
| S, Level 2 | 3.9 | 1.5% | 42% | 78% |
| S, Level 3 | 4.3 | 3.0% | 48% | 79% |
| U, Level 1 (your builds) | 2.9 | 0.1% | 16% | 38% |
| U, Level 2 | 2.4 | 0.1% | 13% | 33% |
| U, Level 3 | 2.6 | 0.8% | 22% | 65% |

Against the first pass, on the same fights (500 a mix, paired):

| Party | Rounds | Someone Down | Health left (% of max) |
|---|---|---|---|
| S, Level 2 | -0.29 ±0.05 | -5.3 ±1.6 | +1.8 ±0.7 |
| S, Level 3 | -0.25 ±0.06 | -1.6 ±1.4 | +1.6 ±0.7 |
| U, Level 2 | +0.04 ±0.01 | +0.8 ±0.6 | -0.9 ±0.2 |
| U, Level 3 | +0.04 ±0.03 | +0.8 ±1.4 | -2.4 ±0.4 |

Party U is a little worse off, as expected: Sable lost Toughened Body and
Ashleigh lost Forward! and her Insight and Composure ranks. Party S came out *better*, which
surprised me. Swapping one piece back at a time (Level 2, 500 a mix) found
it: putting Feint back costs the party 0.24 rounds (±0.04), +5.8 points of
someone Down (±1.3) and -3.4 Health left (±0.5), while putting Bark Turns the
Blade back is worth +1.2 Health left (±0.4).

How often the new Techniques get used, per fight (160 fights each):

- Party S, Level 3: Swallow Skims the Water 2.0, Willow Springs Back 1.9,
  Sickness Takes the Flock 0.8, Hand Rings the Bell 0.3, Magehunter 0.3,
  Spellblade 0.2.
- Party U, Level 3: Suppressing Fire 2.3, Blinkstep 0.3, Rally to Victory
  0.2, Cry of Victory 0.1, Ricochet Shot 0.03, Bolstering Refrain 0.01.
  Heroic Inspiration came up 0.1 a fight at Level 2 and not at all at
  Level 3.

What that says:

- **The sim plays Feint badly.** It spends Feint on Enith's first weapon
  attack every fight. That attack deals no damage, and the Harried it puts on
  only pays off if the rest of the party hits the same enemy, which the sim's
  targeting doesn't arrange. Whether Feint is weak or the sim's timing is
  wrong is still open.
- **Ashleigh's support kit barely gets used.** Bolstering Refrain needs three
  hurt allies with one Wounded, and Heroic Inspiration needs two allies with
  enemies on them; in 2.5-round fights that seldom happens. Either my rules
  are too strict, or she wants the longer fights (enemy Health x1.75 or x2) to
  show what she's worth.
- **Ricochet Shot hardly fires**: it needs a second enemy next to the first,
  and the sim's enemies don't bunch up much.
- **The sim doesn't enforce one Style at a time.** No current sample knows two,
  so nothing's moved so far, but it should pick one (or switch) before a
  build carries two.
