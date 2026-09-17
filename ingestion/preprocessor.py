"""
InsightOS - Data Preprocessing & Cleaning Pipeline
Handles missing values, outlier detection (IQR & Z-score), date transformations,
and feature normalization for downstream analytics and machine learning.
"""

from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np


class DataPreprocessor:
    """Preprocesses and cleans tabular business data."""

    @staticmethod
    def detect_outliers_iqr(df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.Series:
        """Detect outliers using Interquartile Range (IQR) rule."""
        series = pd.to_numeric(df[column], errors="coerce")
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - multiplier * iqr
        upper_bound = q75 + multiplier * iqr
        return (series < lower_bound) | (series > upper_bound)

    @staticmethod
    def detect_outliers_zscore(df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.Series:
        """Detect outliers using standard Z-score threshold."""
        series = pd.to_numeric(df[column], errors="coerce")
        mean = series.mean()
        std = series.std(ddof=0)
        if std == 0 or np.isnan(std):
            return pd.Series(False, index=df.index)
        z_scores = np.abs((series - mean) / std)
        return z_scores > threshold

    @classmethod
    def clean_customers(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize customers table."""
        df_clean = df.copy()

        # Fill missing values if any
        if "satisfaction_score" in df_clean.columns:
            df_clean["satisfaction_score"] = df_clean["satisfaction_score"].fillna(df_clean["satisfaction_score"].median())
        if "support_tickets" in df_clean.columns:
            df_clean["support_tickets"] = df_clean["support_tickets"].fillna(0)

        # Ensure date format
        if "join_date" in df_clean.columns:
            df_clean["join_date"] = pd.to_datetime(df_clean["join_date"])

        # Numerical type casting
        df_clean["monthly_charges"] = pd.to_numeric(df_clean["monthly_charges"], errors="coerce").fillna(0.0)
        df_clean["total_charges"] = pd.to_numeric(df_clean["total_charges"], errors="coerce").fillna(0.0)
        df_clean["tenure_months"] = pd.to_numeric(df_clean["tenure_months"], errors="coerce").fillna(1).astype(int)

        return df_clean

    @classmethod
    def clean_transactions(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize transactions table."""
        df_clean = df.copy()

        # Parse datetime
        if "transaction_date" in df_clean.columns:
            df_clean["transaction_date"] = pd.to_datetime(df_clean["transaction_date"])
            df_clean["year_month"] = df_clean["transaction_date"].dt.to_period("M").astype(str)
            df_clean["day_of_week"] = df_clean["transaction_date"].dt.day_name()

        # Ensure numeric columns
        for col in ["quantity", "unit_price", "discount_pct", "total_amount", "total_cost", "net_profit"]:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0.0)

        return df_clean
