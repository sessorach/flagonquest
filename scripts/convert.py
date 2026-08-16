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

BASE ITEM OPTIONS — items.csv can have an optional "Base Item Options"
column, for Masterwork items only: a comma-separated list of item IDs
that a Masterwork power can be built onto (e.g. a Torso enchantment that
works on either Light or Heavy Armor). The site shows a base-item picker
on the Character Sheet for any Masterwork item that has this filled in,
and adds the chosen base item's own flat stat bonuses on top of the
Masterwork item's own when it's equipped.

  Leave the cell blank when a Masterwork item's only valid base (per the
  rulebook's per-slot default, e.g. "basic clothing or basic jewelry")
  doesn't carry any stats of its own — there's nothing useful to pick
  between, so no selector is needed.

MARKDOWN SOURCES — the Rulebook and Glossary tabs aren't spreadsheets,
they're just hand-edited Markdown: scripts/rulebook.md and
scripts/glossary.md, straight text files you can open and edit in
anything. This script parses them into data/rulebook.json and
data/glossary-page.json (the two tab pages) — and data/glossary.json,
the mouseover-tooltip term list used site-wide, is generated from
glossary.md too, so there's exactly one place to add or correct a term
rather than two that can drift out of sync.

  # / ## / ### / #### — heading levels 1-4. Level 1 is a chapter (big
  gold heading, own line in the sidebar Contents); level 2 a section
  (also in Contents); level 3 a subsection (in the page, not the
  Contents list); level 4 a compact "term: definition" entry (a Skill
  under its Stat, a Rules Tag, a Glossary term) — several of these can
  follow each other tightly without each needing its own big heading.

  Blank lines separate paragraphs/blocks, same as a normal document.

  **bold** — inline emphasis, anywhere in a line.

  - bullet — a line starting with "- " is a list item; a run of
    consecutive "- " lines becomes one bullet list. Indent a line two
    extra spaces ("  - ") to nest it as a sub-item under the bullet
    above it — only one level of nesting is supported.

  A paragraph block starting with "Example:" renders italicized and
  indented (see renderBody in rulebook.html/glossary.html) — no special
  syntax needed, just start the block with the literal word "Example:".

  A level-1 heading may end with "{Supplement Name}" (e.g. "# Goblin
  Game {Goblin Game}") to tag that chapter — and every section nested
  under it, down through level 4, until the next level-1 heading — as
  belonging to that supplement. The brace tag is stripped from the
  displayed title. A level-1 heading with no tag (i.e. everything
  today) defaults to "Base Game", same as an untagged items.csv/
  techniques.csv/backgrounds.csv row. The Rulebook/Glossary pages use
  this to offer a per-supplement view — see the supplement tabs in
  rulebook.html/glossary.html.

  Glossary.md's own heading text can include the bracket/tag styling
  used elsewhere ("[Encounter]", "Bleeding [Fleeting]", "Sift (X
  cards)") — the mouseover list strips that down to the actual word
  that'll appear (capitalized) in real item/technique text, e.g.
  "[Encounter]" becomes the term "Encounter". A heading that isn't a
  literal word on its own, like "(Level X)", is skipped for the
  mouseover list (but still renders fine as a heading on the page).

  There's no draft-and-review script for these the way items/techniques
  have — Markdown is already meant to be hand-edited directly.
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
    # A permanent increase to the character's *maximum* Health while
    # this technique is known (Toughened Body/Resolve/Spirit) — not a
    # one-time heal like "Healing" above marks. Learning a Duplicate-
    # tagged one more than once counts each copy — see
    # techniqueHealthBonuses in index.html.
    "Shallow Health Bonus": "shallow_health_bonus",
    "Deep Health Bonus":    "deep_health_bonus",
    # Which book this is from — see the matching note on ITEM_MAP's
    # Supplement column. Gates what's offered in the Techniques browse
    # list via the Sources panel, same as items/backgrounds.
    "Supplement":           "supplement",
    # Comma-separated supplement name(s) that, when enabled, hide this
    # specific technique from the browse list even though its own
    # Supplement is otherwise on — for a technique a supplement
    # replaces outright rather than just adding alongside. E.g. Goblin
    # Game's food rules make the standard Street Runner/Pranic
    # Nourishment/Land's Bounty not make sense, so those rows are tagged
    # "Excluded By: Goblin Game" while a separate Goblin Game-supplement
    # Street Runner row (its own Supplement, no Excluded By) takes its
    # place. A technique already in a build is unaffected either way —
    # same non-retroactive rule as Supplement itself.
    "Excluded By":          "excluded_by",
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
    # Flavor text and rules text, split the same way techniques.csv splits
    # Description/Effects — Description (Fluff) is italicized and skipped
    # on the read-only Character Sheet; Effects is the actual rules text,
    # always shown. Not every item has fluff (some data-file entries are
    # purely mechanical), but every item that does anything has Effects.
    "Description (Fluff)": "description",
    "Effects":              "effects",
    "Cost":             "cost",
    # Masterwork items are priced per level (20 Gold/level) rather than a
    # flat Cost — set for a Masterwork item with more than one valid
    # build level, where Cost is left blank since it depends on which
    # level you build it at. The site multiplies this by the level
    # you've picked (see index.html). Fixed-level Masterwork items just
    # get a flat Cost like any other item, and leave this blank. Every
    # catalog Material also uses this (always 1) rather than a flat Cost,
    # since a material is baseline worth its Level in Gold by rule — see
    # the "Crafting materials framework" changelog entry for why that
    # rule matters (Alchemy/Masterwork's Total Materials formula ties to
    # an item's Gold cost).
    "Value Per Level":  "value_per_level",
    "School":           "school",
    "Skill Total":      "skill_total",
    "Total Materials":  "total_materials",
    "Base Materials":   "base_materials",
    "Extra Materials":  "extra_materials",
    "Base Item Options": "base_item_options_raw",  # parsed below into a list of item IDs
    # Flat stat bonuses an equipped/carried item grants, one column per
    # number the Character Sheet's Vitals/Defenses/Health/Resists boxes
    # track — so an item that grants one can feed it in directly instead
    # of only living as unstructured Description prose. Most Masterwork
    # items grant a unique ability rather than a flat number, or let you
    # choose among several stats, so these are blank far more often than
    # not — that's expected, not a gap to fill in.
    "Physical Resist":   "physical_resist",
    "Fire Resist":        "fire_resist",
    "Frost Resist":       "frost_resist",
    "Brilliant Resist":   "brilliant_resist",
    "Shadow Resist":      "shadow_resist",
    "Speed":              "speed",
    "Parry Defense":      "parry_defense",
    "Dodge Defense":      "dodge_defense",
    "Bodily Defense":     "bodily_defense",
    "Mental Defense":     "mental_defense",
    "Instinct Defense":   "instinct_defense",
    "Shallow Health":     "shallow_health",
    "Deep Health":        "deep_health",
    # Weapon/Armor-category items (Category = "Weapon"/"Armor") — their
    # own combat stats, mirroring weapon_categories.csv/armor_categories.csv
    # (which stay as the small reference tables they were, unchanged).
    # Armor's Dodge Penalty/Speed Penalty reuse the dodge_defense/speed
    # columns above (as negative numbers) rather than getting their own —
    # a penalty is just a negative bonus to the same stat.
    "Accuracy":           "accuracy",
    "Damage":             "damage",
    "Weapon Defense":     "weapon_defense",   # only applies to Parry Defense when this weapon is chosen to parry with — see index.html
    "Range":              "range",
    "Relevant Skill":     "relevant_skill",
    "Might Requirement":  "might_requirement",
    "Held Slots":         "held_slots",       # how much of the 2-slot Held capacity this weapon takes (1 or 2)
    # Which book this item is from — "Base Game" for everything in the
    # core rules, or a supplement's own name (e.g. "Goblin Game") for
    # anything added later. Not used for any calculation yet, just
    # tracked so a future supplement filter has something to key off of.
    "Supplement":         "supplement",
    # Category = "Material" only. Comma-separated Material Types (Metal,
    # Wood, Bone, Cloth, Leather, Food, Medicinal, Precious, Brilliant,
    # Fire, Frost, Shadow — see "Material Types" in the rulebook's
    # Creating Items chapter) this material counts as for crafting recipe
    # requirements. A material can list more than one Type (e.g. a
    # special GM-granted material that's both Metal and Fire) — stays a
    # raw string, split client-side the same way Tags is (splitCSV), not
    # parsed into a list here.
    "Material Types":     "material_types",
}

