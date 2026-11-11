"""
Enemy stat blocks by name: the monster manual (monster_manual.csv, one
design per monster, built at any Level as "Name@L") and the older sample
roster (sample_enemies.csv, one row per enemy at its Level). Both build
through enemy_builder.build_enemy; this file decides what a row buys
(`_pruned_picks`, `_big_picks`) and holds the encounters the tools play
(ENCOUNTERS, CURRENT_MIXES: the manual's draws by default,
tunables.ENCOUNTER_SOURCE).

`get_enemy(name)` builds one enemy; `build_encounter(names)` a list, for
`combat_sim.run_fight(..., enemies=)`.
"""
import csv
import os

import game_data
import tunables as T
from enemy_builder import build_enemy
import enemy_builder as eb

_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_enemies.csv")


def _load_rows():
    return [dict(r) for r in game_data.csv_rows(_CSV_PATH)]


_MANUAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monster_manual.csv")


def manual_names():
    return [r["Name"] for r in game_data.csv_rows(_MANUAL_PATH)]


def _manual_row(name):
    """'Gravel Ogre@3': the monster manual's design built at Level 3
    (monster_manual.csv, 2026-11-04). Its picks are the pruned v3's."""
    base, _, level = name.partition("@")
    for r in game_data.csv_rows(_MANUAL_PATH):
        if r["Name"] == base:
            return dict(r, Name=name, Level=level, AttackTier="primary", Abilities="", HealthBonus="",
                        FightingStyle="None", PrunedAction=r["Action"], Roster="FALSE")
    return None


def _row_named(name):
    if "@" in name:
        return _manual_row(name)
    # Read-only lookup into the cached rows (game_data.cached_file).
    rows = game_data.csv_rows(_CSV_PATH)
    index = _INDEX.get(id(rows))
    if index is None:
        _INDEX.clear()
        index = _INDEX[id(rows)] = {r["Name"]: r for r in rows}
    return index.get(name)


_INDEX = {}


def _build_from_row(row):
    if "BigPicks" not in row and float(row.get("Slots") or 1) > 1 and T.LEGACY_BIG:
        # The old sample roster's elites and solo boss have no BigPicks to
        # spend a bigger budget on, so they keep the settings they were
        # tuned with (tunables.LEGACY_BIG).
        saved = {k: getattr(T, k) for k in T.LEGACY_BIG}
        for k, v in T.LEGACY_BIG.items():
            setattr(T, k, v)
        try:
            return _build_from_row(dict(row, BigPicks=""))
        finally:
            for k, v in saved.items():
                setattr(T, k, v)
    if T.V3_HEAVY_MIN_LEVEL and row["Armor"].strip() == "Heavy" and int(row["Level"]) < T.V3_HEAVY_MIN_LEVEL:
        # Heavy armor only from this Level (designer, 2026-11-08): below it a
        # Heavy design wears Medium, and the points it saves are Health.
        row = dict(row, Armor="Medium")
    abilities, action = _pruned_picks(row, _split(row["Abilities"]))
    e = build_enemy(row["Name"], int(row["Level"]), float(row["Slots"]), action, row["Armor"],
                    row["StrongDefense"].strip(), role=(row.get("Role") or "").strip() or None,
                    abilities=abilities, main_effect=(row.get("MainEffect") or "").strip() or None,
                    backup_action=(row.get("BackupAction") or "").strip() or None,
                    weak_defense=(row.get("WeakDefense") or "").strip() or None)
    e["battle_tactic"] = row["BattleTactic"]
    e["fighting_style"] = "None"
    style = T.V3_FIGHTING_STYLE
    if style:
        e["fighting_style"] = (("Single" if T.AUDIT_FIXES and e.get("kind", "attack") != "attack" else
                                "Aimed Shot" if e.get("attack_range") else "Skirmisher") if style == "mixed"
                               else style)
    return e


def _split(cell):
    return [a.strip() for a in (cell or "").split(";") if a.strip()]


