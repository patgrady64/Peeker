from collections import Counter

class HandAnalyzer(object):
    def __init__(self, cards, deck):
        self.player_cards = cards
        self.remaining_deck = deck
        self.rank_name = None
        self.rank_value = None
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)

    def check_straight(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        if card_values[4] - card_values[0] == 4 or card_values == [2, 3, 4, 5, 14]:
            return True
        else:
            return False

    def check_flush(self):
        suits = [card.get_int_suit for card in self.player_cards]
        return len(set(suits)) == 1

    def check_straight_flush(self):
        if self.check_flush() and self.check_straight():
            return True
        else:
            return False

    def check_four_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 4 in value_counts.values()

    def check_full_house(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 2 in value_counts.values() and 3 in value_counts.values()

    def check_three_of_a_kind(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        return 1 in value_counts.values() and 3 in value_counts.values()

    def check_two_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        counter_counts = Counter(list(value_counts.values()))
        return list(counter_counts.values()) == [1,2] or list(counter_counts.values()) == [2,1]

    def check_pair(self):
        card_values = [card.get_int_value for card in self.sorted_hand]
        value_counts = dict(Counter(card_values))
        counter_counts = Counter(list(value_counts.values()))
        return list(counter_counts.values()) == [1,3] or list(counter_counts.values()) == [3,1]

    def analyze(self):
        if self.check_straight_flush() and self.player_cards[0].get_int_value == 10:
            self.rank_name = "Royal Flush"
            self.rank_value = 10
            return
        if self.check_straight_flush():
            self.rank_name = "Straight Flush"
            self.rank_value = 9
            return
        if self.check_four_of_a_kind():
            self.rank_name = "Four of a Kind"
            self.rank_value = 8
            return
        if self.check_full_house():
            self.rank_name = "Full House"
            self.rank_value = 7
            return
        if self.check_flush():
            self.rank_name = "Flush"
            self.rank_value = 6
            return
        if self.check_straight():
            self.rank_name = "Straight"
            self.rank_value = 5
            return
        if self.check_three_of_a_kind():
            self.rank_name = "Three of a Kind"
            self.rank_value = 4
            return
        if self.check_two_pair():
            self.rank_name = "Two Pair"
            self.rank_value = 3
            return
        if self.check_pair():
            self.rank_name = "Pair"
            self.rank_value = 2
            return
        self.rank_name = "High Card"
        self.rank_value = 1

    def print_hand_rank(self):
            print(self.rank_name)