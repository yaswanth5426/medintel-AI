import pandas as pd

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(
    "datasets/combined_kidney_dataset.csv",
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

numeric_columns = [
    "Age",
    "BloodPressure",
    "SpecificGravity",
    "Albumin",
    "Sugar",
    "BloodGlucose",
    "BloodUrea",
    "SerumCreatinine",
    "Sodium",
    "Potassium",
    "Hemoglobin",
    "PackedCellVolume",
    "WBC",
    "RBC",
    "eGFR",
    "UrineProteinCreatinineRatio",
    "UrineOutput",
    "SerumAlbumin",
    "Calcium",
    "Phosphate",
    "BMI",
    "CystatinC"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# Standardize Yes/No Columns
# ==========================================

binary_columns = [
    "Hypertension",
    "Diabetes",
    "CoronaryArteryDisease",
    "PedalEdema",
    "Anemia"
]

for col in binary_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df[col] = df[col].replace({
        "yes": 1,
        "y": 1,
        "1": 1,
        "present": 1,

        "no": 0,
        "n": 0,
        "0": 0,
        "notpresent": 0,
        "not present": 0
    })

# ==========================================
# Smoking
# ==========================================

df["Smoking"] = (
    df["Smoking"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Smoking"] = df["Smoking"].replace({
    "yes": 1,
    "no": 0
})

# ==========================================
# Physical Activity
# ==========================================

df["PhysicalActivity"] = (
    df["PhysicalActivity"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["PhysicalActivity"] = df["PhysicalActivity"].replace({
    "low": 0,
    "moderate": 1,
    "high": 2
})

# ==========================================
# Appetite
# ==========================================

df["Appetite"] = (
    df["Appetite"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Appetite"] = df["Appetite"].replace({
    "good": 1,
    "poor": 0
})

# ==========================================
# Fill Missing Values
# ==========================================

for col in df.columns:

    if col == "Target":
        continue

    if df[col].dtype == object:
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].median())

# ==========================================
# Target Mapping
# ==========================================

df["Target"] = (
    df["Target"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Target"] = df["Target"].replace({

    # Original CKD dataset
    "ckd": 1,
    "ckd\t": 1,
    "notckd": 0,
    "not ckd": 0,

    # New dataset
    "no_disease": 0,
    "low_risk": 0,

    "moderate_risk": 1,
    "high_risk": 1,
    "severe_disease": 1

})

binary_columns = [
    "Hypertension",
    "Diabetes",
    "CoronaryArteryDisease",
    "Appetite",
    "PedalEdema",
    "Anemia",
    "Smoking",
    "PhysicalActivity"
]

for col in binary_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")



# Convert everything else to NaN
df["Target"] = pd.to_numeric(df["Target"], errors="coerce")

# Remove unknown targets
df = df.dropna(subset=["Target"])

# Convert to integer
df["Target"] = df["Target"].astype(int)

# ==========================================
# Save
# ==========================================

df.to_csv(
    "datasets/clean_kidney_dataset.csv",
    index=False
)

print("\n" + "=" * 60)
print("Cleaning Completed Successfully")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nSaved:")
print("datasets/clean_kidney_dataset.csv")