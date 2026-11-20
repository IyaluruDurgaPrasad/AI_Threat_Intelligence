import pandas as pd
from pathlib import Path

# Dataset folder
dataset_folder = Path("datasets")

# Find CSV files
csv_files = list(dataset_folder.glob("*.csv"))

if not csv_files:
    print("No CSV dataset found!")
    exit()

# Read dataset
dataset_path = csv_files[0]

print("Dataset:", dataset_path.name)

df = pd.read_csv(dataset_path)

# Dataset information
print("\n========== DATASET INFORMATION ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nColumn Data Types:")
print(df.dtypes)

# Check label distribution
print("\n========== LABEL DISTRIBUTION ==========")

possible_labels = [
    "Email Type",
    "Email_Type",
    "label",
    "Label",
    "type",
    "Type"
]

for column in possible_labels:
    if column in df.columns:
        print(df[column].value_counts(dropna=False))
        break
else:
    print("Label column not identified automatically.")