# FlagonQuest balance-notes model (reading guide)

A companion note for `flagonquest_balance_notes.xlsx` — explains what the
three key tabs actually compute, so the model can be reused without
re-deriving it from the raw cells each time. The workbook has other tabs
(IDEAS, Suits EVOLVED, Costs, Crafting Table, HExboys, DM Guide, Equipment,
Card Cheating...) that weren't reviewed in depth here; this note covers the
three the designer specifically pointed to: **Baseline**, **THE TABEL**, and
**BALANCE**.

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

One VALUE-per-unit for each mechanic type (row 2, anchored to Fudge Value
= 1), then a full cross-conversion grid so any mechanic can be expressed in
terms of any other. Current per-unit values:

| Mechanic | Value | Mechanic | Value |
|---|---|---|---|
| Fudge Value (baseline) | 1 | Sift | 0.64 |
| Acc / Def 💯 | 1 | Shallow HP 💯 | 5 |
| Damage | 2 | Deep HP 💯 | 4 |
| Card 💯 | ~3.05 | Shallow Heal 💯 | 4 |
| Health 💯 | 4 | Deep Heal 💯 | 5 |
| 1 AP 💯 | 3 | Good Luck 💯 | 2.5 |
| Debuff | 1 | Autoswing 💯 | 5.5 |
| Gold 💯 | 1.5 | Push | 0.5 |
| Protected 💯 | 3 | Difficult Terrain 💯 | 1 |
| | | Concession 💯 *(old name — see note below)* | 2.5 |

The 💯 tag marks a mechanic whose value is **not** discounted for
contingency — it always applies once granted (a flat Accuracy/Defense
bump, a card, Gold, Protected, straight Health, a guaranteed heal, Good
Luck, Autoswing, Difficult Terrain). The untagged mechanics (Damage,
Debuff, Push) are cheaper per unit precisely because they only pay off
when an attack actually connects — roughly 50/50 absent other effects,
matching Baseline's average hit chance.

**Naming note:** "Concession" is this document's era's name for what the
current rules call **Pressure** (renamed earlier this session, along with
the Social Contest rework — see `RULES_DESIGN.md`). Same underlying
mechanic, just an older label.

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
