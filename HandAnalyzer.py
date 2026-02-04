from collections import Counter
from HandRanks import HandRanks

class HandAnalyzer(object):
    def __init__(self, cards, deck):
        self.player_cards = cards
        self.remaining_deck = deck
        self.rank = None
        self.description = None
        self.primary = None
        self.secondary = None
        self.kicker = None
        # self.rank_value_lookup = {"High Card": 1, "Pair": 2, "Two Pair": 3, "Three of a Kind": 4, "Straight": 5, "Flush": 6, "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10}
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)

    def is_straight(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        if (card_values[4] - card_values[0] == 4 and len(set(card_values)) == 5) or card_values == [2, 3, 4, 5, 14]:
            return True
        else:
            return False

    def is_flush(self):
        suits = [card.get_int_suit for card in self.sorted_hand]
        return len(set(suits)) == 1

    def is_straight_flush(self):
        if self.is_flush() and self.is_straight():
            return True
        else:
            return False

    def is_four_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        if 4 in value_counts.values():
            self.primary = [rank for rank, count in value_counts.items() if count == 4][0]
            self.kicker = [rank for rank, count in value_counts.items() if count == 1][0]
            return True
        else:
            return False

    def is_full_house(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        if 2 in value_counts.values() and 3 in value_counts.values():
            self.primary = [r for r, c in value_counts.items() if c == 3][0]
            self.secondary = [r for r, c in value_counts.items() if c == 2][0]
            return True
        else:
            return False

    def is_three_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        if len(set(card_values)) == 3 and max(value_counts.values()) == 3:
            self.primary = [rank for rank, count in value_counts.items() if count == 3][0]
            remaining = [rank for rank in card_values if rank != self.primary]
            self.kicker = max(remaining)
            return True
        else:
            return False

    def is_two_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        if len(set(card_values)) == 3 and max(value_counts.values()) == 2:
            pairs = [rank for rank, count in value_counts.items() if count == 2]
            self.primary = max(pairs)
            self.secondary = min(pairs)
            self.kicker = [rank for rank, count in value_counts.items() if count == 1][0]
            return True
        else:
            return False

    def is_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        if len(set(card_values)) == 4:
            counts = Counter(card_values)
            self.primary = [rank for rank, count in counts.items() if count == 2][0]
            return True
        else:
            return False

    def analyze(self):
        if self.is_straight_flush() and self.player_cards[0].get_int_value == 10:
            self.rank = HandRanks.ROYAL_FLUSH
            return
        if self.is_straight_flush():
            self.rank = HandRanks.STRAIGHT_FLUSH
            return
        if self.is_four_of_a_kind():
            self.rank = HandRanks.FOUR_OF_A_KIND
            return
        if self.is_full_house():
            self.rank = HandRanks.FULL_HOUSE
            return
        if self.is_flush():
            self.rank = HandRanks.FLUSH
            return
        if self.is_straight():
            self.rank = HandRanks.STRAIGHT
            return
        if self.is_three_of_a_kind():
            self.rank = HandRanks.THREE_OF_A_KIND
            return
        if self.is_two_pair():
            self.rank = HandRanks.TWO_PAIR
            return
        if self.is_pair():
            self.rank = HandRanks.PAIR
            return
        self.rank = HandRanks.HIGH_CARD
    #      {max(self.sorted_hand, key=lambda c: c.get_int_value).get_value_name}

    def print_hand_rank(self):
            print(f"{self.rank}")