"""The rest of the Technique catalog, part B (2026-10-27): T100-T205.

Each Technique here is modeled (registered the same way as in
techniques.py), listed in techniques.OUT_OF_COMBAT, or listed in
techniques.DEFERRED with what it would need. combat_sim is `tq.cs` at
fight time (techniques.py's `cs`), not at import.

Most of what's modeled is one of four shapes:
- a Technique attack swapped in for a normal one (`_strike`, the same
  as techniques._tech_attack, plus the name in `passives` so its own
  hooks below can find it): the Martial and Discipline single-target
  strikes and Spectral Spiderwebs;
- an Encounter Technique cast at the start of the turn (`_encounter`):
  the cones and bursts, the Cloaks, Land's Bounty, Chainbreaker and
  Swallow Skims the Water, each resolved with `_resolve` below;
- an Interrupt off someone's attack (`_irq_*` for the AP);
- a Style (`_passive`) read at a hook point.
"""
from types import SimpleNamespace

import techniques as tq
from techniques import technique, hooks, setup_for, OUT_OF_COMBAT, DEFERRED, BuildError  # noqa: F401

# ---- Out of combat ----

OUT_OF_COMBAT.update({
    "T102": "Telepathic Link",
    "T143": "Street Runner",
})

# ---- Deferred: matters in a fight, needs something the sim doesn't have ----

DEFERRED.update({
    "T100": "a rule for picking one of its eight options (the Spell use it spends, and that use's Level, are "
            "encounter.py's)",
    "T101": "summoned creatures",
    "T103": "summoned creatures",
    "T106": "bringing a Downed PC back (the sim never revives one)",
    "T108": "Poison and Potency rules (in neither the glossary nor the sim)",
    "T112": "barricades that block movement as well as giving Cover",
    "T114": "summoned creatures",
    "T115": "weather that gives everyone Cover, starting three rounds after the cast",
    "T118": "a lasting area that hits whoever enters or ends a turn in it (no enemy turn-end hook point)",
    "T119": "casting another known Theurgy Spell as a 0 AP Interrupt",
    "T125": "summoned creatures",
    "T126": "walls with their own Health that block movement",
    "T127": "a damaging wall that hits whoever enters or ends a turn in it",
    "T136": "a second wielded weapon (the sim gives a PC one)",
    "T148": "an Interrupt that turns an enemy's attack into a Parry (attack_declared can't stop the attack)",
    "T166": "an Interrupt that swaps the Defense an enemy spell attack checks, and two Ward types at once",
    "T168": "an Interrupt that takes the PC out of an enemy's attack (attack_declared can't cancel it)",
    "T170": "ignoring Wounded's penalties (tactics.pc_wounded is read everywhere) and Vigor",
    "T178": "a hook that moves an enemy's attack onto another PC's Parry Defense",
    "T179": "an enemy-move hook that fires without Parting Shot in the fight",
    "T181": "Good Luck on enemies' attacks against the PC (there's no enemy-side Good Luck field)",
    "T183": "a rule for where a free 1-meter Shift per attack should go",
    "T186": "Difficult Terrain for enemies only (movement.TERRAIN is one map for everyone)",
    "T188": "the attack's Gamble count at a hook, and a way to drop its Extra Successes",
    "T191": "a Sift 2 from a fortune told earlier that day (the sim has no day before the fight)",
    "T201": "summoned creatures",
})


# ---- Shared pieces ----

def _st(stats, skills, skill):
    return tq._st(stats, skills, skill)


def _med(stats, skills):
    return _st(stats, skills, "Meditation")


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
        dmg = max(0, raw - resist)
        if e.get('protected', 0) > 0 and dmg > 0:
            absorbed = min(dmg, e['protected'])
            e['protected'] -= absorbed
            dmg -= absorbed
        e['health'] -= dmg
        cs._damaged_by_pc(pc, e, dmg)
        if dmg > 0:
            e.setdefault('hit_steps', []).append((cs._STEP[0], e['health'] <= 0))
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
    cs._log(cs._CTX['trace'], round=cs._CTX['rnd'], side='enemy', unit=e['name'], action='move', pos=e['pos'],
            spaces=cs._distance(start, e['pos']), in_range=False, via=f"Pushed by {via}")
    if cs._CTX.get('ps_pcs'):
        cs._parting_shots_on(e, start, pcs, log, pushed=True)


# ---- Interrupt AP off the PC's own turn ----
# One pool for both files' Interrupts: techniques_more_a's (its docstring
# says how it works), so a PC with Interrupts from each can't spend two
# turns' worth.
from techniques_more_a import interrupt_ap_left as _irq_ap, _interrupt_ap as _irq_spend  # noqa: E402


# ---- Builders ----

def _strike(tid, name, factory, unarmed=True):
    """A Technique attack (techniques._tech_attack), with its name also
    in `passives` so this file's hooks for it run. An Unarmed strike is
    built from the row's Weapon, so the row has to be swinging Unarmed."""
    def build(sheet, copies, choices):
        if unarmed and sheet.weapon != "Unarmed":
            raise BuildError(f"{name} is an Unarmed weapon attack; the sim builds it from the row's Weapon, "
                             f"which is {sheet.weapon or '1H Heavy Melee'}")
        sheet.tech_attacks.append((name, factory, len(copies)))
        sheet.passives.append(name)
    technique(tid, name)(build)


def _unarmed(atk, dmg, **kw):
    prof = dict(skill_total=atk, damage=dmg, dmg_type="Physical", opp_def="Parry/Dodge", effect=None,
                skill="Brawl", weapon=True)
    prof.update(kw)
    return prof


def _encounter(tid, name, unarmed=False):
    """An Encounter Technique this file casts itself: one use per copy."""
    def build(sheet, copies, choices):
        if unarmed and sheet.weapon != "Unarmed":
            raise BuildError(f"{name} makes an Unarmed weapon attack; the row's Weapon is "
                             f"{sheet.weapon or '1H Heavy Melee'}")
        sheet.encounter_techs.extend([name] * len(copies))
    technique(tid, name)(build)
    tq.ENCOUNTER_NAMES.add(name)


# ======================================================================
# Theurgy Spells
# ======================================================================

# T113, Level 2, 1 AP, Encounter, "Up to X + 1 creatures within [Theurgy
# Skill Total] meters": "Make a Theurgy spell attack against each
# target's Dodge Defense. If the attack hits, the target is Slowed 4 +
# [Spades] times." Taken with X = 0 (no cards discarded): one target.
_strike("T113", "Spectral Spiderwebs", lambda st, sk, atk, dmg: dict(
    skill_total=_st(st, sk, "Theurgy"), damage=0, dmg_type="Physical", opp_def="Dodge",
    effect=("slowed", 4, "Spades"), skill="Theurgy", range=_st(st, sk, "Theurgy"), ap=1), unarmed=False)


_encounter("T109", "Land's Bounty")


