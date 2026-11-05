# FlagonQuest: Designer Notes

Every design decision, and everything the designer has said matters, in
one place. It's the summary of the principles used anywhere in the
project: if a working note, a balance derivation or the simulator relies
on a rule, the rule has a line here.

**How to read it.** The front page has the few things that matter most.
After it, each section goes from the most important points to the
smaller ones. Points end with a pointer to where the detail lives:

- `→ balance.md`, `→ balance_weights_notes`, `→ ENEMY_ENCOUNTER_DESIGN`,
  `→ enemy_sim/...`: the working notes in `design/`, kept long on purpose
  for pricing and simulation work.
- `→ archive X`: `archive/design_docs_2026-11-03/X.md`, the full text of
  the older design docs as they stood when this was written, so nothing
  in them is lost.
- Work still to do lives in `design/todo/`: notes toward a GM guide, the
  ideas backlog, and the prose review queue.

The rules themselves are in `scripts/rulebook.md` and
`scripts/glossary.md`; this is the why behind them. New decisions go in
here, in the right section, with a pointer to where they were worked
out.

---

## The front page: what matters most

**What the game is for**

- **The game is for telling a story together.** Balance keeps players'
  equal shares (XP, Gold, cards) equal in a fight, measured by the
  hardest fight the party can win. (→ Rules design, Cross-cutting)
- **You play a character you design.** No classes: mix and match any
  abilities, and let adventures send the character down new paths.
  (→ Early notes, Vision and feel)
- **Simple and straightforward.** Fun is proactive; options should be
  varied, distinct, obvious and as few rules deep as possible. Aim for
  about 90% balance: some options better in some contexts, none bad.
  (→ Early notes, Design principles)

**How rules are built**

- **Base rules describe the default; Techniques and items are the
  exceptions.** General rules stay general, the exception lives on the
  specific thing, and the most specific rule wins.
- **No counters to counters.** Two levels of strategy is enough.
- **Some things always cost a resource:** healing and gaining cards.
- **No flat damage or success grants.** Bonuses go through Good Luck,
  lowering a Defense, Gambling or the suit pool.
- **Reward cleverness and risk, not raw power.**
- **An Interrupt happens before its trigger.**
- **Bleeding is Health loss over time;** cashing it in stays rare.

**How balance works**

- **1 value = +1 to a flip; an Extra Success = 2.** Target is Level × 3
  an encounter; Net = Value × Rate of Use − Target.
- **Every adjustment goes on one side of the ledger,** with its sign
  checked every time: what the player gives up is +N to Target, what they
  get goes on Value, a per-use cost comes off Value.
- **Price a situational Technique at its value when used.**
- **Balance work is early (Levels 1-2) and late (3-4).** Level 5 is rare,
  and Level 1 can run a bit under.

**Enemies and the table**

- **Enemies play by the players' rules,** with numbers in the players'
  ballpark: same Stats, Skill Totals, weapons and armor, Health near a
  PC's. A goblin shouldn't have more Health than the PC fighting it.
- **Enemies are legible and simple:** readable from what they visibly
  are, with a spread of Defenses worth finding. They're a canvas for the
  party's Techniques, not the painting.
- **Engaging, not a slog.** Spikier, shorter fights are fine; consumables
  cover the rare bad fight.
- **Count the players, pick enemies adding up to that many Slots.**
- **XP is always composite.** Level N enemies are for PCs within 25 XP of
  that Level's schedule.
- **Measure by the day,** two fights with care between them, not by a
  single fight.

**Writing it down**

- **Rules text is as concise as it can be while still getting the point
  across.** Batch effects by when they happen; avoid once-per-round
  triggers; say "twice", then "three times".

---

## Rules design

Every current rules decision, by system. Most important first in each
list. The full reasoning lives in the originals in
`archive/design_docs_2026-11-03/`; the pointers say where.

### Cross-cutting standing rules

- **STANDING RULE: the game is for telling a story together.** The table uses the game to decide where the story goes. Every player gets an equal share of XP, gold and cards to spend shaping it through their character. Balance keeps those shares equal: each way of spending XP should be about as strong in a fight as any other, measured by how much harder a fight a party can take for what it spent. (2026-10-30, → archive RULES_DESIGN, "What the game is for, and what balance is for")
- **STANDING RULE: base rules describe the default; Techniques and items break it.** Said once, where Techniques are introduced ("Techniques are what's meant to go beyond it"), and never restated. Don't hedge a base rule with "unless a Technique..." (→ archive RULES_DESIGN, "Techniques and items are assumed to break the baseline")
- **STANDING RULE: general rules stay general; the specific thing says how it differs.** No carve-out lists inside a keyword or rulebook section. The exception goes in the item's or Technique's own text, and "the most specific rule always wins" (The Basics) does the rest. When a general rule grows carve-outs, move each onto the thing it's about. `[Fleeting]` vs. Bleeding/Harried is the worked case. (2026-10-09, → archive RULES_DESIGN, "General rules stay general")
- **STANDING RULE: no counters to counters.** Two levels of strategy is enough. Necrotic can counter healing and Protected, but nothing gets built to beat Necrotic (a heal that ignores it). General cleanses that happen to list Necrotic are fine. (2026-10-05, → archive RULES_DESIGN, "No counters to counters")
- **STANDING RULE: some effects always cost a resource.** Healing and gaining a card in hand get paid for with a discard or a consumable. Exceptions are conditional triggers, never on-demand. Prefer a fixed payout over a scaling one. Precedent: Second Wind and Lay On Hands (discard, heal 1, or 2 on a Heart), Healing Magic (discard cards equal to its Level). (2026-09-27, → archive RULES_DESIGN, "Some effects always cost a resource")
- **STANDING RULE: no flat damage or success grants.** An item or Technique never grants an Extra Success or a flat bonus to a flip or to damage. Route it through the existing levers: Good Luck, lowering Defense (Vulnerable and friends), enabling Gambling, or a suit-pool assist (Sift, an extra card in the pool). A Swiftblade Vial draft got turned down for this. (→ archive RULES_DESIGN, "Damage/success bonuses stay routed through the existing systems")
- **STANDING RULE: reward cleverness and risk, not raw power.** Something can sit well outside the normal Net band if the strength comes from the player's choices, a drawback they accepted, or a combo they set up. The test: would it be just as strong in anyone's hands doing nothing clever? If so, it's overpowered. Insanity Potion is the example. (→ archive RULES_DESIGN, "Reward cleverness and risk, not raw power")
- **STANDING RULE: an Interrupt happens before what triggers it.** Interrupts are priced on acting first: if Gainsay Downs the enemy, its attack never comes. "You would become Downed" catches the Down from any source. If the trigger names a later point ("after the attack is resolved"), the Interrupt goes there. (2026-10-28, → archive RULES_DESIGN, "An Interrupt happens before what triggers it")
- **Every mechanic has 1-2 home archetypes.** At home it gets the strong or stacking versions; elsewhere only small riders (a Healer can still clear a stack of Bleeding). (2026-10-05, → archive RULES_DESIGN, "Archetypes: jobs and home mechanics")
- **Check a mechanic exists before designing around it.** True-Seeing Lenses, Circlet of Clarity and Comprehend Languages Circlet all died on this: no invisibility or illusion mechanics, no Charmed keyword (Mental Defense already covers mind control), no language system beyond Goblin illiteracy flavor. (→ archive IDEAS_BACKLOG, "Reviewed and declined")
- **Bringing back archived content: rebuild it against its closest live analogue.** Don't trust old numbers, terms or Levels. Distraction (rebuilt against Vanish) is the template. (→ archive IDEAS_BACKLOG, "Source material to mine: cut FlagonQuest content")
- **Binned ideas get logged.** Anything cut or considered and not drafted goes in the backlog's "Reviewed and declined" with a one-line why. Declined isn't deleted forever. (→ CLAUDE.md, "Editing content")
- **(penciled) Niche tools should be frictionless.** A Technique covering a narrow job (taking prisoners) just lets you do it: no extra flip, no penalty. Price the rest of the Technique and treat the niche part as a rounding error. Lawman's Hand is the first case. (2026-09-28, → archive RULES_DESIGN, "Niche tools should be frictionless")

### Core resolution

- **Successes come from exactly two places: Gambling and suit matches.** A flip that beats the difficulty is 1 success. Each Gamble that still succeeds adds 1, and each card in the suit pool matching the Skill's suit adds 1. The margin-based "+1 per 2 points over" idea was considered and cut. (→ archive RULES_DESIGN, "Applied so far")
- **Gambling is a blind bet.** Declare how many times before the flip; each Gamble is -2 to the result and +1 Extra Success if it still succeeds. Not GM-gated. A character with Skill to spare bets safely; one at the edge risks the whole flip. (→ archive RULES_DESIGN, "Successes as the universal resolution currency")
- **Only weapon attacks can be Gambled on, among damaging attacks.** Spell attacks can't. Always intended, written down later. (→ archive PROSE_REVIEW_QUEUE, "### Gambling")
- **An attack is a check like any other.** Flip, add Skill Total, compare to the Defense. Each success past the first is +1 damage on any damaging attack (weapon or not). Combat adds pacing (AP, turn order), not a separate resolution system. (→ archive RULES_DESIGN, "Applied so far", Making an Attack)
- **Hearts has no flat attack-damage bonus.** The old `[Hearts]` damage rule is gone; attack damage comes only from the general Successes rule. Hearts' role stays healing and support. (→ archive RULES_DESIGN, "Applied so far")
- **Supporting is how the whole party joins a scene.** Name a Skill (any Skill the GM accepts) before the check, flip against a flat 11, and on a success the leader gets Good Luck. Framed as encouraged, not a fallback. No AP cost stated; it isn't a formal combat action. (→ archive RULES_DESIGN, "Applied so far", Supporting)
- **Multi-success checks can keep retrying.** What counts as a bad fail, and its cost, is GM fiat per scene (time pressure, being noticed). No formula. (→ archive RULES_DESIGN, "Open questions / TODO")
- **Play: a card from hand either replaces a flipped card or just adds its suit to the pool.** A replacing card's suit joins the pool too. The old "+1 to that flip's card" is gone, and the glossary says "Discard a card from your hand," matching Technique card costs. (→ archive PROSE_REVIEW_QUEUE, "#### Play")
- **Good and Bad Luck cancel one for one.** Each Good Luck flips an extra card and you pick; Bad Luck makes you take the lowest. (rulebook, "Good and Bad Luck")
- **Rounding is always down.** Any calculated fraction rounds down. (→ archive PROSE_REVIEW_QUEUE, "## Calculated Statistics")
- **"Once per day" resets on your next full night's rest, not a 24-hour clock.** A long stretch without rest doesn't refresh early; it risks Exhaustion. (→ archive PROSE_REVIEW_QUEUE, "## A Full Night's Rest")

### Suits and cards

- **Each suit is a full portfolio, roughly as useful overall, not useful the same way.** Asymmetry is fine. Skill count and usage don't need to match (Hearts has the fewest Skills but the second-most usage, thanks to Theurgy). (→ archive RULES_DESIGN, "Suits: an emerging identity per suit")
- **Suit ↔ element is the tie-breaker.** Hearts↔Brilliant, Clubs↔Fire, Diamonds↔Shadow, Spades↔Frost. Concrete mechanical ties beat lore arguments (Insight stays Spades because it sets Reflex and turn order). (→ archive RULES_DESIGN, "Suits")
- **Skill → suit table.** ♥ Presence, Rapport, Performance, Survival, Theurgy. ♣ Brawl, Athletics, Resilience, Might, Meditation, Sorcery. ◆ Acrobatics, Craft, Composure, Masquerade, Streetwise, Mixology, Stealth. ♠ Melee, Archery, Awareness, Insight, Persuasion, Academics, Medicine. Every Skill's rulebook entry names its suit too. (→ archive RULES_DESIGN, "Suits")
- **Suit portfolios.** ♥ offense Frightened, Taunted; defense Brilliant Ward, healing scales off Hearts. ♣ offense Bleeding, Crippled; defense Fire Ward, Hasted, Shift. ◆ offense Harried, Vulnerable, Necrotic; defense Shadow Ward, Cover/Concealment. ♠ offense Slowed, Push, Difficult Terrain; defense Frost Ward, Protected; utility turn-order adjustment and card manipulation (a placeholder tie, not a rule every card effect is Spades). (→ archive RULES_DESIGN, "Suit portfolio so far")
- **A Technique can name a suit directly** regardless of Skill (Slowed scales with Spades). Otherwise the matching suit is the Skill's. (rulebook, "The Suit Pool")
- **Card-sharing is a throughline.** Players should want to hand each other cards. The Play rule already allows it on any willing ally's flip; Ritual Magic lets an ally discard to pay your Spell costs. (→ archive RULES_DESIGN, "Card-sharing as a deliberate design throughline")
- **A patient doesn't spend their own cards on their own healing.** Pressure Point Revitalization keeps that as its one unique trick. (→ archive RULES_DESIGN, "Things considered and deliberately not done")
- **Characters need a couple of ways to spend cards from creation.** More generic Level 1-2 card sinks like Second Wind (0 AP, discard, heal 1 or 2 on a Heart). (2026-09-28, → archive IDEAS_BACKLOG, "More generic card-spending Techniques")
- **Embolden and Bolstered stay cut.** GM rulings cover Taunted/Frightened case by case, and Wounded clears on any healing. Warpath (Level 4 Barbarian Style) is the one place that ignores Taunted, Frightened and Wounded, because a Style is where non-stacking rule-breaks go. (2026-09-28, → archive RULES_DESIGN, "Suits")

### Character building

- **XP costs.** A Skill point costs the new total; a Stat point costs twice the new total; a Technique costs three times its Level. Stats and Skills cap at 5 ranks; at creation, 3. (→ archive PROSE_REVIEW_QUEUE, "## Spending Experience")
- **Starting XP is 75 and covers Stats, Skills and Techniques from one pool.** The Quick Creation numbers (29 + 28 + 18) were always meant to. (→ archive RULES_DESIGN, "Applied so far")
- **Skill Total drives every calculation; raw Skill value is only for prereqs.** Skill Total is Stat + Skill. Defenses are 8 + a Skill Total (Vital: Resilience; Mental: Composure; Vigilant: Insight; Dodge: Acrobatics or Brawl; Parry: the weapon's Skill + its Defense). (→ CLAUDE.md, "Design conventions"; rulebook, "Calculated Statistics")
- **Archetype list.** Monk, Duelist, Barbarian, Guardian, Archer, Sorcerer, Theurgist, Druid (added 2026-09-30), Healer, Leader, Face, Rogue, Scout, Crafter, Scholar, plus a General tag. A design tag the site never shows. Hybrids (paladin, spellblade) are two tags. Summoner and Necromancer dropped; summons sit with their caster. (2026-09-28, → archive RULES_DESIGN, "Character archetypes")
- **Every combat archetype has 2-4 home mechanics, at least one available at Levels 1-2.** Generalist Styles get tagged with every archetype where their mechanic is home or shared. A coverage check looks for archetypes with no early home, mechanics with no home, or homes nothing's built on. (2026-10-05, → archive RULES_DESIGN, "Archetypes: jobs and home mechanics")
- **Home mechanics by archetype.** Guardian: Taunted, Protected, holding ground. Barbarian: Bleeding, Gambling, ignoring debuffs and Wounded, Vigor. Duelist: Harried, Opportunity Attack, Repeat, focus fire. Rogue: Vulnerable, Crippled, hidden attacks. Archer: Good Luck on accuracy, pinning, covering fire. Scout: Outflank/Stagger, first strike, hidden. Sorcerer: Burst, elements, Teleport. Theurgist: Ward, healing, Necrotic. Healer: healing, clearing Bleeding and Poison, raising the Downed. Druid: Summon, terrain. Leader: Hasted, Good Luck for allies, combat Support. Face: Frightened, Taunted, Presence attacks, Pressure. Monk: the martial Schools table. (→ archive RULES_DESIGN, "Archetypes: jobs and home mechanics")
- **Skill Total 7 is the ceiling for the best ordinary craftsperson.** Chargen tops out at 6 (3 + 3). 7 is a season or two of practice; 8+ means adventuring or hard training. A consideration when setting a mundane recipe, not a hard cap. (→ archive RULES_DESIGN, "Skill Total 7 as a crafting-tier anchor")
- **Calculated statistics.** Health 5 Shallow + 5 Deep. Speed 1 + Agility. Reflex = Insight Skill Total. Cards per day = twice (Cunning + Mind). Rest healing = Body. Every Resist starts at Essence. (rulebook, "Calculated Statistics")
- **(penciled) Archetype prereq Skills.** Many Techniques need only their main Skill. A secondary prereq is flavor, mostly on combat Techniques and Styles. Monk: Brawl/Meditation, secondary per School. Duelist: Melee/Acrobatics/Archery, Insight (Tiger: Acrobatics). Barbarian: Might, Resilience. Guardian: Resilience/Melee/Brawl/Presence, Might. Archer: Archery (Acrobatics for thrown), Awareness. Sorcerer: Sorcery, Resilience (pencil). Theurgist: Theurgy, none settled. Druid: Theurgy, Survival. Healer: Medicine/Theurgy, Composure (pencil). Leader: Performance/Presence, Rapport (pencil). Face: Presence/Rapport/Persuasion, Insight (pencil). Rogue: Stealth/Masquerade/Streetwise, Acrobatics (pencil). Scout: Survival/Athletics/Awareness, Athletics (pencil). Crafter: Craft/Mixology, Academics (pencil). Scholar: Academics, Insight (pencil). If Guardian and Barbarian need pulling apart, Guardian's defense could lead with Composure. (2026-09-30, → archive RULES_DESIGN, "Archetype prereq Skills")

### Techniques and Styles

- **STANDING RULE: what belongs in a Style.** Fun, powerful effects that break a fundamental rule and mustn't stack: defensive options too good stacked, raw stat boosts, Good Luck, always-on oddities (elemental Unarmed). One Style at a time keeps them from interacting in ways nobody planned. Every archetype should have at least one Style it wants. (2026-09-28, → archive RULES_DESIGN, "What belongs in a Style")
- **A Style Condition only exists to pay for something.** A Condition added for theme just locks out other archetypes; drop it and let the archetype tag carry the theme. Follow Through and Inexhaustible Guardian lost theirs. (2026-09-30, → archive RULES_DESIGN, "Style Conditions only when they pay for something")
- **A flat Defense bonus is too good.** It's been stripped from several Style drafts (Drunken Brawling redraft, Swashbuckler's Focus, Earthen Fist Posture). (2026-10-03, → archive IDEAS_BACKLOG, "Reviewed and declined")
- **Style coverage target.** Each combat archetype gets a few early Styles (Levels 1-2) and a few late (3-4); long-run 3+ early, 2+ late. A couple per archetype is enough for now. Crafter, Scholar and General need none. A multi-tag Style counts for each. (2026-10-05, → archive IDEAS_BACKLOG, "Style coverage by archetype")
- **Level 5 Styles are rare.** A character buys at most one, late, around 200+ XP if ever. Balance and coverage work happens in the early and late buckets. (→ archive IDEAS_BACKLOG, "Style coverage by archetype")
- **Style entry and exit.** Enter or leave at the start of your turn; entering one leaves any other; break the Condition and you leave at once. (glossary, `[Style]`)
- **Spellblades are first-class.** A Spell or Discipline channeled through a weapon Implement counts as an attack with that weapon. (→ archive RULES_DESIGN, "Weapon and Implement Masterwork enhancements")
- **Turn-order adjustment is a mechanic to lean into.** It lets one character act inside a window another opened. (penciled) Value 1.0 per place shifted, linear, uncapped for now; revisit if a design needs double-digit places. (→ archive RULES_DESIGN, "Turn-order adjustment")
- **Builder Notes** hold "how this card works" reference text for any Technique whose behavior isn't obvious from Effects. (→ CLAUDE.md, "Design conventions")
- **(open) The Ritual Magic pattern** ("a willing ally may pay your cost") may spread beyond Spells, possibly as a Style so it can't stack with other strong enablers. Ritual Magic itself is now a Style. (→ archive RULES_DESIGN, "Card-sharing")

