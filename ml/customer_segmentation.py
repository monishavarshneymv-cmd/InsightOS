"""
InsightOS - Customer Segmentation & RFM Clustering Module
Calculates Recency, Frequency, Monetary (RFM) distributions, performs K-Means clustering,
computes Silhouette evaluation metrics, and maps mathematical clusters to human business personas.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import config


class CustomerSegmentation:
    """RFM Analysis and K-Means Customer Clustering."""

    def __init__(self, n_clusters: int = config.RFM_CLUSTERS):
        self.n_clusters = n_clusters
        self.kmeans: KMeans | None = None
        self.scaler = StandardScaler()
        self.silhouette_avg: float = 0.0
        self.cluster_profiles: pd.DataFrame | None = None

    def compute_rfm(self, customers_df: pd.DataFrame, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Derive Recency, Frequency, and Monetary metrics per customer."""
        txns = transactions_df[transactions_df["payment_status"] == "Completed"].copy()
        txns["transaction_date"] = pd.to_datetime(txns["transaction_date"])
        ref_date = txns["transaction_date"].max()

        # Group by customer
        rfm = txns.groupby("customer_id").agg({
            "transaction_date": lambda x: (ref_date - x.max()).days,
            "transaction_id": "count",
            "total_amount": "sum"
        }).reset_index()

        rfm.columns = ["customer_id", "recency_days", "frequency", "monetary_total"]
        rfm["monetary_total"] = rfm["monetary_total"].round(2)

        # Merge with customer metadata
        merged = pd.merge(
            customers_df[["customer_id", "company_name", "segment", "region", "tenure_months"]],
            rfm,
            on="customer_id",
            how="inner"
        )
        return merged

    def fit_predict(self, rfm_df: pd.DataFrame) -> pd.DataFrame:
        """Scale RFM features, fit K-Means, and assign executive personas."""
        df = rfm_df.copy()

        # Log transform to reduce positive skewness
        rfm_features = ["recency_days", "frequency", "monetary_total"]
        log_transformed = np.log1p(df[rfm_features])
        scaled_features = self.scaler.fit_transform(log_transformed)

        # Fit K-Means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=config.RANDOM_SEED,
            n_init=10
        )
        cluster_labels = self.kmeans.fit_predict(scaled_features)
        df["cluster"] = cluster_labels

        # Silhouette score
        if len(df) > self.n_clusters:
            self.silhouette_avg = round(float(silhouette_score(scaled_features, cluster_labels)), 4)

        # Map clusters to descriptive personas based on relative RFM averages
        cluster_means = df.groupby("cluster")[rfm_features].mean()
        
        # Determine personas by sorting on Monetary and Recency
        # High M, High F, Low R = Champions
        # High M, High R = At-Risk High Value
        # Low M, Low R = New / Promising
        # Low M, High R = Hibernating
        personas = {}
        for c in range(self.n_clusters):
            row = cluster_means.loc[c]
            r = row["recency_days"]
            m = row["monetary_total"]
            f = row["frequency"]

            if m >= cluster_means["monetary_total"].median() and r <= cluster_means["recency_days"].median():
                personas[c] = "Champions (High Value, Active)"
            elif m >= cluster_means["monetary_total"].median() and r > cluster_means["recency_days"].median():
                personas[c] = "At-Risk Enterprise Accounts"
            elif m < cluster_means["monetary_total"].median() and r <= cluster_means["recency_days"].median():
                personas[c] = "Promising Growth / Frequent"
            else:
                personas[c] = "Hibernating / Low Engagement"

        # If duplicate persona names occur due to tight groupings, make unique
        seen = {}
        unique_personas = {}
        for c, name in personas.items():
            if name in seen:
                seen[name] += 1
                unique_personas[c] = f"{name} Tier {seen[name]}"
            else:
                seen[name] = 1
                unique_personas[c] = name

        df["segment_persona"] = df["cluster"].map(unique_personas)

        # Compute cluster profile summary
        self.cluster_profiles = df.groupby(["cluster", "segment_persona"]).agg(
            account_count=("customer_id", "count"),
            avg_recency_days=("recency_days", lambda x: round(x.mean(), 1)),
            avg_frequency=("frequency", lambda x: round(x.mean(), 1)),
            avg_monetary=("monetary_total", lambda x: round(x.mean(), 2)),
            total_spend_share=("monetary_total", lambda x: round((x.sum() / df["monetary_total"].sum()) * 100.0, 1))
        ).reset_index()

        return df

    def get_summary(self) -> Dict[str, Any]:
        """Return segmentation metrics and profile table."""
        return {
            "n_clusters": self.n_clusters,
            "silhouette_score": self.silhouette_avg,
            "profiles": self.cluster_profiles
        }
