"""
Database management and analytical query execution engine for InsightOS.
"""
from .db_manager import DatabaseManager
from .analytics_queries import QUERY_CATALOG

__all__ = ["DatabaseManager", "QUERY_CATALOG"]
