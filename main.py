from Deck import Deck
from Player import Player
from HandAnalyzer import HandAnalyzer

if __name__ == '__main__':
    deck = Deck()
    player = Player()
    for i in range(5):
        player.inject(["3h", "3c", "3d", "ah", "as"], deck)
    player.print_cards()
    analyzed = HandAnalyzer(player.get_cards, deck.get_cards)
    analyzed.analyze()