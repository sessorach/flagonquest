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
               "Heal Range", "Passives", "Battle Tactic")}
    parry = 8 + skill_total(stats, skills, "Melee")
    dodge = 8 + skill_total(stats, skills, "Acrobatics")
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
        atk_skill_total = skill_total(stats, skills, w["skill"]) + w["accuracy"]
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
            attack_range = w["range_per_skill"] * skill_total(stats, skills, w["skill"])
    else:
        atk_skill_total = skill_total(stats, skills, "Melee")
        damage = 4 + int(stats["Body"])
        dmg_type = "Physical"
        opp_def = "Parry/Dodge"

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
    card_uses_left = hand_size // 3

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
    if weapon_uses_left is not None and "Warmage's Reserves" in card_techniques:
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
        bottled_fire_profile = dict(skill_total=skill_total(stats, skills, "Acrobatics"), damage=8,
                                     dmg_type="Fire", opp_def="Dodge")
        cards_for_gold = hand_size * 2 // 3
        gold_budget = 4 * cards_for_gold
        daily_count = int(gold_budget // T.BOTTLED_FIRE_GOLD_COST)
        bottled_fire_uses = daily_count // 2

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
              damage=damage, dmg_type=dmg_type, opp_def=opp_def, weapon_name=weapon_name,
              physres=physres, elemres=elemres, armor=armor,
              health=health, max_health=health, speed=speed, reflex=reflex,
              crippled=0, vulnerable=0, bleeding=0, good_luck=good_luck,
              strategy=strategy, heal_uses_left=hand_size // 4,
              heal_cards=heal_cards, heal_bonus=heal_bonus, heal_range=heal_range,
              passives=passives, battle_tactic=battle_tactic,
              card_techniques=card_techniques, card_uses_left=card_uses_left)
    if attack_range is not None:
        pc["attack_range"] = attack_range
    if weapon_uses_left is not None:
        pc["weapon_uses_left"] = weapon_uses_left
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