@hooks.on('pc_turn_start', "Land's Bounty", order=82)
def _lands_bounty(pc, c):
    """Land's Bounty (T109, 2 AP, Encounter, "Burst 2, centered on a space
    within [Theurgy Skill Total] meters"): "affected terrain has up to
    [Mind] levels of Difficult Terrain" (movement.TERRAIN, as Glacier).
    Cast in front of two or more melee enemies still walking in, where no
    ally is standing or about to be."""
    cs = tq.cs
    name = "Land's Bounty"
    if tq.encounter.left(pc, name) <= 0 or not c.movement_on or c.ap < 2:
        return 0
    allies = [p for p in c.pcs if p['health'] > 0]
    coming = [e for e in c.enemies if e['health'] > 0 and (e.get('attack_range') or 0) <= cs.T.MELEE_RANGE
              and all(cs._distance(e['pos'], p['pos']) > cs.T.MELEE_RANGE for p in allies)]
    if len(coming) < 2:
        return 0
    center = (round(sum(e['pos'][0] for e in coming) / len(coming)),
              round(sum(e['pos'][1] for e in coming) / len(coming)))
    reach = pc['skill_totals']["Theurgy"] + pc['ley']
    if cs._distance(pc['pos'], center) > reach:
        return 0
    caught = [e for e in coming if cs._distance(e['pos'], center) <= 2]
    if len(caught) < 2 or any(cs._distance(p['pos'], center) <= 3 for p in allies):
        return 0
    tq.encounter.spend(pc, name)
    n = pc['stats']['Mind']
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            cell = cs._movement.clamp((center[0] + dx, center[1] + dy))
            cs._movement.TERRAIN[cell] = cs._movement.TERRAIN.get(cell, 0) + n
    if c.log:
        c.log(unit=pc['name'], action='technique', via=name,
              effects=f"Difficult Terrain +{n} in Burst 2 at {center}, {len(caught)} enemies in it")
    return 2


def _cloak(pc, c, name, kind):
    """Cloak of Awe / Cloak of Command (T116 / T117, 1 AP, Encounter,
    "Yourself or an ally within [Theurgy Skill Total] meters"): "Make a
    Theurgy spell attack against the Mental Defense of each enemy in
    Burst 3 of the target. The target Frightens [Taunts] each creature
    hit 3 + [Hearts] times." Command goes on the sturdiest ally with two
    or more enemies around them (it pulls their attacks there); Awe on
    whoever has the most enemies around them (their attacks on that ally
    get Bad Luck)."""
    cs = tq.cs
    if tq.encounter.left(pc, name) <= 0 or not c.movement_on or c.ap < 1:
        return 0
    reach = pc['skill_totals']["Theurgy"] + pc['ley']
    living = [e for e in c.enemies if e['health'] > 0]
    key = 'taunted_by' if kind == 'taunt' else 'frightened_by'
    best = None
    for p in c.pcs:
        if p['health'] <= 0 or cs._distance(pc['pos'], p['pos']) > reach:
            continue
        around = [e for e in living if cs._distance(e['pos'], p['pos']) <= 3 and e.get(key) is not p]
        if len(around) < 2:
            continue
        score = (p['max_health'], len(around)) if kind == 'taunt' else (len(around), -p['health'] / p['max_health'])
        if best is None or score > best[0]:
            best = (score, p, around)
    if best is None:
        return 0
    _, ally, around = best
    tq.encounter.spend(pc, name)
    for e in around:
        r = _resolve(pc, e, c.pcs, skill_total=pc['skill_totals']["Theurgy"], opp_def='Mental', damage=0,
                     dmg_type='Brilliant', skill='Theurgy')
        notes = []
        if r.hit:
            n = 3 + cs._suit_count(r.pool, 'Hearts')
            cs._test_rider(ally, e, kind, n)
            notes.append(f"{'Taunted' if kind == 'taunt' else 'Frightened'} by {ally['name']} +{n}")
        _log_strike(c.log, pc, e, r, name, notes)
    return 1


_encounter("T116", "Cloak of Awe")
_encounter("T117", "Cloak of Command")


@hooks.on('pc_turn_start', "Cloak of Command", order=34)
def _cloak_of_command(pc, c):
    return _cloak(pc, c, "Cloak of Command", 'taunt')


@hooks.on('pc_turn_start', "Cloak of Awe", order=35)
def _cloak_of_awe(pc, c):
    return _cloak(pc, c, "Cloak of Awe", 'fright')


# ======================================================================
# Styles and passives
# ======================================================================

for _tid, _name in (("T129", "Disciple of the Flowing Hand"), ("T134", "Lion School - Eternal Riposte"),
                    ("T135", "Shugen School - Spirit Hands"), ("T138", "Follow Through"),
                    ("T171", "Tiger School - Rending Claws"), ("T172", "Demon School - Hands of Defilement"),
                    ("T173", "Snake School - Infinite Coiling"), ("T174", "Bear School - Furious Swipes"),
                    ("T176", "Drunken Brawling"), ("T177", "Doubleshot"), ("T180", "Earthen Fist Posture"),
                    ("T182", "Earthen Mantle Approach"), ("T184", "Crashing Wave Approach"),
                    ("T185", "Deadeye's Shadow"), ("T187", "Aura of Death"), ("T195", "Forward!"),
                    ("T196", "Lead by Example"), ("T198", "Commander's Gambit"), ("T199", "Intimidating Presence"),
                    ("T200", "Dread Reputation"), ("T202", "Grasping Earth"), ("T203", "Twin Spell"),
                    ("T204", "Exploit the Opening"), ("T205", "Suppressing Fire")):
    tq._passive(_tid, _name)


@hooks.on('attack_declared', "Disciple of the Flowing Hand")
def _flowing_hand(pc, c):
    # T129: "Attacks against your Dodge or Parry Defense have Bad Luck."
    # The enemy's attack reads bad_luck_next right after this point.
    if c.prof.get('opp_def') in ('Parry/Dodge', 'Dodge'):
        c.attacker['bad_luck_next'] = c.attacker.get('bad_luck_next', 0) + 1
    return 0


@hooks.on('pc_parried', "Lion School - Eternal Riposte")
def _eternal_riposte(pc, c):
    """T134: "When you Parry an attack, you may make an Opportunity Attack
    against the attacker as a 0 AP Interrupt" - a weapon attack, so only
    while the attacker's in the Weapon's reach."""
    cs = tq.cs
    e = c.attacker
    if (pc['health'] <= 0 or e['health'] <= 0 or pc.get('weapon_is_spell')
            or ('pos' in pc and cs._distance(pc['pos'], e['pos']) > cs.effective_range(pc))):
        return
    pc['ripostes'] = pc.get('ripostes', 0) + 1
    cs._reaction_attack(pc, e, cs._CTX.get('pcs') or [pc], f"{pc['weapon_name']} (Eternal Riposte)", None,
                        _ctx_log())


def _unarmed_style(pc, dmg_type, opp_def):
    # The PC's own Unarmed attack takes the Style's damage type and
    # Defense. A Technique strike keeps the Defense its own text names.
    if pc.get('weapon_name') == 'Unarmed':
        pc['dmg_type'], pc['opp_def'] = dmg_type, opp_def


@setup_for("Shugen School - Spirit Hands")
def _spirit_hands_setup(name, pc, s):
    # T135: "Your Unarmed weapon attacks deal Brilliant damage and are made
    # against the target's Mental Defense."
    _unarmed_style(pc, 'Brilliant', 'Mental')


