# 特征工程（Feature Engineering）

## 1. 核心概念

「数据和特征决定了机器学习的上限，模型和算法只是去逼近这个上限。」特征工程就是把原始数据**转化为模型更易学习的形式**：处理缺失、编码类别、缩放数值、构造新特征、筛选重要特征。

它往往比选模型更影响最终效果，也是工业界最耗时的环节。

## 2. 核心方法

**缺失值处理：**
- 删除（缺失比例过高且非关键信息）；
- 数值填充（均值/中位数）、类别填充（众数/`'missing'` 单独成类）；
- 复杂场景用模型预测填充。

**特征编码（类别 → 数值）：**
- **One-Hot**：无序类别，避免模型误判大小关系（维度爆炸需用稀疏/`drop_first`）；
- **Label / Ordinal**：有序类别（如学历）；
- **WOE（证据权重）**：风控评分卡专用，把类别映射为对「好坏比」的对数变换，兼具单调性与可解释性；
- **目标编码**：用目标均值编码（需防泄漏，配合交叉验证）。

**特征缩放（数值）：**
- **标准化 Z-score**：$(x-\mu)/\sigma$，适合 SVM / 梯度下降 / PCA；
- **归一化 Min-Max**：缩到 $[0,1]$，适合边界敏感的模型；
- **Robust Scaling**：用分位数，抗离群值。

**特征构造与选择：**
- 构造：日期拆年/月/星期、占比、交叉特征、多项式特征；
- 选择：方差阈值、卡方检验、`RFE`、基于树模型的重要性、L1 正则。

## 3. 关键细节与调优

- **防数据泄漏（Leakage）**：用训练集的统计量（均值/最大最小）去拟合测试集，会虚高效果。正确做法：`Pipeline` + 在训练折内 fit。
- **One-Hot 后勿再标准化**（已是 0/1）；树模型可不吃缩放。
- **高基数类别**（如城市）直接 One-Hot 会维度爆炸，改用目标编码/WOE/嵌入。
- **用 Pipeline 串起预处理+模型**：保证 CV 与上线一致性。
- **WOE 要求单调性**：评分卡希望特征对好坏的边际效应单调，否则需分箱（binning）调整。

## 4. 实战案例

- 📎 标准伪代码：[pseudocode/traditional-ml/feature_engineering.md](../../pseudocode/traditional-ml/feature_engineering.md)（缺失填充、One-Hot/Label/WOE 编码、Z-score/Min-Max/Robust 缩放、选择、防泄漏）
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：缺失填充 + One-Hot + 标准化 + Pipeline。
- [`case4_credit_scoring.py`](../../code/01-traditional-ml/case4_credit_scoring.py)：WOE 编码思路演示。

## 5. 扩展阅读

- 《Feature Engineering for Machine Learning》(Alice Zheng)
- scikit-learn User Guide: Preprocessing
