# Prose review queue

`rulebook.md`/`glossary.md` sections written or edited during an
AI-assisted session, so a later full read-through can find them without
combing the whole book looking for what changed. This is a checklist,
not a permanent record — **delete an entry once you've reviewed it**
(git history is the permanent record; `git log -p -- scripts/rulebook.md
scripts/glossary.md` or the commit hash noted below gets you the exact
diff for any entry here). Populated starting from this session forward,
not retroactively audited across the whole project history — ask for
that separately if you want it.

## rulebook.md

- **`## A Full Night's Rest`** — renamed the three resting steps to
  Cycles (the Discard Cycle, the Recovery Cycle, the Draw Cycle), added
  a default ordering rule ("the listed action happens first, then
  anything else from your items/abilities tied to that Cycle"). Commit
  `93efdc2`.

## glossary.md

- **`#### Burst (X)`** (new entry, `# Keywords`) — added to name "this
  space, plus every space within X meters of it" for area effects, used
  going forward instead of ad hoc "adjacent to"/"within X meters of"
  phrasing. Commit `4ab9a21`.
