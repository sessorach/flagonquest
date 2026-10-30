# How the game plays at the table

Notes from the designer (2026-10-07) on how fights actually go at their
table, as opposed to how a perfectly efficient party would play them.
This is the reference for making the simulator play like real people.
Loose notes; add to it whenever something new about real play comes up.

## Why this exists

The sim's party was playing too well. Measured against the designer's
table (2026-10-07): an enemy that's taken a hit gets another turn about
half the time at the table, and 40% of the time in the sim. Level 2
Party A hits 65% of the time for 4.2 damage after Resist, against the
value economy's baseline of ~50% for ~2.25. Bleeding's price turned out
to hinge on how long hit enemies live, so this matters beyond fight
difficulty.

## How players fight

- **Play style splits by character type.** Tanky characters dive in and
  trust their abilities to keep them alive in melee (Hilde, Browndog).
  Fragile ones (a healer, an archer, a mage) hang back, do what they
  safely can, and trust the tank to handle the front. Some sit in the
  middle: they stay on the edges and attack who they can, a bit more
  aggressive than the back line, but not if it puts them in clear danger.
- **The party talks.** "Let's go for that one," "you should do this."
  They coordinate, but not perfectly.
- **Safety first, on the whole.** The party generally won't expose
  itself to danger, and prefers playing safe over playing aggressively.
- **Attacking twice is attractive.** If a player can attack twice at the
  start of their turn, they usually will. If they can't, they'll often
  attack and then move to a better spot, rather than move first.
- **Focus fire, within reason.** If an enemy's already Harried, others
  pile on ("may as well"). But nobody goes far out of their way to focus
  one target, and a back-liner who can't focus safely takes an easy
  double attack on something else instead.
- **Players don't know enemy Health.** They read context: armor, who's
  hanging back casting, who looks hurt. A lightly armored caster healing
  from the back is an obvious priority, but players won't risk much to
  reach it; they'll often decide to just plow through whoever's being
  healed.
- **Players are sometimes reckless for fun.** Suboptimal picks and
  deliberately silly moves happen all the time.

## Cards and resources

- **Two fights a day** is the working assumption. The party usually isn't
  beaten down enough after the first that anyone's Wounded.
- **A player commits about a third (a quarter to a third) of their hand
  to a given fight**, across everything: playing a card in for a better
  result, healing, card-fueled Techniques like Second Wind.
- **Cards rescue key moments.** A wounded enemy, a player who'd finish it
  with a hit, and a miss: if they've got a 12 in hand, they throw it in.
  Knowing they hold a queen, they may Gamble once or twice on an attack
  that hits on an 8+, and play the queen if the flip comes up short.
  Players see this as reasonable strategy, and it is.
- **Healing after a fight is part of what healers are for** (designer,
  2026-10-29). It's why healing costs cards: it stops Wounded in a fight,
  and it tops the party up so they go to bed full or close to it. Carrick's
  Patch Up is for this too.

### Between fights (day_sim.py, my play rules, 2026-10-29)

- Anyone up who knows From the Brink of Death uses it on each Downed ally
  first (no cost).
- Then each PC spends the cards they can spare: Healing Magic on the
  Downed first, then whoever's missing the most it can restore; Lay On
  Hands the same; Bolstering Refrain when two or more allies are missing
  Shallow; Second Wind on themselves.
- After the first fight a PC keeps a fight's budget (a third of the
  morning's hand) for the second. After the second they spend everything,
  since the Discard Cycle takes the hand at night anyway.
- Patch Up goes on the most hurt before bed, with one card.
- Healing Magic, Second Wind and Bolstering Refrain heal Shallow only, as
  written ("heals 1 Shallow Health"), unless Healing Magic has Deep
  Mending. In a fight the sim still heals its one Health number up to the
  top, which is a little generous; between fights it's exact.
- The night: committed Health comes back, then Body plus any "extra 1
  Health" (Gritty, Pranic Nourishment, Shawl of the Land, Patch Up), Deep
  first.

## Builds

- **Not optimized for combat.** Players build for fun, with an eye on
  being good when the game demands it. The designer's guideline: about
  two-thirds to four-fifths of XP goes to combat; the rest is overhead
  (social skills, knowledge skills, adventuring skills like Awareness,
  Insight, Athletics, Might for climbing, and ribbon Techniques like
  Minor Oracle, which a player happily spent 3 XP on for flavor).
- **Skills spread out.** A reasonable character has a couple of points
  in Awareness and Insight, maybe a social skill, a bit of Might and
  Athletics. Skills overlap enough (several social skills, several
  knowledge skills) that characters can be good at things relative to
  each other.
- **Once the combat basics are down, XP goes elsewhere.** The current
  campaign is at about 90 XP. The designer can collect real builds from
  the players to base sample characters on.
- **A typical party** might be one melee fighter/tank/strategist, plus a
  healer or disruptor, an archer and a mage. Often only one character
  wants to be in melee.

## The battlefield

- **Fights start 6–10 meters apart.** (The sim used 5–10.)
- **Some line of sight issues, not many.** Whether an archer has to move
  to get a shot is about a coin toss; sometimes they can sit back and
  double attack freely. Archers are strong for it, which is why bows got
  so much.

## Enemies

- **Each stat block has its tactic baked in** ("go for the squishiest
  looking party member," "attack whoever's closest"), so the GM doesn't
  have to think about it at the table.
- **Mixed approaches.** Sometimes enemies swarm the party; on a cramped
  battlefield they try to really twist the knife. Sometimes they just
  walk straight in.
- **Enemies are simple on purpose.** Their job isn't to give the GM lots
  of tools. It's to put the players in a bind, so the players have plenty
  to work with and their builds get to shine. Just complicated enough to
  make the players' builds feel fun.

## Plan: a sim that plays like the table (drafted 2026-10-07)

Built in stages, each switchable on and off so its effect can be
measured on its own. After each stage, check the calibration targets
below; only reach for a blunt dial like enemy Health once the
play-style pieces are in.

1. **Play styles.** Each PC gets one: **Diver** (goes for the best
   target it can reach, doesn't mind ending its turn next to enemies),
   **Skirmisher** (attacks what it can reach without ending its turn
   next to more than one enemy, prefers attack-then-move, joins a
   Harried target when it's safe) or **Back-liner** (only attacks what
   it can reach without moving closer than a safe distance to any enemy;
   takes an easy double attack over a riskier focus target; moves away
   when an enemy closes in). Plus a small chance per turn of something
   reckless or off-plan.
2. **What the party can see.** Target choice uses visible cues instead
   of true Health: armor, ranged or casting, healing others, and a rough
   "unhurt / hurt / badly hurt" read.
3. **Real hands of cards.** Each PC draws its hand size at the start of
   the day and commits about a third of it to the fight. Cards get
   played to turn a near-miss into a hit when it matters (a finishing
   blow, or a hit on a Harried focus target), to back a Gamble when a
   high card is in hand, and on card-fueled Techniques. Uses the
   rulebook's "play a card to replace a flipped card" rule directly.
4. **Realistic builds.** Sample characters with about a quarter of their
   XP outside combat, ideally from the players' real ~90 XP builds. A
   new sample party in the shape above: one melee front-liner, a healer
   or disruptor, an archer, a mage.
5. **Battlefield.** Start 6–10 meters apart. A coin-toss chance that a
   ranged PC has no clear shot from where it stands and has to move.
6. **Enemy tactics.** Check each stat block's baked-in tactic against
   what the designer would actually write, and add a "swarm" tactic.
7. **A fast mode.** Once the rich version reads right, keep only the
   pieces that move the results, so batch runs stay quick.

### Calibration targets (designer, 2026-10-08)

For an on-level fight (most fights are on level):

- **Length: about three rounds, five at the outside.** Some fights end
  fast: the party takes a couple of bad hits, piles on, and drops them.
- **The party basically never loses.** Losing outright is very rare.
- **Someone goes Down less than once every few fights.** It happens:
  a dangerous enemy lands a couple of hits, or the enemies focus one PC
  and drop them before the party mops up.
- **Someone ends up Wounded about every other fight.** Often near the
  end, so it's not a big worry; sometimes they need topping up. Something
  the party keeps in mind, not usually a problem.
- **A hit enemy gets another turn about half the time,** after its first
  hit and after any hit alike. The usual shape: the party lands a hit,
  the enemy takes its turn, the party piles onto it because it's hurt,
  and about half the time it's dropped before it acts again. Focus isn't
  perfect: one enemy gets focused down while another takes a few
  incidental hits, then that one gets focused next.

Real party builds (~90 XP, the current campaign) are on their way, for
a more realistic spread of what players actually build.

## First calibration runs (2026-10-08)

`enemy_sim/calibrate.py`, 400 fights per mix on the standard four Level 2
mixes, Party A (Hilde, Browndog, Carrick, Sable) and Party D (Browndog,
Hanforth, Felix, Beornhard). Each stage adds one piece to the one
before; all are switches in tunables.py.

1. **Wounded** (`WOUNDED_RULES`): the sim had no Shallow/Deep split, so
   PCs never suffered Wounded's Bad Luck and -2 to Defenses and Speed.
   Now tracked (every sample PC has 5 Shallow), and heals go to whoever
   is Wounded.
2. **Retarget fix** (`RETARGET_RANGE_FIX`): after a kill, a PC used to
   attack its next target from wherever it stood, in range or not (~2%
   of all PC attacks). Now it has to walk there first.
3. **Battlefield**: 6–10 m start (was 5–10), and line of sight
   (`LINE_OF_SIGHT`): half of fights are cluttered, and in those a ranged
   attacker on either side that hasn't moved spends a move action
   repositioning half the time.
4. **Play styles** (`PLAY_STYLES`, `play_styles.py`, the Play Style
   column in sample_pcs.csv): Hilde and Browndog are Divers; Carrick and
   Felix Skirmishers; Sable, Beornhard and Hanforth Back-liners (Hanforth
   fights hit-and-run, since his weapon is his fists).

| Stage | Party A: rounds / loses / Down / Wounded | Party D: rounds / loses / Down / Wounded |
|---|---|---|
| Before | 3.6 / 6% / 60% / 88% | 4.9 / 7% / 55% / 94% |
| + Wounded | 3.8 / 10% / 66% / 92% | 5.4 / 14% / 61% / 94% |
| + retarget fix | 3.9 / 11% / 67% / 93% | 5.4 / 15% / 62% / 94% |
| + battlefield | 4.1 / 10% / 66% / 94% | 5.6 / 14% / 60% / 95% |
| + play styles | 4.3 / 10% / 71% / 95% | 8.8 / 41% / 78% / 99% |
| **Table** | **~3 (5 max) / ~0 / < 1 in 3 / ~1 in 2** | same |

"Down" and "Wounded" are the share of fights where at least one PC got
there at some point.

A hit enemy acting again (after its first hit / a hit it survived):

| Stage | Party A | Party D |
|---|---|---|
| Before | 39% / 44% | 48% / 54% |
| + play styles (all stages) | 45% / 53% | 57% / 68% |
| **Table** | **about half** | |

**What it says.**

- **Enemies last about as long as at the table.** A hit enemy that
  survives the hit acts again 44–57% of the time, right around "about
  half," before any change to enemy Health. (Counting killing blows as
  hits drags "any hit" down to 26–34%, but a killing blow can't be
  followed by a turn, so it's not the comparison the designer meant.)
- **The party gets hurt far more than at the table**: someone Down in
  55–78% of fights against under a third, someone Wounded in nearly
  every fight against about half, and losses of 6–41% against roughly
  never. Party A loses about half its total Health in an average fight.
  Per PC (before play styles): Carrick goes Down in about half of all
  fights, Hilde and Browndog in about a quarter.
- **Every step toward real play makes the party weaker**, which widens
  that gap instead of closing it. Play styles hit Party D hard: with
  Hanforth holding back (56% of his turns) and Felix refusing to stand
  next to two enemies (25%), Browndog is the only PC in melee and gets
  swarmed (Down 64% of fights).
- **The encounters were tuned to a harder target.** The Level 2 mixes
  were settled in the Horde experiments (ENEMY_ENCOUNTER_DESIGN.md) at
  "79–92% wins, with the party keeping about half its Health." The table
  is easier than that.

So the next question isn't enemy Health; it's how much damage the
party takes. Candidates: encounter difficulty itself, PC tools the sim
doesn't model (Brace, healing items, most Techniques that aren't
attacks), and how the GM runs enemies (every sim enemy attacks twice a
turn when it can).

## Second round (2026-10-08, after the designer's answers)

**Designer's answers.** Enemies double attack like players unless
there's a reason not to (the Fighting Styles that capped them didn't pan
out; every current enemy already attacks twice). A PC going Down should
be a bit uncommon. Between fights players top off their Health, and they
have some Techniques that help defensively. A melee character who can
double attack prefers that to playing safe, but won't close in on
several enemies just to attack once, and uses spare movement to work
round the edges of a fight.

**Melee play style reworked to match.** A melee Skirmisher (Felix)
double attacks whenever something's in reach, crowd or not; otherwise it
only steps in where it ends up next to its target alone, attacks once,
and spends the spare move working round the edge (`play_styles.
_plan_melee_cautious`, `edge_pos`). A melee Back-liner (Hanforth) does
the same, but only for enemies an ally is already fighting. A ranged
Skirmisher (Carrick) attacks once and steps away only with two or more
enemies on it. Party D's turn mix afterwards: Felix double attacks 40%
of his turns and steps in beside one enemy 47%; Hanforth double attacks
45% and holds off 27%.

| | Party A: rounds / loses / Down / Wounded | Party D |
|---|---|---|
| First play styles | 4.3 / 10% / 71% / 95% | 8.8 / 41% / 78% / 99% |
| Melee reworked | 4.3 / 10% / 70% / 94% | 5.9 / 17% / 62% / 96% |

