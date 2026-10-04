import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(".")
DB = ROOT / "data" / "ecommerce.db"
CSV = ROOT / "data" / "transactions.csv"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(CSV, parse_dates=["order_date"])
con = sqlite3.connect(DB)
df.to_sql("transactions", con, if_exists="replace", index=False)

# Run SQL outputs
queries = {
"kpi_summary": '''
SELECT ROUND(SUM(revenue),2) revenue,
       ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)*100.0/NULLIF(SUM(revenue),0),2) profit_margin,
       ROUND(SUM(revenue)*1.0/COUNT(DISTINCT transaction_id),2) aov,
       ROUND(COUNT(DISTINCT CASE WHEN customer_orders > 1 THEN customer_id END)*100.0/
             NULLIF(COUNT(DISTINCT customer_id),0),2) repeat_purchase_rate,
       ROUND(SUM(CASE WHEN returned=1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2) return_rate
FROM (
    SELECT t.*, COUNT(*) OVER(PARTITION BY customer_id) customer_orders
    FROM transactions t
);
''',
"monthly_sales": '''
SELECT strftime('%Y-%m', order_date) month,
       ROUND(SUM(revenue),2) revenue,
       ROUND(SUM(profit),2) profit,
       COUNT(*) orders,
       COUNT(DISTINCT customer_id) customers
FROM transactions
GROUP BY 1 ORDER BY 1;
''',
"regional_performance": '''
SELECT region, ROUND(SUM(revenue),2) revenue, ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)*100.0/NULLIF(SUM(revenue),0),2) profit_margin,
       COUNT(DISTINCT customer_id) customers
FROM transactions GROUP BY region ORDER BY revenue DESC;
''',
"product_performance": '''
SELECT product_id, category,
       ROUND(SUM(revenue),2) revenue, ROUND(SUM(profit),2) profit,
       ROUND(SUM(profit)*100.0/NULLIF(SUM(revenue),0),2) profit_margin,
       SUM(quantity) units
FROM transactions
GROUP BY product_id, category
ORDER BY revenue DESC;
'''
}

for name, q in queries.items():
    pd.read_sql_query(q, con).to_csv(OUT / f"{name}.csv", index=False)

# RFM segmentation
max_date = df["order_date"].max()
rfm = df.groupby("customer_id").agg(
    recency=("order_date", lambda x: (max_date - x.max()).days),
    frequency=("transaction_id","nunique"),
    monetary=("revenue","sum")
).reset_index()

rfm["R"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1], duplicates="drop").astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)

def segment(r):
    if r.R >= 4 and r.F >= 4 and r.M >= 4: return "Champions"
    if r.R >= 3 and r.F >= 3: return "Loyal"
    if r.R >= 4 and r.F <= 2: return "New / Promising"
    if r.R <= 2 and r.F >= 3: return "At Risk"
    return "Needs Attention"

rfm["segment"] = rfm.apply(segment, axis=1)
rfm.to_csv(OUT / "rfm_segments.csv", index=False)

# Cohort retention
d = df[["customer_id","order_date"]].copy()
d["order_month"] = d["order_date"].dt.to_period("M").dt.to_timestamp()
first = d.groupby("customer_id")["order_month"].min().rename("cohort_month")
d = d.join(first, on="customer_id")
d["cohort_index"] = ((d["order_month"].dt.year-d["cohort_month"].dt.year)*12 +
                     d["order_month"].dt.month-d["cohort_month"].dt.month)
cohort = d.groupby(["cohort_month","cohort_index"])["customer_id"].nunique().reset_index()
base = cohort[cohort["cohort_index"]==0][["cohort_month","customer_id"]].rename(columns={"customer_id":"cohort_size"})
cohort = cohort.merge(base,on="cohort_month")
cohort["retention_pct"] = (cohort["customer_id"]*100.0/cohort["cohort_size"]).round(2)
cohort.to_csv(OUT / "cohort_retention.csv", index=False)

con.close()
print("Analysis complete. Power BI files are in output/.")
