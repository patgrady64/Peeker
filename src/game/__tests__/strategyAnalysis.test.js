import { findBestHolds } from '../bestHold';
import { analyzeBestHold } from '../strategyAnalysis';

function card(rank, suit) {
  return { rank, suit };
}

describe('analyzeBestHold', () => {
  test('uses a fast rule and still calculates its expected value', () => {
    const hand = [
      card('J', 'clubs'),
      card('4', 'diamonds'),
      card('J', 'hearts'),
      card('9', 'spades'),
      card('4', 'clubs'),
    ];

    const remainingDeck = [card('A', 'spades')];
    const analysis = analyzeBestHold(hand, remainingDeck);

    expect(analysis.method).toBe('fast');
    expect(analysis.rule).toBe('Hold both pairs');
    expect(analysis.bestHolds[0].heldIndexes).toEqual([0, 1, 2, 4]);
    expect(analysis.bestHolds[0].possibleDraws).toBe(1);
    expect(analysis.bestHolds[0].expectedValue).toBe(2);
  });

  test('falls back to exhaustive analysis for a penalty-card exception', () => {
    const hand = [
      card('10', 'hearts'),
      card('J', 'hearts'),
      card('K', 'clubs'),
      card('2', 'diamonds'),
      card('7', 'spades'),
    ];

    const remainingDeck = [
      card('J', 'clubs'),
      card('K', 'hearts'),
      card('A', 'spades'),
      card('3', 'diamonds'),
      card('7', 'clubs'),
    ];

    const analysis = analyzeBestHold(hand, remainingDeck);
    const exhaustiveBestHolds = findBestHolds(hand, remainingDeck);

    expect(analysis.method).toBe('exhaustive');
    expect(analysis.rule).toBeNull();
    expect(analysis.bestHolds).toEqual(exhaustiveBestHolds);
  });

  test('uses wager-aware exhaustive analysis below max bet', () => {
    const hand = [
      card('J', 'clubs'),
      card('4', 'diamonds'),
      card('J', 'hearts'),
      card('9', 'spades'),
      card('4', 'clubs'),
    ];

    const remainingDeck = [card('A', 'spades')];
    const analysis = analyzeBestHold(hand, remainingDeck, 1);

    expect(analysis.method).toBe('exhaustive');
  });

});