**The first real build: HOLE** (~90 XP; archive/player_builds/
HOLE_2026-10-08.md, sample_pcs.csv's `HOLE (90 XP)`). About a quarter of
its XP is outside combat (Spacious Gut, Gorger, Vow of Poverty, Survival,
Theurgy with no Theurgy Technique), and its best attack is +5 against
the Level 2 samples' +7 to +9. The share link carries no gear or
per-Technique choices, so its weapon (Soulblade's type), armor and
Temper Soulblade's Level and power are assumptions for now.

**Two checks on the damage the party takes:**

- *How Assassins read "squishy"* (`ASSASSIN_READS`). Half the enemies in
  these mixes are Assassins, which go for the PC with the least Health
  right now. Going for whoever *looks* squishiest instead (lowest max
  Health, then lightest armor, the designer's own wording) made Party A
  worse, Down 82%: the same two light PCs get chased all fight. Kept as
  it was.
- *How far off the enemies' offense is* (`ENEMY_ACCURACY_ADJ`,
  `ENEMY_DAMAGE_ADJ`, measurement only, 300 fights per mix):

| Enemy offense | Party A: loses / Down / Wounded / Health left | Party D |
|---|---|---|
| As built | 10% / 70% / 94% / 54 | 17% / 62% / 96% / 57 |
| Accuracy −1 | 7% / 61% / 90% / 60 | 10% / 54% / 93% / 65 |
| Accuracy −2 | 4% / 56% / 84% / 66 | 5% / 46% / 89% / 71 |
| Damage −1 | 2% / 52% / 88% / 68 | 2% / 31% / 92% / 78 |
| Damage −2 | 0% / 27% / 73% / 80 | 0% / 9% / 64% / 89 |
| **Table** | **~0 / uncommon / ~half** | |

The table sits between −1 and −2 damage per enemy hit, roughly a third
less incoming damage. A hit enemy acting again barely moves with any of
these (47–57% after a hit it survived), so it stays on target. Where
that third goes at the table is the open question: PC defensive
Techniques the sim doesn't model (Brace's 3 Protected soaks a hit and a
half), heavier armor or more Resist on real builds, or enemy damage in
the encounter builder running a bit hot.

## Third round: Level 1 (2026-10-08)

**Designer's answers.** Enemies are about the party's Level: Level 1 up
to ~100 XP, Level 2 from 100 to 150, and so on. Difficulty is mostly
managed with more enemies, or a more complicated battlefield. HOLE wears
Light armor, Soulblade likely makes a Heavy Thrown weapon, and Temper
Soulblade is Fatestealer at Level 2 (81 XP spent). The sim now has Heavy
Thrown (tunables.WEAPON); Fatestealer pays out in cards, which the sim
doesn't track yet.

**So the table's fights are a ~90 XP party against Level 1 enemies**,
well into the Level 1 band. Every run above was Level 2: 125 XP
characters whose builds were extrapolated from the Level 1 ones, mostly
into combat. The Level 1 sample characters are the players' own starting
builds (75 XP), and HOLE fits right among them (attack +5, Health 10,
against +5 to +7 and 10).

`calibrate.py -L 1`, 400 fights per mix, everything on:

| Level 1 | Rounds | Loses | Someone Down | Someone Wounded | Acts again (first hit / hit it survived) |
|---|---|---|---|---|---|
| Party A (Hilde, Browndog, Carrick, Sable) | 3.6 | 1% | 35% | 78% | 38% / 43% |
| Party H (A with HOLE for Carrick) | 3.4 | 1% | 32% | 74% | 33% / 40% |
| Party D (Browndog, Hanforth, Felix, Beornhard) | 5.9 | 25% | 62% | 95% | 53% / 60% |
| **Table** | **~3** | **~0** | **uncommon** | **~half** | **~half** |

- **Party A at Level 1 is close to the table** on fight length, losses
  and Downs, and its party sits at 75 XP, the bottom of the band; the
  table's ~90 XP party should have it a little easier still. Wounded
  (74–78% against ~half) is the one that's still high.
- **Party D is weak at Level 1 for its own reasons**: about 35 damage a
  fight between four PCs (Felix hits for 4, Hanforth for 5), one
  front-liner, and fights that run to 6 rounds. It's a made-up mix, not
  a real party.
- **The "third more damage" gap was a Level 2 result**, with the
  extrapolated Level 2 builds. Whether Level 2 encounters run hot, or
  those builds are off, waits for real Level 2 data (the campaign
  passing 100 XP).

**Bleeding at Level 1** (`bleed_vs_damage.py 1 1`, plus a points
count, Party A carriers): a single stack lands 24% of the time against
61% for a +1 on a hit, so a first stack is worth 0.40 of a nominal point,
**1.6 Value**. Bleeding on every hit or Parry lands 0.97 points a fight;
a 5-stack dose 0.26, barely more than one stack. That matches the Level
2 reads (1.6 as built, 1.9 at enemy Health ×1.25).

## The sample roster (agreed 2026-10-08)

Ten Level 1 characters as the sim's representative sample, only real
builds from the designer (Builder Export files, which keep armor,
weapons and Technique choices; share links drop those). The designer
will level them to Level 2 and Level 3 too: around 125 and 175 XP puts
each in the middle of its band (Level 1 enemies up to ~100 XP, Level 2
from 100 to 150, and so on).

| # | Character | Archetype | Status |
|---|---|---|---|
| 1 | Hilde | Barbarian | uploaded (export, 2026-09-20); 125 and 175 XP uploaded and modeled 2026-10-24 |
| 2 | Browndog | Guardian | uploaded (export, 2026-09-20); 125 and 175 XP uploaded and modeled 2026-10-24 |
| 3 | Carrick | Rogue | uploaded (export, 2026-09-20); 125 and 175 XP uploaded and modeled 2026-10-24 |
| 4 | Jackal | Alchemist | uploaded (export, 2026-09-20); 125 and 175 XP uploaded and modeled 2026-10-24 |
| 5 | Beornhard | Sorcerer | uploaded (export, 2026-09-21); 125 and 175 XP uploaded and modeled 2026-10-24 |
| 6 | Sable | Archer | uploaded (export, 2026-09-21) |
| 7 | Hanforth | Healer | uploaded (export, 2026-09-21) |
| 8 | Felix | Monk, cat Wildfolk (he/him) | uploaded (export, 2026-10-08), modeled 2026-10-09 |
| 9 | Enith | Duelist, the Warlock stand-in, Settler (she/her) | uploaded (export, 2026-10-08), modeled 2026-10-09 |
| 10 | Ashleigh | Leader, a bard, cat Wildfolk (she/her) | uploaded (export, 2026-10-08), modeled 2026-10-09 |

Not part of the sample: Rook and Wren (reference builds made to test
movement), HOLE (a real ~90 XP build, set aside for now), the Baseline
Tier rows, and the `(L2)` rows other than Hilde's, Browndog's,
Carrick's, Jackal's and Beornhard's (extrapolated from the Level 1 builds, mostly into combat, not
built by the designer). The 09-20 exports were saved to
archive/player_builds/ on 2026-10-24; their Stats and Skills match the
rows exactly. The designer's 125 and 175 XP builds are the `(L2)` and
`(L3)` rows for those five.

Sample parties to build from it once the last three are in:

- **Typical table**: Browndog, Hanforth, Sable, Beornhard (one
  front-liner, a healer, an archer, a mage).
