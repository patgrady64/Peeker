const RANKS = [
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '10',
  'J',
  'Q',
  'K',
  'A',
];

const HIGH_PAIR_RANKS = new Set(['J', 'Q', 'K', 'A']);

const STRAIGHT_RANKS = [
  ['A', '2', '3', '4', '5'],
  ['2', '3', '4', '5', '6'],
  ['3', '4', '5', '6', '7'],
  ['4', '5', '6', '7', '8'],
  ['5', '6', '7', '8', '9'],
  ['6', '7', '8', '9', '10'],
  ['7', '8', '9', '10', 'J'],
  ['8', '9', '10', 'J', 'Q'],
  ['9', '10', 'J', 'Q', 'K'],
  ['10', 'J', 'Q', 'K', 'A'],
];

const ROYAL_RANKS = ['10', 'J', 'Q', 'K', 'A'];

const PAYOUTS = {
  royalFlush: 800,
  straightFlush: 50,
  fourOfAKind: 25,
  fullHouse: 9,
  flush: 6,
  straight: 4,
  threeOfAKind: 3,
  twoPair: 2,
  jacksOrBetter: 1,
};

function choose(n, k) {
  if (k < 0 || n < k) {
    return 0;
  }

  if (k === 0 || n === k) {
    return 1;
  }

  let result = 1;
  const smallerK = Math.min(k, n - k);

  for (let index = 1; index <= smallerK; index += 1) {
    result = (result * (n - smallerK + index)) / index;
  }

  return result;
}

function buildAvailability(remainingDeck) {
  const rankCounts = Object.fromEntries(RANKS.map((rank) => [rank, 0]));
  const suitCards = new Map();

  for (const card of remainingDeck) {
    rankCounts[card.rank] += 1;

    if (!suitCards.has(card.suit)) {
      suitCards.set(card.suit, new Set());
    }

    suitCards.get(card.suit).add(card.rank);
  }

  return { rankCounts, suitCards };
}

function hasAllRanks(rankSet, ranks) {
  return ranks.every((rank) => rankSet.has(rank));
}

function countStraightFlushes(suitCards) {
  let royalFlushes = 0;
  let allStraightFlushes = 0;

  for (const rankSet of suitCards.values()) {
    if (hasAllRanks(rankSet, ROYAL_RANKS)) {
      royalFlushes += 1;
    }

    for (const straightRanks of STRAIGHT_RANKS) {
      if (hasAllRanks(rankSet, straightRanks)) {
        allStraightFlushes += 1;
      }
    }
  }

  return {
    royalFlushes,
    straightFlushes: allStraightFlushes - royalFlushes,
    allStraightFlushes,
  };
}

function countFourOfAKind(rankCounts, totalCards) {
  let count = 0;

  for (const rank of RANKS) {
    if (rankCounts[rank] === 4) {
      count += totalCards - 4;
    }
  }

  return count;
}

function countFullHouses(rankCounts) {
  let count = 0;

  for (const tripRank of RANKS) {
    const tripChoices = choose(rankCounts[tripRank], 3);

    if (tripChoices === 0) {
      continue;
    }

    for (const pairRank of RANKS) {
      if (pairRank === tripRank) {
        continue;
      }

      count += tripChoices * choose(rankCounts[pairRank], 2);
    }
  }

  return count;
}

function countFlushes(suitCards, allStraightFlushes) {
  let allFlushes = 0;

  for (const rankSet of suitCards.values()) {
    allFlushes += choose(rankSet.size, 5);
  }

  return allFlushes - allStraightFlushes;
}

function countStraights(rankCounts, suitCards) {
  let count = 0;

  for (const straightRanks of STRAIGHT_RANKS) {
    let rankCombinationCount = 1;

    for (const rank of straightRanks) {
      rankCombinationCount *= rankCounts[rank];
    }

    if (rankCombinationCount === 0) {
      continue;
    }

    let flushCombinationCount = 0;

    for (const rankSet of suitCards.values()) {
      if (hasAllRanks(rankSet, straightRanks)) {
        flushCombinationCount += 1;
      }
    }

    count += rankCombinationCount - flushCombinationCount;
  }

  return count;
}

