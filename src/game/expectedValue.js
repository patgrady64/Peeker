import { calculateDiscardAllExpectedValue } from './discardAllExpectedValue';
import { forEachCombination } from './drawCombinations';
import { evaluateHand } from './handEvaluator';
import { getPayoutMultiplier } from './payTable';

export function calculateHoldExpectedValue(
  hand,
  remainingDeck,
  heldIndexes,
  wager = 5,
) {
  if (heldIndexes.length === 0) {
    return calculateDiscardAllExpectedValue(remainingDeck, wager);
  }

  const heldCards = heldIndexes.map((index) => hand[index]);

  const cardsToDraw = hand.length - heldCards.length;
  const finalHand = new Array(hand.length);

  for (let index = 0; index < heldCards.length; index += 1) {
    finalHand[index] = heldCards[index];
  }

  let totalPayout = 0;

  const possibleDraws = forEachCombination(
    remainingDeck,
    cardsToDraw,
    (drawnCards) => {
      for (let index = 0; index < drawnCards.length; index += 1) {
        finalHand[heldCards.length + index] = drawnCards[index];
      }

      const result = evaluateHand(finalHand);
      totalPayout += getPayoutMultiplier(result, wager);
    },
  );

  const expectedValue = possibleDraws === 0 ? 0 : totalPayout / possibleDraws;

  return {
    heldIndexes: [...heldIndexes],
    possibleDraws,
    totalPayout,
    expectedValue,
  };
}
