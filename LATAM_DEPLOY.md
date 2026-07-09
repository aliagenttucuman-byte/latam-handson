# LATAM_DEPLOY.md — Chuleta de Migración a Cosmos Real

**Esta es la guía paso a paso que seguís el día que arranques el hands-on en el sandbox GCP real de LATAM.**

---

## Pre-flight (antes de empezar)

- [ ] Tenés usuario LATAM con acceso a GitLab
- [ ] Tenés el GCP Sandbox creado (Template → "Sandbox" → nombre `nelson-acosta-ob`)
- [ ] Tenés permisos de Owner en el proyecto GCP `nelson-acosta-ob-dev`
- [ ] Tenés acceso al Cosmos Catalog (`https://catalog.cosmos...`)
- [ ] Sabés tu **dominio** y **equipo** (preguntale a Carmen Pedrique o tu Buddy)
- [ ] Tenés los IDs de proyecto dev y prod anotados:
  - `dev_project_id`: `___________________`
  - `prod_project_id`: `___________________`

---

## PASO 1 — Crear el Producto en Cosmos Catalog

**DÓNDE**: Cosmos Catalog → buscar template **"Product"**

**DATOS**:
```
Product Name:           nelson-acosta-ob
Branch Strategy:        default (GitFlow)
Environments:           dev, prod
Project Mapping:
  dev  → <dev_project_id>
  prod → <prod_project_id>
Team:                   <tu equipo de dominio>
```

**RESULTADO**: Se crea un repo GitLab en el grupo de tu dominio, y un folder en el bucket `dataplatforms-tools-prod-79e1_cosmos-service-management` con el `product_definition.json`.

**VERIFICAR**:
```bash
# 1. Andá a Google Cloud Console → Cloud Storage → bucket transversal
# 2. Buscá el folder: nelson-acosta-ob/
# 3. Adentro tiene que estar: product_definition.json
```

---

## PASO 2 — Crear el Repo de Infraestructura

**DÓNDE**: Cosmos Catalog → buscar template **"Terraform Infrastructure"**

**DATOS**:
```
Product Name:     nelson-acosta-ob
Service Name:     infrastructure
GitLab Group ID:  <ID de tu grupo en GitLab>
Team:             <tu equipo>
Domain Variables: default
Approval on Prod: ✅ activado
```

**RESULTADO**: Se crea un repo GitLab con la estructura `infra/`.

**VERIFICAR**:
```bash
# Cloná el repo
git clone git@gitlab.com:<grupo>/nelson-acosta-ob-infrastructure.git
cd nelson-acosta-ob-infrastructure

# Verificá que existe la rama develop
git branch -a
# Si no existe:
git checkout -b develop
git push origin develop

# Verificá el CI/CD (debería haber un .gitlab-ci.yml)
cat .gitlab-ci.yml
```

---

## PASO 3 — Implementar Infraestructura Base (Terraform)

**ACÁ EMPIEZA EL TRABAJO REAL.** Mirá `infra/environments/dev/main.tf` (placeholder en este repo) y reemplazá los TODOs con los módulos reales de LATAM.

**MÓDULOS DE TERRAFORM DE COSMOS** (todos en `terraform-modules-cosmos-common`):

| Recurso | Módulo | Uso |
|---|---|---|
| Bucket GCS | `gcs_bucket` | Almacena archivos crudos (Parquet) + documentos RAG |
| IAM del bucket | `gcs_bucket_iam` | Permisos de lectura/escritura |
| Dataset BigQuery | `bigquery_dataset` | Capa processed y staging |
| Tabla BigQuery | `bigquery_table` | Tabla de predicciones ML |
| Light RAG | `infrastructure/light_rag` | Cloud Run + Cloud Scheduler + IAM |
| Service Account | `service_account` | SA del producto |
| Cloud Run | `cloudrun` | Para servicios backend |

**FLUJO**:
```bash
# En el repo de infraestructura
git checkout develop
git checkout -b feature/cosmos-infra

# Editá infra/environments/dev/main.tf (siguiendo el placeholder)
# Editá infra/environments/dev/variables.tf
# Editá infra/environments/dev/terraform.tfvars

# Commit
git add .
git commit -m "feat: Implement infrastructure using Cosmos modules"
git push origin feature/cosmos-infra
```

