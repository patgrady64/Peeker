import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#075E45',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingVertical: 8,
  },


  headerRow: {
    width: '100%',
    maxWidth: 760,
    minHeight: 40,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },

  wagerBar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },

  creditReadout: {
    minWidth: 48,
    alignItems: 'center',
  },

  wagerLabel: {
    color: '#A9D8C8',
    fontSize: 8,
    fontWeight: '800',
    letterSpacing: 0.4,
  },

  wagerValue: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '900',
    lineHeight: 18,
  },

  wagerButton: {
    minWidth: 64,
    minHeight: 28,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#B8E2D4',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 7,
  },

  wagerButtonPressed: {
    opacity: 0.65,
  },

  wagerButtonDisabled: {
    opacity: 0.35,
  },

  wagerButtonText: {
    color: '#FFFFFF',
    fontSize: 9,
    fontWeight: '900',
    letterSpacing: 0.25,
  },

  title: {
    color: '#FFFFFF',
    fontSize: 30,
    fontWeight: '900',
    letterSpacing: 5,
  },

  subtitle: {
    color: '#CDEADF',
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 5,
  },

  resultSubtitle: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: '900',
    lineHeight: 28,
    marginBottom: 7,
  },

  winResultText: {
    color: '#FFD54A',
    fontSize: 20,
    fontWeight: '900',
  },

  feedbackRow: {
    width: '100%',
    maxWidth: 760,
    minHeight: 58,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
    transform: [{ translateY: -10 }],
  },

  feedbackSlot: {
    flex: 1,
    alignItems: 'flex-start',
    justifyContent: 'center',
  },

  trainerPanel: {
    flex: 1,
    marginLeft: 14,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#3F806B',
    backgroundColor: 'rgba(0, 0, 0, 0.12)',
    paddingHorizontal: 6,
    paddingVertical: 3,
  },

  trainerStatsRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  trainerStat: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 0,
  },

  trainerStatValue: {
    color: '#FFFFFF',
    fontSize: 13,
    fontWeight: '800',
    lineHeight: 15,
  },

  trainerStatLabel: {
    color: '#A9D8C8',
    fontSize: 7,
    fontWeight: '700',
    letterSpacing: 0.3,
    lineHeight: 9,
  },

  startOverButton: {
    width: 74,
    minHeight: 23,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#B8E2D4',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 5,
  },

  startOverButtonPressed: {
    opacity: 0.65,
  },

  startOverButtonDisabled: {
    opacity: 0.4,
  },

  startOverButtonText: {
    color: '#FFFFFF',
    fontSize: 8,
    fontWeight: '800',
    letterSpacing: 0.3,
  },

  startOverSpacer: {
    width: 74,
  },

  compactFeedback: {
    minWidth: 280,
    maxWidth: 375,
    borderRadius: 8,
    borderWidth: 2,
    paddingHorizontal: 10,
    paddingVertical: 4,
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


  cardBack: {
    borderColor: '#B8E2D4',
    backgroundColor: '#0B4D3A',
  },

  cardBackText: {
    color: '#B8E2D4',
    fontSize: 18,
    fontWeight: '900',
    letterSpacing: 2,
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
    marginTop: 9,
    paddingHorizontal: 28,
    paddingVertical: 11,
  },

  dealButtonPressed: {
    opacity: 0.7,
  },

  dealButtonText: {
    color: '#17211d',
    fontSize: 16,
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
    fontSize: 13,
    fontWeight: 'bold',
  },

  feedbackText: {
    color: '#ffffff',
    fontSize: 11,
    marginTop: 1,
  },

  feedbackEvText: {
    color: '#FFD9D6',
    fontSize: 9,
    fontWeight: '700',
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
