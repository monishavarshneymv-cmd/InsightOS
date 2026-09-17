"""
InsightOS - Customer Churn Prediction Module
Implements supervised binary classification, evaluation metrics (ROC-AUC, Precision, Recall, F1),
confusion matrix derivation, global feature importance explainability, and individual risk scoring.
"""

from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
import config


class ChurnPredictor:
    """Predicts customer churn and delivers feature importance explainability."""

    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.pipeline: Optional[Pipeline] = None
        self.feature_names: list[str] = []
        self.metrics: Dict[str, Any] = {}
        self.is_trained: bool = False

        self.categorical_features = ["segment", "region", "contract_type", "payment_method"]
        self.numeric_features = [
            "tenure_months", "monthly_charges", "total_charges",
            "support_tickets", "satisfaction_score", "paperless_billing"
        ]

    def _build_pipeline(self) -> Pipeline:
        """Construct preprocessing and estimator pipeline."""
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numeric_features),
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), self.categorical_features)
            ]
        )

        if self.model_type == "logistic_regression":
            classifier = LogisticRegression(max_iter=1000, random_state=config.RANDOM_SEED, class_weight="balanced")
        else:
            classifier = RandomForestClassifier(
                n_estimators=150,
                max_depth=8,
                min_samples_split=6,
                random_state=config.RANDOM_SEED,
                class_weight="balanced"
            )

        return Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ])

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Train model and record validation metrics."""
        # Ensure target exists
        if "churn" not in df.columns:
            raise ValueError("DataFrame must contain 'churn' column.")

        X = df[self.numeric_features + self.categorical_features].copy()
        y = df["churn"].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=config.RANDOM_SEED, stratify=y
        )

        self.pipeline = self._build_pipeline()
        self.pipeline.fit(X_train, y_train)

        # Predictions
        y_pred = self.pipeline.predict(X_test)
        y_prob = self.pipeline.predict_proba(X_test)[:, 1]

        # Derive transformed feature names
        encoder = self.pipeline.named_steps["preprocessor"].named_transformers_["cat"]
        cat_encoded_cols = encoder.get_feature_names_out(self.categorical_features).tolist()
        self.feature_names = self.numeric_features + cat_encoded_cols

        # Evaluation metrics
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)

        self.metrics = {
            "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
            "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
            "confusion_matrix": cm.tolist(),
            "roc_curve": {"fpr": fpr.tolist(), "tpr": tpr.tolist()},
            "test_sample_size": len(y_test)
        }
        self.is_trained = True
        return self.metrics

    def get_feature_importances(self) -> pd.DataFrame:
        """Return global feature importances or model coefficients."""
        if not self.is_trained or self.pipeline is None:
            raise ValueError("Model must be trained before extracting feature importance.")

        classifier = self.pipeline.named_steps["classifier"]
        if hasattr(classifier, "feature_importances_"):
            importances = classifier.feature_importances_
        elif hasattr(classifier, "coef_"):
            importances = np.abs(classifier.coef_[0])
        else:
            importances = np.zeros(len(self.feature_names))

        importance_df = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance": importances
        }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

        # Normalize to 0-100%
        total = importance_df["Importance"].sum()
        if total > 0:
            importance_df["Relative_Pct"] = round((importance_df["Importance"] / total) * 100.0, 2)
        else:
            importance_df["Relative_Pct"] = 0.0

        return importance_df

    def predict_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score customer DataFrame with churn probabilities and risk categories."""
        if not self.is_trained or self.pipeline is None:
            raise ValueError("Model must be trained prior to inference.")

        X = df[self.numeric_features + self.categorical_features].copy()
        probabilities = self.pipeline.predict_proba(X)[:, 1]

        result_df = df.copy()
        result_df["churn_probability"] = np.round(probabilities, 4)
        result_df["churn_risk_level"] = pd.cut(
            result_df["churn_probability"],
            bins=[-0.01, 0.30, 0.65, 1.00],
            labels=["Low Risk", "Medium Risk", "High Risk"]
        )
        return result_df
