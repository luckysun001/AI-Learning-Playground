# Agent 智能体

> 状态：🚧 进行中（提示词模板已填充，原理文档 + 实战代码待补充）

Agent 是「能自主调用工具、规划任务、反思迭代」的 LLM 应用形态。本模块先从**最可复用、最能拉开差距的工程资产——提示词模板**入手，再逐步补齐原理与实战。

## 已完成：提示词模板

- 📘 [prompt_templates.md](prompt_templates.md) —— 六种核心提示词模式的原理 + 完整可复制模板：
  1. **ReAct**（边想边做，Thought/Action/Observation 循环）
  2. **Plan-and-Execute**（先列计划再逐步执行）
  3. **Function Calling**（用 JSON Schema 声明工具）
  4. **Reflection**（Actor 产出 → Critic 评审 → 修订迭代）
  5. **对话记忆**（角色设定 + 长期记忆注入 + 防注入）
  6. **多智能体角色**（Orchestrator + Researcher/Engineer/Reviewer 分工）

## 规划覆盖的知识点

- ReAct 模式
- 工具调用 / Function Calling
- 规划与反思
- 记忆系统

## 文档索引

| 主题 | 文档 |
|---|---|
| 提示词模板（总览） | [prompt_templates.md](prompt_templates.md) |

每篇请遵循 [`../traditional-ml/_template.md`](../traditional-ml/_template.md) 六段模板。

## 可复用模板文件

配套可运行的独立模板见 [`../../code/07-agent/prompts/`](../../code/07-agent/prompts/)，每个文件含占位符 `<XXX>` 与 Python 使用示例，可直接 `str.replace` 或 Jinja2 渲染。
