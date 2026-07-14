import pandas as pd
import numpy as np

# ==========================================
# Load Datasets
# ==========================================

uci = pd.read_csv("datasets/kidney_disease.csv")

test2 = pd.read_csv("datasets/kidney_disease_test2.csv")

dataset1 = pd.read_csv("datasets/kidney_disease_dataset1.csv")

# ==========================================
# Master Schema
# ==========================================

MASTER_COLUMNS = [

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

    "Hypertension",

    "Diabetes",

    "CoronaryArteryDisease",

    "Appetite",

    "PedalEdema",

    "Anemia",

    "eGFR",

    "UrineProteinCreatinineRatio",

    "UrineOutput",

    "SerumAlbumin",

    "Calcium",

    "Phosphate",

    "BMI",

    "Smoking",

    "PhysicalActivity",

    "CystatinC",

    "Target"

]

# ==========================================
# UCI Dataset
# ==========================================

uci = uci.rename(columns={

    "age": "Age",

    "bp": "BloodPressure",

    "sg": "SpecificGravity",

    "al": "Albumin",

    "su": "Sugar",

    "bgr": "BloodGlucose",

    "bu": "BloodUrea",

    "sc": "SerumCreatinine",

    "sod": "Sodium",

    "pot": "Potassium",

    "hemo": "Hemoglobin",

    "pcv": "PackedCellVolume",

    "wc": "WBC",

    "rc": "RBC",

    "htn": "Hypertension",

    "dm": "Diabetes",

    "cad": "CoronaryArteryDisease",

    "appet": "Appetite",

    "pe": "PedalEdema",

    "ane": "Anemia",

    "classification": "Target"

})

# ==========================================
# TEST2 Dataset
# ==========================================

test2 = test2.rename(columns={

    "age": "Age",

    "bp": "BloodPressure",

    "sg": "SpecificGravity",

    "al": "Albumin",

    "su": "Sugar",

    "bgr": "BloodGlucose",

    "bu": "BloodUrea",

    "sc": "SerumCreatinine",

    "sod": "Sodium",

    "pot": "Potassium",

    "hemo": "Hemoglobin",

    "pcv": "PackedCellVolume",

    "wc": "WBC",

    "rc": "RBC",

    "htn": "Hypertension",

    "dm": "Diabetes",

    "cad": "CoronaryArteryDisease",

    "appet": "Appetite",

    "pe": "PedalEdema",

    "ane": "Anemia",

    "classification": "Target"

})

# ==========================================
# Rich Dataset
# ==========================================

dataset1 = dataset1.rename(columns={

    "Age of the patient": "Age",

    "Blood pressure (mm/Hg)": "BloodPressure",

    "Specific gravity of urine": "SpecificGravity",

    "Albumin in urine": "Albumin",

    "Sugar in urine": "Sugar",

    "Random blood glucose level (mg/dl)": "BloodGlucose",

    "Blood urea (mg/dl)": "BloodUrea",

    "Serum creatinine (mg/dl)": "SerumCreatinine",

    "Sodium level (mEq/L)": "Sodium",

    "Potassium level (mEq/L)": "Potassium",

    "Hemoglobin level (gms)": "Hemoglobin",

    "Packed cell volume (%)": "PackedCellVolume",

    "White blood cell count (cells/cumm)": "WBC",

    "Red blood cell count (millions/cumm)": "RBC",

    "Hypertension (yes/no)": "Hypertension",

    "Diabetes mellitus (yes/no)": "Diabetes",

    "Coronary artery disease (yes/no)": "CoronaryArteryDisease",

    "Appetite (good/poor)": "Appetite",

    "Pedal edema (yes/no)": "PedalEdema",

    "Anemia (yes/no)": "Anemia",

    "Estimated Glomerular Filtration Rate (eGFR)": "eGFR",

    "Urine protein-to-creatinine ratio": "UrineProteinCreatinineRatio",

    "Urine output (ml/day)": "UrineOutput",

    "Serum albumin level": "SerumAlbumin",

    "Serum calcium level": "Calcium",

    "Serum phosphate level": "Phosphate",

    "Body Mass Index (BMI)": "BMI",

    "Smoking status": "Smoking",

    "Physical activity level": "PhysicalActivity",

    "Cystatin C level": "CystatinC",

    "Target": "Target"

})

# ==========================================
# Add Missing Columns
# ==========================================

for df in [uci, test2, dataset1]:

    for col in MASTER_COLUMNS:

        if col not in df.columns:
            df[col] = np.nan

# ==========================================
# Same Column Order
# ==========================================

uci = uci[MASTER_COLUMNS]

test2 = test2[MASTER_COLUMNS]

dataset1 = dataset1[MASTER_COLUMNS]

# ==========================================
# Merge
# ==========================================

combined = pd.concat(

    [

        uci,

        test2,

        dataset1

    ],

    ignore_index=True

)

# ==========================================
# Save
# ==========================================

combined.to_csv(

    "datasets/combined_kidney_dataset.csv",

    index=False

)

print("=" * 50)
print("Combined Successfully")
print("=" * 50)

print("Rows :", combined.shape[0])
print("Columns :", combined.shape[1])
print()
print(combined.columns.tolist())