### Martial Schools

- **Five unarmed Schools in two kinds.** Snake and Bear are the normal ones: effects scale on Brawl, with a secondary Skill as a prereq only (Snake: Insight, changed from Acrobatics 2026-09-28; Bear: Might). Demon, Shugen and Great Old Oak are supernatural and scale on Meditation. (→ archive RULES_DESIGN, "The three supernatural martial Schools")
- **Demon / Shugen / Oak split** (a goal to steer by). Demon: offense; hybrids vs. Vital, Shadow damage; owns Vulnerable, Harried, Necrotic, Bleeding (shared with Bear), Health loss, self-costs. Shugen: control; vs. Mental, Brilliant; owns Crippled, Frightened, Slowed, Push, Teleport. Oak: defense, closest thing to a tank; vs. Vigilant, Physical (may get a buff later), defensive riders on a hit; owns Protected, Ward, self-healing, clearing your own debuffs, counters, Taunted. Hasted belongs to none. (→ archive RULES_DESIGN, "The three supernatural martial Schools")
- **Hybrid Technique shape.** An Unarmed weapon attack (Brawl to hit) against the School's Defense, dealing the School's element, extra effects free to scale on Meditation. Don't swap Meditation in for the attack itself. (→ archive RULES_DESIGN, "The three supernatural martial Schools")
- **Pure Meditation attacks mirror the matching spell.** Meditation to hit, Mind for damage, against the School's Defense. Firefly Leaves the Hand is Level 1 War Magic with its point on Range, dealing Brilliant. (→ archive RULES_DESIGN, "The three supernatural martial Schools")
- **Coverage target: each supernatural School has a Technique at Levels 2, 3 and 4 on both tracks.** Met as of 2026-09-28. (→ archive IDEAS_BACKLOG, "Level coverage (unarmed Schools)")
- **School pricing gets a bonus.** Each School backs an archetype weaker on its own, so its Techniques (mostly always-on Styles) get a bit extra budget. A Dueling Style gives up a shield's +2 Parry and may have about that much more. Brawl takes a -1 Skill adjustment; needing both hands empty is +2 on top. (→ archive IDEAS_BACKLOG, "Pricing principle for all Schools")
- **Lion = Dueling, Tiger = dual-wielding.** Lion: one one-handed weapon, empty off hand. New Lion/Tiger content is designed fresh. (→ archive IDEAS_BACKLOG, "Lion / Tiger")
- **Empty hands count as dual-wielded Unarmed weapons.** So Storm of Blades already covers flurry-of-blows. (2026-10-03, → archive IDEAS_BACKLOG, "Flurry of Blows")
- **Bear needs empty hands but allows armor.** Snake's Techniques don't apply debuffs. Overlap stays light: Bear's Slowed/Frightened are riders, Shugen's are the main effect; Snake and Bear Push by shoving, Shugen by ki wave; Snake clears debuffs by breaking a grapple, Oak by endurance. (→ archive RULES_DESIGN, "The three supernatural martial Schools"; archive IDEAS_BACKLOG, "Bear")
- **Naming.** Shugen gets poetic martial-form names, a nod to what it does. Demon split from Shugen and its names are rotten twists of Shugen ones (Firefly Dies in the Hand). Both stay about five words or fewer, not too abstract. Oak names are plain natural imagery, 3-4 words. (→ archive RULES_DESIGN, "Naming and story")
- **Ki = Shugen.** "Ki Style" is the old name. (→ archive IDEAS_BACKLOG, "Ki = Shugen")
- **(penciled) Spirit Hands vs. Shugen's Brilliant attacks.** Keep a plain "Unarmed deals Brilliant" Style; likely fix is +1 damage when the attack already deals Brilliant. (→ archive IDEAS_BACKLOG, "Known conflict")
- **(idea) Oak Physical Resist boosts only if exclusive with armor**, as an optional unarmored line. (→ archive IDEAS_BACKLOG, "Great Old Oak")

### Combat and effect keywords

- **STANDING RULE: Bleeding is Health loss over time.** It goes around Resist. When it decays, half the stacks come off, rounded up, and the bearer loses that much Health. It always decays at the end of the bearer's turn, even the turn it was gained. Protected stops a tick like any Health loss. Leftover stacks keep decaying after a fight. Rare as a main tool, otherwise small add-ons. Was one stack per turn until 2026-10-19. (2026-10-07, reworked 2026-10-19, → archive RULES_DESIGN, "Bleeding is Health loss over time")
- **Cashing in Bleeding stays rare.** Turning stacks into Health loss at once (Reign of Blood, Circling Vulture) stays in a few lanes: Sorcerer's War Magic, maybe a Style. No weapon-user version (Open the Wound was declined). (2026-10-17, → archive RULES_DESIGN, "Bleeding is Health loss over time")
- **Spending Bleeding is plain cost wording.** Spent stacks are gone and cause no Health loss; "for each" counts only what's actually spent. An ability that spends Bleeding gives something in its own lane (Barbarian gains Protected, Duelist Harries the target). (2026-10-20, → archive RULES_DESIGN, "Spending Bleeding")
- **Bleeding's Health loss is tied to decay only.** Cleansing stacks never hurts. (→ archive RULES_DESIGN, "Applied so far", Bleeding)
- **`[Fleeting]`: lose 1 stack at the end of your turn; same-turn skip only.** If you gain it on your own turn from zero, skip that turn's removal. Bleeding and Harried say in their own entries that they still come off. In social encounters, remove 1 stack after each Statement your party makes; outside encounters, roughly every 6 seconds. The skip "might get re-evaluated." (2026-10-09, → archive RULES_DESIGN, "Applied so far", Fleeting; archive PROSE_REVIEW_QUEUE, "#### [Fleeting]")
- **Protected is a mandatory substitution.** "If you would lose Health to something other than a cost, remove up to that many stacks instead." (→ archive RULES_DESIGN, "Ward reimagined")
- **Ward: +2 Resist to its element while you have stacks, and each stack absorbs 1 Health loss from that element.** Raised from +1. Never scales per stack: Resist has no upper bound, so that path leads to immunity. (→ archive RULES_DESIGN, "Ward reimagined")
- **Necrotic counters healing and Protected.** Protected soaks it up somewhat, as intended. (→ archive RULES_DESIGN, "No counters to counters")
- **Harried: -1 Dodge and Parry per stack, all cleared at the end of your turn.** (glossary, Harried)
- **Opportunity Attack (renamed from Counterattack).** A weapon attack, or a Technique making a weapon attack against only that creature, costing at most 2 AP. Extra AP spent on top doesn't count toward the cap. (→ archive PROSE_REVIEW_QUEUE, "#### Opportunity Attack")
- **Negated (renamed from Countered).** The thing is still expended and its costs paid, but has no effect. Renamed so it doesn't read as related to Opportunity Attack. (→ archive PROSE_REVIEW_QUEUE, "#### Counterattack")
- **Repeat.** Make the attack again against the same target in the same action, with its Technique's effects. AP, the Encounter use and self-effects happen once. A Grenade is used up per attack. A Repeat can't be Repeated. Repeat's home is Storm of Blades. (→ archive PROSE_REVIEW_QUEUE, "#### Repeat"; archive IDEAS_BACKLOG, "Crashing Wave Approach")
- **Range increases also move "adjacent" effects.** They can target something adjacent to your chosen point instead. (→ archive PROSE_REVIEW_QUEUE, "#### Range")
- **Burst (X): the space plus everything within X meters, in a circle.** Burst 0 is the space itself. Use it for every new area effect instead of "adjacent to" or "within X meters"; convert old text on sight, no full sweep. Kilometer-scale weather stays as is. (→ archive RULES_DESIGN, "New keyword: Burst (X)")
- **Vigor: pay a Technique's Level to regain a use.** Unifies Soul Soup's and Solemn Covenant's bespoke point names. (→ archive PROSE_REVIEW_QUEUE, "#### Vigor")
- **`[Poison]` lasts until it exposes a creature or the wielder's next full night's rest.** Was 1 hour; the feel-bad of early expiry outweighed the narrative oddity. (→ archive RULES_DESIGN, "Open questions / TODO", Poison duration)
- **Light Two-Handed weapons attack with Melee or Brawl.** Spear or quarterstaff gives a brawler a weapon without buying Melee. Runs a point hot for Brawl users; left as is. (2026-10-24, → archive RULES_DESIGN, "Light Two-Handed weapons can use Brawl")
- **Thrown weapons are abstracted.** You have enough to fight with and recover them after the encounter. No mid-fight return items. (→ archive IDEAS_BACKLOG, "Returning Knives / Weapon of Sending")
- **Any weapon attack can be Parried.** (→ archive IDEAS_BACKLOG, "Branches in the Wind")
- **Non-lethal attacks take Bad Luck**, unless a Technique like Lawman's Hand removes it. (→ archive RULES_DESIGN, "Niche tools should be frictionless")
- **Counter actions are gone.** Leftover AP is what Interrupts spend. (→ archive IDEAS_BACKLOG, "Archived Stances, declined")
- **Dead keywords.** Dazed, Snared, Weakened, Off-Balance, Enervated, Prone and Spirit damage aren't live; translate (Off-Balance became Harried in one port). (→ archive IDEAS_BACKLOG, "Heads-up for drafting")

### Elements and Resist

- **Five damage types: Physical, Fire, Frost, Brilliant, Shadow.** An attack deals one type and checks that one Resist. (→ CLAUDE.md, "Editing content")
- **STANDING RULE: Fire is the common element.** Not better, just the obvious thing to resist. Rule of thumb: 3 in 4 enemies deal only Physical; among the rest Fire is about twice as common as each other element (Fire ~10%, others ~5% each). When an element shows up, it's about two-thirds of that fight's damage. New elemental content defaults to Fire unless theme says otherwise. Battle Magic's baseline is Fire, Fire Masterwork items are built one Level lower, low-Level damage Grenades default to Fire. (→ archive RULES_DESIGN, "Fire is the deliberately common element")
- **Players can prepare for a specific element**, mostly with consumables for a known fight. (→ archive RULES_DESIGN, "Fire is the deliberately common element")
- **Resist lives on Torso.** +1 Resist from Torso gear, maybe +2 at Level 5. No archive source pairs Resist with Neck or Ring. (→ archive RULES_DESIGN, "Equipment slots each have an intended design lane")
- **Baseline damage over Resist: 2-3.** A baseline weapon hit with no Stat in damage should net 2-3 over Light Armor's Resist 1 (Light 1H 3+Stat, Light 2H and Heavy 1H 4+Stat, Heavy 2H 5+Stat). That's why Damage is worth 2/pt with no Resist discount. Check new weapon and enemy numbers against it. (→ archive RULES_DESIGN, "Baseline damage-over-Resist assumption")

### Items and equipment

- **STANDING RULE: each slot has a lane.**

  | Slot | Lane |
  |---|---|
  | Head | Mental, vision |
  | Hands | What your hands can do: manipulate, create, access. Nothing that grants or modifies an attack |
  | Feet | Mobility |
  | Belt | Carrying items |
  | Torso | Direct protection, vitality/healing, Resist |
  | Held | Weapons and other active-use items needing an action |
  | Neck | Niche, boring, passive utility. Not interactive or defensive |
  | Ring | A specific active ability, or an augment to one Skill/ability |

  (→ archive RULES_DESIGN, "Equipment slots each have an intended design lane")
