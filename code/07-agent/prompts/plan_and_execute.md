<!--
模板名：Plan-and-Execute（先计划，后执行）
适用：可拆多步、步骤间有依赖的长任务；希望先有全局规划再动手。
占位符：
  <GOAL>            用户的总体目标
  <COMPLETED_STEPS> 已完成步骤及结果的摘要（首步为空）
  <CURRENT_STEP>    当前要执行的步骤描述
  <TOOLS_DESCRIPTION> 可用工具说明
输出协议：规划器输出 {"plan":[{step,description,depends_on}]}；
          执行器每步输出 {"result","status","note"}。
-->

===== 规划器（第一轮调用）=====

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

===== 执行器（每步复用）=====

你是执行者。请根据「当前这一步」的目标完成任务，需要时使用工具。
全局目标：<GOAL>
已完成步骤与结果：
<COMPLETED_STEPS>
当前要执行的步骤：<CURRENT_STEP>
可用工具：<TOOLS_DESCRIPTION>

请完成当前步骤，并以 JSON 返回：
{"result": "<这一步的产物>", "status": "done|blocked", "note": "<备注>"}

<!-- 使用示例（Python）
planner = read("plan_and_execute.md").split("===== 执行器")[0]
executor = read("plan_and_execute.md").split("===== 执行器")[1]
plan_prompt = planner.replace("<GOAL>", user_goal)
step_prompt = (executor
    .replace("<GOAL>", user_goal)
    .replace("<COMPLETED_STEPS>", completed_summary)
    .replace("<CURRENT_STEP>", current_step_desc)
    .replace("<TOOLS_DESCRIPTION>", tools_desc))
-->
