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
        self.new()  # Reset to 52
        # Use a list comprehension to filter - it's much safer than .remove()
        for target in cards_to_inject:
            self.cards = [c for c in self.cards if not (c.value == target.value and c.suit == target.suit)]

        print(f"DEBUG: Deck size after inject: {len(self.cards)}")  # This MUST say 47

    def shuffle(self):
        random.shuffle(self.cards)

    def dealOne(self):
        return self.cards.pop()

    @property
    def get_cards(self):
        return self.cards