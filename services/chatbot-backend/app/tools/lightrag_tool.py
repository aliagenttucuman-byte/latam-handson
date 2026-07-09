"""
Tool para consultar Light RAG desde el agente LangGraph.
"""

# TODO: Imports
# import requests
# from langchain.tools import Tool
# import os


# ─────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────
# TODO: Levantar de variables de entorno o application.yaml
# LIGHT_RAG_URL = os.getenv("LIGHT_RAG_URL", "https://tu-light-rag-service-url")


# ─────────────────────────────────────────────────────────────────────────
# Función de la tool
# ─────────────────────────────────────────────────────────────────────────
def light_rag_search(query: str) -> str:
    """
    Consulta Light RAG con una pregunta en lenguaje natural.
    Devuelve la respuesta + fuentes citadas.
    
    Args:
        query: Pregunta del usuario (ej. "¿Cuáles son las políticas de equipaje?")
    
    Returns:
        String formateado con respuesta y fuentes.
    """
    # TODO: Implementar
    # 1. endpoint = f"{LIGHT_RAG_URL.rstrip('/')}/query"
    # 2. payload = {
    #      "query": query,
    #      "max_results": 5,
    #      "include_sources": True,
    #    }
    # 3. response = requests.post(endpoint, json=payload, timeout=30)
    # 4. response.raise_for_status()
    # 5. result = response.json()
    # 6. return _format_response(result)
    pass


def _format_response(result: dict) -> str:
    """Formatea la respuesta de Light RAG para el agente."""
    # TODO: Implementar
    # answer = result.get("answer", "No se encontró información")
    # sources = result.get("sources", [])
    # 
    # formatted = f"**Respuesta:** {answer}\n\n"
    # if sources:
    #     formatted += "**Fuentes:**\n"
    #     for i, source in enumerate(sources[:3], 1):
    #         title = source.get("title", "Documento")
    #         score = source.get("score", "N/A")
    #         formatted += f"{i}. {title} (Score: {score})\n"
    # return formatted
    pass


# ─────────────────────────────────────────────────────────────────────────
# Registro como Tool de LangChain
# ─────────────────────────────────────────────────────────────────────────
# TODO: Descomentar cuando esté implementado
# light_rag_tool = Tool(
#     name="document_search",
#     description=(
#         "Busca información en documentos corporativos de LATAM. "
#         "Usa esta tool para consultas sobre políticas, procedimientos, "
#         "y documentación oficial."
#     ),
#     func=light_rag_search,
# )
