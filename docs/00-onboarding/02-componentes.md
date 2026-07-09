# 02 — Componentes (Detalle por Servicio)

## Repositorio de Infraestructura (`infra/`)

**Qué hace**: Crea todos los recursos GCP (bucket, dataset, tabla, Light RAG, service accounts, IAM) usando Terraform y los módulos de Cosmos.

**Input**: variables en `terraform.tfvars` (project_id, region, product_name, team).

**Output**: 
- GCS bucket `propension-data-bucket`
- BigQuery dataset `nelson-acosta-ob_processed` 
- BigQuery tabla `customer_predictions`
- Cloud Run service de Light RAG
- Cloud Scheduler para ingesta
- Service Account `nelson-acosta-ob-sa@<project>.iam.gserviceaccount.com`

**Archivos clave**:
- `infra/environments/dev/main.tf` — define los módulos a crear
- `infra/environments/dev/variables.tf` — declaración de variables
- `infra/environments/dev/terraform.tfvars` — valores para dev
- `infra/modules/data-product/main.tf` — lógica custom (si hay)

**Cuándo tocarlo**: Cada vez que agregás un servicio nuevo (Light RAG, Cloud Run extra, etc).

---

## BigQuery Orchestrator (`services/bigquery-orchestrator/`)

**Qué hace**: Pipeline de transformaciones SQL que toma datos crudos de las 6 fuentes y los convierte en una tabla limpia (`hands_on_master_cl`) lista para ML.

**Input**: 
- 6 fuentes de BigQuery (declaradas, no copiadas)
- Tabla raw de GA4 (del File Ingestor)

**Output**: 
- `nelson-acosta-ob_processed.hands_on_master_cl` (tabla final con features)
- Tablas intermedias en `processed/` (features_propension, predictions_input)

**Archivos clave**:
- `definitions/declarations/*.sqlx` — declara las 6 fuentes externas
- `definitions/models/raw/export_mst_all_hits.sqlx` — referencia a tabla raw de GA4
- `definitions/models/processed/hands_on_master_cl.sqlx` — query principal (la que tenés que escribir)
- `terraform/main.tf` — Dataform workflow + cron schedule

**Cuándo tocarlo**: Cada vez que necesitás una feature nueva o cambiás una transformación.

---

## File Ingestor (`services/file-ingestor-ga4/`)

**Qué hace**: Ingesta archivos Parquet desde un GCS bucket origen hacia una tabla raw en BigQuery. Es el "puente" entre archivos planos y BQ.

**Input**: Parquet files en GCS (eventos de Google Analytics 4).

**Output**: Tabla `iniciales_nombreapellido_ob_raw_mst_all_hits` en BigQuery.

**Archivos clave**:
- `schemas/biglake_table.json` — schema de la tabla (copia del de `new-hire-integration/assets/`)
- `terraform/main.tf` — pipeline de ingesta
- `terraform/custom_infrastructure.tf` — permisos especiales (dar `roles/storage.objectUser` a `hands-on-bqo-sa`)

**Cuándo tocarlo**: Si cambian los archivos de GA4 o agregás otra fuente Parquet.

---

## Vertex Pipelines ML (`services/ml-propension/`)

**Qué hace**: Entrena y sirve un modelo de clasificación (XGBoost o similar) que predice la propensión de compra de cada cliente.

**Input**: Tabla `hands_on_master_cl` (del componente Data).

**Output**: 
- Modelo en Vertex Model Registry
- Predicciones en BigQuery (`customer_predictions`)
- Métricas en MLflow (accuracy, precision, recall, F1, AUC)
- Reportes de drift, backtesting, data quality

**Archivos clave**:
- `pipelines/training_pipeline.py` — pipeline completo de training
- `pipelines/serving_pipeline.py` — pipeline de predicción batch
- `pipelines/drift_pipeline.py` — drift detection (pipeline independiente)
- `pipelines/backtesting_pipeline.py` — backtesting con datos históricos
- `components/*.py` — cada paso del pipeline (get_master_data, preprocessing, train_model, etc.)
- `mlflow_config.py` — setup de MLflow
- `vertex_config.py` — config de Vertex AI

**Componentes del training pipeline** (orden):
1. `get_master_data` — lee `hands_on_master_cl` de BQ
2. `preprocessing` — limpia, normaliza, hace feature engineering
3. `train_model` — entrena XGBoostClassifier, loggea métricas a MLflow
4. `postprocessing` — guarda modelo en Vertex Model Registry

