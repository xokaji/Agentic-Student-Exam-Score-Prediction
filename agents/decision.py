class Decision:
    def decide(self, predicted_score: float):
        if predicted_score < 50:
            return "INTENSIVE_SUPPORT"
        elif predicted_score < 70:
            return "IMPROVEMENT_PLAN"
        else:
            return "ADVANCED_TRACK"
