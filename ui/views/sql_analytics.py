"""
InsightOS - Smart SQL Insights
Friendly, business-focused query answers with instant results and optional code inspection.
"""

import time
import streamlit as st
import pandas as pd
from database.db_manager import DatabaseManager
from database.analytics_queries import QUERY_CATALOG
from ui.components import render_welcome_banner, render_insight_takeaway


def render_sql_analytics_view(db: DatabaseManager):
    """Render friendly SQL analytics view."""
    render_welcome_banner(
        title="Executive SQL Intelligence 📈",
        subtitle="Instant answers to critical business questions powered by optimized PostgreSQL window functions, CTEs, and joins.",
        badge_text="● PostgreSQL Analytics Engine"
    )

    tab_answers, tab_sandbox = st.tabs([
        "💡 Business Questions Answered",
        "🛠️ Custom SQL Sandbox (For Analysts)"
    ])

    with tab_answers:
        # User-friendly dropdown mapping
        friendly_questions = [
            "📈 How is our monthly revenue growing, and what is our dollar change? (Window Function: LAG)",
            "👑 Who are our most valuable enterprise accounts in each region? (Window Function: DENSE_RANK)",
            "📊 How does revenue accumulate across product lines over time? (Window Function: SUM OVER)",
            "🏆 How are our sales reps performing against their quotas? (CTEs & Tiered Commissions)",
            "💰 Which customer tier and product category yields the best profit? (Multi-Table Joins)",
            "⏱️ Are fulfillment delays causing customer refund requests? (CASE Statement Analysis)",
            "🎯 Which top accounts drive over 80% of our business? (Pareto Subquery)"
        ]

        selected_q_idx = st.selectbox("👉 Choose a business question to answer:", range(len(QUERY_CATALOG)), format_func=lambda x: friendly_questions[x])
        query_data = QUERY_CATALOG[selected_q_idx]

        # Execute query immediately
        start_t = time.perf_counter()
        try:
            result_df = db.execute_query(query_data["sql"])
            exec_time = (time.perf_counter() - start_t) * 1000
        except Exception as e:
            st.error(f"Error running query: {e}")
            return

        # Friendly Takeaway Header
        st.markdown(f"""
        <div class="human-card">
            <div class="human-card-header">
                <div class="human-card-title">{query_data['title']}</div>
                <span style="font-size: 11px; font-weight: 700; color: #2563EB; background: #EFF6FF; padding: 2px 8px; border-radius: 9999px;">
                    Retrieved in {exec_time:.1f} ms
                </span>
            </div>
            <div style="font-size: 14px; color: #475569; margin-bottom: 12px;">
                <strong>What this answers:</strong> {query_data['business_question']}
            </div>
        """, unsafe_allow_html=True)

        # Show Table
        st.dataframe(result_df, use_container_width=True)

        render_insight_takeaway(
            text=f"<strong>Why this SQL is powerful:</strong> {query_data['explanation']}",
            title="🧠 How the Database Solved This"
        )

        # Optional Code Inspector (Hidden by default so non-technical users aren't overwhelmed)
        with st.expander("🔍 Click to inspect the PostgreSQL query code"):
            st.code(query_data["sql"], language="sql")

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        csv_file = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download These Results as CSV",
            data=csv_file,
            file_name=f"{query_data['id']}_report.csv",
            mime="text/csv"
        )

    with tab_sandbox:
        st.markdown("<div style='font-size: 14px; color: #64748B; margin-bottom: 12px;'>Write and execute any custom SQL query directly on the live database:</div>", unsafe_allow_html=True)

        sample_sql = """SELECT 
    c.segment AS customer_tier,
    COUNT(t.transaction_id) AS orders_count,
    ROUND(SUM(t.total_amount), 2) AS total_revenue,
    ROUND(AVG(t.total_amount), 2) AS average_deal_size
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.payment_status = 'Completed'
GROUP BY c.segment
ORDER BY total_revenue DESC;"""

        user_sql = st.text_area("SQL Editor:", value=sample_sql, height=180)
        if st.button("Run My Query", type="primary"):
            try:
                t0 = time.perf_counter()
                custom_df = db.execute_query(user_sql)
                ms = (time.perf_counter() - t0) * 1000
                st.success(f"Success! Retrieved {len(custom_df):,} rows in {ms:.1f} ms.")
                st.dataframe(custom_df, use_container_width=True)
            except Exception as err:
                st.error(f"SQL Error: {err}")
