# 0002 — Elección de Light RAG para RAG

**Status**: Aceptado  
**Fecha**: 2026-07-09  
**Contexto**: Hands-on onboarding Cosmos — componente GenAI

## Contexto

El chatbot necesita responder preguntas sobre documentos corporativos de LATAM (políticas, procedimientos, FAQs). Necesitamos un sistema RAG (Retrieval-Augmented Generation).

Opciones consideradas:
- **Vertex AI Search**: solución de Google, fácil de integrar, vendor lock-in.
- **Light RAG (LATAM)**: framework interno de LATAM, desplegado como Cloud Run, ya tiene integración con GenAI Gateway.
- **LangChain + ChromaDB en Cloud Run**: full custom, máximo control.
- **Haystack (deepset)**: open-source, maduro, pero requiere más setup.

## Decisión

**Light RAG** (el módulo de LATAM).

## Razones

1. **Estandarización**: es el estándar en LATAM. Otros equipos ya lo usan, hay soporte interno.
2. **Compliance**: ya está aprobado por el equipo de seguridad de LATAM (los PDFs no salen de LATAM).
3. **Integración con GenAI Gateway**: usa el gateway de LATAM para LLM, no hay que configurar API keys.
4. **Módulo Terraform oficial**: `terraform-modules-cosmos-common/infrastructure/light_rag` está mantenido por el equipo ADO.
5. **Costo**: $0 extra (corre en Cloud Run, escala a cero).
6. **Inspector compartido**: hay un inspector de LATAM para debuggear (`lightrag-inspector-cr-...run.app`).

## Consecuencias

### Positivas
- Setup rápido: una vez que el módulo de Terraform está aplicado, funciona.
- No hay que mantener embeddings store: Light RAG lo maneja.
- Scheduler de ingesta automática configurable.

### Negativas
- Vendor lock-in (interno): si Light RAG cambia de API, hay que actualizar.
- Menos flexible que un setup custom (no podemos elegir el modelo de embeddings, chunking, etc.).
- Dependencia del GenAI Gateway de LATAM (si se cae, el RAG se cae).

## Alternativas descartadas

- **Vertex AI Search**: vendor lock-in con Google, costo extra, y nos aleja del stack estándar de LATAM.
- **LangChain + ChromaDB custom**: más trabajo de setup y mantenimiento, sin ganancia clara para este caso.
- **Haystack**: requiere DevOps dedicado, no se justifica para el hands-on.

## Configuración aplicada

```hcl
# Módulo Terraform de Light RAG
module "light_rag" {
  source = "git@gitlab.com:latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common.git//infrastructure/light_rag?ref=tags/1.240.1"
  
  project_id            = var.project_ids[terraform.workspace]
  gcp_region            = var.gcp_region
  product_name          = var.product_name
  team                  = var.team
  
  location              = "us-east1"
  gcs_folder            = "gs://${module.gcs_bucket.bucket_name}/files"
  default_service_account = local.sa_email
  genai_gateway_url     = "https://genai.cosmos.dev.appslatam.com"
  
  ingestor_scheduler    = "30 8 1 * *"  # Día 1 de cada mes, 08:30
  ingestion_mode        = "STRICT"
}
```

## Referencias

- [Cosmos Terraform Modules - Light RAG](https://gitlab.com/latamairlines/data/data-ai-ops/cosmos/terraform-modules/terraform-modules-cosmos-common)
- [Light RAG Inspector](https://lightrag-inspector-cr-1024012608689.us-east1.run.app/)
