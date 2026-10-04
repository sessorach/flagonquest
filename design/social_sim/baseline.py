"""Social Encounter Baseline (balance_weights_notes.md) as an exact
recursion, so Social Maneuver Features can be priced against it
(2026-10-04).

Baseline: a +6 lead (succeeds on a card >= 7) and three +4 Supporters
(>= 9, the baseline's own simplification), 5 successes to win, Pressure
+1 after every round and the encounter lost when it reaches 5. Pressure
is Bad Luck on the Statement and every Support check. Each successful
Support is Good Luck on the Statement. Card rescue: with net Good Luck
or neutral the Statement always succeeds; with net Bad Luck it's
rescued only if exactly one card is the spoiler. A successful Statement
gives 1 success plus 1 per card in its suit pool (every flipped card,
1/4 each).

A Feature is a once-per-encounter use (one copy of Social Maneuver),
spent at the start of whichever round gives the best odds from the
current state, the way a player would actually spend it."""
from functools import lru_cache
from math import comb

NEED, FAIL = 5, 5
LEAD_T, SUP_T, SUPPORTERS = 7, 9, 3


def p_flip(threshold, luck):
    """Chance a flip with net luck `luck` (+ Good, - Bad) clears threshold."""
    n = 1 + abs(luck)
    miss = (threshold - 1) / 13
    return 1 - miss ** n if luck >= 0 else (1 - miss) ** n


def p_lead(luck):
    if luck >= 0:
        return 1.0  # card rescue
    n = 1 - luck
    hit = (14 - LEAD_T) / 13
    return hit ** n + n * (1 - hit) * hit ** (n - 1)


