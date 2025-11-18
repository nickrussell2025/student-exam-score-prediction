.PHONY: help install train predict serve test-local build run push deploy clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make train        - Train the model"
	@echo "  make predict      - Test prediction locally"
	@echo "  make serve        - Run FastAPI server locally"
	@echo "  make test-local   - Test local API endpoint"
	@echo "  make build        - Build Docker image"
	@echo "  make run          - Run Docker container locally"
	@echo "  make push         - Push image to GCR"
	@echo "  make deploy       - Deploy to Cloud Run"
	@echo "  make clean        - Remove generated files"
	@echo "  make lint         - Check for issues"
	@echo "  make lint-fix     - Check & auto-fix"
	@echo "  make format       - Format code"
	@echo "  make format-check - Check if code is formatted"
	@echo "  make quality      - Format & lint code"

		

install:
	uv sync

train:
	uv run train.py

predict:
	uv run predict.py

serve:
	uv run uvicorn app:app --reload --port 8000

test-local:
	curl -X POST "http://localhost:8000/predict" \
	  -H "Content-Type: application/json" \
	  -d '{"hours_studied": 30, "attendance": 90, "parental_involvement": "high", "access_to_resources": "high", "extracurricular_activities": "yes", "sleep_hours": 7, "previous_scores": 85, "motivation_level": "high", "internet_access": "yes", "tutoring_sessions": 2, "family_income": "medium", "teacher_quality": "high", "school_type": "public", "peer_influence": "positive", "physical_activity": 3, "learning_disabilities": "no", "parental_education_level": "college", "distance_from_home": "near", "gender": "female"}'

build:
	docker build -t student-score-api .

run:
	docker run -p 8080:8080 student-score-api

push:
	docker tag student-score-api gcr.io/midterm-ml-project/student-score-api
	docker push gcr.io/midterm-ml-project/student-score-api

deploy: push
	gcloud run deploy student-score-api \
	  --image gcr.io/midterm-ml-project/student-score-api \
	  --platform managed \
	  --region europe-west2 \
	  --allow-unauthenticated

clean:
	rm -f model.pkl dv.pkl
	rm -rf .venv __pycache__ .pytest_cache

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

quality: format lint
	@echo "✓ Code formatting and linting complete"