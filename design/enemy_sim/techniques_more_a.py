"""The rest of the Technique catalog, part A (2026-10-27): T005-T099.

Each Technique here is modeled (registered the same way as in
techniques.py), listed in techniques.OUT_OF_COMBAT, or listed in
techniques.DEFERRED with what it would need. combat_sim is `tq.cs` at
fight time (techniques.py's `cs`), not at import.

The helpers they share (Interrupt AP, paying cards, healing, reach) are
in tech_common.py.
"""
import math

import techniques as tq
from techniques import technique, hooks, setup_for, OUT_OF_COMBAT, DEFERRED, BuildError  # noqa: F401

OUT_OF_COMBAT.update({
    "T008": "Canopy Creeper", "T009": "Falling Tumble", "T015": "Trout Seeming",
    "T024": "Artisanal Training", "T025": "Extensive Background", "T026": "Practiced Persona",
    "T028": "Ventriloquy", "T029": "Air of Mystery", "T038": "Practical Necromancy",
    "T040": "Re-purpose Materials", "T043": "Street Runner", "T044": "Wisdom of the Woods",
    "T046": "Artisan's Eye", "T047": "Bespoke Masterpieces", "T048": "Environmental Esoterica",
    "T049": "Gather the Evidence", "T051": "Preparation", "T054": "One of Many Faces",
    "T057": "Social Maneuver (a Statement's Features)",
    "T061": "A Perfectly Good Explanation", "T085": "Pranic Nourishment",
    "T095": "Placeholder's Tender Telekinesis", "T096": "Placeholder's Wizardly Witchlight",
    # Follower (T059) is out of combat, so its knacks are too. Squire and
    # Magical Adept would touch a fight, through a follower the sim doesn't
    # put on the field.
    "T060": "Follower: Knack",
    # Like Soulblade (T002): what it conjures is the row's own Weapon and
    # armor.
    "T094": "Conjure Armament (the gear it makes is the row's Weapon and armor)",
})

DEFERRED.update({
    "T005": "vision rules (darkness, hidden or invisible creatures)",
    "T030": "summoned companions",
    "T031": "summoned companions (Animal Companion)",
    "T032": "Masterwork item rules",
    "T041": "item rules (crafting an item mid-fight)",
    "T052": "a can't-see state that enemy targeting respects, and hiding",
    "T056": "surprise rounds",
    "T081": "PC grapple attacks, and throwing a creature into objects",
    "T084": "a hook where a PC gains an effect (_apply_to_pc), to ignore the stacks",
    "T087": "a Teleport-and-swap move the PC's turn plans around",
    "T088": "enemy_left_reach firing without Parting Shot (_CTX['ps_pcs']), and a Countered move",
    "T089": "a hook between an enemy's flip and its hit, to set the PC's Parry and redirect the attack",
    "T090": "poison item rules",
    "T092": "PC grapples, and redirecting a Parried attack",
    "T098": "summoned creatures",
    "T099": "allies paying a Spell's discards (tactics' Healing Magic card spend)",
})


# ---- Shared helpers ----

from tech_common import (interrupt_ap_left, _interrupt_ap, _can_pay, _pay_card, _heal,  # noqa: E402,F401
                         _near, _missing)


# ---- Solemn Pact (T013) ----

@technique("T013", "Solemn Pact")
def _solemn_pact(sheet, copies, choices):
    """T013, Encounter, "0 AP - Interrupt (you make a flip of the chosen
    type with the chosen Skill)": "You gain Good Luck twice on the flip."
    The pact is the Choices column ("Solemn Pact: Melee attack flips");
    blank is the Weapon's own Skill's attack flips. A non-attack pact
    never comes up in a fight."""
    import tunables as T
    pick = choices[0] if choices else ""
    skill = next((k for k in T.PC_SKILL_STAT if k.lower() in pick.lower()), None)
    if pick and skill is None:
        raise BuildError(f"Solemn Pact: no Skill named in Choices ({pick!r})")
    sheet.pact = None if "non-attack" in pick.lower() else (skill or "")
    sheet.encounter_techs.extend(["Solemn Pact"] * len(copies))


tq.ENCOUNTER_NAMES.add("Solemn Pact")


@setup_for("Solemn Pact")
def _pact_setup(name, pc, s):
    pact = getattr(s.sheet, 'pact', "")
    pc['pact_skill'] = (pact or s.w_skill) if pact is not None else None


@hooks.on('attack_luck', 'Solemn Pact', order=50)
def _pact_luck(pc, c):
    # Declared as the flip's made, so it can't wait to see the card. It
    # goes on a Battle Maneuver or Technique attack when one of the pact's
    # Skill is still to come, else on the first attack with that Skill.
    skill = pc.get('pact_skill')
    if not skill or tq.encounter.left(pc, 'Solemn Pact') <= 0:
        return 0
    if ((c.substitute or {}).get('skill') or pc['attack_skill']) != skill:
        return 0
    big = c.mv is not None or (c.substitute is not None and 'uses' in c.substitute)
    pending = (pc.get('maneuver') or {}).get('uses', 0) > 0 or any(
        t['uses'] > 0 and t.get('skill') == skill for t in pc.get('tech_attacks', ()))
    if not big and pending:
        return 0
    tq.encounter.spend(pc, 'Solemn Pact')
    c.notes.append("Good Luck twice (Solemn Pact)")
    return 2


