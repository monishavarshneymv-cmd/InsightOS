"""
Unit Tests for Machine Learning Models: Churn, RFM Segmentation, Sales Forecasting, and Anomaly Detection.
"""

import pytest
import pandas as pd
from data.generator import generate_customers, generate_products, generate_sales_reps, generate_transactions
from ml.churn_predictor import ChurnPredictor
from ml.customer_segmentation import CustomerSegmentation
from ml.sales_forecaster import SalesForecaster
from ml.anomaly_detector import AnomalyDetector


@pytest.fixture(scope="module")
def ml_test_data():
    """Generate datasets for ML training and evaluation."""
    customers = generate_customers(n=250)
    products = generate_products()
    sales_reps = generate_sales_reps()
    transactions = generate_transactions(customers, products, sales_reps, n_transactions=800)
    return {
        "customers": customers,
        "products": products,
        "sales_reps": sales_reps,
        "transactions": transactions
    }


def test_churn_predictor_training(ml_test_data):
    """Verify ChurnPredictor trains and outputs valid evaluation metrics and feature importances."""
    predictor = ChurnPredictor(model_type="random_forest")
    metrics = predictor.train(ml_test_data["customers"])

    assert "roc_auc" in metrics
    assert "accuracy" in metrics
    assert metrics["accuracy"] > 0.60
    assert metrics["roc_auc"] > 0.50

    feat_df = predictor.get_feature_importances()
    assert not feat_df.empty
    assert "Relative_Pct" in feat_df.columns

    scored = predictor.predict_customers(ml_test_data["customers"].head(20))
    assert "churn_probability" in scored.columns
    assert "churn_risk_level" in scored.columns


def test_customer_segmentation_rfm(ml_test_data):
    """Verify RFM calculation and K-Means clustering."""
    segmenter = CustomerSegmentation(n_clusters=4)
    rfm = segmenter.compute_rfm(ml_test_data["customers"], ml_test_data["transactions"])
    assert "recency_days" in rfm.columns
    assert "frequency" in rfm.columns
    assert "monetary_total" in rfm.columns

    clustered = segmenter.fit_predict(rfm)
    assert "cluster" in clustered.columns
    assert "segment_persona" in clustered.columns
    assert segmenter.silhouette_avg != 0.0


def test_sales_forecaster(ml_test_data):
    """Verify daily aggregation and autoregressive forecasting."""
    forecaster = SalesForecaster(horizon_days=30)
    forecast_df, metrics = forecaster.train_and_forecast(ml_test_data["transactions"])

    assert len(forecast_df) == 30
    assert "forecast_revenue" in forecast_df.columns
    assert "lower_bound_90pct" in forecast_df.columns
    assert "upper_bound_90pct" in forecast_df.columns
    assert "mae" in metrics


def test_anomaly_detector(ml_test_data):
    """Verify Isolation Forest anomaly detection and root cause breakdown."""
    detector = AnomalyDetector()
    scored = detector.fit_detect(ml_test_data["transactions"])

    assert "is_anomaly_detected" in scored.columns
    assert "anomaly_score" in scored.columns
    assert "anomaly_primary_cause" in scored.columns

    summary = detector.get_summary(scored)
    assert summary["anomalies_detected"] > 0
    assert "root_cause_distribution" in summary
