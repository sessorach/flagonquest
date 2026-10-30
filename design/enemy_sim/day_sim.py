"""A whole day: two fights, the party's care between and after them, and
a full night's rest (2026-10-29).

Per the designer: Health left after one fight isn't the whole story. The
question is whether a fight took more out of the party than it can get
back, since a party that goes to bed short starts the next day short,
and a party that keeps doing that eventually loses a fight. Healing
after a fight is part of what healers are for.

The day (rulebook.md, "A Full Night's Rest"; cards.start_fight):

- The morning's hand is dealt once (the Draw Cycle). Each fight's card
  budget is CARDS_FIGHT_SHARE of it, as in a single fight; the second
  fight plays with whatever the first left in hand.
- Health, Shallow lost and committed Health (Grim Resolve) carry from the
  first fight into the second. Encounter uses come back (glossary.md,
  [Encounter]).
- After each fight the party looks after itself (`care`, my play rules,
  TABLE_PLAY_NOTES.md "Between fights"): From the Brink of Death on
  anyone Downed, then Healing Magic, Lay On Hands, Bolstering Refrain and
  Second Wind with the cards a PC can spare. After the first fight a PC
  keeps a fight's budget for the second; after the second, everything
  goes, since the Discard Cycle takes the hand anyway. Patch Up goes on
  the most hurt before bed.
- Healing Magic, Second Wind and Bolstering Refrain heal Shallow Health
  only ("heals 1 Shallow Health"), unless Healing Magic has Deep
  Mending. A Downed target's first point may restore a Deep (rulebook.md,
  Health). The night heals Body plus any "extra 1 Health" (Gritty, Pranic
  Nourishment, Shawl of the Land, Patch Up), Deep first, and committed
  Health comes back.

A day is lost if either fight is. Each day reports, among other things:

- `morning`: the party's Health after the night, 0 for a lost day. The
  day's score, in points like the single-fight score.
- `short`: each PC's Health still missing in the morning, and `nights`:
  how many more nights the slowest PC needs to be full again.

    python3 day_sim.py -L 3 -p H -n 100
    python3 day_sim.py -L 3 -p H --swap "Hilde (L3)=hall_of_fame/runs/hilde_l3.json:0"
    python3 day_sim.py -L 3 -p H --days 10 -n 50   # days until a fight is lost
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T, tactics, cards  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
# The day standard (designer, 2026-10-29): two fights at ×1.75, the
# single-fight standard, lose most days.
MULT = 1.0
# Off: nobody heals between fights or before bed (what care is worth).
CARE = True
CARRY_KEYS = ("health", "max_health", "shallow_lost", "_last_health")


# ---- Health, Shallow and Deep ----

def _settle(p):
    """After a fight: Shallow lost up to date, no Health below 0."""
    tactics.sync_wounded(p)
    p['health'] = max(0, p['health'])
    p['shallow_lost'] = min(p['shallow_lost'], p['max_health'] - p['health'])
    p['_last_health'] = p['health']


def _deep_lost(p):
    return p['max_health'] - p['health'] - p['shallow_lost']


def restorable(p, deep_ok):
    return p['shallow_lost'] + (_deep_lost(p) if deep_ok else (1 if p['health'] <= 0 else 0))


def heal(p, n, deep_ok=False, deep_first=False):
    """Heals `p` by up to `n`: Shallow only unless `deep_ok`; while
    Downed the first point may restore a Deep. Returns what it healed."""
    done = 0
    if n > 0 and p['health'] <= 0 and _deep_lost(p) > 0:
        p['health'] += 1
        n -= 1
        done += 1
    order = ("deep", "shallow") if deep_first else ("shallow", "deep")
    for kind in order:
        if kind == "shallow":
            s = min(n, p['shallow_lost'])
            p['shallow_lost'] -= s
        elif deep_ok:
            s = min(n, _deep_lost(p))
        else:
            s = 0
        p['health'] += s
        n -= s
        done += s
    p['_last_health'] = p['health']
    return done


# ---- Cards outside a fight ----

def _discard(p, c):
    p['hand'].remove(c)
    p['deck'].discard.append(c)


def _take(p, k):
    """The `k` cards a heal costs: Hearts first (each heals 1 more), then
    the lowest. Returns how many were Hearts."""
    hearts = 0
    for _ in range(k):
        c = cards.lowest(p['hand'], prefer_suit=cards.HEARTS)
        hearts += cards.suit(c) == cards.HEARTS
        _discard(p, c)
    return hearts


def _neediest(pcs, deep_ok, exclude=()):
    """Downed first, then whoever's missing the most this heal can restore."""
    cands = [q for q in pcs if q not in exclude and restorable(q, deep_ok) > 0]
    return max(cands, key=lambda q: (q['health'] <= 0, restorable(q, deep_ok)), default=None)


