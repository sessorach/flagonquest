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

This is the third pass, all on 2026-10-28. The first put nearly every point
into fighting; the second moved 10-20% of each level-up into side interests;
this one spreads the Stats the way your builds do. Both earlier passes are in
git (commits 111436b and e6a28fa).

How they were made:

- **XP**: exactly 125 (Level 2) and 175 (Level 3), by the rulebook's costs (a
  Skill rank costs its new rank, a Stat point twice its new rank, a Technique
  three times its Level).
- **Rank cap**: 4 at Level 2 and 5 at Level 3, the most your own Level 2 and 3
  exports go to (the rulebook only states the 3 at creation).
- **Stats like yours**: nothing below 2, 13 points at Level 2 and 15-16 at
  Level 3 (yours: 12-15 and 15-18).
- **Fewer Techniques, more Defense Skills**: your Level 3s spend 33-51 XP on
  Techniques and have 7-9 ranks across Resilience, Composure and Insight
  (the Skills behind Vital, Mental, Vigilant and Reflex). Mine now spend
  39-54 and have 7-9. Each character dropped the Technique that fired least
  in the sim.
- **Out of combat**: 12-18% of each build's XP, against 3-34% in yours.
- **Checked**: every Prereq Check, every Feature budget, and that the sim
  loads it.
- **One Style each**: the glossary's "you may only be in one Style at a time".
  The sim doesn't enforce that yet (it plays every Style a character knows),
  so where a character switches Styles, the one she doesn't fight in is in the
  row's Unmodeled column.

## Felix (Monk, unarmed)

Level 2: Sickness Takes the Flock (Vulnerable and Necrotic on a target) and
Pranic Nourishment, which fits a monk who meditates instead of sleeping.
Cunning up to 2, and Composure, Insight and Resilience ranks.

**Felix (L2, proposed)** (48 Stats + 47 Skills + 30 Techniques = 125 XP)

- Stats: Agility 3, Body 3 (+1), Cunning 2 (+1), Mind 2, Essence 3 (+1)
- Skills: Acrobatics 2 (+2), Brawl 4 (+1), Stealth 2, Awareness 1, Might 1, Resilience 3 (+2), Insight 3 (+1), Survival 1 (+1), Composure 2 (+1), Meditation 4 (+1), Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2) **new**; Pranic Nourishment (L2) **new**
- In a fight: Health 10, Parry 16, Dodge 15, Vital 14, Mental 12, Vigilant 13, Speed 4, Reflex 5; Unarmed attack 9 for 5 Physical

