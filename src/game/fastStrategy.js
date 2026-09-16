import { evaluateHand } from './handEvaluator';

const royalRanks = new Set(['10', 'J', 'Q', 'K', 'A']);
const highRanks = new Set(['J', 'Q', 'K', 'A']);

const straightSequences = [
  [14, 2, 3, 4, 5],
  [2, 3, 4, 5, 6],
  [3, 4, 5, 6, 7],
  [4, 5, 6, 7, 8],
  [5, 6, 7, 8, 9],
  [6, 7, 8, 9, 10],
  [7, 8, 9, 10, 11],
  [8, 9, 10, 11, 12],
  [9, 10, 11, 12, 13],
  [10, 11, 12, 13, 14],
];

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

function findRankGroups(hand) {
  const groups = new Map();

  hand.forEach((card, index) => {
    const indexes = groups.get(card.rank) ?? [];
    indexes.push(index);
    groups.set(card.rank, indexes);
  });

  return [...groups.entries()];
}

function findIndexesWithCount(hand, count) {
  return findRankGroups(hand)
    .filter(([, indexes]) => indexes.length === count)
    .flatMap(([, indexes]) => indexes)
    .sort((left, right) => left - right);
}

function findRankSet(hand, ranks) {
  const indexes = ranks.map((rank) =>
    hand.findIndex((card) => card.rank === rank),
  );

  if (indexes.some((index) => index === -1)) {
    return null;
  }

  return indexes.sort((left, right) => left - right);
}

function findSuitedPair(hand, firstRank, secondRank) {
  const indexes = findRankSet(hand, [firstRank, secondRank]);

  if (!indexes) {
    return null;
  }

  return hand[indexes[0]].suit === hand[indexes[1]].suit ? indexes : null;
}

function findUnsuitedPair(hand, firstRank, secondRank) {
  const indexes = findRankSet(hand, [firstRank, secondRank]);

  if (!indexes) {
    return null;
  }

  return hand[indexes[0]].suit !== hand[indexes[1]].suit ? indexes : null;
}

function findThreeToRoyal(hand) {
  const suits = ['spades', 'hearts', 'diamonds', 'clubs'];

  for (const suit of suits) {
    const indexes = hand
      .map((card, index) => ({ card, index }))
      .filter(({ card }) => card.suit === suit && royalRanks.has(card.rank))
      .map(({ index }) => index);

    if (indexes.length === 3) {
      return indexes;
    }
  }

  return null;
}

function findFourToFlush(hand) {
  const suits = ['spades', 'hearts', 'diamonds', 'clubs'];

  for (const suit of suits) {
    const indexes = hand
      .map((card, index) => ({ card, index }))
      .filter(({ card }) => card.suit === suit)
      .map(({ index }) => index);

    if (indexes.length === 4) {
      return indexes;
    }
  }

  return null;
}

function findLowPair(hand) {
  const lowPair = findRankGroups(hand).find(
    ([rank, indexes]) => indexes.length === 2 && rankValues[rank] <= 10,
  );

  return lowPair ? [...lowPair[1]].sort((left, right) => left - right) : null;
}

function findUnsuitedTJQK(hand) {
  const indexes = findRankSet(hand, ['10', 'J', 'Q', 'K']);

  if (!indexes) {
    return null;
  }

  const suits = new Set(indexes.map((index) => hand[index].suit));

  return suits.size > 1 ? indexes : null;
}

function findFourToOutsideStraight(hand) {
  const valuesByIndex = hand.map((card, index) => ({
    index,
    value: rankValues[card.rank],
  }));

  for (let start = 2; start <= 9; start += 1) {
    const targetValues = [start, start + 1, start + 2, start + 3];
    const indexes = targetValues.map((value) =>
      valuesByIndex.find(({ value: cardValue }) => cardValue === value)?.index,
    );

    if (indexes.every((index) => index !== undefined)) {
      return indexes.sort((left, right) => left - right);
    }
  }

  return null;
}

function isConservativeRoyalFlushConflict(hand, threeToRoyal, fourToFlush) {
  if (!threeToRoyal || !fourToFlush) {
    return false;
  }

  const royalRanksInHold = new Set(
    threeToRoyal.map((index) => hand[index].rank),
  );

  return royalRanksInHold.has('10') && royalRanksInHold.has('A');
}

