"""
Cloud Run Job: transfiere predicciones ML de BigQuery a GCS.
"""

# TODO: Implementar
# 
# from google.cloud import bigquery, storage
# import os
# from datetime import datetime
# 
# PROJECT_ID = os.getenv("GCP_PROJECT_ID", "nelson-acosta-ob-dev")
# BUCKET_NAME = os.getenv("BUCKET_NAME", "propension-data-bucket")
# SOURCE_TABLE = os.getenv("SOURCE_TABLE", "nelson_acosta_ob_processed.customer_predictions")
# 
# 
# def transfer_bq_to_bucket():
#     """Lee predicciones de BQ y las sube al bucket como CSV."""
#     # 1. Leer predicciones
#     client = bigquery.Client(project=PROJECT_ID)
#     query = f"""
#         SELECT
#             customer_id,
#             propensity_score,
#             predicted_at,
#             model_version
#         FROM `{PROJECT_ID}.{SOURCE_TABLE}`
#         WHERE predicted_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
#     """
#     df = client.query(query).to_dataframe()
#     print(f"Read {len(df)} predictions from {SOURCE_TABLE}")
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
#     print(f"Uploaded to gs://{BUCKET_NAME}/data/predictions_{today}.csv")
# 
# 
# if __name__ == "__main__":
#     transfer_bq_to_bucket()
