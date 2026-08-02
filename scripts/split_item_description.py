"""
Drafts a "Description (Fluff)" + "Effects" split for items.csv, same idea
as split_building_text.py for techniques.csv: items.csv currently has one
"Description" column mixing flavor text and rules text together (a doc
paragraph break usually — not always — falls between them). One-time
helper — not part of the normal convert.py pipeline.

Usage: python scripts/split_item_description.py

Reads items.csv, splits each row's Description at its first paragraph
break ("\\n", preserved from the docx), and writes
scripts/item_description_draft.csv with the split-off Fluff/Effects text
plus a Status column: OK (2+ paragraphs, first is probably fluff), or
NEEDS REVIEW (0 or 1 paragraph — could be all-fluff, all-effect, or fluff
that itself contains a rule; needs a human/hand read). Skips rows that
already have separate Description (Fluff)/Effects columns filled in.

Every row's split (OK or NEEDS REVIEW) still needs a skim — the "first
paragraph = fluff" heuristic is often but not always right (some items
skip flavor text entirely and start straight into rules). Copy "Fluff
(draft)" into Description (Fluff) and "Effects (draft)" into a new
Effects column, fixing rows by hand as needed, then run convert.py.
"""

import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path   = os.path.join(script_dir, "items.csv")
out_path   = os.path.join(script_dir, "item_description_draft.csv")

with open(csv_path, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

out_rows = []
counts = {"OK": 0, "NEEDS REVIEW": 0, "SKIPPED (already filled in)": 0, "EMPTY": 0}
for r in rows:
    existing_fluff = (r.get("Description (Fluff)") or "").strip()
    existing_effects = (r.get("Effects") or "").strip()
    if existing_fluff or existing_effects:
        out_rows.append([r["ID"], r["Name"], r.get("Description", ""), existing_fluff, existing_effects, "SKIPPED (already filled in)"])
        counts["SKIPPED (already filled in)"] += 1
        continue

    text = (r.get("Description") or "").strip()
    if not text:
        out_rows.append([r["ID"], r["Name"], "", "", "", "EMPTY"])
        counts["EMPTY"] += 1
        continue

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    if len(paragraphs) >= 2:
        fluff = paragraphs[0]
        effects = "\n".join(paragraphs[1:])
        status = "OK"
        counts["OK"] += 1
    else:
        fluff = ""
        effects = text
        status = "NEEDS REVIEW — only one paragraph, couldn't guess a fluff/effects split"
        counts["NEEDS REVIEW"] += 1
    out_rows.append([r["ID"], r["Name"], text, fluff, effects, status])

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Description (original)", "Fluff (draft)", "Effects (draft)", "Status"])
    writer.writerows(out_rows)

print(f"✓ Wrote {out_path} ({len(out_rows)} rows)")
for status, n in counts.items():
    print(f"   {status}: {n}")
print("\nSkim every row (not just NEEDS REVIEW) — copy \"Fluff (draft)\" into a new")
print("\"Description (Fluff)\" column and \"Effects (draft)\" into a new \"Effects\"")
print("column, fixing rows by hand as needed, then run convert.py.")
