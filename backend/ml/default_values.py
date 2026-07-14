"""
Default values used when a feature is not available
from the uploaded medical report.

These values can later be replaced with the
training-set mean/median values.
"""

DEFAULT_VALUES = {

    # =====================================================
    # Diabetes
    # =====================================================

    "Pregnancies": 0,
    "Insulin": 80,
    "Hypertension": 0,
    "Smoking": 0,
    "FamilyHistory": 0,
    "HeartDisease": 0,

    # =====================================================
    # Heart Disease
    # =====================================================

    "Diabetes": 0,
    "Alcohol": 0,
    "PhysicalActivity": 1,
    "HeartRate": 72,
    "Platelets": 250000,

    # =====================================================
    # CKD
    # =====================================================

    "SpecificGravity": 1.020,
    "Albumin": 4.0,
    "Sugar": 0,
    "PackedCellVolume": 42,
    "WBC": 7500,
    "RBC": 4.8,
    "CoronaryArteryDisease": 0,
    "Appetite": 1,
    "PedalEdema": 0,
    "Anemia": 0,
    "eGFR": 90,
    "UrineProteinCreatinineRatio": 0.15,
    "UrineOutput": 1500,
    "SerumAlbumin": 4.2,
    "Calcium": 9.2,
    "Phosphate": 3.5,
    "CystatinC": 0.9,

    # =====================================================
    # Common
    # =====================================================

    "Height": 170,
    "Weight": 70,
    "BMI": 24.2,

    "BloodPressure": "120/80",

    "SystolicBP": 120,
    "DiastolicBP": 80,

    "Glucose": 100,
    "BloodGlucose": 100,

    "HbA1c": 5.5,

    "BloodUrea": 25,

    "SerumCreatinine": 1.0,

    "TotalCholesterol": 180,

    "Hemoglobin": 14,

    "Sodium": 140,

    "Potassium": 4.2,

    "CPK": 90
}