"""
Pipeline de training del modelo de propensión.

Este es el archivo principal del componente ML. Se ejecuta en Vertex AI Pipelines.
Adapta el notebook de entrenamiento (link en el enunciado) a la estructura de
Vertex Pipelines con @component.
"""

# TODO: Imports necesarios
# from kfp import dsl
# from kfp.dsl import component, Input, Output, Dataset, Model, Metrics
# from google.cloud import bigquery, aiplatform
# import pandas as pd
# import xgboost as xgb
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
# from cosmos_model import log_model, log_metrics  # MLOps de Cosmos
# import mlflow


# ─────────────────────────────────────────────────────────────────────────
# Component 1: get_master_data
# ─────────────────────────────────────────────────────────────────────────
@component(
    base_image="python:3.11",
    packages_to_install=["google-cloud-bigquery", "pandas", "db-dtypes"]
)
def get_master_data(
    project_id: str,
    table_id: str,
    output_dataset: Output[Dataset]
):
    """
    Lee la tabla hands_on_master_cl de BigQuery.
    Guarda el DataFrame como CSV en output_dataset.path.
    """
    # TODO: Implementar
    # 1. client = bigquery.Client(project=project_id)
    # 2. query = f"SELECT * FROM `{project_id}.{table_id}`"
    # 3. df = client.query(query).to_dataframe()
    # 4. df.to_csv(output_dataset.path, index=False)
    # 5. Loggear shape: print(f"Loaded {df.shape[0]} rows, {df.shape[1]} cols")
    pass


# ─────────────────────────────────────────────────────────────────────────
# Component 2: preprocessing
# ─────────────────────────────────────────────────────────────────────────
@component(
    base_image="python:3.11",
    packages_to_install=["pandas", "scikit-learn", "numpy"]
)
def preprocessing(
    input_dataset: Input[Dataset],
    output_dataset: Output[Dataset],
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Limpia, normaliza, hace feature engineering.
    Split train/test.
    """
    # TODO: Implementar
    # 1. df = pd.read_csv(input_dataset.path)
    # 2. Manejar nulos (imputar con mediana para numéricos, moda para categóricos)
    # 3. Encoding de categóricas (one-hot o target encoding)
    # 4. Split X/y: y = df['target_purchase_30d'], X = df.drop(columns=['target_purchase_30d', 'customer_id'])
    # 5. X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    # 6. Guardar como parquet (preserva tipos)
    # 7. Loggear distribución del target
    pass


# ─────────────────────────────────────────────────────────────────────────
# Component 3: train_model
# ─────────────────────────────────────────────────────────────────────────
@component(
    base_image="python:3.11",
    packages_to_install=["xgboost", "scikit-learn", "mlflow", "pandas", "numpy"]
)
def train_model(
    train_dataset: Input[Dataset],
    output_model: Output[Model],
    metrics: Output[Metrics],
    n_estimators: int = 200,
    max_depth: int = 5,
    learning_rate: float = 0.1,
    # TODO: Agregar más hiperparámetros que quieras tunear
):
    """
    Entrena XGBoostClassifier. Loggea métricas a MLflow.
    Guarda el modelo en Vertex Model Registry.
    """
    # TODO: Implementar
    # 1. train = pd.read_parquet(train_dataset.path)
    # 2. X_train = train.drop(columns=['target'])
    # 3. y_train = train['target']
    # 4. model = xgb.XGBClassifier(
    #      n_estimators=n_estimators,
    #      max_depth=max_depth,
    #      learning_rate=learning_rate,
    #      scale_pos_weight=...,  # para class imbalance
    #      random_state=42,
    #      use_label_encoder=False,
    #      eval_metric='logloss'
    #    )
    # 5. model.fit(X_train, y_train)
    # 
    # # Métricas en train (sanity check)
    # 6. y_pred_train = model.predict(X_train)
    # 7. train_acc = accuracy_score(y_train, y_pred_train)
    # 8. train_prec = precision_score(y_train, y_pred_train)
    # 
    # # Loggear a MLflow
    # 9. with mlflow.start_run():
    #      mlflow.log_params({...})
    #      mlflow.log_metrics({"train_accuracy": train_acc, "train_precision": train_prec})
    #      mlflow.xgboost.log_model(model, "model")
    # 
    # # Guardar el modelo
    # 10. joblib.dump(model, output_model.path)
    # 11. metrics.log_metric("train_accuracy", train_acc)
    # 12. metrics.log_metric("train_precision", train_prec)
    pass


# ─────────────────────────────────────────────────────────────────────────
# Component 4: postprocessing
# ─────────────────────────────────────────────────────────────────────────
@component(
    base_image="python:3.11",
    packages_to_install=["google-cloud-aiplatform"]
)
def postprocessing(
    model: Input[Model],
    project_id: str,
    region: str,
    model_display_name: str = "nelson-acosta-ob-propension"
):
    """
    Sube el modelo entrenado a Vertex Model Registry.
    """
    # TODO: Implementar
    # 1. aiplatform.init(project=project_id, location=region)
    # 2. uploaded_model = aiplatform.Model.upload(
    #      display_name=model_display_name,
    #      artifact_uri=model.uri,  # o el path local
    #      serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-7:latest",
    #      sync=False
    #    )
    # 3. print(f"Model uploaded: {uploaded_model.resource_name}")
    pass


# ─────────────────────────────────────────────────────────────────────────
# Pipeline definition
# ─────────────────────────────────────────────────────────────────────────
@dsl.pipeline(
    name="nelson-acosta-ob-propension-training",
    description="Training pipeline for customer propension model"
)
def training_pipeline(
    project_id: str = "nelson-acosta-ob-dev",
    region: str = "us-east1",
    bq_table_id: str = "nelson_acosta_ob_processed.hands_on_master_cl",
    # TODO: Hiperparámetros
):
    """Define el grafo del pipeline."""
    
    get_data_task = get_master_data(
        project_id=project_id,
        table_id=bq_table_id
    )
    
    preprocess_task = preprocessing(
        input_dataset=get_data_task.output
    )
    
    train_task = train_model(
        train_dataset=preprocess_task.output
    )
    
    postprocess_task = postprocessing(
        model=train_task.output,
        project_id=project_id,
        region=region
    )


# TODO: Compilar el pipeline
# if __name__ == "__main__":
#     from kfp import compiler
#     compiler.Compiler().compile(training_pipeline, "training_pipeline.yaml")
