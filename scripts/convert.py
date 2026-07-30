"""
FlagonQuest spreadsheet → JSON converter
Usage: python scripts/convert.py

Put exported CSVs in the same folder as this script.
The script renames display headers to code-friendly keys
and writes JSON files into the data/ folder.
"""

import csv
import json
import os

# Maps each CSV's display header → the key name the app uses.
# If you add or rename columns in the spreadsheet, update these maps.
TECHNIQUE_MAP = {
    "ID":                   "id",
    "Name":                 "name",
    "Level Min":            "level_min",
    "Level Max":            "level_max",
    "Category":             "category",
    "Spell School":         "spell_school",
    "Tags":                 "tags",
    "Description (Fluff)":  "description",
    "Condition":            "condition",
    "Action":               "action",
    "Cost":                 "cost",
    "Target":               "target",
    "Effects":              "effects",
    "Special":              "special",
    "Prereqs (Full)":       "prereqs",
    "Prereq Skills":        "related_skills",
    "Uses Cards":           "use_cards",
    "Healing":              "healing",
    "Buildable":            "buildable",
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

TABLES = {
    "techniques.csv": ("../data/techniques.json", TECHNIQUE_MAP),
    "features.csv":   ("../data/features.json",   FEATURE_MAP),
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

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"✓ {csv_file} → {json_file}  ({len(rows)} rows)")

print("\nDone. Commit and push the data/ folder to update the live site.")