@setup_for("Demon School - Hands of Defilement")
def _defilement_setup(name, pc, s):
    # T172: "Your Unarmed weapon attacks deal Shadow damage and are made
    # against the target's Vital Defense."
    _unarmed_style(pc, 'Shadow', 'Vital')


@hooks.on('attack_luck', "Shugen School - Spirit Hands", order=36)
def _spirit_hands_luck(pc, c):
    # "If an attack would already do both, it has Good Luck instead": a
    # strike whose own text is Brilliant against Mental (Hand Rings the Bell).
    sub = c.substitute
    return 1 if sub and sub.get('weapon') and sub['dmg_type'] == 'Brilliant' and sub['opp_def'] == 'Mental' else 0


@hooks.on('hit_riders', "Demon School - Hands of Defilement", order=31)
def _defilement_bleed(pc, c):
    # "If an attack would already do both, the target gains Bleeding if it
    # hits": a strike whose own text is Shadow against Vital (Ripjaw Gambit).
    sub = c.substitute
    if c.hit and sub and sub.get('weapon') and sub['dmg_type'] == 'Shadow' and sub['opp_def'] == 'Vital':
        tq.cs._gain(c.target, 'bleeding', 1)
        c.notes.append("Bleeding +1 (Hands of Defilement)")


@setup_for("Follow Through")
def _follow_through_setup(name, pc, s):
    # The Weapon's own attack, for a Follow Through after a Technique strike
    # (the attack loop has the strike's numbers on the PC at that point).
    pc['base_prof_b'] = dict(skill_total=s.atk_skill_total, damage=s.damage, dmg_type=s.dmg_type,
                             opp_def=s.opp_def, skill=s.w_skill)


@hooks.on('after_hit', "Follow Through", order=55)
def _follow_through(pc, c):
    """T138: "When one of your melee weapon attacks Downs a creature, you
    may immediately make an attack with the same weapon against another
    creature adjacent to it." Free, at the weakest one in reach. It
    doesn't chain: the extra attack is a reaction attack, which doesn't
    run the hit hooks."""
    cs = tq.cs
    t, sub = c.target, c.substitute
    if t['health'] > 0 or pc.get('attack_range') or not _is_weapon_attack(pc, sub) or 'pos' not in t:
        return
    near = [e for e in c.enemies if e['health'] > 0 and e is not t
            and cs._distance(e['pos'], t['pos']) <= cs.T.MELEE_RANGE
            and cs._distance(pc['pos'], e['pos']) <= cs.effective_range(pc)]
    if not near:
        return
    e = min(near, key=lambda u: u['health'])
    pc['follow_throughs'] = pc.get('follow_throughs', 0) + 1
    cs._reaction_attack(pc, e, c.pcs, f"{pc['weapon_name']} (Follow Through)",
                        pc['base_prof_b'] if sub else None, c.log)


@hooks.on('hit_riders', "Tiger School - Rending Claws", order=32)
def _rending_claws(pc, c):
    # T171: "When one of your weapon attacks hits or is Parried, the target
    # gains 2 + [Diamonds] stacks of Harried."
    if _is_weapon_attack(pc, c.substitute):
        n = 2 + tq.cs._suit_count(c.pool, 'Diamonds')
        c.target['harried'] = c.target.get('harried', 0) + n
        c.notes.append(f"Harried +{n} (Rending Claws)")


@hooks.on('attack_declared', "Snake School - Infinite Coiling")
def _infinite_coiling(pc, c):
    # T173: "While you're grappling, the grapple doesn't give creatures
    # Good Luck on attacks against your Dodge or Parry Defense." The enemy's
    # attack adds that Good Luck on its own; one Bad Luck cancels it.
    if pc.get('grapple') is not None and c.prof.get('opp_def') in ('Parry/Dodge', 'Dodge'):
        c.attacker['bad_luck_next'] = c.attacker.get('bad_luck_next', 0) + 1
    return 0


def _may_push_1(pc, c, via):
    # "you may Push the target 1 meter": Kinetic's "up to" policy
    # (techniques.kinetic_helps), off a ranged ally or a target nobody's
    # fighting yet, not away from the party's own melee.
    t = c.target
    if t['health'] > 0 and 'pos' in t and 'pos' in pc and tq.kinetic_helps(t, c.pcs):
        _push_from(pc, t, pc['pos'], 1, c.pcs, c.log, c.notes, via)


@hooks.on('after_hit', "Bear School - Furious Swipes", order=61)
def _furious_swipes(pc, c):
    """T174: "When one of your Unarmed attacks hits, you may Push the
    target 1 meter, and it either gains Bleeding or is Slowed once."
    Slowed when it has to walk to reach the party afterwards, Bleeding
    when it's already in someone's face."""
    cs = tq.cs
    if not _is_unarmed_weapon(pc, c.substitute) or c.target['health'] <= 0:
        return
    _may_push_1(pc, c, "Furious Swipes")
    t = c.target
    engaged = 'pos' in t and any(p['health'] > 0 and cs._distance(p['pos'], t['pos']) <= cs.T.MELEE_RANGE
                                 for p in c.pcs)
    key = 'bleeding' if engaged else 'slowed'
    cs._gain(t, key, 1)
    c.notes.append(f"{key.capitalize()} +1 (Furious Swipes)")


@hooks.on('after_hit', "Earthen Fist Posture", order=62)
def _earthen_fist(pc, c):
    # T180: "When one of your weapon attacks hits, you may Push the target
    # 1 meter."
    if _is_weapon_attack(pc, c.substitute):
        _may_push_1(pc, c, "Earthen Fist Posture")


@hooks.on('after_hit', "Crashing Wave Approach", order=63)
def _crashing_wave(pc, c):
    # T184: "When one of your melee weapon attacks hits, you may Push the
    # target 1 meter, and you gain Protected." The Protected doesn't wait
    # on the Push (read as two effects of the hit).
    if _is_weapon_attack(pc, c.substitute) and not pc.get('attack_range'):
        _may_push_1(pc, c, "Crashing Wave Approach")
        if not getattr(c, 'repeat', False):
            tq.cs._gain(pc, 'protected', 1)
            c.notes.append("Protected +1 (Crashing Wave Approach)")


@setup_for("Earthen Mantle Approach")
def _earthen_mantle(name, pc, s):
    # T182: "+2 bonus to Fire, Frost, Brilliant, and Shadow Resist" - the
    # sim's one elemental Resist.
    pc['elemres'] += 2


@hooks.on('hit_riders', "Deadeye's Shadow", order=33)
def _deadeye(pc, c):
    # T185: "When one of your ranged weapon attacks hits, the target is
    # Taunted by you."
    if c.hit and _is_ranged_weapon(pc, c.substitute):
        tq.cs._test_rider(pc, c.target, 'taunt', 1)
        c.notes.append("Taunted +1 (Deadeye's Shadow)")


@hooks.on('hit_riders', "Intimidating Presence", order=34)
def _intimidating(pc, c):
    # T199: "When one of your attacks hits, the target is Frightened of you."
    if c.hit:
        tq.cs._test_rider(pc, c.target, 'fright', 1)
        c.notes.append("Frightened +1 (Intimidating Presence)")


