from langchain_core.prompts import PromptTemplate


REPORT_PROMPT = PromptTemplate(
    input_variables=[
        "patient",
        "lab_values",
        "prediction"
    ],
    template="""
You are MedIntel AI.

Generate a medical report using ONLY the information below.

Patient Details:
{patient}

Lab Values:
{lab_values}

Prediction:
{prediction}

Instructions:
- Explain the report in simple English.
- Highlight important findings.
- Mention possible health concerns.
- Suggest general healthy lifestyle habits.
- Recommend consulting a doctor.
- Do NOT prescribe medicines.
- Mention this is AI-generated and not a medical diagnosis.

Medical Report:
"""
)


def create_report_prompt(patient, lab_values, prediction):

    return REPORT_PROMPT.format(
        patient=patient,
        lab_values=lab_values,
        prediction=prediction
    )