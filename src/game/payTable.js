export const MIN_WAGER = 1;
export const MAX_WAGER = 5;

export const jacksOrBetterPayTable = {
  'Royal Flush': 800,
  'Straight Flush': 50,
  'Four of a Kind': 25,
  'Full House': 9,
  Flush: 6,
  Straight: 4,
  'Three of a Kind': 3,
  'Two Pair': 2,
  'Jacks or Better': 1,
  Nothing: 0,
};

export function normalizeWager(wager) {
  if (!Number.isFinite(wager)) {
    return MAX_WAGER;
  }

  return Math.min(MAX_WAGER, Math.max(MIN_WAGER, Math.trunc(wager)));
}

export function getPayoutMultiplier(handResult, wager = MAX_WAGER) {
  if (handResult === 'Royal Flush' && normalizeWager(wager) < MAX_WAGER) {
    return 250;
  }

  return jacksOrBetterPayTable[handResult] ?? 0;
}

export function getPayoutCredits(handResult, wager = MAX_WAGER) {
  const normalizedWager = normalizeWager(wager);
  return getPayoutMultiplier(handResult, normalizedWager) * normalizedWager;
}
