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
  if (!hand || hand.length !== 5) {
    return 'Nothing';
  }

  const rankCounts = new Uint8Array(15);

  let uniqueRankCount = 0;
  let lowestRank = 15;
  let highestRank = 0;
  let isFlush = true;

  const firstSuit = hand[0].suit;

  for (let index = 0; index < 5; index += 1) {
    const card = hand[index];
    const rankValue = rankValues[card.rank];

    if (rankCounts[rankValue] === 0) {
      uniqueRankCount += 1;
    }

    rankCounts[rankValue] += 1;

    if (rankValue < lowestRank) {
      lowestRank = rankValue;
    }

    if (rankValue > highestRank) {
      highestRank = rankValue;
    }

    if (card.suit !== firstSuit) {
      isFlush = false;
    }
  }

  let pairCount = 0;
  let pairRank = 0;
  let hasThreeOfAKind = false;
  let hasFourOfAKind = false;

  for (let rank = 2; rank <= 14; rank += 1) {
    const count = rankCounts[rank];

    if (count === 4) {
      hasFourOfAKind = true;
    } else if (count === 3) {
      hasThreeOfAKind = true;
    } else if (count === 2) {
      pairCount += 1;
      pairRank = rank;
    }
  }

  const isNormalStraight =
    uniqueRankCount === 5 && highestRank - lowestRank === 4;

  const isLowAceStraight =
    uniqueRankCount === 5 &&
    rankCounts[14] === 1 &&
    rankCounts[2] === 1 &&
    rankCounts[3] === 1 &&
    rankCounts[4] === 1 &&
    rankCounts[5] === 1;

  const isStraight = isNormalStraight || isLowAceStraight;

  const isRoyal =
    uniqueRankCount === 5 && lowestRank === 10 && highestRank === 14;

  if (isFlush && isRoyal) {
    return 'Royal Flush';
  }

  if (isFlush && isStraight) {
    return 'Straight Flush';
  }

  if (hasFourOfAKind) {
    return 'Four of a Kind';
  }

  if (hasThreeOfAKind && pairCount === 1) {
    return 'Full House';
  }

  if (isFlush) {
    return 'Flush';
  }

  if (isStraight) {
    return 'Straight';
  }

  if (hasThreeOfAKind) {
    return 'Three of a Kind';
  }

  if (pairCount === 2) {
    return 'Two Pair';
  }

  if (pairCount === 1 && pairRank >= rankValues.J) {
    return 'Jacks or Better';
  }

  return 'Nothing';
}

export function evaluateHandValue(hand) {
  const payoutResult = evaluateHand(hand);

  if (payoutResult === 'Jacks or Better') {
    return 'Pair';
  }

  if (payoutResult !== 'Nothing') {
    return payoutResult;
  }

  if (!hand || hand.length !== 5) {
    return 'Nothing';
  }

  const seenRanks = new Set();

  for (const card of hand) {
    if (seenRanks.has(card.rank)) {
      return 'Pair';
    }

    seenRanks.add(card.rank);
  }

  return 'Nothing';
}

