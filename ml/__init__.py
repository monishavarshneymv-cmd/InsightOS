"""
Machine Learning Suite for InsightOS.
Modules: Customer Churn Prediction, RFM Customer Segmentation, Sales Forecasting, Anomaly Detection.
"""
from .churn_predictor import ChurnPredictor
from .customer_segmentation import CustomerSegmentation
from .sales_forecaster import SalesForecaster
from .anomaly_detector import AnomalyDetector

__all__ = ["ChurnPredictor", "CustomerSegmentation", "SalesForecaster", "AnomalyDetector"]
