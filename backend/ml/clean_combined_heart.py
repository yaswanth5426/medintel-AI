import pandas as pd
import numpy as np

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(
    "datasets/combined_heart_dataset.csv",
    low_memory=False
)

print("=" * 60)
print("Original Shape:", df.shape)

# ==========================================
# Remove Duplicates
# ==========================================

df = df.drop_duplicates()

# ==========================================
# Convert Numeric Columns
# ==========================================

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# Fill Missing Values
# ==========================================

for col in df.columns:

    if col == "Target":
        continue

    median = df[col].median()

    df[col] = df[col].fillna(median)

# ==========================================
# Remove Impossible Values
# ==========================================

if "Age" in df.columns:
    df = df[df["Age"] > 0]

if "SystolicBP" in df.columns:
    df = df[df["SystolicBP"] > 0]

if "DiastolicBP" in df.columns:
    df = df[df["DiastolicBP"] > 0]

# ==========================================
# Reset Index
# ==========================================

df = df.reset_index(drop=True)

# ==========================================
# Save
# ==========================================

df.to_csv(
    "datasets/clean_heart_dataset.csv",
    index=False
)

# ==========================================
# Summary
# ==========================================

print("\n" + "=" * 60)
print("Cleaning Completed Successfully")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst Five Rows:")
print(df.head())

print("\nSaved:")
print("datasets/clean_heart_dataset.csv")