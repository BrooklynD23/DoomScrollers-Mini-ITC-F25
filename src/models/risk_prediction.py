"""
ML Models for breach risk prediction and pattern detection.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, classification_report, silhouette_score
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from data.database import get_all_incidents

MODEL_DIR = Path(__file__).parent / "saved_models"
MODEL_DIR.mkdir(exist_ok=True)


class BreachCostPredictor:
    """Predict breach cost based on incident characteristics."""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def prepare_features(self, df):
        """Prepare features for modeling."""
        df = df.copy()

        # Encode categorical variables
        for col in ['system_name', 'region', 'attack_type']:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])

        feature_cols = [
            'system_name_encoded', 'region_encoded', 'attack_type_encoded',
            'data_sensitivity_level', 'records_exposed',
            'detection_delay_days', 'response_time_days'
        ]

        return df[feature_cols]

    def train(self, df):
        """Train the cost prediction model."""
        X = self.prepare_features(df)
        y = df['estimated_total_cost_usd']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Cost Predictor Performance:")
        print(f"  RMSE: ${np.sqrt(mse):,.2f}")
        print(f"  R2 Score: {r2:.3f}")

        return {'rmse': np.sqrt(mse), 'r2': r2}

    def get_feature_importance(self):
        """Get feature importance from the model."""
        features = [
            'System', 'Region', 'Attack Type', 'Sensitivity',
            'Records', 'Detection Delay', 'Response Time'
        ]
        importance = pd.DataFrame({
            'feature': features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return importance

    def save(self):
        """Save the model."""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'encoders': self.label_encoders
        }, MODEL_DIR / 'cost_predictor.joblib')


class RiskClusterAnalyzer:
    """Cluster incidents to identify risk patterns."""

    def __init__(self, n_clusters=4):
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()

    def analyze(self, df):
        """Perform cluster analysis on incidents."""
        features = [
            'data_sensitivity_level', 'records_exposed',
            'estimated_total_cost_usd', 'detection_delay_days', 'response_time_days'
        ]

        X = df[features].copy()
        X_scaled = self.scaler.fit_transform(X)

        # Fit clusters
        clusters = self.model.fit_predict(X_scaled)
        df = df.copy()
        df['cluster'] = clusters

        # Analyze each cluster
        cluster_profiles = df.groupby('cluster').agg({
            'estimated_total_cost_usd': ['mean', 'count'],
            'records_exposed': 'mean',
            'data_sensitivity_level': 'mean',
            'detection_delay_days': 'mean',
            'response_time_days': 'mean'
        }).round(2)

        silhouette = silhouette_score(X_scaled, clusters)

        return {
            'cluster_profiles': cluster_profiles,
            'silhouette_score': silhouette,
            'labeled_data': df
        }


class DetectionImpactModel:
    """Model the relationship between detection time and cost."""

    def __init__(self):
        self.model = LinearRegression()

    def fit(self, df):
        """Fit the model to estimate detection impact."""
        X = df[['detection_delay_days', 'response_time_days', 'records_exposed']].values
        y = df['estimated_total_cost_usd'].values

        self.model.fit(X, y)

        coef = self.model.coef_

        return {
            'detection_day_impact': coef[0],
            'response_day_impact': coef[1],
            'record_impact': coef[2],
            'intercept': self.model.intercept_
        }

    def estimate_savings(self, df, detection_improvement=1, response_improvement=1):
        """Estimate cost savings from faster detection/response."""
        current_cost = df['estimated_total_cost_usd'].sum()

        # Create improved scenario
        improved_df = df.copy()
        improved_df['detection_delay_days'] = np.maximum(
            0, improved_df['detection_delay_days'] - detection_improvement
        )
        improved_df['response_time_days'] = np.maximum(
            0, improved_df['response_time_days'] - response_improvement
        )

        X_improved = improved_df[['detection_delay_days', 'response_time_days', 'records_exposed']].values
        improved_costs = self.model.predict(X_improved)
        improved_total = np.maximum(0, improved_costs).sum()

        savings = current_cost - improved_total

        return {
            'current_total_cost': current_cost,
            'improved_total_cost': improved_total,
            'estimated_savings': savings,
            'savings_percentage': (savings / current_cost) * 100
        }


def run_all_models():
    """Run all ML models and return comprehensive results."""
    print("\n" + "=" * 60)
    print("MACHINE LEARNING ANALYSIS")
    print("=" * 60)

    df = get_all_incidents()

    # 1. Cost Prediction Model
    print("\n1. COST PREDICTION MODEL (Random Forest)")
    print("-" * 60)
    cost_predictor = BreachCostPredictor()
    cost_predictor.train(df)

    print("\nFeature Importance:")
    importance = cost_predictor.get_feature_importance()
    for _, row in importance.iterrows():
        print(f"  {row['feature']:20} {row['importance']:.3f}")

    cost_predictor.save()

    # 2. Risk Clustering
    print("\n2. RISK CLUSTER ANALYSIS (K-Means)")
    print("-" * 60)
    cluster_analyzer = RiskClusterAnalyzer(n_clusters=4)
    cluster_results = cluster_analyzer.analyze(df)

    print(f"Silhouette Score: {cluster_results['silhouette_score']:.3f}")
    print("\nCluster Profiles:")
    print(cluster_results['cluster_profiles'])

    # 3. Detection Impact Model
    print("\n3. DETECTION TIME IMPACT MODEL (Linear Regression)")
    print("-" * 60)
    impact_model = DetectionImpactModel()
    impacts = impact_model.fit(df)

    print(f"Cost per detection day: ${impacts['detection_day_impact']:,.2f}")
    print(f"Cost per response day: ${impacts['response_day_impact']:,.2f}")
    print(f"Cost per record exposed: ${impacts['record_impact']:.2f}")

    # Estimate savings
    savings = impact_model.estimate_savings(df, detection_improvement=2, response_improvement=1)
    print(f"\nEstimated savings (2-day faster detection, 1-day faster response):")
    print(f"  Current cost: ${savings['current_total_cost']:,.2f}")
    print(f"  Improved cost: ${savings['improved_total_cost']:,.2f}")
    print(f"  Savings: ${savings['estimated_savings']:,.2f} ({savings['savings_percentage']:.1f}%)")

    return {
        'cost_predictor': cost_predictor,
        'cluster_results': cluster_results,
        'detection_impact': impacts,
        'savings_analysis': savings
    }


if __name__ == "__main__":
    results = run_all_models()
