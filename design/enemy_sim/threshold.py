"""The toughest enemies a party can still beat half the time (2026-10-30).

Per the designer, strength is how much harder a fight a party can take
for what it spent (RULES_DESIGN.md, "What the game is for"). `find`
halves an interval of enemy Health multipliers, reading the win rate at
each midpoint on the same fixed fights, then fits a logistic curve,
win rate against log(multiplier), through every point it tried and
returns where the curve crosses one half. Halving alone moves in steps:
two changes a step apart read the same, and a change smaller than one
reads +0%. The fit uses every reading, so it moves smoothly.
"""
import math


def _sigmoid(z):
    # Stable both ways: a fit on cleanly split data runs z off to +-inf.
    if z >= 0:
        return 1 / (1 + math.exp(-min(z, 700)))
    e = math.exp(max(z, -700))
    return e / (1 + e)


def fit(points):
    """(multiplier, wins, n) points -> the multiplier at a 50% win rate,
    or None if the points don't pin a falling curve down.

    Newton's method on the binomial log-likelihood, with the x values
    (log multipliers) centred and scaled first and every step shortened
    until it improves the fit: plain Newton from a fixed start overshoots
    and flies apart on a wide spread of x (whole-step stresses, 2026-10-30).
    """
    xs = [(math.log(m), w, n) for m, w, n in points if n]
    if not xs or all(w == 0 for _, w, _ in xs) or all(w == n for _, w, n in xs):
        return None
    total = sum(n for _, _, n in xs)
    mu = sum(x * n for x, _, n in xs) / total
    sd = math.sqrt(sum(n * (x - mu) ** 2 for x, _, n in xs) / total) or 1.0
    zs = [((x - mu) / sd, w, n) for x, w, n in xs]

    def loglik(a, b):
        out = 0.0
        for z, w, n in zs:
            p = min(max(_sigmoid(a + b * z), 1e-300), 1 - 1e-16)
            out += w * math.log(p) + (n - w) * math.log(1 - p)
        return out
    a, b = 0.0, -1.0
    cur = loglik(a, b)
    for _ in range(200):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for z, w, n in zs:
            p = _sigmoid(a + b * z)
            r = w - n * p
            v = n * p * (1 - p)
            g0 += r
            g1 += r * z
            h00 += v
            h01 += v * z
            h11 += v * z * z
        det = h00 * h11 - h01 * h01
        if det <= 1e-12:
            return None
        da = (h11 * g0 - h01 * g1) / det
        db = (h00 * g1 - h01 * g0) / det
        t = 1.0
        while True:
            na, nb = a + t * da, b + t * db
            new = loglik(na, nb)
            if new >= cur - 1e-12 or t < 1e-8:
                break
            t /= 2
        a, b, cur = na, nb, new
        if abs(t * da) + abs(t * db) < 1e-10:
            break
    # A falling curve, and not a cliff: cleanly split points (every
    # reading 0% or 100%) send b toward -inf and say nothing about where.
    if b >= 0 or b < -1e4:
        return None
    x50 = mu + sd * (-a / b)
    if abs(x50) > 700:
        return None
    return math.exp(x50)


def grid(rate, xs):
    """For a stress that only comes in whole steps (enemy damage or
    accuracy +N): `rate(x)` -> (wins, n) at every x in `xs`, and the x
    where a logistic through all of them crosses one half (linear in x),
    or None if they don't pin it down."""
    pts = [(x,) + tuple(rate(x)) for x in xs]
    t = fit([(math.exp(x), w, n) for x, w, n in pts])
    return (None if t is None else math.log(t)), pts


def find(rate, lo, hi, steps=8):
    """`rate(m)` -> (wins, n) at enemy Health multiplier m. Returns
    (threshold, points); the threshold falls back to the halving's own
    answer if the fit can't be made or lands outside what was tried."""
    pts = []
    a, b = lo, hi
    for _ in range(steps):
        mid = (a + b) / 2
        w, n = rate(mid)
        pts.append((mid, w, n))
        a, b = (mid, b) if w > n / 2 else (a, mid)
    t = fit(pts)
    if t is None or not lo <= t <= hi:
        t = (a + b) / 2
    return t, pts
