---
type: synthesis
status: active
confidence: 0.5
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 研究, 工作]
aliases: [算法面试, RAG落地真相, AI Agent面试]
relates_to:
  - 检索增强生成
  - 多跳推理
  - 知识图谱增强RAG
  - 代码RAG
  - 面向Agent的工具设计
  - AI与游戏创作
  - 强化学习
  - Agentic Search
supersedes: null
---

# 算法面试与RAG落地真相

## 概述
从一场真实算法工程师面试中提炼的大模型落地核心洞察。涵盖RAG从混合检索到知识图谱的演进路径、多跳推理的破局方案、代码RAG的实操结论、Coding Agent选型逻辑，以及AI+游戏的未来方向。核心观点：行业缺的不是会用工具的人，而是能在成本与效果间做平衡、看透问题本质的落地型人才。

## 关键内容
1. **RAG落地的三阶段路径**：知识库搭建（ES+MySQL）→ 混合检索（query改写+多路召回+重排）→ 专项破局（知识图谱解决多跳推理）。纯语义检索只能解决单跳问题，多跳问题需引入知识图谱建立数据关联。
2. **多跳推理的半Agentic方案**：向量检索获取初始节点 → 知识图谱一层关系拓展 → 大模型过滤节点 → 生成答案。一层拓展解决85%+多跳问题，单点准确率95%+，在成本可控下实现效果最大化。
3. **代码RAG的三个核心结论**：纯代码RAG效果不如字符串匹配；有效方案需1:1配套解释文档；AST树是未来核心方向，可为代码仓库搭建专属"知识图谱"。
4. **Coding Agent选型逻辑**：简单任务用低成本方案（通义千问Code API），复杂核心任务用高准确率方案（Claude Code），选型核心是场景匹配与成本约束。
5. **AI+游戏的真正瓶颈**：不是AI能力，而是工具为人设计而非为Agent设计。未来需要原生面向Agent的工具：配置文件、API schema、命令行入口。

## 来源
- [[raw/articles/essays/thinking-series/011-算法面试]] — 全文

## 相关
- [[检索增强生成]] — part_of
- [[多跳推理]] — extends
- [[知识图谱增强RAG]] — implements
- [[代码RAG]] — relates_to
- [[面向Agent的工具设计]] — relates_to
- [[AI与游戏创作]] — relates_to
- [[强化学习]] — relates_to
- [[Agentic Search]] — compares_to
