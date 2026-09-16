import { findBestHolds } from '../bestHold';

function card(rank, suit) {
  return { rank, suit };
}

describe('findBestHolds', () => {
  test('holds all five cards in a Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
    ];

    const bestHolds = findBestHolds(hand, []);

    expect(bestHolds).toHaveLength(1);
    expect(bestHolds[0].heldIndexes).toEqual([0, 1, 2, 3, 4]);
    expect(bestHolds[0].expectedValue).toBe(800);
  });

  test('selects four cards to a Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('4', 'clubs'),
    ];

    const remainingDeck = [card('A', 'hearts'), card('2', 'clubs')];

    const bestHolds = findBestHolds(hand, remainingDeck);

    expect(bestHolds).toHaveLength(1);
    expect(bestHolds[0].heldIndexes).toEqual([0, 1, 2, 3]);
    expect(bestHolds[0].expectedValue).toBe(400);
  });

  test('keeps multiple holds when they have equal value', () => {
    const hand = [
      card('J', 'spades'),
      card('J', 'hearts'),
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('8', 'spades'),
    ];

    const remainingDeck = [
      card('Q', 'clubs'),
      card('Q', 'diamonds'),
      card('K', 'clubs'),
      card('K', 'diamonds'),
    ];

    const candidateHolds = [[0], [1]];

    const bestHolds = findBestHolds(hand, remainingDeck, candidateHolds);

    expect(bestHolds).toHaveLength(2);
    expect(bestHolds[0].heldIndexes).toEqual([0]);
    expect(bestHolds[1].heldIndexes).toEqual([1]);
    expect(bestHolds[0].expectedValue).toBe(2);
    expect(bestHolds[1].expectedValue).toBe(2);
  });

  test('returns an empty list when no hold can be evaluated', () => {
    const hand = [
      card('2', 'clubs'),
      card('4', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
      card('K', 'clubs'),
    ];

    const bestHolds = findBestHolds(hand, [], [[]]);

    expect(bestHolds).toEqual([]);
  });
});
