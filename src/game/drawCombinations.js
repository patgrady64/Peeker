export function* generateCombinations(
  items,
  chooseCount,
  startIndex = 0,
  currentCombination = [],
) {
  if (chooseCount === 0) {
    yield [...currentCombination];
    return;
  }

  const lastStartingIndex = items.length - chooseCount;

  for (let index = startIndex; index <= lastStartingIndex; index += 1) {
    currentCombination.push(items[index]);

    yield* generateCombinations(
      items,
      chooseCount - 1,
      index + 1,
      currentCombination,
    );

    currentCombination.pop();
  }
}
