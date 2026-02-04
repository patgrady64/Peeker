from HandRanks import HandRanks

PAYOUT_TABLE = {
    HandRanks.ROYAL_FLUSH: 800,
    HandRanks.STRAIGHT_FLUSH: 50,
    HandRanks.FOUR_OF_A_KIND: 25,
    HandRanks.FULL_HOUSE: 9,
    HandRanks.FLUSH: 6,
    HandRanks.STRAIGHT: 4,
    HandRanks.THREE_OF_A_KIND: 3,
    HandRanks.TWO_PAIR: 2,
    HandRanks.PAIR: 1,       # Note: Logic must check if self.primary >= 11
    HandRanks.HIGH_CARD: 0
}