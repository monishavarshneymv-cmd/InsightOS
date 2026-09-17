"""
InsightOS - AI Business Advisor View
Executive AI Decision Intelligence partner powered by RAG and quantitative business telemetry.
Synthesizes natural-language business questions into actionable 4-part C-suite decision briefings.
"""

from typing import Dict, Any, List
import streamlit as st
from database.db_manager import DatabaseManager
from ai_analyst.rag_engine import BusinessRAGEngine
from ai_analyst.business_advisor import BusinessAdvisor
from ui.components import render_executive_header, render_callout


def render_ai_advisor_view(db: DatabaseManager):
    """Render the AI Business Advisor conversational decision interface."""
    render_executive_header(
        title="AI Business Analyst & Decision Engine",
        subtitle="Conversational business intelligence powered by RAG, SQL telemetry, and predictive ML models.",
        badge_text="Executive Decision Intelligence"
    )

    # Initialize RAG & Advisor in session state
    if "rag_engine" not in st.session_state:
        with st.spinner("Indexing relational schema, live metrics, and ML models into RAG knowledge base..."):
            rag = BusinessRAGEngine(db)
            # Pass any available ML artifacts
            ml_artifacts = {}
            if "churn_predictor" in st.session_state:
                ml_artifacts["churn_features"] = st.session_state["churn_predictor"].get_feature_importances()
            if "rfm_summary" in st.session_state:
                ml_artifacts["rfm_summary"] = st.session_state["rfm_summary"]
            if "anomaly_summary" in st.session_state:
                ml_artifacts["anomaly_summary"] = st.session_state["anomaly_summary"]

            rag.build_knowledge_base(ml_artifacts=ml_artifacts)
            st.session_state["rag_engine"] = rag

    rag = st.session_state["rag_engine"]
    advisor = BusinessAdvisor(db, rag)

    # Engine Configuration Sidebar / Top Bar
    col_mode, col_api = st.columns([1.5, 2.0])
    with col_mode:
        provider = st.selectbox(
            "Intelligence Engine Provider:",
            options=["Local Offline Intelligence (Zero API Key)", "OpenAI (GPT-4o-mini)", "Google Gemini (1.5-Flash)"],
            index=0
        )
    with col_api:
        api_key = ""
        if "OpenAI" in provider:
            api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...", help="Your key is kept in memory only.")
            provider_key = "openai"
        elif "Gemini" in provider:
            api_key = st.text_input("Gemini API Key:", type="password", placeholder="AIzaSy...", help="Your key is kept in memory only.")
            provider_key = "gemini"
        else:
            provider_key = "local"
            st.markdown("<div style='padding-top: 28px; font-size: 13px; color: #059669; font-weight: 600;'>● Running in offline deterministic mode with built-in quantitative RAG</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Suggested Prompts
    st.markdown("<div style='font-size: 13px; font-weight: 600; text-transform: uppercase; color: #64748B; margin-bottom: 8px;'>Executive Inquiry Templates:</div>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    prompt_clicked = None
    with s1:
        if st.button("📉 Churn Drivers & Retention Plan", use_container_width=True):
            prompt_clicked = "What is driving our customer churn rate and how can we mitigate account attrition?"
    with s2:
        if st.button("📊 Revenue Velocity & Trajectory", use_container_width=True):
            prompt_clicked = "Analyze our revenue growth rate across regions and projected trajectory."
    with s3:
        if st.button("⚠️ Anomaly & Margin Leakage", use_container_width=True):
            prompt_clicked = "Where is transaction margin leakage occurring and how can we prevent unauthorized discounting?"
    with s4:
        if st.button("🎯 90-Day Executive Strategic Plan", use_container_width=True):
            prompt_clicked = "Synthesize an executive 90-day action plan for the CEO based on all telemetry."

    # Question Input
    default_q = prompt_clicked if prompt_clicked else "What are our primary churn drivers and how can we improve retention?"
    user_query = st.text_input("Ask a Natural Language Business Question:", value=default_q, key="nl_business_query")

    col_btn, col_empty = st.columns([1.0, 4.0])
    with col_btn:
        generate_btn = st.button("Generate Executive Briefing", type="primary", use_container_width=True)

    if generate_btn or prompt_clicked:
        with st.spinner("Retrieving RAG telemetry and synthesizing quantitative briefing..."):
            response = advisor.answer_question(
                question=user_query,
                api_key=api_key if provider_key != "local" else None,
                llm_provider=provider_key
            )

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Header with Mode Badge
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #0F172A; font-weight: 700;">Executive Decision Report</h3>
                <span class="badge-tag badge-blue">{response['mode']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Render Briefing inside clean container
            st.markdown(f"""
            <div class="content-box" style="border-left: 4px solid #1E293B;">
                {response['briefing']}
            </div>
            """, unsafe_allow_html=True)

            # Show Retrieved RAG Knowledge Snippets
            with st.expander("Inspect Grounding Telemetry (Retrieved RAG Context)", expanded=False):
                st.markdown("<div style='font-size: 13px; color: #64748B; margin-bottom: 8px;'>The following factual snippets were retrieved from the schema, database queries, and ML models:</div>", unsafe_allow_html=True)
                for snippet in response["retrieved_context"]:
                    st.markdown(f"""
                    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 12px; color: #334155;">
                            <span>{snippet['topic']}</span>
                            <span style="color: #2563EB;">Relevance: {snippet['relevance_score']}</span>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin-top: 4px;">{snippet['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
