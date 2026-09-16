import { createDeck } from '../deck';
import { calculateDiscardAllExpectedValue } from '../discardAllExpectedValue';
import { forEachCombination } from '../drawCombinations';
import { evaluateHand } from '../handEvaluator';
import { getPayoutMultiplier } from '../payTable';

function card(rank, suit) {
  return { rank, suit };
}

function bruteForce(remainingDeck) {
  let totalPayout = 0;
  const possibleDraws = forEachCombination(remainingDeck, 5, (drawnCards) => {
    totalPayout += getPayoutMultiplier(evaluateHand(drawnCards));
  });

  return {
    possibleDraws,
    totalPayout,
    expectedValue: possibleDraws === 0 ? 0 : totalPayout / possibleDraws,
  };
}

function remainingDeckAfter(hand) {
  const discarded = new Set(hand.map((item) => `${item.rank}-${item.suit}`));
  return createDeck().filter(
    (item) => !discarded.has(`${item.rank}-${item.suit}`),
  );
}

describe('calculateDiscardAllExpectedValue', () => {
  test('matches the known full-deck redraw result exactly', () => {
    const hand = [
      card('2', 'clubs'),
      card('5', 'diamonds'),
      card('8', 'hearts'),
      card('10', 'spades'),
      card('3', 'clubs'),
    ];

    const result = calculateDiscardAllExpectedValue(remainingDeckAfter(hand));

    expect(result.heldIndexes).toEqual([]);
    expect(result.possibleDraws).toBe(1533939);
    expect(result.totalPayout).toBe(551088);
    expect(result.expectedValue).toBe(551088 / 1533939);
  });

  test('matches brute force on a smaller mixed deck', () => {
    const remainingDeck = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
      card('9', 'hearts'),
      card('J', 'clubs'),
      card('J', 'diamonds'),
      card('4', 'clubs'),
      card('4', 'diamonds'),
      card('7', 'spades'),
    ];

    const optimized = calculateDiscardAllExpectedValue(remainingDeck);
    const brute = bruteForce(remainingDeck);

    expect(optimized.possibleDraws).toBe(brute.possibleDraws);
    expect(optimized.totalPayout).toBe(brute.totalPayout);
    expect(optimized.expectedValue).toBe(brute.expectedValue);
  });

  test('returns zero when fewer than five cards can be drawn', () => {
    const result = calculateDiscardAllExpectedValue([
      card('A', 'spades'),
      card('K', 'spades'),
      card('Q', 'spades'),
      card('J', 'spades'),
    ]);

    expect(result.possibleDraws).toBe(0);
    expect(result.totalPayout).toBe(0);
    expect(result.expectedValue).toBe(0);
  });
});

describe('calculateDiscardAllExpectedValue wager-aware Royal payout', () => {
  test('uses 250 per credit below max bet and 800 per credit at max bet', () => {
    const royalOnlyDeck = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('Q', 'hearts'),
      card('K', 'hearts'),
      card('A', 'hearts'),
    ];

    expect(calculateDiscardAllExpectedValue(royalOnlyDeck, 1).expectedValue).toBe(250);
    expect(calculateDiscardAllExpectedValue(royalOnlyDeck, 5).expectedValue).toBe(800);
  });
});
