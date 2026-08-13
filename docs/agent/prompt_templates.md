# Agent 提示词模板（Prompt Templates）

> 状态：✅ 已填充（提示词模式原理 + 可复用模板）。配套可运行模板文件见 [`../../code/07-agent/prompts/`](../../code/07-agent/prompts/)。

「提示词（Prompt）」是 LLM Agent 的**源代码**。模型权重是固定的，Agent 的能力边界几乎完全由你写进提示词的**角色设定、任务拆解方式、工具描述、输出格式约束**决定。本文把业界最成熟的几类 Agent 提示词模式拆开讲透，并给出**可直接复制、填空使用**的模板。

> 约定：模板中的 `<XXX>` 是占位符，使用时用真实内容替换（如 `<QUESTION>` → 用户问题）。可复用文件见 `code/07-agent/prompts/`，那里用同样的占位符约定。

---

## 1. 核心概念

为什么 Agent 需要专门的提示词工程？和普通 chatbot 不同，Agent 要**自主决定「下一步做什么」**，这要求提示词必须：

1. **给角色与边界**：它是谁、能做什么、不能做什么；
2. **给思考框架**：遇到复杂任务该怎么拆解（ReAct / Plan）；
3. **给工具说明书**：有哪些工具、何时用、输入输出是什么；
4. **给输出协议**：必须按机器可解析的格式回复（否则代码无法驱动下一步）；
5. **给反思与记忆接口**：从错误中学习、跨轮次记住上下文。

本文覆盖 6 大模式，按「从简单到复杂」排列：

| 模式 | 一句话 | 关键输出协议 |
|---|---|---|
| ReAct | 边想边做，思考与行动交替 | `Thought/Action/Observation` |
| Plan-and-Execute | 先列计划再逐步执行 | 计划列表 + 分步执行 |
| Function Calling | 用结构化 schema 声明工具 | `tool_calls` JSON |
| Reflection | 先干后审，自我迭代 | 草稿 → 批评 → 修订 |
| 对话记忆 | 带长期记忆的助手 | 系统提示 + 历史注入 |
| 多智能体角色 | 不同角色分工协作 | 角色专属提示词 |

---

## 2. 六种提示词模式详解

### 2.1 ReAct（Reason + Act）

**适用场景**：需要调用外部工具（搜索、计算器、API）的单智能体任务，如问答、数据分析。

**核心思想**：让模型交替输出「推理轨迹」和「动作」，形成 `Thought → Action → Observation → Thought …` 的循环，直到能给出最终答案。Observation 由外部执行器喂回。

**完整模板（System + 单轮 Few-shot）：**

```
你是一个能使用工具的智能助手。
面对用户问题，你必须严格按照以下格式回应，每一步只能输出一个块：

Thought: 你当前的内心推理，说明你接下来为什么这么做
Action: 要调用的工具名称（必须是 [<TOOL_NAMES>] 之一）
Action Input: 该工具的输入参数（JSON 格式）
（执行器会返回结果并替换下面这一行）
Observation: <TOOL_RESULT>
... 以上 Thought/Action/Action Input/Observation 可重复多次 ...
Thought: 我已经掌握足够信息，可以作答了
Final Answer: 给用户的最终答案（自然语言，简洁准确）

# 可用工具
<TOOLS_DESCRIPTION>

# 示例
Question: <EXAMPLE_QUESTION>
Thought: 我需要先查一下 <...>，再计算 <...>
Action: <EXAMPLE_ACTION>
Action Input: <EXAMPLE_INPUT>
Observation: <EXAMPLE_OBSERVATION>
Thought: 已知 <...>，现在可以计算最终答案
Final Answer: <EXAMPLE_FINAL_ANSWER>

# 现在开始
Question: <QUESTION>
```

**各部分讲解**
- `Thought`：强制模型「把推理写下来」，既可提升准确率（ chain-of-thought），又让调试者看到决策链路。
- `Action` / `Action Input`：机器可解析的动作指令；执行器据此调用工具。
- `Observation`：由代码注入，不是模型生成——这是 ReAct 与纯 CoT 的关键区别。
- `Final Answer`：终止信号，解析器据此停止循环。

**关键技巧**
- 务必在解析器里「只认 Final Answer 才停」，避免模型提前收尾；
- 循环设最大步数（如 8 步），超限让模型总结已得信息兜底；
- 工具描述写清「何时用、返回什么」，能显著降低乱用工具。

---

### 2.2 Plan-and-Execute（先计划，后执行）

**适用场景**：任务可拆成多步、步骤间有依赖，且希望**先有全局规划再动手**（比 ReAct 更省 token、更可控）。

**核心思想**：第一轮让规划器产出「步骤清单」，之后每一步用执行器（可再套 ReAct）完成，并回写进度。

**规划器模板：**

