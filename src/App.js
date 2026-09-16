import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { Pressable, Text, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import * as ScreenOrientation from 'expo-screen-orientation';

import PlayingCard from './components/PlayingCard';
import { dealRound } from './game/deck';
import { calculateHoldExpectedValue } from './game/expectedValue';
import { evaluateHand, evaluateHandValue } from './game/handEvaluator';
import {
  getPayoutCredits,
  MAX_WAGER,
  MIN_WAGER,
} from './game/payTable';
import { analyzeBestHold } from './game/strategyAnalysis';
import styles from './styles/appStyles';

const STARTING_CREDITS = 100;
const DEFAULT_WAGER = MAX_WAGER;

const EMPTY_SESSION_STATS = {
  hands: 0,
  correct: 0,
  mistakes: 0,
  streak: 0,
  bestStreak: 0,
};

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

function formatExpectedValue(expectedValue) {
  return expectedValue.toFixed(3);
}

export default function App() {
  const [round, setRound] = useState(() => dealRound());
  const [heldCards, setHeldCards] = useState([]);
  const [phase, setPhase] = useState('ready');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [trainingFeedback, setTrainingFeedback] = useState(null);
  const [sessionStats, setSessionStats] = useState(EMPTY_SESSION_STATS);
  const [credits, setCredits] = useState(STARTING_CREDITS);
  const [wager, setWager] = useState(DEFAULT_WAGER);
  const [currentWager, setCurrentWager] = useState(0);
  const [lastWin, setLastWin] = useState(0);

  const handValue = phase === 'result' ? evaluateHandValue(round.hand) : null;
  const wagerControlsEnabled = phase !== 'hold' && !isAnalyzing;
  const canDeal = credits >= wager && credits > 0;

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

  function cycleWager() {
    if (!wagerControlsEnabled) {
      return;
    }

    const maxAffordableWager =
      credits > 0 ? Math.min(MAX_WAGER, credits) : MIN_WAGER;

    setWager((currentWagerValue) =>
      currentWagerValue >= maxAffordableWager
        ? MIN_WAGER
        : currentWagerValue + 1,
    );
  }

  function selectMaxWager() {
    if (!wagerControlsEnabled) {
      return;
    }

    setWager(credits > 0 ? Math.min(MAX_WAGER, credits) : MAX_WAGER);
  }

  function dealNewHand() {
    if (isAnalyzing || !canDeal) {
      return;
    }

    setCredits((currentCredits) => currentCredits - wager);
    setCurrentWager(wager);
    setLastWin(0);
    setRound(dealRound());
    setHeldCards([]);
    setPhase('hold');
    setTrainingFeedback(null);
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

    const handResult = evaluateHand(finalHand);
    const payout = getPayoutCredits(handResult, currentWager);

    setRound({
      hand: finalHand,
      remainingDeck: round.remainingDeck.slice(nextCardIndex),
    });
    setCredits((currentCredits) => currentCredits + payout);
    setLastWin(payout);
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

        const analysis = analyzeBestHold(
          openingHand,
          round.remainingDeck,
          currentWager,
        );
        const { bestHolds } = analysis;
        const bestHold = bestHolds[0];

        const playerWasCorrect = bestHolds.some((candidateHold) =>
          holdsMatch(heldCards, candidateHold.heldIndexes),
        );

        const playerExpectedValue = playerWasCorrect
          ? bestHold.expectedValue
          : calculateHoldExpectedValue(
              openingHand,
              round.remainingDeck,
              heldCards,
              currentWager,
            ).expectedValue;

        const calculationTime = Date.now() - startTime;
        const recommendedHold = bestHold.heldIndexes;

        setSessionStats((currentStats) => {
          const nextStreak = playerWasCorrect ? currentStats.streak + 1 : 0;

          return {
            hands: currentStats.hands + 1,
            correct: currentStats.correct + (playerWasCorrect ? 1 : 0),
            mistakes: currentStats.mistakes + (playerWasCorrect ? 0 : 1),
            streak: nextStreak,
            bestStreak: Math.max(currentStats.bestStreak, nextStreak),
          };
        });

        setTrainingFeedback({
          isCorrect: playerWasCorrect,
          recommendation: describeHold(openingHand, recommendedHold),
          playerExpectedValue: playerExpectedValue * currentWager,
          bestExpectedValue: bestHold.expectedValue * currentWager,
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

  function startOver() {
    if (isAnalyzing) {
      return;
    }

    setSessionStats({ ...EMPTY_SESSION_STATS });
    setCredits(STARTING_CREDITS);
    setWager(DEFAULT_WAGER);
    setCurrentWager(0);
    setLastWin(0);
    setRound(dealRound());
    setHeldCards([]);
    setPhase('ready');
    setTrainingFeedback(null);
  }

  function handleMainButton() {
    if (isAnalyzing) {
      return;
    }

    if (phase === 'hold') {
      analyzeAndDraw();
    } else {
      dealNewHand();
    }
  }

  const mainButtonDisabled =
    isAnalyzing || (phase !== 'hold' && !canDeal);

  return (
    <SafeAreaProvider>
      <SafeAreaView
        style={styles.screen}
        edges={['top', 'right', 'bottom', 'left']}>
        <StatusBar hidden />

        <View style={styles.headerRow}>
          <Text style={styles.title}>PEEKER</Text>

          <View style={styles.wagerBar}>
          <View style={styles.creditReadout}>
            <Text style={styles.wagerLabel}>CREDITS</Text>
            <Text style={styles.wagerValue}>{credits}</Text>
          </View>

          <View style={styles.creditReadout}>
            <Text style={styles.wagerLabel}>BET</Text>
            <Text style={styles.wagerValue}>
              {phase === 'hold' ? currentWager : wager}
            </Text>
          </View>

          <View style={styles.creditReadout}>
            <Text style={styles.wagerLabel}>WIN</Text>
            <Text style={styles.wagerValue}>{lastWin}</Text>
          </View>

          <Pressable
            disabled={!wagerControlsEnabled}
            style={({ pressed }) => [
              styles.wagerButton,
              pressed && styles.wagerButtonPressed,
              !wagerControlsEnabled && styles.wagerButtonDisabled,
            ]}
            onPress={cycleWager}>
            <Text style={styles.wagerButtonText}>BET ONE</Text>
          </Pressable>

          <Pressable
            disabled={!wagerControlsEnabled}
            style={({ pressed }) => [
              styles.wagerButton,
              pressed && styles.wagerButtonPressed,
              !wagerControlsEnabled && styles.wagerButtonDisabled,
            ]}
            onPress={selectMaxWager}>
            <Text style={styles.wagerButtonText}>MAX BET</Text>
          </Pressable>
          </View>

        </View>
        <Text
          style={[
            styles.subtitle,
            phase === 'result' && styles.resultSubtitle,
          ]}>
          {isAnalyzing
            ? 'Finding the best hold...'
            : phase === 'ready'
              ? 'Choose your wager and deal'
              : phase === 'hold'
                ? 'Choose cards to hold'
                : handValue}
          {phase === 'result' && lastWin > 0 && (
            <Text style={styles.winResultText}>
              {'  •  '}YOU WON {lastWin} {lastWin === 1 ? 'CREDIT' : 'CREDITS'}
            </Text>
          )}
        </Text>

        <View style={styles.feedbackRow}>
          <View style={styles.feedbackSlot}>
            {trainingFeedback && !trainingFeedback.error && (
              <View
                style={[
                  styles.compactFeedback,
                  trainingFeedback.isCorrect
                    ? styles.correctFeedback
                    : styles.incorrectFeedback,
                ]}>
                <Text style={styles.feedbackTitle}>
                  {trainingFeedback.isCorrect
                    ? 'CORRECT PLAY'
                    : 'BETTER PLAY AVAILABLE'}
                </Text>

                <Text style={styles.feedbackText} numberOfLines={1}>
                  {trainingFeedback.recommendation}
                </Text>

                <Text style={styles.feedbackEvText} numberOfLines={1}>
                  {trainingFeedback.isCorrect ? (
                    <>
                      EV: {formatExpectedValue(trainingFeedback.bestExpectedValue)}
                    </>
                  ) : (
                    <>
                      YOUR EV: {formatExpectedValue(trainingFeedback.playerExpectedValue)}{' '}
                      | BETTER PLAY EV:{' '}
                      {formatExpectedValue(trainingFeedback.bestExpectedValue)}
                    </>
                  )}
                </Text>
              </View>
            )}

            {trainingFeedback?.error && (
              <Text style={styles.errorText} numberOfLines={1}>
                Analysis error: {trainingFeedback.error}
              </Text>
            )}
          </View>

          <View style={styles.trainerPanel}>
            <View style={styles.trainerStatsRow}>
              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>{sessionStats.hands}</Text>
                <Text style={styles.trainerStatLabel}>HANDS</Text>
              </View>

              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>{sessionStats.correct}</Text>
                <Text style={styles.trainerStatLabel}>CORRECT</Text>
              </View>

              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>{sessionStats.mistakes}</Text>
                <Text style={styles.trainerStatLabel}>MISTAKES</Text>
              </View>

              <Pressable
                disabled={isAnalyzing}
                style={({ pressed }) => [
                  styles.startOverButton,
                  pressed && styles.startOverButtonPressed,
                  isAnalyzing && styles.startOverButtonDisabled,
                ]}
                onPress={startOver}>
                <Text style={styles.startOverButtonText}>START OVER</Text>
              </Pressable>
            </View>

            <View style={styles.trainerStatsRow}>
              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>
                  {sessionStats.hands === 0
                    ? '--'
                    : `${Math.round(
                        (sessionStats.correct / sessionStats.hands) * 100,
                      )}%`}
                </Text>
                <Text style={styles.trainerStatLabel}>ACCURACY</Text>
              </View>

              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>{sessionStats.streak}</Text>
                <Text style={styles.trainerStatLabel}>STREAK</Text>
              </View>

              <View style={styles.trainerStat}>
                <Text style={styles.trainerStatValue}>
                  {sessionStats.bestStreak}
                </Text>
                <Text style={styles.trainerStatLabel}>BEST</Text>
              </View>

              <View style={styles.startOverSpacer} />
            </View>
          </View>
        </View>

        <View style={styles.cardRow}>
          {round.hand.map((card, index) => (
            <PlayingCard
              key={`${card.id}-${index}`}
              card={card}
              isHeld={heldCards.includes(index)}
              isFaceDown={phase === 'ready'}
              onToggle={() => toggleHold(index)}
            />
          ))}
        </View>

        <Pressable
          disabled={mainButtonDisabled}
          style={({ pressed }) => [
            styles.dealButton,
            pressed && styles.dealButtonPressed,
            mainButtonDisabled && styles.dealButtonDisabled,
          ]}
          onPress={handleMainButton}>
          <Text style={styles.dealButtonText}>
            {isAnalyzing
              ? 'ANALYZING...'
              : phase === 'hold'
                ? 'DRAW'
                : canDeal
                  ? 'DEAL'
                  : 'NOT ENOUGH CREDITS'}
          </Text>
        </Pressable>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
