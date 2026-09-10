const HAND_SIZE = 5;

export function createHoldCombinations() {
  const combinations = [];

  for (let mask = 0; mask < 2 ** HAND_SIZE; mask += 1) {
    const heldIndexes = [];

    for (let cardIndex = 0; cardIndex < HAND_SIZE; cardIndex += 1) {
      const cardIsHeld = (mask & (1 << cardIndex)) !== 0;

      if (cardIsHeld) {
        heldIndexes.push(cardIndex);
      }
    }

    combinations.push(heldIndexes);
  }

  return combinations;
}