# ---- Skin of Stone (T016) ----

tq._encounter("T016", "Skin of Stone")


def _try_skin(pc, enemies, movement_on, ap, start, log):
    """Skin of Stone (1 AP, Encounter) is taken when Brace would be: with
    AP left over at the end of a turn while an enemy's close enough to
    come for this PC, or at the start of a turn spent in melee
    unprotected (round 2 on). Returns the AP spent."""
    cs = tq.cs
    if tq.encounter.left(pc, 'Skin of Stone') <= 0 or ap < 1 or pc.get('protected', 0) > 0:
        return 0
    living = [e for e in enemies if e['health'] > 0]
    if not living:
        return 0
    if movement_on:
        near = min(cs._distance(pc['pos'], e['pos']) for e in living)
        if start and not (near <= cs.T.MELEE_RANGE and ap >= cs.T.ATTACK_AP_COST + 1 and pc.get('acted_round', 1) >= 2):
            return 0
        if not start and near > cs.T.BRACE_THREAT_RANGE:
            return 0
    elif start:
        return 0
    tq.encounter.spend(pc, 'Skin of Stone')
    amount = 1 + tq.half(pc, 'Resilience')  # "1 + [half your Resilience Skill Total]"
    cs._gain(pc, 'protected', amount)
    if log:
        log(unit=pc['name'], action='technique', via='Skin of Stone', effects=f"Protected +{amount}")
    return 1


@hooks.on('pc_turn_start', 'Skin of Stone', order=41)
def _skin_start(pc, c):
    return _try_skin(pc, c.enemies, c.movement_on, c.ap, True, c.log)


@hooks.on('pc_turn_end', 'Skin of Stone', order=21)
def _skin_end(pc, c):
    return _try_skin(pc, c.enemies, c.movement_on, c.ap, False, c.log)


# ---- Solemn Perseverance (T017) ----

tq._passive("T017", "Solemn Perseverance")


@hooks.on('pc_hit', 'Solemn Perseverance', order=20)
def _perseverance(pc, c):
    """T017: "After the first time you lose Health each encounter, you
    gain: Protected three times; remove up to 2 total stacks of your
    choice of Bleeding/Crippled/Frightened/Slowed/Taunted/Vulnerable."
    Triggered by an attack's hit; a Bleeding tick is Health lost too, but
    the sim has no hook there, so a PC whose first loss is a tick waits
    for the first hit. Bleeding goes first, then Crippled, then whatever
    there's most of (Boughs Unbroken's order)."""
    cs = tq.cs
    if c.dmg <= 0 or pc.get('_persevered') or pc['health'] <= 0:
        return
    pc['_persevered'] = True
    cs._gain(pc, 'protected', 3)
    left = 2
    for key in ('bleeding', 'crippled'):
        n = min(left, pc.get(key, 0))
        pc[key] = pc.get(key, 0) - n
        left -= n
    for key in sorted(('slowed', 'vulnerable', 'taunted', 'frightened'), key=lambda k: -pc.get(k, 0)):
        n = min(left, pc.get(key, 0))
        if n:
            pc[key] -= n
            left -= n
            if pc[key] == 0 and key in ('taunted', 'frightened'):
                pc[key + '_by'] = None
    c.applied.append(f"Protected +3, {2 - left} stacks removed (Solemn Perseverance)")


# ---- Lay On Hands (T020) ----

tq._passive("T020", "Lay On Hands")


@hooks.on('pc_turn_end', 'Lay On Hands', order=30)
def _lay_on_hands(pc, c):
    """T020, 1 AP, discard a card, yourself or an adjacent willing
    creature: "2. Remove up to 2 stacks of Bleeding. 3. Target heals 1
    Health, or 2 if the discarded card was a Heart." (Step 1's Poison
    isn't in the sim.) Spent from AP left at the end of the turn, a Heart
    if there's one in hand, on whoever it does the most for, and only
    when that's 3 Health or more: a card's worth (tunables.CARD_VALUE)."""
    cs = tq.cs
    spent = 0
    while c.ap - spent >= 1 and _can_pay(pc):
        heal = 2
        if cs.T.CARDS:
            heal = 2 if cs.cards.suit(cs.cards.lowest(pc['hand'], prefer_suit=cs.cards.HEARTS)) == cs.cards.HEARTS else 1
        pool = [p for p in c.pcs if p['health'] > 0 and (p is pc or _near(pc, p, c.movement_on))]
        if not pool:
            break
        p = max(pool, key=lambda p: min(2, p.get('bleeding', 0)) + min(heal, _missing(p)))
        if min(2, p.get('bleeding', 0)) + min(heal, _missing(p)) < 3:
            break
        _pay_card(pc, cs.cards.HEARTS)
        removed = min(2, p.get('bleeding', 0))
        p['bleeding'] = p.get('bleeding', 0) - removed
        healed = _heal(p, heal)
        spent += 1
        if c.log:
            c.log(unit=pc['name'], action='heal', target=p['name'], amount=healed, target_hp_after=p['health'],
                  via='Lay On Hands', effects=f"Bleeding -{removed}")
    return spent