function findFourToRoyal(hand) {
  const suits = ['spades', 'hearts', 'diamonds', 'clubs'];

  for (const suit of suits) {
    const indexes = hand
      .map((card, index) => ({ card, index }))
      .filter(({ card }) => card.suit === suit && royalRanks.has(card.rank))
      .map(({ index }) => index);

    if (indexes.length === 4) {
      return indexes;
    }
  }

  return null;
}

function countStraightCompletions(cards) {
  const values = new Set(cards.map((card) => rankValues[card.rank]));

  if (values.size !== cards.length) {
    return 0;
  }

  return straightSequences.filter((sequence) =>
    [...values].every((value) => sequence.includes(value)),
  ).length;
}

function findFourToStraightFlush(hand) {
  let bestIndexes = null;
  let bestCompletionCount = 0;

  for (let discardedIndex = 0; discardedIndex < 5; discardedIndex += 1) {
    const indexes = [0, 1, 2, 3, 4].filter((index) => index !== discardedIndex);
    const cards = indexes.map((index) => hand[index]);
    const sameSuit = cards.every((card) => card.suit === cards[0].suit);

    if (!sameSuit) {
      continue;
    }

    const completionCount = countStraightCompletions(cards);

    if (completionCount > bestCompletionCount) {
      bestCompletionCount = completionCount;
      bestIndexes = indexes;
    }
  }

  return bestIndexes;
}

function createThreeCardCombinations() {
  const combinations = [];

  for (let first = 0; first < 3; first += 1) {
    for (let second = first + 1; second < 4; second += 1) {
      for (let third = second + 1; third < 5; third += 1) {
        combinations.push([first, second, third]);
      }
    }
  }

  return combinations;
}

function classifyThreeToStraightFlush(cards) {
  const sameSuit = cards.every((card) => card.suit === cards[0].suit);

  if (!sameSuit) {
    return null;
  }

  const ranks = new Set(cards.map((card) => card.rank));

  if (ranks.size !== 3) {
    return null;
  }

  const isAceLow =
    ranks.has('A') &&
    [...ranks].every((rank) => ['A', '2', '3', '4', '5'].includes(rank));

  if (isAceLow) {
    return 'type2';
  }

  const values = cards
    .map((card) => rankValues[card.rank])
    .sort((left, right) => left - right);

  if (values[0] === 2 && values[1] === 3 && values[2] === 4) {
    return 'type2';
  }

  const spread = values[2] - values[0];

  if (spread > 4) {
    return null;
  }

  const gaps = spread - 2;
  const highCardCount = cards.filter((card) => highRanks.has(card.rank)).length;

  if (highCardCount >= gaps) {
    return 'type1';
  }

  if (
    (gaps === 1 && highCardCount === 0) ||
    (gaps === 2 && highCardCount === 1)
  ) {
    return 'type2';
  }

  if (gaps === 2 && highCardCount === 0) {
    return 'type3';
  }

  return null;
}

function findThreeToStraightFlush(hand, type) {
  for (const indexes of createThreeCardCombinations()) {
    const cards = indexes.map((index) => hand[index]);

    if (classifyThreeToStraightFlush(cards) === type) {
      return indexes;
    }
  }

  return null;
}

function findFourToInsideStraight(hand, highCardCount) {
  const candidates = [];

  for (let discardedIndex = 0; discardedIndex < 5; discardedIndex += 1) {
    const indexes = [0, 1, 2, 3, 4].filter((index) => index !== discardedIndex);
    const cards = indexes.map((index) => hand[index]);

    if (countStraightCompletions(cards) !== 1) {
      continue;
    }

    const candidateHighCardCount = cards.filter((card) =>
      highRanks.has(card.rank),
    ).length;

    if (candidateHighCardCount === highCardCount) {
      candidates.push(indexes);
    }
  }

  return candidates.length === 1 ? candidates[0] : null;
}

function findFirstSuitedPair(hand, rankPairs) {
  for (const [firstRank, secondRank] of rankPairs) {
    const indexes = findSuitedPair(hand, firstRank, secondRank);

    if (indexes) {
      return indexes;
    }
  }

  return null;
}

function findFirstUnsuitedPair(hand, rankPairs) {
  for (const [firstRank, secondRank] of rankPairs) {
    const indexes = findUnsuitedPair(hand, firstRank, secondRank);

    if (indexes) {
      return indexes;
    }
  }

  return null;
}

