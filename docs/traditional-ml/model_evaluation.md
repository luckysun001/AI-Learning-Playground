# 模型评估（Model Evaluation）

## 1. 核心概念

评估回答两个问题：**模型准不准？泛化能力好不好？** 不评估就上线，等于盲飞。评估的核心矛盾是**偏差-方差权衡**（Bias-Variance Tradeoff）：模型要么欠拟合（高偏差）、要么过拟合（高方差）。

贯穿始终的原则：**用训练集学、用独立的验证/测试集评估**，绝不能用测试集调参。

## 2. 数学原理

**回归指标：**
- MSE $\frac{1}{m}\sum(y-\hat{y})^2$、RMSE（同量纲）、MAE $\frac{1}{m}\sum|y-\hat{y}|$（对离群稳健）
- $R^2 = 1 - \frac{\sum(y-\hat{y})^2}{\sum(y-\bar{y})^2}$

**分类指标（基于混淆矩阵）：**

| | 预测正 | 预测负 |
|---|---|---|
| 实际正 | TP | FN |
| 实际负 | FP | TN |

- Accuracy $=\frac{TP+TN}{TP+TN+FP+FN}$
- Precision $=\frac{TP}{TP+FP}$（查得准不准）
- Recall $=\frac{TP}{TP+FN}$（查得全不全）
- F1 $= 2\frac{P\cdot R}{P+R}$
- **AUC-ROC**：综合不同阈值下的 TPR/FPR，对不平衡数据比 Accuracy 可靠

**交叉验证（CV）：** 把数据切 $k$ 份，轮流用 $k-1$ 份训练、1 份验证，取均值，**更充分利用数据、估计更稳定**（常用 $k=5$ 或 10）。

## 3. 关键细节与调优

- **先分训练/验证/测试**：常见 80/10/10 或 70/15/15；小数据用 CV。
- **类别不平衡看 AUC / F1，别只看 Accuracy**：100 个里 99 个负类，全猜负也有 99% 准。
- **学习曲线诊断**：训练误差高→欠拟合（加特征/复杂度）；训练低但验证高→过拟合（正则/更多数据）。
- **不要拿测试集调超参**：测试集只能最终汇报一次，调参用验证集或 CV。
- **业务代价不对称**：欺诈/疾病检测里 FN 代价远高于 FP，Recall 优先、阈值可调。

## 4. 实战案例

- 📎 标准伪代码：[pseudocode/traditional-ml/model_evaluation.md](../../pseudocode/traditional-ml/model_evaluation.md)（混淆矩阵、k 折 CV、ROC/AUC 梯形积分、学习曲线）
- [`case1_regression_comparison.py`](../../code/01-traditional-ml/case1_regression_comparison.py)：多模型 RMSE / $R^2$ 对比。
- [`case2_churn_prediction.py`](../../code/01-traditional-ml/case2_churn_prediction.py)：Accuracy / Precision / Recall / F1 / AUC 全套。

## 5. 扩展阅读

- 《The Elements of Statistical Learning》第 7 章（模型评估与选择）
- scikit-learn User Guide: Model Evaluation
