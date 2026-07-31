"""
Drafts a "Building" column (and the trimmed Effects text to go with it)
by splitting each Feature-built technique's Effects text at "When you
learn this...", so the "how to build it" instructions stop repeating
near-verbatim across every Feature-built technique's Effects text and
showing up in front of players on the Character Sheet. One-time helper —
not part of the normal convert.py pipeline.

Usage: python scripts/split_building_text.py

Reads techniques.csv, looks at every row with Features = TRUE, and skips
any that already have a "Building" value. For the rest, splits Effects at
the first "When you learn this" and writes scripts/building_text_draft.csv
with the trimmed Effects and the split-off Building text, plus a Status
column: OK, or NEEDS REVIEW (Features is TRUE but Effects doesn't contain
that phrase — split it by hand). Copy "Effects (trimmed draft)" over your
existing Effects column and "Building (draft)" into a new Building column,
skim the NEEDS REVIEW rows, then run convert.py.
"""

import csv
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path   = os.path.join(script_dir, "techniques.csv")
out_path   = os.path.join(script_dir, "building_text_draft.csv")

# Anchored on "choose features", not just "when you learn this" — War
# Magic's Effects text also says "...chosen when you learn this)" mid
# sentence for an unrelated reason, and that's not the boilerplate split
# point.
SPLIT_RE = re.compile(r"When you learn this,\s*choose features", re.IGNORECASE)


def split(effects_text):
    text = effects_text or ""
    m = SPLIT_RE.search(text)
    if not m:
        return None, None
    return text[:m.start()].strip(), text[m.start():].strip()


with open(csv_path, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

out_rows = []
counts = {"OK": 0, "NEEDS REVIEW": 0, "SKIPPED (already filled in)": 0, "NOT BUILDABLE": 0}
for r in rows:
    if (r.get("Features") or "").strip().upper() != "TRUE":
        counts["NOT BUILDABLE"] += 1
        continue
    existing = (r.get("Building") or "").strip()
    if existing:
        out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), r.get("Effects", ""), existing, "SKIPPED (already filled in)"])
        counts["SKIPPED (already filled in)"] += 1
        continue
    effects, building = split(r.get("Effects", ""))
    if effects is None:
        out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), "", "", "NEEDS REVIEW — no \"When you learn this, choose features\" found in Effects"])
        counts["NEEDS REVIEW"] += 1
        continue
    status = "OK" if effects else "OK — Effects is now empty, nothing left to show but the picker"
    out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), effects, building, status])
    counts["OK"] += 1

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Effects (original)", "Effects (trimmed draft)", "Building (draft)", "Status"])
    writer.writerows(out_rows)

print(f"✓ Wrote {out_path} ({len(out_rows)} rows)")
for status, n in counts.items():
    print(f"   {status}: {n}")
print("\nFor the OK rows: replace Effects with \"Effects (trimmed draft)\" and add")
print("\"Building (draft)\" as a new \"Building\" column. Hand-split the NEEDS")
print("REVIEW rows the same way, then run convert.py.")
