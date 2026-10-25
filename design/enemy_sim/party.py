"""
Builds the sample characters for a fight. Each `sample_pcs.csv` row
names a Builder export in `builds/` (Stats, Skills, every Technique copy
with its Level and Features, the inventory); `load_sheet` reads it,
hands each Technique ID to its entry in techniques.py, maps the items
through game_data.py, and adds what only the row says: which weapon the
sim attacks with (`Weapon`), picks an export doesn't carry (`Choices`),
Techniques carried knowingly unplayed (`Unmodeled`), `Play Style`,
`Battle Tactic`, `Bottles Item`, and a `Health` override for the abstract
builds. Anything it can't place stops the load with a BuildError.

`_pc_dict` turns the sheet into the fight dict - the rulebook formulas:
- Defense = 8 + [governing Skill Total]: Parry from the best held weapon
  (8 + its Skill Total + its Weapon Defense, Unarmed if none can Parry),
  Dodge from Acrobatics or Brawl plus Armor's penalty, Vital from
  Resilience, Mental from Composure, Vigilant from Insight
- the attack from `Weapon` (tunables.WEAPON): its Skill, Accuracy,
  Damage, damage type, Defense and Range; blank is 1H Heavy Melee
- Resist starts at Essence; Armor adds to Physical Resist only
- Speed = 1 + Agility, plus Armor's penalty; Reflex = Insight Skill Total
- Health = 5 Shallow + 5 Deep + Technique and item bonuses
- a day's hand = twice (Cunning + Mind), which sets the Card Technique,
  healing and Bottomless Bottles budgets

Each Technique's own fight fields (uses, ranges, profiles) come from its
`setup` in techniques.py. Use `make_pc` to build a character changed for
a test, `make_party(tier)` for the Roster, `make_party_from([names])`
for a chosen party. Older notes on the Roster's derivation are in
sample_characters.md and ENEMY_ENCOUNTER_DESIGN.md's Analysis section.
"""
import collections
import csv
import json
import math
import os
from types import SimpleNamespace

import tunables as T
import play_styles
import game_data
import techniques
from techniques import BuildError

_HERE = os.path.dirname(os.path.abspath(__file__))
_CSV_PATH = os.path.join(_HERE, "sample_pcs.csv")
BUILDS_DIR = os.path.join(_HERE, "builds")
STATS = ("Agility", "Body", "Cunning", "Mind", "Essence")


