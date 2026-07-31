# Module 11b: JOINs & Aggregation

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [01-sql-basics.md](01-sql-basics.md)

## 🎯 Learning Objectives
- [ ] Combine data across tables with `INNER JOIN` and `LEFT JOIN`
- [ ] Summarize data with `GROUP BY` and aggregate functions
- [ ] Filter grouped results with `HAVING`
- [ ] Map each SQL concept to its Pandas equivalent from Module 07

---

## Module Goal

Learn SQL's two most powerful data-combination tools — `JOIN` and `GROUP BY` — which are the *exact same concepts* as `pd.merge()` and `.groupby()` from Module 07, expressed in a different syntax. If Module 07 clicked, this module should feel like translation practice more than new material.

## Why This Matters on the Job

Real databases split data across many tables — customers, orders, products, each normalized separately — and joining them correctly to answer a business question is one of the most common daily SQL tasks. `GROUP BY` answers the "totals/averages per category" questions that come up constantly in business reporting. Recognizing that these map directly onto skills you already have (Module 07's merge/groupby) should make this module feel far less like new material and more like a second language for something you already understand.

---

## Setup: Two Related Tables

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL)")

cursor.executemany("INSERT INTO customers VALUES (?, ?)", [
    (1, "Ada"), (2, "Grace"), (3, "Alan"), (4, "Katherine")
])
cursor.executemany("INSERT INTO orders VALUES (?, ?, ?)", [
    (1, 1, 50.0), (2, 2, 75.0), (3, 1, 30.0), (4, 3, 120.0), (5, 2, 60.0)
])
conn.commit()
```

Notice `orders.customer_id` refers back to `customers.id` — this is a **foreign key** relationship, the standard way relational databases link tables together (conceptually identical to the shared `"department"` key column used in Module 07's `pd.merge()` example). Note that customer `4` (Katherine) has placed **no orders**.

## `INNER JOIN`: Only Matching Rows

```python
cursor.execute("""
SELECT customers.name, orders.amount
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id
""")
print(cursor.fetchall())
```
```
[('Ada', 50.0), ('Grace', 75.0), ('Ada', 30.0), ('Alan', 120.0), ('Grace', 60.0)]
```

**How it works:** `INNER JOIN customers ON orders.customer_id = customers.id` combines rows from both tables wherever the join condition matches — every order gets paired with its customer's name. Katherine, with no orders, doesn't appear at all — exactly like `pd.merge(..., how="inner")` from Module 07.

## `LEFT JOIN`: Keep Every Row From the "Left" Table

```python
cursor.execute("""
SELECT customers.name, orders.amount
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
""")
print(cursor.fetchall())
```
```
[('Ada', 30.0), ('Ada', 50.0), ('Grace', 60.0), ('Grace', 75.0), ('Alan', 120.0), ('Katherine', None)]
```

**How it works:** `FROM customers LEFT JOIN orders` keeps **every** row from `customers` (the "left" table in the `FROM` clause), filling in `NULL` (SQL's equivalent of `NaN`) wherever there's no matching order — Katherine now appears, with `amount` as `None`/`NULL`. This is exactly `pd.merge(customers, orders, how="left")` from Module 07.

| SQL | Pandas equivalent |
|---|---|
| `INNER JOIN` | `pd.merge(df1, df2, how="inner")` |
| `LEFT JOIN` | `pd.merge(df1, df2, how="left")` |
| `RIGHT JOIN` (not supported in SQLite — swap table order + `LEFT JOIN` instead) | `pd.merge(df1, df2, how="right")` |
| `FULL OUTER JOIN` | `pd.merge(df1, df2, how="outer")` |

💡 **Tip:** SQLite doesn't support `RIGHT JOIN` or `FULL OUTER JOIN` directly (some databases, like PostgreSQL, do) — in SQLite, you can usually get the same result from a `RIGHT JOIN` by swapping which table comes first and using `LEFT JOIN` instead.

## `GROUP BY`: Summarizing Data by Category

```python
cursor.execute("""
SELECT customers.name, SUM(orders.amount) as total_spent, COUNT(orders.id) as order_count
FROM customers
JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name
ORDER BY total_spent DESC
""")
print(cursor.fetchall())
```
```
[('Grace', 135.0, 2), ('Alan', 120.0, 1), ('Ada', 80.0, 2)]
```

**How it works:** `GROUP BY customers.name` groups all matching rows by customer, and `SUM(orders.amount)`/`COUNT(orders.id)` compute an aggregate *per group* — exactly the split-apply-combine idea from Module 07's `.groupby("customer_name")["amount"].agg(["sum", "count"])`. `JOIN` (without a keyword prefix) defaults to `INNER JOIN` in SQL.

| SQL aggregate function | Pandas equivalent |
|---|---|
| `SUM(col)` | `.sum()` |
| `AVG(col)` | `.mean()` |
| `COUNT(col)` | `.count()` |
| `MIN(col)` / `MAX(col)` | `.min()` / `.max()` |

## `HAVING`: Filtering *Grouped* Results

```python
cursor.execute("""
SELECT customers.name, SUM(orders.amount) as total_spent
FROM customers
JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.name
HAVING SUM(orders.amount) > 70
""")
print(cursor.fetchall())
```
```
[('Ada', 80.0), ('Alan', 120.0), ('Grace', 135.0)]
```

**How it works:** `WHERE` filters individual rows *before* grouping; `HAVING` filters *groups* themselves, after aggregation — you can't write `WHERE SUM(orders.amount) > 70` because `WHERE` runs before `SUM()` is even computed. This is a very common SQL gotcha and interview question.

⚠️ **Warning:** Mixing up `WHERE` and `HAVING` is one of the most common SQL mistakes — remember: `WHERE` filters rows going *into* the group; `HAVING` filters the *aggregated results coming out*.

🎯 **On the job:** `GROUP BY ... HAVING` is exactly how you'd answer "which customers have spent more than $X in total?" directly at the database level, without pulling every individual order into Python first.

---

## Hands-On Exercise

**Task:** Write `joins_and_groupby_practice.py` that:
1. Creates `students` (`id`, `name`) and `enrollments` (`id`, `student_id`, `course`, `grade`) tables, with at least 5 students (one with **no** enrollments) and 8 enrollment records.
2. Writes an `INNER JOIN` query listing each enrolled student's name alongside their course and grade.
3. Writes a `LEFT JOIN` query that includes the student with no enrollments (their course/grade should show as missing).
4. Writes a `GROUP BY` query computing each student's average grade across their courses, ordered highest to lowest.
5. Writes a query using `HAVING` to find only students whose average grade is above 85.

<details>
<summary>✅ Click to see the solution</summary>

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("""
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course TEXT,
    grade REAL
)
""")

cursor.executemany("INSERT INTO students VALUES (?, ?)", [
    (1, "Ada"), (2, "Grace"), (3, "Alan"), (4, "Katherine"), (5, "Linus")
])
cursor.executemany("INSERT INTO enrollments VALUES (?, ?, ?, ?)", [
    (1, 1, "Math", 92), (2, 1, "Physics", 88),
    (3, 2, "Math", 95), (4, 2, "Physics", 97),
    (5, 3, "Math", 70), (6, 3, "Physics", 75),
    (7, 4, "Math", 84), (8, 4, "Physics", 80),
    # Linus (id=5) has no enrollments
])
conn.commit()

cursor.execute("""
SELECT students.name, enrollments.course, enrollments.grade
FROM enrollments
INNER JOIN students ON enrollments.student_id = students.id
""")
print(cursor.fetchall())

cursor.execute("""
SELECT students.name, enrollments.course, enrollments.grade
FROM students
LEFT JOIN enrollments ON students.id = enrollments.student_id
""")
print(cursor.fetchall())

cursor.execute("""
SELECT students.name, AVG(enrollments.grade) as avg_grade
FROM students
JOIN enrollments ON students.id = enrollments.student_id
GROUP BY students.name
ORDER BY avg_grade DESC
""")
print(cursor.fetchall())

cursor.execute("""
SELECT students.name, AVG(enrollments.grade) as avg_grade
FROM students
JOIN enrollments ON students.id = enrollments.student_id
GROUP BY students.name
HAVING AVG(enrollments.grade) > 85
""")
print(cursor.fetchall())
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Using `WHERE` to filter an aggregated value | Use `HAVING` for conditions on aggregates like `SUM()`/`AVG()` |
| Expecting `INNER JOIN` to include unmatched rows | Use `LEFT JOIN` when the "no match" case matters |
| Forgetting SQLite has no `RIGHT JOIN`/`FULL OUTER JOIN` | Swap table order + `LEFT JOIN`, or switch databases if you truly need these |
| Not recognizing the Pandas equivalent | `JOIN` ≈ `pd.merge()`; `GROUP BY` ≈ `.groupby()` — lean on what you already know |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can write `INNER JOIN` and `LEFT JOIN` queries
- [ ] Understand the SQL join types map directly to `pd.merge()`'s `how=` options
- [ ] Can use `GROUP BY` with aggregate functions (`SUM`, `AVG`, `COUNT`)
- [ ] Understand the difference between `WHERE` and `HAVING`
- [ ] Completed the `joins_and_groupby_practice.py` exercise

**Next:** Continue to [`03-subqueries-and-real-world-sql.md`](03-subqueries-and-real-world-sql.md)
