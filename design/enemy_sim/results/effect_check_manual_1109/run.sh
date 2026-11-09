#!/bin/bash
# effect_check on the monster manual's encounters (8 mixes, so half the
# fights per mix of the 10-29 run for the same total), ordinary fights at
# built Health (x1: the table is squared at x1 since 11-09).
OUT=/tmp/claude-0/-home-user-flagonquest/e6747bdc-fa39-5126-8ea2-8c3b178a4574/scratchpad/ec_manual
cd /home/user/flagonquest/design/enemy_sim
P=manual_
[ -s $OUT/${P}all.csv ] || python3 tools/effect_check.py --variants all --set standard -m 1 -n 500 --csv $OUT/${P}all.csv > $OUT/${P}all.txt 2>&1
for SET in standard level2 chief ogre; do
  [ -s $OUT/${P}danger_$SET.csv ] || python3 tools/effect_check.py --variants danger --set $SET -m 1 -n 250 --csv $OUT/${P}danger_$SET.csv > $OUT/${P}danger_$SET.txt 2>&1
done
[ -s $OUT/${P}fill_standard.csv ] || python3 tools/effect_check.py --variants fill --set standard -m 1 -n 250 --csv $OUT/${P}fill_standard.csv > $OUT/${P}fill_standard.txt 2>&1
[ -s $OUT/${P}fill_ogre.csv ] || python3 tools/effect_check.py --variants fill --set ogre -m 1 -n 250 --csv $OUT/${P}fill_ogre.csv > $OUT/${P}fill_ogre.txt 2>&1
[ -s $OUT/${P}fill_durable.csv ] || python3 tools/effect_check.py --variants fill --set ogre_durable -m 1 -n 250 -e necrotic -e aim_necrotic --csv $OUT/${P}fill_durable.csv > $OUT/${P}fill_durable.txt 2>&1
echo ALL DONE $(date) >> $OUT/progress.txt
