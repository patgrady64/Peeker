from collections import Counter

class HandAnalyzer(object):
    def __init__(self, cards, deck):
        self.player_cards = cards
        self.remaining_deck = deck
        self.rank_name = None
        self.rank_value_lookup = {"High Card": 1, "Pair": 2, "Two Pair": 3, "Three of a Kind": 4, "Straight": 5, "Flush": 6, "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10}
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)

    def is_straight(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        if card_values[4] - card_values[0] == 4 or card_values == [2, 3, 4, 5, 14]:
            return True
        else:
            return False

    def is_flush(self):
        suits = [card.get_int_suit for card in self.player_cards]
        return len(set(suits)) == 1

    def is_straight_flush(self):
        if self.is_flush() and self.is_straight():
            return True
        else:
            return False

    def is_four_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 4 in value_counts.values()

    def is_full_house(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 2 in value_counts.values() and 3 in value_counts.values()

    def is_three_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 1 in value_counts.values() and 3 in value_counts.values()

    def is_two_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        counter_counts = Counter(list(value_counts.values()))
        return list(counter_counts.values()) == [1,2] or list(counter_counts.values()) == [2,1]

    def is_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        counter_counts = Counter(list(value_counts.values()))
        return list(counter_counts.values()) == [1,3] or list(counter_counts.values()) == [3,1]

    def analyze(self):
        if self.is_straight_flush() and self.player_cards[0].get_int_value == 10:
            self.rank_name = "Royal Flush"
            return
        if self.is_straight_flush():
            self.rank_name = "Straight Flush"
            return
        if self.is_four_of_a_kind():
            self.rank_name = "Four of a Kind"
            return
        if self.is_full_house():
            self.rank_name = "Full House"
            return
        if self.is_flush():
            self.rank_name = "Flush"
            return
        if self.is_straight():
            self.rank_name = "Straight"
            return
        if self.is_three_of_a_kind():
            self.rank_name = "Three of a Kind"
            return
        if self.is_two_pair():
            self.rank_name = "Two Pair"
            return
        if self.is_pair():
            self.rank_name = "Pair"
            return
        self.rank_name = "High Card"

    def print_hand_rank(self):
            print(self.rank_name)