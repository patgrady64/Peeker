import { createHoldCombinations } from '../holdCombinations';

describe('createHoldCombinations', () => {
  const combinations = createHoldCombinations();

  test('creates all 32 possible holds', () => {
    expect(combinations).toHaveLength(32);
  });

  test('includes discarding every card', () => {
    expect(combinations).toContainEqual([]);
  });

  test('includes holding every card', () => {
    expect(combinations).toContainEqual([0, 1, 2, 3, 4]);
  });

  test('does not create duplicate holds', () => {
    const serializedCombinations = combinations.map((combination) =>
      JSON.stringify(combination),
    );

    const uniqueCombinations = new Set(serializedCombinations);

    expect(uniqueCombinations.size).toBe(32);
  });

  test('includes each card in exactly 16 holds', () => {
    for (let cardIndex = 0; cardIndex < 5; cardIndex += 1) {
      const appearances = combinations.filter((combination) =>
        combination.includes(cardIndex),
      ).length;

      expect(appearances).toBe(16);
    }
  });
});
