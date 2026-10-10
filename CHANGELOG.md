# 更新日志

本文件记录 AI-Learning-Playground 的重要变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

项目采用「原理讲解（`docs/`）+ 标准伪代码（`pseudocode/`）+ 可运行实战（`code/`）」三条路径并行的结构，
每个模块的进度见 [README 模块概览](README.md#-模块概览与进度)。

---

## [未发布]

以下模块仍在建设中，欢迎参与贡献：

- 数学基础 & Python 编程
- 深度学习基础（CNN / RNN / 优化器 / 正则化）
- Transformer 架构
- 预训练与微调
- 迁移学习
- RAG 检索增强生成
- 多智能体系统

---

## 2026-10-10

### 工程

- 新增 `.github/workflows/ci.yml`（多版本 Python CI），CI 首次在远程生效
- 修正默认分支命名：本地 `master` → `main`，与远程保持一致

### 文档

- README 新增「相关项目」章节，与 [ai-education](https://github.com/luckysun001/ai-education) 互链
  （本仓库讲「为什么能用」，实战指南讲「怎么用」）

---

## 2026-08-13

### 新增

- **Agent 智能体模块（进行中）**
  - `docs/agent/prompt_templates.md`：六大提示词模式的原理与完整模板
    - ReAct（Thought / Action / Observation 循环）
    - Plan-and-Execute（规划器 + 执行器）
    - Function Calling（系统提示 + JSON Schema 工具声明）
    - Reflection（Actor 产出 → Critic 评审 → 修订）
    - 对话记忆（角色设定 + 长期记忆注入 + 防注入）
    - 多智能体角色（Orchestrator + Researcher / Engineer / Reviewer）
  - `code/07-agent/prompts/`：6 个可直接被代码读取替换的模板文件

- **传统机器学习模块（已完成）**
  - 12 篇原理文档（线性回归、逻辑回归、决策树、随机森林、SVM、KNN、朴素贝叶斯、
    KMeans、PCA、模型评估、特征工程）
  - 11 篇标准伪代码
  - 8 个可离线运行的实战脚本，全部使用合成数据，无需联网即可跑通
    - 从零实现：梯度下降线性回归、逻辑回归、KMeans++、CART 决策树
    - 综合案例：回归对比、流失预测、聚类 + PCA、信贷评分

- **项目骨架**
  - `docs/` / `code/` / `pseudocode/` 各 8 个模块目录
  - 分级依赖：`requirements-base.txt` / `requirements-dl.txt` /
    `requirements-llm.txt` / `requirements-full.txt`
  - 文档模板 `docs/traditional-ml/_template.md`（六段结构）与伪代码格式 `pseudocode/_format.md`

---

[v未发布]: https://github.com/luckysun001/AI-Learning-Playground/commits/main