# ---- Mind and Body Unbroken (T021) ----

tq._passive("T021", "Mind and Body Unbroken")


@hooks.on('pc_hit', 'Mind and Body Unbroken', order=90)
def _unbroken(pc, c):
    """T021, "0 AP - Interrupt (you would become Downed)", discard a card:
    "You are not Downed. Instead you have 1 Shallow and 1 Deep Health
    remaining." Not an Encounter Technique: it works as long as the cards
    last. Checked right after an attack's damage lands (pc_hit), before
    the enemy moves on; a Down from a Bleeding tick isn't caught."""
    if pc['health'] > 0 or _pay_card(pc) is None:
        return
    pc['health'] = 2
    pc['unbroken'] = pc.get('unbroken', 0) + 1
    c.applied.append("not Downed: 2 Health left (Mind and Body Unbroken)")


# ---- Hand of the Chirurgeon (T033) ----

tq._passive("T033", "Hand of the Chirurgeon")


def _try_chirurgeon(pc, c, start):
    """T033, 2 AP, yourself or an adjacent willing patient: "Remove up to
    [half your Medicine Skill Total] stacks of Bleeding from the target."
    Each stack is a Health it won't lose, so it's worth an attack's AP at
    the start of a turn when it clears 3 or more, and any AP left at the
    end of one. Returns the AP spent."""
    if c.ap < 2 or tq.half(pc, 'Medicine') <= 0:
        return 0
    pool = [p for p in c.pcs if p['health'] > 0 and p.get('bleeding', 0) > 0
            and (p is pc or _near(pc, p, c.movement_on))]
    if not pool:
        return 0
    p = max(pool, key=lambda p: p['bleeding'])
    n = min(tq.half(pc, 'Medicine'), p['bleeding'])
    if start and n < 3:
        return 0
    p['bleeding'] -= n
    if c.log:
        c.log(unit=pc['name'], action='technique', target=p['name'], via='Hand of the Chirurgeon',
              effects=f"Bleeding -{n}")
    return 2


@hooks.on('pc_turn_start', 'Hand of the Chirurgeon', order=45)
def _chirurgeon_start(pc, c):
    return _try_chirurgeon(pc, c, True)


@hooks.on('pc_turn_end', 'Hand of the Chirurgeon', order=31)
def _chirurgeon_end(pc, c):
    return _try_chirurgeon(pc, c, False)


# ---- Analyze Stance (T045) ----

tq._passive("T045", "Analyze Stance")


@hooks.on('before_attack', 'Analyze Stance', order=60)
def _analyze_own(pc, c):
    """T045, "1 AP - Interrupt (any time)": "The next attack against the
    target's Dodge or Parry Defense made by you or someone you choose has
    Good Luck." On this PC's own attack when its AP only covers one, like
    Eagle Eyes (which goes first if the PC has both). The Academics attack
    that follows only learns the target's numbers, which the sim already
    knows."""
    cs = tq.cs
    opp = (c.substitute or {}).get('opp_def') or pc.get('opp_def')
    if opp in ('Parry/Dodge', 'Dodge') and cs.T.ATTACK_AP_COST < c.ap < 2 * cs.T.ATTACK_AP_COST:
        pc['gl_next'] = pc.get('gl_next', 0) + 1
        return 1
    return 0


@hooks.on('pc_turn_end', 'Analyze Stance', order=40)
def _analyze_end(pc, c):
    # AP left at the end of a turn: one use per AP, on the enemies nearest
    # this PC, for whoever attacks them next.
    cs = tq.cs
    living = [e for e in c.enemies if e['health'] > 0 and not e.get('analyzed')]
    if c.movement_on:
        living.sort(key=lambda e: cs._distance(pc['pos'], e['pos']))
    spent = 0
    for e in living[:max(0, c.ap)]:
        e['analyzed'] = 1
        spent += 1
        if c.log:
            c.log(unit=pc['name'], action='technique', target=e['name'], via='Analyze Stance',
                  effects="Good Luck on the next attack against it")
    return spent


@hooks.on('attack_luck', order=45)
def _analyzed_luck(pc, c):
    if c.target.get('analyzed') and pc.get('opp_def') in ('Parry/Dodge', 'Dodge'):
        c.target['analyzed'] = 0
        return 1
    return 0


# ---- Optimize Blood (T050) ----

tq._passive("T050", "Optimize Blood")


@hooks.on('fight_start_order', 'Optimize Blood')
def _optimize_blood(pc, c):
    """T050, 10 minutes, yourself or a willing patient: "For the next [half
    your Medicine Skill Total] Health the target would lose, instead they
    gain that many stacks of Bleeding." Done before the fight, on the
    party member most likely to be hit: the melee one with the most
    Health. One patient a fight; with Medicinal Supplies (an item) a
    healer could dose more."""
    cs = tq.cs
    party = [u for side, u in c.order if side == 'party' and u['health'] > 0]
    if not party or tq.half(pc, 'Medicine') <= 0:
        return
    p = min(party, key=lambda u: (cs.effective_range(u) > cs.T.MELEE_RANGE, -u['max_health']))
    p['optimize_blood'] = max(p.get('optimize_blood', 0), tq.half(pc, 'Medicine'))


