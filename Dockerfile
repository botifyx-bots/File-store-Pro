# ================================================
# File-Store-Pro — Dockerfile
# Made by: botifyx-bots | @BotifyX_Pro_Botz
# Supports: Heroku · Render · VPS · Local
# ------------------------------------------------
# Before deploying, edit config.py with your values
# ================================================

FROM python:3.11-slim-bullseye

LABEL maintainer="botifyx-bots"
LABEL description="File-Store-Pro — Advanced Telegram File Share Bot"
LABEL version="2.0.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy full project (includes your edited config.py)
COPY . .

# Expose port defined in config.py (default 5010)
EXPOSE 5010

# Health check — hits Flask's "/" route
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5010/ || exit 1

CMD ["python", "main.py"]
