from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from src.model import train_model
from src.data_loader import load_data
from agents.decision import Decision
from actions.recommendations import get_recommendation

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the decision agent
decision_agent = Decision()

# Load and train once
data = load_data("data/raw/student_scores.csv")
X = data[["study_hours", "attendance", "sleep_hours"]]
y = data["exam_score"]
model = train_model(X, y)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]

    decision = decision_agent.decide(prediction)
    recommendation = get_recommendation(decision)

    return jsonify({
        "predicted_score": float(prediction),
        "agent_decision": decision,
        "recommendation": recommendation
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
