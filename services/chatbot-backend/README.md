# Chatbot Backend — LangGraph Agent

## ¿Qué hace?

API conversacional con un agente LangGraph que:
1. Recibe un mensaje del usuario
2. Decide si buscar en documentos (Light RAG) o consultar predicciones ML
3. Devuelve una respuesta en lenguaje natural

## Estructura

```
chatbot-backend/
├── app/
│   ├── main.py                # FastAPI app
│   ├── agent/
│   │   ├── graph.py           # StateGraph de LangGraph (el archivo principal)
│   │   ├── router.py          # Lógica de routing
│   │   └── state.py           # Estado del agente
│   ├── tools/
│   │   ├── lightrag_tool.py   # Tool de Light RAG
│   │   ├── ml_predictions_tool.py  # Tool de predicciones ML
│   │   └── base.py            # Clase base para tools
│   ├── api/
│   │   └── chat.py            # Endpoint POST /chat
│   └── core/
│       └── config.py          # Config (URLs, secrets, etc.)
├── tests/
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_api.py
├── application.yaml           # Config del Cloud Run
├── Dockerfile
├── requirements.txt
└── README.md
```

## ¿Qué archivos tocar?

1. **`app/agent/graph.py`** — Definir el StateGraph. Tiene TODOs marcados.
2. **`app/tools/lightrag_tool.py`** — Implementar la llamada HTTP a Light RAG.
3. **`app/tools/ml_predictions_tool.py`** — Implementar la query a BigQuery.
4. **`application.yaml`** — Setear las URLs (Light RAG, GCP project, etc.).

## Las 2 tools

### Tool 1: `document_search` (Light RAG)

- **Input**: query en lenguaje natural
- **Output**: respuesta + fuentes
- **Cuándo se usa**: preguntas sobre políticas, procedimientos, documentos

```python
light_rag_tool = Tool(
    name="document_search",
    description="Busca información en documentos corporativos de LATAM...",
    func=light_rag_search,
)
```

### Tool 2: `propension_lookup` (ML)

- **Input**: `customer_id` (string)
- **Output**: propensión de compra
- **Cuándo se usa**: preguntas sobre clientes específicos

```python
ml_predictions_tool = Tool(
    name="propension_lookup",
    description="Consulta la propensión de compra de un cliente específico...",
    func=get_propension_for_customer,
)
```

## Configuración

### `application.yaml`

```yaml
server:
  port: 8080

api:
  routes:
    - path: "/chat"
      method: "POST"

# URLs de servicios externos
light_rag:
  url: "https://<light-rag-service-url>"  # TODO: setear con tu URL
  timeout: 30
  max_results: 5

# GCP
gcp:
  project_id: "nelson-acosta-ob-dev"
  region: "us-east1"
  
# LLM (vía GenAI Gateway de LATAM)
llm:
  gateway_url: "https://genai.cosmos.dev.appslatam.com"
  model: "gpt-4"  # o el modelo que ofrezca el gateway
  temperature: 0.0
```

## Cómo correr local

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Variables de entorno
export LIGHT_RAG_URL="https://..."
export GCP_PROJECT_ID="nelson-acosta-ob-dev"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/sa.json"

# Run
uvicorn app.main:app --reload --port 8080
```

## Cómo deployar

1. Compilá la imagen Docker:
   ```bash
   docker build -t us-east1-docker.pkg.dev/nelson-acosta-ob-dev/chatbot/chatbot-backend:latest .
   ```

2. Subila a Artifact Registry:
   ```bash
   docker push us-east1-docker.pkg.dev/nelson-acosta-ob-dev/chatbot/chatbot-backend:latest
   ```

3. Deployá a Cloud Run (manual o vía CI/CD del template GenAI Bundle):
   - Service name: `chatbot-backend`
   - Image: la que subiste
   - Port: 8080
   - Env vars: las del `application.yaml`
   - Allow unauthenticated (si el front lo consume directo)

## Tests

```bash
# Unit tests
pytest tests/test_tools.py -v

# Agent tests
pytest tests/test_agent.py -v

# API tests
pytest tests/test_api.py -v
```

## Pruebas manuales

```bash
# 1. Test del LLM solo
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'

# 2. Test con Light RAG
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son las políticas de equipaje?"}'

# 3. Test con ML
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuál es la propensión de compra del cliente 12345?"}'
```

## Referencias

- [LangGraph docs](https://langchain-ai.github.io/langgraph/)
- [Cosmos GenAI Bundle template](https://catalog.cosmos.../templates/genai-bundle)
- [Light RAG Inspector](https://lightrag-inspector-cr-1024012608689.us-east1.run.app/)
