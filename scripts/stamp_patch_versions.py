"""
Auto-stamps the "Patch" column on techniques.csv/items.csv for every row
that's new or has changed since a given point in git history — see
PATCH TRACKING at the top of convert.py for how the site uses this.

Not something to hand-maintain: a person editing a row doesn't touch
Patch themselves (easy to forget, exactly the kind of manual-sync drift
CLAUDE.md's data-over-prose principle warns about elsewhere) — this
script derives it directly from what git says actually changed.

Usage: python scripts/stamp_patch_versions.py [--since REF] [--version VERSION] [--dry-run]

  --since REF       Git ref to diff the working-tree CSVs against.
                     Defaults to the most recent git tag (`git describe
                     --tags --abbrev=0`) — see the release workflow in
                     convert.py's PATCH TRACKING doc for why a release
                     should end with a tag.
  --version VERSION The value to stamp onto changed rows. Defaults to
                     the contents of scripts/version.txt — bump that
                     file first, then run this script, so the two never
                     disagree about what version is being released.
  --dry-run         Print what would change without writing the CSVs.

Compares every column except "Patch" itself, "ID" (the join key), and
"Description (Fluff)" — a row is "changed" if any of those differ from
its value at --since, or if its ID didn't exist there at all (a
brand-new row). Flavor-only rewrites deliberately don't count: the
badge exists to tell players "the rules for this changed," and a new
line of in-fiction dialogue isn't that. Only touches
rows that actually changed; everything else keeps whatever Patch value
it already had. Compares on the *intersection* of column names present
in both the old and new header, so this still works even if a column
was added/renamed since --since — it just can't detect a change in a
column that didn't exist yet at the old ref.
"""

import argparse
import csv
import io
import os
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
TARGET_FILES = ["techniques.csv", "items.csv"]
# Never compared — see the module docstring for why Fluff is excluded.
IGNORED_COLUMNS = ("ID", "Patch", "Description (Fluff)")


def run_git(args):
    result = subprocess.run(["git", *args], cwd=repo_root, capture_output=True, text=True)
    return result


def latest_tag():
    result = run_git(["describe", "--tags", "--abbrev=0"])
    if result.returncode != 0:
        sys.exit(
            "No git tags found, and no --since ref was given.\n"
            "This script needs a baseline to diff against — tag the commit you want to\n"
            "treat as \"the last release\" (e.g. `git tag v1.0`) and try again, or pass\n"
            "--since <ref> explicitly."
        )
    return result.stdout.strip()


def read_csv_at_ref(ref, filename):
    """Returns (fieldnames, {id: row_dict}) for scripts/<filename> as it
    existed at `ref`, or (None, {}) if the file didn't exist there yet."""
    result = run_git(["show", f"{ref}:scripts/{filename}"])
    if result.returncode != 0:
        return None, {}
    reader = csv.DictReader(io.StringIO(result.stdout))
    rows = {row["ID"]: row for row in reader if row.get("ID")}
    return reader.fieldnames, rows


def read_working_csv(filename):
    path = os.path.join(script_dir, filename)
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    # A CSV with no Patch column at all — e.g. after resolving a merge by
    # taking a branch that was cut before this column existed — gets it
    # re-added here (blank = "unchanged since tracking began") rather
    # than needing someone to hand-repair it first. Lossless in that
    # situation, since every baseline Patch value was blank anyway.
    added_column = "Patch" not in fieldnames
    if added_column:
        fieldnames.append("Patch")
        for row in rows:
            row["Patch"] = ""
    return fieldnames, rows, added_column


def row_changed(new_row, old_row, compare_cols):
    return any((new_row.get(c) or "") != (old_row.get(c) or "") for c in compare_cols)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", help="Git ref to diff against (default: latest tag)")
    parser.add_argument("--version", help="Version to stamp (default: scripts/version.txt)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files")
    args = parser.parse_args()

    since = args.since or latest_tag()

    if args.version:
        version = args.version
    else:
        version_path = os.path.join(script_dir, "version.txt")
        if not os.path.exists(version_path):
            sys.exit("scripts/version.txt not found and no --version given.")
        with open(version_path, encoding="utf-8") as f:
            version = f.read().strip()

    print(f"Stamping changed/new rows with Patch = {version!r} (diffing against {since!r})\n")

    any_changes = False
    for filename in TARGET_FILES:
        new_fieldnames, new_rows, added_column = read_working_csv(filename)
        old_fieldnames, old_rows_by_id = read_csv_at_ref(since, filename)
        if added_column:
            print(f"{filename}: had no Patch column — re-added it (blank) before stamping.")

        if old_fieldnames is None:
            print(f"⚠ {filename} didn't exist at {since!r} — every row will be stamped as new.")
            compare_cols = [c for c in new_fieldnames if c not in IGNORED_COLUMNS]
        else:
            compare_cols = [c for c in new_fieldnames if c in old_fieldnames and c not in IGNORED_COLUMNS]

        changed_ids = []
        for row in new_rows:
            rid = row.get("ID")
            if not rid:
                continue
            old_row = old_rows_by_id.get(rid)
            if old_row is None:
                changed_ids.append((rid, row.get("Name"), "new"))
                row["Patch"] = version
            elif row_changed(row, old_row, compare_cols):
                changed_ids.append((rid, row.get("Name"), "changed"))
                row["Patch"] = version

        if changed_ids:
            any_changes = True
            print(f"{filename}: {len(changed_ids)} row(s) stamped")
            for rid, name, reason in changed_ids:
                print(f"   {rid}  {name!r}  ({reason})")
        else:
            print(f"{filename}: no changes since {since!r}")

        if (changed_ids or added_column) and not args.dry_run:
            path = os.path.join(script_dir, filename)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=new_fieldnames)
                writer.writeheader()
                writer.writerows(new_rows)

    print()
    if args.dry_run:
        print("Dry run — no files written." if any_changes else "Dry run — nothing would change.")
    else:
        print("Done. Run convert.py next to regenerate data/*.json, then commit and tag the release.")


if __name__ == "__main__":
    main()
