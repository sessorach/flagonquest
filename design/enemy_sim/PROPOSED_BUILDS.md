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

How they were made:

- **XP**: exactly 125 (Level 2) and 175 (Level 3), by the rulebook's costs (a
  Skill rank costs its new rank, a Stat point twice its new rank, a Technique
  three times its Level).
- **Rank cap**: 4 at Level 2 and 5 at Level 3, the most your own Level 2 and 3
  exports go to (the rulebook only states the 3 at creation).
- **Checked**: every Prereq Check, every Feature budget, and that the sim
  loads it. Spending roughly follows your own builds' split: about 40% of the
  new XP on Stats, 30% Skills, 30% Techniques.
- **One Style each**: the glossary's "you may only be in one Style at a time".
  The sim doesn't enforce that yet (it plays every Style a character knows),
  so where a character switches Styles, the one she doesn't fight in is in the
  row's Unmodeled column.
- **Picks lean towards Techniques the sim plays that no sample carries yet**,
  so each build also tells us something new.

## Felix (Monk, unarmed)

Level 2: more of what he already does. Sickness Takes the Flock puts
Vulnerable and Necrotic on a target (no sample character puts Necrotic on
enemies yet),
Hand Rings the Bell is his Slowing strike against Mental, and Bark Turns the
Blade is a 2 AP Interrupt when he's hit, the first real test of every
character holding AP between turns. Body and Essence up for his punch and
Meditation; Resilience 3 opens Toughened Body later.

**Felix (L2, proposed)** (44 Stats + 45 Skills + 36 Techniques = 125 XP)

- Stats: Agility 3, Body 3 (+1), Cunning 1, Mind 2, Essence 3 (+1)
- Skills: Acrobatics 2 (+2), Brawl 4 (+1), Stealth 2, Awareness 2 (+1), Might 1, Resilience 3 (+2), Insight 2, Composure 2 (+1), Meditation 4 (+1), Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2) **new**; Great Old Oak School - Bark Turns the Blade (L2) **new**; Shugen School - Hand Rings the Bell (L2) **new**
- In a fight: Health 10, Parry 16, Dodge 15, Vital 14, Mental 12, Vigilant 11, Speed 4, Reflex 3; Unarmed attack 9 for 5 Physical

Level 3: Swallow Skims the Water teleports him next to a target and strikes
its Mental Defense, the gap-closer a melee skirmisher wants, and Willow
Springs Back spends AP he has left at the end of a turn to get an Encounter
use back. In the sim, Willow gets a use back about twice a fight, and Swallow (which
he knows once) gets cast about twice. Toughened Body takes him from 10 to 13 Health; your own
Level 3 front-liners all bought Health.

**Felix (L3, proposed)** (60 Stats + 55 Skills + 60 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 3, Cunning 1, Mind 2, Essence 4 (+1)
- Skills: Acrobatics 2, Brawl 5 (+1), Stealth 2, Awareness 2, Might 1, Resilience 3, Insight 2, Composure 2, Meditation 5 (+1), Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2); Great Old Oak School - Bark Turns the Blade (L2); Shugen School - Hand Rings the Bell (L2); Shugen School - Swallow Skims the Water (L3) **new**; Great Old Oak School - Willow Springs Back (L3) **new**; Toughened Body (L2) **new**
- In a fight: Health 13, Parry 18, Dodge 17, Vital 14, Mental 12, Vigilant 11, Speed 5, Reflex 3; Unarmed attack 11 for 5 Physical

Alternatives worth a look: Spirit Hands (Level 3 Style, his Unarmed attacks
against Mental for Brilliant damage) instead of Boughs Unbroken; Blood-Powered
Spirit, though it about broke even for him in yesterday's test.

## Enith (Duelist, your Warlock stand-in)

Level 2: Spellblade, which spends her War Magic uses on weapon hits (Bleeding
[3 x Level]); Feint (her first weapon attack against Vigilant, Harried on a
hit) and Magehunter (an Interrupt on enemy casters). Agility, Cunning and
Essence up for her blade and Sorcery.

