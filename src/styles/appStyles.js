import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#075E45',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
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
    marginBottom: 8,
  },

  feedbackRow: {
    width: '100%',
    maxWidth: 720,
    minHeight: 52,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },

  feedbackSlot: {
    flex: 1,
    alignItems: 'flex-start',
    justifyContent: 'center',
  },

  feedbackSpacer: {
    flex: 1,
  },

  compactFeedback: {
    minWidth: 260,
    maxWidth: 350,
    borderRadius: 8,
    borderWidth: 2,
    paddingHorizontal: 12,
    paddingVertical: 5,
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
    marginTop: 12,
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
    fontSize: 18,
    fontWeight: 'bold',
  },

  correctFeedback: {
    backgroundColor: '#174f39',
    borderColor: '#65d69e',
  },

  incorrectFeedback: {
    backgroundColor: '#542828',
    borderColor: '#ff8a80',
  },

  feedbackTitle: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
  },

  feedbackText: {
    color: '#ffffff',
    fontSize: 12,
    marginTop: 1,
  },

  errorText: {
    color: '#ff8a80',
    fontSize: 13,
  },

  dealButtonDisabled: {
    opacity: 0.5,
  },
});

export default styles;
