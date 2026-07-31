"""
Generates the synthetic customer churn dataset used in this capstone.

Run this once to produce customer_churn.csv. The data is synthetic (no real
customers), but deliberately modeled on realistic telecom/subscription churn
patterns and includes intentional messiness (missing values, outliers,
inconsistent text casing, duplicate rows) so the capstone gives you authentic
data-cleaning practice, not just a pre-cleaned toy dataset.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
n = 2000

customer_id = np.arange(1000, 1000 + n)
age = np.random.normal(45, 15, n).clip(18, 85).round(0)
tenure_months = np.random.exponential(scale=20, size=n).clip(0, 72).round(0)
monthly_charges = np.random.normal(65, 25, n).clip(15, 150).round(2)
contract_type = np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.25, 0.20])
internet_service = np.random.choice(["DSL", "Fiber optic", "No"], n, p=[0.35, 0.45, 0.20])
tech_support = np.random.choice(["Yes", "No"], n, p=[0.35, 0.65])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n
)
num_support_calls = np.random.poisson(1.5, n)
total_charges = (tenure_months * monthly_charges * np.random.uniform(0.85, 1.15, n)).round(2)

# Churn probability driven by realistic factors: shorter tenure, higher charges,
# month-to-month contracts, fiber internet, no tech support, and more support
# calls all increase churn risk -- exactly the kind of relationships a real
# analysis should be able to (re)discover.
churn_score = (
    -0.05 * tenure_months
    + 0.02 * monthly_charges
    + (contract_type == "Month-to-month") * 2.0
    + (internet_service == "Fiber optic") * 0.8
    + (tech_support == "No") * 1.0
    + num_support_calls * 0.3
    + np.random.normal(0, 1.5, n)
)
churn_prob = 1 / (1 + np.exp(-(churn_score - 5.2)))
churn = (np.random.uniform(0, 1, n) < churn_prob).astype(int)

df = pd.DataFrame({
    "customer_id": customer_id,
    "age": age,
    "tenure_months": tenure_months,
    "contract_type": contract_type,
    "internet_service": internet_service,
    "tech_support": tech_support,
    "payment_method": payment_method,
    "monthly_charges": monthly_charges,
    "total_charges": total_charges,
    "num_support_calls": num_support_calls,
    "churn": churn,
})

# --- Inject realistic messiness ---

# 1. Missing values scattered across a few columns (common in real exports)
missing_idx = np.random.choice(df.index, size=60, replace=False)
df.loc[missing_idx[:30], "total_charges"] = np.nan
df.loc[missing_idx[30:45], "tech_support"] = np.nan
df.loc[missing_idx[45:], "age"] = np.nan

# 2. A handful of outlier/data-entry-error rows in monthly_charges
outlier_idx = np.random.choice(df.index, size=5, replace=False)
df.loc[outlier_idx, "monthly_charges"] = df.loc[outlier_idx, "monthly_charges"] * 10

# 3. Inconsistent text casing/whitespace in a categorical column (common when
# data comes from multiple source systems)
inconsistent_idx = np.random.choice(df.index, size=100, replace=False)
df.loc[inconsistent_idx, "internet_service"] = df.loc[inconsistent_idx, "internet_service"].str.upper()
whitespace_idx = np.random.choice(df.index, size=50, replace=False)
df.loc[whitespace_idx, "contract_type"] = " " + df.loc[whitespace_idx, "contract_type"] + " "

# 4. A few exact duplicate rows (simulating an accidental double-import)
duplicate_rows = df.sample(n=8, random_state=1)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Shuffle so duplicates/messy rows aren't conspicuously grouped together
df = df.sample(frac=1, random_state=2).reset_index(drop=True)

df.to_csv("customer_churn.csv", index=False)
print(f"Generated customer_churn.csv with {len(df)} rows.")
print(f"Churn rate: {df['churn'].mean():.2%}")
