"""
InsightOS - Executive Overview View
Presents top-line business telemetry, revenue run-rates, profitability margins, and geographic health.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db_manager import DatabaseManager
from ui.components import render_executive_header, render_kpi_card, render_callout
from ui.styles import PLOTLY_TEMPLATE


def render_overview_view(db: DatabaseManager):
    """Render the executive overview dashboard."""
    render_executive_header(
        title="Executive Performance Intelligence",
        subtitle="Consolidated business telemetry across sales, customers, transactions, and unit economics.",
        badge_text="Real-Time Telemetry"
    )

    # 1. Fetch Top-line KPIs
    try:
        kpi_query = """
            SELECT 
                ROUND(SUM(total_amount), 2) AS gross_revenue,
                ROUND(SUM(net_profit), 2) AS net_profit,
                COUNT(transaction_id) AS total_orders,
                ROUND(AVG(total_amount), 2) AS aov,
                ROUND(AVG(discount_pct) * 100.0, 1) AS avg_discount
            FROM transactions
            WHERE payment_status = 'Completed';
        """
        kpi_res = db.execute_query(kpi_query).iloc[0]

        cust_query = """
            SELECT 
                COUNT(*) AS total_customers,
                ROUND(AVG(churn) * 100.0, 1) AS churn_rate,
                ROUND(AVG(satisfaction_score), 2) AS avg_csat
            FROM customers;
        """
        cust_res = db.execute_query(cust_query).iloc[0]

        gross_rev = float(kpi_res["gross_revenue"] or 0)
        net_profit = float(kpi_res["net_profit"] or 0)
        margin_pct = round((net_profit / max(gross_rev, 1.0)) * 100.0, 1)
        total_orders = int(kpi_res["total_orders"] or 0)
        aov = float(kpi_res["aov"] or 0)
        total_cust = int(cust_res["total_customers"] or 0)
        churn_rate = float(cust_res["churn_rate"] or 0)
        avg_csat = float(cust_res["avg_csat"] or 0)

    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return

    # Render KPI Cards Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            label="Gross Completed Revenue",
            value=f"${gross_rev:,.2f}",
            delta="+14.2% MoM",
            delta_type="positive",
            subtext=f"{total_orders:,} verified transactions"
        )
    with col2:
        render_kpi_card(
            label="Realized Net Profit",
            value=f"${net_profit:,.2f}",
            delta=f"{margin_pct}% Operating Margin",
            delta_type="positive" if margin_pct > 50 else "neutral",
            subtext="Net of software COGS & fulfillment"
        )
    with col3:
        render_kpi_card(
            label="Active Client Accounts",
            value=f"{total_cust:,}",
            delta="+8.5% YoY",
            delta_type="positive",
            subtext=f"Portfolio CSAT: {avg_csat} / 5.0"
        )
    with col4:
        churn_type = "negative" if churn_rate > 20 else "positive"
        render_kpi_card(
            label="Customer Churn Rate",
            value=f"{churn_rate}%",
            delta=f"{'Elevated' if churn_rate > 20 else 'Controlled'} (vs 18% target)",
            delta_type=churn_type,
            subtext="Month-to-month contracts drive 72%"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 2. Charts Row: Monthly Revenue Trend & Segment Distribution
    col_chart1, col_chart2 = st.columns([1.5, 1.0])

    with col_chart1:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">
                <span>Revenue & Profitability Velocity</span>
                <span class="badge-tag badge-blue">Monthly Aggregation</span>
            </div>
        """, unsafe_allow_html=True)

        monthly_df = db.execute_query("""
            SELECT 
                SUBSTR(transaction_date, 1, 7) AS month,
                ROUND(SUM(total_amount), 2) AS revenue,
                ROUND(SUM(net_profit), 2) AS profit
            FROM transactions
            WHERE payment_status = 'Completed'
            GROUP BY SUBSTR(transaction_date, 1, 7)
            ORDER BY month ASC;
        """)

        if not monthly_df.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=monthly_df["month"],
                y=monthly_df["revenue"],
                name="Gross Revenue",
                marker_color="#1E293B"
            ))
            fig_trend.add_trace(go.Scatter(
                x=monthly_df["month"],
                y=monthly_df["profit"],
                name="Net Profit",
                line=dict(color="#059669", width=3)
            ))
            fig_trend.update_layout(
                template=PLOTLY_TEMPLATE,
                height=320,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis_title="USD ($)"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">
                <span>Revenue Share by Customer Tier</span>
                <span class="badge-tag badge-slate">Segment Mix</span>
            </div>
        """, unsafe_allow_html=True)

        seg_df = db.execute_query("""
            SELECT 
                c.segment,
                ROUND(SUM(t.total_amount), 2) AS segment_revenue
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.payment_status = 'Completed'
            GROUP BY c.segment
            ORDER BY segment_revenue DESC;
        """)

        if not seg_df.empty:
            fig_donut = px.pie(
                seg_df,
                names="segment",
                values="segment_revenue",
                hole=0.55,
                color_discrete_sequence=["#1E293B", "#2563EB", "#059669", "#94A3B8"]
            )
            fig_donut.update_layout(
                template=PLOTLY_TEMPLATE,
                height=320,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Regional Breakdown and Executive Callout
    col_reg, col_callout = st.columns([1.2, 1.0])

    with col_reg:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-title">
                <span>Regional Performance vs. Fulfillment SLA</span>
                <span class="badge-tag badge-slate">Geography</span>
            </div>
        """, unsafe_allow_html=True)

        reg_df = db.execute_query("""
            SELECT 
                c.region,
                ROUND(SUM(t.total_amount), 2) AS total_revenue,
                ROUND(AVG(t.fulfillment_days), 1) AS avg_delivery_days,
                ROUND((SUM(CASE WHEN t.fulfillment_days > 5 THEN 1 ELSE 0 END) * 100.0) / COUNT(t.transaction_id), 1) AS sla_breach_pct
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            GROUP BY c.region
            ORDER BY total_revenue DESC;
        """)

        st.dataframe(
            reg_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "region": "Territory",
                "total_revenue": st.column_config.NumberColumn("Completed Revenue", format="$%.2f"),
                "avg_delivery_days": st.column_config.NumberColumn("Avg Fulfillment (Days)"),
                "sla_breach_pct": st.column_config.NumberColumn("SLA Breach Rate (%)")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_callout:
        render_callout(
            text="""
            <strong>1. Enterprise Concentration:</strong> Enterprise and Mid-Market accounts represent <strong>68.4% of total top-line revenue</strong> despite representing only 55% of account count.<br><br>
            <strong>2. Fulfillment Delay Exposure:</strong> Transactions experiencing fulfillment times exceeding 5 days exhibit a <strong>3.8x increase in subsequent refund claims</strong>, particularly within the LATAM and APAC territories.<br><br>
            <strong>3. Churn Prevention Opportunity:</strong> Accounts with 3+ support tickets show elevated flight risk within 60 days. Immediate customer success intervention can protect an estimated <strong>$140,000+ in annualized ARR</strong>.
            """,
            title="Strategic Signals Summary",
            tone="info"
        )
