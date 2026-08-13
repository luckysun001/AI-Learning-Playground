# 朴素贝叶斯（Naive Bayes）

> 基于贝叶斯定理 + 特征条件独立假设的分类器。训练极快、数据需求小，在文本/高维稀疏任务上稳健。
> 详见文档：[docs/traditional-ml/naive_bayes.md](../traditional-ml/naive_bayes.md)

## 输入
- X_train：训练特征矩阵，形状 (m, n)
- y_train：训练标签，形状 (m,)，取值 {1..C}
- X_query：待预测样本特征，形状 (q, n)
- α：平滑系数（Laplace，默认 1，避免零概率）
- variant：`gaussian` | `multinomial` | `bernoulli`
- ε：数值稳定常数（如 1e-9，防 ln(0) 或 σ=0）

## 输出
- y_pred：预测类别，形状 (q,)

## 训练阶段（统计充分统计量）
1. **类别先验**：FOR c = 1..C：
   - `P(c) = (count(y=c) + α) / (m + α·C)`
2. **依 variant 估计类条件概率参数**：
   - **高斯**：FOR c, j：
     - `μ[c][j] = mean(X[y=c, j])`
     - `σ²[c][j] = var(X[y=c, j]) + ε`
   - **多项式**（计数 / 词频）：FOR c, j：
     - `θ[c][j] = ( Σ_{i: y_i=c} X[i][j] + α ) / ( Σ_{i: y_i=c} Σ_j X[i][j] + α·V )`
     - 其中 V = 特征数（词表大小）
   - **伯努利**（二值 0/1）：FOR c, j：
     - `θ[c][j] = ( count(X[y=c, j] > 0) + α ) / ( count(y=c) + 2α )`
3. **保存** P(c) 与各 variant 参数供预测使用

## 预测阶段（对数后验，防下溢）
FOR 每个查询样本 x：
1. FOR c = 1..C：
   - `log_posterior[c] = ln P(c)`
   - FOR j = 1..n：
     - 计算类条件概率 `p = P(x_j | c)`（依 variant）：
       - 高斯：`p = (1/√(2πσ²[c][j])) · exp(-(x_j - μ[c][j])² / (2σ²[c][j]))`
       - 多项式：`p = θ[c][j]`
       - 伯努利：`p = (x_j > 0) ? θ[c][j] : (1 - θ[c][j])`
     - `log_posterior[c] += ln(p + ε)`  ← 连乘转为对数连加，避免浮点下溢
2. `y_pred = argmax_c( log_posterior[c] )`

## 子算法：高斯概率密度
- `N(x; μ, σ²) = (1 / √(2πσ²)) · exp( - (x - μ)² / (2σ²) )`
- ε 防止 σ=0 或 p=0 时 `ln(0) = -∞` 污染整句后验

## 复杂度分析
- 训练：O(m·n)（一次遍历统计）
- 预测：O(q · C · n)
- 空间：O(C·n)

## 关键细节
- 「朴素」来自特征条件独立假设；特征强相关时仍常「错得有用」
- Laplace 平滑 α>0 防止未见特征使整句概率塌为 0
- 用**对数概率相加**替代概率连乘，避免下溢
- 无需特征缩放；适合高维稀疏文本（垃圾邮件、情感）
- 多分类直接可用；无需 One-vs-Rest 包装
