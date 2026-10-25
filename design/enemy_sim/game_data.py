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
import functools
import os

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


def _read(name):
    with open(os.path.join(_SCRIPTS, name), newline="", encoding="utf-8") as f:
        return {r["ID"]: r for r in csv.DictReader(f)}


@functools.lru_cache(maxsize=None)
def techniques():
    return _read("techniques.csv")


@functools.lru_cache(maxsize=None)
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


def item_health_bonus(iid):
    row = items()[iid]
    return _int(row.get("Shallow Health")), _int(row.get("Deep Health"))
