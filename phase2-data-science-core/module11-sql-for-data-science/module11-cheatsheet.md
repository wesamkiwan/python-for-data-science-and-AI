# 📋 Module 11 Cheat Sheet: SQL for Data Scientists

Fast reference for SQLite from Python, and how every concept maps to Pandas.

## Setup
```python
import sqlite3
conn = sqlite3.connect(":memory:")       # or "file.db" to persist to disk
cursor = conn.cursor()

cursor.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
cursor.executemany("INSERT INTO t VALUES (?, ?, ?)", rows)   # ALWAYS use ? placeholders
conn.commit()                                                    # required after INSERT/UPDATE/DELETE

cursor.execute("SELECT * FROM t")
cursor.fetchall()                # list of tuples

import pandas as pd
pd.read_sql("SELECT * FROM t", conn)     # query result -> DataFrame directly
```

## Basic Queries
```sql
SELECT col1, col2 FROM table;
SELECT * FROM table WHERE condition;
SELECT * FROM table ORDER BY col DESC;
SELECT * FROM table ORDER BY col DESC LIMIT 5;
```

## JOINs
```sql
SELECT a.col, b.col FROM a INNER JOIN b ON a.key = b.key;   -- only matching rows
SELECT a.col, b.col FROM a LEFT JOIN b ON a.key = b.key;      -- all rows from a, NULL if no match
```

## Aggregation
```sql
SELECT category, SUM(value), AVG(value), COUNT(*)
FROM table
GROUP BY category
HAVING SUM(value) > 1000     -- filters GROUPS (after aggregation)
ORDER BY SUM(value) DESC;
```
⚠️ `WHERE` filters rows before grouping; `HAVING` filters after.

## Subqueries & CTEs
```sql
-- Subquery in WHERE
SELECT name FROM t WHERE value > (SELECT AVG(value) FROM t);

-- CTE (preferred for multi-step queries -- more readable)
WITH averages AS (
    SELECT category, AVG(value) as avg_val FROM t GROUP BY category
)
SELECT * FROM averages WHERE avg_val > 100;
```

## SQL ↔ Pandas Rosetta Stone

| SQL | Pandas |
|---|---|
| `SELECT col1, col2 FROM t` | `df[["col1", "col2"]]` |
| `WHERE age > 50` | `df[df["age"] > 50]` |
| `WHERE a > 50 AND b = 'x'` | `df[(df["a"] > 50) & (df["b"] == "x")]` |
| `ORDER BY col DESC` | `df.sort_values("col", ascending=False)` |
| `LIMIT 5` | `df.head(5)` |
| `INNER JOIN ... ON` | `pd.merge(df1, df2, on="key", how="inner")` |
| `LEFT JOIN ... ON` | `pd.merge(df1, df2, on="key", how="left")` |
| `GROUP BY col` + `SUM()`/`AVG()` | `df.groupby("col").agg(...)` |
| `HAVING` | `.groupby(...).filter(lambda g: ...)` or filter the result after `.agg()` |

## Security: Parameterized Queries
```python
# ❌ NEVER
cursor.execute(f"SELECT * FROM t WHERE name = '{user_input}'")

# ✅ ALWAYS
cursor.execute("SELECT * FROM t WHERE name = ?", (user_input,))
```

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Changes don't persist / disappear | Forgot `conn.commit()` | Call it after any `INSERT`/`UPDATE`/`DELETE` |
| `HAVING`-style condition in `WHERE` fails | `WHERE` runs before aggregation, can't reference `SUM()`/`AVG()` | Move the condition to `HAVING` |
| Expected unmatched rows missing from results | Used `INNER JOIN` | Switch to `LEFT JOIN` to keep unmatched rows (as `NULL`) |
| `RIGHT JOIN` / `FULL OUTER JOIN` not supported | SQLite doesn't support them | Swap table order + `LEFT JOIN` for the right-join case |
| Query vulnerable to injection | Built with f-string/concatenation | Use `?` placeholders, always |

## The "New SQL Task" Workflow
1. Identify the table(s) and whether you need a `JOIN`.
2. Filter with `WHERE` as early/aggressively as possible — reduce data before it leaves the database.
3. `GROUP BY` + aggregate if you need a summary; `HAVING` to filter that summary.
4. For multi-step logic, reach for a CTE (`WITH`) over nested subqueries.
5. Load the result into Pandas (`pd.read_sql`) for anything beyond what SQL is built for (stats, viz, ML).
