"""Every buff and debuff in the sim, priced against THE TABEL (2026-10-21).

Per the designer: check all the buffs and debuffs with the sim, since
most of THE TABEL's weights for them are model-based (Pencil) and some
were never measured, and flag anything that lands well outside its
estimate.

The method is turnorder_single.py's, at Level 1 (the table-matched
setup): one PC of Party A carries the test, and the score is the party's
expected Health left over the four mixes (Health left on a win, losses
count 0), paired seeds against the same party without it. A Health
ladder (+2 Health on every PC) turns the difference into Value: one PC's
+1 Health is a quarter of the ladder's slope per point, worth 4 Value
(THE TABEL's Health). Every PC in the party takes a turn as the carrier,
since what an effect is worth depends a lot on who has it.

The tests are combat_sim's "Test:<effect>:<n>:<mode>" passives (see
_test_effects): n stacks on the carrier's first hit each fight, or a
stack on every hit; buffs on the carrier at the start of its first turn,
or every turn. Stat tests change the carrier's numbers directly, and the
Autoswing control (one extra attack a fight, THE TABEL's 5.5) checks the
scale. Vulnerable only matters to attacks against Vital, Mental and
Vigilant, which nobody in the Level 1 parties makes with their weapon,
so it's also measured in Party A with every weapon attack against Vital
(party "AV").

Each test gets three numbers, all a fight's worth, averaged over the four
carriers: THE TABEL's price (its value for one application, times
applications a fight), THE TABEL's own unit rates times what the sim
counted the test doing (attack points, stack-turns, Health stopped or
landed - exposure_price), and the measured Value. The middle one checks
THE TABEL's assumptions about how much an effect gets used (windows,
survival, rate of use) apart from what a use is worth; the measured one
also picks up what the counts miss (who gets attacked instead, longer
or shorter fights).

Enemy Health x1.75 is table toughness, the setting the Bleeding prices
use (2026-10-19); x1 is the sim as built.

    python3 effect_check.py                  # everything, both settings
    python3 effect_check.py -e crippled -e taunt
    python3 effect_check.py -n 500 -m 1.75   # fights per mix, one setting
    python3 effect_check.py --csv out.csv    # also every cell, for digging"""
import argparse
import ast
import csv
import math
import os
import statistics as st
import sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combat_sim as cs, sample_enemies as se, party, tunables as T

NAMES = ["Hilde", "Browndog", "Carrick", "Sable"]
PARTIES = {"A": NAMES, "AV": NAMES}
HEALTH_VALUE = 4
CHUNK = 250

# THE TABEL's price for one application of n stacks (balance_weights.csv,
# balance_weights_notes.md's Debuff bucket). Ward's assumes a fight where
# its damage type matters, per its own derivation.
TABEL = {
    "crippled": {1: 1.5, 2: 4.5, 4: 15},
    "vulnerable": {1: 1, 2: 3, 4: 10},
    "slowed": {1: 1.1, 2: 3.3, 4: 11},
    "hasted": {1: 0.55, 2: 1.65, 4: 5.5},
    "harried": {1: 1, 2: 2, 4: 4},
    "taunt": {1: 2.2, 2: 4.4, 4: 8.8},
    "fright": {1: 2.2, 2: 4.4, 4: 8.8},
    "badluck": {1: 2.2, 2: 4.4, 4: 8.8},
    "push": {n: 0.89375 * n for n in (1, 2, 3, 4)},
    "pushmay": {n: 0.89375 * n for n in (1, 2, 3, 4)},
    "stagger": {1: 1.35, 2: 2.7, 4: 5.4},
    "necrotic": {1: 3, 2: 6, 4: 12},
    "bleeding": {1: 4, 2: 8, 4: 11},
    "protected": {1: 3, 2: 6, 4: 12},
    "ward_fire": {1: 2.72, 2: 5.28, 4: 9.92},
    "ward_shadow": {1: 2.36, 2: 4.64, 4: 8.96},
    "goodluck": {1: 2.4, 2: 3.6},
}
ON_HIT = ("crippled", "slowed", "harried", "taunt", "fright", "badluck", "push", "pushmay", "stagger", "necrotic",
          "bleeding")
ON_SELF = ("protected", "hasted", "ward_fire", "ward_shadow")


