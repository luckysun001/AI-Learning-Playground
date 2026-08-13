# Agent 智能体 · 实战代码

> 状态：🚧 进行中（提示词模板已就绪，实战脚本待补充）

## 提示词模板（prompts/）

本目录 `prompts/` 下是可**直接复用**的提示词模板文件，每个文件含占位符 `<XXX>` 与 Python 使用示例：

| 文件 | 模式 | 要点 |
|---|---|---|
| [prompts/react.md](prompts/react.md) | ReAct | Thought/Action/Observation 循环，带 Few-shot |
| [prompts/plan_and_execute.md](prompts/plan_and_execute.md) | 计划-执行 | 规划器 + 执行器两段模板 |
| [prompts/function_calling.md](prompts/function_calling.md) | 工具调用 | 系统提示 + JSON Schema 工具声明 |
| [prompts/reflection.md](prompts/reflection.md) | 自我反思 | Actor/Critic/修订 三段模板 |
| [prompts/conversational_memory.md](prompts/conversational_memory.md) | 对话记忆 | 角色 + 长期记忆注入 + 摘要维护 |
| [prompts/multi_agent_roles.md](prompts/multi_agent_roles.md) | 多智能体 | Orchestrator + 三角色模板 |

## 规划实战案例

1. ReAct 数学解题 Agent
2. 联网搜索 Agent
3. 代码执行 Agent（Python REPL）
4. 带长期记忆的个人助理

## 运行方式

```bash
cd code/07-agent
pip install -r ../../requirements-llm.txt   # 大模型 / Agent 依赖

# 以 react.md 为例，渲染模板（需自备 LLM 调用）
python - <<'PY'
tpl = open("prompts/react.md").read()
# 按文件内注释替换 <XXX> 占位符后即可发送给模型
PY
```
