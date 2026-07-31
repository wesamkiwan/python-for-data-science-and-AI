# Module 14b: Hierarchical Clustering & PCA

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-kmeans-clustering.md](01-kmeans-clustering.md)

## 🎯 Learning Objectives
- [ ] Explain hierarchical clustering and read a dendrogram
- [ ] Explain what dimensionality reduction is and why it's useful
- [ ] Apply PCA to reduce features while preserving most of the variance
- [ ] Visualize high-dimensional data in 2D using PCA

---

## Module Goal

Learn a second clustering approach — **hierarchical clustering**, which builds a full tree of nested groupings rather than committing to one fixed `k` upfront — and **PCA (Principal Component Analysis)**, the standard technique for compressing many features down to a smaller number while preserving as much information as possible.

## Why This Matters on the Job

Hierarchical clustering is especially useful when you don't know how many groups to expect, or when the *nested* relationship between groups matters (e.g., biological taxonomies, organizational hierarchies). PCA is one of the most widely used tools in all of data science — for visualizing high-dimensional data in 2D, for speeding up downstream models by reducing feature count, and as a stepping stone toward the dimensionality concepts that reappear throughout Phase 4's deep learning content.

---

## Hierarchical Clustering

**Hierarchical clustering** builds a tree (a **dendrogram**) of nested clusters — starting with every point as its own cluster and progressively merging the closest pairs, all the way up to one single cluster containing everything.

```python
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

agg_clustering = AgglomerativeClustering(n_clusters=3)
cluster_labels = agg_clustering.fit_predict(X_scaled)
print(cluster_labels[:20])
```

**How it works:** `AgglomerativeClustering` (the standard scikit-learn hierarchical clustering implementation) still requires specifying `n_clusters` to produce a final flat clustering, but the algorithm underneath builds the full merge tree first — unlike K-Means, which directly optimizes for `k` clusters from the start.

### Visualizing the Tree: A Dendrogram

```python
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# Using a small subset for a readable plot (dendrograms get cluttered with many points)
Z = linkage(X_scaled[:30], method="ward")

fig, ax = plt.subplots(figsize=(10, 5))
dendrogram(Z, ax=ax)
ax.set_title("Hierarchical Clustering Dendrogram")
fig.savefig("dendrogram.png")
```

**How it works:** `linkage(X, method="ward")` computes the merge tree — `"ward"` is a common method that minimizes the variance being merged at each step. The resulting dendrogram shows every point at the bottom, with lines merging upward — the *height* at which two branches merge represents how dissimilar those groups were when combined. **Cutting** the dendrogram horizontally at a chosen height determines the final number of clusters: a cut low down produces many small clusters; a cut near the top produces just a couple of large ones.

| K-Means | Hierarchical Clustering |
|---|---|
| Must choose `k` upfront | Can choose the cut height *after* seeing the full tree |
| Fast, scales well to large datasets | Slower, typically used on smaller datasets |
| Produces flat, non-nested clusters | Produces a full nested hierarchy (useful when sub-groupings matter) |

💡 **Tip:** A dendrogram is genuinely useful even before deciding on a final number of clusters — visually scanning it for a natural, large gap between merge heights (a long vertical stretch with no merges) is a strong hint for a good place to "cut."

## PCA: Principal Component Analysis (Dimensionality Reduction)

**Dimensionality reduction** means compressing many features down to fewer, while preserving as much of the original information (variance) as possible. **PCA** is the standard technique for this.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)   # compress down to just 2 new "components"
X_pca = pca.fit_transform(X_scaled)

