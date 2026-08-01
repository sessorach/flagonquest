"""
FlagonQuest spreadsheet → JSON converter
Usage: python scripts/convert.py

Put exported CSVs in the same folder as this script.
The script renames display headers to code-friendly keys
and writes JSON files into the data/ folder.

PREREQ CHECK — techniques.csv can have an optional "Prereq Check" column
that lets the site verify whether a character's current build actually
meets a technique's prerequisites, instead of just displaying the
"Prereqs (Full)" text for a human to read. It's a small structured
mini-syntax, separate from "Prereqs (Full)" (which stays free text for
display) since prose like "Craft 2 (if Smithing/Carving/...)" can't be
checked by a machine at all.

  Clauses are comma-separated — ALL of them must be true (AND):
    Skill:N                    e.g. Resilience:3
    (Skill1|Skill2|...):N      an OR of skills, e.g. (Composure|Meditation):2
    AnySkill:N                 any one skill at N — for "(Any Skill) 5"
    Technique:Exact Name       the character must know that technique

  N (the threshold) is either a plain integer, or scales with the
  technique's own level: [Level], [Level]+1, [Level]-1.

  Examples, matching real "Prereqs (Full)" text:
    "Resilience 2"                              → Resilience:2
    "(Composure or Meditation) 2"               → (Composure|Meditation):2
    "Resilience 2, Composure 2"                 → Resilience:2,Composure:2
    "(Acrobatics, Archery, Brawl, or Melee)
       [Level + 1]"                             → (Acrobatics|Archery|Brawl|Melee):[Level]+1
    "Theurgy [Level] + 1"                       → Theurgy:[Level]+1
    "Animal Companion"                          → Technique:Animal Companion
    "Solemn Pact, (Resilience or Presence) 3"   → Technique:Solemn Pact,(Resilience|Presence):3

  Leave the cell blank for anything that can't be mechanically checked
  (vague text, a choice the sheet doesn't track, "None", etc.) — the
  site just won't show a check for those, same as today.

  scripts/draft_prereq_check.py will attempt to auto-fill this column
  from the existing "Prereqs (Full)" text and flag whatever it can't
  confidently convert, so you don't have to type all ~140 by hand.

FEATURE BUDGET — techniques.csv can also have an optional "Feature Budget"
column for Feature-built techniques (Battle Maneuver, Healing Magic, etc).
It replaces the site having to regex the point budget back out of the
"Points: Level 1: 3 basic; Level 2: 6 basic; ..." sentence buried in the
Effects text — that sentence can now just be prose, and this column is
the real source of truth for the Feature-builder's level picker.

  Comma-separated Level:Points entries, one per level the technique can
  be bought at. Append "/adv" to a level to mark that Advanced-tier
  Features unlock starting at that level (and every level after it —
  advanced never turns back off at a higher level).

    "1:3, 2:6, 3:9/adv, 4:12/adv"
      → Level 1: 3 points, Basic only
        Level 2: 6 points, Basic only
        Level 3: 9 points, Basic + Advanced
        Level 4: 12 points, Basic + Advanced

  A level left out of the column just won't be offered in the picker, so
  normally every level from "Level Min" to "Level Max" should appear.
  Leave the whole cell blank for a technique that doesn't use a point
  budget (including non-Feature "Buildable" techniques like Temper
  Soulblade, which only need the level picker itself, not a budget).

  scripts/draft_feature_budget.py will attempt to auto-fill this column
  from the existing Effects text, same idea as draft_prereq_check.py.

BUILDING — techniques.csv can also have an optional "Building" column:
free text, just like Effects, but specifically for "how you build this"
instructions ("When you learn this, choose features that apply... Points:
...") that would otherwise repeat near-verbatim across every Feature-built
technique's Effects text. It's shown alongside the Feature-builder on the
Techniques/Builder tabs, but — like Prereqs and Related Skills — left off
the read-only Character Sheet, which only needs to show what the
technique actually *does*, not how it was built.

  scripts/split_building_text.py will draft this column (and a trimmed
  Effects to go with it) by splitting each Feature-built technique's
  Effects text at "When you learn this...", same idea as the other
  draft scripts.
"""

import csv
import json
import os
import re

