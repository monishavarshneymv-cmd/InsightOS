"""
InsightOS - SQL Analytics Studio & Interactive Query Console
Provides prebuilt enterprise analytical queries (CTEs, Window Functions, Complex Joins, CASE statements)
and a live SQL execution laboratory. Compatible with both PostgreSQL and SQLite.
"""

import time
import streamlit as st
import pandas as pd
from database.db_manager import DatabaseManager
from database.analytics_queries import QUERY_CATALOG
from ui.components import render_executive_header, render_callout


def render_sql_analytics_view(db: DatabaseManager):
    """Render the SQL analytics workbench interface."""
    render_executive_header(
        title="SQL-Based Business Analytics Studio",
        subtitle="Advanced SQL query execution engine utilizing CTEs, Window Functions (DENSE_RANK, LAG, SUM OVER), Joins, and CASE statements.",
        badge_text="PostgreSQL / ANSI SQL Compatible"
    )

    tab_catalog, tab_console = st.tabs(["Prebuilt Analytical Query Catalog", "Interactive SQL Console"])

    # 1. Prebuilt Query Catalog Tab
    with tab_catalog:
        st.markdown("""
        <div style="font-size: 14px; color: #475569; margin-bottom: 16px;">
            Select a verified enterprise SQL query from our curated library. Each query is architected for PostgreSQL performance standards.
        </div>
        """, unsafe_allow_html=True)

        query_titles = [f"[{q['category']}] {q['title']}" for q in QUERY_CATALOG]
        selected_idx = st.selectbox("Select Business Analysis Query:", range(len(QUERY_CATALOG)), format_func=lambda x: query_titles[x])
        query_item = QUERY_CATALOG[selected_idx]

        # Query Details Header
        col_meta1, col_meta2 = st.columns([2.0, 1.0])
        with col_meta1:
            st.markdown(f"### {query_item['title']}")
            st.markdown(f"**Business Inquiry:** {query_item['business_question']}")
        with col_meta2:
            st.markdown(f"""
            <div style="text-align: right; margin-top: 10px;">
                <span class="badge-tag badge-blue" style="font-size: 12px;">{query_item['category']}</span>
            </div>
            """, unsafe_allow_html=True)

        # Technical explanation callout
        render_callout(query_item["explanation"], title="SQL Architecture & Technique", tone="info")

        # Code Block
        st.code(query_item["sql"], language="sql")

        # Execution Button
        if st.button("Execute Query", type="primary", key="btn_exec_catalog"):
            start_t = time.perf_counter()
            try:
                res_df = db.execute_query(query_item["sql"])
                duration_ms = (time.perf_counter() - start_t) * 1000

                st.success(f"Query completed in {duration_ms:.1f} ms — Retrieved {len(res_df):,} rows.")
                st.dataframe(res_df, use_container_width=True)

                # Download CSV
                csv_data = res_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Result Set (CSV)",
                    data=csv_data,
                    file_name=f"{query_item['id']}_results.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"SQL Execution Error: {str(e)}")

    # 2. Interactive SQL Console Tab
    with tab_console:
        st.markdown("""
        <div style="font-size: 14px; color: #475569; margin-bottom: 14px;">
            Execute custom SQL queries against the active database. Schema includes <code>customers</code>, <code>products</code>, <code>sales_reps</code>, and <code>transactions</code>.
        </div>
        """, unsafe_allow_html=True)

        default_sql = """-- Write custom ANSI SQL query below:
SELECT 
    c.segment,
    COUNT(t.transaction_id) AS total_orders,
    ROUND(SUM(t.total_amount), 2) AS total_revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_deal_size
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.payment_status = 'Completed'
GROUP BY c.segment
ORDER BY total_revenue DESC;"""

        user_sql = st.text_area("SQL Query Input:", value=default_sql, height=180)

        col_run, col_hint = st.columns([1.0, 3.0])
        with col_run:
            run_custom = st.button("Run Custom SQL", type="primary", key="btn_exec_custom")

        if run_custom:
            start_t = time.perf_counter()
            try:
                custom_df = db.execute_query(user_sql)
                duration_ms = (time.perf_counter() - start_t) * 1000

                st.success(f"Returned {len(custom_df):,} rows in {duration_ms:.1f} ms.")
                st.dataframe(custom_df, use_container_width=True)

                csv_custom = custom_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Export Custom Query Results (CSV)",
                    data=csv_custom,
                    file_name="custom_sql_results.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Query Execution Failure: {str(e)}")
