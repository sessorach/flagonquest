# FlagonQuest balance-notes model (reading guide)

A companion note for `flagonquest_balance_notes.xlsx` (the designer's
historical balance notes, in `archive/`) — explains what the three key
tabs actually compute, so the model can be reused without re-deriving it
from the raw cells each time. The workbook has other tabs (IDEAS, Suits
EVOLVED, Costs, Crafting Table, HExboys, DM Guide, Equipment, Card
Cheating...) that weren't reviewed in depth here; this note covers the
three the designer specifically pointed to: **Baseline**, **THE TABEL**,
and **BALANCE**. See `balance_weights_notes.md` for the full derivation
behind every value in THE TABEL below — this file gives the short version
of each; that one shows the actual math and where it came from.

## The core idea

Everything is priced against one anchor: **1 value ≈ +1 to a flip**, fixed
by the fact that Gambling costs 2 and grants an Extra Success, so an Extra
Success = 2 value. Every other mechanic (Damage, a Card, a point of Health,
1 AP, Gold, Good Luck, a stack of Protected, and so on) gets its own
value-per-unit figured out relative to that anchor, and then a Technique or
item's total worth is just the weighted sum of everything it grants,
checked against what its Level should "cost."

## Baseline tab — the assumed encounter

Sets the real-world assumptions the whole model is calibrated against, then
derives a chain of aggregate values from them:

- Party of 4 vs. 4 enemies, ~50% average hit chance, ~2.25 Health lost per
  hit that lands.
- **Health value = 4** — since an attack that deals 2 damage only lands
  ~50% of the time, its "guaranteed" value is double the raw number.
- 5 rounds per combat, with enemies dying off through the fight (assumed
  ~3.6 enemies still active round 1, down to ~0.4 by round 5) — used to
  derive a total "enemy value" and "player value" per fight.
- **Baseline turn value ≈ 8.25** (attacks/turn × per-attack value) — this
  is the reference a Technique's own value gets checked against.
- A parallel chain for the *resource* economy: ~10 cards/day, each worth 2
  (card value), ~32 total value recovered per rest, translating to ~1.55
  "full encounters" worth of resources per day.
- Consumables/magic items per encounter and their value-per-tier (Consume
  = 3, Magic Item = 30), plus a Value↔Gold conversion ratio (≈0.667) used
  to sanity-check item pricing against the same value currency everything
  else is priced in.

## THE TABEL — the exchange-rate matrix

One VALUE-per-unit for each mechanic type, then a full cross-conversion
grid so any mechanic can be expressed in terms of any other. The table
below is the **current, reconciled set** — several values have been
revised from the original workbook (each row says which), and the old
💯 emoji marker has been replaced with a plain **Guaranteed?** column,
same meaning as before: **Yes** means the value is *not* discounted for
contingency — it always applies once granted (a flat Accuracy/Defense
bump, a card, Gold, Protected, straight Health, Good Luck...). **No**
means the mechanic is typically delivered as an on-hit rider (Damage,
Debuff, Push) and is priced cheaper per unit to reflect that it only
pays off when the attack actually connects — roughly 50/50 absent other
effects, matching Baseline's average hit chance.

