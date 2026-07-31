# Module 11a: SQL Basics — SELECT, WHERE & ORDER BY

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [Module 10 — EDA & Statistics](../module10-eda-statistics/03-full-eda-workflow.md)

## 🎯 Learning Objectives
- [ ] Explain what SQL is and why data scientists need it
- [ ] Set up a working SQLite database directly from Python
- [ ] Write `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT` queries
- [ ] Load SQL query results directly into a Pandas DataFrame

---

## Module Goal

Learn **SQL (Structured Query Language)**, the standard language for retrieving data from databases — closing out Phase 2 by teaching you how to get data *out* of the systems where most real-world data actually lives, rather than always starting from a pre-made CSV.

## Why This Matters on the Job

Most company data lives in a database, not a CSV file sitting on someone's laptop. Every data scientist is expected to write SQL fluently — to pull exactly the data they need, filtered and aggregated at the source, rather than hauling an entire table into Python just to filter it there. SQL interview questions are also close to universal in data science hiring, precisely because this skill is assumed baseline.

---

## What Is SQL, and Why Learn It Alongside Pandas?

SQL is a declarative language for querying **relational databases** — data organized into tables with rows and columns, much like the DataFrames you already know well. In fact, you'll notice throughout this module that most SQL concepts have a near-exact Pandas equivalent, because both are built around the same relational-data ideas — `WHERE` mirrors boolean filtering, `GROUP BY` mirrors `.groupby()`, and SQL's `JOIN` mirrors `pd.merge()`.

💡 **Why this course uses SQLite:** SQLite is a lightweight, file-based (or fully in-memory) database engine built into Python's standard library — no server, installation, or account needed. It's not what powers large production systems (those typically use PostgreSQL, MySQL, or cloud data warehouses), but the SQL syntax you learn here transfers almost entirely to those systems, and SQLite lets you practice immediately with zero setup.

## Setting Up a Database

```python
import sqlite3

conn = sqlite3.connect(":memory:")   # an in-memory, temporary database (or pass a filename to persist it)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    age INTEGER
)
""")

employees_data = [
    (1, "Ada", "Engineering", 95000, 36),
    (2, "Grace", "Engineering", 120000, 85),
    (3, "Alan", "Research", 88000, 41),
    (4, "Katherine", "Research", 130000, 101),
    (5, "Linus", "Engineering", 91000, 33),
]
cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees_data)
conn.commit()
```

**How it works:** `sqlite3.connect(":memory:")` creates a temporary database that exists only in RAM for this Python session — perfect for learning and testing (pass a filename like `"mydata.db"` instead to persist it to disk). `CREATE TABLE` defines the table's structure (columns and their types: `INTEGER`, `TEXT`, `REAL`). `executemany()` inserts multiple rows at once, using `?` placeholders — never build SQL strings with Python f-strings/concatenation directly (more on why in the next lesson's warning about SQL injection).

⚠️ **Warning:** `conn.commit()` is required after any change (`INSERT`, `UPDATE`, `DELETE`) — without it, your changes exist only in the current transaction and may be lost. Read-only queries (`SELECT`) don't need it.

## `SELECT`: Retrieving Data

```python
cursor.execute("SELECT * FROM employees")
print(cursor.fetchall())
```
```
[(1, 'Ada', 'Engineering', 95000.0, 36), (2, 'Grace', 'Engineering', 120000.0, 85), (3, 'Alan', 'Research', 88000.0, 41), (4, 'Katherine', 'Research', 130000.0, 101), (5, 'Linus', 'Engineering', 91000.0, 33)]
```

**How it works:** `SELECT * FROM employees` retrieves every column (`*`) from every row of the `employees` table. `cursor.execute()` runs the query; `cursor.fetchall()` retrieves the results as a list of tuples — one tuple per row.

Selecting specific columns:

```python
cursor.execute("SELECT name, salary FROM employees")
print(cursor.fetchall())
```
```
[('Ada', 95000.0), ('Grace', 120000.0), ('Alan', 88000.0), ('Katherine', 130000.0), ('Linus', 91000.0)]
```

## `WHERE`: Filtering Rows

```python
cursor.execute("SELECT name, salary FROM employees WHERE age > 50")
print(cursor.fetchall())
```
```
[('Grace', 120000.0), ('Katherine', 130000.0)]
```

**How it works:** `WHERE age > 50` filters to only rows matching the condition — the exact same concept as Pandas' `df[df["age"] > 50]` boolean filtering from Module 07.

