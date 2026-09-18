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

# 2. Inject Warm, Human-Crafted Styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# 3. Database Initialization & Auto-Seed
@st.cache_resource
def get_database_connection() -> DatabaseManager:
    """Initialize database and seed baseline tables if empty."""
    db = DatabaseManager()
    counts = db.get_table_row_counts()
    if counts.get("customers", 0) == 0 or counts.get("transactions", 0) == 0:
        seed_database(force_regenerate=False)
    return db


db = get_database_connection()


# 4. Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 6px 0 16px 0; border-bottom: 1.5px solid #E2E8F0; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #0F172A; color: #FFFFFF; font-size: 16px; font-weight: 800; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                ⚡
            </div>
            <div>
                <div class="brand-title" style="font-size: 22px !important;">
                    Insight<span class="brand-blue">OS</span>
                </div>
                <div class="brand-subtitle">
                    AI Business Intelligence Platform
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em; margin-bottom: 8px;'>Main Navigation Menu</div>", unsafe_allow_html=True)

    nav_selection = st.radio(
        "Menu",
        options=[
            "📊 Business Pulse",
            "🔍 Data Health & Explorer",
            "📈 Smart SQL Insights",
            "🤖 Predictive Machine Learning",
            "💬 Ask InsightOS (AI Advisor)"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Friendly System Health Card
    counts = db.get_table_row_counts()
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; font-size: 12.5px;">
        <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px; font-size: 12px; display: flex; align-items: center; gap: 6px;">
            <span>🟢</span> Live System Health
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B;">
            <span>Verified Clients:</span> <strong style="color: #0F172A;">{customers:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B;">
            <span>Sales Orders:</span> <strong style="color: #0F172A;">{transactions:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B;">
            <span>Products Listed:</span> <strong style="color: #0F172A;">{products:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; color: #64748B;">
            <span>PostgreSQL Engine:</span> <strong style="color: #059669;">Active</strong>
        </div>
    </div>
    """.format(**counts), unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Refresh data button
    if st.button("🔄 Reset to Fresh Demo Data", use_container_width=True):
        with st.spinner("Re-generating clean demo dataset..."):
            seed_database(force_regenerate=True)
            st.cache_resource.clear()
            st.rerun()

    st.markdown("""
    <div style="margin-top: 28px; font-size: 11px; color: #94A3B8; text-align: center; line-height: 1.4;">
        InsightOS Platform • Built by Monisha Varshney<br>Python • Pandas • Scikit-Learn • PostgreSQL • GenAI
    </div>
    """, unsafe_allow_html=True)


# 5. Top Brand Navbar (Visible on Main Screen)
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0 16px 0; margin-bottom: 20px; border-bottom: 1.5px solid #E2E8F0;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="background: #0F172A; color: #FFFFFF; font-size: 18px; font-weight: 800; width: 38px; height: 38px; border-radius: 9px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(15,23,42,0.12);">
            ⚡
        </div>
        <div>
            <div class="brand-title">
                Insight<span class="brand-blue">OS</span>
            </div>
            <div class="brand-subtitle">
                AI-Powered Business Intelligence & Decision Platform
            </div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="background: #ECFDF5; color: #047857; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #A7F3D0;">
            ● Engine Online
        </span>
        <span style="background: #F1F5F9; color: #334155; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 9999px; border: 1px solid #E2E8F0;">
            Enterprise Edition
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# 6. Route to Selected View
if "Business Pulse" in nav_selection:
    render_overview_view(db)
elif "Data Health" in nav_selection:
    render_eda_view(db)
elif "Smart SQL" in nav_selection:
    render_sql_analytics_view(db)
elif "Predictive" in nav_selection:
    render_ml_studio_view(db)
elif "Ask InsightOS" in nav_selection:
    render_ai_advisor_view(db)
