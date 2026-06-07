# Dockerfile for deploying the FastAPI backend on Hugging Face Spaces.
# HF Docker Spaces serve the app on port 7860.
FROM python:3.11-slim

# Install CA certificates so HTTPS calls to the OpenAI API work reliably
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates curl && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces best practice: run as a non-root user (uid 1000)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install Python dependencies first (better build caching)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY --chown=user . .

# HF Spaces expects the app on port 7860
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
