import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { Pressable, Text, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import * as ScreenOrientation from 'expo-screen-orientation';

import PlayingCard from './components/PlayingCard';
import { dealRound } from './game/deck';
import { evaluateHand } from './game/handEvaluator';
import { analyzeBestHold } from './game/strategyAnalysis';
import styles from './styles/appStyles';

function holdsMatch(firstHold, secondHold) {
  if (firstHold.length !== secondHold.length) {
    return false;
  }

  const sortedFirst = [...firstHold].sort((first, second) => first - second);

  const sortedSecond = [...secondHold].sort((first, second) => first - second);

  return sortedFirst.every(
    (cardIndex, index) => cardIndex === sortedSecond[index],
  );
}

function describeHold(hand, heldIndexes) {
  if (heldIndexes.length === 0) {
    return 'Discard all five cards';
  }

  if (heldIndexes.length === 5) {
    return 'Hold all five cards';
  }

  const cards = heldIndexes.map((index) => {
    const card = hand[index];
    return `${card.rank}${card.symbol}`;
  });

  return `Hold ${cards.join(', ')}`;
}

export default function App() {
  const [round, setRound] = useState(() => dealRound());
  const [heldCards, setHeldCards] = useState([]);
  const [phase, setPhase] = useState('hold');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [trainingFeedback, setTrainingFeedback] = useState(null);

  const handResult = phase === 'result' ? evaluateHand(round.hand) : null;

  useEffect(() => {
    ScreenOrientation.lockAsync(
      ScreenOrientation.OrientationLock.LANDSCAPE_RIGHT,
    );
  }, []);

  function toggleHold(cardIndex) {
    if (phase !== 'hold' || isAnalyzing) {
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

  function analyzeAndDraw() {
    setIsAnalyzing(true);
    setTrainingFeedback(null);

    setTimeout(() => {
      try {
        const openingHand = round.hand;
        const startTime = Date.now();

        const analysis = analyzeBestHold(openingHand, round.remainingDeck);
        const { bestHolds } = analysis;

        const calculationTime = Date.now() - startTime;

        const playerWasCorrect = bestHolds.some((bestHold) =>
          holdsMatch(heldCards, bestHold.heldIndexes),
        );

        const recommendedHold = bestHolds[0].heldIndexes;

        setTrainingFeedback({
          isCorrect: playerWasCorrect,
          recommendation: describeHold(openingHand, recommendedHold),
          expectedValue: bestHolds[0].expectedValue,
          calculationTime,
          strategyRule: analysis.rule,
        });

        drawCards();
      } catch (error) {
        setTrainingFeedback({
          error: error.message,
        });
      } finally {
        setIsAnalyzing(false);
      }
    }, 50);
  }

  function startNewRound() {
    setRound(dealRound());
    setHeldCards([]);
    setPhase('hold');
    setTrainingFeedback(null);
  }

  function handleMainButton() {
    if (isAnalyzing) {
      return;
    }

    if (phase === 'hold') {
      analyzeAndDraw();
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
          {isAnalyzing
            ? 'Finding the best hold...'
            : phase === 'hold'
              ? 'Choose cards to hold'
              : 'Final hand'}
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

        {trainingFeedback && !trainingFeedback.error && (
          <View
            style={[
              styles.feedbackPanel,
              trainingFeedback.isCorrect
                ? styles.correctFeedback
                : styles.incorrectFeedback,
            ]}>
            <Text style={styles.feedbackTitle}>
              {trainingFeedback.isCorrect
                ? 'CORRECT PLAY'
                : 'BETTER PLAY AVAILABLE'}
            </Text>

            <Text style={styles.feedbackText}>
              {trainingFeedback.recommendation}
            </Text>

            <Text style={styles.feedbackDetails}>
              Expected value: {trainingFeedback.expectedValue.toFixed(4)}
              {'  •  '}
              Analysis: {trainingFeedback.calculationTime} ms
            </Text>

            {trainingFeedback.strategyRule && (
              <Text style={styles.feedbackDetails}>
                Strategy: {trainingFeedback.strategyRule}
              </Text>
            )}
          </View>
        )}

        {trainingFeedback?.error && (
          <Text style={styles.errorText}>
            Analysis error: {trainingFeedback.error}
          </Text>
        )}

        <Pressable
          disabled={isAnalyzing}
          style={({ pressed }) => [
            styles.dealButton,
            pressed && styles.dealButtonPressed,
            isAnalyzing && styles.dealButtonDisabled,
          ]}
          onPress={handleMainButton}>
          <Text style={styles.dealButtonText}>
            {isAnalyzing
              ? 'ANALYZING...'
              : phase === 'hold'
                ? 'DRAW'
                : 'DEAL NEW HAND'}
          </Text>
        </Pressable>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