# Maps each CSV's display header → the key name the app uses.
# If you add or rename columns in the spreadsheet, update these maps.
TECHNIQUE_MAP = {
    "ID":                   "id",
    "Name":                 "name",
    "Level Min":            "level_min",
    "Level Max":            "level_max",
    "Tags":                 "tags",
    "Description (Fluff)":  "description",
    "Condition":            "condition",
    "Action":               "action",
    "Cost":                 "cost",
    "Target":               "target",
    "Effects":              "effects",
    "Building":             "building",   # how to build it — kept off the read-only sheet, see index.html
    "Special":              "special",
    "Prereqs (Full)":       "prereqs",
    "Prereq Check":         "prereq_check_raw",     # parsed below, not passed through as-is
    "Feature Budget":       "feature_budget_raw",   # parsed below, not passed through as-is
    "Relevant Skills":      "related_skills",
    "Uses Cards":           "use_cards",
    "Healing":              "healing",
    "Features":             "features",
    "Free Text":            "free_text",
}

FEATURE_MAP = {
    "ID":                   "id",
    "Technique ID":         "technique_id",
    "Technique":            "technique_name",
    "Feature Name":         "feature_name",
    "Tier":                 "tier",
    "Point Cost":           "point_cost",
    "Description":          "description",
    "Additional Prereq":    "prereq",
}

# Items — everything from Other Equipment through Masterwork Items, since
# they share the same shape (a name, level, description, and the crafting
# fields for whichever apply). Category distinguishes what kind of item a
# row is (Equipment, Pack/Gear, Tool/Kit, Food, Grenade, Potion, Poison,
# Masterwork); Slot only applies to Masterwork items.
ITEM_MAP = {
    "ID":               "id",
    "Name":             "name",
    "Category":         "category",
    "Slot":             "slot",
    "Tags":             "tags",
    "Level":            "level",
    "Description":      "description",
    "Cost":             "cost",
    "School":           "school",
    "Skill Total":      "skill_total",
    "Total Materials":  "total_materials",
    "Base Materials":   "base_materials",
    "Extra Materials":  "extra_materials",
    "Base Item":        "base_item",
}

BACKGROUND_MAP = {
    "ID":           "id",
    "Name":         "name",
    "Category":     "category",
    "Description":  "description",
}

# Basic Items' crafting recipes (Weapons, Armor, Basic Clothing, etc.) —
# what School/Skill Total/materials it takes to make each equipment
# category, as opposed to items.csv's specific named items.
CRAFTING_RECIPE_MAP = {
    "ID":               "id",
    "Name":             "name",
    "Description":      "description",
    "School":           "school",
    "Skill Total":      "skill_total",
    "Total Materials":  "total_materials",
    "Base Materials":   "base_materials",
    "Extra Materials":  "extra_materials",
}

WEAPON_CATEGORY_MAP = {
    "ID":         "id",
    "Weapon":     "name",
    "Accuracy":   "accuracy",
    "Damage":     "damage",
    "Defense":    "defense",
    "Range":      "range",
    "Skill":      "skill",
    "Might STR":  "might_str",
}

ARMOR_CATEGORY_MAP = {
    "ID":                       "id",
    "Armor":                    "name",
    "Physical Resist":          "physical_resist",
    "Dodge Penalty":            "dodge_penalty",
    "Speed Penalty":            "speed_penalty",
    "Might Skill Total Req.":   "might_str",
}

TABLES = {
    "techniques.csv":         ("../data/techniques.json",         TECHNIQUE_MAP),
    "features.csv":           ("../data/features.json",           FEATURE_MAP),
    "items.csv":              ("../data/items.json",              ITEM_MAP),
    "backgrounds.csv":        ("../data/backgrounds.json",        BACKGROUND_MAP),
    "crafting_recipes.csv":   ("../data/crafting_recipes.json",   CRAFTING_RECIPE_MAP),
    "weapon_categories.csv":  ("../data/weapon_categories.json",  WEAPON_CATEGORY_MAP),
    "armor_categories.csv":   ("../data/armor_categories.json",   ARMOR_CATEGORY_MAP),
}

