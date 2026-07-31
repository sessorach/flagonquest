"""
Drafts a "Feature Budget" column from the "Points: Level N: M basic(/advanced);
..." sentence already buried in each Feature-built technique's Effects text,
so you're not typing it by hand. One-time/occasional helper — not part of
the normal convert.py pipeline.

Usage: python scripts/draft_feature_budget.py

Reads techniques.csv, leaves any row that already has a "Feature Budget"
value alone, and writes scripts/feature_budget_draft.csv with a best-guess
value for every technique whose Effects text matches that sentence, plus
a Status column: OK, NOT BUILDABLE (Features isn't TRUE — no budget
needed), or NEEDS REVIEW (Features is TRUE but no matching sentence was
found — hand-write that one). Copy the "Feature Budget (draft)" column
into your spreadsheet, skim the NEEDS REVIEW rows, then run convert.py —
it validates the syntax and flags anything the draft got wrong.
"""

import csv
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path   = os.path.join(script_dir, "techniques.csv")
out_path   = os.path.join(script_dir, "feature_budget_draft.csv")

# Same pattern parsePointBudget() in index.html has always used to regex
# this out of the Effects prose at runtime.
POINTS_RE = re.compile(r"Level\s*(\d+):\s*(\d+)\s*basic(/advanced)?", re.IGNORECASE)


def draft(effects_text):
    text = effects_text or ""
    matches = POINTS_RE.findall(text)
    if not matches:
        return "", "NEEDS REVIEW — no \"Level N: M basic\" sentence found in Effects"
    entries = [f"{level}:{points}{'/adv' if adv else ''}" for level, points, adv in matches]
    return ", ".join(entries), "OK"


with open(csv_path, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

out_rows = []
counts = {"OK": 0, "NOT BUILDABLE": 0, "NEEDS REVIEW": 0, "SKIPPED (already filled in)": 0}
for r in rows:
    existing = (r.get("Feature Budget") or "").strip()
    if existing:
        out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), existing, "SKIPPED (already filled in)"])
        counts["SKIPPED (already filled in)"] += 1
        continue
    if (r.get("Features") or "").strip().upper() != "TRUE":
        out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), "", "NOT BUILDABLE"])
        counts["NOT BUILDABLE"] += 1
        continue
    value, status = draft(r.get("Effects", ""))
    bucket = "NEEDS REVIEW" if status.startswith("NEEDS REVIEW") else status
    counts[bucket] += 1
    out_rows.append([r["ID"], r["Name"], r.get("Effects", ""), value, status])

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Effects", "Feature Budget (draft)", "Status"])
    writer.writerows(out_rows)

print(f"✓ Wrote {out_path} ({len(out_rows)} rows)")
for status, n in counts.items():
    print(f"   {status}: {n}")
print("\nCopy the \"Feature Budget (draft)\" column into your spreadsheet's new")
print("\"Feature Budget\" column for the OK rows, hand-write the NEEDS REVIEW")
print("ones, then run convert.py — it validates the syntax for real.")
