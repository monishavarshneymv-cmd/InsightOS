"""
InsightOS - Enterprise SQL Analytics Catalog
Production-grade analytical SQL queries utilizing CTEs, Window Functions (DENSE_RANK, LAG, LEAD, SUM OVER),
Complex Joins, Subqueries, and CASE statements for executive decision-making.
Compatible with both PostgreSQL and SQLite 3.25+.
"""

from typing import Dict, Any, List

QUERY_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "mom_revenue_growth_lag",
        "title": "Month-over-Month (MoM) Revenue Velocity",
        "category": "Window Functions",
        "business_question": "What is our monthly revenue trajectory, absolute dollar delta, and percentage growth rate month-over-month?",
        "sql": """
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
        """.strip(),
        "explanation": "Uses a Common Table Expression (CTE) to aggregate completed order totals by month, then applies the LAG() window function to compare current month performance with the previous month without requiring self-joins."
    },
    {
        "id": "customer_regional_rank_dense_rank",
        "title": "Top Customer Lifetime Value by Region",
        "category": "Window Functions",
        "business_question": "Who are our top-spending enterprise accounts within each global sales region?",
        "sql": """
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.company_name,
        c.region,
        c.segment,
        COUNT(t.transaction_id) AS total_orders,
        ROUND(SUM(t.total_amount), 2) AS total_spent,
        ROUND(AVG(t.total_amount), 2) AS avg_order_value
    FROM customers c
    JOIN transactions t ON c.customer_id = t.customer_id
    WHERE t.payment_status = 'Completed'
    GROUP BY c.customer_id, c.company_name, c.region, c.segment
)
SELECT 
    region,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY total_spent DESC) AS regional_rank,
    company_name,
    segment,
    total_orders,
    total_spent,
    avg_order_value
FROM customer_spending
ORDER BY region ASC, regional_rank ASC;
        """.strip(),
        "explanation": "Applies DENSE_RANK() with PARTITION BY region to rank accounts strictly within their geographical market. DENSE_RANK guarantees consecutive rankings without gaps in the case of spend ties."
    },
    {
        "id": "cumulative_category_run_rate",
        "title": "Cumulative Running Revenue by Product Category",
        "category": "Window Functions",
        "business_question": "How does revenue accumulate over time across different product lines?",
        "sql": """
WITH daily_category_sales AS (
    SELECT 
        SUBSTR(t.transaction_date, 1, 10) AS sales_date,
        p.category,
        ROUND(SUM(t.total_amount), 2) AS daily_revenue
    FROM transactions t
    JOIN products p ON t.product_id = p.product_id
    WHERE t.payment_status = 'Completed'
    GROUP BY SUBSTR(t.transaction_date, 1, 10), p.category
)
SELECT 
    sales_date,
    category,
    daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY category 
        ORDER BY sales_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_cumulative_revenue
FROM daily_category_sales
ORDER BY category, sales_date DESC;
        """.strip(),
        "explanation": "Utilizes SUM(...) OVER (PARTITION BY category ORDER BY sales_date) to compute continuous running totals for each distinct business unit across the calendar timeline."
    },
    {
        "id": "sales_rep_quota_tiers_case",
        "title": "Sales Rep Quota Attainment & Commission Tiers",
        "category": "CTEs & CASE Statements",
        "business_question": "How are sales reps performing against quota targets and what are their tiered commission payouts?",
        "sql": """
WITH rep_performance AS (
    SELECT 
        r.rep_id,
        r.name AS rep_name,
        r.region,
        r.quota,
        r.commission_rate,
        ROUND(SUM(t.total_amount), 2) AS actual_revenue,
        COUNT(t.transaction_id) AS deals_closed
    FROM sales_reps r
    LEFT JOIN transactions t ON r.rep_id = t.rep_id AND t.payment_status = 'Completed'
    GROUP BY r.rep_id, r.name, r.region, r.quota, r.commission_rate
)
SELECT 
    rep_name,
    region,
    quota,
    actual_revenue,
    ROUND((actual_revenue / NULLIF(quota, 0)) * 100.0, 2) AS quota_attainment_pct,
    CASE 
        WHEN (actual_revenue / NULLIF(quota, 0)) >= 1.20 THEN 'President Club (120%+)'
        WHEN (actual_revenue / NULLIF(quota, 0)) >= 1.00 THEN 'Target Achieved (100-119%)'
        WHEN (actual_revenue / NULLIF(quota, 0)) >= 0.75 THEN 'On Pace (75-99%)'
        ELSE 'Underperforming (<75%)'
    END AS performance_band,
    ROUND(
        actual_revenue * commission_rate * 
        CASE 
            WHEN (actual_revenue / NULLIF(quota, 0)) >= 1.20 THEN 1.25 -- 25% accelerator bonus
            WHEN (actual_revenue / NULLIF(quota, 0)) >= 1.00 THEN 1.00
            ELSE 0.80 -- penalty on missing quota
        END, 
        2
    ) AS estimated_payout
FROM rep_performance
ORDER BY quota_attainment_pct DESC;
        """.strip(),
        "explanation": "Employs Common Table Expression (CTE) aggregation combined with conditional CASE logic to categorize performance bands and apply executive accelerator multipliers on commissions."
    },
    {
        "id": "segment_margin_health_join",
        "title": "Gross Margin Health by Customer Segment & Product Category",
        "category": "Multi-Table Joins",
        "business_question": "Which product category and customer tier combinations generate the healthiest profit margins vs. high discount erosion?",
        "sql": """
SELECT 
    c.segment AS customer_segment,
    p.category AS product_category,
    COUNT(t.transaction_id) AS transaction_count,
    ROUND(SUM(t.total_amount), 2) AS net_revenue,
    ROUND(SUM(t.total_cost), 2) AS total_cost,
    ROUND(SUM(t.net_profit), 2) AS net_profit,
    ROUND((SUM(t.net_profit) * 100.0) / NULLIF(SUM(t.total_amount), 0), 2) AS realized_profit_margin_pct,
    ROUND(AVG(t.discount_pct) * 100.0, 2) AS avg_discount_pct
FROM transactions t
INNER JOIN customers c ON t.customer_id = c.customer_id
INNER JOIN products p ON t.product_id = p.product_id
WHERE t.payment_status = 'Completed'
GROUP BY c.segment, p.category
HAVING COUNT(t.transaction_id) > 10
ORDER BY net_profit DESC;
        """.strip(),
        "explanation": "Executes multi-table inner joins across fact and dimension tables, computing realized gross margin percentage and average discounting rate to expose margin compression."
    },
    {
        "id": "sla_breach_case_analysis",
        "title": "Fulfillment SLA Compliance & Delivery Risk",
        "category": "CASE Statements",
        "business_question": "What percentage of transactions breach our 5-day delivery SLA, and how does this correlate with refund requests?",
        "sql": """
SELECT 
    c.region,
    COUNT(t.transaction_id) AS total_orders,
    SUM(CASE WHEN t.fulfillment_days <= 3 THEN 1 ELSE 0 END) AS fast_delivery_count,
    SUM(CASE WHEN t.fulfillment_days BETWEEN 4 AND 5 THEN 1 ELSE 0 END) AS standard_delivery_count,
    SUM(CASE WHEN t.fulfillment_days > 5 THEN 1 ELSE 0 END) AS sla_breached_count,
    ROUND(
        (SUM(CASE WHEN t.fulfillment_days > 5 THEN 1 ELSE 0 END) * 100.0) / COUNT(t.transaction_id), 
        2
    ) AS sla_breach_rate_pct,
    ROUND(
        (SUM(CASE WHEN t.payment_status = 'Refunded' THEN 1 ELSE 0 END) * 100.0) / COUNT(t.transaction_id),
        2
    ) AS refund_rate_pct
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
GROUP BY c.region
ORDER BY sla_breach_rate_pct DESC;
        """.strip(),
        "explanation": "Demonstrates conditional counting using CASE inside SUM() to calculate discrete operational KPI buckets (Fast, Standard, SLA Breach) and their relationship to refund churn."
    },
    {
        "id": "pareto_high_value_customers_subquery",
        "title": "Pareto Top 10% Revenue Contributors",
        "category": "Subqueries",
        "business_question": "Which customers generate the highest share of company revenue, exceeding average account spend by 3x?",
        "sql": """
SELECT 
    c.customer_id,
    c.company_name,
    c.segment,
    c.region,
    ROUND(SUM(t.total_amount), 2) AS customer_total_spend,
    ROUND(AVG(t.total_amount), 2) AS avg_deal_size,
    COUNT(t.transaction_id) AS lifetime_orders
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
WHERE t.payment_status = 'Completed'
GROUP BY c.customer_id, c.company_name, c.segment, c.region
HAVING SUM(t.total_amount) > (
    SELECT AVG(total_spend) * 2.5
    FROM (
        SELECT SUM(total_amount) AS total_spend
        FROM transactions
        WHERE payment_status = 'Completed'
        GROUP BY customer_id
    ) AS account_spend_subquery
)
ORDER BY customer_total_spend DESC;
        """.strip(),
        "explanation": "Features an uncorrelated scalar subquery within the HAVING clause that dynamically determines the population spend average and filters accounts outperforming the baseline by 2.5x."
    }
]
