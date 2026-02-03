import random
import Card

class Deck(object):
    def __init__(self):
        self.cards = []
        self.new()
        self.shuffle()

    def new(self):
        for s in ["c", "d", "h", "s"]:
            for v in ["2", "3", "4", "5", "6", "7", "8", "9", "t", "j", "q", "k", "a"]:
               self.cards.append(Card.Card(s, v))

    def inject(self, cards_to_inject):
        self.cards.clear()
        self.new()
        for card in cards_to_inject:
            for check in self.cards:
                if card.get_int_value == check.get_int_value and card.get_int_suit == check.get_int_suit:
                    self.cards.remove(check)



    def shuffle(self):
        random.shuffle(self.cards)

    def dealOne(self):
        return self.cards.pop()

    @property
    def get_cards(self):
        return self.cards