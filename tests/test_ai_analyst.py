"""
Unit Tests for AI Business Analyst and RAG Retrieval Engine.
"""

import pytest
from database.db_manager import DatabaseManager
from data.generator import generate_customers, generate_products, generate_sales_reps, generate_transactions
from ai_analyst.rag_engine import BusinessRAGEngine
from ai_analyst.business_advisor import BusinessAdvisor


@pytest.fixture(scope="module")
def ai_test_environment():
    """Create populated in-memory database and initialized RAG engine."""
    db = DatabaseManager(db_url="sqlite:///:memory:")
    db.initialize_schema()

    customers = generate_customers(n=100)
    products = generate_products()
    sales_reps = generate_sales_reps()
    transactions = generate_transactions(customers, products, sales_reps, n_transactions=300)

    db.load_table("customers", customers)
    db.load_table("products", products)
    db.load_table("sales_reps", sales_reps)
    db.load_table("transactions", transactions)

    rag = BusinessRAGEngine(db)
    rag.build_knowledge_base()

    return {"db": db, "rag": rag}


def test_rag_retrieval(ai_test_environment):
    """Verify semantic retrieval returns relevant documents with positive similarity."""
    rag = ai_test_environment["rag"]
    snippets = rag.retrieve("What is our customer churn rate?", top_k=3)

    assert len(snippets) > 0
    assert any("churn" in s["topic"].lower() or "churn" in s["content"].lower() for s in snippets)
    assert snippets[0]["relevance_score"] >= 0.0


def test_advisor_local_briefing(ai_test_environment):
    """Verify BusinessAdvisor answers questions using local deterministic RAG engine."""
    db = ai_test_environment["db"]
    rag = ai_test_environment["rag"]
    advisor = BusinessAdvisor(db, rag)

    response = advisor.answer_question("Why are customers churning and what can we do?")

    assert "briefing" in response
    assert "retrieved_context" in response
    assert "What Happened?" in response["briefing"]
    assert "Why Did It Happen?" in response["briefing"]
    assert "Recommended Action Plan" in response["briefing"]
