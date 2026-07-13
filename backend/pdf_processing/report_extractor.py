import re


def search_patterns(patterns, text):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


def extract_report_details(text: str):

    details = {

        "age": None,

        "gender": None,

        "height": None,

        "weight": None,

        "bmi": None

    }

    # -----------------------
    # AGE
    # -----------------------

    age_patterns = [

        r"Age\s*:?\s*(\d+)",

        r"Age\/Sex\s*:?\s*(\d+)",

        r"(\d+)\s*Years"

    ]

    age = search_patterns(
        age_patterns,
        text
    )

    if age:

        details["age"] = int(age)

    # -----------------------
    # GENDER
    # -----------------------

    gender_patterns = [

        r"Gender\s*:?\s*(Male|Female|Other)",

        r"Sex\s*:?\s*(Male|Female|Other)",

        r"Age\/Sex\s*:?\s*\d+\s*/\s*(M|F)"

    ]

    gender = search_patterns(
        gender_patterns,
        text
    )

    if gender:

        gender = gender.upper()

        if gender == "M":

            gender = "Male"

        elif gender == "F":

            gender = "Female"

        details["gender"] = gender.title()

    # -----------------------
    # HEIGHT
    # -----------------------

    height_patterns = [

        r"Height\s*:?\s*(\d+(?:\.\d+)?)",

        r"Height\s*\(cm\)\s*:?\s*(\d+(?:\.\d+)?)"

    ]

    height = search_patterns(
        height_patterns,
        text
    )

    if height:

        details["height"] = float(height)

    # -----------------------
    # WEIGHT
    # -----------------------

    weight_patterns = [

        r"Weight\s*:?\s*(\d+(?:\.\d+)?)",

        r"Weight\s*\(kg\)\s*:?\s*(\d+(?:\.\d+)?)"

    ]

    weight = search_patterns(
        weight_patterns,
        text
    )

    if weight:

        details["weight"] = float(weight)

    # -----------------------
    # BMI
    # -----------------------

    bmi_patterns = [

        r"BMI\s*:?\s*(\d+(?:\.\d+)?)"

    ]

    bmi = search_patterns(
        bmi_patterns,
        text
    )

    if bmi:

        details["bmi"] = float(bmi)

    elif details["height"] and details["weight"]:

        height = details["height"]

        # Convert cm → m
        if height > 3:

            height /= 100

        details["bmi"] = round(

            details["weight"] /

            (height * height),

            2

        )

    return details


if __name__ == "__main__":

    sample = """

    Patient Name : Yaswanth

    Age/Sex : 22 / M

    Height : 172

    Weight : 70

    """

    print(extract_report_details(sample))