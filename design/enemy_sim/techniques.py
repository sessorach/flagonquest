"""
Every Technique the sim knows, keyed by its techniques.csv ID - the one
place to look (or add) when a character sheet names a Technique.

A Builder export lists Techniques by ID, one entry per known copy, each
with its Level and (for a Buildable one) its Features. party.py hands
each ID's copies to that ID's entry here, which says what the Technique
adds to the character: a passive the fight checks for, a Card
Technique, an Encounter Technique's uses, an attack profile, a hex, a
Battle Maneuver copy's Features. An ID with no entry stops the load
with its name - add an entry, or list it in OUT_OF_COMBAT if it never
matters in a fight - so a sheet can't quietly lose a Technique. A
Feature the entry doesn't model stops it the same way.

Each Technique has up to three parts, all in this file:
- `build(sheet, copies, choices)`: what it adds to the character sheet,
  from the export (registered with @technique, by ID);
- `setup(pc, s)`: what it puts on the fight dict once the sheet's
  numbers are worked out - its uses, a range, a profile (@setup_for, by
  name, so a test that adds the passive by name gets it too);
- hooks: what it does in the fight (@hooks.on, by name; see hooks.py for
  the points and the order they run in).
Adding a Technique means adding those here, and a new hook point in
combat_sim only if it does something none of the existing points cover.
"""
import collections
from types import SimpleNamespace

import game_data
import hooks

REGISTRY = {}

# IDs that never matter in a fight: the loader accepts them and moves on.
OUT_OF_COMBAT = {
    "T002": "Soulblade (the weapon it makes is the row's Weapon)",
    "T004": "Vow of Poverty", "T007": "Bound Across Mountains", "T034": "Legerdemain",
    "T036": "Patch Up", "T039": "Quick Draw", "T042": "Shadow's Path", "T059": "Follower",
    "T063": "Favorite Face", "T065": "Rumormonger", "T141": "Spacious Gut", "T142": "Gorger",
    "T144": "Distraction", "T027": "Profession", "T068": "Dominate Mind",
    # Health only: the loader adds techniques.csv's Health bonus columns
    # for every Technique, so these need nothing else.
    "T014": "Toughened Body", "T023": "Toughened Spirit",
}


class BuildError(ValueError):
    pass


class Technique:
    def __init__(self, tid, name, build, features=()):
        self.tid, self.name, self.build = tid, name, build
        self.features = set(features)  # Features this sim models (Buildable ones)

    def check_features(self, copies):
        for c in copies:
            for f in c["features"]:
                if f not in self.features:
                    raise BuildError(f"{self.name}: Feature {f!r} isn't modeled "
                                     f"(techniques.py knows {sorted(self.features) or 'none'})")


def technique(tid, name, features=()):
    """Registers `fn(sheet, copies, choices)` as the build for `tid`.
    `copies` is the export's entries for that ID, each {"level": int,
    "features": {name: count}}; `choices` the row's per-copy picks for
    this Technique (Choices column), one string per copy, if any."""
    def deco(fn):
        REGISTRY[tid] = Technique(tid, name, fn, features)
        return fn
    return deco


# ---- Simple kinds: a passive name, a Card Technique, Encounter uses ----

def _passive(tid, name):
    technique(tid, name)(lambda sheet, copies, choices: sheet.passives.append(name))


def _card(tid, name):
    technique(tid, name)(lambda sheet, copies, choices: sheet.card_techniques.append(name))


def _encounter(tid, name):
    # One entry per known copy: each copy is one use a fight.
    technique(tid, name)(lambda sheet, copies, choices: sheet.encounter_techs.extend([name] * len(copies)))


for _tid, _name in (("T010", "Grim Resolve"), ("T011", "One Eye Behind You"), ("T019", "Toughened Resolve"),
                    ("T035", "Mighty Mixologist"), ("T069", "Raise Spirits"), ("T079", "Cloak and Dagger"),
                    ("T128", "Lawman's Hand"), ("T130", "Furious Rage"), ("T131", "Hand of Chaos"),
                    ("T132", "Indomitable Phalanx"), ("T133", "Placeholder's Lengthy Ley-weaving"),
                    ("T137", "Eagle Eyes"), ("T139", "Inexhaustible Guardian"), ("T140", "Overchanneling"),
                    ("T175", "Boughs Unbroken"), ("T192", "Seize the Moment"), ("T193", "Lie in Wait"),
                    ("T194", "Ambush Predator"), ("T197", "Command the Tempo"),
                    # Healer Styles (2026-10-26), read by tactics._heal_one.
                    ("T189", "Field Medic"), ("T190", "Lifeward")):
    _passive(_tid, _name)

for _tid, _name in (("T012", "Second Wind"), ("T053", "Bottomless Bottles"), ("T078", "Perfect Strike"),
                    ("T124", "Warmage's Reserves")):
    _card(_tid, _name)

for _tid, _name in (("T001", "Brace"), ("T018", "Strength from the Slain"), ("T058", "Challenge"),
                    ("T067", "Exert Pressure"), ("T076", "Parting Shot"), ("T077", "Blinkstep"),
                    ("T097", "Shadow Jaunt"), ("T107", "Gust of Wind"), ("T110", "Lifeline"),
                    ("T122", "Gainsay"), ("T123", "Wall of Shadows")):
    _encounter(_tid, _name)


# ---- Technique attacks: swapped in for a normal attack, one use a copy ----
# Each builds the attack profile combat_sim's attack loop overlays for one
# use: (stats, skills, weapon Skill Total, weapon Damage) -> profile.
# `effect` is what a hit puts on the target: (key, stacks, bonus suit), the
# suit adding 1 more stack when it's flipped. `skill` is the attack's Skill
# (for its suit); `weapon` marks a weapon attack, the only kind that can be
# Gambled on (rulebook.md).

def _st(stats, skills, skill):
    import party  # skill_total lives with the rest of the sheet formulas
    return party.skill_total(stats, skills, skill)


def _unarmed_vs_mental(effect=None):
    # Shugen School weapon strikes: "Make an Unarmed weapon attack against
    # the target's Mental Defense. If it hits, it deals Brilliant damage"
    # - the PC's own Unarmed attack, redirected. Assumes the PC's Weapon
    # is Unarmed, which holds for every row that knows one.
    return lambda st, sk, atk, dmg: dict(skill_total=atk, damage=dmg, dmg_type="Brilliant",
                                         opp_def="Mental", effect=effect, skill="Brawl", weapon=True)


def _tech_attack(tid, name, factory):
    technique(tid, name)(lambda sheet, copies, choices: sheet.tech_attacks.append((name, factory, len(copies))))


# T154, Level 2, 2 AP: "...and the target is Slowed 2 + [Spades] times."
_tech_attack("T154", "Hand Rings the Bell", _unarmed_vs_mental(("slowed", 2, "Spades")))
# T080, Level 1, 2 AP: "Make a Meditation attack against the target's
# Mental Defense. If it hits, it deals 2 + [Mind] Brilliant damage."
_tech_attack("T080", "Firefly Leaves the Hand", lambda st, sk, atk, dmg: dict(
    skill_total=_st(st, sk, "Meditation"), damage=2 + int(st["Mind"]),
    dmg_type="Brilliant", opp_def="Mental", effect=None, skill="Meditation"))
# T159, Level 2, 2 AP: "Make a Meditation attack against the target's
# Vital Defense. If it hits, it deals 2 + [Mind] Shadow damage, and you
# may discard a card to heal 3 Health." The heal is taken when he's
# missing 3 or more (designer, 2026-10-09).
_tech_attack("T159", "Thief Empties the Vessel", lambda st, sk, atk, dmg: dict(
    skill_total=_st(st, sk, "Meditation"), damage=2 + int(st["Mind"]),
    dmg_type="Shadow", opp_def="Vital", effect=None, skill="Meditation", heal_on_hit=3))


# ---- Hexes: cast at the start of a turn (combat_sim._try_hexes) ----

@technique("T111", "Reckoning")
def _reckoning(sheet, copies, choices):
    # T111, Level 2, 2 AP, "A creature within [Theurgy Skill Total]
    # meters": "Make a Theurgy spell attack against the target's Mental
    # Defense. If it hits, they are Crippled 5 + [Clubs] times."
    sheet.hexes.append(dict(via="Reckoning", kind="crippled", amount=5, suit="Clubs", opp_def="Mental",
                            skill="Theurgy", uses=len(copies), ranged=True))


# ---- War Magic (T120): every copy is built from its own Features ----

def _war_magic_name(feats):
    return "War Magic (" + ", ".join(f if n == 1 else f"{f} {n}" for f, n in feats.items()) + ")"


@technique("T120", "War Magic", features=(
        "Lance", "Destructive", "Sanguine", "Reign of Blood", "Draw Power", "Furrow (Shape)", "Funnel (Shape)",
        "Nova (Shape)", "Tormenting Curse", "Frigid", "Kinetic", "Corrupting", "Necrotic", "Barraging", "Abjuring",
        "Piercing Elements", "Wild Magic"))