BACKGROUND_MAP = {
    "ID":           "id",
    "Name":         "name",
    "Category":     "category",
    "Description":  "description",
    # Which book this is from — see the matching note on ITEM_MAP's
    # Supplement column. A Goblin clan background's Category is the
    # clan's own name (e.g. "Rockbiters") rather than "General"/
    # "Settler"/"Wildfolk" — see index.html's backgroundSlot for how
    # that keeps clan picks freely combinable instead of exclusive.
    "Supplement":   "supplement",
}

# Recipes for what it takes to craft an item — covers both the fixed,
# hand-authored set (Weapons, Armor, Basic Clothing, etc.) and generic
# fallback recipes for large open-ended categories (Masterwork, Potions,
# Poisons, Grenades, Food) that would be impractical to hand-author one
# row per item for. items.csv's specific named items still take priority
# over anything here — see the Applies To comment below.
CRAFTING_RECIPE_MAP = {
    "ID":               "id",
    "Name":             "name",
    "Description":      "description",
    # One School per row — a recipe covering more than one School (e.g.
    # a Weapon can be made via Carving or Smithing) is one row per
    # School instead of one row with a "(if School)" conditional, so
    # every field here is a flat, unconditional value. See CR001/CR002
    # for the Weapon example. Leave blank ("Varies") for a fallback
    # recipe that's genuinely different per item (e.g. Masterwork).
    "School":           "school",
    "Skill Total":      "skill_total",
    # Kind picks which of the two material-requirement shapes the rest
    # of this row uses — "Slots" (Primary/Leeway Types below) or "Value"
    # (Total/Base/Extra Materials below). Blank defaults to Slots, since
    # that's what every recipe used before Kind existed.
    "Kind":             "kind_raw",
    # Primary/Leeway ("Slots" kind) — a small fixed count of material
    # "slots" instead of a count tied to the item's price. Primary is
    # the type(s) that must fill most of the slots; Leeway is a
    # broader, more forgiving list for the rest. E.g. Weapon (Smithing):
    # 2 Primary slots needing Metal, 1 Leeway slot accepting Cloth or
    # Leather too. Used for the fixed, hand-authored set (Weapons,
    # Armor, Tools) where the small roster makes hand-authoring
    # practical.
    "Primary Types":    "primary_types",
    "Primary Count":    "primary_count",
    "Leeway Types":     "leeway_types",
    "Leeway Count":     "leeway_count",
    # Total/Base/Extra Materials ("Value" kind) — the same Gold-value
    # model items.csv's ITEM_MAP uses for a per-item override (see its
    # Total Materials/Base Materials/Extra Materials comment), just
    # expressed as a table row instead of columns on one specific item.
    # Used for large, open-ended categories (Masterwork, Potions,
    # Poisons, Grenades, Food) where a formula scales and a hand-
    # authored template per item doesn't. Total Materials can be a flat
    # number or the "[Item's base price in Gold]" token.
    "Total Materials":  "total_materials",
    "Base Materials":   "base_materials",
    "Extra Materials":  "extra_materials",
    # Which items.csv rows this recipe covers, so index.html can resolve
    # "what does it take to craft this item" without guessing from name/
    # description text. Comma-separated clauses, ALL must match (AND):
    #   Category:X       — item.category === X
    #   Name:X            — item.name === X (exact)
    #   NameContains:X    — item.name includes X (case-insensitive)
    # Blank means "reference only" (see Other Items) — too variable to
    # auto-match, not shown as a specific item's recipe in the browser.
    # Multiple rows can share the same Applies To (one per School) —
    # the browser shows each as its own way to craft the same item.
    # A specific item's own School/Skill Total/Total Materials/*
    # Materials columns (on the item itself, see ITEM_MAP) always take
    # priority over anything here — "special items require you to find
    # a specific recipe for them" per the rulebook, so a populated
    # per-item override means this generic table doesn't apply at all.
    "Applies To":       "applies_to",
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


def parse_item_levels(raw):
    """Parses an items.csv "Level" cell — "3", "1-5", "1, 2", or "3 or 4"
    — into a sorted list of the specific levels it can be built at, e.g.
    [1,2,3,4,5] or [3,4]. A single-entry result means the level is fixed
    (Masterwork items just get a "Lv N" badge); more than one means it's
    buildable at a choice of levels (Masterwork items get a level picker
    on the Character Sheet instead). Returns [] if unparseable.
    clean() already turns a plain-digit cell like "3" into an int, so a
    bare int (already a single valid level) is accepted as-is too."""
    if isinstance(raw, int):
        return [raw]
    text = raw.replace(" or ", ",")
    levels = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            levels.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            levels.add(int(part))
        else:
            return []
    return sorted(levels)


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


def slugify(title, used_ids):
    """Turns a heading's text into a URL-safe #id, deduping against ids
    already handed out (two headings with the same text, e.g. the "Okay,
    is there a quick way..." pattern, still need distinct anchors)."""
    s = re.sub(r"[^\w\s-]", "", title.lower()).strip()
    s = re.sub(r"[\s_]+", "-", s).strip("-") or "section"
    base, n = s, 2
    while s in used_ids:
        s = f"{base}-{n}"
        n += 1
    used_ids.add(s)
    return s


def parse_markdown_sections(text):
    """Parses rulebook.md/glossary.md into the same flat
    {id, level, title, body, supplement} shape the site already expects
    — see the MARKDOWN SOURCES doc below for the syntax. Consecutive
    non-blank lines form one block (blank lines separate blocks,
    matching how the site already splits a section's body on blank
    lines); the site's renderer decides at display time whether a block
    is a bullet list or a plain paragraph, based on whether its lines
    start with "- "."""
    used_ids = set()
    sections = []
    current = None
    block_lines = []
    current_supplement = "Base Game"

    def flush_block():
        if block_lines:
            block = "\n".join(block_lines).rstrip()
            if block:
                current["body_blocks"].append(block)
            block_lines.clear()

    for raw_line in text.split("\n"):
        line = raw_line.rstrip()
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_block()
            level, title = len(m.group(1)), m.group(2).strip()
            if level == 1:
                tag = re.search(r"\{([^{}]+)\}\s*$", title)
                current_supplement = tag.group(1).strip() if tag else "Base Game"
                if tag:
                    title = title[:tag.start()].rstrip()
            current = {"id": slugify(title, used_ids), "level": level, "title": title, "supplement": current_supplement, "body_blocks": []}
            sections.append(current)
        elif not line.strip():
            flush_block()
        elif current is not None:
            block_lines.append(raw_line)
    flush_block()

    for s in sections:
        s["body"] = "\n\n".join(s.pop("body_blocks"))
    return sections


# Rules Tags / Type Tags / Common Effects entries in glossary.md are
# headed things like "[Encounter]", "Bleeding [Fleeting]", "Sift (X
# cards)", or "(Fire/Frost/Brilliant/Shadow) Ward [Fleeting]" — useful as
# a heading, but not the literal word that'll actually appear (capitalized)
# in running item/technique text for the mouseover glossary to match
# against. This trims a glossary.md heading down to the term(s) it
# actually stands for; returns a list since the Ward entry stands for 4
# separate terms sharing one description.
def glossary_terms_from_heading(title):
    if title == "(Fire/Frost/Brilliant/Shadow) Ward [Fleeting]":
        return [f"{element} Ward" for element in ["Fire", "Frost", "Brilliant", "Shadow"]]
    t = title.strip()
    stripped = re.sub(r"\s*\[Fleeting\]\s*$", "", t)
    if stripped.strip():
        t = stripped
    t = re.sub(r"\s*\(.*?\)\s*$", "", t).strip()  # "Sift (X cards)" -> "Sift"
    m = re.fullmatch(r"\[(.+)\]", t)
    if m:
        t = m.group(1)
    if not t or t == "Level X":
        return []  # not a literal word that would appear in running prose
    if t == "Pushing":
        t = "Pushed"  # matches how item/technique text actually uses it
    return [t]


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
        known_categories = {"Equipment", "Pack/Gear", "Tool/Kit", "Food", "Grenade", "Potion", "Poison", "Masterwork", "Weapon", "Armor", "Material"}
        known_slots = {"Head", "Neck", "Torso", "Hands", "Ring", "Held", "Belt", "Feet", "Other"}
        slotted_categories = {"Masterwork", "Weapon", "Armor"}
        item_errors = []
        items_by_id = {r.get("id"): r for r in rows}
        for r in rows:
            category = r.get("category")
            if category not in known_categories:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: unknown Category {category!r}")
            slot = r.get("slot")
            if slot and category not in slotted_categories:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: has a Slot but Category isn't Masterwork/Weapon/Armor")
            if slot and slot not in known_slots:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: unknown Slot {slot!r}")
            if r.get("held_slots") is not None and category != "Weapon":
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: has Held Slots but Category isn't Weapon")
            if r.get("material_types") and category != "Material":
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: has Material Types but Category isn't Material")
            if category == "Material" and not r.get("material_types"):
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: Category is Material but Material Types is blank")

            raw_base_opts = r.pop("base_item_options_raw", None)
            ids = [s.strip() for s in raw_base_opts.split(",") if s.strip()] if raw_base_opts else []
            if ids and category != "Masterwork":
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: has Base Item Options but Category isn't Masterwork")
            for bid in ids:
                base = items_by_id.get(bid)
                if not base:
                    item_errors.append(f"{r.get('id')} {r.get('name')!r}: Base Item Options references unknown item {bid!r}")
                elif base.get("slot") != slot:
                    item_errors.append(f"{r.get('id')} {r.get('name')!r}: Base Item Options item {bid!r} has Slot {base.get('slot')!r}, expected {slot!r}")
            r["base_item_options"] = ids

            raw_level = r.get("level")
            r["levels"] = parse_item_levels(raw_level) if raw_level else []
            if raw_level and not r["levels"]:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: couldn't parse Level {raw_level!r}")
            out_of_range = [lv for lv in r["levels"] if lv < 1 or lv > 5]
            if out_of_range:
                item_errors.append(f"{r.get('id')} {r.get('name')!r}: Level {raw_level!r} includes level(s) {out_of_range} outside 1-5")

            value_per_level = r.get("value_per_level")
            if value_per_level is not None:
                # Masterwork items are priced per level by design choice
                # (build cost scales with power). Materials are priced per
                # level by rule — a material is baseline worth its Level in
                # Gold — which is why every catalog material's Value Per
                # Level is a flat 1 rather than something authored per item.
                if category not in ("Masterwork", "Material"):
                    item_errors.append(f"{r.get('id')} {r.get('name')!r}: has Value Per Level but Category isn't Masterwork or Material")
                elif len(r["levels"]) <= 1:
                    item_errors.append(f"{r.get('id')} {r.get('name')!r}: has Value Per Level but only one valid Level — give it a flat Cost instead")
                if r.get("cost"):
                    item_errors.append(f"{r.get('id')} {r.get('name')!r}: has both a flat Cost and a Value Per Level — pick one")
        if item_errors:
            print(f"\n⚠ {len(item_errors)} issue(s) in {csv_file}:")
            for e in item_errors:
                print(f"   {e}")
            print()

    if csv_file == "crafting_recipes.csv":
        recipe_errors = []
        slots_cols  = ("primary_types", "primary_count", "leeway_types", "leeway_count")
        value_cols  = ("total_materials", "base_materials", "extra_materials")
        for r in rows:
            kind = r.get("kind_raw") or "Slots"
            if kind not in ("Slots", "Value"):
                recipe_errors.append(f"{r.get('id')} {r.get('name')!r}: unknown Kind {kind!r}, expected \"Slots\" or \"Value\"")
            other_cols = value_cols if kind == "Slots" else slots_cols
            populated = [c for c in other_cols if r.get(c) is not None]
            if populated:
                recipe_errors.append(f"{r.get('id')} {r.get('name')!r}: Kind is {kind!r} but has {', '.join(populated)} filled in — pick one shape")
            r["kind_raw"] = kind
        if recipe_errors:
            print(f"\n⚠ {len(recipe_errors)} issue(s) in {csv_file}:")
            for e in recipe_errors:
                print(f"   {e}")
            print()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"✓ {csv_file} → {json_file}  ({len(rows)} rows)")

