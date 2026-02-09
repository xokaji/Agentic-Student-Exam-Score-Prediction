from pathlib import Path

from src.data_loader import load_data
from src.model import train_model, save_model


def main():
    data = load_data("data/raw/student_scores.csv")
    X = data[["study_hours", "attendance", "sleep_hours"]]
    y = data["exam_score"]

    model = train_model(X, y)

    artifacts_dir = Path("models/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    model_path = artifacts_dir / "linear_regression.joblib"
    save_model(model, model_path)

    print(f"Saved model to: {model_path}")


if __name__ == "__main__":
    main()
