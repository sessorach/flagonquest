# The Hall of Fame

The most broken builds the optimizer can find, one folder per version of
the game. Per the designer (2026-10-28): keep the top couple of builds
for each archetype every time we run it, so we can look back over time
at what delivered the most for its XP, and not make the same mistakes
twice.

## How a build gets here

`build_optimizer.py` takes one of the sample characters as an archetype
(its weapon, armor, background and play style stay as they are) and
searches everything XP buys: Stats, Skills, Techniques and their Levels,
a Buildable's Features. Every build it keeps is legal: exactly its XP
(125 at Level 2, 175 at Level 3, at most 2 unspent), no rank over the cap
(4 at Level 2, 5 at Level 3), every prereq met, Feature budgets held,
one Style. It's scored the way the sim scores everything: the party's
Health left (losses count 0) with the build in the sample's place, at
enemy Health x1.75 against that Level's four encounter mixes. The best
are then rescored on fresh fights, so the number in each entry is honest
rather than the lucky draw that got it picked.

**How the Hall ranks them** (2026-10-30, the designer's pick): by the
toughest day the party still wins half the time with the build in its
sample's place (`--rescore`, threshold.py), against the sample's own.
The search scores (Health left after a fight, Health in the morning)
give a bigger pool credit just for being bigger, so they only find the
candidates.

Each `.json` is a Builder export: open it in the Builder's Import to see
the whole sheet. The `simNotes` field says what it scored against the
sample. The names and concepts are flavor, in the spirit of the
trench-coat power gamer this whole folder is for.

## What it isn't

- Items aren't searched. A build here uses its sample's gear.
- The optimizer only knows what the sim models. A Technique that's
  deferred or out of combat can't show up, and a Technique whose play
  rule (mine) is too cautious or too eager can look worse or better than
  it would at the table.
- "Broken" means "the most Health left for the party per XP in the
  sim's fights". A build that's dull to play but efficient will rank
  above one that's fun.

## Versions

Each version's findings are in `v<version>/HALL.md`: the builds, what
makes them strong, and anything worth a standing design note. Newest
first:

- [v1.2](v1.2/HALL.md)
