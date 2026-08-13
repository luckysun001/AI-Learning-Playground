# K 近邻（KNN, K-Nearest Neighbors）

> 最朴素的「基于实例」学习器：无显式训练（lazy learning），预测时直接检索训练集中最近的 $K$ 个邻居并「投票 / 平均」。
> 详见文档：[docs/traditional-ml/knn.md](../traditional-ml/knn.md)

## 输入
- X_train：训练特征矩阵，形状 (m, n)
- y_train：训练标签，形状 (m,)（分类取离散值，回归取连续值）
- X_query：待预测样本特征，形状 (q, n)（单样本时为 (1, n)）
- K：近邻个数（分类建议奇数，避免平票）
- metric：距离度量（`euclidean` / `manhattan` / `cosine`）
- weights：`uniform`（等权）或 `distance`（按距离反比加权）

## 输出
- y_pred：预测标签，形状 (q,)（分类）；或预测值（回归）

## 伪代码：主流程（惰性训练）
1. **存储阶段（无参数学习）**
   - 直接把 X_train、y_train 存入内存
   - 训练复杂度 O(1)，不估计任何参数
2. **对每个查询样本** x ∈ X_query：
   - 调用子算法 A 计算 x 与全部 m 个训练样本的距离，得 d[1..m]
   - 取距离最小的 K 个训练样本下标：`idx = argsort(d)[1..K]`
3. **分类任务**：
   - 若 `weights='uniform'` → 调用子算法 B（多数投票）
   - 若 `weights='distance'` → 调用子算法 C（距离加权投票）
   - **回归任务**：`y_pred = mean( y_train[idx] )`（或距离加权均值）
4. **RETURN** y_pred

## 子算法 A：距离度量
- 欧氏：`d(x,z) = sqrt( Σ_j (x_j - z_j)² )`
- 曼哈顿：`d(x,z) = Σ_j |x_j - z_j|`
- 余弦距离：`d(x,z) = 1 - (x·z) / (||x|| · ||z||)`
- ⚠️ 距离对量纲极度敏感，预测前应做标准化（见 [feature_engineering.md](feature_engineering.md)）

## 子算法 B：多数投票（uniform）
1. `counts = 每个类别在 K 个近邻中的出现次数`
2. `y_pred = argmax(counts)`（出现最多的类别）
3. **平票处理**：取距离更近者优先；或按类别序；或随机（需固定随机种子保证可复现）

## 子算法 C：距离加权投票（distance）
1. FOR 每个近邻 i ∈ idx：
   - `w_i = 1 / (d_i + ε)`（ε 防零距离导致除零）
2. FOR 每个类别 c：
   - `score_c = Σ_{i : y_i = c} w_i`
3. `y_pred = argmax_c(score_c)`

## 加速：KDTree / BallTree（空间索引）
- **训练阶段**：用 X_train 构建 KDTree（按坐标轴递归划分超平面）或 BallTree（超球嵌套）
- **查询阶段**：树检索最近 K 个，复杂度从 O(m) 降至约 O(log m)（低维有效）
- ⚠️ **维度灾难**：维度 ≳ 20 时树结构退化近似线性，宜用暴力法或先 PCA 降维

## 复杂度分析
- 训练：O(1)（仅存储）
- 预测（暴力）：O(q · m · n)
- 预测（KDTree，低维）：O(q · log m · n)
- 空间：O(m · n)（训练集必须常驻内存）

## 关键细节
- 必须特征标准化，否则大尺度特征主导距离
- K 选择：交叉验证选最优；K 太小→对噪声敏感过拟合，K 太大→边界模糊欠拟合
- 类别不平衡：用 `weights='distance'` 抑制多数类霸权
- 高维数据：先 PCA 降维再 KNN，否则距离区分度骤降
