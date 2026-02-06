import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import messagebox
from Deck import Deck
from HandAnalyzer import HandAnalyzer
from GameState import GameState
from HandRank import HandRank
from PayoutTable import PAYOUT_TABLE
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peeker")
        self.root.geometry("1150x800")
        self.root.configure(bg="#0a3d0a")

        # --- Game Logic Objects ---
        self.deck = Deck()
        self.current_hand = []
        self.starting_bankroll = 200
        self.bankroll = 200
        self.holds = [False] * 5
        self.game_state = GameState.DEAL
        self.analyzer = None
        self.current_bet = 1
        self.max_bet_limit = 5
        self.bankroll_history = [200]
        self.card_images = {}
        self.best_win = 0
        self.current_streak = 0

        # --- UI Elements ---
        self.hand_rank = ""
        self._setup_ui()
        self.update_payout_display()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_dashboard(self):
        self.dashboard_frame = tk.Frame(self.game_area, bg="#0a3d0a")
        self.dashboard_frame.pack(side="bottom", pady=(10, 30), fill="x")

        # Stats Row
        self.stats_frame = tk.Frame(self.dashboard_frame, bg="#0a3d0a")
        self.stats_frame.pack(fill="x")

        # Hands Played Counter
        self.hands_lbl = tk.Label(self.stats_frame, text="HANDS: 0", font=("Courier", 12, "bold"), bg="#0a3d0a",
                                  fg="#ffcc00")
        self.hands_lbl.pack(side="left", padx=20)

        # Win/Loss Percentage
        self.profit_lbl = tk.Label(self.stats_frame, text="PROFIT: $0", font=("Courier", 12, "bold"), bg="#0a3d0a",
                                   fg="white")
        self.profit_lbl.pack(side="right", padx=20)

        # Matplotlib Plot below stats
        self.fig, self.ax = plt.subplots(figsize=(6, 2.5), dpi=100)
        self.fig.patch.set_facecolor('#0a3d0a')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.dashboard_frame)
        self.canvas.get_tk_widget().pack()
        self.update_graph()

    def update_payout_display(self):
        # Use PAYOUT_TABLE instead of PAYOUT_BASE
        for rank, base_val in PAYOUT_TABLE.items():
            if rank == HandRank.HIGH_CARD:
                continue

            # Calculation logic
            win = base_val * self.current_bet

            # Standard Video Poker: Royal Flush bonus at Max Bet (5 coins)
            if rank == HandRank.ROYAL_FLUSH and self.current_bet == 5:
                win = 4000

            # Update the specific labels for this rank
            if rank in self.payout_rows:
                self.payout_rows[rank][1].config(text=str(win))

    def _setup_ui(self):
        """Initializes the visual components with a sidebar layout."""
        # 1. Main Container (Splits the window into Left and Right)
        self.main_container = tk.Frame(self.root, bg="#0a3d0a")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Left Side: Game Area (Bankroll, Cards, Controls)
        self.game_area = tk.Frame(self.main_container, bg="#0a3d0a")
        self.game_area.pack(side="left", fill="both", expand=True)

        # 3. Right Side: Payout Area (The Sidebar)
        self.payout_area = tk.Frame(
            self.main_container,
            bg="#072b07",
            highlightthickness=2,
            highlightbackground="#ffcc00",
            padx=10,
            pady=10
        )
        self.payout_area.pack(side="right", padx=(10, 0), anchor="n")

        # --- FILL THE GAME AREA (Left) ---

        # Bankroll Display
        self.header_label = tk.Label(
            self.game_area,
            text=f"Bankroll: ${self.bankroll}",
            font=("Arial", 22, "bold"),
            bg="#0a3d0a",
            fg="white"
        )
        self.header_label.pack(pady=10)

        # Bet Control Row
        self.bet_frame = tk.Frame(self.game_area, bg="#0a3d0a")
        self.bet_frame.pack(pady=5)

        self.btn_less = tk.Button(self.bet_frame, text="←", command=lambda: self.change_bet(-1),
                                  font=("Arial", 12, "bold"), width=3, bg="#444", fg="white")
        self.btn_less.grid(row=0, column=0, padx=5)

        self.bet_label = tk.Label(self.bet_frame, text=f"BET: {self.current_bet}",
                                  font=("Arial", 14, "bold"), bg="#0a3d0a", fg="white", width=8)
        self.bet_label.grid(row=0, column=1, padx=5)

        self.btn_more = tk.Button(self.bet_frame, text="→", command=lambda: self.change_bet(1),
                                  font=("Arial", 12, "bold"), width=3, bg="#444", fg="white")
        self.btn_more.grid(row=0, column=2, padx=5)

        self.btn_max = tk.Button(self.bet_frame, text="MAX BET", command=self.set_max_bet,
                                 font=("Arial", 10, "bold"), bg="#cc0000", fg="white")
        self.btn_max.grid(row=0, column=3, padx=15)

        # Card Display Area
        self.card_frame = tk.Frame(self.game_area, bg="#0a3d0a")
        self.card_frame.pack(pady=30)

        self.card_labels = []
        # Point to your specific back image name
        back_img = self.get_card_image("back_green")

        for i in range(5):
            lbl = tk.Label(
                self.card_frame,
                text="",  # Ensure text is empty
                image=back_img,  # Start with the back image
                bg="#0a3d0a",  # Match background
                padx=0, pady=0,  # Remove internal padding
                borderwidth=0,  # Clean edges
                highlightthickness=4,
                highlightbackground="#0a3d0a"
            )
            # Use pixel-based sizing now
            lbl.config(width=110, height=155)
            lbl.grid(row=0, column=i, padx=5)
            lbl.bind("<Button-1>", lambda event, i=i: self.toggle_hold(event, i))
            self.card_labels.append(lbl)

            # Save reference so it doesn't disappear
            if back_img:
                lbl.image = back_img

        lbl = tk.Label(
            self.card_frame,
            image=back_img,
            bg="#0a3d0a",
            highlightthickness=4,
            highlightbackground="#0a3d0a"
        )
        lbl.image = back_img

        # Result Display Area
        self.result_label = tk.Label(
            self.game_area,
            text="",
            font=("Arial", 24, "bold"),  # Made slightly larger for impact
            bg="#0a3d0a",
            fg="#ffcc00",
            height=2  # Give it a fixed height so it doesn't "jump" when text appears
        )
        self.result_label.pack(pady=5)

        # Action Button (DEAL/DRAW)
        self.deal_button = tk.Button(
            self.game_area,
            text="DEAL",
            command=self.play_action,
            font=("Arial", 16, "bold"),
            width=15,
            height=2,
            bg="#ffcc00",
            state=tk.NORMAL
        )
        self.deal_button.pack(pady=10)
        self._setup_dashboard()

        # --- FILL THE PAYOUT AREA (Right) ---
        self._setup_payout_table()

        self.summary_box = tk.Frame(
            self.payout_area,  # Putting it inside the right sidebar container
            bg="#051c05",  # Slightly darker green
            highlightthickness=1,
            highlightbackground="#555",
            padx=10,
            pady=10
        )
        self.summary_box.pack(side="bottom", fill="x", pady=(20, 0))

        tk.Label(self.summary_box, text="SESSION SUMMARY", font=("Arial", 10, "bold"),
                 bg="#051c05", fg="#ffcc00").pack(anchor="w")

        self.best_win_lbl = tk.Label(self.summary_box, text="BEST WIN: $0",
                                     font=("Arial", 9), bg="#051c05", fg="white")
        self.best_win_lbl.pack(anchor="w", pady=2)

        self.last_win_lbl = tk.Label(self.summary_box, text="LAST WIN: None",
                                     font=("Arial", 9), bg="#051c05", fg="white")
        self.last_win_lbl.pack(anchor="w", pady=2)

        self.streak_lbl = tk.Label(self.summary_box, text="STREAK: 0",
                                   font=("Arial", 9), bg="#051c05", fg="white")
        self.streak_lbl.pack(anchor="w", pady=2)

        # --- Sidebar Strategy & History (Bottom Right) ---
        self.strategy_frame = tk.Frame(
            self.payout_area,
            bg="#051c05",
            highlightthickness=1,
            highlightbackground="#444",
            padx=5,
            pady=5
        )
        # side="bottom" ensures it stays below the payout rows
        self.strategy_frame.pack(side="bottom", fill="both", expand=True, pady=(20, 0))

        tk.Label(
            self.strategy_frame,
            text="STRATEGY ADVISOR",
            font=("Arial", 10, "bold"),
            bg="#051c05",
            fg="#ffcc00"
        ).pack(anchor="w")

        # The Log Box
        self.history_list = tk.Listbox(
            self.strategy_frame,
            bg="#051c05",
            fg="#ffffff",
            font=("Courier", 9),
            borderwidth=0,
            highlightthickness=0,
            height=10,  # Adjust height to fill the green space
            selectbackground="#051c05"
        )
        self.history_list.pack(fill="both", expand=True, pady=5)

    def _setup_payout_table(self):
        for widget in self.payout_area.winfo_children():
            widget.destroy()

        self.payout_rows = {}

        tk.Label(self.payout_area, text="PAY TABLE", font=("Arial", 14, "bold"),
                 bg="#072b07", fg="#ffcc00").pack(pady=(0, 15))

        winning_ranks = [r for r in PAYOUT_TABLE.keys() if r != HandRank.HIGH_CARD]

        for rank in winning_ranks:
            row_frame = tk.Frame(self.payout_area, bg="#072b07")
            row_frame.pack(fill="x", pady=2)

            # Restored labels with more width and clearer colors
            name_lbl = tk.Label(
                row_frame,
                text=rank.name.replace("_", " ").title(),
                font=("Arial", 11, "bold"),
                bg="#072b07",
                fg="#ffffff",  # Changed to white so it's visible
                width=22,  # Wider to prevent cutting off
                anchor="w"
            )
            name_lbl.pack(side="left")

            val_lbl = tk.Label(
                row_frame,
                text="0",
                font=("Arial", 11, "bold"),
                bg="#072b07",
                fg="#ffcc00",  # Changed to gold for the numbers
                width=12,
                anchor="e"
            )
            val_lbl.pack(side="right")

            self.payout_rows[rank] = [name_lbl, val_lbl]

    def highlight_win(self, hand_rank_enum):
        """Highlights the winning row in the pay table."""
        # 1. Reset all rows to the sidebar's dark background
        for labels in self.payout_rows.values():
            for lbl in labels:
                lbl.config(bg="#072b07", fg="#aaa")

        # 2. Highlight the specific rank in Gold
        if hand_rank_enum in self.payout_rows:
            for lbl in self.payout_rows[hand_rank_enum]:
                lbl.config(bg="#ffcc00", fg="black")

    def change_bet(self, amount):
        if self.game_state == GameState.DEAL:
            new_bet = self.current_bet + amount
            if 0 <= new_bet <= self.max_bet_limit:
                self.current_bet = new_bet
                self.bet_label.config(text=f"BET: {self.current_bet}")
                self.update_payout_display()

                # Visual feedback only (No state=tk.DISABLED)
                if self.current_bet > 0:
                    self.deal_button.config(bg="#ffcc00", fg="black")
                else:
                    self.deal_button.config(bg="#555", fg="#888")

    def set_max_bet(self):
        """Instantly sets bet to 5 and starts the game."""
        if self.game_state == GameState.DEAL:
            self.current_bet = self.max_bet_limit
            self.bet_label.config(text=f"BET: {self.current_bet}")
            self.update_payout_display()

            # 1. CLEAR OLD RESULTS: Make it look fresh
            self.result_label.config(text="MAX BET DEAL...", fg="white")

            # 2. RESET PAYTABLE: Remove old winning highlights
            for labels in self.payout_rows.values():
                for lbl in labels:
                    lbl.config(bg="#072b07", fg="#aaa")

            # 3. ENABLE BUTTON: Ensure it's active for the click
            self.deal_button.config(state=tk.NORMAL, bg="#ffcc00", fg="black")

            # 4. START: Trigger the deal
            self.play_action()

    def get_card_image(self, card_name):
        """Loads 'as.png', 'kd.png', etc."""
        if card_name in self.card_images:
            return self.card_images[card_name]

        # Force lowercase to match your files: 'as.png'
        filename = f"{card_name.lower()}.png"
        path = f"cards/{filename}"

        try:
            img = Image.open(path)
            # Standard video poker card size
            img = img.resize((110, 155), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.card_images[card_name] = photo
            return photo
        except Exception as e:
            print(f"File not found: {path}")
            return None

    def show_cards(self, index=0):
        if index < len(self.current_hand):
            card = self.current_hand[index]
            card_name = f"{card.value}{card.suit}".lower()
            img = self.get_card_image(card_name)
            if img:
                self.card_labels[index].config(image=img, text="")
                self.card_labels[index].image = img
            # This MUST be inside the 'if index' block
            self.root.after(150, lambda: self.show_cards(index + 1))

    def animate_draw(self, index=0):
        if index < 5:
            if not self.holds[index]:
                # 1. Briefly show the back to simulate the card being replaced
                back_img = self.get_card_image("back_green")
                self.card_labels[index].config(image=back_img)

                # 2. Wait a tiny bit, then show the actual new card
                self.root.after(100, lambda: self.reveal_single_card(index))
            else:
                self.animate_draw(index + 1)

    def reveal_single_card(self, index):
        """Helper to reveal the card and move to the next one."""
        card = self.current_hand[index]
        card_name = f"{card.value}{card.suit}".lower()
        img = self.get_card_image(card_name)
        self.card_labels[index].config(image=img)
        self.card_labels[index].image = img

        # Move to next card
        self.animate_draw(index + 1)

    def analyze(self):
        self.analyzer = HandAnalyzer(self.current_hand, self.deck.get_cards)
        self.analyzer.analyze()

    def reset_to_backs(self):
        """Instantly turns all cards face-down to the green back image."""
        back_img = self.get_card_image("back_green")
        if back_img:
            for lbl in self.card_labels:
                lbl.config(image=back_img, text="")
                lbl.image = back_img

    def process_deal(self):
        # 1. Safety Checks
        if self.current_bet == 0:
            self.flash_bet_label()
            self.result_label.config(text="PLACE A BET FIRST", fg="#ff3333")
            return

        if self.bankroll < self.current_bet:
            messagebox.showerror("Insufficient Funds", "You don't have enough credits!")
            return

        # 2. Reset UI for New Hand
        self.result_label.config(text="")
        self.reset_to_backs()
        for labels in self.payout_rows.values():
            for lbl in labels:
                lbl.config(bg="#072b07", fg="#aaa")

        # 3. Handle Money
        self.bankroll -= self.current_bet
        self.header_label.config(text=f"Bankroll: ${self.bankroll}")

        # 4. Logic & State Change
        self.game_state = GameState.DRAW
        self.deck = Deck()
        self.current_hand = [self.deck.dealOne() for _ in range(5)]
        self.analyze()

        # 5. Start Animation
        self.show_cards(0)

    def process_draw(self):
        """
        Phase 1 of the Draw:
        1. Captures player choices for the Advisor.
        2. Replaces unheld cards.
        3. Starts the visual 'flip' animation.
        4. Schedules the final scoring.
        """
        # 1. CAPTURE HOLDS: Save player's choices for the History Log
        # We do this before cards are replaced and holds are reset.
        self.last_player_holds = self.holds[:]

        # 2. LOGIC: Replace cards that were NOT held
        for i, held in enumerate(self.holds):
            if not held:
                # Replace card in the hand with a new one from the deck
                self.current_hand[i] = self.deck.dealOne()

        # 3. VISUALS: Turn cards face-down briefly or start reveal
        # If any card is not held, we indicate it's being drawn
        self.result_label.config(text="DRAWING...", fg="white")

        # 4. ANIMATION: Start the recursive reveal for the 5 card slots
        self.animate_draw(0)

        # 5. SCORE DELAY: Wait for the cards to finish flipping (approx 800ms)
        # then call the big reveal/payout logic.
        self.root.after(800, self.finish_hand_logic)

    def finish_hand_logic(self):
        """Phase 2: Evaluation, Strategy Advisor update, and UI cleanup."""
        # 1. Evaluate final hand
        rank, val = self.analyzer.evaluate_hand_fast(self.current_hand)
        rank_display = rank.name.replace("_", " ").title()

        # 2. Payouts
        base_payout = self.analyzer.get_payout(rank, val)
        win_amount = base_payout * self.current_bet

        # Royal Flush Max Bet Bonus
        if rank == HandRank.ROYAL_FLUSH and self.current_bet == 5:
            win_amount = 4000

        # 3. Strategy Advisor (Parse Mask + Symbols)
        best_data = self.analyzer.best_move
        best_mask_str = best_data.get('mask', '00000')
        best_indices = [i for i, bit in enumerate(best_mask_str) if bit == '1']

        symbols = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}

        if len(best_indices) == 5:
            move_txt = "Hold All"
        elif not best_indices:
            move_txt = "Discard All"
        else:
            cards_str = []
            for idx in best_indices:
                c = self.current_hand[idx]
                v = "10" if c.value == 't' else c.value.upper()
                s = symbols.get(c.suit.lower(), c.suit)
                cards_str.append(f"{v}{s}")
            move_txt = "Hold " + " ".join(cards_str)

        # Comparison Logic
        player_indices = [i for i, h in enumerate(self.last_player_holds) if h]
        is_correct = set(player_indices) == set(best_indices)

        # Log to Sidebar Strategy List
        icon = "[✓]" if is_correct else "[!]"
        log_entry = f"{icon} {rank_display[:8]} | {move_txt}"

        if hasattr(self, 'history_list'):
            self.history_list.insert(0, log_entry)
            self.history_list.itemconfig(0, fg="#00ff00" if is_correct else "#ffaa00")
            if self.history_list.size() > 12:
                self.history_list.delete(12)

        # 4. Handle Bankroll and Result Label
        if win_amount > 0:
            self.result_label.config(text=f"{rank_display} - WIN ${win_amount}!", fg="#ffcc00")
            self.bankroll += win_amount

            # Update Best Win
            if win_amount > self.best_win:
                self.best_win = win_amount
                if hasattr(self, 'best_win_lbl'):
                    self.best_win_lbl.config(text=f"BEST WIN: ${self.best_win}")

            # Update Win Streak
            if self.current_streak < 0: self.current_streak = 0
            self.current_streak += 1
            self.streak_lbl.config(text=f"STREAK: {self.current_streak} Wins", fg="#00ff00")

            # Payout Animations
            if rank.value >= 6:
                self.flash_payout_row(rank)
            else:
                self.highlight_win(rank)
        else:
            # Handle Loss
            self.result_label.config(text=rank_display, fg="white")
            if self.current_streak > 0: self.current_streak = 0
            self.current_streak -= 1
            self.streak_lbl.config(text=f"STREAK: {abs(self.current_streak)} Losses", fg="#ff3333")

        # 5. Update HUD (Critical Profit/Hand Count Fix)
        # Update bankroll history first
        self.bankroll_history.append(self.bankroll)

        # Calculate stats
        total_hands = len(self.bankroll_history) - 1
        profit = self.bankroll - 200  # Assumes 200 is start. Use self.starting_bankroll if defined.

        # Update UI
        self.header_label.config(text=f"Bankroll: ${self.bankroll}")

        if hasattr(self, 'hands_lbl'):
            self.hands_lbl.config(text=f"HANDS: {total_hands}")

        if hasattr(self, 'profit_lbl'):
            color = "#00ff00" if profit >= 0 else "#ff3333"
            prefix = "+" if profit > 0 else ""
            self.profit_lbl.config(text=f"PROFIT: {prefix}${profit}", fg=color)

        self.update_graph()

        # 6. Cleanup for Next Hand
        self.reset_holds()
        if not self.check_game_over():
            self.game_state = GameState.DEAL
            self.deal_button.config(text="DEAL", state=tk.NORMAL)

    def reset_holds(self):
        """Clears all hold selections and resets card borders to the background color."""
        self.holds = [False] * 5
        for lbl in self.card_labels:
            # Set this to match your card_frame background color
            lbl.config(highlightbackground="#0a3d0a")

    def update_graph(self):
        self.ax.clear()

        # Data points
        data = self.bankroll_history
        x = range(len(data))

        # Color logic: Green if current bankroll > start (200), Red if below
        current_color = "#00ff00" if data[-1] >= 200 else "#ff3333"

        # 1. Plot the main line with a "neon" glow effect
        self.ax.plot(x, data, color=current_color, linewidth=3, zorder=5)
        self.ax.plot(x, data, color=current_color, linewidth=8, alpha=0.1, zorder=4)  # Outer glow

        # 2. Fill with a gradient effect
        self.ax.fill_between(x, data, 0, color=current_color, alpha=0.1)

        # 3. Add a "Current Position" marker
        self.ax.scatter(x[-1], data[-1], color="white", s=50, edgecolors=current_color, zorder=6)

        # 4. Fixed Axis & Baseline
        current_max = max(max(data), 300)
        self.ax.set_ylim(0, current_max + 20)
        self.ax.axhline(200, color='white', linestyle=':', alpha=0.4, label="Break Even")

        # Formatting
        self.ax.set_title("SESSION VOLATILITY", color='#ffcc00', fontsize=12, fontweight='bold', pad=10)
        self.ax.set_facecolor('#072b07')
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.grid(True, color='#0a3d0a', alpha=0.3)

        # Remove border box for a "HUD" look
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.canvas.draw()

    def check_game_over(self):
        """Checks if the player has enough money to continue."""
        # If they are out of money
        if self.bankroll <= 0:
            self.result_label.config(text="GAME OVER - OUT OF CREDITS", fg="red")
            self.deal_button.config(state="disabled", bg="#333")
            messagebox.showinfo("Game Over", "You've run out of credits! Please restart to play again.")
            return True
        return False

    def play_action(self):
        if self.game_state == GameState.DEAL:
            if self.current_bet == 0:
                self.flash_bet_label()
                return
            self.process_deal()
            # Button changes to DRAW immediately upon deal
            self.deal_button.config(text="DRAW")
            self.game_state = GameState.DRAW

        elif self.game_state == GameState.DRAW:
            # Disable the button briefly so they don't click it twice during animation
            self.deal_button.config(state=tk.DISABLED)
            self.process_draw()
            # The button is re-enabled and set to "DEAL" inside finish_hand_logic

    def toggle_hold(self, event, i):
        if self.game_state == GameState.DRAW:
            self.holds[i] = not self.holds[i]

            if self.holds[i]:
                self.card_labels[i].config(highlightbackground="lime")
            else:
                self.card_labels[i].config(highlightbackground="#0a3d0a")

    def on_closing(self):
        """Cleanly shuts down the app and Matplotlib."""
        plt.close('all')  # This kills the background graph threads
        self.root.quit()  # This stops the Tkinter mainloop
        self.root.destroy()  # This closes the window

    def flash_payout_row(self, rank, count=0):
        if rank in self.payout_rows:
            labels = self.payout_rows[rank]
            try:
                # Check if the first label still exists before trying to config it
                if not labels[0].winfo_exists(): return

                if count % 2 == 0:
                    bg_color, fg_color = "#ffcc00", "black"
                else:
                    bg_color, fg_color = "#072b07", "#ffcc00"

                for lbl in labels:
                    lbl.config(bg=bg_color, fg=fg_color)

                if count < 8:
                    self.root.after(200, lambda: self.flash_payout_row(rank, count + 1))
                else:
                    self.highlight_win(rank)
            except tk.TclError:
                # This catches the error if the widget was destroyed mid-flash
                pass

    def flash_bet_label(self, count=0):
        """Flashes the bet label red to grab attention."""
        if count < 6:  # Flashes 3 times (Red -> White, Red -> White, etc.)
            current_color = self.bet_label.cget("fg")
            next_color = "#ff3333" if current_color == "white" else "white"
            self.bet_label.config(fg=next_color)

            # Call again in 150ms
            self.root.after(150, lambda: self.flash_bet_label(count + 1))
        else:
            # Ensure it ends on white
            self.bet_label.config(fg="white")

    def reset_session(self):
        """Resets all session statistics and bankroll."""
        self.bankroll = 200
        self.bankroll_history = [200]
        self.best_win = 0
        self.current_streak = 0

        # Update UI Labels
        self.header_label.config(text=f"Bankroll: ${self.bankroll}")
        if hasattr(self, 'hands_lbl'): self.hands_lbl.config(text="HANDS: 0")
        if hasattr(self, 'profit_lbl'): self.profit_lbl.config(text="PROFIT: $0", fg="#00ff00")
        if hasattr(self, 'best_win_lbl'): self.best_win_lbl.config(text="BEST WIN: $0")
        if hasattr(self, 'history_list'): self.history_list.delete(0, tk.END)

        self.update_graph()
        self.result_label.config(text="SESSION RESET", fg="white")