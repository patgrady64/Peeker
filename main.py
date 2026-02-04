import Deck
import Player
import HandAnalyzer

if __name__ == '__main__':
    deck = Deck.Deck()
    player = Player.Player()
    for i in range(5):
        player.add(deck.dealOne())
    # player.inject(["ts", "6s", "6c", "5c", "th"], deck)
    player.print_cards()
    analyzed = HandAnalyzer.HandAnalyzer(player.get_cards, deck.get_cards)
    analyzed.analyze()
    analyzed.print_hand_rank()