function findSingleRank(hand, rank) {
  const index = hand.findIndex((card) => card.rank === rank);
  return index === -1 ? null : [index];
}

export function getFastStrategyHold(hand) {
  const madeHand = evaluateHand(hand);

  if (madeHand === 'Royal Flush' || madeHand === 'Straight Flush') {
    return {
      heldIndexes: [0, 1, 2, 3, 4],
      rule: madeHand,
    };
  }

  if (madeHand === 'Four of a Kind') {
    return {
      heldIndexes: findIndexesWithCount(hand, 4),
      rule: 'Hold the four of a kind',
    };
  }

  const fourToRoyal = findFourToRoyal(hand);

  if (fourToRoyal) {
    return {
      heldIndexes: fourToRoyal,
      rule: 'Four cards to a Royal Flush',
    };
  }

  if (madeHand === 'Full House' || madeHand === 'Flush') {
    return {
      heldIndexes: [0, 1, 2, 3, 4],
      rule: madeHand,
    };
  }

  if (madeHand === 'Three of a Kind') {
    return {
      heldIndexes: findIndexesWithCount(hand, 3),
      rule: 'Hold the three of a kind',
    };
  }

  if (madeHand === 'Straight') {
    return {
      heldIndexes: [0, 1, 2, 3, 4],
      rule: 'Straight',
    };
  }

  const fourToStraightFlush = findFourToStraightFlush(hand);

  if (fourToStraightFlush) {
    return {
      heldIndexes: fourToStraightFlush,
      rule: 'Four cards to a Straight Flush',
    };
  }

  if (madeHand === 'Two Pair') {
    return {
      heldIndexes: findIndexesWithCount(hand, 2),
      rule: 'Hold both pairs',
    };
  }

  if (madeHand === 'Jacks or Better') {
    return {
      heldIndexes: findIndexesWithCount(hand, 2),
      rule: 'Hold the high pair',
    };
  }

  const threeToRoyal = findThreeToRoyal(hand);
  const fourToFlush = findFourToFlush(hand);

  if (
    threeToRoyal &&
    !isConservativeRoyalFlushConflict(hand, threeToRoyal, fourToFlush)
  ) {
    return {
      heldIndexes: threeToRoyal,
      rule: 'Three cards to a Royal Flush',
    };
  }

  if (
    threeToRoyal &&
    isConservativeRoyalFlushConflict(hand, threeToRoyal, fourToFlush)
  ) {
    return null;
  }

  if (fourToFlush) {
    return {
      heldIndexes: fourToFlush,
      rule: 'Four cards to a Flush',
    };
  }

  const unsuitedTJQK = findUnsuitedTJQK(hand);

  if (unsuitedTJQK) {
    return {
      heldIndexes: unsuitedTJQK,
      rule: 'Unsuited 10-J-Q-K',
    };
  }

  const lowPair = findLowPair(hand);

  if (lowPair) {
    return {
      heldIndexes: lowPair,
      rule: 'Hold the low pair',
    };
  }

  const fourToOutsideStraight = findFourToOutsideStraight(hand);

  if (fourToOutsideStraight) {
    return {
      heldIndexes: fourToOutsideStraight,
      rule: 'Four cards to an outside Straight',
    };
  }

  const straightFlushType1 = findThreeToStraightFlush(hand, 'type1');

  if (straightFlushType1) {
    return {
      heldIndexes: straightFlushType1,
      rule: 'Three cards to a Straight Flush (type 1)',
    };
  }

  const suitedQJ = findSuitedPair(hand, 'Q', 'J');
  const insideStraightFourHigh = findFourToInsideStraight(hand, 4);

  if (suitedQJ && insideStraightFourHigh) {
    return null;
  }

  if (suitedQJ) {
    return {
      heldIndexes: suitedQJ,
      rule: 'Suited Q-J',
    };
  }

  if (insideStraightFourHigh) {
    return {
      heldIndexes: insideStraightFourHigh,
      rule: 'Four cards to an inside Straight with four high cards',
    };
  }

  const suitedKQorKJ = findFirstSuitedPair(hand, [
    ['K', 'Q'],
    ['K', 'J'],
  ]);

  if (suitedKQorKJ) {
    return {
      heldIndexes: suitedKQorKJ,
      rule: 'Suited K-Q or K-J',
    };
  }

  const suitedAceHighPair = findFirstSuitedPair(hand, [
    ['A', 'K'],
    ['A', 'Q'],
    ['A', 'J'],
  ]);

  if (suitedAceHighPair) {
    return {
      heldIndexes: suitedAceHighPair,
      rule: 'Suited A-K, A-Q, or A-J',
    };
  }

  const insideStraightThreeHigh = findFourToInsideStraight(hand, 3);
  const straightFlushType2 = findThreeToStraightFlush(hand, 'type2');

  if (insideStraightThreeHigh && straightFlushType2) {
    return null;
  }

  if (insideStraightThreeHigh) {
    return {
      heldIndexes: insideStraightThreeHigh,
      rule: 'Four cards to an inside Straight with three high cards',
    };
  }

  if (straightFlushType2) {
    return {
      heldIndexes: straightFlushType2,
      rule: 'Three cards to a Straight Flush (type 2)',
    };
  }

  const unsuitedJQK = findRankSet(hand, ['J', 'Q', 'K']);

  if (unsuitedJQK) {
    return {
      heldIndexes: unsuitedJQK,
      rule: 'Unsuited J-Q-K',
    };
  }

  const unsuitedJQ = findUnsuitedPair(hand, 'J', 'Q');

  if (unsuitedJQ) {
    return {
      heldIndexes: unsuitedJQ,
      rule: 'Unsuited J-Q',
    };
  }

  const suitedTJ = findSuitedPair(hand, '10', 'J');
  const unsuitedJK = findUnsuitedPair(hand, 'J', 'K');

  if (suitedTJ && unsuitedJK) {
    return null;
  }

  if (suitedTJ) {
    return {
      heldIndexes: suitedTJ,
      rule: 'Suited 10-J',
    };
  }

  const unsuitedKingHighPair = findFirstUnsuitedPair(hand, [
    ['J', 'K'],
    ['Q', 'K'],
  ]);

  if (unsuitedKingHighPair) {
    return {
      heldIndexes: unsuitedKingHighPair,
      rule: 'Two unsuited high cards, King highest',
    };
  }

  const suitedTQ = findSuitedPair(hand, '10', 'Q');
  const unsuitedQA = findUnsuitedPair(hand, 'Q', 'A');

  if (suitedTQ && unsuitedQA) {
    return null;
  }

  if (suitedTQ) {
    return {
      heldIndexes: suitedTQ,
      rule: 'Suited 10-Q',
    };
  }

  const unsuitedAceHighPair = findFirstUnsuitedPair(hand, [
    ['J', 'A'],
    ['Q', 'A'],
    ['K', 'A'],
  ]);

  if (unsuitedAceHighPair) {
    return {
      heldIndexes: unsuitedAceHighPair,
      rule: 'Two unsuited high cards, Ace highest',
    };
  }

  const jackOnly = findSingleRank(hand, 'J');

  if (jackOnly) {
    return {
      heldIndexes: jackOnly,
      rule: 'Hold the Jack',
    };
  }

  const suitedTK = findSuitedPair(hand, '10', 'K');

  if (suitedTK && hand.some((card) => card.rank === '9')) {
    return null;
  }

  if (suitedTK) {
    return {
      heldIndexes: suitedTK,
      rule: 'Suited 10-K',
    };
  }

  const queenOnly = findSingleRank(hand, 'Q');

  if (queenOnly) {
    return {
      heldIndexes: queenOnly,
      rule: 'Hold the Queen',
    };
  }

  const kingOnly = findSingleRank(hand, 'K');

  if (kingOnly) {
    return {
      heldIndexes: kingOnly,
      rule: 'Hold the King',
    };
  }

  const aceOnly = findSingleRank(hand, 'A');

  if (aceOnly) {
    return {
      heldIndexes: aceOnly,
      rule: 'Hold the Ace',
    };
  }

  const straightFlushType3 = findThreeToStraightFlush(hand, 'type3');

  if (straightFlushType3) {
    return {
      heldIndexes: straightFlushType3,
      rule: 'Three cards to a Straight Flush (type 3)',
    };
  }

  return {
    heldIndexes: [],
    rule: 'Discard all five cards',
  };
}
