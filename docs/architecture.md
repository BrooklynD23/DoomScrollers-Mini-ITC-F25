# Architecture Overview

This project follows a simple, data-driven architecture that starts with CSV ingestion and ends with analytics, ML models, and presentation-ready outputs.

## Component Layers

### 1. Data Ingestion & Storage
- `load_csv_to_db` reads `databreach.csv`, normalizes column names, and writes the data into a SQLite database (`src/data/missatech_breach.db`).【F:src/data/database.py†L8-L44】
- Query utilities (`query`, `get_all_incidents`) provide a consistent data access layer for analytics and models.【F:src/data/database.py†L46-L69】

### 2. Analytics & Summaries
- `breach_analysis.py` contains SQL-based aggregations for cost analysis, detection/response metrics, correlation checks, and risk scoring.【F:src/analysis/breach_analysis.py†L10-L138】
- Executive summary logic pulls key KPIs such as total cost, detection delays, and most costly systems/regions.【F:src/analysis/breach_analysis.py†L139-L172】

### 3. Visualization Pipeline
- `charts.py` creates bar charts, heatmaps, scatter plots, and Pareto analyses from the SQLite-backed dataset, storing PNGs under `src/visualizations/output`.【F:src/visualizations/charts.py†L17-L339】

### 4. Machine Learning Models
- `risk_prediction.py` trains:
  - A Random Forest regressor for breach cost prediction.
  - A K-Means cluster model for incident segmentation.
  - A linear regression model to estimate detection/response impact on cost.
  These models are saved to `src/models/saved_models`.【F:src/models/risk_prediction.py†L20-L221】

### 5. Presentation & Dashboard
- `leadership_slides.py` generates a PDF slide deck with executive summaries and recommendations.【F:src/presentation/leadership_slides.py†L15-L200】
- `monitoring_dashboard.py` provides a Tkinter GUI with KPIs, charts, and alert callouts for ongoing monitoring.【F:src/dashboard/monitoring_dashboard.py†L1-L278】

## End-to-End Flow
1. `main.py` loads the CSV into SQLite.
2. Analytics are computed and printed to the console.
3. Visualizations and ML models are generated and persisted.
4. Users can optionally create the executive presentation or launch the dashboard via the interactive menu.【F:main.py†L1-L409】
