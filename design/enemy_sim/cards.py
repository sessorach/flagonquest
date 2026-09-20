"""
A single, named place for "which suit is this card" assumptions. This
sim has no real deck/hand/suit-pool tracking (see combat_sim.py's own
module docstring - no Extra Successes from suit-pool matching either),
so any mechanic that cares about a card's suit (Healing Magic's Hearts,
a future Spades-keyed Push, a Diamonds-keyed Vulnerable, etc.) needs a
documented stand-in instead of re-deriving "how likely is this" ad hoc
at each call site.

Two cases, matching how rulebook.md itself splits "flip a card" from
"discard/play a card":

- A **flipped** card (an attack roll, a Skill check) is genuinely random
  - the player doesn't choose it. `flipped_matches(suit)` models this as
  an even 1-in-4 roll, a standard deck's own 4-suit split.
- A **discarded/played** card (paying a cost, like Healing Magic's
  "Discard [Level] cards") is chosen by the player from their whole
  hand, not flipped - rulebook.md's own Hand rules: "you may play any
  number of cards from your hand." `chosen_matches(suit)` models this as
  always true - not a claim that every possible hand always contains
  that suit, but a reasonable stand-in specifically for a cost that's a
  small slice of a full hand (Healing Magic's own use here spends at
  most hand_size // 4 cards this way - see party.py's Support
  paragraph), where a player who wants a specific suit for a chosen
  cost can usually find one.
"""
import random

SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")


def flipped_matches(suit):
    """True if a genuinely random flipped card happens to be `suit`."""
    return random.choice(SUITS) == suit


def chosen_matches(suit):
    """True, always - see the module docstring for when this stand-in
    for a player-chosen discard/play is (and isn't) reasonable."""
    return True
