# K-Means 聚类

## 1. 核心概念

K-Means 是最经典的**无监督**聚类算法：把 $m$ 个样本划分成 $K$ 个簇，使**簇内样本尽量相近、簇间尽量远离**。它寻找的是让「样本到所属簇中心距离平方和（SSE / 惯性）」最小的划分。

属于**原型聚类**：每个簇用一个质心（centroid）代表。

## 2. 数学原理

**目标函数（惯性 / WCSS）：**

$$J = \sum_{i=1}^{m}\sum_{k=1}^{K} r_{ik}\|x_i - \mu_k\|^2, \quad r_{ik}=\begin{cases}1 & x_i\in \text{簇}k\\0 & \text{否则}\end{cases}$$

**Lloyd 算法（EM 思想的两步迭代）：**
1. **初始化** $K$ 个质心（常用 k-means++，避免糟糕的初始点）；
2. **E 步（分配）**：每个样本归入最近的质心；
3. **M 步（更新）**：质心移向本簇样本均值；
4. 重复 2-3 直到质心不再变化 / 达到最大迭代。

**确定 $K$：** 肘部法（SSE 随 $K$ 下降的拐点）、轮廓系数（Silhouette）。

## 3. 伪代码实现

参见 [`pseudocode/traditional-ml/kmeans.md`](../../pseudocode/traditional-ml/kmeans.md)。

实战代码：[`code/01-traditional-ml/kmeans_scratch.py`](../../code/01-traditional-ml/kmeans_scratch.py)（从零实现 + PCA 可视化）。

## 4. 关键细节与调优

- **必须特征缩放**：基于距离，量纲影响巨大。
- **K-Means++ 初始化**：显著优于随机初始化，scikit-learn 默认即用。
- **对初值敏感 / 可能局部最优**：多次运行取最优（`n_init`）。
- **假设簇呈球形、等方差**：对非凸形状、密度不均的数据效果差（可用 DBSCAN / GMM）。
- **异常值敏感**：质心易被离群点拉偏。
- **高维先用 PCA**：降维后聚类更稳、可视化更易（见 [pca.md](pca.md)、[case3](../../code/01-traditional-ml/case3_clustering_pca.py)）。

## 5. 实战案例

- [`kmeans_scratch.py`](../../code/01-traditional-ml/kmeans_scratch.py)：从零实现 + sklearn 对比 + PCA 二维可视化。
- [`case3_clustering_pca.py`](../../code/01-traditional-ml/case3_clustering_pca.py)：用户画像聚类（K-Means + PCA）。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 14 章
- Arthur & Vassilvitskii (2007) *k-means++*