def variants():
    """(label, effect, spec) for every test. spec: a Test passive string,
    or a dict of stat changes / flags."""
    out = []
    for eff in ON_HIT:
        for n in (1, 2, 4):
            out.append((f"{eff} {n}, first hit", eff, f"Test:{eff}:{n}:first"))
        out.append((f"{eff} 1, every hit", eff, f"Test:{eff}:1:hit"))
    out.append(("push 3, every hit", "push", "Test:push:3:hit"))
    out.append(("pushmay 3, every hit", "pushmay", "Test:pushmay:3:hit"))
    for eff in ON_SELF:
        for n in (1, 2, 4):
            out.append((f"{eff} {n}, first turn", eff, f"Test:{eff}:{n}:first"))
        out.append((f"{eff} 1, every turn", eff, f"Test:{eff}:1:turn"))
    out += [("goodluck 1, first attack", "goodluck", "Test:goodluck:1:first"),
            ("goodluck 2, first attack", "goodluck", "Test:goodluck:2:first"),
            ("goodluck 1, every turn", "goodluck", "Test:goodluck:1:turn")]
    out += [("Health +2", "stat", {"health": 2}),
            # Health is Deep Health in the sim (Shallow is a flat 5); THE
            # TABEL prices a point of Shallow at 5 and Deep at 4.
            ("Shallow Health +1", "stat", {"health": 1, "shallow_max": 1}),
            ("Damage +1", "stat", {"damage": 1}),
            ("Accuracy +1", "stat", {"skill_total": 1}),
            ("Parry/Dodge +1", "stat", {"parry": 1, "dodge": 1}),
            ("Physical Resist +1", "stat", {"physres": 1}),
            ("Speed +1", "stat", {"speed": 1}),
            ("Autoswing", "stat", {"bonus_attack_control": True}),
            ("Damage +1, first hit", "stat", {"passive": "Damage Once"})]
    return out


VULN = [(f"vulnerable {n}, first hit", "vulnerable", f"Test:vulnerable:{n}:first") for n in (1, 2, 4)] + \
       [("vulnerable 1, every hit", "vulnerable", "Test:vulnerable:1:hit")]

_LAST = [None]


def make(pname, carrier, spec, health_all):
    rows = {r["Name"]: r for r in party._load_rows()}

    def mk(t, good_luck=0):
        pcs = []
        for i, n in enumerate(PARTIES[pname], 1):
            row = dict(rows[n])
            row["Health"] = str(int(row["Health"]) + health_all)
            pc = party._pc_dict(row, i, good_luck)
            if pname == "AV":
                pc["opp_def"] = "Vital"
            if n == carrier and spec:
                if isinstance(spec, str):
                    pc["passives"] = list(pc["passives"]) + [spec]
                else:
                    for k, v in spec.items():
                        if k == "passive":
                            pc["passives"] = list(pc["passives"]) + [v]
                        elif k == "health":
                            pc["health"] += v
                            pc["max_health"] += v
                        elif isinstance(v, bool):
                            pc[k] = v
                        else:
                            pc[k] += v
            pcs.append(pc)
        _LAST[0] = pcs
        return pcs
    return mk


COUNT_KEYS = ("rounds", "test_applied", "gl_used", "crip_points", "vuln_points", "harried_points", "badluck_used",
              "fright_badluck", "prot_absorbed", "ward_absorbed", "ward_resist_saved", "necrotic_cancelled",
              "necrotic_heal_blocked", "bleed_dealt", "plus_one_dealt", "pc_attacks", "st_crippled", "st_slowed",
              "st_vulnerable", "st_taunted", "st_frightened")


def job(args):
    cell, mi, k0, k1 = args
    pname, carrier, label, mult, spec, health_all = cell
    cs.make_party = make(pname, carrier, spec, health_all)
    mix = se.CURRENT_MIXES[mi]
    scores, counts = [], dict.fromkeys(COUNT_KEYS + ("c_attacks", "c_received", "c_received_pd", "c_hits",
                                                     "c_dmg_once", "received", "losses"), 0.0)
    for k in range(k0, k1):
        en = se.build_encounter(se.ENCOUNTERS[1][mix])
        for e in en:
            e["health"] = e["max_health"] = math.ceil(e["health"] * mult)
        r = cs.run_fight(1, 1, movement=True, enemies=en, seed=100_000 * mi + k)
        won = r["winner"] == "party"
        scores.append(100 * r["party_hp_pct"] if won else 0.0)
        counts["losses"] += not won
        for key in COUNT_KEYS:
            counts[key] += float(r.get(key, 0))
        pcs = _LAST[0]
        counts["received"] += sum(p.get("attacks_received", 0) for p in pcs)
        c = next((p for p in pcs if p["name"].startswith(carrier)), None) if carrier else None
        if c:
            counts["c_attacks"] += c.get("attacks_made", 0)
            counts["c_received"] += c.get("attacks_received", 0)
            counts["c_received_pd"] += c.get("attacks_vs_parry_dodge", 0)
            counts["c_hits"] += c.get("hits_received", 0)
            counts["c_dmg_once"] += bool(c.get("dmg_test_used"))
    return (cell[:4], mi, k0), scores, counts


