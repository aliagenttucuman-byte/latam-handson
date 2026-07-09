FROM python:3.11-slim

WORKDIR /app

# TODO: Dependencias del sistema si las necesitás (build-essential, etc.)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Vertex AI Pipelines usa el entrypoint estándar
ENTRYPOINT ["python", "-m", "kfp.components"]