# ---- Pressure Point Revitalization (T055) ----

tq._passive("T055", "Pressure Point Revitalization")


@hooks.on('pc_turn_start', 'Pressure Point Revitalization', order=46)
def _pressure_points(pc, c):
    """T055, 2 AP, discard a card, an adjacent willing patient: "Make a
    Medicine flip with difficulty 11. If you succeed, gain 1 extra success
    for each 2 you beat the difficulty by; X = total successes. Your
    target may discard up to X cards, then heals 1 Health for each card
    discarded, plus 1 Health for each unique suit among cards discarded."
    Tried on an adjacent ally missing 4 or more with cards to spend, when
    the flip's at least even odds; the patient discards its lowest card
    of each suit first. Real cards only
    (the suits are the point). Returns the AP spent."""
    cs = tq.cs
    if not cs.T.CARDS or c.ap < 2 or not cs.cards.can_spend(pc):
        return 0
    pool = [p for p in c.pcs if p is not pc and p['health'] > 0 and _missing(p) >= 4
            and _near(pc, p, c.movement_on) and cs.cards.can_spend(p)]
    if not pool:
        return 0
    mod = pc['skill_totals']['Medicine'] - pc.get('crippled', 0)
    # Not when the flip's more likely to miss than make it.
    if cs._p_flip_at_least(11 - mod, 1 + pc.get('good_luck', 0)) < 0.5:
        return 0
    p = max(pool, key=_missing)
    _pay_card(pc)
    value, _ = cs._pc_flip(pc, mod, 11, pc.get('good_luck', 0), cs.tactics.pc_wounded(pc))
    total = mod + value
    healed = 0
    if total >= 11:
        x = 1 + (total - 11) // 2
        chosen, suits = [], set()
        for card in sorted(p['hand'], key=cs.cards.rank):
            if len(chosen) >= min(x, p['budget']) or len(chosen) + len(suits) >= _missing(p):
                break
            if cs.cards.suit(card) not in suits:
                chosen.append(card)
                suits.add(cs.cards.suit(card))
        for card in sorted(p['hand'], key=cs.cards.rank):
            if len(chosen) >= min(x, p['budget']) or len(chosen) + len(suits) >= _missing(p):
                break
            if card not in chosen:
                chosen.append(card)
        for card in chosen:
            cs.cards.spend(p, card)
        healed = _heal(p, len(chosen) + len(suits))
    if c.log:
        c.log(unit=pc['name'], action='heal', target=p['name'], amount=healed, target_hp_after=p['health'],
              via='Pressure Point Revitalization', roll=total, defense=11, hit=total >= 11)
    return 2


# ---- Cry of Victory (T062) ----

tq._passive("T062", "Cry of Victory")


@hooks.on('after_hit', 'Cry of Victory', order=80)
def _cry_of_victory(pc, c):
    """T062, "0 AP - Interrupt (you Down a hostile creature)", any number
    of hostile creatures within [Presence Skill Total] meters: "Make a
    Presence attack against the Mental Defense of each target. You
    Frighten each target hit 2 + [Hearts] times." No cost and no limit,
    so every Down from this PC's own attacks sets it off (a Down from a
    bonus attack or a Bleeding tick doesn't, for want of a hook). An enemy
    this PC is Taunting is left out: Frightening it would end the Taunt
    (glossary.md). The flips aren't worth rescuing with cards."""
    cs = tq.cs
    if c.target['health'] > 0:
        return
    for e in c.enemies:
        if e['health'] <= 0 or (e.get('taunted', 0) > 0 and e.get('taunted_by') is pc):
            continue
        if not _near(pc, e, True, pc['skill_totals']['Presence']):
            continue
        defense = e['mental'] - e.get('vulnerable', 0)
        mod = pc['skill_totals']['Presence'] - pc.get('crippled', 0)
        value, pool = cs._pc_flip(pc, mod, defense, pc.get('good_luck', 0), cs._pc_status_bad_luck(pc, e))
        hit = mod + value >= defense
        if hit:
            n = 2 + cs._suit_count(pool, 'Hearts')
            cs._test_rider(pc, e, 'fright', n)  # glossary.md's Frightened, as the effect check applies it
        if c.log:
            c.log(unit=pc['name'], action='taunt', target=e['name'], roll=mod + value, defense=defense, hit=hit,
                  via='Cry of Victory', effects=f"Frightened {e['frightened']}" if hit else None,
                  cards=cs._take_notes(pc))
        pc.pop('_notes', None)


# ---- Heroic Inspiration (T064) ----

tq._encounter("T064", "Heroic Inspiration")


