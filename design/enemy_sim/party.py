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
import copy
import csv
import json
import math
import os
from types import SimpleNamespace

import tunables as T
import party_tactics
import play_styles
import encounter
import game_data
import techniques
from techniques import BuildError

_HERE = os.path.dirname(os.path.abspath(__file__))
_CSV_PATH = os.path.join(_HERE, "sample_pcs.csv")
BUILDS_DIR = os.path.join(_HERE, "builds")
STATS = ("Agility", "Body", "Cunning", "Mind", "Essence")


def _load_rows():
    return [dict(r) for r in game_data.csv_rows(_CSV_PATH)]


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
    """A build file from builds/. A variant (2026-10-25) names a `base`
    file and lists only what it changes (apply_edits), so it follows its
    base when that export is replaced. Read once and shared (2026-10-27):
    don't change what comes back; apply_edits makes a copy."""
    return _read_build(filename)[0]


_VARIANTS = {}


def _read_build(filename):
    """read_build's build, and the modification times of the file and its
    base chain (what a cached sheet depends on)."""
    path = os.path.join(BUILDS_DIR, filename)
    build = game_data.cached_file(path, json.load)
    stamps = (os.stat(path).st_mtime_ns,)
    if "base" in build:
        base, base_stamps = _read_build(build["base"])
        stamps += base_stamps
        hit = _VARIANTS.get(filename)
        if hit is None or hit[0] != stamps:
            notes = base.get("simNotes", []) + build.get("simNotes", [])
            hit = _VARIANTS[filename] = (stamps, dict(apply_edits(base, build), simNotes=notes))
        build = hit[1]
    return build, stamps


def _entry(t):
    """A Technique entry as an export writes it, from the shorthand a
    variant can use ({"id", "level", "features": {name: count}})."""
    feats = t.get("features", [])
    if isinstance(feats, dict):
        feats = [{"name": k, "count": v} for k, v in feats.items()]
    e = {"id": t["id"], "name": game_data.technique_name(t["id"]), "level": t.get("level", 1)}
    if feats or "features" in t:
        e["features"] = feats
    if t.get("note"):
        e["note"] = t["note"]
    return e


def apply_edits(build, edits):
    """A copy of `build` with `edits` applied - the format a variant file
    or make_pc(edits=...) uses:
      "replace": [{"id": "T120", "copy": 2, "level": 2, "features": {"Lance": 1, "Frigid": 2}}]
          (the 2nd copy of that ID, in the export's order; a key left out
          keeps the copy's own)
      "remove":  [{"id": "T097", "copy": 1}]
      "add":     [{"id": "T104", "level": 2, "features": {...}}]
      "stats" / "skills": {"Mind": 4}   (only the ones that change)
      "inventory": [...]                 (the whole list)
      "build": {...}                     (a whole build instead: fit()'s result)
    """
    if "build" in edits:
        return json.loads(json.dumps(edits["build"]))
    b = json.loads(json.dumps(build))
    techs = b["techniques"]

    def find(spec):
        hits = [i for i, t in enumerate(techs) if t["id"] == spec["id"]]
        n = spec.get("copy", 1)
        if n > len(hits):
            raise BuildError(f"edit names copy {n} of {spec['id']}, the build has {len(hits)}")
        return hits[n - 1]
    for spec in edits.get("replace", ()):
        i = find(spec)
        new = _entry(dict(techs[i], **{k: v for k, v in spec.items() if k != "copy"}))
        techs[i] = new
    for spec in sorted(edits.get("remove", ()), key=lambda s: -s.get("copy", 1)):
        del techs[find(spec)]
    techs.extend(_entry(t) for t in edits.get("add", ()))
    b["statPoints"].update(edits.get("stats", {}))
    b["skillPoints"].update(edits.get("skills", {}))
    if "inventory" in edits:
        b["inventory"] = edits["inventory"]
    return b


# ---- XP and prereqs, for swaps (2026-10-28) ----
# The rulebook's costs: a Skill rank costs its new rank, a Stat point twice
# its new rank, a Technique three times its Level. Prereqs are Prereq Check
# (techniques.csv; convert.py's PREREQ CHECK) against raw points.

def tech_level(t):
    return game_data.fixed_level(t["id"]) or _level(t.get("level", 1))


