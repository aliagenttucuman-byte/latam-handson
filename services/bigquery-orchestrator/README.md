# BigQuery Orchestrator (BQO)

## ¿Qué hace?

Pipeline de transformaciones SQL (SQLx / Dataform) que toma datos crudos de las 6 fuentes de LATAM y los convierte en una tabla limpia (`hands_on_master_cl`) lista para entrenar el modelo ML.

## Estructura

```
bigquery-orchestrator/
├── definitions/
│   ├── declarations/          # Tablas externas (6 fuentes)
│   │   ├── all_declarations.sqlx       (referencia)
│   │   ├── ebiz_google_analytics_4.sqlx
│   │   ├── dmt_commercial_us.sqlx
│   │   ├── dmt_reference_us.sqlx
│   │   ├── dmt_customer_us.sqlx
│   │   ├── customer_management.sqlx
│   │   └── customer_marketing.sqlx
│   ├── models/
│   │   ├── raw/               # Tablas raw (ingesta de archivos)
│   │   │   └── export_mst_all_hits.sqlx
│   │   └── processed/         # Tablas processed (features para ML)
│   │       ├── hands_on_master_cl.sqlx       (LA MÁS IMPORTANTE)
│   │       ├── features_propension.sqlx
│   │       └── predictions_input.sqlx
│   └── tests/
│       └── assertions.sqlx    # Tests de calidad sobre las tablas
├── terraform/
│   └── main.tf                # Dataform workflow + cron schedule
└── README.md
```

## ¿Qué archivos tocar?

1. **`definitions/declarations/*.sqlx`** — Reemplazar con las declaraciones reales de las 6 fuentes (1 archivo por fuente).
2. **`definitions/models/processed/hands_on_master_cl.sqlx`** — La query principal. Tiene TODOs marcados. Reemplazá con SQL real.
3. **`terraform/main.tf`** — Configurar el cron schedule (default: día 1 de cada mes a las 02:00).

## Configuración del schedule

En `terraform/main.tf`, módulo `dataform_workflow_daily`:

```hcl
dataform_workflow_daily: nombre del workflow
cron_schedule: "0 2 1 * *"  # día 1 de cada mes, 02:00
```

## Service Account

La SA `nelson-acosta-ob-bqo-sa@<project>.iam.gserviceaccount.com` se crea automáticamente cuando instanciás el template de BQO en Cosmos Catalog. **No tenés que crearla a mano.**

Necesita estos permisos (pedirselos a tu Staff):
- `roles/bigquery.dataViewer` en las 6 fuentes
- `roles/bigquery.jobUser` en el proyecto dev
- `roles/bigquery.dataEditor` en tu dataset `nelson_acosta_ob_processed`

## Tests

En `definitions/tests/assertions.sqlx`, definí aserciones sobre la tabla `hands_on_master_cl`:

```sql
config { type: "assertion" }

-- La tabla no debería estar vacía
ASSERT (
  SELECT COUNT(*) > 0
  FROM ${ref("hands_on_master_cl")}
) AS "hands_on_master_cl should not be empty";

-- El target no debería tener solo 0s
ASSERT (
  SELECT SUM(target_purchase_30d) / COUNT(*) > 0.01
  FROM ${ref("hands_on_master_cl")}
) AS "target should have at least 1% positive rate";
```

## Cómo correr el pipeline

1. Andá a Dataform Studio en GCP Console
2. Abrí el workspace de tu repo
3. Click en "Start Execution"
4. Seleccioná tags (ej. `master` o `all`)
5. Esperá el status `success`

## Referencias

- [BigQuery Orchestrator Template](https://catalog.cosmos.../templates/bqo-2.0)
- [Dataform docs](https://cloud.google.com/dataform/docs)
- [`../../docs/00-onboarding/03-fuentes-datos.md`](../../docs/00-onboarding/03-fuentes-datos.md)