# Must stay in sync with STAT_SKILLS in index.html.
KNOWN_SKILLS = {
    "Acrobatics", "Archery", "Brawl", "Melee", "Stealth",
    "Athletics", "Awareness", "Might", "Presence", "Resilience",
    "Insight", "Masquerade", "Persuasion", "Streetwise", "Survival",
    "Academics", "Composure", "Craft", "Medicine", "Mixology",
    "Meditation", "Performance", "Rapport", "Sorcery", "Theurgy",
}

def clean(val):
    """Normalize cell values: strip whitespace, convert TRUE/FALSE, integers."""
    if val is None:
        return None
    val = val.strip()
    if val == "":
        return None
    if val.upper() == "TRUE":
        return True
    if val.upper() == "FALSE":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    return val


def parse_threshold(text, errors, context):
    """A plain integer, or [Level] / [Level]+N / [Level]-N."""
    text = text.strip()
    if text.isdigit():
        return {"base": int(text)}
    m = re.fullmatch(r"\[\s*Level\s*\]\s*([+-]\s*\d+)?", text, re.IGNORECASE)
    if m:
        offset = int(m.group(1).replace(" ", "")) if m.group(1) else 0
        return {"level_offset": offset}
    errors.append(f"{context}: couldn't parse threshold {text!r}")
    return None


def parse_prereq_check(raw, technique_names, errors, context):
    """Parses one 'Prereq Check' cell into a list of clause dicts — see the
    mini-syntax documented in the file header above TECHNIQUE_MAP."""
    clauses = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue

        if part.startswith("Technique:"):
            name = part[len("Technique:"):].strip()
            if name not in technique_names:
                errors.append(f"{context}: unknown technique {name!r} in {part!r}")
                continue
            clauses.append({"type": "technique", "name": name})
            continue

        if part.startswith("AnySkill:"):
            threshold = parse_threshold(part[len("AnySkill:"):], errors, context)
            if threshold:
                clauses.append({"type": "any_skill", "threshold": threshold})
            continue

        m = re.fullmatch(r"\(([^)]+)\)\s*:\s*(.+)", part)
        if m:
            skills = [s.strip() for s in m.group(1).split("|") if s.strip()]
            threshold_text = m.group(2)
        else:
            m2 = re.fullmatch(r"([A-Za-z]+)\s*:\s*(.+)", part)
            if not m2:
                errors.append(f"{context}: couldn't parse clause {part!r}")
                continue
            skills = [m2.group(1).strip()]
            threshold_text = m2.group(2)

        bad_skills = [s for s in skills if s not in KNOWN_SKILLS]
        if bad_skills:
            errors.append(f"{context}: unknown skill(s) {bad_skills} in {part!r}")
            continue

        threshold = parse_threshold(threshold_text, errors, context)
        if threshold:
            clauses.append({"type": "skill", "options": skills, "threshold": threshold})

    return clauses


def parse_feature_budget(raw, level_min, level_max, errors, context):
    """Parses one 'Feature Budget' cell into { level: {points, advanced} } —
    see the mini-syntax documented in the file header above TECHNIQUE_MAP."""
    budget = {}
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)\s*:\s*(\d+)\s*(/\s*adv)?", part, re.IGNORECASE)
        if not m:
            errors.append(f"{context}: couldn't parse entry {part!r}")
            continue
        level = int(m.group(1))
        budget[level] = {"points": int(m.group(2)), "advanced": bool(m.group(3))}

    if level_min is not None and level_max is not None:
        missing = [lv for lv in range(level_min, level_max + 1) if lv not in budget]
        if missing:
            errors.append(f"{context}: no budget for level(s) {missing} — those levels won't be pickable")

    advanced_seen = False
    for level in sorted(budget):
        if budget[level]["advanced"]:
            advanced_seen = True
        elif advanced_seen:
            errors.append(f"{context}: level {level} isn't marked /adv but an earlier level was — advanced should stay unlocked once it appears")

    return budget


script_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(script_dir, "../data"), exist_ok=True)