def _load_rows():
    with open(_CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _level(raw):
    # The Builder writes a Buildable copy's Level as a number and a fixed
    # one as "Lv 2".
    return int(str(raw).replace("Lv", "").strip())


def _choices(cell):
    """The Choices column: picks a Builder export doesn't carry, per copy
    in the export's order - "War Magic: Dodge, Vital; Temper Soulblade:
    Fatestealer"."""
    out = {}
    for part in (cell or "").split(";"):
        if part.strip():
            name, _, picks = part.partition(":")
            out[name.strip()] = [p.strip() for p in picks.split(",")]
    return out


def read_build(filename):
    with open(os.path.join(BUILDS_DIR, filename), encoding="utf-8") as f:
        return json.load(f)


def load_sheet(row, build=None):
    """Everything about one sample character the fight needs: the Builder
    export named in `Build` (builds/), read through techniques.py, plus
    the row's own columns for what an export doesn't say - which weapon
    the sim swings, picks the Builder keeps outside the export, how the
    character plays. Stops with a BuildError on anything it can't place:
    an unknown Technique, Feature or item, a pick that names nothing."""
    build = build or read_build(row["Build"])
    sheet = SimpleNamespace(
        name=row["Name"],
        stats={s: int(build["statPoints"][s]) for s in STATS},
        skills={k: int(v) for k, v in build["skillPoints"].items()},
        weapon=(row.get("Weapon") or "").strip(), armor="Unarmored", parry_weapons=[],
        passives=[], card_techniques=[], encounter_techs=[], tech_attacks=[], hexes=[], maneuvers=[],
        blessing_features={}, weapon_uses=None, defense_choices=[],
        support=False, heal_cards=1, heal_bonus=0, heal_reach=None, heal_range=None,
        battle_tactic=(row.get("Battle Tactic") or "").strip() or None,
        play_style=(row.get("Play Style") or "").strip(),
        bottles_item=(row.get("Bottles Item") or "").strip())
    if set(sheet.skills) != set(T.PC_SKILL_STAT):
        raise BuildError(f"{row['Name']}: the export's Skills don't match the sim's 25")

    # Items: armor and held weapons. The Weapon column says which one the
    # sim attacks with; every held weapon counts for Parry (rulebook.md:
    # the best of what you're holding).
    for it in build.get("inventory", ()):
        iid = it["id"]
        if iid in game_data.ARMOR_ITEMS:
            sheet.armor = game_data.ARMOR_ITEMS[iid]
        elif iid in game_data.WEAPON_ITEMS:
            sheet.parry_weapons.append(game_data.WEAPON_ITEMS[iid])
        elif iid not in game_data.NOT_MODELED_ITEMS:
            raise BuildError(f"{row['Name']}: item {iid} {game_data.items().get(iid, {}).get('Name', '?')} "
                             "isn't modeled (game_data.py)")
    if sheet.weapon and sheet.weapon not in sheet.parry_weapons:
        sheet.parry_weapons.append(sheet.weapon)

    # Techniques, grouped by ID in the export's order.
    copies = {}
    for t in build.get("techniques", ()):
        copies.setdefault(t["id"], []).append(
            dict(level=_level(t.get("level", 1)), features={f["name"]: int(f["count"]) for f in t.get("features", ())}))
    choices = _choices(row.get("Choices"))
    # Unmodeled: Techniques this row carries knowingly unplayed (a power
    # the sim doesn't have yet). Their Health bonus still counts.
    unmodeled = {t.strip() for t in (row.get("Unmodeled") or "").split(",") if t.strip()}
    names_in_build = {game_data.technique_name(tid) for tid in copies}
    for name in unmodeled - names_in_build:
        raise BuildError(f"{row['Name']}: Unmodeled names {name!r}, which the build doesn't have")
    known = set()
    shallow = deep = 5  # rulebook.md: 5 Shallow and 5 Deep Health to start
    for tid, cs in copies.items():
        tech = techniques.get(tid)
        bonus = game_data.health_bonus(tid)
        shallow += bonus[0] * len(cs)
        deep += bonus[1] * len(cs)
        if tech is None or game_data.technique_name(tid) in unmodeled:
            continue
        tech.check_features(cs)
        tech.build(sheet, cs, choices.get(tech.name, []))
        known.add(tech.name)
    for name in choices:
        if name not in known:
            raise BuildError(f"{row['Name']}: Choices names {name!r}, which the build doesn't have")
    for it in build.get("inventory", ()):
        if it["id"] in game_data.items():
            bonus = game_data.item_health_bonus(it["id"])
            shallow += bonus[0]
            deep += bonus[1]
    override = (row.get("Health") or "").strip()
    sheet.health = int(override) if override else shallow + deep

    # A War Magic Weapon on a sheet with no War Magic copies (Wren, a
    # reference build that never picked Techniques) stands in as an
    # attack that's always there.
    if sheet.weapon.startswith("War Magic") and "T120" not in copies:
        sheet.weapon_uses = None
    elif sheet.weapon.startswith("War Magic") and sheet.weapon_uses is None:
        sheet.weapon_uses = 0
    if sheet.support:
        ley = 3 if any("Ley-weaving" in p for p in sheet.passives) else 0
        theurgy = skill_total(sheet.stats, sheet.skills, "Theurgy")
        sheet.heal_range = 1 + (theurgy if sheet.heal_reach else 0) + ley
    return sheet


def skill_total(stats, skills, skill):
    stat = T.PC_SKILL_STAT[skill]
    return int(stats[stat]) + int(skills[skill])


def _maneuver_features(feats):
    """One Battle Maneuver copy's Features ({name: copies}), as the
    numbers combat_sim reads."""
    return dict(lunges=feats.get("Lunging", 0), guard=feats.get("Half Guard", 0),
                battering=feats.get("Battering", 0),
                # Open the Wound X (draft, 2026-10-16): Reign of
                # Blood's text as a Battle Maneuver Feature.
                cashout=2 * feats.get("Open the Wound", 0),
                # Hilde's Level 3 copy (2026-10-24): Whirlwind (F018) hits
                # a second target, Victorious (F013) draws a card on a
                # Down, Ascended Blade (F017) may deal Brilliant damage.
                whirlwind=bool(feats.get("Whirlwind")), victorious=bool(feats.get("Victorious")),
                ascended=bool(feats.get("Ascended Blade")),
                # Wind Slash X (Jackal): +[twice X] range for the attack.
                wind=feats.get("Wind Slash", 0),
                # Calculated (F016, Good Luck), Wing Clip (F006, Crippled X),
                # Hamstring (F008, Slowed X), Harrying (F007, Harried 1 + X)
                # and Distracting (F004, Taunt X), all + their suit.
                calculated=feats.get("Calculated", 0), wing_clip=feats.get("Wing Clip", 0),
                hamstring=feats.get("Hamstring", 0), harrying=feats.get("Harrying", 0),
                distracting=feats.get("Distracting", 0))


def _pc_dict(sheet, index, good_luck):
    """One PC's fight dict from a loaded sheet (load_sheet)."""
    stats, skills = sheet.stats, sheet.skills
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
    health = sheet.health
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
    armor = sheet.armor
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
    weapon = sheet.weapon
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
    parry_weapons = list(sheet.parry_weapons)
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
    strategy = "support_healer" if sheet.support else "attacker"

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
    heal_cards = sheet.heal_cards
    heal_bonus = sheet.heal_bonus

    # `Heal Range` (blank = no check, the original "adjacent ally,
    # assumed reachable" behavior) - Healing Magic's own Target text
    # ("an adjacent ally") is really just this build's own Range feature
    # talking; a build that's actually picked Reach (features.csv F053)
    # can heal from farther off. Only enforced under movement=True
    # (positions exist to check at all) - see tactics.
    # strategy_support_healer.
    heal_range = sheet.heal_range

    # `Passives` (comma-separated tags, e.g. "Hand of Chaos") - an
    # always-on Technique effect with no AP/card cost of its own, unlike
    # Card Techniques above - see tactics.sift_bonus.
    passives = list(sheet.passives)

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
    battle_tactic = sheet.battle_tactic

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
    card_techniques = list(sheet.card_techniques)
    # `Encounter Techniques` (comma-separated, one entry per known copy):
    # AP-costing Encounter Techniques the sim runs on its own - so far
    # just Challenge (T058), a Taunt that pulls attacks off the fragile.
    encounter_techs = list(sheet.encounter_techs)
    card_uses_left = hand_size // 3

    # Technique attacks from `Encounter Techniques` (TECH_ATTACKS below):
    # one use per known copy, each swapped in for a normal attack by
    # combat_sim's attack loop. These are what give the sim's party
    # attacks against Vital and Mental, not just Parry/Dodge.
    tech_attacks = []
    for tname, factory, uses in sheet.tech_attacks:
        prof = factory(stats, skills, atk_skill_total, damage)
        prof.update(via=tname, uses=uses)
        tech_attacks.append(prof)
    # Overchanneling's +1 goes on damaging Spell attacks, the technique
    # ones included.
    if "Overchanneling" in passives:
        for prof in tech_attacks:
            if prof.get("skill") == "Sorcery" and prof["damage"] > 0:
                prof["damage"] += 1

    # `Defense Choices` ("Dodge|Vital"): each attack picks one of these at
    # random. Stands in for a War Magic caster whose copies are split
    # between the two Defenses War Magic can be learned against (T120:
    # "Dodge or Vital, chosen when you learn this"), per the designer.
    defense_choices = list(sheet.defense_choices)

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
    weapon_uses_left = sheet.weapon_uses
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
        if sheet.bottles_item == "Acidic Flask":
            bottled_fire_profile = dict(skill_total=skill_total(stats, skills, "Acrobatics"),
                                         damage=T.ACID_FLASK_DAMAGE, dmg_type="Fire" if T.ACID_FLASK_DAMAGE else None,  # elemental materials; one elemental Resist in this sim
                                         opp_def="Dodge", skill="Acrobatics",
                                         effect=("bleeding", T.ACID_FLASK_STACKS, "Clubs"), item="Acidic Flask")
            item_cost = 2
        cards_for_gold = hand_size * 2 // 3
        gold_budget = 4 * cards_for_gold
        daily_count = int(gold_budget // item_cost)
        bottled_fire_uses = daily_count // 2

    # Placeholder's Lengthy Ley-weaving (T133, a Style): "Your Spells and
    # non-weapon-attack Disciplines have their Ranges increased by 3
    # meters." Hanforth's Heal Range of 4 already counts it.
    ley = 3 if any("Ley-weaving" in p for p in passives) else 0

    # Ranged hexes (HEXES above), one use per known copy.
    # A ranged hex reaches [its Skill Total] meters (Reckoning's Target,
    # War Magic with Lance); without Lance War Magic is "An adjacent
    # creature".
    hexes = []
    for h in sheet.hexes:
        h = dict(h)
        ranged = h.pop("ranged")
        h["skill_total"] = skill_total(stats, skills, h["skill"])
        h["range"] = (h["skill_total"] if ranged else 1) + ley
        hexes.append(h)

    # Battle Maneuver (T072, Encounter, "Make a weapon attack") with its
    # Features (`Maneuver Features`, e.g. "Bare-Handed, Lunging 2, Half
    # Guard 3"): Lunging X is X free Shifts of up to 2 meters, Half Guard
    # X is X + [Spades] Protected on a hit. Bare-Handed just makes it an
    # Unarmed attack, which is already the PC's weapon for every row
    # that has it.
    maneuver = None
    maneuver_queue = []
    if sheet.maneuvers:
        # Copies built the same way share one entry; copies built
        # differently (Hilde, Browndog) are used in the sheet's order,
        # combat_sim moving to the next once one's spent.
        groups = [_maneuver_features(f) for f in sheet.maneuvers]
        if all(g == groups[0] for g in groups):
            maneuver = dict(uses=len(groups), **groups[0])
        else:
            copies = [dict(uses=1, **g) for g in groups]
            maneuver, maneuver_queue = copies[0], copies[1:]

    # Every copy gets its own suffix, Roster rows included (a Roster
    # build used to keep its bare row Name - "Baseline Tier 1 Party
    # Member" x4, all identical - since nothing needed to tell 4
    # otherwise-identical clones apart; a trace/log does, though
    # (narrate_fight.py's stable per-fight labels collapse into one if
    # two units share a name), and `name` is cosmetic everywhere else in
    # this file/combat_sim.py, so it's safe to always suffix.
    pc = dict(name=f"{sheet.name}{index}",
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
    if maneuver_queue:
        pc["maneuver_queue"] = maneuver_queue
    # What each Technique needs on the fight dict (its uses, a range, a
    # profile) is set by its own entry in techniques.py. Run for every
    # name the PC carries, a test's added passive included. `techs` is the
    # Card and Encounter Techniques by name, which hooks.py checks
    # alongside `passives`.
    pc["techs"] = list(dict.fromkeys(encounter_techs + card_techniques))
    setup = SimpleNamespace(stats=stats, skills=skills, uses=collections.Counter(encounter_techs), ley=ley,
                            sheet=sheet, weapon=weapon, weapon_name=weapon_name, w_skill=w_skill,
                            atk_skill_total=atk_skill_total, damage=damage, dmg_type=dmg_type, opp_def=opp_def)
    for name in dict.fromkeys(list(passives) + pc["techs"]):
        techniques.setup(name, pc, setup)
    # rulebook.md, Grapple: no "actions that require two hands".
    pc["two_handed"] = weapon in ("2H Heavy Melee", "2H Light Melee", "Light Bow")
    # How cautiously this PC plays (play_styles.py); a blank cell falls
    # back to what the build suggests.
    pc["play_style"] = (sheet.play_style
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


def _rows():
    return {r["Name"]: r for r in _load_rows()}


def make_pc(name, index=1, good_luck=0, health=0, add_passives=(), drop_passives=(), battle_tactic=None,
            rows=None):
    """One sample character's fight dict, optionally changed for a test:
    `health` more max Health, test passives added (effect_check's
    "Test:..." ones, a Style being priced) or dropped, a different Battle
    Tactic. The one way scripts should build a modified character, so none
    of them depend on the CSV's columns."""
    row = (rows or _rows())[name]
    sheet = load_sheet(row)
    sheet.health += health
    sheet.passives = [p for p in sheet.passives if p not in drop_passives] + list(add_passives)
    if battle_tactic:
        sheet.battle_tactic = battle_tactic
    return _pc_dict(sheet, index, good_luck)


def make_party(tier, good_luck=0):
    """4 copies of the Roster row for this Tier. `good_luck`: how many
    stacks of Good Luck every PC has on their own attack roll (rulebook.md:
    each stack flips one extra card, keep the highest) - 0 by default, a
    param specifically so combat_sim's good-luck-value experiment can turn
    it on without a second copy of this function."""
    for row in _load_rows():
        if row["Roster"].strip().upper() == "TRUE" and int(row["Tier"]) == tier:
            sheet = load_sheet(row)
            return [_pc_dict(sheet, i + 1, good_luck) for i in range(4)]
    raise ValueError(f"no Roster row for Tier {tier}")


def get_pc(name, good_luck=0):
    rows = _rows()
    if name not in rows:
        raise KeyError(f"no sample_pcs.csv row named {name!r}")
    return make_pc(name, 1, good_luck, rows=rows)


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
    rows = _rows()
    return [make_pc(name, i + 1, good_luck, rows=rows) for i, name in enumerate(names)]


def all_pcs():
    rows = _rows()
    return [make_pc(name, 1, 0, rows=rows) for name in rows]


if __name__ == "__main__":
    for p in all_pcs():
        print(p["name"], "| Parry", p["parry"], "| Dodge", p["dodge"], "| Bodily", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])
