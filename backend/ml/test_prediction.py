# pyrefly: ignore [missing-import]
from predict import (
    predict_diabetes,
    predict_heart,
    predict_kidney
)


# ---------------------------
# Diabetes Sample
# ---------------------------

diabetes_sample = [
    6,
    148,
    72,
    35,
    0,
    33.6,
    0.627,
    50
]

print("=" * 40)
print("DIABETES TEST")
print("=" * 40)

result = predict_diabetes(diabetes_sample)

print("Prediction :", result["prediction"])
print("Confidence :", f'{result["confidence"] * 100:.0f}%')
print("Probabilities :", result["probabilities"])


# ---------------------------
# Heart Sample
# ---------------------------

heart_sample = [
    63,
    1,
    3,
    145,
    233,
    1,
    0,
    150,
    0,
    2.3,
    0,
    0,
    1
]

print("\n" + "=" * 40)
print("HEART DISEASE TEST")
print("=" * 40)

result = predict_heart(heart_sample)

print("Prediction :", result["prediction"])
print("Confidence :", f'{result["confidence"] * 100:.0f}%')
print("Probabilities :", result["probabilities"])


# ---------------------------
# Kidney Sample
# ---------------------------

kidney_sample = [
    1,
    48,
    80,
    1.020,
    1,
    0,
    1,
    1,
    0,
    0,
    121,
    36,
    1.2,
    135,
    4.5,
    15.4,
    44,
    7800,
    5.2,
    1,
    1,
    0,
    1,
    0,
    0
]

print("\n" + "=" * 40)
print("KIDNEY DISEASE TEST")
print("=" * 40)

result = predict_kidney(kidney_sample)

print("Prediction :", result["prediction"])
print("Confidence :", f'{result["confidence"] * 100:.0f}%')
print("Probabilities :", result["probabilities"])