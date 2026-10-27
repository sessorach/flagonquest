"""
The game's own data, read straight from `scripts/techniques.csv` and
`scripts/items.csv` - the same files the site compiles - so the sim
never keeps a second hand-typed copy of a fact the game already states
(Technique names, Health bonuses, item stats).

Only what the build loader (party.py) needs is exposed here: a
Technique's name and Health bonuses by ID, an item's row by ID, and the
mapping from a weapon or armor item to the sim's own tables
(`tunables.WEAPON` / `tunables.ARMOR`).
"""
import csv
import os
import re

_SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts")

# Weapon and armor items -> the sim's tunables.WEAPON / tunables.ARMOR
# keys. Items are matched by ID, not by name, so a renamed item can't
# silently stop mapping. An item missing here (a potion, a Masterwork
# piece) isn't modeled yet: party.py stops with its name rather than
# quietly dropping it - add it to NOT_MODELED_ITEMS to carry it anyway.
WEAPON_ITEMS = {
    "I117": "1H Light Melee", "I118": "1H Heavy Melee", "I119": "2H Light Melee",
    "I120": "2H Heavy Melee", "I121": "Light Thrown", "I122": "Heavy Thrown",
    "I123": "Light Bow", "I125": "Unarmed", "I126": "Shield",
}
ARMOR_ITEMS = {"I127": "Medium", "I128": "Light", "I129": "Heavy"}
# Items a sample character may carry that the sim doesn't play yet
# (TABLE_PLAY_NOTES.md: items get tested once the roster reaches about
# Level 3). Empty so far: no export carries one.
NOT_MODELED_ITEMS = set()


_FILES = {}


def cached_file(path, parse):
    """`parse(open file)` for `path`, read once and kept while the file's
    unchanged (its modification time), so a fight loop doesn't re-read
    the same CSV or build for every unit of every fight. Callers mustn't
    change what comes back: copy it first."""
    stamp = os.stat(path).st_mtime_ns
    hit = _FILES.get(path)
    if hit is None or hit[0] != stamp:
        with open(path, newline="", encoding="utf-8") as f:
            hit = _FILES[path] = (stamp, parse(f))
    return hit[1]


def csv_rows(path):
    return cached_file(path, lambda f: tuple(csv.DictReader(f)))


def _read(name):
    return cached_file(os.path.join(_SCRIPTS, name), lambda f: {r["ID"]: r for r in csv.DictReader(f)})


def techniques():
    return _read("techniques.csv")


def items():
    return _read("items.csv")


def technique_name(tid):
    row = techniques().get(tid)
    return row["Name"] if row else f"unknown Technique {tid}"


def _int(cell):
    cell = (cell or "").strip()
    return int(cell) if cell else 0


def health_bonus(tid):
    """Shallow + Deep Health a Technique adds (Toughened Body/Resolve/
    Spirit), from techniques.csv's own bonus columns - the same ones the
    Character Sheet sums."""
    row = techniques()[tid]
    return _int(row.get("Shallow Health Bonus")), _int(row.get("Deep Health Bonus"))


def _tags_by_name():
    rows = techniques()
    hit = _TAGS.get("rows")
    if hit is None or hit[0] is not rows:
        out = {}
        for r in rows.values():
            out.setdefault(r["Name"], set()).update(t.strip() for t in (r.get("Tags") or "").split(",") if t.strip())
        hit = _TAGS["rows"] = (rows, out)
    return hit[1]


_TAGS = {}


def fixed_level(tid):
    """A Technique's Level when techniques.csv gives it just one (Level
    Min = Level Max), else None (a Buildable one, whose Level is each
    copy's own)."""
    row = techniques().get(tid) or {}
    lo, hi = (row.get("Level Min") or "").strip(), (row.get("Level Max") or "").strip()
    return int(lo) if lo and lo == hi else None


def level_range(tid):
    """(Level Min, Level Max) from techniques.csv, or (None, None)."""
    row = techniques().get(tid) or {}
    lo, hi = (row.get("Level Min") or "").strip(), (row.get("Level Max") or "").strip()
    return (int(lo), int(hi or lo)) if lo else (None, None)


