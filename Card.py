class Card(object):
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit
        self.full_value = None
        self.int_value = None
        self.int_suit = None
        self.full_suit = None

        match self.value:
            case "2":
                self.full_value = "Two"
                self.int_value = 2
            case "3":
                self.full_value = "Three"
                self.int_value = 3
            case "4":
                self.full_value = "Four"
                self.int_value = 4
            case "5":
                self.full_value = "Five"
                self.int_value = 5
            case "6":
                self.full_value = "Six"
                self.int_value = 6
            case "7":
                self.full_value = "Seven"
                self.int_value = 7
            case "8":
                self.full_value = "Eight"
                self.int_value = 8
            case "9":
                self.full_value = "Nine"
                self.int_value = 9
            case "t":
                self.full_value = "Ten"
                self.int_value = 10
            case "j":
                self.full_value = "Jack"
                self.int_value = 11
            case "q":
                self.full_value = "Queen"
                self.int_value = 12
            case "k":
                self.full_value = "King"
                self.int_value = 13
            case "a":
                self.full_value = "Ace"
                self.int_value = 14
        match suit:
            case "c":
                self.full_suit = "Clubs"
                self.int_suit = 1
            case "d":
                self.full_suit = "Diamonds"
                self.int_suit = 2
            case "h":
                self.full_suit = "Hearts"
                self.int_suit = 3
            case "s":
                self.full_suit = "Spades"
                self.int_suit = 4

    def show_full(self):
        print("{} of {}".format(self.full_value, self.full_suit))

    def show_mini(self):
        print("{}{}".format(self.value,self.suit))

    @property
    def get_int_value(self):
        return self.int_value

    @property
    def get_int_suit(self):
        return self.int_suit