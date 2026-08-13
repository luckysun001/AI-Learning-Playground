# 线性回归（Linear Regression）

## 1. 核心概念

线性回归解决**回归问题**：给定特征 $X$，预测一个连续的数值 $y$。它假设 $y$ 与 $X$ 各特征之间是**线性关系**：

$$\hat{y} = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \dots + \theta_n x_n = X\theta$$

其中 $\theta_0$ 是截距（偏置），$\theta_{1..n}$ 是各特征的权重。学习的目标就是找到一组 $\theta$，使预测值 $\hat{y}$ 尽可能接近真实 $y$。

它是几乎所有机器学习模型的「原型」：梯度下降、损失函数、正则化等概念都能在它身上以最简单的形式呈现。

## 2. 数学原理

**损失函数（MSE，均方误差）：**

$$J(\theta) = \frac{1}{2m}\sum_{i=1}^{m}(\hat{y}^{(i)} - y^{(i)})^2$$

**闭式解（正规方程）：**

$$\theta = (X^TX)^{-1}X^Ty$$

优点：一步到位、无需调学习率。缺点：求逆复杂度 $O(n^3)$，特征数 $n$ 很大时不实用，且 $X^TX$ 可能不可逆（多重共线性）。

**梯度下降更新：** 对每个参数

$$\frac{\partial J}{\partial \theta_j} = \frac{1}{m}\sum_{i=1}^{m}(\hat{y}^{(i)} - y^{(i)})x_j^{(i)}$$

$$\theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j}$$

**正则化（防止过拟合）：**
- Ridge（L2）：$J += \lambda\sum\theta_j^2$
- Lasso（L1）：$J += \lambda\sum|\theta_j|$，可做特征选择

## 3. 伪代码实现

参见 [`pseudocode/traditional-ml/linear_regression.md`](../../pseudocode/traditional-ml/linear_regression.md)。

实战代码：[`code/01-traditional-ml/linear_regression_gd.py`](../../code/01-traditional-ml/linear_regression_gd.py)。

## 4. 关键细节与调优

- **必须特征缩放**：梯度下降对量纲极敏感，先对 $X$ 做标准化（Z-score）或归一化（Min-Max），否则收敛极慢甚至不收敛。
- **学习率 $\alpha$**：过大→损失震荡/发散；过小→收敛慢。常用 0.01~0.1，可配合学习率调度。
- **闭式解 vs 梯度下降**：特征 < 1e4 用闭式解更稳；特征极多或数据流式到达用梯度下降（含 SGD / Mini-batch）。
- **多重共线性**：特征间高度相关会让 $X^TX$ 接近奇异，权重估计不稳定——用 Ridge 缓解。
- **评估**：回归用 MSE / RMSE / MAE / $R^2$。

## 5. 实战案例

- [`linear_regression_gd.py`](../../code/01-traditional-ml/linear_regression_gd.py)：从零梯度下降实现，并与 `sklearn.LinearRegression` 对比 MSE。
- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：多算法回归对比（含线性回归）。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 3 章
- 吴恩达 Coursera Machine Learning Week 1-2
- scikit-learn User Guide: Linear Models
