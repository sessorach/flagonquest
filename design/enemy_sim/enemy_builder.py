"""Builds an enemy stat block the way a PC is built (2026-11-03 onward).

Per the designer (ENEMY_ENCOUNTER_DESIGN.md, "First principles" and the
sections after it): the players' own Stats, Skill Totals, weapons and
armor, so Defense = 8 + Skill Total, Damage = the weapon's base + the
damage Stat, Resist = the Resist Stat + armor. A row reads its Level's
line in ENEMY_TABLE, adds its archetype (ROLE_ADDS), and spends its
Level's points (tunables.V3_PRUNED_ALLOWANCE + V3_PRUNED_EXTRA) on
Abilities, loadout and armor at ABILITY_PRICES / LOADOUT_PRICES /
ARMOR_PRICES; what's left is Health. sample_enemies.py picks what a row
buys; this file turns the picks into numbers.

The table, prices and caps are the outcome of the November tuning, all
written up in ENEMY_ENCOUNTER_DESIGN.md. The v1 builder, v2 table and the
earlier v3 versions and adjustment layers were retired 2026-11-11 (git
history and archive/enemy_sim_experiments/ have them).
"""
import math
import tunables as T

STAT_CAP, SKILL_CAP = 5, 10

# One row per Level (designer, in pencil 2026-11-09; GM_GUIDE_NOTES.md's
# Level table). skill: the weapon Skill Total (Parry with a melee weapon,
# and the Strong Defense); accuracy: the attack's Skill Total; damage: the
# damage Stat; resist: the Resist Stat (armor adds); health: per Slot,
# before the points left over. tunables.V3_TABLE_NUDGE adds to it for an
# experiment ("1:accuracy=3/health=-2;2:damage=-1", as SIM_SET carries it).
ENEMY_TABLE = {
    1: dict(skill=4, accuracy=4, damage=2, resist=3, health=6),
    2: dict(skill=7, accuracy=5, damage=3, resist=4, health=7),
    3: dict(skill=9, accuracy=7, damage=3, resist=5, health=7),
    4: dict(skill=10, accuracy=8, damage=4, resist=5, health=7),
    5: dict(skill=10, accuracy=8, damage=4, resist=5, health=9),
}
for _part in filter(None, T.V3_TABLE_NUDGE.split(";")):
    _L, _c = _part.split(":")
    for _x in _c.split("/"):
        _k, _v = _x.split("=")
        ENEMY_TABLE[int(_L)][_k] += int(_v)

ELEMENTS = ("Brilliant", "Fire", "Frost", "Shadow")
OPPOSITE = {"Brilliant": "Shadow", "Shadow": "Brilliant", "Fire": "Frost", "Frost": "Fire"}

