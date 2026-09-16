import { findBestHolds } from './bestHold';
import { calculateHoldExpectedValue } from './expectedValue';
import { getFastStrategyHold } from './fastStrategy';

export function analyzeBestHold(hand, remainingDeck) {
  const fastHold = getFastStrategyHold(hand);

  if (fastHold) {
    return {
      bestHolds: [
        calculateHoldExpectedValue(
          hand,
          remainingDeck,
          fastHold.heldIndexes,
        ),
      ],
      method: 'fast',
      rule: fastHold.rule,
    };
  }

  return {
    bestHolds: findBestHolds(hand, remainingDeck),
    method: 'exhaustive',
    rule: null,
  };
}
