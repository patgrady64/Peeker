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

export function getPayoutMultiplier(handResult) {
  return jacksOrBetterPayTable[handResult] ?? 0;
}
