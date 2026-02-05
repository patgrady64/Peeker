from HandRank import HandRank

PAYOUT_TABLE = {
    HandRank.ROYAL_FLUSH: 800,
    HandRank.STRAIGHT_FLUSH: 50,
    HandRank.FOUR_OF_A_KIND: 25,
    HandRank.FULL_HOUSE: 9,
    HandRank.FLUSH: 6,
    HandRank.STRAIGHT: 4,
    HandRank.THREE_OF_A_KIND: 3,
    HandRank.TWO_PAIR: 2,
    HandRank.PAIR: 1,       # Note: Logic must check if self.primary >= 11
    HandRank.HIGH_CARD: 0
}