def _war_magic(sheet, copies, choices):
    """Copies with the same Features and Defense are one profile with that
    many uses. A plain Lance copy is the row's own War Magic (Lance)
    Weapon, counted in Weapon Uses. Tormenting Curse ("deals no damage")
    makes a hex of the copy's Frigid ("Slowed [twice X] + [Spades]
    times") or Kinetic ("Pushed up to [four times X] + Spades meters").
    Everything else is a damaging technique attack: 2 + [Mind] Fire,
    Destructive "an extra X damage", Sanguine "an extra 3 damage" that
    becomes Bleeding, Reign of Blood cashing in [twice X] stacks, Furrow
    a line [half your Sorcery Skill Total] long (which is also its reach
    without Lance), Draw Power a card on a Down. Lance is the reach of
    the Weapon itself, so a Lance copy needs no range of its own. The
    rest of the Features ride on the hit (combat_sim and this file's
    War Magic hooks): Frigid, Kinetic, Corrupting, Necrotic, Barraging,
    Abjuring, Piercing Elements, Wild Magic, Funnel and Nova. Arcane
    Chant, Glacier (no Difficult Terrain in the sim) and Channel aren't
    modeled, so a copy with one stops the load.
    War Magic is learned against Dodge or Vital (the Choices column, per
    copy; Dodge when blank)."""
    groups = collections.OrderedDict()
    for i, c in enumerate(copies):
        defense = choices[i] if i < len(choices) and choices[i] else "Dodge"
        key = (tuple(sorted(c["features"].items())), defense)
        groups.setdefault(key, [c["features"], defense, 0])[2] += 1
    for feats, defense, n in groups.values():
        name = _war_magic_name(feats)
        if set(feats) == {"Lance"} and sheet.weapon.startswith("War Magic") and defense == "Dodge":
            sheet.weapon_uses = (sheet.weapon_uses or 0) + n
            continue
        if "Tormenting Curse" in feats:
            # The hex lands its first rider of these: Frigid "Slowed [twice
            # X] + [Spades]", Kinetic "Pushed up to [four times X] + Spades
            # meters", Corrupting "[twice X] + [Diamonds] Vulnerable",
            # Necrotic "[twice X] + [Diamonds] Necrotic", Barraging "Harried
            # X + [Hearts]".
            for feat, kind, mult, suit in (("Frigid", "slowed", 2, "Spades"), ("Kinetic", "push", 4, "Spades"),
                                           ("Corrupting", "vulnerable", 2, "Diamonds"),
                                           ("Necrotic", "necrotic", 2, "Diamonds"),
                                           ("Barraging", "harried", 1, "Hearts")):
                if feat in feats:
                    break
            else:
                raise BuildError(f"{name}: a Tormenting Curse copy needs a rider (Frigid, Kinetic, Corrupting, "
                                 "Necrotic or Barraging) to do anything here")
            sheet.hexes.append(dict(via=name, kind=kind, amount=mult * feats[feat], suit=suit, opp_def=defense,
                                    skill="Sorcery", uses=n, ranged="Lance" in feats))
            continue
        if sum(1 for f in feats if f.endswith("(Shape)")) > 1:
            raise BuildError(f"{name}: only one Shape feature per Spell")
        sheet.tech_attacks.append((name, _war_magic_factory(feats, defense), n))


def _war_magic_factory(feats, defense):
    def build(st, sk, atk, dmg):
        sorcery = _st(st, sk, "Sorcery")
        prof = dict(skill_total=sorcery, damage=2 + int(st["Mind"]) + feats.get("Destructive", 0),
                    dmg_type="Fire", opp_def=defense, effect=None, skill="Sorcery")
        if feats.get("Sanguine"):
            prof["damage"] += 3 * feats["Sanguine"]
            prof["sanguine"] = True
        if feats.get("Reign of Blood"):
            prof["cashout"] = 2 * feats["Reign of Blood"]
        if feats.get("Furrow (Shape)"):
            prof["line"] = sorcery // 2
            if "Lance" not in feats:
                prof["range"] = sorcery // 2
        if feats.get("Draw Power"):
            prof["draw_power"] = True
        # Funnel: "all creatures within a 2-meter-long cone". Nova: "all
        # adjacent creatures", so it reaches only what's next to you.
        if feats.get("Funnel (Shape)"):
            prof["cone"] = 2
            prof["range"] = 2
        if feats.get("Nova (Shape)"):
            prof["nova"] = True
            prof["range"] = 1
        # Riders on the hit, each [twice X] or the like + its suit:
        # Frigid "Slowed [twice X] + [Spades] times", Kinetic "Pushed up to
        # [four times X] + Spades meters", Corrupting "[twice X] +
        # [Diamonds] stacks of Vulnerable", Necrotic "[twice X] +
        # [Diamonds] stacks of Necrotic" (before damage), Barraging
        # "Harried X + [Hearts] stacks" on a hit or a Dodge, Abjuring "X + 1
        # stacks of [attack's damage type] Ward + [Hearts]" afterwards.
        for key, feat in (("frigid", "Frigid"), ("kinetic", "Kinetic"), ("corrupting", "Corrupting"),
                          ("necrotic", "Necrotic"), ("barraging", "Barraging"), ("abjuring", "Abjuring"),
                          ("wild", "Wild Magic")):
            if feats.get(feat):
                prof[key] = feats[feat]
        if feats.get("Piercing Elements"):
            prof["piercing"] = feats["Piercing Elements"]  # Good Luck on the spell attack
        # "You may change the attack's damage type to Frost / Shadow."
        types = ["Fire"] + (["Frost"] if feats.get("Frigid") else []) + (
            ["Shadow"] if any(feats.get(f) for f in ("Corrupting", "Necrotic", "Draw Power")) else [])
        if len(types) > 1:
            prof["dmg_types"] = types
        return prof
    return build


# ---- Buildable Techniques whose Features the fight reads ----

@technique("T072", "Battle Maneuver", features=(
        "Lunging", "Half Guard", "Battering", "Whirlwind", "Victorious", "Ascended Blade", "Wind Slash",
        "Calculated", "Wing Clip", "Hamstring", "Harrying", "Distracting", "Bare-Handed", "Turn Elements",
        "Backfoot", "Lodestone", "Blade of Four Fates", "Elemental", "Viper's Sting", "Fleet Step",
        "Ricochet Shot", "Flurry",
        # A draft Feature (2026-10-16): Reign of Blood's text on a Battle
        # Maneuver, only on the Felix (Cash) test build.
        "Open the Wound"))
def _battle_maneuver(sheet, copies, choices):
    """Each copy keeps its own Features, used in the sheet's order. Turn
    Elements and Elemental need an element, per copy in the Choices
    column ("Battle Maneuver: , Frost" for the second copy)."""
    sheet.encounter_techs.extend(["Battle Maneuver"] * len(copies))
    for i, c in enumerate(copies):
        feats = dict(c["features"])
        if "Turn Elements" in feats or "Elemental" in feats:
            element = choices[i] if i < len(choices) else ""
            if element not in ("Fire", "Frost", "Brilliant", "Shadow"):
                raise BuildError(f"Battle Maneuver copy {i + 1}: Turn Elements/Elemental needs an element in Choices")
            if "Elemental" in feats and element == "Brilliant":
                raise BuildError("Battle Maneuver: Elemental is Fire, Frost or Shadow")
            feats["_element"] = element
        sheet.maneuvers.append(feats)


@technique("T104", "Spirit Blessing", features=(
        "Shielding", "Step of Air", "Guided Hand", "Quickened", "Reach", "Mass Blessing", "Turn Elements",
        "Steady", "Embolden", "Retribution", "River's Might", "Touch of Chaos", "Elemental Enhancement",
        "Alacrity", "Steal Fate"))
def _spirit_blessing(sheet, copies, choices):
    """Copies built the same way share one entry; copies built differently
    (2026-10-26) are separate entries, tried in the sheet's order, one cast
    a turn. Turn Elements and Elemental Enhancement take their element from
    Choices, per copy."""
    sheet.encounter_techs.extend(["Spirit Blessing"] * len(copies))
    groups = []
    for i, c in enumerate(copies):
        feats = dict(c["features"])
        if "Turn Elements" in feats or "Elemental Enhancement" in feats:
            element = choices[i] if i < len(choices) else ""
            if element not in ("Fire", "Frost", "Brilliant", "Shadow"):
                raise BuildError(f"Spirit Blessing copy {i + 1}: Turn Elements/Elemental Enhancement needs an "
                                 "element in Choices")
            feats["_element"] = element
        for g in groups:
            if g[0] == feats:
                g[1] += 1
                break
        else:
            groups.append([feats, 1])
    sheet.blessing_features = groups[0][0]
    sheet.blessing_groups = groups


@technique("T105", "Healing Magic", features=("Vitality", "Reach", "Purify", "Rejuvenate", "Guardian Angel",
                                               "Triage", "Deep Mending", "Healing Pact"))
def _healing_magic(sheet, copies, choices):
    """A Support PC's Healing Magic: "Discard [this Spell's Level] cards"
    (Heal Cards), Vitality "+1 healing" per copy (Heal Bonus), and
    "Yourself or an adjacent ally" plus Reach and Ley-weaving (Heal Range,
    finished by the loader once every passive is known). The healer's
    play (tactics.strategy_support_healer) comes with it."""
    c = copies[0]
    sheet.support = True
    sheet.heal_cards = c["level"]
    sheet.heal_bonus = c["features"].get("Vitality", 0)
    sheet.heal_reach = "Reach" in c["features"]
    # Read by tactics.strategy_support_healer. Deep Mending ("may apply to
    # Deep or Shallow Health") changes nothing here: the sim keeps one
    # Health pool and heals it up to the top.
    sheet.heal_features = {f: n for f, n in c["features"].items()
                           if f in ("Purify", "Rejuvenate", "Guardian Angel", "Triage", "Healing Pact")}


@technique("T003", "Temper Soulblade")
def _temper_soulblade(sheet, copies, choices):
    """The Masterwork power picked for each copy is the Choices column (it
    isn't in the export). Only Fatestealer at Level 1 is modeled
    (combat_sim._fatestealer)."""
    for i, c in enumerate(copies):
        power = choices[i] if i < len(choices) else ""
        if power != "Fatestealer" or c["level"] != 1:
            raise BuildError(f"Temper Soulblade: {power or 'no power picked'} at Level {c['level']} isn't modeled "
                             "(only Fatestealer at Level 1)")
        sheet.passives.append("Fatestealer")


# ---- Setup: what a Technique puts on the fight dict ----

