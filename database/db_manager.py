"""
InsightOS - Database Manager
Handles database connection pooling, schema initialization, bulk loading,
and safe execution of advanced analytical queries.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text, Engine
import config


class DatabaseManager:
    """Manages SQLite / PostgreSQL connections and query execution."""

    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or config.DATABASE_URL
        self._engine: Optional[Engine] = None

    @property
    def engine(self) -> Engine:
        """Lazy-initialize SQLAlchemy engine."""
        if self._engine is None:
            # For SQLite, enable check_same_thread=False for Streamlit concurrency
            connect_args = {"check_same_thread": False} if self.db_url.startswith("sqlite") else {}
            self._engine = create_engine(self.db_url, connect_args=connect_args, echo=False)
        return self._engine

    def initialize_schema(self, schema_file: Optional[Path] = None) -> None:
        """Execute DDL statements to construct tables and indexes."""
        if schema_file is None:
            schema_file = Path(__file__).resolve().parent / "schema.sql"

        with open(schema_file, "r", encoding="utf-8") as f:
            ddl_script = f.read()

        # Split statements by semicolon
        statements = [stmt.strip() for stmt in ddl_script.split(";") if stmt.strip()]
        with self.engine.begin() as conn:
            for stmt in statements:
                conn.execute(text(stmt))

    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int:
        """Load a Pandas DataFrame into the specified database table."""
        with self.engine.begin() as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        return len(df)

    def execute_query(self, sql_query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute an analytical SQL query and return results as a Pandas DataFrame."""
        with self.engine.connect() as conn:
            result_df = pd.read_sql_query(text(sql_query), conn, params=params)
        return result_df

    def get_table_row_counts(self) -> Dict[str, int]:
        """Fetch row count statistics for primary business tables."""
        tables = ["customers", "products", "sales_reps", "transactions"]
        counts = {}
        with self.engine.connect() as conn:
            for table in tables:
                try:
                    res = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    counts[table] = res.scalar() or 0
                except Exception:
                    counts[table] = 0
        return counts

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database."""
        try:
            with self.engine.connect() as conn:
                res = conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
                return True
        except Exception:
            return False