def tags_of(tid):
    return {t.strip() for t in (techniques().get(tid, {}).get("Tags") or "").split(",") if t.strip()}


def technique_tags(name):
    """techniques.csv's Tags for a Technique, by name (a name used by more
    than one row gets all their Tags). Empty for a name the CSV doesn't
    have, such as a test's made-up Technique."""
    return _tags_by_name().get(name, set())


def item_gold(iid):
    """An item's Cost in Gold ("4 Gold")."""
    m = re.match(r"\s*(\d+)", items()[iid].get("Cost") or "")
    return int(m.group(1)) if m else 0


def _choices(cell):
    # "Acrobatics or Melee", "Body or Cunning" -> a tuple of the options.
    return tuple(p.strip() for p in cell.split(" or ") if p.strip())


def weapon_table():
    """The weapons items.csv lists (WEAPON_ITEMS), in the shape the sim's
    tunables.WEAPON uses (2026-10-27; it was a hand-kept copy before):
    `skill` (a tuple when the item says "X or Y": the PC's better one),
    `accuracy`, `damage_base` and `damage_stat` ("N + [Stat]"; a tuple
    for "[Stat or Stat]", the higher one), the range ("19", or "Close, or
    3 × Body"; "Close" is melee) and `defense` (Weapon Defense, None for
    one that can't Parry). Weapons all deal Physical damage against
    Parry/Dodge (rulebook.md)."""
    out = {}
    for iid, name in WEAPON_ITEMS.items():
        r = items()[iid]
        skills = _choices(r.get("Relevant Skills") or "")
        dmg = (r.get("Damage") or "").strip()
        m = re.match(r"(\d+)\s*(?:\+\s*\[([^\]]+)\])?$", dmg)
        if not m or not skills:
            raise ValueError(f"items.csv {iid} {r['Name']}: can't read Damage {dmg!r} / Relevant Skills")
        stats = _choices(m.group(2)) if m.group(2) else ()
        w = dict(skill=skills if len(skills) > 1 else skills[0], accuracy=_int(r.get("Accuracy")),
                 damage_base=int(m.group(1)), damage_stat=stats if len(stats) > 1 else (stats[0] if stats else None),
                 dmg_type="Physical", opp_def="Parry/Dodge")
        rng = (r.get("Range") or "").strip()
        per_body = re.search(r"(\d+)\s*[×x]\s*Body", rng)
        if per_body:
            w["range_per_body"] = int(per_body.group(1))
        elif rng.isdigit():
            w["range"] = int(rng)
        elif rng != "Close":
            raise ValueError(f"items.csv {iid} {r['Name']}: can't read Range {rng!r}")
        wd = (r.get("Weapon Defense") or "").strip()
        w["defense"] = int(wd) if wd else None
        out[name] = w
    return out


def armor_table():
    """Worn armor from items.csv (ARMOR_ITEMS): Physical Resist, Dodge and
    Speed, with Unarmored all zeroes."""
    out = {"Unarmored": dict(dodge=0, speed=0, physres=0)}
    for iid, name in ARMOR_ITEMS.items():
        r = items()[iid]
        out[name] = dict(dodge=_int(r.get("Dodge Defense")), speed=_int(r.get("Speed")),
                         physres=_int(r.get("Physical Resist")))
    return out


def item_health_bonus(iid):
    row = items()[iid]
    return _int(row.get("Shallow Health")), _int(row.get("Deep Health"))


def features():
    """features.csv by (Technique ID, Feature name)."""
    return cached_file(os.path.join(_SCRIPTS, "features.csv"),
                       lambda f: {(r["Technique ID"], r["Feature Name"]): r for r in csv.DictReader(f)})


def feature_budget(tid):
    """techniques.csv's Feature Budget ("1:3, 2:6, 3:9/adv") as {level:
    (points, advanced allowed)}, or None for a Technique with no Features."""
    cell = (techniques()[tid].get("Feature Budget") or "").strip()
    if not cell:
        return None
    out = {}
    for part in cell.split(","):
        lvl, _, rest = part.strip().partition(":")
        pts, _, adv = rest.partition("/")
        out[int(lvl)] = (int(pts), adv.strip() == "adv")
    return out
