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

export function forEachCombination(items, chooseCount, callback) {
  if (chooseCount < 0 || chooseCount > items.length) {
    return 0;
  }

  const combination = new Array(chooseCount);
  let combinationCount = 0;

  function visit(startIndex, depth) {
    if (depth === chooseCount) {
      callback(combination);
      combinationCount += 1;
      return;
    }

    const cardsStillNeeded = chooseCount - depth;
    const finalStartIndex = items.length - cardsStillNeeded;

    for (let index = startIndex; index <= finalStartIndex; index += 1) {
      combination[depth] = items[index];
      visit(index + 1, depth + 1);
    }
  }

  visit(0, 0);

  return combinationCount;
}
