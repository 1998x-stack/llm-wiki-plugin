---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, javascript, development-tools, source-map, 工具与框架]
aliases: ["Source Map Leak", "Source Map 泄露", ".map 文件泄露"]
relates_to: 
  - target: "[[Claude Code]]"
    type: affects
    confidence: 0.9
  - target: "[[Anthropic]]"
    type: impacts
    confidence: 0.9
  - target: "[[Bun]]"
    type: relates_to
    confidence: 0.7
  - target: "[[TypeScript]]"
    type: technology_used
    confidence: 0.8
supersedes: null
---

# Source Map 泄露事件

## 概述
[[Source Map]] 泄露事件是指在 2026 年 3 月 31 日发生的 [[Claude-Code|Anthropic Claude Code]] 源码泄露事故，由于构建工具错误地将包含完整源码的 .map 文件发布到了公共 npm 包中。

## 关键内容

1. **技术原理**：
   - [[Source Map]] 是开发工具生成的映射文件，用于将压缩后的代码映射回原始源码
   - [[Source Map]] 的 sourcesContent 字段存储了所有原始文件的完整内容，包括注释、内部常量、系统提示词
   - 正常情况下这些文件应该被排除在生产环境中

2. **事件经过**：
   - [[Anthropic]] 选用了自家收购的 Bun 作为运行时和打包器
   - Bun 的打包器默认启用 [[Source Map]] 生成，除非显式关闭
   - 某次发布中，有人忘记在 .npmignore 里屏蔽 *.map，或者没有在构建[[Configuration|配置]]里关闭 source map 生成
   - 结果：v2.1.88 版本的 @anthropic-ai/[[Claude-Code|claude-code]] npm 包里附带了一个 59.8 MB 的 .map 文件

3. **泄露规模**：
   - 泄露版本：@anthropic-ai/[[Claude-Code|claude-code]] v2.1.88
   - 文件数量：~1,906 个 [[TypeScript]] 文件
   - 代码行数：512,000+ 行
   - 压缩包大小：59.8 MB (.map 文件)

4. **安全影响**：
   - 暴露了系统提示词、内部常量、完整的源码结构
   - 暴露了 [[Anthropic]] 内部的模型代号和性能数据
   - 暴露了未来未发布功能的实现细节

## 来源
- [[01_overview_architecture]] — 事件详细描述

## 相关
- [[Claude Code]] — affects
- [[Source Map]] — core_technology
- [[Bun]] — tool_involved
- [[Anthropic]] — impacted_organization