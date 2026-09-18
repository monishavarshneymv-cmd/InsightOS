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
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%); color: #FFFFFF !important; font-size: 15px; font-weight: 800; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(37,99,235,0.25); letter-spacing: -0.02em;">
                IO
            </div>
            <div>
                <div class="brand-title" style="font-size: 22px !important; color: #0F172A !important;">
                    Insight<span class="brand-blue">OS</span>
                </div>
                <div class="brand-subtitle" style="color: #64748B !important;">
                    AI Business Intelligence Platform
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B !important; letter-spacing: 0.05em; margin-bottom: 8px;'>Navigation Menu</div>", unsafe_allow_html=True)

    nav_selection = st.radio(
        "Menu",
        options=[
            "📊 Executive Overview",
            "🔍 Data Health & Quality",
            "📈 SQL Business Analytics",
            "🧠 Predictive ML Studio",
            "💬 Ask InsightOS (AI Advisor)"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Friendly System Health Card
    counts = db.get_table_row_counts()
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 14px; font-size: 12.5px;">
        <div style="font-weight: 700; color: #0F172A !important; margin-bottom: 8px; font-size: 12px; display: flex; align-items: center; gap: 6px;">
            <span>🟢</span> System Status: Online
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B !important;">
            <span>Verified Clients:</span> <strong style="color: #0F172A !important;">{customers:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B !important;">
            <span>Sales Orders:</span> <strong style="color: #0F172A !important;">{transactions:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px; color: #64748B !important;">
            <span>Products Listed:</span> <strong style="color: #0F172A !important;">{products:,}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; color: #64748B !important;">
            <span>PostgreSQL Engine:</span> <strong style="color: #059669 !important;">Active</strong>
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
    <div style="margin-top: 28px; font-size: 11px; color: #94A3B8 !important; text-align: center; line-height: 1.4;">
        InsightOS Platform • Built by Monisha Varshney<br>Python • Pandas • Scikit-Learn • PostgreSQL • GenAI
    </div>
    """, unsafe_allow_html=True)


# 5. Top Brand Navbar (Visible on Main Screen)
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0 16px 0; margin-bottom: 20px; border-bottom: 1.5px solid #E2E8F0; flex-wrap: wrap; gap: 12px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%); color: #FFFFFF !important; font-size: 16px; font-weight: 800; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(37,99,235,0.25); letter-spacing: -0.02em;">
            IO
        </div>
        <div>
            <div class="brand-title" style="color: #0F172A !important;">
                Insight<span class="brand-blue">OS</span>
            </div>
            <div class="brand-subtitle" style="color: #64748B !important;">
                AI-Powered Business Intelligence & Decision Platform
            </div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="background: #ECFDF5; color: #047857 !important; font-size: 11px; font-weight: 700; padding: 5px 12px; border-radius: 9999px; border: 1px solid #A7F3D0;">
            ● Engine Online
        </span>
        <span style="background: #F1F5F9; color: #334155 !important; font-size: 11px; font-weight: 600; padding: 5px 12px; border-radius: 9999px; border: 1px solid #E2E8F0;">
            Enterprise Edition
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# 6. Route to Selected View
if "Overview" in nav_selection or "Pulse" in nav_selection:
    render_overview_view(db)
elif "Health" in nav_selection:
    render_eda_view(db)
elif "SQL" in nav_selection:
    render_sql_analytics_view(db)
elif "Predictive" in nav_selection or "ML" in nav_selection:
    render_ml_studio_view(db)
elif "Ask InsightOS" in nav_selection or "Advisor" in nav_selection:
    render_ai_advisor_view(db)
