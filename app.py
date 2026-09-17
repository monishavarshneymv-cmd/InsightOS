"""
InsightOS – AI-Powered Business Intelligence & Decision Platform
Main Application Entrypoint.
"""

from pathlib import Path
import streamlit as st
import config
from database.db_manager import DatabaseManager
from database.seed_db import seed_database
from ui.styles import CUSTOM_CSS
from ui.views.overview import render_overview_view
from ui.views.eda_view import render_eda_view
from ui.views.sql_analytics import render_sql_analytics_view
from ui.views.ml_studio import render_ml_studio_view
from ui.views.ai_advisor_view import render_ai_advisor_view


# 1. Page Configuration
st.set_page_config(
    page_title="InsightOS – Decision Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Editorial Custom Styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# 3. Database Initialization & Auto-Seed
@st.cache_resource
def get_database_connection() -> DatabaseManager:
    """Initialize database and seed baseline tables if empty."""
    db = DatabaseManager()
    # Check if tables exist and have data
    counts = db.get_table_row_counts()
    if counts.get("customers", 0) == 0 or counts.get("transactions", 0) == 0:
        seed_database(force_regenerate=False)
    return db


db = get_database_connection()


# 4. Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 16px;">
        <div style="font-size: 20px; font-weight: 800; color: #0F172A; letter-spacing: -0.03em;">
            Insight<span style="color: #2563EB;">OS</span>
        </div>
        <div style="font-size: 11px; font-weight: 500; color: #64748B; margin-top: 2px;">
            AI-Powered Business Intelligence & Decision Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        "Navigation",
        options=[
            "Executive Overview",
            "Data Ingestion & Automated EDA",
            "SQL Analytics Studio",
            "Machine Learning Suite",
            "AI Business Analyst"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Telemetry Status Widget in Sidebar
    counts = db.get_table_row_counts()
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; font-size: 12px;">
        <div style="font-weight: 700; color: #1E293B; margin-bottom: 6px; text-transform: uppercase; font-size: 11px; letter-spacing: 0.04em;">
            System Telemetry
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #64748B;">
            <span>Customers:</span> <strong style="color: #0F172A;">{customers:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #64748B;">
            <span>Transactions:</span> <strong style="color: #0F172A;">{transactions:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #64748B;">
            <span>Products:</span> <strong style="color: #0F172A;">{products:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; color: #64748B;">
            <span>Database:</span> <strong style="color: #059669;">Connected</strong>
        </div>
    </div>
    """.format(**counts), unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Re-seed button in sidebar for developer flexibility
    if st.button("Regenerate Fresh Data", use_container_width=True):
        with st.spinner("Regenerating fresh synthetic data and reseeding database..."):
            seed_database(force_regenerate=True)
            st.cache_resource.clear()
            st.rerun()

    st.markdown("""
    <div style="margin-top: 30px; font-size: 11px; color: #94A3B8; text-align: center;">
        InsightOS Enterprise Decision Engine v1.0<br>Python • Pandas • Scikit-Learn • PostgreSQL • GenAI
    </div>
    """, unsafe_allow_html=True)


# 5. Route to Selected View
if nav_selection == "Executive Overview":
    render_overview_view(db)
elif nav_selection == "Data Ingestion & Automated EDA":
    render_eda_view(db)
elif nav_selection == "SQL Analytics Studio":
    render_sql_analytics_view(db)
elif nav_selection == "Machine Learning Suite":
    render_ml_studio_view(db)
elif nav_selection == "AI Business Analyst":
    render_ai_advisor_view(db)
