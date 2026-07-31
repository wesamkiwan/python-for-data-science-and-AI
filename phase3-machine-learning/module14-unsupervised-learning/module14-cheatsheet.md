# 📋 Module 14 Cheat Sheet: Unsupervised Learning & Clustering

Fast reference for K-Means, hierarchical clustering, and PCA.

## Supervised vs. Unsupervised

| | Supervised | Unsupervised |
|---|---|---|
| Data | `X` (features) + `y` (known target) | `X` only, no labels |
| Goal | Predict `y` for new data | Find structure/groupings |
| Evaluate with | Accuracy, RMSE, R², etc. | Silhouette score (no ground truth to compare to) |

## K-Means Clustering
```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

X_scaled = StandardScaler().fit_transform(X)      # ALWAYS scale first -- distance-based

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)                 # combines fit + predict in one call

kmeans.cluster_centers_    # centroid coordinates, one row per cluster
kmeans.inertia_               # sum of squared distances to nearest centroid (lower = tighter)
```

## Elbow Method (choosing k)
```python
inertias = []
for k in range(1, 8):
    m = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    inertias.append(m.inertia_)
# plot inertias vs. k -- look for the "elbow" where improvement flattens
```
⚠️ Inertia always decreases as k increases — never pick k by minimizing inertia alone.

## Silhouette Score (evaluating clusters)
```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X_scaled, labels)   # -1 to +1; higher = better-separated clusters
```

## Hierarchical Clustering
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

agg = AgglomerativeClustering(n_clusters=3)
labels = agg.fit_predict(X_scaled)

Z = linkage(X_scaled, method="ward")
dendrogram(Z)   # visualize the full merge tree; cut height determines final cluster count
```

| K-Means | Hierarchical |
|---|---|
| Must choose k upfront | Can inspect the full tree before choosing a cut |
| Scales well to large data | Better for smaller datasets |
| Flat clusters | Nested hierarchy |

## PCA (Dimensionality Reduction)
```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)          # ALWAYS scale features first
X_pca = pca.fit_transform(X_scaled)

pca.explained_variance_ratio_        # variance captured by each component
sum(pca.explained_variance_ratio_)      # total variance preserved
```
💡 Keep enough components to preserve ~90-95% of total variance, as a common rule of thumb.

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Clusters look arbitrary/meaningless | Ran K-Means/hierarchical without scaling | Scale features first |
| Picked k by lowest inertia | Inertia always decreases with more clusters | Use the elbow (biggest relative drop), not the minimum |
| PCA components dominated by one original feature | Skipped scaling before PCA | Scale first — PCA is variance-based |
| Dendrogram unreadable | Too many points plotted at once | Use a smaller subset, or truncate the dendrogram display |
| Low silhouette score | Clusters genuinely overlap, or wrong k chosen | Try different k values; some real data just doesn't cluster cleanly |

## The "New Clustering Task" Workflow
1. Scale features first — every technique in this module is distance/variance-based.
2. If you don't know k: run the elbow method, inspect a dendrogram, or try both.
3. Fit K-Means or `AgglomerativeClustering` with your chosen k.
4. Evaluate with the silhouette score (no ground truth available otherwise).
5. If features are numerous, use PCA to compress to 2D for visualization.