# ── Rulebook & Glossary — hand-edited Markdown, not spreadsheets. See
# the MARKDOWN SOURCES doc at the top of this file for the syntax.
rulebook_md_path = os.path.join(script_dir, "rulebook.md")
if os.path.exists(rulebook_md_path):
    with open(rulebook_md_path, encoding="utf-8") as f:
        rulebook_sections = parse_markdown_sections(f.read())
    with open(os.path.join(script_dir, "../data/rulebook.json"), "w", encoding="utf-8") as f:
        json.dump(rulebook_sections, f, indent=2, ensure_ascii=False)
    print(f"✓ rulebook.md → ../data/rulebook.json  ({len(rulebook_sections)} sections)")
else:
    print("⚠ Not found, skipping: rulebook.md")

glossary_md_path = os.path.join(script_dir, "glossary.md")
if os.path.exists(glossary_md_path):
    with open(glossary_md_path, encoding="utf-8") as f:
        glossary_sections = parse_markdown_sections(f.read())
    with open(os.path.join(script_dir, "../data/glossary-page.json"), "w", encoding="utf-8") as f:
        json.dump(glossary_sections, f, indent=2, ensure_ascii=False)
    print(f"✓ glossary.md → ../data/glossary-page.json  ({len(glossary_sections)} sections)")

    # The mouseover glossary (data/glossary.json) is derived from this
    # same file's level-4 term entries — one source, so the tooltip and
    # the Glossary tab's own page can never drift apart the way they did
    # when glossary.json was hand-curated separately.
    glossary_entries = []
    seen_terms = set()
    for s in glossary_sections:
        if s["level"] != 4 or not s["body"]:
            continue
        for term in glossary_terms_from_heading(s["title"]):
            if term in seen_terms:
                continue
            seen_terms.add(term)
            glossary_entries.append({"term": term, "description": s["body"]})
    with open(os.path.join(script_dir, "../data/glossary.json"), "w", encoding="utf-8") as f:
        json.dump(glossary_entries, f, indent=2, ensure_ascii=False)
    print(f"✓ glossary.md → ../data/glossary.json  ({len(glossary_entries)} mouseover terms)")
else:
    print("⚠ Not found, skipping: glossary.md")

print("\nDone. Commit and push the data/ folder to update the live site.")
