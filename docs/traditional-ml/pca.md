# 主成分分析（PCA, Principal Component Analysis）

## 1. 核心概念

PCA 是最常用的**无监督降维**方法：在尽量保留数据方差（信息）的前提下，把高维数据投影到低维空间。新坐标轴（主成分）彼此**正交**，且按「能解释的方差大小」排序。

它既能**降维去噪**、**可视化高维数据**，也是聚类/分类前的标准预处理。

## 2. 数学原理

**核心**：寻找投影方向 $w$（单位向量），使投影后方差最大。

$$\max_w \; w^T\Sigma w \quad \text{s.t. } \|w\|=1$$

其中 $\Sigma$ 是数据的协方差矩阵。最优解正是 $\Sigma$ 的**特征向量**，对应特征值即该方向解释的方差。

**算法步骤：**
1. 中心化数据：$X \leftarrow X - \bar{x}$；
2. 计算协方差矩阵 $\Sigma = \frac{1}{m}X^TX$；
3. 对 $\Sigma$ 做特征值分解，取前 $k$ 大特征值对应的特征向量 $W_k$；
4. 降维表示：$Z = XW_k$（形状 $m\times k$）。

**选择 $k$：** 按「保留方差比例」$\frac{\sum_{i=1}^{k}\lambda_i}{\sum_{j}\lambda_j} \ge 0.95$ 等阈值。

## 3. 伪代码实现

实战代码：scikit-learn `PCA`（本项目实战直接使用；从零实现思路见练习）。

## 4. 关键细节与调优

- **必须标准化**：PCA 基于方差，量纲大的特征会 dominate，先 Z-score 标准化。
- **线性方法**：只能捕获线性相关性，非线性结构用 Kernel PCA / t-SNE / UMAP。
- **主成分不可解释**：是原始特征的线性组合，失去业务语义（代价换来的压缩）。
- **降维≠去标签**：PCA 不看标签，可能把区分信息也压掉——分类前降维需谨慎。
- **典型用途**：可视化（降到 2/3 维）、去噪、加速后续模型、缓解维度灾难。

## 5. 实战案例

- [`case3_clustering_pca.py`](../../code/01-traditional-ml/case3_clustering_pca.py)：先 PCA 降维再 K-Means 聚类并可视化。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 14 章
- Jolliffe (2002) *Principal Component Analysis*
