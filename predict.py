import pickle

# Load the saved model and encoder
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("dv.pkl", "rb") as f:
    dv = pickle.load(f)


def predict(student_data):
    """
    Predict exam score for a student
    """
    # Convert to dict format for DictVectorizer
    X = dv.transform([student_data])

    # Predict
    prediction = model.predict(X)[0]

    return prediction


# Test
if __name__ == "__main__":
    student = {
        "hours_studied": 30,
        "attendance": 90,
        "parental_involvement": "high",
        "access_to_resources": "high",
        "extracurricular_activities": "yes",
        "sleep_hours": 7,
        "previous_scores": 85,
        "motivation_level": "high",
        "internet_access": "yes",
        "tutoring_sessions": 2,
        "family_income": "medium",
        "teacher_quality": "high",
        "school_type": "public",
        "peer_influence": "positive",
        "physical_activity": 3,
        "learning_disabilities": "no",
        "parental_education_level": "college",
        "distance_from_home": "near",
        "gender": "female",
    }

    score = predict(student)
    print(f"Predicted exam score: {score:.2f}")
