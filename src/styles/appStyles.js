import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#075E45',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },

  title: {
    color: '#FFFFFF',
    fontSize: 34,
    fontWeight: '900',
    letterSpacing: 5,
  },

  subtitle: {
    color: '#CDEADF',
    fontSize: 15,
    marginBottom: 24,
  },

  cardRow: {
    flexDirection: 'row',
    gap: 14,
  },

  card: {
    width: 125,
    height: 170,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    borderWidth: 4,
    borderColor: '#D9D9D9',
    alignItems: 'center',
    justifyContent: 'center',
  },

  heldCard: {
    borderColor: '#FFD54A',
    transform: [{ translateY: -10 }],
  },

  cardText: {
    color: '#151515',
    fontSize: 40,
    fontWeight: '800',
  },

  holdText: {
    color: '#075E45',
    fontSize: 11,
    fontWeight: '800',
    marginTop: 22,
  },

  instructions: {
    color: '#FFFFFF',
    fontSize: 15,
    marginTop: 22,
  },

  redCardText: {
    color: '#c62828',
  },

  dealButton: {
    backgroundColor: '#ffd54a',
    borderRadius: 8,
    marginTop: 20,
    paddingHorizontal: 28,
    paddingVertical: 12,
  },

  dealButtonPressed: {
    opacity: 0.7,
  },

  dealButtonText: {
    color: '#17211d',
    fontSize: 16,
    fontWeight: 'bold',
  },

  handResult: {
    color: '#ffd54a',
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 12,
  },
});

export default styles;
