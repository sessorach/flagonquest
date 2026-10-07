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

### Calibration targets (to fill in with the designer)

- An enemy that's taken a hit gets another turn: **about half the time**.
- Typical fight length in rounds: ?
- How often the party loses an on-level fight, and how often someone
  goes Down or ends Wounded: ?
