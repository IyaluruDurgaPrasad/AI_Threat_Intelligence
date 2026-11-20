import pandas as pd
from pathlib import Path

# Dataset paths
DATASET_DIR = Path(__file__).resolve().parent / "datasets"

input_path = DATASET_DIR / "Phishing_Email.csv"
output_path = DATASET_DIR / "cleaned_phishing_emails.csv"

# Load dataset
df = pd.read_csv(input_path)

print("Original Dataset Shape:", df.shape)

# Select required columns
df = df[["Email Text", "Email Type"]].copy()

# Remove missing values
df.dropna(subset=["Email Text", "Email Type"], inplace=True)

# Remove empty emails
df["Email Text"] = df["Email Text"].astype(str).str.strip()
df = df[df["Email Text"] != ""]

# Remove duplicate emails
df.drop_duplicates(subset=["Email Text"], inplace=True)

# Convert labels into numbers
label_mapping = {
    "Safe Email": 0,
    "Phishing Email": 1
}

df["Label"] = df["Email Type"].map(label_mapping)

# Check unknown labels
if df["Label"].isnull().any():
    raise ValueError("Unknown email labels found in dataset!")

# Rename columns
df = df.rename(columns={
    "Email Text": "email_text"
})

# Keep only required columns
df = df[["email_text", "Label"]]

# Convert label to integer
df["Label"] = df["Label"].astype(int)

# Save cleaned dataset
df.to_csv(output_path, index=False)

print("\n========== PREPROCESSING COMPLETED ==========")

print("\nCleaned Dataset Shape:")
print(df.shape)

print("\nLabel Distribution:")
print(df["Label"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst Five Records:")
print(df.head())

print("\nCleaned Dataset Saved Successfully!")
print("Location:", output_path)
