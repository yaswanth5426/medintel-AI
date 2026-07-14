# pyrefly: ignore [missing-import]

# pyrefly: ignore [missing-import]
from predict import (
    predict_diabetes,
    predict_heart,
    predict_kidney
)

try:
    from backend.ml.predict import (
        predict_diabetes,
        predict_heart,
        predict_kidney,
    )
    from backend.ml.feature_mapping import map_features

except ModuleNotFoundError:
    # pyrefly: ignore [missing-import]
    from predict import (
        predict_diabetes,
        predict_heart,
        predict_kidney,
    )
    # pyrefly: ignore [missing-import]
    from feature_mapping import map_features

# pyrefly: ignore [missing-import]
from feature_mapping import map_features

print("\n" + "=" * 60)
print("MEDINTEL AI - MODEL TESTING")
print("=" * 60)

# ======================================================
# Diabetes Test
# ======================================================

print("\nDIABETES TEST\n")

diabetes_report = {

    "Age": 45,
    "Glucose": 180,
    "BMI": 31.5

}

mapped = map_features("diabetes", diabetes_report)

print("Mapped Feature Vector")
print(mapped)

result = predict_diabetes(mapped)

print("\nPrediction :", result["prediction"])
print("Confidence :", result["confidence"])
print("Risk :", result["risk"])
print("Probabilities :", result["probabilities"])

# ======================================================
# Heart Test
# ======================================================

print("\n" + "=" * 60)
print("HEART DISEASE TEST")
print("=" * 60)

heart_report = {

    "Age": 63,
    "Sex": 1,
    "SystolicBP": 145,
    "Glucose": 170

}

mapped = map_features("heart", heart_report)

print("Mapped Feature Vector")
print(mapped)

result = predict_heart(mapped)

print("\nPrediction :", result["prediction"])
print("Confidence :", result["confidence"])
print("Risk :", result["risk"])
print("Probabilities :", result["probabilities"])

# ======================================================
# Kidney Test
# ======================================================

print("\n" + "=" * 60)
print("KIDNEY DISEASE TEST")
print("=" * 60)

kidney_report = {

    "Age": 48,
    "BloodPressure": 80,
    "SerumCreatinine": 2.2

}

mapped = map_features("kidney", kidney_report)

print("Mapped Feature Vector")
print(mapped)

result = predict_kidney(mapped)

print("\nPrediction :", result["prediction"])
print("Confidence :", result["confidence"])
print("Risk :", result["risk"])
print("Probabilities :", result["probabilities"])

# ======================================================
# Invalid Input Test
# ======================================================

print("\n" + "=" * 60)
print("INVALID INPUT TEST")
print("=" * 60)

invalid_report = {

    "Age": -10,
    "Glucose": -100

}

try:

    for key, value in invalid_report.items():

        if value < 0:
            raise ValueError(f"{key} cannot be negative.")

    mapped = map_features("diabetes", invalid_report)

    result = predict_diabetes(mapped)

    print(result)

except ValueError as e:

    print("Validation Error :", e)