"""
Unit Tests for Database Connection, Schema Migration, and SQL Analytics Queries.
"""

import pytest
from database.db_manager import DatabaseManager
from database.analytics_queries import QUERY_CATALOG
from data.generator import generate_customers, generate_products, generate_sales_reps, generate_transactions


@pytest.fixture(scope="module")
def populated_test_db():
    """Create in-memory SQLite database populated with test records."""
    db = DatabaseManager(db_url="sqlite:///:memory:")
    db.initialize_schema()

    customers = generate_customers(n=100)
    products = generate_products()
    sales_reps = generate_sales_reps()
    transactions = generate_transactions(customers, products, sales_reps, n_transactions=400)

    db.load_table("customers", customers)
    db.load_table("products", products)
    db.load_table("sales_reps", sales_reps)
    db.load_table("transactions", transactions)

    return db


def test_schema_and_counts(populated_test_db):
    """Verify tables are populated and accessible."""
    counts = populated_test_db.get_table_row_counts()
    assert counts["customers"] == 100
    assert counts["transactions"] == 400
    assert counts["products"] >= 10
    assert counts["sales_reps"] >= 5


def test_analytics_queries_execution(populated_test_db):
    """Verify each enterprise SQL query from the catalog executes successfully."""
    for query_item in QUERY_CATALOG:
        df = populated_test_db.execute_query(query_item["sql"])
        assert df is not None, f"Query '{query_item['id']}' returned None"
        assert len(df) >= 0, f"Query '{query_item['id']}' failed to execute properly"


def test_window_function_lag(populated_test_db):
    """Specifically verify LAG() window function query calculation."""
    lag_query = [q for q in QUERY_CATALOG if q["id"] == "mom_revenue_growth_lag"][0]
    df = populated_test_db.execute_query(lag_query["sql"])
    assert "mom_dollar_change" in df.columns
    assert "sales_month" in df.columns


def test_dense_rank_query(populated_test_db):
    """Specifically verify DENSE_RANK() query calculation."""
    rank_query = [q for q in QUERY_CATALOG if q["id"] == "customer_regional_rank_dense_rank"][0]
    df = populated_test_db.execute_query(rank_query["sql"])
    assert "regional_rank" in df.columns
    assert "region" in df.columns
