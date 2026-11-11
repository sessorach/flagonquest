# Finished simulator studies (archived 2026-11-11)

One-off studies from `design/enemy_sim/experiments/`, moved here when the
simulator was tidied. Their results are written up in
`design/ENEMY_ENCOUNTER_DESIGN.md`, `design/balance_weights_notes.md` and
`design/DESIGNER_NOTES.md`, which name them; the decisions they led to
live in `design/enemy_sim/tunables.py`.

They won't run from here. Most were written for settings that have since
changed (the old roster's four mixes, enemy tables v1/v2, enemy Health
x1.75, an earlier Bleeding rule), and many import each other or helpers
that now live in `design/enemy_sim/tools/bands.py`. To rerun one, copy it
back into `design/enemy_sim/experiments/<topic>/` and expect to update it.

- `bleeding/`: the Bleeding rule studies (October).
- `enemies/`: the enemy tables, the roster-era encounter studies, big
  enemies, and the table-tuning one-offs of November.
- `pc_options/`: Play Styles, turn order, party targeting, the Beornhard,
  Hanforth and Maneuver sweeps.
- `yardsticks/`: the yardstick debate (late October).
- `results/`: two effect-check cell scripts that only ran from a scratch
  folder.
- `run_grid.py`: the original Tier × Level grid on the retired v1 enemies.
