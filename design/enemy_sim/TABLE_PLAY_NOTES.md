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
| 1 | Hilde | Barbarian | uploaded (export, 2026-09-20) |
| 2 | Browndog | Guardian | uploaded (export, 2026-09-20) |
| 3 | Carrick | Rogue | uploaded (export, 2026-09-20) |
| 4 | Jackal | Alchemist | uploaded (export, 2026-09-20) |
| 5 | Beornhard | Sorcerer | uploaded (export, 2026-09-21) |
| 6 | Sable | Archer | uploaded (export, 2026-09-21) |
| 7 | Hanforth | Healer | uploaded (export, 2026-09-21) |
| 8 | Felix | Monk, cat Wildfolk (he/him) | uploaded (export, 2026-10-08), partly modeled |
| 9 | Enith | Duelist, the Warlock stand-in, Settler (she/her) | uploaded (export, 2026-10-08), partly modeled |
| 10 | Ashleigh | Leader, a bard, cat Wildfolk (she/her) | uploaded (export, 2026-10-08), partly modeled |

Not part of the sample: Rook and Wren (reference builds made to test
movement), HOLE (a real ~90 XP build, set aside for now), the Baseline
Tier rows, and every current `(L2)` row (extrapolated from the Level 1
builds, mostly into combat, not built by the designer).

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
