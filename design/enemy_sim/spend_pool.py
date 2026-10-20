"""How many Bleeding stacks a hit finds on its target (2026-10-20), under the
current rule (half ticks, Protected stops them), for pricing abilities that
spend a target's Bleeding: for each party and enemy toughness, how often a
PC's hit finds 1, 2, 3+ stacks, the average it could spend with a cap of
2 / 3 / 4, and how often a bleeding target lives through the hit. See
balance_weights_notes.md, "Bleeding's value under half ticks, and spending
it".

    python3 spend_pool.py"""
import sys, os, math, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import combat_sim as cs, sample_enemies as se, party

PARTIES = {"A + Furious Rage": ["Hilde (Bleed)", "Browndog", "Carrick", "Sable"],
           "X, all Bleeding builds": ["Hilde (Bleed)", "Felix (Bleed)", "Jackal (Bleed)", "Beornhard (Bleed)"]}
N = 400

def job(j):
    pname, mult = j
    names = PARTIES[pname]
    rec = []
    orig = cs._kill_topup
    def wrapped(pc, target, raw, resist, skill, allies):
        net = max(0, raw - resist)
        lethal = net - min(net, target.get('protected', 0)) >= target['health']
        rec.append((pc['name'].rstrip('0123456789'), target.get('bleeding', 0), lethal))
        return orig(pc, target, raw, resist, skill, allies)
    cs._kill_topup = wrapped
    cs.make_party = lambda t, good_luck=0: party.make_party_from(names, good_luck)
    for mi, mix in enumerate(se.CURRENT_MIXES):
        for k in range(N):
            en = se.build_encounter(se.ENCOUNTERS[1][mix])
            for e in en:
                e['health'] = e['max_health'] = math.ceil(e['health'] * mult)
            cs.run_fight(1, 1, movement=True, enemies=en, seed=100_000 * mi + k)
    return j, rec

if __name__ == "__main__":
    jobs = [(p, m) for p in PARTIES for m in (1.0, 1.75)]
    with Pool() as pool:
        out = dict(pool.map(job, jobs))
    fights = N * len(se.CURRENT_MIXES)
    for (p, m), rec in out.items():
        print(f"== {p}, enemy Health x{m}: {len(rec)/fights:.1f} hits a fight")
        groups = {"whole party": rec}
        for name in dict.fromkeys(r[0] for r in rec):
            groups[name] = [r for r in rec if r[0] == name]
        for g, rs in groups.items():
            n = len(rs)
            any1 = [r for r in rs if r[1] >= 1]
            line = (f"  {g:22} hits {n/fights:4.2f}/fight | target bleeding: >=1 {100*len(any1)/n:3.0f}%, "
                    f">=2 {100*sum(r[1]>=2 for r in rs)/n:3.0f}%, >=3 {100*sum(r[1]>=3 for r in rs)/n:3.0f}% | "
                    f"spendable a hit, cap 2/3/4: {st.mean(min(r[1],2) for r in rs):.2f} / {st.mean(min(r[1],3) for r in rs):.2f} / {st.mean(min(r[1],4) for r in rs):.2f}"
                    f" | of bleeding hits, target survives the hit {100*sum(not r[2] for r in any1)/max(1,len(any1)):3.0f}%")
            print(line)
