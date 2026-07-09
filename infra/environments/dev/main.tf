terraform {
  required_version = ">= 1.5.0"
  
  backend "gcs" {
    # TODO: Configurar el bucket de state en GCP.
    # Cada ambiente (dev, prod) tiene su propio state.
    # Formato típico: <project>-terraform-state/<env>/terraform.tfstate
    # Ejemplo para dev:
    #   bucket = "dataplatforms-tools-prod-79e1_cosmos-terraform-state"
    #   prefix = "nelson-acosta-ob/infrastructure/dev"
  }
}

provider "google" {
  project = var.project_ids[terraform.workspace]
  region  = var.gcp_region
}

# ─────────────────────────────────────────────────────────────────────────
# Módulo: Service Account del producto
# ─────────────────────────────────────────────────────────────────────────
# TODO: Crear la SA principal del producto.
# Esta SA la usan TODOS los servicios (BQO, Light RAG, chatbot, etc).
# En LATAM, el módulo de Cosmos ya la crea con los roles estándar.

# module "service_account" {
#   source = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//service_account?ref=tags/latest"
#   project_id   = var.project_ids[terraform.workspace]
#   product_name = var.product_name
#   team         = var.team
# }

# locals {
#   sa_email = "${var.product_name}-sa@${var.project_ids[terraform.workspace]}.iam.gserviceaccount.com"
# }


# ─────────────────────────────────────────────────────────────────────────
# Módulo: GCS Bucket (raw, processed, files de RAG)
# ─────────────────────────────────────────────────────────────────────────
# TODO: Crear el bucket para landing de File Ingestor + documentos RAG.
# Módulo de Cosmos: gcs_bucket (envuelve google_storage_bucket con naming estándar).

module "gcs_bucket" {
  source       = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//gcs_bucket?ref=tags/latest"
  project_id   = var.project_ids[terraform.workspace]
  bucket_name  = "propension-data-bucket"
  product_name = var.product_name
  team         = var.team
  
  # TODO: Configurar lifecycle, versioning, retention según política LATAM.
  # lifecycle_rules, force_destroy, etc.
}


# ─────────────────────────────────────────────────────────────────────────
# Módulo: IAM del bucket
# ─────────────────────────────────────────────────────────────────────────
# TODO: Dar permisos a usuarios/SA que necesitan acceso al bucket.
# Mínimo: tu usuario LATAM + la SA de BQO.

module "gcs_bucket_iam" {
  source  = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//gcs_bucket_iam?ref=tags/latest"
  bucket  = module.gcs_bucket.bucket_name
  members = [
    # TODO: Reemplazar con tu email real de LATAM
    # "user:tu-email@latam.com",
    # TODO: SA del BQO (se crea con el template de BQO, no acá)
    # "serviceAccount:nelson-acosta-ob-bqo-sa@${var.project_ids[terraform.workspace]}.iam.gserviceaccount.com",
  ]
}


# ─────────────────────────────────────────────────────────────────────────
# Módulo: BigQuery Dataset
# ─────────────────────────────────────────────────────────────────────────
# TODO: Crear el dataset "processed" donde van las features.

# module "bigquery_dataset" {
#   source             = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//bigquery_dataset?ref=tags/latest"
#   project_id         = var.project_ids[terraform.workspace]
#   dataset_id         = "nelson-acosta_ob_processed"  # guiones bajos, no guiones
#   dataset_description = "Dataset for customer propension analysis"
#   product_name       = var.product_name
#   team               = var.team
# }


# ─────────────────────────────────────────────────────────────────────────
# Módulo: BigQuery Table (predicciones ML)
# ─────────────────────────────────────────────────────────────────────────
# TODO: Crear la tabla customer_predictions.
# Schema: customer_id (STRING), propensity_score (FLOAT), predicted_at (TIMESTAMP).

# module "bigquery_table" {
#   source          = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//bigquery_table?ref=tags/latest"
#   project_id      = var.project_ids[terraform.workspace]
#   dataset_id      = "nelson_acosta_ob_processed"
#   table_id        = "customer_predictions"
#   table_description = "Customer propension predictions from ML model"
#   product_name    = var.product_name
#   team            = var.team
#   schema = jsonencode([
#     { name = "customer_id",       type = "STRING" },
#     { name = "propensity_score",  type = "FLOAT" },
#     { name = "predicted_at",      type = "TIMESTAMP" },
#     { name = "model_version",     type = "STRING" },
#   ])
# }


# ─────────────────────────────────────────────────────────────────────────
# Módulo: Light RAG (Cloud Run + Cloud Scheduler + IAM)
# ─────────────────────────────────────────────────────────────────────────
# TODO: Agregar este módulo para tener RAG sobre PDFs en el bucket.
# Documentación del módulo: terraform-modules-cosmos-common/infrastructure/light_rag

# locals {
#   underscore_product_name = replace(var.product_name, "-", "_")
# }

# module "light_rag" {
#   source = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//infrastructure/light_rag?ref=tags/1.240.1"
#   
#   project_id   = var.project_ids[terraform.workspace]
#   gcp_region   = var.gcp_region
#   product_name = var.product_name
#   team         = var.team
#   
#   location                = "us-east1"
#   gcs_folder              = "gs://${module.gcs_bucket.bucket_name}/files"
#   default_service_account = local.sa_email
#   genai_gateway_url       = "https://genai.cosmos.dev.appslatam.com"
#   
#   ingestor_scheduler = "30 8 1 * *"  # Día 1 de cada mes a las 08:30
#   ingestion_mode     = "STRICT"
# }


# ─────────────────────────────────────────────────────────────────────────
# Outputs
# ─────────────────────────────────────────────────────────────────────────
# TODO: Exportar lo que otros módulos/repos necesitan consumir.

# output "bucket_name" {
#   value = module.gcs_bucket.bucket_name
# }
# 
# output "light_rag_url" {
#   value = module.light_rag.service_url
# }
