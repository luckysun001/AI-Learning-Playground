# 线性回归（梯度下降法 / Gradient Descent）

## 输入
- X：特征矩阵，形状 (m, n)，已含偏置列或另行处理
- y：标签向量，形状 (m,)
- α：学习率（如 0.01）
- iterations：迭代次数（如 1000）

## 输出
- θ：拟合参数，形状 (n,)

## 伪代码
1. 初始化 θ 为全零（或小随机）向量
2. 归一化特征 X（Z-score 或 Min-Max）
3. FOR i FROM 1 TO iterations:
4.     y_pred = X · θ
5.     error = y_pred - y
6.     gradient = (Xᵀ · error) / m
7.     θ = θ - α · gradient
8.     loss = (1/(2m)) · Σ(error²)
9. RETURN θ

## 复杂度分析
- 时间复杂度：O(iterations · m · n)
- 空间复杂度：O(m · n)

## 闭式解（对照）
θ = (XᵀX)⁻¹ Xᵀy
- 时间复杂度：O(n³)（矩阵求逆），适合 n 不大时
