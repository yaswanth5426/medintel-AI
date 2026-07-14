import re

REPORT_KEYWORDS = {

    "diabetes": [

        "diabetes",
        "diabetic",
        "glucose",
        "blood sugar",
        "fasting blood sugar",
        "fbs",
        "ppbs",
        "hba1c",
        "glycemic"

    ],

    "heart": [

        "heart",
        "cardiac",
        "cardio",
        "lipid",
        "cholesterol",
        "ecg",
        "echo",
        "troponin",
        "cpk"

    ],

    "ckd": [

        "kidney",
        "renal",
        "ckd",
        "kft",
        "creatinine",
        "blood urea",
        "egfr"

    ]

}


def clean_text(text: str):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text


def identify_disease(text: str):
    """
    Detect disease from report name / first page text.

    Returns:
    {
        "disease": "...",
        "matched_keyword": "...",
        "score": ...
    }
    """

    text = clean_text(text)

    scores = {

        "diabetes": 0,

        "heart": 0,

        "ckd": 0

    }

    matched_keywords = {

        "diabetes": [],

        "heart": [],

        "ckd": []

    }

    for disease, keywords in REPORT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                scores[disease] += 1

                matched_keywords[disease].append(keyword)

    best = max(

        scores,

        key=scores.get

    )

    if scores[best] == 0:

        return {

            "disease": None,

            "matched_keyword": None,

            "score": 0

        }

    return {

        "disease": best,

        "matched_keyword": matched_keywords[best],

        "score": scores[best]

    }


if __name__ == "__main__":

    sample = """

    APOLLO HOSPITAL

    HEART HEALTH PROFILE

    Total Cholesterol

    HDL

    LDL

    Triglycerides

    ECG

    """

    result = identify_disease(sample)

    print(result)