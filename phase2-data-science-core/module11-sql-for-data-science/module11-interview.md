# 🎤 Module 11 Interview Prep: SQL for Data Scientists

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between `WHERE` and `HAVING`?**
> A: `WHERE` filters individual rows before any grouping/aggregation happens. `HAVING` filters groups *after* aggregation — it's the only place you can put a condition on an aggregate function like `SUM()` or `AVG()`, because those values don't exist yet when `WHERE` runs. If you need "customers with total orders over $100," that's a `HAVING SUM(amount) > 100` after a `GROUP BY`, not a `WHERE`.

**Q: What's the difference between `INNER JOIN` and `LEFT JOIN`?**
> A: `INNER JOIN` returns only rows that have a match in both tables — if a row on either side has no counterpart, it's excluded. `LEFT JOIN` keeps every row from the "left" (first-listed) table regardless of whether a match exists, filling in `NULL` for columns from the right table when there's no match. I'd use `LEFT JOIN` whenever I need to guarantee every record from my primary table appears in the result, matched or not.

**Q: Why should you never build a SQL query by inserting a variable directly into an f-string?**
> A: This exposes the query to SQL injection — if the variable ever contains untrusted (e.g., user-typed) input, an attacker could include SQL syntax that changes the query's meaning entirely, potentially returning or modifying data they shouldn't have access to. Parameterized queries (`?` placeholders passed as a separate argument) guarantee the value is always treated as pure data, never as executable SQL, regardless of its content.

### 🟡 Intermediate

**Q: When would you use a subquery instead of a `JOIN`?**
> A: A subquery is the right tool when you need to compare individual rows against a single aggregate value computed from the same (or a related) table — e.g., "employees earning more than the company-wide average salary." A `JOIN` is for combining rows from two tables based on a shared key, producing a wider combined row-set. They can sometimes solve overlapping problems, but subqueries shine specifically for "compare against an aggregate" logic that a plain join and `GROUP BY`/`HAVING` can't always express as directly.

**Q: What's the benefit of using a CTE (`WITH` clause) over a nested subquery?**
> A: A CTE names each logical step of a multi-stage query, letting you read it top-to-bottom in the order you'd naturally reason about the problem, rather than parsing inward from a deeply nested subquery. Functionally, a CTE and an equivalent nested subquery often produce identical results and performance — the real benefit is readability and maintainability, especially once a query has more than one logical step.

**Q: You need to analyze a 50-million-row table using both SQL and Pandas. How would you divide the work?**
> A: I'd do as much filtering, joining, and aggregation as possible directly in SQL first — `WHERE` to narrow down rows, `GROUP BY` for any straightforward per-category summaries — so that only the reduced, relevant subset of data actually gets pulled into Python. Anything beyond what SQL is built for — detailed statistical analysis, visualization, machine learning — I'd do in Pandas/NumPy/scikit-learn once the data is a manageable size. Pulling the full 50 million rows into a DataFrame just to filter it there would be far less efficient than letting the database do that work first.

## Practical/Coding Questions

**Q: Write a query to find the top 3 highest-paid employees in each department (conceptually — a full "top N per group" solution uses window functions, beyond this module's scope, but describe the simpler approach this module covers).**
```sql
-- Simplified: top 3 overall, not per-department (true per-group top-N needs window functions)
SELECT name, department, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;
```
> Explanation: `ORDER BY salary DESC LIMIT 3` is the standard pattern this module covers for "top N overall." A true "top N per group" (top 3 within *each* department) requires window functions like `ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)`, which is a natural next topic once this module's fundamentals are solid.

**Q: Write a parameterized query that safely searches for orders above a minimum amount, where the minimum is a variable.**
```python
min_amount = 100
cursor.execute("SELECT * FROM orders WHERE amount > ?", (min_amount,))
print(cursor.fetchall())
```
> Explanation: even though `min_amount` here is a trusted, hardcoded value, using the `?` placeholder is the correct habit regardless — it costs nothing when the value is safe, and it's the only safe pattern the moment that value could ever come from user input.

## Scenario Questions

**Q: A query using `WHERE COUNT(*) > 5` fails with an error. What's wrong, and how do you fix it?**
> A: `WHERE` executes before aggregation, so `COUNT(*)` (an aggregate function) isn't computed yet at the point `WHERE` runs — the database can't evaluate a condition on a value that doesn't exist yet at that stage. The fix is to move the condition to `HAVING COUNT(*) > 5`, which runs after `GROUP BY` has produced the aggregated counts.

**Q: You're asked to find all customers who have never placed an order. How would you write this?**
> A: I'd use a `LEFT JOIN` from `customers` to `orders`, then filter for rows where the `orders` side is `NULL` — since `LEFT JOIN` keeps every customer row regardless of a match, any customer with zero orders shows up with `NULL` in every order-related column. In SQL: `SELECT customers.name FROM customers LEFT JOIN orders ON customers.id = orders.customer_id WHERE orders.id IS NULL`.

## "Gotcha" Questions

**Q: Why does this query return a syntax/logic problem, and how would you fix it?**
```sql
SELECT department, AVG(salary)
FROM employees
WHERE AVG(salary) > 90000
GROUP BY department;
```
> A: `WHERE` can't reference `AVG(salary)` because aggregation hasn't happened yet when `WHERE` is evaluated — this needs to be a `HAVING` clause instead, placed *after* `GROUP BY`: `... GROUP BY department HAVING AVG(salary) > 90000`.

**Q: A junior developer builds a query as `f"SELECT * FROM users WHERE username = '{username}'"` using a value typed into a login form. What's the risk, concretely?**
> A: If `username` contains something like `x' OR '1'='1`, the resulting query becomes `SELECT * FROM users WHERE username = 'x' OR '1'='1'` — since `'1'='1'` is always true, this returns *every* row in the table, completely bypassing the intended filter. Depending on how the result is used (e.g., login logic), this could let an attacker log in as any user without a valid password. The fix is a parameterized query: `cursor.execute("SELECT * FROM users WHERE username = ?", (username,))`.

## Quick-Fire Rapid Review

- Q: Filters rows before grouping? → **`WHERE`**
- Q: Filters groups after aggregation? → **`HAVING`**
- Q: Join that keeps every row from the "left" table? → **`LEFT JOIN`**
- Q: Join that keeps only matching rows from both tables? → **`INNER JOIN`**
- Q: SQL clause that names a subquery for readability? → **`WITH` (CTE)**
- Q: Safe way to include a variable in a query? → **`?` parameterized placeholder**
- Q: Required after `INSERT`/`UPDATE`/`DELETE` in sqlite3? → **`conn.commit()`**
- Q: Pandas equivalent of SQL's `JOIN`? → **`pd.merge()`**
