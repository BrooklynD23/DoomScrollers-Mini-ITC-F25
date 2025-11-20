"""
Visualization module for MissaTech breach data analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from data.database import get_all_incidents, query
from analysis.breach_analysis import cost_analysis_by_dimension, correlation_analysis

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def plot_cost_by_system():
    """Bar chart of total cost by system."""
    df = cost_analysis_by_dimension('system_name')

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['system_name'], df['total_cost'] / 1e6, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])

    ax.set_xlabel('System', fontsize=12)
    ax.set_ylabel('Total Cost (Millions USD)', fontsize=12)
    ax.set_title('Total Breach Cost by System', fontsize=14, fontweight='bold')

    # Add value labels
    for bar, cost in zip(bars, df['total_cost']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'${cost/1e6:.1f}M', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cost_by_system.png', dpi=150)
    plt.close()
    print(f"Saved: cost_by_system.png")


def plot_cost_by_region():
    """Horizontal bar chart of cost by region."""
    df = cost_analysis_by_dimension('region').head(15)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(df['region'], df['total_cost'] / 1e6, color=plt.cm.RdYlBu(range(15)))

    ax.set_xlabel('Total Cost (Millions USD)', fontsize=12)
    ax.set_ylabel('Region', fontsize=12)
    ax.set_title('Total Breach Cost by Region (Top 15)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cost_by_region.png', dpi=150)
    plt.close()
    print(f"Saved: cost_by_region.png")


def plot_attack_type_distribution():
    """Pie chart of attack type distribution."""
    df = cost_analysis_by_dimension('attack_type')

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # By frequency
    axes[0].pie(df['incident_count'], labels=df['attack_type'], autopct='%1.1f%%',
                colors=['#e74c3c', '#3498db', '#2ecc71'])
    axes[0].set_title('Incidents by Attack Type', fontweight='bold')

    # By cost
    axes[1].pie(df['total_cost'], labels=df['attack_type'], autopct='%1.1f%%',
                colors=['#e74c3c', '#3498db', '#2ecc71'])
    axes[1].set_title('Cost by Attack Type', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'attack_type_distribution.png', dpi=150)
    plt.close()
    print(f"Saved: attack_type_distribution.png")


def plot_detection_response_heatmap():
    """Heatmap of detection and response times by system."""
    df = get_all_incidents()

    pivot = df.pivot_table(
        values=['detection_delay_days', 'response_time_days'],
        index='system_name',
        aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r', ax=ax)
    ax.set_title('Average Detection & Response Times by System (Days)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'detection_response_heatmap.png', dpi=150)
    plt.close()
    print(f"Saved: detection_response_heatmap.png")


def plot_cost_vs_detection_scatter():
    """Scatter plot of cost vs detection time."""
    df = get_all_incidents()

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        df['detection_delay_days'],
        df['estimated_total_cost_usd'] / 1e6,
        c=df['data_sensitivity_level'],
        cmap='RdYlGn_r',
        s=df['records_exposed'] / 1000,
        alpha=0.6
    )

    ax.set_xlabel('Detection Delay (Days)', fontsize=12)
    ax.set_ylabel('Total Cost (Millions USD)', fontsize=12)
    ax.set_title('Cost vs Detection Time\n(Size = Records Exposed, Color = Sensitivity)',
                 fontsize=14, fontweight='bold')

    plt.colorbar(scatter, label='Sensitivity Level')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cost_vs_detection.png', dpi=150)
    plt.close()
    print(f"Saved: cost_vs_detection.png")


def plot_risk_matrix():
    """Risk matrix showing high-risk system-region combinations."""
    df = get_all_incidents()

    # Aggregate by system and region
    risk_df = df.groupby(['system_name', 'region']).agg({
        'estimated_total_cost_usd': 'sum',
        'records_exposed': 'sum'
    }).reset_index()

    # Create pivot for heatmap
    pivot = risk_df.pivot_table(
        values='estimated_total_cost_usd',
        index='system_name',
        columns='region',
        aggfunc='sum',
        fill_value=0
    )

    # Select top regions by total cost
    top_regions = df.groupby('region')['estimated_total_cost_usd'].sum().nlargest(10).index
    pivot = pivot[pivot.columns.intersection(top_regions)]

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(pivot / 1e6, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax)
    ax.set_title('Cost by System-Region (Millions USD)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'risk_matrix.png', dpi=150)
    plt.close()
    print(f"Saved: risk_matrix.png")


def plot_sensitivity_analysis():
    """Bar chart showing cost by data sensitivity level."""
    sql = """
    SELECT
        data_sensitivity_level,
        COUNT(*) as count,
        AVG(estimated_cost_per_record_usd) as avg_cost_per_record,
        SUM(estimated_total_cost_usd) as total_cost
    FROM breach_incidents
    GROUP BY data_sensitivity_level
    ORDER BY data_sensitivity_level
    """
    df = query(sql)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Average cost per record by sensitivity
    bars1 = axes[0].bar(df['data_sensitivity_level'], df['avg_cost_per_record'],
                        color=plt.cm.RdYlGn_r([0.2, 0.4, 0.6, 0.8, 1.0]))
    axes[0].set_xlabel('Data Sensitivity Level', fontsize=12)
    axes[0].set_ylabel('Avg Cost per Record (USD)', fontsize=12)
    axes[0].set_title('Cost per Record by Sensitivity', fontsize=14, fontweight='bold')

    # Total cost by sensitivity
    bars2 = axes[1].bar(df['data_sensitivity_level'], df['total_cost'] / 1e6,
                        color=plt.cm.RdYlGn_r([0.2, 0.4, 0.6, 0.8, 1.0]))
    axes[1].set_xlabel('Data Sensitivity Level', fontsize=12)
    axes[1].set_ylabel('Total Cost (Millions USD)', fontsize=12)
    axes[1].set_title('Total Cost by Sensitivity', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'sensitivity_analysis.png', dpi=150)
    plt.close()
    print(f"Saved: sensitivity_analysis.png")


def plot_correlation_matrix():
    """Correlation matrix of numeric variables."""
    df = get_all_incidents()

    numeric_cols = ['data_sensitivity_level', 'records_exposed', 'estimated_cost_per_record_usd',
                    'estimated_total_cost_usd', 'detection_delay_days', 'response_time_days']

    corr_matrix = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, ax=ax)
    ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_matrix.png', dpi=150)
    plt.close()
    print(f"Saved: correlation_matrix.png")


def generate_all_visualizations():
    """Generate all visualizations."""
    print("\nGenerating visualizations...")
    print("-" * 40)

    plot_cost_by_system()
    plot_cost_by_region()
    plot_attack_type_distribution()
    plot_detection_response_heatmap()
    plot_cost_vs_detection_scatter()
    plot_risk_matrix()
    plot_sensitivity_analysis()
    plot_correlation_matrix()

    print(f"\nAll visualizations saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_visualizations()
