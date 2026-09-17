"""
InsightOS - Database Seeding Pipeline
Generates or reads raw business data, establishes database schema, and loads tables.
"""

import sys
from pathlib import Path

# Add project root to sys.path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import config
from data.generator import generate_all_datasets
from database.db_manager import DatabaseManager


def seed_database(force_regenerate: bool = False) -> None:
    """Populate database tables with enterprise data bundle."""
    db = DatabaseManager()

    # 1. Initialize tables and indexes
    print("Initializing database schema...")
    db.initialize_schema()

    # 2. Check if raw CSV files exist
    cust_file = config.RAW_DATA_DIR / "customers.csv"
    prod_file = config.RAW_DATA_DIR / "products.csv"
    reps_file = config.RAW_DATA_DIR / "sales_reps.csv"
    txn_file = config.RAW_DATA_DIR / "transactions.csv"

    if force_regenerate or not (cust_file.exists() and prod_file.exists() and reps_file.exists() and txn_file.exists()):
        print("Raw datasets not found or regeneration requested. Generating synthetic data...")
        bundle = generate_all_datasets(save_to_disk=True)
    else:
        print("Reading existing raw datasets from disk...")
        bundle = {
            "customers": pd.read_csv(cust_file),
            "products": pd.read_csv(prod_file),
            "sales_reps": pd.read_csv(reps_file),
            "transactions": pd.read_csv(txn_file)
        }

    # 3. Load into database
    print("Loading tables into relational database...")
    for table_name, df in bundle.items():
        loaded_rows = db.load_table(table_name, df, if_exists="replace")
        print(f"  ✓ Loaded {loaded_rows:,} rows into '{table_name}'")

    print("\nDatabase Seeding Complete! Summary:")
    counts = db.get_table_row_counts()
    for tbl, cnt in counts.items():
        print(f"  - {tbl}: {cnt:,} rows")


if __name__ == "__main__":
    seed_database()
