# 0001 — Elección de XGBoost como modelo de clasificación

**Status**: Aceptado  
**Fecha**: 2026-07-09  
**Contexto**: Hands-on onboarding Cosmos

## Contexto

Necesitamos predecir la propensión de compra de tickets (clasificación binaria: ¿compra o no compra en los próximos 30 días?).

Opciones consideradas:
- **Logistic Regression**: simple, interpretable, baseline.
- **Random Forest**: robusto, fácil de tunear.
- **XGBoost**: gradient boosting, alta performance, soporta missing values.
- **LightGBM**: más rápido que XGBoost en datasets grandes, similar accuracy.
- **Neural Network (MLP)**: flexible, pero overkill para tabular.

## Decisión

**XGBoost**.

## Razones

1. **Performance**: Consistentemente top-3 en benchmarks de tabular data (Kaggle, OpenML).
2. **Soporte para missing values**: GA4 tiene muchos nulos, XGBoost los maneja nativamente.
3. **Explicabilidad**: SHAP values funcionan out-of-the-box con XGBoost.
4. **Integración con Vertex AI**: hay un container oficial de XGBoost para Vertex AI Pipelines.
5. **Costo computacional**: Entrena rápido (minutos) en datasets de 1-10M filas.
6. **Conocimiento del equipo**: La mayoría de los data scientists de LATAM ya lo conocen.

## Consecuencias

### Positivas
- Modelo con accuracy > 0.7 alcanzable sin tuning agresivo.
- Métricas loggeables fácilmente a MLflow con el callback de `cosmos-model`.
- Permite hacer backtesting comparando versiones de modelo.

### Negativas
- No es tan rápido como LightGBM en datasets > 50M filas (no es nuestro caso).
- Menos interpretable que Logistic Regression (mitigado con SHAP).

## Alternativas descartadas

- **Logistic Regression**: muy simple, no captura interacciones de features.
- **Random Forest**: más lento de entrenar, peor en datasets con muchas features categóricas.
- **LightGBM**: marginalmente más rápido, pero requiere más tuning. Lo dejamos como upgrade futuro.
- **Neural Network**: overkill, requiere más datos, menos explicable.

## Referencias

- [XGBoost docs](https://xgboost.readthedocs.io/)
- [Vertex AI + XGBoost tutorial](https://cloud.google.com/vertex-ai/docs/training/using-xgboost)
- [SHAP para XGBoost](https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/tree_based_models/XGBoost%20with%20SHAP.html)
