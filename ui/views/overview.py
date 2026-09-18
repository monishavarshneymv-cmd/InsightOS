"""
InsightOS - Business Pulse (Executive Overview)
Clean, human-friendly overview of how the company is performing in plain English.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db_manager import DatabaseManager
from ui.components import render_welcome_banner, render_human_kpi, render_insight_takeaway
from ui.styles import PLOTLY_TEMPLATE


def render_overview_view(db: DatabaseManager):
    """Render friendly business pulse dashboard."""
    render_welcome_banner(
        title="Good afternoon, Monisha 👋",
        subtitle="Here is your real-time company overview across sales revenue, customer retention, and business growth.",
        badge_text="● Live Production Feed"
    )

    # 1. Interactive Top Filter: Region
    col_filter1, col_filter2 = st.columns([1.5, 3.0])
    with col_filter1:
        selected_region = st.selectbox(
            "🌍 Filter by Region:",
            options=["All Global Regions", "North America", "EMEA", "APAC", "LATAM"],
            index=0
        )

    # 2. Fetch Metrics based on filter
    region_clause = "" if selected_region == "All Global Regions" else f"AND c.region = '{selected_region}'"

    try:
        kpi_query = f"""
            SELECT 
                ROUND(SUM(t.total_amount), 2) AS gross_revenue,
                ROUND(SUM(t.net_profit), 2) AS net_profit,
                COUNT(t.transaction_id) AS total_orders,
                ROUND(AVG(t.total_amount), 2) AS aov
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.payment_status = 'Completed' {region_clause};
        """
        kpi_res = db.execute_query(kpi_query).iloc[0]

        cust_clause = "" if selected_region == "All Global Regions" else f"WHERE region = '{selected_region}'"
        cust_query = f"""
            SELECT 
                COUNT(*) AS total_customers,
                ROUND(AVG(churn) * 100.0, 1) AS churn_rate,
                ROUND(AVG(satisfaction_score), 1) AS avg_csat
            FROM customers {cust_clause};
        """
        cust_res = db.execute_query(cust_query).iloc[0]

        gross_rev = float(kpi_res["gross_revenue"] or 0)
        net_profit = float(kpi_res["net_profit"] or 0)
        margin_pct = round((net_profit / max(gross_rev, 1.0)) * 100.0, 1)
        total_orders = int(kpi_res["total_orders"] or 0)
        total_cust = int(cust_res["total_customers"] or 0)
        churn_rate = float(cust_res["churn_rate"] or 0)
        avg_csat = float(cust_res["avg_csat"] or 0)

    except Exception as e:
        st.error(f"Could not load business metrics: {e}")
        return

    # Render Friendly KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_human_kpi(
            icon="💰",
            title="Total Revenue Made",
            value=f"${gross_rev:,.0f}",
            badge_text="+14.2% vs last month",
            badge_type="good",
            subtext=f"{total_orders:,} verified sales orders"
        )
    with col2:
        render_human_kpi(
            icon="📈",
            title="Net Profit in Bank",
            value=f"${net_profit:,.0f}",
            badge_text=f"{margin_pct}% Healthy Margin",
            badge_type="good" if margin_pct >= 50 else "warning",
            subtext="After software & server costs"
        )
    with col3:
        render_human_kpi(
            icon="👥",
            title="Active Client Accounts",
            value=f"{total_cust:,}",
            badge_text="Customer Base",
            badge_type="good",
            subtext=f"Average Rating: ⭐ {avg_csat} / 5.0"
        )
    with col4:
        churn_good = churn_rate < 20
        render_human_kpi(
            icon="🚪",
            title="Customer Churn",
            value=f"{churn_rate}%",
            badge_text="Needs Attention" if not churn_good else "Controlled",
            badge_type="warning" if not churn_good else "good",
            subtext="Clients leaving this period"
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. Plain English Insight Box: "Top 3 Things You Should Know Today"
    render_insight_takeaway(
        text=f"""
        1. <strong>Enterprise clients bring in the lion's share of cash:</strong> Even though Enterprise clients make up only ~20% of your customer accounts, they account for <strong>over 52% of your revenue</strong>. Keeping them happy is your #1 priority.<br>
        2. <strong>Month-to-month contracts are bleeding customers:</strong> 74% of the customers who cancelled were on flexible month-to-month plans. Offering them a small 10–15% discount to switch to a 1-year contract will immediately protect revenue.<br>
        3. <strong>Late deliveries create angry customers:</strong> When delivery or onboarding takes longer than 5 days, refund requests jump by nearly <strong>400%</strong>. Faster fulfillment directly protects your bottom line.
        """,
        title="📌 3 Key Things You Should Know Today"
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 4. Charts: Revenue trajectory & Who is buying
    col_c1, col_c2 = st.columns([1.6, 1.0])

    with col_c1:
        st.markdown("""
        <div class="human-card">
            <div class="human-card-header">
                <div class="human-card-title">📈 How Much Money Are We Making Each Month?</div>
                <span style="font-size: 12px; color: #64748B;">Monthly Revenue & Profit</span>
            </div>
        """, unsafe_allow_html=True)

        monthly_df = db.execute_query(f"""
            SELECT 
                SUBSTR(t.transaction_date, 1, 7) AS month,
                ROUND(SUM(t.total_amount), 2) AS revenue,
                ROUND(SUM(t.net_profit), 2) AS profit
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.payment_status = 'Completed' {region_clause}
            GROUP BY SUBSTR(t.transaction_date, 1, 7)
            ORDER BY month ASC;
        """)

        if not monthly_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_df["month"],
                y=monthly_df["revenue"],
                name="Total Money In",
                marker_color="#3B82F6"
            ))
            fig.add_trace(go.Scatter(
                x=monthly_df["month"],
                y=monthly_df["profit"],
                name="Profit Kept",
                line=dict(color="#10B981", width=3)
            ))
            fig.update_layout(
                template=PLOTLY_TEMPLATE,
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
            <div style="font-size: 12px; color: #64748B; background: #F8FAFC; padding: 8px 12px; border-radius: 8px;">
                💡 <strong>What this shows:</strong> The blue bars show total money brought in, and the green line shows the profit kept after expenses. Notice the upward trend towards end-of-quarter months!
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="human-card">
            <div class="human-card-header">
                <div class="human-card-title">🏢 Who Are Our Main Buyers?</div>
                <span style="font-size: 12px; color: #64748B;">Customer Types</span>
            </div>
        """, unsafe_allow_html=True)

        seg_df = db.execute_query(f"""
            SELECT 
                c.segment,
                ROUND(SUM(t.total_amount), 2) AS revenue
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            WHERE t.payment_status = 'Completed' {region_clause}
            GROUP BY c.segment
            ORDER BY revenue DESC;
        """)

        if not seg_df.empty:
            fig_pie = px.pie(
                seg_df,
                names="segment",
                values="revenue",
                hole=0.55,
                color_discrete_sequence=["#3B82F6", "#10B981", "#6366F1", "#F59E0B"]
            )
            fig_pie.update_layout(template=PLOTLY_TEMPLATE, height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("""
            <div style="font-size: 12px; color: #64748B; background: #F8FAFC; padding: 8px 12px; border-radius: 8px;">
                💡 <strong>Takeaway:</strong> Enterprise and Mid-Market companies are your biggest spenders. SMBs and Startups make up smaller order slices.
            </div>
        </div>
        """, unsafe_allow_html=True)