def care(pcs, reserve, log):
    """The party looks after itself after a fight. `reserve(p)`: cards `p`
    keeps for later. Returns the Health it restored."""
    healed = 0
    # From the Brink of Death (T106, no cost): 1 Deep to a Downed ally.
    for p in pcs:
        if p['health'] > 0 and 'T106' in p['known_ids']:
            for q in pcs:
                if q['health'] <= 0:
                    healed += heal(q, 1, deep_ok=True)
                    log.append(f"{p['name']}: From the Brink of Death on {q['name']}")
    while True:
        before = healed
        for p in pcs:
            if p['health'] <= 0:
                continue
            spare = len(p['hand']) - reserve(p)
            # Healing Magic (T105): "Discard [Level] cards", 1 Shallow plus
            # one per Heart, plus Vitality; Triage and Field Medic on the
            # Wounded; Healing Pact a second target.
            if p.get('strategy') == 'support_healer' and spare >= p.get('heal_cards', 1):
                feats = p.get('heal_features') or {}
                deep_ok = bool(feats.get('Deep Mending'))
                target = _neediest(pcs, deep_ok)
                if target is not None:
                    hearts = _take(p, p.get('heal_cards', 1))
                    targets = [target]
                    if feats.get('Healing Pact'):
                        second = _neediest(pcs, deep_ok, exclude=targets)
                        targets += [second] if second else []
                    for t in targets:
                        amt = 1 + hearts + p.get('heal_bonus', 0)
                        if t['shallow_lost'] >= t['shallow_max'] and t['health'] > 0:
                            amt += 2 * feats.get('Triage', 0) + ('Field Medic' in p.get('passives', ()))
                        got = heal(t, amt, deep_ok=deep_ok)
                        healed += got
                        log.append(f"{p['name']}: Healing Magic on {t['name']}, {got}")
                    continue
            # Lay On Hands (T020): a card, 1 Health (2 on a Heart), either kind.
            if 'T020' in p['known_ids'] and spare >= 1:
                target = _neediest(pcs, True)
                if target is not None:
                    got = heal(target, 1 + _take(p, 1), deep_ok=True)
                    healed += got
                    log.append(f"{p['name']}: Lay On Hands on {target['name']}, {got}")
                    continue
            # Bolstering Refrain (T066): 2 cards, 1 Shallow to each of up to
            # [half Performance] allies; worth it for two or more.
            if 'T066' in p['known_ids'] and spare >= 2:
                k = p['skill_totals']['Performance'] // 2
                who = sorted((q for q in pcs if restorable(q, False) > 0), key=lambda q: -restorable(q, False))[:k]
                if len(who) >= 2:
                    _take(p, 2)
                    got = sum(heal(q, 1) for q in who)
                    healed += got
                    log.append(f"{p['name']}: Bolstering Refrain, {got}")
                    continue
            # Second Wind (T012): a card, 1 Shallow (2 on a Heart), yourself.
            if 'T012' in p['known_ids'] and spare >= 1 and p['shallow_lost'] > 0:
                got = heal(p, 1 + _take(p, 1))
                healed += got
                log.append(f"{p['name']}: Second Wind, {got}")
        if healed == before:
            return healed


def patch_up(pcs, log):
    """Patch Up (T036), before bed: a card, and up to [half Medicine] of
    the most hurt heal an extra Health tonight."""
    for p in pcs:
        if p['health'] <= 0 or 'T036' not in p['known_ids'] or not p['hand']:
            continue
        k = p['skill_totals']['Medicine'] // 2
        who = sorted((q for q in pcs if q['max_health'] - q['health'] > 0 and not q.get('patched')),
                     key=lambda q: -(q['max_health'] - q['health']))[:k]
        if who:
            _discard(p, cards.lowest(p['hand']))
            for q in who:
                q['patched'] = 1
            log.append(f"{p['name']}: Patch Up on {', '.join(q['name'] for q in who)}")


