"""Helpers the Technique files share (2026-10-27): techniques.py,
techniques_more_a.py and techniques_more_b.py all reach for these,
rather than each keeping its own. combat_sim is `tq.cs` at fight time.

- Interrupt AP (`_interrupt_ap`): every PC's AP pool, `ap_bank`.
  rulebook.md gives AP at the start of the fight and again at the end
  of each of your turns, so it's there for Interrupts until your next
  turn, which spends what's left (combat_sim._take_pc_turn).
- Cards: with real cards (tunables.CARDS) a cost is the lowest card in
  hand, out of the fight's budget (cards.spend); with CARDS off it comes
  out of `card_uses_left` and a suit the cost wants is assumed (the
  cards.chosen_matches convention).
- Healing goes through tactics.necrotic_cut, like every other heal.
- `_resolve`/`_log_strike`: an attack resolved off the attack loop (a
  cone, a burst, an Interrupt), and its log line.
- Reach: `_near(a, b, ...)` is True when movement is off (everything's
  in reach); `_within(pc, units, reach, movement_on)` is empty then (an
  aura doesn't reach anyone without positions).
"""
from types import SimpleNamespace

import techniques as tq


def interrupt_ap_left(pc):
    """AP this PC has for an Interrupt right now: its pool."""
    return pc.get('ap_bank', 0)


def _interrupt_ap(pc, n):
    """Pays `n` AP for an Interrupt from the pool, or returns False if
    it won't cover it."""
    if interrupt_ap_left(pc) < n:
        return False
    pc['ap_bank'] -= n
    return True


def _can_pay(pc, k=1):
    if tq.cs.T.CARDS:
        return tq.cs.cards.can_spend(pc, k)
    return pc.get('card_uses_left', 0) >= k


def _pay_card(pc, suit=None):
    """Discards one card for a cost, the lowest of `suit` if held. Returns
    the suit discarded (None if it couldn't pay); with CARDS off, the suit
    asked for is assumed."""
    cs = tq.cs
    if cs.T.CARDS:
        if not cs.cards.can_spend(pc):
            return None
        c = cs.cards.lowest(pc['hand'], prefer_suit=suit)
        cs.cards.spend(pc, c)
        return cs.cards.suit(c)
    if pc.get('card_uses_left', 0) <= 0:
        return None
    pc['card_uses_left'] -= 1
    return suit if suit is not None else -1


def _heal(p, n):
    n = tq.cs.tactics.necrotic_cut(p, n)
    n = max(0, min(n, p['max_health'] - p['health']))
    p['health'] += n
    return n


def _near(a, b, movement_on, reach=None):
    cs = tq.cs
    if not movement_on or 'pos' not in a or 'pos' not in b:
        return True
    return cs._distance(a['pos'], b['pos']) <= (cs.T.MELEE_RANGE if reach is None else reach)


def _missing(p):
    return p['max_health'] - p['health']


def _ctx_log():
    """A party log for a hook point whose ctx has none (pc_parried,
    pc_hit): the round's trace, if the fight is being traced."""
    cs = tq.cs
    trace = cs._CTX.get('trace')
    if trace is None:
        return None
    rnd = cs._CTX['rnd']
    return lambda **kw: cs._log(trace, round=rnd, side='party', **kw)


def _extra_successes(pool, skill):
    """Extra Successes a no-damage hit gets from its suit pool: one per
    card of the attack Skill's suit. The attack's Gambles aren't at the
    hook points, and a no-damage attack doesn't Gamble anyway (its EV
    search sees no damage to gain)."""
    cs = tq.cs
    if not cs.T.CARDS:
        return 0
    return pool.count(cs.cards.SKILL_SUIT[skill])


def _is_unarmed_weapon(pc, sub):
    # "Your Unarmed weapon attacks": the PC's own Unarmed attack, or a
    # Technique strike that makes one (Boughs Unbroken reads it the same way).
    return pc.get('weapon_name') == 'Unarmed' and (not sub or sub.get('weapon'))