Level 3: Swallow Skims the Water teleports him next to a target and strikes
its Mental Defense, and Willow Springs Back spends AP he has left at the end
of a turn to get an Encounter use back. Stealth 3 and Shadow's Path build on
the Stealth 2 he started with (he's a cat).

**Felix (L3, proposed)** (70 Stats + 51 Skills + 54 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 3, Cunning 2, Mind 3 (+1), Essence 4 (+1)
- Skills: Acrobatics 2, Brawl 4, Stealth 3 (+1), Athletics 1 (+1), Awareness 1, Might 1, Resilience 3, Insight 3, Survival 1, Composure 2, Meditation 4, Rapport 2
- Techniques: Shugen School - Firefly Leaves the Hand (L1); Demon School - Thief Empties the Vessel (L2); Great Old Oak School - Boughs Unbroken (L2); Battle Maneuver (L1: Bare-Handed, Lunging 2, Half Guard 3); Demon School - Sickness Takes the Flock (L2); Pranic Nourishment (L2); Shugen School - Swallow Skims the Water (L3) **new**; Great Old Oak School - Willow Springs Back (L3) **new**; Shadow's Path (L2) **new**
- In a fight: Health 10, Parry 17, Dodge 16, Vital 14, Mental 13, Vigilant 13, Speed 5, Reflex 5; Unarmed attack 10 for 5 Physical

Alternatives: Hand Rings the Bell (his Slowing strike against Mental) was cut
here for the Defense ranks; it fired 0.3 times a fight. Bark Turns the Blade
(a 2 AP Interrupt when he's hit) instead of Pranic Nourishment leaves his
party 1.2 percentage points more of its Health a fight. Spirit Hands (Level 3
Style) instead of Boughs Unbroken.

## Enith (Duelist, your Warlock stand-in)

Level 2: Spellblade, which spends her War Magic uses on weapon hits (Bleeding
[3 x Level]), and Magehunter (an Interrupt on enemy casters). Body up to 2.
For the side: Persuasion 3, a rank of Survival (she's a Settler), and
Placeholder's Wizardly Witchlight.

**Enith (L2, proposed)** (48 Stats + 47 Skills + 30 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 2 (+1), Cunning 3 (+1), Mind 2, Essence 3 (+1)
- Skills: Acrobatics 3 (+1), Melee 3 (+1), Stealth 1, Awareness 1, Might 2, Resilience 1, Insight 3, Persuasion 3 (+1), Survival 1 (+1), Academics 2 (+1), Composure 2, Sorcery 4 (+1)
- Techniques: Soulblade (L1: Light One-Handed Melee Weapon); Temper Soulblade (L1: Fatestealer); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2) **new**; Magehunter (L1) **new**; Placeholder's Wizardly Witchlight (L1) **new**
- In a fight: Health 10, Parry 15, Dodge 14, Vital 11, Mental 12, Vigilant 14, Speed 4, Reflex 6; 1H Light Melee attack 7 for 6 Physical

Level 3: a Level 3 War Magic copy built for damage (Lance, Destructive 3),
plus Mind 3, Resilience 2, and Academics, Stealth and Survival. In the first
pass the damage copy beat a third hex (Corrupting 4 with Piercing Elements)
by +10.7% wins (±3.2) at enemy Health x1.75; the hex is a fine pick if you
want her purely as the controller. Toughened Body is out (she's at 10
Health), to pay for the Stats.

**Enith (L3, proposed)** (70 Stats + 66 Skills + 39 Techniques = 175 XP)

- Stats: Agility 4 (+1), Body 2, Cunning 3, Mind 3 (+1), Essence 4 (+1)
- Skills: Acrobatics 3, Melee 4 (+1), Stealth 2 (+1), Athletics 1 (+1), Awareness 1, Might 2, Resilience 2 (+1), Insight 3, Persuasion 3, Survival 2 (+1), Academics 3 (+1), Composure 2, Sorcery 5 (+1)
- Techniques: Soulblade (L1: Light One-Handed Melee Weapon); Temper Soulblade (L1: Fatestealer); Hand of Chaos (L2); War Magic (L1: Tormenting Curse, Lance, Frigid 3); War Magic (L1: Tormenting Curse, Lance, Kinetic 3); Spellblade (L2); Magehunter (L1); Placeholder's Wizardly Witchlight (L1); War Magic (L3: Lance, Destructive 3) **new**
- In a fight: Health 10, Parry 17, Dodge 15, Vital 12, Mental 13, Vigilant 14, Speed 5, Reflex 6; 1H Light Melee attack 9 for 6 Physical

## Ashleigh (Leader, bard)

Level 2: Heroic Inspiration (party-wide Protected) and Cry of Victory
(Frightens nearby enemies when she Downs one), plus Profession as a Busker,
which is what a bard does between adventures. Cunning and Mind up to 2,
Essence for Performance.

**Ashleigh (L2, proposed)** (50 Stats + 42 Skills + 33 Techniques = 125 XP)

- Stats: Agility 3 (+1), Body 2, Cunning 2 (+1), Mind 2 (+1), Essence 4 (+1)
- Skills: Acrobatics 3 (+1), Stealth 1, Awareness 1, Might 1, Presence 4 (+1), Resilience 2 (+1), Insight 1, Composure 2, Performance 4 (+1), Rapport 3
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2) **new**; Profession (L1: Busker) **new**; Cry of Victory (L2) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 12, Mental 12, Vigilant 11, Speed 4, Reflex 3; Light Thrown attack 7 for 4 Physical, range 6

Level 3: Rally to Victory (Level 4: allies Sift and swap out low cards) and A
Perfectly Good Explanation, a social Technique for the party's talker, plus
Body 3, Essence 5, Resilience and Composure 3, and Insight from 1 to 3.
Bolstering Refrain was cut for those ranks; it fired 0.01 times a fight.

**Ashleigh (L3, proposed)** (66 Stats + 58 Skills + 51 Techniques = 175 XP)

- Stats: Agility 3, Body 3 (+1), Cunning 2, Mind 2, Essence 5 (+1)
- Skills: Acrobatics 3, Stealth 1, Awareness 1, Might 1, Presence 4, Resilience 3 (+1), Insight 3 (+2), Composure 3 (+1), Performance 5 (+1), Rapport 3
- Techniques: Raise Spirits (L4); Favorite Face (L2); Heroic Inspiration (L2); Profession (L1: Busker); Cry of Victory (L2); Rally to Victory (L4) **new**; A Perfectly Good Explanation (L2) **new**
- In a fight: Health 10, Parry 12, Dodge 14, Vital 14, Mental 13, Vigilant 13, Speed 4, Reflex 5; Light Thrown attack 7 for 4 Physical, range 9

Alternatives: Forward! (her Style, Hasted to nearby allies) instead of
Profession; it fired 1.7 times a fight in the first pass, but I haven't
measured it on its own.

## Sable (Deadeye, bow)

Level 2: a Battle Maneuver (Calculated and Wing Clip 3: Good Luck, then
Crippled on a hit), Stealth 3 and Shadow's Path, and a rank of Survival.
Agility and Cunning up, and Body, Mind and Essence up to 2.

**Sable (L2, proposed)** (50 Stats + 45 Skills + 30 Techniques = 125 XP)

- Stats: Agility 4 (+1), Body 2 (+1), Cunning 3 (+1), Mind 2 (+1), Essence 2 (+1)
- Skills: Acrobatics 3 (+1), Archery 4 (+1), Stealth 3 (+1), Athletics 1 (+1), Awareness 2, Might 2, Resilience 2, Insight 3, Persuasion 2, Survival 1 (+1), Composure 2
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3) **new**; Shadow's Path (L2) **new**
- In a fight: Health 10, Parry 13, Dodge 15, Vital 12, Mental 12, Vigilant 14, Speed 5, Reflex 6; Light Bow attack 9 for 6 Physical, range 19

Level 3: Suppressing Fire (Style: every bow shot Cripples the target, hit or
miss), and a second Maneuver with Ricochet Shot (an extra target next to the
first). She'd switch from Hand of Chaos to Suppressing Fire, so the sim plays
that one. Body and Essence to 3, Survival 3 for tracking and a rank of
Streetwise; Blinkstep was cut for Resilience and Composure (it fired 0.3
times a fight).

**Sable (L3, proposed)** (62 Stats + 65 Skills + 48 Techniques = 175 XP)

- Stats: Agility 4, Body 3 (+1), Cunning 3, Mind 2, Essence 3 (+1)
- Skills: Acrobatics 3, Archery 5 (+1), Stealth 3, Athletics 1, Awareness 3 (+1), Might 2, Resilience 3 (+1), Insight 3, Persuasion 2, Streetwise 1 (+1), Survival 3 (+2), Composure 3 (+1)
- Techniques: Hand of Chaos (L2); Perfect Strike (L2); One Eye Behind You (L2); Battle Maneuver (L2: Calculated, Wing Clip 3); Shadow's Path (L2); Suppressing Fire (L3) **new**; Battle Maneuver (L3: Ricochet Shot, Calculated, Wing Clip) **new**
- In a fight: Health 10, Parry 13, Dodge 15, Vital 14, Mental 13, Vigilant 14, Speed 5, Reflex 6; Light Bow attack 10 for 6 Physical, range 19
- The sim leaves out: Hand of Chaos (she fights in her other Style)

Alternatives: Wisdom of the Woods (needs Survival 3, which she now has) is
the next ribbon on her list. Deadeye's Shadow (Level 2 Style: Taunts on her
hits) would test whether an archer can draw attacks, but she's on 10 Health
at the back.

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
| Felix | 11% | 12% | 14% |
| Enith | 16% | 14% | 13% |
| Ashleigh | 20% | 14% | 14% |
| Sable | 16% | 18% | 15% |

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
| Felix (proposed) | 10 | 17 | 16 | 14 | 13 | 13 | 5 | 5 | 10 for 5 |
| Enith (proposed) | 10 | 17 | 15 | 12 | 13 | 14 | 5 | 6 | 9 for 6 |
| Ashleigh (proposed) | 10 | 12 | 14 | 14 | 13 | 13 | 4 | 5 | 7 for 4 |
| Sable (proposed) | 10 | 13 | 15 | 14 | 13 | 14 | 5 | 6 | 10 for 6 |

And at Level 2 (Beornhard's Lance is 8 for 9):

| Character | Health | Parry | Dodge | Vital | Mental | Vigilant | Speed | Reflex | Attack |
|---|---|---|---|---|---|---|---|---|---|
| Hilde | 13 | 15 | 12 | 15 | 12 | 12 | 4 | 4 | 7 for 9 |
| Browndog | 10 | 16 | 12 | 15 | 12 | 12 | 3 | 4 | 6 for 8 |
| Jackal | 10 | 12 | 15 | 13 | 14 | 12 | 4 | 4 | 8 for 4 |
| Beornhard | 10 | none | 13 | 13 | 14 | 11 | 3 | 3 | 8 for 7 |
| Hanforth | 10 | 15 | 14 | 13 | 13 | 13 | 4 | 5 | 7 for 7 |
| Carrick | 10 | 12 | 15 | 12 | 12 | 14 | 4 | 6 | 8 for 5 |
| Felix (proposed) | 10 | 16 | 15 | 14 | 12 | 13 | 4 | 5 | 9 for 5 |
| Enith (proposed) | 10 | 15 | 14 | 11 | 12 | 14 | 4 | 6 | 7 for 6 |
| Ashleigh (proposed) | 10 | 12 | 14 | 12 | 12 | 11 | 4 | 3 | 7 for 4 |
| Sable (proposed) | 10 | 13 | 15 | 12 | 12 | 14 | 5 | 6 | 9 for 6 |

What changed with this pass:

- **Their best attack is 10 now**, like yours (Felix and Sable were at 11).
- **Vital, Mental and Vigilant average 13.3** across my four at Level 3,
  against 13.9 across your six (12.4 in the second pass). At Level 2 it's
  12.4 against 12.9. No Defense of theirs is below 12 at Level 3.
- **Health is 10 for all four.** Your front-liners have 13-14; none of these
  four is a front-liner, and Toughened Body was the first thing to go when
  the Stats needed paying for.
- **Spreading the Stats alone did little**: when I first paid for them out of
  Insight, Composure and Resilience ranks, the Defenses barely moved (12.75
  at Level 3), since those ranks feed the same Defenses. What closed most of
  the difference was taking one Technique off each of Felix, Ashleigh and
  Sable and putting it into those Skills.

## How they do in the sim

Your two Level 1 test parties, at Levels 2 and 3 (200 fights a mix, the
calibrate settings). Measured before the Assassin tactic changed later on
2026-10-28 (TECHNIQUE_PASS.md), which made Level 1-2 fights rougher. Party S is Enith, Felix, Jackal and Hanforth; Party U is
Browndog, Ashleigh, Sable and Beornhard. Jackal, Hanforth, Browndog and
Beornhard are your own builds.

| Party | Rounds | Losses | Someone Down | Someone Wounded |
|---|---|---|---|---|
| S, Level 1 (your builds) | 3.9 | 2.1% | 37% | 76% |
| S, Level 2 | 3.9 | 1.4% | 38% | 74% |
| S, Level 3 | 4.1 | 3.9% | 51% | 80% |
| U, Level 1 (your builds) | 2.9 | 0.1% | 16% | 38% |
| U, Level 2 | 2.5 | 0.1% | 11% | 33% |
| U, Level 3 | 2.6 | 0.5% | 22% | 62% |

Against the second pass, on the same fights (500 a mix, paired), the spread
builds come out about even: Party S does a little better at Level 2 (someone
Down -4.2 points, ±2.4) and a little worse at Level 3 (-2.2 points of
Health left, ±1.1); Party U doesn't move outside the noise.

How often the new Techniques get used, per fight (160 fights each):

- Party S, Level 3: Willow Springs Back 1.9, Swallow Skims the Water 1.9,
  Sickness Takes the Flock 0.7, Spellblade 0.2, Magehunter 0.2.
- Party U, Level 3: Suppressing Fire 2.4, Rally to Victory 0.3, Cry of
  Victory 0.1, Ricochet Shot 0.03. Heroic Inspiration came up 0.1 a fight
  at Level 2 and almost never at Level 3.

## Feint as a setup

You said Feint only works aimed at setting up a target for the party to
Gamble and wallop, so the sim now plays it that way (`tunables.FEINT_SETUP`,
on by default). Enith only Feints when at least two allies who act before
the target's next turn can attack it against Parry or Dodge, and a Feint that
hits "calls" the target: those allies go for it, and they already Gamble
harder against the lower Defense. Before, she Feinted on her first swing of
every fight.

Tested on Enith (L2, proposed) with Feint in place of Magehunter, Party S,
500 fights a mix, paired against the build without it. Health left is in
percentage points of the party's max Health:

| How she plays it | Health left vs no Feint | Feints a fight | Ally attacks on the target before its turn |
|---|---|---|---|
| First swing (the old play) | -3.5 ±0.5 | 0.85 | 0.82 |
| Wait for 1 ally, and call | -2.2 ±0.4 | 0.71 | 0.85 |
| Wait for 2 allies, no call | -1.3 ±0.3 | 0.52 | 0.71 |
| Wait for 2 allies, and call (the default) | -1.3 ±0.3 | 0.52 | 0.72 |
| Wait for 3 allies, and call | -0.7 ±0.2 | 0.27 | 0.40 |

Waiting helps a lot, and calling the target adds nothing measurable (the
allies who can reach it mostly attack it anyway). But Feint still costs the
party at every setting, and costs less the less she uses it. The reason:
Harried clears at the end of the target's own turn, so after a Feint hits
only about 1.6 ally attacks go at the target before it's gone, and those
attacks hit about 89% of the time, lowered Defense included. The Harried mostly turns
into a bit of extra Gambling damage, which is less than the damaging swing
Enith gives up to make the Feint. So the proposals leave it out.

If you want Feint to pay, the levers are the ones that rule sets: more
attacks inside the window (Harried that lasts until the end of the round, or
until the target's next turn ends), more value per attack (Feint also deals
its damage, or adds a Bad Luck), or a cheaper cost (0 AP, or Feint as part of
another attack). I haven't tested any of those; say which you'd like to see.

## Other findings

- **Ashleigh's support kit barely gets used.** Heroic Inspiration needs two
  allies with enemies on them, and Bolstering Refrain (cut this pass) needed
  three hurt allies with one Wounded; in 2.5-round fights that seldom
  happens. Either my rules are too strict, or she wants the longer fights
  (enemy Health x1.75 or x2) to show what she's worth.
- **Ricochet Shot hardly fires**: it needs a second enemy next to the first,
  and the sim's enemies don't bunch up much.
- **The sim doesn't enforce one Style at a time.** No current sample knows two,
  so nothing's moved so far, but it should pick one (or switch) before a
  build carries two.