```
你是一个任务规划专家。请把用户的复杂请求拆解成有序、可独立执行的步骤。
要求：
1. 每步只做一件事，写明「这一步要达成什么」；
2. 标出步骤间依赖（如「步骤3依赖步骤1的结果」）；
3. 不要写代码细节，只写目标。

用户请求：<GOAL>

请以如下 JSON 格式只输出计划（不要多余文字）：
{
  "plan": [
    {"step": 1, "description": "<第一步要做什么>", "depends_on": []},
    {"step": 2, "description": "<第二步要做什么>", "depends_on": [1]}
  ]
}
```

**执行器模板（每步复用）：**

```
你是执行者。请根据「当前这一步」的目标完成任务，需要时使用工具。
全局目标：<GOAL>
已完成步骤与结果：
<COMPLETED_STEPS>
当前要执行的步骤：<CURRENT_STEP>
可用工具：<TOOLS_DESCRIPTION>

请完成当前步骤，并以 JSON 返回：
{"result": "<这一步的产物>", "status": "done|blocked", "note": "<备注>"}
```

**关键技巧**
- 规划与执行可用**不同模型**：规划用强模型（GPT-4 级），执行用便宜模型，省成本；
- 把「已完成步骤结果」持续回灌，避免重复劳动；
- 适合长任务：即使中途失败，计划还在，可重跑单步。

---

### 2.3 Function Calling / Tool Calling

**适用场景**：所有需要模型「决定调用哪个函数、填什么参数」的场景（最主流的 Agent 落地方式，OpenAI / Claude / 通义等均支持）。

**核心思想**：把工具定义为 **JSON Schema**，模型不直接拼字符串，而是输出符合 schema 的 `tool_calls` 结构，由框架安全执行。

**工具 Schema 示例：**

```json
{
  "name": "get_weather",
  "description": "查询指定城市当前天气",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "城市名，如 北京"},
      "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
    },
    "required": ["city"]
  }
}
```

**系统提示词（引导模型用工具）：**

```
你是天气助手。当用户询问天气时，必须调用 get_weather 工具获取真实数据，
不要凭记忆编造。拿到工具返回结果后，用一句话中文总结给用户。
若用户未指定城市，先礼貌追问。
```

**关键技巧**
- `description` 写得好坏直接决定调用准确率——要写「何时该用、参数是什么语义」；
- 用 `required` 强制必填，减少无效调用；
- 拿到 `tool_calls` 后**一定要把 tool 结果再发回模型**让它整合，否则它不知道结果；
- 并行调用：无依赖的多个工具可一次返回多个 `tool_calls`。

---

### 2.4 Reflection（自我反思 / 自我批判）

**适用场景**：写作、代码生成、方案设计等「初稿质量不稳定、需要迭代」的任务。

**核心思想**：Actor 产出初稿 → Critic（或另一个角色）给出批评 → Actor 修订，可多轮直到满意。

**Actor 模板：**

```
你是<ROLE>，请根据要求产出<DELIVERABLE>。
要求：<REQUIREMENTS>
只输出成品本身，不要解释。
```

**Critic 模板：**

```
你是严格的评审专家。请审阅下面这份<DELIVERABLE>，从以下维度打分并指出具体问题：
- 正确性：有无事实/逻辑错误
- 完整性：是否遗漏要求中的要点
- 清晰性：表达是否准确无歧义
- 改进建议：逐条列出可执行的修改

待评审内容：
<ACTOR_OUTPUT>

以 JSON 返回：{"score": 0-100, "issues": ["..."], "suggestions": ["..."]}
```

**迭代控制（伪逻辑）：**

```
draft = actor(prompt)
FOR i IN 1..max_iter:
    review = critic(draft)
    IF review.score >= threshold: BREAK
    draft = actor(prompt + "根据评审意见修订：" + review.suggestions)
RETURN draft
```

**关键技巧**
- Critic 与 Actor 最好用**不同系统提示**（甚至不同模型），避免「自己护短」；
- 给 Critic 明确的评分维度，比「随便评价」有效得多；
- 设分数阈值 + 最大轮数，防止无限循环。

---

### 2.5 对话记忆（Conversational + Memory）

**适用场景**：客服、个人助理等需要记住历史、跨多轮对话的 Agent。

**核心思想**：系统提示固定「角色 + 规矩」，每轮把「摘要记忆 + 近期原文」注入上下文，避免超出窗口。

**系统提示模板：**

```
你是<ASSISTANT_NAME>，一名<PERSONA>（如：严谨的 Python 编程助手）。
你的行为准则：
1. 只用中文回答；
2. 不确定时明确说「不确定」，绝不编造；
3. 涉及危险操作（删文件、付费）必须先确认；
4. 保持友好、简洁。

# 关于用户的长期记忆（由记忆模块维护）
<USER_PROFILE_SUMMARY>

# 当前对话近期记录
<RECENT_HISTORY>

# 用户最新输入
<USER_MESSAGE>
```

