const ranks = [
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '10',
  'J',
  'Q',
  'K',
  'A',
];

const suits = [
  {
    name: 'spades',
    symbol: '♠',
    color: 'black',
  },
  {
    name: 'hearts',
    symbol: '♥',
    color: 'red',
  },
  {
    name: 'diamonds',
    symbol: '♦',
    color: 'red',
  },
  {
    name: 'clubs',
    symbol: '♣',
    color: 'black',
  },
];

export function createDeck() {
  return suits.flatMap((suit) =>
    ranks.map((rank) => ({
      id: `${rank}-${suit.name}`,
      rank,
      suit: suit.name,
      symbol: suit.symbol,
      color: suit.color,
    })),
  );
}

export function shuffleDeck(deck) {
  const shuffledDeck = [...deck];

  for (let index = shuffledDeck.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));

    [shuffledDeck[index], shuffledDeck[randomIndex]] = [
      shuffledDeck[randomIndex],
      shuffledDeck[index],
    ];
  }

  return shuffledDeck;
}

export function dealRound() {
  const shuffledDeck = shuffleDeck(createDeck());

  return {
    hand: shuffledDeck.slice(0, 5),
    remainingDeck: shuffledDeck.slice(5),
  };
}
