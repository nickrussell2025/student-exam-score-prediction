# Student Exam Score Prediction

Predicts student exam scores based on study habits, attendance, and background factors using Linear Regression.

## Problem Description

This project predicts exam scores (0-100) for students based on 19 features including hours studied, attendance, parental involvement, and access to resources. The model achieves an RMSE of 1.745 and R² of 0.769 on test data.

## Dataset

- **Source:** [Kaggle - Student Performance Factors](https://www.kaggle.com/datasets/mosapabdelghany/student-performance-factors-dataset/data)
- **Size:** 6,607 students
- **Features:** 19 (6 numerical, 13 categorical)
- **Target:** exam_score (continuous)

## Model Performance

| Model | RMSE | R² |
|-------|------|-----|
| Linear Regression | 1.745 | 0.769 |
| Ridge Regression | 2.469 | 0.616 |
| Random Forest | 2.694 | 0.543 |

## Quick Start

### Prerequisites
- Python 3.12+
- UV package manager
- Docker (optional, for containerization)

### Installation
```bash
git clone https://github.com/nickrussell2025/student-exam-score-prediction.git
cd student-exam-score-prediction
make install
```

### Using Make Commands

**Model Training & Testing:**
```bash
make train        # Train the model
make predict      # Test prediction locally
```

**Run API Locally:**
```bash
make serve        # Start FastAPI server on port 8000
make test-local   # Test the local endpoint (run in another terminal)
```

Visit http://localhost:8000/docs for interactive API documentation.


**Docker:**
```bash
make build        # Build Docker image
make run          # Run container locally on port 8080
```

**Cloud Deployment:**
```bash
make deploy       # Build, push, and deploy to Cloud Run
```

### Manual Commands (without Make)

**Train Model:**
```bash
uv run train.py
```

**Test Prediction:**
```bash
uv run predict.py
```

**Run API Locally:**
```bash
uv run uvicorn app:app --reload --port 8000
```

**Docker:**
```bash
docker build -t student-score-api .
docker run -p 8080:8080 student-score-api
```

## Cloud Deployment

Deployed on Google Cloud Run:
- **URL:** https://student-score-api-848792746238.europe-west2.run.app
- **Region:** europe-west2 (London)

### Test Cloud Endpoint
```bash
curl -X POST 'https://student-score-api-848792746238.europe-west2.run.app/predict' \
  -H 'Content-Type: application/json' \
  -d '{
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
    "gender": "female"
  }'
```

## Files

- `notebook.ipynb` - EDA & model testings 
- `train.py` - model training pipeline
- `predict.py` - prediction script
- `app.py` - FastAPI web service
- `Dockerfile` - container configuration
- `pyproject.toml` - dependencies
- `model.pkl` - trained model
- `dv.pkl` - feature encoder
- `StudentPerformanceFactors.csv`- source data
- `Makefile` - build & deployment automation

## Key Findings

- **Attendance** (MI: 0.31) and **hours_studied** (MI: 0.18) are the strongest predictors
- Linear relationships dominate - complex models don't improve performance
- 27 out of 40 one-hot encoded features had zero predictive power and were dropped

## Author

Nick - ML Zoomcamp Midterm Project 2025