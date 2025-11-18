FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY uv.lock . 
COPY train.py .
COPY predict.py .
COPY app.py .
COPY model.pkl .
COPY dv.pkl .

# Install dependencies
RUN uv sync --frozen --no-cache

# Expose port
EXPOSE 8080

# Run the app
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]