- **Two front-liners**: Hilde, Browndog, Carrick, Sable (today's Party A).
- **Skirmishers**: Enith, Felix, Jackal, Hanforth.
- **Support-heavy**: Browndog, the Leader, Sable, Beornhard.

### The last three builds (2026-10-08)

Exports in archive/player_builds/; rows `Felix` (replacing the stand-in),
`Enith` and `Ashleigh` in sample_pcs.csv, all 75 XP. Per the designer:
Enith's spells are non-damaging Sorcery debuffs she pairs with her
blade as her bread-and-butter offense; Felix plays carefully but tries
to take targets out tactically, and can hold the front line.

| | Attack | Damage | Parry / Dodge / Vital / Mental | Health | Speed | Reflex | Plays as |
|---|---|---|---|---|---|---|---|
| Felix (Unarmed) | +8 | 4 | 15 / 14 / 11 / 11 | 10 | 4 | 3 | Skirmisher |
| Enith (Soulblade, 1H Light) | +5 | 5 | 13 / 12 / 10 / 12 | 10 | 3 | 5 | Skirmisher |
| Ashleigh (Light Thrown, 6 m) | +5 | 4 | 11 / 12 / 11 / 11 | 10 | 3 | 2 | Back-liner |

Modeled so far: Felix's Firefly Leaves the Hand and Thief Empties the
Vessel as Encounter attacks; Enith's Hand of Chaos and Hex of Sloth
(no damage, Slowed 2 + [Spades]). Still to wire up, each needing new
logic: Raise Spirits (Ashleigh's Interrupt Good Luck for allies), Thief
Empties the Vessel's card-for-3-Health heal, Boughs Unbroken (Felix's
Style), Battle Maneuver's Features, Hex of Rebuking's Push (the sim has
no Push), and Fatestealer (cards).

**Two fixes these builds turned up.**

- *The Feature builder* didn't enforce once-only Features or the extra
  points Bare-Handed (+2) and Tormenting Curse (+3) grant, so Felix's
  and Enith's exports were built on smaller budgets than their Features
  allow. features.csv now has Max Copies and Bonus Points columns the
  builder reads (see convert.py's FEATURE LIMITS).
- *Dodge in the sim* used Acrobatics alone; the rulebook lets you pick
  Acrobatics or Brawl. Fixed in party.py: Felix 11 → 14, Hanforth and
  Beornhard up 2–3, Browndog up 1. Level 1 calibration after the fix:
  Party A 3.6 rounds, loses 1%, Down 34%, Wounded 77% (no real change,
  since Browndog Parries); Party D, now with the real Felix, 6.0 rounds,
  loses 24%, Down 60%, Wounded 96%.

## Fourth round: real cards, and the last three builds (2026-10-09)

**Designer's answers.** Felix's Battle Maneuver splits Bare-Handed's 2
extra points evenly: Lunging x2 and Half Guard x3, used as his opening
move. Enith's hexes are Lance plus the rest on the one effect (Tormenting
Curse's 3 points): Hex of Sloth is Slowed 6 + [Spades], Hex of Rebuking
is Pushed 12 + [Spades] meters, range 5. She's a tactical skirmisher,
almost a disabler: the hexes split enemies up and isolate them so the
party can divide and conquer. Ashleigh boosts anyone's attack with Raise
Spirits, puts big attacks (Beornhard's Encounter spells) first, stays in
range of the party, and throws a knife with what's left. Felix's Thief
heal goes when he's missing 3 or more. Boughs Unbroken clears Bleeding,
then Crippled, then anything else. Fatestealer needs real cards. And:
get the sim playing with cards as close to the table as it can while
still running lots of fights.

### The card model (cards.py, tunables.CARDS)

Straight from the rulebook's card rules (Flips, Your Hand and Playing
Cards, The Suit Pool; the glossary's Card Terms):

- Every PC has its own 52-card deck; the GM has one for every enemy.
  Flips are real cards off the top, Good and Bad Luck flip extra cards
  and cancel one for one, and used cards go to the discard.
- Every card flipped or played is in the suit pool. A card matching the
  attack Skill's suit is an Extra Success, +1 damage. Riders like
  "Slowed 6 + [Spades]" count that suit in the pool.
- A PC draws the day's hand (twice Cunning plus Mind) and commits a
  third of it to a fight (CARDS_FIGHT_SHARE). Half of fights are the
  day's second fight, with a third of the hand already gone. Bottomless
  Bottles' crafting comes out of the hand first: Jackal throws her six
  lowest cards into it and fights with four.

How players spend it, following the table notes above:

- **Rescues.** A miss can be fixed by playing the cheapest hand card
  that clears it (with Bad Luck, every low card needs replacing). How
  freely depends on how much the hit matters (RESCUE_RESERVE): a kill
  shot or an Encounter attack gets a card whenever there's one in the
  budget, a hit on a hurt or Harried target only with a card to spare,
  a plain hit only with plenty. On a kill shot an ally can throw in a
  card too.
- **Gambles behind a card.** Holding a card that still clears the attack
  after a Gamble or two, a player Gambles (at most twice) when the hit
  would kill or it's on a focus target, and plays the card if the flip
  comes up short.
- **Kill top-ups.** A hit that leaves the target a point or two short
  gets matching-suit cards added to the pool to finish it.
- **Card Techniques**, all from the real hand: Perfect Strike with a
  low card (a high one is worth more as a rescue), Second Wind and
  Healing Magic with Hearts first, Warmage's Reserves when War Magic
  runs out, Thief's heal, Cloak and Dagger with a Spade if there is one.
- **Enemies** have no Skill, so they get no suit Extra Successes
  (ENEMY_SUIT_EXTRA, an assumption).

With every new switch off, the sim reproduces the old numbers exactly
(checked on fixed seeds). A fight still takes about 5 ms.

### Three rules fixes found along the way

- **Fleeting's skip.** Since 2026-08-29 the glossary has said a Fleeting
  effect gained from zero skips its next removal. The sim never did
  this. Read literally, it applies to everything: a fresh Bleeding stack
  then only deals its point at the end of the target's second turn.
  Settled by the designer later the same day: the skip only applies to
  an effect gained during the bearer's own turn (a player putting
  Protected on themselves), Bleeding never skips, and Harried just
  clears at the end of the turn (FLEETING_SKIP = 'own_turn',
  FLEETING_SKIP_EXEMPT).
- **Protected decays.** It's Fleeting, and the sim never took stacks off.
  It now does, for PCs and enemies (PROTECTED_DECAYS).
- **No Gambling on spells.** The rulebook says only weapon attacks can
  be Gambled on; Beornhard's War Magic was Gambling.

All three barely move the party numbers (a point or two at most).

### The three builds, modeled

- **Felix**: Battle Maneuver on his first attack of the fight. Its two
  free Shifts carry him 4 m in, often leaving the AP for both attacks; a
  hit gives him 3 + [Spades] Protected (3.4 on average). It lands 99% of
  the time, since it's worth a card. Thief Empties the Vessel heals 3
  for a card when he's missing 3 or more. Used early, the heal almost
  never fired (0.02 a fight), so he now saves Thief until he's hurt or
  it's round 3 (my call). Boughs Unbroken: no Harried from Parrying,
  and an unarmed hit cleanses.
- **Enith**: Hex of Sloth is against Dodge, Hex of Rebuking against
  Vital (the designer's split). At the start of her turn, with both
  hexes ready, the biggest fresh melee threat that's engaged with the
  party gets Slowed,
  then Pushed away from the party (a Speed 4 enemy with 6+ Slowed can't
  move for about three turns). Otherwise she Pushes an enemy off a
  fragile ally, or Slows one still walking in. A Push needs two enemies
  standing. Watching replays showed the party walking over to the enemy
  she'd just stranded, so the party now leaves an enemy that's stuck
  (Slowed to 0 Speed, nobody in reach) for last (tactics.
  STUCK_DISCOUNT). She lands about 1.3 hexes a fight. Fatestealer at
  Level 1 needs three kills to draw a card, which hardly happens in one
  fight; the sim starts each fight at 0 charges.
- **Ashleigh**: Raise Spirits spends her Interrupt AP on Good Luck for
  allies' attacks, about 8 a fight, holding her last AP for an
  Encounter attack while an ally still has one. Leftover AP on her own
  turn goes on staying in range of the party.

### Results

`calibrate.py -L 1`, 300 fights per mix, everything on, against the
same with no cards and no rules fixes:

| Level 1 | Rounds | Loses | Someone Down | Someone Wounded | Acts again (first hit / hit it survived) |
|---|---|---|---|---|---|
| A, two front-liners (Hilde, Browndog, Carrick, Sable) | 2.7 (was 3.6) | 0% (1%) | 14% (34%) | 54% (77%) | 20% / 27% (38% / 43%) |
| T, typical (Browndog, Hanforth, Sable, Beornhard) | 2.7 (4.3) | 0.2% (4%) | 15% (35%) | 51% (84%) | 21% / 27% (44% / 48%) |
| S, skirmishers (Enith, Felix, Jackal, Hanforth) | 3.8 (6.0) | 0.5% (16%) | 28% (67%) | 74% (96%) | 25% / 36% (50% / 58%) |
| U, support-heavy (Browndog, Ashleigh, Sable, Beornhard) | 2.9 (4.6) | 0.1% (3%) | 17% (49%) | 51% (84%) | 24% / 32% (45% / 49%) |
| D (Browndog, Hanforth, Felix, Beornhard) | 3.0 | 0.8% | 18% | 59% | 27% / 34% |
| H (A with HOLE for Carrick) | 2.6 | 0% | 12% | 48% | 18% / 24% |
| **Table** | **~3 (5 max)** | **~0** | **uncommon** | **~half** | **~half** |

**What it says.**

- **Cards are a big share of the party's strength**, and the sim was
  missing it. Each PC spends most of its third of a hand: about 6 cards
  a fight across the party out of a 7-10 card budget, mostly rescuing
  misses, backing Gambles and Perfect Strike (`card_stats.py` breaks it
  down per PC). Without the hand (suit pool
  only) Party A runs 4.1 rounds with someone Down in half of fights.
- **Four of the five targets now land** at the encounters' own Health:
  about three rounds, the party almost never loses, someone goes Down
  in 12-28% of fights, someone's Wounded in about half. Party S, with no
  front-liner, is the hard case: 3.8 rounds, Wounded 74%.
- **A hit enemy acting again is now too rare**: 18-27% after its first
  hit against the table's "about half". Cards make hits more lethal
  (kill shots get rescued and topped up), so fewer hit enemies survive
  to act. Raising enemy Health brings it up, but takes the other targets
  with it: at x1.25 it's 32-40% with fights of 3.4-4.7 rounds and Down
  25-38%; at x1.5 it's 43-51% with 4.0-5.7 rounds and Down 34-51%.
  Spending fewer cards (a quarter of the hand, or rescues only for kill
  shots) barely moves it, and neither does looser focus fire. The
  targets pull against each other here; which one to trust is the
  designer's call.

### Bleeding, with cards and the skip

Same setup as "Bleeding at Level 1" in balance_weights_notes.md:

| | First stack lands | A +1 on a hit lands | First stack worth |
|---|---|---|---|
| Before cards (2026-10-08) | 24% | 61% | 1.6 Value |
| Cards, no skip or same-turn skip | 12% | 54% | 0.9 Value |
| Cards, skip as written | 1% | 54% | ~0.05 Value |

Shorter fights mean fewer stacks get to tick. Bleeding on every hit
(Hilde, Sable carrying it) lands 0.3-0.6 points a fight now, and
0.02-0.05 with the skip read literally. The pending reprice's 1.6 for a
first stack is out of date either way.

### Open questions for the designer

1. ~~Fleeting's skip~~: answered, same-turn only, Bleeding and Harried
   exempt. The glossary wording still needs updating to match.
2. ~~The glossary's Play entry~~: answered, a played card either
   replaces a flipped card (its suit joins the pool too) or just adds
   its suit to the pool. The glossary now says so; the sim already
   worked that way.
3. ~~Enemy suits~~: answered, for now +1 damage per Heart in an enemy's
   flip (ENEMY_SUIT_EXTRA), something more detailed later.
4. "A hit enemy acts again about half the time" against the other
   targets (above).
5. ~~Durable with decaying Protected~~: fine as is. It's meant to give
   1-2 rolling Protected until the enemy gets focused down.
6. ~~Which Defense each of Enith's hexes targets~~: answered, Sloth
   against Dodge, Rebuking against Vital. With the split nothing in the
   party numbers moved (Party S still 3.8 rounds, Down 28%); she still
   lands about 1.3 hexes a fight, spending cards to make them stick.
7. ~~A healer's card budget~~: fine as is. The point is what a party
   does with average resources.

### Enemy Hearts (2026-10-09, later)

With +1 damage per Heart on enemy attacks, `calibrate.py -L 1`, 300 fights
per mix (before → after):

| Level 1 | Rounds | Loses | Someone Down | Someone Wounded | Acts again (first hit / hit it survived) |
|---|---|---|---|---|---|
| A | 2.7 → 2.8 | 0% → 0.3% | 14% → 20% | 54% → 59% | 21% / 28% |
| T | 2.7 → 2.8 | 0.2% → 0.5% | 15% → 19% | 51% → 55% | 21% / 28% |
| S | 3.8 → 3.8 | 0.6% → 1.1% | 28% → 35% | 74% → 76% | 25% / 37% |
| U | 2.9 → 2.9 | 0.1% → 0.1% | 17% → 24% | 51% → 58% | 25% / 32% |
| D | 3.0 → 3.1 | 0.8% → 1.8% | 18% → 24% | 59% → 63% | 27% / 35% |
| H | 2.6 → 2.6 | 0% → 0% | 12% → 18% | 48% → 55% | 19% / 25% |

Fights are no longer and the party still almost never loses, but someone
goes Down about 5 points more often. Party S, with no front-liner, is
just over one fight in three. A hit enemy acting again is unchanged and
still the one target the sim misses (open question 4).

### Leftover Bleeding counts (2026-10-19)

Per the designer, a PC's leftover Bleeding now ticks out after the fight
(tick size and Protected as in it) before Health left is measured
(tunables.BLEED_RESOLVE_AFTER). On the standard Level 1 calibration that
moved only Health left: Party A 81.0 → 80.3, Party D 81.2 → 80.7. A PC it
drops after the fight is counted apart from someone Down during it.

### The new Bleeding rule (2026-10-19, later)

Per the designer, Bleeding now loses half its stacks, rounded up, each
time it decays, and Protected stops its ticks (tunables.BLEED_TICK
'half', BLEED_PROTECTED 'ticks'). `calibrate.py`, 300 fights per mix,
old rule → new:

| Level 1 | Rounds | Loses | Someone Down | Someone Wounded | Health left |
|---|---|---|---|---|---|
| A | 2.8 → 2.8 | 0.3% → 0.3% | 20% → 21% | 59% → 62% | 80.3 → 80.3 |
| T | 2.8 → 2.8 | 0.5% → 0.5% | 19% → 19% | 55% → 57% | 83.3 → 83.4 |
| S | 3.8 → 3.8 | 1.1% → 1.1% | 35% → 37% | 76% → 76% | 77.9 → 77.9 |
| U | 2.9 → 2.9 | 0.1% → 0.1% | 24% → 25% | 58% → 60% | 81.1 → 81.1 |
| D | 3.1 → 3.1 | 1.8% → 1.9% | 24% → 24% | 63% → 64% | 80.7 → 80.7 |
| H | 2.6 → 2.6 | 0% → 0% | 18% → 19% | 55% → 57% | 82.1 → 82.2 |

Level 2: someone Down goes 45% → 47% (A) and 35% → 36% (D); nothing
else moves. The only Bleeding in these parties is Warband's Footpads
Poisoning the PCs. With half ticks it lands during the fight instead of
after it, so someone is Down or Wounded a point or two more often, and
Health left stays put.

## Where things stand (2026-10-25)

The sections above are dated and describe the sim on their day. Since
then:

- **Everything the 10-08 notes left to wire up is in**: Raise Spirits,
  Thief Empties the Vessel's heal, Boughs Unbroken, Hex of Rebuking's
  Push, Fatestealer and Battle Maneuver's Features. So are Brace, Furious
  Rage on Hilde, Strength from the Slain, Exert Pressure, Eagle Eyes,
  Grim Resolve and Beornhard's Destructive and Furrow War Magic.
- **Every combat Technique on the roster's sheets is in** (2026-10-25):
  Shadow Jaunt, Gainsay and Wall of Shadows (Beornhard), Gust of Wind,
  Ley-weaving, Lifeline and Spirit Blessing (Hanforth), Blinkstep and
  Parting Shot (Sable and Rook at Level 2), Sable's Level 2 Battle
  Maneuver, and One Eye Behind You's discard to move up the order.
  Reckoning is a ranged cast now, not a stand-in for Hanforth's punch.
  The rest are out of combat: Follower, Legerdemain, Rumormonger,
  Distraction, Patch Up, Bound Across Mountains, Quick Draw, Shadow's
  Path, Favorite Face, Spacious Gut, Gorger, Vow of Poverty.
- **The sample characters load from their Builder exports** (later on
  10-25): `builds/`, one file per character, with `sample_pcs.csv`
  down to the play choices an export doesn't carry. A Technique, Feature
  or item the sim doesn't know stops the load instead of being skipped.
  Technique and Ability effects live in `techniques.py` and
  `enemy_abilities.py`, plugged into `hooks.py`'s points; combat_sim no
  longer tests for each one by name.
- **So is the whole enemy Ability catalog**, at the draft's pick costs:
  the rest of the Strike and Poison riders, Cleaving, Grappling (with
  the rulebook's grapple rules on both sides), Devastating, Omniguard,
  Resilient, Retribution Aura, Sturdy, Shadow Jaunt, the three 0 AP
  Actions, Attunement and Resist by element, Elemental Spell and Weapon,
  Enhanced Range/Reflexes/Speed, Improved Support, and the Curse, Great
  Heal and Shielding Nova actions. No sample enemy carries the new ones
  yet.
- **Thrown weapons hit a point softer** (2 + Cunning, 3 + Body for
  Heavy), matching `items.csv`. Ashleigh's damage in the 10-08 table is
  3 now, not 4.
- **The designer's own builds** are the `(L2)` and `(L3)` rows for
  Hilde, Browndog, Carrick, Jackal and Beornhard; Party B is Hilde,
  Browndog, Jackal and Beornhard, the designer's at every Level. So are
  Hanforth's `(L2)` and `(L3)` since 10-26. Sable and Felix are still
  Level 1 builds plus extrapolated `(L2)` rows; Enith and Ashleigh are
  Level 1 only.
- **Calibration against built Health** (`calibrate.py`, 200 fights a
  mix), next to the targets above:

| | Rounds | Losses | Someone Down | Someone Wounded | Hit enemy acts again |
|---|---|---|---|---|---|
| Level 2, Party A | 2.5 | 0% | 13% | 38% | 21-31% |
| Level 2, Party B | 2.1 | 0% | 7% | 31% | 13-22% |
| Level 2, Party D | 2.8 | 0% | 16% | 43% | 15-35% |
| Level 3, Party A | 2.9 | 3.1% | 56% | 86% | 21-39% |
| Level 3, Party B | 2.2 | 0.2% | 36% | 65% | 10-24% |
| Level 3, Party D | 2.6 | 0.5% | 38% | 76% | 12-31% |

The leveled builds end Level 2 fights fast and almost never lose, and a
hit enemy gets another turn far less than the table's half. Level 3 is
rougher on Party A (Sable is still her Level 2 build there). The
10-25 Techniques moved these a little: Health left went up 1-3 points
for every leveled party. The big one is Lifeline: Party D's someone-Down
fell from 19% to 2%, because Hanforth takes any hit that would Down an
ally and keeps taking them while he can. That was the extrapolated
Hanforth (L2), though. The designer's real 125 XP build (10-26) doesn't
take Lifeline, and Party D's someone-Down is 16% with it. Party D at
Level 3 is Party B with Hanforth for Jackal, since
there's no Felix (L3) yet. Gust of Wind costs Hanforth's
Level 1 party about a point of Health: a pushed enemy walks back on 2 AP
and still attacks, so the push rarely takes anything off it.

- **Table toughness** for the as-built Level 1 Party A is ×2.0 enemy
  Health, not ×1.75 (`balance_weights_notes.md`, "The sample
  characters, as built"). Scripts still default to 1.75.

## Healing and blessing at Levels 1-3 (2026-10-26)

Groundwork for the Healing and Blessing magic pass, from Hanforth's real
75, 125 and 175 XP builds in Party D (Browndog, Hanforth, Felix and
Beornhard; Hilde for Felix at Level 3), at about five-round toughness.
`compare_builds.py` and the `Hanforth (L2, ...)`/`(L3, ...)` variants
reproduce it.

What Hanforth does in a fight, 240 fights a Level:

| | Party max Health | Rounds | Damage taken | Healed | Shielding stacks given | Protected soaked (all sources) |
|---|---|---|---|---|---|---|
| Level 1, ×1.75 | 40 | 7.0 | 21.5 | 2.3 | none | 4.4 |
| Level 2, ×1.75 | 43 | 4.4 | 10.8 | 1.8 | 3.8 | 3.6 |
| Level 3, ×2.25 | 47 | 5.4 | 26.2 | 3.3 | 4.3 | 6.8 |

He casts Healing Magic about once every two fights at every Level, and
at Level 3 nearly all of it goes on himself. Why so little:

- **There's seldom anyone to heal.** The sim heals only a Wounded ally,
  and on 2-3 of his turns a fight nobody is. Healing anyone down 4 or
  more instead moved Health left by -0.1 to +1.3, so the trigger isn't
  what's holding him back.
- **The cards do more elsewhere.** A cast costs its Level in cards and
  only the Hearts add healing. At Level 1 he spends about 2.4 cards a
  fight on his own attacks (rescuing misses, topping up kills) and under
  1 on healing. Making him keep a cast's worth back
  (`tunables.HEALER_KEEPS_CARDS`, off) costs the party 0.4-1.1 Health
  at every Level: a card saving a hit beats the same card as healing.
- **The heal barely grows.** 1 + Hearts + Vitality: 5 at most at Levels 1
  and 2 (Vitality 2 both times), 8 at Level 3 (Vitality 4, three cards).
  Vitality costs 2 points for +1.
- **Spirit Blessing's budget grows a point a Level** (3, 4, 5, 6), so
  two Level 1 copies (6 points, two casts) beat one Level 2 copy (4
  points, one cast) for the same 6 XP. The 175 XP build takes two Level
  1 copies.

**Units (corrected 2026-10-27):** "Health" in the table below (not the per-fight one above, which is in points) is the party's Health left as a share of its max Health, in percentage points (compare_builds.py scored it that way until 10-27). At these party sizes, 40-47 max Health, a point is about 0.45 Health, about 1.8 Value. Rankings within a table hold; a swap that adds max Health (Toughened Body) reads low.

Hanforth in Jackal's seat in Party B (paired, 300 fights a mix):

| | Hanforth for Jackal | With Lifeline |
|---|---|---|
| Level 1, ×2.0 | -6.4 ±2.0 Health, wins -8 points | |
| Level 2, ×2.75 | +3.2 ±1.4 Health, someone Down -6 points | +6.9 ±1.4, Down -19 points |
| Level 3, ×2.25 | +5.5 ±1.6 Health, someone Down -14 points | +7.5 ±1.5, Down -20 points |

So the healer goes from a step behind a damage dealer at Level 1 to a
step ahead at Level 3, by keeping people standing more than by winning
more. Lifeline is still the biggest single piece: swapped in for
Minor Oracle and Profession (same XP), it takes Level 2 Party D's
someone-Down from 33% to 16% at ×1.75.

Directions the numbers point, for the pass: heals that cost fewer
cards, or count more than Hearts; Vitality at 1 point; a Spirit Blessing
budget that grows like Healing Magic's (1, 4, 8, 11); and a look at
whether Lifeline is doing the job Healing Magic should.

## Hanforth's options (2026-10-26, later)

A broad look at what else Hanforth could take, for the Healing Magic
and Spirit Blessing pass (`hanforth_sweep.py`, `compare_builds.sweep`).
Each swap fits its copy's Feature Budget and spends XP the build
already spends: "XP" rows move his out-of-combat XP (Minor Oracle and
Profession, 6; Dominate Mind, 12 more at Level 3) into combat. Two
parties a Level, 100 fights a mix, paired on the same seeds, so the
margins are wide (±0.4 to ±2.4 Health) and anything inside about a
point is a wash. "HM" is Healing Magic, "SB" Spirit Blessing.

**Units (corrected 2026-10-27):** "Health" in this section's tables and bullets is the party's Health left as a share of its max Health, in percentage points (compare_builds.py scored it that way until 10-27). At these party sizes, 40-47 max Health, a point is about 0.45 Health, about 1.8 Value. Rankings within a table hold; a swap that adds max Health (Toughened Body) reads low.

Change in Health left at the end of the fight, and in how often someone
goes Down (points):

Level 2. Party D, ×1.75: wins 96%, Health left 78.7, someone Down 33%, 4.6 rounds. Hilde, Browndog, Hanforth, Beornhard, ×2.5: wins 94%, Health left 76.4, someone Down 29%, 5.1 rounds.

| Swap | Party D, ×1.75 | Hilde, Browndog, Hanforth, Beornhard, ×2.5 |
|---|---|---|
| XP: Toughened Body | +3.3 ±1.0, Down -6 | +2.3 ±0.8, Down -2 |
| XP: HM to Level 3 (Triage, Vitality 2, Reach), one more SB Step of Air 3 | +2.1 ±1.5, Down -8 | +3.5 ±1.3, Down -5 |
| XP: Lifeline | +2.4 ±1.1, Down -16 | +2.5 ±1.2, Down -13 |
| XP: more SB, Shielding 3 and Step of Air 3 | +1.3 ±1.5, Down -5 | +2.9 ±1.2, Down -4 |
| HM: Triage, Reach | +1.0 ±0.6, Down -3 | +1.4 ±0.9, Down -1 |
| XP: a Level 2 SB, Shielding 2, Quickened, Reach | +0.6 ±0.6, Down -3 | +1.6 ±0.8, Down -1 |
| XP: two more SB Shielding 3 | +0.9 ±0.7, Down -2 | +1.0 ±0.6, Down -1 |
| XP: HM to Level 3 (Vitality 4), one more SB Shielding 3 | +0.6 ±0.8, Down -2 | +1.0 ±0.8, Down -0 |
| HM: Vitality 1, Guardian Angel 1, Reach | +0.1 ±0.6, Down -4 | +1.1 ±1.0, Down -2 |
| SB: Shielding 2, Reach | +0.1 ±0.6, Down -1 | +0.2 ±0.9, Down +0 |
| SB: Elemental Enhancement 3 (Fire) | -0.5 ±1.3, Down -2 | +0.4 ±1.4, Down -1 |
| SB: Touch of Chaos 3 | -0.6 ±1.5, Down -0 | +0.4 ±1.5, Down -0 |
| SB: Step of Air 3 | -0.7 ±1.5, Down -2 | +0.3 ±1.4, Down -0 |
| SB: Shielding 2, Quickened | -0.3 ±0.7, Down -1 | -0.3 ±0.8, Down +2 |
| HM: Guardian Angel 2, Vitality 1 | -0.5 ±0.4, Down -1 | -0.1 ±0.5, Down -1 |
| HM: Vitality 1, Purify, Reach | -0.6 ±0.6, Down -1 | -0.0 ±0.9, Down +0 |
| SB: Step of Air 2, Quickened | -0.6 ±1.4, Down -2 | -0.1 ±1.4, Down +3 |
| SB: Shielding 1, Step of Air 1, Quickened | -0.5 ±0.9, Down -2 | -0.6 ±0.8, Down +2 |
| Lifeline for Reckoning | -0.5 ±1.3, Down -11 | -0.9 ±1.4, Down -6 |
| SB: Turn Elements 3 (Shadow Ward) | -0.7 ±0.6, Down -0 | -0.7 ±0.8, Down +2 |
| SB: River's Might 3 | -0.8 ±1.5, Down -1 | -0.8 ±1.7, Down +0 |
| SB: Retribution 2, Shielding 1 | -0.9 ±0.6, Down +1 | -1.1 ±0.6, Down +2 |
| HM: Rejuvenate, Vitality 1, Reach | -3.2 ±1.0, Down +3 | -1.9 ±1.0, Down +4 |
| Field Medic and an SB Shielding 3 for Ley-weaving | -2.4 ±1.3, Down +1 | -3.0 ±1.6, Down +8 |

Level 3. Browndog, Hanforth, Hilde, Beornhard, ×2.25: wins 79%, Health left 53.8, someone Down 64%, 5.5 rounds. Hilde, Hanforth, Jackal, Beornhard, ×2.0: wins 75%, Health left 45.9, someone Down 80%, 5.1 rounds.

| Swap | Browndog, Hanforth, Hilde, Beornhard, ×2.25 | Hilde, Hanforth, Jackal, Beornhard, ×2.0 |
|---|---|---|
| XP 12: Lifeline, Toughened Body | +6.5 ±2.4, Down -23 | +10.2 ±2.2, Down -30 |
| XP 18: Lifeline, SB L3 Mass Blessing, Shielding 3, SB L1 Step of Air 3 | +1.1 ±1.6, Down -4 | +8.2 ±2.3, Down -22 |
| XP 6: Lifeline | +1.4 ±0.9, Down -4 | +6.6 ±2.0, Down -21 |
| HM: Triage, Vitality 1, Guardian Angel 2, Reach | +1.5 ±0.8, Down -2 | +2.4 ±1.1, Down -6 |
| HM: Vitality 2, Guardian Angel 2, Reach, Purify | +0.9 ±0.7, Down -1 | +2.3 ±1.2, Down -6 |
| XP 12: HM to Level 4 (Vitality 5, Reach), SB L3 Guided Hand 2, Quickened | +1.1 ±1.3, Down -0 | +1.8 ±1.3, Down -1 |
| HM: Vitality 3, Guardian Angel 2 | +1.1 ±0.7, Down -1 | +0.8 ±0.7, Down -1 |
| HM: Triage, Vitality 2, Reach | +0.4 ±0.5, Down -0 | +1.0 ±0.9, Down -4 |
| XP 12: SB L3 Guided Hand 2, Quickened, SB L1 Step of Air 3 | +0.6 ±1.1, Down -0 | +0.4 ±1.3, Down +0 |
| XP 12: SB L3 Alacrity, Shielding 3, SB L1 Shielding 3 | +0.4 ±0.4, Down -0 | +0.5 ±0.4, Down +0 |
| XP 12: SB L3 Mass Blessing, Shielding 3, SB L1 Shielding 3 | +0.4 ±0.4, Down -0 | +0.4 ±0.4, Down +0 |
| SB: both Shielding 2, Quickened | +1.2 ±1.0, Down +1 | -1.2 ±1.2, Down +1 |
| SB: second copy Shielding 2, Quickened | -0.0 ±0.2, Down +0 | -0.2 ±0.5, Down +0 |
| Lifeward for Ley-weaving and Minor Oracle | +1.8 ±1.3, Down -3 | -2.4 ±1.7, Down +7 |
| SB: second copy Retribution 2, Shielding 1 | -0.5 ±0.3, Down +0 | -0.7 ±0.7, Down +1 |
| SB: second copy Elemental Enhancement 3 (Fire) | -1.4 ±1.5, Down +1 | +0.2 ±1.6, Down -2 |
| SB: second copy Touch of Chaos 3 | -1.7 ±1.6, Down +2 | -0.5 ±1.9, Down +0 |
| SB: second copy Step of Air 3 | -1.3 ±1.6, Down +0 | -1.0 ±1.6, Down -0 |
| XP 12: HM to Level 4 (Healing Pact, Vitality 3), SB L3 Mass Blessing, Shielding 3 | -0.9 ±0.8, Down +2 | -1.5 ±0.7, Down +2 |
| HM: Healing Pact, Vitality 1, Reach | -1.5 ±0.9, Down +3 | -1.6 ±1.1, Down +0 |
| Field Medic for Ley-weaving (3 XP spare unspent) | -0.7 ±1.1, Down +0 | -4.7 ±1.5, Down +8 |

How the sim plays them: a defensive blessing (Shielding, Retribution,
Turn Elements) goes to whoever has the most enemies next to them, often
Hanforth himself; an offensive one (Step of Air, Touch of Chaos,
Elemental Enhancement, Guided Hand) to the hardest hitter who hasn't
acted yet. One blessing a turn. Copies built differently are new as of
today (`techniques.py`), and so are Field Medic and Lifeward.

What it says, roughly:

- **Keeping Hanforth up beats everything else.** Toughened Body and
  Lifeline top both Levels, and Lifeline plus Toughened Body at Level 3
  is worth 6-10 Health and 23-30 points off someone-Down. No Feature
  swap comes close at Level 3. At Level 2, putting the 6 XP into a
  Level 3 Healing Magic and one more blessing does about as well as
  Lifeline. At Level 3 he goes Down himself in 47-66% of fights (Health
  10, like Beornhard and Jackal); at Level 2, in about 1 in 6.
- **Healing Magic: Guardian Angel and Triage beat Vitality**, more so at
  Level 3, where Triage, Vitality 1, Guardian Angel 2 and Reach is the
  best of the Feature swaps (+1.5 to +2.4). Healing Pact is the worst
  Level 3 pick, even at Level 4. Rejuvenate is the worst at Level 2.
- **Spirit Blessing: Shielding 3 as built is as good as anything at
  Level 1.** Step of Air, Touch of Chaos, Elemental Enhancement and
  River's Might land within about a point and a half of it, either
  way. Retribution and a
  Shadow Ward come out a little behind. Quickened's saved AP doesn't buy
  back the Protected it costs. More copies help a little (about a point
  for two more). The Advanced Features at Level 3 (Mass Blessing,
  Alacrity, Guided Hand) add about half a point for 12 XP, where
  Lifeline adds 1.4-6.6 for 6.
- **The Styles mostly measure Ley-weaving.** Swapping it out drops his
  heal's reach from 4 meters to 1, so Field Medic costs 1-5 Health.
  Lifeward (Protected equal to what's healed) splits: +1.8 in one party,
  -2.4 in the other.
- **Lifeline for Reckoning** leaves Health about even but cuts
  someone-Down by 6-11 points, so Reckoning's Crippled is worth about
  as much Health as Lifeline is.

## Beornhard's War Magic options (2026-10-26, later)

**Units (corrected 2026-10-27):** "Health" in this section's tables and bullets is the party's Health left as a share of its max Health, in percentage points (compare_builds.py scored it that way until 10-27). At these party sizes, 40-47 max Health, a point is about 0.45 Health, about 1.8 Value. Rankings within a table hold; a swap that adds max Health (Toughened Body) reads low.

The same broad sweep for the designer's 125 and 175 XP Beornhard
(`beornhard_sweep.py`): other Features on his War Magic copies, the
Defense they're learned against, and his other Techniques traded for
more War Magic or Force Missiles. Party B and Party D at each Level,
100 fights a mix, paired. "WM" is a Level 2 copy at Level 2 (both
rebuilt the same), "WM2"/"WM4" his Level 2 or Level 4 copies at Level 3.

Three things changed in the sim to run it. Force Missiles is modeled (a
1 AP Encounter spell against the target's better of Parry and Dodge,
3 + Mind Physical). A War Magic copy with neither Lance nor a Shape now
reaches only an adjacent creature, as its Target says; before, it had
his full range, which no sample build had tripped over. And
`tunables.SHAPE_SETUP` (off) lets a caster step in to catch two or more
enemies with a Furrow, Funnel or Nova copy: as a Back-liner, Beornhard
(L3) cast his Level 4 Furrow copy 0.14 times a fight, since a 4-meter
line from his own space rarely reaches anyone. With it on, 0.46. The
Level 3 table is with it on; with it off, the Shape rows all read zero.

Change in Health left at the end of the fight, and in wins (points):

Level 2. Party B, ×2.75: wins 90%, Health left 69.0, someone Down 40%, 5.2 rounds. Party D, ×1.75: wins 96%, Health left 78.7, someone Down 33%, 4.6 rounds.

| Swap | Party B, ×2.75 | Party D, ×1.75 |
|---|---|---|
| XP: Shadow Jaunt for Force Missiles | +1.3 ±0.8, wins +0 | +1.6 ±0.8, wins +2 |
| XP: Shadow Jaunt for a Level 1 Lance | +0.9 ±0.8, wins +1 | +0.7 ±0.7, wins +2 |
| WM: as built, all vs Vital | +0.2 ±1.2, wins +1 | +1.0 ±1.0, wins +2 |
| XP: Overchanneling for Force Missiles and a Level 1 Lance | -1.8 ±1.3, wins -2 | +0.6 ±1.2, wins +1 |
| XP: Overchanneling for a Level 2 Lance, Destructive 2 | -1.8 ±1.2, wins -2 | +0.1 ±1.2, wins -0 |
| WM: Lance, Wild Magic 2 | -3.0 ±1.5, wins -2 | +1.2 ±1.1, wins +2 |
| WM: Lance, Destructive 1, Corrupting 1, all vs Vital | -2.0 ±1.3, wins -0 | +0.1 ±1.1, wins +2 |
| WM: Lance, Destructive 1, Wild Magic 1 | -1.8 ±1.5, wins -2 | -0.4 ±1.2, wins +0 |
| WM: one copy Frigid 2, one Destructive 2 | -2.1 ±1.5, wins -3 | -0.6 ±1.0, wins +0 |
| WM: a Tormenting Curse hex, Lance, Frigid 5 | -2.7 ±1.5, wins -3 | -1.1 ±1.4, wins -2 |
| XP: Warmage's Reserves for a Level 2 Lance, Destructive 2 | -2.3 ±1.1, wins -2 | -1.7 ±1.1, wins -2 |
| WM: Lance, Destructive 1, Barraging 1 | -2.2 ±1.1, wins -2 | -2.1 ±0.9, wins -2 |
| WM: Lance, Corrupting 2, all vs Vital | -3.6 ±1.7, wins -2 | -1.2 ±1.3, wins +2 |
| WM: Lance, Destructive 1, Frigid 1 | -2.7 ±1.2, wins -2 | -2.1 ±0.9, wins -2 |
| WM: Lance, Destructive 1, Kinetic 1 | -4.2 ±1.5, wins -4 | -2.6 ±1.3, wins -2 |
| WM: Lance, Frigid 2 | -5.7 ±1.8, wins -8 | -2.4 ±1.3, wins -1 |
| WM: Lance, Abjuring 2 | -6.3 ±1.9, wins -7 | -2.3 ±1.5, wins -2 |
| WM: Lance, Barraging 2 | -5.6 ±1.9, wins -6 | -3.3 ±1.3, wins -2 |
| WM: Lance, Necrotic 2 | -6.9 ±1.9, wins -8 | -3.5 ±1.3, wins -2 |
| WM: Destructive 3, no Lance | -11.4 ±2.1, wins -12 | -8.5 ±1.9, wins -8 |
| WM: Lance, Sanguine, Destructive 1 | -9.1 ±2.0, wins -10 | -11.6 ±2.2, wins -9 |

Level 3, with Shape setup on. Party B, ×2.25: wins 82%, Health left 50.8, someone Down 77%, 4.7 rounds. Party D, ×2.25: wins 80%, Health left 54.2, someone Down 63%, 5.2 rounds.

| Swap | Party B, ×2.25 | Party D, ×2.25 |
|---|---|---|
| WM4: Lance, Destructive 5 | +4.2 ±1.3, wins +5 | +3.7 ±1.4, wins +5 |
| WM4: Lance, Destructive 3, Wild Magic 2 | +2.5 ±1.2, wins +1 | +2.7 ±1.3, wins +3 |
| WM4: Lance, Destructive 3, Piercing Elements, Draw Power | +2.0 ±1.1, wins +2 | +2.2 ±1.2, wins +2 |
| XP: Shadow Jaunt for Force Missiles | +2.7 ±1.2, wins +3 | +1.0 ±0.9, wins +1 |
| XP: Wall of Shadows for a Level 2 Lance, Destructive 2 | +0.9 ±0.8, wins +3 | +1.6 ±1.6, wins +4 |
| WM4: Lance, Piercing Elements, Destructive 2, Barraging 2 | +1.5 ±1.1, wins +0 | +0.6 ±1.2, wins +0 |
| XP: the Level 4 copy at Level 3 (Lance, Destructive 2, Piercing) and a Level 1 Lance | +1.5 ±1.0, wins +1 | +0.5 ±1.2, wins +1 |
| WM4: Furrow, Destructive 3 | +0.3 ±0.3, wins +0 | +0.4 ±0.4, wins +0 |
| WM2: both Lance, Destructive 1, Wild Magic 1 | +0.0 ±1.3, wins +2 | +0.5 ±1.2, wins +2 |
| WM4: Funnel, Destructive 3 | +0.6 ±0.6, wins +0 | -0.4 ±0.9, wins -1 |
| WM4: Furrow, Frigid 2, Destructive 1 | -0.3 ±0.4, wins -0 | +0.3 ±0.7, wins +1 |
| WM4: Furrow, Necrotic 1, Destructive 2 | -0.1 ±0.1, wins +0 | +0.0 ±0.1, wins +0 |
| WM4: Nova, Destructive 3 | +0.2 ±0.6, wins -0 | -0.6 ±1.2, wins -1 |
| XP: Wall of Shadows and Gainsay for a Level 3 Lance, Destructive 2, Piercing | -0.5 ±1.3, wins +1 | -0.4 ±1.8, wins +2 |
| XP: Overchanneling for a Level 2 Lance, Destructive 2 | -1.0 ±0.9, wins -1 | -0.9 ±1.0, wins -0 |
| WM2: both Lance, Destructive 1, Barraging 1 | -1.2 ±0.8, wins -2 | -0.7 ±0.9, wins -1 |
| WM2: both Lance, Frigid 2 | -2.0 ±1.3, wins -3 | -0.0 ±1.5, wins -1 |
| XP: Gainsay for a Level 1 Lance | -1.2 ±1.2, wins -0 | -1.1 ±1.5, wins +0 |
| WM: as built, all vs Vital | -3.5 ±1.3, wins -4 | -1.4 ±1.3, wins -2 |

What it says, roughly:

- **Damage beats every rider.** Each Level 2 swap of Destructive for
  Frigid, Kinetic, Barraging, Necrotic or Abjuring costs 2-7 Health in
  Party B and 0.6-3.5 in Party D. Wild Magic and Corrupting (against
  Vital) come out even in Party D and behind in Party B. Sanguine costs
  9-12: it turns the hit's damage into Bleeding.
- **Lance is a must.** Without it War Magic only reaches next to him,
  and the copy costs 8.5-11.4 Health.
- **The Level 4 copy is best as one big single-target spell.** Lance
  and Destructive 5 is the best swap in the sweep (+3.7 to +4.2 Health,
  +5 points of wins); Destructive 3 with Wild Magic or Piercing Elements
  and Draw Power is next. The Shapes all land within a point of his own
  Furrow even when he steps in for them: stepping into a 4-meter line
  costs about what the second target pays.
- **Dodge or Vital**: a wash at Level 2, 1.4-3.5 Health worse at Level
  3 (and 6-7 with Shape setup off). The front line keeps about 2 Harried
  on his targets at both Levels, and Harried lowers Dodge, not Vital.
  Why the gap only opens at Level 3, I don't know.
- **His other Techniques**: Force Missiles for Shadow Jaunt gains 1-2.7
  Health at both Levels, and Wall of Shadows traded for another War
  Magic copy gains about a point. Trading Overchanneling, Warmage's
  Reserves or Gainsay for War Magic copies loses up to 2 (Overchanneling's
  trade breaks even in Party D at Level 2).

## Battle Maneuver options (2026-10-27)

**Units (corrected 2026-10-27):** "Health" in this section's tables and bullets is the party's Health left as a share of its max Health, in percentage points (compare_builds.py scored it that way until 10-27). At these party sizes, 40-47 max Health, a point is about 0.45 Health, about 1.8 Value. Rankings within a table hold; a swap that adds max Health (Toughened Body) reads low.

The same broad sweep for Hilde's and Browndog's Battle Maneuvers at 125
and 175 XP (`maneuver_sweep.py`): each copy swapped through the
Features, copies merged into a higher-Level one, and out-of-combat XP
(Hilde's Bound Across Mountains, Browndog's Follower) spent on more
Maneuvers. Party B and Party A, 100 fights a mix, paired. The sim uses
the copies in sheet order, the first as the opener. Hilde (L2) has
Lunging 3 then Half Guard 3; Browndog has Lunging 3, Half Guard 3,
Lunging 3 at both Levels; Hilde (L3) adds a Level 3 copy (Whirlwind,
Victorious, Ascended Blade) and a second Lunging. No sim changes this
round.

Change in Health left at the end of the fight, and in wins (points):

**Hilde (L2).** Party B ×2.75: wins 90%, Health left 69.0, someone Down 40%, 5.2 rounds. Party A ×2.25: wins 92%, Health left 69.1, someone Down 46%, 5.1 rounds.

| Swap | Party B, ×2.75 | Party A, ×2.25 |
|---|---|---|
| both as one Level 2 copy: Lunging 3, Half Guard 3 | +0.7 ±1.0, wins +1 | +1.1 ±0.8, wins +2 |
| copy 2: Turn Elements 3 (Fire Ward) | -0.5 ±0.7, wins -0 | +0.1 ±0.8, wins +0 |
| copy 2: Viper's Sting | -1.4 ±1.3, wins -1 | +0.5 ±1.2, wins +0 |
| copy 1: Viper's Sting | -0.4 ±0.4, wins +0 | -1.1 ±0.6, wins -2 |
| copy 2: Fleet Step 3 | -1.6 ±1.2, wins -2 | -0.2 ±1.0, wins -1 |
| copy 2: Victorious, Half Guard 1 | -2.2 ±0.8, wins -3 | -0.7 ±0.7, wins -1 |
| copy 2: Elemental (Fire), Half Guard 1 | -2.0 ±0.9, wins -3 | -1.3 ±0.6, wins -2 |
| copy 2: Backfoot 3 | -2.1 ±1.2, wins -3 | -1.4 ±0.8, wins -2 |
| copy 2: Wing Clip 3 | -2.9 ±0.9, wins -3 | -1.8 ±0.8, wins -2 |
| copy 2: Harrying 3 | -3.2 ±1.0, wins -4 | -1.6 ±0.8, wins -2 |
| copy 2: Lunging 3 | -3.1 ±1.0, wins -3 | -2.1 ±0.7, wins -2 |
| copy 2: Blade of Four Fates 3 | -2.9 ±1.3, wins -3 | -2.5 ±1.3, wins -2 |
| copy 2: Battering 3 | -3.4 ±0.9, wins -3 | -2.3 ±0.7, wins -2 |
| copy 2: Calculated | -3.0 ±1.0, wins -3 | -3.1 ±0.9, wins -4 |
| both as one Level 2 copy: Lunging 3, Calculated | -3.3 ±1.2, wins -4 | -2.8 ±1.0, wins -3 |
| copy 2: Hamstring 3 | -3.8 ±0.9, wins -4 | -2.6 ±0.7, wins -2 |
| copy 2: Wind Slash 3 | -3.8 ±0.9, wins -4 | -2.7 ±0.7, wins -2 |
| copy 1: Wing Clip 3 | -3.9 ±1.6, wins -4 | -2.7 ±1.4, wins -3 |
| copy 1: Harrying 3 | -4.0 ±1.5, wins -4 | -2.9 ±1.4, wins -3 |
| copy 2: Lodestone 3 | -4.3 ±1.3, wins -5 | -3.5 ±1.0, wins -4 |
| copy 1: Calculated | -4.4 ±1.6, wins -4 | -3.9 ±1.5, wins -3 |
| copy 2: Distracting 3 | -4.8 ±1.1, wins -4 | -3.9 ±0.9, wins -3 |
| both as one Level 2 copy: Calculated, Wing Clip 3 | -5.5 ±1.8, wins -6 | -5.4 ±1.6, wins -5 |

**Browndog (L2).** Party B ×2.75: wins 90%, Health left 69.0, someone Down 40%, 5.2 rounds. Party A ×2.25: wins 92%, Health left 69.1, someone Down 46%, 5.1 rounds.

| Swap | Party B, ×2.75 | Party A, ×2.25 |
|---|---|---|
| copies 2-3 as one Level 2 copy: Half Guard 3, Lunging 3 | +1.3 ±0.9, wins +0 | +1.1 ±0.6, wins +1 |
| Follower's XP: one more copy, Half Guard 3 | +1.0 ±0.3, wins +0 | +1.0 ±0.3, wins +0 |
| copies 2-3 as one Level 2 copy: Calculated, Half Guard 3 | +0.1 ±0.7, wins -1 | +1.0 ±0.6, wins +0 |
| Follower's XP: one more copy, Calculated | +0.2 ±0.3, wins +0 | +0.5 ±0.3, wins +0 |
| copy 3: Viper's Sting | -0.1 ±0.5, wins -1 | +0.4 ±0.4, wins +0 |
| copy 2: Viper's Sting | -0.6 ±1.5, wins +0 | +0.5 ±1.3, wins +0 |
| copy 3: Harrying 3 | -0.1 ±0.6, wins -1 | +0.0 ±0.2, wins -0 |
| copy 3: Calculated | -0.3 ±0.5, wins -1 | +0.1 ±0.3, wins -0 |
| copy 2: Elemental (Fire), Half Guard 1 | -1.2 ±0.5, wins -0 | -1.1 ±0.4, wins -1 |
| copy 2: Lunging 3 | -1.3 ±0.8, wins +0 | -1.1 ±0.8, wins +0 |
| copy 2: Victorious, Half Guard 1 | -1.4 ±0.3, wins -1 | -1.1 ±0.4, wins -0 |
| copy 2: Turn Elements 3 (Fire Ward) | -1.2 ±0.6, wins +0 | -1.8 ±0.5, wins -0 |
| copy 2: Backfoot 3 | -2.0 ±0.5, wins -0 | -2.0 ±0.5, wins -1 |
| copy 2: Fleet Step 3 | -2.0 ±0.7, wins +0 | -2.1 ±0.6, wins -1 |
| copy 2: Blade of Four Fates 3 | -1.9 ±0.9, wins +0 | -2.3 ±0.8, wins -0 |
| copy 2: Wing Clip 3 | -2.1 ±0.5, wins -0 | -2.3 ±0.5, wins -2 |
| copy 2: Harrying 3 | -2.3 ±0.6, wins -0 | -2.3 ±0.6, wins -0 |
| copy 2: Battering 3 | -2.5 ±0.5, wins -0 | -2.3 ±0.6, wins -1 |
| copy 2: Lodestone 3 | -2.4 ±0.7, wins -1 | -2.5 ±0.7, wins -1 |
| copy 2: Calculated | -2.6 ±0.7, wins -1 | -2.3 ±0.6, wins -1 |
| copy 2: Distracting 3 | -2.5 ±0.6, wins -0 | -2.6 ±0.6, wins -2 |
| copy 2: Hamstring 3 | -2.6 ±0.5, wins -0 | -2.6 ±0.5, wins -1 |
| copy 2: Wind Slash 3 | -2.6 ±0.5, wins -0 | -2.7 ±0.5, wins -2 |

**Hilde (L3).** Party B ×2.25: wins 81%, Health left 51.2, someone Down 76%, 4.8 rounds. Party A ×2.0: wins 68%, Health left 42.5, someone Down 82%, 5.7 rounds.

| Swap | Party B, ×2.25 | Party A, ×2.0 |
|---|---|---|
| Level 3 copy: Whirlwind, Viper's Sting, Half Guard 1 | +2.9 ±1.5, wins +4 | +3.2 ±1.6, wins +4 |
| Level 3 copy: Calculated, Viper's Sting, Lunging 3 | +2.6 ±1.4, wins +3 | +3.1 ±1.4, wins +4 |
| Level 3 copy: Flurry, Calculated | +1.2 ±1.1, wins +4 | +1.8 ±1.4, wins +3 |
| Bound Across Mountains' XP: a Level 2 copy, Calculated, Half Guard 3 | +1.1 ±0.4, wins +0 | +1.9 ±0.7, wins +3 |
| Bound Across Mountains' XP: two more copies, Half Guard 3 and Calculated | +0.7 ±0.3, wins +0 | +1.7 ±0.6, wins +3 |
| Level 3 copy: Flurry, Wing Clip 3 | +0.8 ±1.1, wins +2 | +1.2 ±1.3, wins +2 |
| Level 3 copy: Flurry, Lunging 3 | +0.6 ±1.1, wins +2 | +1.0 ±1.3, wins +1 |
| Level 3 copy: Whirlwind, Calculated, Half Guard 1 | -0.3 ±0.8, wins +0 | +1.0 ±1.0, wins +2 |
| Level 3 copy: Whirlwind, Victorious, Elemental (Fire) | +0.0 ±0.0, wins +0 | +0.0 ±0.0, wins +0 |
| Level 3 copy: Calculated, Wing Clip 3, Harrying 3 | -0.6 ±0.9, wins -0 | -0.7 ±1.2, wins -1 |
| Level 3 copy: Whirlwind, Wing Clip 4 | -0.9 ±0.8, wins -1 | -0.8 ±0.9, wins -0 |
| Level 3 copy: Whirlwind, Harrying 4 | -1.2 ±0.7, wins -2 | -1.3 ±0.9, wins -1 |
| copy 3: Wing Clip 3 | -0.8 ±0.7, wins -0 | -1.9 ±0.9, wins -3 |
| Level 3 copy: Whirlwind, Battering 4 | -1.7 ±0.8, wins -2 | -1.3 ±0.8, wins -2 |
| copy 3: Calculated | -1.3 ±0.7, wins -1 | -2.3 ±1.0, wins -3 |
| copy 3: Harrying 3 | -1.7 ±0.6, wins -2 | -2.0 ±0.8, wins -3 |
| copy 3: Battering 3 | -1.4 ±0.5, wins -1 | -2.4 ±0.9, wins -3 |

**Browndog (L3).** Party B ×2.25: wins 81%, Health left 51.2, someone Down 76%, 4.8 rounds. Party A ×2.0: wins 68%, Health left 42.5, someone Down 82%, 5.7 rounds.

| Swap | Party B, ×2.25 | Party A, ×2.0 |
|---|---|---|
| Follower's XP: one more copy, Half Guard 3 | +0.8 ±0.3, wins +1 | +1.0 ±0.3, wins +1 |
| copies 2-3 and Follower's XP as one Level 3 copy: Flurry, Half Guard 3 | +0.2 ±0.8, wins +0 | +1.2 ±0.8, wins +2 |
| Follower's XP: one more copy, Calculated | +0.1 ±0.3, wins +0 | +0.7 ±0.4, wins +2 |
| copies 2-3 and Follower's XP as one Level 3 copy: Whirlwind, Half Guard 3, Lunging 1 | -0.8 ±0.7, wins -1 | -0.1 ±0.7, wins -1 |
| all three as one Level 3 copy: Flurry, Calculated | -1.7 ±1.5, wins +0 | +0.5 ±1.6, wins +1 |
| all three as one Level 3 copy: Flurry, Lunging 3 | -0.8 ±1.4, wins +1 | -0.5 ±1.4, wins -1 |
| copy 2: Fleet Step 3 | -0.7 ±0.7, wins +1 | -1.1 ±1.0, wins -2 |
| copy 2: Wing Clip 3 | -1.7 ±0.4, wins -1 | -1.3 ±0.5, wins -2 |
| copy 2: Backfoot 3 | -1.9 ±0.6, wins -1 | -1.3 ±0.9, wins -2 |
| copy 2: Calculated | -2.2 ±0.5, wins -2 | -1.3 ±0.8, wins -2 |
| copy 2: Battering 3 | -2.2 ±0.4, wins -1 | -1.4 ±0.6, wins -1 |
| copy 2: Harrying 3 | -2.1 ±0.4, wins -2 | -1.9 ±0.7, wins -2 |
| all three as one Level 3 copy: Calculated 3 | -3.5 ±1.2, wins -2 | -1.1 ±1.5, wins -2 |
| all three as one Level 3 copy: Whirlwind, Calculated, Lunging 1 | -3.4 ±1.1, wins -2 | -2.9 ±1.4, wins -5 |

What it says, roughly:

- **Half Guard is the standout.** Swapping a Half Guard 3 copy for
  another 3-point pick costs up to 5 Health for Hilde and up to 2.7 for
  Browndog; only Viper's Sting, Fleet Step and a Fire Ward come out
  about even, and only for Hilde. An extra Half Guard copy bought with Follower's 3 XP gains about a
  point. Protected is used up stack for stack, so Half Guard 3 + Spades
  blocks about 3.5 damage on a front-liner who's being hit; none of the
  3-stack debuffs do as much.
- **The debuff riders bunch up.** Wing Clip, Harrying, Hamstring,
  Battering, Backfoot, Lodestone, Fleet Step, Blade of Four Fates and
  Wind Slash land within a point or two of each other, all behind Half
  Guard. Distracting and Lodestone come last for Hilde. These reps can't
  rank them further.
- **Calculated** (Good Luck on one attack, 3 points) is no better than
  the riders on a Level 1 copy, and Calculated 3 is among the worst ways
  to merge Browndog's copies.
- **Hilde's opening Lunging is worth keeping**: swapping it for a rider
  or Calculated costs 3-4, for Viper's Sting about 1.
  Browndog's second Lunging copy isn't: anything in its place comes out
  even.
- **Viper's Sting** is a wash on a Level 1 copy, but it's the best thing
  for Hilde's Level 3 copy: Whirlwind + Viper's Sting + Half Guard 1,
  or Calculated + Viper's Sting + Lunging 3, gain 2.6-3.2 Health. The
  turn she uses that copy she can move and still attack twice, about
  half an attack more a fight. Victorious and Ascended Blade add little,
  and Elemental (Fire) in place of Ascended Blade changes nothing,
  since enemies have one Resist for every element. Flurry with
  Calculated gains 1.2-1.8 again.
- **One Level 2 copy with Lunging 3 and Half Guard 3** beats two Level 1
  copies a little (+0.7 to +1.3 for both of them), presumably because the
  Half Guard comes with the opener. Merging all three of Browndog's
  copies into one Level 3 copy loses up to 3.5; the two Flurry versions
  come out about even.
- **Out-of-combat XP into Maneuvers** gains 0.1-1.9 (Bound Across
  Mountains for Hilde, Follower for Browndog), with Half Guard copies at
  the top.

## Mechanic baseline (2026-10-27)

Per the designer: a broad pulse on what each mechanic the Buildable
Techniques deliver is worth, for adjusting the weights
(`mechanic_baseline.py`). Each test character carries one Technique copy
with its Feature points left unspent; each test spends them on one
Feature, paired on the same seeds against that bare copy, in one or two
parties at table toughness (fights of about five rounds). Scored the
effect check's way: the party's Health left in points, losses 0, turned
into Value with a Health ladder (+2 Health on every PC; one PC's +1
Health is 4). The ladders put one point of party Health left at 3.7-4.8
Value. 100 fights a mix, so margins run ±0.5 to ±3: read the patterns,
not single cells.

"Stacks landed" is what the Feature added over the bare copy, counted
from the trace (healing too). "THE TABEL for them" prices those stacks
at THE TABEL's base rates with no realization discount (healing at
Health's 4), so it's the most THE TABEL would credit them. Half Guard's
Protected on the carrier isn't in the count. "Own damage dealt" is the
carrier's change in damage landed.

To run it, the sim needed the last three War Magic Features: Arcane
Chant (spends AP that won't buy another attack on more of the Spell's
own Destructive or rider), Glacier (Difficult Terrain, now in
`movement.py`; the Play Style plans that set a PC's spot directly don't
pay it yet) and Channel. Every combat Feature of every Buildable is in
now; Social Maneuver's are social.

#### Hilde (L2) (hilde2)

| Feature | Points | B2: Value (±) | A2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Lunging | 3 | +1.2 ±0.7 | +1.0 ±0.8 | +0.4 | - | -0.1 | +0.6 |
| Wind Slash (melee, rerun 10-27) | 3 | -1.0 ±1.4 | -0.2 ±1.5 | -0.2 | - | -0.1 | -0.1 |
| Distracting | 3 | -1.7 ±1.2 | -2.4 ±1.3 | -0.7 | Taunted +3.3, healed +0.1 | +7.6 | -0.8 |
| Battering | 3 | +0.6 ±0.5 | +0.6 ±0.6 | +0.2 | Bleeding +3.3 | +13.1 | -0.1 |
| Wing Clip | 3 | +1.4 ±0.8 | +1.6 ±0.9 | +0.5 | Crippled +3.2 | +4.7 | +0.3 |
| Harrying | 3 | +0.9 ±0.7 | +1.9 ±0.9 | +0.5 | Harried +4.2 | +4.1 | +0.0 |
| Hamstring | 3 | +0.0 ±0.0 | +0.1 ±0.3 | +0.0 | Slowed +3.1 | +3.4 | +0.0 |
| Backfoot | 3 | +2.9 ±1.5 | +2.3 ±1.0 | +0.9 | Staggered +2.1 | +2.8 | +0.5 |
| Lodestone | 3 | -0.9 ±2.0 | -1.5 ±1.4 | -0.4 | Pushed +4.4, Hasted +0.1, Protected +0.1 | +4.3 | +0.3 |
| Half Guard | 3 | +6.4 ±1.6 | +5.0 ±1.3 | +1.9 | , healed -0.1 | -0.4 | +1.6 |
| Blade of Four Fates | 3 | +1.4 ±1.9 | +0.3 ±2.2 | +0.3 | Hasted +0.1, Protected +0.1 | +0.1 | +1.3 |
| Fleet Step | 3 | +3.6 ±1.6 | +4.7 ±1.7 | +1.4 | Outflanked +2.5, Hasted +0.1, Protected +0.1 | +3.7 | +2.2 |
| Turn Elements (Fire) | 3 | +5.5 ±1.7 | +5.1 ±1.4 | +1.8 | Ward +3.2 | +3.1 | +1.1 |
| Calculated | 3 | +1.3 ±0.7 | -0.8 ±1.2 | +0.1 | - | +0.1 | +0.6 |
| Viper's Sting | 3 | +4.0 ±1.9 | +6.0 ±2.3 | +1.7 | Hasted +0.2, Protected +0.2 | +0.6 | +2.2 |
| Victorious | 2 | +0.9 ±0.6 | +1.4 ±0.8 | +0.6 | - | +0.2 | +0.3 |
| Elemental (Fire) | 2 | +0.8 ±0.8 | +0.4 ±0.5 | +0.3 | - | -0.1 | +0.7 |

#### Browndog (L2) (browndog2)

| Feature | Points | B2: Value (±) | D2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Lunging | 3 | +2.3 ±1.2 | +3.0 ±1.2 | +0.9 | Protected +0.1, Taunted -0.1 | -0.0 | +1.7 |
| Wind Slash (melee, rerun 10-27) | 3 | +2.8 ±1.7 | +3.1 ±1.9 | +1.0 | - | +0.0 | +1.5 |
| Distracting | 3 | +0.3 ±0.5 | +0.1 ±0.1 | +0.1 | Taunted +2.5 | +5.5 | -0.2 |
| Battering | 3 | +0.3 ±0.3 | +0.2 ±0.2 | +0.1 | Bleeding +2.5 | +9.9 | -0.2 |
| Wing Clip | 3 | +1.0 ±0.4 | +0.6 ±0.3 | +0.3 | Crippled +2.0 | +3.0 | +0.0 |
| Harrying | 3 | +0.5 ±0.7 | +0.3 ±0.4 | +0.1 | Harried +3.2 | +3.2 | +0.1 |
| Hamstring | 3 | +0.0 ±0.1 | +0.0 ±0.0 | +0.0 | Slowed +2.0 | +2.2 | +0.0 |
| Backfoot | 3 | +1.1 ±0.5 | +0.5 ±0.3 | +0.3 | Staggered +1.1 | +1.5 | +0.1 |
| Lodestone | 3 | +0.4 ±1.1 | -0.9 ±1.0 | -0.1 | Pushed +3.8 | +3.4 | +0.3 |
| Half Guard | 3 | +4.5 ±0.8 | +3.9 ±1.1 | +1.4 | , healed -0.1 | -0.4 | +0.7 |
| Blade of Four Fates | 3 | +1.2 ±1.4 | +1.0 ±1.3 | +0.4 | - | -0.2 | +0.6 |
| Fleet Step | 3 | +1.1 ±1.0 | +0.9 ±0.8 | +0.3 | Outflanked +1.3 | +1.6 | +0.8 |
| Turn Elements (Fire) | 3 | +2.4 ±1.0 | +1.1 ±0.5 | +0.6 | Ward +2.0 | +1.9 | +0.5 |
| Calculated | 3 | +0.0 ±1.0 | +0.6 ±0.7 | +0.1 | - | +0.1 | +0.6 |
| Viper's Sting | 3 | +3.5 ±2.5 | +6.8 ±2.1 | +1.7 | Taunted -0.8, Protected -0.3, healed -0.1 | -3.0 | +4.4 |
| Victorious | 2 | -0.1 ±0.4 | +0.1 ±0.5 | -0.0 | - | +0.1 | +0.2 |
| Elemental (Fire) | 2 | +0.4 ±0.6 | +0.1 ±0.4 | +0.1 | - | -0.0 | +0.6 |

#### Sable (L2) (sable2)

| Feature | Points | A2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|
| Lunging | 3 | +0.0 ±0.0 | +0.0 | - | +0.0 | +0.0 |
| Wind Slash | 3 | +0.0 ±0.0 | +0.0 | - | +0.0 | +0.0 |
| Distracting | 3 | -9.7 ±2.8 | -3.2 | Taunted +3.9 | +8.5 | -3.5 |
| Battering | 3 | +1.5 ±1.2 | +0.5 | Bleeding +3.9 | +15.6 | -0.2 |
| Wing Clip | 3 | +2.1 ±1.2 | +0.7 | Crippled +3.8 | +5.7 | +0.0 |
| Harrying | 3 | +2.5 ±1.8 | +0.8 | Harried +4.9 | +4.9 | +1.1 |
| Hamstring | 3 | +6.2 ±2.5 | +2.1 | Slowed +4.0 | +4.4 | +0.0 |
| Backfoot | 3 | +1.9 ±2.0 | +0.6 | Staggered +2.9 | +4.0 | +0.1 |
| Lodestone | 3 | +2.8 ±2.6 | +0.9 | Pushed +5.8 | +5.1 | -0.1 |
| Half Guard | 3 | +3.6 ±1.5 | +1.2 | - | +0.0 | +0.7 |
| Blade of Four Fates | 3 | -0.2 ±3.3 | -0.1 | - | +0.0 | +1.2 |
| Fleet Step | 3 | +0.2 ±1.4 | +0.1 | Outflanked +0.6 | +0.8 | -0.3 |
| Turn Elements (Fire) | 3 | +4.3 ±1.7 | +1.4 | Ward +3.8 | +3.8 | +0.8 |
| Calculated | 3 | -0.3 ±3.0 | -0.1 | - | +0.0 | +1.3 |
| Viper's Sting | 3 | +2.5 ±2.1 | +0.8 | - | +0.0 | +0.6 |
| Victorious | 2 | +0.0 ±1.0 | +0.0 | - | +0.0 | +0.0 |
| Elemental (Fire) | 2 | +1.9 ±1.7 | +0.9 | - | +0.0 | +0.6 |

#### Jackal (L3) (jackal3)

| Feature | Points | B3: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|
| Lunging | 3 | +0.0 ±0.0 | +0.0 | - | +0.0 | +0.0 |
| Wind Slash | 3 | -0.1 ±0.1 | -0.0 | - | +0.0 | +0.0 |
| Distracting | 3 | -0.8 ±1.6 | -0.3 | Taunted +2.6 | +5.6 | -0.8 |
| Battering | 3 | +0.6 ±0.5 | +0.2 | Bleeding +2.7 | +10.6 | +0.0 |
| Wing Clip | 3 | +1.3 ±0.6 | +0.4 | Crippled +2.6 | +4.0 | +0.2 |
| Harrying | 3 | +0.5 ±0.5 | +0.2 | Harried +3.4 | +3.4 | +0.1 |
| Hamstring | 3 | +0.1 ±0.6 | +0.0 | Slowed +2.6 | +2.9 | +0.1 |
| Backfoot | 3 | +1.9 ±1.4 | +0.6 | Staggered +2.0 | +2.7 | +0.7 |
| Lodestone | 3 | -3.0 ±2.4 | -1.0 | Pushed +3.4 | +3.1 | +0.1 |
| Half Guard | 3 | +5.4 ±1.6 | +1.8 | - | +0.0 | +2.4 |
| Blade of Four Fates | 3 | -2.0 ±2.3 | -0.7 | - | +0.0 | +0.1 |
| Fleet Step | 3 | +1.1 ±1.5 | +0.4 | Outflanked +1.5 | +2.0 | +1.4 |
| Turn Elements (Fire) | 3 | +1.8 ±1.1 | +0.6 | Ward +2.5 | +2.5 | +0.6 |
| Calculated | 3 | +0.5 ±1.2 | +0.2 | - | +0.0 | +0.5 |
| Viper's Sting | 3 | +0.2 ±0.6 | +0.1 | - | +0.0 | +0.2 |
| Victorious | 2 | +0.7 ±0.7 | +0.3 | - | +0.0 | +0.5 |
| Elemental (Fire) | 2 | +0.7 ±1.2 | +0.4 | - | +0.0 | +1.0 |

#### Beornhard (L2) (beornhard2)

| Feature | Points | B2: Value (±) | D2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Destructive | 2 | +12.0 ±3.2 | +5.8 ±2.1 | +4.4 | - | +0.0 | +7.1 |
| Frigid | 2 | +2.4 ±1.9 | +2.0 ±1.3 | +1.1 | Slowed +16.6 | +18.2 | +0.2 |
| Glacier | 2 | -4.8 ±2.5 | -3.0 ±1.8 | -1.9 | - | +0.0 | +0.2 |
| Kinetic | 2 | +2.2 ±2.4 | -0.5 ±1.9 | +0.4 | Pushed +6.3 | +5.6 | +0.2 |
| Corrupting (all vs Vital) | 2 | +5.8 ±1.8 | +3.9 ±1.6 | +2.4 | Vulnerable +11.2 | +11.2 | +7.7 |
| Necrotic | 2 | +0.4 ±0.3 | +0.3 ±0.2 | +0.2 | Necrotic +16.4 | +49.2 | +0.2 |
| Barraging | 2 | +2.5 ±1.1 | +0.6 ±0.4 | +0.8 | Harried +9.2 | +9.2 | +0.3 |
| Abjuring | 2 | +1.3 ±1.1 | +2.2 ±1.0 | +0.9 | Ward +13.1 | +13.1 | +0.4 |
| Wild Magic | 2 | +6.9 ±3.2 | +7.7 ±2.4 | +3.6 | - | +0.0 | +6.2 |
| Sanguine | 1 | -3.3 ±2.4 | -13.0 ±3.1 | -8.2 | Bleeding +17.5 | +69.8 | -9.1 |
| Arcane Chant, Destructive 1 | 2 | +9.6 ±2.9 | +4.9 ±2.2 | +3.6 | - | +0.0 | +6.3 |
| Destructive 1 (half) | 1 | +6.9 ±2.6 | +2.1 ±1.9 | +4.5 | - | +0.0 | +2.7 |

#### Beornhard (L3) (beornhard3)

| Feature | Points | B3: Value (±) | D3: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Destructive 5 | 5 | +8.3 ±2.2 | +9.2 ±2.6 | +1.8 | - | +0.0 | +8.1 |
| Piercing Elements | 1 | +0.3 ±0.9 | +0.2 ±0.7 | +0.3 | - | +0.0 | +0.1 |
| Draw Power | 1 | +0.0 ±0.0 | +0.0 ±0.0 | +0.0 | - | +0.0 | +0.0 |
| Channel | 3 | -0.0 ±0.3 | +0.0 ±0.5 | +0.0 | - | +0.0 | +0.0 |
| Furrow (no Lance) | 3 | -1.2 ±2.1 | -0.3 ±2.9 | -0.3 | - | +0.0 | +0.8 |
| Funnel (no Lance) | 3 | -1.0 ±2.1 | -1.0 ±2.5 | -0.3 | - | +0.0 | +0.7 |
| Nova (no Lance) | 3 | -2.1 ±2.0 | -2.4 ±2.4 | -0.7 | - | +0.0 | +0.0 |

#### Hanforth (L2) (hanforth2sb)

| Feature | Points | D2: Value (±) | H2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Shielding | 3 | +1.7 ±2.0 | -0.1 ±2.2 | +0.3 | Protected +3.6, Pushed +0.2, Crippled +0.1, healed +0.1 | +11.5 | -1.5 |
| Step of Air | 3 | +0.6 ±1.6 | +0.4 ±0.9 | +0.2 | Hasted +4.0, Pushed +0.2 | +2.4 | -0.5 |
| Turn Elements (Fire) | 3 | -1.3 ±2.0 | -1.3 ±2.0 | -0.4 | Ward +3.6, Pushed +0.2, healed +0.1 | +4.2 | -1.9 |
| Retribution | 3 | -1.7 ±1.9 | -2.8 ±1.9 | -0.8 | Pushed +0.2, healed +0.2 | +0.8 | -2.0 |
| River's Might | 3 | +0.4 ±1.5 | -1.4 ±2.1 | -0.2 | Pushed +0.5 | +0.5 | -0.8 |
| Touch of Chaos | 3 | +0.8 ±1.7 | +0.4 ±2.1 | +0.2 | - | +0.2 | -0.2 |
| Elemental Enhancement (Fire) | 3 | +0.9 ±0.5 | +0.4 ±0.6 | +0.2 | - | -0.2 | +0.0 |
| Steady, Embolden | 2 | -0.8 ±2.0 | -0.9 ±1.9 | -0.4 | Pushed +0.1 | +0.1 | -0.3 |
| Quickened, Shielding 2 | 3 | +1.1 ±2.1 | -0.6 ±2.2 | +0.1 | Protected +2.7, Crippled +0.2, Pushed +0.2 | +8.5 | -0.5 |

#### Hanforth (L2) (hanforth2hm)

| Feature | Points | D2: Value (±) | H2: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|---|
| Vitality 2 | 4 | +3.9 ±1.0 | +2.7 ±0.9 | +0.8 | , healed +0.7 | +2.9 | +0.2 |
| Triage, Reach | 4 | +5.4 ±1.3 | +5.0 ±1.6 | +1.3 | , healed +1.0 | +4.1 | -0.3 |
| Guardian Angel 4 | 4 | +2.2 ±1.1 | +2.1 ±1.2 | +0.5 | - | +0.1 | +0.2 |
| Purify 4 | 4 | +0.1 ±0.1 | +0.1 ±0.1 | +0.0 | - | +0.0 | +0.0 |
| Rejuvenate, Vitality 1, Reach | 4 | -1.2 ±1.4 | -0.4 ±1.1 | -0.2 | , healed -0.9 | -3.8 | -0.4 |
| Reach | 1 | -0.0 ±0.7 | +1.4 ±1.1 | +0.7 | , healed +0.2 | +0.6 | -0.4 |

#### Hanforth (L3) (hanforth3hm)

| Feature | Points | D3: Value (±) | Value/point | Stacks landed a fight | THE TABEL for them | Own damage dealt |
|---|---|---|---|---|---|---|
| Vitality 4 | 8 | +7.7 ±2.0 | +1.0 | Protected +0.2, Crippled +0.1, Pushed +0.1, healed +1.6 | +7.3 | +0.3 |
| Healing Pact, Vitality 1, Reach | 8 | +4.2 ±1.6 | +0.5 | Protected +0.1, Crippled +0.1, healed +0.6 | +2.8 | +0.1 |
| Triage, Vitality 2, Reach | 8 | +8.6 ±2.2 | +1.1 | Protected +0.2, Crippled +0.1, Pushed +0.1, healed +1.7 | +7.6 | +0.2 |
| Guardian Angel 8 | 8 | +11.0 ±2.7 | +1.4 | Protected +0.4, Crippled +0.2, Pushed +0.1 | +1.6 | +0.9 |

Value per point of Health left: A2 4.1, B2 3.9, B3 4.5, D2 3.7, D3 4.8, H2 3.7

### What each mechanic did, against THE TABEL

Measured Value a fight, against THE TABEL's price for the stacks it
landed, across the carriers above:

| Mechanic (Feature) | Measured | THE TABEL for the stacks | Roughly |
|---|---|---|---|
| Damage (Destructive, War Magic) | +2 to +12 | about 12-14 (2 a point a cast, about 3.5 casts) | 0.7x |
| Bleeding (Battering) | +0.2 to +1.5 | 10-16 | 0.1x |
| Crippled (Wing Clip) | +0.6 to +2.1 | 3-6 | 0.3x |
| Harried (Harrying, Barraging) | +0.3 to +2.5 | 3-9 | 0.3x |
| Taunt (Distracting) | -9.7 to +0.3 | 5.5-8.5 | 0 from a tank, worse from anyone else |
| Slowed (Hamstring, Frigid) | 0 (melee) to +6.2 (Sable, a bow) | 2-18 | depends on whether the target has to walk |
| Push (Lodestone, Kinetic) | -3 to +2.8 | 3-6 | about 0 |
| Stagger (Backfoot) | +0.5 to +2.9 | 1.5-4 | 0.7x |
| Outflank (Fleet Step) | +0.2 to +4.7 | 0.8-3.7 | about 1x |
| Ward (Turn Elements, Abjuring) | -1.3 to +5.5 | 2-13 | about 1x on a Maneuver; 0.1x from Abjuring; below 0 from a blessing |
| Protected, self on a hit (Half Guard) | +3.6 to +6.4 | about 6 (3.25 stacks x 3 x hit chance) | about 1x |
| Protected, from a blessing (Shielding) | -0.1 to +1.7 | 8.5-11.5 | 0.1x |
| Hasted (Step of Air) | +0.4 to +0.6 | 2.4 | 0.2x |
| Vulnerable (Corrupting, all vs Vital) | +3.9 to +5.8 | 11 | 0.4x |
| Necrotic | +0.3 to +0.4 | 49 | about 0, as its Weak column says |
| Good Luck once (Calculated) | -0.8 to +1.3 | 2.4 | 0.2x |
| Sift (Blade of Four Fates; Wild Magic on a spell) | -2 to +1.4; +6.9 to +7.7 | not counted; about 13-34 by hand (21 sifts a fight at 0.6-1.62) | about 0 on a Maneuver; good on a spell |
| 1 AP once (Viper's Sting) | +3.5 to +6.8 melee; +0.2 to +2.5 ranged | 2.75 | 2x melee, 0.5x ranged |
| A card (Victorious, Draw Power) | 0 to +1.4 | up to 2.7 | small |
| Healing (Vitality, Triage) | +2.7 to +8.6 | +2.9 to +7.6 (healing x 4) | about 1x |
| Stopping a Down (Guardian Angel) | +2.1 to +11 | none | not in THE TABEL |

What it says, roughly:

- **Damage and healing land close to their weights; most debuffs don't.**
  Damage realizes about 0.7 of THE TABEL's 2 a point at table toughness
  (×2-2.75 enemy Health, which dilutes every point of damage), and
  healing lands at about its 4 a point. Bleeding, Crippled, Harried,
  Hasted, Good Luck once and Shielding realize a tenth to a third of
  their base rates as one-a-fight riders. That's the base rate against
  what actually happened, so it's consistent with the Weak/Average
  columns being well below the base rates.
- **Who carries it matters as much as what it is.** Taunt is about zero
  from Browndog and a big loss from Sable or Hilde. Slowed is nothing
  from a melee carrier (the target's already next to her) and the best
  Maneuver pick for Sable (+6.2). The 1 AP from Viper's Sting is worth
  twice its 2.75 to a melee carrier and half to an archer. Protected on
  the person being hit (Half Guard) is worth its full 3 a stack; handed
  out by a blessing, a tenth.
- **A Feature point isn't worth the same across Techniques.** The best
  picks buy about 2 Value a point on a Battle Maneuver (Half Guard,
  Hamstring on an archer, Viper's Sting), 3.6-4.5 on War Magic
  (Destructive, Wild Magic, Arcane Chant), 1-1.4 on Healing Magic
  (Triage, Guardian Angel) and 0.3 on Spirit Blessing. Spirit Blessing's Features are the cheapest in
  practice, and its budget grows slowest.
- **Down prevention needs a term.** Guardian Angel 8 is +11, the best
  healing pick, and THE TABEL has nothing for it. Lifeline is the same
  story.
- **Glacier costs the party** (-3 to -4.8): its Difficult Terrain sits
  around the enemies the front-liners are walking up to.
- **Wind Slash** on a melee weapon gives reach, per the designer
  (10-27; the first run had it doing nothing, and the two melee rows are
  the rerun). It's worth about 1 Value a Feature point for Browndog and nothing
  for Hilde, whose Wind Slash copy comes after her Lunging opener, when
  she's already in melee. On a thrown weapon or a bow the extra range
  rarely comes up. A Diver takes the long reach only when it gets as
  many attacks that turn as walking up (`combat_sim._diver_reach`), and
  every attack now checks range again first (`tunables.RECHECK_RANGE`),
  so an attack after the reach one walks in or stops; before, it went
  off from wherever she stood. That changed nothing in the regression
  or the Level 3 calibration.

Where the weights could move, for the designer: on-hit debuff riders
priced off their Average or Weak columns instead of the base rates
(Bleeding hardest); Taunt priced by who's taunting; Protected split into
self-on-a-hit (keep 3) and handed-out (much lower); 1 AP split by melee
and ranged; a term for stopping a Down; and Spirit Blessing's Feature
costs or budget looked at against the rest.

## Party tactics (2026-10-27, later)

Per the designer: the sim should switch the whole party between playing
cautious, staying at max range, diving in and so on, as one switch.
`party_tactics.py` holds the presets: each hands out a Play Style by
role (front-liner, other melee, ranged, support), and can set the
party's targeting and a few tunables. They combine with "+" ("max
range+focus fire"). `tunables.PARTY_TACTIC`, `-t` on `calibrate.py`,
`compare_builds.py` and the sweep studies, or `tactics_compare.py` to
run a party under every preset. With none set, each PC plays its own
Play Style column, as before, and the regression is unchanged.

Three new Play Styles in `play_styles.py` for the presets to hand out
(the turn planners are a table now, `PLANNERS`):

- **Kiter**: a shooter that keeps 6 spaces (KITE_KEEP_AWAY) from every
  enemy, or one less than its reach, and backs off when anything gets
  close.
- **Holder**: attacks what's in reach, takes one step for a target at
  most, and otherwise waits, but only while a melee enemy within 8
  spaces is on its way. The first version also waited on archers and
  casters who never walk in, and lost a fifth to a third more fights.
- **Guardian**: sticks with the frailest ally who hangs back and fights
  whatever gets within 2 of them, staying by them while a melee enemy is
  coming; with none coming it skirmishes.

Each preset against the party as built, paired, 100 fights a mix:
change in Health left (points) and in how often someone goes Down.

As built: Party A, L2, ×2.25: wins 92%, Health left 31.8, someone Down 46%, 5.1 rounds; Party B, L2, ×2.75: wins 90%, Health left 29.6, someone Down 40%, 5.2 rounds; Party D, L2, ×1.75: wins 96%, Health left 33.9, someone Down 33%, 4.6 rounds; Party B, L3, ×2.25: wins 81%, Health left 23.6, someone Down 76%, 4.8 rounds.

| Tactic | Party A, L2, ×2.25 | Party B, L2, ×2.75 | Party D, L2, ×1.75 | Party B, L3, ×2.25 |
|---|---|---|---|---|
| all in | +0.4 ±0.7, Down -3 | +0.3 ±0.6, Down +0 | +1.2 ±0.7, Down -4 | -0.3 ±0.7, Down -2 |
| focus fire | +0.8 ±0.6, Down -3 | -0.5 ±0.6, Down +2 | -0.3 ±0.5, Down -1 | +0.1 ±0.7, Down -2 |
| finish the weakest | -0.5 ±0.8, Down +1 | -1.6 ±0.8, Down +5 | -0.5 ±0.7, Down -1 | -0.9 ±0.8, Down +3 |
| nearest first | -0.4 ±0.7, Down +2 | -1.4 ±0.7, Down +4 | -0.3 ±0.6, Down -1 | -1.8 ±0.9, Down +2 |
| bodyguard | -1.2 ±0.9, Down +0 | -1.8 ±0.8, Down +5 | -1.3 ±0.8, Down +1 | -0.9 ±0.8, Down -1 |
| cautious | -1.2 ±0.9, Down +2 | -2.3 ±0.9, Down +10 | -0.8 ±0.8, Down -2 | -1.4 ±0.9, Down +0 |
| max range | -0.9 ±0.5, Down +2 | -2.6 ±0.6, Down +4 | -1.9 ±0.6, Down +5 | -2.0 ±0.7, Down +2 |
| hold the line | -2.5 ±1.0, Down +4 | -3.2 ±1.0, Down +13 | -1.3 ±0.8, Down -0 | -2.4 ±0.9, Down +0 |

The sample parties are built to fight forward, and it shows: the party
as built, "all in" and "focus fire" land within about a point of each
other, and every more careful preset costs 1-3 Health a fight and makes
fights longer. "Hold the line" costs the most, and Party B at Level 2 goes
Down 13 points more often with it. That's the sim's turn planners, not
how a table plays a careful party, so read these as what each style
does to these builds rather than which one is right.

## Still to do

- **Items.** The sim doesn't model items yet beyond weapons, armor and
  Jackal's Bottomless Bottles. They matter more as characters level, so
  per the designer (2026-10-09): test their impact once the sample roster
  reaches about Level 3.
- **The other four leveled builds** (Sable, Felix, Enith, Ashleigh),
  from the designer.
- **Healing and Blessing magic pass** (designer, 2026-10-26): how
  healers and support scale. Groundwork in "Healing and blessing at
  Levels 1-3" above.
- **Pick table toughness** (×1.75 or ×2.0) with the designer, then move
  the scripts' defaults.
- **Re-run the Weak/Average/Strong columns** (`effect_check.py`) once
  the roster's complete; they're on the old Party A.
- **Level 2 and 3 enemy tuning**: the leveled builds outrun their own
  Level's encounters (table above, and `balance_weights_notes.md`). Fix
  the enemies, the characters or THE TABEL's baseline: the designer's
  call.
- **Card rescues on Encounter attacks**: the party spends cards to save
  any big attack that misses, so Beornhard's War Magic lands 96-99% of
  the time. Check that against how the table spends cards.
- **Lifeline** is strong enough to look at: at ×1.75, Level 2 Party D's
  someone-Down is 16% with it and 33% without.
- **Retribution Aura** cost the Level 2 Party A a fifth of its Health
  when all four Warband enemies had it, far over the draft's one-pick
  estimate. Worth pricing before a sample enemy carries it.
- **Weights from the mechanic baseline** (2026-10-27): the designer's
  call on the adjustments listed there.
- **Shape setup** (`tunables.SHAPE_SETUP`): turn it on? It's how a
  player would use a Furrow, Funnel or Nova copy, but it moves Party B's
  Level 3 numbers a little, so it waits for the designer.
- **Wall of Shadows** seldom pays: Beornhard (L3) put it up in 9 of 240
  fights against Level 2 encounters, since it blocks his own spells too,
  and the shooters it would block die fast anyway.
- **The deferred Techniques** (`coverage.py` lists all 35 with what
  each needs). Summons (seven Techniques) are the biggest group, and the
  most work.
- **Sanguine wants an overhaul** (designer, 2026-10-28; not now). Under
  the current Bleeding rule (half the stacks, rounded up, at the end of
  the target's turn) it costs a caster's party 6.6 Health a fight
  (Beornhard; Enith 1.4): it turns the whole hit into Bleeding, which
  pays out over the target's next few turns, some of it after the target
  is Down or the fight is over.
- **The Assassin tactic** (designer, 2026-10-28): "all else equal,
  assassin enemies are going to intuit 'softest target' by whichever PC
  is wearing the lightest armor". `ASSASSIN_READS = 'softest'` is the
  default: hurt worst first (share of Health lost), then the lightest
  armor, then chance. The old reading ('current') went for the least
  current Health, so at full Health every Assassin picked whoever was
  first in the party list, and a point off one PC's max Health moved them
  all onto that PC (Felix's party +6.4 Health with Felix on 9 instead of
  10). Level 1-2 calibrate parties got rougher (someone Wounded 36-47% ->
  55-76%); Level 3 about the same.
- **Interrupts happen before their trigger** (designer, 2026-10-28;
  RULES_DESIGN.md). Checked every modeled one: Gainsay, Magehunter, Bark
  Turns the Blade, Lifeline, Raise Spirits, Arrow Finds Only Mist and
  Lend Bulwark all resolve before their trigger, and an attacker Downed
  by one never attacks. Mind and Body Unbroken used to restore the PC
  after the Down landed and missed Downs from Bleeding; it's now at
  `pc_would_drop`, before the Health comes off, from any source. Parting
  Shot resolves after the enemy has stepped away, which comes out the
  same (a Downed enemy doesn't attack).
- **Attack Interrupts, my rules to confirm** (2026-10-28). A once-a-fight
  save (Arrow Finds Only Mist before the flip, Swatting Paw and
  Slithering Hands after it) goes on an attack whose expected Health
  loss is at least `INTERRUPT_SAVE_MIN` (1.5), or that could Down the PC;
  after the flip only one that would hit. Slithering Hands' redirect
  checks the attacker's own Defense of the kind its attack named, with
  the attacker's own damage less its Resist. Seasons Pass the Forest has
  no flip of its own, so no Hearts in its Wards; it's used on the first
  damaging spell at the PC. Lend Bulwark takes an adjacent ally's attack
  when this PC's Parry is 2 better than the ally's Defense against it, or
  when the hit could Down the ally. Storm of Blades assumes the row's
  one-handed Weapon is in both hands.
- **Regaining uses, my rules to confirm** (2026-10-27, `encounter.py`):
  a spent use comes back when it outranks every attack use still in hand
  (attacks first, then Level, then damage); Vigor is spent that way as
  soon as it covers one. Willow Springs Back is paid only from AP left at
  the end of a turn: paying at the start cost Felix an attack, and his
  fights ran 0.6 rounds longer. Placeholder's Alacritous Adaptation only
  trades away utility uses not touched by round 3, for a spent attack.
- **Blood-Powered Spirit and Spellblade, my rules to confirm**
  (2026-10-27). Blood-Powered Spirit pays Health only to finish a target
  (the least X that turns this hit into a Down), and casts a spent use
  only for an attack that hits harder than the PC's own, always keeping
  half its max Health (`BLOOD_SPIRIT_HEALTH`). Paying 1 Health every
  cast, my first try, cost Felix's party 3.3 Health left and 3.5% of
  wins; as it stands Beornhard (L3) gains 2.8% wins (±2.1) and 0.3
  rounds for 0.7 Health, and Felix about breaks even. Spellblade spends
  a utility Spell untouched by round 3 (else a Spell attack the turn
  passed over) and puts Bleeding [3 x X] on the hit, or the school's
  Vulnerable / Crippled once the target's bleeding that much; on
  Hanforth (L2) it's +0.7% wins (±0.7). Its range, Push, Ward, Slowed,
  Necrotic, Shift and Protected options aren't used.
- **Every PC holds its AP pool between turns** (designer, 2026-10-27:
  AP comes at the start of the fight and at the end of each turn, so
  it's free for Interrupts). The sim used to give the pool only to a PC
  with an Interrupt, and counted Gainsay and Lifeline only while a use
  was left, so Beornhard's last Gainsay never came off his next turn.
  Now every PC has it; Level 3 Parties B and D lose 0.2 and 0.4 points
  of party Health, nothing else moves.
- **Parting Shot has two paths, for the designer** (2026-10-27 review):
  the general one (any enemy walking or Pushed out of reach, with
  `close_profile`) and an older one for a Kiting enemy's retreat, with
  the PC's own Weapon. Both spend the same use, so it can't fire twice,
  but they swing different weapons. Changing it moves the numbers.
- **One Style at a time isn't enforced** (2026-10-28). glossary.md: "You
  may only be in one Style at a time"; the sim plays every Style a
  character knows. No sample knows two yet; a build that does should list
  the one it doesn't fight in under Unmodeled until the sim picks (or
  switches) Styles itself.
- **Proposed builds for Felix, Enith, Ashleigh and Sable** (2026-10-28,
  PROPOSED_BUILDS.md): Levels 2 and 3, waiting on the designer's tweaks.
  Third pass the same day: Stats spread like the designer's (nothing
  below 2), one Technique each traded for Resilience/Composure/Insight,
  10-20% of each level-up out of combat.
- **Feint as a setup** (designer, 2026-10-28: only worth it "specifically
  aimed at setting up a target for the party to Gamble and wallop").
  `tunables.FEINT_SETUP` waits for two allies who can follow up before the
  target's turn and calls the target for them. That cuts Feint's cost to
  Enith's party from -3.5 to -1.3 points of Health left, but it never pays:
  Harried clears at the end of the target's turn, so only about 1.6 ally
  attacks follow a Feint. Waiting for three allies costs -0.7, because it
  fires half as often. What would make it pay is a rules call (longer
  Harried, damage too, cheaper); PROPOSED_BUILDS.md lists the levers.
- **Exports to rebuild** (designer, 2026-10-27: the sim always plays
  the live CSVs; rebuild the characters later). Twelve sample exports
  were made before some fixed-Level Techniques went up a Level (Felix
  (L2)'s Hand Rings the Bell was Lv 1, it's Level 2 now), so their XP
  may be off. `coverage.py` and SHEETS.md list them.
- **Rules readings to confirm** for the Techniques wired in 2026-10-27
  (each one's docstring says what it assumes). The ones most likely to
  matter: Solemn Perseverance and Mind and Body Unbroken only trigger off
  an attack's hit, not a Bleeding tick; Optimize Blood doses one patient
  a fight; Crashing Wave's Protected comes on every hit, Push or not;
  Oak Draws the Lightning's "2 rounds" is this round and the next; and
  Twin Spell only Repeats a War Magic Weapon with no Features of its
  own. When to use the cones and bursts (two targets, or one from round
  3) is my rule, not the designer's.
- **Not modeled**: Cloak and Dagger never fires for a thrower at range;
  Furrow seldom has a target in its 4-meter line; the PCs don't steer
  around an enemy's Parting Shot; enemies can't Teleport out of a
  grapple, and a Heavy Melee enemy doesn't count as two-handed.

## A whole day (2026-10-29)

Per the designer: Health left after one fight isn't the whole story. A
party that goes to bed short starts the next day short, and one that
keeps doing that loses a fight eventually. `day_sim.py` plays two fights,
the care between and after them ("Between fights" above) and the night,
and scores the party's Health in the morning. With `--days` it keeps
going, day after day, until a fight is lost (up to ten days here).

The sample parties at Level 3 (600 days each; 240 runs of up to ten days):

| Party | Enemy Health | Days won | Morning Health (of full) | More nights to full, won days | Days in a row |
|---|---|---|---|---|---|
| Enith, Felix, Jackal, Hanforth | ×1.0 | 83.5% | 29.2 of 40 | 1.55 | 2.67 |
| Browndog, Ashleigh, Sable, Beornhard | ×1.0 | 90.0% | 31.1 of 44 | 2.56 | 1.75 |
| Hilde, Carrick, Hanforth, Beornhard | ×1.0 | 87.5% | 34.2 of 43 | 0.98 | 3.08 |
| Enith, Felix, Jackal, Hanforth | ×1.25 | 63.5% | 21.5 of 40 | 1.77 | 1.11 |
| Browndog, Ashleigh, Sable, Beornhard | ×1.25 | 71.0% | 23.4 of 44 | 2.73 | 1.02 |
| Hilde, Carrick, Hanforth, Beornhard | ×1.25 | 67.7% | 25.0 of 43 | 1.34 | 1.29 |
| Hilde, Carrick, Hanforth, Beornhard | ×1.75 | 35.2% | 12.4 of 43 | 1.66 | 0.46 |

- Two fights at ×1.75, the single-fight standard, is a hard day: most
  lost days go in the second fight. ×1.0 or ×1.25 reads better for days.
- The days in a row are well short of what the day's win rate would give
  if days didn't carry over (83.5% a day would average about five days).
  That's the morning shortfall at work.
- Hanforth is often the one Downed (the Assassins read the softest
  target), and a Downed healer heals nobody after the fight.

### The optimizer's Hilde, by the morning

The optimizer's best Level 3 Hilde (`hall_of_fame/runs/hilde_l3.json`,
first entry: two Toughened Resolve, Toughened Body, Earthen Mantle
Approach, Lifeline, Essence 5) was found on Health left after one fight.
The question was whether a big pool that soaks the party's hits through
Lifeline can get its Health back. It can, well enough (1,000 days each;
400 runs of up to ten days):

| Enemy Health | Days won, sample / optimizer | Morning, optimizer less sample | Hilde still missing in the morning | Ten days in a row |
|---|---|---|---|---|
| ×1.0 | 87.1% / 99.5% | +13.97 ± 0.89 | 0.35 / 1.97 | 6% / 90% |
| ×1.25 | 68.3% / 96.4% | +18.76 ± 1.19 | 0.57 / 3.78 | 0% / 54% |
| ×1.75 | 35.2% / 81.4% | +21.87 ± 1.39 | 0.82 / 6.63 | 0% / 4% |

She does wake up short (Body 3 heals 3 a night), but the rest of the
party wakes up nearly full, and they win so much more often that it
doesn't catch up with them. What each part is worth (×1.25, 600 days,
against the sample party's morning):

| Build | Days won | Morning | Against the sample |
|---|---|---|---|
| The optimizer's build | 96.7% | 44.0 of 51 | +19.06 ± 1.53 |
| without Lifeline | 80.5% | 34.6 of 51 | +9.64 ± 1.77 |
| without Earthen Mantle Approach | 90.7% | 39.9 of 51 | +14.93 ± 1.60 |
| without both Toughened Resolve | 88.2% | 34.4 of 43 | +9.44 ± 1.66 |
| without Toughened Body | 95.3% | 41.1 of 48 | +16.17 ± 1.55 |
| The sample, plus Lifeline (free) | 70.0% | 27.5 of 43 | +2.56 ± 1.13 |

Lifeline is worth about +9.4 on the big pool and +2.6 on the sample:
most of what it does here comes from having Health to spare. Watch list
material for the Hall of Fame.

### The day standard, and standard checks (2026-10-29, later)

Per the designer, days are measured at enemy Health ×1.0 (`day_sim.MULT`);
the other multipliers are worth a look now and then. `day_checks.py` runs
a set of plain swaps, each read three ways against the party as built on
the same fights. Level 3, ×1.0, 1,000 fights and days each; 400 runs of
up to ten days:

| Check | One fight: Health left | A day: morning Health | Days won | Ten days in a row: days |
|---|---|---|---|---|
| repeat (other fights) | - | +0.12 ± 1.21 | -0.4 pts | +0.33 ± 0.37 |
| nobody heals after fights | - | -8.10 ± 0.77 | -10.0 pts | -1.66 ± 0.26 |
| Carrick without Patch Up | +0.00 ± 0.00 | -0.76 ± 0.05 | +0.0 pts | -0.10 ± 0.18 |
| +1 Body, Beornhard | +0.14 ± 0.07 | +0.26 ± 0.20 | +0.0 pts | +0.07 ± 0.12 |
| +1 Body, Hilde | +0.25 ± 0.13 | +0.60 ± 0.39 | +0.9 pts | +0.24 ± 0.20 |
| +1 Body, Hanforth | +0.15 ± 0.08 | +0.62 ± 0.22 | +0.6 pts | +0.42 ± 0.17 |
| Toughened Body, Beornhard | +3.21 ± 0.16 | +3.45 ± 0.42 | +3.3 pts | +0.53 ± 0.18 |
| Lifeline, Hanforth | +1.06 ± 0.29 | +1.13 ± 0.72 | +4.0 pts | +0.11 ± 0.26 |
| Hanforth without Healing Magic | -1.97 ± 0.24 | -11.18 ± 0.88 | -16.4 pts | -2.04 ± 0.26 |
| +1 Body, Hanforth (Enith's party) | +0.09 ± 0.08 | +0.79 ± 0.34 | +1.3 pts | +0.01 ± 0.16 |

The rest is Hilde's party (Hilde, Carrick, Hanforth, Beornhard). As built,
it has 32.5 Health left after one fight, wins 87.1% of days, wakes up with
34.0 of 43 and lasts 3.05 days in a row. Enith's party: 30.4, 82.4%, 28.9
of 40, 2.67 days. "repeat" isn't paired (other fights), so it's the noise
between two runs; every other line is paired and much tighter.

- **Healing is worth far more by the day.** Taking Healing Magic off
  Hanforth costs about 2 Health after one fight, and 11 by the next morning,
  16 points of days won and two days of the three. Healing between fights
  alone (everything else the same) is worth 8 Health in the morning. The
  one-fight score has been underpricing healers.
- **Patch Up shows up now:** nothing in a fight, 0.76 Health a morning.
- **+1 Body is small either way.** It's worth a little more by the morning,
  from the extra Health a night, but it's under a Health in every reading.
- **Morning Health counts a bigger pool in full.** Toughened Body's +3
  Health reads +3.45 by the morning. Most of that is Beornhard simply having
  3 more to wake up with, used or not, as with Health left after a fight.
  Days in a row has no such lean, so it's the one to trust for a pool:
  +0.53 days for Toughened Body, against +2.04 days lost without Healing
  Magic.
- **Days in a row is the noisier reading** (±0.2-0.3 days on about 3), and
  it costs the most per run. At ×1.0 parties last two to three days, so a
  run is around seven fights
  (the days won, plus the one lost).

## Two kinds of measure (2026-10-30)

Per the designer: Health left, or Health in the morning, gives a bigger
pool credit just for being bigger. Is that the right yardstick for how
much a change helps? `measure_compare.py` reads the same changes to
Hilde's party (Level 3) two ways:

- **What it can take:** the enemy Health multiplier at which the party
  wins half its fights, and half its days, against the party as built.
  Nothing is counted but winning. Eight halvings on the same fights,
  with a curve fitted through every point tried (threshold.py).
- **What it spends:** how much Health it loses on a won fight (×1.75),
  and how much is still missing the next morning after a won day (×1.0).

600 fights and 400 days per reading. "Other fights" is the party as
built on a second set of fights: the noise between two runs. Every other
row is on the same fights as the first, so differences between rows are
steadier than that.

| Change | XP | Max Health | Fight: toughest x (vs as built) | Day: toughest x (vs as built) | Fight wins | Health lost on a win | Day wins | Missing next morning | Health left (old score) |
|---|---|---|---|---|---|---|---|---|---|
| as built | +0 | 43 | x2.26 (+0%) | x1.52 (+0%) | 76% | 14.5 | 88% | 4.0 | 21.7 |
| as built, other fights (noise) | +0 | 43 | x2.23 (-1%) | x1.47 (-4%) | 77% | 14.7 | 86% | 3.7 | 21.8 |
| 2 Toughened Resolve, Hilde | +22 | 51 | x2.47 (+10%) | x1.73 (+13%) | 89% | 16.5 | 92% | 4.5 | 30.7 |
| 2 Toughened Resolve, Beornhard | +22 | 51 | x2.49 (+10%) | x1.69 (+11%) | 86% | 16.1 | 92% | 4.7 | 29.9 |
| Toughened Body, Beornhard | +6 | 46 | x2.32 (+3%) | x1.56 (+2%) | 81% | 15.4 | 90% | 4.5 | 24.8 |
| +1 Body, Beornhard | +8 | 43 | x2.26 (+0%) | x1.53 (+0%) | 77% | 14.6 | 88% | 3.7 | 22.0 |
| +1 Essence, Hilde | +6 | 43 | x2.42 (+7%) | x1.65 (+8%) | 85% | 14.7 | 90% | 3.9 | 24.1 |
| +1 Acrobatics (her attack), Carrick | +5 | 43 | x2.32 (+3%) | x1.57 (+3%) | 79% | 14.2 | 89% | 3.9 | 22.8 |
| another Lunging Maneuver, Hilde | +3 | 43 | x2.27 (+1%) | x1.53 (+0%) | 76% | 14.4 | 88% | 4.0 | 21.8 |
| Lifeline, Hanforth | +6 | 43 | x2.41 (+7%) | x1.62 (+6%) | 83% | 14.6 | 92% | 4.6 | 23.6 |
| Hanforth without Healing Magic | -9 | 43 | x2.14 (-5%) | x1.20 (-21%) | 72% | 16.7 | 71% | 10.6 | 18.9 |

Per XP (the change's gain in each, divided by its XP):

| Change | XP | Fight: tougher per XP | Day: tougher per XP | Health left per XP (old score) |
|---|---|---|---|---|
| 2 Toughened Resolve, Hilde | 22 | 0.42% | 0.63% | 0.41 |
| 2 Toughened Resolve, Beornhard | 22 | 0.46% | 0.51% | 0.37 |
| Toughened Body, Beornhard | 6 | 0.44% | 0.44% | 0.52 |
| +1 Body, Beornhard | 8 | 0.00% | 0.08% | 0.04 |
| +1 Essence, Hilde | 6 | 1.18% | 1.43% | 0.40 |
| +1 Acrobatics, Carrick | 5 | 0.53% | 0.66% | 0.22 |
| another Lunging Maneuver, Hilde | 3 | 0.15% | 0.22% | 0.03 |
| Lifeline, Hanforth | 6 | 1.11% | 1.10% | 0.32 |
| Healing Magic, Hanforth (what losing it costs) | 9 | 0.59% | 2.34% | 0.31 |

(The 2 Toughened Resolve rows cost 22 XP: 18 for the copies, 4 for the
Resilience rank they need. Per-XP figures are worked from the
multipliers, not the rounded percentages.)

- **The old score flatters Health pools.** By Health left, Toughened Body
  is the best buy per XP here (0.52). By what the party can take, it's
  middling (0.44% per XP), level with Toughened Resolve.
- **Toughened Resolve helps, at an ordinary rate.** Two copies let the
  party take 10-13% tougher enemies, about 0.4-0.6% per XP. +1 Essence
  (Resist) and Lifeline do two to three times as much per XP.
- **A bigger pool spends more.** With Toughened Resolve the party loses
  more Health on a won fight (16.5 against 14.5) and wakes up a little
  shorter. Health spent and Health left both move with the pool, in
  opposite directions; neither says how much stronger the party got.
- **Healing is the best buy per XP by the day:** losing Healing Magic
  costs 21% of the toughest day the party can take, 2.3% per XP. In a
  single fight it's an ordinary 0.6%.
- **Noise:** the same party on other fights reads 1% (fight) and 4% (day)
  off. A change a few percent either way isn't telling us much on its own.
- Both optimizer runs searched on scores that count the pool (Health
  left; Health in the morning), which is part of why every build they
  found stacks Toughened Resolve. Their finalists are now ranked by the
  toughest day instead (hall_of_fame/).
