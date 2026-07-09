# 0003 — Elección de LangGraph para el agente GenAI

**Status**: Aceptado  
**Fecha**: 2026-07-09  
**Contexto**: Hands-on onboarding Cosmos — componente GenAI

## Contexto

El chatbot necesita decidir dinámicamente si responder una pregunta usando documentos (Light RAG) o consultando predicciones ML (BigQuery). Necesitamos un framework de agentes.

Opciones consideradas:
- **LangGraph**: framework de grafos de estado de LangChain, explícito, debuggeable.
- **LangChain Agent (legacy)**: menos explícito, deprecated a favor de LangGraph.
- **Haystack Pipelines**: poderoso pero verbose, pensado más para RAG puro.
- **Custom (FastAPI + lógica manual)**: máximo control, mucho más código.

## Decisión

**LangGraph** con un `StateGraph` simple (router + 2 tools).

## Razones

1. **Estándar en LATAM**: el template "GenAI Project Bundle" de Cosmos ya viene con LangGraph configurado.
2. **Explícito**: el routing es visible en el código, no es magia. Mejor para code review.
3. **Stateful**: el `AgentState` permite llevar contexto entre turns (memoria de la conversación).
4. **Integración con LangChain**: las tools se definen igual que en LangChain (`Tool(name, description, func)`).
5. **Debuggeable**: hay un visualizador de grafos que muestra el flujo.

## Consecuencias

### Positivas
- Setup rápido: el template ya trae la estructura.
- Cada tool es una clase Python testeable unitariamente.
- El routing se puede tunear sin tocar el resto del código.

### Negativas
- LangGraph está en evolución (breaking changes entre versiones menores).
- Requiere conocer el concepto de `StateGraph`, `add_node`, `add_conditional_edges`.
- Debugging en producción requiere logs estructurados (los agregamos).

## Diseño del agente

```python
# services/chatbot-backend/app/agent/graph.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Estado del agente
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_action: Optional[str]

# Tools
tools = [light_rag_tool, ml_predictions_tool]
tool_node = ToolNode(tools)

# Routing
def router(state: AgentState) -> str:
    """Decide si ir a tools o terminar."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Grafo
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_llm)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("agent", router, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")
workflow.set_entry_point("agent")

app = workflow.compile()
```

## Alternativas descartadas

- **LangChain Agent legacy**: deprecated, peor debugging.
- **Haystack**: más verboso, menos herramientas pre-built para GenAI puro.
- **Custom**: mucho más código, reinventamos la rueda.

## Referencias

- [LangGraph docs](https://langchain-ai.github.io/langgraph/)
- [Cosmos GenAI Bundle template](https://catalog.cosmos.../templates/genai-bundle)