SETUP = {}


def setup_for(*names):
    def deco(fn):
        for n in names:
            SETUP[n] = fn
        return fn
    return deco


def setup(name, pc, s):
    fn = SETUP.get(name)
    if fn:
        fn(name, pc, s)


def _skill(s, skill):
    return _st(s.stats, s.skills, skill)


@setup_for("Brace", "Strength from the Slain", "Exert Pressure")
def _uses(name, pc, s):
    # Brace (T001, 3 Protected), Strength from the Slain (T018, eaten
    # after a kill), Exert Pressure (T067, a Taunt on everyone close): one
    # use per known copy.
    key = {"Brace": "brace_uses_left", "Strength from the Slain": "slain_uses_left",
           "Exert Pressure": "pressure_uses_left"}[name]
    pc[key] = s.uses[name]


@setup_for("Toughened Resolve")
def _toughened_resolve(name, pc, s):
    # T019: +2 Shallow and +2 Deep Health. The Health total already counts
    # both; this moves where Wounded starts.
    pc["shallow_max"] += 2


@setup_for("Shadow Jaunt")
def _shadow_jaunt_setup(name, pc, s):
    pc["jaunt_uses_left"] = s.uses[name]
    pc["jaunt_range"] = max(_skill(s, "Sorcery"), _skill(s, "Theurgy"))


@setup_for("Gainsay")
def _gainsay_setup(name, pc, s):
    pc["gainsay_uses_left"] = s.uses[name]


@setup_for("Wall of Shadows")
def _wall_setup(name, pc, s):
    pc["wall_uses_left"] = s.uses[name]
    pc["sorcery_skill_total"] = _skill(s, "Sorcery")


@setup_for("Blinkstep")
def _blinkstep_setup(name, pc, s):
    pc["blinkstep"] = True


@setup_for("Parting Shot")
def _parting_shot_setup(name, pc, s):
    pc["parting_shot"] = True
    # "a close-range weapon you are wielding": the Weapon itself if it
    # works up close (thrown weapons and melee), else Unarmed.
    if s.weapon == "Light Bow" or s.weapon.startswith("War Magic"):
        import tunables as T
        u = T.WEAPON["Unarmed"]
        pc["close_profile"] = dict(skill_total=_skill(s, "Brawl") + u["accuracy"],
                                   damage=u["damage_base"] + max(int(s.stats["Body"]), int(s.stats["Cunning"])),
                                   dmg_type="Physical", opp_def="Parry/Dodge", skill="Brawl", via="Unarmed")
    else:
        pc["close_profile"] = dict(skill_total=s.atk_skill_total, damage=s.damage, dmg_type=s.dmg_type,
                                   opp_def=s.opp_def, skill=s.w_skill, via=s.weapon_name)


@setup_for("Lifeline")
def _lifeline_setup(name, pc, s):
    pc["lifeline_uses_left"] = s.uses[name]
    pc["lifeline_range"] = _skill(s, "Theurgy") + s.ley


def _blessing_features(feats, theurgy, ley):
    """Spirit Blessing's Features as numbers: Shielding X is Protected
    X + 1, Step of Air X Hasted X + 1, Guided Hand X Good Luck on the next
    X attacks, Quickened makes it 1 AP, Reach adds [Theurgy Skill Total]
    meters to "yourself or an adjacent ally", Mass Blessing a second
    target. The rest (2026-10-25): Turn Elements X Ward X + 1, Steady and
    Embolden one stack off, Retribution / River's Might / Steal Fate / Elemental
    Enhancement X charges, Touch of Chaos [twice X] Sifted flips, Alacrity
    2 places up the turn order."""
    return dict(protected=feats["Shielding"] + 1 if "Shielding" in feats else 0,
                hasted=feats["Step of Air"] + 1 if "Step of Air" in feats else 0,
                guided=feats.get("Guided Hand", 0),
                ap=1 if "Quickened" in feats else 2,
                range=1 + (theurgy if "Reach" in feats else 0) + ley,
                targets=2 if "Mass Blessing" in feats else 1,
                ward=feats["Turn Elements"] + 1 if "Turn Elements" in feats else 0, element=feats.get("_element"),
                steady=feats.get("Steady", 0), embolden=feats.get("Embolden", 0),
                retribution=feats.get("Retribution", 0), rivers=feats.get("River's Might", 0),
                chaos=2 * feats.get("Touch of Chaos", 0), enhance=feats.get("Elemental Enhancement", 0),
                alacrity=2 if "Alacrity" in feats else 0, steal=feats.get("Steal Fate", 0))


@setup_for("Spirit Blessing")
def _blessing_setup(name, pc, s):
    groups = s.sheet.blessing_groups
    pc["blessings"] = [dict(uses=s.uses[name] if len(groups) == 1 else n,
                            **_blessing_features(feats, _skill(s, "Theurgy"), s.ley)) for feats, n in groups]
    pc["blessing"] = pc["blessings"][0]


@setup_for("Gust of Wind")
def _gust_setup(name, pc, s):
    pc["gust_uses_left"] = s.uses[name]
    pc["theurgy_skill_total"] = _skill(s, "Theurgy")
    pc["gust_push"] = 2 * int(s.stats["Mind"])


@setup_for("Cloak and Dagger", "Grim Resolve")
def _flag_setup(name, pc, s):
    # Cloak and Dagger (T079) was a test-only field before Carrick had it.
    pc["cloak_and_dagger" if name == "Cloak and Dagger" else "grim_resolve"] = True


@setup_for("Raise Spirits")
def _raise_spirits_setup(name, pc, s):
    # T069: "an ally within [Performance Skill Total] meters".
    pc["raise_range"] = _skill(s, "Performance")


def get(tid):
    t = REGISTRY.get(tid)
    if t is None and tid not in OUT_OF_COMBAT:
        raise BuildError(f"{tid} {game_data.technique_name(tid)} isn't in techniques.py: add an entry "
                         "(or list it in OUT_OF_COMBAT)")
    return t


# ======================================================================
# In the fight: each Technique's hooks (hooks.py) and the functions they
# call. `cs` is combat_sim, set when it finishes loading (combat_sim
# imports party, which imports this file, so it can't be imported here).
# ======================================================================
cs = None


def _cast_hex(pc, hx, e, pcs, allies, rnd, trace, log):
    """One of Enith's hexes at `e`: a Sorcery spell attack against the
    hex's own Defense (Sloth Dodge, Rebuking Vital), no damage; on a hit,
    Slowed or Pushed by its amount plus the suit. Raise Spirits and Hand
    of Chaos apply (it's an attack); a miss is worth a card. Only the
    Dodge one Harries its target. A Push goes straight away from the
    middle of the party (glossary.md [Pushing]: "forcibly moved", not
    moving). Returns AP."""
    hx['uses'] -= 1
    defense = cs.enemy_defense_for_pc_attack(hx, e)
    mod = hx['skill_total'] - pc.get('crippled', 0)
    good = pc.get('good_luck', 0) + cs._raise_spirits(pc, pcs, defense - mod, True)
    bad = cs._pc_status_bad_luck(pc, e)
    cover = cs._cover_bad_luck(pc, e, hx['opp_def'])
    if cover:
        bad = int(bad) + cover
    value, pool = cs._pc_flip(pc, mod, defense, good, bad, cs.BIG, pcs, cs._hand_of_chaos(pc))
    hit = mod + value >= defense
    if hx['opp_def'] in ('Parry/Dodge', 'Dodge'):
        e['harried'] = e.get('harried', 0) + 1
    note = start = None
    if hit:
        n = hx['amount'] + cs._suit_count(pool, hx['suit'])
        if hx['kind'] in ('slowed', 'crippled', 'vulnerable', 'necrotic'):
            cs._gain(e, hx['kind'], n)
            note = f"{hx['kind'].capitalize()} +{n}"
        elif hx['kind'] == 'harried':
            e['harried'] = e.get('harried', 0) + n
            note = f"Harried +{n}"
        else:
            cx = round(sum(p['pos'][0] for p in allies) / len(allies))
            cy = round(sum(p['pos'][1] for p in allies) / len(allies))
            start = cs._push(e, (cx, cy), n)
            note = f"Pushed {cs._distance(start, e['pos'])} m (up to {n})"
    pc['hexes_cast'] = pc.get('hexes_cast', 0) + 1
    pc['hexes_hit'] = pc.get('hexes_hit', 0) + hit
    if log:
        log(unit=pc['name'], action='hex', target=e['name'], roll=mod + value, defense=defense, hit=hit,
            dmg=0, raw_dmg=0, resist=0, target_hp_after=e['health'], target_harried_after=e.get('harried', 0),
            via=hx['via'], effects=note, cards=cs._take_notes(pc), opp_def=hx['opp_def'])
    pc.pop('_notes', None)
    if start is not None:
        cs._log(trace, round=rnd, side='enemy', unit=e['name'], action='move', pos=e['pos'],
             spaces=cs._distance(start, e['pos']), in_range=False, via=f"Pushed by {hx['via']}")
        # Parting Shot: "would move or be Pushed outside your range".
        if cs._CTX.get('ps_pcs'):
            cs._parting_shots_on(e, start, pcs, log, pushed=True)
    return cs.T.ATTACK_AP_COST


