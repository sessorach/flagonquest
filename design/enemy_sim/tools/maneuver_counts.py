"""Whole-fight counts with each investment, Level 2 middle parties, +1 Slot days."""
import sys, json, collections
from multiprocessing import Pool

import _paths, xp_investments as xi, combat_sim as cs, sample_enemies as se, party, day_sim as ds
import bands
DAYS = 60

def bm(features, lvl=2):
    return lambda b: (b["techniques"].append(party._entry({"id": "T072", "level": lvl, "features": features})), b)[1]

def variant(build, pc, name):
    if name == "base":
        return build
    if name == "attack skill +1":
        b = json.loads(json.dumps(build)); b["skillPoints"][pc["attack_skill"]] = int(b["skillPoints"][pc["attack_skill"]]) + 1; return b
    feats = {"wing6": {"Wing Clip": 6}, "calc_wing3": {"Calculated": 1, "Wing Clip": 3}, "battering6": {"Battering": 6}}[name]
    return bm(feats)(json.loads(json.dumps(build)))

def job(args):
    gi, seat, name = args
    xi.register(2, 1)
    gname, names, swaps = [g for g in bands.groups(2, bands.MID[2]) if g[0] != "stand-ins"][gi]
    swaps = dict(swaps); m = names[seat]; rows = party._rows()
    pc = party.make_pc(m, 1, rows=rows, edits=swaps[m][0], row_changes=swaps[m][1])
    b = variant(json.loads(json.dumps(swaps[m][0]["build"])), pc, name)
    try:
        party.load_sheet(rows[m], b, strict=False)
    except Exception:
        return name, None
    swaps[m] = ({"build": b}, swaps[m][1])
    real = cs.run_fight; c = collections.Counter()
    def traced(*a, **k):
        t = []; r = real(*a, trace=t, **k)
        c['fights'] += 1; c['rounds'] += r['rounds']; c['lost'] += r['winner'] != 'party'
        for e in t:
            if e.get('action') != 'attack': continue
            if e.get('side') == 'party':
                c['party_att'] += 1; c['party_hit'] += bool(e.get('hit')); c['party_dmg'] += e.get('dmg', 0) if e.get('hit') else 0
                if str(e.get('unit')).startswith(m):
                    c['car_att'] += 1; c['car_hit'] += bool(e.get('hit'))
                    if e.get('via') == 'Battle Maneuver':
                        c['car_bm'] += 1; c['car_bm_hit'] += bool(e.get('hit'))
                        c['car_bm_card'] += bool(e.get('cards'))
            else:
                c['en_att'] += 1; c['en_hit'] += bool(e.get('hit')); c['en_dmg'] += e.get('dmg', 0) if e.get('hit') else 0
        return r
    cs.run_fight = traced
    for k in range(DAYS):
        mi = k % 8
        rec, _ = ds.play_day(names, swaps, 2, ds.day_mixes(mi, k), 100_000 * mi + k, rows)
        c['days'] += 1; c['days_lost'] += bool(rec['lost'])
    cs.run_fight = real
    return name, c

if __name__ == '__main__':
    names = ["base", "attack skill +1", "wing6", "calc_wing3", "battering6"]
    seats = sorted({(c[0], c[1]) for c in xi.cells(2) if c[2] == "Battle Maneuver L2: Wing Clip x6 (Crippled)"})
    tot = {n: collections.Counter() for n in names}
    with Pool() as p:
        for name, c in p.imap_unordered(job, [(g, s, n) for g, s in seats for n in names]):
            if c: tot[name].update(c)
    print(f"{len(seats)} carriers, {DAYS} days each\n")
    print("| | Days lost | Rounds a fight | Carrier attacks / hits a fight | its Maneuver attacks / hit% / with a card | Party hits a fight | Enemy attacks / hits / damage a fight |")
    print("|---|---|---|---|---|---|---|")
    for n in names:
        c = tot[n]; f = c['fights']
        print(f"| {n} | {100 * c['days_lost'] / c['days']:.1f}% | {c['rounds'] / f:.2f} | {c['car_att'] / f:.2f} / {c['car_hit'] / f:.2f} | "
              f"{c['car_bm'] / f:.2f} / {100 * c['car_bm_hit'] / max(1, c['car_bm']):.0f}% / {100 * c['car_bm_card'] / max(1, c['car_bm']):.0f}% | "
              f"{c['party_hit'] / f:.2f} | {c['en_att'] / f:.2f} / {c['en_hit'] / f:.2f} / {c['en_dmg'] / f:.2f} |")
