import { findBestHolds } from './bestHold';
import { calculateHoldExpectedValue } from './expectedValue';
import { getFastStrategyHold } from './fastStrategy';

export function analyzeBestHold(hand, remainingDeck, wager = 5) {
  // The fast chart is the standard max-coin 9/6 Jacks or Better strategy.
  // At 1-4 credits the Royal Flush bonus is lower, so use exhaustive EV
  // to make sure the trainer remains correct for the selected wager.
  if (wager === 5) {
    const fastHold = getFastStrategyHold(hand);

    if (fastHold) {
      return {
        bestHolds: [
          calculateHoldExpectedValue(
            hand,
            remainingDeck,
            fastHold.heldIndexes,
            wager,
          ),
        ],
        method: 'fast',
        rule: fastHold.rule,
      };
    }
  }

  return {
    bestHolds: findBestHolds(hand, remainingDeck, undefined, wager),
    method: 'exhaustive',
    rule: null,
  };
}
