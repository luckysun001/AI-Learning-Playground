"""
K-Means 聚类：从零实现（k-means++ 初始化）+ 与 sklearn 对比 + PCA 可视化
------------------------------------------------------------------------
背景：无监督聚类。把样本分成 K 个簇，使簇内紧凑、簇间分离。

运行：python kmeans_scratch.py
依赖：numpy, scikit-learn, matplotlib
说明：可视化图保存为 ../../assets/kmeans_pca.png（如无法显示则用 Agg 后端）
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# 无界面环境也能跑
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def kmeans_plus_plus_init(X, k, rng):
    n = X.shape[0]
    centers = [X[rng.integers(n)]]
    for _ in range(1, k):
        dist2 = np.min(
            [np.sum((X - c) ** 2, axis=1) for c in centers], axis=0
        )
        probs = dist2 / dist2.sum()
        idx = rng.choice(n, p=probs)
        centers.append(X[idx])
    return np.array(centers)


def kmeans_scratch(X, k, max_iter=100, seed=42):
    rng = np.random.default_rng(seed)
    centroids = kmeans_plus_plus_init(X, k, rng)
    labels = np.zeros(X.shape[0], dtype=int)
    for _ in range(max_iter):
        # E 步
        dists = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        new_labels = dists.argmin(axis=1)
        # M 步
        new_centroids = centroids.copy()
        for j in range(k):
            if np.sum(new_labels == j) > 0:
                new_centroids[j] = X[new_labels == j].mean(axis=0)
        if np.allclose(new_centroids, centroids):
            break
        centroids, labels = new_centroids, new_labels
    return centroids, labels


def main():
    X, y_true = make_blobs(
        n_samples=1000, n_features=8, centers=4, random_state=42
    )

    # 从零实现
    centroids, labels = kmeans_scratch(X, k=4)

    # sklearn 对比
    km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X)
    sk_labels = km.labels_

    print("【K-Means · 从零实现 vs sklearn】")
    print("  从零实现  轮廓系数=%.4f" % silhouette_score(X, labels))
    print("  sklearn   轮廓系数=%.4f" % silhouette_score(X, sk_labels))

    # PCA 降到 2 维并可视化
    X2 = PCA(n_components=2).fit_transform(X)
    plt.figure(figsize=(6, 5))
    plt.scatter(X2[:, 0], X2[:, 1], c=labels, cmap="viridis", s=12)
    plt.scatter(centroids[:, 0], centroids[:, 1], c="red", marker="X",
                s=200, edgecolors="k", label="centroids")
    plt.title("K-Means Clustering (PCA 2D projection)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("../../assets/kmeans_pca.png", dpi=120)
    print("  可视化已保存: ../../assets/kmeans_pca.png")


if __name__ == "__main__":
    main()
