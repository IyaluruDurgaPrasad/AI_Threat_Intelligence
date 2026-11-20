import joblib
from pathlib import Path

# Step 1: Load trained model
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "phishing_email_model.pkl"

model = joblib.load(MODEL_PATH)

print("Phishing Email Detection System")
print("=" * 40)

# Step 2: Get email text from user
email_text = input("\nEnter email text: ")

if not email_text.strip():
    print("Error: Email text cannot be empty!")
    exit()

# Step 3: Predict email category
prediction = model.predict([email_text])[0]

# Step 4: Get prediction probabilities
probabilities = model.predict_proba([email_text])[0]

print('Probabilities :',probabilities)

safe_probability = probabilities[0] * 100
phishing_probability = probabilities[1] * 100

# Step 5: Display results
print("\n========== PREDICTION RESULT ==========")

if prediction == 1:
    print("Prediction: PHISHING EMAIL")
    print("Threat Level: Suspicious")
else:
    print("Prediction: SAFE EMAIL")
    print("Threat Level: Low")

print(f"Safe Email Probability: {safe_probability:.2f}%")
print(f"Phishing Email Probability: {phishing_probability:.2f}%")

print("\nNote: Model probabilities are estimates, not guaranteed risk scores.")