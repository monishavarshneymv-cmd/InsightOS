"""
Unit Tests for Data Ingestion, Validation, Preprocessing, and Automated EDA.
"""

import pytest
import pandas as pd
import numpy as np
from data.generator import generate_customers, generate_products, generate_sales_reps, generate_transactions
from ingestion.validator import DataValidator
from ingestion.preprocessor import DataPreprocessor
from ingestion.eda_engine import EDAEngine


@pytest.fixture
def sample_data_bundle():
    """Generate small sample dataset bundle for testing."""
    customers = generate_customers(n=100)
    products = generate_products()
    sales_reps = generate_sales_reps()
    transactions = generate_transactions(customers, products, sales_reps, n_transactions=500)
    return {
        "customers": customers,
        "products": products,
        "sales_reps": sales_reps,
        "transactions": transactions
    }


def test_data_generation_dimensions(sample_data_bundle):
    """Verify generated dataframes meet expected dimensions and column presence."""
    assert len(sample_data_bundle["customers"]) == 100
    assert len(sample_data_bundle["products"]) >= 10
    assert len(sample_data_bundle["sales_reps"]) >= 5
    assert len(sample_data_bundle["transactions"]) == 500


def test_data_validator(sample_data_bundle):
    """Verify schema validation and referential integrity checks."""
    validator = DataValidator()
    cust_val = validator.validate_table(sample_data_bundle["customers"], "customers")
    assert cust_val["passed"] is True
    assert cust_val["row_count"] == 100

    txn_val = validator.validate_table(sample_data_bundle["transactions"], "transactions")
    assert txn_val["passed"] is True

    # Referential integrity
    ref_issues = validator.validate_referential_integrity(sample_data_bundle)
    assert len(ref_issues) == 0


def test_preprocessor_outliers():
    """Verify IQR and Z-Score outlier detection functions."""
    data = pd.DataFrame({"val": [10, 11, 12, 10, 11, 10, 12, 100]})
    iqr_outliers = DataPreprocessor.detect_outliers_iqr(data, "val")
    assert iqr_outliers.iloc[-1] == True
    assert iqr_outliers.sum() == 1

    z_outliers = DataPreprocessor.detect_outliers_zscore(data, "val", threshold=2.0)
    assert z_outliers.iloc[-1] == True


def test_eda_engine(sample_data_bundle):
    """Verify automated exploratory data analysis outputs."""
    eda = EDAEngine(sample_data_bundle["customers"], dataset_name="Customers")
    overview = eda.get_dataset_overview()
    assert overview["rows"] == 100
    assert overview["columns"] == len(sample_data_bundle["customers"].columns)

    stats = eda.get_numerical_statistics()
    assert not stats.empty
    assert "monthly_charges" in stats["Feature"].values

    missing = eda.get_missing_values_summary()
    assert not missing.empty
    assert "Missing Count" in missing.columns
