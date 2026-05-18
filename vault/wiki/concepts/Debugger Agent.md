---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [debugging, agent, troubleshooting, root-cause-analysis, AI工程]
aliases: ["Debug Agent", "调试代理"]
relates_to: []
supersedes: null
---

# Debugger Agent

## 概述
Debugger Agent是一种专门用于处理错误、测试失败和异常行为的专家级排错人员，负责根因分析和故障修复。

## 关键内容

1. **主要职责**：
   - 获取错误信息和堆栈追踪
   - 复现问题步骤
   - 定位故障位置
   - 实施最小修复
   - 验证修复效果

2. **排错流程**：
   - 分析错误信息和日志
   - 检查最近的代码变更
   - 提出并测试假设
   - 隔离故障
   - 实现并验证修复

3. **调试输出格式**：
   - Error: 原始错误信息
   - Root Cause: 故障根本原因
   - Evidence: 确定原因的证据
   - Fix: 具体代码修改
   - Testing: 修复验证方法
   - Prevention: 避免复发策略

## 来源
- [[debugger.md]] — 原始配置和流程说明

## 相关
- [[Skills]] — 与其他技能工具的交互
- [[Code Reviewer Agent]] — 代码审查相关的调试
- [[Error Handling Testing]] — 错误处理测试

## 指令
每个新建/更新的页面执行 BM25 索引：
Bash: bash scripts/wiki.sh bm25_index update <wiki_file_path>