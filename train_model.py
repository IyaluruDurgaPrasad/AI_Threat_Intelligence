import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# STEP 1: Define Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "datasets" / "cleaned_phishing_emails.csv"

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "phishing_email_model.pkl"


# ==========================================
# STEP 2: Load Cleaned Dataset
# ==========================================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

X = df["email_text"]
y = df["Label"]

print("Total Emails:", len(df))


# ==========================================
# STEP 3: Split Dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Emails:", len(X_train))
print("Testing Emails:", len(X_test))


# ==========================================
# STEP 4: Create ML Pipeline
# ==========================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=10000,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])


# ==========================================
# STEP 5: Train Model
# ==========================================

print("\nTraining phishing detection model...")

model.fit(X_train, y_train)

print("Model training completed!")


# ==========================================
# STEP 6: Evaluate Model
# ==========================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL PERFORMANCE ==========")

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Safe Email", "Phishing Email"]
    )
)

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred))


# ==========================================
# STEP 7: Save Trained Model
# ==========================================

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print("Model Location:", MODEL_PATH)