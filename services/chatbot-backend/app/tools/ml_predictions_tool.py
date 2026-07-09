"""
Tool para consultar predicciones del modelo ML desde el agente LangGraph.
"""

# TODO: Imports
# from google.cloud import bigquery
# from langchain.tools import Tool
# import os


# ─────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────
# TODO: Levantar de variables de entorno o application.yaml
# PROJECT_ID = os.getenv("GCP_PROJECT_ID", "nelson-acosta-ob-dev")
# BQ_TABLE = os.getenv("BQ_PREDICTIONS_TABLE", "nelson_acosta_ob_processed.customer_predictions")


# ─────────────────────────────────────────────────────────────────────────
# Función de la tool
# ─────────────────────────────────────────────────────────────────────────
def get_propension_for_customer(customer_id: str) -> str:
    """
    Consulta la propensión de compra de un cliente específico.
    
    Args:
        customer_id: ID del cliente (ej. "CUST-12345" o el ID que uses).
    
    Returns:
        String con la propensión y metadata relevante.
    """
    # TODO: Implementar
    # 1. client = bigquery.Client(project=PROJECT_ID)
    # 2. query = f"""
    #      SELECT
    #        customer_id,
    #        propensity_score,
    #        predicted_at,
    #        model_version
    #      FROM `{PROJECT_ID}.{BQ_TABLE}`
    #      WHERE customer_id = @customer_id
    #      ORDER BY predicted_at DESC
    #      LIMIT 1
    #    """
    # 3. job = client.query(query, job_config=bigquery.QueryJobConfig(
    #      query_parameters=[bigquery.ScalarQueryParameter("customer_id", "STRING", customer_id)]
    #    ))
    # 4. result = list(job.result())
    # 5. if not result:
    #      return f"No se encontró predicción para el cliente {customer_id}."
    # 6. row = result[0]
    # 7. score = row.propensity_score
    # 8. propensity_label = _score_to_label(score)
    # 9. return (
    #      f"Cliente {customer_id}: propensión de compra = {score:.1%} ({propensity_label}). "
    #      f"Última predicción: {row.predicted_at.strftime('%Y-%m-%d')} "
    #      f"(modelo {row.model_version})."
    #    )
    pass


def _score_to_label(score: float) -> str:
    """Convierte un score numérico a una etiqueta legible."""
    # TODO: Implementar (los thresholds dependen del modelo entrenado)
    # if score >= 0.7:
    #     return "alta"
    # elif score >= 0.4:
    #     return "media"
    # else:
    #     return "baja"
    pass


# ─────────────────────────────────────────────────────────────────────────
# Registro como Tool de LangChain
# ─────────────────────────────────────────────────────────────────────────
# TODO: Descomentar cuando esté implementado
# ml_predictions_tool = Tool(
#     name="propension_lookup",
#     description=(
#         "Consulta la propensión de compra de un cliente específico. "
#         "Usa esta tool cuando el usuario pregunte por la probabilidad de compra "
#         "de un customer_id. Input: customer_id (string)."
#     ),
#     func=get_propension_for_customer,
# )
