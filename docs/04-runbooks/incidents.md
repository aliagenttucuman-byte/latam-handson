# Runbook — Incidentes en Producción

**Este es el runbook para cuando algo se rompe en prod.** Para problemas del día a día durante el hands-on, mirá [`../00-onboarding/05-runbook.md`](../00-onboarding/05-runbook.md).

## Estructura del runbook

Cada incidente tiene:
- **Síntoma**: cómo se manifiesta
- **Diagnóstico**: cómo confirmar la causa
- **Mitigación inmediata**: qué hacer ahora
- **Solución permanente**: qué hacer después

---

## INC-001: Pipeline de serving no ejecuta

**Síntoma**: Las predicciones no se actualizan en `customer_predictions`. Vertex AI muestra error en el último run.

**Diagnóstico**:
```bash
# 1. Mirá el último run en Vertex AI → Pipelines
# 2. Identificá qué componente falló
# 3. Mirá los logs de ese componente
```

**Mitigación inmediata**:
- Si es error de permisos: reejecutá con la SA correcta
- Si es error de query: revisá el SQL del componente `get_master_data`
- Si es timeout: subí el límite en la config del pipeline

**Solución permanente**:
- Agregá retry policy al componente
- Agregá alertas en Cloud Monitoring

---

## INC-002: Light RAG no responde (5xx)

**Síntoma**: El chatbot devuelve "Error consultando documentos" o timeout.

**Diagnóstico**:
```bash
# 1. Mirá los logs del Cloud Run de Light RAG
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=light-rag" --limit 50

# 2. Verificá que el servicio esté corriendo
gcloud run services describe light-rag --region=us-east1
```

**Mitigación inmediata**:
- Si el servicio está down: re-deployá
- Si es error de GenAI Gateway: esperá, es un servicio compartido

**Solución permanente**:
- Agregá circuit breaker en el chatbot (si Light RAG falla 3 veces, no lo llama más)
- Configurá alertas de latencia

---

## INC-003: Drift detectado en producción

**Síntoma**: El pipeline de drift marca un feature con `p_value < 0.05`.

**Diagnóstico**:
1. Identificá qué feature tiene drift (mirar el log del pipeline)
2. Verificá si es drift natural (temporada) o de datos (bug)
3. Compará la distribución con un período histórico equivalente

**Mitigación inmediata**:
- Si es real: reentrená el modelo con datos recientes
- Si es falso positivo: subí el threshold o agregá más datos de baseline

**Solución permanente**:
- Configurá alertas automáticas a Slack/email cuando drift > threshold
- Documentá la causa raíz

---

## INC-004: Permisos denegados en BQO

**Síntoma**: El pipeline de BQO falla con `Permission denied` en alguna de las 6 fuentes.

**Diagnóstico**:
```bash
# Verificá que la SA tenga el rol correcto
gcloud projects get-iam-policy <project> \
  --flatten="bindings[].members" \
  --filter="bindings.members:<sa-email>"
```

**Mitigación inmediata**:
- Si falta el rol: pedíselo a tu Staff (no lo asignes vos en prod)
- Si la SA es incorrecta: reasigná en la config del workflow

**Solución permanente**:
- Documentá los permisos requeridos en `services/bigquery-orchestrator/README.md`
- Agregá validación pre-flight en el pipeline

---

## Escalación

| Severidad | Tiempo de respuesta | Quién escala |
|---|---|---|
| **P1** (servicio caído) | 15 min | Oncall + Staff |
| **P2** (degradado) | 1 hora | Buddy + Staff |
| **P3** (bug menor) | 1 día hábil | Buddy |

**Si no sabés la severidad**: asumí P2 y escalá.

---

## Comunicación

**Durante el incidente**:
1. Abrí un thread en #cosmos-incidents
2. Cada 30 min: update de status
3. Cuando se resuelva: post-mortem (incluso si fue simple)