@hooks.on('pc_turn_start', 'Heroic Inspiration', order=55)
def _heroic_inspiration(pc, c):
    """T064, 2 AP, Encounter, any number of allies who can see or hear
    you: "Choose one of the following, [half your Performance Skill Total]
    times: a target is Protected twice (plus once per extra time
    targeted); ...". Cast once enemies are on the party: one pick each for
    the allies in melee (most pressed first), the rest piled on the most
    pressed. Its other two picks (a stack of Taunted or Frightened off, a
    place in turn order) aren't used. Returns the AP spent."""
    cs = tq.cs
    if tq.encounter.left(pc, 'Heroic Inspiration') <= 0 or tq.half(pc, 'Performance') <= 0 or c.ap < 2:
        return 0
    living = [e for e in c.enemies if e['health'] > 0]
    allies = [p for p in c.pcs if p['health'] > 0]

    def pressed(p):
        return sum(1 for e in living if _near(p, e, c.movement_on))
    pool = sorted((p for p in allies if pressed(p) > 0), key=lambda p: (-pressed(p), p['health']))
    if not living or len(pool) < min(2, len(allies)):
        return 0
    picks = tq.half(pc, 'Performance')
    given = {}
    for p in pool[:picks]:
        given[p['name']] = [p, 2]
    for _ in range(picks - len(given)):
        given[pool[0]['name']][1] += 1
    tq.encounter.spend(pc, 'Heroic Inspiration')
    for p, n in given.values():
        cs._gain(p, 'protected', n)
    if c.log:
        c.log(unit=pc['name'], action='technique', via='Heroic Inspiration',
              effects=', '.join(f"{p['name']} Protected +{n}" for p, n in given.values()))
    return 2


# ---- Bolstering Refrain (T066) ----

tq._passive("T066", "Bolstering Refrain")


@hooks.on('pc_turn_start', 'Bolstering Refrain', order=56)
def _bolstering_refrain(pc, c):
    """T066, 2 AP, discard 2 cards, up to [half your Performance Skill
    Total] allies who can see or hear you: "Each target heals 1 Shallow
    Health." Two cards and an attack's AP for a point each, so it's sung
    only when it reaches three hurt allies (or all it can, if that's
    fewer) and one of them is Wounded. Returns the AP spent."""
    cs = tq.cs
    cap = tq.half(pc, 'Performance')
    if cap <= 0 or c.ap < 2 or not _can_pay(pc, 2):
        return 0
    hurt = sorted((p for p in c.pcs if p is not pc and p['health'] > 0 and _missing(p) > 0),
                  key=lambda p: -_missing(p))[:cap]
    if len(hurt) < min(cap, 3) or not any(cs.tactics.pc_wounded(p) for p in hurt):
        return 0
    _pay_card(pc)
    _pay_card(pc)
    healed = {p['name']: _heal(p, 1) for p in hurt}
    if c.log:
        c.log(unit=pc['name'], action='heal', target=', '.join(healed), amount=sum(healed.values()),
              via='Bolstering Refrain')
    return 2


# ---- Rally to Victory (T070) ----

tq._passive("T070", "Rally to Victory")


@hooks.on('pc_turn_end', 'Rally to Victory', order=35)
def _rally_to_victory(pc, c):
    """T070, 1 AP, discard a card for each target, willing allies who can
    see or hear you: "Each target Sifts X cards (X = [half your
    Performance Skill Total]), then discards up to X cards, then draws a
    card for each one discarded." With AP left at the end of a turn, on
    the ally holding the most low cards (2 or more under SIFT_KEEP_RANK,
    the Sift's own line) who still has cards to play this fight; they
    swap those for draws off a freshly Sifted deck. Real cards only.
    Returns the AP spent."""
    cs = tq.cs
    x = tq.half(pc, 'Performance')
    if not cs.T.CARDS or x <= 0:
        return 0
    keep = lambda card: cs.cards.rank(card) >= cs.T.SIFT_KEEP_RANK  # noqa: E731
    spent = 0
    done = set()
    while c.ap - spent >= 1 and cs.cards.can_spend(pc):
        pool = [p for p in c.pcs if p is not pc and p['health'] > 0 and p['name'] not in done
                and p.get('budget', 0) > 0 and sum(1 for card in p['hand'] if not keep(card)) >= 2]
        if not pool:
            break
        p = max(pool, key=lambda p: sum(1 for card in p['hand'] if not keep(card)))
        done.add(p['name'])
        _pay_card(pc)
        spent += 1
        p['deck'].sift(x, keep)
        low = sorted((card for card in p['hand'] if not keep(card)), key=cs.cards.rank)[:x]
        for card in low:
            p['hand'].remove(card)
            p['deck'].discard.append(card)
        p['hand'].extend(p['deck'].draw() for _ in low)
        if c.log:
            c.log(unit=pc['name'], action='technique', target=p['name'], via='Rally to Victory',
                  effects=f"swapped {len(low)} low cards")
    return spent


# ---- The Gatekeeper (T071) ----

tq._encounter("T071", "The Gatekeeper")


