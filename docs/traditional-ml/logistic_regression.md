# 逻辑回归（Logistic Regression）

## 1. 核心概念

逻辑回归解决**二分类问题**（名字带「回归」却是分类模型）。它在线性回归的输出上套一个 **Sigmoid 函数**，把任意实数压缩到 $(0,1)$，解释为「属于正类的概率」：

$$\hat{y} = \sigma(X\theta) = \frac{1}{1 + e^{-X\theta}}$$

若 $\hat{y} \ge 0.5$ 判为正类，否则负类。它输出的是**概率**，可解释性极强，是工业界风控、点击率预估的常青模型。

## 2. 数学原理

**Sigmoid：** $\sigma(z) = \frac{1}{1+e^{-z}}$，性质 $\sigma'(z)=\sigma(z)(1-\sigma(z))$。

**损失函数（对数损失 / 交叉熵）：**

$$J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}\big[y^{(i)}\log\hat{y}^{(i)} + (1-y^{(i)})\log(1-\hat{y}^{(i)})\big]$$

该损失是**凸函数**，保证梯度下降能收敛到全局最优。

**梯度：** 形式与线性回归惊人地一致：

$$\frac{\partial J}{\partial \theta_j} = \frac{1}{m}\sum_{i=1}^{m}(\hat{y}^{(i)} - y^{(i)})x_j^{(i)}$$

**多分类扩展（Softmax / 一对多）：** 多类时用 Softmax 回归或训练 $K$ 个二分类器（OvR）。

**正则化：** 同线性回归，用 L2（默认）抑制过拟合、提升泛化。

## 3. 伪代码实现

参见 [`pseudocode/traditional-ml/logistic_regression.md`](../../pseudocode/traditional-ml/logistic_regression.md)。

实战代码：[`code/01-traditional-ml/logistic_regression_gd.py`](../../code/01-traditional-ml/logistic_regression_gd.py)。

## 4. 关键细节与调优

- **必须特征缩放**：同线性回归，梯度下降前标准化。
- **决策边界是线性的**：只能分线性可分数据；非线性要靠特征交叉或核方法。
- **类别不平衡**：用 `class_weight='balanced'` 或上/下采样，否则模型会偏向多数类。
- **阈值可调**：默认 0.5，风控场景常调高（宁错杀）或调低（宁放过），依业务代价而定。
- **评估**：Accuracy、Precision、Recall、F1、AUC-ROC（见 [model_evaluation.md](model_evaluation.md)）。

## 5. 实战案例

- [`logistic_regression_gd.py`](../../code/01-traditional-ml/logistic_regression_gd.py)：从零实现 + 与 `sklearn.LogisticRegression` 对比。
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：客户流失二分类（逻辑回归 + 特征工程）。
- [`case4_credit_scoring.py`](../../code/01-traditional-ml/case4_credit_scoring.py)：信贷评分卡。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 4 章
- scikit-learn User Guide: Logistic Regression
