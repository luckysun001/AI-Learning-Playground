# 决策树（Decision Tree）

## 1. 核心概念

决策树通过一系列**if-then 规则**对样本做划分，形似一棵倒长的树：内部节点是「对某个特征的判断」，分支是判断结果，叶节点是预测值（分类的类别 / 回归的数值）。

它**无需特征缩放**、能捕捉非线性、天然可解释（可以直接把规则念给人听）。代表算法：ID3、C4.5、CART（最常用，scikit-learn 即采用）。

## 2. 数学原理

核心是**如何选分裂特征**——目标是让分裂后「纯度」最高（不确定性最低）。

**基尼不纯度（CART 分类默认）：**

$$Gini = 1 - \sum_{k=1}^{K} p_k^2$$

$p_k$ 为节点中第 $k$ 类样本占比。Gini 越小越纯（全同类时为 0）。

**信息熵（ID3/C4.5）：**

$$Entropy = -\sum_{k=1}^{K} p_k \log_2 p_k$$

**信息增益：** $\text{Gain} = Entropy(\text{父}) - \sum \frac{|D_v|}{|D|}Entropy(D_v)$

分裂时选使加权不纯度下降最大的特征。

**回归树：** 用「方差」代替不纯度，叶节点取区域内样本均值。

**剪枝：** 预剪枝（限制深度 `max_depth`、最小样本数 `min_samples_leaf`）+ 后剪枝（CCP），防止过拟合。

## 3. 伪代码实现

参见 [`pseudocode/traditional-ml/decision_tree.md`](../../pseudocode/traditional-ml/decision_tree.md)。

实战代码：[`code/01-traditional-ml/decision_tree_scratch.py`](../../code/01-traditional-ml/decision_tree_scratch.py)（从零 CART 分类）。

## 4. 关键细节与调优

- **单棵树极易过拟合**：深度不设限会记住训练集，所以实践中很少单独用，多作为集成（随机森林 / GBDT）的基学习器。
- **对特征尺度不敏感**：无需标准化。
- **对数据微小变动敏感**：训练集稍变，树结构可能大变——这是用集成来稳定它的动机。
- **类别特征**：scikit-learn 的 `DecisionTreeClassifier` 不直接支持类别型，需先编码（见 [feature_engineering.md](feature_engineering.md)）。
- **关键超参**：`max_depth`、`min_samples_split`、`min_samples_leaf`、`criterion`（gini/entropy）。

## 5. 实战案例

- [`decision_tree_scratch.py`](../../code/01-traditional-ml/decision_tree_scratch.py)：从零实现 CART 分类树并可视化规则。
- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：作为对比模型之一。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 9 章
- 李航《统计学习方法》第 5 章
