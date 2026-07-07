# Medical Intelligence AI - ML Module

## Overview

This module contains the Machine Learning pipeline for predicting three medical conditions:

- Diabetes
- Heart Disease
- Chronic Kidney Disease (CKD)

The module includes data preprocessing, model training, prediction, evaluation, and explainability using SHAP.

---

# Project Structure

```
backend/ml/
│
├── models/
│   ├── diabetes_model.pkl
│   ├── heart_model.pkl
│   ├── ckd_model.pkl
│   └── preprocessors/
│
├── evaluate.py
├── evaluation_results.txt
├── feature_engineering.py
├── predict.py
├── shap_explainer.py
├── test_prediction.py
└── README.md
```

---

# Datasets

## Diabetes

Dataset:
- Pima Indians Diabetes Dataset

Target:
- Outcome

Features:

- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age

---

## Heart Disease

Dataset:
- UCI Heart Disease Dataset

Target:
- target

Features:

- age
- sex
- cp
- trestbps
- chol
- fbs
- restecg
- thalach
- exang
- oldpeak
- slope
- ca
- thal

---

## Chronic Kidney Disease

Dataset:
- Chronic Kidney Disease Dataset

Target:
- classification

Features:

- age
- bp
- sg
- al
- su
- rbc
- pc
- pcc
- ba
- bgr
- bu
- sc
- sod
- pot
- hemo
- pcv
- wc
- rc
- htn
- dm
- cad
- appet
- pe
- ane

---

# Model

Algorithm used for all datasets:

- XGBoost Classifier

Saved Models:

- models/diabetes_model.pkl
- models/heart_model.pkl
- models/ckd_model.pkl

---

# Feature Engineering

The preprocessing pipeline is implemented in:

```
feature_engineering.py
```

Pipeline includes:

- Dataset loading
- Missing value handling
- Categorical encoding
- Feature scaling
- Feature preparation

---

# Model Evaluation

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score

Results are stored in:

```
evaluation_results.txt
```

---

# Model Accuracy

The latest evaluation metrics are available in:

```
backend/ml/evaluation_results.txt
```

---

# Prediction

Prediction functions are available in:

```
predict.py
```

Each prediction returns:

```python
{
    "prediction": "...",
    "confidence": 0.91,
    "probabilities": {
        "...": 0.91,
        "...": 0.09
    }
}
```

---

# Explainability

SHAP explanations are generated using:

```
shap_explainer.py
```

Top contributing features are returned for each prediction.

---

# Training

Train the models using:

```bash
uv run python backend/ml/train.py
```

---

# Evaluation

Run model evaluation:

```bash
uv run python backend/ml/evaluate.py
```

---

# Prediction Testing

Run inference tests:

```bash
uv run python backend/ml/test_prediction.py
```

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- Joblib

---

# Authors

Medical Intelligence AI Team