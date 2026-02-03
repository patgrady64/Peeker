class HandAnalyzer(object):
    def __init__(self, cards, deck):
        self.player_cards = cards
        self.remaining_deck = deck
        self.rank_name = None
        self.rank_value = None
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)

    def check_straight(self, player_cards):
        return False

    def check_flush(self, player_cards):
        return False

    def check_royal_flush(self, player_cards):
        if self.check_flush(player_cards) and self.check_straight(player_cards) and player_cards[0].get_int_value == 10:
            return True
        else:
            return False

    def analyze(self):
        if self.check_royal_flush(self.player_cards):
            self.rank_name = "Royal Flush"
            self.rank_value = 10
            return
        # if check_straight_flush(player_cards):
        #     return 9
        # if check_four_of_a_kind(player_cards):
        #     return 8
        # if check_full_house(player_cards):
        #     return 7
        # if check_flush(player_cards):
        #     return 6
        # if check_straight(player_cards):
        #     return 5
        # if check_three_of_a_kind(player_cards):
        #     return 4
        # if check_two_pair(player_cards):
        #     return 3
        # if check_pair(player_cards):
        #     return 2
        # return 1