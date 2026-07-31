# Starter Guide: Customer Churn Capstone

Use this as a scaffold — it tells you *what* to figure out at each stage, not *how*. Try each step yourself before peeking at `solution.md`.

## Step 1: First Look

- Load `customer_churn.csv`. What's the shape? What are the column dtypes?
- Run `.isna().sum()`. Which columns have missing data, and how much?
- Check `.duplicated().sum()`. Are there exact duplicate rows?
- Look at the unique values in each categorical column (`contract_type`, `internet_service`, `tech_support`, `payment_method`). Do you see anything inconsistent (casing, whitespace)?
- What's the churn rate (`df["churn"].mean()`)? Is this a balanced or imbalanced classification problem? Why does that matter for later steps?

## Step 2: Clean the Data

- Decide how to handle each missing column. Is a simple median/mode fill appropriate, or is there a smarter way to fill `total_charges` using other columns you already have?
- Standardize the inconsistent categorical values you found in Step 1.
- Remove duplicate rows.
- Check `monthly_charges` for outliers (recall the IQR method). Are there rows that look like data-entry errors? Decide: drop, cap, or investigate further?
- After cleaning, re-run `.isna().sum()` and `.duplicated().sum()` to confirm you're done.

## Step 3: Explore the Data

- For each numeric feature, compare its distribution for churned vs. non-churned customers (box plots are a great tool here).
- For each categorical feature, compute the churn rate *within* each category (a groupby). Which categories look highest-risk?
- Build a correlation heatmap for the numeric features. Any strong relationships?
- Write 2-3 sentences summarizing what you see *before* building any model — what's your hypothesis about what drives churn?

## Step 4: Prepare Features & Split

- Separate features (`X`) from the target (`y`). Which column(s) should definitely NOT be a feature (hint: think about what a `customer_id` actually represents)?
- Split into train/test BEFORE any scaling or encoding.
- Identify which columns are numeric (need scaling) vs. categorical (need encoding). Build a `ColumnTransformer` + `Pipeline` that handles both correctly and avoids data leakage.

## Step 5: Train and Compare Models

- Train at least 3 models: a linear model (e.g., `LogisticRegression`), and at least one ensemble method (e.g., `RandomForestClassifier` and/or `XGBClassifier`).
- Use cross-validation (not a single split) to compare them fairly. What metric are you optimizing for, and why (hint: think about the class imbalance from Step 1)?
- Which model performs best on cross-validation? Does that match its performance on the held-out test set?

## Step 6: Tune the Winner

- Pick the best-performing model from Step 5 and tune at least one meaningful hyperparameter with `RandomizedSearchCV` or `GridSearchCV`.
- Does tuning meaningfully improve performance over the default settings?

## Step 7: Evaluate Honestly

- Report accuracy, precision, recall, F1, and AUC on the test set.
- Look at the confusion matrix. Given the business goal ("flag at-risk customers so retention can reach out"), is precision or recall more important here? What happens if you try `class_weight="balanced"`?

## Step 8: Interpret and Recommend

- If you used a linear model, look at its coefficients. If you used a tree-based model, look at `.feature_importances_`. What are the top 3-5 factors driving churn?
- Write a short, non-technical paragraph (no code, no jargon) explaining your findings and one concrete, actionable recommendation for the Customer Success team — being careful to separate what the data clearly shows from what would need further investigation to confirm.

---

Once you've worked through this yourself, compare with [`solution.md`](solution.md).
