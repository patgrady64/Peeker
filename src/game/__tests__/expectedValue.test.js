import { calculateHoldExpectedValue } from '../expectedValue';

function card(rank, suit) {
  return { rank, suit };
}

describe('calculateHoldExpectedValue', () => {
  test('returns 800 when holding a Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
    ];

    const result = calculateHoldExpectedValue(hand, [], [0, 1, 2, 3, 4]);

    expect(result.possibleDraws).toBe(1);
    expect(result.totalPayout).toBe(800);
    expect(result.expectedValue).toBe(800);
  });

  test('averages all possible replacement payouts', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('4', 'clubs'),
    ];

    const remainingDeck = [card('A', 'hearts'), card('2', 'clubs')];

    const result = calculateHoldExpectedValue(
      hand,
      remainingDeck,
      [0, 1, 2, 3],
    );

    expect(result.possibleDraws).toBe(2);
    expect(result.totalPayout).toBe(800);
    expect(result.expectedValue).toBe(400);
  });

  test('returns zero for a held losing hand', () => {
    const hand = [
      card('2', 'clubs'),
      card('4', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
      card('K', 'clubs'),
    ];

    const result = calculateHoldExpectedValue(hand, [], [0, 1, 2, 3, 4]);

    expect(result.possibleDraws).toBe(1);
    expect(result.totalPayout).toBe(0);
    expect(result.expectedValue).toBe(0);
  });

  test('handles a deck without enough replacement cards', () => {
    const hand = [
      card('2', 'clubs'),
      card('4', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
      card('K', 'clubs'),
    ];

    const result = calculateHoldExpectedValue(hand, [card('A', 'hearts')], []);

    expect(result.possibleDraws).toBe(0);
    expect(result.expectedValue).toBe(0);
  });
});
