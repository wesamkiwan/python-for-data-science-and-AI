# Module 14a: K-Means Clustering

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 13 — Feature Engineering & Model Evaluation](../module13-feature-engineering-evaluation/03-cross-validation-and-overfitting.md)

## 🎯 Learning Objectives
- [ ] Explain unsupervised learning and how it differs from everything in Modules 12-13
- [ ] Run K-Means clustering with scikit-learn
- [ ] Use the elbow method to choose a reasonable number of clusters
- [ ] Evaluate clustering quality with the silhouette score

---

## Module Goal

Meet **unsupervised learning** — a fundamentally different problem shape from everything so far in Phase 3. Instead of learning to predict a known target (Module 12/13's classification/regression), you'll learn to find hidden structure and groupings in data that has **no labels at all**.

## Why This Matters on the Job

"We have 100,000 customers and no predefined segments — can you find natural groupings in their behavior?" is a classic unsupervised learning request. Customer segmentation, anomaly detection, and organizing unlabeled documents by topic are all real, common business applications where there's no "correct answer" column to train against — you're discovering structure, not predicting a known outcome.

---

## Supervised vs. Unsupervised Learning

Recall from Module 12a: supervised learning has a **target** (`y`) — labeled, correct answers to learn from. **Unsupervised learning** has no target at all — just features (`X`), and the goal is to find inherent structure or patterns within them.

| | Supervised (Modules 12-13) | Unsupervised (this module) |
|---|---|---|
| Data | Features + known target (`X`, `y`) | Features only (`X`) |
| Goal | Predict the target for new data | Discover structure/groupings |
| Example | "Is this transaction fraud?" | "What natural customer segments exist?" |
| Evaluation | Accuracy, RMSE, etc. (compare to true answer) | No true answer to compare to — different metrics needed |

💡 **Tip:** This missing "correct answer" is precisely why unsupervised learning needs its own evaluation approach (the silhouette score, later in this lesson) — there's no `y_test` to check predictions against.

## K-Means Clustering

**K-Means** is the most common clustering algorithm — it groups data into `k` clusters, where each point belongs to whichever cluster's center (**centroid**) is closest.

```python
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

iris = load_iris()
X = iris.data   # NOTE: we deliberately ignore iris.target here -- unsupervised means no labels used

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)   # scaling matters here too -- KMeans is distance-based (Module 13a)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

print(cluster_labels[:20])   # which cluster (0, 1, or 2) each of the first 20 flowers was assigned to
print(kmeans.cluster_centers_.shape)   # (3, 4) -- one centroid per cluster, each with 4 feature values
```

**How it works:** `.fit_predict()` combines fitting the model *and* returning each point's assigned cluster in one step (there's no separate `y` to fit against — unlike supervised learning's `.fit(X, y)`). `n_clusters=3` tells K-Means how many groups to find; `n_init=10` runs the algorithm 10 times with different random starting points and keeps the best result (K-Means can get stuck in different local solutions depending on its random start).

⚠️ **Warning:** K-Means is distance-based, so feature scaling (Module 13a) matters just as much here as it did for logistic regression/KNN — without scaling, a feature with a much larger numeric range would dominate the distance calculation and distort the clusters.

### Do the Clusters Make Sense? (A Sanity Check)

Since we deliberately ignored the true species labels, let's peek at them purely to sanity-check whether K-Means found something meaningful:

```python
import pandas as pd

comparison = pd.DataFrame({"cluster": cluster_labels, "species": iris.target_names[iris.target]})
print(pd.crosstab(comparison["cluster"], comparison["species"]))
```
```
species  setosa  versicolor  virginica
cluster
0             0          39         14
1            50           0          0
2             0          11         36
```

**How it works:** Cluster `1` corresponds almost perfectly to `setosa` (all 50 setosa flowers, no others), while clusters `0` and `2` split `versicolor`/`virginica` with some overlap — reflecting that these two species are genuinely harder to visually distinguish by these measurements alone. This is a great illustration of the point: K-Means found this structure *without ever being told* the species labels, purely from the numeric feature patterns.

## The Elbow Method: Choosing `k`

In real unsupervised problems, you often don't know the "right" number of clusters ahead of time (unlike this Iris example, where we happen to know there are 3 species). The **elbow method** helps estimate a reasonable `k`.

```python
inertias = []
for k in range(1, 8):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertias.append(model.inertia_)

print(inertias)
```
```
[600.0, 222.36, 139.82, 114.09, 90.93, 81.54, 72.63]
```

**How it works:** `inertia_` measures how tightly clustered the points are around their centroids (lower is "tighter") — it always decreases as `k` increases (more clusters can always fit the data more tightly), so you can't just pick the `k` with the lowest inertia, or you'd end up with one cluster per point. Instead, plot inertia against `k` and look for the "elbow" — the point where adding more clusters stops giving a meaningfully large improvement. Here, the drop from `k=2` to `k=3` (222→140) is much larger than from `k=3` to `k=4` (140→114), suggesting `k=3` is a reasonable elbow — which happens to match the true number of species.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(range(1, 8), inertias, marker="o")
ax.set_xlabel("Number of clusters (k)")
ax.set_ylabel("Inertia")
ax.set_title("Elbow Method")
fig.savefig("elbow_plot.png")
```

## Evaluating Clusters: The Silhouette Score

Since there's no `y_test` to check against, clustering needs its own evaluation metric.

```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X_scaled, cluster_labels)
print(f"Silhouette score: {score:.4f}")   # 0.4599
```

**How it works:** The **silhouette score** ranges from -1 to 1, measuring how well each point fits its assigned cluster compared to the *next-closest* other cluster. A score near `+1` means points are tightly grouped with their own cluster and far from others (great clustering); near `0` means clusters overlap significantly; negative means points may be assigned to the wrong cluster entirely. `0.46` here reflects decent, but not perfect, separation — consistent with the overlap seen between versicolor and virginica above.

🎯 **On the job:** Run the elbow method *and* compare silhouette scores across a few candidate `k` values together — they can occasionally disagree slightly, and looking at both gives more confidence in the final choice than either alone.

---

## Hands-On Exercise

**Task:** Write `kmeans_practice.py` that:
1. Loads `load_wine()` from `sklearn.datasets` (used in Modules 12-13).
2. Scales the features with `StandardScaler`.
3. Runs the elbow method for `k` from 1 to 8, printing the inertia at each step.
4. Based on the printed inertias, picks a reasonable `k` and runs K-Means with it.
5. Prints the silhouette score for that choice of `k`.
6. Cross-tabulates the resulting clusters against `wine.target` (the true class, just for a sanity check) and prints it.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

wine = load_wine()
X = wine.data

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
for k in range(1, 8):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertias.append(model.inertia_)
print(inertias)

# Wine has 3 known classes -- a reasonable k to try, given the elbow
chosen_k = 3
kmeans = KMeans(n_clusters=chosen_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

score = silhouette_score(X_scaled, cluster_labels)
print(f"Silhouette score (k={chosen_k}): {score:.4f}")

comparison = pd.DataFrame({"cluster": cluster_labels, "true_class": wine.target})
print(pd.crosstab(comparison["cluster"], comparison["true_class"]))
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Running K-Means without scaling features | Scale first — K-Means is distance-based, exactly like KNN |
| Picking `k` by minimizing inertia alone | Inertia always decreases with more clusters — use the elbow, not the minimum |
| Treating cluster labels (0, 1, 2...) as meaningful order | They're arbitrary IDs, not ranked categories |
| Assuming clusters will perfectly match a known category | Real clusters often show overlap — clustering finds structure in the *features*, not a hidden ground truth |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand the core difference between supervised and unsupervised learning
- [ ] Can run K-Means clustering with scikit-learn
- [ ] Can use the elbow method to help choose `k`
- [ ] Can evaluate clustering quality with the silhouette score
- [ ] Completed the `kmeans_practice.py` exercise

**Next:** Continue to [`02-hierarchical-clustering-and-pca.md`](02-hierarchical-clustering-and-pca.md)
