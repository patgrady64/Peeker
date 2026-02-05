from Deck import Deck
from Player import Player
from HandAnalyzer import HandAnalyzer

if __name__ == '__main__':
    deck = Deck()
    player = Player()
    for i in range(5):
        player.add(deck.dealOne())
    # player.inject(["5s", "jc", "jh", "5d", "js"], deck)
    player.print_cards()
    analyzed = HandAnalyzer(player.get_cards, deck.get_cards)
    analyzed.analyze()