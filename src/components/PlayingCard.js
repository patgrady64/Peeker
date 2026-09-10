import { Pressable, Text } from 'react-native';

import styles from '../styles/appStyles';

export default function PlayingCard({ card, isHeld, onToggle }) {
  const cardTextStyle = [
    styles.cardText,
    card.color === 'red' && styles.redCardText,
  ];

  return (
    <Pressable
      style={[styles.card, isHeld && styles.heldCard]}
      onPress={onToggle}>
      <Text style={cardTextStyle}>
        {card.rank}
        {card.symbol}
      </Text>

      <Text style={styles.holdText}>{isHeld ? 'HELD' : 'TAP TO HOLD'}</Text>
    </Pressable>
  );
}
