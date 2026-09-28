"""
Auto-stamps the "Patch" column on techniques.csv/items.csv with the
current version (the one row marked Current = yes in
scripts/versions.csv) for every row that's new or has changed — see
PATCH TRACKING at the top of convert.py for how the site uses this.

Not something to hand-maintain: a person editing a row doesn't touch
Patch themselves (easy to forget, exactly the kind of manual-sync drift
CLAUDE.md's data-over-prose principle warns about elsewhere) — this
derives it from what git says actually changed. convert.py calls it
automatically on every run, so in normal use nobody runs this directly.

Usage: python scripts/stamp_patch_versions.py [--since REF] [--version VERSION] [--dry-run]

  --since REF       Git ref to diff the working-tree CSVs against.
                     Defaults to HEAD, i.e. "whatever's been edited but
                     not committed yet" — which is what convert.py wants,
                     since it runs right after a CSV edit. Pass an older
                     ref to catch up on commits that edited a CSV without
                     running convert.py.
  --version VERSION The value to stamp onto changed rows. Defaults to the
                     Current = yes row of scripts/versions.csv.
  --dry-run         Print what would change without writing the CSVs.

Compares every column except "Patch" itself, "ID" (the join key), and
"Description (Fluff)" — a row is "changed" if any of those differ from
its value at --since, or if its ID didn't exist there at all (a
brand-new row). Flavor-only rewrites don't count: the badge exists to
tell players "the rules for this changed," and a new line of in-fiction
dialogue isn't that. Only touches rows that actually changed; everything
else keeps whatever Patch value it already had. Safe to run repeatedly —
a second run before committing just re-stamps the same rows with the
same version. Compares on the *intersection* of column names present in
both the old and new header, so this still works if a column was
added/renamed since --since.
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
VERSIONS_PATH = os.path.join(script_dir, "versions.csv")
# Never compared — see the module docstring for why Fluff is excluded.
IGNORED_COLUMNS = ("ID", "Patch", "Description (Fluff)")


def run_git(args):
    return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, text=True)


def read_versions():
    """Returns (versions, current) from scripts/versions.csv — the full
    list of {version, current, focus} rows in file order, and the one
    version marked Current = yes. Exits if there isn't exactly one."""
    if not os.path.exists(VERSIONS_PATH):
        sys.exit("scripts/versions.csv not found.")
    with open(VERSIONS_PATH, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("Version") or "").strip()]
    versions = [{
        "version": r["Version"].strip(),
        "current": (r.get("Current") or "").strip().lower() in ("yes", "y", "true"),
        "focus": (r.get("Focus") or "").strip(),
    } for r in rows]
    current = [v["version"] for v in versions if v["current"]]
    if len(current) != 1:
        sys.exit(f"scripts/versions.csv needs exactly one row with Current = yes (found {len(current)}).")
    return versions, current[0]


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
    # than needing someone to hand-repair it first.
    added_column = "Patch" not in fieldnames
    if added_column:
        fieldnames.append("Patch")
        for row in rows:
            row["Patch"] = ""
    return fieldnames, rows, added_column


def _norm(value):
    # `git show` output goes through text-mode universal newlines, which
    # turns a CRLF inside a quoted multi-line field into LF, while the
    # working-tree file is read with newline="" and keeps it. Without
    # this, any row with a multi-line field (T027 Profession's Choice
    # Effects) would look "changed" on every run.
    return (value or "").replace("\r\n", "\n")


def row_changed(new_row, old_row, compare_cols):
    return any(_norm(new_row.get(c)) != _norm(old_row.get(c)) for c in compare_cols)


def stamp(version, since="HEAD", dry_run=False, verbose=True):
    """Stamps every changed/new row since `since` with `version`. Returns
    the number of rows whose Patch value actually changed (a row already
    carrying `version` doesn't count, so a repeat run reports 0)."""
    newly_stamped = 0
    for filename in TARGET_FILES:
        new_fieldnames, new_rows, added_column = read_working_csv(filename)
        old_fieldnames, old_rows_by_id = read_csv_at_ref(since, filename)
        if added_column and verbose:
            print(f"{filename}: had no Patch column — re-added it (blank) before stamping.")

        if old_fieldnames is None:
            if verbose:
                print(f"⚠ {filename} didn't exist at {since!r} — every row will be stamped as new.")
            compare_cols = [c for c in new_fieldnames if c not in IGNORED_COLUMNS]
        else:
            compare_cols = [c for c in new_fieldnames if c in old_fieldnames and c not in IGNORED_COLUMNS]

        changed = []
        for row in new_rows:
            rid = row.get("ID")
            if not rid:
                continue
            old_row = old_rows_by_id.get(rid)
            if old_row is None or row_changed(row, old_row, compare_cols):
                if row.get("Patch") != version:
                    changed.append((rid, row.get("Name"), "new" if old_row is None else "changed"))
                    row["Patch"] = version

        newly_stamped += len(changed)
        if verbose:
            for rid, name, reason in changed:
                print(f"   Patch {version}: {filename} {rid} {name!r} ({reason})")

        if (changed or added_column) and not dry_run:
            path = os.path.join(script_dir, filename)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=new_fieldnames)
                writer.writeheader()
                writer.writerows(new_rows)
    return newly_stamped


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", default="HEAD", help="Git ref to diff against (default: HEAD)")
    parser.add_argument("--version", help="Version to stamp (default: Current row of scripts/versions.csv)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files")
    args = parser.parse_args()

    version = args.version or read_versions()[1]
    print(f"Stamping changed/new rows with Patch = {version!r} (diffing against {args.since!r})")
    n = stamp(version, args.since, args.dry_run)
    if n == 0:
        print("Nothing new to stamp.")
    elif args.dry_run:
        print("Dry run — no files written.")


if __name__ == "__main__":
    main()