print(X_pca.shape)                       # (150, 2) -- 4 original features compressed to 2
print(pca.explained_variance_ratio_)       # [0.7296 0.2285] -- how much variance each component captures
print(sum(pca.explained_variance_ratio_))     # 0.9581 -- together, these 2 components preserve ~96% of the info
```

**How it works:** PCA creates new features (**principal components**) that are combinations of the original ones, ordered so the first component captures the most variance (spread/information) possible, the second captures the most *remaining* variance, and so on. Here, the first 2 components together preserve about 96% of the original 4 features' total variance — a huge compression (4 → 2 features) with very little information lost.

⚠️ **Warning:** Always scale features (Module 13a) *before* PCA — since PCA is fundamentally about variance, an unscaled feature with a naturally larger numeric range would dominate the components regardless of its actual importance, exactly like the distance-based algorithms from the last lesson.

### Visualizing High-Dimensional Data in 2D

The Iris dataset has 4 features — impossible to plot directly on a normal 2D scatter plot. PCA solves this by compressing it down to exactly 2 dimensions for visualization:

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
df["species"] = iris.target_names[iris.target]

fig, ax = plt.subplots()
sns.scatterplot(data=df, x="PC1", y="PC2", hue="species", ax=ax)
ax.set_title("Iris Dataset Compressed to 2 Principal Components")
fig.savefig("pca_scatter.png")
```

**How it works:** Even though `PC1` and `PC2` aren't any single original measurement — they're mathematical combinations of all 4 original features — plotting them reveals the same clear separation between species that the original 4-dimensional data contained, just made visible in 2D.

🎯 **On the job:** This "compress to 2D and plot" pattern is one of the most common ways data scientists explore a high-dimensional dataset visually — you can't plot 20 features against each other directly, but you *can* plot their first two principal components and often still see meaningful structure.

### Choosing How Many Components to Keep

```python
pca_full = PCA()   # no n_components limit -- keep all of them, just to inspect variance
pca_full.fit(X_scaled)
print(pca_full.explained_variance_ratio_)   # [0.7296 0.2285 0.0367 0.0052]
```

💡 **Tip:** A common rule of thumb: keep enough components to preserve 90-95% of total variance. Here, the first 2 components alone already reach ~96%, so keeping just 2 (out of the original 4) is a very reasonable choice for this dataset.

---

## Hands-On Exercise

**Task:** Write `hierarchical_pca_practice.py` that:
1. Loads `load_wine()`, scales it with `StandardScaler`.
2. Runs `AgglomerativeClustering` with `n_clusters=3` and prints the first 20 cluster labels.
3. Applies PCA to reduce the Wine dataset (13 features) down to 2 components, and prints the explained variance ratio for each, plus their sum.
4. Creates a Seaborn scatter plot of the 2 principal components, colored by `wine.target`, and saves it.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA

wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

agg = AgglomerativeClustering(n_clusters=3)
labels = agg.fit_predict(X_scaled)
print(labels[:20])

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)
print(f"Total variance preserved: {sum(pca.explained_variance_ratio_):.4f}")

df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
df["class"] = wine.target_names[wine.target]

fig, ax = plt.subplots()
sns.scatterplot(data=df, x="PC1", y="PC2", hue="class", ax=ax)
ax.set_title("Wine Dataset Compressed to 2 Principal Components")
fig.savefig("wine_pca_scatter.png")
```

**Expected outcome:** The first 2 components should preserve a majority (though likely somewhat less than Iris's ~96%, since Wine has more original features/complexity) of the total variance, and the scatter plot should show reasonably distinct groupings by wine class.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Running PCA on unscaled features | Always scale first — PCA is fundamentally about variance, sensitive to scale |
| Reading dendrogram merge order as "importance" | Merge height reflects dissimilarity at that step, not feature importance |
| Assuming principal components are individually meaningful/interpretable | They're mathematical combinations of original features, not a single original measurement |
| Keeping too few or too many components without checking `explained_variance_ratio_` | Check the cumulative variance and choose based on how much information you need to preserve |

---

## ✅ Module 14 Completion Checklist
- [ ] Can run hierarchical clustering and read a dendrogram
- [ ] Understand how K-Means and hierarchical clustering differ
- [ ] Can apply PCA to reduce dimensionality
- [ ] Can interpret `explained_variance_ratio_` to decide how many components to keep
- [ ] Can visualize high-dimensional data in 2D using PCA
- [ ] Completed the `hierarchical_pca_practice.py` exercise
- [ ] Reviewed [`module14-cheatsheet.md`](module14-cheatsheet.md)
- [ ] Reviewed [`module14-interview.md`](module14-interview.md)
- [ ] Browsed [`module14-references.md`](module14-references.md)

**Next Step:** Module 15 — Ensemble Methods & Advanced ML (`phase3-machine-learning/module15-ensemble-advanced-ml/`)
