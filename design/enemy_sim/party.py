"""
Loads PC stat blocks from sample_pcs.csv - real named Stat/Skill builds
(all 5 Stats, all 25 Skills, matching index.html's own STAT_SKILLS),
not one abstract number per Tier. Same Roster/reference split as
sample_enemies.csv:

- **Roster** (`Roster` column TRUE) - exactly one per Tier 1-5, "Baseline
  Tier N Party Member." This is `tunables.py`'s old PC_SKILLS_COMBAT (the
  smoothed variant) migrated into full character-sheet form - see
  ENEMY_ENCOUNTER_DESIGN.md's Analysis section for the derivation, and
  the smoothing rationale (avoids PC_SKILLS' real Tier-4 capstone spike
  swinging enemy calibration depending on whether a fight lands before or
  after it). `make_party(tier)` pulls this row and duplicates it x4 -
  still 4 identical party members, no distinct roles, no Techniques or
  items layered on top, no gear-based Resist bonus (just raw Essence).
- **Reference builds** (`Roster` FALSE) - named Level 1 characters, one
  leaning into each of the 5 Stats, built to rulebook.md's own Quick
  Creation Reference shape (2 Skills@3, 5@2, 2@1; 1 Stat@3, 2@2, 2@1) and
  verified to cost exactly 57 XP in Skills+Stats (75 total chargen
  budget minus 18 XP/6 Levels of Techniques, which aren't modeled here).
  `get_pc(name)` pulls these by name; `make_party_of(name)` duplicates
  one x4 into a full party, for testing a single build's own attack
  profile against the validated Roster; `make_party_from([names])`
  assembles a custom 4-person mix instead, for testing party
  composition itself (see combat_sim.py's own note on what both showed).
  Melee-attacking: Hilde, Browndog, Carrick, Jackal, Felix (Felix,
  Essence-primary with barely any Melee, reads as a weak attacker
  despite being a coherent character on paper - see the Weapon
  paragraph below for why, and Wren for the same Essence-primary
  concept actually built to attack through Sorcery instead).
  Ranged-attacking (see `Weapon` below): Sable (Archery/Light Bow), Rook
  (Acrobatics/Light Thrown), Wren (Sorcery/War Magic + Lance).
  Support: Beornhard (weak Melee attacker, solid Theurgy - see
  `Support` below).

**`Weapon`** (blank for most rows) switches which Skill/Stat combo
governs a PC's own attack roll, Damage, damage type, opposed Defense,
and attack range - a real capability this sim didn't have originally,
when every PC's attack was hardcoded to Melee/Physical regardless of
build. A blank cell keeps that original 1H Heavy Melee default (Melee
Skill Total, Damage = 4 + Body, Physical, opposed by Parry/Dodge, no
attack_range - falls back to `MELEE_RANGE` under `movement=True`); a
name from `tunables.WEAPON` (`"Light Bow"`, `"Light Thrown"`, `"War
Magic (Lance)"`) switches to that weapon's own real numbers - see
`tunables.WEAPON`'s own comment for the weapon_categories.csv/
features.csv sourcing, including why War Magic's damage is Fire (so it
draws on a target's `elemres`, not `physres` - see combat_sim.
enemy_resist_for_pc_attack) and opposed by Dodge alone rather than
Parry/Dodge. This is fully decoupled from
parry/dodge/bodily/mental/vigilant, which always come from
Melee/Acrobatics/Resilience/Composure/Insight regardless of `Weapon` -
a War Magic caster's Sorcery Skill Total drives their own attack and
Range without touching their (separately tracked) Parry.

**`Support`** (`TRUE`/blank) flags a PC who spends *some* of their turns
healing an ally instead of attacking - a hard-capped resource, not a
per-round coin flip, so a support PC still fights their own weapon
attack most rounds rather than sitting idle. Translated here into
`strategy="support_healer"` (`"attacker"` otherwise) - a name from
`tactics.PC_STRATEGIES`, the pluggable-"AI" registry combat_sim.py
dispatches every PC's turn through (see tactics.py's own module
docstring for the pattern and why it exists - adding a future strategy
means writing one function and registering it there, not adding a new
boolean CSV column and a matching `if` in combat_sim.py). `heal_uses_left`
(every PC dict, not just Support ones) is `hand_size // 4`, `hand_size`
being rulebook.md's own "Cards Per Day"/Draw Cycle formula (twice
Cunning plus Mind) standing in for how many cards this PC carries into
a fresh encounter - one use of Healing Magic at Level 1 costs 1 card,
so a quarter of a full hand caps how many times they can afford to cast
it in one fight. `tactics.strategy_support_healer` spends a use (and
only a use) once a living ally drops to half Health or below - "if
necessary, ESPECIALLY if wounded" (the designer's own framing) reads as
"only when it's actually needed," given how few uses there usually are
- approximating T105 Healing Magic, 1 Shallow Health + 1 more since the
discarded card is assumed to always be a Heart (cards.chosen_matches -
a player choosing from their whole hand, not flipping blind, on a cost
that's only ever a quarter of it). See combat_sim.py's own docstring
for what all of this showed. Doesn't change anything else in this file
- `strategy`/`heal_uses_left` just get threaded onto the PC dict for
tactics.py/combat_sim.py to read.

**`Armor`** (`Unarmored`/`Light`/`Medium`/`Heavy`, blank = `Unarmored`)
is the real armor_categories.csv table (`tunables.ARMOR`, shared with
enemy_builder.py - see its own comment), applied the same way on both
sides: Physical Resist gets the armor bonus, Dodge/Speed take the
penalty, elemental Resist (`elemres` - Fire/Frost/Brilliant/Shadow, one
pool in this sim) stays Essence-only regardless of Armor. Every
existing row defaults to Unarmored (bare Essence Physical Resist, no
Dodge/Speed change) unless its `Armor` cell says otherwise - see each
row's own Notes for why that tier was picked (usually: does this
character's Might Skill Total actually clear that armor's real
Might Requirement, per weapon_categories.csv - not mechanically
enforced here, just used as the judgment call for which tier reads as
plausible for that build).

Every Stat/Skill/Defense formula here is straight from rulebook.md:
- Defense = 8 + [governing Skill Total], plus Armor's Dodge penalty for
  Dodge specifically
- Weapon Damage = 4 + Body (Heavy 1H Melee formula, weapon_categories.csv)
  unless `Weapon` names a ranged option (see above)
- Resist starts equal to Essence (rulebook.md's Calculated Statistics:
  "Resists... starts equal to your Essence"); Physical Resist then adds
  Armor's own bonus, elemental Resist (`elemres`) doesn't
- Speed = 1 + Agility (rulebook.md's Calculated Statistics), plus
  Armor's Speed penalty - only used by combat_sim.py's optional
  movement mode (run_fight(..., movement=True), see movement.py);
  ignored entirely otherwise, same as before Armor existed.
"""
import csv
import math
import os
import tunables as T
import play_styles

