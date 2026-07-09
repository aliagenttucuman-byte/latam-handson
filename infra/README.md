# infra/ — Repositorio de Infraestructura (Terraform)

## ¿Qué hace?

Define TODOS los recursos GCP del producto: bucket, dataset, tabla, service accounts, IAM, Light RAG, etc. Usa los módulos de `terraform-modules-cosmos-common` (estándar de LATAM).

## Estructura

```
infra/
├── environments/
│   ├── dev/
│   │   ├── main.tf            # Recursos a crear (CON TODOs)
│   │   ├── variables.tf       # Declaración de variables
│   │   ├── terraform.tfvars   # Valores para dev
│   │   └── backend.tf         # Configuración del state
│   └── prod/
│       └── (mismo structure)
├── modules/
│   └── data-product/          # Custom (si tenés lógica propia)
├── .gitlab-ci.yml
└── README.md
```

## ¿Cómo crear este repo?

1. En Cosmos Catalog → buscar template **"Terraform Infrastructure"**
2. Llenar el formulario
3. El template genera un repo GitLab con esta estructura base
4. Reemplazá los archivos `environments/dev/*.tf` con los de este repo (los que tienen TODOs)

## Módulos de Terraform que vas a usar

Todos vienen de `terraform-modules-cosmos-common`:

| Módulo | Crea | Cuándo |
|---|---|---|
| `service_account` | SA del producto | Inmediato |
| `gcs_bucket` | GCS bucket | Inmediato |
| `gcs_bucket_iam` | Permisos del bucket | Después del bucket |
| `bigquery_dataset` | Dataset BQ | Después del bucket |
| `bigquery_table` | Tabla BQ | Después del dataset |
| `infrastructure/light_rag` | Cloud Run + Scheduler + IAM | Semana 2 (componente GenAI) |
| `cloudrun` | Cloud Run Service | Para chatbot backend |
| `cloudrun_job` | Cloud Run Job | Para data-to-bucket |

**IMPORTANTE**: NUNCA definas recursos GCP con `google_*` directo. SIEMPRE usá los módulos de Cosmos.

## Variables críticas

```hcl
# terraform.tfvars
project_ids = {
  dev  = "<tu-proyecto-dev>"
  prod = "<tu-proyecto-prod>"
}
gcp_region   = "us-east1"
product_name = "nelson-acosta-ob"
team         = "<tu-equipo>"
```

## Workflow típico

```bash
# 1. Clonar
git clone git@gitlab.com:<grupo>/nelson-acosta-ob-infrastructure.git
cd nelson-acosta-ob-infrastructure

# 2. Crear branch
git checkout develop
git checkout -b feature/cosmos-infra

# 3. Editar environments/dev/main.tf (reemplazar TODOs)
# 4. Editar environments/dev/variables.tf
# 5. Editar environments/dev/terraform.tfvars

# 6. Commit + push
git add .
git commit -m "feat: Implement infrastructure using Cosmos modules"
git push origin feature/cosmos-infra

# 7. Abrir MR a develop en GitLab

# 8. Esperar pipeline (lint + plan)
# 9. Si está verde, pedir approval
# 10. Merge

# 11. Verificar en GCP
```

## Verificación post-deploy

- [ ] BigQuery: `nelson_acosta_ob_processed` dataset visible
- [ ] BigQuery: `customer_predictions` tabla visible
- [ ] GCS: `propension-data-bucket` con labels Cosmos
- [ ] IAM: SA del producto tiene permisos correctos
- [ ] (Si agregaste Light RAG): Cloud Run service corriendo, Scheduler creado

## Referencias

- [LATAM_DEPLOY.md](../../LATAM_DEPLOY.md) — Paso a paso
- [Cosmos Terraform Modules](https://gitlab.com/latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common)
- [Cosmos Infrastructure Template](https://catalog.cosmos.../templates/terraform-infra)
