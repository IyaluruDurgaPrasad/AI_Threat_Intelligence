import joblib
from pathlib import Path

from application.llm_analyzer import analyze_threat


# Project root directory
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR=Path(__file__).resolve().parents[2]

# Trained ML model path
MODEL_PATH = BASE_DIR / "models" / "phishing_email_model.pkl"

# Load trained model once with fallback handling
try:
    ml_model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Error loading model from {MODEL_PATH}: {e}")
    ml_model = None


def hybrid_threat_analysis(email_text):

    # Validate model availability
    if ml_model is None:
        return {
            "error": "Machine learning model could not be loaded. Please ensure models/phishing_email_model.pkl exists."
        }

    # Validate input
    if not isinstance(email_text, str) or not email_text.strip():
        return {
            "error": "Email text cannot be empty."
        }

    # Step 1: Machine Learning Prediction
    prediction = int(ml_model.predict([email_text])[0])

    # Step 2: Prediction Probabilities
    probabilities = ml_model.predict_proba([email_text])[0]

    safe_probability = float(probabilities[0] * 100)
    phishing_probability = float(probabilities[1] * 100)

    # Step 3: Classification
    if prediction == 1:
        prediction_label = "Phishing Email"
    else:
        prediction_label = "Safe Email"

    # Step 4: LLM Threat Analysis
    llm_report = analyze_threat(email_text)

    # Step 5: Combine Results
    result = {
        "prediction": prediction_label,
        "safe_probability": round(safe_probability, 2),
        "phishing_probability": round(phishing_probability, 2),
        "llm_analysis": llm_report
    }

    return result