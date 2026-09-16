import { findBestHolds } from '../bestHold';
import { createDeck } from '../deck';

describe('optimal-hold performance', () => {
  test('analyzes a complete 47-card unseen deck', () => {
    const deck = createDeck();
    const hand = deck.slice(0, 5);
    const remainingDeck = deck.slice(5);

    const startTime = Date.now();

    const bestHolds = findBestHolds(hand, remainingDeck);

    const elapsedMilliseconds = Date.now() - startTime;

    console.log(`Complete analysis: ${elapsedMilliseconds} ms`);

    console.log('Best hold:', bestHolds[0].heldIndexes);

    console.log('Expected value:', bestHolds[0].expectedValue);

    expect(bestHolds.length).toBeGreaterThan(0);
  }, 120000);
});