| SQL | Pandas equivalent |
|---|---|
| `WHERE age > 50` | `df[df["age"] > 50]` |
| `WHERE department = 'Engineering'` | `df[df["department"] == "Engineering"]` |
| `WHERE age > 50 AND department = 'Engineering'` | `df[(df["age"] > 50) & (df["department"] == "Engineering")]` |
| `WHERE department IN ('Research', 'Sales')` | `df[df["department"].isin(["Research", "Sales"])]` |

## `ORDER BY`: Sorting Results

```python
cursor.execute("SELECT name, salary FROM employees ORDER BY salary DESC")
print(cursor.fetchall())
```
```
[('Katherine', 130000.0), ('Grace', 120000.0), ('Ada', 95000.0), ('Linus', 91000.0), ('Alan', 88000.0)]
```

**How it works:** `ORDER BY salary DESC` sorts descending (`ASC` for ascending, the default if omitted) — directly equivalent to Module 07's `df.sort_values("salary", ascending=False)`.

## `LIMIT`: Restricting Row Count

```python
cursor.execute("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 2")
print(cursor.fetchall())
```
```
[('Katherine', 130000.0), ('Grace', 120000.0)]
```

**How it works:** `LIMIT 2` returns only the first 2 rows of the result — combined with `ORDER BY`, this is the standard SQL way to answer "top N" questions (here, the top 2 highest-paid employees).

## Loading Query Results Directly into Pandas

You'll rarely work with raw `cursor.fetchall()` tuples for real analysis — Pandas can run a query and return a DataFrame directly:

```python
import pandas as pd

df = pd.read_sql("SELECT * FROM employees WHERE department = 'Engineering'", conn)
print(df)
```
```
   id   name   department    salary  age
0   1    Ada  Engineering   95000.0   36
1   2  Grace  Engineering  120000.0   85
2   5  Linus  Engineering   91000.0   33
```

✅ **Best Practice:** `pd.read_sql(query, conn)` is what you'll actually use in real analysis work — write your `WHERE`/`ORDER BY`/aggregation logic in SQL to filter/reduce data *at the database*, rather than pulling an entire huge table into Python and filtering with Pandas afterward. For genuinely large tables, this is far more efficient — the database does the heavy filtering work before any data even reaches Python.

---

## Hands-On Exercise

**Task:** Write `sql_basics_practice.py` that:
1. Creates an in-memory SQLite database with a `products` table (`id`, `name`, `price`, `category`) and inserts at least 6 rows across at least 2 categories.
2. Writes a query selecting `name` and `price` for products with `price > 50`, ordered by price descending.
3. Writes a query finding the 3 cheapest products overall (`ORDER BY` + `LIMIT`).
4. Loads the full `products` table into a Pandas DataFrame using `pd.read_sql()` and prints it.

<details>
<summary>✅ Click to see the solution</summary>

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    category TEXT
)
""")

products_data = [
    (1, "Laptop", 999.99, "Electronics"),
    (2, "Mouse", 25.50, "Accessories"),
    (3, "Keyboard", 45.00, "Accessories"),
    (4, "Monitor", 249.99, "Electronics"),
    (5, "Webcam", 60.00, "Accessories"),
    (6, "Desk Lamp", 30.00, "Furniture"),
]
cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products_data)
conn.commit()

cursor.execute("SELECT name, price FROM products WHERE price > 50 ORDER BY price DESC")
print(cursor.fetchall())

cursor.execute("SELECT name, price FROM products ORDER BY price ASC LIMIT 3")
print(cursor.fetchall())

df = pd.read_sql("SELECT * FROM products", conn)
print(df)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `conn.commit()` after `INSERT`/`UPDATE`/`DELETE` | Always commit after any data-modifying statement |
| Pulling an entire large table into Pandas just to filter it | Filter/aggregate in SQL (`WHERE`, `GROUP BY`) first, then load only what's needed |
| Building SQL queries with f-strings/string concatenation | Use `?` placeholders — covered further next lesson (SQL injection risk) |
| Confusing `fetchall()` tuples with a DataFrame | Use `pd.read_sql()` when you want a DataFrame directly |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand what SQL is and why it matters alongside Pandas
- [ ] Can set up an SQLite database and insert data from Python
- [ ] Can write `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT` queries
- [ ] Can load query results directly into a Pandas DataFrame with `pd.read_sql()`
- [ ] Completed the `sql_basics_practice.py` exercise

**Next:** Continue to [`02-joins-and-aggregation.md`](02-joins-and-aggregation.md)
