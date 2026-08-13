# 知识点名称（示例：线性回归）

> 复制本模板到对应模块目录，按六段结构撰写。文件名用 kebab-case，例如 `linear_regression.md`。

## 1. 核心概念

（用 2-4 段自然语言讲清「它解决什么问题、核心思想是什么」，可配一张 ASCII / 文字示意图。避免一上来就堆公式。）

## 2. 数学原理

（公式推导、关键定理、假设条件。用 Markdown 数学公式 `$...$` / `$$...$$`。）

例如：

$$
\hat{y} = X\theta
$$

$$
\theta = (X^TX)^{-1}X^Ty \quad \text{(解析解 / 正规方程)}
$$

## 3. 伪代码实现

（给一段标准化伪代码，语言无关、可读性优先。同时链接到 `pseudocode/<模块>/` 下对应的独立伪代码文件。）

参见 [`pseudocode/traditional-ml/linear_regression.md`](../../pseudocode/traditional-ml/linear_regression.md)。

## 4. 关键细节与调优

（工程经验、常见坑、超参选择、数值稳定性等。这是区别于教科书、最有价值的一节。）

- 特征需归一化，否则梯度下降收敛慢；
- 学习率过大易震荡、过小收敛慢；
- ……

## 5. 实战案例

（链接到 `code/<NN-模块>/` 下的可运行脚本，并简述案例背景与预期输出。）

- [`linear_regression_gd.py`](../../code/01-traditional-ml/linear_regression_gd.py)：从零实现 + 与 sklearn 对比。

## 6. 扩展阅读

（论文、经典博客、官方文档等，附链接与一句话推荐理由。）

- 《The Elements of Statistical Learning》第 3 章
- scikit-learn 官方 User Guide: Linear Models
