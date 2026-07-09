FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# TODO: Ajustar el entrypoint si usás un framework distinto
CMD ["python", "main.py"]