def xp_spent(build):
    """(Stats, Skills, Techniques) XP of a build."""
    st = sum(v * (v + 1) for v in map(int, build["statPoints"].values()))
    sk = sum(v * (v + 1) // 2 for v in map(int, build["skillPoints"].values()))
    te = sum(3 * tech_level(t) for t in build["techniques"])
    return st, sk, te


def _points(build):
    return {**{k: int(v) for k, v in build["skillPoints"].items()},
            **{k: int(v) for k, v in build["statPoints"].items()}}


def _threshold(n, level):
    n = n.strip()
    if "[Level]" in n:
        rest = n.replace("[Level]", "").strip()
        return level + (int(rest.replace(" ", "")) if rest else 0)
    return int(n)


def prereq_needs(build):
    """Every unmet Prereq Check clause in `build`: a list of (options, N,
    what) - raise any one of `options` (Skill or Stat names) to N - or
    (None, None, what) for one no rank can fix (a Technique it needs)."""
    pts, out = _points(build), []
    names = {game_data.technique_name(t["id"]) for t in build["techniques"]}
    skills = list(build["skillPoints"])
    for t in build["techniques"]:
        cell = (game_data.techniques()[t["id"]].get("Prereq Check") or "").strip()
        if not cell or cell == "None":
            continue
        level = tech_level(t)
        what = game_data.technique_name(t["id"])
        clauses = []
        for raw in cell.split(","):
            raw = raw.strip()
            if "{" in raw:
                # ChoiceField{a|b=Skill:N&Skill:N; c=...}: the branch for this copy's pick.
                body = raw[raw.index("{") + 1:raw.rindex("}")]
                for branch in body.split(";"):
                    when, _, cl = branch.partition("=")
                    if t.get("note") and t["note"] in [w.strip() for w in when.split("|")]:
                        clauses += cl.split("&")
                continue
            clauses.append(raw)
        for cl in clauses:
            cl = cl.strip()
            if not cl:
                continue
            if cl.startswith("Technique:"):
                if cl.split(":", 1)[1] not in names:
                    out.append((None, None, f"{what} needs {cl.split(':', 1)[1]}"))
                continue
            who, _, n = cl.rpartition(":")
            n = _threshold(n, level)
            opts = skills if who == "AnySkill" else who.strip("()").split("|")
            if max(pts.get(o, 0) for o in opts) < n:
                out.append((opts, n, f"{what} needs {cl}"))
    return out


def _rank_cost(kind_stat, frm, to):
    k = 2 if kind_stat else 1
    return sum(k * r for r in range(frm + 1, to + 1))


DONORS = ("Resilience", "Composure", "Insight", "Awareness", "Athletics", "Might")


def fit(build, add=(), remove=(), donors=DONORS, budget=None, cap=None, free=False):
    """A copy of `build` with Techniques added/removed and the XP total
    kept: prereq ranks the new Techniques need are bought (the cheapest
    option of an OR), then the XP over budget comes off `donors` (Skill or
    Stat names; the highest rank first, never below what a prereq needs),
    and anything left under budget goes back into donors, then into an
    untrained Skill at 1 XP, so the total lands exactly. `free` skips the
    trimming: the Techniques and their prereq ranks come on top. Returns
    (build, notes, prereq XP bought); raises BuildError when it can't (a
    Technique prereq, the rank cap, or not enough donor ranks)."""
    b = apply_edits(build, {"add": list(add), "remove": list(remove)})
    budget = budget if budget is not None else sum(xp_spent(build))
    stats = set(b["statPoints"])
    notes = []
    before = sum(xp_spent(b))
    for _ in range(30):
        need = prereq_needs(b)
        if not need:
            break
        opts, n, what = need[0]
        if opts is None:
            raise BuildError(what)
        pts = _points(b)
        o = min(opts, key=lambda x: _rank_cost(x in stats, pts.get(x, 0), n))
        if cap is not None and n > cap:
            raise BuildError(f"{what}: over the rank cap {cap}")
        (b["statPoints"] if o in stats else b["skillPoints"])[o] = n
        notes.append(f"{o} {pts.get(o, 0)}->{n} for a prereq")
    bought = sum(xp_spent(b)) - before
    if free:
        return b, notes, bought

    def spent():
        return sum(xp_spent(b))

    def floor(name):
        # The lowest a donor can go without breaking a prereq.
        lo = 1 if name in stats else 0
        for v in range((b["statPoints"] if name in stats else b["skillPoints"]).get(name, 0) - 1, lo - 1, -1):
            box = b["statPoints"] if name in stats else b["skillPoints"]
            old = box[name]
            box[name] = v
            ok = not prereq_needs(b)
            box[name] = old
            if not ok:
                return v + 1
        return lo
    trimmed = collections.Counter()
    while spent() > budget:
        cands = [d for d in donors if (b["statPoints"] if d in stats else b["skillPoints"]).get(d, 0) > floor(d)]
        if not cands:
            raise BuildError(f"not enough donor ranks to pay {spent() - budget} XP")
        d = max(cands, key=lambda x: (b["statPoints"] if x in stats else b["skillPoints"]).get(x, 0))
        box = b["statPoints"] if d in stats else b["skillPoints"]
        box[d] -= 1
        trimmed[d] += 1
    left = budget - spent()
    while left > 0:
        pts = _points(b)
        grow = [d for d in reversed(donors) if trimmed[d] > 0 and _rank_cost(d in stats, pts[d], pts[d] + 1) <= left]
        # XP freed up (a Technique taken off) goes into the donors too, the
        # lowest rank first, within the cap.
        grow = grow or sorted((d for d in donors if _rank_cost(d in stats, pts.get(d, 0), pts.get(d, 0) + 1) <= left
                               and (cap is None or pts.get(d, 0) + 1 <= cap)), key=lambda d: pts.get(d, 0))
        if grow:
            d = grow[0]
            (b["statPoints"] if d in stats else b["skillPoints"])[d] = pts.get(d, 0) + 1
            trimmed[d] -= 1
        else:
            # A Skill no fight reads, so the last XP or two changes nothing.
            fresh = [k for k in ("Craft", "Streetwise", "Masquerade", "Medicine", "Mixology", "Academics",
                                 "Persuasion", "Survival") if int(b["skillPoints"].get(k, 0)) == 0]
            if not fresh:
                break
            b["skillPoints"][fresh[0]] = 1
            notes.append(f"{fresh[0]} 0->1 to land on the XP")
        left = budget - spent()
    notes += [f"{d} {-n:+d}" for d, n in trimmed.items() if n]
    return b, notes, bought


def check_budget(name, build):
    """Every Buildable copy within its Level's Feature Budget
    (techniques.csv), Advanced Features only where the Level allows them,
    no Feature past its Max Copies, bonus points from Tormenting Curse /
    Bare-Handed counted (features.csv). A Feature features.csv doesn't
    list (a draft) isn't priced. Returns what's over, as text (an export
    made before the CSVs changed: load_sheet notes it for a rebuild)."""
    out = []
    for t in build.get("techniques", ()):
        budget = game_data.feature_budget(t["id"])
        feats = t.get("features") or []
        if budget is None or not feats:
            continue
        level = _level(t.get("level", 1))
        if level not in budget:
            out.append(f"{t.get('name', t['id'])} at Level {level} has no Feature Budget")
            continue
        points, adv_ok = budget[level]
        spent = 0
        for f in feats:
            row = game_data.features().get((t["id"], f["name"]))
            if row is None:
                continue
            n = int(f["count"])
            if row["Max Copies"].strip() and n > int(row["Max Copies"]):
                out.append(f"{f['name']} x{n} is over its Max Copies ({row['Max Copies']})")
            if row["Tier"].strip() == "Advanced" and not adv_ok:
                out.append(f"{f['name']} is Advanced, not open at Level {level}")
            spent += int(row["Point Cost"]) * n
            if row["Bonus Points"].strip():
                points += int(row["Bonus Points"])
        if spent > points:
            out.append(f"{t.get('name', t['id'])} Level {level} spends {spent} of {points} points "
                       f"({', '.join(f['name'] + ' ' + str(f['count']) for f in feats)})")
    return out


def load_sheet(row, build=None, strict=False):
    """Everything about one sample character the fight needs: the Builder
    export named in `Build` (builds/), read through techniques.py, plus
    the row's own columns for what an export doesn't say - which weapon
    the sim swings, picks the Builder keeps outside the export, how the
    character plays. Stops with a BuildError on anything it can't place:
    an unknown Technique, Feature or item, a pick that names nothing.

    The game's data always comes from the live CSVs. Where an export
    disagrees with them (made before a Level or a Feature cost changed),
    the character still plays, by the CSVs, and `sheet.rebuild` lists
    what to fix when it's next rebuilt in the Builder (SHEETS.md and
    coverage.py show them). `strict` stops instead: for a script's own
    edits, where it's a mistake in the script."""
    build = build or read_build(row["Build"])
    rebuild = check_budget(row["Name"], build)
    if strict and rebuild:
        raise BuildError(f"{row['Name']}: " + "; ".join(rebuild))
    sheet = SimpleNamespace(
        name=row["Name"],
        stats={s: int(build["statPoints"][s]) for s in STATS},
        skills={k: int(v) for k, v in build["skillPoints"].items()},
        weapon=(row.get("Weapon") or "").strip(), armor="Unarmored", parry_weapons=[],
        passives=[], card_techniques=[], encounter_techs=[], tech_attacks=[], hexes=[], maneuvers=[],
        blessing_features={}, blessing_groups=[], weapon_uses=None, weapon_level=None, defense_choices=[],
        levels={}, rebuild=rebuild,
        support=False, heal_cards=1, heal_bonus=0, heal_reach=None, heal_range=None, heal_features={},
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
        # A fixed-Level Technique's Level is techniques.csv's (an export
        # can carry an older one: Felix's Hand Rings the Bell says Lv 1, the
        # CSV 2); a Buildable copy's is its own.
        # A fixed-Level Technique's export "level" is just the CSV's label
        # when it was exported; the CSV's Level now is what counts.
        fixed = game_data.fixed_level(t["id"])
        level = fixed or _level(t.get("level", 1))
        lo, hi = game_data.level_range(t["id"])
        if fixed and _level(t.get("level", fixed)) != fixed:
            rebuild.append(f"{game_data.technique_name(t['id'])}: techniques.csv now says Level {fixed} "
                           f"(Lv {_level(t['level'])} when exported)")
        elif lo is not None and not lo <= level <= hi:
            rebuild.append(f"{game_data.technique_name(t['id'])}: built at Level {level}, techniques.csv now allows "
                           f"{lo}-{hi}")
        copies.setdefault(t["id"], []).append(
            dict(level=level, features={f["name"]: int(f["count"]) for f in t.get("features", ())}))
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
        bonus = game_data.health_bonus(tid)
        shallow += bonus[0] * len(cs)
        deep += bonus[1] * len(cs)
        # Checked first, so a Technique the sim has no entry for at all
        # can be carried unplayed too.
        if game_data.technique_name(tid) in unmodeled:
            continue
        tech = techniques.get(tid)
        if tech is None:
            continue
        tech.check_features(cs)
        tech.build(sheet, cs, choices.get(tech.name, []))
        known.add(tech.name)
        # Each copy's Level, for its Encounter uses (encounter.py).
        sheet.levels.setdefault(tech.name, []).extend(c["level"] for c in cs)
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
                distracting=feats.get("Distracting", 0),
                # 2026-10-25, the rest of the basic list and the Advanced
                # doubling ones (techniques.py's Battle Maneuver hooks):
                # Turn Elements X (Ward), Backfoot X (Stagger [twice X]),
                # Lodestone X (Push 2 x X), Blade of Four Fates X (Sift X),
                # Elemental (damage type), Viper's Sting (1 AP), Fleet Step
                # X (Outflank [twice X]), Ricochet Shot, Flurry (Repeat).
                turn_elements=feats.get("Turn Elements", 0), element=feats.get("_element"),
                backfoot=feats.get("Backfoot", 0), lodestone=feats.get("Lodestone", 0),
                blade=feats.get("Blade of Four Fates", 0), elemental=bool(feats.get("Elemental")),
                viper=bool(feats.get("Viper's Sting")), fleet=feats.get("Fleet Step", 0),
                ricochet=bool(feats.get("Ricochet Shot")), flurry=bool(feats.get("Flurry")))


def _pc_dict(sheet, index, good_luck):
    """One PC's fight dict from a loaded sheet (load_sheet)."""
    stats, skills = sheet.stats, sheet.skills
    parry = 8 + skill_total(stats, skills, "Melee")
    # rulebook.md: "you choose Acrobatics or Brawl" for Dodge - the sim
    # used Acrobatics alone until 2026-10-08, shortchanging Brawl builds
    # (Felix, Hanforth). (A Technique that needs a Skill Total itself, like
    # Blinkstep's Acrobatics or Cloak and Dagger's Stealth, reads it off
    # `skill_totals`, so Armor's Dodge penalty can't leak into it.)
    dodge = 8 + max(skill_total(stats, skills, "Acrobatics"), skill_total(stats, skills, "Brawl"))
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
        # "[Body or Cunning]" (a tuple) is whichever this PC has higher.
        ds = w["damage_stat"]
        damage_stat = max(ds, key=lambda s: int(stats[s])) if isinstance(ds, tuple) else ds
        damage_stat = damage_stat or max(("Body", "Cunning"), key=lambda s: int(stats[s]))
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
    for entry in sheet.tech_attacks:
        tname, factory, uses = entry[:3]
        meta = entry[3] if len(entry) > 3 else {}
        prof = factory(stats, skills, atk_skill_total, damage)
        tech = meta.get("tech", tname)
        prof.update(encounter.group(tech, meta.get("level") or _level_of(sheet, tech), uses, attack=True))
        prof.update(via=tname)
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
            item_cost = game_data.item_gold("I028")
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
        h.update(encounter.group(h.pop("tech"), h.pop("level"), h["uses"], attack=True))
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
    maneuvers = []
    if sheet.maneuvers:
        # Copies built the same way (and at the same Level) share one
        # entry; copies built differently (Hilde, Browndog) are used in the
        # sheet's order, combat_sim moving to the next once one's spent.
        groups = [(_maneuver_features(f), level) for f, level in sheet.maneuvers]
        if all(g == groups[0] for g in groups):
            maneuvers = [dict(_maneuver_features(sheet.maneuvers[0][0]),
                              **encounter.group("Battle Maneuver", groups[0][1], len(groups), attack=True))]
        else:
            maneuvers = [dict(g, **encounter.group("Battle Maneuver", level, 1, attack=True)) for g, level in groups]

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
              # The attack's Skill (for its suit) and the day's hand size,
              # for real cards (cards.start_fight).
              attack_skill=w_skill, hand_size=hand_size, weapon_is_spell=weapon.startswith("War Magic"))
    if attack_range is not None:
        pc["attack_range"] = attack_range
    if "Bottomless Bottles" in card_techniques:
        pc["bottles_cards"] = hand_size * 2 // 3  # discarded crafting before the day's first fight
    if hexes:
        pc["hexes"] = hexes
    if maneuvers:
        pc["maneuvers"] = maneuvers
        pc["maneuver"] = maneuvers[0]
    # What each Technique needs on the fight dict (its uses, a range, a
    # profile) is set by its own entry in techniques.py. Run for every
    # name the PC carries, a test's added passive included. `techs` is the
    # Card and Encounter Techniques by name, which hooks.py checks
    # alongside `passives`.
    # Every Skill Total, the Stats and Ley-weaving's reach, so a
    # Technique's hooks can read whichever they need without a setup of
    # their own copying it over.
    pc["skill_totals"] = {k: skill_total(stats, skills, k) for k in T.PC_SKILL_STAT}
    # The Weapon's own attack, for anything that swings it off the normal
    # attack loop (Parting Shot, Follow Through after a Technique strike).
    pc["base_profile"] = dict(skill_total=atk_skill_total, damage=damage, dmg_type=dmg_type, opp_def=opp_def,
                              skill=w_skill, via=weapon_name)
    pc["stats"] = {k: int(v) for k, v in stats.items()}
    pc["ley"] = ley
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
    # A party tactic (party_tactics.py) hands out styles by role instead.
    if T.PARTY_TACTIC:
        pc["play_style"] = party_tactics.style_for(
            party_tactics.role(attack_range, armor, "Shield" in parry_weapons, strategy == "support_healer"),
            pc["play_style"])
    if weapon_uses_left is not None:
        # The War Magic Weapon's casts are Encounter uses too; Warmage's
        # Reserves' up-front uses (cards off) sit on top of the copies.
        pc["weapon_spell"] = encounter.group("War Magic", sheet.weapon_level or 1, sheet.weapon_uses, attack=True,
                                             via=weapon_name, damage=damage)
        pc["weapon_spell"]["uses"] = weapon_uses_left
    if sheet.heal_features:
        pc["heal_features"] = dict(sheet.heal_features)
    if tech_attacks:
        pc["tech_attacks"] = tech_attacks
    if defense_choices:
        pc["opp_def_choices"] = defense_choices
    if bottled_fire_profile is not None:
        pc["bottled_fire_profile"] = bottled_fire_profile
        pc["bottled_fire_uses_left"] = bottled_fire_uses
    _attach_encounter(pc, sheet, encounter_techs)
    return pc


