FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt ./

# Install build tools and dependencies temporarily
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy full app into new image with only Python + dependencies
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