for csv_file, (json_file, col_map) in TABLES.items():
    csv_path  = os.path.join(script_dir, csv_file)
    json_path = os.path.join(script_dir, json_file)

    if not os.path.exists(csv_path):
        print(f"⚠ Not found, skipping: {csv_file}")
        continue

    rows = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Rename display headers to code-friendly keys,
            # skip any columns we don't have a mapping for
            renamed = {}
            for display_key, val in row.items():
                code_key = col_map.get(display_key)
                if code_key:
                    renamed[code_key] = clean(val)
            rows.append(renamed)

    if csv_file == "techniques.csv":
        technique_names = {r["name"] for r in rows if r.get("name")}
        errors = []
        budget_errors = []
        for r in rows:
            raw = r.pop("prereq_check_raw", None)
            context = f"{r.get('id')} {r.get('name')!r}"
            if raw:
                clauses = parse_prereq_check(raw, technique_names, errors, context)
                r["prereq_check"] = clauses if clauses else None
            else:
                r["prereq_check"] = None

            budget_raw = r.pop("feature_budget_raw", None)
            if budget_raw:
                budget = parse_feature_budget(budget_raw, r.get("level_min"), r.get("level_max"), budget_errors, context)
                r["feature_budget"] = budget if budget else None
            else:
                r["feature_budget"] = None
        if errors:
            print(f"\n⚠ {len(errors)} Prereq Check issue(s) in {csv_file} — these techniques won't get a checkable prereq:")
            for e in errors:
                print(f"   {e}")
            print()
        if budget_errors:
            print(f"\n⚠ {len(budget_errors)} Feature Budget issue(s) in {csv_file}:")
            for e in budget_errors:
                print(f"   {e}")
            print()

        # The site's rename field only shows up for Feature-built techniques
        # (see needsLevelPicker/features.length in index.html) — a technique
        # with Features data but no "Buildable" tag would look like it's
        # missing that field's reason for existing. Every features=True
        # technique should carry the "Buildable" tag.
        untagged = [r for r in rows if r.get("features") and "Buildable" not in [t.strip() for t in (r.get("tags") or "").split(",")]]
        if untagged:
            print(f"\n⚠ {len(untagged)} technique(s) have Features but aren't tagged \"Buildable\" in {csv_file}:")
            for r in untagged:
                print(f"   {r.get('id')} {r.get('name')!r}")
            print()

    if csv_file == "features.csv":
        technique_ids = set()
        # Populated below once techniques.csv has been read in this same
        # run; if features.csv is processed first this stays empty and the
        # check is skipped rather than false-flagging everything.
        tech_csv_path = os.path.join(script_dir, "techniques.csv")
        if os.path.exists(tech_csv_path):
            with open(tech_csv_path, newline="", encoding="utf-8-sig") as tf:
                technique_ids = {row.get("ID", "").strip() for row in csv.DictReader(tf)}

        feature_errors = []
        for r in rows:
            tier = r.get("tier")
            if tier not in ("Basic", "Advanced"):
                feature_errors.append(f"{r.get('id')}: Tier is {tier!r}, expected exactly \"Basic\" or \"Advanced\"")
            tid = r.get("technique_id")
            if technique_ids and tid not in technique_ids:
                feature_errors.append(f"{r.get('id')}: Technique ID {tid!r} doesn't match any row in techniques.csv")
        if feature_errors:
            print(f"\n⚠ {len(feature_errors)} issue(s) in {csv_file}:")
            for e in feature_errors:
                print(f"   {e}")
            print()

    if csv_file == "items.csv":
        known_categories = {"Equipment", "Pack/Gear", "Tool/Kit", "Food", "Grenade", "Potion", "Poison", "Masterwork"}
        known_slots = {"Head", "Neck", "Torso", "Hands", "Ring", "Held", "Belt", "Feet", "Other"}
        item_errors = []
        for r in rows:
            category = r.get("category")
            if category not in known_categories:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: unknown Category {category!r}")
            slot = r.get("slot")
            if slot and category != "Masterwork":
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: has a Slot but Category isn't Masterwork")
            if category == "Masterwork" and slot not in known_slots:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: unknown Slot {slot!r}")
        if item_errors:
            print(f"\n⚠ {len(item_errors)} issue(s) in {csv_file}:")
            for e in item_errors:
                print(f"   {e}")
            print()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"✓ {csv_file} → {json_file}  ({len(rows)} rows)")

print("\nDone. Commit and push the data/ folder to update the live site.")
