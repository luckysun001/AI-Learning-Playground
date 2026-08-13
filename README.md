# AI-Learning-Playground

> 系统化人工智能学习开源项目：从传统机器学习到多智能体系统，配套「原理讲解 + 标准伪代码 + 可运行实战」三重学习路径。

本项目的目标是帮助 AI 学习者建立「理论—算法—工程」三位一体的知识体系。每个知识点都提供：

1. **原理讲解**（`docs/`）——核心概念、数学推导、关键细节与调优经验；
2. **标准伪代码**（`pseudocode/`）——语言无关、可读性优先，专注算法逻辑本身；
3. **可运行实战**（`code/`）——数据 + 代码 + 依赖，尽量一键跑通。

---

## 🗂️ 模块概览与进度

| 模块 | 目录 | 状态 |
|---|---|---|
| 数学基础 & Python 编程 | `docs/fundamentals/` | 📅 规划中 |
| 传统机器学习 | `docs/traditional-ml/` · `code/01-traditional-ml/` | ✅ 已完成 |
| 深度学习基础 | `docs/deep-learning/` | 📅 规划中 |
| Transformer 架构 | `docs/transformer/` | 📅 规划中 |
| 预训练与微调 | `docs/pretrain-finetune/` | 📅 规划中 |
| 迁移学习 | `docs/transfer-learning/` | 📅 规划中 |
| RAG 检索增强生成 | `docs/rag/` | 📅 规划中 |
| Agent 智能体 | `docs/agent/` · `code/07-agent/` | 🚧 进行中 |
| 多智能体系统 | `docs/multi-agent/` | 📅 规划中 |

图例：✅ 已完成 · 🚧 进行中 · 📅 规划中

---

## 🧭 学习路线（递进）

```
数学基础 & Python 编程
    ↓
传统机器学习（监督 / 无监督 / 集成 / 评估 / 特征工程）
    ↓
深度学习基础（CNN / RNN / 优化器 / 正则化）
    ↓
Transformer 架构（自注意力、编码器-解码器）
    ↓
预训练 & 微调 & 迁移学习
    ↓
RAG 检索增强生成
    ↓
单智能体系统
    ↓
多智能体协作系统
```

---

## 🚀 快速开始

```bash
git clone https://github.com/luckysun001/AI-Learning-Playground.git
cd AI-Learning-Playground

# 按需安装依赖（分级，详见下方说明）
pip install -r requirements-base.txt     # 传统机器学习所需
# pip install -r requirements-dl.txt     # 深度学习
# pip install -r requirements-llm.txt    # 大模型 / RAG / Agent
# pip install -r requirements-full.txt   # 全部
```

### 跑通第一个案例（传统机器学习 · 从零线性回归）

```bash
cd code/01-traditional-ml
python linear_regression_gd.py
```

脚本会：用梯度下降从零实现线性回归 → 与 `sklearn` 的 `LinearRegression` 对比 → 打印均方误差。

---

## 📖 使用方式

1. 先读 `docs/<模块>/` 下的原理讲解，建立直觉；
2. 再看 `pseudocode/<模块>/` 下的标准伪代码，把握算法骨架；
3. 最后运行 `code/<NN-模块>/` 下的实战代码，把理论落到工程。

---

## 🤝 贡献指南

欢迎社区共建！新增知识点、补充伪代码、提交实战案例、修复 Bug、润色文档都极度需要。

- 完整贡献流程、分支策略、提交规范见 **[CONTRIBUTING.md](CONTRIBUTING.md)**；
- 单篇知识点文档请遵循 `docs/traditional-ml/_template.md` 提供的六段模板；
- 伪代码请遵循 `pseudocode/_format.md` 提供的统一格式。

---

## 📦 依赖分级

| 文件 | 用途 |
|---|---|
| `requirements-base.txt` | 数学 / 传统机器学习（NumPy、Pandas、scikit-learn、Matplotlib） |
| `requirements-dl.txt` | 深度学习（PyTorch、PyTorch-Lightning、TensorBoard） |
| `requirements-llm.txt` | 大模型 / RAG / Agent（Transformers、LangChain、Chroma、OpenAI 等） |
| `requirements-full.txt` | 以上全部 |

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

> 注：部分内容由 AI 辅助生成，已在各文档中标注；代码与算法实现均经过人工复核，可放心学习与二次创作。