**记忆维护模板（周期性摘要）：**

```
以下是某用户与助手的一段对话，请提炼成不超过 <MAX_TOKENS> 的「长期记忆摘要」，
保留：用户身份/偏好/未决事项/重要事实。只输出摘要本身。

对话：
<RAW_HISTORY>
```

**关键技巧**
- 用「**滑动窗口原文 + 滚动摘要**」组合：最近 N 轮原文保真，更早的压成摘要；
- 记忆写入要在「工具/动作之前」，防止动作结果未落库就丢失；
- 隐私：长期记忆可能含敏感信息，要明确告知用户并提供清除入口。

---

### 2.6 多智能体角色（Multi-Agent Roles）

**适用场景**：复杂任务需要「分工协作」，如「研究员 + 程序员 + 审查员」组队完成需求。

**核心思想**：每个角色有独立系统提示，由 Orchestrator（编排者）分发任务、汇总结果。

**编排者（Orchestrator）模板：**

```
你是项目主编。团队由以下角色组成：
- 研究员(researcher)：负责检索与事实核查
- 工程师(engineer)：负责写代码/实现
- 审查员(reviewer)：负责找漏洞与改进

用户需求：<GOAL>
请决定：第一步派哪个角色、给它什么任务。以 JSON 返回：
{"assign_to": "researcher|engineer|reviewer", "task": "<具体任务描述>"}
```

**各角色提示词（节选）：**

```
# researcher
你是研究员。只做信息检索与事实核查，不写最终方案。
输出结构化发现：{"findings": [...], "sources": [...], "open_questions": [...]}

# engineer
你是工程师。基于给定需求产出可运行代码。
输出：{"code": "<代码>", "explanation": "<说明>", "tests": "<自测用例>"}

# reviewer
你是审查员。只挑问题，不重写。
输出：{"blocking_issues": [...], "suggestions": [...], "verdict": "pass|fail"}
```

**关键技巧**
- 角色间通过**结构化消息**（JSON）传递，减少自然语言歧义；
- Orchestrator 负责「何时停止」——所有角色 verdict=pass 或达最大轮数；
- 防止角色「抢戏」：在各自提示里明确「你只负责 X，不负责 Y」。

---

## 3. 伪代码 / 流程

Agent 运行的主循环（以 ReAct + 工具为例）：

```
1. messages = [System(<SYSTEM_PROMPT>), User(<QUESTION>)]
2. FOR step IN 1..max_steps:
3.     resp = LLM(messages)
4.     IF resp 含 Final Answer:
5.         RETURN resp.final_answer
6.     action, action_input = parse(resp)        # 解析 Action / Action Input
7.     observation = execute_tool(action, action_input)
8.     messages += [resp, Observation(observation)] # 把结果喂回上下文
9. RETURN "已达最大步数，基于已知信息作答：" + LLM(messages).summary
```

更完整的 ReAct 解析与多 Agent 协作伪代码规划中（见 `pseudocode/agent/`）。

---

## 4. 关键细节与调优

- **占位符要唯一且自解释**：`<QUESTION>` 比 `<Q>` 好，降低替换出错概率。
- **用分隔符包裹变量**：用户输入用 `"""` 或 XML 标签（如 `<user_input>...</user_input>`）包起来，防止提示词注入（用户用「忽略以上指令」越权）。
- **少样本示例（Few-shot）极其有效**：在模板里放 1–2 个完整示例，模型立刻学会输出格式。
- **约束输出格式**：要求「只输出 JSON」「不要解释」，配合代码端 JSON 解析，鲁棒性大增。
- **失败兜底**：模型可能不按格式输出——解析失败时，用「你违反了格式，请重来」做一步修正重试。
- **token 预算**：把长工具结果截断/摘要后再回灌，避免上下文爆掉。
- **版本化模板**：提示词也是代码，建议存文件、进 git、写变更说明（本项目即如此）。

---

## 5. 实战案例

- 📁 可复用模板文件：[`code/07-agent/prompts/`](../../code/07-agent/prompts/)，每个文件是一个独立模板（含占位符与示例），可直接被 Python 读取并 `str.replace` 使用。
- 运行方式见 [`code/07-agent/README.md`](../../code/07-agent/README.md)。

---

## 6. 扩展阅读

- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (2022)
- Wei et al., *Chain-of-Thought Prompting Elicits Reasoning in LLMs* (2022)
- OpenAI Cookbook: Function calling 最佳实践
- LangChain / LlamaIndex 官方文档：Prompt Templates、Agent 模块
- Anthropic: *Building effective agents*（agent 设计模式长文）
