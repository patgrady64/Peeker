import tkinter as tk
from tkinter import messagebox
from Deck import Deck
from HandAnalyzer import HandAnalyzer


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

        # --- UI Elements ---
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
            self.card_labels.append(lbl)
            lbl.bind("<Button-1>", lambda event, i=i: self.toggle_hold(event, i))

        # 3. Button Area
        self.deal_button = tk.Button(
            self.root,
            text="DEAL",
            command=self.deal_hand,
            font=("Arial", 14, "bold"),
            width=15,
            bg="#ffcc00"
        )
        self.deal_button.pack(pady=20)

    def deal_hand(self):
        """Simple test to see if we can draw from your Deck class."""
        self.deck = Deck()  # Fresh deck
        self.current_hand = [self.deck.dealOne() for _ in range(5)]

        # Update the labels
        for i, card in enumerate(self.current_hand):
            # Using your card's value and suit
            display_text = f"{card.value.upper()}\n{card.suit.upper()}"
            self.card_labels[i].config(text=display_text)

        print("Hand dealt successfully!")

    def toggle_hold(self, event, i):
        # 1. Flip the boolean (True becomes False, False becomes True)
        self.holds[i] = not self.holds[i]

        # 2. Update the visual border
        if self.holds[i]:
            self.card_labels[i].config(highlightbackground="lime")
        else:
            self.card_labels[i].config(highlightbackground="#0a3d0a")

        print(f"Card {i} hold status: {self.holds[i]}")