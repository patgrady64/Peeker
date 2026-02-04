import Deck
import Player
import HandAnalyzer

if __name__ == '__main__':
    deck = Deck.Deck()
    player = Player.Player()
    # for i in range(5):
    #     player.add(deck.dealOne())
    player.inject(["4s", "5c", "6s", "7s", "8s"], deck)
    player.print_cards()
    analyzed = HandAnalyzer.HandAnalyzer(player.get_cards, deck.get_cards)
    analyzed.analyze()
    analyzed.print_hand_rank()