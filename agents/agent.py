from actions.recommendations import get_recommendation

class StudentAgent:
    def __init__(self, perception, reasoning, decision):
        self.perception = perception
        self.reasoning = reasoning
        self.decision = decision

    def run(self, input_data: dict):
        features = self.perception.extract_features(input_data)
        predicted_score = self.reasoning.predict(features)
        agent_decision = self.decision.decide(predicted_score)
        recommendation = get_recommendation(agent_decision)

        return {
            "predicted_score": round(predicted_score, 2),
            "decision": agent_decision,
            "recommendation": recommendation
        }
