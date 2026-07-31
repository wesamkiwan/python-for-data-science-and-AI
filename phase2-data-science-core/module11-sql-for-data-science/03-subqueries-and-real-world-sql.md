# Module 11c: Subqueries, CTEs & Real-World SQL

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-joins-and-aggregation.md](02-joins-and-aggregation.md)

## 🎯 Learning Objectives
- [ ] Write a subquery inside `WHERE` and inside `FROM`
- [ ] Use a CTE (`WITH` clause) to write cleaner, more readable multi-step queries
- [ ] Explain why parameterized queries prevent SQL injection
- [ ] Decide when to push work into SQL vs. when to bring data into Pandas

---

## Module Goal

Finish the SQL toolkit with **subqueries** and **CTEs (Common Table Expressions)** — tools for building multi-step queries — plus one critical security practice (parameterized queries), and close with guidance on dividing work between SQL and Pandas in real analysis.

## Why This Matters on the Job

Real business questions are rarely answerable with one flat `SELECT`— "customers who spent more than average," "departments above the company-wide median" — these require comparing individual rows against an aggregate computed from the *same* dataset, which is exactly what subqueries and CTEs are for. And any time user input ever reaches a SQL query (a search box, a form field), SQL injection is a real, serious vulnerability — this module's security note is not optional reading.

---

## Subqueries: A Query Inside a Query

A **subquery** is a `SELECT` nested inside another query, most commonly to compare against an aggregate value.

### Subquery in `WHERE`

```python
cursor.execute("""
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
""")
print(cursor.fetchall())
```
```
[('Grace', 120000.0), ('Katherine', 130000.0)]
```

**How it works:** The inner query `(SELECT AVG(salary) FROM employees)` computes the company-wide average salary first; the outer query then compares every employee's salary against that single number. This solves a problem `HAVING` can't — `HAVING` filters *grouped* results, but "employees above the overall average" needs to compare individual rows against a single aggregate computed separately, which is exactly what a subquery in `WHERE` does.

### Subquery in `FROM`

```python
cursor.execute("""
SELECT department, avg_salary FROM (
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
) WHERE avg_salary > 90000
""")
print(cursor.fetchall())
```
```
[('Engineering', 102000.0), ('Research', 109000.0)]
```

**How it works:** The inner query computes each department's average salary first, producing a small temporary result; the outer query then filters *that* result. This achieves the same thing `HAVING` would here, but demonstrates the more general pattern: treat any query's result as if it were a table, and query it further.

## CTEs (`WITH`): Cleaner Multi-Step Queries

A **CTE (Common Table Expression)**, written with `WITH`, names a subquery upfront — making complex, multi-step queries much easier to read than nesting subqueries inside each other.

```python
cursor.execute("""
WITH dept_avg AS (
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
)
SELECT * FROM dept_avg WHERE avg_salary > 90000
""")
print(cursor.fetchall())
```
```
[('Engineering', 102000.0), ('Research', 109000.0)]
```

**How it works:** `WITH dept_avg AS (...)` computes the same subquery as before, but gives it a name (`dept_avg`) that the rest of the query can reference like a regular table. This produces an identical result to the "subquery in `FROM`" version above, but reads top-to-bottom far more naturally, especially once you have several steps chained together.

✅ **Best Practice:** Prefer a CTE over a nested subquery whenever a query has more than one logical step — it names each stage of your reasoning, making the query dramatically easier for someone else (or future you) to read and debug.

## ⚠️ SQL Injection: A Critical Security Note

**SQL injection** happens when untrusted input (like user-typed text) is inserted directly into a SQL query string, letting an attacker manipulate the query itself.

```python
# ❌ DANGEROUS -- never do this with any untrusted input
user_input = "Ada"
query = f"SELECT * FROM employees WHERE name = '{user_input}'"
cursor.execute(query)

# If user_input were instead: "Ada' OR '1'='1"
# the query becomes: SELECT * FROM employees WHERE name = 'Ada' OR '1'='1'
# which returns EVERY row, completely bypassing the intended filter!
```

```python
# ✅ SAFE -- always use parameterized queries with placeholders
user_input = "Ada"
cursor.execute("SELECT * FROM employees WHERE name = ?", (user_input,))
print(cursor.fetchall())
```

**How it works:** The `?` placeholder (used throughout this module for `INSERT`s) tells the database driver to treat `user_input` strictly as a *data value*, never as executable SQL syntax — no matter what characters it contains, it can never alter the query's structure. This is the same principle behind avoiding f-string-built SQL entirely, and is a non-negotiable practice anywhere user input reaches a database query.

⚠️ **Warning:** This isn't a theoretical concern — SQL injection has been one of the most damaging, most common real-world security vulnerabilities for decades. ✅ **Best Practice:** *always* use parameterized queries (`?` placeholders passed as a separate tuple/list argument) — never build a SQL string by directly inserting a variable's value with an f-string or `+` concatenation.

