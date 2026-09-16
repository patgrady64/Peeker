import { getFastStrategyHold } from '../fastStrategy';

function card(rank, suit) {
  return { rank, suit };
}

describe('getFastStrategyHold', () => {
  test('holds a completed Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3, 4]);
  });

  test('holds only the four of a kind', () => {
    const hand = [
      card('8', 'clubs'),
      card('8', 'diamonds'),
      card('K', 'clubs'),
      card('8', 'hearts'),
      card('8', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 3, 4]);
  });

  test('holds four cards to a Royal Flush', () => {
    const hand = [
      card('10', 'spades'),
      card('J', 'spades'),
      card('4', 'clubs'),
      card('Q', 'spades'),
      card('K', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 3, 4]);
  });

  test('holds a completed Full House', () => {
    const hand = [
      card('Q', 'clubs'),
      card('4', 'diamonds'),
      card('Q', 'hearts'),
      card('4', 'spades'),
      card('Q', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3, 4]);
  });

  test('holds only Three of a Kind', () => {
    const hand = [
      card('7', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'hearts'),
      card('K', 'spades'),
      card('7', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 2, 4]);
  });

  test('holds four cards to a Straight Flush', () => {
    const hand = [
      card('4', 'clubs'),
      card('5', 'clubs'),
      card('K', 'hearts'),
      card('6', 'clubs'),
      card('7', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 3, 4]);
  });

  test('holds both pairs and discards the kicker', () => {
    const hand = [
      card('J', 'clubs'),
      card('4', 'diamonds'),
      card('J', 'hearts'),
      card('9', 'spades'),
      card('4', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 4]);
  });

  test('holds a high pair', () => {
    const hand = [
      card('K', 'clubs'),
      card('3', 'diamonds'),
      card('7', 'hearts'),
      card('K', 'spades'),
      card('9', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 3]);
  });

  test('holds three cards to a Royal Flush', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('4', 'clubs'),
      card('Q', 'hearts'),
      card('7', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 3]);
  });

  test('falls back when a three-to-Royal and four-flush conflict may need an exception', () => {
    const hand = [
      card('10', 'hearts'),
      card('A', 'hearts'),
      card('Q', 'hearts'),
      card('4', 'hearts'),
      card('7', 'spades'),
    ];

    expect(getFastStrategyHold(hand)).toBeNull();
  });

  test('holds four cards to a Flush', () => {
    const hand = [
      card('2', 'clubs'),
      card('5', 'clubs'),
      card('8', 'clubs'),
      card('K', 'clubs'),
      card('3', 'hearts'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3]);
  });

  test('holds unsuited 10-J-Q-K', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'clubs'),
      card('Q', 'spades'),
      card('K', 'diamonds'),
      card('3', 'hearts'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3]);
  });

  test('holds a low pair', () => {
    const hand = [
      card('8', 'clubs'),
      card('3', 'diamonds'),
      card('8', 'hearts'),
      card('K', 'spades'),
      card('5', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 2]);
  });

  test('holds four cards to an outside Straight', () => {
    const hand = [
      card('5', 'clubs'),
      card('6', 'diamonds'),
      card('K', 'hearts'),
      card('7', 'spades'),
      card('8', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 3, 4]);
  });

  test('holds three cards to a Straight Flush (type 1)', () => {
    const hand = [
      card('4', 'clubs'),
      card('5', 'clubs'),
      card('6', 'clubs'),
      card('K', 'diamonds'),
      card('2', 'hearts'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2]);
  });

  test('holds suited Q-J', () => {
    const hand = [
      card('Q', 'hearts'),
      card('J', 'hearts'),
      card('3', 'clubs'),
      card('7', 'spades'),
      card('9', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds four cards to an inside Straight with four high cards', () => {
    const hand = [
      card('J', 'clubs'),
      card('Q', 'diamonds'),
      card('K', 'hearts'),
      card('A', 'spades'),
      card('3', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3]);
  });

  test('holds suited K-Q', () => {
    const hand = [
      card('K', 'hearts'),
      card('Q', 'hearts'),
      card('3', 'clubs'),
      card('7', 'spades'),
      card('9', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds suited A-K', () => {
    const hand = [
      card('A', 'hearts'),
      card('K', 'hearts'),
      card('3', 'clubs'),
      card('7', 'spades'),
      card('9', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds four cards to an inside Straight with three high cards', () => {
    const hand = [
      card('9', 'clubs'),
      card('J', 'diamonds'),
      card('Q', 'hearts'),
      card('K', 'spades'),
      card('3', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2, 3]);
  });

  test('holds three cards to a Straight Flush (type 2)', () => {
    const hand = [
      card('7', 'clubs'),
      card('8', 'clubs'),
      card('10', 'clubs'),
      card('2', 'hearts'),
      card('K', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2]);
  });

  test('holds unsuited J-Q-K', () => {
    const hand = [
      card('J', 'hearts'),
      card('Q', 'clubs'),
      card('K', 'spades'),
      card('2', 'diamonds'),
      card('7', 'hearts'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2]);
  });

  test('holds unsuited J-Q', () => {
    const hand = [
      card('J', 'hearts'),
      card('Q', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds suited 10-J', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('2', 'clubs'),
      card('7', 'spades'),
      card('9', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds two unsuited high cards with King highest', () => {
    const hand = [
      card('J', 'hearts'),
      card('K', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds suited 10-Q', () => {
    const hand = [
      card('10', 'hearts'),
      card('Q', 'hearts'),
      card('2', 'clubs'),
      card('7', 'spades'),
      card('9', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds two unsuited high cards with Ace highest', () => {
    const hand = [
      card('J', 'hearts'),
      card('A', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'hearts'),
      card('9', 'spades'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test('holds a single Jack', () => {
    const hand = [
      card('J', 'hearts'),
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('7', 'spades'),
      card('9', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0]);
  });

  test('holds suited 10-K', () => {
    const hand = [
      card('10', 'hearts'),
      card('K', 'hearts'),
      card('2', 'clubs'),
      card('7', 'spades'),
      card('8', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1]);
  });

  test.each([
    ['Q', 'Queen'],
    ['K', 'King'],
    ['A', 'Ace'],
  ])('holds a single %s', (rank) => {
    const hand = [
      card(rank, 'hearts'),
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('7', 'spades'),
      card('9', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0]);
  });

  test('holds three cards to a Straight Flush (type 3)', () => {
    const hand = [
      card('6', 'clubs'),
      card('7', 'clubs'),
      card('10', 'clubs'),
      card('2', 'hearts'),
      card('4', 'diamonds'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([0, 1, 2]);
  });

  test('discards all five cards from garbage', () => {
    const hand = [
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('8', 'hearts'),
      card('10', 'spades'),
      card('3', 'clubs'),
    ];

    expect(getFastStrategyHold(hand).heldIndexes).toEqual([]);
  });

  test('falls back for suited Q-J versus a four-high inside Straight conflict', () => {
    const hand = [
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'clubs'),
      card('A', 'diamonds'),
      card('3', 'spades'),
    ];

    expect(getFastStrategyHold(hand)).toBeNull();
  });

  test('falls back for suited 10-J versus unsuited J-K penalty-card conflict', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('K', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'spades'),
    ];

    expect(getFastStrategyHold(hand)).toBeNull();
  });

  test('falls back for suited 10-Q versus unsuited Q-A penalty-card conflict', () => {
    const hand = [
      card('10', 'hearts'),
      card('Q', 'hearts'),
      card('A', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'spades'),
    ];

    expect(getFastStrategyHold(hand)).toBeNull();
  });

  test('falls back conservatively for suited 10-K when a 9 is discarded', () => {
    const hand = [
      card('10', 'hearts'),
      card('K', 'hearts'),
      card('9', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'spades'),
    ];

    expect(getFastStrategyHold(hand)).toBeNull();
  });
});