ACTIONS = {
    "Defensive Melee": {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Offensive Melee": {"acc_mod": 0, "dmg_base": 4, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Light Melee":     {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Heavy Melee":     {"acc_mod": 0, "dmg_base": 5, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Ranged Weapon":   {"acc_mod": 1, "dmg_base": 3, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Melee Spell":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Dodge",       "range": 0},
    "Ranged Spell":    {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Dodge",       "range": 2},
    "Vital Spell":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Bodily",      "range": 2},
    "Shadow Bolt":     {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Dodge",       "range": 2},
    "Vital Fire":      {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Fire",     "opp_def": "Bodily",      "range": 2},
    # Loadouts for the pruned v3 (designer, 2026-11-04): an enemy in melee
    # is presumed to carry a sword and shield; the toggles are heavy versus
    # light and two-handed versus a shield. The numbers are the PC weapon
    # table's (items.csv), Parry taking the better weapon Defense in hand
    # (the shield's 2).
    "Sword and Shield":       {"acc_mod": 1, "dmg_base": 3, "stat": "body_or_cunning", "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Heavy Weapon and Shield": {"acc_mod": 0, "dmg_base": 4, "stat": "body",          "wd": 2, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Light Two-Handed":       {"acc_mod": 1, "dmg_base": 4, "stat": "body_or_cunning", "wd": 1, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Two-Handed Weapon":      {"acc_mod": 0, "dmg_base": 5, "stat": "body",            "wd": 0, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 0},
    "Bow":                    {"acc_mod": 1, "dmg_base": 3, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    "Heavy Bow":              {"acc_mod": 0, "dmg_base": 4, "stat": "cunning",         "wd": None, "dmg_type": "Physical", "opp_def": "Parry/Dodge", "range": 3},
    # The monster manual's Mental attacker (2026-11-04, new for the
    # designer's review): a spell like the Vital Spell, at Mental Defense.
    "Mind Spell":             {"acc_mod": 0, "dmg_base": 2, "stat": "mind",            "wd": None, "dmg_type": "Shadow",   "opp_def": "Mental",      "range": 2},
    # Non-damaging main Actions (see ENEMY_ENCOUNTER_DESIGN.md's enemy
    # variety standard) - each enemy using one carries a BackupAction.
    "Hex":             {"acc_mod": 0, "dmg_base": 0, "stat": "mind",            "wd": None, "dmg_type": None,       "opp_def": "Mental",      "range": 2,
                        "kind": "hex"},
    "Shield Ally":     {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "support"},
    "Mend Ally":       {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 1,
                        "kind": "heal"},
    # The catalog's other main Actions (2026-10-25), at its own numbers:
    # Curse "Target is debuffed +2 times" (Dodge, Range x2), Great Heal
    # "Target ally heals 2 Health" (Range x3), Shielding Nova "Allies in
    # range gain 2 Protected" (Range x3). `stacks` overrides the Level
    # tables below; none of the three is priced against the others yet.
    "Curse":           {"acc_mod": 0, "dmg_base": 0, "stat": "mind",            "wd": None, "dmg_type": None,       "opp_def": "Dodge",       "range": 2,
                        "kind": "hex", "stacks": 2},
    "Great Heal":      {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 3,
                        "kind": "heal", "stacks": 2},
    "Shielding Nova":  {"acc_mod": 0, "dmg_base": 0, "stat": "essence",         "wd": None, "dmg_type": None,       "opp_def": None,          "range": 3,
                        "kind": "nova", "stacks": 2},
}

# How many stacks a Hex lands on a hit, or how much Protected a Shield
# Ally grants, by Level. Priced to trade roughly evenly with a damaging
# attack: an L1-2 enemy hit nets ~2 Health (~8 value), about what 3
# stacks of Slowed/Frightened/Protected or 2-3 of Crippled are worth.
EFFECT_STACKS = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5}

# Shield Ally / Mend Ally never miss, so they're priced against what an
# attacker's action actually delivers on average (hit chance included),
# not against a hit: see GUARANTEED_STACKS' calibration note in
# balance_weights_notes.md.
GUARANTEED_STACKS = {1: 2, 2: 2, 3: 2, 4: 3, 5: 3}
# Hexes, a stack under EFFECT_STACKS (designer, 2026-11-05).
HEX_STACKS = {1: 2, 2: 2, 3: 3, 4: 3, 5: 4}


def action_category(action):
    a = ACTIONS[action]
    if a.get("kind") in ("support", "heal", "nova"):
        return "support"
    if a.get("kind") == "hex" or a["dmg_type"] not in (None, "Physical"):
        return "spell"
    return "weapon"


# Archetypes: additions only (designer, 2026-11-04: "very few things should
# reduce numbers"). "hp" is Health per Slot. The Defender's Parry turns into
# Health (half a point each) in build_enemy: under the Defense cap a shield
# already takes its Parry there.
ROLE_ADDS = {
    # Resist +1 swapped for Health +3 (designer, 2026-11-05): on Heavy Armor
    # it made walls that physical weapons barely hurt. Health +3 reads about
    # the other archetypes' average (2.6 Health), Resist +1 3.3-4.5.
    "Defender": {"parry": 2, "dodge": 2, "hp": 3},
    "Striker": {"dmg": 1, "speed": 1},
    "Bruiser": {"dmg": 1, "hp": 1, "bodily": 2},
    "Strategist": {"acc": 2, "dodge": 1, "mental": 2, "vigilant": 2},
    "Backup": {"res": 1, "parry": 1, "dodge": 2, "bodily": 2, "mental": 2},
    "Skirmisher": {"speed": 2, "dodge": 2, "acc": 1},
}

# Ability prices in points (1 point = 1 Health per Slot), measured on the
# pruned base (ENEMY_ENCOUNTER_DESIGN.md, "v3 Ability prices", "The pruned
# v3", "Re-pricing"). The light on-hit effects are half a point a stack.
ABILITY_PRICES = {
    "Strike (Crippling)": 0.5, "Strike (Vulnerable)": 0.5, "Strike (Slowing)": 0.5,
    "Strike (Frightening)": 0.5, "Strike (Taunting)": 0.5, "Strike (Necrotic)": 0.5,
    "Strike (Harrying)": 1, "Strike (Devastating)": 1, "Strike (Battering)": 2, "Strike (Cleaving)": 2,
    "Strike (Grappling)": 3, "Area Attack": 5, "Strike (Shoving)": 0,
    "Poison (Crippling)": 0.5, "Poison (Slowing)": 0.5, "Poison (Vulnerable)": 0.5, "Poison (Necrotic)": 0.5,
    "Poison (Bleeding)": 2.5,
    "Heavy Weapon": 1, "Powerful Weapon": 4, "Powerful Spell": 3,
    "Durable": 1, "Omniguard": 1, "Resilient": 0, "Sturdy": 0, "Shadow Jaunt": 0, "Retribution Aura": 2,
    "Enhanced Health": 1, "Enhanced Speed": 1, "Enhanced Reflexes": 2, "Enhanced Range": 3,
    "Improved Support": 1, "Action (Parting Shot)": 1, "Action (Intimidating)": 0, "Action (Taunting)": 1,
}
for _el in ELEMENTS:
    ABILITY_PRICES.update({f"Resist ({_el})": 1, f"Attunement ({_el})": 3,
                           f"Elemental Spell ({_el})": 0, f"Elemental Weapon ({_el})": 0})
# Stat Abilities: a bump each, repeatable up to the player caps.
STAT_ABILITIES = {"Damage +1": ("dmg",), "Accuracy +1": ("acc",), "Parry and Dodge +1": ("parry", "dodge"),
                  "Dodge +1": ("dodge",),
                  "Vital/Mental/Vigilant +1": ("bodily", "mental", "vigilant"), "Resist +1": ("res",)}
ABILITY_PRICES.update({"Damage +1": 4, "Accuracy +1": 2, "Parry and Dodge +1": 1, "Dodge +1": 1,
                       "Vital/Mental/Vigilant +1": 1, "Resist +1": 4})
# Armor from Light (Heavy at 6 and Level 3+ only, designer 2026-11-07/08),
# and the loadouts from Sword and Shield.
ARMOR_PRICES = {"Unarmored": -2, "Light": 0, "Medium": 2, "Heavy": 6}
LOADOUT_PRICES = {"Sword and Shield": 0, "Heavy Weapon and Shield": 1, "Light Two-Handed": 2,
                  "Two-Handed Weapon": 2, "Bow": 0, "Heavy Bow": 1, "Hex": -2}
# Picks: these as often as you like up to the caps, riders up to RIDER_CAP
# stacks (Poisons POISON_CAP, they last past the fight), the rest once.
REPEATABLE = {"Accuracy +1", "Parry and Dodge +1", "Dodge +1", "Vital/Mental/Vigilant +1", "Resist +1",
              "Enhanced Health", "Enhanced Speed"}
RIDER_CAP = 4
POISON_CAP = 2
# The Weak Defense when a row doesn't name one: what that kind of enemy
# visibly neglects, skipping its Strong Defense.
WEAK_DEFAULT = {"weapon": ("mental", "vigilant"), "spell": ("bodily", "vigilant"), "support": ("dodge", "vigilant")}


def build_enemy(name, level, slots, action, armor, strong_defense, role=None, abilities=(),
                main_effect=None, backup_action=None, weak_defense=None):
    t = ENEMY_TABLE[level]
    adds = dict(ROLE_ADDS.get(role or "", {}))
    if role == "Defender":
        adds["hp"] = adds.get("hp", 0) + adds.pop("parry", 0) // 2
    barred = set(T.V3_BIG_BARRED) & set(abilities) if slots >= 2 else set()
    if barred:
        raise ValueError(f"{name}: {', '.join(sorted(barred))} can't be taken by an elite or solo boss")
    for ab in set(abilities):
        n = abilities.count(ab)
        rider = ab.startswith("Strike (") or ab.startswith("Poison (")
        if n > 1 and not rider and ab not in REPEATABLE:
            raise ValueError(f"{name}: {ab} can only be taken once")
        cap = POISON_CAP if ab.startswith("Poison (") else RIDER_CAP
        if rider and n > cap:
            raise ValueError(f"{name}: {ab} taken {n} times, more than {cap}")
    for ab, key in STAT_ABILITIES.items():
        for _ in range(abilities.count(ab)):
            for k in key:
                adds[k] = adds.get(k, 0) + 1
    # Paper defenses (designer, 2026-11-06): Parry is the Level's Skill plus
    # the main weapon's Defense; archetypes and Abilities never raise it.
    adds.pop("parry", None)
    act = ACTIONS[action]
    cat = action_category(action)
    skill = min(SKILL_CAP, t["skill"])
    dmg_stat = min(STAT_CAP, t["damage"] + adds.get("dmg", 0))
    res_stat = min(T.V3_RESIST_CAP or STAT_CAP, t["resist"] + adds.get("res", 0))
    gap = T.V3_DEF_GAP
    strong = strong_defense.lower().replace("vital", "bodily")
    weak = (weak_defense or "").lower().replace("vital", "bodily") or next(
        d for d in WEAK_DEFAULT[cat] if d != strong)
    tier = {d: skill - gap for d in ("dodge", "bodily", "mental", "vigilant")}
    tier[strong] = skill
    if weak != strong:
        tier[weak] = skill - 2 * gap

    def defense(d):
        return 8 + min(SKILL_CAP, tier[d] + adds.get(d, 0))
    parry = 8 + min(SKILL_CAP, skill) + act["wd"] if act["wd"] is not None else -99
    stat = {k: dmg_stat for k in ("body", "cunning", "mind", "agility", "body_or_cunning")}
    stat["essence"] = res_stat

    def profile(action_name):
        a = ACTIONS[action_name]
        sk = t["accuracy"] if action_name == action else t["accuracy"] - 2 * gap
        return dict(action=action_name, accuracy=min(SKILL_CAP, sk + adds.get("acc", 0)) + a["acc_mod"],
                    attack_damage=a["dmg_base"] + stat[a["stat"]] if a["dmg_base"] else 0,
                    dmg_type=a["dmg_type"], opp_def=a["opp_def"],
                    attack_range=a["range"] * level + (2 if a["range"] else 0))
    main = profile(action)
    accuracy, attack_damage = main["accuracy"], main["attack_damage"]
    # Powerful Weapon / Spell: plain +1 Damage on that kind of attack.
    if "Powerful Weapon" in abilities or "Powerful Spell" in abilities:
        if ("Powerful Spell" if cat == "spell" else "Powerful Weapon") in abilities and act["dmg_base"]:
            attack_damage += 1
    elif "Heavy Weapon" in abilities:
        attack_damage += 1
        accuracy -= 1
        parry -= 1
    kind = act.get("kind", "attack")
    effect_stacks = act["stacks"] if "stacks" in act else (
        GUARANTEED_STACKS[level] if kind in ("support", "heal") else
        HEX_STACKS[level] if kind == "hex" else EFFECT_STACKS[level])
    if kind != "attack" and not backup_action:
        raise ValueError(f"{name}: a {action} enemy needs a BackupAction to fall back on")
    backup = profile(backup_action) if backup_action else None
    if backup and backup["attack_damage"]:
        if ("Powerful Spell" if action_category(backup_action) == "spell" else "Powerful Weapon") in abilities:
            backup["attack_damage"] += 1
    if kind != "attack":
        attack_damage = 0
    # One budget: the Level's points (k times them for a big enemy, each
    # point 1/k of its Health) buy Abilities, loadout and armor; what's
    # left is Health, and nothing can be spent past it.
    cost = sum(ABILITY_PRICES[a] for a in abilities) + ARMOR_PRICES[armor] + LOADOUT_PRICES.get(action, 0)
    allowance = T.V3_PRUNED_ALLOWANCE + T.V3_PRUNED_EXTRA.get(level, 0)
    k = T.V3_SLOT_BUDGET.get(slots, 1)
    if cost > allowance * k:
        raise ValueError(f"{name}: Abilities, loadout and armor cost {cost} of its {allowance * k} points")
    base_health = t["health"] + (allowance * k - cost) / k

    def cap_def(value):
        # The Defense cap (designer, 2026-11-06): no Defense above 8 + the
        # Level's Skill + V3_DEFENSE_CAP before armor's Dodge penalty.
        if T.V3_DEFENSE_CAP is None or value <= 0:
            return value
        return min(value, 8 + min(SKILL_CAP, t["skill"]) + T.V3_DEFENSE_CAP)
    mult = (T.V3_SOLO_HEALTH if slots == 4 else T.V3_ELITE_HEALTH if slots == 2 else
            T.V3_MINION_HEALTH if slots == 0.5 else T.SLOT_MULTIPLIER[slots])
    health = math.ceil((base_health + adds.get("hp", 0)) * mult - 1e-9) + abilities.count("Enhanced Health")
    enemy = dict(name=name, level=level, slots=slots, role=role or "None", action=action,
                 kind=kind, main_effect=main_effect or {"support": "Protected", "heal": "Health",
                                                        "nova": "Protected"}.get(kind),
                 effect_stacks=effect_stacks, backup=backup, stats=stat,
                 accuracy=accuracy, attack_damage=attack_damage, dmg_type=act["dmg_type"],
                 opp_def=act["opp_def"], attack_range=main["attack_range"],
                 parry=cap_def(parry), dodge=cap_def(defense("dodge")) + T.ARMOR[armor]["dodge"],
                 bodily=cap_def(defense("bodily")), mental=cap_def(defense("mental")),
                 vigilant=cap_def(defense("vigilant")),
                 physres=res_stat + T.ARMOR[armor]["physres"], elemres=res_stat,
                 health=health, max_health=health,
                 speed=math.ceil(level / 2) + 2 + T.ARMOR[armor]["speed"] + adds.get("speed", 0),
                 reflex=2 + level, ability_budget=0, ability_cost=0, abilities=list(abilities),
                 protected=0, armor=armor, weak_defense=weak)
    _apply_catalog(enemy, abilities)
    return enemy


def _apply_catalog(e, abilities):
    """The catalog's build-time numbers (the rest play out in combat_sim):
    Attunement "+4 Resist to that element, -1 Resist to its opposite",
    Resist "+2 Resist to that element alone", Elemental Spell/Weapon
    retypes the attack (Weapon "at -1 Damage"), Enhanced Range "Range x2
    on the enemy's action", Enhanced Reflexes +3, Enhanced Speed +1,
    Improved Support "+50% (round up)" on heals and Protected grants,
    and Strike (Devastating)'s "Damage +1". Per-element Resist sits in
    `resist_by_type`, on top of the one `elemres` pool."""
    for a in abilities:
        if a.startswith("Attunement ("):
            el = a[len("Attunement ("):-1]
            rbt = e.setdefault("resist_by_type", {})
            rbt[el] = rbt.get(el, 0) + 4
            rbt[OPPOSITE[el]] = rbt.get(OPPOSITE[el], 0) - 1
        elif a.startswith("Resist ("):
            el = a[len("Resist ("):-1]
            rbt = e.setdefault("resist_by_type", {})
            rbt[el] = rbt.get(el, 0) + 2
        elif a.startswith("Elemental Spell (") or a.startswith("Elemental Weapon ("):
            el = a[a.index("(") + 1:-1]
            spell = a.startswith("Elemental Spell")
            for prof in (e, e.get("backup")):
                if not prof or not prof.get("attack_damage"):
                    continue
                is_spell = action_category(prof["action"]) == "spell"
                if is_spell == spell:
                    prof["dmg_type"] = el
                    if not spell:
                        prof["attack_damage"] -= 1
        elif a == "Enhanced Range" and e.get("attack_range"):
            e["attack_range"] *= 2
        elif a == "Enhanced Reflexes":
            e["reflex"] += 3
        elif a == "Enhanced Speed":
            e["speed"] += 1
        elif a == "Improved Support" and e["kind"] in ("support", "heal", "nova"):
            e["effect_stacks"] = math.ceil(e["effect_stacks"] * 1.5)
        elif a == "Strike (Devastating)":
            for prof in (e, e.get("backup")):
                if prof and prof.get("attack_damage"):
                    prof["attack_damage"] += 1
