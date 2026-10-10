# 朴素贝叶斯（Naive Bayes）

## 1. 核心概念

朴素贝叶斯是基于**贝叶斯定理**与**特征条件独立假设**的分类器。尽管「特征相互独立」在现实里几乎不成立（这正是「朴素」之处），它依然在文本分类、垃圾邮件识别等任务上表现稳健，且**训练极快、数据需求小**。

核心公式：

$$P(y|x_1,\dots,x_n) = \frac{P(y)\prod_{i=1}^{n}P(x_i|y)}{P(x)}$$

预测时取后验概率最大的类别。

## 2. 数学原理

**贝叶斯定理：** $P(y|X)=\frac{P(X|y)P(y)}{P(X)}$

在条件独立假设下：$P(X|y)=\prod_i P(x_i|y)$。

**常用变体：**
- **高斯朴素贝叶斯**：连续特征假设服从高斯分布，$P(x_i|y)=\mathcal{N}(\mu_{y,i},\sigma_{y,i}^2)$。
- **多项式朴素贝叶斯**：特征为计数（如词频），适合文本。
- **伯努利朴素贝叶斯**：二值特征（出现/不出现）。

**平滑（Laplace）：** 用 $\frac{count + \alpha}{total + \alpha\cdot V}$ 避免零概率（未见词导致整句概率为 0）。

## 3. 伪代码实现

- 📎 标准伪代码：[pseudocode/traditional-ml/naive_bayes.md](../../pseudocode/traditional-ml/naive_bayes.md)（高斯/多项式/伯努利三变体、Laplace 平滑、对数概率防下溢）
- 实战代码：scikit-learn `GaussianNB` / `MultinomialNB`（本项目实战直接使用）。

## 4. 关键细节与调优

- **不需要特征缩放**：基于概率分布，对量纲不敏感。
- **训练/预测都极快**：只统计频次，适合海量高维稀疏数据（文本）。
- **独立假设很硬**：特征强相关时会低估不确定性，但实践常「错得有用」。
- **数值稳定性**：实际用对数概率相加，避免连乘下溢。
- **适用**：文本分类（ spam、情感）、多分类基线；不适合特征高度相关的稠密数据。

## 5. 实战案例

- 文本分类常作为基线；本项目传统 ML 模块未单独列脚本，可与 [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py) 的类别型特征结合尝试。

## 6. 扩展阅读

- 《The Elements of Statistical Learning》第 6 章
- 吴恩达 NLP / 生成模型讲义
