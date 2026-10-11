"""
案例3：用户画像聚类（K-Means + PCA 可视化）
-------------------------------------------
背景：无标签用户行为数据，先用 PCA 降维去噪，再 K-Means 聚成若干画像，
      最后在 2D 平面可视化。对应文档：docs/traditional-ml/kmeans.md, pca.md。

运行：python case3_clustering_pca.py
依赖：numpy, scikit-learn, matplotlib
说明：可视化图保存到仓库根目录的 assets/user_clusters_pca.png
      （输出路径按脚本所在位置计算，因此从任意目录运行都写到同一位置）
"""

from pathlib import Path

# 输出目录 = 仓库根目录/assets，与运行脚本时的当前目录无关
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def main():
    # 合成「用户行为」高维数据（10 维，3 类画像）
    X, _ = make_blobs(
        n_samples=1200, n_features=10, centers=3, cluster_std=1.5, random_state=42
    )
    X = StandardScaler().fit_transform(X)

    # 用肘部法粗略选 K
    print("【案例3 · 用户画像聚类】")
    for k in range(2, 6):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        print(
            f"  K={k}  惯性(Inertia)={km.inertia_:.1f}  "
            f"轮廓系数={silhouette_score(X, km.labels_):.3f}"
        )

    # 选定 K=3
    km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)

    # PCA 降到 2 维做可视化
    X2 = PCA(n_components=2).fit_transform(X)
    plt.figure(figsize=(6, 5))
    plt.scatter(X2[:, 0], X2[:, 1], c=km.labels_, cmap="tab10", s=12)
    plt.scatter(
        km.cluster_centers_[:, 0],
        km.cluster_centers_[:, 1],
        c="red",
        marker="X",
        s=200,
        edgecolors="k",
        label="centers",
    )
    plt.title("User Personas: K-Means (PCA 2D)")
    plt.legend()
    plt.tight_layout()
    out_path = ASSETS_DIR / "user_clusters_pca.png"
    plt.savefig(out_path, dpi=120)
    print(f"  聚类完成，可视化已保存: assets/{out_path.name}")


if __name__ == "__main__":
    main()
