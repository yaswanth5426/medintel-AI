import pandas as pd
import numpy as np

# -----------------------------
# Load datasets
# -----------------------------

pima = pd.read_csv("datasets/diabetes.csv")

clinical = pd.read_csv("datasets/diabetes_data.csv")

notes = pd.read_csv("datasets/diabetes_dataset_with_notes.csv")

# -----------------------------
# Create master columns
# -----------------------------

MASTER_COLUMNS = [
    "Age",
    "Gender",
    "Pregnancies",
    "Glucose",
    "HbA1c",
    "BMI",
    "BloodPressure",
    "Insulin",
    "Hypertension",
    "Smoking",
    "FamilyHistory",
    "HeartDisease",
    "Outcome"
]

# -----------------------------
# Convert Pima
# -----------------------------

pima_master = pd.DataFrame()

pima_master["Age"] = pima["Age"]
pima_master["Gender"] = np.nan
pima_master["Pregnancies"] = pima["Pregnancies"]
pima_master["Glucose"] = pima["Glucose"]
pima_master["HbA1c"] = np.nan
pima_master["BMI"] = pima["BMI"]
pima_master["BloodPressure"] = pima["BloodPressure"]
pima_master["Insulin"] = pima["Insulin"]
pima_master["Hypertension"] = np.nan
pima_master["Smoking"] = np.nan
pima_master["FamilyHistory"] = pima["DiabetesPedigreeFunction"]
pima_master["HeartDisease"] = np.nan
pima_master["Outcome"] = pima["Outcome"]

# -----------------------------
# Convert Clinical Dataset
# -----------------------------

clinical_master = pd.DataFrame()

clinical_master["Age"] = np.nan
clinical_master["Gender"] = np.nan
clinical_master["Pregnancies"] = np.nan
clinical_master["Glucose"] = clinical["Fasting_Blood_Glucose"]
clinical_master["HbA1c"] = clinical["HbA1c"]
clinical_master["BMI"] = clinical["BMI"]
clinical_master["BloodPressure"] = clinical["Blood_Pressure_Systolic"]
clinical_master["Insulin"] = clinical["Insulin_Levels"]
clinical_master["Hypertension"] = clinical["Hypertension"]
clinical_master["Smoking"] = clinical["Smoking"]
clinical_master["FamilyHistory"] = clinical["Family_History_of_Diabetes"]
clinical_master["HeartDisease"] = np.nan
clinical_master["Outcome"] = clinical["Diabetes_Status"]

# -----------------------------
# Convert Notes Dataset
# -----------------------------

notes_master = pd.DataFrame()

notes_master["Age"] = notes["age"]
notes_master["Gender"] = notes["gender"]
notes_master["Pregnancies"] = np.nan
notes_master["Glucose"] = notes["blood_glucose_level"]
notes_master["HbA1c"] = notes["hbA1c_level"]
notes_master["BMI"] = notes["bmi"]
notes_master["BloodPressure"] = np.nan
notes_master["Insulin"] = np.nan
notes_master["Hypertension"] = notes["hypertension"]
notes_master["Smoking"] = notes["smoking_history"]
notes_master["FamilyHistory"] = np.nan
notes_master["HeartDisease"] = notes["heart_disease"]
notes_master["Outcome"] = notes["diabetes"]

# -----------------------------
# Merge
# -----------------------------

combined = pd.concat(
    [
        pima_master,
        clinical_master,
        notes_master
    ],
    ignore_index=True
)

# -----------------------------
# Remove duplicates
# -----------------------------

combined = combined.drop_duplicates()

# -----------------------------
# Save
# -----------------------------

combined.to_csv(
    "datasets/combined_diabetes_dataset.csv",
    index=False
)

print("=" * 50)
print("Combined Successfully")
print("=" * 50)
print("Rows :", len(combined))
print("Columns :", len(combined.columns))
print("\nColumns:")
print(combined.columns.tolist())