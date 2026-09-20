"""
Runs ONE seeded fight with tracing on (combat_sim.run_fight(...,
trace=[])) and renders it as a round-by-round position map plus a
combat log - for actually looking at what this simulator does, not
just reading an aggregate win rate off run_grid.py. Also good for
sanity-checking a new tactic/strategy in tactics.py: read the log and
check it's doing what you meant.

Usage:
    python3 narrate_fight.py [tier] [enemy_level] [seed]
        [--n-enemies N] [--static] [--party name1,name2,name3,name4]
        [--json out.json]

`--static` runs the original (non-movement) mode instead - no position
map then, just the combat log. `--party` swaps in a custom mix (see
party.make_party_from) instead of the Tier's Roster; give exactly 4
names. `--json` also writes the raw trace (plus the fight result) to a
file, e.g. for narrate_fight.html to render as a real graphical
battle-map instead of ASCII.
"""
import argparse
import json
import sys

import combat_sim as cs
import tunables as T
from party import make_party_from


def build_labels(first_positions_event):
    """A stable {unit_name: 'P1'/'E1'/...} map, built once from round 1's
    positions event (logged before anyone can have died, so it always
    has the full roster) - reused for every later round instead of
    re-numbering whoever's still alive each time, which would silently
    reassign 'P2' to a different character the moment the original P2
    died."""
    labels = {}
    for i, u in enumerate(first_positions_event['party'], 1):
        labels[u['unit']] = f'P{i}'
    for i, u in enumerate(first_positions_event['enemies'], 1):
        labels[u['unit']] = f'E{i}'
    return labels


def render_positions_ascii(party_units, enemy_units, labels, size):
    """A `size`x`size` top-down ASCII map - stable per-fight markers
    (`labels`) at each unit's rounded (x, y), read bottom-to-top so 'up'
    on the page matches 'higher y' in the arena. Two units landing in
    the same rounded cell (rare at this scale, but possible) show as
    the first one placed, with the overlap called out in the returned
    `overlaps` list rather than silently lost."""
    cells = {}
    for u in party_units + enemy_units:
        cells.setdefault((round(u['pos'][0]), round(u['pos'][1])), []).append(labels[u['unit']])
    rows = []
    for y in range(size - 1, -1, -1):
        row = [cells.get((x, y), ['..'])[0] for x in range(size)]
        rows.append(' '.join(f'{c:>2}' for c in row))
    overlaps = [f"{'/'.join(ls)} occupy the same cell" for ls in cells.values() if len(ls) > 1]
    return rows, overlaps


def render_event(event):
    if event.get('type') in ('positions', 'result'):
        return None
    unit, action = event['unit'], event['action']
    if action == 'move':
        pos = tuple(round(c, 1) for c in event['pos'])
        return f"  {unit} moves toward its target, ends at {pos} - still out of range, no attack."
    if action == 'attack':
        verb = 'HITS' if event['hit'] else 'misses'
        extra = f" for {event['dmg']} damage (-> {event['target_hp_after']} HP)" if event['hit'] else ''
        return f"  {unit} attacks {event['target']}: rolls {event['roll']} vs {event['defense']} - {verb}{extra}"
    if action == 'heal':
        return f"  {unit} heals {event['target']} for {event['amount']} (-> {event['target_hp_after']} HP)"
    return f"  {unit} {action} {event}"


def narrate(trace, movement_on):
    by_round = {}
    result = None
    for event in trace:
        if event.get('type') == 'result':
            result = event
            continue
        by_round.setdefault(event['round'], []).append(event)
    labels = None
    for rnd in sorted(by_round):
        print(f"\n=== Round {rnd} ===")
        events = by_round[rnd]
        positions = next((e for e in events if e.get('type') == 'positions'), None)
        if movement_on and positions:
            labels = labels or build_labels(positions)
            rows, overlaps = render_positions_ascii(positions['party'], positions['enemies'], labels, T.ARENA_SIZE)
            print('\n'.join(rows))
            for u in positions['party'] + positions['enemies']:
                print(f"  {labels[u['unit']]} = {u['unit']} ({u['health']} HP)")
            for o in overlaps:
                print(f"  ({o})")
        for e in events:
            line = render_event(e)
            if line:
                print(line)
    if result:
        print(f"\n=== Fight over: {result['winner']} wins ===")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tier', nargs='?', type=int, default=1)
    ap.add_argument('enemy_level', nargs='?', type=int, default=1)
    ap.add_argument('seed', nargs='?', type=int, default=1)
    ap.add_argument('--n-enemies', type=int, default=4)
    ap.add_argument('--static', action='store_true', help='run movement=False instead')
    ap.add_argument('--party', help='comma-separated names, exactly 4 (default: the Tier Roster)')
    ap.add_argument('--json', help='also write the raw trace + result to this file')
    args = ap.parse_args()

    movement_on = not args.static
    if args.party:
        names = args.party.split(',')
        cs.make_party = lambda tier, good_luck=0, names=names: make_party_from(names, good_luck)

    trace = []
    result = cs.run_fight(args.tier, args.enemy_level, n_enemies=args.n_enemies,
                           seed=args.seed, movement=movement_on, trace=trace)
    narrate(trace, movement_on)

    if args.json:
        with open(args.json, 'w') as f:
            json.dump({'trace': trace, 'result': result, 'arena_size': T.ARENA_SIZE}, f, indent=2)
        print(f"\nWrote trace to {args.json}", file=sys.stderr)


if __name__ == '__main__':
    main()
