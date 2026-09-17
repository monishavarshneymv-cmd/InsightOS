"""
InsightOS - Sales Forecasting Module
Performs time-series aggregation, autoregressive feature engineering (lags, rolling stats, seasonality),
trains regression models, computes validation metrics (MAE, RMSE, MAPE), and forecasts forward revenue with confidence intervals.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import config


class SalesForecaster:
    """Time-series daily revenue forecasting engine."""

    def __init__(self, horizon_days: int = config.FORECAST_HORIZON_DAYS):
        self.horizon_days = horizon_days
        self.model = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=config.RANDOM_SEED)
        self.metrics: Dict[str, float] = {}
        self.historical_daily: pd.DataFrame | None = None
        self.forecast_df: pd.DataFrame | None = None

    def prepare_time_series(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate transactions to daily revenue series and build lag features."""
        df = transactions_df[transactions_df["payment_status"] == "Completed"].copy()
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        df["date"] = df["transaction_date"].dt.normalize()

        daily = df.groupby("date").agg(
            revenue=("total_amount", "sum"),
            order_count=("transaction_id", "count"),
            avg_order_value=("total_amount", "mean")
        ).reset_index()

        daily = daily.sort_values("date").reset_index(drop=True)
        # Fill any missing calendar dates with 0
        full_idx = pd.date_range(start=daily["date"].min(), end=daily["date"].max(), freq="D")
        daily = daily.set_index("date").reindex(full_idx, fill_value=0.0).rename_axis("date").reset_index()

        # Feature engineering
        daily["day_of_week"] = daily["date"].dt.dayofweek
        daily["day_of_month"] = daily["date"].dt.day
        daily["month"] = daily["date"].dt.month
        daily["is_weekend"] = daily["day_of_week"].isin([5, 6]).astype(int)

        # Autoregressive lags
        for lag in [1, 7, 14, 21, 28]:
            daily[f"lag_{lag}"] = daily["revenue"].shift(lag)

        # Rolling window averages
        daily["rolling_mean_7"] = daily["revenue"].shift(1).rolling(window=7, min_periods=1).mean()
        daily["rolling_mean_14"] = daily["revenue"].shift(1).rolling(window=14, min_periods=1).mean()
        daily["rolling_mean_30"] = daily["revenue"].shift(1).rolling(window=30, min_periods=1).mean()

        # Drop initial NaN rows created by lags
        self.historical_daily = daily.dropna().reset_index(drop=True)
        return self.historical_daily

    def train_and_forecast(self, transactions_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """Train forecaster on time series and project forward horizon."""
        daily = self.prepare_time_series(transactions_df)

        feature_cols = [
            "day_of_week", "day_of_month", "month", "is_weekend",
            "lag_1", "lag_7", "lag_14", "lag_21", "lag_28",
            "rolling_mean_7", "rolling_mean_14", "rolling_mean_30"
        ]

        # Holdout split: last 60 days for validation
        test_size = min(60, len(daily) // 5)
        train_data = daily.iloc[:-test_size]
        test_data = daily.iloc[-test_size:]

        X_train, y_train = train_data[feature_cols], train_data["revenue"]
        X_test, y_test = test_data[feature_cols], test_data["revenue"]

        # Train model
        self.model.fit(X_train, y_train)
        preds_test = self.model.predict(X_test)

        # Calculate metrics
        mae = float(mean_absolute_error(y_test, preds_test))
        rmse = float(np.sqrt(mean_squared_error(y_test, preds_test)))
        r2 = float(r2_score(y_test, preds_test))
        mape = float(np.mean(np.abs((y_test - preds_test) / np.maximum(y_test, 1.0))) * 100.0)

        self.metrics = {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2_score": round(r2, 4),
            "mape_pct": round(mape, 2)
        }

        # Retrain on full historical dataset for forward projection
        self.model.fit(daily[feature_cols], daily["revenue"])

        # Recursive Multi-Step Forward Forecast
        future_dates = pd.date_range(start=daily["date"].max() + timedelta(days=1), periods=self.horizon_days, freq="D")
        extended_series = daily[["date", "revenue"]].copy()

        future_records = []
        residual_std = rmse  # Use test RMSE as standard error estimate for confidence bounds

        for target_date in future_dates:
            # Recompute lag features from extended_series
            rev_history = extended_series["revenue"].values

            features = {
                "day_of_week": target_date.dayofweek,
                "day_of_month": target_date.day,
                "month": target_date.month,
                "is_weekend": 1 if target_date.dayofweek in [5, 6] else 0,
                "lag_1": rev_history[-1],
                "lag_7": rev_history[-7] if len(rev_history) >= 7 else rev_history[-1],
                "lag_14": rev_history[-14] if len(rev_history) >= 14 else rev_history[-1],
                "lag_21": rev_history[-21] if len(rev_history) >= 21 else rev_history[-1],
                "lag_28": rev_history[-28] if len(rev_history) >= 28 else rev_history[-1],
                "rolling_mean_7": np.mean(rev_history[-7:]),
                "rolling_mean_14": np.mean(rev_history[-14:]),
                "rolling_mean_30": np.mean(rev_history[-30:] if len(rev_history) >= 30 else rev_history)
            }

            feat_df = pd.DataFrame([features])[feature_cols]
            pred_rev = max(0.0, float(self.model.predict(feat_df)[0]))

            # Append to extended series for recursive autoregression
            new_row = pd.DataFrame([{"date": target_date, "revenue": pred_rev}])
            extended_series = pd.concat([extended_series, new_row], ignore_index=True)

            lower_bound = max(0.0, pred_rev - 1.645 * residual_std)
            upper_bound = pred_rev + 1.645 * residual_std

            future_records.append({
                "date": target_date,
                "forecast_revenue": round(pred_rev, 2),
                "lower_bound_90pct": round(lower_bound, 2),
                "upper_bound_90pct": round(upper_bound, 2)
            })

        self.forecast_df = pd.DataFrame(future_records)
        return self.forecast_df, self.metrics