def _pruned_picks(row, abilities):
    """The pruned v3 (2026-11-04): a redesigned row (PrunedPicks) names its
    loadout (PrunedAction) and every Ability it buys; any other row keeps
    its own Abilities and buys back the Damage and Accuracy the base table
    gave up, so it plays as it did. tunables.V3_PRUNED_EXTRA gives a Level
    more points, spent down the row's PrunedExtra list in order (a pick
    that doesn't fit what's left is skipped; what's left is Health)."""
    buyback = ["Damage +1", "Accuracy +1"]
    designed = _split(row.get("PrunedPicks"))
    in_table = int(row["Level"]) >= T.V3_ACCURACY_IN_TABLE
    if in_table:
        # The table carries this Accuracy +1 from that Level (2026-11-08).
        buyback = ["Damage +1"]
    if not designed:
        return abilities + buyback, row["Action"]
    picks = list(designed)
    left = T.V3_PRUNED_EXTRA.get(int(row["Level"]), 0)
    action = (row.get("PrunedAction") or "").strip() or row["Action"]
    # One budget: the extra points buy only what the design leaves room
    # for; points the design leaves unspent stay Health.
    cost = (sum(eb.ABILITY_PRICES[p] for p in picks) + eb.ARMOR_PRICES[row["Armor"].strip()]
            + eb.LOADOUT_PRICES.get(action, 0))
    left = min(left, T.V3_PRUNED_ALLOWANCE + left - cost)
    # Extra points on offense first (Accuracy, then Damage), then the row's own.
    order = (([] if in_table else ["Accuracy +1"]) + ["Damage +1"]
             + [p for p in _split(row.get("PrunedExtra")) if p not in ("Accuracy +1", "Damage +1")])
    for pick in order:
        price = eb.ABILITY_PRICES[pick]
        n = picks.count(pick)
        rider = pick.startswith("Strike (") or pick.startswith("Poison (")
        # A pick the row already has that can't be taken again (Damage +1
        # once; a rider at its cap) is skipped, as BigPicks' are.
        if n and not rider and pick not in eb.REPEATABLE:
            continue
        if rider and n >= (eb.POISON_CAP if pick.startswith("Poison (") else eb.RIDER_CAP):
            continue
        if price <= left:
            picks.append(pick)
            left -= price
    picks += _big_picks(row, picks)
    return picks, action


# Picks that make an enemy tougher rather than more dangerous: the points a
# size adds can't buy them (designer, 2026-11-06; on a big enemy they're
# far too cheap, experiments/enemies/big_enemy_options.py).
BIG_PICKS_BARRED = {"Dodge +1", "Parry and Dodge +1", "Vital/Mental/Vigilant +1", "Resist +1", "Durable",
                    "Omniguard", "Resilient", "Enhanced Health", "Sturdy"}


def _big_picks(row, picks):
    """An elite's or solo boss's extra points (tunables.V3_SLOT_BUDGET:
    k times the budget, so k - 1 more of it), spent down the row's
    BigPicks list in order: a pick that doesn't fit what's left, or would
    pass a cap, is skipped; what's left is Health. Offense, on-hit effects
    and Actions only."""
    k = T.V3_SLOT_BUDGET.get(float(row["Slots"]), 1)
    if k <= 1:
        return []
    level = int(row["Level"])
    left = (T.V3_PRUNED_ALLOWANCE + T.V3_PRUNED_EXTRA.get(level, 0)) * (k - 1)
    t = eb.ENEMY_TABLE[level]
    role_acc = eb.ROLE_ADDS.get((row.get("Role") or "").strip(), {}).get("acc", 0)
    out, have = [], list(picks)
    for p in _split(row.get("BigPicks")):
        if p in BIG_PICKS_BARRED or p.startswith("Resist ("):
            raise ValueError(f"{row['Name']}: {p} can't be bought with the points a size adds")
        price = eb.ABILITY_PRICES[p]
        n = have.count(p)
        rider = p.startswith("Strike (") or p.startswith("Poison (")
        if price > left + 1e-9:
            continue
        if rider and n >= (eb.POISON_CAP if p.startswith("Poison (") else eb.RIDER_CAP):
            continue
        if n and not rider and p not in eb.REPEATABLE:
            continue
        if p == "Accuracy +1" and t["accuracy"] + role_acc + n + 1 > eb.SKILL_CAP:
            continue
        out.append(p)
        have.append(p)
        left -= price
    return out


def get_enemy(name):
    row = _row_named(name)
    if row is not None:
        if T.ENEMY_LEVEL_UP:
            # tunables.ENEMY_LEVEL_UP: the same row, built Levels higher.
            row = dict(row, Level=str(int(row["Level"]) + T.ENEMY_LEVEL_UP))
        return _build_from_row(row)
    raise KeyError(f"no sample_enemies.csv row named {name!r}")


def all_enemies():
    return [_build_from_row(row) for row in _load_rows()]


# The old sample roster's encounter mixes (2026-09-30 enemy-variety pass):
# most fights two stat blocks, a complicated one three, never more than one
# enemy that doesn't attack. Kept for ENCOUNTER_SOURCE 'roster' and the
# replays; the manual's draws (below) are what the tools play.
def _lv(name, level):
    return name if level == 1 else f"{name} (L{level})"


ENCOUNTERS = {
    level: {
        # 2026-09-30, per the designer's own habits: most fights use two
        # stat blocks, a complicated one three, and never more than one
        # enemy that doesn't attack (a healer or debuffer). Two or more
        # non-attackers made fights drag.
        "Frontline": [_lv(n, level) for n in ("Brute", "Brute", "Grave Caller", "Grave Caller")],
        "Shield Wall": [_lv(n, level) for n in ("Hedge Knight", "Hedge Knight", "Marsh Archer", "Marsh Archer")],
        "Warband": [_lv(n, level) for n in ("Brute", "Skulking Footpad", "Skulking Footpad", "Warpriest")],
        # The Slot rule: 4 PCs = 4 Slots; each Minion is 0.5.
        # Two casters behind the minions: with a Hexer in the second
        # slot, nearly all of Horde's damage came from one caster
        # (2026-10-01 horde_experiments.py).
        "Horde": [_lv(n, level) for n in ("Goblin Cutthroat", "Goblin Cutthroat", "Goblin Cutthroat",
                                          "Goblin Cutthroat", "Ember Caster", "Ember Caster")],
    }
    for level in (1, 2, 3)
}
# The old roster's mixes, everything up to 2026-11-09 was tuned on.
ROSTER_MIXES = ("Frontline", "Shield Wall", "Warband", "Horde")


