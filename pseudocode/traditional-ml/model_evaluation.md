# 模型评估（Model Evaluation）

> 回答两个问题：**模型准不准？泛化能力好不好？** 核心矛盾是偏差-方差权衡（Bias-Variance Tradeoff）。
> 贯穿原则：用训练集学、用独立验证/测试集评估，绝不用测试集调参。
> 详见文档：[docs/traditional-ml/model_evaluation.md](../traditional-ml/model_evaluation.md)

## 输入
- y_true：真实标签，形状 (m,)
- y_pred：预测标签，形状 (m,)（分类）或预测值（回归）
- y_score：预测为正类的概率，形状 (m,)（用于 ROC / AUC）
- k：交叉验证折数（默认 5 或 10）

## 输出
- 分类指标：Accuracy / Precision / Recall / F1 / AUC
- 回归指标：MSE / RMSE / MAE / R²
- k 折 CV 均值与标准差、ROC 曲线点、学习曲线

## 子算法 A：混淆矩阵与分类指标
1. 初始化 `TP = FP = TN = FN = 0`
2. FOR i = 1..m：
   - `y_t = y_true[i]; y_p = y_pred[i]`
   - IF y_t==1 AND y_p==1: TP++
   - ELSE IF y_t==0 AND y_p==1: FP++
   - ELSE IF y_t==1 AND y_p==0: FN++
   - ELSE: TN++
3. `Accuracy = (TP + TN) / m`
4. `Precision = TP / (TP + FP)`（FP=0 时记为 1 或按约定）
5. `Recall = TP / (TP + FN)`
6. `F1 = 2 · P · R / (P + R)`
7. **多分类**：
   - 宏平均（macro）：各类指标算完再取均值（各类平等）
   - 微平均（micro）：先汇总全局 TP/FP/FN 再算指标（受大类主导）

## 子算法 B：k 折交叉验证（k-fold CV）
1. 打乱样本索引，均分为 k 份 `folds[1..k]`
2. FOR f = 1..k：
   - `train_idx = 除第 f 折外的所有样本`
   - `valid_idx = 第 f 折`
   - `model.fit(X[train_idx], y[train_idx])`
   - `score[f] = evaluate(model.predict(X[valid_idx]), y[valid_idx])`
3. `CV_mean = mean(score); CV_std = std(score)`
- 用途：更充分利用数据、估计更稳定；**调参用验证折 / CV，测试集仅最终汇报一次**

## 子算法 C：ROC 曲线与 AUC
1. 取所有候选阈值 `t ∈ unique(sorted(y_score))`（含 0 与 1 边界）
2. FOR 每个阈值 t：
   - `y_pred_t = (y_score >= t)`（大于等于阈值判为正）
   - `TPR = TP / (TP + FN)`（真正率 / 召回）
   - `FPR = FP / (FP + TN)`（假正率）
   - 记录曲线点 `(FPR, TPR)`
3. `AUC = 梯形积分 Σ_i (FPR_{i+1} - FPR_i) · (TPR_i + TPR_{i+1}) / 2`，值域 [0,1]
- 解读：AUC = 0.5 等于随机；越大越好；对类别不平衡比 Accuracy 可靠

## 子算法 D：回归指标
- `MSE = mean( (y_true - y_pred)² )`
- `RMSE = sqrt(MSE)`（与标签同量纲，易解释）
- `MAE = mean( |y_true - y_pred| )`（对离群稳健）
- `R² = 1 - Σ(y_true - y_pred)² / Σ(y_true - mean(y_true))²`（1 为完美，0 为朴素均值基线）

## 子算法 E：学习曲线（诊断偏差 / 方差）
1. 定义递增的训练样本量序列 `s ∈ {s_1 < s_2 < ... < s_max}`
2. FOR 每个 s：
   - `model.fit(X_train[:s], y_train[:s])`
   - `err_train = error on X_train[:s]`
   - `err_val = error on X_valid`
3. 绘制 err_train 与 err_val 随 s 的变化：
   - 两曲线间隙大 → **过拟合**（增数据 / 加正则 / 降复杂度）
   - err_train 本身就高 → **欠拟合**（增特征 / 增模型复杂度）

## 复杂度分析
- 混淆矩阵：O(m)
- k 折 CV：O(k · 单次训练成本)
- ROC / AUC：O(m log m)（排序）
- 学习曲线：O(折数 · 单次训练成本)

## 关键细节
- 类别不平衡：看 AUC / F1，别只看 Accuracy（全猜负类也能高准）
- 业务代价不对称（欺诈/疾病）：Recall 优先、阈值可调
- 测试集只能最终汇报一次，调参一律走验证集或 CV
- 防数据泄漏：评估/缩放统计必须来自训练折，禁止用全量信息