@hooks.on('pc_turn_start', 'The Gatekeeper', order=31)
def _gatekeeper(pc, c):
    """T071, 1 AP, Encounter, any number of creatures who can see or hear
    you: "Make a Presence attack against the Mental Defense of each
    target. You Taunt each target hit an infinite number of times. These
    stacks are removed at the end of the encounter." A tank's opener:
    taken by anyone but a Back-liner once two or more enemies aren't
    already Taunted by this PC. "Infinite" is a stack count that never
    decays away within a fight; another Taunter or this PC's own Frighten
    still replaces it (glossary.md). Returns the AP spent."""
    cs = tq.cs
    if tq.encounter.left(pc, 'The Gatekeeper') <= 0 or c.ap < 1 or pc.get('play_style') == 'Back-liner':
        return 0
    pool = [e for e in c.enemies if e['health'] > 0 and e.get('taunted_by') is not pc]
    if len(pool) < 2:
        return 0
    tq.encounter.spend(pc, 'The Gatekeeper')
    for e in pool:
        defense = e['mental'] - e.get('vulnerable', 0)
        mod = pc['skill_totals']['Presence'] - pc.get('crippled', 0)
        value, _ = cs._pc_flip(pc, mod, defense, pc.get('good_luck', 0), cs._pc_status_bad_luck(pc, e),
                               cs.BIG, c.pcs)
        hit = mod + value >= defense
        if hit:
            if e.get('taunted', 0) <= 0 and cs._skips(e):
                e['skip_taunted'] = True
            e['taunted'], e['taunted_by'] = 10 ** 6, pc
            if e.get('frightened_by') is pc:
                e['frightened'], e['frightened_by'] = 0, None
        if c.log:
            c.log(unit=pc['name'], action='taunt', target=e['name'], roll=mod + value, defense=defense, hit=hit,
                  via='The Gatekeeper', effects='Taunted for the encounter' if hit else None,
                  cards=cs._take_notes(pc))
        pc.pop('_notes', None)
    return 1


# ---- Bladeslinging (T073) ----

tq._passive("T073", "Bladeslinging")


@setup_for("Bladeslinging")
def _bladeslinging(name, pc, s):
    """T073: "Wielding a one-handed weapon with two hands makes it
    two-handed (+1 damage)", changing grip for 0 AP. A one-handed melee
    Weapon (blank is 1H Heavy Melee) with nothing else in hand is swung
    two-handed for the +1; the grip goes back to one hand for free when
    grappled, so it never counts as two-handed. Gripping a two-handed
    Weapon one-handed (-1 damage, to keep attacking in a grapple) isn't
    modeled: the sim can't take the 1 off only while grappled."""
    if s.weapon not in ("", "1H Light Melee"):
        return
    if any(w != s.weapon for w in s.sheet.parry_weapons):
        return
    pc['damage'] += 1


# ---- Feint (T074) and Magehunter (T075): combat_sim's own fields ----

tq._encounter("T074", "Feint")
tq._encounter("T075", "Magehunter")


# Feint (T074, 1 AP, Encounter) is in combat_sim's attack loop: a use
# left turns the next weapon attack into the Feint (Vigilant Defense,
# Harried 3 + [Diamonds] on a hit, no damage). It's a setup for the party
# (designer, 2026-10-28): with tunables.FEINT_SETUP it waits for allies
# who can follow up, and a hit calls the target for them.


# Magehunter (T075, 1 AP Interrupt, Encounter) is combat_sim.
# _magehunter_interrupt: an Opportunity Attack on an enemy declaring a
# Spell in reach. Knowing it also gives the PC its Interrupt AP pool.


# ---- Demon School - Sickness Takes the Flock (T083) ----

def _flock(st, sk, atk, dmg):
    # T083, Level 2, 2 AP, Encounter: "Make an Unarmed weapon attack
    # against the target's Vital Defense. If it hits, it deals Shadow
    # damage and the target gains [half your Meditation Skill Total] +
    # [Diamonds] stacks each of Necrotic and Vulnerable." The PC's own
    # Unarmed attack (as for the Shugen strikes); `effect` carries the
    # Vulnerable, `flock_necrotic` the Necrotic (_flock_necrotic).
    n = tq._st(st, sk, "Meditation") // 2
    return dict(skill_total=atk, damage=dmg, dmg_type="Shadow", opp_def="Vital",
                effect=("vulnerable", n, "Diamonds"), skill="Brawl", weapon=True, flock_necrotic=n)


tq._tech_attack("T083", "Demon School - Sickness Takes the Flock", _flock)


@hooks.on('after_hit', order=65)
def _flock_necrotic(pc, c):
    sub = c.substitute
    if sub and sub.get('flock_necrotic'):
        n = sub['flock_necrotic'] + tq.cs._suit_count(c.pool, 'Diamonds')
        tq.cs._gain(c.target, 'necrotic', n)
        c.notes.append(f"Necrotic +{n}")


# ---- Great Old Oak School - Bark Turns the Blade (T086) ----

tq._encounter("T086", "Great Old Oak School - Bark Turns the Blade")


