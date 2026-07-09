# File Ingestor — GA4

## ¿Qué hace?

Ingesta archivos Parquet (eventos de Google Analytics 4) desde un GCS bucket origen hacia una tabla raw en BigQuery. Es el "puente" entre archivos planos y BQ.

## Estructura

```
file-ingestor-ga4/
├── schemas/
│   └── biglake_table.json     # Schema de la tabla raw (CONTRACTUAL)
├── terraform/
│   ├── main.tf                # Pipeline de ingesta
│   ├── custom_infrastructure.tf  # Permisos especiales
│   └── variables.tf
└── README.md
```

## ¿Qué archivos tocar?

1. **`schemas/biglake_table.json`** — Reemplazar con el schema real de GA4 (de `new-hire-integration/assets/biglake_table.json`).
2. **`terraform/custom_infrastructure.tf`** — Dar permisos a la SA del BQO.

## Permisos críticos

En `terraform/custom_infrastructure.tf`:

```hcl
# Dar acceso a la SA del BQO al landing bucket
resource "google_storage_bucket_iam_member" "bqo_landing_access" {
  bucket = module.gcs_bucket.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:hands-on-bqo-sa@<project>.iam.gserviceaccount.com"
}
```

## Cómo correr la ingesta

1. Subí archivos Parquet al bucket origen
2. Andá a Dataform Studio → tu workspace del BQO
3. Navegá a `definitions -> raw -> export_mst_all_hits.sqlx`
4. En el bloque `uri`, cambiá el bucket por el de tu landing-bucket
5. Click "Start execution"
6. Seleccioná:
   - Tags: `file-ingestor-hands-on`
   - Service account: `hands-on-bqo-sa`
7. Click "Start execution"
8. Esperá status `success`

## Verificación

```bash
# 1. Bucket origen
gsutil ls gs://<origen-bucket>/*.parquet

# 2. Landing bucket (procesados)
gsutil ls gs://<landing-bucket>/

# 3. Failed bucket (errores)
gsutil ls gs://<failed-bucket>/  # debería estar vacío

# 4. Tabla en BigQuery
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM \`<project>.<dataset>.mst_all_hits\`"
```

## Troubleshooting

- **"Permission denied" en el bucket**: verificá `custom_infrastructure.tf`
- **"Schema mismatch"**: el Parquet no coincide con `biglake_table.json`. Verificá las columnas.
- **"No files found"**: el bucket origen está vacío o la URI es incorrecta.

## Referencias

- [File Ingestor Template](https://catalog.cosmos.../templates/file-ingestor)