function countThreeOfAKind(rankCounts) {
  let count = 0;

  for (let tripIndex = 0; tripIndex < RANKS.length; tripIndex += 1) {
    const tripRank = RANKS[tripIndex];
    const tripChoices = choose(rankCounts[tripRank], 3);

    if (tripChoices === 0) {
      continue;
    }

    for (let firstIndex = 0; firstIndex < RANKS.length - 1; firstIndex += 1) {
      if (firstIndex === tripIndex) {
        continue;
      }

      for (let secondIndex = firstIndex + 1; secondIndex < RANKS.length; secondIndex += 1) {
        if (secondIndex === tripIndex) {
          continue;
        }

        count +=
          tripChoices *
          rankCounts[RANKS[firstIndex]] *
          rankCounts[RANKS[secondIndex]];
      }
    }
  }

  return count;
}

function countTwoPair(rankCounts) {
  let count = 0;

  for (let firstPairIndex = 0; firstPairIndex < RANKS.length - 1; firstPairIndex += 1) {
    const firstPairRank = RANKS[firstPairIndex];
    const firstPairChoices = choose(rankCounts[firstPairRank], 2);

    if (firstPairChoices === 0) {
      continue;
    }

    for (let secondPairIndex = firstPairIndex + 1; secondPairIndex < RANKS.length; secondPairIndex += 1) {
      const secondPairRank = RANKS[secondPairIndex];
      const secondPairChoices = choose(rankCounts[secondPairRank], 2);

      if (secondPairChoices === 0) {
        continue;
      }

      for (let kickerIndex = 0; kickerIndex < RANKS.length; kickerIndex += 1) {
        if (kickerIndex === firstPairIndex || kickerIndex === secondPairIndex) {
          continue;
        }

        count +=
          firstPairChoices *
          secondPairChoices *
          rankCounts[RANKS[kickerIndex]];
      }
    }
  }

  return count;
}

function countJacksOrBetter(rankCounts) {
  let count = 0;

  for (let pairIndex = 0; pairIndex < RANKS.length; pairIndex += 1) {
    const pairRank = RANKS[pairIndex];

    if (!HIGH_PAIR_RANKS.has(pairRank)) {
      continue;
    }

    const pairChoices = choose(rankCounts[pairRank], 2);

    if (pairChoices === 0) {
      continue;
    }

    for (let firstIndex = 0; firstIndex < RANKS.length - 2; firstIndex += 1) {
      if (firstIndex === pairIndex) {
        continue;
      }

      for (let secondIndex = firstIndex + 1; secondIndex < RANKS.length - 1; secondIndex += 1) {
        if (secondIndex === pairIndex) {
          continue;
        }

        for (let thirdIndex = secondIndex + 1; thirdIndex < RANKS.length; thirdIndex += 1) {
          if (thirdIndex === pairIndex) {
            continue;
          }

          count +=
            pairChoices *
            rankCounts[RANKS[firstIndex]] *
            rankCounts[RANKS[secondIndex]] *
            rankCounts[RANKS[thirdIndex]];
        }
      }
    }
  }

  return count;
}

export function calculateDiscardAllExpectedValue(remainingDeck) {
  const possibleDraws = choose(remainingDeck.length, 5);

  if (possibleDraws === 0) {
    return {
      heldIndexes: [],
      possibleDraws: 0,
      totalPayout: 0,
      expectedValue: 0,
    };
  }

  const { rankCounts, suitCards } = buildAvailability(remainingDeck);
  const {
    royalFlushes,
    straightFlushes,
    allStraightFlushes,
  } = countStraightFlushes(suitCards);

  const fourOfAKind = countFourOfAKind(rankCounts, remainingDeck.length);
  const fullHouses = countFullHouses(rankCounts);
  const flushes = countFlushes(suitCards, allStraightFlushes);
  const straights = countStraights(rankCounts, suitCards);
  const threeOfAKind = countThreeOfAKind(rankCounts);
  const twoPair = countTwoPair(rankCounts);
  const jacksOrBetter = countJacksOrBetter(rankCounts);

  const totalPayout =
    royalFlushes * PAYOUTS.royalFlush +
    straightFlushes * PAYOUTS.straightFlush +
    fourOfAKind * PAYOUTS.fourOfAKind +
    fullHouses * PAYOUTS.fullHouse +
    flushes * PAYOUTS.flush +
    straights * PAYOUTS.straight +
    threeOfAKind * PAYOUTS.threeOfAKind +
    twoPair * PAYOUTS.twoPair +
    jacksOrBetter * PAYOUTS.jacksOrBetter;

  return {
    heldIndexes: [],
    possibleDraws,
    totalPayout,
    expectedValue: totalPayout / possibleDraws,
  };
}
