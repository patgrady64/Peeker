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
        self.primary = None
        self.secondary = None
        self.kicker = None
        self.all_possible_holds = []
        self.best_ev = -1
        self.best_move = None
        self.sorted_hand = sorted(cards, key=lambda c: c.get_int_value)
        self.all_move_results = []
        self.all_possible_holds = self.generate_all_combinations()

    def generate_all_combinations(self):
        """Generates all 32 possible hold combinations using self.player_cards."""
        # Check if the attribute exists and has the expected 5 cards
        if not hasattr(self, 'player_cards') or len(self.player_cards) < 5:
            print("!!! Error: player_cards not found or incomplete.")
            return []

        combinations = []
        for i in range(32):
            mask = format(i, '05b')
            # We map the binary mask to self.player_cards
            held_cards = [self.player_cards[j] for j in range(5) if mask[j] == '1']

            combinations.append({
                "mask": mask,
                "cards": held_cards
            })

        return combinations

    def evaluate_hand_fast(self, cards):
        # 1. Safety Gate: Must have 5 cards to evaluate a rank
        if not cards or len(cards) != 5:
            return HandRank.HIGH_CARD, 0

        # 2. Extract Data
        # Using properties: .suit and .get_int_value (as per your Card class)
        suits = [c.suit for c in cards]
        values = sorted([c.get_int_value for c in cards])

        counts_map = Counter(values)
        counts_list = sorted(counts_map.values(), reverse=True)

        # 3. Check Flush (All 5 same suit)
        is_flush = len(set(suits)) == 1

        # 4. Check Straight (All 5 sequential)
        is_straight = False
        high_val = values[4]
        if len(set(values)) == 5:  # No pairs allowed in a straight
            if values[4] - values[0] == 4:
                is_straight = True
            elif values == [2, 3, 4, 5, 14]:  # Ace-low (Wheel)
                is_straight = True
                high_val = 5

        # 5. Assign Ranks (Highest to Lowest)

        # Royal / Straight Flush
        if is_flush and is_straight:
            if high_val == 14:
                return HandRank.ROYAL_FLUSH, 14
            return HandRank.STRAIGHT_FLUSH, high_val

        # Four of a Kind
        if counts_list[0] == 4:
            val = [v for v, c in counts_map.items() if c == 4][0]
            return HandRank.FOUR_OF_A_KIND, val

        # Full House
        if counts_list == [3, 2]:
            val = [v for v, c in counts_map.items() if c == 3][0]
            return HandRank.FULL_HOUSE, val

        # Flush
        if is_flush:
            return HandRank.FLUSH, values[4]

        # Straight
        if is_straight:
            return HandRank.STRAIGHT, high_val

        # Three of a Kind
        if counts_list[0] == 3:
            val = [v for v, c in counts_map.items() if c == 3][0]
            return HandRank.THREE_OF_A_KIND, val

        # Two Pair
        if counts_list[:2] == [2, 2]:
            val = max([v for v, c in counts_map.items() if c == 2])
            return HandRank.TWO_PAIR, val

        # One Pair (Jacks or Better check)
        if counts_list[0] == 2:
            val = [v for v, c in counts_map.items() if c == 2][0]
            if val >= 11:  # Jack=11, Queen=12, King=13, Ace=14
                return HandRank.PAIR, val
            else:
                return HandRank.HIGH_CARD, 0

        # 6. Final Fallback (Always returns a tuple to prevent unpacking errors)
        return HandRank.HIGH_CARD, 0

    def analyze(self):
        """
        The main entry point: identifies the current hand and triggers the EV analysis.
        """
        # 1. Identify current hand rank (e.g., Straight, Pair, High Card)
        self.rank, self.primary = self.evaluate_hand(self.sorted_hand, True)
        print(f"\n[ Current Hand ]: {self.rank.name}")

        # 2. Run the heavy EV strategy analysis
        self.run_heavy_analysis()

    def run_heavy_analysis(self):
        """
        Calculates EV for all 32 combinations and prints the formatted results table.
        """
        print("Analyzing strategies... (Running Synchronously)")

        # 1. Execute the EV math for all 32 possible holds
        self.find_optimal_move()

        if not hasattr(self, 'all_move_results') or not self.all_move_results:
            print("!!! Analysis Error: No results were generated.")
            return

        # 2. Print Table Header
        print("\n" + "=" * 95)
        print(f"{'RANK':<5} | {'EV':<7} | {'FREQ %':<8} | {'LIKELY RESULT':<18} | {'HOLD STRATEGY'}")
        print("-" * 95)

        # 3. Print Top 5 Strategies (Sorted by EV)
        for i, res in enumerate(self.all_move_results[:5]):
            # Use an arrow to highlight the best move
            rank_str = f"--> #{i + 1}" if i == 0 else f"    #{i + 1}"

            # Format the cards for display (e.g., 'th' becomes '10H')
            if not res['cards']:
                hold_str = "DISCARD ALL"
            else:
                card_labels = []
                for c in res['cards']:
                    val_display = "10" if c.value == 't' else c.value.upper()
                    card_labels.append(f"{val_display}{c.suit.upper()}")
                hold_str = "HOLD " + " ".join(card_labels)

            # Fixed: Only ONE print statement here to prevent double-printing lines
            print(
                f"{rank_str:<5} | {res['ev']:<7.3f} | {res['hit_rate'] * 100:>5.1f}%   | {res['most_likely']:<18} | {hold_str}")

        print("=" * 95)

        # 4. Strategy Summary Analysis
        best_ev = self.all_move_results[0]['ev']
        second_best_ev = self.all_move_results[1]['ev'] if len(self.all_move_results) > 1 else 0
        ev_gap = best_ev - second_best_ev

        print("\n--- Strategy Analysis ---")

        if best_ev > 1.0:
            print(
                f"STATUS: High-Value Situation! The {self.all_move_results[0]['most_likely']} is worth {best_ev:.3f} credits.")

        # Alert if the choice between #1 and #2 is very close
        if 0 < ev_gap < 0.05:
            print(f"ADVICE: Close call! Move #1 is only {ev_gap:.3f} better than Move #2.")

        elif best_ev < 0.40:
            print("STATUS: Defensive Play. No strong draws; follow Strategy #1 to minimize loss.")

        print(f"OPTIMAL EXPECTED VALUE: {best_ev:.3f}")
        print("Analysis Complete.\n")

    def get_all_hold_combinations(self):
        self.all_possible_holds = []
        bit_masks = list(itertools.product([0, 1], repeat=5))
        for mask in bit_masks:
            held_cards = [self.player_cards[i] for i in range(5) if mask[i] == 1]
            self.all_possible_holds.append({"mask": mask, "cards": held_cards})

    def get_payout(self, hand_rank, rank_value):
        if hand_rank == HandRank.PAIR:
            if rank_value >= 11:
                return PAYOUT_TABLE[HandRank.PAIR]
            else:
                return 0
        return PAYOUT_TABLE.get(hand_rank, 0)

    def calculate_hold_ev(self, held_cards):
        import random
        from collections import Counter
        from math import comb

        num_to_draw = 5 - len(held_cards)
        deck_pool = list(self.remaining_deck)

        # Calculate how many possible combinations exist
        total_combinations = comb(len(deck_pool), num_to_draw)

        # We'll use a sample limit to keep the speed snappy.
        # 10,000 is a sweet spot for accuracy vs. speed.
        sample_limit = 10000

        actual_draws = []

        if total_combinations <= sample_limit:
            # If the total combinations are small (e.g., holding 3 or 4 cards),
            # calculate EVERY possibility for 100% accuracy.
            import itertools
            actual_draws = list(itertools.combinations(deck_pool, num_to_draw))
        else:
            # For large draws (holding 0, 1, or 2 cards), take a random sample.
            # This prevents "ordering bias" from the deck's initial state.
            for _ in range(sample_limit):
                actual_draws.append(random.sample(deck_pool, num_to_draw))

        sample_size = len(actual_draws)
        local_total_payout = 0
        local_hits = 0
        local_rank_counts = Counter()

        for draw in actual_draws:
            # Combine held cards with the sampled draw
            full_hand = held_cards + list(draw)

            # Use your fast evaluation method
            rank_enum, rank_val = self.evaluate_hand_fast(full_hand)
            payout = self.get_payout(rank_enum, rank_val)

            if payout > 0:
                local_hits += 1

            local_rank_counts[rank_enum] += 1
            local_total_payout += payout

        # Final Math
        ev = local_total_payout / sample_size if sample_size > 0 else 0
        hit_rate = local_hits / sample_size if sample_size > 0 else 0

        return ev, hit_rate, local_rank_counts

    def find_optimal_move(self):
        """
        Analyzes all 32 possible hold combinations and identifies the mathematically
        optimal strategy based on Expected Value (EV).
        """
        results = []

        # 1. Safety Gate: Ensure we have combinations to analyze
        # If self.all_possible_holds is empty, the loop won't run and causes an IndexError later.
        if not hasattr(self, 'all_possible_holds') or not self.all_possible_holds:
            # Attempt to generate them if they are missing
            if hasattr(self, 'generate_all_combinations'):
                self.all_possible_holds = self.generate_all_combinations()

            # If still empty, we cannot proceed
            if not self.all_possible_holds:
                print("!!! Critical Error: No hold combinations found in all_possible_holds.")
                return

        # 2. Loop through every possible way to hold the cards (32 total)
        for move in self.all_possible_holds:
            # Run the simulation/calculation for this hold
            ev, hit_rate, rank_counts = self.calculate_hold_ev(move["cards"])

            held = move["cards"]
            num_held = len(held)
            suits = [c.suit for c in held]

            # --- START LIKELY RESULT (ml_name) LOGIC ---

            # A. Check if the held cards ALREADY form a winning hand (Pat Hand)
            pat_rank, pat_val = self.evaluate_hand_fast(held)

            if num_held == 5 and pat_rank != HandRank.HIGH_CARD:
                ml_name = pat_rank.name.replace("_", " ").title()

            # B. Check for strong Draws if we aren't holding a full hand
            elif any(suits.count(s) == 4 for s in set(suits)):
                ml_name = "4-Flush Draw"

            elif any(len([c for c in held if c.value == v]) == 2 for v in
                     set([c.value for c in held])) and num_held == 2:
                ml_name = "Pair Draw"

            elif any(suits.count(s) == 3 for s in set(suits)) and num_held == 3:
                ml_name = "3-Flush Draw"

            else:
                # C. Fallback: Get most common win from rank_counts (excluding High Card)
                winning_ranks = [r for r, count in rank_counts.most_common() if r != HandRank.HIGH_CARD]
                if winning_ranks:
                    ml_name = winning_ranks[0].name.replace("_", " ").title()
                else:
                    ml_name = "High Card"
            # --- END LIKELY RESULT LOGIC ---

            results.append({
                "mask": move["mask"],
                "cards": held,
                "ev": float(ev),
                "hit_rate": float(hit_rate),
                "most_likely": ml_name
            })

        # 3. Final Safety Gate and Sorting
        if results:
            # Sort results by EV descending (Highest EV at Index 0)
            results.sort(key=lambda x: x["ev"], reverse=True)

            self.all_move_results = results
            self.best_move = results[0]
            self.best_ev = results[0]["ev"]
        else:
            print("!!! Error: The analysis loop ran but produced zero results.")
            self.all_move_results = []

    # --- HELPER FUNCTIONS (Returning Tuples) ---
    def is_straight(self, cards):
        if len(cards) != 5: return False, None
        values = sorted([c.get_int_value for c in cards])
        if values == [2, 3, 4, 5, 14]: return True, 5
        if all(values[i] == values[i - 1] + 1 for i in range(1, 5)):
            return True, values[4]
        return False, None

    def is_flush(self, cards):
        if len(cards) != 5: return False, None
        suit_values = [c.get_int_suit for c in cards]
        if len(set(suit_values)) == 1:
            return True, suit_values[0]
        return False, None

    def is_straight_flush(self, cards):
        # FIX: Explicitly unpack the tuples!
        is_f, _ = self.is_flush(cards)
        is_s, high = self.is_straight(cards)
        if is_f and is_s:
            return True, high
        return False, None

    def is_four_of_a_kind(self, cards):
        if len(cards) != 5: return False, None, None
        vals = [c.get_int_value for c in cards]
        counts = Counter(vals)
        if 4 in counts.values():
            prim = [r for r, c in counts.items() if c == 4][0]
            kick = [r for r, c in counts.items() if c == 1][0]
            return True, prim, kick
        return False, None, None

    def is_full_house(self, cards):
        if len(cards) != 5: return False, None, None
        vals = [c.get_int_value for c in cards]
        counts = Counter(vals)
        if sorted(counts.values()) == [2, 3]:
            prim = [r for r, c in counts.items() if c == 3][0]
            sec = [r for r, c in counts.items() if c == 2][0]
            return True, prim, sec
        return False, None, None

    def is_three_of_a_kind(self, cards):
        if len(cards) != 5: return False, None, None
        vals = [c.get_int_value for c in cards]
        counts = Counter(vals)
        for val, count in counts.items():
            if count == 3:
                kickers = sorted([v for v, c in counts.items() if c != 3], reverse=True)
                return True, val, kickers
        return False, None, None

    def is_two_pair(self, cards):
        if len(cards) != 5: return False, None, None, None
        vals = [c.get_int_value for c in cards]
        counts = Counter(vals)
        pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)
        if len(pairs) == 2:
            kicker = [v for v, c in counts.items() if c == 1][0]
            return True, pairs[0], pairs[1], kicker
        return False, None, None, None

    def is_pair(self, cards):
        if len(cards) != 5: return False, None, None
        vals = [c.get_int_value for c in cards]
        counts = Counter(vals)
        pair_vals = [v for v, c in counts.items() if c == 2]
        if len(pair_vals) == 1 and 3 not in counts.values():
            kickers = sorted([v for v, c in counts.items() if c != 2], reverse=True)
            return True, pair_vals[0], kickers
        return False, None, None

    def evaluate_hand(self, cards, is_player):
        # This function provides detailed data for the UI/Human
        if len(cards) != 5:
            return HandRank.HIGH_CARD, 0

        sorted_cards = sorted(cards, key=lambda c: c.get_int_value)
        final_rank = HandRank.HIGH_CARD
        primary = sorted_cards[-1].get_int_value
        secondary = None
        kicker = None

        # FIX: We must index [0] to get the boolean from the tuple
        if self.is_straight_flush(sorted_cards)[0]:
            final_rank = HandRank.ROYAL_FLUSH if sorted_cards[0].get_int_value == 10 else HandRank.STRAIGHT_FLUSH
            _, primary = self.is_straight_flush(sorted_cards)

        elif self.is_four_of_a_kind(sorted_cards)[0]:
            _, primary, kicker = self.is_four_of_a_kind(sorted_cards)
            final_rank = HandRank.FOUR_OF_A_KIND

        elif self.is_full_house(cards)[0]:
            _, primary, secondary = self.is_full_house(cards)
            final_rank = HandRank.FULL_HOUSE

        elif self.is_flush(cards)[0]:
            final_rank = HandRank.FLUSH
            primary = cards[-1].get_int_value

        elif self.is_straight(cards)[0]:
            final_rank = HandRank.STRAIGHT
            primary = cards[-1].get_int_value

        elif self.is_three_of_a_kind(cards)[0]:
            _, primary, kicker = self.is_three_of_a_kind(cards)
            final_rank = HandRank.THREE_OF_A_KIND

        elif self.is_two_pair(cards)[0]:
            _, primary, secondary, kicker = self.is_two_pair(cards)
            final_rank = HandRank.TWO_PAIR

        elif self.is_pair(sorted_cards)[0]:
            # FIX: Only unpack 3 values because is_pair returns (True, val, kickers)
            _, primary, _ = self.is_pair(sorted_cards)
            final_rank = HandRank.PAIR

        else:
            final_rank = HandRank.HIGH_CARD
            primary = cards[-1].get_int_value

        if is_player:
            self.rank = final_rank
            self.primary = primary
            self.secondary = secondary
            self.kicker = kicker

        return final_rank, primary

    def format_move_compact(self, move):
        mask = move["mask"]
        holds = []
        rank_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        suit_map = {4: '♣', 3: '♦', 2: '♥', 1: '♠'}  # Ensure this matches your Int Lookup

        for i, bit in enumerate(mask):
            if bit == 1:
                card = self.player_cards[i]
                rv = card.get_int_value
                r_str = rank_map.get(rv, str(rv))
                s_icon = suit_map.get(card.get_int_suit, "?")
                holds.append(f"{r_str}{s_icon}")

        if not holds:
            return "DISCARD ALL"
        return "HOLD " + " ".join(holds)