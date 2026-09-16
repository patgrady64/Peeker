import { forEachCombination, generateCombinations } from '../drawCombinations';

describe('generateCombinations', () => {
    test('walks combinations using a callback', () => {
      const receivedCombinations = [];

      const count = forEachCombination(['A', 'B', 'C'], 2, (combination) => {
        receivedCombinations.push([...combination]);
      });

      expect(count).toBe(3);

      expect(receivedCombinations).toEqual([
        ['A', 'B'],
        ['A', 'C'],
        ['B', 'C'],
      ]);
    });

    test('calls the callback once when choosing zero', () => {
      const receivedCombinations = [];

      const count = forEachCombination(['A', 'B'], 0, (combination) => {
        receivedCombinations.push([...combination]);
      });

      expect(count).toBe(1);
      expect(receivedCombinations).toEqual([[]]);
    });

  test('generates every two-item combination', () => {
    const combinations = Array.from(generateCombinations(['A', 'B', 'C'], 2));

    expect(combinations).toEqual([
      ['A', 'B'],
      ['A', 'C'],
      ['B', 'C'],
    ]);
  });

  test('generates one empty combination when drawing zero', () => {
    const combinations = Array.from(generateCombinations(['A', 'B', 'C'], 0));

    expect(combinations).toEqual([[]]);
  });

  test('generates nothing when requesting too many items', () => {
    const combinations = Array.from(generateCombinations(['A', 'B'], 3));

    expect(combinations).toEqual([]);
  });

  test('produces the correct counts for five items', () => {
    const items = ['A', 'B', 'C', 'D', 'E'];

    const counts = [0, 1, 2, 3, 4, 5].map(
      (chooseCount) =>
        Array.from(generateCombinations(items, chooseCount)).length,
    );

    expect(counts).toEqual([1, 5, 10, 10, 5, 1]);
  });
});

