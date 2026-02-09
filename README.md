# Student Exam Score Prediction

Beginner-friendly ML project that predicts a student's exam score from
study hours, attendance, and sleep hours, then returns a simple decision
and recommendation.

## What This Project Does
1. Trains a Linear Regression model from a CSV dataset.
2. Saves the trained model to disk.
3. Serves predictions via a Flask API.
4. Adds a decision label + recommendation based on the predicted score.

## Inputs and Output
Inputs (per student):
- `study_hours` (0-24)
- `attendance` (0-100)
- `sleep_hours` (0-24)

Output:
- `predicted_score` (0-100)
- `agent_decision` (INTENSIVE_SUPPORT | IMPROVEMENT_PLAN | ADVANCED_TRACK)
- `recommendation` (human-readable advice)

## Folder Structure (Important Parts)
- `data/raw/student_scores.csv`  
  Training data used by the model.
- `src/data_loader.py`  
  Reads the CSV into a pandas DataFrame.
- `src/model.py`  
  Trains, saves, and loads the Linear Regression model.
- `models/train_and_save.py`  
  Trains on the full dataset and saves the model artifact.
- `models/artifacts/linear_regression.joblib`  
  Saved trained model (generated after training).
- `app.py`  
  Flask API that loads the saved model and serves predictions.
- `agents/decision.py`  
  Converts predicted score into a decision label.
- `actions/recommendations.py`  
  Maps decision label to recommendation text.
- `templates/index.html`  
  Simple web UI to input features and get predictions.

## Setup
1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Train and Save the Model
Run this once after you update the CSV:
```
python models/train_and_save.py
```
This writes the model file to `models/artifacts/linear_regression.joblib`.

## Run the API
```
python app.py
```
Server runs on port `8000`.

### Example API Request (PowerShell)
```
$body = @{
  study_hours = 6
  attendance = 80
  sleep_hours = 7
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
  -Method Post -Body $body -ContentType "application/json"
```

## Data Validation Rules
The API rejects invalid inputs:
- `study_hours >= 0`
- `sleep_hours >= 0`
- `attendance` between 0 and 100
- `study_hours + sleep_hours <= 24`

Predictions are clamped to the 0-100 range.

## Notebook (Exploration)
The notebook `notebooks/01_exploration.ipynb` is for:
- loading and inspecting the data
- plotting relationships
- training/testing and evaluating MSE
- comparing baseline models

## How the System Works (Simple Flow)
1. You submit input features.
2. Flask loads the saved model (or trains and saves if missing).
3. Model predicts an exam score.
4. Decision logic assigns a label based on score.
5. Recommendation text is returned with the prediction.

## Troubleshooting
- If `/predict` fails, make sure the Flask app is running on port `8000`.
- If results look wrong, retrain the model after updating the CSV:
  ```
  python models/train_and_save.py
  ```
