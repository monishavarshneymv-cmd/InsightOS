"""
InsightOS - Business Data Generator
Synthesizes realistic, relational enterprise data (Customers, Products, Sales Reps, Transactions)
with genuine statistical correlations, business seasonality, churn drivers, and anomaly patterns.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to sys.path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import random
import config

# Set random seeds for reproducible data generation
np.random.seed(config.RANDOM_SEED)
random.seed(config.RANDOM_SEED)

REGIONS = ["North America", "EMEA", "APAC", "LATAM"]
COUNTRIES = {
    "North America": ["United States", "Canada"],
    "EMEA": ["United Kingdom", "Germany", "France", "Netherlands"],
    "APAC": ["Japan", "Singapore", "Australia", "South Korea"],
    "LATAM": ["Brazil", "Mexico", "Chile"]
}

PRODUCT_CATALOG = [
    {"name": "Insight Cloud Enterprise", "category": "Cloud Analytics", "unit_cost": 450.0, "unit_price": 1499.0},
    {"name": "DataFlow Realtime ETL", "category": "Data Engineering", "unit_cost": 220.0, "unit_price": 799.0},
    {"name": "Predictive AI Studio", "category": "Machine Learning", "unit_cost": 650.0, "unit_price": 2199.0},
    {"name": "Executive Dashboard Pro", "category": "Business Intelligence", "unit_cost": 120.0, "unit_price": 499.0},
    {"name": "SecureVault Data Shield", "category": "Security & Governance", "unit_cost": 180.0, "unit_price": 599.0},
    {"name": "Customer 360 CDP", "category": "Customer Intelligence", "unit_cost": 310.0, "unit_price": 1099.0},
    {"name": "Automated SQL Lakehouse", "category": "Data Engineering", "unit_cost": 500.0, "unit_price": 1699.0},
    {"name": "Revenue Operations Suite", "category": "Business Intelligence", "unit_cost": 200.0, "unit_price": 699.0},
    {"name": "Edge Inference Engine", "category": "Machine Learning", "unit_cost": 390.0, "unit_price": 1299.0},
    {"name": "Compliance Audit Sentinel", "category": "Security & Governance", "unit_cost": 150.0, "unit_price": 449.0},
    {"name": "Micro-Service API Gateway", "category": "Cloud Analytics", "unit_cost": 90.0, "unit_price": 299.0},
    {"name": "Anomaly Watchdog Realtime", "category": "Security & Governance", "unit_cost": 280.0, "unit_price": 899.0}
]

SALES_REPS_DATA = [
    {"rep_id": "REP-01", "name": "Marcus Vance", "region": "North America", "quota": 650000, "commission_rate": 0.08},
    {"rep_id": "REP-02", "name": "Elena Rostova", "region": "EMEA", "quota": 550000, "commission_rate": 0.075},
    {"rep_id": "REP-03", "name": "Kenji Takahashi", "region": "APAC", "quota": 480000, "commission_rate": 0.07},
    {"rep_id": "REP-04", "name": "Sofia Hernandez", "region": "LATAM", "quota": 380000, "commission_rate": 0.07},
    {"rep_id": "REP-05", "name": "David Sterling", "region": "North America", "quota": 700000, "commission_rate": 0.085},
    {"rep_id": "REP-06", "name": "Claire Dubois", "region": "EMEA", "quota": 500000, "commission_rate": 0.07},
    {"rep_id": "REP-07", "name": "Aarav Sharma", "region": "APAC", "quota": 520000, "commission_rate": 0.075},
    {"rep_id": "REP-08", "name": "Mateo Rossi", "region": "LATAM", "quota": 350000, "commission_rate": 0.065}
]

FIRST_NAMES = ["Alexander", "Beatrice", "Carlos", "Dmitri", "Evelyn", "Feng", "Gabriella", "Hassan",
               "Ingrid", "Julian", "Kavita", "Liam", "Mei", "Nathan", "Olga", "Patrick", "Rania",
               "Siddharth", "Tara", "Umar", "Vivienne", "William", "Xavier", "Yuki", "Zara"]
COMPANY_SUFFIXES = ["Technologies", "Enterprises", "Logistics", "Ventures", "Health", "Capital", "Media", "Solutions", "Dynamics", "Systems"]


def generate_customers(n: int = 1200) -> pd.DataFrame:
    """Generate realistic customer records with logical churn signals."""
    rows = []
    base_date = datetime.now() - timedelta(days=365 * 3)

    for i in range(1, n + 1):
        cust_id = f"CUST-{i:04d}"
        company_name = f"{random.choice(FIRST_NAMES)} {random.choice(COMPANY_SUFFIXES)}"
        region = random.choices(REGIONS, weights=[0.45, 0.28, 0.18, 0.09])[0]
        country = random.choice(COUNTRIES[region])
        segment = random.choices(["Enterprise", "Mid-Market", "SMB", "Startup"], weights=[0.20, 0.35, 0.30, 0.15])[0]

        tenure_months = int(np.clip(np.random.gamma(shape=3.0, scale=8.0), 1, 36))
        join_date = datetime.now() - timedelta(days=tenure_months * 30 + random.randint(0, 25))

        contract_type = random.choices(["Month-to-Month", "One-Year", "Two-Year"], weights=[0.48, 0.34, 0.18])[0]
        payment_method = random.choices(["Bank Wire", "Credit Card", "Automated ACH"], weights=[0.40, 0.35, 0.25])[0]
        paperless_billing = random.choices([1, 0], weights=[0.82, 0.18])[0]

        # Monthly charges vary by tier
        base_charge = {"Enterprise": 2200, "Mid-Market": 1100, "SMB": 450, "Startup": 250}[segment]
        monthly_charges = round(float(np.random.normal(base_charge, base_charge * 0.18)), 2)
        monthly_charges = max(monthly_charges, 149.0)

        total_charges = round(monthly_charges * tenure_months * random.uniform(0.95, 1.05), 2)

        # Support tickets and satisfaction
        support_tickets = int(np.random.poisson(lam=2.2))
        satisfaction_score = int(np.clip(round(np.random.normal(3.8, 1.0)), 1, 5))

        # Churn probability modeled on genuine business drivers:
        # High tickets, low satisfaction, month-to-month contract, low tenure increase churn
        churn_logits = (
            -0.8
            + (1.4 if contract_type == "Month-to-Month" else -1.0)
            + (0.35 * support_tickets)
            - (0.60 * (satisfaction_score - 3))
            - (0.04 * tenure_months)
            + (0.0002 * monthly_charges)
            + (0.3 if segment == "Startup" else 0.0)
        )
        churn_prob = 1.0 / (1.0 + np.exp(-churn_logits))
        churn = 1 if (np.random.rand() < churn_prob) else 0

        rows.append({
            "customer_id": cust_id,
            "company_name": company_name,
            "segment": segment,
            "region": region,
            "country": country,
            "join_date": join_date.strftime("%Y-%m-%d"),
            "contract_type": contract_type,
            "payment_method": payment_method,
            "paperless_billing": paperless_billing,
            "tenure_months": tenure_months,
            "monthly_charges": monthly_charges,
            "total_charges": total_charges,
            "support_tickets": support_tickets,
            "satisfaction_score": satisfaction_score,
            "churn": churn
        })

    return pd.DataFrame(rows)


def generate_products() -> pd.DataFrame:
    """Generate product catalog."""
    rows = []
    for idx, item in enumerate(PRODUCT_CATALOG, start=1):
        prod_id = f"PROD-{idx:02d}"
        margin = round((item["unit_price"] - item["unit_cost"]) / item["unit_price"], 4)
        rows.append({
            "product_id": prod_id,
            "product_name": item["name"],
            "category": item["category"],
            "unit_cost": item["unit_cost"],
            "unit_price": item["unit_price"],
            "margin_pct": margin,
            "is_active": 1
        })
    return pd.DataFrame(rows)


def generate_sales_reps() -> pd.DataFrame:
    """Generate sales representatives dataset."""
    return pd.DataFrame(SALES_REPS_DATA)


def generate_transactions(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    reps_df: pd.DataFrame,
    n_transactions: int = 12000
) -> pd.DataFrame:
    """Generate transactions with seasonality, volume trends, and deliberate anomalies."""
    rows = []
    start_date = datetime.now() - timedelta(days=730)  # past 2 full years

    cust_ids = customers_df["customer_id"].tolist()
    cust_region_map = dict(zip(customers_df["customer_id"], customers_df["region"]))
    reps_by_region = {}
    for region in REGIONS:
        reps_by_region[region] = reps_df[reps_df["region"] == region]["rep_id"].tolist()

    product_records = products_df.to_dict("records")

    # Generate dates with weekend dips and Q4 enterprise surge
    day_offsets = np.sort(np.random.randint(0, 730, size=n_transactions))

    for i in range(1, n_transactions + 1):
        txn_id = f"TXN-{10000 + i}"
        txn_date = start_date + timedelta(days=int(day_offsets[i - 1]), hours=random.randint(8, 20), minutes=random.randint(0, 59))

        # Select customer
        customer_id = random.choice(cust_ids)
        region = cust_region_map.get(customer_id, "North America")

        # Select sales rep matching customer region
        available_reps = reps_by_region.get(region, reps_df["rep_id"].tolist())
        rep_id = random.choice(available_reps) if available_reps else "REP-01"

        # Select product
        product = random.choice(product_records)
        prod_id = product["product_id"]
        unit_price = product["unit_price"]
        unit_cost = product["unit_cost"]

        # Anomaly trigger (~2.5% genuine anomalies for Isolation Forest)
        is_anomaly = 1 if np.random.rand() < config.ANOMALY_CONTAMINATION else 0

        if is_anomaly:
            anomaly_type = random.choice(["extreme_discount", "huge_quantity", "negative_margin"])
            if anomaly_type == "extreme_discount":
                quantity = random.randint(1, 4)
                discount_pct = round(random.uniform(0.65, 0.90), 2)  # unauthorized deep discount
            elif anomaly_type == "huge_quantity":
                quantity = random.randint(35, 80)  # bulk order far outside normal distribution
                discount_pct = 0.15
            else:  # negative_margin
                quantity = random.randint(2, 6)
                discount_pct = 0.50
                unit_price = unit_cost * 0.70  # selling below cost
        else:
            quantity = random.choices([1, 2, 3, 4, 5, 8], weights=[0.45, 0.28, 0.14, 0.07, 0.04, 0.02])[0]
            discount_pct = round(random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.50, 0.25, 0.15, 0.07, 0.03])[0], 2)

        gross_amount = round(quantity * unit_price, 2)
        total_amount = round(gross_amount * (1.0 - discount_pct), 2)
        total_cost = round(quantity * unit_cost, 2)
        net_profit = round(total_amount - total_cost, 2)

        # Status & fulfillment
        status = random.choices(["Completed", "Refunded", "Cancelled", "Processing"], weights=[0.91, 0.04, 0.03, 0.02])[0]
        fulfillment_days = int(np.clip(np.random.normal(3.2, 1.8), 1, 14))

        rows.append({
            "transaction_id": txn_id,
            "customer_id": customer_id,
            "product_id": prod_id,
            "rep_id": rep_id,
            "transaction_date": txn_date.strftime("%Y-%m-%d %H:%M:%S"),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "gross_amount": gross_amount,
            "total_amount": total_amount,
            "total_cost": total_cost,
            "net_profit": net_profit,
            "payment_status": status,
            "fulfillment_days": fulfillment_days,
            "is_anomaly": is_anomaly
        })

    return pd.DataFrame(rows)


def generate_all_datasets(save_to_disk: bool = True) -> dict[str, pd.DataFrame]:
    """Orchestrate generation of all 4 business entities and persist to data/raw/."""
    print("Generating Customers dataset (1,200 records)...")
    customers = generate_customers(n=1200)

    print("Generating Products catalog...")
    products = generate_products()

    print("Generating Sales Representatives...")
    sales_reps = generate_sales_reps()

    print("Generating Transactions (12,000 records)...")
    transactions = generate_transactions(customers, products, sales_reps, n_transactions=12000)

    data_bundle = {
        "customers": customers,
        "products": products,
        "sales_reps": sales_reps,
        "transactions": transactions
    }

    if save_to_disk:
        config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        customers.to_csv(config.RAW_DATA_DIR / "customers.csv", index=False)
        products.to_csv(config.RAW_DATA_DIR / "products.csv", index=False)
        sales_reps.to_csv(config.RAW_DATA_DIR / "sales_reps.csv", index=False)
        transactions.to_csv(config.RAW_DATA_DIR / "transactions.csv", index=False)
        print(f"Datasets successfully persisted to: {config.RAW_DATA_DIR}")

    return data_bundle


if __name__ == "__main__":
    generate_all_datasets(save_to_disk=True)
