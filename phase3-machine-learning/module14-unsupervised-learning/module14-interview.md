# 🎤 Module 14 Interview Prep: Unsupervised Learning & Clustering

## Conceptual Questions

### 🟢 Beginner

**Q: What's the fundamental difference between supervised and unsupervised learning?**
> A: Supervised learning trains on data with known, labeled outcomes (a target variable `y`) and learns to predict that target for new data. Unsupervised learning works with features only, no labels — the goal is to discover inherent structure or patterns in the data itself, like natural groupings, rather than predicting a known answer.

**Q: How does K-Means decide which cluster a point belongs to?**
> A: Each point is assigned to whichever cluster's centroid (center point) it's closest to, using distance in feature space. The algorithm iterates: assign points to the nearest current centroid, recompute each centroid as the average of its assigned points, then repeat until assignments stop changing.

**Q: Why can't you evaluate clustering with accuracy the way you would a classifier?**
> A: Accuracy requires knowing the true, correct label for each data point to compare predictions against — but unsupervised learning has no labels at all. Instead, metrics like the silhouette score evaluate cluster quality intrinsically, based on how tightly grouped points are within their own cluster versus how far they are from other clusters, without needing any ground-truth answer.

### 🟡 Intermediate

**Q: Why does inertia always decrease as you increase the number of clusters in K-Means, and why does that make choosing k tricky?**
> A: More clusters means each point has more, smaller groups to choose from, so points can always be assigned closer to *some* centroid — in the extreme, one cluster per point gives zero inertia. This means you can't simply pick the k with the lowest inertia; instead, the elbow method looks for the point where adding more clusters stops producing a meaningfully large improvement, since the "always decreasing" property makes a naive minimum meaningless.

**Q: What's the difference between K-Means and hierarchical clustering, and when would you prefer one over the other?**
> A: K-Means requires choosing the number of clusters upfront and directly optimizes for that many flat, non-nested groups — it's fast and scales well to large datasets. Hierarchical clustering builds a full nested tree of merges first, letting you choose the number of clusters *after* seeing the whole structure (by deciding where to "cut" the dendrogram), and naturally reveals sub-group relationships — but it's typically slower and less practical on very large datasets. I'd prefer hierarchical clustering when the nested structure itself is meaningful or when I'm unsure of the right number of clusters, and K-Means when I need something fast and scalable, especially on larger data.

**Q: Explain what PCA actually does, without using the word "eigenvector."**
> A: PCA creates new features (principal components) that are weighted combinations of the original features, ordered so the first one captures as much of the data's overall variance (spread/information) as possible, the second captures as much of what's left, and so on. This lets you keep just the first few components — often preserving 90%+ of the original information — while dramatically reducing the number of features, which is useful for visualization, speeding up downstream models, and reducing noise.

## Practical/Coding Questions

**Q: Write code that scales a dataset, runs K-Means with k=4, and reports the silhouette score.**
```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

score = silhouette_score(X_scaled, labels)
print(f"Silhouette score: {score:.4f}")
```
> Explanation: scaling first is essential since K-Means is distance-based; `fit_predict` handles clustering in one call; the silhouette score gives an intrinsic quality measure with no ground truth needed.

**Q: Write code to reduce a dataset to 2 principal components and report how much variance is preserved.**
```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

variance_preserved = sum(pca.explained_variance_ratio_)
print(f"Variance preserved by 2 components: {variance_preserved:.4f}")
```
> Explanation: `explained_variance_ratio_` gives the fraction of total variance each component captures; summing the first `n_components` values tells you how much of the original information survives the compression.

## Scenario Questions

**Q: A marketing team wants to segment customers into groups for targeted campaigns but has no predefined categories. How would you approach this?**
> A: This is a classic unsupervised clustering problem — I'd gather relevant behavioral/demographic features (purchase frequency, average order value, tenure, etc.), scale them, and run K-Means, using the elbow method and silhouette score together to settle on a reasonable number of segments. I'd then profile each resulting cluster (average feature values per cluster) to give the marketing team human-readable descriptions of each segment ("high-frequency, low-value" vs. "infrequent, high-value," for example), since raw cluster IDs alone aren't actionable for a business team.

**Q: You have a dataset with 50 numeric features and want to visually explore whether any natural groupings exist. How would you approach visualization given you can't plot 50 dimensions directly?**
> A: I'd apply PCA to compress the 50 features down to 2 (or occasionally 3) principal components, check `explained_variance_ratio_` to confirm those components capture a meaningful share of the original variance, then create a 2D scatter plot of the data in that compressed space — optionally coloring points by a clustering result (K-Means) or any known categorical variable, to visually assess whether groupings appear.

## "Gotcha" Questions

**Q: A colleague runs K-Means on unscaled data where one feature ranges 0-1 and another ranges 0-100,000, and gets clusters that seem to only reflect the second feature. What's happening?**
> A: K-Means uses Euclidean distance to assign points to clusters, and without scaling, the feature with the much larger numeric range dominates that distance calculation almost entirely — differences in the 0-1 feature become numerically negligible by comparison. The fix is to scale both features (e.g., with `StandardScaler`) before clustering, exactly as required for any other distance-based algorithm.

**Q: Why might two different runs of K-Means on the identical dataset (same k) produce slightly different clusters?**
> A: K-Means starts by placing initial centroids somewhat randomly, and the algorithm can converge to different local solutions depending on that starting point. `n_init` (running the algorithm multiple times with different random starts and keeping the best result by inertia) reduces this variability but random_state still affects the specific outcome — setting `random_state` explicitly makes results reproducible run to run.

## Quick-Fire Rapid Review

- Q: Does unsupervised learning use a target variable `y`? → **No — features only**
- Q: What must you always do before K-Means/PCA on numeric features? → **scale them**
- Q: Metric that always decreases as k increases in K-Means? → **inertia**
- Q: Metric for evaluating clustering without ground-truth labels? → **silhouette score**
- Q: Which clustering method lets you choose cluster count after seeing the full structure? → **hierarchical clustering (via the dendrogram)**
- Q: What does PCA's `explained_variance_ratio_` tell you? → **the fraction of total variance each component captures**
- Q: Are principal components the same as original features? → **No — they're weighted combinations of the originals**
- Q: Silhouette score range? → **-1 to +1 (higher is better)**