@hooks.on('enemy_hit_damage', order=40)
def _bark_turns_the_blade(e, c):
    """T086, "2 AP - Interrupt (you are hit by an attack, before the attack
    is resolved)", Encounter: "You gain [half your Meditation Skill Total]
    stacks of Protected." The Protected soaks this hit, and what's left
    stays. Taken on a hit that would cost 2 Health or more, or Down the
    PC. Runs before Strike (Devastating) turns what's left into Bleeding."""
    t = c.target
    if tq.encounter.left(t, 'Great Old Oak School - Bark Turns the Blade') <= 0 or c.dmg <= 0:
        return
    n = tq.half(t, 'Meditation')
    if n <= 0:
        return
    if c.dmg < min(n, 2) and c.dmg < t['health']:
        return
    if not _interrupt_ap(t, 2):
        return
    tq.encounter.spend(t, 'Great Old Oak School - Bark Turns the Blade')
    soaked = min(c.dmg, n)
    c.dmg -= soaked
    t['prot_absorbed'] = t.get('prot_absorbed', 0) + soaked
    tq.cs._gain(t, 'protected', n - soaked)
    c.applied.append(f"Protected +{n}, {soaked} soaked (Bark Turns the Blade)")


@hooks.on('enemy_hit_damage', order=95)
def _optimized_blood(e, c):
    # Optimize Blood (T050): the Health this hit would cost becomes
    # Bleeding, up to what's left of the dose.
    t = c.target
    left = t.get('optimize_blood', 0)
    if left <= 0 or c.dmg <= 0:
        return
    n = min(left, c.dmg)
    t['optimize_blood'] -= n
    c.dmg -= n
    tq.cs._apply_to_pc(t, 'Bleeding', n, e)
    c.applied.append(f"Bleeding +{n} (Optimize Blood)")


# ---- Shugen School - Dawn Wind Bends the Grass (T091) ----

def _dawn_wind(st, sk, atk, dmg):
    # T091, Level 3, 2 AP, Encounter, all creatures in a 2-meter cone:
    # "Make a Meditation attack against each target's Mental Defense. If
    # it hits, it deals 2 + [Mind] Brilliant damage and the target is
    # Slowed 2 + [Spades] times." The cone is War Magic's Funnel (`cone`,
    # techniques.shape_targets), and its Slow is War Magic's Frigid at 1
    # ("Slowed [twice X] + [Spades]"), which spell_riders puts on every
    # target the cone hits.
    return dict(skill_total=tq._st(st, sk, "Meditation"), damage=2 + int(st["Mind"]), dmg_type="Brilliant",
                opp_def="Mental", effect=None, skill="Meditation", cone=2, range=2, frigid=1)


tq._tech_attack("T091", "Shugen School - Dawn Wind Bends the Grass", _dawn_wind)


# ---- Great Old Oak School - Sap Seals the Wound (T093) ----

tq._passive("T093", "Great Old Oak School - Sap Seals the Wound")


@hooks.on('pc_turn_end', 'Great Old Oak School - Sap Seals the Wound', order=32)
def _sap_seals(pc, c):
    """T093, 1 AP, discard X cards (at most [half your Meditation Skill
    Total]): "At the start of each of your next X turns, you heal 2
    Health. You also heal 1 Health immediately for each Heart discarded."
    With AP left at the end of a turn, missing 4 or more and no Sap
    running: as many cards as the missing Health needs, Hearts first.
    Returns the AP spent."""
    cs = tq.cs
    if c.ap < 1 or pc.get('sap_turns', 0) > 0 or _missing(pc) < 4:
        return 0
    budget = pc.get('budget', 0) if cs.T.CARDS else pc.get('card_uses_left', 0)
    if cs.T.CARDS:
        budget = min(budget, len(pc['hand']))
    x = min(tq.half(pc, 'Meditation'), budget, math.ceil(_missing(pc) / 2))
    if x <= 0:
        return 0
    hearts = sum(1 for _ in range(x) if _pay_card(pc, cs.cards.HEARTS) == cs.cards.HEARTS)
    pc['sap_turns'] = x
    healed = _heal(pc, hearts)
    if c.log:
        c.log(unit=pc['name'], action='heal', target=pc['name'], amount=healed, target_hp_after=pc['health'],
              via='Sap Seals the Wound', effects=f"2 a turn for {x} turns")
    return 1


@hooks.on('pc_turn_start', 'Great Old Oak School - Sap Seals the Wound', order=2)
def _sap_tick(pc, c):
    if pc.get('sap_turns', 0) > 0:
        pc['sap_turns'] -= 1
        healed = _heal(pc, 2)
        if c.log and healed:
            c.log(unit=pc['name'], action='heal', target=pc['name'], amount=healed, target_hp_after=pc['health'],
                  via='Sap Seals the Wound')
    return 0


# ---- Regaining Encounter uses (2026-10-27): encounter.py's rules ----

@hooks.on('pc_turn_start', order=1)
def _spend_vigor(pc, c):
    # Any Vigor a PC has, from any source (Solemn Covenant below; Warpath
    # and items once they're in), is spent the one way: encounter.py.
    if pc.get('vigor'):
        tq.encounter.spend_vigor(pc, c.log)
    return 0


tq._passive("T022", "Solemn Covenant")


@setup_for("Solemn Covenant")
def _covenant_setup(name, pc, s):
    # T022: "At the start of each encounter, you gain 4 Vigor that lasts
    # for the encounter." Breaking the pact is out of combat.
    pc['vigor'] = pc.get('vigor', 0) + 4


