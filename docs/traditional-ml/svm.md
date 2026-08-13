# 支持向量机（SVM, Support Vector Machine）

## 1. 核心概念

SVM 的核心思想是：**找到一个最大化类别间隔（margin）的分割超平面**。离超平面最近的那几个样本点叫**支持向量**，它们决定了边界——这也是名字由来。

SVM 通过**核技巧（kernel trick）** 把数据映射到高维空间，从而把线性不可分问题变可分，是兼顾理论与效果的经典模型。

## 2. 数学原理

**硬间隔（线性可分）：** 决策面 $w^Tx + b = 0$，约束 $y_i(w^Tx_i+b)\ge 1$，最大化间隔等价于最小化 $\frac{1}{2}\|w\|^2$。

**软间隔（引入松弛变量 $\xi$ 与惩罚 $C$）：**

$$\min_{w,b,\xi} \frac{1}{2}\|w\|^2 + C\sum_{i=1}^{m}\xi_i$$

$C$ 越大越不容忍误分（易过拟合），$C$ 越小间隔越宽（易欠拟合）。

**核技巧：** 用核函数 $K(x_i,x_j)=\phi(x_i)^T\phi(x_j)$ 隐式计算高维内积，无需显式映射。常用：
- 线性核：$K(x,z)=x^Tz$
- 多项式核：$(x^Tz+1)^d$
- RBF/高斯核：$\exp(-\gamma\|x-z\|^2)$（最常用，$\gamma$ 控制影响半径）

**对偶问题（用拉格朗日乘子 $\alpha$ 求解）：** 预测仅依赖支持向量对应的 $\alpha_i>0$。

## 3. 伪代码实现

实战代码：scikit-learn `SVC` / `SVR`（核方法计算较重，本项目实战直接使用库实现）。

## 4. 关键细节与调优

- **必须特征缩放**：SVM 对量纲极度敏感，务必标准化。
- **核与超参**：默认 RBF；调 `C` 与 `gamma`（`gamma` 大→过拟合、小→欠拟合）。
- **训练成本高**：复杂度约 $O(m^2\sim m^3)$，大数据集慎用；可用 `LinearSVC` 处理大规模线性问题。
- **多分类**：scikit-learn 默认 OvO（一对一）。
- **适用**：中小样本、特征维度高（甚至维度 > 样本数）时表现优秀；不擅长超大样本。

## 5. 实战案例

- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：SVR 作为回归对比模型之一。
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：可作为分类基线。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 12 章
- 李航《统计学习方法》第 7 章
