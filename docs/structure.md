# Repository Structure

This document explains how the repository is organized and where to find key assets.

## Top-Level Layout
```
.
├── docs/                       # Consolidated documentation (this folder)
├── presentation/               # Presentation assets (visuals, slides)
├── src/                        # Application source code
├── databreach.csv              # Source dataset for analysis
├── main.py                     # End-to-end pipeline entrypoint
└── requirements.txt            # Python dependencies
```

## Source Code Breakdown (`src/`)
```
src/
├── analysis/                   # SQL-based analytics and summary logic
├── dashboard/                  # Tkinter monitoring dashboard
├── data/                       # SQLite database + CSV ingestion utilities
├── models/                     # ML models (prediction + clustering)
├── presentation/               # PDF presentation generator
└── visualizations/             # Matplotlib/Seaborn chart builders
```

### Notable Modules
- `main.py`: Runs the full pipeline, including data loading, analytics, visualizations, modeling, and optional dashboard/presentation steps.【F:main.py†L1-L409】
- `src/data/database.py`: Loads `databreach.csv` into SQLite and exposes query helpers.【F:src/data/database.py†L1-L49】
- `src/analysis/breach_analysis.py`: Aggregations, risk scoring, and executive summary logic.【F:src/analysis/breach_analysis.py†L1-L172】
- `src/visualizations/charts.py`: Generates all charts into `src/visualizations/output`.【F:src/visualizations/charts.py†L1-L339】
- `src/models/risk_prediction.py`: Cost prediction, clustering, and detection impact models; saves artifacts to `saved_models`.【F:src/models/risk_prediction.py†L1-L221】
- `src/dashboard/monitoring_dashboard.py`: GUI for KPIs, charts, and alerts.【F:src/dashboard/monitoring_dashboard.py†L1-L278】
- `src/presentation/leadership_slides.py`: Builds the leadership slide deck PDF.【F:src/presentation/leadership_slides.py†L1-L200】

## Generated Artifacts
Some directories contain generated files. These are created when you run the pipeline:
- `src/data/missatech_breach.db` from CSV ingestion.【F:src/data/database.py†L8-L44】
- `src/visualizations/output/*.png` from `generate_all_visualizations`.【F:src/visualizations/charts.py†L17-L339】
- `src/models/saved_models/*.joblib` from ML model saves.【F:src/models/risk_prediction.py†L20-L121】
- `src/presentation/MissaTech_Executive_Presentation.pdf` from the presentation generator.【F:src/presentation/leadership_slides.py†L15-L36】
