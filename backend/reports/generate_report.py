from google import genai

from backend.config import GEMINI_API_KEY
from backend.rag.report_prompt import create_report_prompt


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_report(patient, lab_values, prediction):

    prompt = create_report_prompt(
        patient=patient,
        lab_values=lab_values,
        prediction=prediction
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    patient = {
        "patient_name": "John",
        "age": 52,
        "gender": "Male"
    }

    lab_values = {
        "fasting_glucose": 180,
        "post_meal_glucose": 250,
        "hba1c": 8.4
    }

    prediction = {
        "prediction": "Diabetes",
        "confidence": 0.94,
        "risk": "High"
    }

    report = generate_report(
        patient,
        lab_values,
        prediction
    )

    print(report)