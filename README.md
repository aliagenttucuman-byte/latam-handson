# Data Product: nelson-acosta-ob

**Owner**: Nelson Acosta  
**Dominio**: (a confirmar con Carmen Pedrique / Buddy)  
**Status**: Onboarding Hands-On — En construcción

---

## ¿Qué es esto?

Este es el **kit de migración al hands-on de Cosmos**. Replica la estructura canónica de un Data Product de LATAM Airlines generado por los templates de Cosmos Catalog, con placeholders, documentación y la "chuleta" (`LATAM_DEPLOY.md`) que vas a usar el día que arranques en el sandbox real.

**No es código ejecutable.** Es un molde estructural para que sepas qué archivo tocar, qué variable setear, qué módulo de Terraform elegir, sin tener que abrir docs de LATAM el día del hands-on.

---

## Componentes

| Servicio | ¿Qué hace? | Estado |
|---|---|---|
| **infra/** | Repositorio de Terraform. Define el proyecto, bucket, dataset, tabla, Light RAG. | Placeholder |
| **services/bigquery-orchestrator/** | BQO. Pipeline de transformaciones SQLx (raw → processed). | Placeholder |
| **services/file-ingestor-ga4/** | Ingesta de Parquet desde GCS → tabla raw en BigQuery. | Placeholder |
| **services/ml-propension/** | Vertex AI Pipelines. Training + serving + DQ + drift + backtesting. | Placeholder |
| **services/chatbot-backend/** | LangGraph agent con tools (Light RAG + ML predictions). | Placeholder |
| **frontend/** | UI del chatbot (Streamlit / Gradio placeholder). | Placeholder |
| **data-to-bucket/** | Cloud Run Job: transfiere predicciones BQ → GCS para Light RAG. | Placeholder |

---

## Cómo usar este repo

1. **Hoy**: Leé `docs/00-onboarding/` para entender la arquitectura.
2. **Cuando tengas el sandbox GCP real**: Seguí `LATAM_DEPLOY.md` paso a paso.
3. **Durante el hands-on (2 semanas)**: Copiá los archivos de cada `services/<x>/` al repo generado por el template de Cosmos Catalog.

---

## Documentación

- [`LATAM_DEPLOY.md`](./LATAM_DEPLOY.md) — Chuleta de migración
- [`docs/00-onboarding/`](./docs/00-onboarding/) — Onboarding conceptual
- [`docs/01-arquitectura/`](./docs/01-arquitectura/) — Diagramas y arquitectura detallada
- [`docs/02-decisiones/`](./docs/02-decisiones/) — ADRs (Architecture Decision Records)
- [`docs/04-runbooks/`](./docs/04-runbooks/) — Resolución de problemas comunes
- [`services/*/README.md`](./services/) — Docs por servicio
