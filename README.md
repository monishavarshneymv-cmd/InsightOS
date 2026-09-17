# InsightOS – AI-Powered Business Intelligence & Decision Platform

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![PostgreSQL Compatible](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![GenAI RAG](https://img.shields.io/badge/AI-Retrieval--Augmented%20Generation-0F172A?logo=openai&logoColor=white)](https://github.com/monishavarshneymv-cmd/InsightOS)
[![License](https://img.shields.io/badge/License-MIT-059669.svg)](LICENSE)

> **InsightOS** is an enterprise-grade Decision Intelligence and Business Analytics platform engineered to bridge the gap between static operational dashboards and actionable executive strategy. Rather than presenting raw numbers, InsightOS answers the four fundamental executive questions: **What happened? Why did it happen? What is likely to happen next? What actions should be taken?**

Designed with a calm, editorial, human-crafted executive aesthetic—avoiding generic dark neon/cyberpunk AI tropes in favor of clean financial clarity.

---

## 🏛️ System Architecture

```
                                  ┌──────────────────────────────────────────────┐
                                  │          Enterprise Data Sources             │
                                  │ Customers • Products • Sales Reps • Txns     │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                                                         ▼
                                  ┌──────────────────────────────────────────────┐
                                  │      Ingestion & Automated EDA Engine        │
                                  │  • Schema Validation  • Missing Value Audit  │
                                  │  • Outlier Detection  • Correlation Matrix   │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                                 ┌───────────────────────┴───────────────────────┐
                                 ▼                                               ▼
     ┌──────────────────────────────────────────┐    ┌──────────────────────────────────────────┐
     │      SQL Analytics Studio (PostgreSQL)   │    │          Machine Learning Suite          │
     │  • Window Functions (DENSE_RANK, LAG)    │    │  • Churn Classification & Explainability │
     │  • CTEs & Multi-Table Joins              │    │  • RFM K-Means Customer Segmentation     │
     │  • CASE Statements & Subqueries          │    │  • Autoregressive Sales Forecasting      │
     │  • Interactive Query Console             │    │  • Isolation Forest Anomaly Detection    │
     └───────────────────┬──────────────────────┘    └───────────────────┬──────────────────────┘
                         │                                               │
                         └───────────────────────┬───────────────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────────────────────┐
                                  │       AI Business Analyst Workflow           │
                                  │  • RAG Knowledge Retriever (Schema + Telemetry)│
                                  │  • Dual-Engine: Fast Local Offline + Cloud   │
                                  │  • 4-Part Structured Decision Briefings      │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                                                         ▼
                                  ┌──────────────────────────────────────────────┐
                                  │       Executive Decision Interface           │
                                  │     (Streamlit • Bespoke Editorial CSS)      │
                                  └──────────────────────────────────────────────┘
```

---

## 🌟 Key Capabilities

### 1. Automated Data Ingestion, Validation & Exploratory Data Analysis (EDA)
- **Multi-Entity Relational Data Pipeline**: Handles interconnected datasets across `customers` (1,200 accounts), `products` (catalog with cost/price margins), `sales_reps` (quota targets and regions), and `transactions` (12,000+ orders spanning 2 years).
- **Automated Validation**: Rigorous schema checks, column constraints, range verifications, and referential integrity validation between foreign keys.
- **Statistical EDA Engine**: Automated calculation of descriptive statistics, skewness, kurtosis, Interquartile Range (IQR) and Z-score ($>3\sigma$) outlier detection, Pearson correlation heatmaps, and categorical distribution breakdowns.

### 2. Advanced SQL Business Analytics Engine (PostgreSQL / ANSI SQL)
Fully compatible with PostgreSQL and SQLite 3.25+, featuring a curated query catalog solving real business challenges:
- **Window Functions**:
  - `LAG()` and `LEAD()` to compute Month-over-Month (MoM) revenue velocity and dollar delta without expensive self-joins.
  - `DENSE_RANK() OVER (PARTITION BY region ORDER BY total_spent DESC)` to rank high-value enterprise accounts strictly within geographic markets.
  - `SUM(...) OVER (PARTITION BY category ORDER BY sales_date)` for cumulative running revenue tracking.
- **Common Table Expressions (CTEs)**: Multi-stage pipeline aggregations for sales rep quota attainment and cohort retention.
- **Conditional CASE Statements**: Dynamic classification of sales performance tiers, quota accelerators, and fulfillment SLA breach risk (`CASE WHEN fulfillment_days > 5 ...`).
- **Complex Multi-Table Joins & Subqueries**: 4-table relational joins analyzing product margin contribution across customer tiers, and Pareto principle subqueries filtering accounts driving top 80% revenue.
- **Interactive SQL Console**: Live query execution workbench with execution timers, error diagnostics, and CSV export.

### 3. Machine Learning Suite (Scikit-Learn)
- **Customer Churn Prediction with Explainability**:
  - Supervised classification using Random Forest and Logistic Regression with class-weight balancing.
  - Complete evaluation suite: ROC-AUC, Accuracy, Precision, Recall, F1-Score, ROC curve, and confusion matrix.
  - **Model Explainability**: Global feature importance ranking (revealing support tickets, tenure, satisfaction, and contract type as top drivers) and customer-level probability risk scoring.
- **Customer Segmentation (RFM + K-Means)**:
  - Derives Recency, Frequency, and Monetary (RFM) metrics per customer.
  - Applies logarithmic transformations, standard scaling, and K-Means clustering with Silhouette Score evaluation.
  - Automatically maps clusters to actionable business personas: *Champions*, *At-Risk Enterprise Accounts*, *Promising Growth*, and *Hibernating Accounts*.
- **Sales Forecasting**:
  - Time-series autoregressive lag modeling (lags 1, 7, 14, 21, 28, and 7/14/30-day rolling means).
  - Projects daily revenue 30–90 days forward with **90% confidence intervals**.
  - Evaluated on holdout data with MAE, RMSE, and MAPE metrics.
- **Transaction Anomaly Detection**:
  - Unsupervised Isolation Forest detecting multi-dimensional transactional outliers across volume, pricing, discounts, and margins.
  - Classifies root causes: *Excessive Discount Overrides*, *Negative Profit Margins*, *Irregular Volume*, and *Severe SLA Delays*.

### 4. AI Business Analyst Workflow (RAG + GenAI)
- **Quantitative Knowledge Base**: Indexes relational schema definitions, real-time database KPI aggregates, SQL query documentation, and machine learning diagnostic findings.
- **Semantic RAG Retrieval**: Uses TF-IDF cosine vector matching to ground inquiries directly in quantitative data before generating recommendations.
- **Dual-Engine Architecture**:
  - **Local Deterministic Intelligence (Default)**: 100% offline, zero external API key required. Delivers immediate, grounded executive briefings.
  - **Generative Cloud LLM (Optional)**: Pluggable OpenAI (GPT-4o-mini) or Google Gemini (1.5-Flash) API key input for deep conversational reasoning.
- **Executive 4-Part Output Framework**:
  1. **What Happened?** — Descriptive summary of quantitative baseline and shifts.
  2. **Why Did It Happen?** — Diagnostic analysis connecting metrics to root drivers.
  3. **What Is Likely To Happen Next?** — Predictive outlook from ML forecasts and risk flags.
  4. **Recommended Action Plan** — Prioritized 30/60/90-day operational decisions.

### 5. Human-Crafted Executive Design System
- **Tone**: Editorial financial intelligence.
- **Color Palette**: Deep Slate (`#0F172A`, `#1E293B`), Clean Porcelain Canvas (`#F8FAFC`, `#FFFFFF`), Muted Slate Borders (`#E2E8F0`), Emerald Green (`#059669`) for positive growth, Crimson (`#BE123C`) for churn/anomalies, and Precision Cobalt (`#2563EB`) for forecasting.
- **Zero AI Clichés**: No fluorescent neon gradients or cybernetic glows. Designed for high information density, boardrooms, and executive presentations.

---

## 🗂️ Project Structure

```
InsightOS/
├── app.py                      # Main Streamlit application orchestrating views & state
├── config.py                   # Configuration, paths, database URI, and design tokens
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules for virtualenv, databases, and caches
│
├── data/                       # Data layer
│   ├── generator.py            # Synthetic enterprise relational data generator
│   └── raw/                    # Persisted raw CSV tables (Customers, Products, Reps, Txns)
│
├── ingestion/                  # Ingestion & Data Quality
│   ├── validator.py            # Schema constraints, null checks, referential integrity
│   ├── preprocessor.py         # Outlier detection (IQR & Z-score), normalization, dates
│   └── eda_engine.py           # Automated exploratory data analysis (stats, correlations)
│
├── database/                   # Database & SQL Analytics Engine
│   ├── schema.sql              # PostgreSQL / ANSI SQL DDL schema & indexes
│   ├── db_manager.py           # SQLAlchemy / SQLite / PostgreSQL connection manager
│   ├── analytics_queries.py    # Query catalog: CTEs, Window functions, Joins, CASE
│   └── seed_db.py              # Database seeding pipeline
│
├── ml/                         # Scikit-Learn Machine Learning Suite
│   ├── churn_predictor.py      # Customer churn model with feature importance
│   ├── customer_segmentation.py# RFM analysis & K-Means clustering with personas
│   ├── sales_forecaster.py     # Autoregressive time-series revenue forecaster
│   └── anomaly_detector.py     # Isolation Forest transaction anomaly detector
│
├── ai_analyst/                 # AI Business Analyst (RAG + GenAI)
│   ├── rag_engine.py           # Business telemetry semantic retrieval engine
│   ├── prompt_templates.py     # Executive C-suite briefing prompt engineering
│   └── business_advisor.py     # Dual-engine recommendation synthesizer
│
├── ui/                         # Streamlit Presentation Layer
│   ├── styles.py               # Custom editorial CSS & Plotly layout styling
│   ├── components.py           # Reusable HTML KPI cards, badges, and callouts
│   └── views/
│       ├── overview.py         # Executive KPI summary & health pulse
│       ├── eda_view.py         # Automated EDA & Data Ingestion workbench
│       ├── sql_analytics.py    # SQL Studio & Interactive Query Console
│       ├── ml_studio.py        # Machine Learning Suite (Churn, RFM, Forecast, Anomalies)
│       └── ai_advisor_view.py  # Conversational AI Business Analyst & Q&A
│
└── tests/                      # Automated Unit Test Suite (Pytest)
    ├── test_ingestion.py       # Ingestion, validation, and EDA unit tests
    ├── test_sql_engine.py      # Database connection, CTEs, and Window function tests
    ├── test_ml_models.py       # Churn, RFM, Forecasting, and Anomaly tests
    └── test_ai_analyst.py      # RAG indexing and executive advisor synthesis tests
```

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/monishavarshneymv-cmd/InsightOS.git
cd InsightOS
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
python3 database/seed_db.py
```
*This generates 1,200 customers, product catalog, sales reps, and 12,000 transactions, initializes the SQL schema, and loads the tables.*

### 4. Launch the Platform
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to access the platform.

---

## 🗄️ PostgreSQL Setup (Optional)

By default, InsightOS uses a zero-dependency local SQLite database. To run against an enterprise **PostgreSQL** instance:

1. Create your database in PostgreSQL:
   ```sql
   CREATE DATABASE insight_os;
   ```
2. Set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/insight_os"
   ```
3. Run the seeder to construct tables and load records:
   ```bash
   python3 database/seed_db.py
   ```
4. Start the application:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Automated Testing

Run the automated test suite with `pytest`:
```bash
python -m pytest tests/ -v
```

All 13 unit tests validate:
- Dataset generation and schema validation rules
- Execution of all advanced SQL queries (CTEs, Window Functions, Joins, CASE)
- Training and scoring of all 4 Machine Learning models
- RAG semantic context retrieval and executive advice synthesis

---

## 📊 SQL Analytics Showcase

Here is a preview of the Window Function used in InsightOS to calculate Month-over-Month Revenue Growth Velocity:

```sql
WITH monthly_revenue AS (
    SELECT 
        SUBSTR(transaction_date, 1, 7) AS sales_month,
        COUNT(transaction_id) AS total_orders,
        ROUND(SUM(total_amount), 2) AS gross_revenue,
        ROUND(SUM(net_profit), 2) AS net_profit
    FROM transactions
    WHERE payment_status = 'Completed'
    GROUP BY SUBSTR(transaction_date, 1, 7)
)
SELECT 
    sales_month,
    total_orders,
    gross_revenue,
    net_profit,
    LAG(gross_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue,
    ROUND(gross_revenue - LAG(gross_revenue, 1) OVER (ORDER BY sales_month), 2) AS mom_dollar_change,
    ROUND(
        ((gross_revenue - LAG(gross_revenue, 1) OVER (ORDER BY sales_month)) * 100.0) / 
        NULLIF(LAG(gross_revenue, 1) OVER (ORDER BY sales_month), 0), 
        2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY sales_month DESC;
```

---

## 👤 Author & Contribution

Developed as an advanced AI-powered Business Intelligence & Decision Platform by **[Monisha Varshney](https://github.com/monishavarshneymv-cmd)**.

Contributions, issues, and feature suggestions are welcome via pull requests!
