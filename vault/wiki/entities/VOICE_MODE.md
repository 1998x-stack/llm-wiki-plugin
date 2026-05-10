---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [feature, ai-tools, voice-interface]
aliases: ["VOICE_MODE", "Voice Mode", "语音模式"]
relates_to:
  - target: "[[Claude Code]]"
    type: feature_of
  - target: "[[Push-to-Talk]]"
    type: implements
  - target: "[[Speech Recognition]]"
    type: uses
supersedes: null
---

# VOICE_MODE

## 概述
[[Claude Code]] 中的语音输入接口功能，由 Feature Flag 控制的未发布功能。

## 关键内容

1. **设计模式**：
   - 采用 Push-to-Talk（按住说话）模式
   - 用户按住快捷键开始语音输入，松开后语音转录为文本

2. **技术实现**：
   - 通过浏览器/系统麦克风 API 录音
   - 语音识别（本地或云端 API）转换为文本
   - 文本注入到 [[Claude Code]] 输入框进入正常 Agent 处理流程

3. **优势**：
   - 避免持续监听的隐私问题
   - 减少背景噪音干扰
   - 适用于远程开发、手解放等场景

## 来源
- [[07_terminal_renderer_features]] — 

## 相关
- [[Claude Code]] — feature_of
- [[Push-to-Talk]] — implements
- [[Speech Recognition]] — uses