- **STANDING RULE: Weapon and Implement Masterwork overlap heavily.** Loot should excite both martial and caster players, and a spellblade shouldn't need two held items. (→ archive RULES_DESIGN, "Weapon and Implement Masterwork enhancements are meant to overlap heavily")
- **STANDING RULE: Masterwork slots don't need equal Level bands.** Some mechanics plateau (Belt capacity), and some slots are just less exciting to build toward. Let each slot's spread follow what it supports. (→ archive RULES_DESIGN, "Masterwork slots don't need equal Level bands")
- **New Masterwork defaults to Levels 1-3.** Levels 4-5 completionism isn't a priority: loot is plentiful by then, and capstones are usually weapons or armor. (→ archive RULES_DESIGN, "Where new Masterwork content should go")
- **Held, Torso, Ring and Neck are the "range" slots.** They should offer variety. Feet and the like stay narrow by design. An under-used material (Frost) goes into one of those four. (→ archive RULES_DESIGN, "Where new Masterwork content should go")
- **Every Masterwork item sits on a base item.** Head: Basic Clothing or Basic Jewelry. Neck: either (cloak or necklace is the crafter's choice). Ring: Basic Jewelry only. Hands, Feet, Belt: Basic Clothing. Torso: Light Armor, Heavy Armor or Basic Clothing. Held: the weapons. Basic Clothing and Basic Jewelry are both usable on their own and as Masterwork bases. (→ archive RULES_DESIGN, "Every Masterwork item ties back to a real Base Item Option"; "Crafting Schools")
- **Unarmored is an opt-in archetype choice.** Basic Clothing isn't armor of any kind. Going without is meant for builds with Techniques that reward it, the same as Unarmed. (→ archive RULES_DESIGN, "Unarmored as an opt-in archetype choice")
- **Weapon and armor costs.** 1H melee 3 Gold, 2H melee 6, thrown 5, bows 6 (two-handed), shields 3, light armor 4, heavy armor 8. Bigger tiers double (Cart Small/Medium/Large 12/24/48). (→ archive RULES_DESIGN, "Final correction"; "Cart, Medium / Wagon, Large")
- **Spirit Quest Ointment is a Potion,** a special-rule consumable that breaks the pattern on purpose (15 materials, three Main Types). (→ archive RULES_DESIGN, "Spirit Quest Ointment moved out of Masterwork")
- **Identifying a Masterwork item takes an hour of examination, no roll.** (→ archive IDEAS_BACKLOG, "Artisan's Eye")

### Crafting

- **No check to craft. Settled.** The uncertainty already happened upstream (finding materials, the fight, the recipe). A crafting roll would re-roll something the fiction resolved. (→ archive RULES_DESIGN, "Crafting simplification (applied)")
- **One materials formula for everything.** Each recipe states Total Materials outright. At least half (rounded down) must be Main Types; the rest can be Optional, up to half. Every material must be at least the item's Level. "Cost ÷ Level" is only an authoring guideline, never a live rule. (→ archive RULES_DESIGN, "Decided replacement: one universal formula")
- **Totals by family.** Masterwork 20 (Level × 20 Gold price, materials worth 1 Gold per Level). Potions, Poisons, Grenades and Food 2. Alcohol 1. Weapons, armor and tools use their own Gold cost. Unarmed Enhancer 3. Unarmed and Improvised weapons aren't craftable. (→ archive RULES_DESIGN, "Original numbers restored"; "Final correction")
- **Masterwork Optional Type comes from the base item.** The enhancement lists its own Main Type; the chosen base's Main Type becomes Optional. An item you already own can stand in for the Optional materials if it's at least the enhancement's Level. (→ archive RULES_DESIGN, "Concise baseline recipe format"; rulebook, "Materials")
- **Masterwork has no separate School when it goes on a base item.** Building the base already took the training. A Masterwork with no base states its own School. Replaces the old "same as base item" rule. (crafting_recipes.csv, CR017)
- **Several Main Types without "or" means one of each.** "Wood or Bone" is a choice; a list with no "or", where each Type drives a separate part of the item (Robes of the Elemental Lord's four Resists), needs at least one of each. (→ archive PROSE_REVIEW_QUEUE, "#### Materials / #### Time")
- **STANDING RULE: Optional never repeats a Main Type.** It unlocks nothing. Applies cleanly to single-base slots (Neck/Ring, Hands/Feet/Belt); multi-base slots (Head, Torso, Held) can overlap the union. (→ archive RULES_DESIGN, "Optional Materials shouldn't repeat an item's own Main Type"; "A second redundancy sweep")
- **Err toward material flexibility.** A player already paid for the Craft Skill and the School. Cloth/Leather and Wood/Bone are full analogues; Weapon and Armor recipes list the other Schools' Main Types as Optional (full three-way symmetry). Types are coarse categories, not a parts list. (→ archive RULES_DESIGN, "Crafting simplification", Weapons/Armor; "Crafting Schools")
- **Schools pair up.** Smithing (Metal) with Carving (Wood, Bone); Jewelrymaking (Precious) with Tailoring (Cloth, Leather). Alchemy (Mixology) uses Medicinal; Cooking (Mixology or Survival) uses Food. (→ archive RULES_DESIGN, "Crafting Schools")
- **Bows are Carving-only. Heavy Armor is Smithing-only.** Bows give Carving its own niche. Carving gets Medium Armor like the others. Small metal tools staying Smithing-only is fine. (→ archive RULES_DESIGN, "Crafting Schools", Smithing vs. Carving)
- **Medicinal is Alchemy's glue.** Potions, Poisons and Grenades take Medicinal as their only Optional. Food also takes Bone, since food should be easier to manage. Medicinal Supply counts as an Alchemy consumable. (→ archive RULES_DESIGN, "Resolved", Alchemy)
- **Basic Clothing:** Main Cloth or Leather; Optional Bone, Metal, Precious ("something a little nicer"). (→ archive RULES_DESIGN, "Crafting Schools", follow-up)
- **Crafting Skill Total by tier.** Masterwork Craft and Alchemy/Food Mixology both follow 4/6/8/9/10 by Level. Weapons Craft 4, Medium Armor Craft 5, Heavy Armor and Wagon (Large) Craft 7. Full table in `design/balance.md`. (→ archive RULES_DESIGN, "Skill Total 7 as a crafting-tier anchor")
- **Time is two GM-adjustable baselines.** Clothing, armor, weapons and Masterwork: 8 hours. Alchemy and Food: 1 hour, any number of the same item at once. (→ archive RULES_DESIGN, "Follow-on: #### Time simplified")
- **Food harvest yields.** A rodent, fish, bird or fistful of insects is 1 Food; person-sized about 5; a boar, elk or bear 10+. (→ archive PROSE_REVIEW_QUEUE, "## Material Types")
- **Materials are worth Gold equal to their Level.** Most sell for much less; Precious sells at full value. (rulebook, "Material Types")

### Resting, food and costs

- **A full night's rest runs three Cycles in order: Discard, Recovery, Draw.** In each, the rulebook's action comes first, then anything from items or abilities tied to that Cycle. Draw your hand, then add a bonus draw. (→ archive RULES_DESIGN, "New term: Cycle")
- **Only the first special meal a day counts.** A second still feeds you but grants no bonus. Closes a stacking hole the Food pricing assumed was closed. (→ archive PROSE_REVIEW_QUEUE, "## Food and Exhaustion")
- **Food and Exhaustion isn't wilderness-only.** 1 Food item and 4 liters of water a day; a day without, or 24 hours without rest, means exhausted (-2 to flips, Speed, Defenses); a prolonged stretch can kill. Lives in Health and Resources. (→ archive RULES_DESIGN, "Traveling and Exploration", comparison pass)
- **Costs: "spend" means paid and gone.** Variable costs are at least 1. You choose the Shallow/Deep split when paying Health. (→ archive PROSE_REVIEW_QUEUE, "## Costs and Commitment")
- **Wounded clears on any healing.** (→ archive RULES_DESIGN, "Embolden and Bolstered")

### Social Encounters

- **A social encounter is an extended check.** The GM sets a target number of successes. No team-check subsystem, Concessions, front/back positioning or Charismatic/Strategic statements. (→ archive RULES_DESIGN, "Social contests reworked")
- **Statements have fixed Defenses.** Persuasion targets Vigilant; Presence and Rapport target Mental. Techniques can open the other Defense later. AP isn't mentioned; it only matters in combat. (→ archive RULES_DESIGN, "Social contests reworked")
- **Pressure replaces Concessions.** A GM-tracked total of circumstances piling up, applied as Bad Luck on Statements and Support checks alike. GM paces it (taking too long "may" add some). High enough, the GM ends the check in failure. (→ archive RULES_DESIGN, "Introduced Pressure"; archive PROSE_REVIEW_QUEUE, "## Social Challenges")
- **Ignoring Pressure vs. removing it.** Ignoring drops the Bad Luck but Pressure keeps climbing toward failure. Removing clears it, and is rarer and stronger. (→ archive PROSE_REVIEW_QUEUE, "## Social Challenges")
- **Combat keywords in social encounters.** Fleeting effects lose a stack after each of your party's Statements. Frightened and Taunted cover the checks one side makes to add Pressure to the other; an NPC's Pressure-adding check counts as an attack on the party. (→ archive PROSE_REVIEW_QUEUE, "#### Frightened, #### Taunted"; archive IDEAS_BACKLOG, "Techniques with stale 'Social Contest'-era mechanics")
- **Outcomes unchanged.** Win Over, Disrespect, Agreement. (→ archive RULES_DESIGN, "Social contests reworked")
- **Masquerade needs something to sell it.** Nothing to back the part is Bad Luck. A Disguise Kit clears that for an everyday disguise. A specific prop that belongs to the exact role grants Good Luck at the GM's call. (→ archive PROSE_REVIEW_QUEUE, "#### Masquerade")

### Exploration and travel

- **Turns and AP are combat only.** Exploration and social encounters have their own pacing. (→ archive RULES_DESIGN, "Full-book broad review")
- **Travel runs in legs.** The GM sets a leg's length by terrain and danger. Each character takes one action and one check per leg, no retries. A failure is "nothing happens" or "a complication lands," by GM call. Move isn't a travel action any more. (→ archive RULES_DESIGN, "Traveling and Exploration")
- **Scout: flat difficulty 11.** Reveals the current leg and a clue about the next. **Search:** GM-set difficulty. **Stealth:** the existing group-check rule. (→ archive RULES_DESIGN, "Traveling and Exploration")
- **Pushing the Pace.** The whole party agrees, gives up its leg actions, covers more ground, and any complication lands with no roll. (→ archive RULES_DESIGN, "Traveling and Exploration")
- **Movement: climbing, jumping and swimming share a budget of half your Athletics Skill Total per move action.** 1 per horizontal space, 2 per vertical. It only covers spaces you couldn't otherwise cross, and can't take you past your Speed. A standing character fills two vertical spaces and can reach the space by their head. No running-start rule. Falling: reduce the distance by Essence or half Acrobatics, then lose that much Health. (→ archive PROSE_REVIEW_QUEUE, "## Calculated Statistics / ### Moving")

### The rulebook itself

- **The rulebook is player-facing only.** Vague GM-side calls (a difficulty) aren't holes; only a player's own choices are. GM guidance goes in `GM_GUIDE_NOTES.md`. (→ archive RULES_DESIGN, "Applied so far", scoping note)
- **Chapter order.** Quick Start Guide, Character Creation (with Spending Experience), The Basics, Your Character, Health and Resources, Adventuring, Creating Items, then supplements. A new player reads the Quick Start, builds a character, and learns the rest as they go. (→ archive RULES_DESIGN, "Applied so far", reorders)
- **The Basics stays light.** Successes there just says they exist and how to earn them; Making an Attack carries the full math. (→ archive RULES_DESIGN, "Applied so far")
- **Don't write a rule about what doesn't happen.** Techniques can already do anything a base rule doesn't cover. Design notes go in the design docs, not the book. (→ archive RULES_DESIGN, "Applied so far", style notes)
- **Supplement content goes in its own tagged chapter.** `# Name {Supplement}`, or a tagged subsection when it overrides a base rule. Untagged reads as Base Game. (→ CLAUDE.md, "Editing content")

### Writing rules text

- **As concise as it can be and still clear.** (→ CLAUDE.md, "Editing content")
- **Damage type: "it deals Shadow damage."** Not "as Shadow" or "instead of Physical." (→ CLAUDE.md, "Editing content")
- **Batch effects by when they happen.** "If it hits, it deals Brilliant damage and Pushes the target 3 meters." Damage type first, then riders. Same for "If it's Parried" and "If it hits or is Parried." Split only when it's complicated. (→ CLAUDE.md, "Editing content")
- **Avoid once-per-round triggers.** At 1.25 attacks a round the cap barely binds. Trim the per-trigger effect instead (Furious Swipes). Keep a cap only when the uncapped version breaks, and say why. (2026-10-02, → CLAUDE.md, "Editing content")
- **When a limit is needed: "Once per round, when X, you may Y."** Optional, never "the first time each round." Mandatory only when that's the balance point. (2026-09-30, → CLAUDE.md, "Editing content")
- **Paying more AP: "spend an extra N AP."** On top of the action's own cost; a cost cap only looks at the base cost. (2026-10-04, → CLAUDE.md, "Editing content")
- **"For the encounter,"** never "until the end of the encounter." (→ CLAUDE.md, "Editing content")
- **Counts in words: once, twice, three times, four times.** Never "thrice," never numerals, never "1 Good Luck." Same in formulas ("[twice X]"). (→ CLAUDE.md, "Editing content")
- **State things positively and self-contained.** Say what a thing is or does. Mirror shared wording (Ward's absorption copies Protected's) rather than "same as X, except Y." (→ archive RULES_DESIGN, "Applied so far"; "Ward reimagined")
- **Prose sections read as continuous paragraphs.** Open with the in-fiction reason, then the rule, then an "Example:" paragraph with actual numbers using the named cast. Bullets only for enumerated lists. Asides with " - ". Curly quotes and apostrophes. Dashes and semicolons when they help, not by reflex; vary sentence length. (→ CLAUDE.md, "Editing content"; archive RULES_DESIGN, "Applied so far")
- **Fluff and Effects are separate columns in every content table.** Flavor lead-ins go in Fluff, the rule in Effects; blank Fluff is normal. Split blended rows when touching them. (→ CLAUDE.md, "Editing content")
- **Supplement and Excluded By.** `Supplement` gates what's offered for new picks and never hides what a build already has. When a supplement replaces a Base Game Technique, tag the original "Excluded By" and add a same-named supplement row. (→ CLAUDE.md, "Editing content")
- **Draft rules prose in chat, then commit clean.** No review markers in `rulebook.md` or `glossary.md`. (→ CLAUDE.md, "Quick reference")

### Names and terms

- **Renames, applied on sight.** Elementalism → Sorcery. Instinct Defense → Vigilant Defense (JSON field stays `instinct_defense`). Bodily Defense → Vital Defense. Soak → Resist. Spirit damage → Brilliant. Social Contest → Social Encounter. Concessions → Pressure. `[Stance]` → `[Form]` → `[Style]`. "X Style - Y" Technique names → "X School - Y". Counterattack → Opportunity Attack. Countered → Negated. Legerdemain the Skill → Stealth (not the Legerdemain Technique, T034). Argument/Suspicion Defense → Vigilant/Mental. Adventurer's Kit → Camping Kit, Rope and Firestarter. Stunting → Bingus/Golden Bingus. Ki Style → Shugen. (→ archive RULES_DESIGN, various; CLAUDE.md, "Quick reference")
- **Gone with no replacement.** Focus, Willpower, Mana, Soul, Glory, the old commit-to-cast spell rule (committing a cost in Costs and Commitment is still live), Technique "Power," Counter actions, the Diplomacy and Intimidate Skills, Charismatic/Strategic statements. (→ archive RULES_DESIGN, "Site export gap-fill"; archive IDEAS_BACKLOG)
- **`features.csv`'s `(Style)` Feature label stays.** Different subsystem, not confusable. (→ archive RULES_DESIGN, "Form → Style rename")
- **Never rename a "Placeholder's [Alliterative Name]" item or Technique.** Placeholder is an in-fiction pseudonym for clever, faintly embarrassing student magic, passed down with no traceable author. Marks: silly alliterative names, low-Level utility. The legend is inconsistent on purpose (pronouns, martial demigod vs. prankster student); the one shared detail is 101 maneuvers or incantations. (→ archive RULES_DESIGN, "Naming convention — Placeholder")
- **Demon renames (2026-09-27).** Plague Fist → Sickness Takes the Flock, Hand of Defilement → Shepherd Opens the Gate, Wasting Claw → Circling Vulture. Oak took Iron Skin (Bark Turns the Blade), Ignore Pain (Oak Sheds Its Leaves), Harmonious Mending (Sap Seals the Wound), Channel Ki (Willow Springs Back). (→ archive RULES_DESIGN, "The three supernatural martial Schools")
- **The cast's pronouns.** Hilde, Browndog, Carrick, Jackal, Sable, Enith and Ashleigh: she/her. Beornhard (an old wizard), Felix and Hanforth: he/him. (2026-10-24, → CLAUDE.md, "Quick reference")
- **Felix is a monk with a little Sorcery.** Abasi the Devil is his dark mirror: a Demon School and shadow-magic glass cannon, a good model for a villain. (2026-09-30, → archive IDEAS_BACKLOG, "Abasi the Devil")

### Open rules questions

- Presence's suit: Hearts now, Clubs argued. Flagged as the least certain call in the suit table.
- How far the Ritual Magic "ally pays your cost" pattern spreads beyond Spells.
- Social Maneuver (T057) and its Features need a redesign for the Pressure system; A Perfectly Good Explanation is unpriced.
- Rules that would unlock more Styles: combat Support (Leader), a Hidden keyword (Scout, Rogue; unaware attacks already skip Shallow Health), flanking, per-element Resists on enemies (the GM guide gives every element the same Resist).
- Elemental Blend (spell element swap): parked for a more interesting idea.
- A steal-an-item-on-a-melee-hit Technique, maybe a Level 5 capstone.
- A spend-Health-for-damage Technique (from Bloodshard Ring), needs a usage cap; a Flamefist Style (Brawl hit unlocks a spell, spell hit unlocks a teleport-to-adjacent).
- Spending-Bleeding abilities not drafted yet (Barbarian Protected, Duelist Harried, a War Magic sibling, Fawn Left to the Wolves as a spend). A Style that cashes in Bleeding is still worth a look; so is "Bleeding creatures fear you."
- Turn-order adjustment: whether it needs a cap.
- Masterwork recipes as collected resources (base recipes widely known; Level 1-3 bundles, Level 4-5 individual finds). The rulebook says special recipes must be found, with no mechanic behind it.
- "Same power, choose your slot" items (Jerkin/Shawl of the Land, Periapt/Armor of Constitutional Integrity): keep or consolidate.
- Which "full night's rest" effects should name a Cycle (Patch Up → Recovery Cycle is the clearest). Convert on touch.
- Artisan's Eye implies an "analyze" flip that doesn't exist; write the check or fix the text.
- Crown of Glory's capstone: party card draw doesn't fit Head.
- Confirm only specific effects clear a Poison (Old Growth Digs Deep's list mustn't include them).
- Goblin Game's Food System doesn't say it replaces base Food and Exhaustion.
- Unported archive ideas: a Destroying Objects rule, a never-lose-it signature item (Legend Binding), card-economy Techniques, downtime Meditation Techniques, more Cooking recipes, the archive's "Variety / Distinct / Obvious / Prune" and "Barrier vs. Justification" design checklists.
- Oak's Physical damage may get a buff; Fleeting's same-turn skip may get re-evaluated.

---

## Balance design

The basics every pricing pass leans on. The long derivations stay in
`design/balance.md` and `design/balance_weights_notes.md`; current
numbers are in `design/balance_weights.csv`. Pointers below say where
the detail lives.

### The value model

- **What balance is for.** Every player gets an equal share of XP, gold and cards to shape the story. Balance keeps those shares equal, and combat is where it presses hardest: each way of spending XP should be about as strong in a fight as any other. Strength is how much harder a fight a party can take for what it spent. (→ RULES_DESIGN.md, "What the game is for, and what balance is for", 2026-10-30)
- **1 value = +1 to a flip.** Everything is priced against that one anchor. It's fixed by Gambling costing 2 for an Extra Success, so an **Extra Success = 2**. Every mechanic (Damage, a Card, Health, AP, Gold, Good Luck, Protected...) has a rate against it. (→ balance.md, "The value-economy model, in short")
- **Target, Value, Net.** Target is what the thing is owed: **Level × 3 per encounter** for a Technique or item. Value is what it delivers. `Net = Value × Rate of Use − Target`. Positive Net reads strong for its Level, negative reads weak. (→ archive/flagonquest_balance_notes_model.md; balance.md, "Every adjustment goes on one side of the ledger")
- **Rate of Use** is a separate judgment per entry: how often it comes up in an encounter (or a day, for daily things). Situational frequency goes there, never into a weight. (→ balance_weights_notes, "Necrotic = 3/stack when it actually resolves")
- **The Baseline those numbers come from.** A 5-round encounter, a party of 4, about 50% hit chance, about 2.25 damage a hit after Resist, about 1.875 hits on each PC an encounter, 2 encounters an adventuring day. Representative stats: Body 3, Agility 3 (Speed 4). (→ balance_weights_notes, "Resist"; "Lifeforce Plate")
- **Two prices for a point of harm.** Damage (2) is a point that still has to hit; it already has the ~50% hit chance in it and is priced before Resist. A point that skips the attack roll (a Bleeding tick, a point stopped by Resist on a hit that landed) prices at Health's rate, 4. Picking the wrong one is the most likely way to mis-score an item. (→ balance_weights_notes, "Locked" (Damage); "Clarification, caught during the Potion buff-cluster pass")
- **Status of a weight.** Locked: derived and checked. Pencil: reasoned fresh, agreed, not battle-tested. Plausible / Unexplained: inherited and unconfirmed. Treat Pencil numbers as revisable. (→ balance_weights_notes, intro "Status key")
- **Masterwork items don't get a clean pass/fail.** They're priced like Techniques of their Level, but read against similar existing items too, not only the Net. (→ balance.md, "The value-economy model, in short")

### Standing pricing rules

- **Every adjustment goes on one side of the ledger. Say which, every time.** Something the player gives up (a Condition, a restriction, a narrow Skill, a Held slot) is **+N to Target**. Something the player gets is Value; a Skill that also pays off elsewhere is **−N to Target**. A cost paid each use (AP, a Card, a Spell charge, Health) comes **off Value**: `Net = Value − cost`. Pick one way of charging a cost, never both. This has gone wrong twice. (→ balance.md, "Every adjustment goes on one side of the ledger")
- **The one-line sign check.** Before writing an adjustment down: does it make the deal better or worse for the player? Worse means the thing has to deliver more, so the Target goes up or the cost comes off Value. If a restriction ever makes something easier to be on rate, the sign is wrong. (→ balance.md, same section; CLAUDE.md, "Label the side and sign")
- **Price a situational Technique at its value when used**, not discounted by how often its situation comes up. A narrow trigger or Condition on an Encounter Technique pays for an extra feature instead of getting a number. The exception: an effect whose payoff is still uncertain after you've used it (Necrotic) does get discounted. (→ balance.md, "Every adjustment goes on one side of the ledger"; balance_weights_notes, "Snake School - Slithering Hands")
- **Check "Discount Baked In" before combining two weights.** If either already carries a hit-chance, realization or frequency discount, don't apply that discount again. Resist's old rate was wrong for exactly this reason. (→ balance_weights_notes, intro; balance_weights.csv's `Discount Baked In` and `Derived From` columns)
- **Two-debuff Techniques: price for one, not both.** A player mostly gets use from one of the two in a given fight. A pair that's hot with both counted is fine if the more useful half is about on rate alone. (→ balance.md, "Two-debuff Techniques: price for one, not both")
- **Triangulate a hard-to-price effect.** Price it through two or more independent framings and take the middle. When several debuffs are bundled into one prevention, average across the plausible ones; don't sum them as if they all land in one fight. (→ balance.md, "Estimating a genuinely hard-to-price effect")
- **Early, late, and Level 5** (2026-10-05). Balance and coverage work in two buckets: early (Levels 1-2) and late (3-4). Level 5 is rare: most of it lives in IDEAS_BACKLOG.md, a character buys at most one late in a campaign (~200+ XP). An empty Level 5 slot isn't missing coverage. (→ balance.md, "Early, late, and Level 5")
- **Skill-Total-scaled Techniques can run a bit hot early.** Enemy Defenses climb while the Technique's Level stays put, so its hit chance and price come down on their own. Don't trim it just to hit 100% at its own Level. (→ balance.md, "Skill-Total-scaled Techniques can run a bit hot early")
- **Moderate synergy, not the maximum combo.** A build that opts into a keyword is assumed to build around it a little. Price a Feature menu assuming the player puts a reasonable few points into one option, not 1 point spread evenly and not a full optimized dump. Working target: about 1.0 Value per Feature point. (→ balance_weights_notes, "The Debuff bucket, broken out"; "Pricing a menu of stacking-debuff Features")
- **Price the rational best choice.** When a player picks between options (Shallow or Deep healing), price the one they'd sensibly take. (→ balance.md, "Passes completed", Hearty Meal)
- **Niche tools should be frictionless** (penciled, 2026-09-28). A Technique's niche job (taking prisoners) is just "you can do this now", no extra flip. Price the rest and treat the niche part as a rounding error. (→ RULES_DESIGN.md, "Niche tools should be frictionless")
- **Reward cleverness and risk, not raw power.** Something may land well outside the Net band when its strength comes from the player's choices or a drawback they accepted. A plain number that's too generous for its Level isn't that. (→ RULES_DESIGN.md, "Reward cleverness and risk, not raw power")
- **No free Extra Successes or flat flip/damage bonuses.** Bonus damage and successes go through Gambling or suit-pool matches. (→ RULES_DESIGN.md, "Damage/success bonuses stay routed through the existing systems")
- **Healing and card draw always cost a resource.** Put a discard or a consumable in the cost, and prefer a fixed payout over a scaling one. Combat healing is usually a mistake (the AP is better spent ending the fight), so healing Techniques are priced for the Wounded or in-danger moment. (→ RULES_DESIGN.md, "Some effects always cost a resource"; balance_weights_notes, "Healer Styles", 2026-10-05)
- **Measure the moment, not only the fight.** For an effect whose payoff sits in one narrow window (a setup, an Interrupt), compare that moment against a matched control. A whole-fight win-rate delta dilutes it into noise. (→ balance_weights_notes, "Measure the moment, not just the aggregate win-rate delta")
- **Gambling checks use the EV-best count.** Don't assume "gamble until it's still likely to hit"; compute the count that maximizes expected value. (→ balance_weights_notes, "A real bug in `pc_gamble_count`")
- **Level 1 can be a bit underpowered.** Accepted where a curve can't be fit at every Level (Fatestealer, 60% at Level 1). (→ balance_weights_notes, "Fatestealer")
- **A niche item doesn't get stretched to a bigger Level.** Drop it to the Level its value earns. (→ balance_weights_notes, "Greaves of the Stalwart Guardian")
- **Check the mechanic exists before drafting against it.** Three Head items got cut for detecting or resisting things (illusions, charm, languages) the ruleset doesn't have. (→ balance_weights_notes, "Third Eye")

### Scoping and resources

- **Rate and Target must share one window.** The default is per encounter (Target = Level × 3). Something naturally once a day is rescoped as a whole: **Rate = 1, Target = Level × 3 × encounters between uses**. With **2 encounters a day**, once/day is **Level × 6**; every other day is Level × 12. Don't also shrink the Rate; that double-counts. (→ balance.md, "The balance ledger", Scoping window)
- **Social encounters come about once a day**, half as often as combat, so a social Technique's per-encounter value only has to match about twice a combat one's (Level 2: 12 a day). The Social Encounter Baseline wins 57%; 1 Social Maneuver Feature point ≈ 6.7 percentage points. (→ balance_weights_notes, "A Perfectly Good Explanation, priced per day"; "Social Encounter Baseline")
- **1 AP = 2.75**, the opportunity cost of not attacking: one attack (5.5) over its 2 AP. A consumable's AP is charged as negative Value. A Potion costs 2 AP to use (draw + drink); a Grenade's 2 AP is its attack, with no separate draw charge. (→ balance.md, "The balance ledger", methodology; balance_weights_notes, "Locked")
- **Three AP treatments for consumables.** Full AP for in-combat use (Grenades). No AP for things meant to be drunk ahead of time (Calming Brew, Kiss of the Earth, Predator's Cry), whose wording also removes existing stacks so they work in an emergency. **Half AP (−2.75 off Value)** for mixed combat/downtime use (Healing Potion). (→ balance.md, "The balance ledger", methodology)
- **No "does the threat show up" discount on consumables.** A Potion costs Gold once and sits in the pack until it matters. The discount still applies to a niche Technique or a Masterwork mechanic, where a permanent investment can go unused. (→ balance.md, "The balance ledger", methodology)
- **Poisons: one setup, one contingency.** Applying a Poison is a one-time out-of-combat action, so no AP per trigger. The weapon hit and the poison's own roll count as one contingency, so no extra ×0.5. (→ balance.md, "Passes completed", Poisons)
- **The refund trick.** "Regain a Technique use" is priced at the refunded Technique's Target (Level × 3) **× 1.5** for choosing when. The AP tax is fixed while Target scales, so the difference between the potion's Level and the refunded Level shrinks from +1 at low Levels to 0 by Level 4. Vigor uses the same math: **4.5 a point**. (→ balance.md, "Passes completed", refund trick; balance_weights_notes, "Vigor = 4.5/point")
- **Technique value = 3 per Level** an encounter (6 per Level for a once-a-day Technique). Use it whenever an item or effect borrows, refreshes or refunds a Technique. A working assumption, labeled as one. (→ balance_weights_notes, "Focusing Band of [Technique]")
- **Cost-to-use is the lever on borrowed Techniques.** When an item's borrowed Technique cancels against its Target, its activation cost (a Card, −2.7 off Value) is the whole balance. Focusing Band lands at a flat Net −2.7 by design. (→ balance_weights_notes, "Focusing Band of [Technique]")
- **Use-it-or-lose-it locks** stop deck-stacking for the next day (Choker of Defiance locks until the next night's Discard Cycle). (→ balance_weights_notes, "Choker of Defiance")

### Core weights

Current values from `design/balance_weights.csv`. **Locked** rows:

| Mechanic | Value | Note |
|---|---|---|
| Fudge Value / Accuracy / Defense | 1 | the anchor |
| Extra Success | 2 | fixed by Gambling |
| Damage (hit-gated) | 2 | before Resist |
| Health (guaranteed harm) | 4 | Damage ÷ 0.5 |
| Gold | 1.5 | Baseline's Value/Gold ratio |
| Autoswing (a granted attack) | 5.5 | one attack + its Harried |
| 1 AP | 2.75 | Autoswing ÷ 2 |
| Protected | 3 | Health × ~75-84% realized |
| Max Shallow / Deep Health | 5 / 4 a point | Shallow is easier to top up |
| Heal Shallow / Deep | 4 / 5 a point | Deep is scarcer; opposite of the pool row |

**Main Pencil rows**, with the sim-measured cells (one stack each):

| Mechanic | Value | Weak | Average | Strong |
|---|---|---|---|---|
| Good Luck | 2.4 | 1.4 | 1.9 | 2.2 |
| Card (drawn/hand) | 2.7 | | | |
| Bad Luck / Pressure | 2.2 | 0.55 | 2.3 | 5.7 |
| Turn order, a place | 1.35 | 1.1 | 1.2 | 2.7 |
| Harried | 1 a stack, cap 6 | 1.25 | 2.8 | 3.9 |
| Crippled | 1.5 a stack, compounding, cap 42 | 0.34 | 1.1 | 2.4 |
| Vulnerable | 1 a stack, compounding, cap 24 | 1.4 | 2.4 | 4.0 |
| Slowed | 1.1 a stack, compounding, cap 17.6 | 0.35 | 1.1 | 3.7 |
| Hasted | 0.55 a stack, rising toward 2.2 | −0.4 | 0.08 | 0.9 |
| Taunted (from the tank) | 2.2 a stack, linear | 0.6 | 6.5 | 7.6 |
| Frightened | 2.2 a stack, linear | −0.16 | 0.6 | 2.0 |
| Bleeding | 4 a stack, tapered, cap ~12 | 0.8 | 2.4 | 5.1 |
| Necrotic | 3 when it resolves | 0 | 0.02 | 3.2 |
| Protected (measured) | 3 | −0.3 | 1.1 | 4.4 |
| Push, a meter | 0.89 | −0.8 | 0 | 2.6 |
| Speed, permanent, a point | 2.54 | −0.3 | 0.15 | 0.4 |
| Physical Resist, a point | 5.0 | 0.9 | 1.75 | 2.3 |
| Fire / other elemental Resist | 1.0 / 0.5 | | | |
| Ward (Fire / other), flat part | 0.72-2.0 / 0.36-1.0, plus 2.0 a stack absorbed | 0 | 1.1 / 0.7 | 8.1 / 4.0 |
| Speed or Range, one-shot | 0.55 a meter | | | |
| Range, permanent | 3.44 a meter | | | |
| Sift (daily) / Hand Filtering | 0.60 / 1.66 a card | | | |
| Difficult Terrain, degrees 1 / 2+ | 2.75 / 8.25 | | | |
| Vigor | 4.5 a point | | | |

- **Which column to use** (2026-10-22). Delivery decides most of it. A rider that lands on whatever you hit: **Weak**. Control the player aims, or a rider they can hold for the right target: **Average**. **Strong is a ceiling, not a price**; a boss-only Technique priced at its value when used lands between Average and Strong. Value hasn't been switched to these yet; that's the designer's call. (→ balance.md, "Weak, Average and Strong: which number to use")
- **Check the carrier.** Taunted's cells are the tank's; from a fragile PC it can cost the party (Sable's aimed Taunt loses about 7 a fight). Protected and Physical Resist are worth little on a PC enemies leave alone. (→ balance.md, same section; balance_weights_notes, "Weak, Average and Strong, re-measured (2026-10-29)")
- **Extra stacks only pay on a target that lives.** Riding a hit, four stacks are worth four to five times one for Crippled, Slowed and Vulnerable, less for the rest. Rate of Use still goes on top of every column. (→ balance.md, same section)
- **Offense cells are scaled to THE TABEL's footing**: ×2.6 for Harried and Vulnerable, ×2.5 for Bleeding and Necrotic, because the sample characters out-damage the Baseline. Re-measure the cells (`tools/effect_check.py`) when the sim's effects or the sample party change. (→ balance.md, same section; balance_weights_notes, "Weak, Average and Strong, re-measured (2026-10-29)")
- **Two attack rates.** **1.25 attacks a turn** (6.25 an encounter, ~3.75 hits) for an always-on effect riding the wielder's own attacks. **1.5 a turn** for an aggressive or tank-style combatant who takes or makes more hits. (→ balance_weights_notes, "Attacks/turn split into two baselines")
- **Tank multiplier.** An item for a wearer who draws more attacks gets its hit-count term scaled (×1.5 is the example, not a constant). Check armor-like items under both the generic and the tank lens. (→ balance_weights.csv, "Tank / above-average attack draw")

### Effects and keywords

- **Bleeding is Health loss over time** (standing rule, reworked 2026-10-19). Rare and strong as a main tool, otherwise small add-ons. Half the stacks, rounded up, come off each time it decays, 1 Health each. Protected stops a tick. Leftover stacks keep ticking after the fight. Never as good as the same straight damage. (→ RULES_DESIGN.md, "Bleeding is Health loss over time"; balance_weights_notes, "Bleeding's worth under the new rule")
- **Bleeding's price is pending.** The CSV still says 4 a stack, tapered. The measured proposal for Bleeding on an enemy, at table toughness: about **1.8 for the first stack, 0.8 for each after**, about 8 a fight for a stack on every hit. On a PC: about 0.9 Health a stack (4 Value a stack still fits for items that prevent it). Cash-outs that spend stacks stay rare (2026-10-17). (→ balance_weights_notes, "Bleeding's value under half ticks, and spending it")
- **Harried: 1 a stack, linear, cap 6.** It clears at the end of the bearer's turn, so more stacks buy depth, not time; the window is about one follow-up attack. Any attack against Dodge or Parry gives one Harried, hit or miss (+1 credit on a fresh attack). Harried alone can't carry an item's budget. (→ balance_weights_notes, "Harried = 1/stack")
- **Crippled, Vulnerable, Slowed compound** over a 4-turn window up to a cap where the mechanic stops caring (Crippled 7 stacks zeroes hit chance; Vulnerable 6 saturates it; Slowed 4 zeroes Speed 4). Slowed's base is doubled to 1.1 because a Slowed creature needs to move twice a turn. (→ balance_weights_notes, "Crippled", "Vulnerable", "Hasted / Slowed")
- **Taunted and Frightened: 2.2 a stack, linear.** Stacks buy duration only. Bad Luck is the escape hatch, so 2.2 is a ceiling. Taunted funnels the whole field onto the tank and usually realizes it; Frightened only protects one relationship and often doesn't. (→ balance_weights_notes, "Taunted / Frightened")
- **Necrotic: 3 when it resolves**, no stacking curve. How often it resolves goes in Rate of Use. If a Necrotic item reads low, the designer's fix is more enemy healers and Protected users, not a bigger weight. (→ balance_weights_notes, "Necrotic")
- **Protected banks.** A hit uses only as many stacks as the Health it would lose; it works on any Health loss. 3 a stack assumes the carrier takes more hits than average. (→ balance_weights_notes, "Locked" (Protected))
- **Ward = flat +2 Resist while any stacks last, plus each stack absorbs 1 Health loss of its type** (2.0 a stack). Raising the flat bonus was ruled out: it risks immunity to a whole damage type. Ward that lasts an hour prices at the full flat rate with no decay. (→ balance_weights_notes, "Correction: Ward reimagined as flat Resist + a self-limiting absorption charge")
- **Resist differs by damage type**: Physical 2/3 of all damage, Fire 2/15, each other element 1/15. Physical Resist 5.0, Fire 1.0, others 0.5 a point. Base weapon and armor Resist is designed to fit the assumptions and isn't run through this. (→ balance_weights_notes, "Resist")
- **Hasted** converges toward 2.2 a stack with no cap (no target death to cut it short). Measured, it's backward: early stacks are worth more, big stacks little. (→ balance_weights_notes, "Hasted / Slowed"; "Every buff and debuff in the sim")
- **Push: 0.89 a meter** (1 AP over a 4-meter move, +30% for the tactics). Only worth its price when the player picks when to push. (→ balance_weights_notes, "Push decoupled from Speed")
- **Speed and Range.** One-shot movement or Range: 0.55 a meter. Permanent Speed: 2.54 a point (moves an encounter). Permanent Range: 3.44 a meter (attacks an encounter). A weapon's own inherent Range uses its own curve (base weapons, below). (→ balance_weights_notes, "Speed (permanently-worn)"; "Reaching Weapon"; balance_weights.csv Range rows)
- **Cover is priced as the cost of avoiding it.** Heavy Cover's Bad Luck twice (3.29) is a ceiling; a rational target relocates instead, so use the relocation cost in AP (Smokejar: 2 moves, 5.5). (→ balance_weights_notes, "Cover")
- **AoE = 2 enemies hit × 0.8 = 1.6×.** Applies to the AoE part of Value only (damage margin, debuffs, the Harried credit), never to Autoswing. A shaped debuff curve doubles as `curve(N) × 2`, not `curve(2N)`. (→ balance_weights_notes, "AoE multiplier"; "Correction: curves need curve(N) × 2")
- **Pricing a fresh attack from scratch** (Grenades, spells): subtract a Resist placeholder (4 Physical, 3 elemental) from raw Damage, price the margin at 2 a point, add +1 Harried, subtract Autoswing (5.5) as the cost of not just attacking. The placeholder is closer to a Bruiser than a generic enemy; check it against the enemy model. (→ balance_weights_notes, "Pricing a fresh attack from scratch"; "Flamebinder's Promise, follow-up")
- **Immunity wording.** "Cannot gain stacks of X" for a stacking debuff; "ignores the effects of X" for a non-stacking one; "ignore the first N stacks of X you would gain" for count-limited prevention. (→ balance_weights_notes, "Immunity/prevention wording standardized")
- **Price immunity to Taunted/Frightened at the intended enemy rate** (about 1-2 stacks an encounter, ~3), not today's lower one: enemies are meant to threaten through debuffs, not bigger numbers (2026-09-28). (→ balance.md, "Open balance work")

### Techniques and Styles

- **Style Target = Level × 3.6** an encounter (2026-09-29). The ×1.2 is **+Target**: you can only be in one Style, and it keeps a second Style worth the XP. Always-on effects riding your attacks use 6.25 attacks an encounter. School Styles land around 105-120%, a bit extra for being School Styles. (→ balance.md, "Styles: Level × 3.6 per encounter"; balance_weights_notes, "Dual-wield allowance corrected to 2.2")
- **Empty off-hand: +4.5 to Target** (2026-09-30). Giving up a shield's +2 Parry is ~8.9 an encounter; the designer halved it. **Dual-wielding: +2.2 to Target** (gives up 1 Parry). Landing a little under on these is about right. (→ balance.md, "Empty off-hand: half a shield's worth")
- **Unarmored Condition: +0.8 to Target** (Encounter Technique), **+4.0** (Style). Light Armor's +1 Physical Resist, ×0.8 because an unarmored monk draws fewer hits. (→ balance_weights.csv, "Unarmored Condition premium")
- **Count the Condition on every attack.** A dual-wield Style's attacks are one-hander attacks, about a point of damage under a two-hander. (→ balance.md, "Effects that use other Techniques")
- **Effects that copy or boost Techniques: price off a Level 2 Technique**, not the Style's Level. Players rush a defining Style, so most of the game it works with Level 2 and smaller Techniques (2026-10-02). (→ balance.md, "Effects that use other Techniques")
- **Repeat pricing** (corrected 2026-10-06). A Level 2 attack Technique's effects are worth its AP plus its Level budget: 5.5 + 6 = 11.5. A 1 AP Repeat of it nets 8.75; a plain attack's Repeat nets 2.75. Copying a Technique is worth about three times a plain copy. (→ balance.md, same section; balance_weights_notes, "Repeat pricing corrected")
- **Avoid once-per-round triggers.** At 1.25 attacks a turn the cap rarely binds (~3.5 triggers against 3.75). Trim the per-trigger effect instead. Keep a cap only when uncapped breaks (Storm of Blades, Inexhaustible Guardian), and say why. (→ balance_weights_notes, "Lawman's Hand (T128) — uncapped"; CLAUDE.md)
- **Spellblade is a flexibility tool**, not an Encounter Technique. Each option lands about **+2 Net** over trading the Spell's charge. Slowed runs cold at high X by its own cap; accepted. (→ balance_weights_notes, "Spellblade")
- **Integer coefficients only.** A scaling formula reads clean (`[2×X]`, `X+1`), even if options drift a bit at extreme X. An additive shape (`X+1+[Suit]`) beats a multiplier on a steep curve. (→ balance_weights_notes, "Spellblade", second correction)
- **Which Schools scale on what.** Snake and Bear scale on **Brawl**; their secondary Skill (Acrobatics, Might) is only a Prereq. Demon, Shugen and Great Old Oak are supernatural and scale on **Meditation**. (→ balance_weights_notes, "Which Schools scale on what (designer's rule)")
- **Suit riders match the debuff's suit**: Hearts for Frightened/Taunted, Clubs for Bleeding/Crippled, Diamonds for Harried/Vulnerable/Necrotic, Spades for Slowed/Push. Each suit rider is worth 0.25 stacks expected. Check new content against the Suit portfolio table. (→ balance_weights_notes, "Suit riders and Extra Success Bleeding"; RULES_DESIGN.md Suit portfolio)
- **Vital and Mental attacks** are priced assuming an enemy's Vital is 1-2 below its Dodge/Parry. The roster doesn't match yet (see Open questions). (→ balance.md, "Open balance work")
- **Card Techniques: net out the Card.** When a Technique spends a card, subtract 2.7 from what the sim measures. (→ balance_weights_notes, "Perfect Strike")
- **Interrupt and Encounter Techniques in the sim** need both the AP check and the once-per-fight check before their numbers mean anything. (→ balance_weights_notes, "Magehunter")

### Items

- **Masterwork items are priced like a same-Level consumable used about 12 times.** Price is 20 × Level Gold. If an item doesn't look like it'd get used ~12 times over its span, its Level or effect needs a look. (→ balance.md, "Historical Masterwork/magic-item pricing logic")
- **Masterwork items can run a bit hot**, since you can only equip one per slot. Robes get a further bump for giving up armor. (→ balance.md, "Torso Masterwork pass")
- **Resist items are accepted below Target.** Each blunts 10-25% of a same-Level hit (War Magic's damage as the yardstick), which the Net doesn't show. Don't inflate flat Resist; that risks immunity. A chosen-element pick is a bet the player commits to. (→ balance.md, "Torso Masterwork pass"; "Reference: War Magic damage baseline")
- **Slots have design lanes**: Head mental/vision; Hands what your hands can do (no direct-combat items); Feet mobility; Belt carrying; Torso protection and healing; Held weapons and active items; Neck niche passive utility; Ring an active ability or a skill augment. (→ RULES_DESIGN.md, "Equipment slots each have an intended design lane")
- **Every Masterwork item ties to an existing Base Item Option** (Ring `I003`; Neck `I002,I003`), with flavor materials on top. (→ balance.md, Dryad's Mantle follow-up; balance_weights_notes, "Dryad's Mantle")
- **Where new Masterwork content goes**: Level 1-3 variety in Held, Torso, Ring and Neck. Level 4-5 completionism isn't the goal, and not every slot needs thematic range. (→ balance.md, "Material Type and Masterwork Slot × Level coverage"; RULES_DESIGN.md)
- **Trigger frequency tiers: 1, ½, ⅓.** Every encounter (no discount), about once a day, rarer than daily. No finer steps. An item underpowered at ⅓ needs a redesign, not a finer discount. (→ balance_weights_notes, "Trigger frequency tiers, standardized")
- **Narrative Utility items: Value = ⅓ × Target.** A labeled guess for exploration or puzzle effects the model can't price. Say so in the item's note. (→ same section)
- **Storage items** price the AP saved on at most 3 extra slots used (2.75), plus 0.917 a slot for a qualitative extra like large objects. Differentiate similar Storage items by Level, not more pouches. (→ balance_weights_notes, "Storage capacity")
- **Base weapons are un-Leveled.** Raw budget = Accuracy (1) + Damage (2) + Weapon Defense (1). Target = 8, **+2 to Target** Archery (feeds nothing else), **−2** Acrobatics (feeds Dodge), **−1** Brawl, **+2** two-handed (the Held slot, anchored to a Shield's +2 Parry). Accuracy caps at +1 except Unarmed's +2. Reload firearms take ×0.8 on Accuracy and Damage. (→ balance.md, "Baseline Weapons pass"; balance_weights_notes, "Baseline Weapons pass")
- **Thrown weapons stay generous**: a flexible backup for non-combat archetypes. They're an abstracted supply recovered after the fight, so no "return to hand" items. (→ balance.md, "Baseline Weapons pass"; "Held Masterwork pass")
- **Armor tiers: no tier better than another for the same build.** Light 1 Resist / Medium 2 (Dodge −1) / Heavy 3 (Dodge −1, Speed −1). Check both the generic and tank lens. Gold stays cheap (4/6/8) and isn't a lever. (→ balance.md, "Baseline Armor pass")
- **Heavy Armor isn't reachable at creation.** Might Requirement 7 is one past the creation ceiling of 6; it opens after one rank-up. Medium's 5 takes more than a token investment. (→ balance.md, "Baseline Armor pass", follow-up)
- **Poisons get a wider berth, and the low end matters more.** All seven flavors are worth the same (same craft cost). When a clean integer Potency can't hit Target, lean stronger at low Level. (→ balance.md, "Passes completed", Poisons; balance_weights_notes, "Venomous Weapon")
- **Duplicates get cut, not repriced.** A smaller copy of an existing item is removed, with its effect kept in the slot whose lane fits. (→ balance.md, "Torso Masterwork pass")

### Crafting and goods

- **Everyday goods use fixed tiers**, not the value model: Tier 1 consumables 1 Gold; Tier 2 basic permanent gear 2-3; Tier 3a niche mechanical 3, 3b mainstream kits 5; Tier 4 storage +3 per capacity step; Tier 5 vehicles roughly doubling. Check a "basic consumable" for a hidden mechanical role (Medicinal Supply, 2 Gold). (→ balance.md, "Reference: Everyday-goods pricing tiers")
- **Crafting Skill Total curve: 4 / 6 / 8 / 9 / 10 by Level** for Masterwork and Progression Alchemy/Cooking items. Skill Total caps at 10; the curve passes Level 3's 8. Convenience goods sit flat at Mixology 3. (→ balance.md, "Crafting Skill Total tiers, broadly")
- **Recipe tiers**: 3 basic gear, 4 weapons and kits, 5 Medium Armor, 6 Survivalist's Pack, 7 Heavy Armor and Wagon (one step past the creation cap of 6). (→ balance.md, same section)
- **A School's payoff is crafting instead of vendoring loot.** Vendors pay 50-75% of a material's value; crafting keeps all of it, 25-50% recovered at every tier. Whether a School pays off depends on how much material loot the GM hands out. (→ balance.md, "Crafting Schools' XP cost vs. payoff")
- **Food: only the first special-effect meal each day counts.** Food is start-of-day prep, priced once/day (Level × 6). (→ balance.md, "Passes completed", Food)

### Measuring with the simulator

- **The sim checks the model; THE TABEL still prices.** Weak/Average/Strong are per application, measured at table toughness (enemy Health ×1.75, where a hit enemy acts again about half the time) in the Level 1 Party A. (→ balance_weights_notes, "Weak, Average and Strong (2026-10-22)")
- **Score in points of Health, not percent.** The old percent score inflated tests about 2.7-6 times. Check the unit before quoting a number. (→ balance_weights_notes, "A scoring fix first")
- **The day standard**: days run at enemy Health ×1.0. Healing is worth far more by the day than in one fight. (→ enemy_sim/TABLE_PLAY_NOTES.md, "The day standard")
- **Strength is the toughest fight or day a party still wins half the time**, per XP spent. Health-left scores credit a bigger pool just for being bigger. (→ enemy_sim/TABLE_PLAY_NOTES.md, "Two kinds of measure")
- **XP the designer quotes is composite.** A sim party plays at its combat share (0.8 × composite + 5). (→ CLAUDE.md, "XP the designer quotes is composite")

### Open balance questions

- **Switch Value to the Average column?** The designer's call. Until then Value is still the priced number. (→ balance_weights_notes, "Weak, Average and Strong")
- **Bleeding's reprice** (1.8 first stack, 0.8 after) isn't applied to the CSV. (→ balance_weights_notes, "Bleeding's value under half ticks")
- **The offense baseline mismatch.** The sample characters out-damage the Baseline about 2.4 times, so offense measures at about half. Either the baseline moves or the characters do. (→ balance_weights_notes, "Every buff and debuff in the sim", "The biggest misses")
- **The 10-21 per-effect proposals** (Crippled 0.5 flat, Push about 0.6 a first meter, Hasted 0.8 then 0.7...) are pending. Speed (permanent) measured at 0.86 is flagged as a floor. (→ balance_weights_notes, "Proposed (pending the designer)")
- **Vital below Dodge/Parry.** Enemy stat blocks should run Dodge/Parry 1 above the other Defenses, with a way to pump one Defense at a cost (2026-09-27). Not in the roster yet. (→ balance.md, "Open balance work")
- **Gambling is weapon-only for damage**, and the sim still lets casters Gamble. How big the edge is, and whether Discipline attacks count, is open. (→ balance.md, "Open balance work")
- **War Magic's 2 + [Mind] against rising Resist** likely prices under Target past Level 2 for most casters. (→ balance.md, "Open balance work")
- **Resist items as a group** read below Target. Decide on group buffs or Level cuts, maybe with the armor pass's two lenses. (→ balance.md, "Open balance work", Resist-granting items)
- **Bad Luck and Card don't credit the Suit Pool yet.** Bad Luck should drop a little (the target's suit pool grows); Card's floor likely rises to ~2.9. (→ balance_weights_notes, "Correction: Good Luck = 2.4")
- **Turn-order Style Levels** set on 10-06 came from the old score; Seize the Moment reads like a Level 1 again. (→ balance_weights_notes, "Turn order and the Styles, re-measured")
- **Sift outside a daily window** needs its own simulation; 0.60 is daily only. (→ balance_weights_notes, "What's still open")
- **Optional: a School perk** beyond crafting access, so its XP pays from day one. Not pursued. (→ balance.md, "Crafting Schools' XP cost vs. payoff")

---

## Enemies and encounters

### First principles (designer, 2026-11-03)

These come first. Where a balance target clashes with them, they win, and the balance gets found inside them.

- **Enemies play by the players' rules.** Same Stats, Skill Totals and Defenses (Defense = 8 + Skill Total), same weapons and armor from the player tables, Parry from the weapon Skill plus the weapon's Defense, Resist from a Stat plus armor. Only two things get sanded off to keep combat quick: no per-encounter abilities to track, and simple fixed tactics. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **What you see is what it does.** A big two-hander doesn't parry well; sword and board in heavy armor doesn't dodge well. The mechanics should bear out what the party can see. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **Numbers stay in the players' ballpark.** A damage Stat starts around 2 and climbs to 4; an archetype can push it to the player cap of 5. Accuracy and Defenses run up to the players' +10. Health sits near a PC's. No stat goes past what a player could have. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **A goblin shouldn't have more Health than the PC fighting it.** It breaks the sense that the world hangs together, and players read stat blocks by the same yardstick as their own sheet. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **Legible.** Players size an enemy up from what it visibly is (armor, weapon, a wizard's staff) and get rewarded for acting on it. The five Defenses have a spread, so a weak Mental Defense on a brute is worth finding. (→ ENEMY_ENCOUNTER_DESIGN, "First principles"; "Defense tiering")
- **A canvas, not the painting.** Stat blocks and tactics are simple and laid out from the start: an archetype, a main Action, a passive or a tweak to that Action, at most one support enemy that spends most turns healing or shielding. The party's Techniques make a fight interesting; the enemy gives them something to work on. A tough bruiser that gains Protected every turn is enough. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **Engaging, not a slog.** Enemies aren't bags of Health. Leaning a little more dangerous and a little less durable, with spikier fights, is fine: parties build to support each other and carry consumables for the bad fight. (→ ENEMY_ENCOUNTER_DESIGN, "First principles")
- **Enemies are simple on purpose.** Their job is to put the players in a bind so their builds get to shine, not to give the GM lots of tools. Just complicated enough to make the players' builds fun. (designer, 2026-10-07) (→ enemy_sim/TABLE_PLAY_NOTES, "Enemies")
- **Break the melee-clash default.** The original spreadsheet's goal: mechanically separate enemies whose strengths and weaknesses are intuitive from the fiction, so combat doesn't boil down to melee characters double attacking until one tips over. Today that job falls to archetypes, Defense spreads, attack types and riders; the Fighting Styles that first carried it are off. (→ ENEMY_ENCOUNTER_DESIGN, "Design goals, in the designer's own words")

### Building an enemy (the current model: v3)

- **Enemy building has to work on paper** (designer, 2026-11-04). The game is meant to be a book like any tabletop game, so building an enemy should be a short series of "pick from this list" steps, penciled in and tallied at the end: Level, archetype, loadout and armor, Strong and Weak Defense, then spend the Ability budget. Once the numbers are settled, simplify the builder back down to that. A monster manual of varied stat blocks is the test. (→ ENEMY_ENCOUNTER_DESIGN, "Building an enemy on paper")

v3 is the model (2026-11-03; the designer called it far and away the best configuration, then adopted it the same day with the base trimmed and the archetypes bigger). On 2026-11-04 the designer made the pruned v3 the default (`tunables.V3_VERSION = 3`: a thin base, additive archetypes, loadouts and a 6 / 7 / 9 / 9 / 9 Ability budget; see "Pruned v3" below). v2, the first v3 and v3 as adopted on 11-03 stay behind switches for the numbers recorded under them.

- **v3 goes back to the original spreadsheet's shape.** Its Design sheet priced enemy stats in player XP and landed on the player schedule; its Roles were plain bumps. v1 and v2 drifted (big Health, low Resist, damage under the player formula, Accuracy trades) chasing fight length after the fact. (2026-11-03) (→ ENEMY_ENCOUNTER_DESIGN, "v3: enemies built the way PCs are")
- **Skill** is the weapon Skill Total. With a melee weapon in hand, Parry = 8 + Skill + the weapon's Defense. Casters and archers can't Parry; a support with a backup mace Parries at its Weak tier. (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Defenses: one Strong, one Weak, the rest Average.** Strong = 8 + Skill. Weak = Strong − 4, by default what that kind of enemy visibly neglects (a fighter's Mental, a caster's Vital, a support's Dodge). Average = Strong − 2. Armor moves Dodge as for a PC. A step of 2 keeps the spread legible; 1 played about the same. (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Accuracy** is a Skill Total one under Skill, plus the weapon's or spell's own Accuracy (+1 light weapons, +0 heavy weapons and spells). Archetypes that attack well raise it back. (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **The base is a little under a PC's, and the archetype makes up the rest** (designer, 2026-11-03: "trim back a slight bit of the baseline stat block and add that power budget into the archetypes" so enemies feel distinct). The trim was 1 Skill and 1 Accuracy at every Level. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted")
- **Damage** is the player weapon and spell table (light 3, one-handed heavy 4, two-handed heavy 5, spells 2) plus the damage Stat. **Resist** is the Resist Stat plus armor (Light +1, Medium +2, Heavy +3 Physical). (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Caps are the player caps:** Stats 5, Skill Totals 10. (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Each stat steps up at its own Levels,** so two don't jump at once. The designer's damage Stat schedule, 2 / 3 / 3 / 4 / 4, held at every Level once base Accuracy sat one under Skill. (→ ENEMY_ENCOUNTER_DESIGN, "v3", "How the schedule was found")

The v3 table (Defenses as 8 + Skill Total):

| Level | Skill (Parry, Strong) | Accuracy | Defense S / A / W | Damage Stat | Resist Stat | Health per Slot (minion) | Speed | Reflex |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 3 | 12 / 10 / 8 | 2 | 2 | 10 (4) | 3 | 3 |
| 2 | 5 | 4 | 13 / 11 / 9 | 3 | 3 | 11 (4) | 3 | 4 |
| 3 | 6 | 5 | 14 / 12 / 10 | 3 | 3 | 13 (5) | 4 | 5 |
| 4 | 7 | 6 | 15 / 13 / 11 | 4 | 4 | 15 (5) | 4 | 6 |
| 5 | 8 | 7 | 16 / 14 / 12 | 4 | 4 | 15 (5) | 5 | 7 |

Before archetype and armor: a light-weapon fighter hits at +4 for 5 with Parry 13 at Level 1, +8 for 7 with Parry 17 at Level 5. A two-handed heavy weapon hits for 2 more at 1 less Accuracy and adds no weapon Defense to Parry. A caster hits at +3 / +7 for 4 / 6, can't Parry, and has the Weak Vital Defense.

**The six archetypes (v3), bumps capped at the player maximums** (worth in enemy Health per Slot at Levels 2 / 3):

- **Defender:** Resist +1, Parry +2, Dodge +2. 3.6 / 2.8. Adds about two rounds.
- **Striker:** Damage +1, Accuracy +2, Resist −1. 2.8 / 4.4. Pays by being lightly built; spikier fights, a quarter-round shorter.
- **Bruiser:** Damage +1, Resist +1, Vital +2, Parry −1, Dodge −1, Speed −1. 2.9 / 3.5. Pays by being heavy and slow; a hard body to poison.
- **Strategist:** Accuracy +3, Dodge +1, Mental +2, Vigilant +2. 2.5 / 3.6.
- **Skirmisher:** Accuracy +2, Dodge +2, Speed +2. 2.4 / 3.3.
- **Backup:** Resist +1, Parry +1, Dodge +2, Vital +2, Mental +2. 3.1 / 2.5. Adds one and a half to two rounds.

(→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted"; `enemy_builder_pcstyle.ROLE_ADDS_V3`)

- **No archetype pays Accuracy for Damage under v3.** Enemy hits now get well past the party's Resist, so +1 Damage is worth about two and a half Accuracy (under v2 it was worth eight, which forced Accuracy trades). Each archetype reads about 2.5-4.5 enemy Health per Slot. (2026-11-03) (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Every archetype should be a distinct shape and a fair trade.** The designer flagged Bruiser as strictly worse than Striker on 11-02; it's been the tough, clumsy hitter since. (→ ENEMY_ENCOUNTER_DESIGN, "Archetypes and what enemy damage is worth")
- **What a +1 is worth to an enemy (v3, roughly):** Damage 2-3 Health; Resist about 1.4 and most of a round; Accuracy about 1; Parry or Dodge 0.1-0.2 (an enemy defends with the better of the two); Vital or Mental nothing against the sample parties, who rarely target them. (→ ENEMY_ENCOUNTER_DESIGN, "v3")
- **Pruned v3 armor and the Defender (2026-11-05):** armor costs −2 / 0 / 2 / 4 (Unarmored / Light / Medium / Heavy), about 2 Health a step as measured. The Defender's Resist +1 became Health +3 per Slot: on Heavy Armor the Resist made walls physical weapons barely hurt, and Health +3 is priced like the other archetypes. Together they bring the walls back among the ordinary threats. (→ ENEMY_ENCOUNTER_DESIGN, "What armor is worth on the pruned base"; "The Defender's Resist +1 swapped for Health")
- **Bruiser is Resist +1 and Vital +2, not Resist +2.** Resist +2 read 7-9 Health and two extra rounds, twice any other archetype (2026-11-03). (→ enemy_sim/results/enemy_stats/v3_bigroles_bruiser.txt)

- **The monster manual** (2026-11-05): 30 stat blocks covering every archetype, loadout, main Action and most of the catalog. After the designer's review, Hexes land a stack fewer (2 / 2 / 3 / 3 / 4) with 2 points back, and a Poison effect stops at 2 picks since poisons outlast the fight. In a broad test (40 encounters a Level by the encounter rules, every test party) it plays close to the four mixes the table was tuned on. (→ enemy_sim/MONSTER_MANUAL.md; ENEMY_ENCOUNTER_DESIGN, "The monster manual in fights")
- **What the manual taught:** the two heavy walls are the strongest monsters by a distance, mostly from Physical Resist 7 at Level 3 (Heavy Armor plus the Defender's +1, above any PC's 4-5) on a shield Defender's Parry, not from Defense picks (without any, monsters sit 1-2 under the average PC's Defenses with the ranges overlapping); ranged Assassins with Vulnerable spike Downs; Kiting makes an enemy nearly harmless as the sim plays it (Down 0% against 30% for the same monster as an Assassin); healers and hexers trade Downs for longer fights, and the trimmed hexers now do little. Each wants a call before the wide PC-against-enemy test. (→ ENEMY_ENCOUNTER_DESIGN, "The monster manual in fights")

- **Battle Tactics pick a target, nothing more** (designer, 2026-11-05: none of them should conflict with good tactics like attacking twice; they're a quick reference so GMs can run the game smoothly). Hit Whatever: the closest PC. Hold the Line: whoever has hurt its side most this fight. Vanguard: whoever has hurt its back line most this fight. Kiting: the closest, stepping back first only if a PC is in melee reach (ranged enemies only). Assassin: the softest PC. Assassin is the deadliest by far (two to five times Hit Whatever's Downs alone, about double beside other attackers); Hold the Line and Vanguard play close to Hit Whatever; Kiting as first coded (stepping away every turn) made any monster nearly harmless. (→ ENEMY_ENCOUNTER_DESIGN, "Battle Tactics in the sim", GM quick reference)

- **Hexers add next to nothing as built** (2026-11-05). A hexer in place of a fourth Brute takes Downs from 15% to 2-4%, whatever its effect, its stack count, or even a curse that lasts the fight and spreads to nearby PCs; the same budget as a caster whose damaging spell Cripples plays like an attacker. Options for its job: debuff casters instead of Hexes; hexers as half-Slot spice; or a stronger Hex (new rules). For the designer. (→ ENEMY_ENCOUNTER_DESIGN, "What a hexer is for")

### Encounters and Slots

- **Slots stay as they are: count the players, pick enemies adding to that many Slots** (designer, 2026-11-02). If on-level fights are off, the per-Level baseline moves, not the Slot rule. (→ ENEMY_ENCOUNTER_DESIGN, "Base stats against the measured party")
- **Slot sizes: 0.5 (minion), 1 (standard), 2 (elite).** 2 Slots is the usual ceiling. A 4-Slot solo boss (nine times a standard enemy's Health and Upgrades, two turns a round) is a rare exception that hasn't come up in the designer's games. (2026-10-07) (→ ENEMY_ENCOUNTER_DESIGN, "Enemy Level and Encounter Slots")
- **A minion has a third of the Health, rounded up; a 2-Slot elite three times.** Not half and double: two minions get two turns for one Slot, an elite one turn for two. The designer's range was a third to a half; a half made minion versions of normal enemies far too strong, so it went back to a third (2026-10-01). Under v2 a minion's Upgrades follow the same third, rounded down. (→ ENEMY_ENCOUNTER_DESIGN, "Horde and the minion Health ratio"; "v3")
- **How the designer builds a fight** (2026-09-30): usually two stat blocks, three for a complicated one, rarely four. Enemy groups stay simpler than the party. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **At most one enemy that doesn't attack** (a healer or a debuffer). Two or more made the old Chapel mix drag, since fewer enemies push damage. (2026-09-30) (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **Give each stat block a job.** A basic fight: bruisers that Slow on a hit to bog down the front line, plus a damage caster at the back throwing spells at Vital. A complicated one: minions plus a damage caster and a debuffer. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **Difficulty is mostly managed with more enemies or a more complicated battlefield** (designer, 2026-10-08), on top of the Level match. (→ enemy_sim/TABLE_PLAY_NOTES, "Third round: Level 1")
- **Shield Wall stays as a counter-fight** (designer, 2026-10-01). Armored Defenders plus archers are hard on an all-weapon party (40% at Level 2) and fine for any party with elemental damage (72-89%). A fight that counters a lopsided party encourages variety; don't tune around it. Cover it in the sim by modeling weapon-based elemental options, not by softening the mix. (→ ENEMY_ENCOUNTER_DESIGN, "Horde and the minion Health ratio", Shield Wall paragraph)
- **Minions work best as front-line fodder.** Melee minions are about even with the enemy they replace; a pack of minion archers or casters is much harder (halving a shooter's Health matters less than doubling its shots). (→ ENEMY_ENCOUNTER_DESIGN, "Horde and the minion Health ratio")
- **The sim's standard mixes:** Frontline (2 Brutes + 2 Grave Callers), Shield Wall (2 Hedge Knights + 2 Marsh Archers), Warband (a Brute + 2 Footpads + a Warpriest), Horde (4 goblin minions + 2 Ember Casters; the Hexer was swapped for a second caster on 10-01, since a non-attacker plus minions that die before swinging left Horde too easy). (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard"; "Horde and the minion Health ratio")

### Levels and XP bands

- **XP is always composite:** everything a PC has spent, combat and otherwise. It's the designer's unit. Label it composite in write-ups, with the combat figure in brackets when it matters. (2026-11-02) (→ CLAUDE.md, "XP the designer quotes is composite"; ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **The schedule: Level 1 = 75, Level 2 = 125, Level 3 = 175, Level 4 = 225, Level 5 = 275 composite XP.** (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **Level N enemies are for PCs within 25 XP of that Level's schedule.** Level 1: 75-100 (75 is where characters start), Level 2: 100-150, Level 3: 150-200, and so on. "On-level" means the middle of the band. (2026-11-02; same bands first given 2026-10-08) (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2"; enemy_sim/TABLE_PLAY_NOTES, "Third round: Level 1")
- **The bottom of a band should feel friction, the top comfortable.** That's the sense of progression the Levels are for. Measured under v3: about 40-60% of days won at the bottom, 99-100% at the top. (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2"; "v3", "How it plays")
- **By Level 5 some archetypes reach the PC caps** (+10 to an attack or Defense Skill Total, 5 in a damage or Resist Stat), since they face PCs at about 275 XP, where most characters have capped out. (2026-11-02) (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **Below Level 4, no enemy base stat should be the equivalent of a 5.** No damage bonus or Resist of 5 from stats alone; only Physical Resist reaches 5 there, by way of armor. (designer, earlier pass) (→ ENEMY_ENCOUNTER_DESIGN, "Role: the broad archetype")
- **A sim party plays at its combat share:** 0.8 × composite + 5 (105 of 125, 145 of 175). (→ CLAUDE.md, "XP the designer quotes is composite")
- **XP trickles in steadily,** about 5 XP per adventuring day (or every other day) early on, after a handful of fights and other challenges. A party spends roughly five to ten adventuring days in each half of a band, so a few XP either way rarely shows at the table. (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **The GM decides when the next Level's content arrives.** PC growth is continuous; enemy Level is five bins. Holding a region at one Level while the party earns XP produces the on-level-to-outgrown arc by itself. (→ ENEMY_ENCOUNTER_DESIGN, "Analysis: does this actually produce 5 discrete power tiers?")

### Abilities

- **Simple: a passive, or a tweak to the main Action.** No activated abilities and no per-encounter abilities. An enemy has one thing it does, its main Action: attackers attack, supports Protect or heal an ally, debuffers attack a Defense (usually Mental) for no damage and land a big stack of one debuff. (2026-09-30, restated 11-03) (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard"; "First principles")
- **Supports and debuffers carry a backup attack** for when there's nothing useful to buff or debuff. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **Every enemy puts something on the fight:** a debuff on the party (an on-hit rider, or a debuffer's whole Action) or a buff on its allies (Durable). This is why goblins kept Strike (Slowing) over Medium Armor (2026-10-01). (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard"; "Horde and the minion Health ratio")
- **Hex and Shield Ally size:** 3 stacks at Levels 1-2, 4 at 3-4, 5 at 5, priced to trade about evenly with an enemy hit. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **More attack types than melee:** Shadow casters against Vital, Fire casters against Dodge, debuffers against Mental, alongside weapon attacks against Parry/Dodge. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **An attack that's harder to defend against gives up about 1 Accuracy,** priced the same as one that only targets Dodge. No separate price for aiming at Vital, Mental or Vigilant. Spell Actions already pay it (Accuracy +0 and 2 + Stat against a light weapon's +1 and 3 + Stat, and no Parry), like a player's War Magic. (designer, 2026-11-02) (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **What costs something:** an overall gain (better armor, a heavier weapon, an on-hit debuff, more Health) costs Upgrades; a trade is a free choice (archetype, main Action, Strong Defense, choosing a spell's element). (designer, 2026-09-30) (→ ENEMY_ENCOUNTER_DESIGN, "Projection model"; archive GM_GUIDE_NOTES, "The rule for what costs something")
- **Medium or Heavy Armor costs an Upgrade; Heavy is Level 3+ only.** Enemy armor matches the live player numbers (Medium: Physical +2, Dodge −1; Heavy: +3, Dodge −1, Speed −1). (designer, 2026-09-30) (→ ENEMY_ENCOUNTER_DESIGN, "Armor")
- **The whole Ability catalog is in the sim** (2026-10-25). (→ ENEMY_ENCOUNTER_DESIGN, "The v2 kit")
- **Under v3, Abilities and armor are priced in enemy Health** (designer, 2026-11-03: "start ironing out the Ability budget and balancing, at least in terms of Health"; each price gets a second look against the balance weights). Every enemy gets 1 Health per Slot of Abilities and armor free; past that they come off its Health, and what it leaves is Health. At most a third of the table's Health can go. Draft prices: 0 for the one-stack riders, Resilient, Sturdy, Shadow Jaunt and Action (Intimidating); 1 for most others (Necrotic, Harrying, Devastating, Heavy or Powerful Weapon, Durable, Omniguard, Enhanced Speed, Resist, Medium Armor...); 2 for Battering, Cleaving, Enhanced Reflexes, Retribution Aura, Heavy Armor; 3 for Grappling, Poison (Bleeding), Powerful Spell, Enhanced Range, Attunement; Unarmored gives 1 back. With prices on, the middle of every band still lands at 94.5-97% of days won. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted")
- **Debuffs as standard are best paid for with Damage, not Health** (2026-11-04, the designer: enemies should apply debuffs and have mechanics, not be Health sponges). −1 Damage Stat buys about 4-5 Health of on-hit debuffs and keeps fights at the same length and acts-again at every Level. Paid from Health, debuffs about earn their keep but each Health spent takes about a quarter-round off; Levels 1-3 bear about 2 before fights drop under 3 rounds and enemies stop acting again, Levels 4-5 about 3. Accuracy and Resist are poorer currencies. The two free riders together are worth something like half a Health to a Health, not 0. (→ ENEMY_ENCOUNTER_DESIGN, "How much budget can go into on-hit debuffs")
- **Survivability sets fight length; offense doesn't** (2026-11-04). −1 Health, Resist or the party's target Defense takes a quarter to half a round off per Health of worth; −1 Damage (worth about 4 Health) or Accuracy (about 2) barely moves it. So prune the baseline's offense, not its survivability, and let the budget buy offense back. +1 Resist is worth 3-4 Health and over a round. (→ ENEMY_ENCOUNTER_DESIGN, "What each stat is worth")
- **The pruned v3, the default since 2026-11-04** (designer: a thin baseline, archetypes and Abilities that only add; heavier armor the one thing that takes numbers away; damage cut from the base must be buyable back). `V3_VERSION = 3`: Damage Stat and Accuracy one lower, a budget of 7 per Slot that can buy them back (Damage +1 for 4, Accuracy +1 for 2, plus Guard +1 for 1 and Resist +1 for 4), and additive archetypes (Striker Damage +1 and Speed +1, Bruiser Damage +1, Health +1, Vital +2, Strategist and Skirmisher one less Accuracy). Bought back, it plays like v3. Spent on mechanics, fights run 4-5 rounds with enemies acting again about half the time, Level 1 a bit harder and Levels 3-5 a bit softer. The catalog is grouped into Equipment, Stats, On a hit, Toughness, Actions. (→ ENEMY_ENCOUNTER_DESIGN, "The pruned v3")
- **Pruned v3, round two** (designer, 2026-11-04). The weapon is a loadout, not an Ability: an enemy in melee carries a sword and shield by default, and the choices are heavy or light, two-handed or a shield, bows and spells (priced from Sword and Shield, under what they measured so better kit is a cheap upgrade, as it is for players: heavy one-hander and heavy bow 1, two-handers 2; heavy kit free cost the party 4-7 points of days won at every Level). Powerful Weapon and Spell are plain +1 Damage, bought once, like Damage +1. Stats, defense bonuses and on-hit effects can be bought again and again; on-hit effects are a stack a pick, up to 4 (light effects half a point a stack, Necrotic half, Harried 1, Bleeding 2½). The budget is the lever: 6 / 7 / 9 / 9 / 9 at Levels 1-5 at first (the extra at 3-5 best spent on Accuracy), 7 / 8 / 10 / 10 / 10 since the designer asked for a notch more danger. That lands every Level near its targets at 4-5 rounds. (→ ENEMY_ENCOUNTER_DESIGN, "Building an enemy on paper")
- **Extra budget should go to offense, not more mechanics.** More Crippled and better defenses lengthened fights and cost the party days without raising the stakes in a fight. (→ ENEMY_ENCOUNTER_DESIGN, "Building an enemy on paper")
- **A 0 price means the sim reads it as about nothing against the sample parties,** not that it's worthless. The one-stack debuffs are the first to check against the balance weights. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted")
- **Poison (Bleeding) lands 1 stack and Retribution Aura answers melee attackers only, in the sim, under v2 and v3.** As written (2 stacks; every attacker) they read about 5 and 15 Health, too much for one Ability. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted"; "The v2 kit")
- **Durable with decaying Protected is fine as is.** It's meant to give 1-2 rolling Protected until the enemy gets focused down. (designer, 2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Open questions for the designer")
- **Enemy suits: +1 damage per Heart in an enemy's flip,** for now; something more detailed later. (designer, 2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Open questions for the designer")

### Standing decisions

- **Fighting Styles are off** (designer, 2026-09-30). The baseline needed more enemy offense, not less, and Guarded on a stand-still tank was the uncosted combination behind the old Shield Wall wall. Enemies move and attack up to twice a turn. (→ ENEMY_ENCOUNTER_DESIGN, "Fighting Styles off")
- **Enemies double attack like players unless there's a reason not to.** (designer, 2026-10-08) (→ enemy_sim/TABLE_PLAY_NOTES, "Second round")
- **Enemies don't know the party's Defenses.** Targeting is position (nearest) or visible cues (the most hurt), never "who's easiest to hit." A Taunted enemy goes for its Taunter. (2026-09-30) (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **Each stat block has its tactic baked in** (nearest; Assassin, the weak or isolated; Kiting; for supports, the most hurt ally), so the GM doesn't think about it at the table. (2026-10-07) (→ enemy_sim/TABLE_PLAY_NOTES, "Enemies")
- **Assassins read "softest" by sight:** the worst hurt first (share of Health lost), then whoever wears the lightest armor. (designer, 2026-10-28) (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Enemies use player weapons and armor, and Parry from the weapon Skill.** (2026-09-30, restated 11-03) (→ ENEMY_ENCOUNTER_DESIGN, "Armor"; "First principles")
- **Light Armor is the on-level default; a caster can go without.** (→ ENEMY_ENCOUNTER_DESIGN, "Empirical validation"; archive GM_GUIDE_NOTES, "Step 5: Upgrades")
- **Health near a PC's.** This replaced the 09-30 rule that Health was the one stat allowed to break from player numbers, and v2's roughly double Health. (2026-11-03) (→ ENEMY_ENCOUNTER_DESIGN, "First principles"; "Toward PC-like enemy stats")
- **Spikier, shorter fights are accepted for PC-like numbers.** v3 runs 3.5-4.3 rounds against v2's 4-5; the designer took that trade. (2026-11-03) (→ ENEMY_ENCOUNTER_DESIGN, "v3", "How it plays")
- **Consumables cover the rare bad fight,** so an occasional acute loss is fine. Not modeled yet. (2026-11-02) (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **The hand-build has no judgment calls in the budget.** The GM decides what the enemy is and how it spends its Upgrades; everything else is a pick from a list or a lookup. (designer, 2026-10-01) (→ ENEMY_ENCOUNTER_DESIGN, "Codified hand-build rules")
- **Tank and Bruiser's Resist +1 is one +1 to every Resist,** the NPC version of raising Essence, not +1 Physical plus +1 to each element. (→ ENEMY_ENCOUNTER_DESIGN, "Role")

### Targets for how a fight should feel

For an on-level fight (most fights are on level), at the middle of the band, measured by the day standard:

- **The party basically never loses a fight.** About 95% of days won; the worst party in the middle of a band still wins most days. (designer, 2026-10-08; day figure from the 11-03 ranking) (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets"; ENEMY_ENCOUNTER_DESIGN, "Toward PC-like enemy stats")
- **Someone goes Down now and then:** a bit uncommon, about one fresh fight in five or six. (designer, 2026-10-08) (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets"; "Second round")
- **Someone ends up Wounded about every other fight,** often near the end. Something the party keeps in mind, not usually a problem. (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets")
- **A hit enemy gets another turn about half the time.** The party lands a hit, the enemy acts, the party piles on, and about half the time it drops before acting again. It pulls against short fights: only more enemy Health raises it. (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets"; ENEMY_ENCOUNTER_DESIGN, "Base stats against the measured party")
- **Length: about 4 rounds.** 3.5-4.3 accepted under v3 (2026-11-03). Earlier: about three rounds, five at the outside (2026-10-08); then 4-5 on average (2026-11-02). (→ ENEMY_ENCOUNTER_DESIGN, "v3"; "Draft base table v2")
- **Where v3 lands (the pruned default, a notch more dangerous, 2026-11-05):** budget 7 / 9 / 11 / 11 / 11 (a point more at Levels 2-5 after the Defender's Health +3). The average party wins 86-92% of days, someone is Down in about a fifth of fresh fights and Wounded in about half, 4.5-5.6 rounds. Every strong party but one loses a day now and then (the designer: real players coordinate and have items, so even a strong sim party shouldn't win every day). (→ ENEMY_ENCOUNTER_DESIGN, "A point more budget at Levels 2-5"; "A little more dangerous")
- **One party composition is an outlier:** Hilde, Sable and Hanforth with Felix or Carrick win 98-100% of days whatever the enemy budget. That's for the PC balance pass. Otherwise a party's strength is about the sum of its members (95% of it); pairs add little. (→ ENEMY_ENCOUNTER_DESIGN, "A little more dangerous")
- **Weak builds should stand out.** Higher, PC-like enemy Resist spreads the parties out, which is what the yardstick wanted, at the cost of a harder floor. (→ ENEMY_ENCOUNTER_DESIGN, "Toward PC-like enemy stats")

### Open enemy questions

- **Ability prices against the balance weights,** the zeros first; whether 1 Health is the right allowance; Improved Support needs a test with more supports in it. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted", "Open")
- **Whether 3.5-4 rounds is close enough to "4-5".** (→ ENEMY_ENCOUNTER_DESIGN, "v3", "Open")
- **How steep one enemy Level should be.** One Level up is a cliff in every table so far; two Levels up nobody wins. (→ ENEMY_ENCOUNTER_DESIGN, "Base stats against the measured party")
- **Levels 4-5 are checked against grown Level 3 characters,** not sample characters built at those Levels. Level 5 is the least certain row. (→ ENEMY_ENCOUNTER_DESIGN, "v3"; "Draft base table v2")
- **Retribution Aura:** whether "melee attackers only" reads right in the fiction, and its price (2 Health under v3; it cost a Level 2 party a fifth of its Health when all of Warband had it on every attacker). (→ ENEMY_ENCOUNTER_DESIGN, "The v2 kit"; enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Poison (Bleeding)'s shape:** 1 stack (3 Health under v3, 5 Upgrades under v2), waiting on the Bleeding weights. (→ ENEMY_ENCOUNTER_DESIGN, "v3 adopted"; "The v2 kit")
- **A game-ready roster:** "Example PC Builds" and "Example Enemies" documents, once the tunables settle. (→ ENEMY_ENCOUNTER_DESIGN, "Planned next steps")
- **Sturdier fodder,** if wanted, likely needs its own minion trade-off (more Health, weaker attack), not more armor. (→ ENEMY_ENCOUNTER_DESIGN, "Horde and the minion Health ratio")

## How the table plays

### How players fight

All from the designer's notes on their own table (2026-10-07 unless dated).

- **Play style splits by character type.** Tanky characters dive in and trust their abilities (Hilde, Browndog). Fragile ones (healer, archer, mage) hang back and trust the tank. Some sit in the middle, on the edges, attacking who they can without clear danger. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **Safety first, on the whole.** The party generally won't expose itself and prefers playing safe. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **Attacking twice is attractive.** A player who can attack twice at the start of their turn usually will; otherwise they attack, then move to a better spot. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **A melee character who can double attack prefers it to playing safe,** but won't close in on several enemies just to attack once, and uses spare movement to work round the edges. (2026-10-08) (→ enemy_sim/TABLE_PLAY_NOTES, "Second round")
- **The party talks and coordinates, not perfectly.** Focus fire within reason: if an enemy's already Harried, others pile on, but nobody goes far out of their way, and a back-liner takes an easy double attack over a risky focus target. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **Players don't know enemy Health.** They read armor, who's hanging back casting, who looks hurt. A lightly armored healer at the back is an obvious priority, but they won't risk much to reach it, and often just plow through whoever's being healed. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **Players are sometimes reckless for fun.** Suboptimal picks and silly moves happen all the time. (→ enemy_sim/TABLE_PLAY_NOTES, "How players fight")
- **A typical party:** one melee fighter/tank/strategist, a healer or disruptor, an archer and a mage. Often only one character wants to be in melee. (→ enemy_sim/TABLE_PLAY_NOTES, "Builds")
- **How the sample cast plays** (2026-10-08 and 10-09): Felix plays carefully but takes targets out tactically and can hold the front; Enith is a tactical skirmisher, almost a disabler, whose hexes split enemies up so the party can divide and conquer; Ashleigh boosts attacks with Raise Spirits, stays in range of the party and throws a knife with what's left. (→ enemy_sim/TABLE_PLAY_NOTES, "The last three builds"; "Fourth round")
- **The battlefield:** fights start 6-10 meters apart, with some line-of-sight trouble: whether an archer has to move to get a shot is about a coin toss. Archers are strong for it. (→ enemy_sim/TABLE_PLAY_NOTES, "The battlefield")
- **How enemies come on:** sometimes they swarm; on a cramped battlefield they try to twist the knife; sometimes they just walk straight in. (→ enemy_sim/TABLE_PLAY_NOTES, "Enemies")

### Cards and resources

- **A player commits about a third (a quarter to a third) of their hand to a fight,** across everything: rescuing a flip, healing, card-fueled Techniques. (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources")
- **Cards rescue key moments, and that's good play.** A wounded enemy, a finishing hit that misses, a 12 in hand: in it goes. Holding a queen, a player may Gamble once or twice on an 8+ and play the queen if the flip comes up short. (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources")
- **Cards are a big share of the party's strength.** Modeling the hand took fights from about 3.6 rounds to 2.7 and halved how often someone went Down. (2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Fourth round", "Results")
- **A played card either replaces a flipped card (its suit joins the pool too) or just adds its suit to the pool.** (designer, 2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Open questions for the designer")
- **A healer's card budget is fine as is.** The point is what a party does with average resources. (designer, 2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Open questions for the designer")
- **Rules readings settled along the way** (designer): Fleeting's skip only applies to an effect gained during the bearer's own turn, Bleeding never skips and Harried clears at the end of the turn (10-09); only weapon attacks can be Gambled on (10-09); Bleeding loses half its stacks, rounded up, each time it decays, and Protected stops its ticks (10-19); a PC's leftover Bleeding ticks out after the fight (10-19); Interrupts happen before their trigger (10-28); AP comes at the start of the fight and at the end of each turn, so it's free for Interrupts (10-27); one Style at a time (glossary); Wind Slash on a melee weapon gives reach (10-27). (→ enemy_sim/TABLE_PLAY_NOTES, "Three rules fixes", "The new Bleeding rule", "Still to do", "Mechanic baseline")

### Between fights and the day

- **Two fights a day** is the working assumption. The party usually isn't beaten down enough after the first that anyone's Wounded. (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources")
- **Between fights players top off their Health,** and some have Techniques that help defensively. (designer, 2026-10-08) (→ enemy_sim/TABLE_PLAY_NOTES, "Second round")
- **Healing after a fight is part of what healers are for.** It's why healing costs cards: it stops Wounded in a fight and tops the party up so they go to bed full or close to it. Carrick's Patch Up is for this too. (designer, 2026-10-29) (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources")
- **Health left after one fight isn't the whole story.** A party that goes to bed short starts the next day short, and one that keeps doing that loses a fight eventually. So the day is the unit. (designer, 2026-10-29) (→ enemy_sim/TABLE_PLAY_NOTES, "A whole day")
- **Healing is worth far more by the day than by the fight.** Taking Healing Magic off Hanforth costs about 2 Health after one fight and 11 by the next morning; the one-fight score underpriced healers. (2026-10-29) (→ enemy_sim/TABLE_PLAY_NOTES, "The day standard, and standard checks")
- **How the sim spends the day** (Claude's play rules, 2026-10-29): From the Brink of Death on the Downed first; then cards on healing, keeping a fight's budget (a third of the morning's hand) after the first fight and spending everything after the second, since the Discard Cycle takes the hand at night; Patch Up before bed; the night restores committed Health, then Body plus any "extra 1 Health", Deep first. (→ enemy_sim/TABLE_PLAY_NOTES, "Between fights")

### Builds and XP

- **Players build for fun, with an eye on being good when it counts.** About two-thirds to four-fifths of XP goes to combat; the rest is social and knowledge Skills, adventuring Skills (Awareness, Insight, Athletics, Might for climbing) and ribbon Techniques like Minor Oracle. (designer, 2026-10-07) (→ enemy_sim/TABLE_PLAY_NOTES, "Builds")
- **Hardly anyone builds a pure combat character,** and the XP spent outside fights has to matter outside fights: scouting, talking past an encounter instead of paying a bribe. (designer, 2026-10-30) (→ enemy_sim/TABLE_PLAY_NOTES, "The combat budget")
- **Skills spread out.** A reasonable character has a couple of points in Awareness and Insight, maybe a social Skill, a bit of Might and Athletics. Skills overlap enough that characters can be good at things relative to each other. (→ enemy_sim/TABLE_PLAY_NOTES, "Builds")
- **Once the combat basics are down, XP goes elsewhere.** (→ enemy_sim/TABLE_PLAY_NOTES, "Builds")
- **The combat budget: 145 of 175 composite XP at Level 3, 105 of 125 at Level 2.** The designer first said 130, then moved it to 145, the high end of the non-Carrick builds, as the mid-tier focal point for balance. Test builds and the plain stand-in get this budget. (2026-10-30) (→ enemy_sim/TABLE_PLAY_NOTES, "The combat budget")
- **The sample roster is ten Level 1 characters from the designer's own exports** (agreed 2026-10-08): Hilde, Browndog, Carrick, Jackal, Beornhard, Sable, Hanforth, Felix, Enith, Ashleigh, levelled to 125 and 175 XP. Sample parties: typical table (Browndog, Hanforth, Sable, Beornhard), two front-liners, skirmishers, support-heavy. (→ enemy_sim/TABLE_PLAY_NOTES, "The sample roster")
- **Sample builds are benchmarks.** A prereq a build misses is fine to leave (designer, 2026-10-24). The sim always plays the live CSVs; exports made before a change get rebuilt later (designer, 2026-10-27). (→ CLAUDE.md; enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **At the same combat XP the designer's archetypes come out roughly even,** and about level with a plain fighter. The optimized ceiling is a Level or more above that. (2026-10-30) (→ enemy_sim/TABLE_PLAY_NOTES, "A scorecard at 145 combat XP")
- **Watch the "survives forever" soak** (the designer's name for it): Essence 4-5, Body 1, stacked Toughened Resolve, Lifeline and a one-Feature Healing Magic, dealing almost no damage. Scored with plain stand-ins it looks great; in a party of optimized builds it adds the least, and a second soak adds little. (2026-10-31 to 11-02) (→ enemy_sim/TABLE_PLAY_NOTES, "The first run", "Does the yardstick flatter max Health and Lifeline?")
- **Healing Magic as an Encounter Technique was a test only** (designer, 2026-11-01). techniques.csv is unchanged; it trimmed the ceiling a little and hit the healer hardest, and didn't touch what makes a soak. (→ enemy_sim/TABLE_PLAY_NOTES, "Healing Magic as an Encounter Technique")
- **Feint is only worth it as a setup** "specifically aimed at setting up a target for the party to Gamble and wallop" (designer, 2026-10-28). Even played that way it doesn't pay yet; making it pay is a rules call. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Sanguine wants an overhaul,** not now. (designer, 2026-10-28) (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")

### Calibration targets and how we measure

- **The day standard: two fights, care between them, and the night, at enemy Health ×1.0.** Other multipliers are worth a look now and then. (designer, 2026-10-29) (→ enemy_sim/TABLE_PLAY_NOTES, "The day standard, and standard checks")
- **The fight targets are in "Targets for how a fight should feel"** above (2026-10-08, with the length updated 11-02 and 11-03). (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets")
- **Make the day harder with enemy Levels, not fractional steps or more Health alone, and read it as win rates.** The enemy-Level yardstick builds every sample enemy one or two Levels up through the same builder. Two Levels up nobody wins, so a party's own Level and one up are the readings that tell parties apart. (designer, 2026-10-30) (→ enemy_sim/TABLE_PLAY_NOTES, "The enemy-Level yardstick")
- **Don't let the yardstick credit a pool just for being big.** Health left (or Health in the morning) flatters Toughened Resolve and Toughened Body; "what it can take" (the toughest enemies at which the party wins half its days) counts only winning. (designer's question, 2026-10-30) (→ enemy_sim/TABLE_PLAY_NOTES, "Two kinds of measure"; "Does the yardstick favor durability?")
- **More enemy Health alone favors flat Resist;** a GM levelling a fight up raises Health, damage and Accuracy at once. Enemies whose damage keeps up with their Level are the fairer test. (→ enemy_sim/TABLE_PLAY_NOTES, "Does the yardstick favor durability?"; "Does the yardstick flatter max Health and Lifeline?")
- **Score builds in parties first, with stand-ins as a check.** A soak is only as good as the damage around it. (2026-11-02 conclusion) (→ enemy_sim/TABLE_PLAY_NOTES, "Does the yardstick flatter max Health and Lifeline?")
- **On-level means the middle of a band, measured with parties normalized to that band's combat XP.** Level 1 uses the sample parties at 75. (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **A few percent either way isn't telling us much on its own.** The same party on other fights reads about 1% (fight) and 4% (day) off. (→ enemy_sim/TABLE_PLAY_NOTES, "Two kinds of measure")
- **Test items in the sim once the sample roster reaches about Level 3.** Until then it models only weapons, armor and Jackal's Bottomless Bottles. (designer, 2026-10-09) (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")

### Open questions

- **Single-fight table toughness:** ×1.75 or ×2.0. The day standard is set at ×1.0; the scripts still default to 1.75 for single fights. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do"; "Where things stand")
- **Card rescues on Encounter attacks:** the sim's party saves almost every big attack that misses (War Magic lands 96-99%). Check against how the table spends cards. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Lifeline and Toughened Resolve,** strong enough to look at, mostly as a pair. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do"; "Does the yardstick flatter max Health and Lifeline?")
- **Shape setup** (`tunables.SHAPE_SETUP`): turn it on? Waits for the designer. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Weights from the mechanic baseline** (2026-10-27): on-hit riders priced off their Average or Weak columns, Taunt priced by who's taunting, Protected split into self and handed-out, 1 AP split by melee and ranged, a term for stopping a Down, Spirit Blessing's costs. The designer's call. (→ enemy_sim/TABLE_PLAY_NOTES, "Mechanic baseline")
- **Claude's play rules waiting on confirmation:** attack Interrupts, regaining uses, Blood-Powered Spirit and Spellblade, Parting Shot's two paths, and the rules readings for the Techniques wired 10-27. (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **Leveled builds for Sable, Felix, Enith and Ashleigh,** from the designer (proposals in PROPOSED_BUILDS.md). (→ enemy_sim/TABLE_PLAY_NOTES, "Still to do")
- **The Healing and Blessing magic pass** (designer, 2026-10-26): how healers and support scale. (→ enemy_sim/TABLE_PLAY_NOTES, "Healing and blessing at Levels 1-3")

## Running the game: notes for GMs

### Loot and Materials

- **Put Materials in the loot, not just Gold.** Same instinct as handing out a painting or a jeweled statue instead of a coin count (the designer's framing). An all-Gold hoard gives a crafting character nothing to convert, and the Crafting Schools' XP only pays back if Materials show up. (→ archive GM_GUIDE_NOTES, "Planning loot: Materials vs. Gold")
- **Why Materials exist:** what got looted and what a crafter can build are the same object. The frost wyrm's hide isn't 40 Gold of loot; it's Frost Material at the wyrm's Level, waiting for someone with the right School. (→ archive GM_GUIDE_NOTES, "Why Materials exist")
- **Selling loses value; crafting keeps it.** A vendor pays about 50-75% of a Material's Level in Gold. Precious Materials sell at full value. (→ archive GM_GUIDE_NOTES, "Planning loot")
- **Keep drops roughly on-Level.** A Material must be at least the Level of what it builds. Level 4-5 Materials on a Level 1-3 party are dead weight; never varying drop Level starves higher-Level characters. (→ archive GM_GUIDE_NOTES, "Why Materials exist")
- **Material Type is the worldbuilding lever.** Mundane Types (Bone, Cloth, Leather, Metal, Wood) show up anywhere that fits. Elemental and exotic Types (Fire, Frost, Brilliant, Shadow, Medicinal, Precious) say what a place or creature is about, and carry its theme forward into what the party can build. (→ archive GM_GUIDE_NOTES, "Why Materials exist")
- **Precious vs. discounted Types is a knob.** More Precious reads as liquid treasure; more discounted Types reads as "this table rewards crafting." Turn it to fit how much the group leans on crafting. (→ archive GM_GUIDE_NOTES, "Planning loot")
- **Don't scale how much a place drops with Level.** Every Masterwork takes a flat 20 Materials; only the Level of the drop goes up. (→ archive GM_GUIDE_NOTES, "Why Materials exist")
- **Early loot can be mundane gear** (designer). Looted gambeson nobody wants becomes Cloth through Re-purpose Materials (T040). A found sword or plain cloak can stand in for the Optional-Type half of a Masterwork's materials. (→ archive GM_GUIDE_NOTES, "Early-game loot")
- **How much Material loot per session or Level is still open.** It needs play data or a design pass. (→ archive GM_GUIDE_NOTES, "Planning loot")

### Social Encounters

- **Most social interactions are a single check.** Save the Pressure, multi-round shape for a drawn-out negotiation or interrogation with stakes. Tracking Pressure on every minor beat wears it out. (→ archive GM_GUIDE_NOTES, "Running Social Encounters")
- **The expected shape, round by round:** round 1 the lead's Statement almost always lands; round 2 Support starts struggling; round 3 is the swing round, where cumulative odds cross 50%; round 4 is tense; round 5 is do-or-die. About 57% of these encounters are won overall. (→ archive GM_GUIDE_NOTES, "Running Social Encounters"; balance_weights_notes, "Social Encounter Baseline")
- **Let failure land.** A 43% chance of losing isn't small. Be ready to play out what losing the Encounter means, and don't fudge it toward success because it's a social scene. (→ archive GM_GUIDE_NOTES, "Running Social Encounters")
- **Be generous with card rescues.** Letting a player search their hand to save a failing Statement or Support check holds the whole difficulty up: 57% with it, under 10% without. A table that hoards cards for combat will find social scenes much harder. (→ archive GM_GUIDE_NOTES, "Running Social Encounters")
- **Ignore vs. remove Pressure.** Ignoring it softens this round; removing it buys more rounds. Round 5 is still round 5 under "ignore." (→ archive GM_GUIDE_NOTES, "Running Social Encounters")
- **The written Support Difficulty is a flat 11,** easier than the model assumed. If Support lands more often than the table above suggests, that's expected. (→ archive GM_GUIDE_NOTES, "Running Social Encounters")
- **Every card drawn from a Good or Bad Luck flip counts toward its suit pool,** combat included. Apply it the same way everywhere. (→ archive GM_GUIDE_NOTES, "Running Social Encounters")

### Judgment calls

- **Crafting Types are coarse on purpose.** A recipe asking for Cloth wants that many materials of a qualifying Type, flavored however the player likes, not a parts list. Don't turn narration into a new requirement. (→ archive GM_GUIDE_NOTES, "Judgment calls")
- **Cloth/Leather and Wood/Bone are near-interchangeable pairs.** Treat "or"-joined Main Types as one pool. (→ archive GM_GUIDE_NOTES, "Judgment calls")
- **A material close to a listed Optional Type is usually fine.** If you can say in one sentence why it works, it's close enough. A player who invested in a Craft Skill and a School has earned some flexibility. (→ archive GM_GUIDE_NOTES, "Judgment calls")

### Building fights

- **Count the players; pick enemies adding to that many Slots.** That's an on-level fight. Make it harder with more enemies or a busier battlefield. (→ ENEMY_ENCOUNTER_DESIGN, "Base stats against the measured party"; enemy_sim/TABLE_PLAY_NOTES, "Third round")
- **Pick the Level from the party's composite XP:** Level N for parties within 25 XP of N's schedule (75 / 125 / 175 / 225 / 275). Expect a hard day at the bottom of a band and an easy one at the top. (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **Keep it simpler than the party.** Two stat blocks, three for a complicated fight. At most one enemy that doesn't attack. (→ archive GM_GUIDE_NOTES, "Putting a fight together")
- **Give each stat block a job** (a Slowing bruiser line plus a back-line caster; minions plus a caster and a debuffer). (→ archive GM_GUIDE_NOTES, "Putting a fight together")
- **Build from what the enemy visibly is.** Its weapon sets its Parry; its Weak Defense is what that kind of enemy neglects (a fighter's Mental, a caster's Vital). The party should be able to read it. (→ ENEMY_ENCOUNTER_DESIGN, "First principles"; "v3")
- **Bake in the tactic** (nearest, Assassin, Kiting, help the most hurt) so you don't decide at the table. Enemies don't know the party's Defenses; they go by position and what they can see. (→ ENEMY_ENCOUNTER_DESIGN, "Enemy variety standard")
- **Counter-fights are fine.** A shield wall with archers is hard on an all-weapon party on purpose. Don't soften it because one lopsided party struggles. (→ archive GM_GUIDE_NOTES, "Putting a fight together")
- **Minions as front-line fodder.** A pack of minion archers or casters is a hard fight. Starting minions close (an ambush) lets them hit before they're picked off; that's a GM tool, not a default. (→ archive GM_GUIDE_NOTES, "Minions and big enemies")
- **A room full of Defenders or Backups makes a slog,** not just a harder fight: each adds about a round. (→ ENEMY_ENCOUNTER_DESIGN, "Archetype comparison"; "v3")
- **Picks that fit the enemy's job punch a little above their price** (Taunting on the shield tank, Medium Armor on the front line, Bleeding on skirmishers). (→ archive GM_GUIDE_NOTES, "Step 5: Upgrades")
- **Match riders to the fight.** Vulnerable only matters if something in the fight attacks Vital or Mental. (→ archive GM_GUIDE_NOTES, "Step 5: Upgrades")
- **The by-hand worksheet is stale.** GM_GUIDE_NOTES' six steps (Level, archetype, main Action, Strong Defense, Upgrades, stat block) still describe the process, but its numbers are v1's. Use the v3 table above until a v3 worksheet is written. (→ archive GM_GUIDE_NOTES, "Enemy stat blocks by hand"; ENEMY_ENCOUNTER_DESIGN, "v3")

### Pacing

- **Two fights a day,** with the party topping up between them and healers doing most of their healing after fights. (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources")
- **A fight runs about four rounds.** Some end fast: the party takes a couple of bad hits, piles on and drops them. (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets"; ENEMY_ENCOUNTER_DESIGN, "v3")
- **On-level, the party basically never loses;** someone goes Down now and then and someone's Wounded about every other fight. An occasional acute loss is fine; consumables are the fallback. (→ enemy_sim/TABLE_PLAY_NOTES, "Calibration targets"; ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **Hold a region at one Level while the party grows.** They start stretched, then clearly outgrow it; bring in the next Level at a story beat. (→ ENEMY_ENCOUNTER_DESIGN, "Analysis: does this actually produce 5 discrete power tiers?")
- **XP comes slowly,** about 5 per adventuring day early on, so a party spends five to ten adventuring days in each half of a band. (→ ENEMY_ENCOUNTER_DESIGN, "Draft base table v2")
- **Let players spend cards freely on key moments,** in fights and in social scenes. The game's difficulty assumes they do. (→ enemy_sim/TABLE_PLAY_NOTES, "Cards and resources"; archive GM_GUIDE_NOTES, "Running Social Encounters")

---

## Early notes, 2018-2023

The designer's own notes from before this project, distilled: the old site, the 2k19 and v5 manifestos, the items notes and the 2023 player's guide. A record of how the thinking developed, not current rules; where a point here was later decided differently, the sections above win.

Old terms are translated: "Bodily Defense" and "Resistance Defense" are Vital Defense, "Soak" is Resist, and the old Legerdemain Skill is Stealth.

**Sources, oldest first.** Each bullet ends with its tag.

- **(old site, *page*)**: `archive/flagonquest_site_other.md`, the old Google Site. It's the oldest material. The 2k19 manifesto opens by leaving that site behind, and its System Mk 1 page is dated 5/24/2018.
- **(manifesto 2k19)**: `archive/flagonquest_manifesto_2k19.md`.
- **(items 2k20)** and **(items 2k22)**: `archive/flagonquest_items_2k20.md` and `_2k22.md`. These are mostly the same text, and 2k22 is a light revision.
- **(manifesto v5)**: `archive/flagonquest_manifesto_v5.md`, for prototype v5. It isn't dated. It builds the suit system on top of 2k19's black/red change and uses Vital Defense, so it's later than 2k19.
- **(player's guide 2023)**: `archive/flagonquest_content_original.docx`, "Flagonquest Player's Guide v 2023.1". It's almost all rules text, so only a few lines come from it.


### Vision and feel

- You play a character you design. There are no classes or archetypes, so you mix and match any abilities. As the character grows, you can keep improving what they have, or let their adventures send them down a new path. (old site, Home)
- The game uses a full 54-card deck with both jokers. A streak of good or bad luck balances out as you near the end of your deck. (old site, Home)
- The cards are fate. Your deck is your fate and luck, and Good Luck, Bad Luck and drawing cards are you taking fate into your own hands. (old site, Manifesto)
- Not every character has to be good at everything. (old site, Home)
- What's the point of the game? The designer separates the actual play (the storytelling, playing a character) from "the game" (the mechanics that make up a character and how they show up in play). It's not a new idea, but it's worth stressing. (old site, Manifesto)
- The mechanics need a cohesive vision above them: what's important, and what the game's strength and focus should be. The answer the notes give is simplicity and straightforwardness. (old site, Manifesto)
- Fun is proactive. Make things active where possible, and let players choose which cool thing to do. (old site, Manifesto)
- Aim for 90% balance. At 100% nothing matters, and that's boring. Low balance is boring too, because half the options are bad. At 90% there's a choice, and some options are better or worse depending on context. (old site, Manifesto)
- PCs are exceptional. On the 0-5 Skill scale, most people who do something for a living have 1-2 points in it, or 3 in extreme cases. If a small army has a handful of people at 5 in a combat Skill, odds are most of them are PCs. (old site, Quarantine)

### Design principles

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

### Cards, luck and suits

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

### Resources: Focus, cards and daily limits

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

### Character building, XP and prerequisites

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

### Techniques: Levels, groups and structure

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

### Combat

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

### Buffs, debuffs and healing

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

### Magic and summoning

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

### Martial arts

- Why fight unarmed when a sword is a sharper fist? Because you can grapple, and because if the best praise for a swordsman is that the blade is "like an extension of their body," there may be something to using a literal extension of your body. (old site, Manifesto)
- **The schools** (old site, Manifesto and System Mk 2):
  - **Snake Style** is tricky and reactive, all grabs and trips that outmaneuver anyone.
  - **Bear Style** runs on Might and cancels out the advantages of weapons and armor: it can't be parried and does something about armor. It's a great leveler.
  - **Demon Style** is brutal, reckless and sacrificial.
  - **Great Old Oak Style** is a defensive juggernaut that doesn't lose offense.
  - **Ki Style** blends the martial and the supernatural.
  - **Shugen Style** is purely supernatural use of Meditation.
- Martial Arts Techniques mean buying into one strategy, while Tactical ones are reactive and analytical. Meditation works as a sort of third caster Skill. (old site, Manifesto)

### Exploration and skill challenges

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

### Social contests

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

### Crafting, items and Gold

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

### Enemies and encounters

- **Enemy roles** (manifesto 2k19):
  - **Support** shields, heals and buffs.
  - **Damage** attacks, with a cool buff on it.
  - **Control** attacks or makes obstacles, but mostly debuffs, maybe with Bleeding and poison.
  - The roles overlap, but each enemy has a focus.
- An enemy gets baseline actions and as few passives as possible. Keep the stat block short, with 1 or maybe 2 actions a turn. Each action is Martial, Discipline or Spell, and all of a creature's actions are at its Level. (manifesto 2k19)
- Every enemy gets an attack style and a strategy. An attack style is a net-zero limit, such as attacking only once a round in exchange for bonus movement or Good Luck. A strategy is how it fights, like going after the weakest PC it can see or keeping its distance. (manifesto v5)
- About half of enemies should have an alternate attack against Mental or Vital Defense. Across all enemies, that's about 50% of attacks against Dodge or Parry, 25% against Mental and 25% against Vital. (manifesto v5)

### Backgrounds and ancestries

- If a background has three parts, each should be worth 2 XP or about 8 Gold of specific goods. (manifesto 2k19)
- 2k19 planned to fold the non-beastfolk races into one catch-all group, maybe renamed so it doesn't draw complaints, alongside a beastfolk group. Each group got small traits, like extra reading skill or a magic trick on one side, and prehensile tails or night vision on the other. By the 2023 guide these had become backgrounds: you get two, from the General list plus either Settler or Wildfolk. (manifesto 2k19; player's guide 2023)

### At the table: roleplaying, presentation and style

- You play *as* your character, and every decision should come from them, not from you as a player. The two golden rules (old site, Meta Book):
  - **No metagaming.** Act only on what your character knows.
  - **Keep morals and politics in character.** Characters can have strong or radical beliefs, and characters at odds can make for great play, but that never carries outside the game.
- The basic loop: the GM describes the scene, players say what their characters try, the GM decides the results and calls for flips, and then describes the outcome. The GM has the final word, but players should feel free to raise a possible mistake so everyone's on the same page. (old site, Meta Book)
- Write rules in active, precise language: "you push the target," not "the target is pushed." (manifesto v5)
- Player-facing text can be light and a bit jokey, like "These are fun, you'll love them," or "Stats and Skills lists the... Stats and Skills." In-fiction quotes and flavor sit beside the rules. (old site, Home; player's guide 2023)
- "Placeholder" is an in-fiction arcanist pseudonym behind a line of named spells and items. (player's guide 2023)
- **Sheet design.** Swap the boxes for values that change a lot for shapes that match a dice set, so players can rest dice on their sheets: squares (d6) for fleeting effects, and triangles (d4 or d8?) for Health levels. The 2k19 notes mark this done ("Ayy we did it boys"). (manifesto 2k19)
- The 2k19 site layout: an intro (Stats and Skills, gameplay examples, a sample character), How to Play (character creation, Glossary, Basic, Combat, Adventuring and Social rules), Techniques, then Items and Things. (manifesto 2k19)

### Ideas noted but not adopted

Ideas from the notes that weren't found in the current game. Suit-pair sets and named check types are listed above.

- **Palhalla.** When you die, you come back. XP turns into "Glory," and Glory buys Techniques at Levels 1-5. One example, "Binding: Legend of {Item}," makes an item part of your legend. You can always reveal it as being on you, nobody else can own it, it can't be destroyed, and it costs Glory equal to the item's Level. Idea, not yet in the game. (old site, Palhalla and Legend Binding)
- **Trap card.** A ranger Technique where you set a card from your deck aside as a prepared trap. When an enemy moves close, you spring it as an Interrupt and attack. "The point is you get to see the card but the GM can't, which is funny." Idea, not yet in the game. (old site, W I P)
- **Mastermind (Level 5).** It needed some effect beyond extra cards a day, which gets weird untied to a Stat. Left unfinished. (manifesto 2k19)
- **Harried at the start of combat.** Everyone starts Harried, to make Reflex flips matter. Considered and set aside. (old site, Manifesto)
