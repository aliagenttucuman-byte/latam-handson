# ML Propensión — Vertex AI Pipelines

## ¿Qué hace?

Entrena y sirve un modelo de clasificación (XGBoost) que predice la propensión de compra de tickets. Implementa:
- Training pipeline
- Serving pipeline (batch)
- Data quality checks
- Data drift detection
- Backtesting

## Estructura

```
ml-propension/
├── pipelines/
│   ├── training_pipeline.py       # Pipeline de entrenamiento
│   ├── serving_pipeline.py        # Pipeline de predicción
│   ├── drift_pipeline.py          # Drift detection
│   └── backtesting_pipeline.py    # Backtesting
├── components/
│   ├── get_master_data.py         # Lee tabla de BQ
│   ├── preprocessing.py           # Limpia + feature engineering
│   ├── train_model.py             # Entrena XGBoost
│   ├── postprocessing.py          # Sube modelo a Vertex Registry
│   ├── data_quality.py            # Valida calidad de datos
│   ├── detect_drift.py            # Detecta drift
│   └── serve_predictions.py       # Genera predicciones
├── tests/
│   ├── test_training.py
│   └── test_preprocessing.py
├── mlflow_config.py               # Setup de MLflow
├── vertex_config.py               # Config de Vertex AI
├── requirements.txt
├── Dockerfile
└── README.md
```

## ¿Qué archivos tocar?

1. **`pipelines/training_pipeline.py`** — Tiene todos los `@component` con TODOs. Reemplazá con código real.
2. **`pipelines/serving_pipeline.py`** — Similar estructura, pero para predicción.
3. **`pipelines/drift_pipeline.py`** — Usar `data_drift.py` (mini-cosmos) como referencia.
4. **`pipelines/backtesting_pipeline.py`** — Usar `optimization.py` (mini-cosmos) como referencia.

## Métricas objetivo

- **Accuracy > 0.7**
- **Precision > 0.65**

## Configuración

### `mlflow_config.py`

```python
import mlflow

# Tracking URI (Vertex AI Experiments)
mlflow.set_tracking_uri("vertex-ai-experiments://nelson-acosta-ob-dev")

# Experiment name
EXPERIMENT_NAME = "nelson-acosta-ob-propension"
mlflow.set_experiment(EXPERIMENT_NAME)
```

### `vertex_config.py`

```python
from google.cloud import aiplatform

PROJECT_ID = "nelson-acosta-ob-dev"
REGION = "us-east1"
BUCKET_URI = "gs://propension-data-bucket"
EXPERIMENT_NAME = "nelson-acosta-ob-propension"

aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
    staging_bucket=BUCKET_URI,
    experiment=EXPERIMENT_NAME,
)
```

## Cómo correr el pipeline

1. Compilá el pipeline:
   ```bash
   python pipelines/training_pipeline.py
   ```
   Esto genera `training_pipeline.yaml`.

2. Subilo a Vertex AI Pipelines:
   - Andá a Vertex AI → Pipelines
   - Click "Create Run"
   - Subí el YAML
   - Configurá los parámetros
   - Click "Submit"

3. Monitoreá la ejecución:
   - Vertex AI → Pipelines → tu run
   - Vas a ver el grafo con el estado de cada componente
   - Logs de cada componente clickeando en el nodo

## Métricas y tracking

Todas las métricas se loggean a MLflow (que en LATAM se integra con Vertex AI Experiments).

Para verlas:
- Vertex AI → Experiments → tu experimento
- O usá MLflow UI local si lo tenés configurado

## Data Quality

Usá el `DataQualityChecker` de MLOps de Cosmos:

```python
from cosmos_model.data_quality import DataQualityChecker

checker = DataQualityChecker(
    table="<project>.nelson_acosta_ob_processed.hands_on_master_cl",
    checks=[
        {"column": "customer_id", "check": "not_null", "threshold": 1.0},
        {"column": "target_purchase_30d", "check": "not_null", "threshold": 0.95},
        {"column": "bookings_count_12m", "check": "min", "value": 0},
        {"column": "propensity_score", "check": "range", "min": 0.0, "max": 1.0},
    ]
)
checker.run()
```

## Data Drift

Pipeline separado. Usá KS test, PSI o Wasserstein (mirá `mini-cosmos/data_drift.py` para implementación de referencia).

```python
from scipy.stats import ks_2samp

baseline = pd.read_csv("baseline.csv")  # datos de training
serving = pd.read_csv("serving.csv")    # datos de hoy

for col in numeric_features:
    stat, p_value = ks_2samp(baseline[col], serving[col])
    if p_value < 0.05:
        print(f"DRIFT detected in {col}: p={p_value:.4f}")
```

## Backtesting

Reentrená el modelo con datos de los últimos N meses y compará con la versión actual. Usá `optimization.py` de mini-cosmos como referencia para hacer HPO (Random/Grid search).

## Referencias

- [Cosmos MLOps docs](https://.../mlops)
- [Vertex AI Pipelines](https://cloud.google.com/vertex-ai/docs/pipelines/introduction)
- [XGBoost en Vertex AI](https://cloud.google.com/vertex-ai/docs/training/using-xgboost)
- [MLflow + Vertex AI](https://cloud.google.com/vertex-ai/docs/experiments/mlflow)
