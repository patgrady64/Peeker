class Card(object):
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit
        self.full_value_lookup = {"2": "Two", "3": "Three", "4": "Four", "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine", "t": "Ten", "j": "Jack", "q": "Queen", "k": "King", "a": "Ace"}
        self.full_value_plural_lookup = {"2": "Twos", "3": "Threes", "4": "Fours", "5": "Fives", "6": "Sixes", "7": "Sevens", "8": "Eights", "9": "Nines", "t": "Tens", "j": "Jacks", "q": "Queens", "k": "Kings", "a": "Aces"}
        self.int_value_lookup = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "t": 10, "j": 11, "q": 12, "k": 13, "a": 14}
        self.int_suit_lookup = {"c": 1, "s": 2, "h": 3, "d": 4}
        self.full_suit_lookup = {"c": "Clubs", "s": "Spades", "h": "Hearts", "d": "Diamonds"}

    def print_full(self):
        print(f"{self.full_value_lookup[self.value]} of {self.full_suit_lookup[self.suit]}")

    def print_mini(self):
        print(f"{self.value}{self.suit}")

    @property
    def get_int_value(self):
        return self.int_value_lookup[self.value]

    @property
    def get_int_suit(self):
        return self.int_suit_lookup[self.suit]