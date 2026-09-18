"""
InsightOS - Ask InsightOS (AI Business Advisor)
Conversational business intelligence providing plain-English executive briefings and recommendations.
"""

from typing import Dict, Any, List
import streamlit as st
from database.db_manager import DatabaseManager
from ai_analyst.rag_engine import BusinessRAGEngine
from ai_analyst.business_advisor import BusinessAdvisor
from ui.components import render_welcome_banner


def render_ai_advisor_view(db: DatabaseManager):
    """Render friendly conversational AI business advisor view."""
    render_welcome_banner(
        title="AI Executive Advisor 💬",
        subtitle="Ask strategic business questions in plain English to receive data-backed executive briefings and action plans.",
        badge_text="● Decision Intelligence RAG"
    )

    # Initialize RAG in session state
    if "rag_engine" not in st.session_state:
        with st.spinner("Preparing business knowledge base..."):
            rag = BusinessRAGEngine(db)
            rag.build_knowledge_base()
            st.session_state["rag_engine"] = rag

    rag = st.session_state["rag_engine"]
    advisor = BusinessAdvisor(db, rag)

    # 1. Choose Engine
    col_opt, col_key = st.columns([1.5, 2.0])
    with col_opt:
        provider = st.selectbox(
            "Intelligence Engine:",
            options=["Instant Local Offline (Free • 0 API Key Needed)", "OpenAI (GPT-4o)", "Google Gemini (1.5-Flash)"],
            index=0
        )
    with col_key:
        api_key = ""
        if "OpenAI" in provider:
            api_key = st.text_input("Enter OpenAI Key:", type="password", placeholder="sk-...")
            provider_key = "openai"
        elif "Gemini" in provider:
            api_key = st.text_input("Enter Gemini Key:", type="password", placeholder="AIzaSy...")
            provider_key = "gemini"
        else:
            provider_key = "local"
            st.markdown("<div style='padding-top: 28px; font-size: 13px; color: #059669; font-weight: 600;'>🟢 Running 100% offline using your local database metrics</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 2. Suggested Human Questions
    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #64748B; margin-bottom: 8px;'>💡 QUICK QUESTIONS (CLICK ANY TO ASK):</div>", unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)
    clicked_prompt = None
    with q1:
        if st.button("📉 Why are customers canceling?", use_container_width=True):
            clicked_prompt = "Why are customers canceling and how do we stop them?"
    with q2:
        if st.button("💰 How do we grow revenue?", use_container_width=True):
            clicked_prompt = "How can we increase our monthly revenue and profit margin?"
    with q3:
        if st.button("⚠️ Where is money leaking?", use_container_width=True):
            clicked_prompt = "Where is money leaking from discounts and fulfillment issues?"
    with q4:
        if st.button("🎯 Give me a 30-day plan", use_container_width=True):
            clicked_prompt = "Give me a simple 30-day action plan for my leadership team."

    # 3. Text Input
    default_text = clicked_prompt if clicked_prompt else "Why are customers canceling and how do we stop them?"
    user_q = st.text_input("Ask a question about your business:", value=default_text)

    if st.button("Get Plain-English Answer", type="primary") or clicked_prompt:
        with st.spinner("Analyzing numbers and formulating advice..."):
            ans = advisor.answer_question(
                question=user_q,
                api_key=api_key if provider_key != "local" else None,
                llm_provider=provider_key
            )

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="human-card" style="border-left: 5px solid #2563EB;">
                <div class="human-card-header">
                    <div class="human-card-title">📋 Executive Decision Report</div>
                    <span style="font-size: 11px; font-weight: 700; color: #2563EB; background: #EFF6FF; padding: 2px 8px; border-radius: 9999px;">
                        {ans['mode']}
                    </span>
                </div>
                <div style="font-size: 14px; line-height: 1.6; color: #1E293B;">
                    {ans['briefing']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔍 See the exact database facts used to build this answer"):
                for s in ans["retrieved_context"]:
                    st.markdown(f"• **{s['topic']}**: {s['content']}")
