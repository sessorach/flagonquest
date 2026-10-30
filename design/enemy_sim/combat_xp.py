"""How much of a build's XP goes to fights (2026-10-30).

Per the designer: players don't build pure combat characters. At Level 3
(175 XP) assume about 145 goes to things that matter in a fight (the
mid-tier focal point for balance) and the rest to social Skills,
sneaking, fun low-Level Techniques and the like; 105 of 125 at Level 2.
Every test build gets exactly the combat share (normalize()), so
archetypes compare at the same combat XP: what Carrick or Hilde would
look like if they put the same into fights.

Combat XP is every Stat, the attack and Defense Skills, any Skill named in
techniques.csv's Relevant Skills for a Technique the character uses in a
fight, and every Technique the sim plays in a fight. The rest (other
Skills, out-of-combat Techniques) is the character's life outside fights.
"""
import game_data, party, techniques as tq

COMBAT_BUDGET = {2: 105, 3: 145}  # of 125 / 175 (designer, 2026-10-30: 145 is the mid-tier focal point)
CORE_SKILLS = {"Melee", "Archery", "Brawl", "Acrobatics", "Resilience", "Composure", "Insight", "Might",
               "Sorcery", "Theurgy", "Meditation"}
HEALTH_ONLY = {"T014", "T023"}    # in OUT_OF_COMBAT only because the loader adds their Health


def in_fight(tid, unmodeled=()):
    return not ((tid in tq.OUT_OF_COMBAT and tid not in HEALTH_ONLY) or game_data.technique_name(tid) in unmodeled)


def split(build, unmodeled=()):
    """(combat XP, other XP, the combat Skills)."""
    techs = build["techniques"]
    skills = set(CORE_SKILLS)
    for t in techs:
        if in_fight(t["id"], unmodeled):
            rel = game_data.techniques()[t["id"]].get("Relevant Skills") or ""
            skills |= {s.strip() for s in rel.split(",") if s.strip()}
    stat = sum(v * (v + 1) for v in map(int, build["statPoints"].values()))
    sk_c = sum(int(v) * (int(v) + 1) // 2 for k, v in build["skillPoints"].items() if k in skills)
    sk_o = sum(int(v) * (int(v) + 1) // 2 for k, v in build["skillPoints"].items() if k not in skills)
    te_c = sum(3 * party.tech_level(t) for t in techs if in_fight(t["id"], unmodeled))
    te_o = sum(3 * party.tech_level(t) for t in techs if not in_fight(t["id"], unmodeled))
    return stat + sk_c + te_c, sk_o + te_o, skills


CAP = {2: 4, 3: 5}
_RAISE = ("Essence", "Resilience", "Insight", "Composure", "Acrobatics", "Melee")


def normalize(build, level, attack_skill, unmodeled=()):
    """`build` brought to exactly COMBAT_BUDGET[level] combat XP (at most 2
    under), keeping who the character is. Over: the highest combat ranks
    come down one at a time, never the attack Skill, its Stat or anything a
    prereq needs; then the most recent combat Technique goes. Under: the
    attack Skill and its Stat go up, then Essence and the Defense Skills, in
    turn. Returns (build, notes)."""
    import copy
    import tunables as T
    b = copy.deepcopy(build)
    budget, cap = COMBAT_BUDGET[level], CAP[level]
    keep = {attack_skill, T.PC_SKILL_STAT.get(attack_skill)}
    notes, locked = [], set()

    def box(k):
        return b["statPoints"] if k in b["statPoints"] else b["skillPoints"]
    for _ in range(500):
        c, _o, skills = split(b, unmodeled)
        if budget - 2 <= c <= budget:
            break
        if c > budget:
            cands = [k for k in list(b["statPoints"]) + [k for k in b["skillPoints"] if k in skills]
                     if k not in keep and k not in locked and int(box(k)[k]) > (1 if k in b["statPoints"] else 0)]
            if cands:
                k = max(cands, key=lambda k: (int(box(k)[k]), k in b["skillPoints"]))
                box(k)[k] = int(box(k)[k]) - 1
                if party.prereq_needs(b):
                    box(k)[k] = int(box(k)[k]) + 1
                    locked.add(k)
                else:
                    notes.append(f"{k} -1")
                continue
            fights = [i for i, t in enumerate(b["techniques"]) if in_fight(t["id"], unmodeled)]
            if not fights:
                break
            t = b["techniques"].pop(fights[-1])
            notes.append(f"dropped {game_data.technique_name(t['id'])}")
            locked.clear()
            continue
        left = budget - c
        order = [attack_skill, T.PC_SKILL_STAT.get(attack_skill)] + list(_RAISE)
        for k in order:
            v = int(box(k)[k])
            cost = 2 * (v + 1) if k in b["statPoints"] else v + 1
            if v < cap and cost <= left:
                box(k)[k] = v + 1
                notes.append(f"{k} +1")
                break
        else:
            break
    return b, notes
