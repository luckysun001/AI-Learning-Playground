# K-Means 聚类（Lloyd / k-means++）

## 输入
- X：样本矩阵，形状 (m, n)
- K：簇数
- max_iter：最大迭代次数

## 输出
- centroids：K 个质心
- labels：每个样本所属簇

## 伪代码
1. centroids = kmeans_plus_plus_init(X, K)     # 或随机选 K 个样本
2. FOR iter FROM 1 TO max_iter:
3.     # E 步：分配
4.     FOR EACH 样本 x_i:
5.         labels[i] = argmin_k ||x_i - centroids[k]||²
6.     # M 步：更新
7.     old_centroids = centroids
8.     FOR k FROM 1 TO K:
9.         centroids[k] = mean( x_i : labels[i] == k )   # 若簇为空则重初始化
10.    IF centroids == old_centroids: BREAK
11. RETURN centroids, labels

## k-means++ 初始化（选彼此远离的质心）
1. 随机选第一个质心
2. WHILE 质心数 < K:
3.     对每个样本计算到最近已选质心的距离 d²
4.     以 d² 为权重概率采样下一个质心

## 复杂度分析
- 时间复杂度：O(iter · m · K · n)
- 空间复杂度：O(m · n + K · n)

## 说明
目标函数 J = Σ Σ r_ik ||x_i - μ_k||²（惯性 / WCSS）。对初值与异常值敏感，建议多次运行取最优。