def manual_encounters(level, k, seed=1):
    """`k` encounters from the monster manual by the variety standard
    (ENEMY_ENCOUNTER_DESIGN.md): 4 Slots, two stat blocks usually and three
    sometimes, at most one enemy that doesn't attack; the solo boss alone,
    added from Level 3 (the k draws never include it). Moved here from
    manual_check.encounters, unchanged."""
    import itertools
    import random
    rng = random.Random(seed * 100 + level)
    ms = {}
    for n in manual_names():
        e = get_enemy(f"{n}@3")
        ms[n] = dict(slots=float(e.get("slots", 1)), passive=e["kind"] != "attack")
    pool = [n for n, m in ms.items() if m["slots"] != 4.0]
    out, seen = [], set()
    while len(out) < k:
        picks = rng.sample(pool, 2 if rng.random() < 0.6 else 3)
        options = []
        for counts in itertools.product(range(1, 9), repeat=len(picks)):
            if abs(sum(c * ms[p]["slots"] for c, p in zip(counts, picks)) - 4) > 1e-9:
                continue
            if sum(c for c, p in zip(counts, picks) if ms[p]["passive"]) > 1:
                continue
            options.append(counts)
        if not options:
            continue
        counts = rng.choice(options)
        enc = tuple(sorted(n for c, p in zip(counts, picks) for n in [p] * c))
        if enc not in seen:
            seen.add(enc)
            out.append(enc)
    if level >= 3:
        out += [tuple(n for n, m in ms.items() if m["slots"] == 4.0)]
    return out


def install_manual_mixes(level_into=None, build_level=None):
    """Registers tunables.MANUAL_MIXES manual encounters as "Manual 1".. and
    returns their keys. By default at each Level 1-5, built at that Level
    (a tool at Level 4-5 that raises Level 3's fights with ENEMY_LEVEL_UP
    gets Level 3's draw built higher). `level_into`/`build_level`: one
    Level's draw, built at `build_level`, filed under ENCOUNTERS[level_into]
    (table_check's days at Levels 4-5, with ENEMY_LEVEL_UP 0)."""
    up, T.ENEMY_LEVEL_UP = T.ENEMY_LEVEL_UP, 0
    try:
        levels = [build_level] if build_level else [1, 2, 3, 4, 5]
        for L in levels:
            encs = manual_encounters(L, T.MANUAL_MIXES)[:T.MANUAL_MIXES]
            keys = []
            for i, e in enumerate(encs):
                keys.append(f"Manual {i + 1}")
                ENCOUNTERS.setdefault(level_into or L, {})[keys[-1]] = [f"{x}@{L}" for x in e]
    finally:
        T.ENEMY_LEVEL_UP = up
    return tuple(keys)


# The mixes current scripts should run (tunables.ENCOUNTER_SOURCE).
CURRENT_MIXES = ROSTER_MIXES

# Boss fights (2026-10-07), Level 2 only: a long-lived target, which is
# where Bleeding should pay off most. Solo Boss is one 4-slot boss with
# two turns a round (tunables.TURNS_BY_SLOTS); Boss and Guards is a
# 2-slot boss plus two standard Brutes. Both are 4 Slots. Not in CURRENT_MIXES.
ENCOUNTERS[2]["Solo Boss"] = ["Brute Warlord (L2)"]
ENCOUNTERS[2]["Boss and Guards"] = ["Brute Boss (L2)", "Brute (L2)", "Brute (L2)"]
BOSS_MIXES = ("Solo Boss", "Boss and Guards")

# Dangerous fights (2026-10-21, effect_check.py's --set chief): a Level 1
# mix at 1.5 times the slots, with a 2-slot Brute Chief leading it. Here
# for the replays; the effect check builds all four itself.
ENCOUNTERS[1]["Chief's Frontline"] = ["Brute Chief"] + ENCOUNTERS[1]["Frontline"]


def build_encounter(names):
    """The named enemies, in order, for run_fight's `enemies=`."""
    return [get_enemy(name) for name in names]


if __name__ == "__main__":
    for e in all_enemies():
        print(e["level"], e["name"], "|", e["role"], "|", e["battle_tactic"], "|", e["fighting_style"],
              "| Acc", e["accuracy"], "| Dmg", e["attack_damage"], e["dmg_type"],
              "| Parry", e["parry"], "Mental", e["mental"], "| PhysRes", e["physres"], "| HP", e["health"])


if T.ENCOUNTER_SOURCE == "manual":
    # Done last so every helper above exists; the manual's encounters
    # replace the roster's four as what the shared tools play.
    CURRENT_MIXES = install_manual_mixes()
