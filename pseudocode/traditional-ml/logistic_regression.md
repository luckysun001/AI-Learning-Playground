# 逻辑回归（Logistic Regression）

## 输入
- X：特征矩阵，形状 (m, n)
- y：标签向量，取值 {0, 1}，形状 (m,)
- α：学习率
- iterations：迭代次数

## 输出
- θ：拟合参数，形状 (n,)
- 预测时输出概率 ŷ = σ(Xθ)

## 伪代码
1. 初始化 θ 为全零向量
2. 归一化特征 X
3. FOR i FROM 1 TO iterations:
4.     z = X · θ
5.     ŷ = sigmoid(z) = 1 / (1 + e⁻ᶻ)
6.     error = ŷ - y
7.     gradient = (Xᵀ · error) / m
8.     θ = θ - α · gradient
9.     loss = -(1/m) Σ [ y·log ŷ + (1-y)·log(1-ŷ) ]
10. 预测: IF σ(Xθ) ≥ 0.5 THEN 正类 ELSE 负类
11. RETURN θ

## 复杂度分析
- 时间复杂度：O(iterations · m · n)
- 空间复杂度：O(m · n)

## 说明
梯度形式与线性回归一致（因 sigmoid 导数特性），但损失为交叉熵（凸）。
