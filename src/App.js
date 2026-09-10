import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { Pressable, Text, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import * as ScreenOrientation from 'expo-screen-orientation';

import PlayingCard from './components/PlayingCard';
import { dealRound } from './game/deck';
import { evaluateHand } from './game/handEvaluator';
import styles from './styles/appStyles';

export default function App() {
  const [round, setRound] = useState(() => dealRound());
  const [heldCards, setHeldCards] = useState([]);
  const [phase, setPhase] = useState('hold');

  const handResult = phase === 'result' ? evaluateHand(round.hand) : null;

  useEffect(() => {
    ScreenOrientation.lockAsync(
      ScreenOrientation.OrientationLock.LANDSCAPE_RIGHT,
    );
  }, []);

  function toggleHold(cardIndex) {
    if (phase !== 'hold') {
      return;
    }

    setHeldCards((currentHeldCards) => {
      if (currentHeldCards.includes(cardIndex)) {
        return currentHeldCards.filter((index) => index !== cardIndex);
      }

      return [...currentHeldCards, cardIndex];
    });
  }

  function drawCards() {
    let nextCardIndex = 0;

    const finalHand = round.hand.map((card, index) => {
      if (heldCards.includes(index)) {
        return card;
      }

      const replacementCard = round.remainingDeck[nextCardIndex];

      nextCardIndex += 1;
      return replacementCard;
    });

    setRound({
      hand: finalHand,
      remainingDeck: round.remainingDeck.slice(nextCardIndex),
    });

    setHeldCards([]);
    setPhase('result');
  }

  function startNewRound() {
    setRound(dealRound());
    setHeldCards([]);
    setPhase('hold');
  }

  function handleMainButton() {
    if (phase === 'hold') {
      drawCards();
    } else {
      startNewRound();
    }
  }

  return (
    <SafeAreaProvider>
      <SafeAreaView
        style={styles.screen}
        edges={['top', 'right', 'bottom', 'left']}>
        <StatusBar hidden />

        <Text style={styles.title}>PEEKER</Text>

        <Text style={styles.subtitle}>
          {phase === 'hold' ? 'Choose cards to hold' : 'Final hand'}
        </Text>

        {handResult && <Text style={styles.handResult}>{handResult}</Text>}

        <View style={styles.cardRow}>
          {round.hand.map((card, index) => (
            <PlayingCard
              key={`${card.id}-${index}`}
              card={card}
              isHeld={heldCards.includes(index)}
              onToggle={() => toggleHold(index)}
            />
          ))}
        </View>

        <Pressable
          style={({ pressed }) => [
            styles.dealButton,
            pressed && styles.dealButtonPressed,
          ]}
          onPress={handleMainButton}>
          <Text style={styles.dealButtonText}>
            {phase === 'hold' ? 'DRAW' : 'DEAL NEW HAND'}
          </Text>
        </Pressable>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
