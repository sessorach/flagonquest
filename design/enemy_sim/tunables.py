"""
Every number in the enemy/party model that's still subject to revision —
edit this file when the PC or enemy baselines change, not enemy_builder.py
or party.py. Those two files implement the *shape* of the formulas (how
Level/Role/Armor/Defense-tier combine); this file is *what the numbers
currently are*, kept separate specifically so re-tuning doesn't require
touching mechanics code.

Enemy-side curves are a direct port of archive/flagonquest_encounter_
builder.xlsx's "Design" and "Encounter References" tabs (verified against
its own live worked example — see enemy_builder.py's __main__ block).
PC-side curves are this project's own estimate (see design/
ENEMY_ENCOUNTER_DESIGN.md's "Analysis" section for the derivation) and
are the piece most likely to move as the PC/enemy models get revisited.
"""
import game_data  # items.csv's weapons and armor (WEAPON, ARMOR below)

# ---- Enemy Level curve (Design sheet) ----
ACCURACY = {1: 4, 2: 6, 3: 7, 4: 8, 5: 9}
DMG_RESIST = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}
HEALTH_BASE = {1: 7, 2: 8, 3: 10, 4: 11, 5: 13}
ABILITY_RATE = {1: 2, 2: 3, 3: 4, 4: 5, 5: 8}

# ---- Encounter Slots -> Health multiplier (non-linear, action-economy tax) ----
# Half-slot minions: 1/3 of a full enemy's Health. 1/2 was tried
# (2026-10-01) and was far too generous: split into minions, real
# enemies got much harder (horde_experiments.py; ENEMY_ENCOUNTER_DESIGN.md).
# 4 Slots (2026-10-07, a solo boss for a party of four): 9, continuing
# the same curve (each doubling of Slots triples Health and Upgrades).
SLOT_MULTIPLIER = {1: 1, 0.5: 1 / 3, 2: 3, 4: 9}

# ---- Encounter Slots -> turns per round ----
# Per the designer (2026-10-07): a 4-slot solo boss takes two turns each
# round, so it isn't out-acted four to one. Each turn gets its own place
# in the turn order (its own Reflex flip). Anything not listed takes one.
TURNS_BY_SLOTS = {4: 2}

# ---- Movement mode (combat_sim.run_fight(..., movement=True)) ----
# A bounded square arena, in meters ("space" and "meter" are the same
# unit throughout this project - see weapon/spell Range values). 20x20
# was picked as a representative mid-size arena, not derived from
# anything - a real Range value at Level 5 (Heavy Bow: 17m, Ranged
# Spell: 12m) can span most of it, while Level 1's shorter ranges (5-6m)
# leave real room for a kiter to actually use the space.
ARENA_SIZE = 20
# How close two units need to be for a melee Action (attack_range == 0
# from enemy_builder's own formula) to actually connect - the real rule
# (the designer's own clarification, not a guess anymore): movement is
# whole spaces, no fractions, and ending up in any space adjacent to a
# target (Chebyshev distance 1, including diagonally) is enough to
# melee it. Used to be an invented "close enough" buffer (2) since no
# real number existed yet - see movement.py's own docstring for the
# grid/Chebyshev-distance rule this now assumes throughout.
MELEE_RANGE = 1
# Area Attack's Burst (2026-11-08): other PCs within this many meters of the
# target are attacked too.
AREA_BURST = 1

# ---- Armor tiers (armor_categories.csv, the real player-facing table) ----
# One shared table for both sides now - enemies and PCs alike wear real
# armor and get the real armor bonus (see party.py's own Armor
# paragraph for the PC side; enemy_builder.py already used this table).
# Physical Resist only - rulebook.md's Resist rule ("starts equal to
# your Essence") only gets a further boost from Armor for Physical
# damage; elemental Resist (Fire/Frost/Brilliant/Shadow, collapsed into
# one `elemres` pool in this sim) stays Essence-only on both sides, no
# armor contribution, matching armor_categories.csv's own column being
# titled "Physical Resist" specifically. Unarmored is the implicit
# baseline (all zeroes) - armor_categories.csv only lists the three worn
# tiers, each relative to bare skin. This used to be a different,
# enemy-only table anchored one step over Unarmored (to compensate for
# PCs having no armor modeled at all) - now that PCs get the real thing
# too (see party.py), that workaround isn't needed; both sides read off
# this one real table. Note this does shift every enemy that wasn't
# already on Light Armor (all 5 Roster enemies are, so the validated
# grid's own enemy side is unaffected - only Medium/Heavy archetype
# rows, like the Tank archetype, see a small Dodge/Speed change).
# Read from items.csv (Medium/Light/Heavy Armor, I127-I129) since
# 2026-10-27, so a change there reaches the sim with nothing copied over.
ARMOR = game_data.armor_table()

