# Data to Bucket — Cloud Run Job

## ¿Qué hace?

Job batch que transfiere las predicciones ML desde BigQuery al bucket GCS en un formato que Light RAG pueda indexar. Esto le permite al chatbot consultar predicciones vía RAG (no solo vía la tool directa).

## Estructura

```
data-to-bucket/
├── main.py                    # Lógica del job
├── Dockerfile
├── requirements.txt
└── README.md
```

## ¿Qué archivos tocar?

1. **`main.py`** — Implementar la query a BQ y la escritura a GCS.

## Flujo

```
BigQuery (customer_predictions)
  ↓ SELECT *
  ↓ Formatear como CSV/Parquet
GCS (gs://<bucket>/data/predictions_YYYYMMDD.csv)
  ↓ (Light RAG los indexa en su próxima ingesta)
```

## main.py (esqueleto)

```python
# TODO: Implementar
# 
# from google.cloud import bigquery, storage
# import pandas as pd
# from datetime import datetime
# import os
# 
# PROJECT_ID = os.getenv("GCP_PROJECT_ID")
# BUCKET_NAME = os.getenv("BUCKET_NAME")
# SOURCE_TABLE = os.getenv("SOURCE_TABLE", "nelson_acosta_ob_processed.customer_predictions")
# 
# def transfer_bq_to_bucket():
#     # 1. Leer predicciones de BigQuery
#     client = bigquery.Client(project=PROJECT_ID)
#     query = f"SELECT customer_id, propensity_score, predicted_at FROM `{PROJECT_ID}.{SOURCE_TABLE}`"
#     df = client.query(query).to_dataframe()
#     
#     # 2. Formatear como CSV
#     today = datetime.now().strftime("%Y%m%d")
#     csv_content = df.to_csv(index=False)
#     
#     # 3. Subir al bucket
#     storage_client = storage.Client(project=PROJECT_ID)
#     bucket = storage_client.bucket(BUCKET_NAME)
#     blob = bucket.blob(f"data/predictions_{today}.csv")
#     blob.upload_from_string(csv_content, content_type="text/csv")
#     
#     print(f"Uploaded {len(df)} predictions to gs://{BUCKET_NAME}/data/predictions_{today}.csv")
# 
# if __name__ == "__main__":
#     transfer_bq_to_bucket()
```

## Cómo deployar

1. Compilá:
   ```bash
   docker build -t us-east1-docker.pkg.dev/nelson-acosta-ob-dev/data-jobs/data-to-bucket:latest .
   docker push us-east1-docker.pkg.dev/nelson-acosta-ob-dev/data-jobs/data-to-bucket:latest
   ```

2. Deployá como Cloud Run Job (no Service):
   - Tipo: Job (no Service)
   - Image: la que subiste
   - Env vars: `GCP_PROJECT_ID`, `BUCKET_NAME`, `SOURCE_TABLE`
   - Service account: una con permisos `bigquery.dataViewer` y `storage.objectCreator`

3. Triggereá:
   - Manual desde Cloud Run Jobs
   - O con Cloud Scheduler (cron)
   - O como último paso del serving pipeline de Vertex AI

## Referencias

- [Cloud Run Jobs](https://cloud.google.com/run/docs/create-jobs)
- [BigQuery client library](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [Cloud Storage client library](https://cloud.google.com/python/docs/reference/storage/latest)
