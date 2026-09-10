import { generateCombinations } from './drawCombinations';
import { evaluateHand } from './handEvaluator';
import { getPayoutMultiplier } from './payTable';

export function calculateHoldExpectedValue(hand, remainingDeck, heldIndexes) {
  const heldCards = heldIndexes.map((index) => hand[index]);

  const cardsToDraw = hand.length - heldCards.length;

  let totalPayout = 0;
  let possibleDraws = 0;

  for (const drawnCards of generateCombinations(remainingDeck, cardsToDraw)) {
    const finalHand = [...heldCards, ...drawnCards];
    const result = evaluateHand(finalHand);
    const payout = getPayoutMultiplier(result);

    totalPayout += payout;
    possibleDraws += 1;
  }

  const expectedValue = possibleDraws === 0 ? 0 : totalPayout / possibleDraws;

  return {
    heldIndexes: [...heldIndexes],
    possibleDraws,
    totalPayout,
    expectedValue,
  };
}