@hooks.on('attack_resolved', "Suppressing Fire", order=40)
def _suppressing_fire(pc, c):
    # T205: "When you make a ranged weapon attack, the target is Crippled
    # once, whether it hits or not."
    if _is_ranged_weapon(pc, c.substitute) and c.target['health'] > 0:
        tq.cs._gain(c.target, 'crippled', 1)
        c.notes.append("Crippled +1 (Suppressing Fire)")


@hooks.on('attack_luck', "Exploit the Opening", order=37)
def _exploit_the_opening(pc, c):
    # T204: "Your attacks against the Dodge or Parry Defense of a Harried
    # creature have Good Luck."
    return 1 if c.target.get('harried', 0) > 0 and pc.get('opp_def') in ('Parry/Dodge', 'Dodge') else 0


@hooks.on('attack_luck', "Doubleshot", order=38)
def _doubleshot_luck(pc, c):
    # T177: "Your ranged weapon attacks have Bad Luck" - counted against
    # the attack's Good Luck (the flip nets them, cards.flip_for).
    return -1 if _is_ranged_weapon(pc, c.substitute) else 0


def _within_3(pc, c, units):
    cs = tq.cs
    if not c.movement_on:
        return []
    return [u for u in units if u is not pc and u['health'] > 0 and cs._distance(pc['pos'], u['pos']) <= 3]


def _aura_log(pc, c, via, units, effect):
    if units and c.log:
        c.log(unit=pc['name'], action='technique', via=via, target=', '.join(u['name'] for u in units),
              effects=effect)


@hooks.on('pc_turn_start', "Aura of Death", order=90)
def _aura_of_death(pc, c):
    # T187: "At the start of your turn, each enemy within 3 meters of you
    # gains Necrotic."
    near = _within_3(pc, c, c.enemies)
    for e in near:
        tq.cs._gain(e, 'necrotic', 1)
    _aura_log(pc, c, "Aura of Death", near, "Necrotic +1")
    return 0


@hooks.on('pc_turn_start', "Dread Reputation", order=91)
def _dread_reputation(pc, c):
    # T200: "At the start of your turn, each enemy within 3 meters of you
    # that can see you is Frightened of you." Line of sight isn't checked.
    near = _within_3(pc, c, c.enemies)
    for e in near:
        tq.cs._test_rider(pc, e, 'fright', 1)
    _aura_log(pc, c, "Dread Reputation", near, "Frightened +1")
    return 0


@hooks.on('pc_turn_start', "Forward!", order=92)
def _forward(pc, c):
    # T195: "At the start of your turn, each ally within 3 meters of you is
    # Hasted."
    near = _within_3(pc, c, c.pcs)
    for p in near:
        tq.cs._gain(p, 'hasted', 1)
    _aura_log(pc, c, "Forward!", near, "Hasted +1")
    return 0


@hooks.on('after_hit', "Lead by Example", order=64)
def _lead_by_example(pc, c):
    # T196: "When one of your attacks hits, the next attack an ally makes
    # against that creature this round has Good Luck."
    c.target['lead_by_b'] = (c.rnd, pc)


@hooks.on('attack_luck', order=39)
def _lead_by_example_luck(pc, c):
    # Any PC's attack: is there a Lead by Example mark on this target from
    # an ally, this round? (A dict lookup for everyone else.)
    mark = c.target.get('lead_by_b')
    if mark and mark[0] == c.rnd and mark[1] is not pc:
        c.target['lead_by_b'] = None
        return 1
    return 0


@hooks.on('after_hit', "Commander's Gambit", order=65)
def _commanders_gambit(pc, c):
    """T198: "Once per round, when one of your attacks hits, an ally within
    5 meters of you may spend 1 AP to make an Opportunity Attack against
    the target." The hardest hitter whose Weapon reaches it and who has
    an Interrupt AP left."""
    cs = tq.cs
    t = c.target
    if pc.get('gambit_round_b') == c.rnd or t['health'] <= 0 or 'pos' not in pc:
        return
    ready = [p for p in c.pcs if p is not pc and p['health'] > 0 and not p.get('weapon_is_spell')
             and cs._distance(pc['pos'], p['pos']) <= 5 and cs._distance(p['pos'], t['pos']) <= cs.effective_range(p)
             and _irq_ap(p) >= 1]
    if not ready:
        return
    ally = max(ready, key=lambda p: p['damage'])
    pc['gambit_round_b'] = c.rnd
    _irq_spend(ally, 1)
    ally['gambits_b'] = ally.get('gambits_b', 0) + 1
    cs._reaction_attack(ally, t, c.pcs, f"{ally['weapon_name']} (Commander's Gambit)", None, c.log)


@hooks.on('enemy_turn_start', order=60)
def _grasping_earth(e, c):
    # T202: "Enemies that start their turn in Difficult Terrain are Slowed
    # once." Runs for every enemy; nothing to do without terrain or the
    # Style on a PC who's still up.
    cs = tq.cs
    terrain = cs._movement.TERRAIN
    if not terrain or 'pos' not in e:
        return
    if not any(p['health'] > 0 and 'Grasping Earth' in p.get('passives', ()) for p in cs._CTX.get('pcs') or ()):
        return
    if terrain.get(cs._movement.clamp(e['pos']), 0) > 0:
        cs._gain(e, 'slowed', 1)
        e['grasped_b'] = e.get('grasped_b', 0) + 1


# Drunken Brawling (T176): "When you move or Shift, each enemy you're
# adjacent to at any point during that movement is Harried. An enemy can
# only be Harried by this once per turn." The sim's movement has no hook
# along the path, so it's read where the PC ends up: before each attack and
# at the end of the turn, once it has moved, every enemy next to it.

@hooks.on('pc_turn_start', "Drunken Brawling", order=2)
def _brawling_start(pc, c):
    pc['brawl_b'] = (tuple(pc['pos']) if 'pos' in pc else None, set(), c.enemies)
    return 0


def _brawling_harry(pc):
    cs = tq.cs
    start, done, enemies = pc.get('brawl_b') or (None, None, ())
    if start is None or tuple(pc['pos']) == start:
        return
    for e in enemies:
        if e['health'] > 0 and id(e) not in done and cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE:
            done.add(id(e))
            e['harried'] = e.get('harried', 0) + 1
            pc['brawl_harried'] = pc.get('brawl_harried', 0) + 1


@hooks.on('before_attack', "Drunken Brawling")
def _brawling_before(pc, c):
    _brawling_harry(pc)
    return 0


@hooks.on('pc_turn_end', "Drunken Brawling", order=30)
def _brawling_end(pc, c):
    _brawling_harry(pc)
    return 0


# ---- Repeats: Doubleshot and Twin Spell ----
# glossary.md, Repeat: "you make that attack again against the same
# target as part of the same action ... A Repeat can't itself be
# Repeated." combat_sim's Repeat (`_repeat`, Flurry's) carries a Battle
# Maneuver copy; a plain attack's Repeat carries a copy with no Features.

def _record_last(pc, c):
    pc['_last_b'] = SimpleNamespace(hit=c.hit, target=c.target, sub=c.substitute, mv=c.mv,
                                    repeat=bool(getattr(c, 'repeat', False)))


