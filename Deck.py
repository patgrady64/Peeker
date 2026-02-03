import random

import Card

class Deck(object):
    def __init__(self):
        self.cards = []
        self.new()
        self.shuffle()

    def new(self):
        for s in ["c", "d", "h", "s"]:
            for v in ["2", "3", "4", "5", "6", "7", "8", "9", "t", "j", "q", "k", "a"]:
                match v:
                    case "2":
                        fullValue = "Two"
                        intValue = 2
                    case "3":
                        fullValue = "Three"
                        intValue = 3
                    case "4":
                        fullValue = "Four"
                        intValue = 4
                    case "5":
                        fullValue = "Five"
                        intValue = 5
                    case "6":
                        fullValue = "Six"
                        intValue = 6
                    case "7":
                        fullValue = "Seven"
                        intValue = 7
                    case "8":
                        fullValue = "Eight"
                        intValue = 8
                    case "9":
                        fullValue = "Nine"
                        intValue = 9
                    case "t":
                        fullValue = "Ten"
                        intValue = 10
                    case "j":
                        fullValue = "Jack"
                        intValue = 11
                    case "q":
                        fullValue = "Queen"
                        intValue = 12
                    case "k":
                        fullValue = "King"
                        intValue = 13
                    case "a":
                        fullValue = "Ace"
                        intValue = 14
                match s:
                    case "c":
                        fullSuit = "Clubs"
                    case "d":
                        fullSuit = "Diamonds"
                    case "h":
                        fullSuit = "Hearts"
                    case "s":
                        fullSuit = "Spades"

                newCard = Card.Card(v,s, fullValue, intValue, fullSuit)
                self.cards.append(newCard)

    def shuffle(self):
        random.shuffle(self.cards)

    def dealOne(self):
        return self.cards.pop()