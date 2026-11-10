#!/bin/bash
# effect_check over whole days (2026-11-10): ordinary days (+0 Slots) and
# threatening days (+1 Slot), every test; 250 days a mix. Skips what's done.
OUT=/tmp/claude-0/-home-user-flagonquest/e6747bdc-fa39-5126-8ea2-8c3b178a4574/scratchpad/ec_day
cd /home/user/flagonquest/design/enemy_sim
for X in 0 1; do
  for V in all danger fill; do
    F=$OUT/day_x${X}_$V
    [ -s $F.csv ] || python3 tools/effect_check.py --day --extra $X --variants $V -n 250 --csv $F.csv > $F.txt 2>&1
  done
done
echo ALL DONE $(date) >> $OUT/progress.txt
