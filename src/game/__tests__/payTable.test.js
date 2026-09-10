import { getPayoutMultiplier, jacksOrBetterPayTable } from '../payTable';

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
});
