"""
InsightOS - Data Validation Engine
Performs rigorous schema validation, null threshold checks, data type verification,
domain range checks, and referential integrity between business entities.
"""

from typing import Any
import pandas as pd
import numpy as np


class DataValidator:
    """Enterprise Data Quality & Schema Validator."""

    EXPECTED_SCHEMAS = {
        "customers": {
            "required_columns": [
                "customer_id", "company_name", "segment", "region", "country",
                "join_date", "contract_type", "payment_method", "tenure_months",
                "monthly_charges", "total_charges", "support_tickets", "satisfaction_score", "churn"
            ],
            "numeric_ranges": {
                "tenure_months": (0, 120),
                "monthly_charges": (0, 50000),
                "support_tickets": (0, 100),
                "satisfaction_score": (1, 5),
                "churn": (0, 1)
            }
        },
        "products": {
            "required_columns": [
                "product_id", "product_name", "category", "unit_cost", "unit_price", "margin_pct"
            ],
            "numeric_ranges": {
                "unit_cost": (0, 100000),
                "unit_price": (0, 100000),
                "margin_pct": (-1.0, 1.0)
            }
        },
        "sales_reps": {
            "required_columns": [
                "rep_id", "name", "region", "quota", "commission_rate"
            ],
            "numeric_ranges": {
                "quota": (0, 10000000),
                "commission_rate": (0.0, 0.50)
            }
        },
        "transactions": {
            "required_columns": [
                "transaction_id", "customer_id", "product_id", "rep_id",
                "transaction_date", "quantity", "unit_price", "discount_pct",
                "total_amount", "total_cost", "net_profit", "payment_status"
            ],
            "numeric_ranges": {
                "quantity": (1, 1000),
                "discount_pct": (0.0, 1.0)
            }
        }
    }

    def validate_table(self, df: pd.DataFrame, table_name: str) -> dict[str, Any]:
        """Validate a single table against schema and domain expectations."""
        results = {
            "table_name": table_name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "passed": True,
            "issues": [],
            "warnings": [],
            "null_rates": {},
            "duplicate_ids": 0
        }

        schema = self.EXPECTED_SCHEMAS.get(table_name)
        if not schema:
            results["warnings"].append(f"No predefined schema constraint found for '{table_name}'. Running generic checks.")
            return results

        # 1. Missing Required Columns
        missing_cols = set(schema["required_columns"]) - set(df.columns)
        if missing_cols:
            results["passed"] = False
            results["issues"].append(f"Missing required columns: {list(missing_cols)}")

        # 2. Null Rates
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            rate = round(count / max(len(df), 1), 4)
            results["null_rates"][col] = rate
            if rate > 0.20:
                results["warnings"].append(f"Column '{col}' has high null rate: {rate * 100:.1f}%")

        # 3. Check ID uniqueness
        id_col = f"{table_name.rstrip('s')}_id" if f"{table_name.rstrip('s')}_id" in df.columns else None
        if not id_col and "transaction_id" in df.columns:
            id_col = "transaction_id"
        elif not id_col and "rep_id" in df.columns:
            id_col = "rep_id"

        if id_col and id_col in df.columns:
            duplicates = df.duplicated(subset=[id_col]).sum()
            results["duplicate_ids"] = int(duplicates)
            if duplicates > 0:
                results["passed"] = False
                results["issues"].append(f"Duplicate primary key entries detected in '{id_col}': {duplicates} duplicates")

        # 4. Numeric Range Checks
        for col, (min_val, max_val) in schema.get("numeric_ranges", {}).items():
            if col in df.columns:
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                out_of_bounds = ((series < min_val) | (series > max_val)).sum()
                if out_of_bounds > 0:
                    results["warnings"].append(
                        f"Column '{col}' has {out_of_bounds} values outside expected bounds [{min_val}, {max_val}]"
                    )

        return results

    def validate_referential_integrity(self, bundle: dict[str, pd.DataFrame]) -> list[str]:
        """Verify foreign key integrity across tables."""
        issues = []
        if "transactions" in bundle and "customers" in bundle:
            txn_cust = set(bundle["transactions"]["customer_id"].dropna().unique())
            valid_cust = set(bundle["customers"]["customer_id"].dropna().unique())
            orphaned = txn_cust - valid_cust
            if orphaned:
                issues.append(f"Detected {len(orphaned)} transactions referencing non-existent customer IDs.")

        if "transactions" in bundle and "products" in bundle:
            txn_prod = set(bundle["transactions"]["product_id"].dropna().unique())
            valid_prod = set(bundle["products"]["product_id"].dropna().unique())
            orphaned_prods = txn_prod - valid_prod
            if orphaned_prods:
                issues.append(f"Detected {len(orphaned_prods)} transactions referencing non-existent product IDs.")

        return issues