def _try_hexes(pc, pcs, enemies, rnd, movement_on, trace, log, ap):
    """Enith's hexes (Hex of Sloth, Slowed 6 + [Spades]; Hex of Rebuking,
    Pushed 12 + [Spades] meters), each once a fight, range 5. Per the
    designer (2026-10-09) she's a tactical disabler: the hexes split
    enemies up and isolate them so the party can divide and conquer. At
    the start of her turn, in order:

    1. With both left and 4 AP: the biggest melee threat that's engaged
       with the party and still fresh gets Slowed, then Pushed away. A
       Speed 4 enemy with 6+ Slowed can't move for about three turns.
    2. An enemy in melee with a fragile ally (a back-liner, someone
       Wounded, or Enith) gets Pushed off them.
    3. A melee enemy still on its way in gets Slowed.

    A Push needs at least two enemies standing: with one left there's
    nothing to split up. Returns the AP spent."""
    ready = {h['kind']: h for h in pc.get('hexes', ()) if h['uses'] > 0}
    if not ready or not movement_on or ap < cs.T.ATTACK_AP_COST:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    allies = [p for p in pcs if p['health'] > 0]
    # Reckoning (T111, Hanforth's Level 2 build): Crippled 5 + [Clubs] on
    # the biggest threat in reach that isn't Crippled yet - any enemy, not
    # just a melee one.
    # A Tormenting Curse with Corrupting, Necrotic or Barraging goes the
    # same way: the biggest threat in reach that hasn't got it yet.
    for kind in ('crippled', 'vulnerable', 'necrotic', 'harried'):
        hx = ready.pop(kind, None)
        if not hx:
            continue
        pool = [e for e in living if cs._distance(pc['pos'], e['pos']) <= hx['range'] and e.get(kind, 0) <= 0]
        if pool:
            return _cast_hex(pc, hx, max(pool, key=lambda e: cs.tactics.enemy_threat(e, allies)),
                             pcs, allies, rnd, trace, log)
    if not ready:
        return 0
    in_range = [e for e in living if cs._distance(pc['pos'], e['pos']) <= max(h['range'] for h in ready.values())
                and (e.get('attack_range') or 0) <= cs.T.MELEE_RANGE]
    if not in_range:
        return 0

    def engaged(e):
        return [p for p in allies if cs._distance(p['pos'], e['pos']) <= cs.T.MELEE_RANGE]

    def fragile(p):
        return p is pc or p.get('play_style') == 'Back-liner' or cs.tactics.pc_wounded(p)

    def threat(e):
        return cs.tactics.enemy_threat(e, allies)
    slow, push = ready.get('slowed'), ready.get('push')
    if len(living) < 2:
        push = None
    if slow and push and ap >= 2 * cs.T.ATTACK_AP_COST:
        fresh = [e for e in in_range if engaged(e) and e['health'] > e['max_health'] / 2]
        if fresh:
            e = max(fresh, key=threat)
            return (_cast_hex(pc, slow, e, pcs, allies, rnd, trace, log)
                    + _cast_hex(pc, push, e, pcs, allies, rnd, trace, log))
    if push:
        on_fragile = [e for e in in_range if any(fragile(p) for p in engaged(e))]
        if on_fragile:
            return _cast_hex(pc, push, max(on_fragile, key=threat), pcs, allies, rnd, trace, log)
    if slow:
        coming = [e for e in in_range if not engaged(e)]
        if coming:
            return _cast_hex(pc, slow, max(coming, key=threat), pcs, allies, rnd, trace, log)
    return 0


def _try_challenge(pc, pcs, enemies, movement_on, log=None):
    """Challenge (T058, 1 AP, Encounter): "Make a Presence attack
    against the target's Mental Defense. If the attack hits, you Taunt
    the target 5 + [Hearts] times." Range [Presence Skill Total]
    meters. Used on an enemy nobody's already Taunting, picking the one
    closest to the party's most fragile member (lowest max Health, then
    lowest current Health) - the whole point is pulling attacks off
    whoever can't take them. Returns the AP spent (0 or 1)."""
    if pc.get('challenge_uses_left', 0) <= 0:
        return 0
    pool = [e for e in enemies if e['health'] > 0 and not (e.get('taunted', 0) > 0)]
    if movement_on:
        pool = [e for e in pool if cs._distance(pc['pos'], e['pos']) <= pc['presence_skill_total']]
    if not pool:
        return 0
    others = [p for p in pcs if p['health'] > 0 and p is not pc]
    if movement_on and others:
        ward = min(others, key=lambda p: (p['max_health'], p['health']))
        target = min(pool, key=lambda e: cs._distance(e['pos'], ward['pos']))
    else:
        target = pool[0]
    pc['challenge_uses_left'] -= 1
    defense = target['mental'] - target.get('vulnerable', 0)
    if cs.T.CARDS:
        good = cs._raise_spirits(pc, pcs, defense - pc['presence_skill_total'], True)
        value, pool = cs._pc_flip(pc, pc['presence_skill_total'], defense, good, cs.tactics.pc_wounded(pc), cs.BIG,
                               allies=pcs)
    else:
        value, pool = cs.flip(), []
    roll = pc['presence_skill_total'] + value
    hit = roll >= defense
    if hit:
        stacks = 5 + cs._suit_count(pool, 'Hearts')
        if target.get('taunted', 0) <= 0 and cs._skips(target):
            target['skip_taunted'] = True
        target['taunted'] = stacks
        target['taunted_by'] = pc
    if log:
        log(unit=pc['name'], action='taunt', target=target['name'], roll=roll, defense=target['mental'], hit=hit,
            via='Challenge', effects=f"Taunted +{target['taunted']}" if hit else None, cards=cs._take_notes(pc))
    pc.pop('_notes', None)
    return 1


def _try_brace(pc, enemies, movement_on, ap, start, log=None):
    """Brace (T001, 1 AP, Encounter): "You gain 3 stacks of Protected."
    Taken with AP left over at the end of a turn while an enemy is close
    enough to come for this PC, or at the start of a turn spent in melee
    unprotected (round 2 on, giving up the second attack). Returns the AP
    spent."""
    if pc.get('brace_uses_left', 0) <= 0 or ap < 1 or pc.get('protected', 0) > 0:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    if not living:
        return 0
    if movement_on:
        near = min(cs._distance(pc['pos'], e['pos']) for e in living)
        if start and not (near <= cs.T.MELEE_RANGE and ap >= cs.T.ATTACK_AP_COST + 1 and pc.get('acted_round', 1) >= 2):
            return 0
        if not start and near > cs.T.BRACE_THREAT_RANGE:
            return 0
    elif start:
        return 0
    pc['brace_uses_left'] -= 1
    cs._gain(pc, 'protected', 3)
    if log:
        log(unit=pc['name'], action='technique', via='Brace', effects='Protected +3')
    return 1


def _try_exert_pressure(pc, pcs, enemies, movement_on, ap=1, log=None):
    """Exert Pressure (T067, 1 AP, Encounter): "Make a Presence attack
    against the Mental Defense of each target [any number of creatures
    within 2 meters]. You Taunt each target hit 3 + [Hearts] times."
    Used at the start of a turn or with AP left at its end, once two or
    more enemies are that close and at least one isn't already Taunted by
    this PC; it goes on the ones that aren't. Returns the AP spent."""
    if pc.get('pressure_uses_left', 0) <= 0 or ap < 1:
        return 0
    near = [e for e in enemies if e['health'] > 0]
    if movement_on:
        near = [e for e in near if cs._distance(pc['pos'], e['pos']) <= 2]
    pool = [e for e in near if e.get('taunted_by') is not pc]
    if len(near) < 2 or not pool:
        return 0
    pc['pressure_uses_left'] -= 1
    for target in pool:
        defense = target['mental'] - target.get('vulnerable', 0)
        if cs.T.CARDS:
            good = cs._raise_spirits(pc, pcs, defense - pc['presence_skill_total'], True)
            value, flipped = cs._pc_flip(pc, pc['presence_skill_total'], defense, good, cs.tactics.pc_wounded(pc), cs.BIG,
                                      allies=pcs)
        else:
            value, flipped = cs.flip(), []
        roll = pc['presence_skill_total'] + value
        hit = roll >= defense
        if hit:
            if target.get('taunted', 0) <= 0 and cs._skips(target):
                target['skip_taunted'] = True
            target['taunted'] = 3 + cs._suit_count(flipped, 'Hearts')
            target['taunted_by'] = pc
        if log:
            log(unit=pc['name'], action='taunt', target=target['name'], roll=roll, defense=target['mental'],
                hit=hit, via='Exert Pressure', effects=f"Taunted +{target['taunted']}" if hit else None,
                cards=cs._take_notes(pc))
        pc.pop('_notes', None)
    return 1


def _strength_from_slain(pc, corpse, log=None):
    """Strength from the Slain (T018, 1 AP, Level 3): eat the heart of an
    adjacent creature just Downed - Hasted and Protected three times each,
    and Good Luck on one Melee (or other Body/Agility-skill) flip this
    encounter, which the next attack takes."""
    pc['slain_uses_left'] -= 1
    cs._gain(pc, 'hasted', 3)
    cs._gain(pc, 'protected', 3)
    pc['gl_next'] = pc.get('gl_next', 0) + 1
    if log:
        log(unit=pc['name'], action='technique', target=corpse['name'], via='Strength from the Slain',
            effects='Hasted +3, Protected +3, Good Luck')


def _boughs_cleanse(pc):
    """Great Old Oak School - Boughs Unbroken (T175): "When one of your
    Unarmed attacks hits, choose Bleeding, Crippled, Frightened, Necrotic,
    Slowed, Taunted, or Vulnerable, then remove all stacks of it from
    yourself." Per the designer: Bleeding first, then Crippled, then
    whichever of the rest he has most of. Returns the effect cleared."""
    have = [k for k in ('bleeding', 'crippled') if pc.get(k, 0) > 0]
    if not have:
        rest = [k for k in ('slowed', 'vulnerable', 'taunted', 'frightened') if pc.get(k, 0) > 0]
        have = sorted(rest, key=lambda k: -pc[k])
    if not have:
        return None
    key = have[0]
    pc[key] = 0
    pc.pop('skip_' + key, None)
    if key in ('taunted', 'frightened'):
        pc[key + '_by'] = None
    pc['cleansed'] = pc.get('cleansed', 0) + 1
    return key


