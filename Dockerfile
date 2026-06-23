# AuditPilot container.
# Default CMD launches the Gradio demo (HF Spaces-compatible: app on $PORT/7860).
# To run the FastAPI service instead, override CMD (see comment below).

FROM python:3.11-slim

# System deps kept minimal; add build tools only if a wheel needs compiling.
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source.
COPY . .

# HF Spaces injects PORT; default to 7860 locally.
ENV PORT=7860
EXPOSE 7860

# Gradio demo entry point (HF Spaces expects app.py).
CMD ["python", "app.py"]

# To run the FastAPI service instead:
#   docker run ... auditpilot \
#     uvicorn api.main:app --host 0.0.0.0 --port 8000