# Encounter Techniques that replace a normal attack, from techniques.csv.
# Each builds the attack profile combat_sim's attack loop overlays for
# one use: (stats, skills, weapon Skill Total, weapon Damage) -> profile.
# `effect` is what a hit puts on the target: (key, stacks, bonus suit),
# the suit adding 1 more stack when it's flipped.
def _unarmed_vs_mental(effect=None):
    # Shugen School weapon strikes: "Make an Unarmed weapon attack against
    # the target's Mental Defense. If it hits, it deals Brilliant damage"
    # - the PC's own Unarmed attack, redirected. Assumes the PC's Weapon
    # is Unarmed, which holds for every row that knows one.
    return lambda st, sk, atk, dmg: dict(skill_total=atk, damage=dmg, dmg_type="Brilliant",
                                         opp_def="Mental", effect=effect, skill="Brawl", weapon=True)


# `skill` is the attack's Skill, for its suit (cards.SKILL_SUIT); `weapon`
# marks a weapon attack, the only kind that can be Gambled on
# (rulebook.md). `big` marks an Encounter attack, worth a card to land.
TECH_ATTACKS = {
    # T154, Level 2, 2 AP: "...and the target is Slowed 2 + [Spades] times."
    "Hand Rings the Bell": _unarmed_vs_mental(("slowed", 2, "Spades")),
    # T080, Level 1, 2 AP: "Make a Meditation attack against the target's
    # Mental Defense. If it hits, it deals 2 + [Mind] Brilliant damage."
    "Firefly Leaves the Hand": lambda st, sk, atk, dmg: dict(
        skill_total=skill_total(st, sk, "Meditation"), damage=2 + int(st["Mind"]),
        dmg_type="Brilliant", opp_def="Mental", effect=None, skill="Meditation"),
    # T159, Level 2, 2 AP (Felix): "Make a Meditation attack against the
    # target's Vital Defense. If it hits, it deals 2 + [Mind] Shadow
    # damage, and you may discard a card to heal 3 Health." The heal is
    # taken when he's missing 3 or more (designer, 2026-10-09).
    "Thief Empties the Vessel": lambda st, sk, atk, dmg: dict(
        skill_total=skill_total(st, sk, "Meditation"), damage=2 + int(st["Mind"]),
        dmg_type="Shadow", opp_def="Vital", effect=None, skill="Meditation", heal_on_hit=3),
    # T111, Level 2, 2 AP: "Make a Theurgy spell attack against the
    # target's Mental Defense. If it hits, they are Crippled 5 + [Clubs]
    # times." No damage.
    # War Magic (T120) at Level 2 with Lance, Sanguine and Destructive x1
    # (Beornhard's Bleeding variant, 2026-10-09): "deals an extra 3
    # damage. If it would cause the target to lose Health, instead they
    # gain that many stacks of Bleeding + [Clubs] stacks", +1 from
    # Destructive. combat_sim converts the hit's damage on landing.
    "Sanguine War Magic": lambda st, sk, atk, dmg: dict(
        skill_total=skill_total(st, sk, "Sorcery"), damage=2 + int(st["Mind"]) + 3 + 1,
        dmg_type="Fire", opp_def="Dodge", effect=None, skill="Sorcery", sanguine=True),
    "Reckoning": lambda st, sk, atk, dmg: dict(
        skill_total=skill_total(st, sk, "Theurgy"), damage=0,
        dmg_type=None, opp_def="Mental", effect=("crippled", 5, "Clubs"), skill="Theurgy"),
}

