from collections import Counter
from HandRank import HandRank
from PayoutTable import PAYOUT_TABLE
import itertools
import threading
from math import comb

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
        self.memo = {}
        self.memo_full = {}  # Exact hand (Rank + Suit)
        self.memo_pattern = {}  # Pattern (Just Ranks)

    def evaluate_hand_fast(self, cards):
        # 1. Create the Full Fingerprint (Rank + Suit)
        full_key = tuple(sorted([(c.get_int_value, c.get_int_suit) for c in cards]))
        if full_key in self.memo_full:
            return self.memo_full[full_key]

        # 2. Check if a Flush or Straight is even possible
        # (If suits are all different or ranks are far apart, we can skip suit logic)
        suits = [c.get_int_suit for c in cards]
        ranks = sorted([c.get_int_value for c in cards])

        is_flush_possible = len(set(suits)) == 1
        # Simple check for straight: max - min must be 4 (or Ace-low)
        is_straight_possible = (ranks[4] - ranks[0] <= 4) or (ranks == [2, 3, 4, 5, 14])

        # 3. If neither is possible, use the Pattern Cache
        if not is_flush_possible and not is_straight_possible:
            pattern_key = tuple(ranks)
            if pattern_key in self.memo_pattern:
                return self.memo_pattern[pattern_key]

            # Calculate once, save to pattern cache
            result = self.evaluate_hand(cards, False)
            self.memo_pattern[pattern_key] = result
            return result

        # 4. Otherwise, calculate the full hand and save to full cache
        result = self.evaluate_hand(cards, False)
        self.memo_full[full_key] = result
        return result

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
        self.memo_full.clear()
        self.memo_pattern.clear()

        try:
            self.get_all_hold_combinations()
            self.find_optimal_move()

            print("\n" + "=" * 50)
            print("FINAL STRATEGY DECISION")
            print("=" * 50)

            if self.best_move:
                print(f"ACTION: {self.format_move(self.best_move)}")
                print(f"EXPECTED VALUE: {self.best_ev:.4f}")
            else:
                print("ACTION: Discard All")
                print(f"EXPECTED VALUE: {self.best_ev:.4f}")

            print("=" * 50 + "\n")

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
        # If hand_rank is an Enum (like HandRank.PAIR),
        # make sure PAYOUT_TABLE has that Enum as a key.
        payout = PAYOUT_TABLE.get(hand_rank, 0)

        if hand_rank == HandRank.PAIR:
            return payout if rank_val >= 11 else 0

        return payout

    def calculate_hold_ev(self, held_cards):
        num_to_draw = 5 - len(held_cards)

        # 1. Instant Case: No cards to draw
        if num_to_draw == 0:
            hr, rv = self.evaluate_hand_fast(held_cards)
            return self.get_payout(hr, rv)

        total_payout = 0
        count = 0

        # 2. Decision Engine: Exact vs. Sampling
        # Draw 1: 47 combos (Exact)
        # Draw 2: 1,081 combos (Exact)
        # Draw 3: 16,215 combos (Exact - takes ~0.2 seconds)
        # Draw 4/5: 178k to 2.6M (Sampled)

        is_exact = num_to_draw <= 3
        sample_limit = 10000  # Enough for 99.9% accuracy on big draws

        # 3. Execution
        all_draws = itertools.combinations(self.remaining_deck, num_to_draw)

        for draw in all_draws:
            possible_hand = list(held_cards) + list(draw)

            # Use our fast cache-based evaluator
            rank_enum, rank_val = self.evaluate_hand_fast(possible_hand)
            total_payout += self.get_payout(rank_enum, rank_val)

            count += 1

            # If we aren't doing Exact math, stop at the limit
            if not is_exact and count >= sample_limit:
                break

        return total_payout / count if count > 0 else 0

    def find_optimal_move(self):
        self.best_ev = -1.0
        self.best_move = None

        print("Thinking...", end="", flush=True)
        for i, move in enumerate(self.all_possible_holds):
            if i % 4 == 0:
                print(".", end="", flush=True)

            current_ev = self.calculate_hold_ev(move["cards"])

            # --- THE MISSING LINK ---
            # Compare the result of this move to the best one we've seen so far
            if current_ev > self.best_ev:
                self.best_ev = current_ev
                self.best_move = move

        print(" Done!")

    def is_straight(self, cards):
        if len(cards) != 5:
            return False

        # CRITICAL: Sort the integers so [0] is the lowest and [4] is the highest
        values = sorted([c.get_int_value for c in cards])

        # Check for unique cards (no pairs)
        if len(set(values)) != 5:
            return False

        # Standard Straight (Highest - Lowest == 4)
        if values[4] - values[0] == 4:
            return True

        # Ace-Low Straight [2, 3, 4, 5, 14]
        if values == [2, 3, 4, 5, 14]:
            return True

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
        # CRITICAL: If the hand isn't finished, it's worth 0 credits.
        # This prevents the bot from thinking 3 suited cards = a Flush.
        if len(cards) != 5:
            return HandRank.HIGH_CARD, 0

        # Sort to ensure straight/rank logic works
        sorted_cards = sorted(cards, key=lambda c: c.get_int_value)

        final_rank = HandRank.HIGH_CARD
        primary = sorted_cards[-1].get_int_value
        secondary = None
        kicker = None

        # Now run your checks (is_flush, is_straight, etc.)
        if self.is_straight_flush(sorted_cards):
            final_rank = HandRank.ROYAL_FLUSH if sorted_cards[0].get_int_value == 10 else HandRank.STRAIGHT_FLUSH
            primary = sorted_cards[-1].get_int_value

        elif self.is_four_of_a_kind(sorted_cards)[0]:
            _, primary, kicker = self.is_four_of_a_kind(sorted_cards)
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

        elif self.is_pair(sorted_cards)[0]:
            _, primary = self.is_pair(sorted_cards)
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

    def format_move(self, move):
        if not move:
            return "No move found."

        # Mappings to turn integers back into readable strings
        rank_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        # If it's not in the map (2-10), just use the number itself

        suit_map = {1: '♣', 3: '♦', 2: '♥', 4: '♠'}  # Adjust these to match your get_int_suit values

        mask = move["mask"]
        output = []

        for i, bit in enumerate(mask):
            card = self.player_cards[i]

            # Get rank string (e.g., 12 -> 'Q')
            rv = card.get_int_value
            r_str = rank_map.get(rv, str(rv))

            # Get suit icon
            s_icon = suit_map.get(card.get_int_suit, "?")

            card_display = f"[{r_str}{s_icon}]"

            if bit == 1:
                output.append(f"HOLD {card_display}")
            else:
                output.append(f"     {card_display}")

        return " | ".join(output)

    def print_hand_rank(self):
        if self.rank is not None:
            name = self.rank.name.replace("_", " ").title()
            print(f"Hand Rank: {name}")
        else:
            # Check if the thread is still alive
            print(f"Hand Rank: [Calculating...] (self.rank is currently None)", flush=True)
