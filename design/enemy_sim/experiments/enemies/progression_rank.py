"""Rank progression_sweep.py's configs against the table targets (2026-11-03).

Middle of the band, per Level: days won about 95% (the designer's "won
almost always"), someone Down in about a fifth of fresh fights (under a
third), Wounded about every other fight, 4-5 rounds (designer,
2026-11-02), a hit enemy acting again about half the time. The miss is a
sum of how far each reading sits outside its target band, scaled so a
point of each counts about the same; Levels are summed.

    python3 experiments/enemies/progression_rank.py results/enemy_stats/progressions.jsonl [--top 15]
"""
import argparse
import json

# (low, high, points per unit outside)
TARGETS = {"day": (93, 98, 1 / 2), "down": (12, 28, 1 / 4), "wounded": (42, 58, 1 / 4),
           "rounds": (4.0, 5.0, 4), "again": (42, 60, 1 / 8)}


def miss(row):
    f1 = row["1"] if "1" in row else row[1]
    vals = dict(day=row["day"], down=f1["down"], wounded=f1["wounded"], rounds=f1["rounds"], again=f1["again"])
    out = 0.0
    for k, (lo, hi, w) in TARGETS.items():
        v = vals[k]
        out += w * (lo - v if v < lo else v - hi if v > hi else 0)
    return out, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(a.path) if l.strip()]
    scored = []
    for r in recs:
        mids = {k: v for k, v in r["rows"].items()}
        per = {k: miss(v) for k, v in mids.items()}
        scored.append((sum(m for m, _ in per.values()), r, per))
    scored.sort(key=lambda x: x[0])
    for total, r, per in scored[:a.top]:
        e = r["enemy_l3"]
        print(f"{total:6.1f}  {r['label']:34s} L3 enemy Health {e['health']:4.1f} Resist {e['physres']:.1f}/{e['elemres']:.1f} "
              f"Damage {e['damage']:.1f} Acc {e['accuracy']:.1f}")
        for k in sorted(per, key=lambda k: int(k.split(":")[0])):
            m, v = per[k]
            print(f"         L{k.split(':')[0]} days {v['day']:5.1f} Down {v['down']:3.0f} Wnd {v['wounded']:3.0f} "
                  f"rds {v['rounds']:.1f} again {v['again']:2.0f}   miss {m:4.1f}")


if __name__ == "__main__":
    main()
