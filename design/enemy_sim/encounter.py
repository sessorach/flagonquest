"""Encounter uses (2026-10-27): every Encounter Technique use a PC has, in
one list.

glossary.md's [Encounter]: expended when used, regained when the
encounter ends. Each Technique copy's use carries the copy's Level from
the export, and its kinds (Martial, Discipline, Spell) from
techniques.csv's Tags, so anything that regains or trades uses by Level
(Vigor, Willow Springs Back, Placeholder's Alacritous Adaptation,
Warmage's Reserves) works on every Encounter Technique, present and
future, with nothing written for each one.

A *group* is a dict with:
- `uses`: left this fight; `max`: what the fight started with;
- `tech`: the Technique's name; `level`; `kinds`: a frozenset of
  "Martial", "Discipline", "Spell" and the Spell's school ("Sorcery",
  "Theurgy", "General");
- `attack`: True for an attack the PC's attack loop uses up (a Technique
  attack, a hex, a Battle Maneuver copy, the War Magic Weapon).
Groups that carry a profile are the profile dicts the fight already
reads (`tech_attacks`, `hexes`, `blessings`, `maneuvers`,
`weapon_spell`), so `g['uses']` there works as it always did. A
Technique with nothing else to carry (Brace, Gainsay, Skin of Stone...)
gets a plain group, made for every name in the sheet's
`encounter_techs`: an `_encounter()` Technique needs only `left()` and
`spend()` by name, no setup.
"""
import game_data

KINDS = frozenset(("Martial", "Discipline", "Spell"))


def _tags(tech):
    # By the sim's own name for it (techniques.py may shorten the CSV's,
    # "Hand Rings the Bell"), through its ID; else the CSV's name.
    import techniques
    tid = techniques.ID_BY_NAME.get(tech)
    return game_data.tags_of(tid) if tid else game_data.technique_tags(tech)


def kinds_of(tech):
    # "Sorcery Spell" is a Spell and a Sorcery one.
    out = set()
    for tag in _tags(tech):
        words = tag.split()
        if words and words[-1] in KINDS:
            out.add(words[-1])
            out.update(words[:-1])
    return frozenset(out)


def group(tech, level, uses, attack=False, **extra):
    g = dict(extra)
    g.update(tech=tech, level=level, uses=uses, max=uses, kinds=kinds_of(tech), attack=attack)
    return g


def attach(pc, groups):
    """Indexes `groups` on the fight dict: `encounter` is every group in
    the order the sheet lists them, `_enc` the same by Technique name."""
    pc['encounter'] = list(groups)
    by = {}
    for g in pc['encounter']:
        by.setdefault(g['tech'], []).append(g)
    pc['_enc'] = by


def groups_of(pc, tech):
    return pc.get('_enc', {}).get(tech, ())


def left(pc, tech):
    return sum(g['uses'] for g in groups_of(pc, tech))


def spend(pc, tech):
    """Expends one use of `tech` (its first group with one left). Returns
    whether there was one."""
    for g in groups_of(pc, tech):
        if g['uses'] > 0:
            g['uses'] -= 1
            return True
    return False


def weapon_left(pc):
    """Casts left of a War Magic Weapon (party.py's `weapon_spell`), or
    None for a Weapon that isn't an Encounter Technique (always there)."""
    g = pc.get('weapon_spell')
    return None if g is None else g['uses']


# ---- Regaining uses ----
# Which spent use a PC wants back is one rule for everything: its
# attacks first (the uses its turn is built around), then the higher
# Level, then the harder hitter; among the rest, the higher Level.

def value(g):
    return (g['attack'], g['level'], g.get('damage', 0))


def spent(pc, kinds=None):
    return [g for g in pc.get('encounter', ()) if g['uses'] < g['max'] and (kinds is None or g['kinds'] & kinds)]


def wanted(pc, max_level=None, kinds=None):
    """The spent group this PC most wants back, of Level `max_level` or
    less, or None."""
    pool = [g for g in spent(pc, kinds) if max_level is None or g['level'] <= max_level]
    return max(pool, key=value) if pool else None


def worth_regaining(pc, g):
    """Whether getting `g` back beats what's still in hand: it outranks
    (value) every attack use left. A use the PC holds but never picks
    (Felix's Firefly Leaves the Hand, worse than his punch) doesn't stop
    a better spent one coming back, and once the attacks are all spent
    anything is worth it."""
    best = max((value(h) for h in pc.get('encounter', ()) if h['attack'] and h['uses'] > 0), default=None)
    return best is None or value(g) > best


def regain(pc, g, via, log=None):
    g['uses'] += 1
    # A Battle Maneuver copy back in hand goes back in line (the attack
    # loop reads pc['maneuver'], the copy in use).
    m = pc.get('maneuver')
    if g['tech'] == 'Battle Maneuver' and (m is None or m['uses'] <= 0):
        pc['maneuver'] = g
    if log:
        log(unit=pc['name'], action='technique', via=via, note=f"regained a use of {g.get('via', g['tech'])} "
                                                            f"(Level {g['level']})")


# ---- The ways to regain a use, each one rule for every Technique ----

def spend_vigor(pc, log=None):
    """glossary.md, Vigor: "You may spend Vigor equal to an expended
    Encounter Technique's Level to regain a use of it." On the best spent
    use the Vigor left covers, whenever it's worth_regaining, as many
    times as it covers."""
    regained = 0
    while pc.get('vigor', 0) > 0:
        g = wanted(pc, max_level=pc['vigor'])
        if g is None or not worth_regaining(pc, g):
            break
        pc['vigor'] -= g['level']
        regain(pc, g, 'Vigor', log)
        regained += 1
    return regained


def trade_for(pc, target_kinds, rnd, log=None, via=None):
    """Expend unspent uses to regain a better spent one, the cost being
    more total Level than the regained use's (Placeholder's Alacritous
    Adaptation). Only uses the PC hasn't touched by round 3 are traded
    away, and only for a spent attack: what wasn't needed by then is worth
    less than the offense that's run out. Returns whether it traded."""
    if rnd < 3:
        return False
    w = wanted(pc, kinds=target_kinds)
    if w is None or not w['attack'] or not worth_regaining(pc, w):
        return False
    donors = sorted((g for g in pc.get('encounter', ()) if g is not w and not g['attack'] and g['kinds'] & target_kinds
                     and g['uses'] == g['max'] > 0), key=lambda g: g['level'])
    paid, total = [], 0
    for g in donors:
        for _ in range(g['uses']):
            if total > w['level']:
                break
            paid.append(g)
            total += g['level']
    if total <= w['level']:
        return False
    for g in paid:
        g['uses'] -= 1
    regain(pc, w, via, log)
    return True
