"""Where a Wing Clip Battle Maneuver's stacks go, Level 2 middle parties, +1 Slot days."""
import sys, re, collections, statistics as st
from multiprocessing import Pool

import _paths, xp_investments as xi, combat_sim as cs, sample_enemies as se, party, day_sim as ds
import tunables as T
LABEL = sys.argv[1] if len(sys.argv) > 1 else "Battle Maneuver L2: Wing Clip x6 (Crippled)"
DAYS = 40

def job(args):
    gi, seat = args
    xi.register(2, 1)
    gname, names, swaps = xi.edited(2, gi, seat, LABEL)
    carrier = names[seat]
    rows = party._rows()
    real = cs.run_fight
    traces = []
    def traced(*a, **k):
        t = []
        r = real(*a, trace=t, **k)
        traces.append(t)
        return r
    cs.run_fight = traced
    for k in range(DAYS):
        mi = k % 8
        ds.play_day(names, swaps, 2, ds.day_mixes(mi, k), 100_000 * mi + k, rows)
    cs.run_fight = real
    c = collections.Counter()
    for tr in traces:
        c['fights'] += 1
        crip = {}
        last = None
        for t in tr:
            u = t.get('unit')
            if u != last and last in crip and crip[last] > 0 and last is not None and not str(last).startswith(tuple(names)):
                crip[last] -= 1   # the enemy's turn ended
            last = u
            if t.get('action') != 'attack':
                continue
            if t.get('side') == 'party' and str(u).startswith(carrier) and 'Crippled +' in str(t.get('effects') or ''):
                n = int(re.search(r'Crippled \+(\d+)', t['effects']).group(1))
                c['hits_with_stacks'] += 1
                c['stacks'] += n
                if t.get('target_hp_after', 1) <= 0:
                    c['killed_same_hit'] += 1
                    c['stacks_wasted_kill'] += n
                else:
                    crip[t['target']] = crip.get(t['target'], 0) + n
                    c['landed_alive'] += 1
            elif t.get('side') == 'enemy' and crip.get(u, 0) > 0:
                cc = crip[u]
                c['enemy_attacks_crippled'] += 1
                c['penalty_points'] += cc
                if not t.get('hit') and t.get('roll', 0) + cc >= t.get('defense', 99):
                    c['hits_prevented'] += 1
                    c['dmg_prevented_est'] += 0
        # stacks never used: left on enemies when they died or the fight ended
    return c

if __name__ == '__main__':
    cells = sorted({(c[0], c[1]) for c in xi.cells(2) if c[2] == LABEL})
    tot = collections.Counter()
    with Pool() as p:
        for c in p.imap_unordered(job, cells):
            tot.update(c)
    f = tot['fights']
    print(LABEL, f"- {len(cells)} carriers, {f} fights")
    print(f"  Maneuver hits that landed stacks, per fight: {tot['hits_with_stacks'] / f:.2f}")
    print(f"  stacks per landing: {tot['stacks'] / max(1, tot['hits_with_stacks']):.1f}")
    print(f"  ...landed on a target the same hit dropped: {100 * tot['killed_same_hit'] / max(1, tot['hits_with_stacks']):.0f}%")
    print(f"  enemy attacks made while Crippled, per landing on a survivor: {tot['enemy_attacks_crippled'] / max(1, tot['landed_alive']):.2f}")
    print(f"  penalty points used on those attacks, per landing: {tot['penalty_points'] / max(1, tot['landed_alive']):.2f}")
    print(f"  enemy hits turned into misses, per fight: {tot['hits_prevented'] / f:.3f}  (per day {2 * tot['hits_prevented'] / f:.3f})")
