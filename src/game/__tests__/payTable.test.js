import {
  getPayoutCredits,
  getPayoutMultiplier,
  jacksOrBetterPayTable,
} from '../payTable';

describe('Jacks or Better payout table', () => {
  test('uses the 9/6 Full House and Flush payouts', () => {
    expect(jacksOrBetterPayTable['Full House']).toBe(9);
    expect(jacksOrBetterPayTable.Flush).toBe(6);
  });

  test('pays one unit for Jacks or Better', () => {
    expect(getPayoutMultiplier('Jacks or Better')).toBe(1);
  });

  test('pays nothing for a losing hand', () => {
    expect(getPayoutMultiplier('Nothing')).toBe(0);
  });

  test('safely returns zero for an unknown result', () => {
    expect(getPayoutMultiplier('Unknown Hand')).toBe(0);
  });

  test('uses the standard 250-for-1 Royal payout below max bet', () => {
    expect(getPayoutMultiplier('Royal Flush', 1)).toBe(250);
    expect(getPayoutCredits('Royal Flush', 4)).toBe(1000);
  });

  test('uses the 800-for-1 Royal bonus at five credits', () => {
    expect(getPayoutMultiplier('Royal Flush', 5)).toBe(800);
    expect(getPayoutCredits('Royal Flush', 5)).toBe(4000);
  });

  test('multiplies normal hand payouts by the wager', () => {
    expect(getPayoutCredits('Full House', 5)).toBe(45);
    expect(getPayoutCredits('Jacks or Better', 3)).toBe(3);
  });
});
