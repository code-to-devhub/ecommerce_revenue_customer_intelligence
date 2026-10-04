import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
OUT = Path("data")
OUT.mkdir(exist_ok=True)

N = 520_000
n_customers = 45_000
n_products = 300
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")

customers = pd.DataFrame({
    "customer_id": np.arange(1, n_customers + 1),
    "region": np.random.choice(["North","South","East","West","Central"], n_customers,
                               p=[.20,.22,.18,.20,.20])
})

products = pd.DataFrame({
    "product_id": np.arange(1, n_products + 1),
    "category": np.random.choice(["Electronics","Home","Fashion","Beauty","Sports"], n_products),
    "unit_price": np.round(np.random.lognormal(np.log(45), .65, n_products).clip(8, 600), 2),
})
products["cost"] = np.round(products["unit_price"] * np.random.uniform(.45,.90,n_products), 2)

tx = pd.DataFrame({
    "transaction_id": np.arange(1, N + 1),
    "customer_id": np.random.randint(1, n_customers + 1, N),
    "product_id": np.random.randint(1, n_products + 1, N),
    "order_date": np.random.choice(dates, N),
    "quantity": np.random.choice([1,2,3,4], N, p=[.62,.25,.10,.03]),
})

tx = tx.merge(products, on="product_id", how="left").merge(customers, on="customer_id", how="left")
tx["discount"] = np.round(np.random.choice([0,.05,.10,.15,.20], N, p=[.45,.20,.18,.12,.05]), 2)
tx["gross_sales"] = tx["unit_price"] * tx["quantity"]
tx["revenue"] = np.round(tx["gross_sales"] * (1 - tx["discount"]), 2)
tx["profit"] = np.round(tx["revenue"] - tx["cost"] * tx["quantity"], 2)
tx["returned"] = np.random.random(N) < .07

tx[["transaction_id","customer_id","product_id","order_date","quantity","unit_price",
    "discount","revenue","profit","returned","region","category"]].to_csv(
    OUT / "transactions.csv", index=False
)
print(f"Generated {len(tx):,} transactions.")