for _key in ("Doubleshot", "Twin Spell", "Snake School - Striking Constrictor", "Demon School - Circling Vulture"):
    hooks.on('attack_resolved', _key, order=45)(_record_last)


def _plain_repeat():
    import party  # party imports techniques, which imports this file
    return party._maneuver_features({})


@hooks.on('after_attack', "Doubleshot", order=20)
def _doubleshot(pc, c):
    # T177: "...and you Repeat each one."
    last = pc.get('_last_b')
    if (last and not last.repeat and last.target is c.target and c.target['health'] > 0
            and not pc.get('_repeat') and _is_ranged_weapon(pc, last.sub)):
        pc['_repeat'] = last.mv or _plain_repeat()
        pc['repeats_b'] = pc.get('repeats_b', 0) + 1
    return 0


@hooks.on('after_attack', "Twin Spell", order=21)
def _twin_spell(pc, c):
    """T203: "When you make a damaging Spell attack against a single
    target, you may expend another of your Encounter Spells of the same
    Level or higher to Repeat it." Only the row's own War Magic Weapon:
    a Repeat here is the Weapon's attack, and the attack loop takes a
    Weapon use for it, which is the other Spell expended. A War Magic
    copy with its own Features (a Technique attack) isn't Repeated."""
    last = pc.get('_last_b')
    if (last and not last.repeat and last.sub is None and pc.get('weapon_is_spell') and pc['damage'] > 0
            and last.target is c.target and c.target['health'] > 0 and not pc.get('_repeat')
            and (tq.encounter.weapon_left(pc) or 0) >= 1):
        pc['_repeat'] = _plain_repeat()
        pc['repeats_b'] = pc.get('repeats_b', 0) + 1
    return 0


# ======================================================================
# Martial and Discipline Schools
# ======================================================================

