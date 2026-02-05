import tkinter as tk
from tkinter import messagebox
from Deck import Deck
from HandAnalyzer import HandAnalyzer
from GameState import GameState


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

        # --- UI Elements ---
        self.hand_rank = ""
        self._setup_ui()

    def _setup_ui(self):
        """Initializes the visual components."""
        # 1. Top Title / Bankroll Area
        self.header_label = tk.Label(
            self.root,
            text=f"Bankroll: ${self.bankroll}",
            font=("Arial", 18, "bold"),
            bg="#0a3d0a",
            fg="white"
        )
        self.header_label.pack(pady=20)

        # 2. Card Display Area (A Frame to hold 5 cards)
        self.card_frame = tk.Frame(self.root, bg="#0a3d0a")
        self.card_frame.pack(pady=50)

        # Let's create 5 placeholders for cards
        self.card_labels = []
        for i in range(5):
            lbl = tk.Label(
                self.card_frame,
                text="?",
                font=("Arial", 24, "bold"),
                width=5,
                height=3,
                relief="raised",
                bg="white",
                highlightthickness=4,
                highlightbackground="#0a3d0a"
            )
            lbl.grid(row=0, column=i, padx=10)
            lbl.bind("<Button-1>", lambda event, i=i: self.toggle_hold(event, i))
            self.card_labels.append(lbl)

        # 2.5 Result Display Area
        self.result_label = tk.Label(
            self.root,
            text=f"{self.hand_rank}",
            font=("Arial", 20, "bold"),
            bg="#0a3d0a",
            fg="#ffcc00"  # Gold color for that "Winner" feel
        )
        self.result_label.pack(pady=10)

        # 3. Button Area
        self.deal_button = tk.Button(
            self.root,
            text="DEAL",
            command=self.play_action,
            font=("Arial", 14, "bold"),
            width=15,
            bg="#ffcc00"
        )
        self.deal_button.pack(pady=20)

    def show_cards(self):
        for i, card in enumerate(self.current_hand):
            self.card_labels[i].config(text=f"{card.value.upper()}{card.suit.upper()}")

    def analyze(self):
        self.analyzer = HandAnalyzer(self.current_hand, self.deck.get_cards)
        self.analyzer.analyze()

    def process_deal(self):
        self.result_label.config(text="")
        self.game_state = GameState.DRAW
        self.deck = Deck()
        self.current_hand = [self.deck.dealOne() for _ in range(5)]
        self.analyze()
        self.show_cards()

    def reset_holds(self):
        self.holds = [False] * 5
        for lbl in self.card_labels:
            lbl.config(highlightbackground="#0a3d0a")

    def process_draw(self):
        for i, held in enumerate(self.holds):
            if not held:
                self.current_hand[i] = self.deck.dealOne()

        self.show_cards()
        self.result_label.config(text=f"{self.analyzer.rank.name.replace("_", " ")}")
        self.reset_holds()

    def play_action(self):
        if self.game_state == GameState.DEAL:
            self.process_deal()  # Logic for dealing
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