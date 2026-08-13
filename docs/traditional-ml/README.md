# 传统机器学习（Traditional ML）

> 状态：✅ 已完成（原理文档 + 伪代码 + 实战代码齐备）

传统机器学习是深度学习和大模型的地基。它用**显式设计的特征 + 可解释性强的模型**解决预测问题，训练成本低、可解释性好，至今仍是工业界的主力。

## 本模块覆盖

| 类别 | 知识点 | 文档 |
|---|---|---|
| 监督·回归 | 线性回归 | [linear_regression.md](linear_regression.md) |
| 监督·分类 | 逻辑回归 | [logistic_regression.md](logistic_regression.md) |
| 监督·分类 | 决策树 | [decision_tree.md](decision_tree.md) |
| 集成 | 随机森林 | [random_forest.md](random_forest.md) |
| 监督·分类 | SVM | [svm.md](svm.md) |
| 监督·分类 | KNN | [knn.md](knn.md) |
| 监督·分类 | 朴素贝叶斯 | [naive_bayes.md](naive_bayes.md) |
| 无监督 | K-Means 聚类 | [kmeans.md](kmeans.md) |
| 降维 | PCA | [pca.md](pca.md) |
| 评估 | 模型评估 | [model_evaluation.md](model_evaluation.md) |
| 工程 | 特征工程 | [feature_engineering.md](feature_engineering.md) |

## 学习建议

1. 先建立「监督 vs 无监督」「回归 vs 分类」的全局认知；
2. 线性回归是几乎所有模型的原型——吃透它的闭式解与梯度下降；
3. 决策树 → 随机森林 是一条理解「集成学习」最自然的路径；
4. 每个算法都建议：读本文档 → 看 [`pseudocode/traditional-ml/`](../../pseudocode/traditional-ml/) 伪代码 → 跑 [`code/01-traditional-ml/`](../../code/01-traditional-ml/) 实战。

## 实战案例索引

| 案例 | 脚本 | 要点 |
|---|---|---|
| 房价回归对比 | [case1_regression_comparison.py](../../code/01-traditional-ml/case1_regression_comparison.py) | LR / DT / RF / KNN / SVM 同台对比 |
| 客户流失预测 | [case2_churn_prediction.py](../../code/01-traditional-ml/case2_churn_prediction.py) | 特征工程 + 逻辑回归 + 评估 |
| 用户聚类可视化 | [case3_clustering_pca.py](../../code/01-traditional-ml/case3_clustering_pca.py) | K-Means + PCA 二维可视化 |
| 信贷评分卡 | [case4_credit_scoring.py](../../code/01-traditional-ml/case4_credit_scoring.py) | 逻辑回归 + WOE 编码思路 |