| Mechanic | Value | Guaranteed? | How the value was determined (short — see `balance_weights_notes.md` for the full math) |
|---|---|---|---|
| Fudge Value | 1 | Yes | The anchor itself, by definition — 1 value ≈ +1 to a flip. |
| Accuracy / Defense | 1 | Yes | Same as Fudge Value by definition — a flat Accuracy/Defense bonus *is* a flip bonus. |
| Damage | 2 | No | Confirmed: Health(4) × average hit chance(0.5), pricing a *contingent* point of harm (an attack that has to land) before Resist, which is a separate reduction applied later. A guaranteed point of harm that skips the attack roll uses Health's full rate (4) instead, not this one. |
| Debuff | 1 | No | Calibrated to Baseline's own "Harried value" (~1) — the generic bucket every stacking status effect (Crippled, Slowed, Vulnerable, Bleeding, Necrotic...) gets lumped into. |
| Resist (Physical) | 2.8/point | Yes | New row — never had one, despite 7 current Masterwork items granting Resist. `Damage's weight (2) × expected hits of that type absorbed per encounter`, using Baseline's own combat math (~1.875 hits/player/encounter, any type) and the designer's stated enemy mix (3 in 4 enemies are Physical-only). |
| Resist (Fire) | 0.375/point | Yes | Same formula as Physical Resist, at Fire's share of enemies (1 in 10, since Fire is the deliberately-common element — see the design note on Fire being the default/likely element). |
| Resist (Frost / Brilliant / Shadow, each) | 0.19/point | Yes | Same formula, at each of the other three elements' share (1 in 20 each) — about half Fire's rate and ~1/15th of Physical's. |
| Health | 4 | Yes | Baseline formula: Damage(2) ÷ average hit chance(0.5). |
| Shallow HP (max pool) | 5 | Yes | Worth *more* than Deep as a pool increase, since it's easier to top back up at rest. |
| Deep HP (max pool) | 4 | Yes | The baseline "effective healing" rate — doesn't need healing to already count. |
| Shallow Heal | 4 | Yes | Healing the *less*-restricted resource — the inverse ranking from the max-pool rows above. |
| Deep Heal | 5 | Yes | Healing the scarcer, more-restricted resource. |
| 1 AP | 2.75 *(was 3)* | Yes | Confirmed: priced as opportunity cost against attacking instead — "how valuable does this need to be considering I could just attack" — `(value of one attack, 5.5) ÷ (its AP cost, 2)`. AP is deliberately scarce (very few things grant it directly) and quantized (attacks cost a full 2 AP each, no fractional attacks), which is exactly why this ratio is the right anchor. |
| Card (drawn / from hand) | 2.7 *(was ~3.05)* | Yes | Floor = Good Luck's own marginal (2.2 — playing a hand card to replace a flip is the same math as Good Luck); a premium above that for timing/targeting/Suit Pool flexibility, which is a judgment call, not a computed number. |
| Good Luck | 2.2 *(was 2.5)* | Yes | Exact expectation of flip-2-take-highest from a real 52-card deck (9.196) minus the 1-card baseline (7). |
| Pressure *(was "Concession," 2.5)* | 2.2 | Yes | Exactly mirrors Good Luck — Pressure literally *is* imposed Bad Luck under current rules, and the underlying card math is symmetric (harm from worst-of-2 = benefit from best-of-2). |
| Gold | 1.5 | Yes | Reciprocal of Baseline's own "Value / Gold ratio" (2/3). |
| Protected | 3 | Yes | Confirmed: Health's value (4) × the real (bank-partial, not burn-all) mechanic, simulated across a full encounter at the designer's stated "takes more hits than average" targeting assumption — lands at ~75-84% of full value realized for a realistic 1-4 stack grant, matching the ~25% `[Fleeting]`-driven discount. |
| Sift | 0.6/card *(was 0.64)* | Yes | Simulated the real mechanic (discard low cards, let the rest reshuffle back in) — ~0.60/card is what lands within one adventuring day's worth of draws; the true long-run value is ~1.62/card. |
| Speed | 0.6/point | Yes | New row — THE TABEL never had one, despite real items granting flat Speed. `(1 AP's value) ÷ (baseline Speed + 1)`, at an agreed baseline of Agility 3 (Speed 4). |
| Push | 0.6/meter *(was 0.5)* | No | Directly Speed's own per-meter rate — still priced as an on-hit-style rider, same reasoning as Damage/Debuff above. |
| Difficult Terrain | 0.6/degree *(was 1)* | Yes | Same per-meter-of-Speed rate as Push, but usually granted as a standalone zone effect rather than an attack rider — still carries its own AoE/zone-size uncertainty on top of this rate. |
| Autoswing | 5.5 | Yes | Confirmed: the bundled credit for a Technique/item that grants an attack as part of a larger effect (Battle Maneuver's base "make a weapon attack" is the live example) — value of one typical attack (damage, hit-chance discounted) plus the Harried stack any attack applies. Not a "guaranteed hit" mechanic. |

## BALANCE tab — every Technique/Item, audited

One row per Technique or Item (~125 in the current dump: mostly draft
Techniques, plus a handful of Items like Bottled Fire, Bonemelter, Power
Snack). Columns `H` through `AF` record how much of each THE TABEL
mechanic that entry grants (e.g. `M` = 1 AP, `N` = Debuff, `W` = Autoswing);
three computed columns turn that into a verdict:

- **Value** (`E`) = `SUMPRODUCT($H$1:$AF$1, H:AF)` — the per-use value of
  everything the entry grants, using THE TABEL's value-per-unit weights
  (row 1 here mirrors THE TABEL's VALUE row exactly).
- **Target** (`G`) = `Level × 3` — the expected value budget for a
  Technique of that Level, echoing Baseline's turn-value scaling.
- **Net** (`D`) = `Value × Rate of Use/Encounter − Target` — the real
  verdict: total value actually delivered per encounter, weighed against
  budget. **Positive Net = reads as overpowered for its Level; negative =
  underpowered.** (Rate of Use/Encounter, column `F`, is a separate
  judgment call per entry — e.g. Second Wind is valued at ~2.27/use but
  assumed used 3×/encounter, so `2.27 × 3 − 6 = +0.81` net.)

This is the tool to point at any of the 18 newly-drafted Masterwork items
(or an existing one) during a balance pass: express what it grants in
THE TABEL's mechanic vocabulary, multiply by the value weights, and see
whether the result sits close to zero Net for its Level — or, since
Masterwork items aren't Techniques and don't share the same Level→3-value
Target formula, at least see how its value compares to similarly-priced
existing items already run through the same math (Bottled Fire, Bonemelter,
Sunbeam, Hellfire Bomb are the four Items already in this sheet).
