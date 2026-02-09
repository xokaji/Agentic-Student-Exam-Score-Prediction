from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from pathlib import Path
from src.model import train_model, load_model, save_model
from src.data_loader import load_data
from agents.decision import Decision
from actions.recommendations import get_recommendation

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the decision agent
decision_agent = Decision()


def validate_input(payload):
    required = ["study_hours", "attendance", "sleep_hours"]
    for key in required:
        if key not in payload:
            return False, f"Missing field: {key}"
        if payload[key] is None:
            return False, f"Field '{key}' cannot be null"

    try:
        study = float(payload["study_hours"])
        attendance = float(payload["attendance"])
        sleep = float(payload["sleep_hours"])
    except (TypeError, ValueError):
        return False, "All fields must be numeric"

    if study < 0 or sleep < 0:
        return False, "Study hours and sleep hours must be >= 0"
    if attendance < 0 or attendance > 100:
        return False, "Attendance must be between 0 and 100"
    if study + sleep > 24:
        return False, "Study hours + sleep hours must be <= 24"

    return True, (study, attendance, sleep)

# Load saved model (or train and save if missing)
model_path = Path("models/artifacts/linear_regression.joblib")
if model_path.exists():
    model = load_model(model_path)
else:
    data = load_data("data/raw/student_scores.csv")
    X = data[["study_hours", "attendance", "sleep_hours"]]
    y = data["exam_score"]
    model = train_model(X, y)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    save_model(model, model_path)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or {}
    ok, result = validate_input(data)
    if not ok:
        return jsonify({"error": result}), 400

    study, attendance, sleep = result
    input_df = pd.DataFrame([{
        "study_hours": study,
        "attendance": attendance,
        "sleep_hours": sleep
    }])
    prediction = model.predict(input_df)[0]
    prediction = max(0, min(100, prediction))
    prediction = max(0, min(100, prediction))
    prediction = round(prediction, 2)
    
    decision = decision_agent.decide(prediction)
    recommendation = get_recommendation(decision)

    return jsonify({
        "predicted_score": float(prediction),
        "agent_decision": decision,
        "recommendation": recommendation
    })


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
