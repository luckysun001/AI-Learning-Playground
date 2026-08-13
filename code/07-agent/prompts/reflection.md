<!--
模板名：Reflection（自我反思 / 自我批判）
适用：写作、代码生成、方案设计等「初稿质量不稳定、需迭代」的任务。
占位符：
  <ROLE>          产出者角色，如 "技术文档写手"
  <DELIVERABLE>   交付物名称，如 "API 设计文档"
  <REQUIREMENTS>  对交付物的要求
  <ACTOR_OUTPUT>  当前草稿内容
  <MAX_TOKENS>    评审意见允许的最大长度
  <DIMENSIONS>    评分维度说明
迭代：actor 产出 -> critic 评审 -> 未达阈值则 actor 据建议修订，循环至满意或上限。
-->

===== Actor（产出初稿）=====

你是<ROLE>，请根据要求产出<DELIVERABLE>。
要求：<REQUIREMENTS>
只输出成品本身，不要解释。

===== Critic（评审）=====

你是严格的评审专家。请审阅下面这份<DELIVERABLE>，从以下维度打分并指出具体问题：
<DIMENSIONS>

待评审内容：
<ACTOR_OUTPUT>

以 JSON 返回：{"score": 0-100, "issues": ["..."], "suggestions": ["..."]}

===== 修订（基于评审）=====

你是<ROLE>。下面是你上一版<DELIVERABLE>与评审意见，请逐条采纳建议修订：
【上一版】
<ACTOR_OUTPUT>
【评审意见】
<CRITIC_SUGGESTIONS>
只输出修订后的成品本身。

<!-- 迭代控制伪逻辑
draft = actor(prompt)
for i in range(max_iter):
    review = critic(draft)
    if review["score"] >= threshold: break
    draft = revise(prompt, draft, review["suggestions"])
-->
