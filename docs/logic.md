# Analysis & Modeling Logic

This document describes the main analytical logic used throughout the project.

## Core Analytics (SQL + Pandas)
- **Cost analysis by dimension** groups incidents by system, region, or attack type and aggregates totals, averages, and detection/response metrics.【F:src/analysis/breach_analysis.py†L10-L31】
- **Top costliest incidents** are pulled directly from the database to highlight the most impactful breaches.【F:src/analysis/breach_analysis.py†L34-L43】
- **Detection/response analysis** summarizes min/avg/max detection and response times by system to expose operational gaps.【F:src/analysis/breach_analysis.py†L46-L59】
- **Correlation analysis** calculates relationships between cost, detection delay, response delay, and records exposed to inform priorities.【F:src/analysis/breach_analysis.py†L62-L76】
- **Risk scoring** normalizes frequency, cost, sensitivity, detection delay, and exposure volume into a composite score per system/region pair.【F:src/analysis/breach_analysis.py†L79-L116】
- **Cost-time regression** estimates the marginal cost of detection and response delays to quantify savings from faster action.【F:src/analysis/breach_analysis.py†L130-L157】

## Visualization Logic
Visuals are built from the same SQLite-backed dataset to keep metrics consistent:
- System, region, and attack-type charts summarize top contributors to total cost.【F:src/visualizations/charts.py†L21-L93】
- Detection/response heatmaps and scatter plots show operational delays and their correlation to cost impact.【F:src/visualizations/charts.py†L96-L147】
- Risk matrices, sensitivity charts, and Pareto analyses help prioritize mitigation actions.【F:src/visualizations/charts.py†L150-L284】

## Machine Learning Logic
- **Random Forest cost prediction** encodes categorical variables (system, region, attack type) and predicts total breach cost using incident characteristics.【F:src/models/risk_prediction.py†L20-L84】
- **K-Means clustering** groups incidents by sensitivity, exposure, cost, and timing features to reveal patterns across breaches.【F:src/models/risk_prediction.py†L124-L159】
- **Linear regression impact model** estimates how detection and response delays drive cost, and simulates savings from faster response times.【F:src/models/risk_prediction.py†L162-L215】

## Dashboard Logic
The monitoring dashboard refreshes data from the SQLite database and surfaces:
- KPI cards (total cost, detection time, response time, records exposed).【F:src/dashboard/monitoring_dashboard.py†L114-L152】
- System-level cost charts and detection/response comparisons.【F:src/dashboard/monitoring_dashboard.py†L154-L219】
- High-risk system-region combinations and pre-seeded alerts for action items.【F:src/dashboard/monitoring_dashboard.py†L221-L266】
