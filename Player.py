import Card
import Deck

class Player:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def print_cards(self):
        for card in self.cards:
            card.show_full()

    def inject(self,cards_to_inject, deck):
        self.cards.clear()
        for c in cards_to_inject:
            self.cards.append(Card.Card(c[1], c[0]))
        deck.inject(self.cards)

    @property
    def get_cards(self):
        return self.cards