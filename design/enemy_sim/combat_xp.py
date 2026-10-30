"""How much of a build's XP goes to fights (2026-10-30).

Per the designer: players don't build pure combat characters. At Level 3
(175 XP) assume about 130 goes to things that matter in a fight and 45 to
social Skills, sneaking, fun low-Level Techniques and the like; the test
builds (stand-ins, the optimizer) get the combat share only.

Combat XP is every Stat, the attack and Defense Skills, any Skill named in
techniques.csv's Relevant Skills for a Technique the character uses in a
fight, and every Technique the sim plays in a fight. The rest (other
Skills, out-of-combat Techniques) is the character's life outside fights.
"""
import game_data, party, techniques as tq

COMBAT_BUDGET = {2: 95, 3: 130}   # of 125 / 175
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
