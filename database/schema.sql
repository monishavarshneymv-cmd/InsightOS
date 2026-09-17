-- ==============================================================================
-- InsightOS Relational Schema
-- Standard ANSI SQL (Fully compatible with PostgreSQL and SQLite 3.25+)
-- ==============================================================================

-- 1. Customers Dimension
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    join_date DATE NOT NULL,
    contract_type VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    paperless_billing INTEGER DEFAULT 1,
    tenure_months INTEGER NOT NULL,
    monthly_charges NUMERIC(10, 2) NOT NULL,
    total_charges NUMERIC(12, 2) NOT NULL,
    support_tickets INTEGER DEFAULT 0,
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5),
    churn INTEGER DEFAULT 0 CHECK (churn IN (0, 1))
);

-- 2. Products Dimension
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_cost NUMERIC(10, 2) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    margin_pct NUMERIC(6, 4) NOT NULL,
    is_active INTEGER DEFAULT 1
);

-- 3. Sales Representatives Dimension
CREATE TABLE IF NOT EXISTS sales_reps (
    rep_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    quota NUMERIC(12, 2) NOT NULL,
    commission_rate NUMERIC(5, 4) NOT NULL
);

-- 4. Transactions Fact Table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    rep_id VARCHAR(20) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    discount_pct NUMERIC(5, 2) DEFAULT 0.0,
    gross_amount NUMERIC(12, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    total_cost NUMERIC(12, 2) NOT NULL,
    net_profit NUMERIC(12, 2) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    fulfillment_days INTEGER DEFAULT 3,
    is_anomaly INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);

-- Analytical Indexes
CREATE INDEX IF NOT EXISTS idx_txn_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_txn_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_txn_product ON transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_cust_region ON customers(region);
CREATE INDEX IF NOT EXISTS idx_cust_segment ON customers(segment);
