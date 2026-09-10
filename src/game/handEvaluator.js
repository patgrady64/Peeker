const rankValues = {
  2: 2,
  3: 3,
  4: 4,
  5: 5,
  6: 6,
  7: 7,
  8: 8,
  9: 9,
  10: 10,
  J: 11,
  Q: 12,
  K: 13,
  A: 14,
};

export function evaluateHand(hand) {
  const values = hand
    .map((card) => rankValues[card.rank])
    .sort((first, second) => first - second);

  const rankCounts = {};

  values.forEach((value) => {
    rankCounts[value] = (rankCounts[value] || 0) + 1;
  });

  const counts = Object.values(rankCounts).sort(
    (first, second) => second - first,
  );

  const uniqueValues = [...new Set(values)];

  const isFlush = hand.every((card) => card.suit === hand[0].suit);

  const isNormalStraight =
    uniqueValues.length === 5 && uniqueValues[4] - uniqueValues[0] === 4;

  const isLowAceStraight =
    JSON.stringify(uniqueValues) === JSON.stringify([2, 3, 4, 5, 14]);

  const isStraight = isNormalStraight || isLowAceStraight;

  const isRoyal =
    JSON.stringify(uniqueValues) === JSON.stringify([10, 11, 12, 13, 14]);

  if (isFlush && isRoyal) {
    return 'Royal Flush';
  }

  if (isFlush && isStraight) {
    return 'Straight Flush';
  }

  if (counts[0] === 4) {
    return 'Four of a Kind';
  }

  if (counts[0] === 3 && counts[1] === 2) {
    return 'Full House';
  }

  if (isFlush) {
    return 'Flush';
  }

  if (isStraight) {
    return 'Straight';
  }

  if (counts[0] === 3) {
    return 'Three of a Kind';
  }

  if (counts[0] === 2 && counts[1] === 2) {
    return 'Two Pair';
  }

  const pairEntry = Object.entries(rankCounts).find(([, count]) => count === 2);

  if (pairEntry) {
    const pairValue = Number(pairEntry[0]);

    if (pairValue >= rankValues.J) {
      return 'Jacks or Better';
    }
  }

  return 'Nothing';
}
