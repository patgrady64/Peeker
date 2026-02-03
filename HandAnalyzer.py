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

    def check_flush(self):
        suits = [card.get_int_suit for card in self.player_cards]
        return len(set(suits)) == 1

    def check_straight_flush(self):
        if self.check_flush() and self.check_straight():
            return True
        else:
            return False

    def analyze(self):
        if self.check_straight_flush() and self.player_cards[0].get_int_value == 10:
            self.rank_name = "Royal Flush"
            self.rank_value = 10
            return
        if self.check_straight_flush():
            self.rank_name = "Straight Flush"
            self.rank_value = 9
            return
        # if check_four_of_a_kind(player_cards):
        #     return 8
        # if check_full_house(player_cards):
        #     return 7
        if self.check_flush():
            self.rank_name = "Flush"
            self.rank_value = 6
            return
        if self.check_straight():
            self.rank_name = "Straight"
            self.rank_value = 5
            return
        # if check_three_of_a_kind(player_cards):
        #     return 4
        # if check_two_pair(player_cards):
        #     return 3
        # if check_pair(player_cards):
        #     return 2
        # return 1

    def print_hand_rank(self):
            print(self.rank_name)