def binom(n, k, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def round_outcomes(pressure_luck, lead_bonus=0, sup_bonus=0, extra_on_success=0, airtight=False, approach=False):
    """[(prob, successes gained)] for one round."""
    q = p_flip(SUP_T, sup_bonus - pressure_luck)
    out = {}
    for k in range(SUPPORTERS + 1):
        pk = binom(SUPPORTERS, k, q)
        luck = k + lead_bonus - pressure_luck
        cards = 1 + abs(luck)
        ps = p_lead(luck)
        out[0] = out.get(0, 0) + pk * (1 - ps)
        for m in range(cards + 1):
            pm = binom(cards, m, 0.25)
            gain = 1 + m + extra_on_success
            if approach:  # [Suit] extra successes: another 1/4 per card
                for a in range(cards + 1):
                    g2 = gain + a
                    out[g2] = out.get(g2, 0) + pk * ps * pm * binom(cards, a, 0.25)
                continue
            if airtight:
                p4 = sum((-1) ** j * comb(4, j) * ((4 - j) / 4) ** cards for j in range(5))
                out[gain + 4] = out.get(gain + 4, 0) + pk * ps * pm * p4
                out[gain] = out.get(gain, 0) + pk * ps * pm * (1 - p4)
                continue
            out[gain] = out.get(gain, 0) + pk * ps * pm
    return [(p, g) for g, p in out.items()]


def win_prob(feature=None):
    @lru_cache(None)
    def W(s, P, avail, ignore_next):
        if s >= NEED:
            return 1.0
        if P >= FAIL:
            return 0.0
        options = [(False,)]
        if avail:
            options.append((True,))
        best = 0.0
        for (use,) in options:
            luck_p = 0 if ignore_next else P
            kw = {}
            if use:
                kw = FEATURES[feature]["round"]
            total = 0.0
            for prob, gain in round_outcomes(luck_p, **kw):
                if use and FEATURES[feature].get("clear") and gain > 0:
                    # Trade any number of successes for Pressure removed.
                    total += prob * max(W(min(NEED, s + gain - t), P + 1 - t if P + 1 - t >= 0 else 0, False, False)
                                        for t in range(gain + 1))
                    continue
                nxt_ignore = bool(use and FEATURES[feature].get("friendly") and gain > 0)
                total += prob * W(min(NEED, s + gain), P + 1, avail and not use, nxt_ignore)
            if use and FEATURES[feature].get("comeback"):
                total = comeback(s, P, ignore_next, W)
            best = max(best, total)
        return best

    return W(0, 0, feature is not None, False)


def comeback(s, P, ignore_next, W):
    """Two Statements this round; the second has no Support."""
    luck_p = 0 if ignore_next else P
    total = 0.0
    for p1, g1 in round_outcomes(luck_p):
        q2 = p_lead(-luck_p)
        cards = 1 + luck_p
        total += p1 * (1 - q2) * W(min(NEED, s + g1), P + 1, False, False)
        for m in range(cards + 1):
            total += p1 * q2 * binom(cards, m, 0.25) * W(min(NEED, s + g1 + 1 + m), P + 1, False, False)
    return total


FEATURES = {
    "Careful Delivery (Good Luck)": {"round": {"lead_bonus": 1}},
    "Emotional Appeal (+1 success)": {"round": {"extra_on_success": 1}},
    "Approach ([Suit] extra successes)": {"round": {"approach": True}},
    "Airtight Argument": {"round": {"airtight": True}},
    "Clear the Air": {"round": {}, "clear": True},
    "Friendly-Faced": {"round": {}, "friendly": True},
    "Setup & Follow": {"round": {"sup_bonus": 1}},
    "Practiced Comeback (alone)": {"round": {}, "comeback": True},
}

if __name__ == "__main__":
    base = win_prob()
    print(f"Baseline win {100 * base:.2f}% (locked: 57.03%)")
    for name in FEATURES:
        w = win_prob(name)
        print(f"  {name:36} {100 * w:6.2f}%  {100 * (w - base):+6.2f}pp")


def variants():
    """Alternatives checked while pricing (2026-10-04)."""
    import itertools
    base = win_prob()
    res = {}

    def p_suits_at_least(cards, k):
        # Chance `cards` flips (1/4 per suit, independent) cover >= k suits.
        tot = 0.0
        for combo in itertools.product(range(4), repeat=cards):
            tot += (len(set(combo)) >= k) * 0.25 ** cards
        return tot

    def custom(round_fn):
        @lru_cache(None)
        def W(s, P, avail):
            if s >= NEED:
                return 1.0
            if P >= FAIL:
                return 0.0
            best = sum(p * W(min(NEED, s + g), P + 1, avail) for p, g in round_outcomes(P))
            if avail:
                best = max(best, sum(p * W(min(NEED, s + g), P + 1 + dp, False) for p, g, dp in round_fn(P)))
            return best
        return W(0, 0, True)

    def airtight(suits, bonus):
        def fn(P):
            out = []
            q = p_flip(SUP_T, -P)
            for k in range(SUPPORTERS + 1):
                pk = binom(SUPPORTERS, k, q)
                luck = k - P
                cards = 1 + abs(luck)
                ps = p_lead(luck)
                out.append((pk * (1 - ps), 0, 0))
                pa = p_suits_at_least(cards, suits)
                for m in range(cards + 1):
                    pm = binom(cards, m, 0.25)
                    out.append((pk * ps * pm * pa, 1 + m + bonus, 0))
                    out.append((pk * ps * pm * (1 - pa), 1 + m, 0))
            return out
        return fn

    res["Airtight: 3+ suits, +2"] = custom(airtight(3, 2))
    res["Airtight: 3+ suits, +3"] = custom(airtight(3, 3))
    res["Prevent 1 Pressure (once)"] = custom(lambda P: [(p, g, -1) for p, g in round_outcomes(P)])
    res["Setup & Follow: Supports Good Luck twice"] = custom(lambda P: [(p, g, 0) for p, g in round_outcomes(P, sup_bonus=2)])
    res["Setup & Follow: Statement Good Luck twice"] = custom(lambda P: [(p, g, 0) for p, g in round_outcomes(P, lead_bonus=2)])
    for k, v in res.items():
        print(f"  {k:42} {100 * v:6.2f}%  {100 * (v - base):+6.2f}pp")