## Deciding: SQL vs. Pandas — Where Should the Work Happen?

| Situation | Do it in... |
|---|---|
| Filtering a huge table down to what you actually need | SQL (`WHERE`) — reduces data transferred before it ever reaches Python |
| Simple aggregations (totals, averages per category) | Either — SQL (`GROUP BY`) if the database can do it efficiently; Pandas if you need the raw rows too |
| Combining data from multiple tables | SQL (`JOIN`) if both tables are already in the database |
| Complex statistical analysis, visualization, machine learning | Pandas/NumPy/scikit-learn — SQL isn't built for this |
| Iterative, exploratory "let me try a few different views of this" work | Pandas — much faster to adjust than repeatedly rewriting SQL queries |

✅ **Best Practice:** A common, effective real-world pattern: write a SQL query that filters and joins down to *roughly* the dataset you need (reducing what has to travel over the network/into memory), then do the rest of the analysis — cleaning, statistics, visualization — in Pandas, where you have Modules 06-10's full toolkit available.

---

## Hands-On Exercise

**Task:** Write `subqueries_practice.py` using the `students`/`enrollments` tables from the previous lesson (recreate them):
1. Write a subquery finding students whose average grade is above the *overall* average grade across all enrollments (not per-student — the single overall average).
2. Rewrite the same query as a CTE, and confirm both produce the same result.
3. Write a parameterized query (`?` placeholder) that safely looks up all enrollments for a course name provided as a Python variable, and test it with `course = "Math"`.
4. In a comment, explain in your own words why using an f-string to build that same query would be a security risk.

<details>
<summary>✅ Click to see the solution</summary>

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("""
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY, student_id INTEGER, course TEXT, grade REAL
)
""")
cursor.executemany("INSERT INTO students VALUES (?, ?)", [
    (1, "Ada"), (2, "Grace"), (3, "Alan"), (4, "Katherine")
])
cursor.executemany("INSERT INTO enrollments VALUES (?, ?, ?, ?)", [
    (1, 1, "Math", 92), (2, 1, "Physics", 88),
    (3, 2, "Math", 95), (4, 2, "Physics", 97),
    (5, 3, "Math", 70), (6, 3, "Physics", 75),
    (7, 4, "Math", 84), (8, 4, "Physics", 80),
])
conn.commit()

# Subquery version
cursor.execute("""
SELECT students.name, AVG(enrollments.grade) as avg_grade
FROM students
JOIN enrollments ON students.id = enrollments.student_id
GROUP BY students.name
HAVING AVG(enrollments.grade) > (SELECT AVG(grade) FROM enrollments)
""")
print(cursor.fetchall())

# CTE version -- should match exactly
cursor.execute("""
WITH overall_avg AS (
    SELECT AVG(grade) as avg_grade FROM enrollments
)
SELECT students.name, AVG(enrollments.grade) as student_avg
FROM students
JOIN enrollments ON students.id = enrollments.student_id
GROUP BY students.name
HAVING AVG(enrollments.grade) > (SELECT avg_grade FROM overall_avg)
""")
print(cursor.fetchall())

# Parameterized query
course = "Math"
cursor.execute("SELECT * FROM enrollments WHERE course = ?", (course,))
print(cursor.fetchall())

# An f-string like f"... WHERE course = '{course}'" would let someone pass a value
# such as "Math' OR '1'='1" to alter the query's logic and return unintended rows --
# the ? placeholder guarantees `course` is always treated as pure data, never as SQL syntax.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Nesting several subqueries inside each other | Use a CTE (`WITH`) to name each step clearly |
| Building SQL queries with f-strings/concatenation | Always use `?` parameterized placeholders |
| Pulling an entire table into Pandas before filtering | Filter/join in SQL first when working with large tables |
| Using SQL for tasks it's not built for (stats, ML, plotting) | Bring data into Pandas/NumPy/scikit-learn for that work |

---

## ✅ Module 11 Completion Checklist
- [ ] Can write a subquery in `WHERE` and in `FROM`
- [ ] Can rewrite a subquery as a cleaner CTE using `WITH`
- [ ] Understand SQL injection and always use parameterized (`?`) queries
- [ ] Can reason about when to do work in SQL vs. Pandas
- [ ] Completed the `subqueries_practice.py` exercise
- [ ] Reviewed [`module11-cheatsheet.md`](module11-cheatsheet.md)
- [ ] Reviewed [`module11-interview.md`](module11-interview.md)
- [ ] Browsed [`module11-references.md`](module11-references.md)

**Next Step:** Module 12 — ML Foundations with scikit-learn (`phase3-machine-learning/module12-ml-foundations/`)

---

## 🎉 Phase 2 Complete!

You've finished **Phase 2: Data Science Core** — you can now load, clean, visualize, statistically analyze, and query data from a database. Everything from Phase 3 onward (Machine Learning) is built directly on top of these skills: every model you train starts from a Pandas DataFrame prepared exactly the way you've been practicing.