# T150, Level 3, 2 AP, cost 1 Health: "Make an Unarmed weapon attack
# against the target's Vital Defense. If it hits, it deals Shadow damage
# plus an extra [half your Meditation Skill Total]."
_strike("T150", "Demon School - Ripjaw Gambit", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg + _med(st, sk) // 2, dmg_type="Shadow", opp_def="Vital"))


@hooks.on('before_attack', "Demon School - Ripjaw Gambit")
def _ripjaw_cost(pc, c):
    # The Cost, paid as it's made. Not taken out of the last Health point.
    if c.substitute and c.substitute['via'] == "Demon School - Ripjaw Gambit" and pc['health'] > 1:
        pc['health'] -= 1
    return 0


# T151, Level 3: "Make an Unarmed weapon attack against the target's Vital
# Defense. If it hits, it deals Shadow damage and the target gains [half
# your Meditation Skill Total] + [Diamonds] stacks each of Harried and
# Vulnerable."
_strike("T151", "Demon School - Shepherd Opens the Gate", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, dmg_type="Shadow", opp_def="Vital", effect=("vulnerable", _med(st, sk) // 2, "Diamonds"),
    harry=_med(st, sk) // 2))


# T155, Level 3: "...against the target's Mental Defense. If it hits, it
# deals Brilliant damage and Pushes the target [Meditation Skill Total] +
# [Spades] meters."
_strike("T155", "Shugen School - Tide Rolls Back the Shore", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, dmg_type="Brilliant", opp_def="Mental", push=_med(st, sk)))

# T156, Level 4: "...against the target's Mental Defense. If it hits, it
# deals Brilliant damage and the target is Crippled [half your Meditation
# Skill Total] + [Clubs] times."
_strike("T156", "Shugen School - Lantern Gutters in the Wind", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, dmg_type="Brilliant", opp_def="Mental", effect=("crippled", _med(st, sk) // 2, "Clubs")))

# T147, Level 2: "Make an Unarmed weapon attack against the target. If the
# attack is Parried, the target gains a stack of Bleeding. If it hits, it
# deals no damage; instead the target gains 2 stacks of Bleeding, plus 1
# for each Extra Success, and is Slowed 2 + [Spades] times."
_strike("T147", "Bear School - Shattering Slam", lambda st, sk, atk, dmg: _unarmed(
    atk, 0, effect=("slowed", 2, "Spades")))

# Great Old Oak School, against the target's Vigilant Defense: T163
# (Level 2) "you gain [half your Meditation Skill Total] + [Hearts] stacks
# of Protected"; T164 (Level 3) "the target is Taunted by you [half your
# Meditation Skill Total] + [Hearts] times, and you ignore Harried for 2
# rounds"; T165 (Level 4) "remove up to [half your Meditation Skill Total]
# total stacks of Bleeding, Crippled, Frightened, Necrotic, Slowed,
# Taunted, and/or Vulnerable from yourself, and it deals extra damage
# equal to the number of stacks removed."
_strike("T163", "Great Old Oak School - Tree Withstands the Storm", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, opp_def="Vigilant", half_med=_med(st, sk) // 2))
_strike("T164", "Great Old Oak School - Oak Draws the Lightning", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, opp_def="Vigilant", half_med=_med(st, sk) // 2))
_strike("T165", "Great Old Oak School - Old Growth Digs Deep", lambda st, sk, atk, dmg: _unarmed(
    atk, dmg, opp_def="Vigilant", half_med=_med(st, sk) // 2))

# Discipline attacks (Meditation, not a weapon): T158 (Level 1, "An
# adjacent creature") "against the target's Vital Defense. If it hits, it
# deals 3 + [Mind] Shadow damage"; T161 (Level 2, within [Meditation Skill
# Total] meters) "Vital Defense. If it hits, the target gains 4 +
# [Diamonds] stacks each of Vulnerable and Necrotic"; T162 (Level 4, the
# same reach) "Vital Defense. If it hits, the target gains 2 + [Clubs]
# stacks of Bleeding, then it deals 2 + [Mind] Shadow damage plus 1 per
# stack of Bleeding the target has"; T167 (Level 2, the same reach)
# "Mental Defense. If it hits, the target is Crippled 3 + [Clubs] times
# and Frightened of you 2 + [Hearts] times." Ley-weaving's +3 meters isn't
# added to the reach (a profile doesn't see the passives).


def _discipline(st, sk, opp_def, damage, dmg_type="Shadow", reach=None, **kw):
    med = _med(st, sk)
    prof = dict(skill_total=med, damage=damage, dmg_type=dmg_type, opp_def=opp_def, effect=None,
                skill="Meditation", range=med if reach is None else reach)
    prof.update(kw)
    return prof


_strike("T158", "Demon School - Firefly Dies in the Hand", lambda st, sk, atk, dmg: _discipline(
    st, sk, "Vital", 3 + int(st["Mind"]), reach=1), unarmed=False)
_strike("T161", "Demon School - Bell Tolls a Dirge", lambda st, sk, atk, dmg: _discipline(
    st, sk, "Vital", 0, effect=("vulnerable", 4, "Diamonds")), unarmed=False)
_strike("T162", "Demon School - Fawn Left to the Wolves", lambda st, sk, atk, dmg: _discipline(
    st, sk, "Vital", 2 + int(st["Mind"])), unarmed=False)
_strike("T167", "Shugen School - Gaze of Pale Moonlight", lambda st, sk, atk, dmg: _discipline(
    st, sk, "Mental", 0, dmg_type="Brilliant", effect=("crippled", 3, "Clubs")), unarmed=False)


def _via(c, name):
    return bool(c.substitute) and c.substitute.get('via') == name


@hooks.on('hit_riders', "Bear School - Shattering Slam", order=35)
def _shattering_slam(pc, c):
    cs = tq.cs
    if not _via(c, "Bear School - Shattering Slam"):
        return
    n = 1 if c.parried else 2 + _extra_successes(c.pool, 'Brawl')
    cs._gain(c.target, 'bleeding', n)
    c.notes.append(f"Bleeding +{n}")


@hooks.on('hit_riders', "Demon School - Fawn Left to the Wolves", order=36)
def _fawn_left(pc, c):
    # Before the damage: the Bleeding goes on, then the damage counts it.
    # pc['damage'] is the strike's own here, put back after the attack.
    cs = tq.cs
    if c.hit and _via(c, "Demon School - Fawn Left to the Wolves"):
        n = 2 + cs._suit_count(c.pool, 'Clubs')
        cs._gain(c.target, 'bleeding', n)
        pc['damage'] += c.target['bleeding']
        c.notes.append(f"Bleeding +{n}, +{c.target['bleeding']} damage")


@hooks.on('hit_riders', "Great Old Oak School - Old Growth Digs Deep", order=37)
def _old_growth(pc, c):
    """The stacks come off before the damage, which counts them: Bleeding
    first, then Crippled, then whichever there is most of (Boughs
    Unbroken's order). "For the encounter, you can't be moved, Pushed,
    Shifted, or Teleported against your will" isn't modeled: combat_sim's
    Push has no check for it."""
    if not (c.hit and _via(c, "Great Old Oak School - Old Growth Digs Deep")):
        return
    budget = c.substitute['half_med']
    order = ['bleeding', 'crippled'] + sorted(('slowed', 'vulnerable', 'necrotic', 'taunted', 'frightened'),
                                              key=lambda k: -pc.get(k, 0))
    removed = 0
    for k in order:
        n = min(budget - removed, pc.get(k, 0))
        if n > 0:
            pc[k] -= n
            removed += n
            if pc[k] == 0:
                pc.pop('skip_' + k, None)
                if k in ('taunted', 'frightened'):
                    pc[k + '_by'] = None
    if removed:
        pc['damage'] += removed
        c.notes.append(f"removed {removed} stacks from the PC, +{removed} damage")


@hooks.on('after_hit', "Demon School - Shepherd Opens the Gate", order=66)
def _shepherd(pc, c):
    if _via(c, "Demon School - Shepherd Opens the Gate"):
        n = c.substitute['harry'] + tq.cs._suit_count(c.pool, 'Diamonds')
        c.target['harried'] = c.target.get('harried', 0) + n
        c.notes.append(f"Harried +{n}")


@hooks.on('after_hit', "Shugen School - Tide Rolls Back the Shore", order=67)
def _tide_rolls_back(pc, c):
    t = c.target
    if _via(c, "Shugen School - Tide Rolls Back the Shore") and t['health'] > 0 and 'pos' in t:
        n = c.substitute['push'] + tq.cs._suit_count(c.pool, 'Spades')
        _push_from(pc, t, pc['pos'], n, c.pcs, c.log, c.notes, "Tide Rolls Back the Shore")


@hooks.on('after_hit', "Demon School - Bell Tolls a Dirge", order=68)
def _bell_tolls(pc, c):
    # The Necrotic half; the Vulnerable half is the strike's own effect.
    if _via(c, "Demon School - Bell Tolls a Dirge"):
        n = 4 + tq.cs._suit_count(c.pool, 'Diamonds')
        tq.cs._gain(c.target, 'necrotic', n)
        c.notes.append(f"Necrotic +{n}")


@hooks.on('after_hit', "Shugen School - Gaze of Pale Moonlight", order=69)
def _gaze(pc, c):
    if _via(c, "Shugen School - Gaze of Pale Moonlight") and c.target['health'] > 0:
        n = 2 + tq.cs._suit_count(c.pool, 'Hearts')
        tq.cs._test_rider(pc, c.target, 'fright', n)
        c.notes.append(f"Frightened +{n}")


@hooks.on('after_hit', "Great Old Oak School - Tree Withstands the Storm", order=70)
def _tree_withstands(pc, c):
    if _via(c, "Great Old Oak School - Tree Withstands the Storm"):
        n = c.substitute['half_med'] + tq.cs._suit_count(c.pool, 'Hearts')
        tq.cs._gain(pc, 'protected', n)
        c.notes.append(f"Protected +{n} (self)")


@hooks.on('after_hit', "Great Old Oak School - Oak Draws the Lightning", order=71)
def _oak_draws(pc, c):
    # "for 2 rounds": this round and the next.
    if _via(c, "Great Old Oak School - Oak Draws the Lightning") and c.target['health'] > 0:
        n = c.substitute['half_med'] + tq.cs._suit_count(c.pool, 'Hearts')
        tq.cs._test_rider(pc, c.target, 'taunt', n)
        pc['oak_until_b'] = c.rnd + 1
        c.notes.append(f"Taunted +{n}; ignores Harried through round {c.rnd + 1}")


@hooks.on('attack_declared', "Great Old Oak School - Oak Draws the Lightning")
def _oak_ignores_harried(pc, c):
    # The enemy's flip reads the PC's Defense right after this point, before
    # adding this attack's own Harried.
    if pc.get('oak_until_b', 0) >= tq.cs._CTX['rnd']:
        pc['harried'] = 0
    return 0


# ---- Interrupts on an Unarmed hit (1 AP, Encounter), in the PC's own turn ----

for _tid, _name in (("T145", "Snake School - Striking Constrictor"), ("T152", "Demon School - Circling Vulture")):
    _encounter(_tid, _name, unarmed=True)


def _keeps_grapple(pc):
    # The reverse of combat_sim._try_break_grapple's test: a PC who'd
    # spend the next turn breaking the grapple doesn't start one.
    cs = tq.cs
    return not (pc.get('two_handed') or cs.effective_range(pc) > cs.T.MELEE_RANGE
                or pc.get('play_style') in ('Back-liner', 'Skirmisher'))


@hooks.on('after_attack', "Snake School - Striking Constrictor", order=30)
def _striking_constrictor(pc, c):
    """T145 (1 AP Interrupt, "you hit with an Unarmed weapon attack"):
    "Make an Unarmed weapon attack with Good Luck against the target's
    Dodge or Parry Defense. If it hits, you grapple the target, as the
    Grapple maneuver." Only by a PC who'd keep the grapple (play style
    and weapon), on a target not already in one."""
    cs = tq.cs
    name = "Snake School - Striking Constrictor"
    last, t = pc.get('_last_b'), c.target
    if (not last or not last.hit or last.target is not t or t['health'] <= 0 or c.ap < 1
            or tq.encounter.left(pc, name) <= 0 or not _is_unarmed_weapon(pc, last.sub) or not _keeps_grapple(pc)
            or pc.get('grapple') is not None or t.get('grapple') is not None):
        return 0
    tq.encounter.spend(pc, name)
    r = _resolve(pc, t, cs._CTX['pcs'], skill_total=pc['skill_total'], opp_def='Parry/Dodge',
                 damage=pc['damage'], dmg_type=pc['dmg_type'], skill=pc['attack_skill'], weapon=True, good=1)
    notes = []
    if r.hit and t['health'] > 0:
        pc['grapple'], t['grapple'] = t, pc
        pc['my_grapple_b'] = t  # Chainbreaker leaves the PC's own grapple alone
        pc['grapples_b'] = pc.get('grapples_b', 0) + 1
        notes.append("grappled")
    _log_strike(c.log, pc, t, r, "Striking Constrictor", notes)
    return 1


@hooks.on('after_attack', "Demon School - Circling Vulture", order=31)
def _circling_vulture(pc, c):
    """T152 (1 AP Interrupt, "you hit with an Unarmed weapon attack"):
    "Make a Meditation attack against the target's Vital Defense. If it
    hits, remove all stacks of Bleeding, Necrotic, and Vulnerable from the
    target. It loses Health equal to the number of stacks removed, up to
    [Meditation Skill Total]." Cashed in once there are 4 or more."""
    cs = tq.cs
    name = "Demon School - Circling Vulture"
    last, t = pc.get('_last_b'), c.target
    if (not last or not last.hit or last.target is not t or t['health'] <= 0 or c.ap < 1
            or tq.encounter.left(pc, name) <= 0 or not _is_unarmed_weapon(pc, last.sub)):
        return 0
    stacks = sum(t.get(k, 0) for k in ('bleeding', 'necrotic', 'vulnerable'))
    if stacks < 4:
        return 0
    tq.encounter.spend(pc, name)
    med = pc['skill_totals']["Meditation"]
    r = _resolve(pc, t, cs._CTX['pcs'], skill_total=med, opp_def='Vital', damage=0, dmg_type='Shadow',
                 skill='Meditation')
    notes = []
    if r.hit:
        for k in ('bleeding', 'necrotic', 'vulnerable'):
            t[k] = 0
            t.pop('skip_' + k, None)
        loss = min(stacks, med, t['health'])
        t['health'] -= loss
        cs._damaged_by_pc(pc, t, loss)
        notes.append(f"removed {stacks} stacks, lost {loss} Health")
    _log_strike(c.log, pc, t, r, "Circling Vulture", notes)
    return 1


# ---- Cast at the start of the turn ----

_encounter("T146", "Snake School - Chainbreaker", unarmed=True)
_encounter("T153", "Shugen School - Swallow Skims the Water", unarmed=True)
_encounter("T149", "Bear School - The Grizzly Awakens", unarmed=True)
_encounter("T157", "Shugen School - Great Wind Scatters the Leaves")
_encounter("T160", "Demon School - Dusk Wind Withers the Grass")
_encounter("T169", "Demon School - Blood Answers Blood")


@hooks.on('pc_turn_start', "Snake School - Chainbreaker", order=12)
def _chainbreaker(pc, c):
    """T146 (2 AP, Encounter): "If you are grappled, the grapple ends.
    Then remove up to [half your Brawl Skill Total] total stacks of
    Bleeding, Crippled, and/or Slowed from yourself, and make an Unarmed
    weapon attack against the target." Taken when an enemy has the PC in a
    grapple, or the PC carries 2 or more of those stacks with an enemy already
    next to it (before the break-grapple roll, which it makes moot)."""
    cs = tq.cs
    name = "Snake School - Chainbreaker"
    if tq.encounter.left(pc, name) <= 0 or c.ap < 2 or not c.movement_on:
        return 0
    held = cs._grappled(pc)
    stacks = sum(pc.get(k, 0) for k in ('bleeding', 'crippled', 'slowed'))
    near = [e for e in c.enemies if e['health'] > 0 and cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE]
    if held is pc.get('my_grapple_b'):
        held = None
    if not near or not (held is not None or stacks >= 2):
        return 0
    tq.encounter.spend(pc, name)
    if held is not None:
        cs._end_grapple(pc)
    budget = pc['skill_totals']["Brawl"] // 2
    removed = 0
    for k in ('bleeding', 'crippled', 'slowed'):
        n = min(budget - removed, pc.get(k, 0))
        if n > 0:
            pc[k] -= n
            removed += n
            if pc[k] == 0:
                pc.pop('skip_' + k, None)
    t = held if held is not None and held['health'] > 0 else min(near, key=lambda e: e['health'])
    r = _resolve(pc, t, c.pcs, skill_total=pc['skill_total'], opp_def=pc['opp_def'], damage=pc['damage'],
                 dmg_type=pc['dmg_type'], skill=pc['attack_skill'], weapon=True)
    notes = [f"removed {removed} stacks" + (", broke the grapple" if held is not None else "")]
    _log_strike(c.log, pc, t, r, "Chainbreaker", notes)
    return 2


@hooks.on('pc_turn_start', "Shugen School - Swallow Skims the Water", order=13)
def _swallow(pc, c):
    """T153 (1 AP, Encounter, "A creature within [Meditation Skill Total]
    meters"): "Teleport to an empty space adjacent to the target, then make
    an Unarmed weapon attack against its Mental Defense. If it hits, it
    deals Brilliant damage." The gap-closer for a melee fighter with no
    enemy next to it: the weakest one in reach. A Teleport isn't a move,
    so nothing gets a Parting Shot."""
    cs = tq.cs
    name = "Shugen School - Swallow Skims the Water"
    if tq.encounter.left(pc, name) <= 0 or c.ap < 1 or not c.movement_on or cs.effective_range(pc) > cs.T.MELEE_RANGE:
        return 0
    living = [e for e in c.enemies if e['health'] > 0]
    if any(cs._distance(pc['pos'], e['pos']) <= cs.T.MELEE_RANGE for e in living):
        return 0
    reach = pc['skill_totals']["Meditation"]
    pool = [e for e in living if cs._distance(pc['pos'], e['pos']) <= reach]
    if not pool:
        return 0
    t = min(pool, key=lambda e: e['health'])
    tq.encounter.spend(pc, name)
    start = pc['pos']
    pc['pos'] = cs._movement.clamp(cs._movement._step_toward(t['pos'][0], t['pos'][1], start[0], start[1]))
    if c.log:
        c.log(unit=pc['name'], action='move', pos=pc['pos'], spaces=cs._distance(start, pc['pos']),
              via='Swallow Skims the Water (Teleport)')
    good = 1 if "Shugen School - Spirit Hands" in pc.get('passives', ()) else 0
    r = _resolve(pc, t, c.pcs, skill_total=pc['skill_total'], opp_def='Mental', damage=pc['damage'],
                 dmg_type='Brilliant', skill=pc['attack_skill'], weapon=True, good=good)
    _log_strike(c.log, pc, t, r, "Swallow Skims the Water")
    return 1


def _cone_targets(pc, c, length):
    """The enemies a cone `length` meters long catches, aimed at whichever
    enemy gets the most of them with no ally inside (techniques._in_cone,
    Funnel's shape). Used with two or more caught, or one from round 3 (an
    unused Encounter Technique is wasted)."""
    cs = tq.cs
    living = [e for e in c.enemies if e['health'] > 0 and 'pos' in e]
    others = [p for p in c.pcs if p['health'] > 0 and p is not pc]
    best = []
    for aim in living:
        if not 0 < cs._distance(pc['pos'], aim['pos']) <= length:
            continue
        if any(tq._in_cone(pc['pos'], aim['pos'], p['pos'], length) for p in others):
            continue
        caught = [e for e in living if tq._in_cone(pc['pos'], aim['pos'], e['pos'], length)]
        if len(caught) > len(best):
            best = caught
    return best if len(best) >= 2 or (best and c.rnd >= 3) else []


@hooks.on('pc_turn_start', "Bear School - The Grizzly Awakens", order=24)
def _grizzly(pc, c):
    """T149 (3 AP, Encounter, a 3-meter cone): "Make an Unarmed weapon
    attack against the Dodge Defense of each target creature. If it hits,
    it deals no damage; instead the target gains 3 stacks of Bleeding,
    plus 1 for each Extra Success, and is Slowed once." Objects don't
    come up in the sim."""
    cs = tq.cs
    name = "Bear School - The Grizzly Awakens"
    if tq.encounter.left(pc, name) <= 0 or c.ap < 3 or not c.movement_on:
        return 0
    targets = _cone_targets(pc, c, 3)
    if not targets:
        return 0
    tq.encounter.spend(pc, name)
    for e in targets:
        r = _resolve(pc, e, c.pcs, skill_total=pc['skill_total'], opp_def='Dodge', damage=0,
                     dmg_type=pc['dmg_type'], skill=pc['attack_skill'], weapon=True)
        notes = []
        if r.hit:
            n = 3 + _extra_successes(r.pool, pc['attack_skill'])
            cs._gain(e, 'bleeding', n)
            cs._gain(e, 'slowed', 1)
            notes.append(f"Bleeding +{n}, Slowed +1")
        _log_strike(c.log, pc, e, r, "The Grizzly Awakens", notes)
    return 3


@hooks.on('pc_turn_start', "Demon School - Dusk Wind Withers the Grass", order=25)
def _dusk_wind(pc, c):
    """T160 (2 AP, Encounter, a 2-meter cone): "Make a Meditation attack
    against each target's Vital Defense. If it hits, it deals 2 + [Mind]
    Shadow damage and the target gains 2 + [Clubs] stacks of Bleeding."""
    cs = tq.cs
    name = "Demon School - Dusk Wind Withers the Grass"
    if tq.encounter.left(pc, name) <= 0 or c.ap < 2 or not c.movement_on:
        return 0
    targets = _cone_targets(pc, c, 2)
    if not targets:
        return 0
    tq.encounter.spend(pc, name)
    for e in targets:
        r = _resolve(pc, e, c.pcs, skill_total=pc['skill_totals']["Meditation"], opp_def='Vital',
                     damage=2 + pc['stats']['Mind'], dmg_type='Shadow', skill='Meditation')
        notes = []
        if r.hit:
            n = 2 + cs._suit_count(r.pool, 'Clubs')
            cs._gain(e, 'bleeding', n)
            notes.append(f"Bleeding +{n}")
        _log_strike(c.log, pc, e, r, "Dusk Wind Withers the Grass", notes)
    return 2


@hooks.on('pc_turn_start', "Shugen School - Great Wind Scatters the Leaves", order=26)
def _great_wind(pc, c):
    """T157 (2 AP, Encounter, "Any number of creatures within 2 meters of
    you"): "Choose a direction, then make a Meditation attack against each
    target's Mental Defense. If it hits, it deals 2 + [Mind] Brilliant
    damage and the target is Pushed [Meditation Skill Total] + [Spades]
    meters in that direction. If it misses, the target is Pushed 2 meters
    in that direction." Every enemy that close, pushed away from the rest
    of the party; two or more, or one from round 3."""
    cs = tq.cs
    name = "Shugen School - Great Wind Scatters the Leaves"
    if tq.encounter.left(pc, name) <= 0 or c.ap < 2 or not c.movement_on:
        return 0
    targets = [e for e in c.enemies if e['health'] > 0 and cs._distance(pc['pos'], e['pos']) <= 2]
    if not (len(targets) >= 2 or (targets and c.rnd >= 3)):
        return 0
    allies = [p for p in c.pcs if p['health'] > 0]
    ax = sum(p['pos'][0] for p in allies) / len(allies)
    ay = sum(p['pos'][1] for p in allies) / len(allies)
    ex = sum(e['pos'][0] for e in targets) / len(targets)
    ey = sum(e['pos'][1] for e in targets) / len(targets)
    dx, dy = (ex > ax) - (ex < ax), (ey > ay) - (ey < ay)
    if (dx, dy) == (0, 0):
        dx = 1
    tq.encounter.spend(pc, name)
    med = pc['skill_totals']["Meditation"]
    for e in targets:
        r = _resolve(pc, e, c.pcs, skill_total=med, opp_def='Mental', damage=2 + pc['stats']['Mind'],
                     dmg_type='Brilliant', skill='Meditation')
        notes = []
        if e['health'] > 0:
            n = med + cs._suit_count(r.pool, 'Spades') if r.hit else 2
            # Pushed from a point just behind it, so it goes the one way.
            _push_from(pc, e, (e['pos'][0] - dx, e['pos'][1] - dy), n, c.pcs, c.log, notes,
                       "Great Wind Scatters the Leaves")
        _log_strike(c.log, pc, e, r, "Great Wind Scatters the Leaves", notes)
    return 2


@hooks.on('pc_hit', "Demon School - Blood Answers Blood", order=20)
def _blood_answers_blood(pc, c):
    """T169 (1 AP Interrupt, "a creature's attack makes you lose Health,
    after you lose it"; the attacker, within [Meditation Skill Total]
    meters): "Make a Meditation attack against the target's Vital
    Defense. If it hits, it deals 2 + [Mind] Shadow damage and the target
    gains stacks of Bleeding equal to the Health you lost, up to [half
    your Meditation Skill Total]." A non-weapon Discipline, so Ley-weaving
    adds its 3 meters."""
    cs = tq.cs
    name = "Demon School - Blood Answers Blood"
    e = c.attacker
    if (c.dmg <= 0 or pc['health'] <= 0 or e['health'] <= 0 or tq.encounter.left(pc, name) <= 0 or _irq_ap(pc) < 1):
        return
    med = pc['skill_totals']["Meditation"]
    if 'pos' in pc and cs._distance(pc['pos'], e['pos']) > med + pc['ley']:
        return
    tq.encounter.spend(pc, name)
    _irq_spend(pc, 1)
    r = _resolve(pc, e, cs._CTX.get('pcs') or [pc], skill_total=med, opp_def='Vital', damage=2 + pc['stats']['Mind'],
                 dmg_type='Shadow', skill='Meditation')
    notes = []
    if r.hit and e['health'] > 0:
        n = min(c.dmg, med // 2)
        cs._gain(e, 'bleeding', n)
        notes.append(f"Bleeding +{n}")
    _log_strike(_ctx_log(), pc, e, r, "Blood Answers Blood", notes)
