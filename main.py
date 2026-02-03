import Deck
import Player

if __name__ == '__main__':
    deck = Deck.Deck()
    player = Player.Player()
    for i in range(5):
        player.add(deck.dealOne())
    player.printCards()