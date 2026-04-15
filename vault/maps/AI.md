---
topic: "AI"
type: map
page_count: 16
updated: 2026-04-15
---

# AI

## 概念

- [[ACP协议]] — Agent Client Protocol（ACP） 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和消息流交互。DeepAgen (confidence: 0.85)
- [[Agent Harness模式]] — Agent Harness（"马具"）是一种 AI Agent 工程架构模式：不从零实现 Agent 运行时，而是在现有 LLM 框架（如 LangGraph 的 `create_ (confidence: 0.9)
- [[Claude-Code-Hook-System]] — Claude Code Hook System 是 Claude Code 编程助手提供的一种扩展机制，允许开发者通过编写脚本拦截和响应 AI 会话的生命周期事件。该系统包含一组预 (confidence: 0.9)
- [[Context-Engineering]] — Context Engineering（上下文工程）是指对 LLM 的有限上下文窗口进行策展与管理的系统化方法。Anthropic 将其定义为：在固定 token 预算下最大化有用 (confidence: 0.92)
- [[DeepAgents中间件体系]] — DeepAgents 中间件（`libs/deepagents/deepagents/middleware/`）是 Agent Harness模式 的核心扩展点：每个中间件继承 ` (confidence: 0.9)
- [[DeepAgents后端协议]] — DeepAgents 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtocol` 定义统一的文件类 AP (confidence: 0.9)
- [[DeepAgents评估体系]] — DeepAgents 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹"（trajectory），用 (confidence: 0.9)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义准则打分，代替人工评估。适用于难以用规则/子串匹配表达的语义正确性、风格、完整性、多条件综合等评估目标。核心 (confidence: 0.9)
- [[分层记忆架构]] — 分层记忆架构（Hierarchical Memory Architecture）是 Context-Engineering 的核心实现模式。将 LLM 上下文从单一聊天历史升级为五 (confidence: 0.9)
- [[渐进式披露-Progressive-Disclosure]] — 渐进式披露（Progressive Disclosure）是一种交互设计和信息管理策略，旨在通过分阶段、按需的方式向用户（或 AI 模型）展示信息，以避免认知过载和资源浪费。在 A (confidence: 0.9)

## 人物

- [[Alex-Newman]] — Alex Newman（社交媒体账号 @thedotmack）是一位开源软件开发者，以其在 AI 编程辅助工具领域的创新工作而闻名。他是 Claude-Mem 项目的创始人和主要维 (confidence: 0.9)
- [[ChromaDB]] — ChromaDB 是一个开源的向量数据库（Vector Database），专为 AI/LLM 应用设计，用于存储和检索向量嵌入（Embeddings）。它支持语义搜索——将文本转 (confidence: 0.85)
- [[Claude-Code]] — Claude Code 是 Anthropic 官方发布的 AI 编程助手 CLI（命令行界面）工具，基于 Claude 模型（Opus/Sonnet/Haiku）驱动。它深度集成 (confidence: 0.95)
- [[Claude-Mem]] — Claude-Mem 是一个专为 Claude Code 设计的开源持久化记忆插件，旨在解决大型语言模型（LLM）固有的“无状态”缺陷。通过自动捕获会话中的工具调用、利用 AI 进 (confidence: 1.0)
- [[DeepAgents]] — LangChain 官方开源的 生产级 Agent Harness（`langchain-ai/deepagents`），基于 LangGraph 构建。定位"batteries- (confidence: 0.95)

## 综合分析

- [[DeepAgents评估设计哲学]] — DeepAgents 的评估体系建立在三条核心分离线上，每条分离线都针对一个常见的"评估混淆陷阱"： (confidence: 0.9)