**Enith (L2, proposed)** (44 Stats + 51 Skills + 30 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 1, Cunning 3 (+1), Mind 2, Essence 3 (+1)
- Skills: Acrobatics 3 (+1), Melee 3 (+1), Stealth 1, Awareness 2 (+1), Might 2, Resilience 2 (+1), Insight 4 (+1), Persuasion 2, Academics 2 (+1), Composure 2, Sorcery 4 (+1)
- Techniques: Soulblade (L1); Temper Soulblade (L1); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2) **new**; Magehunter (L1) **new**; Feint (L1) **new**
- In a fight: Health 10, Parry 15, Dodge 14, Vital 11, Mental 12, Vigilant 15, Speed 4, Reflex 7; 1H Light Melee attack 7 for 6 Physical

Level 3: a Level 3 War Magic copy built for damage (Lance, Destructive 3),
Toughened Body, and Parting Shot. My first draft made that copy another hex
(Corrupting 4 with Piercing Elements): all control and no damage, like her
other two. With it her parties ran long, so I tried the damage copy in the
same party (with Browndog, Jackal and Hanforth, at enemy Health x1.75): +10.7% wins (±3.2), +4.1
Health left, 0.3 rounds shorter. The hex version is a fine pick if you want
her purely as the controller.

**Enith (L3, proposed)** (60 Stats + 67 Skills + 48 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 1, Cunning 3, Mind 2, Essence 4 (+1)
- Skills: Acrobatics 4 (+1), Melee 4 (+1), Stealth 1, Awareness 2, Might 2, Resilience 2, Insight 4, Persuasion 2, Academics 2, Composure 3 (+1), Sorcery 5 (+1)
- Techniques: Soulblade (L1); Temper Soulblade (L1); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2); Magehunter (L1); Feint (L1); War Magic (L3: Lance, Destructive 3) **new**; Toughened Body (L2) **new**; Parting Shot (L1) **new**
- In a fight: Health 13, Parry 17, Dodge 16, Vital 11, Mental 13, Vigilant 15, Speed 5, Reflex 7; 1H Light Melee attack 9 for 6 Physical

Worth knowing: Body 1 leaves her Vital Defense at 11, the lowest of the four.
Eternal Riposte and Exploit the Opening fit her well, but they're Styles, and
she already has Hand of Chaos.

## Ashleigh (Leader, bard)

Level 2: Heroic Inspiration (party-wide Protected), Forward! (her Style:
Hasted to allies within 3 meters at the start of her turn) and Cry of Victory
(Frightens nearby enemies when she Downs one). Essence for Performance, Body
for Presence, Agility for her thrown weapon.

**Ashleigh (L2, proposed)** (48 Stats + 44 Skills + 33 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 3 (+1), Cunning 1, Mind 1, Essence 4 (+1)
- Skills: Acrobatics 3 (+1), Stealth 1, Awareness 1, Might 1, Presence 4 (+1), Resilience 2 (+1), Insight 2 (+1), Composure 2, Performance 4 (+1), Rapport 3
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2) **new**; Forward! (L1) **new**; Cry of Victory (L2) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 13, Mental 11, Vigilant 11, Speed 4, Reflex 3; Light Thrown attack 7 for 3 Physical, range 9

Level 3: Bolstering Refrain (heals up to [half Performance] allies) and Rally
to Victory (Level 4: allies Sift and swap out low cards). Essence 5 makes
Performance 10.

**Ashleigh (L3, proposed)** (62 Stats + 59 Skills + 54 Techniques = 175 XP)

- Stats: Agility 3, Body 3, Cunning 2 (+1), Mind 1, Essence 5 (+1)
- Skills: Acrobatics 3, Stealth 1, Awareness 1, Might 1, Presence 4, Resilience 2, Insight 3 (+1), Composure 3 (+1), Performance 5 (+1), Rapport 4 (+1)
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2); Forward! (L1); Cry of Victory (L2); Bolstering Refrain (L3) **new**; Rally to Victory (L4) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 13, Mental 12, Vigilant 13, Speed 4, Reflex 5; Light Thrown attack 7 for 4 Physical, range 9

Worth knowing: in the sim her new support Techniques seldom fire (numbers
below). Party U's fights are short (2.5 rounds), and my rules for when to cast
them are cautious, so this says more about the rules than about her.
Command the Tempo (Level 3 Style) is the alternative to Forward!.

