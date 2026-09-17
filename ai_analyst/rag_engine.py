"""
InsightOS - Business RAG (Retrieval-Augmented Generation) Engine
Indexes relational schema definitions, prebuilt SQL insights, ML model outputs, and real-time business metrics.
Performs semantic context retrieval using TF-IDF cosine vector matching to augment executive queries.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.db_manager import DatabaseManager
from database.analytics_queries import QUERY_CATALOG


class BusinessRAGEngine:
    """Knowledge indexing and retrieval engine for business intelligence."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.documents: List[Dict[str, str]] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.doc_vectors = None
        self.is_indexed: bool = False

    def build_knowledge_base(self, ml_artifacts: Dict[str, Any] | None = None) -> None:
        """Construct knowledge documents from database, SQL queries, and ML models."""
        docs = []

        # 1. Schema & Table Definitions
        docs.append({
            "topic": "Schema: Customers Table",
            "content": "The 'customers' table contains 1,200 accounts with customer_id, company_name, segment (Enterprise, Mid-Market, SMB, Startup), region (North America, EMEA, APAC, LATAM), tenure_months, monthly_charges, total_charges, support_tickets, satisfaction_score (1-5), and churn flag (0 or 1)."
        })
        docs.append({
            "topic": "Schema: Products Table",
            "content": "The 'products' table lists software and cloud products with product_id, product_name, category (Cloud Analytics, Data Engineering, Machine Learning, Security & Governance, Business Intelligence), unit_cost, unit_price, and margin_pct."
        })
        docs.append({
            "topic": "Schema: Transactions Table",
            "content": "The 'transactions' table logs completed and refunded orders with transaction_id, customer_id, product_id, rep_id, transaction_date, quantity, unit_price, discount_pct, total_amount, net_profit, payment_status, and fulfillment_days."
        })
        docs.append({
            "topic": "Schema: Sales Reps Table",
            "content": "The 'sales_reps' table contains sales personnel with rep_id, name, region, annual quota, and base commission_rate."
        })

        # 2. Database Live Metrics
        try:
            rev_query = "SELECT ROUND(SUM(total_amount), 2) AS total_rev, COUNT(*) AS total_txns, ROUND(AVG(total_amount), 2) AS aov FROM transactions WHERE payment_status = 'Completed';"
            rev_df = self.db.execute_query(rev_query)
            if not rev_df.empty:
                tot_rev = rev_df.iloc[0]["total_rev"]
                tot_txns = rev_df.iloc[0]["total_txns"]
                aov = rev_df.iloc[0]["aov"]
                docs.append({
                    "topic": "Live Metric: Gross Revenue and Orders",
                    "content": f"Total completed revenue to date is ${tot_rev:,.2f} across {tot_txns:,} completed transactions with an average order value (AOV) of ${aov:,.2f}."
                })

            churn_query = "SELECT ROUND(AVG(churn) * 100.0, 2) AS churn_rate, COUNT(*) AS cust_count FROM customers;"
            churn_df = self.db.execute_query(churn_query)
            if not churn_df.empty:
                c_rate = churn_df.iloc[0]["churn_rate"]
                c_count = churn_df.iloc[0]["cust_count"]
                docs.append({
                    "topic": "Live Metric: Customer Population and Churn Rate",
                    "content": f"The total customer base is {c_count:,} accounts with an overall customer churn rate of {c_rate}%."
                })

            region_query = "SELECT region, ROUND(SUM(total_amount), 2) AS rev FROM transactions t JOIN customers c ON t.customer_id = c.customer_id WHERE t.payment_status = 'Completed' GROUP BY region ORDER BY rev DESC;"
            region_df = self.db.execute_query(region_query)
            if not region_df.empty:
                top_region = region_df.iloc[0]["region"]
                top_rev = region_df.iloc[0]["rev"]
                docs.append({
                    "topic": "Live Metric: Top Performing Region",
                    "content": f"The top performing sales region is {top_region} generating ${top_rev:,.2f} in completed revenue."
                })
        except Exception as e:
            docs.append({
                "topic": "Live Metrics Status",
                "content": f"Live database metric calculation encountered: {str(e)}"
            })

        # 3. SQL Query Catalog Documentation
        for item in QUERY_CATALOG:
            docs.append({
                "topic": f"Analytical Query: {item['title']}",
                "content": f"Query '{item['title']}' ({item['category']}). Business Question: {item['business_question']}. SQL Logic explanation: {item['explanation']}."
            })

        # 4. Machine Learning Insights if available
        if ml_artifacts:
            if "churn_features" in ml_artifacts:
                top_f = ml_artifacts["churn_features"].head(3)["Feature"].tolist()
                docs.append({
                    "topic": "ML Insight: Churn Predictor Drivers",
                    "content": f"Machine learning churn analysis identifies {', '.join(top_f)} as the primary quantitative drivers predicting customer churn."
                })
            if "rfm_summary" in ml_artifacts:
                docs.append({
                    "topic": "ML Insight: Customer RFM Segmentation",
                    "content": "K-Means customer segmentation clusters accounts into 4 operational tiers: Champions, At-Risk Enterprise, Promising Growth, and Hibernating accounts."
                })
            if "anomaly_summary" in ml_artifacts:
                anom = ml_artifacts["anomaly_summary"]
                docs.append({
                    "topic": "ML Insight: Transaction Anomalies",
                    "content": f"Isolation Forest identified {anom.get('anomalies_detected', 0)} irregular transactions (~{anom.get('anomaly_rate_pct', 0)}% contamination rate), primarily driven by excessive discounts and negative margins."
                })

        self.documents = docs

        # Fit TF-IDF Vectorizer
        corpus = [f"{d['topic']} {d['content']}" for d in docs]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.doc_vectors = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Retrieve most relevant knowledge snippets for a natural language inquiry."""
        if not self.is_indexed or self.vectorizer is None or self.doc_vectors is None:
            self.build_knowledge_base()

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            results.append({
                "topic": self.documents[idx]["topic"],
                "content": self.documents[idx]["content"],
                "relevance_score": round(float(similarities[idx]), 3)
            })
        return results
