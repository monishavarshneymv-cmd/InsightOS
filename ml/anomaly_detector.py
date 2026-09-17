"""
InsightOS - Transaction Anomaly Detection Module
Employs Isolation Forest unsupervised learning to identify irregular transaction behaviors,
unauthorized discount spikes, negative gross margins, and volume irregularities.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import config


class AnomalyDetector:
    """Detects multi-dimensional transactional anomalies using Isolation Forest."""

    def __init__(self, contamination: float = config.ANOMALY_CONTAMINATION):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=config.RANDOM_SEED,
            n_estimators=120
        )
        self.scaler = StandardScaler()
        self.feature_columns = [
            "quantity", "unit_price", "discount_pct",
            "total_amount", "net_profit", "fulfillment_days"
        ]

    def fit_detect(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Fit model and return transactions annotated with anomaly indicators and classifications."""
        df = transactions_df.copy()

        # Ensure numeric features
        X = df[self.feature_columns].copy().fillna(0.0)
        X_scaled = self.scaler.fit_transform(X)

        # Isolation forest returns -1 for anomalies, 1 for normal
        preds = self.model.fit_predict(X_scaled)
        scores = self.model.decision_function(X_scaled)

        df["is_anomaly_detected"] = (preds == -1).astype(int)
        df["anomaly_score"] = np.round(scores, 4)

        # Root-cause classification for detected anomalies
        reasons = []
        for idx, row in df.iterrows():
            if row["is_anomaly_detected"] == 1:
                causes = []
                if row["net_profit"] < 0:
                    causes.append("Negative Profit Margin")
                if row["discount_pct"] >= 0.50:
                    causes.append(f"Excessive Discount ({row['discount_pct']*100:.0f}%)")
                if row["quantity"] > 20:
                    causes.append(f"Irregular Volume ({row['quantity']} units)")
                if row["fulfillment_days"] > 8:
                    causes.append("Severe SLA Breach")
                if not causes:
                    causes.append("Multi-attribute Outlier Vector")
                reasons.append("; ".join(causes))
            else:
                reasons.append("Normal")

        df["anomaly_primary_cause"] = reasons
        return df

    def get_summary(self, scored_df: pd.DataFrame) -> Dict[str, Any]:
        """Aggregate anomaly audit findings."""
        total_txns = len(scored_df)
        anomalies = scored_df[scored_df["is_anomaly_detected"] == 1]
        count_anom = len(anomalies)

        loss_exposure = anomalies[anomalies["net_profit"] < 0]["net_profit"].sum()

        cause_breakdown = anomalies["anomaly_primary_cause"].value_counts().to_dict()

        return {
            "total_transactions_analyzed": total_txns,
            "anomalies_detected": count_anom,
            "anomaly_rate_pct": round((count_anom / max(total_txns, 1)) * 100.0, 2),
            "negative_margin_loss_usd": round(abs(float(loss_exposure)), 2),
            "root_cause_distribution": cause_breakdown,
            "high_risk_sample": anomalies.sort_values(by="anomaly_score").head(15)
        }
