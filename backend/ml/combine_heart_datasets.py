import pandas as pd
import numpy as np

# ==========================================
# Load Datasets
# ==========================================

framingham = pd.read_csv("datasets/new_heart_disease1.csv")

cardio = pd.read_csv("datasets/new_heart_disease2.csv", sep=";")

heart_failure = pd.read_csv(
    "datasets/heart_failure_clinical_records_dataset.csv"
)

# ==========================================
# Master Schema
# ==========================================

MASTER_COLUMNS = [

    "Age",
    "Sex",

    "Height",
    "Weight",

    "BMI",

    "SystolicBP",
    "DiastolicBP",

    "TotalCholesterol",

    "Glucose",

    "Smoking",

    "Diabetes",

    "Hypertension",

    "Alcohol",

    "PhysicalActivity",

    "HeartRate",

    "Platelets",

    "SerumCreatinine",

    "SerumSodium",

    "CPK",

    "Target"
]

# ==========================================
# -------- Framingham ----------
# ==========================================

framingham = framingham.rename(columns={

    "age": "Age",
    "male": "Sex",

    "sysBP": "SystolicBP",
    "diaBP": "DiastolicBP",

    "totChol": "TotalCholesterol",

    "glucose": "Glucose",

    "currentSmoker": "Smoking",

    "diabetes": "Diabetes",

    "prevalentHyp": "Hypertension",

    "heartRate": "HeartRate",

    "BMI": "BMI",

    "TenYearCHD": "Target"

})

# ==========================================
# -------- Cardio Dataset ----------
# ==========================================

cardio = cardio.rename(columns={

    "age": "Age",

    "gender": "Sex",

    "height": "Height",

    "weight": "Weight",

    "ap_hi": "SystolicBP",

    "ap_lo": "DiastolicBP",

    "cholesterol": "TotalCholesterol",

    "gluc": "Glucose",

    "smoke": "Smoking",

    "alco": "Alcohol",

    "active": "PhysicalActivity",

    "cardio": "Target"

})

# ==========================================
# -------- Heart Failure ----------
# ==========================================

heart_failure = heart_failure.rename(columns={

    "age": "Age",

    "sex": "Sex",

    "diabetes": "Diabetes",

    "high_blood_pressure": "Hypertension",

    "platelets": "Platelets",

    "serum_creatinine": "SerumCreatinine",

    "serum_sodium": "SerumSodium",

    "creatinine_phosphokinase": "CPK",

    "DEATH_EVENT": "Target"

})

# ==========================================
# Add Missing Columns
# ==========================================

for df in [framingham, cardio, heart_failure]:

    for col in MASTER_COLUMNS:

        if col not in df.columns:

            df[col] = np.nan

    df = df[MASTER_COLUMNS]

# ==========================================
# Keep Same Column Order
# ==========================================

framingham = framingham[MASTER_COLUMNS]

cardio = cardio[MASTER_COLUMNS]

heart_failure = heart_failure[MASTER_COLUMNS]

# ==========================================
# Merge
# ==========================================

combined = pd.concat(

    [

        framingham,

        cardio,

        heart_failure

    ],

    ignore_index=True

)

# ==========================================
# Save
# ==========================================

combined.to_csv(

    "datasets/combined_heart_dataset.csv",

    index=False

)

print("=" * 50)

print("Combined Successfully")

print("=" * 50)

print("Rows :", combined.shape[0])

print("Columns :", combined.shape[1])

print()

print(combined.columns.tolist())