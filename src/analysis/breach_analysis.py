"""
Core analysis functions for MissaTech breach data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from data.database import query, get_all_incidents


def cost_analysis_by_dimension(dimension):
    """Calculate total and average cost by a specific dimension."""
    sql = f"""
    SELECT
        {dimension},
        COUNT(*) as incident_count,
        SUM(estimated_total_cost_usd) as total_cost,
        AVG(estimated_total_cost_usd) as avg_cost,
        SUM(records_exposed) as total_records,
        AVG(detection_delay_days) as avg_detection_days,
        AVG(response_time_days) as avg_response_days
    FROM breach_incidents
    GROUP BY {dimension}
    ORDER BY total_cost DESC
    """
    return query(sql)


def get_top_costliest_incidents(n=3):
    """Get the top N costliest incidents with full details."""
    sql = f"""
    SELECT *
    FROM breach_incidents
    ORDER BY estimated_total_cost_usd DESC
    LIMIT {n}
    """
    return query(sql)


def detection_response_analysis():
    """Analyze detection and response times across systems."""
    sql = """
    SELECT
        system_name,
        AVG(detection_delay_days) as avg_detection,
        AVG(response_time_days) as avg_response,
        MIN(detection_delay_days) as min_detection,
        MAX(detection_delay_days) as max_detection,
        COUNT(*) as incidents
    FROM breach_incidents
    GROUP BY system_name
    ORDER BY avg_detection DESC
    """
    return query(sql)


def correlation_analysis():
    """Analyze correlations between variables."""
    df = get_all_incidents()

    correlations = {
        'detection_vs_cost': df['detection_delay_days'].corr(df['estimated_total_cost_usd']),
        'response_vs_cost': df['response_time_days'].corr(df['estimated_total_cost_usd']),
        'records_vs_cost': df['records_exposed'].corr(df['estimated_total_cost_usd']),
        'sensitivity_vs_cost': df['data_sensitivity_level'].corr(df['estimated_total_cost_usd']),
        'detection_vs_records': df['detection_delay_days'].corr(df['records_exposed'])
    }

    return correlations


def risk_score_calculation():
    """Calculate risk scores for each system-region combination."""
    sql = """
    SELECT
        system_name,
        region,
        COUNT(*) as incident_frequency,
        SUM(estimated_total_cost_usd) as total_cost,
        AVG(data_sensitivity_level) as avg_sensitivity,
        AVG(detection_delay_days) as avg_detection,
        SUM(records_exposed) as total_records
    FROM breach_incidents
    GROUP BY system_name, region
    """
    df = query(sql)

    # Normalize each factor to 0-1 scale (handle division by zero)
    for col in ['incident_frequency', 'total_cost', 'avg_sensitivity', 'avg_detection', 'total_records']:
        col_range = df[col].max() - df[col].min()
        if col_range == 0:
            df[f'{col}_norm'] = 0.5  # Default to mid-range if all values are the same
        else:
            df[f'{col}_norm'] = (df[col] - df[col].min()) / col_range

    # Calculate composite risk score
    df['risk_score'] = (
        df['incident_frequency_norm'] * 0.2 +
        df['total_cost_norm'] * 0.3 +
        df['avg_sensitivity_norm'] * 0.2 +
        df['avg_detection_norm'] * 0.15 +
        df['total_records_norm'] * 0.15
    ) * 100

    return df.sort_values('risk_score', ascending=False)


def attack_vector_analysis():
    """Analyze attack vectors and their effectiveness."""
    sql = """
    SELECT
        attack_type,
        COUNT(*) as frequency,
        SUM(estimated_total_cost_usd) as total_cost,
        AVG(estimated_total_cost_usd) as avg_cost,
        AVG(records_exposed) as avg_records,
        AVG(detection_delay_days) as avg_detection,
        AVG(response_time_days) as avg_response
    FROM breach_incidents
    GROUP BY attack_type
    ORDER BY total_cost DESC
    """
    return query(sql)


def sensitivity_impact_analysis():
    """Analyze how data sensitivity affects breach impact."""
    sql = """
    SELECT
        data_sensitivity_level,
        COUNT(*) as incident_count,
        AVG(estimated_cost_per_record_usd) as avg_cost_per_record,
        AVG(estimated_total_cost_usd) as avg_total_cost,
        SUM(notification_required) as requiring_notification
    FROM breach_incidents
    GROUP BY data_sensitivity_level
    ORDER BY data_sensitivity_level DESC
    """
    return query(sql)


def cost_time_regression():
    """Estimate cost savings from faster detection/response."""
    df = get_all_incidents()

    # Calculate average cost per day of detection delay
    cost_per_detection_day = df['estimated_total_cost_usd'].sum() / df['detection_delay_days'].sum()
    cost_per_response_day = df['estimated_total_cost_usd'].sum() / df['response_time_days'].sum()

    # Estimate savings from 1-day improvement
    total_incidents = len(df)
    detection_savings = cost_per_detection_day * total_incidents * 0.1  # 10% cost correlated with detection
    response_savings = cost_per_response_day * total_incidents * 0.05   # 5% cost correlated with response

    return {
        'cost_per_detection_day': cost_per_detection_day,
        'cost_per_response_day': cost_per_response_day,
        'estimated_savings_1day_faster_detection': detection_savings,
        'estimated_savings_1day_faster_response': response_savings
    }


def generate_executive_summary():
    """Generate a complete executive summary of the breach analysis."""
    df = get_all_incidents()

    summary = {
        'total_incidents': len(df),
        'total_cost': df['estimated_total_cost_usd'].sum(),
        'total_records_exposed': df['records_exposed'].sum(),
        'avg_cost_per_incident': df['estimated_total_cost_usd'].mean(),
        'avg_detection_days': df['detection_delay_days'].mean(),
        'avg_response_days': df['response_time_days'].mean(),
        'most_costly_system': cost_analysis_by_dimension('system_name').iloc[0]['system_name'],
        'most_costly_region': cost_analysis_by_dimension('region').iloc[0]['region'],
        'most_common_attack': cost_analysis_by_dimension('attack_type').iloc[0]['attack_type'],
        'highest_sensitivity_incidents': len(df[df['data_sensitivity_level'] >= 4]),
        'notifications_required': df['notification_required'].sum()
    }

    return summary


if __name__ == "__main__":
    print("=" * 60)
    print("MISSATECH BREACH ANALYSIS REPORT")
    print("=" * 60)

    # Executive Summary
    summary = generate_executive_summary()
    print("\n EXECUTIVE SUMMARY")
    print("-" * 60)
    print(f"Total Incidents: {summary['total_incidents']}")
    print(f"Total Financial Impact: ${summary['total_cost']:,.2f}")
    print(f"Total Records Exposed: {summary['total_records_exposed']:,}")
    print(f"Average Cost per Incident: ${summary['avg_cost_per_incident']:,.2f}")
    print(f"Average Detection Time: {summary['avg_detection_days']:.1f} days")
    print(f"Average Response Time: {summary['avg_response_days']:.1f} days")

    # Cost by System
    print("\n COST BY SYSTEM")
    print("-" * 60)
    system_costs = cost_analysis_by_dimension('system_name')
    for _, row in system_costs.iterrows():
        print(f"{row['system_name']:12} | Total: ${row['total_cost']:>14,.2f} | Avg: ${row['avg_cost']:>12,.2f}")

    # Cost by Region
    print("\n COST BY REGION (Top 10)")
    print("-" * 60)
    region_costs = cost_analysis_by_dimension('region').head(10)
    for _, row in region_costs.iterrows():
        print(f"{row['region']:15} | Total: ${row['total_cost']:>12,.2f} | Avg: ${row['avg_cost']:>12,.2f}")

    # Cost by Attack Type
    print("\n COST BY ATTACK TYPE")
    print("-" * 60)
    attack_costs = cost_analysis_by_dimension('attack_type')
    for _, row in attack_costs.iterrows():
        print(f"{row['attack_type']:20} | Total: ${row['total_cost']:>14,.2f} | Avg: ${row['avg_cost']:>12,.2f}")

    # Top 3 Costliest Incidents
    print("\n TOP 3 COSTLIEST INCIDENTS")
    print("-" * 60)
    top_incidents = get_top_costliest_incidents(3)
    for i, row in top_incidents.iterrows():
        print(f"\n{i+1}. Cost: ${row['estimated_total_cost_usd']:,.2f}")
        print(f"   System: {row['system_name']} | Region: {row['region']}")
        print(f"   Attack: {row['attack_type']} | Sensitivity: {row['data_sensitivity_level']}")
        print(f"   Records: {row['records_exposed']:,} | Detection: {row['detection_delay_days']} days")

    # Correlations
    print("\n CORRELATION ANALYSIS")
    print("-" * 60)
    corrs = correlation_analysis()
    for key, value in corrs.items():
        print(f"{key.replace('_', ' ').title()}: {value:.3f}")
