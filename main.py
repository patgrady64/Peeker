from Deck import Deck
from Player import Player
from HandAnalyzer import HandAnalyzer
from VideoPokerSim import VideoPokerSim

if __name__ == '__main__':
    deck = Deck()
    player = Player()
    # for i in range(5):
    #     player.inject(["3h", "3c", "3d", "ah", "as"], deck)
    # player.print_cards()
    # analyzed = HandAnalyzer(player.get_cards, deck.get_cards)
    # analyzed.analyze()

    # Create the simulator, passing your classes in
    sim = VideoPokerSim(Deck, initial_bankroll=200, bet_amount=1)

    # Run 500 hands
    sim.run_session(num_hands=500, silent=False)