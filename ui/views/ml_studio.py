"""
InsightOS - Machine Learning Studio
Unified predictive and unsupervised intelligence suite:
1. Customer Churn Prediction with Feature Importance Explainability
2. RFM Customer Segmentation with K-Means Clustering
3. Sales Forecasting with Autoregressive Time Series & Confidence Intervals
4. Transaction Anomaly Detection via Isolation Forest
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from database.db_manager import DatabaseManager
from ml.churn_predictor import ChurnPredictor
from ml.customer_segmentation import CustomerSegmentation
from ml.sales_forecaster import SalesForecaster
from ml.anomaly_detector import AnomalyDetector
from ui.components import render_executive_header, render_kpi_card, render_callout
from ui.styles import PLOTLY_TEMPLATE


def render_ml_studio_view(db: DatabaseManager):
    """Render the Machine Learning Studio interface."""
    render_executive_header(
        title="Machine Learning & Predictive Intelligence Studio",
        subtitle="Supervised and unsupervised models delivering churn classification, RFM segmentation, time-series forecasting, and anomaly detection.",
        badge_text="Scikit-Learn ML Suite"
    )

    tab_churn, tab_seg, tab_forecast, tab_anom = st.tabs([
        "Customer Churn Prediction",
        "RFM Customer Segmentation",
        "Revenue Forecasting",
        "Transaction Anomaly Detection"
    ])

    # =========================================================================
    # TAB 1: CUSTOMER CHURN PREDICTION
    # =========================================================================
    with tab_churn:
        st.markdown("### Customer Churn Prediction & Explainability")
        st.markdown("<div style='font-size: 14px; color: #64748B; margin-bottom: 16px;'>Supervised classification model identifying churn probabilities and feature importance drivers across 1,200 accounts.</div>", unsafe_allow_html=True)

        col_opts, col_train = st.columns([2.0, 1.0])
        with col_opts:
            model_choice = st.selectbox(
                "Model Architecture:",
                options=["Random Forest Classifier", "Logistic Regression"],
                index=0
            )
        with col_train:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            re_train = st.button("Train / Evaluate Model", type="primary", key="btn_train_churn")

        model_type_key = "logistic_regression" if "Logistic" in model_choice else "random_forest"

        # Cache model training in session state
        if "churn_predictor" not in st.session_state or re_train or st.session_state.get("churn_model_type") != model_type_key:
            with st.spinner("Training churn prediction model on cross-validation folds..."):
                cust_df = db.execute_query("SELECT * FROM customers;")
                predictor = ChurnPredictor(model_type=model_type_key)
                metrics = predictor.train(cust_df)
                st.session_state["churn_predictor"] = predictor
                st.session_state["churn_metrics"] = metrics
                st.session_state["churn_model_type"] = model_type_key

        predictor = st.session_state["churn_predictor"]
        metrics = st.session_state["churn_metrics"]

        # 1. Metrics Scorecard
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1:
            st.metric("ROC-AUC Score", f"{metrics['roc_auc']:.3f}")
        with col_m2:
            st.metric("Accuracy", f"{metrics['accuracy'] * 100:.1f}%")
        with col_m3:
            st.metric("Precision", f"{metrics['precision'] * 100:.1f}%")
        with col_m4:
            st.metric("Recall", f"{metrics['recall'] * 100:.1f}%")
        with col_m5:
            st.metric("F1-Score", f"{metrics['f1_score']:.3f}")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # 2. Feature Importance & Confusion Matrix
        col_feat, col_cm = st.columns([1.5, 1.0])
        with col_feat:
            st.markdown("#### Global Feature Importance (Explainability)")
            feat_df = predictor.get_feature_importances().head(10)
            fig_feat = px.bar(
                feat_df,
                x="Relative_Pct",
                y="Feature",
                orientation="h",
                text="Relative_Pct",
                color="Relative_Pct",
                color_continuous_scale=["#94A3B8", "#1E293B"],
                title="Top Predictive Churn Drivers (% Contribution)"
            )
            fig_feat.update_layout(
                template=PLOTLY_TEMPLATE,
                height=340,
                yaxis=dict(autorange="reversed"),
                xaxis_title="Relative Contribution (%)",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_feat, use_container_width=True)

        with col_cm:
            st.markdown("#### Validation Confusion Matrix")
            cm = np.array(metrics["confusion_matrix"])
            fig_cm = px.imshow(
                cm,
                text_auto=True,
                labels=dict(x="Predicted Class", y="Actual Class"),
                x=["Retained (0)", "Churned (1)"],
                y=["Retained (0)", "Churned (1)"],
                color_continuous_scale=["#FFFFFF", "#1E293B"]
            )
            fig_cm.update_layout(template=PLOTLY_TEMPLATE, height=340, coloraxis_showscale=False)
            st.plotly_chart(fig_cm, use_container_width=True)

        # 3. High-Risk Customer Watchlist
        st.markdown("#### High-Risk Customer Watchlist (Scored Inference)")
        cust_df = db.execute_query("SELECT * FROM customers;")
        scored_df = predictor.predict_customers(cust_df)
        high_risk = scored_df[scored_df["churn_risk_level"] == "High Risk"].sort_values(
            by="churn_probability", ascending=False
        )

        st.dataframe(
            high_risk[["customer_id", "company_name", "segment", "region", "contract_type", "monthly_charges", "support_tickets", "churn_probability", "churn_risk_level"]].head(20),
            use_container_width=True,
            hide_index=True,
            column_config={
                "churn_probability": st.column_config.ProgressColumn(
                    "Churn Probability",
                    format="%.2f",
                    min_value=0.0,
                    max_value=1.0
                ),
                "monthly_charges": st.column_config.NumberColumn("Monthly Spend", format="$%.2f")
            }
        )

    # =========================================================================
    # TAB 2: RFM CUSTOMER SEGMENTATION
    # =========================================================================
    with tab_seg:
        st.markdown("### RFM Customer Segmentation & Clustering")
        st.markdown("<div style='font-size: 14px; color: #64748B; margin-bottom: 16px;'>Derives Recency, Frequency, and Monetary (RFM) distributions and segments accounts using K-Means with Silhouette scoring.</div>", unsafe_allow_html=True)

        col_k, col_run_seg = st.columns([2.0, 1.0])
        with col_k:
            k_val = st.slider("Select Number of Clusters (K):", min_value=3, max_value=6, value=4)
        with col_run_seg:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            run_clustering = st.button("Run Segmentation", type="primary", key="btn_run_rfm")

        if "rfm_data" not in st.session_state or run_clustering or st.session_state.get("rfm_k") != k_val:
            cust_df = db.execute_query("SELECT * FROM customers;")
            txns_df = db.execute_query("SELECT * FROM transactions;")
            segmenter = CustomerSegmentation(n_clusters=k_val)
            rfm_raw = segmenter.compute_rfm(cust_df, txns_df)
            segmented_df = segmenter.fit_predict(rfm_raw)
            st.session_state["rfm_data"] = segmented_df
            st.session_state["rfm_summary"] = segmenter.get_summary()
            st.session_state["rfm_k"] = k_val

        seg_data = st.session_state["rfm_data"]
        seg_summary = st.session_state["rfm_summary"]

        st.metric("Silhouette Score (Cluster Quality)", f"{seg_summary['silhouette_score']:.3f}")

        # 2D Scatter Plot
        col_scatter, col_prof = st.columns([1.5, 1.0])
        with col_scatter:
            st.markdown("#### Recency vs. Monetary Spend Distribution")
            fig_rfm = px.scatter(
                seg_data,
                x="recency_days",
                y="monetary_total",
                color="segment_persona",
                size="frequency",
                hover_data=["company_name", "segment", "region"],
                title="Customer Segmentation Matrix",
                color_discrete_sequence=["#1E293B", "#2563EB", "#059669", "#D97706", "#BE123C"]
            )
            fig_rfm.update_layout(
                template=PLOTLY_TEMPLATE,
                height=380,
                xaxis_title="Recency (Days Since Last Order)",
                yaxis_title="Monetary Spend (USD)"
            )
            st.plotly_chart(fig_rfm, use_container_width=True)

        with col_prof:
            st.markdown("#### Segment Persona Distribution")
            st.dataframe(seg_summary["profiles"], use_container_width=True, hide_index=True)

    # =========================================================================
    # TAB 3: SALES FORECASTING
    # =========================================================================
    with tab_forecast:
        st.markdown("### Daily Sales Forecasting & Confidence Horizon")
        st.markdown("<div style='font-size: 14px; color: #64748B; margin-bottom: 16px;'>Autoregressive lag features, rolling velocity, and calendar seasonality projecting forward revenue trajectory.</div>", unsafe_allow_html=True)

        horizon = st.select_slider("Forecast Projection Window (Days):", options=[30, 45, 60, 90], value=60)

        if "forecast_df" not in st.session_state or st.session_state.get("forecast_horizon") != horizon:
            with st.spinner("Generating autoregressive sales forecast..."):
                txns_df = db.execute_query("SELECT * FROM transactions;")
                forecaster = SalesForecaster(horizon_days=horizon)
                f_df, f_metrics = forecaster.train_and_forecast(txns_df)
                st.session_state["forecast_df"] = f_df
                st.session_state["forecast_metrics"] = f_metrics
                st.session_state["forecast_history"] = forecaster.historical_daily
                st.session_state["forecast_horizon"] = horizon

        f_df = st.session_state["forecast_df"]
        f_metrics = st.session_state["forecast_metrics"]
        hist_daily = st.session_state["forecast_history"]

        col_fm1, col_fm2, col_fm3, col_fm4 = st.columns(4)
        with col_fm1:
            st.metric("Test MAE", f"${f_metrics['mae']:,.2f}")
        with col_fm2:
            st.metric("Test RMSE", f"${f_metrics['rmse']:,.2f}")
        with col_fm3:
            st.metric("Forecast MAPE", f"{f_metrics['mape_pct']:.1f}%")
        with col_fm4:
            st.metric("R² Fit Score", f"{f_metrics['r2_score']:.3f}")

        # Forecast Chart with Confidence Interval Band
        recent_hist = hist_daily.tail(90)
        fig_f = go.Figure()

        # Historical Line
        fig_f.add_trace(go.Scatter(
            x=recent_hist["date"],
            y=recent_hist["revenue"],
            name="Observed Daily Revenue",
            line=dict(color="#1E293B", width=2)
        ))

        # Upper Bound
        fig_f.add_trace(go.Scatter(
            x=f_df["date"],
            y=f_df["upper_bound_90pct"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Lower Bound + Fill
        fig_f.add_trace(go.Scatter(
            x=f_df["date"],
            y=f_df["lower_bound_90pct"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(37, 99, 235, 0.12)",
            name="90% Confidence Interval"
        ))

        # Forecast Mean
        fig_f.add_trace(go.Scatter(
            x=f_df["date"],
            y=f_df["forecast_revenue"],
            name="Forecasted Revenue",
            line=dict(color="#2563EB", width=2.5, dash="dot")
        ))

        fig_f.update_layout(
            template=PLOTLY_TEMPLATE,
            height=400,
            title=f"Historical Sales and {horizon}-Day Predictive Horizon",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_f, use_container_width=True)

    # =========================================================================
    # TAB 4: TRANSACTION ANOMALY DETECTION
    # =========================================================================
    with tab_anom:
        st.markdown("### Transaction Anomaly & Fraud Detection")
        st.markdown("<div style='font-size: 14px; color: #64748B; margin-bottom: 16px;'>Isolation Forest detecting multidimensional transactional outliers, unapproved discounts, and margin erosion.</div>", unsafe_allow_html=True)

        if "anomaly_data" not in st.session_state:
            txns_df = db.execute_query("SELECT * FROM transactions;")
            detector = AnomalyDetector()
            scored_anom = detector.fit_detect(txns_df)
            st.session_state["anomaly_data"] = scored_anom
            st.session_state["anomaly_summary"] = detector.get_summary(scored_anom)

        anom_data = st.session_state["anomaly_data"]
        anom_sum = st.session_state["anomaly_summary"]

        col_a1, col_a2, col_a3, col_a4 = st.columns(4)
        with col_a1:
            st.metric("Total Transactions", f"{anom_sum['total_transactions_analyzed']:,}")
        with col_a2:
            st.metric("Anomalies Flagged", f"{anom_sum['anomalies_detected']:,}")
        with col_a3:
            st.metric("Contamination Rate", f"{anom_sum['anomaly_rate_pct']}%")
        with col_a4:
            st.metric("Negative Margin Loss", f"${anom_sum['negative_margin_loss_usd']:,.2f}", delta="-High Risk", delta_type="inverse")

        col_anom_chart, col_anom_table = st.columns([1.0, 1.5])
        with col_anom_chart:
            st.markdown("#### Primary Anomaly Drivers")
            cause_df = pd.DataFrame(
                list(anom_sum["root_cause_distribution"].items()),
                columns=["Primary Driver", "Count"]
            ).sort_values("Count", ascending=True)

            fig_cause = px.bar(
                cause_df,
                x="Count",
                y="Primary Driver",
                orientation="h",
                text="Count",
                color_discrete_sequence=["#BE123C"]
            )
            fig_cause.update_layout(template=PLOTLY_TEMPLATE, height=320, xaxis_title="Flagged Orders")
            st.plotly_chart(fig_cause, use_container_width=True)

        with col_anom_table:
            st.markdown("#### High-Severity Anomaly Queue")
            st.dataframe(
                anom_sum["high_risk_sample"][["transaction_id", "customer_id", "quantity", "discount_pct", "total_amount", "net_profit", "anomaly_primary_cause"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_amount": st.column_config.NumberColumn("Total ($)", format="$%.2f"),
                    "net_profit": st.column_config.NumberColumn("Profit ($)", format="$%.2f"),
                    "discount_pct": st.column_config.NumberColumn("Discount", format="%.0%")
                }
            )
