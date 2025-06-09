FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]