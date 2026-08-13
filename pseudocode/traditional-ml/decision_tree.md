# 决策树（CART 分类，递归二分）

## 输入
- D：训练集，含特征 X 与标签 y
- 停止条件：max_depth、min_samples_split、min_samples_leaf

## 输出
- 一棵决策树（递归结构）

## 伪代码
1. FUNCTION BuildTree(D, depth):
2.     IF 停止条件满足（纯节点 / 达最大深度 / 样本过少）:
3.         RETURN 叶节点（多数类）
4.     best_split = NONE; best_gain = -∞
5.     FOR EACH 特征 j IN 候选特征:
6.         FOR EACH 候选切分点 v:
7.             按 X_j ≤ v 将 D 分为 D_left, D_right
8.             gain = Gini(D) - (|D_left|/|D|)·Gini(D_left) - (|D_right|/|D|)·Gini(D_right)
9.             IF gain > best_gain:
10.                best_gain = gain; best_split = (j, v)
11.     IF best_gain ≤ 0: RETURN 叶节点（多数类）
12.     (D_left, D_right) = 按 best_split 划分 D
13.     node = 内部节点(feature=best_split.j, threshold=best_split.v)
14.     node.left = BuildTree(D_left, depth+1)
15.     node.right = BuildTree(D_right, depth+1)
16.     RETURN node
17. 调用 BuildTree(D, 0) 得到根节点

## 复杂度分析
- 单棵树训练：O(m · n · log m)（每节点扫描特征与切分点）
- 预测：O(树深度) ≈ O(log m)

## 说明
分类默认用 Gini；回归树把 Gini 换成方差、叶节点取均值。