def night(pcs, full):
    """A full night's rest: committed Health back, then Body plus any
    extra, Deep first."""
    for p, f in zip(pcs, full):
        back = f - p['max_health']
        p['max_health'] = f
        p['health'] += back
        p['nightly'] = p['stats']['Body'] + p.get('rest_bonus', 0)
        heal(p, p['nightly'] + p.pop('patched', 0), deep_ok=True, deep_first=True)


# ---- A day, and days in a row ----

def _maker(names, swaps, rows, full):
    last = []

    def make(tier, good_luck=0):
        last[:] = [party.make_pc(m, i, good_luck, rows=rows, edits=swaps[m][0] if m in swaps else None,
                                 row_changes=swaps[m][1] if m in swaps else None)
                   for i, m in enumerate(names, 1)]
        full[:] = [p['max_health'] for p in last]
        return last
    return make, last


def play_day(names, swaps, level, mixes, seed, rows, start=None, log=None):
    """One day: a fight in each of `mixes` (two), care after each, then
    the night. `start`: each PC's state this morning (None: full)."""
    log = [] if log is None else log
    full = []
    make, last = _maker(names, swaps, rows, full)
    cs.make_party = make
    carry = start
    rec = dict(fights=[], care=0, lost=0)
    for f, mix in enumerate(mixes, 1):
        r = cs.run_fight(1, level, movement=True, enemies=se.build_encounter(se.ENCOUNTERS[level][mix]),
                         seed=seed + 1_000_000 * f, carry=carry, day_fight=f)
        pcs = list(last)
        if T.TRACK_SHARES:
            # Per seat, summed over the day (party_power.py's scorecard).
            slots = rec.setdefault('slots', [dict(dmg_out=0, heal_out=0, dmg_in=0, hits_in=0, downed=0) for _ in pcs])
            for sl, p in zip(slots, pcs):
                for k in ('dmg_out', 'heal_out', 'dmg_in', 'hits_in'):
                    sl[k] += p.get(k, 0)
                sl['downed'] += bool(p.get('was_downed'))
        if f == 1:
            # The day's first fight, fresh: how one-sided it was
            # (party_power.py's flags).
            rec['first'] = dict(won=r['winner'] == 'party', rounds=r['rounds'],
                                wounded=any(p.get('was_wounded') for p in pcs))
        if r['winner'] != 'party':
            rec['lost'] = f
            rec['morning'] = 0
            rec['short'] = {p['name']: f0 for p, f0 in zip(pcs, full)}
            rec['full'] = sum(full)
            return rec, None
        for p in pcs:
            _settle(p)
        rec['fights'].append(sum(p['health'] for p in pcs))
        final = f == len(mixes)
        if CARE:
            rec['care'] += care(pcs, (lambda p: 0) if final else
                                (lambda p: math.ceil(p['hand_size'] * T.CARDS_FIGHT_SHARE)), log)
            if final:
                patch_up(pcs, log)
        carry = [dict({k: p[k] for k in CARRY_KEYS}, deck=p.get('deck'), hand=p.get('hand')) for p in pcs]
    night(pcs, full)
    rec['morning'] = sum(p['health'] for p in pcs)
    rec['full'] = sum(full)
    rec['short'] = {p['name']: p['max_health'] - p['health'] for p in pcs}
    rec['nights'] = max((math.ceil((p['max_health'] - p['health']) / max(1, p['nightly'])) for p in pcs), default=0)
    morning = [{k: p[k] for k in CARRY_KEYS} for p in pcs]
    return rec, morning


def day_mixes(mi, k):
    """The first fight is mix `mi`; the second cycles through the other
    three, so every ordered pair comes up equally."""
    m = se.CURRENT_MIXES
    return (m[mi], m[(mi + 1 + k % (len(m) - 1)) % len(m)])


def set_mult(m):
    global MULT
    MULT = T.ENEMY_HEALTH_MULT = m


def _job(args):
    names, swaps, level, mi, ks, days, seed, mult, care_on = args
    global CARE
    T.ENEMY_HEALTH_MULT, CARE = mult, care_on
    rows = party._rows()
    out = []
    for k in ks:
        if days:
            start, won = None, 0
            for d in range(days):
                rec, start = play_day(names, swaps, level, day_mixes((mi + d) % 4, k + d), seed + 100_000 * mi + k
                                      + 10_000_000 * d, rows, start)
                if rec['lost']:
                    break
                won += 1
            out.append(dict(days=won))
        else:
            rec, _ = play_day(names, swaps, level, day_mixes(mi, k), seed + 100_000 * mi + k, rows)
            out.append(rec)
    return out


