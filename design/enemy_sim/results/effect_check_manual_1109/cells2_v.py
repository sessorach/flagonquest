import sys
sys.argv = ["x"]
exec(open(f"/tmp/claude-0/-home-user-flagonquest/e6747bdc-fa39-5126-8ea2-8c3b178a4574/scratchpad/ec_manual/cells_v.py").read().split("show(\"Crippled\"")[0])
F, DS = D["full2_175"], D["danger_standard"]
def both(test, only=None, total=False):
    return wmean([(per_app(F, test, only, total), 2), (per_app(DS, test, only, total), 1)])
def p(label, *vals):
    print(f"{label:52} " + "  ".join("-" if v is None else f"{v:6.2f}" for v in vals))
print("Protected 1 first turn: weak (Car+Sab), avg (all), strong (Hilde) ord / L2 / Chief / Ogre")
p("protected 1", both("protected 1, first turn", ["Carrick", "Sable"]), both("protected 1, first turn"),
  both("protected 1, first turn", ["Hilde"]), per_app(D["danger_level2"], "protected 1, first turn", ["Hilde"]),
  per_app(D["danger_chief"], "protected 1, first turn", ["Hilde"]), per_app(D["fill_ogre"], "protected 1, first turn", ["Hilde"]))
p("protected 4", per_app(F, "protected 4, first turn", ["Carrick", "Sable"]), per_app(F, "protected 4, first turn"),
  per_app(F, "protected 4, first turn", ["Hilde"]), per_app(D["fill_ogre"], "protected 4, first turn", ["Hilde", "Browndog"]),
  per_app(D["fill_ogre"], "protected 4, first turn"))
p("hasted 1: Sable / all / Hilde ord / all Ogre / Hilde Ogre", per_app(F, "hasted 1, first turn", ["Sable"]), per_app(F, "hasted 1, first turn"),
  per_app(F, "hasted 1, first turn", ["Hilde"]), per_app(D["fill_ogre"], "hasted 1, first turn"), per_app(D["fill_ogre"], "hasted 1, first turn", ["Hilde"]))
p("hasted 4: same", per_app(F, "hasted 4, first turn", ["Sable"]), per_app(F, "hasted 4, first turn"),
  per_app(F, "hasted 4, first turn", ["Hilde"]), per_app(D["fill_ogre"], "hasted 4, first turn"), per_app(D["fill_ogre"], "hasted 4, first turn", ["Hilde"]))
p("goodluck: every turn / first / Ogre first / Ogre every", per_app(F, "goodluck 1, every turn"), per_app(F, "goodluck 1, first attack"),
  per_app(D["fill_ogre"], "goodluck 1, first attack"), per_app(D["fill_ogre"], "goodluck 1, every turn"))
p("push every time 1m/3m (per push), ord", per_app(F, "push 1, every hit"), per_app(F, "push 3, every hit"))
p("pushmay 1m/3m every hit, ord", per_app(F, "pushmay 1, every hit"), per_app(F, "pushmay 3, every hit"))
p("pushmay 1m/3m, push 3 every time, Ogre", per_app(D["fill_ogre"], "pushmay 1, every hit"), per_app(D["fill_ogre"], "pushmay 3, every hit"),
  per_app(D["fill_ogre"], "push 3, every hit"))
for nm, src in [("ord", DS), ("L2", D["danger_level2"]), ("Chief", D["danger_chief"]), ("Ogre", D["danger_ogre"])]:
    p(f"stagger per place {nm}: on hit / aimed 2 first (per place) / aimed every turn",
      per_app(src, "stagger 1, every hit"), per_app(src, "stagger 2 on the boss, first turn") / 2, per_app(src, "stagger 1 on the boss, every turn"))
for t in ("ward_fire", "ward_shadow"):
    p(f"{t} 1: all mixes / its mix ; 4: all / its", per_app(F, f"{t} 1, first turn"), None, per_app(F, f"{t} 4, first turn"))