**Componentes del serving pipeline**:
1. `get_serving_data` — lee tabla de serving (puede ser la misma master + filtro temporal)
2. `preprocessing_serving` — mismo preprocessing que training (consistencia crítica)
3. `serve_predictions` — carga modelo del registry, predice, loggea serving data a metadata store
4. `postprocessing_serving` — enriquece con info del cliente, escribe a `customer_predictions`

**Métricas objetivo** (del enunciado): accuracy > 0.7, precision > 0.65.

**Cuándo tocarlo**: Si cambiás el modelo, las features, o la lógica de predicción.

---

## Light RAG (`infra/` → módulo `light_rag`)

**Qué hace**: Servicio de RAG (Retrieval-Augmented Generation) sobre PDFs almacenados en el bucket. Indexa documentos y permite consultas en lenguaje natural.

**Input**: PDFs en `gs://<bucket>/files/`.

**Output**: Endpoint HTTP que responde consultas con respuesta + fuentes citadas.

**Configuración** (en `infra/environments/dev/main.tf`):
- `gcs_folder`: ruta a los PDFs
- `ingestor_scheduler`: cron de ingesta automática (`30 8 1 * *` = día 1 de cada mes a las 08:30)
- `ingestion_mode`: `STRICT` (valida schema) o `LOOSE`
- `genai_gateway_url`: URL del GenAI Gateway de Cosmos

**Inspector compartido**: `https://lightrag-inspector-cr-1024012608689.us-east1.run.app/`

**Cuándo tocarlo**: Cambios de configuración (región, schedule, modo de ingesta).

---

## Chatbot Backend (`services/chatbot-backend/`)

**Qué hace**: API conversacional con LangGraph. Recibe un mensaje del usuario, decide si buscar en documentos (Light RAG) o consultar predicciones ML, y devuelve una respuesta en lenguaje natural.

**Input**: Mensaje del usuario (string).

**Output**: Respuesta del agente (string + opcionalmente fuentes).

**Archivos clave**:
- `app/agent/graph.py` — StateGraph de LangGraph (router + tools)
- `app/agent/router.py` — lógica de routing (qué tool usar)
- `app/agent/state.py` — estado del agente (mensajes, contexto)
- `app/tools/lightrag_tool.py` — tool que consulta Light RAG
- `app/tools/ml_predictions_tool.py` — tool que consulta predicciones ML
- `app/api/chat.py` — endpoint HTTP `POST /chat`
- `application.yaml` — config (URLs, timeouts)

**Tools del agente**:
- `document_search` (Light RAG) — para preguntas sobre políticas, procedimientos, documentos
- `propension_lookup` (ML) — para preguntas sobre clientes específicos: "¿cuál es la propensión de X?"

**Cuándo tocarlo**: Cambios en el routing, nuevas tools, cambios en el prompt del agente.

---

## Frontend (`frontend/`)

**Qué hace**: UI del chatbot (chat window minimalista).

**Stack**: React + Vite + TypeScript (template estándar de Cosmos Frontend).

**Endpoint**: apunta a `https://<chatbot-backend-url>/chat`.

**Cuándo tocarlo**: Casi nunca. El template te da una UI funcional.

---

## Cloud Run Job (`data-to-bucket/`)

**Qué hace**: Job batch que toma predicciones ML de BigQuery y las escribe al bucket en formato que Light RAG pueda indexar.

**Input**: Tabla `customer_predictions` de BigQuery.

**Output**: Archivos (CSV/Parquet) en `gs://<bucket>/data/`.

**Cuándo correrlo**: Después de cada serving pipeline (podés triggerearlo desde Vertex AI como paso final).

---

## Resumen visual

```
┌─────────────────────────────────────────────────────┐
│                    GCP Project                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Dataflow │  │  ML      │  │  GenAI   │          │
│  │(BQO+FI)  │→ │ (Vertex) │→ │ (LangGr) │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│       ↓              ↓              ↓               │
│   [BigQuery]    [Model Reg]   [Cloud Run chatbot]   │
│       ↓              ↓              ↓               │
│       └──────────────┴──────────────┘               │
│                      ↓                              │
│              [Light RAG] (PDFs)                     │
└─────────────────────────────────────────────────────┘
```

---

**Siguiente**: [`03-fuentes-datos.md`](./03-fuentes-datos.md) — qué datos usás y cómo pedirlos.
