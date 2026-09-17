"""
InsightOS - Automated Exploratory Data Analysis (EDA) Engine
Computes comprehensive statistical summaries, distribution metrics, outlier diagnostics,
correlation matrices, and temporal business trends automatically.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .preprocessor import DataPreprocessor


class EDAEngine:
    """Automated Exploratory Data Analysis Engine."""

    def __init__(self, df: pd.DataFrame, dataset_name: str = "Dataset"):
        self.df = df.copy()
        self.dataset_name = dataset_name
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        self.datetime_cols = self.df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

    def get_dataset_overview(self) -> Dict[str, Any]:
        """Return high-level metadata about dataset dimensions and memory."""
        mem_mb = self.df.memory_usage(deep=True).sum() / (1024 * 1024)
        return {
            "name": self.dataset_name,
            "rows": int(len(self.df)),
            "columns": int(len(self.df.columns)),
            "numeric_columns_count": len(self.numeric_cols),
            "categorical_columns_count": len(self.categorical_cols),
            "datetime_columns_count": len(self.datetime_cols),
            "memory_usage_mb": round(mem_mb, 2),
            "duplicate_rows": int(self.df.duplicated().sum())
        }

    def get_missing_values_summary(self) -> pd.DataFrame:
        """Calculate missing value counts and proportions."""
        null_counts = self.df.isnull().sum()
        null_pct = (null_counts / max(len(self.df), 1)) * 100
        dtypes = self.df.dtypes
        summary = pd.DataFrame({
            "Column": self.df.columns,
            "Data Type": [str(dtypes[c]) for c in self.df.columns],
            "Missing Count": null_counts.values,
            "Missing Pct (%)": null_pct.round(2).values
        }).sort_values(by="Missing Count", ascending=False).reset_index(drop=True)
        return summary

    def get_numerical_statistics(self) -> pd.DataFrame:
        """Compute advanced descriptive statistics including skewness and IQR."""
        if not self.numeric_cols:
            return pd.DataFrame()

        records = []
        for col in self.numeric_cols:
            series = self.df[col].dropna()
            if len(series) == 0:
                continue
            q25 = float(series.quantile(0.25))
            q75 = float(series.quantile(0.75))
            iqr = q75 - q25
            skew = float(series.skew()) if len(series) > 2 else 0.0
            kurt = float(series.kurtosis()) if len(series) > 3 else 0.0

            iqr_outliers = int(DataPreprocessor.detect_outliers_iqr(self.df, col).sum())
            z_outliers = int(DataPreprocessor.detect_outliers_zscore(self.df, col).sum())

            records.append({
                "Feature": col,
                "Count": int(len(series)),
                "Mean": round(float(series.mean()), 2),
                "Std Dev": round(float(series.std()), 2),
                "Min": round(float(series.min()), 2),
                "25%": round(q25, 2),
                "Median (50%)": round(float(series.median()), 2),
                "75%": round(q75, 2),
                "Max": round(float(series.max()), 2),
                "IQR": round(iqr, 2),
                "Skewness": round(skew, 2),
                "Kurtosis": round(kurt, 2),
                "IQR Outliers": iqr_outliers,
                "Z-Score Outliers (>3σ)": z_outliers
            })

        return pd.DataFrame(records)

    def get_categorical_summary(self, max_cardinality: int = 20) -> Dict[str, pd.DataFrame]:
        """Compute frequency breakdown for categorical columns."""
        summaries = {}
        for col in self.categorical_cols:
            val_counts = self.df[col].value_counts(dropna=False).head(max_cardinality)
            pct = (val_counts / max(len(self.df), 1)) * 100
            summaries[col] = pd.DataFrame({
                "Value": val_counts.index.astype(str),
                "Count": val_counts.values,
                "Percentage (%)": pct.round(2).values
            })
        return summaries

    def get_correlation_matrix(self, method: str = "pearson") -> pd.DataFrame:
        """Compute correlation matrix among numeric features."""
        if len(self.numeric_cols) < 2:
            return pd.DataFrame()
        corr = self.df[self.numeric_cols].corr(method=method)
        return corr.round(3)

    def run_full_audit(self) -> Dict[str, Any]:
        """Execute complete automated EDA pipeline."""
        return {
            "overview": self.get_dataset_overview(),
            "missing_values": self.get_missing_values_summary(),
            "numerical_stats": self.get_numerical_statistics(),
            "categorical_breakdown": self.get_categorical_summary(),
            "correlation_matrix": self.get_correlation_matrix()
        }
