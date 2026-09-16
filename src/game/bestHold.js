import { calculateHoldExpectedValue } from './expectedValue';
import { createHoldCombinations } from './holdCombinations';

const EQUALITY_TOLERANCE = 0.000000001;

export function findBestHolds(
  hand,
  remainingDeck,
  holdCombinations = createHoldCombinations(),
) {
  let bestExpectedValue = -Infinity;
  let bestHolds = [];

  for (const heldIndexes of holdCombinations) {
    const result = calculateHoldExpectedValue(hand, remainingDeck, heldIndexes);

    if (result.possibleDraws === 0) {
      continue;
    }

    const isBetter =
      result.expectedValue > bestExpectedValue + EQUALITY_TOLERANCE;

    const isTied =
      Math.abs(result.expectedValue - bestExpectedValue) <= EQUALITY_TOLERANCE;

    if (isBetter) {
      bestExpectedValue = result.expectedValue;
      bestHolds = [result];
    } else if (isTied) {
      bestHolds.push(result);
    }
  }

  return bestHolds;
}
