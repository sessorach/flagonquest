"""Weak / Average / Strong per application from the whole-day runs.
Debuffs: Weak = on the first hit, ordinary days; Average = aimed at the
biggest threat, ordinary days; Strong = aimed, threatening days (+1 Slot);
the mean over carriers (Taunt: Browndog's). Buffs and stats: Weak = the
carrier it helps least, ordinary days; Average = the mean, ordinary days;
Strong = the carrier it helps most, threatening days. Offense effects
(Harried, Vulnerable, Bleeding, Necrotic) are also shown scaled by THE
TABEL's +1 Accuracy / +1 Damage over what those measure on ordinary days."""
import csv, statistics as st, sys
from collections import defaultdict
S = sys.argv[1]
def load(fn, party="A"):
    g = defaultdict(dict)
    for r in csv.DictReader(open(f"{S}/{fn}.csv")):
        if r["mix"] == "all" and r["party"] == party and r["carrier"]:
            g[r["test"]][r["carrier"]] = r
    return g
X0 = {**load("day_x0_all"), **load("day_x0_danger"), **load("day_x0_fill")}
X1 = {**load("day_x1_all"), **load("day_x1_danger"), **load("day_x1_fill")}
V0, V1 = load("day_x0_all", "AV"), load("day_x1_all", "AV")
def pa(src, test, who=None, agg="mean", total=False):
    rs = src.get(test, {})
    if who: rs = {c: r for c, r in rs.items() if c in who}
    if not rs: return None
    per = {c: float(r["value"]) / (1 if total else max(1e-9, float(r["applied"]))) for c, r in rs.items()}
    if agg == "mean":
        return st.mean(float(r["value"]) for r in rs.values()) / (1 if total else st.mean(float(r["applied"]) for r in rs.values()))
    c = (min if agg == "min" else max)(per, key=per.get)
    return per[c], c
f = lambda x: "-" if x is None else (f"{x[0]:.2f} ({x[1]})" if isinstance(x, tuple) else f"{x:.2f}")
acc = pa(X0, "Accuracy +1", total=True); dmg = pa(X0, "Damage +1", total=True)
acc1 = pa(X1, "Accuracy +1", total=True); dmg1 = pa(X1, "Damage +1", total=True)
print(f"+1 Accuracy a day: {acc:.2f} ordinary, {acc1:.2f} threatening; +1 Damage: {dmg:.2f}, {dmg1:.2f}")
AF, DF = 5.49 / acc, 10.97 / dmg
print(f"offense scaling: Accuracy-like x{AF:.2f}, Damage-like x{DF:.2f}\n")
print("| Debuff | Weak | Average | Strong | Weak x4 | Average x4 | Strong x4 |\n|---|---|---|---|---|---|---|")
for name, eff, who in [("Crippled", "crippled", None), ("Slowed", "slowed", None), ("Bad Luck", "badluck", None),
                       ("Frightened", "fright", None), ("Taunted (Browndog)", "taunt", ["Browndog"]),
                       ("Bleeding", "bleeding", None), ("Harried", "harried", None)]:
    row = []
    for n in (1, 4):
        row += [pa(X0, f"{eff} {n}, first hit", who), pa(X0, f"{eff} {n} on the boss, first turn", who),
                pa(X1, f"{eff} {n} on the boss, first turn", who)]
    print(f"| {name} | " + " | ".join(f(x) for x in row[:3]) + " | " + " | ".join(f(x) for x in row[3:]) + " |")
nec = [pa(X0, f"necrotic {n}, first hit") for n in (1, 4)] + [pa(X0, f"necrotic {n} on the boss, first turn") for n in (1, 4)] \
    + [pa(X1, f"necrotic {n} on the boss, first turn") for n in (1, 4)]
print(f"| Necrotic | {f(nec[0])} | {f(nec[2])} | {f(nec[4])} | {f(nec[1])} | {f(nec[3])} | {f(nec[5])} |")
vul = [pa(V0, f"vulnerable {n}, first hit") for n in (1, 4)] + [pa(V1, f"vulnerable {n}, first hit") for n in (1, 4)]
print(f"| Vulnerable (first hit only; ordinary / threatening) | {f(vul[0])} | - | {f(vul[2])} | {f(vul[1])} | - | {f(vul[3])} |")
print("\n| Buff or stat | Weak | Average | Strong |\n|---|---|---|---|")
for name, test, tot in [("Protected x1", "protected 1, first turn", False), ("Protected x4", "protected 4, first turn", False),
                        ("Hasted x1", "hasted 1, first turn", False), ("Hasted x4", "hasted 4, first turn", False),
                        ("Good Luck, first attack", "goodluck 1, first attack", False),
                        ("Good Luck, every turn (per use)", "goodluck 1, every turn", False),
                        ("Taunt guard x1", "tauntguard 1, first turn", False),
                        ("Ward (Fire) x1", "ward_fire 1, first turn", False), ("Ward (Shadow) x1", "ward_shadow 1, first turn", False),
                        ("Push when it helps, 1 m (per push)", "pushmay 1, every hit", False),
                        ("Push every time, 1 m (per push)", "push 1, every hit", False),
                        ("Stagger on hit (per place)", "stagger 1, every hit", False),
                        ("Physical Resist +1", "Physical Resist +1", True), ("Speed +1", "Speed +1", True),
                        ("Parry/Dodge +1", "Parry/Dodge +1", True), ("Accuracy +1", "Accuracy +1", True),
                        ("Damage +1", "Damage +1", True), ("Autoswing (THE TABEL 5.5)", "Autoswing", True)]:
    print(f"| {name} | {f(pa(X0, test, agg='min', total=tot))} | {f(pa(X0, test, total=tot))} | {f(pa(X1, test, agg='max', total=tot))} |")
print("\nScaled offense (x THE TABEL's +1 over measured): ")
for name, eff, fac in [("Harried", "harried", AF), ("Bleeding", "bleeding", DF)]:
    w, a, s = pa(X0, f"{eff} 1, first hit"), pa(X0, f"{eff} 1 on the boss, first turn"), pa(X1, f"{eff} 1 on the boss, first turn")
    print(f"  {name}: weak {w * fac:.2f}  avg {a * fac:.2f}  strong {s * fac:.2f}")
print(f"  Vulnerable: weak {vul[0] * AF:.2f}  strong {vul[2] * AF:.2f}")
print(f"  Necrotic: weak {nec[0] * DF:.2f}  avg {nec[2] * DF:.2f}  strong {nec[4] * DF:.2f}")
