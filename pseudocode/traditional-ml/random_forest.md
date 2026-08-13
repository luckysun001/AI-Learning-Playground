# 随机森林（Random Forest / Bagging）

## 输入
- D：训练集
- T：树的数量
- max_features：每节点候选特征数（分类常取 √n）

## 输出
- 森林（T 棵决策树）

## 伪代码
1. forest = []
2. FOR t FROM 1 TO T:
3.     D_boot = BootstrapSample(D)          # 有放回抽 m 个
4.     tree_t = BuildTree(D_boot,
5.                        candidate_features = RandomSubset(全部特征, max_features))
6.     forest.append(tree_t)
7. 预测（分类）:
8.     votes = [tree_t.predict(x) FOR tree_t IN forest]
9.     ŷ = 多数投票(mode(votes))
10. 预测（回归）:
11.    ŷ = mean(tree_t.predict(x) FOR tree_t IN forest)
12. RETURN forest

## 复杂度分析
- 训练：O(T · m · n · log m)，可并行
- 预测：O(T · 树深度)

## 说明
双重随机（样本 bootstrap + 特征子集）降低树间相关性，显著降低方差。
袋外样本（OOB）可免费估计泛化误差。