def _level_of(sheet, tech):
    return max(sheet.levels.get(tech) or [1])


def _attach_encounter(pc, sheet, encounter_techs):
    """Every Encounter use this PC has, as encounter.py groups: the
    profiles that carry their own uses, then one plain group for each
    other Encounter Technique (one use a copy; a test that adds one by
    name gets one use)."""
    for b in pc.get("blessings", ()):
        b.update(encounter.group("Spirit Blessing", b.pop("level"), b["uses"]))
    groups = ([pc["weapon_spell"]] if "weapon_spell" in pc else []) + pc.get("tech_attacks", []) \
        + pc.get("hexes", []) + pc.get("maneuvers", []) + pc.get("blessings", [])
    counts = collections.Counter(encounter_techs)
    for name in pc["passives"]:
        if name in techniques.ENCOUNTER_NAMES and name not in counts:
            counts[name] = 1
    owned = {g["tech"] for g in groups}
    groups += [encounter.group(name, _level_of(sheet, name), n) for name, n in counts.items() if name not in owned]
    encounter.attach(pc, groups)


def _rows():
    return {r["Name"]: r for r in _load_rows()}


def make_pc(name, index=1, good_luck=0, health=0, add_passives=(), drop_passives=(), battle_tactic=None,
            rows=None, edits=None, row_changes=None):
    """One sample character's fight dict, optionally changed for a test:
    `health` more max Health, test passives added (effect_check's
    "Test:..." ones, a Style being priced) or dropped, a different Battle
    Tactic. `edits` changes the build itself for one run (apply_edits'
    format: swap a Feature, a Technique, a Stat) and `row_changes` the
    row's own columns (a Choices pick, the Weapon). The one way scripts
    should build a modified character, so none of them depend on the
    CSV's columns."""
    row = (rows or _rows())[name]
    if row_changes:
        row = dict(row, **row_changes)
    sheet = copy.copy(_cached_sheet(row, edits))
    sheet.health += health
    sheet.passives = [p for p in sheet.passives if p not in drop_passives] + list(add_passives)
    if battle_tactic:
        sheet.battle_tactic = battle_tactic
    return _pc_dict(sheet, index, good_luck)


