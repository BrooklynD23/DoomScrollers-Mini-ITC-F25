"""
Database module for loading and managing the MissaTech breach data.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "missatech_breach.db"
CSV_PATH = Path(__file__).parent.parent.parent / "databreach.csv"


def load_csv_to_db():
    """Load the breach CSV data into SQLite database."""
    # Read only the main data columns (first 10 columns)
    df = pd.read_csv(CSV_PATH, usecols=range(10))

    # Clean column names
    df.columns = [
        'system_name', 'region', 'attack_type', 'data_sensitivity_level',
        'records_exposed', 'estimated_cost_per_record_usd', 'estimated_total_cost_usd',
        'detection_delay_days', 'response_time_days', 'notification_required'
    ]

    # Convert notification_required to boolean
    df['notification_required'] = df['notification_required'].map({'Yes': 1, 'No': 0})

    # Connect to SQLite and create table
    conn = sqlite3.connect(DB_PATH)

    # Write dataframe to SQLite
    df.to_sql('breach_incidents', conn, if_exists='replace', index=False)

    # Create indexes for faster queries
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_system ON breach_incidents(system_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_region ON breach_incidents(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attack ON breach_incidents(attack_type)")

    conn.commit()
    conn.close()

    print(f"Loaded {len(df)} records into database at {DB_PATH}")
    return df


def get_connection():
    """Get a connection to the database."""
    return sqlite3.connect(DB_PATH)


def query(sql, params=None):
    """Execute a query and return results as DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


def get_all_incidents():
    """Get all breach incidents."""
    return query("SELECT * FROM breach_incidents")


if __name__ == "__main__":
    df = load_csv_to_db()
    print("\nData Summary:")
    print(f"Total incidents: {len(df)}")
    print(f"Systems affected: {df['system_name'].nunique()}")
    print(f"Regions affected: {df['region'].nunique()}")
    print(f"Total cost: ${df['estimated_total_cost_usd'].sum():,.2f}")
