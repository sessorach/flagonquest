"""
Real cards (2026-10-09): every PC has its own 52-card deck and a hand,
the GM has one deck for every enemy, and flips draw real cards with real
suits. Switched by tunables.CARDS; with it off the sim falls back to the
old stand-ins (a uniform 1-13 flip, no suit pool, flat per-fight
"card use" counters).

The rules this follows (rulebook.md "Flips", "Your Hand and Playing
Cards", "The Suit Pool"; glossary.md Card Terms):

- A flip turns over the top card of your own deck; Ace is 1, King 13.
  Used cards go to your discard pile, and the discard is shuffled back
  in when the deck runs out.
- Good Luck flips an extra card per stack and you pick; Bad Luck the
  same, but you must use the lowest. They cancel one for one.
- After the flip, before the result, you may play cards from your hand,
  each replacing one flipped card (then Good/Bad Luck picks again), or
  just adding its suit to the suit pool. Every card flipped (replaced or
  not) and every card played is in the suit pool.
- Each card in the pool matching the Skill's suit is an Extra Success:
  +1 damage on a damaging attack. Suit riders like "Slowed 2 + [Spades]"
  count that suit in the pool.
- Sift X: look at the top X cards, discard any you don't want, shuffle
  the rest back.

How players spend the hand (TABLE_PLAY_NOTES.md, "Cards and resources")
lives in combat_sim.py, since it needs the fight's context; this module
only holds the cards themselves.

A card is an int 0-51: rank = c % 13 + 1, suit = c // 13 (an index into
SUITS).
"""
import random

import tunables as T

SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
SUIT_INDEX = {s: i for i, s in enumerate(SUITS)}
SPADES, HEARTS, DIAMONDS, CLUBS = range(4)

# Each Skill's suit (rulebook.md's list; index.html's SUIT_SKILLS).
SKILL_SUIT = {}
for _suit, _skills in (
        (HEARTS, ("Presence", "Rapport", "Performance", "Survival", "Theurgy")),
        (CLUBS, ("Brawl", "Athletics", "Resilience", "Might", "Meditation", "Sorcery")),
        (DIAMONDS, ("Acrobatics", "Craft", "Composure", "Masquerade", "Streetwise", "Mixology", "Stealth")),
        (SPADES, ("Melee", "Archery", "Awareness", "Insight", "Persuasion", "Academics", "Medicine"))):
    for _sk in _skills:
        SKILL_SUIT[_sk] = _suit


def rank(c):
    return c % 13 + 1


def suit(c):
    return c // 13


class Deck:
    """One player's (or the GM's) deck and discard pile. The pile is kept
    shuffled, so popping the end is drawing off the top."""
    __slots__ = ("pile", "discard")

    def __init__(self, exclude=()):
        skip = set(exclude)
        self.pile = [c for c in range(52) if c not in skip]
        random.shuffle(self.pile)
        self.discard = []

    def _refill(self):
        self.pile.extend(self.discard)
        self.discard = []
        random.shuffle(self.pile)
        if not self.pile:  # every card is in someone's hand; shouldn't happen
            self.pile.append(random.randrange(52))

    def flip(self):
        if not self.pile:
            self._refill()
        c = self.pile.pop()
        self.discard.append(c)
        return c

    def draw(self):
        if not self.pile:
            self._refill()
        return self.pile.pop()

    def sift(self, n, keep):
        """Sift n: look at the top n, discard the ones `keep` rejects and
        shuffle the rest back in (a random spot is the same as a shuffle,
        since the pile is already in random order). Returns the cards
        seen."""
        if n > len(self.pile):
            self._refill()
        seen = [self.pile.pop() for _ in range(min(n, len(self.pile)))]
        for c in seen:
            if keep(c):
                self.pile.insert(random.randrange(len(self.pile) + 1), c)
            else:
                self.discard.append(c)
        return seen