_SHEETS = {}


def _cached_sheet(row, edits):
    # load_sheet is the same for the same row, build files and edits, and
    # was a fifth of a fight's run time when redone every fight
    # (2026-10-27). make_pc copies the sheet before changing it.
    _, stamps = _read_build(row["Build"])
    # The game's CSVs are part of the key too (each read is replaced when
    # its file changes), so a cached sheet never outlives the data.
    data = (id(game_data.techniques()), id(game_data.items()), id(game_data.features()))
    key = (tuple(sorted(row.items())), stamps, data, json.dumps(edits, sort_keys=True) if edits else None)
    sheet = _SHEETS.get(key)
    if sheet is None:
        build = apply_edits(read_build(row["Build"]), edits) if edits else None
        sheet = _SHEETS[key] = load_sheet(row, build, strict=bool(edits))
    return sheet


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
        # The fight dict still calls Vital Defense `bodily`, its old name.
        print(p["name"], "| Parry", p["parry"], "| Dodge", p["dodge"], "| Vital", p["bodily"],
              "| Mental", p["mental"], "| Vigilant", p["vigilant"],
              "| Damage", p["damage"], "| PhysRes", p["physres"], "| Health", p["health"])


def rebuild_list(rows=None):
    """{row Name: [what to fix]} for every sample character whose export
    disagrees with the live CSVs (load_sheet's `rebuild`)."""
    out = {}
    for name, row in (rows or _rows()).items():
        notes = _cached_sheet(row, None).rebuild
        if notes:
            out[name] = list(dict.fromkeys(notes))
    return out
