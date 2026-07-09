"""
Agente LangGraph del chatbot.

Este es el archivo principal del componente GenAI.
Define el StateGraph con routing entre 2 tools: Light RAG + ML predictions.
"""

# TODO: Imports
# from typing import TypedDict, List, Optional, Annotated
# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode
# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# from langchain.tools import Tool
# from langchain_openai import ChatOpenAI  # o el LLM del GenAI Gateway de LATAM
# from app.tools.lightrag_tool import light_rag_search
# from app.tools.ml_predictions_tool import get_propension_for_customer


# ─────────────────────────────────────────────────────────────────────────
# Estado del agente
# ─────────────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    """
    Estado que se mantiene entre turns de la conversación.
    """
    messages: Annotated[List[BaseMessage], "conversation history"]
    # TODO: Agregar más campos si necesitás (ej. customer_id extraído de la pregunta)


# ─────────────────────────────────────────────────────────────────────────
# Tools disponibles
# ─────────────────────────────────────────────────────────────────────────
tools = [
    # TODO: Importar las tools reales
    # light_rag_search,  # tool que consulta Light RAG
    # get_propension_for_customer,  # tool que consulta predicciones ML en BQ
]


# ─────────────────────────────────────────────────────────────────────────
# Nodo: agente (LLM con tools)
# ─────────────────────────────────────────────────────────────────────────
def call_llm(state: AgentState) -> AgentState:
    """
    Llama al LLM con el historial de mensajes. El LLM decide si llamar a una tool o responder.
    """
    # TODO: Implementar
    # 1. llm = ChatOpenAI(model="gpt-4", temperature=0)  # o el LLM del GenAI Gateway
    # 2. llm_with_tools = llm.bind_tools(tools)
    # 3. response = llm_with_tools.invoke(state["messages"])
    # 4. return {"messages": state["messages"] + [response]}
    pass


# ─────────────────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────────────────
def router(state: AgentState) -> str:
    """
    Decide si el LLM quiere llamar a una tool o terminar.
    """
    # TODO: Implementar
    # last_message = state["messages"][-1]
    # if hasattr(last_message, "tool_calls") and last_message.tool_calls:
    #     return "tools"
    # return END
    pass


# ─────────────────────────────────────────────────────────────────────────
# Definición del grafo
# ─────────────────────────────────────────────────────────────────────────
def build_graph():
    """
    Construye y compila el StateGraph.
    
    Flujo:
        agent (LLM) -> [tool_calls?] -> tools -> agent (con resultado) -> END
                     -> [no tool_call] -> END
    """
    # TODO: Implementar
    # workflow = StateGraph(AgentState)
    # 
    # # Nodos
    # workflow.add_node("agent", call_llm)
    # workflow.add_node("tools", ToolNode(tools))
    # 
    # # Edges
    # workflow.add_conditional_edges(
    #     "agent",
    #     router,
    #     {
    #         "tools": "tools",
    #         END: END,
    #     }
    # )
    # workflow.add_edge("tools", "agent")
    # 
    # # Entry point
    # workflow.set_entry_point("agent")
    # 
    # return workflow.compile()
    pass


# ─────────────────────────────────────────────────────────────────────────
# Compilación del grafo (singleton)
# ─────────────────────────────────────────────────────────────────────────
# TODO: Compilar al importar
# app = build_graph()


# ─────────────────────────────────────────────────────────────────────────
# Test local
# ─────────────────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     from langchain_core.messages import HumanMessage
#     
#     result = app.invoke({
#         "messages": [HumanMessage(content="¿Cuál es la propensión de compra del cliente 12345?")]
#     })
#     
#     print(result["messages"][-1].content)