def _fatestealer(pc):
    """Fatestealer (I092) at Level 1, Enith's Temper Soulblade power: a
    creature Downed by the weapon gives 1 charge (max 8); "For 1 charge,
    the wielder may Sift 2 cards. For 3 charges, the wielder may draw a
    card." She saves them for the draw: a Sift only thins low cards out
    of the deck. A drawn card joins this fight's budget. Charges last the
    day; the sim starts each fight at 0."""
    pc['fate_charges'] = min(8, pc.get('fate_charges', 0) + 1)
    if cs.T.CARDS and pc['fate_charges'] >= 3:
        pc['fate_charges'] -= 3
        pc['hand'].append(pc['deck'].draw())
        pc['budget'] += 1
        pc['fate_draws'] = pc.get('fate_draws', 0) + 1


def _try_shadow_jaunt(pc, enemies, movement_on, ap, log=None):
    """Shadow Jaunt (T097, 1 AP, Encounter): "You Teleport up to [Sorcery
    or Theurgy Skill Total] meters." A caster taken in melee (or grappled
    - Teleporting ends a grapple) Teleports clear, still in reach of what
    it was fighting, before its attacks. Returns the AP spent."""
    if pc.get('jaunt_uses_left', 0) <= 0 or not movement_on or ap < 1 + cs.T.ATTACK_AP_COST:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    near = [e for e in living if cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE]
    grappler = cs._grappled(pc)
    if not living or (not near and grappler is None):
        return 0
    if cs.effective_range(pc) <= cs.T.MELEE_RANGE and grappler is None:
        return 0  # a melee fighter is where it wants to be
    nearest = grappler or min(near, key=lambda e: cs._distance(pc['pos'], e['pos']))
    spaces = max(2, min(pc['jaunt_range'], cs.effective_range(pc) - 1))
    start = pc['pos']
    pc['pos'] = cs.movement.move_away(pc['pos'], nearest['pos'], spaces)
    if pc['pos'] == start:
        return 0
    pc['jaunt_uses_left'] -= 1
    cs._end_grapple(pc)
    if log:
        log(unit=pc['name'], action='move', pos=pc['pos'], spaces=cs._distance(start, pc['pos']), via='Shadow Jaunt')
    return 1