tq._passive("T082", "Great Old Oak School - Willow Springs Back")


@hooks.on('pc_turn_end', 'Great Old Oak School - Willow Springs Back', order=15)
def _willow(pc, c):
    """T082, "X AP (X must be [half your Meditation Skill Total] or
    less)": "Regain the use of an Encounter Technique with a Level of X or
    less." Not an Encounter Technique itself. Paid from AP left at the end
    of a turn: at the start of one it costs an attack, which a regained
    use seldom beats (Felix's fights ran 0.6 rounds longer). X is the
    regained use's Level. Returns the AP spent."""
    enc = tq.encounter
    g = enc.wanted(pc, max_level=min(c.ap, pc['skill_totals']['Meditation'] // 2))
    if g is None:
        return 0
    enc.regain(pc, g, "Willow Springs Back", c.log)
    return max(1, g['level'])


tq._passive("T037", "Placeholder's Alacritous Adaptation")


@hooks.on('pc_turn_start', "Placeholder's Alacritous Adaptation", order=4)
def _alacritous_adaptation(pc, c):
    """T037, "0 AP - Interrupt (any time)", Cost: "Expend the use of any
    number of Discipline/Martial/Spell Encounter Techniques": "You regain
    the use of one Discipline, Martial, or Spell Encounter Technique. The
    regained Technique's Level must be lower than the total Levels of
    Techniques you expended as a cost." encounter.trade_for says which
    uses are worth trading."""
    tq.encounter.trade_for(pc, tq.encounter.KINDS, c.rnd, c.log, "Placeholder's Alacritous Adaptation")
    return 0


# ---- Blood-Powered Spirit (T006) ----

tq._passive("T006", "Blood-Powered Spirit")
_SPELLISH = frozenset(("Spell", "Discipline"))


def _can_bleed(pc, x):
    return (pc['health'] - x) / pc['max_health'] >= tq.cs.T.BLOOD_SPIRIT_HEALTH


@hooks.on('before_attack', 'Blood-Powered Spirit', order=70)
def _blood_spirit_damage(pc, c):
    """T006, "0 AP - Interrupt (you declare a Spell or Discipline
    Technique)", Cost X Health: "(a) Any attack from the Technique deals
    extra X damage if it hits, or [twice X] if single-target". Health is
    paid only to finish a target: the least X that turns this attack's
    hit into a Down, on a damaging Spell or Discipline attack (a
    Technique attack or a War Magic Weapon cast), while the PC stays
    above tunables.BLOOD_SPIRIT_HEALTH. (Paying 1 every cast cost Felix's
    and Beornhard's parties Health for next to nothing.) Its "may change
    it to Shadow" does nothing here: the sim has one elemental Resist."""
    cs, sub, t = tq.cs, c.substitute, c.target
    if c.repeat:
        return 0
    if sub:
        kinds, prof = sub.get('kinds', frozenset()), sub
    elif pc.get('weapon_is_spell'):
        kinds, prof = tq.encounter.kinds_of("War Magic"), pc
    else:
        return 0
    if not kinds & _SPELLISH or prof['damage'] <= 0:
        return 0
    net = prof['damage'] - cs.enemy_resist_for_pc_attack(prof, t) - t.get('protected', 0)
    short = t['health'] - max(0, net)
    if short <= 0:
        return 0
    single = not (sub and (sub.get('line') or sub.get('cone') or sub.get('nova')))
    x = math.ceil(short / 2) if single else short
    if not _can_bleed(pc, x):
        return 0
    pc['health'] -= x
    pc['_attack_bonus'] = pc.get('_attack_bonus', 0) + (2 * x if single else x)
    pc['blood_spirit_paid'] = pc.get('blood_spirit_paid', 0) + x
    cs._note(pc, f"{x} Health for +{pc['_attack_bonus']} damage on a hit (Blood-Powered Spirit)")
    return 0


@hooks.on('pc_turn_start', 'Blood-Powered Spirit', order=5)
def _blood_spirit_cast(pc, c):
    """T006 "(b) If the Technique's Level is [twice X] or lower, you may
    cast it without expending a use, even if already expended": X is half
    the Level, rounded up. Taken for a spent Spell or Discipline attack
    worth having back (encounter.worth_regaining), on the same Health
    rule as (a); getting the use back now and casting it is the same
    thing as casting it without one. Only for one that hits harder than
    the PC's own attack: Felix paid a Health a turn to get back Hand
    Rings the Bell, no bigger than his punch, and lost by it."""
    enc = tq.encounter
    g = enc.wanted(pc, kinds=_SPELLISH)
    if (g is None or not g['attack'] or not enc.worth_regaining(pc, g)
            or g.get('damage', 0) <= pc['damage']):
        return 0
    x = max(1, math.ceil(g['level'] / 2))
    if not _can_bleed(pc, x):
        return 0
    pc['health'] -= x
    pc['blood_spirit_paid'] = pc.get('blood_spirit_paid', 0) + x
    enc.regain(pc, g, f"Blood-Powered Spirit ({x} Health)", c.log)
    return 0
