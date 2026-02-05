from collections import Counter
from HandRank import HandRank
from PayoutTable import PAYOUT_TABLE
import itertools
import threading

class HandAnalyzer(object):
    def __init__(self, cards, deck):
        self.player_cards = cards
        self.remaining_deck = deck
        self.rank = None
        self.description = None
        self.primary = None
        self.secondary = None
        self.kicker = None
        self.all_possible_holds = []
        self.best_ev = -1
        self.best_move = None
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)

    def analyze(self):
        # 1. Player's hand (Instant)
        self.rank, self.primary = self.evaluate_hand(self.sorted_hand, True)
        print(f"Rank identified: {self.rank.name}", flush=True)

        # 2. Start the heavy math
        # We remove 'daemon=True' so the script doesn't kill the thread on exit
        analysis_thread = threading.Thread(target=self.run_heavy_analysis)
        analysis_thread.start()

        print("Analyzing 32 strategies... please wait (this takes a few seconds).", flush=True)

        # 3. FORCE the main script to wait for the thread to finish
        analysis_thread.join()
        print("All done!")

    def run_heavy_analysis(self):
        try:
            self.get_all_hold_combinations()
            self.find_optimal_move()

            # This will now print ONLY when all 32 combinations are finished
            print(f"BEST MOVE: {self.best_move}", flush=True)
            print(f"EXPECTED VALUE: {self.best_ev:.2f}", flush=True)

        except Exception as e:
            import traceback
            print(f"!!! Analysis Error: {e}")
            traceback.print_exc()

    def get_all_hold_combinations(self):
        self.all_possible_holds = []  # CLEAR THE LIST FIRST
        bit_masks = list(itertools.product([0, 1], repeat=5))

        for mask in bit_masks:
            held_cards = [self.player_cards[i] for i in range(5) if mask[i] == 1]
            self.all_possible_holds.append({
                "mask": mask,
                "cards": held_cards
            })

    def get_payout(self, hand_rank, rank_val):
        if hand_rank == HandRank.PAIR:
            # Jack=11, Queen=12, King=13, Ace=14
            if rank_val >= 11:
                return PAYOUT_TABLE.get(HandRank.PAIR, 0)
            return 0
        return PAYOUT_TABLE.get(hand_rank, 0)

    def calculate_hold_ev(self, held_cards):
        num_to_draw = 5 - len(held_cards)

        if num_to_draw == 0:
            hr, rv = self.evaluate_hand(held_cards, False)
            return self.get_payout(hr, rv)

        total_payout = 0
        count = 0

        # SPEED LIMIT: Stop after this many combinations
        max_samples = 5000

        # We keep the generator here (no list() call) to save RAM
        for draw in itertools.combinations(self.remaining_deck, num_to_draw):
            possible_hand = held_cards + list(draw)
            sorted_possible = sorted(possible_hand, key=lambda c: c.get_int_value)

            rank_enum, rank_val = self.evaluate_hand(sorted_possible, False)
            total_payout += self.get_payout(rank_enum, rank_val)

            count += 1

            # --- THIS IS WHERE THE SPEED HAPPENS ---
            if count >= max_samples:
                break

        return total_payout / count if count > 0 else 0

    def find_optimal_move(self):
        self.best_ev = -1.0  # Use a float
        self.best_move = self.all_possible_holds[0]  # Default to 'Hold All' or 'Discard All'

        for move in self.all_possible_holds:
            current_ev = self.calculate_hold_ev(move["cards"])

            # Use >= to ensure we at least get the first move analyzed
            if current_ev >= self.best_ev:
                self.best_ev = current_ev
                self.best_move = move

    def is_straight(self, cards):
        card_values = [card.get_int_value for card in cards]
        if (card_values[4] - card_values[0] == 4 and len(set(card_values)) == 5) or card_values == [2, 3, 4, 5, 14]:
            return True
        else:
            return False

    def is_flush(self, cards):
        suits = [card.get_int_suit for card in cards]
        return len(set(suits)) == 1

    def is_straight_flush(self, cards):
        if self.is_flush(cards) and self.is_straight(cards):
            return True
        else:
            return False

    def is_four_of_a_kind(self, cards):
        card_values = [card.get_int_value for card in cards]
        value_counts = Counter(card_values)
        if 4 in value_counts.values():
            primary = [rank for rank, count in value_counts.items() if count == 4][0]
            kicker = [rank for rank, count in value_counts.items() if count == 1][0]
            return True, primary, kicker
        return False, None, None

    def is_full_house(self, cards):
        card_values = [card.get_int_value for card in cards]
        value_counts = Counter(card_values)
        if 2 in value_counts.values() and 3 in value_counts.values():
            primary = [r for r, c in value_counts.items() if c == 3][0]
            secondary = [r for r, c in value_counts.items() if c == 2][0]
            return True, primary, secondary
        return False, None, None

    def is_three_of_a_kind(self, cards):
        card_values = [card.get_int_value for card in cards]
        value_counts = Counter(card_values)
        if 3 in value_counts.values():
            primary = [r for r, c in value_counts.items() if c == 3][0]
            # Get highest kicker that isn't the triple
            kicker = max([r for r in card_values if r != primary])
            return True, primary, kicker
        return False, None, None

    def is_two_pair(self, cards):
        card_values = [card.get_int_value for card in cards]
        value_counts = Counter(card_values)
        pairs = [rank for rank, count in value_counts.items() if count == 2]
        if len(pairs) == 2:
            primary = max(pairs)
            secondary = min(pairs)
            kicker = [rank for rank, count in value_counts.items() if count == 1][0]
            return True, primary, secondary, kicker
        return False, None, None, None

    def is_pair(self, cards):
        card_values = [card.get_int_value for card in cards]
        value_counts = Counter(card_values)
        if 2 in value_counts.values():
            primary = [rank for rank, count in value_counts.items() if count == 2][0]
            return True, primary
        return False, None

    def evaluate_hand(self, cards, is_player):
        # 1. Setup default values
        final_rank = HandRank.HIGH_CARD
        primary = cards[-1].get_int_value if cards else 0
        secondary = None
        kicker = None

        # 2. Logic Hierarchy
        # We check from best hand to worst hand

        # ROYAL / STRAIGHT FLUSH
        if self.is_flush(cards) and self.is_straight(cards):
            final_rank = HandRank.ROYAL_FLUSH if cards[0].get_int_value == 10 else HandRank.STRAIGHT_FLUSH
            primary = cards[-1].get_int_value

        elif self.is_four_of_a_kind(cards)[0]:
            _, primary, kicker = self.is_four_of_a_kind(cards)
            final_rank = HandRank.FOUR_OF_A_KIND

        elif self.is_full_house(cards)[0]:
            _, primary, secondary = self.is_full_house(cards)
            final_rank = HandRank.FULL_HOUSE

        elif self.is_flush(cards):
            final_rank = HandRank.FLUSH
            primary = cards[-1].get_int_value

        elif self.is_straight(cards):
            final_rank = HandRank.STRAIGHT
            primary = cards[-1].get_int_value

        elif self.is_three_of_a_kind(cards)[0]:
            _, primary, kicker = self.is_three_of_a_kind(cards)
            final_rank = HandRank.THREE_OF_A_KIND

        elif self.is_two_pair(cards)[0]:
            _, primary, secondary, kicker = self.is_two_pair(cards)
            final_rank = HandRank.TWO_PAIR

        elif self.is_pair(cards)[0]:
            _, primary = self.is_pair(cards)
            final_rank = HandRank.PAIR

        else:
            # Default: High Card
            final_rank = HandRank.HIGH_CARD
            primary = cards[-1].get_int_value if cards else 0

        # 3. Update the Object State
        if is_player:
            self.rank = final_rank
            self.primary = primary
            self.secondary = secondary
            self.kicker = kicker

        # 4. THE ONLY RETURN POINT
        # Ensure this is at the same indentation level as the VERY FIRST 'if'
        return final_rank, primary

    def print_hand_rank(self):
        if self.rank is not None:
            name = self.rank.name.replace("_", " ").title()
            print(f"Hand Rank: {name}")
        else:
            # Check if the thread is still alive
            print(f"Hand Rank: [Calculating...] (self.rank is currently None)", flush=True)
