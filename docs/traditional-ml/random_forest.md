# 随机森林（Random Forest）

## 1. 核心概念

随机森林是 **Bagging（ bootstrap aggregating）** 集成学习的代表：训练许多棵**决策树**，每棵在不同自助采样（bootstrap）的子集上、且每次分裂只考虑随机子集的特征，最后**投票（分类）/ 平均（回归）** 汇总。

它的威力来自两点：**样本扰动 + 特征扰动**双重随机性，让树之间弱相关，从而大幅降低方差、抑制过拟合，是开箱即用、鲁棒性极强的「基线之王」。

## 2. 数学原理

**自助采样（Bootstrap）：** 从 $m$ 个样本中有放回抽 $m$ 个，约 63.2% 样本被抽到（其余作袋外 OOB 评估）。

**特征子集：** 分裂节点时，从全部 $n$ 个特征中随机取 $\sqrt{n}$（分类）或 $n/3$（回归）个候选。

**聚合：**
- 分类：$\hat{y} = \text{mode}\{h_1(x), \dots, h_T(x)\}$
- 回归：$\hat{y} = \frac{1}{T}\sum_{t=1}^{T} h_t(x)$

**OOB 误差：** 用未被第 $t$ 棵树抽到的样本评估该树，整体平均即近似泛化误差，免费获得验证集。

## 3. 伪代码实现

参见 [`pseudocode/traditional-ml/random_forest.md`](../../pseudocode/traditional-ml/random_forest.md)。

实战代码：scikit-learn `RandomForestClassifier` / `RandomForestRegressor`（本项目实战案例直接使用）。

## 4. 关键细节与调优

- **树越多越稳**：`n_estimators` 增大方差持续下降，到一定数量后收益递减；现代实现可并行。
- **`max_features` 是方差-偏差旋钮**：调小→树更独立→方差更低（但偏差略升）。
- **调参顺序**：先定足够多的树，再调 `max_depth`/`min_samples_leaf` 控制单树复杂度，最后调 `max_features`。
- **特征重要性**：`feature_importances_` 基于不纯度下降，可快速做特征筛选（但高基数特征易被高估）。
- **局限**：高维稀疏数据（如文本）表现一般，回归外推能力差（预测值不超过训练标签范围）。

## 5. 实战案例

- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：随机森林作为回归对比模型。
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：与客户流失预测基线对比。

## 6. 扩展阅读

- Breiman (2001) *Random Forests*, Machine Learning
- 《The Elements of Statistical Learning》第 15 章
