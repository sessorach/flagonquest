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
    "Special":              "special",
    "Prereqs (Full)":       "prereqs",
    "Prereq Check":         "prereq_check_raw",  # parsed below, not passed through as-is
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

TABLES = {
    "techniques.csv": ("../data/techniques.json", TECHNIQUE_MAP),
    "features.csv":   ("../data/features.json",   FEATURE_MAP),
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
        for r in rows:
            raw = r.pop("prereq_check_raw", None)
            if raw:
                context = f"{r.get('id')} {r.get('name')!r}"
                clauses = parse_prereq_check(raw, technique_names, errors, context)
                r["prereq_check"] = clauses if clauses else None
            else:
                r["prereq_check"] = None
        if errors:
            print(f"\n⚠ {len(errors)} Prereq Check issue(s) in {csv_file} — these techniques won't get a checkable prereq:")
            for e in errors:
                print(f"   {e}")
            print()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"✓ {csv_file} → {json_file}  ({len(rows)} rows)")

print("\nDone. Commit and push the data/ folder to update the live site.")