def run(cells, n):
    jobs = [(cell, mi, k, min(n, k + CHUNK)) for cell in cells for mi in range(len(se.CURRENT_MIXES))
            for k in range(0, n, CHUNK)]
    out = {}
    with Pool() as pool:
        for i, (key, scores, counts) in enumerate(pool.imap_unordered(job, jobs, chunksize=2)):
            out[key] = (scores, counts)
            if i % 500 == 0:
                print(f"  {i}/{len(jobs)} chunks", file=sys.stderr, flush=True)
    res = {}
    for cell in cells:
        key = cell[:4]
        by_mix, counts_by_mix = [], []
        for mi in range(len(se.CURRENT_MIXES)):
            s, c = [], {}
            for k in range(0, n, CHUNK):
                sc, ct = out[(key, mi, k)]
                s += sc
                for kk, v in ct.items():
                    c[kk] = c.get(kk, 0.0) + v
            by_mix.append(s)
            counts_by_mix.append({kk: v / len(s) for kk, v in c.items()})
        res[key] = dict(by_mix=by_mix, counts_by_mix=counts_by_mix)
    return res


def per_fight(res, key, mixes=None):
    cm = res[key]["counts_by_mix"]
    mixes = range(len(cm)) if mixes is None else mixes
    return {k: st.mean(cm[mi][k] for mi in mixes) for k in cm[0]}


def value(res, base_key, ladder_key, key, mixes=None):
    """Value and its standard error against the paired base, on the ladder.
    `mixes` restricts it to some mixes (indexes), with their own ladder."""
    mixes = range(len(se.CURRENT_MIXES)) if mixes is None else mixes
    pick = lambda k: [x for mi in mixes for x in res[k]["by_mix"][mi]]
    base, ladder, test = pick(base_key), pick(ladder_key), pick(key)
    per_pc = (st.mean(ladder) - st.mean(base)) / 2 / 4
    d = [a - b for a, b in zip(test, base)]
    return st.mean(d) / per_pc * HEALTH_VALUE, st.stdev(d) / math.sqrt(len(d)) / per_pc * HEALTH_VALUE, per_pc


def applications(eff, spec, pf):
    """Applications a fight: the stacks the test put on, over the stacks
    each application adds (Good Luck counts when it's used)."""
    if eff == "stat":
        return None
    n = int(spec.split(":")[2])
    return (pf["gl_used"] if eff == "goodluck" else pf["test_applied"]) / n


def tabel_estimate(eff, label, spec, pf, cpf):
    """THE TABEL's price for what the test did: its value for one
    application, times applications a fight. THE TABEL prices the hit that
    delivers an effect separately, so a fight where it never lands counts
    nothing. The stat tests use the carrier's own counts from the base
    fights (attacks made, attacks and hits taken)."""
    if eff == "stat":
        return {"Health +2": 8.0, "Shallow Health +1": 5.0, "Damage +1": 2 * cpf["c_attacks"],
                "Accuracy +1": cpf["c_attacks"],
                "Parry/Dodge +1": cpf["c_received_pd"], "Physical Resist +1": 4 * cpf["c_hits"],
                "Speed +1": 2.54, "Autoswing": 5.5, "Damage +1, first hit": 4 * pf["c_dmg_once"]}.get(label)
    n, mode = int(spec.split(":")[2]), spec.split(":")[3]
    apps = applications(eff, spec, pf)
    if eff.startswith("ward") and mode == "turn":
        # Kept up all fight: the flat Resist at its cap, plus each stack's absorption.
        return (2.0 if eff == "ward_fire" else 1.0) + 2.0 * apps
    return TABEL[eff][n] * apps


