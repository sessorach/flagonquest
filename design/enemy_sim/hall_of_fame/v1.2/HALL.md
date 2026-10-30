# Hall of Fame, v1.2 (2026-10-30)

The first induction. Two optimizer runs searched every legal Level 2 and
Level 3 build for each of the ten sample characters (the character's
weapon, armor, background and row kept; every XP open). One run searched
on Health left after a fight, one on Health in the morning after a day.
Both runs' finalists were then ranked by the measure the designer picked
(RULES_DESIGN.md, "What the game is for"): **the toughest day the party
can still win half the time** with the build in its sample's place, as
an enemy Health multiplier. ×2.00 means enemies with twice their normal
Health. Each character gets its best build and then the best one with a
different set of Techniques: two different builds, not twins a rank
apart.

Each `.json` here is a Builder export (open it in the Builder's Import).
Its `simNotes` say what it scored and which search found it.

## The leaderboard

"Toughest day" is the enemy Health multiplier the party wins half its
days against, two fights and a night each (day_sim.py, threshold.py),
with the sample party's own in brackets. Two sets of fights read about
4% apart, so a gain of a few percent says little on its own.

| Character | Lv | # | Name | Toughest day (sample) | Max Health (sample) | Found by | What it takes |
|---|---|---|---|---|---|---|---|
| Hilde | 3 | 1 | [Valkyrie Grimsdottir, the Unbroken](hilde_l3_1.json) | ×2.19, +44% (×1.52) | 21 (13) | one fight | Battle Maneuver ×2, Toughened Resolve ×2, Earthen Mantle Approach, Force Missiles, Lifeline, Toughened Body; Essence 5 |
| Hilde | 3 | 2 | [Ragnhild Stormbreaker](hilde_l3_2.json) | ×2.15, +41% (×1.52) | 21 (13) | one fight | Battle Maneuver ×2, Toughened Resolve ×2, Earthen Mantle Approach, Lifeline, Toughened Body; Essence 5 |
| Hilde | 2 | 1 | [Brunhilde Doomhammer](hilde_l2_1.json) | ×2.14, +4% (×2.07) | 29 (13) | one fight | Toughened Resolve ×4, Battle Maneuver, Brace, Lend Bulwark, Toughened Body; Essence 3 |
| Browndog | 3 | 1 | [Sir Gallant Grimhelm](browndog_l3_1.json) | ×1.73, +12% (×1.54) | 26 (14) | a day | Toughened Resolve ×4, Battle Maneuver ×2, Bolstering Refrain, Heroic Inspiration, Second Wind; Essence 4 |
| Browndog | 3 | 2 | [Magnus Dreadbulwark](browndog_l3_2.json) | ×1.68, +9% (×1.54) | 22 (14) | one fight | Battle Maneuver ×3, Toughened Resolve ×3, Brace, Magehunter, Parting Shot; Essence 2 |
| Browndog | 2 | 1 | [Gunnar Steelfang](browndog_l2_1.json) | ×2.37, +15% (×2.05) | 26 (10) | one fight | Toughened Resolve ×4, Battle Maneuver; Essence 4 |
| Browndog | 2 | 2 | [Brutus Ironwolf](browndog_l2_2.json) | ×2.36, +15% (×2.05) | 26 (10) | one fight | Toughened Resolve ×4, Battle Maneuver, Eagle Eyes; Essence 4 |
| Jackal | 3 | 1 | [Ashen Vex](jackal_l3_1.json) | ×2.24, +51% (×1.48) | 14 (10) | one fight | Battle Maneuver ×2, One Eye Behind You, Suppressing Fire, Toughened Resolve; Essence 3 |
| Jackal | 3 | 2 | [Scar Whitlock](jackal_l3_2.json) | ×2.08, +40% (×1.48) | 18 (10) | a day | Toughened Resolve ×2, Battle Maneuver, Eagle Eyes, Lay On Hands; Essence 2 |
| Jackal | 2 | 1 | [Syd Ravage](jackal_l2_1.json) | ×1.94, +17% (×1.66) | 22 (10) | a day | Toughened Resolve ×3, Healing Magic; Essence 4 |
| Jackal | 2 | 2 | [Damien Thornwood](jackal_l2_2.json) | ×1.75, +6% (×1.66) | 22 (10) | one fight | Toughened Resolve ×3, Field Medic; Essence 3 |
| Carrick | 3 | 1 | [Zero Kurogane](carrick_l3_1.json) | ×2.19, +43% (×1.52) | 18 (10) | one fight | Toughened Resolve ×2, Arrow Finds Only Mist, Battle Maneuver, Eagle Eyes, Lifeline, One Eye Behind You, Placeholder's Alacritous Adaptation, Second Wind; Essence 2 |
| Carrick | 3 | 2 | [Raze Kurogane](carrick_l3_2.json) | ×2.13, +40% (×1.52) | 18 (10) | one fight | Toughened Resolve ×2, Arrow Finds Only Mist, Battle Maneuver, Bladeslinging, Eagle Eyes, Lifeline, One Eye Behind You, Placeholder's Alacritous Adaptation, Second Wind; Essence 2 |
| Carrick | 2 | 1 | [Shade Vantablack](carrick_l2_1.json) | ×2.73, +32% (×2.07) | 30 (10) | a day | Toughened Resolve ×5, Lifeline, Second Wind; Essence 4 |
| Carrick | 2 | 2 | [Kage Nightwhisper](carrick_l2_2.json) | ×2.62, +27% (×2.07) | 22 (10) | one fight | Toughened Resolve ×3; Essence 4 |
| Felix | 3 | 1 | [Kenji Shadowfist](felix_l3_1.json) | ×2.06, +39% (×1.48) | 22 (10) | a day | Toughened Resolve ×3, Battle Maneuver, Grim Resolve, Lay On Hands, Swallow Skims the Water; Essence 5 |
| Felix | 3 | 2 | [Daisuke Kurotora](felix_l3_2.json) | ×2.00, +35% (×1.48) | 22 (10) | a day | Toughened Resolve ×3, Battle Maneuver, Grim Resolve, Lay On Hands, Swallow Skims the Water; Essence 5 |
| Felix | 2 | 1 | [Ryu Kaminari](felix_l2_1.json) | ×2.34, +41% (×1.66) | 14 (10) | one fight | Battle Maneuver, Brace, Spirit Hands, Swallow Skims the Water, Toughened Resolve; Essence 4 |
| Felix | 2 | 2 | [Jin Kazekiri](felix_l2_2.json) | ×2.29, +38% (×1.66) | 14 (10) | one fight | Battle Maneuver, Spirit Hands, Swallow Skims the Water, Toughened Resolve; Essence 4 |
| Enith | 3 | 1 | [Kuroi Hime, Blade of the Frozen Eclipse](enith_l3_1.json) | ×2.04, +38% (×1.48) | 26 (10) | one fight | Toughened Resolve ×4, War Magic ×2, Inexhaustible Guardian, Placeholder's Wizardly Witchlight, Second Wind; Essence 5 |
| Enith | 3 | 2 | [Yuki Shiroyasha](enith_l3_2.json) | ×2.00, +35% (×1.48) | 26 (10) | one fight | Toughened Resolve ×4, War Magic ×2, Follow Through, Placeholder's Wizardly Witchlight; Essence 5 |
| Enith | 2 | 1 | [Lilith Frostbourne](enith_l2_1.json) | ×2.39, +44% (×1.66) | 22 (10) | one fight | Toughened Resolve ×3, Placeholder's Lengthy Ley-weaving, War Magic; Essence 4 |
| Enith | 2 | 2 | [Morrigan Ironheart](enith_l2_2.json) | ×1.95, +17% (×1.66) | 34 (10) | a day | Toughened Resolve ×6, Lifeline, Second Wind; Essence 3 |
| Sable | 3 | 1 | [Kite Shinobi](sable_l3_1.json) | ×2.16, +40% (×1.54) | 10 (10) | one fight | Battle Maneuver ×2, Hand of Chaos, Magehunter, One Eye Behind You, Solemn Pact; Essence 4 |
| Sable | 3 | 2 | [Kestrel Darkarrow](sable_l3_2.json) | ×2.13, +38% (×1.54) | 10 (10) | one fight | Battle Maneuver ×2, Hand of Chaos, Magehunter, One Eye Behind You, Solemn Pact; Essence 4 |
| Sable | 2 | 1 | [Artemis Nyx](sable_l2_1.json) | ×2.78, +35% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Battle Maneuver, Field Medic, Healing Magic; Essence 2 |
| Sable | 2 | 2 | [Diana Ravencroft](sable_l2_2.json) | ×2.70, +31% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Battle Maneuver, Field Medic, Healing Magic, One Eye Behind You; Essence 1 |
| Beornhard | 3 | 1 | [Archmage Kaelith Shadowbane](beornhard_l3_1.json) | ×2.44, +59% (×1.54) | 22 (10) | a day | Toughened Resolve ×3, Battle Maneuver, Healing Magic; Essence 5 |
| Beornhard | 3 | 2 | [Valdris the Unspoken](beornhard_l3_2.json) | ×2.41, +56% (×1.54) | 22 (10) | a day | Toughened Resolve ×3, Battle Maneuver, Force Missiles, Healing Magic; Essence 5 |
| Beornhard | 2 | 1 | [Malachai Darkfyre](beornhard_l2_1.json) | ×2.79, +36% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Firefly Leaves the Hand, Healing Magic, Overchanneling, War Magic; Essence 4 |
| Beornhard | 2 | 2 | [Zephyrus Vex](beornhard_l2_2.json) | ×2.73, +33% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Firefly Leaves the Hand, Healing Magic, Overchanneling, War Magic; Essence 4 |
| Hanforth | 3 | 1 | [Saint Lazarus Graves](hanforth_l3_1.json) | ×2.33, +57% (×1.48) | 34 (10) | one fight | Toughened Resolve ×6, Healing Magic, Lifeline, Lifeward, Minor Oracle; Essence 5 |
| Hanforth | 3 | 2 | [Cardinal Mortis](hanforth_l3_2.json) | ×2.22, +50% (×1.48) | 34 (10) | one fight | Toughened Resolve ×6, Healing Magic, Lifeline, Lifeward, Minor Oracle; Essence 4 |
| Hanforth | 2 | 1 | [Brother Requiem](hanforth_l2_1.json) | ×2.21, +33% (×1.66) | 14 (10) | one fight | Field Medic, Healing Magic, Minor Oracle, Spirit Blessing, Toughened Resolve; Essence 4 |
| Hanforth | 2 | 2 | [Father Absolution](hanforth_l2_2.json) | ×2.20, +33% (×1.66) | 14 (10) | one fight | Brace, Field Medic, Healing Magic, Minor Oracle, Toughened Resolve; Essence 4 |
| Ashleigh | 3 | 1 | [Seraph Ashenveil, the Requiem Unending](ashleigh_l3_1.json) | ×2.98, +93% (×1.54) | 30 (10) | one fight | Toughened Resolve ×5, Earthen Mantle Approach, Healing Magic, Heroic Inspiration, Lifeline; Essence 5 |
| Ashleigh | 3 | 2 | [Echo Vanitas](ashleigh_l3_2.json) | ×2.72, +76% (×1.54) | 18 (10) | a day | Toughened Resolve ×2, Battle Maneuver, Field Medic, Healing Magic, Lifeline, One Eye Behind You; Essence 5 |
| Ashleigh | 2 | 1 | [Ravenna Nightsong](ashleigh_l2_1.json) | ×2.60, +27% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Lay On Hands; Essence 3 |
| Ashleigh | 2 | 2 | [Lyric Bloodmoon](ashleigh_l2_2.json) | ×2.55, +24% (×2.05) | 26 (10) | a day | Toughened Resolve ×4, Lay On Hands, Overchanneling; Essence 4 |

Top of the board: **Seraph Ashenveil** (Ashleigh, Level 3), +93%. Five
Toughened Resolves, Earthen Mantle Approach, Lifeline and Healing Magic
with Triage, at Essence 5: 30 Health against the sample's 10, spent
keeping everyone else up.

## What nearly all of them do

Across the 39 builds:

- **Toughened Resolve, stacked.** 37 of 39 take it, three copies on
  average, as many as six (Hanforth and Enith, 34 Health at Level 2-3
  against the sample's 10). It's Duplicate, with no cap on copies. The
  two that skip it (Sable at Level 3) spend everything on not being hit.
- **Essence at or near the cap.** 24 of 39 max it, 8 more are one short.
  Only one sample (Ashleigh at Level 3) is at the cap; the rest sit at 2-4.
- **Lifeline next to the big pools.** 10 of 39, each on a build with 18
  to 34 Health (the samples have 10 to 14).
- **Agility and Body dumped.** 9 builds take Agility 1, 13 take Body 1;
  the samples never go below 2. In a fight, Essence and Health pay for
  themselves and Agility and Body don't seem to.
- **Cheap healing.** 25 of 39 pick up Healing Magic, Lay On Hands,
  Second Wind, Bolstering Refrain or Field Medic, mostly the ones the day
  search found.
- **Everything else goes.** The samples carry Rumormonger, Profession,
  Patch Up, Follower, Legerdemain and the like; these carry nothing that
  doesn't win a fight. Part of every gap here is that, which is a fair
  price for a character with a life outside fights (README.md, "What it
  isn't").

## Watch list (for the designer)

None of these are decisions, just what this pass turned up. Measured
singly on Hilde's party (TABLE_PLAY_NOTES.md, "Two kinds of measure"):

1. **Toughened Resolve stacking.** A copy is an ordinary buy, about
   0.4-0.6% tougher enemies per XP, but nothing stops a build taking six.
   Every copy also raises the Health-left and morning scores in full,
   which is why both searches leaned on it. Worth deciding whether
   Duplicate max-Health Techniques should have a cap or a rising cost.
2. **Essence.** +1 Essence measured 1.2-1.4% per XP, the best stat buy
   here even at twice its new rank in XP, and the builds treat it as
   mandatory. Resist against every damage type may be doing more than
   its price.
3. **Lifeline on a big pool.** Worth about +2.6 morning Health on the
   sample Hilde and +9.4 on the optimizer's, with its Toughened Resolves
   (TABLE_PLAY_NOTES.md, "A whole day"). A cross-character synergy: one big pool paying for the
   party's soft targets.
3b. **Lifeline and self-healing.** The synergy scan's one repeated
   positive: a Lifeline holder with Second Wind keeps the shared pool
   going (+1.1 to +1.4 morning Health on top of the two alone;
   SYNERGY_SCAN.md). Otherwise the scan found nothing outsized, on one
   character or across the party.
4. **Agility and Body as dump stats.** Could be a sim blind spot
   (whatever else Agility and Body do at the table) or a design point.
   Body heals at night, and the day measure still let builds drop it.
5. **Healing per XP.** By the day, Healing Magic was worth about 2.3%
   per XP, the best buy measured. Not a problem in itself, but it means
   healers are underpriced if they're priced by a single fight.

## Caveats

- Items aren't searched; every build uses its sample's gear.
- The sim plays only what it models, with my play rules (TABLE_PLAY_NOTES.md).
- Level 2 Hilde's one entry (+4%) is within the noise.
