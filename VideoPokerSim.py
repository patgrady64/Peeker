import random
from HandAnalyzer import HandAnalyzer


class VideoPokerSim:
    def __init__(self, deck_class, initial_bankroll=100.0, bet_amount=1.0):
        self.Deck = deck_class
        self.bankroll = initial_bankroll
        self.bet_amount = bet_amount
        self.stats = {
            "hands_played": 0,
            "total_invested": 0,
            "total_returned": 0,
            "wins": 0,
            "losses": 0,
            "big_wins": []
        }

    def run_session(self, num_hands=100, silent=False):
        print(f"\n>>> Starting Perfect-Play Session: {num_hands} Hands")

        for i in range(num_hands):
            # 1. Initialize your Deck (Constructor calls new() and shuffle() automatically)
            deck_instance = self.Deck()

            # 2. Pay for the hand
            self.bankroll -= self.bet_amount
            self.stats["total_invested"] += self.bet_amount
            self.stats["hands_played"] += 1

            # 3. Deal 5 cards using your dealOne() method
            initial_hand = [deck_instance.dealOne() for _ in range(5)]

            # 4. Analyze strategy
            # Passing the hand and the actual list of remaining cards
            analyzer = HandAnalyzer(initial_hand, deck_instance.cards)
            analyzer.find_optimal_move()

            # 5. Execute Best Move
            best_move = analyzer.best_move
            num_to_draw = 5 - len(best_move['cards'])

            # Complete the hand using dealOne()
            final_hand = best_move['cards'] + [deck_instance.dealOne() for _ in range(num_to_draw)]

            # 6. Evaluate Result
            rank, val = analyzer.evaluate_hand_fast(final_hand)
            payout = analyzer.get_payout(rank, val) * self.bet_amount

            # 7. Update Stats
            self.bankroll += payout
            self.stats["total_returned"] += payout

            if payout > 0:
                self.stats["wins"] += 1
                # Track hits that pay 5x or more (Flush+)
                if payout >= (self.bet_amount * 5):
                    self.stats["big_wins"].append(f"Hand #{i + 1}: {rank.name} (+{payout})")
            else:
                self.stats["losses"] += 1

            if not silent and (i + 1) % 10 == 0:
                print(f"Progress: {i + 1}/{num_hands} | Bankroll: {self.bankroll:.2f}")

        self.show_report()

    def show_report(self):
        roi = (self.stats["total_returned"] / self.stats["total_invested"]) * 100
        net = self.stats["total_returned"] - self.stats["total_invested"]

        print("\n" + "=" * 50)
        print(f"{'SESSION SUMMARY':^50}")
        print("=" * 50)
        print(f"Total Hands:     {self.stats['hands_played']}")
        print(f"Final Bankroll:  {self.bankroll:.2f}")
        print(f"Net Profit/Loss: {net:+.2f}")
        print(f"Return (ROI):    {roi:.2f}%")
        print(f"Win Frequency:   {(self.stats['wins'] / self.stats['hands_played']) * 100:.1f}%")

        if self.stats["big_wins"]:
            print("\n--- Top Hits ---")
            for win in self.stats["big_wins"][-5:]:
                print(win)
        print("=" * 50 + "\n")