## Sable (Deadeye, bow)

Level 2: a Battle Maneuver (Calculated and Wing Clip 3: Good Luck, then
Crippled on a hit), Blinkstep (a free Shift, to keep her distance), and
Toughened Body. Agility and Cunning up for the bow.

**Sable (L2, proposed)** (42 Stats + 47 Skills + 36 Techniques = 125 XP)

- Stats: Agility 4 (+1), Body 1, Cunning 3 (+1), Mind 1, Essence 2 (+1)
- Skills: Acrobatics 3 (+1), Archery 4 (+1), Stealth 2, Athletics 1 (+1), Awareness 3 (+1), Might 2, Resilience 3 (+1), Insight 3, Persuasion 2, Composure 2
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3) **new**; Blinkstep (L2) **new**; Toughened Body (L2) **new**
- In a fight: Health 13, Parry 13, Dodge 15, Vital 12, Mental 11, Vigilant 14, Speed 5, Reflex 6; Light Bow attack 9 for 6 Physical, range 19

Level 3: Suppressing Fire (Style: every bow shot Cripples the target, hit or
miss), and a second Maneuver with Ricochet Shot (an extra target next to the
first). She'd switch from Hand of Chaos to Suppressing Fire, so the sim plays
that one.

**Sable (L3, proposed)** (60 Stats + 61 Skills + 54 Techniques = 175 XP)

- Stats: Agility 5 (+1), Body 1, Cunning 4 (+1), Mind 1, Essence 2
- Skills: Acrobatics 4 (+1), Archery 5 (+1), Stealth 2, Athletics 1, Awareness 3, Might 2, Resilience 3, Insight 4 (+1), Persuasion 2, Survival 1 (+1), Composure 2
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3); Blinkstep (L2); Toughened Body (L2); Suppressing Fire (L3) **new**; Battle Maneuver (L3: Ricochet Shot, Calculated, Wing Clip) **new**
- In a fight: Health 13, Parry 14, Dodge 17, Vital 12, Mental 11, Vigilant 16, Speed 6, Reflex 8; Light Bow attack 11 for 7 Physical, range 19
- The sim leaves out: Hand of Chaos (she fights in her other Style)

Alternatives: Deadeye's Shadow (Level 2 Style: Taunts on her hits) would test
whether an archer can draw attacks, but she's on 13 Health at the back.

## How they do in the sim

Your two Level 1 test parties, at Levels 2 and 3 (200 fights a mix, the
calibrate settings). Party S is Enith, Felix, Jackal and Hanforth; Party U is
Browndog, Ashleigh, Sable and Beornhard. Jackal, Hanforth, Browndog and
Beornhard are your own builds.

| Party | Rounds | Losses | Someone Down | Someone Wounded |
|---|---|---|---|---|
| S, Level 1 (your builds) | 3.9 | 2.1% | 37% | 76% |
| S, Level 2 | 4.3 | 3.2% | 48% | 80% |
| S, Level 3 | 4.5 | 3.5% | 50% | 80% |
| U, Level 1 (your builds) | 2.9 | 0.1% | 16% | 38% |
| U, Level 2 | 2.4 | 0.0% | 12% | 34% |
| U, Level 3 | 2.5 | 0.2% | 21% | 63% |

Party S was already the fragile one at Level 1: no front-liner. Felix isn't
the problem: with Hilde in Enith's place his Level 2 party never lost
(someone Down 14%). Party U's Level 3 fights go Wounded more often than at
Level 2, against the tougher Level 3 encounters.

How often the new Techniques get used, per fight (160 fights each):

- Party S, Level 3: Swallow Skims the Water 2.0, Willow Springs Back 2.0,
  Sickness Takes the Flock 0.8, Feint 0.8, Hand Rings the Bell 0.4,
  Spellblade 0.3, Magehunter 0.3, Bark Turns the Blade 0.3, Parting Shot 0.2.
- Party U, Level 3: Suppressing Fire 2.3, Forward! 1.7, Rally to Victory 0.3,
  Blinkstep 0.3, Cry of Victory 0.1, Ricochet Shot 0.01, Bolstering Refrain
  never. Heroic Inspiration came up 0.1 a fight at Level 2 and not at all
  at Level 3.

What that says:

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
