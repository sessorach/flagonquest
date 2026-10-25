"""
The enemy Ability catalog in the fight (ENEMY_ENCOUNTER_DESIGN.md, "The
Ability catalog"): each Ability's hooks (hooks.py) and the functions they
call. What an Ability changes at build time (Resist by element, Enhanced
Range, Devastating's +1 Damage...) is enemy_builder_pcstyle._apply_catalog;
what it costs is enemy_builder_pcstyle.PICK_COST. Adding an Ability means
its cost there, and its build-time numbers or its hooks here.

`cs` is combat_sim, set when it finishes loading.
"""
import hooks

cs = None


STRIKE_RIDERS = {
    # 2026-10-01 draft: riders measured at well under one pick's worth
    # (~1 Health) get 2 stacks instead of a fractional cost.
    'Strike (Crippling)': ('Crippled', 1),
    'Strike (Vulnerable)': ('Vulnerable', 2),
    'Poison (Bleeding)': ('Bleeding', 2),
    'Strike (Slowing)': ('Slowed', 2),
    'Strike (Frightening)': ('Frightened', 1),
    'Strike (Taunting)': ('Taunted', 2),
    # The rest of the catalog's riders (2026-10-25), at its own stacks:
    # "2 for Bleeding/Necrotic, 1 for the others".
    'Strike (Necrotic)': ('Necrotic', 2),
    'Poison (Crippling)': ('Crippled', 1),
    'Poison (Necrotic)': ('Necrotic', 2),
    'Poison (Slowing)': ('Slowed', 1),
    'Poison (Vulnerable)': ('Vulnerable', 1),
}


def _melee_profile(e):
    """An enemy's melee attack (its main Action, else its backup), or None."""
    if e.get('kind', 'attack') == 'attack' and not e.get('attack_range'):
        return dict(action=e['action'], accuracy=e['accuracy'], attack_damage=e['attack_damage'],
                    dmg_type=e.get('dmg_type'), opp_def=e['opp_def'], attack_range=0)
    b = e.get('backup')
    if b and not b.get('attack_range') and b.get('attack_damage'):
        return b
    return None


# ---- Hooks (hooks.py) ----

@hooks.on('enemy_turn_start', 'Resilient', order=10)
def _resilient(e, c):
    # "Turn start -> remove 1 of each debuff."
    for key in ('crippled', 'slowed', 'vulnerable', 'necrotic', 'bleeding', 'frightened', 'taunted'):
        if e.get(key, 0) > 0:
            e[key] -= 1
            if e[key] == 0 and key in ('frightened', 'taunted'):
                e[key + '_by'] = None


def _zero_ap_action(e, c, ability, key):
    """Action (Intimidating) / (Taunting): 0 AP, once a turn, Range x2, no
    roll. Intimidating Frightens the nearest PC (the one likeliest to
    attack it); Taunting Taunts the hardest hitter not already Taunted by
    it."""
    reach = 2 * e.get('level', 1) + 2
    pool = [p for p in c.pcs if p['health'] > 0
            and (not c.movement_on or cs._distance(e['pos'], p['pos']) <= reach)
            and not (p.get(key.lower(), 0) > 0 and p.get(key.lower() + '_by') is e)]
    if not pool:
        return
    if key == 'Frightened':
        tg = min(pool, key=lambda p: (cs._distance(e['pos'], p['pos']) if c.movement_on else 0, -p['damage']))
    else:
        tg = max(pool, key=lambda p: p['damage'])
    cs._apply_to_pc(tg, key, 1, e)
    if c.log:
        c.log(unit=e['name'], action='technique', target=tg['name'], via=ability, effects=f"{key} +1")


@hooks.on('enemy_turn_start', 'Action (Intimidating)', order=20)
def _intimidating(e, c):
    _zero_ap_action(e, c, 'Action (Intimidating)', 'Frightened')


@hooks.on('enemy_turn_start', 'Action (Taunting)', order=30)
def _taunting(e, c):
    _zero_ap_action(e, c, 'Action (Taunting)', 'Taunted')


@hooks.on('enemy_hit_damage', 'Strike (Devastating)')
def _devastating(e, c):
    # "attacks deal their damage as Bleeding instead of direct Health
    # loss" (its +1 Damage is in the build).
    if c.dmg > 0:
        cs._apply_to_pc(c.target, 'Bleeding', c.dmg, e)
        c.applied.append(f"Bleeding +{c.dmg} (Devastating)")
        c.dmg = 0


def _rider(ability):
    effect, stacks = STRIKE_RIDERS[ability]

    def apply(e, c):
        cs._apply_to_pc(c.target, effect, stacks, e)
        c.applied.append(f"{effect} +{stacks}")
    hooks.on('enemy_hit_riders', ability, order=10)(apply)


for _ability in STRIKE_RIDERS:
    _rider(_ability)


@hooks.on('enemy_hit_riders', 'Strike (Grappling)', order=20)
def _grappling(e, c):
    # "Attack hits -> target is now grappled."
    t = c.target
    if e.get('grapple') is None and t['health'] > 0 and t.get('grapple') is None:
        e['grapple'], t['grapple'] = t, e
        c.applied.append("grappled")


@hooks.on('enemy_hit_or_parried', 'Strike (Harrying)', order=10)
def _harrying(e, c):
    # "Attack hits *or* is Parried -> target Harried once either way."
    c.target['harried'] = c.target.get('harried', 0) + 1
    c.applied.append("Harried +1")


@hooks.on('enemy_hit_or_parried', 'Strike (Battering)', order=20)
def _battering(e, c):
    # "Attack is Parried -> target still gains a Bleeding stack."
    if c.parried:
        cs._apply_to_pc(c.target, 'Bleeding', 1, e)
        c.applied.append("Bleeding +1 (Battering)")


@hooks.on('pc_damaged_enemy', 'Retribution Aura')
def _retribution(e, c):
    # "Attacker who damages this NPC gains a stack of Bleeding themselves."
    if c.pc['health'] > 0:
        cs._gain(c.pc, 'bleeding', 1)
        c.pc['retribution_taken'] = c.pc.get('retribution_taken', 0) + 1


@hooks.on('pc_left_reach', 'Action (Parting Shot)')
def _enemy_parting_shot(e, c):
    """"Enemy moves out of melee -> free attack against them", with its
    melee attack, once a round. Called after each of a PC's ordinary
    moves (not a Shift or Teleport); the attack resolves with the PC back
    where it started."""
    pc, start, rnd = c.pc, c.start, c.rnd
    if e.get('ps_round') == rnd or 'pos' not in e:
        return
    if cs._distance(e['pos'], start) > cs.T.MELEE_RANGE or cs._distance(e['pos'], pc['pos']) <= cs.T.MELEE_RANGE:
        return
    prof = _melee_profile(e)
    if prof is None:
        return
    e['ps_round'] = rnd
    log = (lambda **kw: cs._log(cs._CTX['trace'], round=rnd, side='enemy', **kw)) if cs._CTX['trace'] is not None else None
    now, pc['pos'] = pc['pos'], start
    cs._enemy_attack(e, prof, pc, 'attack', rnd, c.pcs, c.enemies, True, log, None, via_suffix=' (Parting Shot)')
    pc['pos'] = now