def flip_for(deck, good, bad):
    """One flip with `good` Good Luck and `bad` Bad Luck stacks. Returns
    (cards flipped, net luck); the value used is the highest card when
    net >= 0, the lowest when it's negative."""
    net = good - bad
    return [deck.flip() for _ in range(1 + abs(net))], net


def used_value(flipped, net):
    ranks = [rank(c) for c in flipped]
    return max(ranks) if net >= 0 else min(ranks)


def plain_flip(deck):
    """A flip nobody plays cards on (Reflex, an enemy's attack): just
    the value."""
    return rank(deck.flip())


def _stochastic_round(x):
    whole = int(x)
    return whole + (1 if random.random() < x - whole else 0)


def start_fight(pc):
    """Deals this PC's hand for the fight and sets how many cards it's
    willing to spend in it. Two fights a day (TABLE_PLAY_NOTES.md): the
    hand is the day's draw - twice Cunning plus Mind (rulebook.md's Draw
    Cycle) - minus anything paid before the day's first fight (Bottomless
    Bottles' crafting), and the budget is CARDS_FIGHT_SHARE of that. In
    a second fight (CARDS_SECOND_FIGHT_SHARE of fights) a budget's worth
    of cards is already gone. The budget is rounded at random, so a hand
    of 4 averages 1.33 cards a fight rather than always 1."""
    deck = Deck()
    hand = [deck.draw() for _ in range(pc['hand_size'])]
    # Bottomless Bottles (T053): the day's crafting discards the lowest
    # cards before the first fight (party.py's bottles_cards).
    for _ in range(min(pc.get('bottles_cards', 0), len(hand))):
        low = min(hand, key=rank)
        hand.remove(low)
        deck.discard.append(low)
    budget = min(len(hand), _stochastic_round(len(hand) * T.CARDS_FIGHT_SHARE))
    if random.random() < T.CARDS_SECOND_FIGHT_SHARE:
        for _ in range(min(budget, len(hand))):
            c = hand.pop(random.randrange(len(hand)))
            deck.discard.append(c)
        budget = min(budget, len(hand))
    pc['deck'], pc['hand'], pc['budget'] = deck, hand, budget
    pc['cards_spent'] = 0


def can_spend(pc, k=1):
    return pc.get('budget', 0) >= k and len(pc.get('hand', ())) >= k


def spend(pc, c):
    """Plays or discards card `c` from the hand: off the hand, into the
    discard pile, and out of this fight's budget."""
    pc['hand'].remove(c)
    pc['deck'].discard.append(c)
    pc['budget'] -= 1
    pc['cards_spent'] = pc.get('cards_spent', 0) + 1


def lowest(hand, prefer_suit=None):
    """The card a player throws away for a cost: the lowest of
    `prefer_suit` if they hold one, else the lowest card."""
    if prefer_suit is not None:
        of_suit = [c for c in hand if suit(c) == prefer_suit]
        if of_suit:
            return min(of_suit, key=rank)
    return min(hand, key=rank) if hand else None


def cheapest_at_least(hand, need, k=1):
    """The k lowest cards of value >= need, or None if there aren't k."""
    ok = sorted((c for c in hand if rank(c) >= need), key=rank)
    return ok[:k] if len(ok) >= k else None


_RANKS = {1: "A", 11: "J", 12: "Q", 13: "K"}
_GLYPHS = ("♠", "♥", "◆", "♣")  # the rulebook's own glyphs, ◆ not ♦


def card_str(c):
    return f"{_RANKS.get(rank(c), rank(c))}{_GLYPHS[suit(c)]}"


def highest(hand):
    return max(hand, key=rank) if hand else None


# ---- Stand-ins for CARDS off ----

def flipped_matches(suit_name):
    """True if a random flipped card happens to be `suit_name` (CARDS
    off: an even 1-in-4)."""
    return random.choice(SUITS) == suit_name


def chosen_matches(suit_name):
    """CARDS off: a player picking a card for a cost from their whole
    hand is assumed to find the suit they want."""
    return True
