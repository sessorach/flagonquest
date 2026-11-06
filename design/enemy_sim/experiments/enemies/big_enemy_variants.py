"""Why some big enemies are walls and some pushovers (2026-11-06).

Follows big_enemy_options.py, whose test designs came out far apart: the
two Defenders in Heavy armor (Iron Colossus, Black Knight) can't be
beaten, the two ranged bosses (Lich Sovereign, Dread Huntress) barely
threaten anyone. Here each gets one change at a time (armor, tactic,
loadout, what its bigger budget buys), at today's setting and the two
candidates, and draws (30 rounds with both sides standing) are counted
apart from losses. The Warlord also gets three spending orders, to see
how much the GM's choice of picks moves a boss.

    python3 experiments/enemies/big_enemy_variants.py run
    python3 experiments/enemies/big_enemy_variants.py read --txt results/enemy_stats/big_enemy_variants.txt
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import statistics as st

import _paths  # noqa: E402,F401
import tunables as T  # noqa: E402
import combat_sim as cs  # noqa: E402
import day_sim as ds  # noqa: E402
import party  # noqa: E402
import sample_enemies as se  # noqa: E402
import table_check as tc  # noqa: E402
import progression_sweep as ps  # noqa: E402
import big_enemy_options as b  # noqa: E402

V = {}  # variant name -> (base design, row changes, big list or None)


def variant(name, base, big=None, **changes):
    V[name] = (base, changes, big)


TAUNT_FREE = "Strike (Crippling); Strike (Crippling); Omniguard; Sturdy; Resilient; Strike (Battering)"
for wall in ("Iron Colossus", "Black Knight"):
    variant(f"{wall} [Medium armor]", wall, Armor="Medium")
    variant(f"{wall} [Light armor]", wall, Armor="Light")
    variant(f"{wall} [Hit Whatever]", wall, BattleTactic="Hit Whatever")
    variant(f"{wall} [no Taunting]", wall, big=[p for p in b.BIG[wall] if "Taunting" not in p],
            PrunedPicks=TAUNT_FREE if wall == "Iron Colossus" else "Strike (Crippling); Strike (Crippling); "
                                                                     "Omniguard; Sturdy")
    variant(f"{wall} [Bruiser]", wall, Role="Bruiser")
    variant(f"{wall} [Medium, Hit Whatever, no Taunting]", wall, big=[p for p in b.BIG[wall] if "Taunting" not in p],
            Armor="Medium", BattleTactic="Hit Whatever",
            PrunedPicks=TAUNT_FREE if wall == "Iron Colossus" else "Strike (Crippling); Strike (Crippling); "
                                                                     "Omniguard; Sturdy")
variant("Dread Huntress [Hit Whatever]", "Dread Huntress", BattleTactic="Hit Whatever")
variant("Dread Huntress [Assassin]", "Dread Huntress", BattleTactic="Assassin")
variant("Dread Huntress [Heavy Bow]", "Dread Huntress", Action="Heavy Bow")
variant("Dread Huntress [Heavy Bow, Hit Whatever]", "Dread Huntress", Action="Heavy Bow", BattleTactic="Hit Whatever")
DEFENSIVE = ["Durable", "Parry and Dodge +1", "Vital/Mental/Vigilant +1", "Parry and Dodge +1", "Resist +1",
             "Enhanced Reflexes", "Parry and Dodge +1", "Vital/Mental/Vigilant +1"]
OFFENSIVE = ["Damage +1", "Accuracy +1", "Accuracy +1", "Strike (Vulnerable)", "Strike (Vulnerable)"]
variant("Lich Sovereign [Light armor]", "Lich Sovereign", Armor="Light")
variant("Lich Sovereign [defense first]", "Lich Sovereign", big=DEFENSIVE)
variant("Lich Sovereign [offense first]", "Lich Sovereign", big=OFFENSIVE + ["Attunement (Shadow)", "Strike (Frightening)",
                                                                             "Strike (Frightening)"])
variant("Lich Sovereign [melee backup]", "Lich Sovereign", BackupAction="Sword and Shield")
variant("Brute Warlord [defense first]", "Brute Warlord", big=DEFENSIVE)
variant("Brute Warlord [offense first]", "Brute Warlord",
        big=["Damage +1", "Powerful Weapon", "Accuracy +1", "Accuracy +1", "Strike (Battering)", "Enhanced Speed"])
variant("Brute Warlord [Health]", "Brute Warlord", big=[])  # spends nothing more: the bigger budget is Health

BASES = ["Iron Colossus", "Black Knight", "Dread Huntress", "Lich Sovereign", "Brute Warlord"]

# --prices: what one more pick is worth on a solo boss, in its own Health.
# The Warlord at today's setting buys it (paying its price from Health as
# usual); the plain Warlord at other Health multiples is the yardstick.
WARLORD = "Strike (Cleaving); Action (Parting Shot); Action (Intimidating)"
PRICE = {}
for n_ in (1, 2, 3):
    PRICE[f"Brute Warlord [+{n_} Parry and Dodge]"] = "; Parry and Dodge +1" * n_
PRICE["Brute Warlord [+2 Vital/Mental/Vigilant]"] = "; Vital/Mental/Vigilant +1" * 2
PRICE["Brute Warlord [+1 Resist]"] = "; Resist +1"
PRICE["Brute Warlord [+1 Damage]"] = "; Damage +1"
PRICE["Brute Warlord [+2 Accuracy]"] = "; Accuracy +1" * 2
PRICE["Brute Warlord [+4 Frightening]"] = "; Strike (Frightening)" * 4
PRICE_HP = [4, 5, 6, 7, 8, 9]


def install_variants():
    rows = b.rows()
    for name, extra in PRICE.items():
        rows[name] = dict(rows["Brute Warlord"], Name=name, PrunedPicks=WARLORD + extra)
        b.BIG[name] = []
    for name, (base, changes, big) in V.items():
        rows[name] = dict(rows[base], Name=name, **changes)
        b.BIG[name] = b.BIG[base] if big is None else big


def filler_off(name):
    # "[Health]" leaves the extra unspent, so it goes to Health.
    return V.get(name, (None, None, None))[2] == []


SETS = {4: [(1, 6), (2, 3.5), (2, 4)], 2: [(1, 3), (2, 2), (2, 2.5)]}


def cases(prices=False):
    out = []
    if prices:
        for L in (3, 4, 5):
            for name in PRICE:
                out.append(dict(design=name, level=L, scale=1, hp=6, slots=4, enc=[name]))
            for h in PRICE_HP:
                out.append(dict(design="Brute Warlord", level=L, scale=1, hp=h, slots=4, enc=["Brute Warlord"]))
        return out
    for name in BASES + list(V):
        base = V[name][0] if name in V else name
        slots = 4 if base in b.BOSSES else 2
        for L in ((3, 4, 5) if slots == 4 else (2, 3, 4, 5)):
            for s, h in SETS[slots]:
                out.append(dict(design=name, level=L, scale=s, hp=h, slots=slots,
                                enc=[name] if slots == 4 else [name, name]))
    return out


_W = []
FILLER = list(b.FILLER)
FLOOR = T.V3_HEALTH_FLOOR


def _job(args):
    c, budget, gi, n, seed = args
    b.install()
    install_variants()
    b.FILLER = [] if filler_off(c["design"]) else FILLER
    if not getattr(cs, "_winner_wrapped", False):
        orig = cs.run_fight

        def rf(*a, **k):
            r = orig(*a, **k)
            _W.append(r["winner"])
            return r
        cs.run_fight, cs._winner_wrapped = rf, True
    T.ENEMY_LEVEL_UP = 0
    # A price pick can take the Warlord under the usual Health floor; the
    # measurement wants the plain trade (kit_check did the same).
    T.V3_HEALTH_FLOOR = 0 if c["design"] in PRICE else FLOOR
    b.setting(c["slots"], c["scale"], c["hp"])
    L = c["level"]
    gname, pnames, swaps = tc.groups(L, budget)[gi]
    lvl = min(L, 3)
    se.ENCOUNTERS.setdefault(lvl, {})["_test"] = [f"{x}@{L}" for x in c["enc"]]
    prow = party._rows()
    out = collections.Counter()
    for k in range(n):
        del _W[:]
        rec, _ = ds.play_day(pnames, swaps, lvl, ("_test",), seed + 1000 * k, prow)
        f = rec["per_fight"][0]
        out["won"] += f["won"]
        out["draw"] += _W[0] == "draw"
        out["down"] += f["downs"] > 0
        out["down2"] += f["downs"] > 1
        out["rounds"] += f["rounds"]
    big = se.get_enemy(f"{c['design']}@{L}")
    return dict(c, budget=budget, party=gname, n=n, health=big["max_health"], parry=big["parry"],
                dodge=big["dodge"], physres=big["physres"], accuracy=big["accuracy"], damage=big["attack_damage"],
                picks=b.picks_for(c["design"], L),
                **{k: out[k] / n for k in ("won", "draw", "down", "down2", "rounds")})


def key(r):
    return (r["design"], r["level"], r["scale"], r["hp"], r["party"])


def run(a):
    done = set()
    if os.path.exists(a.o):
        done = {key(r) for r in map(json.loads, open(a.o)) if r}
    jobs = []
    for c in cases(a.prices):
        b_ = ps.MID[c["level"]]
        for gi, (gname, _, _) in enumerate(tc.groups(c["level"], b_)):
            if key(dict(c, party=gname)) not in done:
                jobs.append((c, b_, gi, a.n, a.seed))
    print(len(jobs), "jobs", flush=True)
    with mp.Pool(a.j, maxtasksperchild=50) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=2)):
            with open(a.o, "a") as f:
                f.write(json.dumps(r) + "\n")
            if i % 250 == 0:
                print(i, flush=True)


def read(a):
    recs = [json.loads(l) for l in open(a.o) if l.strip()]
    g = collections.defaultdict(list)
    for r in recs:
        g[(r["design"], r["scale"], r["hp"])].append(r)
    out = ["| Design | Setting | Lost | of which draws | Down | 2+ Down | Rounds | Health / Parry / Dodge / Resist / Acc / Dmg (L4) |",
           "|---|---|---|---|---|---|---|---|"]
    for name in BASES + list(V):
        base = V[name][0] if name in V else name
        slots = 4 if base in b.BOSSES else 2
        for s, h in SETS[slots]:
            rs = g.get((name, s, h))
            if not rs:
                continue
            l4 = next((r for r in rs if r["level"] == 4), rs[0])
            lost = 1 - st.mean(r["won"] for r in rs)
            out.append(f"| {name} | x{s}, Health x{h} | {100 * lost:.0f}% | {100 * st.mean(r['draw'] for r in rs):.0f}% | "
                       f"{100 * st.mean(r['down'] for r in rs):.0f}% | {100 * st.mean(r['down2'] for r in rs):.0f}% | "
                       f"{st.mean(r['rounds'] for r in rs):.1f} | {l4['health']} / {l4['parry']} / {l4['dodge']} / "
                       f"{l4['physres']} / {l4['accuracy']} / {l4['damage']} |")
    text = "\n".join(out)
    print(text)
    if a.txt:
        open(a.txt, "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("run", "read"))
    ap.add_argument("-o", default="results/enemy_stats/big_enemy_variants.jsonl")
    ap.add_argument("--txt")
    ap.add_argument("--prices", action="store_true")
    ap.add_argument("-n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=41)
    ap.add_argument("-j", type=int, default=os.cpu_count())
    a = ap.parse_args()
    {"run": run, "read": read}[a.cmd](a)


if __name__ == "__main__":
    main()
