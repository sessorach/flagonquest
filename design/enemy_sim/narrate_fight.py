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
        [--encounter "Name 1,Name 2,..."] [--json out.json]
        [--html out.html]

`--static` runs the original (non-movement) mode instead - no position
map then, just the combat log. `--party` swaps in a custom mix (see
party.make_party_from) instead of the Tier's Roster; give exactly 4
names. `--encounter` swaps in a custom enemy mix (see sample_enemies.
build_encounter) instead of `n_enemies` copies of the Level's Roster
enemy - any mix of named rows, any Level/Slots combination (e.g. a Tank
plus several Minions - see sample_enemies.py's own module docstring for
the "one Slot per PC" convention); `enemy_level`/`--n-enemies` are
ignored when this is given. `--json` writes the raw trace (plus the
fight result) as JSON. `--html` writes a real self-contained HTML
replay page (battle-map + combat log, same data as this terminal
output but genuinely graphical - see replay_html.py) that you can open
in any browser, no server needed - the easiest way to just look at one
fight without reading a JSON dump.
"""
import argparse
import json
import sys

import combat_sim as cs
import tunables as T
from party import make_party_from
from sample_enemies import build_encounter
from replay_html import render_html


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
        pos = tuple(event['pos'])  # whole spaces already - movement.py's own docstring
        spaces = event.get('spaces')
        moved = f" ({spaces} space{'s' if spaces != 1 else ''})" if spaces is not None else ""
        if event.get('in_range'):
            return f"  {unit} moves{moved} toward its target, ends at {pos} - now in range."
        return f"  {unit} moves{moved} toward its target, ends at {pos} - still out of range, no attack."
    if action == 'attack':
        verb = 'HITS' if event['hit'] else 'misses'
        via = f" with {event['via']}" if event.get('via') else ""
        extra = ''
        if event['hit']:
            absorbed = event.get('protected_absorbed', 0)
            breakdown = f"{event['raw_dmg']} raw - {event['resist']} resist"
            if absorbed:
                breakdown += f" - {absorbed} Protected"
            extra = f" for {event['dmg']} damage ({breakdown} = {event['dmg']}) (-> {event['target_hp_after']} HP)"
        # The target's own Harried count right after this attack -
        # logged regardless of whether *this* attack was the one that
        # added a stack (a Bodily/Mental-opposed attack doesn't grant
        # Harried, but the target can still be carrying stacks from an
        # earlier Parry/Dodge-opposed attack this same round).
        harried = event.get('target_harried_after', 0)
        if harried:
            extra += f" (target now Harried {harried})"
        if event.get('turn_shift'):
            extra += f" [{event['turn_shift']}]"
        return f"  {unit} attacks {event['target']}{via}: rolls {event['roll']} vs {event['defense']} - {verb}{extra}"
    if action == 'heal':
        via = f" with {event['via']}" if event.get('via') else ""
        return f"  {unit} heals {event['target']}{via} for {event['amount']} (-> {event['target_hp_after']} HP)"
    return f"  {unit} {action} {event}"


def narrate(trace, movement_on):
    by_round = {}
    result = None
    initiative = None
    for event in trace:
        if event.get('type') == 'result':
            result = event
            continue
        if event.get('type') == 'initiative':
            initiative = event
            continue
        by_round.setdefault(event['round'], []).append(event)
    if initiative:
        order = ', '.join(f"{o['unit']} ({o['side']})" for o in initiative['order'])
        print(f"Turn order: {order}")
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
    ap.add_argument('--encounter', help='comma-separated sample_enemies.csv names, any mix (default: n_enemies copies of the Level Roster)')
    ap.add_argument('--json', help='also write the raw trace + result to this file')
    ap.add_argument('--html', help='also write a self-contained HTML replay page to this file')
    ap.add_argument('--vs-average', type=int, nargs='?', const=1000, default=None,
                     help='also run N aggregate trials (default 1000) of this exact same matchup/party mods '
                          'and print/embed how this one seeded fight compares - win rate, avg rounds, avg HP on win')
    args = ap.parse_args()

    movement_on = not args.static
    if args.party:
        names = args.party.split(',')
        cs.make_party = lambda tier, good_luck=0, names=names: make_party_from(names, good_luck)
    enemies = build_encounter(args.encounter.split(',')) if args.encounter else None

    trace = []
    result = cs.run_fight(args.tier, args.enemy_level, n_enemies=args.n_enemies,
                           seed=args.seed, movement=movement_on, trace=trace, enemies=enemies)
    narrate(trace, movement_on)

    if args.vs_average:
        # Same matchup/party mods (make_party is already monkeypatched above
        # if --party was given), a fresh unseeded batch - "how does this one
        # seeded fight compare to the shape of the matchup overall."
        win_pct, avg_rounds, avg_hp, _, _ = cs.simulate(
            args.tier, args.enemy_level, n_enemies=args.n_enemies, trials=args.vs_average,
            movement=movement_on, enemies=enemies)
        result['vs_average'] = {'trials': args.vs_average, 'win_pct': win_pct,
                                 'avg_rounds': avg_rounds, 'avg_hp_on_win': avg_hp}
        this_hp = f", {result['party_hp_pct'] * 100:.0f}% party HP" if result['winner'] == 'party' else ''
        print(f"\nThis fight: {result['winner']} won in {result['rounds']} rounds{this_hp}.")
        print(f"Average over {args.vs_average} trials of this same matchup: "
              f"{win_pct:.1f}% win rate, {avg_rounds:.1f} rounds, {avg_hp:.1f}% HP on win.")

    if args.json:
        with open(args.json, 'w') as f:
            json.dump({'trace': trace, 'result': result, 'arena_size': T.ARENA_SIZE}, f, indent=2)
        print(f"\nWrote trace to {args.json}", file=sys.stderr)

    if args.html:
        with open(args.html, 'w') as f:
            f.write(render_html(trace, result, T.ARENA_SIZE))
        print(f"Wrote HTML replay to {args.html} - open it in any browser.", file=sys.stderr)


if __name__ == '__main__':
    main()
