class Player:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def printCards(self):
        for card in self.cards:
            card.showFull()