def exposure_price(eff, spec, pf, bpf):
    """THE TABEL's own unit rates times what the sim saw the test do, a
    fight's worth: enemy attack points lost to Crippled, party attack
    points gained from Vulnerable / Harried (1 each, the Fudge anchor),
    Bad Luck flips taken (2.2), Taunted / Frightened / Slowed stack-turns
    on enemies (2.2 / 2.2 / 1.1 each, their own per-turn rates), Health
    loss stopped or landed (4), Necrotic resolved (3 a Protected stack
    cancelled, 4 a point of healing blocked) and Good Luck used. None
    where there's no clean count."""
    d = lambda k: pf[k] - bpf[k]
    if eff == "crippled":
        return d("crip_points")
    if eff == "vulnerable":
        return d("vuln_points")
    if eff == "harried":
        return d("harried_points")
    if eff == "badluck":
        return 2.2 * pf["badluck_used"]
    if eff in ("taunt", "fright"):
        return 2.2 * d("st_taunted" if eff == "taunt" else "st_frightened")
    if eff == "slowed":
        return 1.1 * d("st_slowed")
    if eff == "protected":
        return 4 * d("prot_absorbed")
    if eff.startswith("ward"):
        return 4 * (pf["ward_absorbed"] + pf["ward_resist_saved"])
    if eff == "necrotic":
        return 3 * pf["necrotic_cancelled"] + 4 * pf["necrotic_heal_blocked"]
    if eff == "goodluck":
        n = int(spec.split(":")[2])
        return TABEL["goodluck"][n] / n * pf["gl_used"]
    if eff == "bleeding":
        return 4 * pf["bleed_dealt"]
    return None


def mechanism(eff, pf, bpf):
    """A few counts behind each number, a fight."""
    d = lambda k: pf[k] - bpf[k]
    att = f"enemy attacks {d('received'):+.2f}, carrier attacked {d('c_received'):+.2f}"
    if eff == "crippled":
        return f"{d('crip_points'):.2f} enemy attack points, {d('st_crippled'):.2f} stack-turns"
    if eff == "vulnerable":
        return f"{d('vuln_points'):.2f} party attack points, {d('st_vulnerable'):.2f} stack-turns"
    if eff == "harried":
        return f"{d('harried_points'):.2f} party attack points"
    if eff == "slowed":
        return f"{d('st_slowed'):.2f} stack-turns; {att}"
    if eff == "taunt":
        return f"{d('st_taunted'):+.2f} Taunted stack-turns; {att}"
    if eff == "fright":
        return f"{d('st_frightened'):.2f} stack-turns, {pf['fright_badluck']:.2f} Bad Luck flips; {att}"
    if eff == "badluck":
        return f"{pf['badluck_used']:.2f} Bad Luck flips"
    if eff in ("push", "pushmay", "stagger", "hasted"):
        return att
    if eff == "necrotic":
        return f"{pf['necrotic_cancelled']:.2f} Protected cancelled, {pf['necrotic_heal_blocked']:.2f} healing blocked"
    if eff == "bleeding":
        return f"{pf['bleed_dealt']:.2f} Health loss landed"
    if eff == "protected":
        return f"{d('prot_absorbed'):.2f} absorbed"
    if eff.startswith("ward"):
        return f"{pf['ward_absorbed']:.2f} absorbed, {pf['ward_resist_saved']:.2f} stopped by its Resist"
    if eff == "goodluck":
        return f"{pf['gl_used']:.2f} Good Luck used"
    return (f"carrier attacks {bpf['c_attacks']:.2f}, attacked {bpf['c_received']:.2f}, hit {bpf['c_hits']:.2f}; "
            f"{att}")


OWN_MIX = {"ward_fire": "Horde", "ward_shadow": "Frontline", "necrotic": "Warband"}