# ---- Action Points (rulebook.md's "Actions on a Turn") ----
# "When you flip Reflex to join an encounter, and again at the end of
# each of your turns, you lose any existing Action Points and gain 4
# Action Points in their place." - a flat per-turn budget every unit
# gets, spent on move actions and attacks (see combat_sim.py's
# spend_movement_ap and the Party's/Enemies' turn loops in run_fight).
AP_PER_TURN = 4
# Healing Potions (designer, 2026-11-09 test): each PC starts the day with
# this many Healing Potions (I043, its heal read from items.csv); they
# don't come back between fights. A PC at POTION_DRINK_AT of its max
# Health or less drinks one at the start of its turn for POTION_AP. 0: off.
PC_POTIONS = 2  # on since 2026-11-09 (designer: tune with the party carrying them)
# 2 AP (designer, 2026-11-09): glossary.md [Potion] says "It takes 1 AP
# to use a Potion, and it must be in your hand to use", and getting it into
# hand from your gear is another 1 AP. The same to feed one to an ally.
POTION_AP = 2
POTION_DRINK_AT = 0.5
# Feeding a potion (designer, 2026-11-09 test: a Potion can go to a
# willing or Downed creature adjacent to you): a PC with one feeds it to a
# Downed ally next to it at the start of its turn, before drinking its own.
POTION_FEED = True
# Drinking between fights (2026-11-09 test): after the first fight's care,
# each PC drinks while it's missing at least a potion's heal, keeping
# POTION_KEEP for the second fight; a Downed PC is fed one by an ally.
POTION_BETWEEN = True
POTION_KEEP = 1
# "A move action takes 1 AP to make... this moves you up to your Speed
# in meters. You can always end a move action early." - can be taken
# more than once in a turn, AP allowing, which is exactly how closing a
# longer gap than one Speed's worth of distance works here.
MOVE_AP_COST = 1
# "Most normal actions that involve a bit of effort, like making an
# attack, take 2 AP to do."
ATTACK_AP_COST = 2
# T105 Healing Magic's own techniques.csv row gives it 1 AP specifically
# (not the standard 2 above) - see tactics.strategy_support_healer.
HEALING_MAGIC_AP_COST = 1
# T075 Magehunter's own techniques.csv row: "1 AP - Interrupt" - see
# combat_sim._magehunter_interrupt.
MAGEHUNTER_AP_COST = 1
# A once-a-fight Interrupt that stops an enemy attack (Arrow Finds Only
# Mist, Swatting Paw, Slithering Hands; 2026-10-28) is spent on an attack
# whose expected Health loss is at least this much, or that could Down
# the PC. Before the flip that's hit chance x damage after Resist; after
# the flip the hit is known, so it's the damage.
INTERRUPT_SAVE_MIN = 1.5
# T076 Parting Shot's own techniques.csv row: "1 AP - Interrupt" - see
# combat_sim._parting_shot_interrupt.
PARTING_SHOT_AP_COST = 1

# ---- Role archetypes (Combat Role catalog, richer/authoritative version) ----
# Tank/Bruiser's Resist +1 is the NPC equivalent of a character raising
# Essence, so it already reaches every Resist (enemy_builder feeds
# `resist` into both physres and elemres). They used to carry an extra
# "elem_all": 1 on top, which double-counted elemental Resist and put a
# Level 3 Bruiser at 5 elemental - past the "no 5s in base stats below
# Level 4" line the designer holds enemies to.
ROLE_MODS = {
    "None":       {},
    "Tank":       {"resist": 1, "parry": 1, "dodge": 1},
    "Striker":    {"accuracy": 1, "damage": 1},
    "Bruiser":    {"damage": 1, "resist": 1, "parry": -1, "dodge": -1},
    "Strategist": {"accuracy": 1, "bodily": 1, "mental": 1},
    "Defensive":  {"parry": 1, "dodge": 1, "bodily": 1, "mental": 1},
}

