# 05 — Runbook (Problemas Comunes y Soluciones)

Guía rápida para resolver los problemas más frecuentes del hands-on. Si después de leer esto seguís trabado, escalá a tu Buddy o abrí un ticket.

---

## 1. Pipeline de Terraform falla en `plan`

### Síntoma
```
Error: Error acquiring the state lock
```
o
```
Error: Failed to read module"
```

### Solución
1. Mirá el log completo del job `plan:dev`
2. Si es "state lock": otro job está corriendo en paralelo. Esperá 5 min.
3. Si es "Failed to read module": verificá que el source del módulo exista y que el `ref=tags/latest` sea válido.
4. Si es "Variable not set": andá a `terraform.tfvars` y completá la variable que falta.

---

## 2. File Ingestor no ingesta archivos

### Síntoma
El pipeline corre verde pero no aparecen datos en la tabla `mst_all_hits`.

### Solución
1. Verificá que haya archivos Parquet en el bucket origen:
   ```bash
   gsutil ls gs://<origen-bucket>/
   ```
2. Andá a Dataform Studio → workspace del BQO → ejecutá el workflow con tag `file-ingestor-hands-on`
3. Si falla: revisá los logs de Dataform (panel inferior)
4. Si pasa pero la tabla está vacía: verificá el schema en `services/file-ingestor-ga4/schemas/biglake_table.json` — tiene que coincidir con el Parquet

---

## 3. Permisos denegados al leer tabla fuente

### Síntoma
```
Permission denied: user @<sa>.iam.gserviceaccount.com does not have bigquery.tables.get on table <tabla>
```

### Solución
1. Verificá que hayas solicitado el acceso en Data Hub
2. Verificá que la SA `nelson-acosta-ob-bqo-sa@<project>.iam.gserviceaccount.com` tenga `roles/bigquery.dataViewer`
3. Si la SA no tiene el rol: pedíselo a tu Staff (no lo hagas vos mismo en prod)

```bash
# Para verificar
gcloud projects get-iam-policy <project> \
  --flatten="bindings[].members" \
  --filter="bindings.members:nelson-acosta-ob-bqo-sa"
```

---

## 4. Drift detection no detecta drift real

### Síntoma
El pipeline de drift corre verde pero en realidad hay drift en los datos.

### Solución
1. Verificá que la tabla de referencia (baseline) sea la correcta
2. Verificá que las features comparadas sean las mismas en baseline y serving
3. Ajustá los thresholds en el código:
   - **KS test**: p_value > 0.05 = drift (recomendado)
   - **PSI**: > 0.2 = drift significativo
   - **Wasserstein**: > 0.1 = drift (en distribuciones similares)
4. Mirá la documentación interna: MLOps/data-drift

---

## 5. Light RAG no responde

### Síntoma
El endpoint `/query` de Light RAG devuelve 500 o timeout.

### Solución
1. **Verificá que los PDFs estén en el bucket**:
   ```bash
   gsutil ls gs://<bucket>/files/
   ```
2. **Verificá que la ingesta se ejecutó**:
   - Andá a Cloud Run → servicio Light RAG → logs
   - Buscá `Ingestion completed` o errores
3. **Si la ingesta nunca corrió**: triggereala manual desde Cloud Scheduler
4. **Si el error es de permisos**: verificá que la SA de Light RAG tenga `roles/storage.objectViewer` en el bucket
5. **Si el error es timeout**: subí el timeout en la config de Light RAG (variable de Terraform)

---

## 6. Chatbot no encuentra tools

### Síntoma
El agente LangGraph responde "No tengo acceso a esa información" o "Tool not found".

### Solución
1. Verificá que las tools estén registradas en `app/agent/graph.py`
2. Verificá que la URL de Light RAG en `application.yaml` sea correcta y accesible
3. Verificá que la query SQL de `ml_predictions_tool` sea válida (testeala en BigQuery directo)
4. Mirá los logs del Cloud Run del chatbot — debería loggear qué tool llamó

---

## 7. Modelo con accuracy < 0.7

### Síntoma
El training pipeline corre verde pero el modelo no llega a la métrica objetivo.

### Solución
1. **Features**: ¿estás usando TODAS las fuentes? Si te falta alguna, el modelo pierde señal.
2. **Target**: ¿estás bien definiendo el target? 
   - Mal: "¿compró alguna vez?" (sesgado, casi siempre True)
   - Bien: "¿compró en los próximos 30 días desde X fecha?" (predictivo)
3. **Class imbalance**: si el target está desbalanceado, probá:
   - `class_weight='balanced'` en XGBoost
   - SMOTE en el preprocessing
4. **Hiperparámetros**: corré un `RandomSearchAlgorithm` o `GridSearchAlgorithm` con `optimization.py` (mirá `services/ml-propension/pipelines/`)
5. **Más datos**: usá un histórico más largo (1 año en vez de 3 meses)

---

## 8. Pipeline de Vertex AI no se ejecuta

### Síntoma
El MR mergea pero el pipeline de Vertex AI no aparece en la UI.

### Solución
1. Verificá que el Dockerfile compile: 
   ```bash
   docker build -t test .
   ```
2. Verificá que `requirements.txt` tenga todas las dependencias
3. Verificá que el servicio account de Vertex AI tenga `roles/aiplatform.user`
4. Andá a Vertex AI Pipelines → tu repo → "Run" manual con la imagen compilada

---

## 9. Frontend no se conecta al backend

### Síntoma
El chatbot UI muestra error de CORS o "Failed to fetch".

### Solución
1. Verificá la URL del backend en `frontend/src/services/api.ts`
2. Verificá que el backend tenga CORS abierto para el dominio del frontend:
   ```python
   # En services/chatbot-backend/app/main.py
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # O el dominio específico
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
3. Verificá que el Cloud Run del chatbot tenga `--allow-unauthenticated` (o auth configurada)

---

## 10. Sandbox se borró antes de tiempo

### Síntoma
Los recursos GCP desaparecieron, MR falla con "project not found".

### Solución
1. El sandbox tiene un TTL de 30 días
2. Si te lo borraron antes, tenés que crear uno nuevo (mismo template)
3. **Lección**: hacé commit diario. NO confíes en que el sandbox va a estar.

---

## Escalación

Si después de probar estas soluciones seguís trabado:

1. **Preguntale a tu Buddy** (saben del hands-on)
2. **Preguntale a Carmen Pedrique** (Booster, conoce el contexto)
3. **Canal #cosmos-help** en Slack
4. **Abrí un ticket** en el portal de staff (último recurso)

**No te quemes 4 horas en un error de Terraform.** Si en 30 min no lo resolvés, escalá.