def _wall_cells(pc, toward, length):
    """A straight wall `length` spaces long across the line from `pc` to
    `toward`, two spaces short of it (as close as reach allows), so it
    cuts the shooters' lines to the whole party. Every space in reach."""
    (x0, y0), (x1, y1) = pc['pos'], toward
    d = max(abs(x1 - x0), abs(y1 - y0)) or 1
    reach = pc['sorcery_skill_total']
    k = max(1, min(reach, d - 2))
    cx, cy = x0 + (x1 - x0) * k / d, y0 + (y1 - y0) * k / d
    nx, ny = -(y1 - y0), (x1 - x0)
    norm = max(abs(nx), abs(ny)) or 1
    cells = set()
    for t in range(-(length // 2), length - length // 2):
        c = cs.movement.clamp((round(cx + nx * t / norm), round(cy + ny * t / norm)))
        if cs._distance(pc['pos'], c) <= reach:
            cells.add(c)
    return cells


def _try_wall_of_shadows(pc, pcs, enemies, movement_on, ap, log=None):
    """Wall of Shadows (T123, 2 AP, Encounter, lasts the scene): up to
    [Sorcery Skill Total] connected spaces, each within [Sorcery Skill
    Total] meters; "Attacks into or through the wall treat it as Heavy
    Cover." Cast across the line to the enemies' shooters when the wall
    would block more of their shots than of the party's own (the party's
    archers and casters shoot through it too). Returns the AP spent."""
    if (pc.get('wall_uses_left', 0) <= 0 or not movement_on or ap < 2 or cs._CTX.get('walls')):
        return 0
    living = [e for e in enemies if e['health'] > 0]
    allies = [p for p in pcs if p['health'] > 0]
    shooters = [e for e in living if (e.get('attack_range') or 0) > cs.T.MELEE_RANGE and e.get('kind', 'attack') != 'support']
    if not shooters:
        return 0
    cx = round(sum(e['pos'][0] for e in shooters) / len(shooters))
    cy = round(sum(e['pos'][1] for e in shooters) / len(shooters))
    cells = _wall_cells(pc, (cx, cy), pc['sorcery_skill_total'])

    def blocked(a, b):
        return tuple(b['pos']) in cells or bool(cs._cells_between(a['pos'], b['pos']) & cells)
    gain = sum(sum(blocked(e, p) for p in allies) / len(allies) for e in shooters)
    archers = [p for p in allies if cs.effective_range(p) > cs.T.MELEE_RANGE]
    loss = sum(sum(blocked(p, e) for e in living) / len(living) for p in archers)
    if gain - loss < 1:
        return 0
    pc['wall_uses_left'] -= 1
    cs._CTX['walls'] = cells
    if log:
        log(unit=pc['name'], action='technique', via='Wall of Shadows',
            effects=f"{len(cells)} spaces: {sorted(cells)}")
    return 2


def _try_spirit_blessing(pc, pcs, enemies, movement_on, ap, log=None, rnd=None, order=None):
    """Spirit Blessing (T104, Encounter). Who gets it depends on what the
    copy does:
    - defensive (Shielding, Turn Elements, Retribution): the ally (or
      himself) in reach with the most enemies on them and no Protected,
      once someone's in a fight - Hanforth's Level 2 copy (Shielding 2,
      Quickened, Reach);
    - a cleanse only (Steady, Embolden): whoever in reach carries the
      most of what it removes;
    - offensive (Guided Hand, Step of Air, River's Might, Touch of Chaos,
      Elemental Enhancement, Steal Fate, Alacrity): the hardest hitter in
      reach who hasn't acted yet this round, as early as it can go.
    Returns the AP spent. A sheet with copies built differently tries
    each in turn and casts the first that has a target."""
    for b in pc.get('blessings') or ([pc['blessing']] if pc.get('blessing') else []):
        spent = _cast_blessing(pc, b, pcs, enemies, movement_on, ap, log, rnd, order)
        if spent:
            return spent
    return 0


def _cast_blessing(pc, b, pcs, enemies, movement_on, ap, log, rnd, order):
    if b['uses'] <= 0 or ap < b['ap']:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    if not living:
        return 0
    reach = [p for p in pcs if p['health'] > 0
             and (not movement_on or cs._distance(pc['pos'], p['pos']) <= b['range'])]

    def pressed(p):
        return sum(1 for e in living if cs._distance(e['pos'], p['pos']) <= cs.T.MELEE_RANGE) if movement_on else 1

    def cleansable(p):
        return ((p.get('slowed', 0) + p.get('crippled', 0) if b['steady'] else 0)
                + (p.get('taunted', 0) + p.get('frightened', 0) if b['embolden'] else 0))
    if b['protected'] or b['ward'] or b['retribution']:
        pool = [p for p in reach if p.get('protected', 0) == 0 and pressed(p) > 0]
        chosen = sorted(pool, key=lambda p: (-pressed(p), p['health'] / p['max_health']))[:b['targets']]
    elif b['steady'] or b['embolden']:
        pool = [p for p in reach if cleansable(p) > 0]
        chosen = sorted(pool, key=lambda p: -cleansable(p))[:b['targets']]
    else:
        pool = [p for p in reach if p.get('acted_round') != rnd or p is pc]
        chosen = sorted(pool, key=lambda p: (-p['damage'], p is pc))[:b['targets']]
    if not chosen:
        return 0
    b['uses'] -= 1
    for p in chosen:
        notes = []
        if b['protected']:
            cs._gain(p, 'protected', b['protected'])
            notes.append(f"Protected +{b['protected']}")
        if b['hasted']:
            cs._gain(p, 'hasted', b['hasted'])
            notes.append(f"Hasted +{b['hasted']}")
        if b['guided']:
            p['gl_next'] = p.get('gl_next', 0) + b['guided']
            notes.append(f"Guided +{b['guided']}")
        if b['ward']:
            p['ward_type'] = b['element']
            cs._gain(p, 'ward', b['ward'])
            notes.append(f"{b['element']} Ward +{b['ward']}")
        for flag, pair in (('steady', ('slowed', 'crippled')), ('embolden', ('taunted', 'frightened'))):
            if b[flag]:
                key = max(pair, key=lambda k: p.get(k, 0))
                if p.get(key, 0) > 0:
                    p[key] -= 1
                    if p[key] == 0 and key in ('taunted', 'frightened'):
                        p[key + '_by'] = None
                    notes.append(f"{key.capitalize()} -1")
        # Charges the fight's hooks spend (this file's Spirit Blessing hooks).
        for key, field in (('retribution', 'retribution_charges'), ('rivers', 'rivers_might'),
                           ('chaos', 'touch_chaos'), ('steal', 'steal_fate')):
            if b[key]:
                p[field] = p.get(field, 0) + b[key]
                notes.append(f"{field.replace('_', ' ')} {b[key]}")
        if b['enhance']:
            p['enhance'] = [b['element'], b['enhance']]
            notes.append(f"{b['element']} on the next {b['enhance']}")
        if b['alacrity'] and order is not None:
            cs._shift_in_order(order, p, -b['alacrity'])
            notes.append(f"Outflanks {b['alacrity']}")
        if log:
            log(unit=pc['name'], action='technique', target=p['name'], via='Spirit Blessing',
                effects=', '.join(notes))
    return b['ap']


def _try_gust_of_wind(pc, pcs, enemies, movement_on, ap, rnd, trace, log=None):
    """Gust of Wind (T107, 1 AP, Encounter): "Make a Theurgy spell attack
    against the Dodge Defense of each target [all creatures within a
    3-meter-long cone]. Each target hit is Pushed back [twice your Mind]
    + [Spades] meters." Cast to clear enemies off himself, aimed so no
    ally is in the cone, and not when an ally is fighting something in it
    (pushing that away cost the party more than it saved). Returns the AP
    spent."""
    if pc.get('gust_uses_left', 0) <= 0 or not movement_on or ap < 1:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    near = [e for e in living if cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE]
    if not near:
        return 0
    near = [e for e in near if tuple(e['pos']) != tuple(pc['pos'])]  # no direction to blow one on his square
    if not near:
        return 0
    aim = min(near, key=lambda e: e['health'])['pos']
    ax, ay = aim[0] - pc['pos'][0], aim[1] - pc['pos'][1]

    def in_cone(u):
        dx, dy = u['pos'][0] - pc['pos'][0], u['pos'][1] - pc['pos'][1]
        if (dx, dy) == (0, 0) or max(abs(dx), abs(dy)) > 3:
            return False
        return (dx * ax + dy * ay) / ((dx * dx + dy * dy) ** 0.5 * (ax * ax + ay * ay) ** 0.5) >= 0.7071 - 1e-9
    others = [p for p in pcs if p['health'] > 0 and p is not pc]
    if any(in_cone(p) for p in others):
        return 0
    targets = [e for e in living if in_cone(e)]
    # Not when it would blow away something an ally is already fighting.
    if any(cs._distance(e['pos'], p['pos']) <= cs.T.MELEE_RANGE for e in targets for p in others):
        return 0
    pc['gust_uses_left'] -= 1
    for e in targets:
        defense = e['dodge'] - e.get('harried', 0)
        mod = pc['theurgy_skill_total'] - pc.get('crippled', 0)
        value, pool = cs._pc_flip(pc, mod, defense, pc.get('good_luck', 0), cs._pc_status_bad_luck(pc, e), cs.BIG, pcs,
                               cs._hand_of_chaos(pc))
        hit = mod + value >= defense
        e['harried'] = e.get('harried', 0) + 1
        note = None
        if hit:
            n = pc['gust_push'] + cs._suit_count(pool, 'Spades')
            start = cs._push(e, pc['pos'], n)
            note = f"Pushed {cs._distance(start, e['pos'])} m (up to {n})"
            cs._log(trace, round=rnd, side='enemy', unit=e['name'], action='move', pos=e['pos'],
                 spaces=cs._distance(start, e['pos']), in_range=False, via='Pushed by Gust of Wind')
            if cs._CTX.get('ps_pcs'):
                cs._parting_shots_on(e, start, pcs, log, pushed=True)
        if log:
            log(unit=pc['name'], action='hex', target=e['name'], roll=mod + value, defense=defense, hit=hit,
                dmg=0, raw_dmg=0, resist=0, target_hp_after=e['health'], target_harried_after=e.get('harried', 0),
                via='Gust of Wind', effects=note, cards=cs._take_notes(pc), opp_def='Dodge')
        pc.pop('_notes', None)
    return 1


def _gainsay(pc, e, pcs, enemies, movement_on, log):
    """Gainsay (T122, 2 AP Interrupt, Encounter): "Cast a Sorcery Spell
    against the target" when a weapon attack is declared against you -
    one of Beornhard's War Magic uses, from his Interrupt AP. Taken
    against a melee attacker, or one whose hit could Down him; a line
    copy (Furrow) is saved for a line."""
    if pc['health'] <= 0 or pc.get('ap_bank', 0) < 2:
        return 0
    dist = cs._distance(pc['pos'], e['pos']) if movement_on else 0
    if dist > cs.T.MELEE_RANGE and e.get('attack_damage', 0) - pc.get('physres', 0) < pc['health']:
        return 0
    copies = [t for t in pc.get('tech_attacks', ()) if t['uses'] > 0 and t.get('skill') == 'Sorcery'
              and t['damage'] > 0 and dist <= (t.get('range') or cs.effective_range(pc))]
    prof = None
    if copies:
        prof = max(copies, key=lambda t: (not t.get('line'), t['damage']))
        prof['uses'] -= 1
    elif pc.get('weapon_is_spell') and pc.get('weapon_uses_left', 0) > 0 and dist <= cs.effective_range(pc):
        pc['weapon_uses_left'] -= 1
    else:
        return 0
    pc['ap_bank'] -= 2
    pc['gainsay_uses_left'] -= 1
    return cs._reaction_attack(pc, e, pcs, 'Gainsay' + (f" ({prof['via']})" if prof else ''),
                            dict(prof, spell=True) if prof else None, log)


# ---- Hooks (hooks.py). ORDER numbers set the sequence within a point ----

@hooks.on('pc_turn_start', 'Shadow Jaunt', order=10)
def _jaunt_hook(pc, c):
    return _try_shadow_jaunt(pc, c.enemies, c.movement_on, c.ap, log=c.log)


@hooks.on('pc_turn_start', 'Challenge', order=20)
def _challenge_hook(pc, c):
    return _try_challenge(pc, c.pcs, c.enemies, c.movement_on, log=c.log)


@hooks.on('pc_turn_start', 'Exert Pressure', order=30)
def _pressure_start_hook(pc, c):
    return _try_exert_pressure(pc, c.pcs, c.enemies, c.movement_on, c.ap, log=c.log)


@hooks.on('pc_turn_start', 'Brace', order=40)
def _brace_start_hook(pc, c):
    return _try_brace(pc, c.enemies, c.movement_on, c.ap, True, log=c.log)


@hooks.on('pc_turn_start', 'Spirit Blessing', order=50)
def _blessing_hook(pc, c):
    return _try_spirit_blessing(pc, c.pcs, c.enemies, c.movement_on, c.ap, log=c.log, rnd=c.rnd, order=c.order)


@hooks.on('pc_turn_start', 'Gust of Wind', order=60)
def _gust_hook(pc, c):
    return _try_gust_of_wind(pc, c.pcs, c.enemies, c.movement_on, c.ap, c.rnd, c.trace, log=c.log)


@hooks.on('pc_turn_start', 'Wall of Shadows', order=70)
def _wall_hook(pc, c):
    return _try_wall_of_shadows(pc, c.pcs, c.enemies, c.movement_on, c.ap, log=c.log)


@hooks.on('pc_turn_start', order=80)
def _hexes_hook(pc, c):
    # Every hex a sheet carries (War Magic with Tormenting Curse, Reckoning).
    return _try_hexes(pc, c.pcs, c.enemies, c.rnd, c.movement_on, c.trace, c.log, c.ap) if pc.get('hexes') else 0


@hooks.on('pc_turn_end', 'Exert Pressure', order=10)
def _pressure_end_hook(pc, c):
    return _try_exert_pressure(pc, c.pcs, c.enemies, c.movement_on, c.ap, log=c.log)


@hooks.on('pc_turn_end', 'Brace', order=20)
def _brace_end_hook(pc, c):
    return _try_brace(pc, c.enemies, c.movement_on, c.ap, False, log=c.log)


@hooks.on('pc_after_turn', 'Seize the Moment')
def _seize_the_moment(pc, c):
    # T192: "At the end of each of your turns, you may Outflank once."
    cs._shift_in_order(c.order, pc, -1)


@hooks.on('before_attack', 'Eagle Eyes')
def _eagle_eyes(pc, c):
    # T137, a Style: "spend an extra 1 AP. If you do, those attacks have
    # Good Luck twice." Taken when the AP left only covers one attack.
    if not c.substitute and pc.get('attack_range') and cs.T.ATTACK_AP_COST < c.ap < 2 * cs.T.ATTACK_AP_COST:
        pc['gl_next'] = pc.get('gl_next', 0) + 2
        return 1
    return 0


@hooks.on('attack_luck', 'Ambush Predator', order=10)
def _ambush_predator(pc, c):
    # T194: Good Luck against a creature that hasn't taken its turn yet
    # this round.
    return 1 if c.target.get('acted_round') != c.rnd else 0


@hooks.on('attack_luck', 'Lie in Wait', order=20)
def _lie_in_wait_luck(pc, c):
    # T193: Good Luck once per place waited (run_fight does the waiting).
    return pc.get('liw_luck', 0) if pc.get('liw_round') == c.rnd else 0


@hooks.on('attack_luck', 'Battle Maneuver', order=30)
def _calculated(pc, c):
    # Calculated (F016): "You have Good Luck on the attack."
    return c.mv.get('calculated', 0) if c.mv else 0


@hooks.on('hit_riders', 'Furious Rage', order=10)
def _furious_rage(pc, c):
    # T130: "If one of your attacks hits or is Parried, the target gains
    # Bleeding."
    cs._gain(c.target, 'bleeding', cs.T.FURIOUS_RAGE_STACKS)


@hooks.on('hit_riders', 'Battle Maneuver', order=20)
def _maneuver_riders(pc, c):
    """A Battle Maneuver copy's riders, each + its suit: Battering (F005,
    hit or Parried, Bleeding X), Wing Clip (F006, hit, Crippled X),
    Hamstring (F008, hit, Slowed X), Harrying (F007, hit or Parried,
    Harried 1 + X), Distracting (F004, hit or Parried, Taunt X)."""
    mv, target, pool = c.mv, c.target, c.pool
    if not mv:
        return
    either = c.hit or c.parried
    if mv.get('battering') and either:
        n = mv['battering'] + cs._suit_count(pool, 'Clubs')
        cs._gain(target, 'bleeding', n)
        c.notes.append(f"Bleeding +{n} (Battering)")
    if mv.get('wing_clip') and c.hit:
        n = mv['wing_clip'] + cs._suit_count(pool, 'Clubs')
        cs._gain(target, 'crippled', n)
        c.notes.append(f"Crippled +{n}")
    if mv.get('hamstring') and c.hit:
        n = mv['hamstring'] + cs._suit_count(pool, 'Spades')
        cs._gain(target, 'slowed', n)
        c.notes.append(f"Slowed +{n}")
    if mv.get('harrying') and either:
        n = 1 + mv['harrying'] + cs._suit_count(pool, 'Diamonds')
        target['harried'] = target.get('harried', 0) + n
        c.notes.append(f"Harried +{n}")
    if mv.get('distracting') and either:
        n = mv['distracting'] + cs._suit_count(pool, 'Hearts')
        cs._test_rider(pc, target, 'taunt', n)
        c.notes.append(f"Taunted +{n}")


@hooks.on('hit_riders', "Lawman's Hand", order=30)
def _lawmans_hand(pc, c):
    # T128: "Once per round, when one of your damaging attacks hits, you
    # may Slow the target once."
    if c.hit and pc['damage'] > 0 and pc.get('lh_round') != c.rnd:
        cs._gain(c.target, 'slowed', 1)
        pc['lh_round'] = c.rnd


@hooks.on('after_hit', 'Battle Maneuver', order=10)
def _half_guard(pc, c):
    # Half Guard (F011): "If the attack hits, you gain X + [Spades] stacks
    # of Protected."
    # A Repeat (Flurry) applies "any effects on you" only once.
    if c.mv and c.mv['guard'] and not getattr(c, 'repeat', False):
        cs._gain(pc, 'protected', c.mv['guard'] + cs._suit_count(c.pool, 'Spades'))


@hooks.on('after_hit', 'Boughs Unbroken', order=20)
def _boughs_hook(pc, c):
    if pc.get('weapon_name') == 'Unarmed' and (not c.substitute or c.substitute.get('weapon')):
        _boughs_cleanse(pc)


@hooks.on('after_hit', 'Fatestealer', order=30)
def _fatestealer_hook(pc, c):
    if not c.substitute and c.target['health'] <= 0:
        _fatestealer(pc)


@hooks.on('after_hit', 'Battle Maneuver', order=40)
def _victorious(pc, c):
    # Victorious (F013): "If the attack Downs the target, draw a card."
    if c.mv and c.mv.get('victorious') and c.target['health'] <= 0:
        cs._draw_card(pc)


@hooks.on('after_hit', 'Command the Tempo', order=50)
def _command_the_tempo(pc, c):
    # T197: the target is Staggered, and "an ally of your choice Outflanks
    # once": the ally furthest back in the order gains most.
    if c.order is None:
        return
    cs._shift_in_order(c.order, c.target, 1)
    allies = [u for sd, u in c.order if sd == 'party' and u is not pc and u['health'] > 0]
    if allies:
        cs._shift_in_order(c.order, allies[-1], -1)


@hooks.on('after_attack', 'Strength from the Slain')
def _slain_hook(pc, c):
    # Eaten right after a kill, while the body's adjacent and there's an AP.
    t = c.target
    if (t['health'] <= 0 and pc.get('slain_uses_left', 0) > 0 and c.ap >= 1
            and (not c.movement_on or cs._distance(pc['pos'], t['pos']) <= cs.T.MELEE_RANGE)):
        _strength_from_slain(pc, t, c.log)
        return 1
    return 0


@hooks.on('pc_parried', 'Inexhaustible Guardian')
def _inexhaustible_guardian(pc, c):
    # T139: "Once per round, when you Parry an attack, you may gain
    # Protected."
    if pc.get('ig_round') != c.rnd:
        cs._gain(pc, 'protected', 1)
        pc['ig_round'] = c.rnd


@hooks.on('fight_start_order', 'One Eye Behind You')
def _one_eye(pc, c):
    """One Eye Behind You (T011): "At any time, you may discard a card to
    adjust your position in turn order by up to [half your Insight Skill
    Total] places." Taken once, as the fight starts, to get ahead of an
    enemy - the order holds from there. (Its Good Luck on Reflex is in
    combat_sim._roll_initiative.)"""
    order = c.order
    if not cs.T.CARDS or not cs.cards.can_spend(pc):
        return
    idx = next(i for i, (s, u) in enumerate(order) if u is pc)
    places = pc['reflex'] // 2
    ahead = [i for i in range(max(0, idx - places), idx) if order[i][0] == 'enemy']
    if not ahead:
        return
    cs.cards.spend(pc, cs.cards.lowest(pc['hand']))
    cs._shift_in_order(order, pc, -(idx - ahead[0]))
    pc['one_eye_moves'] = pc.get('one_eye_moves', 0) + idx - ahead[0]


@hooks.on('attack_declared', 'Gainsay')
def _gainsay_hook(pc, c):
    if c.prof['action'] in cs.WEAPON_ACTIONS and pc.get('gainsay_uses_left', 0) > 0:
        return _gainsay(pc, c.attacker, c.pcs, c.enemies, c.movement_on, c.log)
    return 0


@hooks.on('ally_would_drop', 'Lifeline')
def _lifeline(caster, c):
    """Lifeline's Interrupt (1 AP from the caster's Interrupt pool), cast
    to save an ally from a hit that would Down them, by a caster who can
    take it. Range [Theurgy Skill Total] meters (plus Ley-weaving)."""
    unit, loss = c.ally, c.loss
    if caster['health'] <= loss or caster.get('lifeline_uses_left', 0) <= 0 or caster.get('ap_bank', 0) < 1:
        return 0
    if 'pos' in caster and 'pos' in unit and cs._distance(caster['pos'], unit['pos']) > caster['lifeline_range']:
        return 0
    caster['lifeline_uses_left'] -= 1
    caster['ap_bank'] -= 1
    unit['lifeline'] = caster
    cs._log(cs._CTX['trace'], round=cs._CTX['rnd'], side='party', unit=caster['name'], action='technique',
            target=unit['name'], via='Lifeline', effects='linked (Interrupt)')
    return 1


@hooks.on('enemy_left_reach', 'Parting Shot')
def _parting_shot(pc, c):
    """Parting Shot (T076): "a creature within range of a close-range
    weapon you are wielding would move or be Pushed outside your range" -
    any enemy that walks or is Pushed out of reach, not just a Kiting
    one. Resolved with the enemy back where it started. A Shadow Jaunt
    enemy's own movement is a Teleport, which doesn't trigger it."""
    e, start = c.enemy, c.start
    if 'Shadow Jaunt' in e.get('abilities', ()) and not c.pushed:
        return 0
    prof = pc.get('close_profile')
    if (prof is None or pc['health'] <= 0 or e['health'] <= 0 or pc.get('parting_shot_charge_used')
            or not pc.get('parting_shot') or pc.get('ap_bank', 0) < cs.T.PARTING_SHOT_AP_COST):
        return 0
    if cs._distance(pc['pos'], start) > cs.T.MELEE_RANGE or cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE:
        return 0
    pc['ap_bank'] -= cs.T.PARTING_SHOT_AP_COST
    pc['parting_shot_charge_used'] = True
    now, e['pos'] = e['pos'], start
    dmg = cs._reaction_attack(pc, e, c.pcs, f"{prof['via']} (Parting Shot)", prof, c.log)
    e['pos'] = now
    return dmg


# ---- Features modeled 2026-10-25: War Magic, Battle Maneuver, Spirit
# Blessing and Healing Magic beyond what the sample sheets had ----

def _resist_for(target, dmg_type):
    return cs.enemy_resist_for_pc_attack({'dmg_type': dmg_type}, target)


def damage_type_choice(pc, target, substitute, mv):
    """The damage type for this attack, when a Feature offers one, or None
    to keep it. A War Magic copy that "may change the attack's damage
    type" (Frigid to Frost; Corrupting, Necrotic, Draw Power to Shadow)
    takes whichever the target resists least; Elemental (a Maneuver
    Feature) is that type, full stop; Elemental Enhancement (Spirit
    Blessing) is taken when the target resists it less, and a charge
    goes when the attack hits."""
    if substitute:
        opts = substitute.get('dmg_types')
        if not opts:
            return None
        current = pc['dmg_type']
        return min(opts, key=lambda t: (_resist_for(target, t), t != current))
    if mv and mv.get('elemental'):
        return mv['element']
    enh = pc.get('enhance')
    if enh and enh[1] > 0 and pc.get('damage', 0) > 0 and \
            _resist_for(target, enh[0]) < _resist_for(target, pc['dmg_type']):
        pc['_enh_used'] = True
        return enh[0]
    return None


def sift_extras(pc, substitute, mv, repeating):
    """Suits a Feature Sifts into this attack's pool (glossary.md, Sift:
    "Look at the top X cards of your deck"; a high card stays, a low one
    goes): Wild Magic [three times X] and Blade of Four Fates X, once per
    action and shared with its bonus attacks and Repeat; Touch of Chaos
    one card a flip while its charges last."""
    if not cs.T.CARDS:
        return []

    def sift(n):
        return [cs.cards.suit(c) for c in pc['deck'].sift(n, lambda c: cs.cards.rank(c) >= cs.T.SIFT_KEEP_RANK)]
    if repeating:
        suits = list(pc.get('_action_sift', ()))
    else:
        n = (3 * substitute.get('wild', 0) if substitute else 0) + (mv.get('blade', 0) if mv else 0)
        suits = sift(n) if n else []
        pc['_action_sift'] = suits
    if pc.get('touch_chaos', 0) > 0:
        pc['touch_chaos'] -= 1
        suits = suits + sift(1)
    return suits


def _in_cone(origin, aim, pos, length):
    ax, ay = aim[0] - origin[0], aim[1] - origin[1]
    dx, dy = pos[0] - origin[0], pos[1] - origin[1]
    if (dx, dy) == (0, 0) or (ax, ay) == (0, 0) or max(abs(dx), abs(dy)) > length:
        return False
    return (dx * ax + dy * ay) / ((dx * dx + dy * dy) ** 0.5 * (ax * ax + ay * ay) ** 0.5) >= 0.7071 - 1e-9


def shape_targets(pc, target, enemies, sub):
    """A shaped War Magic copy's other targets: Funnel, "all creatures
    within a 2-meter-long cone" aimed at the target; Nova, "all adjacent
    creatures". Only enemies are counted - the sim assumes the caster
    aims it clear of the party, the same simplification as Furrow."""
    others = [e for e in enemies if e is not target and e['health'] > 0 and 'pos' in e]
    if sub.get('cone'):
        return [e for e in others if _in_cone(pc['pos'], target['pos'], e['pos'], sub['cone'])]
    if sub.get('nova'):
        return [e for e in others if cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE]
    return []


def _push_away_from_party(pc, e, n, ctx):
    allies = [p for p in ctx.pcs if p['health'] > 0 and 'pos' in p] or [pc]
    cx = round(sum(p['pos'][0] for p in allies) / len(allies))
    cy = round(sum(p['pos'][1] for p in allies) / len(allies))
    start = cs._push(e, (cx, cy), n)
    cs._log(ctx.trace, round=cs._CTX['rnd'], side='enemy', unit=e['name'], action='move', pos=e['pos'],
            spaces=cs._distance(start, e['pos']), in_range=False, via='Pushed')
    if cs._CTX.get('ps_pcs'):
        cs._parting_shots_on(e, start, ctx.pcs, ctx.log, pushed=True)
    return start


def kinetic_helps(target, pcs):
    """Kinetic's Push is "up to", so a player picks when to use it: off a
    ranged ally the target is standing next to, yes; away from party melee
    already on it, no (they'd only have to chase it); anything else, yes,
    since it has to walk back. Pushing every time cost Beornhard's Level 2
    party 6 Health a fight next to Hilde and Browndog (2026-10-25)."""
    near = [p for p in pcs if p['health'] > 0 and 'pos' in p
            and cs._distance(p['pos'], target['pos']) <= cs.T.MELEE_RANGE]
    return any(cs.effective_range(p) > cs.T.MELEE_RANGE for p in near) or not near


def spell_riders(pc, c, before_damage):
    """A War Magic copy's riders on one target (the main one through the
    hooks below, each extra one of a Shape through combat_sim's bonus
    attack). Before damage, on a hit: Necrotic ("before damage or other
    effects"), Frigid, Corrupting. After: Kinetic on a hit, Barraging on
    a hit or a Dodge."""
    sub, t, pool = c.substitute, c.target, c.pool
    if before_damage:
        for key, effect, suit in (('necrotic', 'necrotic', 'Diamonds'), ('frigid', 'slowed', 'Spades'),
                                  ('corrupting', 'vulnerable', 'Diamonds')):
            if sub.get(key):
                n = 2 * sub[key] + cs._suit_count(pool, suit)
                cs._gain(t, effect, n)
                c.notes.append(f"{effect.capitalize()} +{n}")
        return
    if sub.get('kinetic') and c.hit and t['health'] > 0 and 'pos' in t and kinetic_helps(t, c.pcs):
        n = 4 * sub['kinetic'] + cs._suit_count(pool, 'Spades')
        start = _push_away_from_party(pc, t, n, c)
        c.notes.append(f"Pushed {cs._distance(start, t['pos'])} m")
    if sub.get('barraging') and (c.hit or c.dodged):
        n = sub['barraging'] + cs._suit_count(pool, 'Hearts')
        t['harried'] = t.get('harried', 0) + n
        c.notes.append(f"Harried +{n}")


@hooks.on('attack_luck', order=35)
def _piercing_elements(pc, c):
    # Piercing Elements (F075): "You have Good Luck on the spell attack."
    return c.substitute.get('piercing', 0) if c.substitute else 0


@hooks.on('hit_riders', order=25)
def _war_magic_before(pc, c):
    if c.substitute and c.hit:
        spell_riders(pc, c, before_damage=True)


@hooks.on('after_hit', order=60)
def _war_magic_kinetic(pc, c):
    if c.substitute and c.substitute.get('kinetic'):
        # Barraging waits for attack_resolved, which also sees a Dodge.
        sub = dict(c.substitute, barraging=0)
        spell_riders(pc, SimpleNamespace(**dict(vars(c), substitute=sub, dodged=False)), before_damage=False)


@hooks.on('attack_resolved', order=10)
def _war_magic_after(pc, c):
    sub = c.substitute
    if not sub:
        return
    if sub.get('barraging') and (c.hit or c.dodged):
        n = sub['barraging'] + cs._suit_count(c.pool, 'Hearts')
        c.target['harried'] = c.target.get('harried', 0) + n
        c.notes.append(f"Harried +{n}")
    # Abjuring (F065): "After the spell attack is resolved, you gain X + 1
    # stacks of [attack's damage type] Ward + [Hearts] stacks."
    if sub.get('abjuring'):
        n = sub['abjuring'] + 1 + cs._suit_count(c.pool, 'Hearts')
        pc['ward_type'] = pc['dmg_type']
        cs._gain(pc, 'ward', n)
        c.notes.append(f"{pc['dmg_type']} Ward +{n}")


@hooks.on('after_hit', 'Battle Maneuver', order=15)
def _turn_elements(pc, c):
    # Turn Elements (F003): "If the attack hits, you gain X + [Hearts]
    # stacks of [chosen Element] Ward."
    if c.mv and c.mv.get('turn_elements') and not getattr(c, 'repeat', False):
        n = c.mv['turn_elements'] + cs._suit_count(c.pool, 'Hearts')
        pc['ward_type'] = c.mv['element']
        cs._gain(pc, 'ward', n)
        c.notes.append(f"{c.mv['element']} Ward +{n}")


@hooks.on('after_hit', 'Battle Maneuver', order=45)
def _backfoot_fleet_step(pc, c):
    # Backfoot (F009): "you may Stagger the target up to [twice X] +
    # [Spades] times." Fleet Step (F082): "you may Outflank up to [twice
    # X] + [Spades] times."
    if not c.mv or c.order is None:
        return
    if c.mv.get('backfoot') and c.target['health'] > 0:
        moved = cs._shift_in_order(c.order, c.target, 2 * c.mv['backfoot'] + cs._suit_count(c.pool, 'Spades'))
        c.notes.append(f"Staggered {moved}")
    if c.mv.get('fleet') and not getattr(c, 'repeat', False):
        moved = cs._shift_in_order(c.order, pc, -(2 * c.mv['fleet'] + cs._suit_count(c.pool, 'Spades')))
        c.notes.append(f"Outflanked {-moved}")


@hooks.on('attack_resolved', 'Battle Maneuver', order=20)
def _lodestone(pc, c):
    # Lodestone (F010): "If the attack hits or is Parried, you Push the
    # target (2 x [X + Spades]) meters." Straight away from the attacker.
    if c.mv and c.mv.get('lodestone') and (c.hit or c.parried) and c.target['health'] > 0 and 'pos' in c.target:
        n = 2 * (c.mv['lodestone'] + cs._suit_count(c.pool, 'Spades'))
        start = cs._push(c.target, pc['pos'], n)
        c.notes.append(f"Pushed {cs._distance(start, c.target['pos'])} m")
        if cs._CTX.get('ps_pcs'):
            cs._parting_shots_on(c.target, start, c.pcs, c.log, pushed=True)


@hooks.on('pc_hit', order=10)
def _retribution_blessing(pc, c):
    # Spirit Blessing's Retribution: "The next X times this encounter that
    # a damaging attack hits the target, the attacker gains a stack of
    # Bleeding."
    if pc.get('retribution_charges', 0) > 0 and c.attacker['health'] > 0:
        pc['retribution_charges'] -= 1
        cs._gain(c.attacker, 'bleeding', 1)
        c.applied.append("Bleeding +1 to the attacker (Retribution)")


@hooks.on('after_hit', order=70)
def _blessing_after_hit(pc, c):
    # River's Might: "For the next X damaging attacks the target hits this
    # encounter, the creature hit is Pushed back 3 meters." Elemental
    # Enhancement spends a charge on the hit that used it.
    if pc.pop('_enh_used', False) and pc.get('enhance'):
        pc['enhance'][1] -= 1
    if pc.get('rivers_might', 0) > 0 and pc['damage'] > 0:
        pc['rivers_might'] -= 1
        if c.target['health'] > 0 and 'pos' in c.target and 'pos' in pc:
            start = cs._push(c.target, pc['pos'], 3)
            c.notes.append(f"Pushed {cs._distance(start, c.target['pos'])} m (River's Might)")
            if cs._CTX.get('ps_pcs'):
                cs._parting_shots_on(c.target, start, c.pcs, c.log, pushed=True)


@hooks.on('attack_resolved', order=30)
def _blessing_resolved(pc, c):
    # Steal Fate: "For the next X weapon attacks the target makes this
    # encounter, if the attack Downs a creature the target may draw a card.
    # They may only draw 1 card per casting."
    pc.pop('_enh_used', None)  # a miss spends no Elemental Enhancement charge
    if pc.get('steal_fate', 0) > 0 and (not c.substitute or c.substitute.get('weapon')):
        pc['steal_fate'] -= 1
        if c.target['health'] <= 0:
            cs._draw_card(pc)
            pc['steal_fate'] = 0
            c.notes.append("drew a card (Steal Fate)")


@hooks.on('pc_turn_start', order=1)
def _rejuvenate(pc, c):
    # Healing Magic's Rejuvenate: "the target heals 1 Shallow Health at the
    # start of each of their turns for [Spell's healing amount] rounds."
    if pc.get('regen', 0) > 0:
        pc['regen'] -= 1
        pc['health'] = min(pc['max_health'], pc['health'] + cs.tactics.necrotic_cut(pc, 1))
    return 0