# Ranged hexes cast at the start of a turn by combat_sim._try_hexes (not
# swapped in for a weapon attack): Enith's War Magic (T120) Level 1
# copies, each Tormenting Curse ("deals no damage", +3 points) plus Lance
# ("Increase the Range... by [Sorcery Skill Total] meters", the same
# range the sim gives Beornhard's Lance) and the rest on one effect
# (designer, 2026-10-09). War Magic is learned against Dodge or Vital;
# per the designer, she split them: Sloth against Dodge, Rebuking against
# Vital. Each is (kind, amount, bonus suit, Defense): Frigid x3 is "Slowed
# [twice X] + [Spades] times", Kinetic x3 is "Pushed up to [four times X]
# + Spades meters".
HEXES = {
    "Hex of Sloth": ("slowed", 6, "Spades", "Dodge"),
    "Hex of Rebuking": ("push", 12, "Spades", "Vital"),
}

_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_pcs.csv")


def _load_rows():
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def skill_total(stats, skills, skill):
    stat = T.PC_SKILL_STAT[skill]
    return int(stats[stat]) + int(skills[skill])


def _pc_dict(row, index, good_luck):
    stats = {s: row[s] for s in ("Agility", "Body", "Cunning", "Mind", "Essence")}
    skills = {k: v for k, v in row.items() if k not in
              ("Name", "Tier", "Agility", "Body", "Cunning", "Mind", "Essence", "Health", "Roster", "Notes",
               "Weapon", "Support", "Armor", "Pronouns", "Card Techniques", "Weapon Uses", "Heal Cards", "Heal Bonus",
               "Heal Range", "Passives", "Battle Tactic", "Parry Weapons", "Encounter Techniques",
               "Defense Choices", "Play Style", "Maneuver Features", "Bottles Item")}
    parry = 8 + skill_total(stats, skills, "Melee")
    # Raw Acrobatics Skill Total - captured before Armor's own Dodge
    # modifier folds into `dodge` below, since Blinkstep (T077, "Shift
    # up to [half your Acrobatics Skill Total] meters") needs the real
    # Skill Total itself, not Dodge (which isn't the same number for
    # anyone in anything but Unarmored/Light Armor - Medium/Heavy's own
    # -1 would otherwise silently leak into a PC's Shift distance too).
    acrobatics_skill_total = skill_total(stats, skills, "Acrobatics")
    # rulebook.md: "you choose Acrobatics or Brawl" for Dodge - the sim
    # used Acrobatics alone until 2026-10-08, shortchanging Brawl builds
    # (Felix, Hanforth).
    dodge = 8 + max(acrobatics_skill_total, skill_total(stats, skills, "Brawl"))
    # Stealth Skill Total - no Defense formula reads Stealth at all (it
    # isn't a Defense-governing Skill the way Melee/Acrobatics/
    # Resilience/Composure/Insight are), so unlike acrobatics_skill_total
    # above there's no existing "+8" field to derive it from - Cloak and
    # Dagger (T079, "Make a Stealth attack against the Vigilant Defense")
    # needs it exposed directly.
    stealth_skill_total = skill_total(stats, skills, "Stealth")
    bodily = 8 + skill_total(stats, skills, "Resilience")
    mental = 8 + skill_total(stats, skills, "Composure")
    vigilant = 8 + skill_total(stats, skills, "Insight")
    health = int(row["Health"])
    speed = 1 + int(stats["Agility"])  # rulebook.md: "Your Speed is equal to 1 + your Agility"
    reflex = skill_total(stats, skills, "Insight")  # rulebook.md: "Your Reflex is equal to your Insight Skill Total"

    # Resist "starts equal to your Essence" (rulebook.md), and worn
    # Armor adds to Physical Resist specifically (armor_categories.csv,
    # T.ARMOR - the same real table enemy_builder.py already uses).
    # elemres (Fire/Frost/Brilliant/Shadow, one pool in this sim) is
    # Essence alone on both sides - no armor contribution, matching
    # armor_categories.csv's own "Physical Resist" column name. Armor's
    # Dodge/Speed penalty apply the same way here - a blank `Armor` cell
    # defaults to Unarmored (T.ARMOR's own all-zero baseline), so an
    # existing row with no Armor set reads exactly as it used to (raw
    # Essence, no Dodge/Speed change) rather than silently changing.
    armor = (row.get("Armor") or "Unarmored").strip() or "Unarmored"
    armor_mod = T.ARMOR[armor]
    physres = int(stats["Essence"]) + armor_mod["physres"]
    elemres = int(stats["Essence"])
    dodge += armor_mod["dodge"]
    speed += armor_mod["speed"]

    # The PC's own attack roll: 1H Heavy Melee (Melee Skill Total, no
    # accuracy bonus, Damage 4 + Body, Physical, opposed by Parry/Dodge,
    # no attack_range - falls back to MELEE_RANGE) unless `Weapon` names
    # a ranged option in T.WEAPON, in which case the attacking
    # Skill/accuracy/Damage/Range/dmg_type/opp_def all switch to that
    # weapon's own numbers - see T.WEAPON's own comment for the real
    # rulebook.md/weapon_categories.csv values behind each one. This is
    # deliberately decoupled from parry/dodge/bodily/mental/vigilant
    # above - a caster's Sorcery Skill Total (or an archer's Archery)
    # drives their own attack roll and Range without touching their
    # Melee-based Parry or any other Defense.
    weapon = (row.get("Weapon") or "").strip()
    attack_range = None
    if weapon and weapon in T.WEAPON:
        w = T.WEAPON[weapon]
        w_skills = w["skill"] if isinstance(w["skill"], tuple) else (w["skill"],)
        w_skill = max(w_skills, key=lambda sk: skill_total(stats, skills, sk))
        atk_skill_total = skill_total(stats, skills, w_skill) + w["accuracy"]
        # `damage_stat: None` (Unarmed) means "Body or Cunning" per
        # weapon_categories.csv - pick whichever this PC's own build
        # actually has higher, rather than hardcoding one.
        damage_stat = w["damage_stat"] or max(("Body", "Cunning"), key=lambda s: int(stats[s]))
        damage = w["damage_base"] + int(stats[damage_stat])
        dmg_type = w["dmg_type"]
        opp_def = w["opp_def"]
        if "range" in w:
            attack_range = w["range"]
        elif "range_per_body" in w:
            attack_range = w["range_per_body"] * int(stats["Body"])
        elif "range_per_skill" in w:
            attack_range = w["range_per_skill"] * skill_total(stats, skills, w_skill)
    else:
        w_skill = "Melee"
        atk_skill_total = skill_total(stats, skills, "Melee")
        damage = 4 + int(stats["Body"])
        dmg_type = "Physical"
        opp_def = "Parry/Dodge"

    # Parry uses whichever held weapon gives the best result (rulebook.md:
    # 8 + that weapon's Skill Total + its Defense). `Parry Weapons` lists
    # what's held for Parrying (a Shield in the off hand, say); blank means
    # just the attacking Weapon (1H Heavy Melee when that's blank too, the
    # Roster default, so Roster rows read exactly as before). A weapon that
    # can't Parry (bow, thrown, spell) falls back to Unarmed.
    parry_weapons = [w.strip() for w in (row.get("Parry Weapons") or "").split(",") if w.strip()]
    if not parry_weapons:
        parry_weapons = [weapon or "1H Heavy Melee"]
    parry_options = []
    for pw in parry_weapons:
        wd = T.WEAPON_DEFENSE.get(pw)
        if wd is None:
            continue
        pw_skills = T.WEAPON[pw]["skill"]
        pw_skills = pw_skills if isinstance(pw_skills, tuple) else (pw_skills,)
        parry_options.append(8 + max(skill_total(stats, skills, sk) for sk in pw_skills) + wd)
    if not parry_options:
        parry_options.append(8 + skill_total(stats, skills, "Brawl") + T.WEAPON_DEFENSE["Unarmed"])
    parry = max(parry_options)

    # A plain display name for this PC's own base attack, for
    # narrate_fight.py/replay_html.py's combat log ("who attacked with
    # what") - the `Weapon` cell itself if set, "Melee" for the blank
    # default (1H Heavy Melee). Purely cosmetic, like `name` - nothing
    # reads this for game logic.
    weapon_name = weapon if weapon else "Melee"

    # "Hand size" for a support PC's own heal-use cap (see tactics.
    # strategy_support_healer) - rulebook.md has no per-encounter
    # hand-size concept, only "Cards Per Day"/"The Draw Cycle": "Draw a
    # number of cards equal to twice the total of your Cunning plus
    # Mind." Reused here as the stand-in for how many cards this PC is
    # carrying into a single isolated encounter (this sim never chains
    # multiple fights in one trial, so "starts every fight with a full
    # hand" is the right simplification). Computed for every PC, not
    # just Support ones - harmless, and one less thing to special-case.
    hand_size = 2 * (int(stats["Cunning"]) + int(stats["Mind"]))

    # `strategy` names a tactics.PC_STRATEGIES entry (blank/unrecognized
    # -> tactics.resolve_pc_strategy's default of "just attack normally,"
    # same as `support`'s old plain-bool gate) - the CSV's own `Support`
    # column stays a simple TRUE/blank for whoever's editing it by hand;
    # translating it into a named strategy here is what lets a future
    # third strategy (a PC who always maximizes Gambling, say) just add
    # another registry entry instead of a new boolean CSV column.
    strategy = "support_healer" if (row.get("Support") or "").strip().upper() == "TRUE" else "attacker"

    # `Heal Cards`/`Heal Bonus` (blank = 1/0, matching the original
    # hardcoded Level-1-with-no-features numbers exactly) - a Support
    # PC's own Healing Magic (T105) isn't one fixed spell: its Cost is
    # "Discard [the Spell's Level] cards" (so a Level 2 build discards
    # 2, not 1) and a Vitality feature ("healing increased by 1" per
    # copy) stacks flat on top - both are real per-build facts, not a
    # universal constant, so they're read from the CSV rather than
    # hardcoded in tactics.strategy_support_healer. Computed for every
    # PC, not just Support ones - harmless, same reasoning as
    # card_uses_left above.
    heal_cards_raw = (row.get("Heal Cards") or "").strip()
    heal_cards = int(heal_cards_raw) if heal_cards_raw else 1
    heal_bonus_raw = (row.get("Heal Bonus") or "").strip()
    heal_bonus = int(heal_bonus_raw) if heal_bonus_raw else 0

    # `Heal Range` (blank = no check, the original "adjacent ally,
    # assumed reachable" behavior) - Healing Magic's own Target text
    # ("an adjacent ally") is really just this build's own Range feature
    # talking; a build that's actually picked Reach (features.csv F053)
    # can heal from farther off. Only enforced under movement=True
    # (positions exist to check at all) - see tactics.
    # strategy_support_healer.
    heal_range_raw = (row.get("Heal Range") or "").strip()
    heal_range = int(heal_range_raw) if heal_range_raw else None

    # `Passives` (comma-separated tags, e.g. "Hand of Chaos") - an
    # always-on Technique effect with no AP/card cost of its own, unlike
    # Card Techniques above - see tactics.sift_bonus.
    passives = [t.strip() for t in (row.get("Passives") or "").split(",") if t.strip()]

    # Overchanneling (T140, a Style): "+1 damage on damaging Spell
    # attacks... You can't Parry." Only War Magic is a Spell attack in
    # this sim; Parry drops out by making it lose every max() against
    # Dodge in pc_defense_for.
    if "Overchanneling" in passives:
        if weapon.startswith("War Magic"):
            damage += 1
        parry = -99
    # 'No Parry' is a test-only passive pricing a can't-Parry cost
    # (Furious Rage had one until 2026-10-07).
    if "No Parry" in passives:
        parry = -99
    # 'Plus One Damage' is a test-only passive: +1 damage on every hit,
    # to check the sim's read of THE TABEL's Damage weight (2 a point).
    if "Plus One Damage" in passives:
        damage += 1

    # `Battle Tactic` - the same tactics.TARGETING registry enemies'
    # own sample_enemies.csv BattleTactic column already dispatches
    # through (tactics.select_target doesn't care which side a unit's
    # on), given to PCs too now that one actually wants a non-default
    # targeting rule (Hanforth's own Straggler Hunter - see tactics.
    # target_straggler). Blank/absent falls through to the same
    # movement-aware closest/first default every other PC already uses.
    battle_tactic = (row.get("Battle Tactic") or "").strip() or None

    # `Card Techniques` (comma-separated tags from tactics.py's
    # try_second_wind/perfect_strike_bonus/bottomless_bottles_choice -
    # "Second Wind", "Perfect Strike", "Bottomless Bottles",
    # "Warmage's Reserves") - a PC technique whose own cost is "discard
    # a card," not AP, per techniques.csv's own Action/Cost columns.
    # `card_uses_left` is the shared per-fight budget all of them draw
    # from - hand_size // 3, the same "quick check, not real hand/suit
    # tracking" shape as heal_uses_left's hand_size // 4, per the
    # designer's own framing ("say 1/3 of those"). Computed for every
    # PC, not just ones with a Card Technique - harmless, one less
    # special case.
    card_techniques = [t.strip() for t in (row.get("Card Techniques") or "").split(",") if t.strip()]
    # `Encounter Techniques` (comma-separated, one entry per known copy):
    # AP-costing Encounter Techniques the sim runs on its own - so far
    # just Challenge (T058), a Taunt that pulls attacks off the fragile.
    encounter_techs = [t.strip() for t in (row.get("Encounter Techniques") or "").split(",") if t.strip()]
    card_uses_left = hand_size // 3

    # Technique attacks from `Encounter Techniques` (TECH_ATTACKS below):
    # one use per known copy, each swapped in for a normal attack by
    # combat_sim's attack loop. These are what give the sim's party
    # attacks against Vital and Mental, not just Parry/Dodge.
    tech_attacks = []
    for tname in dict.fromkeys(encounter_techs):
        if tname in TECH_ATTACKS:
            prof = TECH_ATTACKS[tname](stats, skills, atk_skill_total, damage)
            prof.update(via=tname, uses=encounter_techs.count(tname))
            tech_attacks.append(prof)

    # `Defense Choices` ("Dodge|Vital"): each attack picks one of these at
    # random. Stands in for a War Magic caster whose copies are split
    # between the two Defenses War Magic can be learned against (T120:
    # "Dodge or Vital, chosen when you learn this"), per the designer.
    defense_choices = [d.strip() for d in (row.get("Defense Choices") or "").split("|") if d.strip()]

    # `Weapon Uses`: blank/absent means unlimited (every existing PC),
    # matching the sim's original always-available attack. A number
    # means this PC's own Weapon is an Encounter Technique with that
    # many known copies (Beornhard's 3x War Magic, say) - only that many
    # casts a fight, decremented once per real weapon attack in
    # combat_sim.run_fight (not a Bottomless-Bottles-substituted one,
    # which is a different action entirely). "Warmage's Reserves" in
    # `card_techniques` adds ceil(hand_size / 3) more on top - the
    # designer's own call (rounded up, unlike the floor() card_uses_left
    # budget above, since this is a bonus on an already-scarce resource
    # rather than a fresh one) for how many times its own 'regain an
    # Encounter Technique use' effect can fire in one fight.
    weapon_uses_raw = (row.get("Weapon Uses") or "").strip()
    weapon_uses_left = int(weapon_uses_raw) if weapon_uses_raw else None
    # With real cards (T.CARDS) Warmage's Reserves discards from the hand
    # in the fight instead (combat_sim._warmage_reserves).
    if weapon_uses_left is not None and "Warmage's Reserves" in card_techniques and not T.CARDS:
        weapon_uses_left += math.ceil(hand_size / 3)

    # Bottomless Bottles (T053) - Jackal only makes Bottled Fire (I030)
    # with it now, not Healing Potion too (the designer's own call - "a
    # bit tricky" balancing two items off one budget, not worth it).
    # Bottled Fire is a [Grenade] (glossary.md): Acrobatics Skill Total,
    # no accuracy bonus, flat 8 Fire damage (not scaled by any Stat),
    # opposed by Dodge alone (not Parry/Dodge). combat_sim's attack loop
    # only overlays skill_total/damage/dmg_type/opp_def for a Bottled
    # Fire throw, not attack_range - so this only reads correctly for a
    # PC whose own base Weapon's Range formula already happens to be
    # 3 x Body too (Jackal's Light Thrown is, coincidentally); revisit
    # if a future Bottomless Bottles PC's base Weapon uses a different
    # Range. Hardcoded to this one item rather than a general "what did
    # this PC craft" system - generalize once a second Bottomless
    # Bottles PC needs a different one.
    #
    # How many per fight: T053's own Effects text is "items with a total
    # Gold cost of no more than [4 x X]" for X cards discarded (its own
    # Cost, chosen at use, not tied to the Technique's own XP-Level).
    # The designer's own framing - spend 2/3 of a day's cards on this
    # (X = hand_size x 2 // 3), all toward Bottled Fire, then a single
    # fight gets half of whatever a full day's Gold budget buys - turns
    # into: gold_budget = 4 x X, daily_count = gold_budget //
    # T.BOTTLED_FIRE_GOLD_COST (items.csv's own real Cost - 4 Gold, the
    # designer's general "alchemy items default to 2 x Level Gold"
    # rule), bottled_fire_uses = daily_count // 2. A separate counter
    # from card_uses_left above - Bottomless Bottles' real resource math
    # (Gold, not just "a card") is genuinely different from Second
    # Wind/Perfect Strike/Warmage's Reserves.
    bottled_fire_profile = None
    bottled_fire_uses = None
    if "Bottomless Bottles" in card_techniques:
        # Mighty Mixologist (T035): +1 damage with a damaging Grenade of
        # Level 3 or lower - Bottled Fire is Level 2. Its Grenade-range
        # rider isn't modeled (Range isn't overlaid for Bottled Fire at
        # all, see above).
        bottled_fire_profile = dict(skill_total=skill_total(stats, skills, "Acrobatics"),
                                     damage=8 + (1 if "Mighty Mixologist" in passives else 0),
                                     dmg_type="Fire", opp_def="Dodge", skill="Acrobatics")
        item_cost = T.BOTTLED_FIRE_GOLD_COST
        # `Bottles Item` (2026-10-09): Acidic Flask (I028, Level 1, 2 Gold)
        # instead - "On a hit, the target gains 5 + [Clubs] stacks of
        # Bleeding." No damage, so Mighty Mixologist doesn't apply.
        if (row.get("Bottles Item") or "").strip() == "Acidic Flask":
            bottled_fire_profile = dict(skill_total=skill_total(stats, skills, "Acrobatics"),
                                         damage=T.ACID_FLASK_DAMAGE, dmg_type="Fire" if T.ACID_FLASK_DAMAGE else None,  # elemental materials; one elemental Resist in this sim
                                         opp_def="Dodge", skill="Acrobatics",
                                         effect=("bleeding", T.ACID_FLASK_STACKS, "Clubs"), item="Acidic Flask")
            item_cost = 2
        cards_for_gold = hand_size * 2 // 3
        gold_budget = 4 * cards_for_gold
        daily_count = int(gold_budget // item_cost)
        bottled_fire_uses = daily_count // 2

    # Ranged hexes (HEXES above), one use per known copy.
    hexes = [dict(via=h, kind=HEXES[h][0], amount=HEXES[h][1], suit=HEXES[h][2], uses=encounter_techs.count(h),
                  skill="Sorcery", skill_total=skill_total(stats, skills, "Sorcery"), opp_def=HEXES[h][3],
                  range=skill_total(stats, skills, "Sorcery"))
             for h in dict.fromkeys(encounter_techs) if h in HEXES]

    # Battle Maneuver (T072, Encounter, "Make a weapon attack") with its
    # Features (`Maneuver Features`, e.g. "Bare-Handed, Lunging 2, Half
    # Guard 3"): Lunging X is X free Shifts of up to 2 meters, Half Guard
    # X is X + [Spades] Protected on a hit. Bare-Handed just makes it an
    # Unarmed attack, which is already the PC's weapon for every row
    # that has it.
    maneuver = None
    if "Battle Maneuver" in encounter_techs:
        feats = {}
        for f in (row.get("Maneuver Features") or "").split(","):
            parts = f.strip().rsplit(" ", 1)
            if len(parts) == 2 and parts[1].isdigit():
                feats[parts[0]] = int(parts[1])
            elif f.strip():
                feats[f.strip()] = 1
        maneuver = dict(uses=encounter_techs.count("Battle Maneuver"),
                        lunges=feats.get("Lunging", 0), guard=feats.get("Half Guard", 0),
                        battering=feats.get("Battering", 0))

    # Every copy gets its own suffix, Roster rows included (a Roster
    # build used to keep its bare row Name - "Baseline Tier 1 Party
    # Member" x4, all identical - since nothing needed to tell 4
    # otherwise-identical clones apart; a trace/log does, though
    # (narrate_fight.py's stable per-fight labels collapse into one if
    # two units share a name), and `name` is cosmetic everywhere else in
    # this file/combat_sim.py, so it's safe to always suffix.
    pc = dict(name=f"{row['Name']}{index}",
              parry=parry, dodge=dodge, bodily=bodily, mental=mental, vigilant=vigilant,
              skill_total=atk_skill_total,  # the PC's own attacking Skill Total - see the Weapon block above
              acrobatics_skill_total=acrobatics_skill_total, stealth_skill_total=stealth_skill_total,
              damage=damage, dmg_type=dmg_type, opp_def=opp_def, weapon_name=weapon_name,
              physres=physres, elemres=elemres, armor=armor,
              health=health, max_health=health, speed=speed, reflex=reflex,
              crippled=0, vulnerable=0, bleeding=0, good_luck=good_luck,
              shallow_max=T.BASE_SHALLOW_HEALTH,
              strategy=strategy, heal_uses_left=hand_size // 4,
              heal_cards=heal_cards, heal_bonus=heal_bonus, heal_range=heal_range,
              passives=passives, battle_tactic=battle_tactic,
              card_techniques=card_techniques, card_uses_left=card_uses_left,
              attacks_received=0, attacks_vs_parry_dodge=0, hits_received=0, parries=0,
              challenge_uses_left=encounter_techs.count("Challenge"),
              taunting_strike_uses_left=encounter_techs.count("Taunting Strike"),
              presence_skill_total=skill_total(stats, skills, "Presence"),
              # The attack's Skill (for its suit) and the day's hand size,
              # for real cards (cards.start_fight).
              attack_skill=w_skill, hand_size=hand_size, weapon_is_spell=weapon.startswith("War Magic"))
    if attack_range is not None:
        pc["attack_range"] = attack_range
    if "Bottomless Bottles" in card_techniques:
        pc["bottles_cards"] = hand_size * 2 // 3  # discarded crafting before the day's first fight
    if hexes:
        pc["hexes"] = hexes
    if maneuver:
        pc["maneuver"] = maneuver
    # Raise Spirits (T069): "an ally within [Performance Skill Total]
    # meters".
    if "Raise Spirits" in passives:
        pc["raise_range"] = skill_total(stats, skills, "Performance")
    # How cautiously this PC plays (play_styles.py); a blank cell falls
    # back to what the build suggests.
    pc["play_style"] = ((row.get("Play Style") or "").strip()
                        or play_styles.default_style(attack_range, armor, "Shield" in parry_weapons,
                                                     strategy == "support_healer"))
    if weapon_uses_left is not None:
        pc["weapon_uses_left"] = weapon_uses_left
    if tech_attacks:
        pc["tech_attacks"] = tech_attacks
    if defense_choices:
        pc["opp_def_choices"] = defense_choices
    if bottled_fire_profile is not None:
        pc["bottled_fire_profile"] = bottled_fire_profile
        pc["bottled_fire_uses_left"] = bottled_fire_uses
    return pc


def make_party(tier, good_luck=0):
    """4 copies of the Roster row for this Tier. `good_luck`: how many
    stacks of Good Luck every PC has on their own attack roll (rulebook.md:
    each stack flips one extra card, keep the highest) - 0 by default, a
    param specifically so combat_sim's good-luck-value experiment can turn
    it on without a second copy of this function."""
    for row in _load_rows():
        if row["Roster"].strip().upper() == "TRUE" and int(row["Tier"]) == tier:
            return [_pc_dict(row, i + 1, good_luck) for i in range(4)]
    raise ValueError(f"no Roster row for Tier {tier}")


def get_pc(name, good_luck=0):
    for row in _load_rows():
        if row["Name"] == name:
            return _pc_dict(row, 1, good_luck)
    raise KeyError(f"no sample_pcs.csv row named {name!r}")


def make_party_of(name, good_luck=0):
    """4 copies of a single named reference PC (Roster or not) - same
    duplication pattern as make_party(tier), just keyed by name instead
    of Tier. For testing one build's own attack profile (a ranged PC's
    Weapon, say) against the validated Roster without hand-assembling a
    mixed party - monkeypatch combat_sim.make_party to this the same way
    the README's item-balancing checks monkeypatch combat_sim.make_enemy."""
    return make_party_from([name] * 4, good_luck)


def make_party_from(names, good_luck=0):
    """A custom party assembled from named reference rows in whatever mix
    is asked for (e.g. ["Hilde", "Browndog", "Sable", "Beornhard"]) -
    for testing party composition itself, not just one build cloned x4.
    Same monkeypatch-combat_sim.make_party usage as make_party_of."""
    rows = {r["Name"]: r for r in _load_rows()}
    return [_pc_dict(rows[name], i + 1, good_luck) for i, name in enumerate(names)]


def all_pcs():
    return [_pc_dict(row, 1, 0) for row in _load_rows()]


if __name__ == "__main__":
    for p in all_pcs():
        print(p["name"], "| Parry", p["parry"], "| Dodge", p["dodge"], "| Bodily", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])