**PIPELINE**:
- Andá a GitLab → tu repo → Build → Pipelines
- Verificá que el `terraform plan` corra sin errores
- Si está verde, abrí un **Merge Request** a `develop`
- Título: `feat: Implement infrastructure using Cosmos modules`
- Descripción: referenciar el hands-on y el template
- Pedile aprobación a tu Buddy/Staff
- Después de aprobar, merge a `develop`
- Verificá que el pipeline post-merge corra

**VERIFICAR EN GCP**:
- BigQuery → `nelson-acosta-ob_processed` dataset (creado)
- BigQuery → tabla `customer_predictions` (creada)
- Cloud Storage → bucket `propension-data-bucket` (creado con labels Cosmos)
- IAM → permisos aplicados

---

## PASO 4 — Crear Servicio BQO

**DÓNDE**: Cosmos Catalog → buscar template **"Install BigQuery Orchestrator 2.0"**

**DATOS**:
```
Product Name: nelson-acosta-ob
Team:         <tu equipo>
```

**RESULTADO**: Se crea repo `nelson-acosta-ob-bigquery-orchestrator` con Dataform configurado.

**ACÁ VA TU TRABAJO**:
- Mirá `services/bigquery-orchestrator/definitions/declarations/all_declarations.sqlx` (placeholder en este repo)
- Creá un `.sqlx` por cada fuente de datos
- Mirá `services/bigquery-orchestrator/definitions/models/processed/hands_on_master_cl.sqlx` (placeholder)
- Reemplazá los TODOs con SQL real
- Configurá el cron en `services/bigquery-orchestrator/terraform/main.tf`

---

## PASO 5 — Crear Servicio File Ingestor (GA4)

**DÓNDE**: Cosmos Catalog → buscar template **"File Ingestor"**

**DATOS**:
```
Product Name:           nelson-acosta-ob
Service Name:           file-ingestor-ga4
Team:                   <tu equipo>
Approval on Prod:       ✅
Landing Bucket Strategy: Create new bucket
Dataset ID:             iniciales_nombreapellido_ob_raw_mst_all_hits
Dataset Description:    Raw GA4 historical events data for propension analysis
```

**ACÁ VA TU TRABAJO**:
- Mirá `services/file-ingestor-ga4/schemas/biglake_table.json` (placeholder)
- Reemplazá con el schema real de GA4 (`new-hire-integration/assets/biglake_table.json`)
- Otorgá permisos IAM en `services/file-ingestor-ga4/terraform/custom_infrastructure.tf`
- Corré el pipeline de ingesta desde Dataform Studio

---

## PASO 6 — Solicitar Permisos de Fuentes de Datos

**DÓNDE**: https://data-management.appslatam.com/

**CASO DE USO**: "Desarrollo de modelo de propensión de compra para onboarding Cosmos"

**JUSTIFICACIÓN**: "Acceso requerido para entrenamiento de modelo ML como parte del hands-on de onboarding"

**FUENTES A SOLICITAR** (las 6 que pide el enunciado):

| Fuente | Para qué la usás |
|---|---|
| `ebiz-data-prod.ebiz_google_analytics_4` | Comportamiento web histórico |
| `dlakedomain-prod-20dl.dmt_commercial_us` | Ventas, reservas, compras |
| `dlakedomain-prod-20dl.dmt_reference_us` | Rutas, aeropuertos, productos |
| `cus-data-prod.dmt_customer_us` | Segmentación de clientes |
| `cus-data-prod.customer_management` | Identidad única de clientes |
| `cus-data-prod.customer_marketing` | Campañas de marketing |

**⚠️ El proceso tarda 1-2 días hábiles.** Solicitá AL INICIO, no al final.

---

## PASO 7 — Crear Servicio ML (Vertex Pipelines)

**DÓNDE**: Cosmos Catalog → buscar template **"Cosmos Vertex Pipelines Project"**

