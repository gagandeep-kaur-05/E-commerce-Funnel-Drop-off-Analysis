"""
generate_data.py
Generates a realistic synthetic e-commerce dataset modelled on Olist Brazil.
Prices are converted to INR (1 BRL ≈ 17 INR) for business framing.
Run once: python generate_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N = 110_000  # total orders placed

# ── Helper ────────────────────────────────────────────────────────────────────
def rand_dates(n, start="2017-01-01", end="2018-08-31"):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt   = datetime.strptime(end,   "%Y-%m-%d")
    delta    = (end_dt - start_dt).days
    return [start_dt + timedelta(days=random.randint(0, delta)) for _ in range(n)]

# ── Categories & payment methods ──────────────────────────────────────────────
categories = [
    "electronics", "fashion", "home_appliances", "beauty",
    "sports", "books", "toys", "furniture", "auto", "food"
]
cat_weights = [0.20, 0.18, 0.14, 0.12, 0.10, 0.08, 0.07, 0.05, 0.04, 0.02]

payment_methods = ["credit_card", "boleto", "voucher", "debit_card"]
pay_weights     = [0.74, 0.19, 0.05, 0.02]

states = ["SP","RJ","MG","RS","PR","SC","BA","GO","ES","PE"]
state_w = [0.42,0.13,0.11,0.08,0.07,0.06,0.04,0.03,0.03,0.03]

# ── Core order table ──────────────────────────────────────────────────────────
order_ids      = [f"ORD{str(i).zfill(7)}" for i in range(1, N+1)]
order_dates    = rand_dates(N)
categories_col = np.random.choice(categories, N, p=cat_weights)
payment_col    = np.random.choice(payment_methods, N, p=pay_weights)
states_col     = np.random.choice(states, N, p=state_w)

# Price in BRL, then convert to INR
price_brl = np.random.lognormal(mean=4.2, sigma=0.9, size=N).clip(10, 3000)
price_inr = (price_brl * 17).round(2)

# ── Funnel drop-off logic ─────────────────────────────────────────────────────
# Stage 1 → 2: payment_initiated  (98% — almost all initiate)
# Stage 2 → 3: payment_approved   (85% — boleto & voucher fail more)
# Stage 3 → 4: order_delivered    (92% — some cancellations / lost)
# Stage 4 → 5: review_submitted   (60% — optional step)

payment_initiated = np.ones(N, dtype=bool)   # 100% placed → initiated

# Approval rates vary by payment method
approval_rate = np.where(payment_col == "boleto", 0.72,
                np.where(payment_col == "voucher", 0.78,
                np.where(payment_col == "debit_card", 0.88, 0.91)))
payment_approved = payment_initiated & (np.random.rand(N) < approval_rate)

# Delivery — higher failure for remote states
delivery_rate = np.where(np.isin(states_col, ["SP","RJ","MG","RS","PR","SC"]), 0.94, 0.88)
order_delivered = payment_approved & (np.random.rand(N) < delivery_rate)

# Review — random 60%
review_submitted = order_delivered & (np.random.rand(N) < 0.60)

# ── Assemble DataFrame ────────────────────────────────────────────────────────
df = pd.DataFrame({
    "order_id":           order_ids,
    "order_date":         order_dates,
    "category":           categories_col,
    "payment_method":     payment_col,
    "customer_state":     states_col,
    "order_value_inr":    price_inr,
    "payment_initiated":  payment_initiated,
    "payment_approved":   payment_approved,
    "order_delivered":    order_delivered,
    "review_submitted":   review_submitted,
})

df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

df.to_csv("data/orders.csv", index=False)
print(f"Generated {len(df):,} orders → data/orders.csv")
print(df[["payment_initiated","payment_approved","order_delivered","review_submitted"]].sum())