def report(res, pname, mult, vlist, carriers, rows_out, own_mix=False):
    base_key = (pname, None, "base", mult)
    ladder_key = (pname, None, "ladder", mult)
    fmt = lambda x: "-" if x is None else f"{x:.2f}"
    if own_mix:
        vlist = [v for v in vlist if v[1] in OWN_MIX]
        if not vlist:
            return
        print(f"\n== Party {pname}, enemy Health x{mult}, Ward and Necrotic in the one mix where they come up "
              f"(Ward (Fire): Horde; Ward (Shadow): Frontline; Necrotic: Warband)")
    else:
        bpf = per_fight(res, base_key)
        bscores = [x for s in res[base_key]["by_mix"] for x in s]
        _, _, per_pc = value(res, base_key, ladder_key, base_key)
        print(f"\n== Party {pname}, enemy Health x{mult}: base {st.mean(bscores):.1f} expected Health left, "
              f"{bpf['rounds']:.2f} rounds, losses {100 * bpf['losses']:.1f}%; one PC's +1 Health = {per_pc:.3f}")
    print("| Test | Applied a fight | THE TABEL | TABEL rates x sim counts | Measured | Measured / TABEL | "
          + " | ".join(carriers) + " |")
    print("|---|---|---|---|---|---|" + "---|" * len(carriers))
    for label, eff, spec in vlist:
        mixes = [se.CURRENT_MIXES.index(OWN_MIX[eff])] if own_mix else None
        vals, ses, ests, exps, apps = [], [], [], [], []
        for c in carriers:
            key = (pname, c, label, mult)
            v, s, _ = value(res, base_key, ladder_key, key, mixes)
            pf = per_fight(res, key, mixes)
            cpf = per_fight(res, (pname, c, "base", mult), mixes)
            est = tabel_estimate(eff, label, spec, pf, cpf)
            exp = exposure_price(eff, spec, pf, cpf)
            ap = applications(eff, spec, pf)
            vals.append(v), ses.append(s), ests.append(est), exps.append(exp), apps.append(ap)
            rows_out.append(dict(party=pname, mult=mult, mix=OWN_MIX[eff] if own_mix else "all", test=label,
                                 carrier=c, applied=None if ap is None else round(ap, 3),
                                 tabel=None if est is None else round(est, 3),
                                 exposure=None if exp is None else round(exp, 3),
                                 value=round(v, 3), se=round(s, 3), mechanism=mechanism(eff, pf, cpf)))
        avg = st.mean(vals)
        avg_se = math.sqrt(sum(x * x for x in ses)) / len(ses)
        mean_or_none = lambda xs: None if any(x is None for x in xs) else st.mean(xs)
        est, exp, ap = mean_or_none(ests), mean_or_none(exps), mean_or_none(apps)
        ratio = f"{avg / est:.0%}" if est else "-"
        print(f"| {label} | {fmt(ap)} | {fmt(est)} | {fmt(exp)} | {avg:+.2f} ± {avg_se:.2f} | {ratio} | "
              + " | ".join(f"{x:+.2f}" for x in vals) + " |", flush=True)
    if not own_mix:
        print("\nWhat happened, per carrier (" + " / ".join(carriers) + "):")
        for label, eff, spec in vlist:
            ms = [mechanism(eff, per_fight(res, (pname, c, label, mult)), per_fight(res, (pname, c, "base", mult)))
                  for c in carriers]
            print(f"  {label}: " + " / ".join(ms))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=1000, help="fights per mix")
    ap.add_argument("-m", type=float, action="append", help="enemy Health multiplier(s); default 1.75 and 1")
    ap.add_argument("-e", action="append", help="only these effects (crippled, ..., stat, vulnerable)")
    ap.add_argument("-t", action="append", help="only tests whose name contains this")
    ap.add_argument("-s", action="append", default=[], help="tunables override NAME=VALUE (repeatable)")
    ap.add_argument("--csv", help="write every cell here")
    a = ap.parse_args()
    for kv in a.s:
        k, v = kv.split("=", 1)
        setattr(T, k, ast.literal_eval(v))  # the Pool's workers fork after this
    mults = a.m or [1.75, 1.0]
    want = lambda v: (not a.e or v[1] in a.e) and (not a.t or any(t in v[0] for t in a.t))
    vlist = [v for v in variants() if want(v)]
    vuln = [v for v in VULN if want(v)]
    cells = []
    for mult in mults:
        for pname, vl in (("A", vlist), ("AV", vuln)):
            if not vl:
                continue
            cells += [(pname, None, "base", mult, None, 0), (pname, None, "ladder", mult, None, 2)]
            # Base again under each carrier's name, for its own counts.
            cells += [(pname, c, "base", mult, None, 0) for c in NAMES]
            cells += [(pname, c, label, mult, spec, 0) for label, eff, spec in vl for c in NAMES]
    print(f"{len(cells)} cells, {a.n} fights per mix each", file=sys.stderr, flush=True)
    res = run(cells, a.n)
    rows = []
    for mult in mults:
        for pname, vl in (("A", vlist), ("AV", vuln)):
            if vl:
                report(res, pname, mult, vl, NAMES, rows)
                report(res, pname, mult, vl, NAMES, rows, own_mix=True)
    if a.csv:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
