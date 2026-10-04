-- Advanced SQL examples

-- 1. Customer lifetime revenue + rank
WITH customer_sales AS (
    SELECT customer_id, SUM(revenue) revenue
    FROM transactions
    GROUP BY customer_id
)
SELECT customer_id, revenue,
       RANK() OVER (ORDER BY revenue DESC) revenue_rank
FROM customer_sales;

-- 2. Repeat customers
SELECT customer_id, COUNT(DISTINCT transaction_id) orders
FROM transactions
GROUP BY customer_id
HAVING orders > 1;

-- 3. High-revenue / low-margin products
SELECT product_id, category,
       SUM(revenue) revenue,
       SUM(profit) profit,
       SUM(profit)*100.0/NULLIF(SUM(revenue),0) margin_pct
FROM transactions
GROUP BY product_id, category
HAVING revenue > (SELECT AVG(revenue) FROM (
    SELECT product_id, SUM(revenue) revenue
    FROM transactions GROUP BY product_id
))
AND margin_pct < 15
ORDER BY revenue DESC;

-- 4. Monthly revenue with previous month
WITH m AS (
    SELECT strftime('%Y-%m',order_date) month, SUM(revenue) revenue
    FROM transactions GROUP BY 1
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) previous_month,
       ROUND((revenue-LAG(revenue) OVER (ORDER BY month))*100.0/
             NULLIF(LAG(revenue) OVER (ORDER BY month),0),2) mom_growth_pct
FROM m;
