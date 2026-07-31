"""
Drafts a "Prereq Check" column from the existing "Prereqs (Full)" text,
so you're not typing ~140 rows by hand. One-time/occasional helper —
not part of the normal convert.py pipeline.

Usage: python scripts/draft_prereq_check.py

Reads techniques.csv, leaves any row that already has a "Prereq Check"
value alone, and writes scripts/prereq_check_draft.csv with a best-guess
value for the rest, plus a Status column: OK, NO CHECK NEEDED (blank
source, or literally "None"), or NEEDS REVIEW (couldn't confidently
convert — the original text is left in the report so you can hand-write
that one). Copy the "Prereq Check (draft)" column into your spreadsheet,
skim the NEEDS REVIEW rows, then run convert.py as usual — it'll flag
anything the draft got wrong (unknown skill/technique names, bad syntax)
so mistakes don't silently disappear.
"""

import csv
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path   = os.path.join(script_dir, "techniques.csv")
out_path   = os.path.join(script_dir, "prereq_check_draft.csv")

KNOWN_SKILLS = {
    "Acrobatics", "Archery", "Brawl", "Melee", "Stealth",
    "Athletics", "Awareness", "Might", "Presence", "Resilience",
    "Insight", "Masquerade", "Persuasion", "Streetwise", "Survival",
    "Academics", "Composure", "Craft", "Medicine", "Mixology",
    "Meditation", "Performance", "Rapport", "Sorcery", "Theurgy",
}


def split_top_level(text, sep=","):
    """Splits on `sep`, but not one that's inside parentheses — so
    "(Resilience, Composure, or Meditation) 5" stays one piece."""
    parts, current, depth = [], "", 0
    for ch in text:
        if ch == "(":
            depth += 1
            current += ch
        elif ch == ")":
            depth -= 1
            current += ch
        elif ch == sep and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += ch
    parts.append(current)
    return [p.strip() for p in parts if p.strip()]


def convert_threshold(text):
    text = text.strip()
    if text.isdigit():
        return text
    m = re.match(r"^\[\s*Level\s*\+\s*(\d+)\s*\]$", text, re.IGNORECASE)
    if m:
        return f"[Level]+{m.group(1)}"
    if re.match(r"^\[\s*Level\s*\]$", text, re.IGNORECASE):
        return "[Level]"
    m = re.match(r"^\[\s*Level\s*\]\s*\+\s*(\d+)$", text, re.IGNORECASE)
    if m:
        return f"[Level]+{m.group(1)}"
    m = re.match(r"^\[\s*Level\s*\]\s*-\s*(\d+)$", text, re.IGNORECASE)
    if m:
        return f"[Level]-{m.group(1)}"
    return None


def convert_clause(part, technique_names):
    part = part.strip()

    if part in technique_names:
        return f"Technique:{part}"

    m = re.match(r"^\(([^)]+)\)\s*(.*)$", part)
    if m:
        inner, rest = m.group(1).strip(), m.group(2).strip()
        threshold = convert_threshold(rest)
        if not threshold:
            return None
        if inner.lower() == "any skill":
            return f"AnySkill:{threshold}"
        skills = [s.strip() for s in re.split(r",|\bor\b", inner) if s.strip()]
        if skills and all(s in KNOWN_SKILLS for s in skills):
            return f"({'|'.join(skills)}):{threshold}"
        return None

    m2 = re.match(r"^([A-Za-z]+)\s+(.*)$", part)
    if m2:
        skill, rest = m2.group(1), m2.group(2).strip()
        threshold = convert_threshold(rest)
        if skill in KNOWN_SKILLS and threshold:
            return f"{skill}:{threshold}"

    return None


def draft(raw_prereq, technique_names):
    text = (raw_prereq or "").strip()
    if not text or text.lower() == "none":
        return "", "NO CHECK NEEDED"
    parts = split_top_level(text)
    converted = []
    for p in parts:
        c = convert_clause(p, technique_names)
        if c is None:
            return "", f"NEEDS REVIEW — couldn't convert {p!r}"
        converted.append(c)
    return ",".join(converted), "OK"


with open(csv_path, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

technique_names = {r["Name"].strip() for r in rows if r.get("Name", "").strip()}

out_rows = []
counts = {"OK": 0, "NO CHECK NEEDED": 0, "NEEDS REVIEW": 0, "SKIPPED (already filled in)": 0}
for r in rows:
    existing = (r.get("Prereq Check") or "").strip()
    if existing:
        out_rows.append([r["ID"], r["Name"], r.get("Prereqs (Full)", ""), existing, "SKIPPED (already filled in)"])
        counts["SKIPPED (already filled in)"] += 1
        continue
    value, status = draft(r.get("Prereqs (Full)", ""), technique_names)
    bucket = "NEEDS REVIEW" if status.startswith("NEEDS REVIEW") else status
    counts[bucket] += 1
    out_rows.append([r["ID"], r["Name"], r.get("Prereqs (Full)", ""), value, status])

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Prereqs (Full)", "Prereq Check (draft)", "Status"])
    writer.writerows(out_rows)

print(f"✓ Wrote {out_path} ({len(out_rows)} rows)")
for status, n in counts.items():
    print(f"   {status}: {n}")
print("\nCopy the \"Prereq Check (draft)\" column into your spreadsheet's new")
print("\"Prereq Check\" column, double-check the NEEDS REVIEW rows, then run")
print("convert.py — it validates every skill/technique name for real.")
