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
        self.root.geometry("800x600")
        self.root.configure(bg="#0a3d0a")  # Classic Casino Green

        # --- Game Logic Objects ---
        self.deck = Deck()
        self.current_hand = []
        self.bankroll = 200
        self.holds = [False] * 5
        self.game_state = GameState.DEAL
        self.analyzer = None
        self.current_bet = 0
        self.max_bet_limit = 5
        self.bankroll_history = [200]
        self.card_images = {}

        # --- UI Elements ---
        self.hand_rank = ""
        self._setup_ui()
        self._setup_payout_table()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_dashboard(self):
        self.dashboard_frame = tk.Frame(self.game_area, bg="#0a3d0a")
        self.dashboard_frame.pack(pady=10, fill="both", expand=True)

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
            font=("Arial", 20, "bold"),
            bg="#0a3d0a",
            fg="#ffcc00"
        )
        self.result_label.pack(pady=10)

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

    def _setup_payout_table(self):
        """Creates a clean, single-list vertical pay table."""
        # Clear the area first to prevent duplicates if called again
        for widget in self.payout_area.winfo_children():
            widget.destroy()

        self.payout_rows = {}

        # Header Label
        tk.Label(self.payout_area, text="PAY TABLE", font=("Arial", 12, "bold"),
                 bg="#072b07", fg="#ffcc00").pack(pady=(0, 10))

        # Filter and Sort: Ensure we only iterate through the actual winning hands
        winning_ranks = [r for r in PAYOUT_TABLE.keys() if r != HandRank.HIGH_CARD]

        for rank in winning_ranks:
            row_frame = tk.Frame(self.payout_area, bg="#072b07")
            row_frame.pack(fill="x", pady=3)

            name_lbl = tk.Label(
                row_frame,
                text=rank.name.replace("_", " ").title(),
                font=("Arial", 10, "bold"),
                bg="#072b07",
                fg="#aaa",
                width=14,  # Reduced from 16
                anchor="w"
            )
            name_lbl.pack(side="left")

            val_lbl = tk.Label(
                row_frame,
                text="0",
                font=("Arial", 10, "bold"),
                bg="#072b07",
                fg="#aaa",
                width=8,  # Increased from 6
                anchor="e"
            )
            val_lbl.pack(side="right")

            self.payout_rows[rank] = [name_lbl, val_lbl]

        self.update_payout_display()

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
        if self.game_state == GameState.DEAL:
            self.current_bet = self.max_bet_limit
            self.bet_label.config(text=f"BET: {self.current_bet}")
            self.update_payout_display()

            # Instantly enable and trigger the deal
            self.deal_button.config(state=tk.NORMAL, bg="#ffcc00", fg="black")
            self.play_action()  # This will call process_deal

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

    def show_cards(self):
        for i, card in enumerate(self.current_hand):
            # Format to 'as', 'kd', etc. to match your files
            card_name = f"{card.value}{card.suit}".lower()
            img = self.get_card_image(card_name)

            if img:
                # IMPORTANT: Set text to "" to remove the '4S' ghosting
                self.card_labels[i].config(image=img, text="")
                self.card_labels[i].image = img
            else:
                # Fallback if image is missing
                self.card_labels[i].config(text=card_name.upper(), image="")


    def analyze(self):
        self.analyzer = HandAnalyzer(self.current_hand, self.deck.get_cards)
        self.analyzer.analyze()

    def process_deal(self):
        # Check if the player is trying to play for free!
        if self.current_bet == 0:
            self.flash_bet_label()
            # Optional: Add a subtle status message instead of a popup
            self.result_label.config(text="PLACE A BET FIRST", fg="#ff3333")
            return

        # Check if they have enough money for the bet
        if self.bankroll < self.current_bet:
            messagebox.showerror("Insufficent Funds", "You don't have enough credits for that bet!")
            return

        # --- If checks pass, proceed with the game ---
        self.bankroll -= self.current_bet
        self.header_label.config(text=f"Bankroll: ${self.bankroll}")

        # ... rest of your existing logic ...
        self.result_label.config(text="")
        self.game_state = GameState.DRAW
        # ... etc ...

        # FIX: Reset to the correct DARK background color of the sidebar
        for labels in self.payout_rows.values():
            for lbl in labels:
                lbl.config(bg="#072b07", fg="#aaa")

        self.deck = Deck()
        self.current_hand = [self.deck.dealOne() for _ in range(5)]
        self.analyze()
        self.show_cards()

    def process_draw(self):
        """Finalizes the hand, calculates winnings, and updates the dashboard."""
        # 1. Replace cards that were not 'held'
        for i, held in enumerate(self.holds):
            if not held:
                self.current_hand[i] = self.deck.dealOne()

        self.show_cards()

        # 2. Evaluate the final hand using the analyzer
        rank, val = self.analyzer.evaluate_hand_fast(self.current_hand)

        # 3. Calculate Payout (Base Payout * Current Bet)
        base_payout = self.analyzer.get_payout(rank, val)
        win_amount = base_payout * self.current_bet

        # Special Case: Royal Flush Max Bet Bonus
        if rank == HandRank.ROYAL_FLUSH and self.current_bet == 5:
            win_amount = 4000

        # 4. Update Bankroll and UI Labels
        rank_display = rank.name.replace("_", " ").title()

        if win_amount > 0:
            self.result_label.config(text=f"{rank_display} - WIN ${win_amount}!", fg="#ffcc00")
            self.bankroll += win_amount
            self.highlight_win(rank)
        elif rank == HandRank.PAIR and val < 11:
            # Show the rank but clarify it's not a 'Jacks or Better' winner
            self.result_label.config(text=f"Pair of {val}s (Low)", fg="white")
        else:
            self.result_label.config(text=rank_display, fg="white")

        # Update the main Bankroll text
        self.header_label.config(text=f"Bankroll: ${self.bankroll}")

        # 5. --- DATA DASHBOARD UPDATES ---
        # Track history for the graph
        self.bankroll_history.append(self.bankroll)

        # Update the live text stats (Hands Played and Profit/Loss)
        total_hands = len(self.bankroll_history) - 1
        profit = self.bankroll - 200  # Assuming 200 is starting bankroll
        profit_color = "#00ff00" if profit >= 0 else "#ff3333"

        if hasattr(self, 'hands_lbl'):
            self.hands_lbl.config(text=f"HANDS: {total_hands}")
        if hasattr(self, 'profit_lbl'):
            self.profit_lbl.config(text=f"PROFIT: ${profit}", fg=profit_color)

        # Redraw the neon graph
        self.update_graph()

        # 6. Clean up for next hand
        self.reset_holds()
        self.check_game_over()

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
                return  # Stop here! Don't change button to DRAW.

            self.process_deal()
            self.game_state = GameState.DRAW
            self.deal_button.config(text="DRAW")

        elif self.game_state == GameState.DRAW:
            self.process_draw()
            self.game_state = GameState.DEAL
            self.deal_button.config(text="DEAL")

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