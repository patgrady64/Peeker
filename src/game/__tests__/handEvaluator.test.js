import { evaluateHand, evaluateHandValue } from '../handEvaluator';

function card(rank, suit) {
  return { rank, suit };
}

describe('evaluateHand', () => {
  test('recognizes a Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
    ];

    expect(evaluateHand(hand)).toBe('Royal Flush');
  });

  test('recognizes a Straight Flush', () => {
    const hand = [
      card('5', 'clubs'),
      card('6', 'clubs'),
      card('7', 'clubs'),
      card('8', 'clubs'),
      card('9', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Straight Flush');
  });

  test('recognizes Four of a Kind', () => {
    const hand = [
      card('8', 'clubs'),
      card('8', 'diamonds'),
      card('8', 'hearts'),
      card('8', 'spades'),
      card('K', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Four of a Kind');
  });

  test('recognizes a Full House', () => {
    const hand = [
      card('Q', 'clubs'),
      card('Q', 'diamonds'),
      card('Q', 'hearts'),
      card('4', 'spades'),
      card('4', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Full House');
  });

  test('recognizes a Flush', () => {
    const hand = [
      card('2', 'diamonds'),
      card('5', 'diamonds'),
      card('8', 'diamonds'),
      card('J', 'diamonds'),
      card('K', 'diamonds'),
    ];

    expect(evaluateHand(hand)).toBe('Flush');
  });

  test('recognizes a normal Straight', () => {
    const hand = [
      card('6', 'clubs'),
      card('7', 'diamonds'),
      card('8', 'hearts'),
      card('9', 'spades'),
      card('10', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Straight');
  });

  test('recognizes an ace-low Straight', () => {
    const hand = [
      card('A', 'clubs'),
      card('2', 'diamonds'),
      card('3', 'hearts'),
      card('4', 'spades'),
      card('5', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Straight');
  });

  test('recognizes Three of a Kind', () => {
    const hand = [
      card('7', 'clubs'),
      card('7', 'diamonds'),
      card('7', 'hearts'),
      card('2', 'spades'),
      card('K', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Three of a Kind');
  });

  test('recognizes Two Pair', () => {
    const hand = [
      card('J', 'clubs'),
      card('J', 'diamonds'),
      card('4', 'hearts'),
      card('4', 'spades'),
      card('9', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Two Pair');
  });

  test('recognizes Jacks or Better', () => {
    const hand = [
      card('K', 'clubs'),
      card('K', 'diamonds'),
      card('3', 'hearts'),
      card('7', 'spades'),
      card('9', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Jacks or Better');
  });

  test('rejects a low pair', () => {
    const hand = [
      card('9', 'clubs'),
      card('9', 'diamonds'),
      card('2', 'hearts'),
      card('5', 'spades'),
      card('K', 'clubs'),
    ];

    expect(evaluateHand(hand)).toBe('Nothing');
  });
});

describe('evaluateHandValue', () => {
  test('shows a low pair as Pair even though it does not pay', () => {
    const hand = [
      card('9', 'clubs'),
      card('9', 'diamonds'),
      card('2', 'hearts'),
      card('5', 'spades'),
      card('K', 'clubs'),
    ];

    expect(evaluateHandValue(hand)).toBe('Pair');
  });

  test('shows Jacks or Better as the poker hand value Pair', () => {
    const hand = [
      card('Q', 'clubs'),
      card('Q', 'diamonds'),
      card('2', 'hearts'),
      card('5', 'spades'),
      card('9', 'clubs'),
    ];

    expect(evaluateHandValue(hand)).toBe('Pair');
  });

  test('keeps made hand names such as Full House', () => {
    const hand = [
      card('K', 'clubs'),
      card('K', 'diamonds'),
      card('K', 'hearts'),
      card('4', 'spades'),
      card('4', 'clubs'),
    ];

    expect(evaluateHandValue(hand)).toBe('Full House');
  });

  test('shows Nothing when there is no pair or better', () => {
    const hand = [
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('8', 'hearts'),
      card('J', 'spades'),
      card('K', 'clubs'),
    ];

    expect(evaluateHandValue(hand)).toBe('Nothing');
  });
});