# ---- Combat Actions (own direct Accuracy/Damage/Parry contributions) ----
ACTIONS = {
    "Defensive Melee": {"accuracy": 1, "damage": 3, "parry": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Offensive Melee":  {"accuracy": 0, "damage": 4, "parry": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Ranged Weapon":    {"accuracy": 1, "damage": 3, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Melee Spell":      {"accuracy": 0, "damage": 3, "dmg_type": "Fire", "opp_def": "Dodge", "range": 0},
    "Ranged Spell":     {"accuracy": 0, "damage": 2, "dmg_type": "Fire", "opp_def": "Dodge", "range": 2},
}

# ---- Ability catalog: the old builder's subset ----
# The original enemy_builder.build_enemy (rows with no AttackTier) only
# knows these, at the spreadsheet's 5-point costs. Every row built since
# 2026-10-01 goes through enemy_builder_pcstyle instead, whose PICK_COST
# has the whole catalog (since 2026-10-25; combat_sim plays each one).
ABILITY_COST = {
    "Enhanced Health": 5,
    "Powerful Weapon": 5,
    "Powerful Spell": 5,
    "Strike (Crippling)": 5,
    "Strike (Vulnerable)": 5,
    "Poison (Bleeding)": 5,
    "Durable": 5,
    # 2026-09-30: more on-hit debuffs, so every enemy puts something on
    # the party (the designer's standard: each enemy either debuffs or
    # buffs an ally). Same 5-point cost as the existing Strike riders -
    # one stack per hit.
    "Strike (Slowing)": 5,
    "Strike (Frightening)": 5,
    "Strike (Taunting)": 5,
}

# ---- PC power per Tier (1-5) ----
# PC stat blocks moved to sample_pcs.csv (real named Stat/Skill builds -
# all 5 Stats, all 25 Skills, matching index.html's STAT_SKILLS) - see
# party.py's own module docstring for the Roster/reference-build split
# and ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the original
# derivation and every correction that went into the Roster numbers.
# This used to be four dicts here (PC_SKILLS, PC_STATS, PC_SKILLS_COMBAT,
# PC_HEALTH) - migrated out once real character sheets existed to hold
# them properly, same reasoning as sample_enemies.py's own CSV move.
# The PC_SKILLS_COMBAT-vs-PC_SKILLS smoothing rationale (avoiding a real
# player's Tier-4 "capstone" spike from swinging enemy calibration
# depending on which side of it a fight lands) still applies - it's
# baked directly into the Roster rows now rather than kept as a second
# parallel table.

# Which Stat governs each named PC Skill (index.html's STAT_SKILLS) -
# still needed by party.py to compute Skill Totals from the CSV's raw
# Stat/Skill columns, so it stays here rather than moving to the CSV
# itself (a structural fact, not a tunable number).
PC_SKILL_STAT = {
    "Melee": "Agility", "Acrobatics": "Agility", "Stealth": "Agility", "Archery": "Agility", "Brawl": "Agility",
    "Resilience": "Body", "Awareness": "Body", "Might": "Body", "Athletics": "Body", "Presence": "Body",
    "Persuasion": "Cunning", "Insight": "Cunning", "Streetwise": "Cunning", "Survival": "Cunning", "Masquerade": "Cunning",
    "Composure": "Mind", "Craft": "Mind", "Medicine": "Mind", "Academics": "Mind", "Mixology": "Mind",
    "Meditation": "Essence", "Performance": "Essence", "Rapport": "Essence", "Sorcery": "Essence", "Theurgy": "Essence",
}

# ---- PC weapons (sample_pcs.csv's `Weapon` column) ----
# Every weapon item is read from items.csv (game_data.weapon_table,
# 2026-10-27): Relevant Skills, Accuracy, Damage, Range and Weapon
# Defense, so the sim always plays the current numbers. "X or Y" takes
# the PC's better one. A blank Weapon is 1H Heavy Melee (party.py).
# The one entry kept by hand is War Magic (Lance), which isn't an item:
# War Magic (T120) is "2 + [Mind]" Fire damage, a Sorcery spell attack
# against Dodge (or Vital, chosen when learned: the Choices column), and
# Lance (F064) adds [Sorcery Skill Total] meters of range.
WEAPON = dict(game_data.weapon_table(), **{
    "War Magic (Lance)": {"skill": "Sorcery", "accuracy": 0, "damage_base": 2, "damage_stat": "Mind",
                          "range_per_skill": 1, "dmg_type": "Fire", "opp_def": "Dodge", "defense": None},
})
# Each weapon's own Defense, added to Parry when that weapon is the one
# Parried with (rulebook.md: "8 + [Weapon's relevant Skill Total] +
# Weapon's Defense"). None = can't Parry with it (bows, thrown, spells).
WEAPON_DEFENSE = {name: w["defense"] for name, w in WEAPON.items()}

# Bottled Fire's Cost (I030), for Bottomless Bottles' per-fight count
# (party.py), from items.csv.
BOTTLED_FIRE_GOLD_COST = game_data.item_gold("I030")

# Card (drawn/hand) = 2.7, THE TABEL's own established rate
# (balance_weights_notes.md) for a "discard a card" activation cost -
# used by combat_sim's own EV check for whether a Card Technique
# attempt (Cloak and Dagger, T079) is worth its cost before spending
# it, not just a design-time price to check a Technique against after
# the fact.
CARD_VALUE = 2.7

# ---- Movement mode: party formation and start distance ----
# A 2x2 block, "for simplicity's sake" per the designer, rather than the
# single-file line the enemies still use (_start_positions in
# combat_sim.py) - real formation/facing isn't modeled at all, this is
# just enough that the party's 4 positions aren't identical. spacing=2
# keeps the block tight (roughly MELEE_RANGE-sized) without stacking
# every PC on one exact point.
PARTY_FORMATION_SPACING = 2
# The party's and enemies' front lines start a random distance apart in
# this range (meters) each fight, centered in the arena - "spaced out
# slightly but not opposite ends," per the designer, replacing the
# original fixed 16m corner-to-corner start this mode shipped with.
# run_fight's own `start_gap` param can override this with a fixed
# distance instead, for a controlled before/after comparison.
START_GAP_RANGE = (6, 10)  # was (5, 10); 6-10 per the designer, 2026-10-08

# ---- TODO: PC power budget from loot - partially resolved, not fully ----
# The designer's own point: PCs get a small power bump from the loot they
# find (items/gear), same idea as ENEMY_ENCOUNTER_DESIGN.md's enemy-side
# "loot/Gold discount" (350 Gold total across 15 notional Levels, Gold÷7
# XP-equivalent, subtracted from the enemy's own stat budget before
# pricing - see that doc's "per-Level total budget" section). Real worn
# Armor (see ARMOR above and party.py's own Armor paragraph) is now
# modeled and closes part of this gap - a PC's Physical Resist is no
# longer bare Essence alone. Still missing: every other kind of gear
# (weapons beyond the base weapon_categories.csv options already modeled
# via `Weapon`, Masterwork items, Techniques) - deferred per the
# designer's original framing, same as before. If this gets picked up
# further, the enemy-side Gold÷7 XP-equivalent rate is still the natural
# starting point for whatever's still missing.

# Lie in Wait (T193): how many places a PC waits each round. Two is where
# the paper pricing peaks (Good Luck twice for 2 places).
LIE_IN_WAIT_PLACES = 2

# ---- Bleeding timing (test variants, 2026-10-07) ----
# 'own_turn' is the rule as written (glossary.md): a stack comes off at
# the end of the bearer's own turn and deals 1. 'round_end': every
# Bleeding enemy ticks once at the end of each round instead.
# 'on_damage': a damaging hit on a Bleeding enemy takes a stack off for
# 1 more Health loss; stacks still fall off at the end of its own turn,
# for nothing. Only the party's Bleeding on enemies follows this switch.
# Added 2026-10-09: 'start_turn', a stack comes off as the bearer's turn
# starts; 'on_attack', a stack comes off each time the bearer attacks (and
# at the end of a turn it didn't).
BLEED_MODE = 'own_turn'
# Test variant (2026-10-09): a Bleeding enemy at this much Health or less
# bleeds out and is Downed. 0 is off; 'stacks' means at or below its own
# Bleeding stacks; 'stacks2' the same but never above 2; 'x1/2' half its
# stacks rounded down ('x1/2up' rounded up), and so on for any fraction.
BLEED_OUT = 0
# The execute applies to every creature alike, PCs included: no Bleeding
# rule is PC-specific (designer, 2026-10-09).
# How many stacks come off at each tick, each dealing 1. 'half' is half the
# stacks rounded up, the rule since 2026-10-19 (glossary.md: "When Bleeding
# decays, remove half your stacks of it, rounded up, instead of 1"); 1 was
# the rule before it. Test variants: an int N is "up to N"; 'all' is every
# stack at once.
BLEED_TICK = 'half'
# Test variant (2026-10-16): a damaging hit on a Bleeding creature deals
# this much more, and the stacks stay. 0 is off. Every creature alike.
BLEED_WOUND = 0
# A cash-out (Reign of Blood, Open the Wound) is held until its target has
# at least this many Bleeding stacks (2026-10-16).
CASHOUT_MIN = 2
# ...and the PC holding it goes for the enemy with the most stacks.
CASHOUT_SEEK = True

# ---- Setting up a target (2026-10-28) ----
# Per the designer: Feint is only worth it "specifically aimed at setting
# up a target for the party to Gamble and wallop." With FEINT_SETUP the
# Feinter waits until at least FEINT_FOLLOWUPS allies who act before the
# target's next turn can attack it against Parry or Dodge, and a Feint
# that hits "calls" the target: those allies go for it (tactics.
# select_target) and Gamble harder on the lower Defense, as they already
# do. The call ends with the target's turn, like its Harried. Off is the
# old play: Feint on the first swing of the fight.
FEINT_SETUP = True
FEINT_FOLLOWUPS = 2
FEINT_CALLS = True  # off: the timing alone, allies pick targets as usual

# ---- Bleeding and Protected (test variants, 2026-10-19) ----
# How Protected meets Bleeding. 'ticks' is the rule (the designer,
# 2026-10-19, and glossary.md's Protected as written: Protected stops a
# tick's Health loss like any other, "If you would lose Health to
# something other than a cost..."). 'through': Bleeding's Health loss goes
# straight past Protected, what the sim did until then.
# 'apply': Protected stops stacks from being gained instead, one for one,
# after the attack's own damage has used what it needs; once a stack is on,
# it ticks through Protected. Either way it works the same on everyone.
BLEED_PROTECTED = 'ticks'
# Per the designer: a PC's leftover Bleeding at the end of a fight still
# costs its Health, ticked out under the rules above as if the turns kept
# coming. It counts toward Health left, and a PC it drops counts as Down
# after the fight (pc_downed_after), apart from Down during it.
BLEED_RESOLVE_AFTER = True
# Test riders: stacks of Bleeding every PC hit / every enemy hit adds.
PC_TEST_BLEED = 0
ENEMY_TEST_BLEED = 0
# Test: Durable (1 Protected at the start of each of its turns, up to 4) on
# every 'enemies', 'pcs' or 'both'. None is off.
TEST_DURABLE = None
# Stacks the 'Bleeding Dump' test passive adds (and the +N damage of its
# 'Damage Dump' twin).
TEST_DUMP_STACKS = 5
# Acidic Flask's numbers (I028: 5 + [Clubs] Bleeding, no damage), as dials
# for testing stronger versions.
ACID_FLASK_STACKS = 5
ACID_FLASK_DAMAGE = 0
# Stacks Furious Rage (T130) gives on each hit or Parry (test dial).
FURIOUS_RAGE_STACKS = 1

# ---- Wounded (2026-10-08) ----
# rulebook.md: you lose Shallow Health first, then Deep; while all your
# Shallow Health is gone you're Wounded (Bad Luck on all flips, -2 to all
# Defenses and Speed). Every sample PC has the base 5 Shallow (Toughened
# Body adds Deep). The sim keeps one `health` number and tracks Shallow
# alongside it (tactics.sync_wounded). WOUNDED_RULES off still tracks it
# for the calibration counts, but applies no penalties and keeps the old
# half-Health trigger for heals.
BASE_SHALLOW_HEALTH = 5
WOUNDED_RULES = True

# ---- Retargeting after a kill (2026-10-08) ----
# A PC that kills its target mid-turn has to walk to the next one before
# attacking it. Off reproduces the old behavior (it attacked the new
# target from wherever it stood, ~2% of PC attacks out of range).
RETARGET_RANGE_FIX = True

# ---- Line of sight (2026-10-08) ----
# Per the designer: there are some line-of-sight issues, not many, and
# whether an archer has to move to get a shot is about a coin toss -
# sometimes they can sit back and double attack all fight. Modeled as:
# half of fights are cluttered; in a cluttered fight, a ranged attacker
# (either side) that hasn't moved this turn spends a move action
# repositioning half the time (combat_sim._los_blocked).
LINE_OF_SIGHT = True
LOS_CLUTTERED_FIGHT_CHANCE = 0.5
LOS_BLOCKED_TURN_CHANCE = 0.5

# ---- Play styles (2026-10-08, play_styles.py) ----
# Per the designer: tanky PCs dive in, fragile ones hang back, some sit
# in between. sample_pcs.csv's Play Style column (Diver, Skirmisher,
# Back-liner); off makes every PC a Diver (the old behavior).
PLAY_STYLES = True
BACKLINE_KEEP_AWAY = 3   # spaces a ranged Back-liner keeps from every enemy
# Brace (T001) with AP left at the end of a turn: only when an enemy is
# this close, near enough to reach this PC next round (2026-10-24).
BRACE_THREAT_RANGE = 6
# Warmage's Reserves regains the best spent War Magic copy instead of a
# plain cast (2026-10-24). Off reproduces the older runs exactly.
RESERVES_REGAIN_BEST = True
# Warmage's Reserves by its own text and encounter.py's rule (2026-10-27):
# regains the best spent Sorcery use of Level [X + 1] or less, a Club
# counting double, instead of the hand-picked copy above.
RESERVES_BY_LEVEL = True
# Blood-Powered Spirit (T006) pays Health only while the PC keeps this
# share of its max Health after paying (2026-10-27, my reading of how a
# player would ration it).
BLOOD_SPIRIT_HEALTH = 0.5
RECKLESS_CHANCE = 0.05   # share of turns any PC plays like a Diver anyway

# ---- How the Assassin tactic reads "squishy" (2026-10-08 test) ----
# 'current': whoever has the least Health right now (finishes off the
# hurt). 'looks': whoever looks squishiest - lowest max Health, then
# lightest armor - the designer's own wording for the tactic. 'hurt'
# (2026-10-28): the lowest share of max Health, ties to the squishiest
# looking, then chance. Under 'current' everyone at full Health ties and
# the party's list order picks, so a Technique that takes a point off a
# PC's max Health makes every Assassin go for that PC instead (the broad
# pass, results/TECHNIQUE_PASS.md).
ASSASSIN_READS = 'softest'
# How a Kiting enemy moves: 'engaged' (designer, 2026-11-05: it backs off
# only from a PC in melee reach; otherwise it closes to range and attacks
# twice like anyone else) or 'always' (a move action away from the closest
# PC every turn, as first coded: it halved a kiter's attacks and made any
# monster nearly harmless).
KITING_MOVE = 'engaged'
# Hexer tests (2026-11-05), both off: a Hex's stacks last the fight
# (HEX_PERSIST), and a Hex also lands on every PC within this many meters
# of its target (HEX_AREA; 0 for none).
HEX_PERSIST = False
HEX_AREA = 0
# A solo boss's Health in the pruned v3, in standard enemies. 6 on budget
# x1 (2026-11-05); 4 since it got twice the budget (designer, 2026-11-06:
# the solo boss is a rare, melee exception; boss fights are led by elites).
# As dangerous as 6 was, in 4.3 rounds instead of 7.
# 5 since 2026-11-09: on the hit-target table (small Health) a boss fight
# was no harder than four standard monsters (experiments: day1109_*).
V3_SOLO_HEALTH = 5
# A big enemy's Ability budget, in times a standard enemy's, by Slots
# (pruned v3; designer, 2026-11-06). Each point then costs its Health over
# k, so an enemy that spends nothing keeps the same Health. The extra goes
# down the row's BigPicks, offense only (sample_enemies.BIG_PICKS_BARRED).
# {} = 1 for all (the old path).
V3_SLOT_BUDGET = {2: 2, 4: 2}
# An elite's (2 Slots) Health in the pruned v3, in standard enemies: 3 on
# budget x1; 2.5 with twice the budget (2026-11-06), an elite beside two
# standard monsters about an ordinary fight.
# 3.5 since 2026-11-09, as the solo boss's 5.
V3_ELITE_HEALTH = 3.5
# Abilities an elite or solo boss can't take at all (designer, 2026-11-07):
# the ones that ignore, shed or block what the party does to it. Priced on
# standard enemies; on one that lives two or three times as long each
# adds about 2 points of losses for 0-1 points, all three 10
# (experiments/enemies/elite_debuff_picks.py); Omniguard alone was most of
# the Black Knight's slog (black_knight_pieces.py). () = none.
V3_BIG_BARRED = ("Omniguard", "Resilient", "Durable")
# Elemental-Forged Weaponry on a sample character's sheet (2026-11-07,
# designer: give some sample characters an elemental attack, the game's
# answer to heavy armor). False ignores the item (the old party).
PC_ELEMENTAL_WEAPON = True
# A minion's (0.5 Slots) Health in the pruned v3, in standard enemies (the
# old SLOT_MULTIPLIER's third until tested otherwise, 2026-11-06).
V3_MINION_HEALTH = 1 / 3
# The old sample roster (sample_enemies.csv) has no BigPicks, so its big
# enemies keep the settings they were built with.
LEGACY_BIG = {"V3_SLOT_BUDGET": {}, "V3_ELITE_HEALTH": 3, "V3_SOLO_HEALTH": 6}
# The Defense cap (designer, 2026-11-06): no enemy Defense above 8 + its
# Level's Skill + this, before gear (armor's Dodge penalty after; Parry,
# which nothing but its weapon raises, never reaches it). It ended the Defender walls (experiments/enemies/defense_cap.py).
# None = no cap.
# 1 since 2026-11-09: on the hit-target table, Defenders at Skill +2 were
# walls (two Black Knights 9.6% lost over 9 rounds, four Iron Sentinels
# 14% over 12); at +1, 4.1% and 4.4%, ordinary fights unchanged
# (experiments/enemies/wall_fix.py).
V3_DEFENSE_CAP = 1
# With it, the Defender archetype's +2 Parry becomes Health +1 (Defender:
# Dodge +2, Health +4); the cap would waste the Parry under a shield.
V3_DEFENDER_PARRY_TO_HEALTH = True
# Paper defenses (designer, 2026-11-06): Parry is 8 + the Level's Skill +
# the main Action's weapon Defense, nothing else. Archetypes and Abilities
# never raise it (Parry and Dodge +1 reads as Dodge +1), and an enemy whose
# main Action isn't a weapon (a caster, a healer) has no Parry even with a
# fallback weapon. With V3_DEFENSE_CAP this puts every limit on the
# ability step: no Defense above the Level's 8 + Skill + 2.
V3_PAPER_DEFENSES = True

# ---- Enemy offense dials (2026-10-08, measurement only) ----
# Flat changes to every enemy's Accuracy and attack damage, applied to
# the fight's own copies in run_fight - for sizing the gap between the
# sim's encounters and the designer's table, not a design change.
ENEMY_ACCURACY_ADJ = 0
ENEMY_DAMAGE_ADJ = 0
# Every enemy's Health times this, rounded up (2026-10-09, measurement
# only, same idea as the offense dials).
ENEMY_HEALTH_MULT = 1
# Every sample enemy built this many Levels above its own row's Level,
# through the same PC-style builder (sample_enemies.get_enemy). The
# designer's yardstick for a harder day (2026-10-30): the enemy Levels the
# model already has, read as win rates, no fractional steps. 0: as written.
ENEMY_LEVEL_UP = 0
# The enemy base table: 'v2' (designer, 2026-11-02: "our new one we're
# working off of"), shaped like the designer's original table
# (enemy_builder_pcstyle.ENEMY_TABLE_V2); 'v1' the one before, kept for
# older scripts and their recorded numbers; 'v3' (2026-11-03) built the way
# PCs are (enemy_builder_pcstyle.build_enemy_v3), the default since the
# designer adopted it the same day. Only the codified rows (StrongDefense)
# read it.
ENEMY_TABLE = 'v3'
# v3 (2026-11-03, the designer's "enemies play by the players' rules"):
# Defense tiers. Strong = the Level's attack Skill Total, Average = that
# minus V3_DEF_GAP, Weak = minus twice it (enemy_builder_pcstyle.build_enemy_v3).
V3_DEF_GAP = 2
# Which v3: 2, the trimmed base with the bigger archetypes (adopted
# 2026-11-03); 1, the first one (one more Skill and Accuracy, smaller
# archetypes), for the numbers recorded before that; 3, the pruned one
# (2026-11-04: Damage and Accuracy into the Ability budget, additive
# archetypes, the rows' PrunedPicks added), the default since the designer
# adopted it on 2026-11-04.
V3_VERSION = 3
# Ability shapes under v3: 'catalog' (as written: Poison (Bleeding) lands
# 2 stacks, Retribution Aura answers every attacker) or 'v2' (the v2 kit's
# 1 stack and melee attackers only). 'v2' since 2026-11-03: as written they
# read about 5 and 15 enemy Health, too much to price as one Ability.
V3_KIT_SHAPES = 'v2'
# Draft v3 Ability prices in Health (enemy_builder_pcstyle.ABILITY_HEALTH_V3):
# on, each enemy gets V3_ABILITY_ALLOWANCE Health per Slot of Abilities and
# armor free, and pays or keeps the difference in Health. On since
# 2026-11-03 (designer: "start ironing out the Ability budget... at least
# in terms of Health"); the prices get a second look against the balance
# weights.
V3_ABILITY_PRICES = True
V3_ABILITY_ALLOWANCE = 1
# The pruned v3's budget (V3_VERSION = 3): the 1 above, plus 4 for the
# Damage Stat and 2 for the Accuracy the base table gave up.
V3_PRUNED_ALLOWANCE = 7
# What the pruned v3's rows spend it on: 'picks' (a redesigned row's
# PrunedAction and PrunedPicks; any other row keeps its Abilities and buys
# back Damage +1 and Accuracy +1) or 'buyback' (every row buys them back:
# the old enemies with the new archetypes).
V3_PRUNED_ROSTER = 'picks'
# Extra budget by Level for the pruned v3 ({3: 2} gives Level 3 enemies 2
# more points), spent down each redesigned row's PrunedExtra list.
# Tuned 2026-11-04 (pruned_tune.py, results/enemy_stats/v3p_tune.txt):
# Level 1 one point less, Levels 3-5 two more spent on offense first
# (6 / 7 / 9 / 9 / 9); then a point more everywhere, the designer wanting
# it a little more dangerous since real players coordinate and have items
# (v3p_danger.txt): 7 / 8 / 10 / 10 / 10. Then a point more at Levels 2-5
# (2026-11-05) to win back what the Defender's Health +3 took off:
# 7 / 9 / 11 / 11 / 11. Then a point more everywhere (designer,
# 2026-11-07) to win back the danger the Defense cap and the elemental
# weapons took off: 8 / 10 / 12 / 12 / 12 (experiments: manual_check.py
# --extra; results/enemy_stats/nudge_*).
# Then (2026-11-08, in pencil) the Accuracy +1 everyone bought from Level 2
# went into the table: 8 / 8 / 10 / 10 / 10, and the extra points no longer
# start with Accuracy from Level 2 (V3_ACCURACY_IN_TABLE).
# Level 3 a point fewer (designer, 2026-11-09): its baseline Health went
# 5 -> 7 so Health never steps down between Levels, and the point pays for
# it so Level 3 isn't harder, just steadier. Then a second point, so
# Levels 1-3 all get 8 (designer, same day): 8 / 8 / 8 / 10 / 10.
V3_PRUNED_EXTRA = {1: 1, 2: 1, 3: 1, 4: 3, 5: 3}
V3_ACCURACY_IN_TABLE = 2
# 'row' spends extra points down the row's PrunedExtra; 'offense' on
# Accuracy +1, then Damage +1, first.
V3_PRUNED_EXTRA_ORDER = 'offense'
# Loadout swaps on the redesigned rows, for experiments ({"Bow": "Heavy Bow"}).
V3_PRUNED_SWAP = {}
# The least of the table's Health an enemy can keep after paying for
# Abilities and armor (0 lets experiments spend it all). Unused under
# V3_ONE_BUDGET, where nothing can come out of Health.
V3_HEALTH_FLOOR = 2 / 3
# One budget (designer, 2026-11-07): armor, loadout and picks all come out
# of the Level's points, the extra points buy only what the design leaves
# room for, and a design can't spend past its budget out of Health (no
# floor). What's left is Health, as before. False: the base design and the
# extra points are separate pots and an overspend comes off Health.
V3_ONE_BUDGET = True
# The lowest Level an enemy can wear Heavy armor; below it a Heavy design
# wears Medium and keeps the points as Health (designer, 2026-11-08:
# shorter, safer Heavy fights at Levels 1-2; heavy_level3.py). None: any Level.
V3_HEAVY_MIN_LEVEL = 3
# The enemy Resist Stat's cap (None: STAT_CAP, 5, as a PC's), for the
# hit-size targets' tests (2026-11-08, experiments/enemies/hit_fit.py).
V3_RESIST_CAP = None
# The hit-target table (2026-11-08 candidate, off by default): enemy
# Defense and Resist up to PC-like numbers, Health down so a standard
# monster has about 8, so PCs hit 50-75% for 2-3 and enemies 25-50% for
# 2-3 (experiments/enemies/hit_fit.py). In pencil since 2026-11-09 (the
# designer's firm hit targets); False: the 11-08 table.
V3_HIT_FIT = True
# Experiments: {Level: changes} replacing that Level's row of the candidate
# (enemy_builder_pcstyle.V3_HIT_FIT_TABLE), or as SIM_SET can carry it,
# "2:skill=1/resist=3/health=5;4:skill=3".
V3_HIT_FIT_OVERRIDE = {}
# Experiments: deltas on the final table, "1:accuracy=3/health=-2;2:...".
V3_TABLE_NUDGE = ""
# The squared table (enemy_builder_pcstyle.V3_SQUARE_TABLE), in pencil
# since 2026-11-09: enemy Accuracy +2/+3 so enemies hit about half the time.
V3_SQUARE = True
# Every enemy's Fighting Style, for tests (2026-11-09): '' each row's own
# (all 'None' today: up to two attacks); 'Aimed Shot' (one attack with
# Good Luck); 'Skirmisher' (one attack, then falls back with the AP left);
# 'mixed' (ranged: Aimed Shot; melee: Skirmisher).
# Default 'mixed' since 2026-11-09 (designer: two attacks a round caused
# most of the spikes; a two-attack style may come back per monster).
V3_FIGHTING_STYLE = 'mixed'
# Per-PC counters for party_power's scorecard (2026-10-30): enemy Health
# lost on each PC's own turn (dmg_out), Health it restored to the party
# then (heal_out), Health lost and times hit on enemy
# turns (dmg_in, hits_in). Snapshots only, no random calls, so on or off
# the fights play the same.
TRACK_SHARES = False
# Healing Magic as an Encounter Technique (2026-11-01, the designer's test;
# techniques.csv doesn't have the tag). 0: as written, a cast whenever the
# cards allow. 1: one use per copy a fight, the after-fight care as before
# (the use is back once the encounter ends). 2: also one use per copy in
# the care after each fight.
HEALING_MAGIC_ENCOUNTER = 0

# ---- Real cards (2026-10-09, cards.py) ----
# Every PC has its own 52-card deck and a hand; the GM has one deck for
# all enemies. Flips are real cards, the suit pool is real (a card
# matching the attack's Skill suit is +1 damage), and hand cards rescue
# misses, back Gambles and pay for card Techniques. Off falls back to the
# old stand-ins (uniform 1-13 flips, no suit pool, flat use counters).
CARDS = True
# Per the designer: two fights a day, and a player commits about a third
# (a quarter to a third) of the day's hand to a fight.
CARDS_FIGHT_SHARE = 1 / 3
CARDS_SECOND_FIGHT_SHARE = 0.5
# The whole day's hand as one pool (designer, 2026-11-09: track the
# party's resources across the day's two fights and let them use
# everything in the first if they need it). In a day's first fight a PC
# holds back CARDS_FIGHT_SHARE of the morning's hand for the second and
# can spend the rest; the hold comes free for the whole party once the
# fight turns (someone Down, or the party under DAY_TROUBLE of its
# Health), and for a PC's own big or killing flip. The second fight has
# the whole hand left. False: a fight's budget is CARDS_FIGHT_SHARE of
# the morning's hand, as before.
DAY_CARDS = True  # default since 2026-11-09
DAY_TROUBLE = 0.5
# Fixes from the 2026-11-09 audit of the sim against the rules (an agent's
# read, each checked): PCs' Bad Luck stacks (rulebook.md "Bad Luck works
# the same"); a PC's Health stops at 0 when Downed ("Numbers don't go
# negative") and a heal back up restores a Deep point first; an enemy
# grappling can't swing a two-handed weapon (it lets go to attack); Area
# Attack's splash still lands when the main target drops; a Downed PC
# doesn't hand out potions between fights; a support's one action isn't
# Aimed Shot; a Skirmisher pinned at the edge slides along it; the fight's
# healer heals a Downed ally back up. False: the
# old behavior, for comparison.
AUDIT_FIXES = True
# Which enemies the shared test fights use (sample_enemies.CURRENT_MIXES,
# so day_sim, calibrate, effect_check, compare_builds and the rest).
# 'manual' (designer, 2026-11-09: the manual is the one set of enemies for
# every test): MANUAL_MIXES encounters drawn from monster_manual.csv by the
# variety rules (sample_enemies.manual_encounters: 4 Slots, two or three
# stat blocks, at most one non-attacker, no solo boss), named "Manual 1"..,
# a separate draw at each Level. 'roster': the old four mixes (Frontline,
# Shield Wall, Warband, Horde), for comparison with older numbers.
ENCOUNTER_SOURCE = "manual"
MANUAL_MIXES = 8
# Cards a player keeps back after a rescue, by how much the flip matters
# (combat_sim's NORMAL/FOCUS/BIG/KILL): a plain hit only gets a card when
# there are plenty left; a kill shot or an Encounter attack gets one
# whenever there's one to give.
RESCUE_RESERVE = {1: 2, 2: 1, 3: 0, 4: 0, 5: 0}
# A healer keeps one Healing Magic cast's worth of cards (its Level) out
# of attack rescues and kill top-ups, its own or an ally's (2026-10-26).
# Off, Hanforth spent about 2.4 cards a Level 1 fight on attacks and under
# 1 on healing.
HEALER_KEEPS_CARDS = False
# A caster with a shaped War Magic copy (Furrow, Funnel, Nova) steps in to
# catch two or more enemies with it (play_styles.plan_shape, 2026-10-26).
# Off, Beornhard (L3) cast his Furrow copy 0.2 times a fight.
SHAPE_SETUP = False
# Range checked before every attack in a PC's turn, not just the first
# (2026-10-27): a Wind Slash attack or a Push mid-turn used to leave the
# next attack going off from out of reach.
RECHECK_RANGE = True
# Party tactics (party_tactics.py, 2026-10-27): None plays every PC by its
# own Play Style column; a preset name ("cautious", "max range+focus fire")
# hands out styles by role and sets its own switches.
PARTY_TACTIC = None
KITE_KEEP_AWAY = 6     # a Kiter keeps this far from every enemy (or reach - 1)
HOLD_RANGE = 8         # a Holder waits while a melee enemy this close is on its way
GUARD_RADIUS = 2       # a Guardian fights what's within this of its ward
GUARD_LEASH = 6        # ...and stays by the ward while a melee enemy within this is coming
# Wind Slash ("the chosen weapon's range is increased by [twice X]")
# gives a melee weapon reach too, per the designer (2026-10-27).
WIND_SLASH_MELEE = True
# An ally can throw a card onto someone else's kill shot ("the party
# talks"); the rulebook lets you play cards on an ally's flip.
CARDS_ALLY_RESCUE = True
# "Knowing they hold a queen, they may Gamble once or twice" (designer).
BACKED_GAMBLES_MAX = 2
# Perfect Strike gets thrown with a low card, one that's no good for a
# rescue anyway, unless the hand is deep.
PERFECT_STRIKE_MAX_RANK = 7
# Hand of Chaos's Sift 1 keeps a card this high, discards anything lower.
SIFT_KEEP_RANK = 7
# Enemies attack with Accuracy, not a Skill, so the rules give them no
# suit. Per the designer (2026-10-09), for now: an enemy's damaging attack
# deals +1 damage for each Heart in its flip, the same as a suit match;
# something more detailed may come later. False gives them no suit.
ENEMY_SUIT_EXTRA = True

# ---- Fleeting (2026-10-09) ----
# glossary.md [Fleeting]: "If you had no stacks of a Fleeting effect
# right before gaining some, skip the next removal that would apply to
# it." In the rules since 2026-08-29; the sim decayed every stack at the
# next turn end. Protected is Fleeting too, and the sim never decayed it.
# Per the designer (2026-10-09): the skip is only for an effect gained
# during the bearer's own turn (a player putting Protected on themselves
# shouldn't lose a stack at the end of that same turn), and Bleeding
# never skips, so it always deals its damage. Harried is exempt too: it
# just clears at the end of the turn. 'own_turn' is that rule, with
# FLEETING_SKIP_EXEMPT; True (every fresh effect skips, Bleeding
# included: the glossary read literally) and False (no skip) stay for
# measuring.
FLEETING_SKIP = 'own_turn'
FLEETING_SKIP_EXEMPT = ('bleeding',)  # 'own_turn' only; Harried never goes through the skip at all
PROTECTED_DECAYS = True

# rulebook.md: "For attacks that deal damage, only weapon attacks can be
# Gambled on - spell attacks can't." The sim let War Magic Gamble until
# 2026-10-09; off reproduces that.
NO_SPELL_GAMBLES = True

# ---- The effect check (2026-10-21, effect_check.py) ----
# Whether the party's threat rating (tactics.enemy_threat) takes an
# enemy's Crippled stacks off its hit chance, so a Crippled enemy gets
# left for later. THE TABEL's Crippled weight assumes that ("a creature
# Crippled hard enough stops being a threat and gets left alive on
# purpose"); off is how the party has always picked targets.
THREAT_READS_CRIPPLED = False

# Whether Stagger / Outflank count only living creatures as places
# (glossary.md: "its position in turn order moves down that many
# places"). The dead stay in run_fight's order list, and until
# 2026-10-21 they counted, so about a third of a Stagger's places went
# past the dead. Off reproduces that.
SHIFT_SKIPS_DEAD = True


# A run can set any of these without editing this file:
# SIM_SET="HEALING_MAGIC_ENCOUNTER=1,TRACK_SHARES=True" python3 ...
# (pool workers inherit the environment, so they get it too).
def _env_overrides():
    import ast
    import os
    for item in filter(None, os.environ.get("SIM_SET", "").split(",")):
        k, v = item.split("=", 1)
        if k.strip() not in globals():
            raise KeyError(f"SIM_SET names {k.strip()!r}, which tunables.py doesn't have")
        globals()[k.strip()] = ast.literal_eval(v.strip())


_env_overrides()
