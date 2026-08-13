# K 近邻（KNN, K-Nearest Neighbors）

## 1. 核心概念

KNN 是**最朴素的「基于实例」的学习器**：不做显式训练（lazy learning），预测时直接找训练集中离待预测样本最近的 $K$ 个邻居，**投票（分类）/ 平均（回归）** 得出结果。

「近朱者赤」——假设相似样本标签相近。它没有训练阶段，但预测阶段要计算距离，属于**非参数、惰性**模型。

## 2. 数学原理

**距离度量（最常见欧氏距离）：**

$$d(x,z) = \sqrt{\sum_{j=1}^{n}(x_j - z_j)^2}$$

也可用曼哈顿距离、余弦相似度等。

**预测：**
- 分类：$\hat{y} = \text{mode}\{y_{(1)},\dots,y_{(K)}\}$（可加权：近邻权重更大）
- 回归：$\hat{y} = \frac{1}{K}\sum_{i\in N_K} y_i$

**关键超参：**
- $K$：太小→对噪声敏感、过拟合；太大→边界模糊、欠拟合。
- 距离度量与特征尺度（必须标准化）。

## 3. 伪代码实现

- 📎 标准伪代码：[pseudocode/traditional-ml/knn.md](../../pseudocode/traditional-ml/knn.md)（惰性存储、距离度量、近邻选择、加权投票、KDTree 加速）
- 实战代码：scikit-learn `KNeighborsClassifier` / `KNeighborsRegressor`（本项目实战直接使用；从零实现思路见练习）。

## 4. 关键细节与调优

- **必须特征缩放**：距离对量纲极度敏感，标准化是前提。
- **预测慢、训练快**：每次预测都要遍历全训练集，大数据集用 `KDTree`/`BallTree`（`algorithm='auto'`）加速。
- **维度灾难**：高维空间下距离区分度骤降，KNN 在超高维上效果差，宜先降维（见 [pca.md](pca.md)）。
- **类别不平衡**：用距离加权（`weights='distance'`），避免多数类霸权。
- **适用**：中小数据集、决策边界复杂、需要可解释「相似样本」的场景。

## 5. 实战案例

- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：KNN 回归作为对比模型。
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：可作为分类基线之一。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 13 章（非参数方法）
- scikit-learn User Guide: Neighbors
