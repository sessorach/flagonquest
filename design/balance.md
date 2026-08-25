# Balancing FlagonQuest

Aggregate notes on game balance in the broad sense — approaches, recurring
judgment calls, and conclusions from specific balance passes as they
happen. Companion to `design/RULES_DESIGN.md` (which covers rules
*design* decisions — what a mechanic is and why) and
`design/flagonquest_balance_notes_model.md` (which explains the value-economy
model in `archive/flagonquest_balance_notes.xlsx` that this file's analysis
leans on). This file starts mostly empty and fills in as real balance
passes happen — it's meant to be the current, living version of the kind
of self-notes the designer already kept in the old Manifesto documents
(`archive/flagonquest_manifesto_2k19.md`, `flagonquest_manifesto_v5.md`).

## The value-economy model, in short

Everything is priced against one anchor: 1 value ≈ +1 to a flip (fixed by
Gambling costing 2 for an Extra Success, so an Extra Success = 2 value).
Every mechanic (Damage, a Card, a point of Health, 1 AP, Gold, Good Luck,
a stack of Protected, and so on) has its own value-per-unit relative to
that anchor — see `flagonquest_balance_notes_model.md` for the full
breakdown of Baseline/THE TABEL/BALANCE and exactly how Value, Target, and
Net are computed for a Technique. Masterwork items don't share Techniques'
clean `Level × 3` Target formula, so balancing them is more about relative
comparison against similarly-priced existing entries than a hard
pass/fail number.

## Historical Masterwork/magic-item pricing logic (from the old site)

Pulled from `archive/flagonquest_site_other.md` (the old Google Sites
export's "DM Notes" and "System Mk 2" sections) while looking for the
usage-frequency assumptions behind Masterwork pricing. Two passes, from
different eras — kept both since the later one's derivation explains
*why* the current flat `Level × 20` pricing looks the way it does, even
though neither era's actual numbers are what's live today.

**Earlier pass — Common/Uncommon/Rare/Extraordinary tiers ("DM Notes").**
Masterwork items priced 6/12/24/48 Gold across four power tiers, each
with a rough Technique-Level equivalent:
- **Common** — minor, convenient power ("a weapon that turns into other
  weapon types"), roughly mimics a Level 1 ability with restrictions.
- **Uncommon** — real passive mechanical benefit (inherent Pushes,
  always-on weapon/armor bonuses), roughly a Level 2 ability with
  little restriction.
- **Rare** — a substantial, constant bonus (temp HP every fight,
  extended spell range) — powerful enough to stop trying to mimic
  specific abilities, but called "Level 4-ish" if it did.
- **Extraordinary** — "the dumpster for everything that's disgustingly
  good" — top tier, minimal restraint.

Assumed a character ends up with **~7 magic items total** (1
Extraordinary + 1 Rare + 2 Uncommon + 3 Common), and set a broader Gold
benchmark: **1200 Gold ≈ "the average magic item a party could
realistically afford to buy."**

**Later, more refined pass — the actual per-use derivation ("System Mk
2").** This is the part that looks like the real ancestor of the
current design philosophy:
1. Assumed consumable spending of ~1.5 Gold/session (1 Healing
   Potion/session + 1 tricky-fight consumable every other session), and
   ~1.5 fights/session — working out to **roughly 1 Gold of consumable
   value "spent" per fight**.
2. Asked: how many times would a character need to *use* a static
   magic item for its passive benefit to match that same per-fight
   value? Picked **12 uses** as the benchmark ("because it's
   convenient").
3. Item price = (per-fight consumable value) × 12 — sanity-checked
   against Fortifying Concoction: 6 Gold ≈ 12 uses of "2 temp Health
   for a scene," so a Level 2 item priced at 6 Gold should deliver
   about that much passive benefit.
4. Produces a Level-based pricing ladder: **Level 2 = 6G, Level 3 =
   12G, Level 4 = 24G, Level 5 = 36G** (a later note revises the top
   end from the earlier pass's 48 down to 36).

**Takeaway.** The throughline across both old passes, and into the
current flat `Level × 20` Masterwork pricing, is consistent: **a
Masterwork item's value is calibrated against a consumable of the same
Level, used repeatedly (the old math landed on ~12 times) rather than
once.** The current system dropped the granular Gold-tier/use-count
bookkeeping in favor of round numbers, but the underlying assumption —
Masterwork items are priced like Techniques of their Level because
they're assumed to get used enough over time to be worth it, same as
the user confirmed when this file was started — looks unchanged. Worth
keeping in mind for the upcoming Masterwork balance pass: if a
drafted item's power doesn't obviously look like it'd get used ~12
times per relevant span (session, or however "makes par" ends up being
defined for the current system), that's a signal its Level or its
actual effect may need adjusting, not just its raw Value-model number.

## Open balance work

- **The full Masterwork list, 103 items total** (`items.csv` `I057`-`I115`
  pre-existing, plus `I148`-`I165`, `I168`-`I189`, and `I208`-`I211`
  newly drafted across three gap-fill passes — see `RULES_DESIGN.md`'s
  "Old-docs review," "Site export gap-fill," and "Final Masterwork
  completeness/dedup sweep" entries) needs to be run through the value
  model to get properly statted and leveled — this is the next planned
  pass, and the gap-fill work feeding it is now done. `I210` Scaraculpi's
  Gleaming Justice (unconditional Good Luck on all attacks, no action
  cost) is flagged in RULES_DESIGN.md as a first candidate worth
  sanity-checking, since it's stronger than `I103` Thrumming Focus's
  otherwise-similar AP-gated version.
- The site-export batch also added 18 non-Masterwork items (`I190`-`I207`)
  that don't need value-model leveling but should get a normal
  price/rarity sanity check alongside the rest.

## Passes completed

*(none yet — entries land here as balance passes actually happen)*