def _is_weapon_attack(pc, sub):
    # War Magic is a Spell attack even when it's the row's Weapon.
    return (sub.get('weapon') if sub else not pc.get('weapon_is_spell'))


def _is_ranged_weapon(pc, sub):
    return bool(pc.get('attack_range')) and _is_weapon_attack(pc, sub)


def _resolve(pc, e, pcs, *, skill_total, opp_def, damage, dmg_type, skill, weapon=False, good=0):
    """One attack this file resolves itself, off the attack loop (a cone,
    a burst, an Interrupt): the flip, Harried on a Dodge or Parry, and on
    a hit the damage less Resist and Protected. Only a weapon attack
    Gambles (rulebook.md: spell attacks can't). Returns what happened;
    the caller puts on its riders, then logs it (_log_strike)."""
    cs = tq.cs
    prof = dict(opp_def=opp_def, dmg_type=dmg_type)
    defense = cs.enemy_defense_for_pc_attack(prof, e)
    resist = cs.enemy_resist_for_pc_attack(prof, e)
    mod = skill_total - pc.get('crippled', 0)
    good = pc.get('good_luck', 0) + good + cs._raise_spirits(pc, pcs, defense - mod, True)
    bad = cs._pc_status_bad_luck(pc, e)
    cover = cs._cover_bad_luck(pc, e, opp_def)
    if cover:
        bad = int(bad) + cover
    gambles, imp = 0, cs.BIG
    if weapon and damage > 0 and cs.T.CARDS:
        saved = pc['damage']
        pc['damage'] = damage  # _choose_gambles reads the attack's damage off the PC
        gambles, backed = cs._choose_gambles(pc, e, mod, defense, resist, good)
        pc['damage'] = saved
        if backed:
            imp = cs.PLANNED
    if imp != cs.PLANNED:
        imp = cs._importance(e, damage + gambles - resist - e.get('protected', 0), True)
    value, pool = cs._pc_flip(pc, mod - 2 * gambles, defense, good, bad, imp, pcs, cs._hand_of_chaos(pc))
    roll = mod - 2 * gambles + value
    hit = roll >= defense
    if opp_def in ('Parry/Dodge', 'Dodge'):
        e['harried'] = e.get('harried', 0) + 1
    raw = dmg = absorbed = 0
    if hit and damage > 0:
        raw = damage + gambles + cs._suit_extra(pc, pool, skill)
        dmg, absorbed = cs._land_damage(pc, e, raw, resist)
    return SimpleNamespace(hit=hit, dmg=dmg, raw=raw, resist=resist, absorbed=absorbed, pool=pool, roll=roll,
                           defense=defense, opp_def=opp_def, gambles=gambles)


def _log_strike(log, pc, e, r, via, notes=()):
    cs = tq.cs
    if log:
        log(unit=pc['name'], action='attack', target=e['name'], roll=r.roll, defense=r.defense, hit=r.hit,
            dmg=r.dmg, raw_dmg=r.raw, resist=r.resist, protected_absorbed=r.absorbed, target_hp_after=e['health'],
            target_harried_after=e.get('harried', 0), via=via, effects='; '.join(notes) or None,
            cards=cs._take_notes(pc), opp_def=r.opp_def, gambles=r.gambles)
    pc.pop('_notes', None)


def _push_from(pc, e, origin, n, pcs, log, notes, via):
    """A Push straight away from `origin`, with Parting Shot's "would be
    Pushed outside your range" check, as techniques._push_away_from_party."""
    cs = tq.cs
    start = cs._push(e, origin, n)
    notes.append(f"Pushed {cs._distance(start, e['pos'])} m")
    cs._after_push(e, start, pcs, log, f"Pushed by {via}")


def _within(pc, units, reach, movement_on):
    cs = tq.cs
    if not movement_on:
        return []
    return [u for u in units if u is not pc and u['health'] > 0 and cs._distance(pc['pos'], u['pos']) <= reach]
