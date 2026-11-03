# Designer Notes

This is the designer's own design thinking, pulled out of years of loose notes to themselves and boiled down by topic.
The originals stay in `archive/` (sources below). Nothing here was invented; where the notes changed their mind, both versions are kept with dates.
It's a record of how the designer thought, not the current rules. Current rules live in `scripts/rulebook.md`, and current design decisions in `design/RULES_DESIGN.md`.
Old terms are translated: "Bodily Defense" and "Resistance Defense" are Vital Defense, "Soak" is Resist, and the old Legerdemain Skill is Stealth.

**Sources, oldest first.** Each bullet ends with its tag.

- **(old site, *page*)**: `archive/flagonquest_site_other.md`, the old Google Site. It's the oldest material. The 2k19 manifesto opens by leaving that site behind, and its System Mk 1 page is dated 5/24/2018.
- **(manifesto 2k19)**: `archive/flagonquest_manifesto_2k19.md`.
- **(items 2k20)** and **(items 2k22)**: `archive/flagonquest_items_2k20.md` and `_2k22.md`. These are mostly the same text, and 2k22 is a light revision.
- **(manifesto v5)**: `archive/flagonquest_manifesto_v5.md`, for prototype v5. It isn't dated. It builds the suit system on top of 2k19's black/red change and uses Vital Defense, so it's later than 2k19.
- **(player's guide 2023)**: `archive/flagonquest_content_original.docx`, "Flagonquest Player's Guide v 2023.1". It's almost all rules text, so only a few lines come from it.

---

## Vision and feel

- You play a character you design. There are no classes or archetypes, so you mix and match any abilities. As the character grows, you can keep improving what they have, or let their adventures send them down a new path. (old site, Home)
- The game uses a full 54-card deck with both jokers. A streak of good or bad luck balances out as you near the end of your deck. (old site, Home)
- The cards are fate. Your deck is your fate and luck, and Good Luck, Bad Luck and drawing cards are you taking fate into your own hands. (old site, Manifesto)
- Not every character has to be good at everything. (old site, Home)
- What's the point of the game? The designer separates the actual play (the storytelling, playing a character) from "the game" (the mechanics that make up a character and how they show up in play). It's not a new idea, but it's worth stressing. (old site, Manifesto)
- The mechanics need a cohesive vision above them: what's important, and what the game's strength and focus should be. The answer the notes give is simplicity and straightforwardness. (old site, Manifesto)
- Fun is proactive. Make things active where possible, and let players choose which cool thing to do. (old site, Manifesto)
- Aim for 90% balance. At 100% nothing matters, and that's boring. Low balance is boring too, because half the options are bad. At 90% there's a choice, and some options are better or worse depending on context. (old site, Manifesto)
- PCs are exceptional. On the 0-5 Skill scale, most people who do something for a living have 1-2 points in it, or 3 in extreme cases. If a small army has a handful of people at 5 in a combat Skill, odds are most of them are PCs. (old site, Quarantine)

## Design principles

- The four principles for simplifying the rules (old site, New Ideas and System Mk 2):
  - **Variety**: there should be several options for any scenario.
  - **Distinct**: if two options exist, they should differ from the player's point of view. If they don't, combine them.
  - **Obvious**: options and their consequences should be clear. No "gotcha!" moments.
  - **Prune**: take as many rules as possible off the "necessary reading" list. A rule should only matter to you if you have the Technique that uses it, and otherwise touch as few rules as possible.
- Judge each group of options at first glance. Get a sense of what the group stands for, then cut anything that isn't needed. The example: one defensive ability uses Dodge and another uses Parry, but they do the same thing. At some point that's clutter, though they might feel different. Where to draw the line was left open. (old site, Manifesto)
- Think about it from the player's side. Most players won't get the difference between Crippled (worse attacks) and Weakened (less damage), so maybe remove Weakened. Weakened isn't in today's Common Effects. (old site, Manifesto)
- Snared can almost certainly go. Prone had been a running joke for a while, so maybe fold it into a general cover mechanic: partial cover gives Bad Luck to hit you, and full cover means you can't be attacked. (old site, Manifesto)
- Each group of options should feel a certain way. Not every "fighter" option has to be the same, but each one should fit a group with a clear identity. This also keeps the total number of options down. (old site, Manifesto)
- Some mechanics should never be granted because they're too much trouble, even though they sound good (old site, System Mk 2):
  - bonus Physical or natural Resist,
  - bonus damage,
  - a flat attack bonus, since Gambling already exists,
  - extra actions. Letting a Technique use a smaller action does almost the same thing and keeps edge cases out.
  
  Flat damage and flat Resist are the worst of these, because they tend to spiral out of control.
- Some "universal" mechanics should be common and part of the basic fabric of the game: Healing, temporary Health, drawing cards, Shifting, elemental Resist, elemental damage, Bleeding and Push. (old site, System Mk 2)
- These were noted as mistakes (old site, Quarantine):
  - Frenzy. Its bonus was supposed to be balanced by losing Dodge and Parry, and that didn't work out in play.
  - Any Resist bonus over +1-2 needs a close look.
  - Anything balanced around losing Dodge or Parry mustn't stack with other things that already wreck your defenses.
- About 90% of things are attacks against a Defense, and a few are flips by the target against a difficulty. If something gives a defender a bonus, it should either be a penalty on the attacker or apply to both the Defense and flips of that Defense's Skill. (old site, DM Notes)
- Avoid math-heavy scaling. Scaling poison by Resistance would need sturdier math, "and robust math is the last thing 99% of people want," so use flat values instead. (old site, Quarantine)
- Some Techniques were mostly fluff, like being able to eat poison. Split those parts out, find better homes for them, and make sure every Technique gives an actual benefit rather than a pile of goofy things. (old site, Quarantine)
- Order of work: first balance the abilities against each other and trim them to a good, shorter list. Rework items and everything else. Then do one last pass to tune it all. (old site, Manifesto)
- Tidy the rules near the end: clean up wording, simplify concepts, and fold small corner-case patches into how things work in general. (old site, Manifesto)
- Do the actual math rather than trusting a first impression. In one case, a "probably fine" guess about Mind and Body Unbroken was redone with numbers in the same note, and the conclusion changed. (manifesto 2k19)
- Drop mechanics that don't add much. The [Daily] tag wasn't clunky, but it was one more thing to keep track of for little return. (manifesto 2k19)

## Cards, luck and suits

- A flip is made against a difficulty. Meeting it is a success, and you get an Extra Success for every 2 points you beat it by. It was still open whether effects should scale off all successes or only Extra Successes. (manifesto 2k19)
- From 2k19, you no longer play cards over other people's flips. Instead you discard a card to adjust a flip from -3 to +3 based on the card's value, or to tune a flip to that card's suit. It's a bit complicated, but players got used to it quickly: "if this is the one concession I have to make it's probably fine." (manifesto 2k19)
- 2k19 cut most suit effects down to black or red. A damaging attack gets +1 damage on a black card or +2 on a red one, and secondary effects trigger on black. In week 4 of testing the damage bonus barely mattered. With less variance there were no huge swingy attacks and no tiny ones that didn't matter, and black/red gave enough to build on without much mental math. (manifesto 2k19)
- Suits should matter, be interesting and make flips more dynamic. As a side effect, players get to decide whether to lean into luck or try to control it. This needs some rework, but it should be as simple as possible and fit in seamlessly. (manifesto v5)
- **Suit pool.** Count the suits of every card used for an action: the flipped card, any Good Luck cards and any cards Played to support it. Cards discarded to activate an ability might count, but that shouldn't be the norm. Effects can then use suits like a stat, for example "2 + [Body + Hearts] damage." (manifesto v5)
- Against enemies, cards the party plays take those suits out of the enemy's pool. (manifesto v5)
- **Red and black, again (v5).** Red is +1 damage and black is an Extra Success. Earlier in the same doc, Hearts and Clubs were going to add damage while Spades and Diamonds added to results. The red/black split is where it lands. Red suits push for power: Hearts overwhelm, and Diamonds bend power to win through. Black suits control: Clubs through reliability and stability, and Spades through outright mastery. (manifesto v5)
- Abilities should scale with the suits used. For example, a Battle Strike feature that Cripples applies X + [Clubs] stacks, and a stealthy ability like Vanish adds Diamonds. Weigh abilities as if one card is flipped, so an effect tied to one suit counts as 1/4. (manifesto v5)
- The suits should be about equal on average but distinct, and each should pull certain characters. A barbarian type leans toward Hearts and Clubs, and an assassin leans toward Hearts and Spades. There's some overlap, but the preferences are clear. (manifesto v5)
- **Suit symbolism.** Each suit stands for a set of fundamental things, the way seasons, elements and stages of life do in old mysticism. The notes also gave each suit Skills and buffs/debuffs, and that mapping has moved since (see `SUIT_SKILLS` in `index.html`). (manifesto v5)
  - Hearts: Cups, Spring, Brilliant. Power, love, emotion, intuition, relationships.
  - Clubs: Wands, Summer, Fire. Stability, energy, motivation, purpose, spirituality.
  - Diamonds: Coins, Autumn, Shadow. Flexibility, cleverness, money, work, careers.
  - Spades: Swords, Winter, Frost. Mastery, control, destiny, thoughts, communication, decisions.
- **Suit-pair effect sets.** Idea, not yet in the game. (manifesto v5)
  - "Leveling Tide" (Hearts/Diamonds) mixes control and offense to level the fight.
  - "Crushing Pinnacle" (Clubs/Spades) doubles down on strengths.
  - "Falling Leaf" (Diamonds/Clubs) is a fleeting strategy that skirts danger.
  - "Waking Beast" (Hearts/Spades) is powerful when it matters.
  - "Turning Seasons" is all four suits on offense ("sealing fate").
  - "Breaking Wheel" is all four on defense, for shifting the battle, clearing negative effects and taking back control ("defying fate").
- Abilities that make you discard cards can care about the discarded suits. "Discard for twice Good Luck on a weapon attack" might become Good Luck once plus any discarded Hearts added to the pool. This also fixes Techniques that are only good if you pour every card into them. (manifesto v5)
- Abilities that cycle cards should let you either discard or shuffle back into the deck, for fun. (manifesto v5)
- Once Good Luck adds a suit to the pool, each Good Luck is worth more and the bonus stacks. A long chain of red cards can end someone, which makes combat more dynamic, but Good Luck has to get rarer. (manifesto v5)
- Measured averages: twice Bad Luck 3.77, Bad Luck 4.85, normal flip 7.00, Good Luck 9.15, twice Good Luck 10.23. The same note asks whether Good and Bad Luck should be the main form of most buffs and debuffs that matter. (old site, System Mk 2)

## Resources: Focus, cards and daily limits

- **Old value standards (Focus era):** 1 Focus = 1+ card = Good Luck three times = 5 card cycles = 3-5 Health (4 on average) = 6 Gold = ~2.5 damage = 2 AP (a big maybe). 1 AP = ~1.25 damage. A later line on the same page says Focus converts to Gold one-to-one, which doesn't match the 6 Gold figure. (old site, Manifesto)
- Perfect Strike was the benchmark: Good Luck twice on an attack for 1 Focus, at Level 2, with no limit and no action. From that, 1 Focus is about +3.23. Drawing a card is worth about the same if you can use it on your own flip or on someone else's, and about 1.6 if you only use it for yourself. Three to five card cycles are worth 1 Focus. Removing 10 cards from the deck is about one blind card draw. (old site, Manifesto)
- v5 reprices on a different scale: 1 damage is worth 2, +1 to a result is worth 1, and a card in hand is about 1.5. A card added to the suit pool is worth +1, because it's a 50% chance of about +2. Good Luck used to be +2 and is +3 once it adds a suit. (manifesto v5)
- Focus was the daily power pool. Since Focus abilities already have that limit, they should be fairly unlimited otherwise, and very few things should cost Focus and also be Encounter abilities. Healing is the exception, since it's almost all gated by Focus (or Gold). (old site, Manifesto)
- Once you have one Focus ability, more don't help much. So those abilities might want higher requirements and a lower Level. (old site, Manifesto)
- Proactive spending should beat reactive spending like healing. (old site, Manifesto)
- **Daily tag, changed over time.** The old site said "put a [Daily] tag on some Techniques. Makes things so easy. DO IT." In 2k19 the [Daily] tag goes away, and daily resources become cards discarded. 2k19 is the later view. (old site, System Mk 2; manifesto 2k19)
- **Focus removed (2k19).** Rebalance costs around discarding cards from your hand, with cards per day as something like Instinct + Mind. The designer called it "literally the best idea." In week 4 of testing players had a big handful of cards, and it leaves room for lots of card-burning abilities. Card-drawing abilities built on Focus became obsolete. (manifesto 2k19)
- Anything that generates a card can't be spammable. It has to depend on something limited, like a resource, a kill or once a day. The rough exchange rate is 3 Health = 1 card. (old site, Quarantine)
- Turning Health into cards will get abused. Grim Resolve at "3 Health: draw a card" had to go, "same as how there was never a way to get Focus through Health." The fix was 1 Health committed until a full night's rest. (manifesto 2k19)
- Committing a resource means you can't get it back by any means while it's committed. (manifesto 2k19)
- Keeping cards through a night's rest is oddly strong, since it amounts to a free card after downtime. A flat "extra cards per day" gets weird when it isn't tied to a Stat. (manifesto 2k19)
- An ability that burns a card has to be worth more than just Playing that card. The notes ask this of Evasive Drift ("how is this worth using over just playing the cards?"). Drifting Form was the answer: a 0 AP reaction that does something a Played card or healing can't. (manifesto 2k19)

## Character building, XP and prerequisites

- **Flagged as important:** a Skill rating X costs X(X+1)/2 XP, and a Stat rating X costs X² + X. (manifesto v5)
- The old XP milestones (old site, Character Evolution):
  - 60 XP is "the core," just Stats (1/1/2/2/3) and Skills (eleven at 1, six at 2, three at 3).
  - 100 XP is the starting character.
  - 140 XP is when a character defines their most important facets.
  - After that come 180 "The Thickening," 220 "The Quickening," 260 "Very Rounded" and 300 "Things Are A Little Silly."
- A sample 300 XP character spent 89 on Skills, 112 on Stats and 99 on Techniques. The average Technique is a 2 or maybe a 3, and about half of characters will get a Level 5. (old site, Manifesto)
- System Mk 1 was replaced in 2018. The main reason was Stat imbalance: characters kept one or two Stats at 0 with no Skills under them in use. Weapons were also redesigned so some use something other than Strength, and Technique XP costs might change. "This was about the best it could be... without the Stat overhaul." (old site, System Mk 1)
- **Prerequisites, as their thinking changed:**
  - Old site: prereqs are equal parts barrier and justification. The barrier stops free access, makes choices count and makes characters invest for special or powerful mechanics. The justification makes a character embody what the Technique suggests, mostly through secondary prereqs. Healing Magic is plain Theurgy and needs nothing else, while nature spells also need Survival. (old site, Manifesto)
  - 2k19: a Technique should tie up about its own XP cost in prereqs, so if you want a cool thing you have to be built the way it "should" be. Lowballing a little is fine, and overshooting isn't. The point is mostly to make cheap Techniques easier to get early. An extra lower-tier prereq is fine for something outside a Skill's usual scope, like nature spells for Theurgy or extra features. (manifesto 2k19)
  - v5, latest: prereqs shouldn't raise a Technique's cost. They should require the Skills that justify having the effect. It's more about flavor. Swinging a big weapon needs Might, swinging it to cause Bleeding is still Might's turf, and throwing it well might need Acrobatics. Tricky martial abilities that read an opponent might need Insight. (manifesto v5)
- "Beginner keystone" Techniques like Lay On Hands and Bottomless Bottles are Level 4 with prereqs around 3/3/3, so they can be bought at the start. They need Level 4 power without Level 4's unique mechanics, so they're reliable, straightforward and good outlets for spending resources. (old site, Manifesto)
- Prereq ranges by Level: Level 1 is 2 max and 3 total, Level 2 is 3 max and 5 total, Level 3 is 4 max and 7 total, Level 4 is 5 max and 9 total, and Level 5 is close to 5-5-5. (old site, Quarantine)
- Prereqs needed unifying, especially odd add-on requirements like Academics, along with a clearer idea of what prereqs represent across all ability types. (old site, Manifesto)

## Techniques: Levels, groups and structure

- **What each Level means** (old site, Manifesto and Quarantine):
  - **Level 1**: simple, niche utility, small conveniences and flavor. About 3 XP, or around 6 Gold. Something minor that comes up a lot, or something useful every few sessions.
  - **Level 2**: the cornerstone of a character, solid but simple. An attack that also does something useful, but not on par with two attacks.
  - **Level 3**: strong, and a clear step up. This is where Techniques start costing more than a session's XP, and a few of them make a big impact.
  - **Level 4**: the capstone of a concept. Mixed characters might never take one. It covers the best combat spells, big hitters, and abilities that let your favorite Skill solve half a dozen problems.
  - **Level 5**: "basically breaking the rules." The power is unmatched, the requirements are heavy and the effect is focused. It means putting enough XP to max a Skill from 0 into one thing, and a character only takes one because it fits their concept closely.
- If you sink XP into one Technique up to Level 4, it's fair for it to have more potential than a couple of lower-Level Techniques together. (manifesto v5)
- AP spread: about 75% of Techniques at 2 AP, 75% of the rest at 1 AP, and one or two per category at 3 AP or 0 AP. The notes also wanted more options around 3 AP. (old site, Manifesto)
- The old action types: a Main action does neat stuff that shouldn't be copied outside unique cases. A Move is basic. An Extra covers minor non-attack things. A Counter is conditional, and the better its effect, the narrower its trigger. (old site, Quarantine)
- Tag order on a Technique: type (Martial, Spell...), then extra tags (Subtle, Re-Learning...), then frequency (Encounter, Daily). (old site, System Mk 2)
- **Power types: Magical, Skillful and Strong.** The split has no mechanical effect. It's a way to spread Techniques so it's clear what kind of character gets what. (old site, New Ideas and System Mk 2)
  - **Spells** are easy to write, since magic doesn't have to make sense, so they need clear limits. Their traits: they're a *resource* (almost every spell that matters is Encounter or limited, so a caster builds an armory), they're *impressive* (big and flashy), and they *"cheat"* (elemental damage past armor, big blessing numbers, healing that undoes brutal hits).
  - **Skillful** means being so good at something it defies sense. Its traits: *flexible*, *applicable* (Skills get easier or more reliable to use, not better in the abstract) and *inefficient* (many uses cost money or goods, and better Techniques cost more).
  - **Strong** means physical traits turned up to 11. Its traits: *better* (but only on niche things like carrying capacity and Reflex, so it doesn't break), *passive* (felt as built-in improvements) and *obvious* (in why you'd take it and when it's used).
  - Broad needs, like curing poison, should have an option in every type: a healing spell, a good doctor, or being strong enough to flex the poison out. When something exists for two types but not the third, that should be a choice to keep it from that type.
- **The "feel" of each conceptual bucket** (old site, Manifesto):
  - **Strong** feels reliable and solid, the backbone of a character.
  - Under it, **Tactical** (Acrobatics, Archery, Melee, Brawl) feels like outmaneuvering, with a tactical choice at each step and a default of being well-rounded. **Martial Arts** (Brawl, Meditation) means buying into one strategy you own. **Overpowering** is just being very strong.
  - **Savvy** is flexible and ingenious, with creative ways to solve problems.
  - Under it, **Expert** is good with things, not people, and the more broadly useful an Expert ability is, the more setup it needs. **Willful** forces the world to obey, sometimes at a sacrifice. **Personality** feels strong whenever there are people to work with.
  - **Spellcasting** feels specific and deliberate. You decide exactly what you want when you learn a Spell, and it's very good when it applies.
- The groupings shifted over the years:
  - The 2k19 site plan had Martial, Spells, Strong, Skillful and Personality. (manifesto 2k19)
  - v5 had Martial, Stance, Discipline, Elementalism, Theurgy, General Spell, Power, Expertise and Personality. Power covers body, mind and spirit, and above all lets physical Skills gain extra Health. (manifesto v5)
  - The 2023 guide had Power, Expertise, Personality, Martial, Disciplines, Spells, Sorcery and Stances. (player's guide 2023)
- v5 was a minimal prototype. It tested the new suit mechanics as a core piece, exploration as a well-integrated pillar, and summoning. It focused on rules over content, with only the bare-bones list of Techniques needed to support different styles. (manifesto v5)

## Combat

- **The old fight model** (old site, Manifesto):
  - The party loses about 12.5 Health per fight. That assumes as many enemies as PCs, a ~50% hit chance and ~2.5 Health per hit.
  - A party handles about three fights a day, and a full night's rest heals or mitigates that.
  - Each character has about 2.5 Focus, and 1 Focus gives about 3 Health back or prevents the same.
  - 1 Focus should add about 2-3 damage or remove two enemy combat rounds.
  - The party removes about one enemy a round, and a fight lasts about 4 rounds.
- The old Health budget was 12 base Health plus 3-4 per Health Technique, and about 4 Health of healing per Willpower spent. That comes to roughly 18 Health per character per day. (old site, DM Notes)
- 3 damage is the break-even point between Martial and Spells, so spell damage bonuses should be +2 at most. (old site, DM Notes)
- An attack against several enemies is a separate attack against each one, not one shared result. (manifesto 2k19)
- **Weapons.** Damage is the most important factor, and players will reach for the highest-damage option. That means lower-damage weapons need clear tradeoffs and uses. Weapons sit on a range from one-hander and shield up to the two-handed power melee weapon. (old site, System Mk 2)
  - Finesse weapons have less damage but more accuracy or defense, and run on precision.
  - Power weapons are raw damage.
  - Two-handed melee weapons get more damage, and two-handed ranged weapons get more accuracy, so ranged weapons play a precision role.
  - Unarmed trades down further but is versatile.
- Everything is balanced on an average attack of about 2.5 damage: 2 over armor plus a card flip. Weapons then need about 3/4/5 damage. There are four tiers (manifesto v5):
  - holdout weapons (Unarmed, finesse thrown), which still deal 1-2 on a hit,
  - Finesse,
  - Power, the standard damage set,
  - the two-handed power weapon, the king of damage that gives up everything else.
- Armor at Resist 1, 2 and 3 is "perfect as-is," with clear tradeoffs. Maybe heavy armor's Speed penalty should just be -1, and the Dodge penalty is cool. (manifesto v5)
- **Resist.** The game assumes 1-3 Physical Resist, and 0 is an outlier. Elemental Resist assumes 0-2. A 3 would nearly make you immune, which is fine if it comes from stacking everything you've got. Spells rarely pass 8 base damage, so a stacked Resist means taking about 1. (manifesto 2k19)
- A worry: natural Resist from a Stat makes that Stat disproportionately important. (old site, System Mk 2)
- Turn order should matter more, and not just for lining up Harried attacks. One idea was that everyone starts combat Harried, so Reflex flips matter. Being able to strike first is good already, so this was left alone. (old site, Manifesto)
- A turn-order shuffle is worth about one Technique Level, based on Seize the Initiative. Moving several allies is worth more and needs limits. (old site, Manifesto)
- Difficult Terrain is a neat mechanic and should show up more. Nothing should ignore it except Shifting, and Shifting and teleporting are the counter to it. (old site, Manifesto)
- Shifting is tactical movement and belongs in many "tactical" abilities. (old site, Quarantine)
- **Defenses and what they cover.** Dodge and Parry are grouped. Dodge works against most spells, while Parry is easier to get and goes higher but only stops some attacks. Vital Defense covers Bleeding, poison, disease and weakening. Mental covers taunts, fear and lockouts. (old site, Quarantine)
- **Stances (now Styles)** (old site, System Mk 2):
  - Half-Guard was the designer's favorite: +1 Parry for half Speed. The bonus is small but useful, rarely available elsewhere, and comes at an awkward cost.
  - A Stance should either be good enough that a character gives up something besides XP for it, or be niche and unabusable enough to need no drawback.
  - Any drawback should be a sensible counterweight, and only strong enough to keep the Stance to characters it fits.
  - If a Stance supports your style, you shouldn't be pulled to another Stance just because it's better in the abstract. If an archer skips the ranged Stances for a general one, either that one's too good or the ranged ones aren't good enough.
  - Compare every Stance against Half-Guard within its niche.
- Stance roles: movement, protection (defending allies, weakening enemy attacks), leader (setting up allies' attacks), aggressive (offense at the cost of defense) and resilient (defense at the cost of offense or another defense). Stances might also be tied to weapon loadouts, maybe more than one per loadout. (old site, DM Notes and Quarantine)
- The fighting styles were dueling, dual-wielding, sword and board, two-hander and ranged. v5 added unarmed, with one Stance for each of the six plus two for spellcasting. (old site, Quarantine; manifesto v5)

## Buffs, debuffs and healing

- Debuffs come off one stack per turn, so one more stack is useful when the enemy already has a few. (old site, System Mk 2)
- Write every debuff as "for each stack, you have ___." Ward is "while you have any stacks, +1 Resist to that type," and Taunted and Frightened are "while you have any stacks, Bad Luck..." (manifesto 2k19)
- **Who gets which debuffs:**
  - Martial Techniques make enemies easier to kill, and Spells make them easier to control. (old site, DM Notes)
  - Elementalism's debuffs make enemies easier to kill, and Theurgy's make enemies worse at killing you. (old site, New Ideas)
  - Later version: Martial is straightforward, physical and tactical. Centering (Meditation) is its mysterious supernatural counterpart, with strange combos and penalties whose impact isn't felt right away. Elementalism is destructive and strips defenses. Theurgy stops enemies attacking well and removes debuffs. Creative (alchemy and crafting) covers a wide range at a cost. Rogue sets up a disadvantage, or takes advantage of one, through preparation. (old site, System Mk 2)
- Debuffing is proactive and removing debuffs is reactive, so Blessing-style removal can strip about as much as Battle Magic applies. (old site, System Mk 2)
- **Temporary Health becomes stacks.** The breakthrough was to make temporary Health work like a debuff: you gain stacks that last a short time, and the "debuff" tag gets a more generic name. That's how Protected came about. (old site, Manifesto)
- **Healing targets** (old site, Manifesto and Quarantine; manifesto 2k19):
  - Old site: 1 Focus is about one card, and proactively that's about 3 Health. So 1 Focus of healing is about 3 Health, up to 5 at most. Fewer limitations mean less healing.
  - Old site, another page: 3-7 Health per resource spent. 3 comes with convenience or low requirements, and 7 is for something specific or clunky, like melee range or healing over time.
  - 2k19, after Focus became cards: healing is about 1 Health per card with a small upside, or 3 per 2 cards with an inconvenience.
- A buff averages [Level] added onto a normal action, plus [AP] if the action has no attack. (old site, Manifesto)
- Health was clunky. The designer wanted to keep wound penalties and to buy Health of different "values." The 2023 guide has Shallow Health. (manifesto 2k19; player's guide 2023)

## Magic and summoning

- Spells shouldn't stand in for other Skills so well that a caster never needs those Skills, the same way Dexterity shouldn't replace Strength. Attack spells are fine, since casting Skills are fighting Skills at heart. Utility spells should do what's otherwise impossible, like hidden storage, rather than what a Skill already does. (old site, DM Notes)
- Elementalism and Theurgy shouldn't be skeleton keys. Reusable attacks are kept away from magic for that reason, apart from Placeholder's torch, which is a joke. (old site, New Ideas)
- **Elementalism** is flashy, full-offense magic. Even its exceptions (teleports, defenses) are personal and combat-focused, and its casters feel like they're unleashing power. **Theurgy** is subtle support magic. It has the most flexible healing, blessings and odd utility, and its casters feel like the backbone of the party. **General** magic is the miscellaneous rest. (old site, Manifesto)
- Sorcery is "the prime magic, first and foremost among the magical arts as the refined practice of magecraft developed among civilization." (player's guide 2023)
- The old elements each had a job. Fire is damage with no side effects. Frost reduces movement and dice pools, and stuns at high levels. Lightning takes away moves, knocks back and knocks prone. Shadow reduces strength pools and locks out the daily resource. Spirit adds holy damage and lowers natural Resist. By v5 the four elements were Brilliant, Fire, Shadow and Frost. (old site, DM Notes; manifesto v5)
- **Battle Magic against Battle Strike** (manifesto v5):
  - Battle Strike is easy to balance: three copies of a debuff ability lands right at Level 2.
  - Battle Magic is measured against a one-handed power weapon. Stat + 2 elemental damage that gets past armor is half a point better, assuming average enemy armor of 1.5, which pays for not having a basic attack.
  - The trouble: Archery is a Skill tax that buys a good ranged basic attack, while Elementalism is a Skill tax with no basic attack. So Level 1 Battle Magic was set at 3 + Stat Fire damage at range, with two features instead of one.
- **Wands.** A Level 2 wand matches a Level 1 Technique, Level 3 matches Level 2, Level 4 matches Level 4, and Level 5 is "something very good." At those numbers a wand could just say "while you wield this, you can use the Technique." (old site, Quarantine)
- **Summoning goals (v5).** Is it impactful without breaking the action economy? Does it have its own use that players enjoy? Does it feel like a summoner should? (manifesto v5)
- **Summoning, old model.** A summon gives you another creature to spend your AP on, so you don't gain actions, which is good. Its stats replace yours for those actions. (old site, Manifesto)
- **Summoning, v5 model (later):**
  - Summons don't get AP. Once per round you can spend 2 AP to give one 4 AP, which lets it take Interrupts, and it can only attack once per turn.
  - The limit on attacks smooths out extreme cases. It also answers why anyone would spend XP on a weak summon instead of attacking themselves.
  - Value a summon over about 3 turns of a fight: 1 AP of free movement plus 3 × how far it beats an average PC at that Level.
  - A baseline summon is worth about 3 points, the same as a Level 1 Technique. Each Health is worth 2, Physical Resist 4, Fire Resist 2, other elemental Resist 1, and each immunity to a Defense 1.
  - (manifesto v5)

## Martial arts

- Why fight unarmed when a sword is a sharper fist? Because you can grapple, and because if the best praise for a swordsman is that the blade is "like an extension of their body," there may be something to using a literal extension of your body. (old site, Manifesto)
- **The schools** (old site, Manifesto and System Mk 2):
  - **Snake Style** is tricky and reactive, all grabs and trips that outmaneuver anyone.
  - **Bear Style** runs on Might and cancels out the advantages of weapons and armor: it can't be parried and does something about armor. It's a great leveler.
  - **Demon Style** is brutal, reckless and sacrificial.
  - **Great Old Oak Style** is a defensive juggernaut that doesn't lose offense.
  - **Ki Style** blends the martial and the supernatural.
  - **Shugen Style** is purely supernatural use of Meditation.
- Martial Arts Techniques mean buying into one strategy, while Tactical ones are reactive and analytical. Meditation works as a sort of third caster Skill. (old site, Manifesto)

## Exploration and skill challenges

- Exploration should be a well-integrated pillar of the game. It should support crafting in particular, and make clear how certain Skills get used. (manifesto v5)
- In exploration, each character declares an action each round: either do something or support someone else. (manifesto v5)
- Movement should be easy to run, in a single step with no secondary rolls. The designer looked at how 5E does it, then settled on this: climbing or swimming costs an extra meter per space, and you can jump up to your Athletics Skill Total in meters, or half that vertically. The GM can call for an Athletics check, and failing it Counters the rest of the action. A jump that takes several actions only needs a check on the first one. (manifesto 2k19)
- Movement was checked against world records: an expert's average result (17) should land near them. That gives 7 meters for climbing or swimming, 3 for a vertical jump and 9 for a horizontal jump, or 5 without a running start. (old site, Quarantine)
- **Foraging math** (manifesto v5):
  - A party travels overland about 8 hours every 3 days and forages for about half of that.
  - Half the party forages while the rest orient or keep watch, for about 8 checks: 4 by the Survival expert at a 1/2 success rate and 4 by someone else at 1/3.
  - That's a little over 3 successful forages, enough to feed the party on the road.
  - A foraging-expert Technique lets the party keep full pace and forage the whole way, for about 6-9 value per trip. It was bumped to Level 3 because it's free stockpiled money, and abilities that generate Gold are very rare.
- Survival and Streetwise are wilderness and city mirrors of each other. Each gets bonuses on orienting, assisting, lookout and scavenging. Streetwise also gets rumor-spreading mischief and Preparation, which lets you "dramatic edit." (manifesto v5)
- In combat there are several ways to beat a difficulty. A skill challenge needs more specific methods, and often you only get one try. (manifesto v5)
- **Named check types.** Idea, not yet in the game under these names. The note on Team Checks breaks off mid-sentence. (manifesto v5)
  - A Goal Check is everyone flipping with one success needed, like searching a room for a hidden lever.
  - A Team Check is everyone flipping with everyone needing to succeed.
  - An Individual Check is everyone flipping and succeeding on their own.
  - Draft numbers: difficulty 12-16 across Levels 1-5, Goal Checks 2 higher, against a baseline bonus of +4 to +8.
- Destroying objects should be simple: objects have Resist and Health, and you attack them. Another option is a Might check that deals damage from the result. (old site, Quarantine)

## Social contests

- Social Technique Levels (old site, Manifesto):
  - **Level 1** works from a disadvantage: shoring up weaknesses, "just in case" tools, and replacements so non-social characters can take part.
  - **Level 2** creates an advantage by limiting opponents' moves and making them play your game.
  - **Level 3** uses that advantage to shape the story, with lots of "if you win the contest" effects.
- A later pass asked whether social Techniques were worth taking at all, at about 3 XP against just buying a Skill point. Its Levels: Level 1 is decent and mostly replacements, Level 2 is solid tactics that can swing low-stakes contests, Level 3 is thematic and carries outside the contest, and Level 5 is "overkill in all but the most impossible of social combats." (old site, System Mk 2)
- Names under consideration for the parts of a social contest (manifesto v5):
  - A social "attack" (Statement, Utterance, Declaration, Proclamation).
  - Three kinds of attack, mapped to ethos, pathos and logos. **Forceful** (Presence or Rapport) impresses with bearing and personality. **Maneuvering** (Rapport or Persuasion) reframes things or primes someone to agree. **Debate** (Persuasion only) trips someone up with logic and technicalities.
  - Social "damage" that builds until a side concedes (Demerit, Slight, Snub, Affront).
  - Two Defenses: **Intent** against emotional manipulation and **Logic** against logical attacks.
  - Version 1.1 later rebuilt the social Techniques around Statements and Pressure (see `scripts/versions.csv`).

## Crafting, items and Gold

- **Crafting needs four things** (items 2k20, 2k22):
  - **Skill**: a Skill Total plus training in that School.
  - **Materials**: plus tools, and some Schools need more equipment, like a forge for Smithing.
  - **Recipe**: basic recipes come with the tools, and recipes mostly gate Masterworks.
  - **Time**: 8 hours for a basic item and another 8 for Masterwork, so a full Masterwork is a day's work. The time keeps crafting a downtime activity so the game flows. A Technique might lift that limit for some items.
- The Schools were Smithing, Carving, Leatherworking, Tailoring, Jewelrymaking and Alchemy. (manifesto 2k19)
- Every material type at every Level should have one or two recipes. A Level 3 Fire material should have at least two uses, even if it's just a grenade and a ring. (old site, Manifesto)
- You don't need a version of every potion at every Level. Two healing potions and a grenade or two per Level is fine, and there shouldn't be a perfect assortment of things to make from a given material at a given Level. (old site, Manifesto)
- **What Gold is worth.** The items notes value Gold at about 1.5 value per Gold as a one-time effect. Under "The Gold Standard," the same docs also say 1 Gold is +1 value as a one-time effect, against Techniques that get used about twice a day. Both figures appear side by side and aren't reconciled. v5's foraging math uses 1.5. (items 2k20, 2k22; manifesto 2k19; manifesto v5)
- Masterwork items cost a lot but pay out over and over, while potions are good but the Gold is gone. A good approach probably uses both. (items 2k20, 2k22)
- **Consumable pricing.** A consumable costs 2 Gold per Level and equals a fixed Technique of that Level, so Bottled Fire (a Level 2 grenade) is about a Level 2 Battle Magic spell. Grenades are just bottled battle magic. 2k19 floated 3 Gold per Level, and the later items notes and the 2023 guide use 2. (items 2k20, 2k22; manifesto 2k19; player's guide 2023)
- **Poison pricing.** One stack of a standard debuff like Crippled is worth about 2.5 points: -1 for about 2.5 enemy turns. So a poison is worth a Technique of its Level. (manifesto 2k19; items 2k20, 2k22)
- Round up anything priced in Gold, to reflect how flexible and convenient Gold is compared with committing XP. (items 2k20, 2k22)
- **Permanent purchases.** The designer started from a 12-session campaign of 3-4 hour sessions with 2 fights and 1 non-combat scene each, then decided it doesn't matter (items 2k20, 2k22):
  - Gold and XP both get invested, and earlier buys always give more value over a game.
  - So linear item scaling makes sense. Saving up only "wastes" Gold you couldn't have spent earlier anyway.
  - Being able to sink more Gold into one slot for a bigger benefit has value of its own, since upgrading a cheap item later loses Gold.
- **What each slot is for** (items 2k20, 2k22):
  - Head: mental, vision.
  - Hands: things you do with your hands, like lockpicking or surgery. In 2k22 this is narrowed to Skill-based non-attack actions.
  - Feet: mobility.
  - Belt: carrying items. Added in 2k22.
  - Torso: direct protection, vitality, healing.
  - Held: weapons and anything that takes an action to use.
  - Neck: niche, passive, handy but boring buffs with no interaction.
  - Rings: one specific active ability or a boost to a particular Skill or ability.
- Item bonuses can be passive and good, but should be niche. Apply a debuff instead of +1 damage, and grant Protected when hit instead of +1 Resist. Narrow bonuses mean different characters use the same item in different ways. Items are easy to swap, unlike Techniques, so weird niche items will still get picked up. (old site, Manifesto)
- **Masterwork price tiers, as they changed:**
  - Old site: Common/Uncommon/Rare/Extraordinary at 6/12/24/48 Gold. **Common** is mostly convenience, like a weapon that changes type or a thrown weapon that returns, and might mimic a Level 1 ability. **Uncommon** is a passive combat benefit, like built-in Pushes or reflipping low cards on some Skills, and mimics Level 2. **Rare** is a substantial boost, like temporary Health every fight or more spell range, and would be Level 4 if it mimicked anything. **Extraordinary** is "the dumpster for everything that's disgustingly good." (old site, DM Notes and Manifesto)
  - Old site, later proposal: item Levels 2-5 at 6/12/24/36. That came from aiming each item at about a consumable a fight over about 12 uses, with one healing potion a session and one 1-Gold consumable per tricky fight as the baseline. (old site, System Mk 2)
  - Later, Masterwork costs [20 × Level] Gold. (items 2k22; player's guide 2023)
- 1 Gold is about a $20 bill, and basic items run from 1 Gold up to about 10. Money is abstracted into chunks, so a bar drink is glossed over unless you buy a round for the whole bar. (old site, Manifesto and Quarantine)
- The old equipment budget: weapons for two hands plus backups, medium armor, a pack and kits, one healing potion a session, one moderate poison per hard fight, and about seven magic items (one Extraordinary, one Rare, two Uncommon, three Common). Salvage sells for 1/4 of market price, maybe 1/2. (old site, DM Notes)
- Poison was weak and maybe needed a buff. Give each poison a fixed Potency and let better recipes add +1, rather than scaling off the target's Resistance. Poisons will hurt, so offer counters through several power types. (old site, System Mk 2 and Quarantine)
- Any limit on how often an item works applies to the item, not to each person using it. (player's guide 2023)

## Enemies and encounters

- **Enemy roles** (manifesto 2k19):
  - **Support** shields, heals and buffs.
  - **Damage** attacks, with a cool buff on it.
  - **Control** attacks or makes obstacles, but mostly debuffs, maybe with Bleeding and poison.
  - The roles overlap, but each enemy has a focus.
- An enemy gets baseline actions and as few passives as possible. Keep the stat block short, with 1 or maybe 2 actions a turn. Each action is Martial, Discipline or Spell, and all of a creature's actions are at its Level. (manifesto 2k19)
- Every enemy gets an attack style and a strategy. An attack style is a net-zero limit, such as attacking only once a round in exchange for bonus movement or Good Luck. A strategy is how it fights, like going after the weakest PC it can see or keeping its distance. (manifesto v5)
- About half of enemies should have an alternate attack against Mental or Vital Defense. Across all enemies, that's about 50% of attacks against Dodge or Parry, 25% against Mental and 25% against Vital. (manifesto v5)

## Backgrounds and ancestries

- If a background has three parts, each should be worth 2 XP or about 8 Gold of specific goods. (manifesto 2k19)
- 2k19 planned to fold the non-beastfolk races into one catch-all group, maybe renamed so it doesn't draw complaints, alongside a beastfolk group. Each group got small traits, like extra reading skill or a magic trick on one side, and prehensile tails or night vision on the other. By the 2023 guide these had become backgrounds: you get two, from the General list plus either Settler or Wildfolk. (manifesto 2k19; player's guide 2023)

## At the table: roleplaying, presentation and style

- You play *as* your character, and every decision should come from them, not from you as a player. The two golden rules (old site, Meta Book):
  - **No metagaming.** Act only on what your character knows.
  - **Keep morals and politics in character.** Characters can have strong or radical beliefs, and characters at odds can make for great play, but that never carries outside the game.
- The basic loop: the GM describes the scene, players say what their characters try, the GM decides the results and calls for flips, and then describes the outcome. The GM has the final word, but players should feel free to raise a possible mistake so everyone's on the same page. (old site, Meta Book)
- Write rules in active, precise language: "you push the target," not "the target is pushed." (manifesto v5)
- Player-facing text can be light and a bit jokey, like "These are fun, you'll love them," or "Stats and Skills lists the... Stats and Skills." In-fiction quotes and flavor sit beside the rules. (old site, Home; player's guide 2023)
- "Placeholder" is an in-fiction arcanist pseudonym behind a line of named spells and items. (player's guide 2023)
- **Sheet design.** Swap the boxes for values that change a lot for shapes that match a dice set, so players can rest dice on their sheets: squares (d6) for fleeting effects, and triangles (d4 or d8?) for Health levels. The 2k19 notes mark this done ("Ayy we did it boys"). (manifesto 2k19)
- The 2k19 site layout: an intro (Stats and Skills, gameplay examples, a sample character), How to Play (character creation, Glossary, Basic, Combat, Adventuring and Social rules), Techniques, then Items and Things. (manifesto 2k19)

## Ideas noted but not adopted

Ideas from the notes that weren't found in the current game. Suit-pair sets and named check types are listed above.

- **Palhalla.** When you die, you come back. XP turns into "Glory," and Glory buys Techniques at Levels 1-5. One example, "Binding: Legend of {Item}," makes an item part of your legend. You can always reveal it as being on you, nobody else can own it, it can't be destroyed, and it costs Glory equal to the item's Level. Idea, not yet in the game. (old site, Palhalla and Legend Binding)
- **Trap card.** A ranger Technique where you set a card from your deck aside as a prepared trap. When an enemy moves close, you spring it as an Interrupt and attack. "The point is you get to see the card but the GM can't, which is funny." Idea, not yet in the game. (old site, W I P)
- **Mastermind (Level 5).** It needed some effect beyond extra cards a day, which gets weird untied to a Stat. Left unfinished. (manifesto 2k19)
- **Harried at the start of combat.** Everyone starts Harried, to make Reflex flips matter. Considered and set aside. (old site, Manifesto)
