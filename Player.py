import Card
import Deck

class Player:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def print_cards(self):
        for card in self.cards:
            card.print_full()

    def inject(self, cards_to_inject, deck):
        self.cards.clear()
        for c in cards_to_inject:
            # Input is "jh", "8h", etc.
            val = c[0]  # 'j'
            suit = c[1]  # 'h'
            # IMPORTANT: Match your Card(suit, value) constructor exactly
            self.cards.append(Card.Card(suit, val))

        deck.inject(self.cards)

    @property
    def get_cards(self):
        return self.cards