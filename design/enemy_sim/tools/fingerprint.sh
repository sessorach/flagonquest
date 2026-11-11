#!/bin/bash
# Fixed-seed fingerprint of the live tools (2026-11-11), to prove a change
# moved nothing: run it before and after into two folders, then
#   tools/fingerprint.sh compare BEFORE AFTER
# Run from design/enemy_sim. Small runs (minutes), fixed seeds.
if [ "$1" = compare ]; then
  A=$2; B=$3
  diff -rq -x _status -x manual_read.md -x opt "$A" "$B"
  diff <(sort "$A/manual_read.md") <(sort "$B/manual_read.md") > /dev/null || echo "manual_read differs"
  diff -r "$A/opt" "$B/opt" > /dev/null || echo "optimizer output differs"
  exit
fi
OUT=$(realpath -m "$1"); mkdir -p "$OUT"; rm -rf "$OUT"/*
r() { name=$1; shift; timeout 3000 env "$@" > "$OUT/$name.txt" 2>&1; echo "$name $?" >> "$OUT/_status"; }
r dayhash PYTHONPATH=. python3 -c "
import day_sim as ds, json, hashlib
r = ds.run(['Hilde', 'Browndog', 'Jackal', 'Hanforth'], {}, 2, 6, seed=5)
r2 = ds.run(['Hilde', 'Browndog', 'Jackal', 'Hanforth'], {}, 3, 3, days=3, seed=7)
print(hashlib.md5(json.dumps([r, r2], sort_keys=True, default=str).encode()).hexdigest())"
for L in 1 2 3; do r calibrate$L python3 tools/calibrate.py -n 30 -L $L; done
r effect python3 tools/effect_check.py -n 20 -m 1 -e crippled -e protected --csv "$OUT/effect.csv"
r effect_day python3 tools/effect_check.py --day --extra 1 -n 5 -e crippled -e harried --csv "$OUT/effect_day.csv"
r table python3 tools/table_check.py -L 2 -n 5 -o "$OUT/table.jsonl"
r manual python3 tools/manual_check.py -o "$OUT/manual.jsonl" -L 2 -k 4 -n 2
r manual_read python3 tools/manual_check.py -o "$OUT/manual.jsonl" --read --txt "$OUT/manual_read.md"
r size python3 tools/size_check.py run -o "$OUT/size.jsonl" -n 1 -L 2 --kinds elite
r size_read python3 tools/size_check.py read -o "$OUT/size.jsonl" --txt "$OUT/size_read.md"
r stats python3 tools/combat_stats.py -n 1 --name _fp_stats; mv results/enemy_stats/_fp_stats.txt "$OUT/"
r xpinv SIM_SET="DEBUFF_ABUSE=True" python3 tools/xp_investments.py -L 2 --extra 1 -n 2 -o "$OUT/xpinv_res.txt"
r compare python3 tools/compare_builds.py -L 2 -p B --swap "Beornhard (L2)=Beornhard (L2, Frost)" -n 20
r tactics python3 tools/tactics_compare.py -L 2 -p A -n 20 -t cautious
r reprice python3 tools/reprice.py run -o "$OUT/reprice.jsonl" -n 1 --only "Damage +1"
r optimizer python3 tools/build_optimizer.py --arch Hilde -L 2 -g 1 -n 3 -p 4 -o "$OUT/opt" --seed 3
r tpass python3 tools/technique_pass.py -n 2 --techniques --ids T077,T034 -o "$OUT/tpass.csv"
r manualmd python3 tools/monster_manual.py; cp MONSTER_MANUAL.md "$OUT/"
r bands python3 tools/bands.py --check
r coverage python3 tools/coverage.py
# Strip timings and progress counters; sort what parallel workers wrote in any order.
sed -i -E 's/[0-9]+(\.[0-9]+)?s\b/Xs/g; s/[0-9]+\/[0-9]+ (chunks|jobs)?//g' "$OUT"/*.txt
sed -i "s#$OUT#OUT#g" "$OUT"/*.txt
for f in "$OUT"/*.jsonl; do sort -o "$f" "$f"; done
python3 - "$OUT" <<'PY'
import json, sys, glob
for p in glob.glob(sys.argv[1] + "/*.json"):
    d = json.load(open(p))
    if isinstance(d, list):
        json.dump(sorted([json.dumps(c), sorted(map(json.dumps, r))] for c, r in d), open(p, "w"))
PY
