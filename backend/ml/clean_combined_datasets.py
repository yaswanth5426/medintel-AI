import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(
    "datasets/combined_diabetes_dataset.csv",
    low_memory=False
)

print("=" * 60)
print("Original Shape:", df.shape)

# ==========================================
# Remove Duplicate Rows
# ==========================================

df = df.drop_duplicates()

# ==========================================
# Standardize Gender
# ==========================================

df["Gender"] = (
    df["Gender"]
    .astype(str)
    .str.strip()
    .str.lower()
)

gender_map = {
    "male": 1,
    "m": 1,
    "female": 0,
    "f": 0,
    "0": 0,
    "1": 1,
    "other": 2,
    "nan": np.nan
}

df["Gender"] = df["Gender"].replace(gender_map)
df["Gender"] = pd.to_numeric(df["Gender"], errors="coerce")

# ==========================================
# Standardize Hypertension
# ==========================================

df["Hypertension"] = (
    df["Hypertension"]
    .astype(str)
    .str.strip()
    .str.lower()
)

hypertension_map = {
    "yes": 1,
    "no": 0,
    "1": 1,
    "0": 0,
    "true": 1,
    "false": 0,
    "nan": np.nan
}

df["Hypertension"] = df["Hypertension"].replace(hypertension_map)
df["Hypertension"] = pd.to_numeric(
    df["Hypertension"],
    errors="coerce"
)

# ==========================================
# Standardize Outcome
# ==========================================

df["Outcome"] = (
    df["Outcome"]
    .astype(str)
    .str.strip()
    .str.lower()
)

outcome_map = {
    "positive": 1,
    "negative": 0,
    "1": 1,
    "0": 0,
    "diabetes": 1,
    "no diabetes": 0,
    "yes": 1,
    "no": 0,
    "nan": np.nan
}

df["Outcome"] = df["Outcome"].replace(outcome_map)
df["Outcome"] = pd.to_numeric(
    df["Outcome"],
    errors="coerce"
)

# ==========================================
# Family History
# ==========================================

df["FamilyHistory"] = pd.to_numeric(
    df["FamilyHistory"],
    errors="coerce"
)

# ==========================================
# Smoking
# ==========================================

df["Smoking"] = (
    df["Smoking"]
    .astype(str)
    .str.strip()
    .str.lower()
)

encoder = LabelEncoder()

df["Smoking"] = encoder.fit_transform(df["Smoking"])

# ==========================================
# Convert Remaining Object Columns
# ==========================================

for col in df.columns:

    if df[col].dtype == "object":

        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

# ==========================================
# Fill Missing Values
# ==========================================

for col in df.columns:

    if pd.api.types.is_numeric_dtype(df[col]):

        df[col] = df[col].fillna(df[col].median())

    else:

        df[col] = df[col].fillna(df[col].mode()[0])

# ==========================================
# Remove Impossible Values
# ==========================================

if "Age" in df.columns:
    df = df[df["Age"] > 0]

if "BMI" in df.columns:
    df = df[df["BMI"] > 0]

if "Glucose" in df.columns:
    df = df[df["Glucose"] > 0]

if "BloodPressure" in df.columns:
    df = df[df["BloodPressure"] > 0]

if "HbA1c" in df.columns:
    df = df[df["HbA1c"] > 0]

# ==========================================
# Reset Index
# ==========================================

df = df.reset_index(drop=True)

# ==========================================
# Save Clean Dataset
# ==========================================
print("\nData types BEFORE saving:\n")
print(df.dtypes)
df.to_csv(
    "datasets/clean_diabetes_dataset.csv",
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

print("\nDataset saved as:")
print("datasets/clean_diabetes_dataset.csv")