def run(names, swaps, level, n, days=0, seed=0, pool=None):
    jobs = [(names, swaps, level, mi, range(c, min(n, c + 25)), days, seed, MULT, CARE)
            for mi in range(len(se.CURRENT_MIXES)) for c in range(0, n, 25)]
    res = (pool.map if pool else map)(_job, jobs)
    return [r for chunk in res for r in chunk]


# ---- Reading a run ----

def summary(recs):
    n = len(recs)
    won = [r for r in recs if not r['lost']]
    out = dict(days=n, won=100 * len(won) / n,
               lost_first=100 * sum(r['lost'] == 1 for r in recs) / n,
               lost_second=100 * sum(r['lost'] == 2 for r in recs) / n,
               morning=st.mean(r['morning'] for r in recs),
               full=st.mean(r['full'] for r in recs))
    if won:
        out.update(after_first=st.mean(r['fights'][0] for r in won), after_second=st.mean(r['fights'][1] for r in won),
                   care=st.mean(r['care'] for r in won), morning_won=st.mean(r['morning'] for r in won),
                   nights=st.mean(r['nights'] for r in won),
                   short={k: st.mean(r['short'][k] for r in won) for k in won[0]['short']})
    return out


def swap_arg(text, level):
    """'Hilde (L3)=path.json' or 'path.json:0' (an optimizer run's entry)."""
    import build_optimizer as bo  # it imports this module
    name, _, spec = text.partition("=")
    path, _, idx = spec.partition(":")
    data = json.load(open(spec if os.path.exists(spec) else path))
    build = data[int(idx or 0)]["build"] if isinstance(data, list) else data
    row = bo.choices_for(party._rows()[name], build)
    return name, ({"build": build}, row)


def main():
    import build_optimizer as bo  # it imports this module
    ap = argparse.ArgumentParser()
    ap.add_argument("-L", type=int, default=3)
    ap.add_argument("-p", default="H", help="party: S, U or H (build_optimizer.PARTIES)")
    ap.add_argument("--swap", action="append", default=[], help="'Name=build.json' or 'Name=run.json:index'")
    ap.add_argument("-n", type=int, default=100, help="days per first-fight mix")
    ap.add_argument("--days", type=int, default=0, help="play days in a row, up to this many, until a fight is lost")
    ap.add_argument("-m", type=float, default=MULT, help="enemy Health multiplier")
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    set_mult(a.m)
    names = bo.PARTIES[a.L][a.p]
    swaps = dict(swap_arg(s, a.L) for s in a.swap)
    with mp.Pool(a.j) as pool:
        base = run(names, {}, a.L, a.n, a.days, pool=pool)
        var = run(names, swaps, a.L, a.n, a.days, pool=pool) if swaps else None
    for label, recs in (("as built", base), ("with swaps", var)):
        if recs is None:
            continue
        if a.days:
            d = [r['days'] for r in recs]
            print(f"{label}: days won in a row (up to {a.days}) {st.mean(d):.2f}; "
                  f"all {a.days}: {100 * sum(x == a.days for x in d) / len(d):.0f}%")
            continue
        s = summary(recs)
        print(f"{label}: {s['won']:.1f}% of days won (lost in fight 1 {s['lost_first']:.1f}%, fight 2 "
              f"{s['lost_second']:.1f}%); morning Health {s['morning']:.2f} of {s['full']:.0f}")
        if 'short' in s:
            print(f"  won days: Health after fight 1 {s['after_first']:.2f}, after fight 2 {s['after_second']:.2f}, "
                  f"care +{s['care']:.2f}, morning {s['morning_won']:.2f}, more nights to full {s['nights']:.2f}")
            print("  still missing in the morning: " + ", ".join(f"{k} {v:.2f}" for k, v in s['short'].items()))
    if var is not None and not a.days:
        d = [v['morning'] - b['morning'] for b, v in zip(base, var)]
        print(f"morning Health, swaps less as built: {st.mean(d):+.2f} +/- {1.96 * st.stdev(d) / math.sqrt(len(d)):.2f}")


if __name__ == "__main__":
    main()