**DATOS**:
```
Product Name:     nelson-acosta-ob
Service Name:     ml-propension
GitLab Group ID:  <ID>
Team:             <tu equipo>
Approval on Prod: ✅
```

**ACÁ VA TU TRABAJO** (lo más denso del hands-on):
- Mirá `services/ml-propension/pipelines/training_pipeline.py` (placeholder)
- Mirá `services/ml-propension/components/*.py` (placeholders)
- Adaptá el notebook de entrenamiento (link en el enunciado) a Vertex Pipelines
- Configurá MLflow para loggear métricas
- Hacé lo mismo con `serving_pipeline.py`
- Implementá `data_drift.py`, `data_quality.py`, `backtesting.py`

**MÉTRICAS OBJETIVO**: Accuracy > 0.7, Precision > 0.65

---

## PASO 8 — Crear Servicio GenAI (Chatbot)

**DÓNDE**: Cosmos Catalog → buscar template **"GenAI Project Bundle"**

**DATOS**:
```
Product Name:           nelson-acosta-ob
Service Name:           chatbot-backend
Application Type:       chat
Database for Memory:    ❌
RAG:                    ❌ (usamos Light RAG como tool)
Team:                   <tu equipo>
```

**ACÁ VA TU TRABAJO**:
- Mirá `services/chatbot-backend/app/agent/graph.py` (placeholder LangGraph)
- Mirá `services/chatbot-backend/app/tools/lightrag_tool.py` (placeholder)
- Mirá `services/chatbot-backend/app/tools/ml_predictions_tool.py` (placeholder)
- Reemplazá TODOs con código real
- Configurá la URL de Light RAG en `application.yaml`

---

## PASO 9 — Crear Light RAG (dentro de infra)

**ACÁ**: En el repo de infraestructura, agregá el módulo Light RAG a `infra/environments/dev/main.tf`.

**Mirá** el bloque marcado con `# TODO: Light RAG module` en el placeholder. El módulo es:
```hcl
module "light_rag" {
  source = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//infrastructure/light_rag?ref=tags/1.240.1"
  # ... variables (mirá el placeholder)
}
```

**DESPUÉS**:
- Subí PDFs de prueba al bucket (`gsutil cp *.pdf gs://<bucket>/files/`)
- Triggereá la ingesta manual desde Cloud Scheduler
- Probá con el Inspector: `https://lightrag-inspector-cr-1024012608689.us-east1.run.app/`

---

## PASO 10 — Frontend (opcional)

**DÓNDE**: Cosmos Catalog → buscar template **"Frontend Template"**

**DATOS**:
```
Product Name:  nelson-acosta-ob
Service Name:  chatbot-frontend
Template Type: chatbot
Team:          <tu equipo>
```

**ACÁ VA TU TRABAJO**:
- Mirá `frontend/src/App.tsx` (placeholder)
- Reemplazá con la URL del chatbot backend

---

## CHECKLIST FINAL

- [ ] Producto creado en Cosmos Catalog
- [ ] Repo de infra clonado, MR mergeado
- [ ] Bucket + dataset + tabla visibles en GCP
- [ ] Servicio BQO creado, pipeline inicial corriendo
- [ ] Servicio File Ingestor creado, GA4 ingestado
- [ ] Permisos de 6 fuentes solicitados (y aprobados)
- [ ] Servicio ML creado, training pipeline corre, métricas loggeadas
- [ ] Drift detection implementado
- [ ] Light RAG desplegado, PDFs ingestados
- [ ] Chatbot backend desplegado, responde a /chat
- [ ] Frontend conectado al backend
- [ ] Demo end-to-end funciona: "¿Cuál es la propensión del cliente X?" + "¿Cuáles son las políticas de equipaje?"

---

## Cleanup (cuando termine el hands-on)

El sandbox se borra solo a los 30 días. Si querés borrarlo antes:
```bash
# Andá a Cloud Project Manager (CPM)
# Buscá tu proyecto
# Click en "Delete"
```

---

**DURANTE TODO EL PROCESO**: Si te trabás, abrí un ticket o preguntale a tu Buddy/Staff. No te quemes horas en un error de Terraform.
