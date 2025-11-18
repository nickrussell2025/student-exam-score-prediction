import pickle
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load model and encoder
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("dv.pkl", "rb") as f:
    dv = pickle.load(f)

app = FastAPI()

# Simple rate limiting (10 requests per minute per IP)
request_counts = defaultdict(list)


def check_rate_limit(ip: str):
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)

    # Clean old requests
    request_counts[ip] = [
        req_time for req_time in request_counts[ip] if req_time > minute_ago
    ]

    if len(request_counts[ip]) >= 10:
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Try again later."
        )

    request_counts[ip].append(now)


class Student(BaseModel):
    hours_studied: int
    attendance: int
    parental_involvement: str
    access_to_resources: str
    extracurricular_activities: str
    sleep_hours: int
    previous_scores: int
    motivation_level: str
    internet_access: str
    tutoring_sessions: int
    family_income: str
    teacher_quality: str
    school_type: str
    peer_influence: str
    physical_activity: int
    learning_disabilities: str
    parental_education_level: str
    distance_from_home: str
    gender: str


@app.get("/")
def home():
    return {"message": "Student Exam Score Prediction API"}


@app.post("/predict")
def predict(student: Student):
    # Rate limit check
    check_rate_limit("default")

    student_dict = student.model_dump()
    X = dv.transform([student_dict])
    score = model.predict(X)[0]

    return {"predicted_exam_score": round(score, 2)}
