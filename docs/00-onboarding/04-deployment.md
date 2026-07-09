# 04 — Deployment (CI/CD en LATAM)

## Flujo de branches

LATAM usa **GitFlow** estándar:

```
main (protegida)
  └─ develop (default, integración)
      └─ feature/<nombre> (tu trabajo)
      └─ release/<version> (pre-prod)
      └─ hotfix/<nombre> (urgencias)
```

**Reglas**:
- `main` requiere 2 approvals + pipeline verde
- `develop` requiere 1 approval + pipeline verde
- `feature/*` no requiere approval para pushear
- MR de `feature` → `develop` requiere 1 approval

## Pipeline (`.gitlab-ci.yml`)

Cada repo de Cosmos tiene un pipeline estándar que ejecuta:

### Stage 1: `lint`
- Linter de Terraform (`tflint`)
- Linter de Python (`ruff`)
- Linter de SQL (`sqlfluff`)
- Linter de TypeScript (`eslint`) — solo frontend

### Stage 2: `test`
- Tests unitarios Python (`pytest`)
- Tests unitarios TypeScript (`vitest`)
- Validación de schemas JSON
- Validación de SQLx (compilación de Dataform)

### Stage 3: `build`
- Docker build (si aplica)
- Validación de Dockerfile
- Push a Artifact Registry (solo en `develop`/`main`)

### Stage 4: `plan` (Terraform)
- `terraform init`
- `terraform plan` con el workspace correspondiente
- Output como artifact del pipeline (descargable)
- **NO hace `apply`** — el apply es manual via MR

### Stage 5: `deploy` (manual)
- **Solo se ejecuta manualmente** desde la UI de GitLab
- `terraform apply` con el plan aprobado
- Crea/actualiza recursos en GCP

---

## Flujo típico de un cambio

### Para Terraform (infra)

```bash
# 1. Cloná el repo y creá tu branch
git clone git@gitlab.com:<grupo>/nelson-acosta-ob-infrastructure.git
cd nelson-acosta-ob-infrastructure
git checkout develop
git checkout -b feature/add-light-rag

# 2. Hacé tus cambios en infra/environments/dev/main.tf
# (referenciá el placeholder de este repo)

# 3. Commit + push
git add .
git commit -m "feat: add Light RAG module"
git push origin feature/add-light-rag

# 4. Abrí MR en GitLab
#    Source: feature/add-light-rag
#    Target: develop
#    Título: feat: add Light RAG module
#    Descripción: referenciar el hands-on

# 5. Esperá que el pipeline corra (lint + test + plan)
#    Si está rojo, mirá los logs y corregí

# 6. Pedí aprobación (Buddy/Staff)

# 7. Merge a develop → se ejecuta el deploy automático (si está configurado)
#    O ejecutá el job `deploy:dev` manualmente

# 8. Verificá en GCP que los recursos se crearon
```

### Para SQLx (BQO)

```bash
# Mismo flujo, pero el "test" valida la compilación de Dataform
# El "deploy" es el run del workflow (manual desde Dataform Studio)
```

### Para Python (ML, GenAI)

```bash
# Mismo flujo + tests unitarios
# El "deploy" es el build de Docker + push a Artifact Registry
# Cloud Run se actualiza con la nueva imagen (manual o automático con trigger)
```

---

## Environments y Workspaces

Terraform usa **workspaces** para separar dev y prod:

```bash
# El pipeline detecta el branch:
#   develop → workspace "dev"
#   main    → workspace "prod"
```

Los archivos de variables:
- `infra/environments/dev/terraform.tfvars` — valores dev
- `infra/environments/prod/terraform.tfvars` — valores prod

**NO mezcles valores entre ambientes.**

---

## Service Accounts (SAs)

Cada servicio tiene su propia SA con permisos limitados:

| Servicio | SA | Permisos |
|---|---|---|
| BQO | `<product>-bqo-sa` | `bigquery.dataViewer` + `bigquery.jobUser` |
| Light RAG | `<product>-sa` (compartida) | `storage.objectViewer` en bucket |
| ML (Vertex) | Default Compute Engine SA | `aiplatform.user` |
| Chatbot | `<product>-chatbot-sa` | `bigquery.dataViewer` + URL de Light RAG |

**Convención Cosmos**: el nombre de la SA es siempre `<product-name>-<service-suffix>-sa@<project>.iam.gserviceaccount.com`.

---

## Secrets

**NUNCA** commitees secretos al repo. Usá:

- **GitLab CI/CD Variables** (para secrets de CI): Settings → CI/CD → Variables
- **Secret Manager de GCP** (para secrets de runtime): en el código, leelos con `google-cloud-secret-manager`

**Secretos típicos**:
- API keys de LLM
- Credenciales de servicio
- URLs internas

---

## Merge Request (MR) Templates

Cada repo tiene templates en `.gitlab/merge_request_templates/`. Usá el `default.md`:

```markdown
## ¿Qué cambia?
- [descripción breve]

## ¿Por qué?
- [contexto / issue / ticket]

## ¿Cómo se prueba?
- [ ] Tests automatizados pasan
- [ ] Probado manualmente en dev

## Checklist
- [ ] Pipeline verde
- [ ] Documentación actualizada
- [ ] Sin secrets commiteados
- [ ] Sin archivos de configuración local (.env, etc.)
```

---

## Aprobaciones

| Cambio | Approvers requeridos |
|---|---|
| `feature/*` → `develop` | 1 Buddy o Staff del dominio |
| `develop` → `main` (prod) | 2 (1 Buddy + 1 Staff) |
| Hotfix → `main` | 1 Staff + oncall |
| Cambio en Terraform modules (en repo de Cosmos) | 2 Staffs del equipo ADO |

**Si no sabés quién es tu Staff**: preguntale a Carmen Pedrique o mirá el team roster en el repo de Cosmos.

---

## Troubleshooting común

### "Pipeline rojo en terraform plan"
- Mirá el log del job `plan:dev`
- 90% de las veces es una variable mal seteada en `terraform.tfvars`
- 10% es un módulo de Cosmos deprecado (verificá `tags/latest`)

### "MR pide approval y no tengo a quién"
- Pedí en el canal #cosmos-help de Slack
- O preguntale a tu Buddy directamente

### "Recurso GCP no se creó aunque el pipeline esté verde"
- Terraform es **declarativo**, no ejecuta después del apply si hay un error de IAM
- Andá a GCP Console y verificá que la SA del pipeline tenga permisos para crear ese recurso

### "Tengo conflictos en develop"
- `git fetch origin`
- `git rebase origin/develop` (si te da miedo, merge)
- Resolvé conflictos, pusheá de nuevo

---

**Siguiente**: [`05-runbook.md`](./05-runbook.md) — Runbook con problemas específicos del hands-on.
