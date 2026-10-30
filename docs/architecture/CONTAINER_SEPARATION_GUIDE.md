> **Legacy reference — superseded for new product and architecture work.** Start at [the context router](../INDEX.md). Preserved content records the earlier crypto/MLOps scope; embedded prompts are not active instructions. Original language and claims are historical, not new verification.

# Container Separation Architecture Guide

## 📋 Architecture Overview

AlphaPulse utilizes a **decoupled container architecture**, separating the ETL pipelines from the compute-heavy ML training service:

```
┌───────────────────────────┐      ┌───────────────────────────┐
│     Airflow Container     │      │     Trainer Container     │
│      (Orchestration)      │─────▶│       (ML Service)        │
│                           │ API  │                           │
│ - Data Collection (OHLCV) │      │ - Model Training (XGB)    │
│ - Feature Engineering     │      │ - Hyperparameter Tuning   │
│ - Sentiment Analysis      │      │ - MLflow Integration      │
└───────────────────────────┘      └───────────────────────────┘
              │                                  │
              ▼                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                 PostgreSQL + MLflow + MinIO                  │
└──────────────────────────────────────────────────────────────┘
```

## 🎯 Why Decouple?

### The Problems with Monoliths
- **Dependency Conflicts**: Orchestration tools (Airflow) and ML libraries (PyTorch, XGBoost) often have conflicting C-library requirements.
- **Resource Inefficiency**: The primary orchestration container stays bloated with ML libraries even when not training.
- **Path Complexity**: Managing `PYTHONPATH` across shared source directories becomes brittle.

### The Decoupled Solution
- **Orchestration Tier**: Focused on data movement and metadata management.
- **Compute Tier**: Isolated environment for heavy training jobs, providing an API for scalability.
- **Standard Communication**: Unified HTTP API for triggering jobs, allowing any worker to request training.

## 📁 Directory Structure & Volume Mapping

### Orchestration Tier (Airflow)
```yaml
airflow-scheduler:
  volumes:
    - ./airflow/dags:/opt/airflow/dags
    - ./airflow/plugins:/opt/airflow/plugins
  environment:
    TRAINER_API_URL: http://trainer:8080
```

### Compute Tier (Trainer)
```yaml
trainer:
  volumes:
    - ./src:/app/src
    - ./training:/app/training
    - ./data:/app/data
    - ./models:/app/models
  environment:
    PYTHONPATH: /app/src:/app
    MLFLOW_TRACKING_URI: http://mlflow:5000
```

## 🔄 Training Trigger Workflow

### Triggering via Airflow (Recommended)
```python
@task(task_id='trigger_training')
def trigger_training():
    url = os.getenv("TRAINER_API_URL") + "/train"
    response = requests.post(url, json={"mode": "full"})
    return response.json()
```

### Triggering via CLI (Development)
```bash
# Direct API call
curl -X POST http://localhost:8181/train -H "Content-Type: application/json" -d '{"mode": "ultra_fast"}'

# Monitor status
curl http://localhost:8181/status
```

## 📦 Dependency Isolation

### Airflow Dependencies (`airflow/requirements.txt`)
- Focused on ingestion: `yfinance`, `feedparser`, `sqlalchemy`, `requests`.

### Trainer Dependencies (`training/requirements.txt`)
- Focused on ML: `xgboost`, `scikit-learn`, `mlflow`, `optuna`, `evidently`, `fastapi`.

## 🎉 Key Benefits

✅ **Clarity**: Single Responsibility Principle applied to containers.  
✅ **Stability**: Dependency isolation prevents version hell.  
✅ **Flexibility**: The Trainer can be scaled independently or moved to a GPU-enabled node without affecting Airflow.  
✅ **Maintainability**: Clean environment separation leads to simpler Dockerfiles and faster builds.

---
**Last Updated**: 2026-01-13
**Status**: Active Architecture