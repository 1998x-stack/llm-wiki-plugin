---
type: tool
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏开发, C++, 跨平台, 工具库]
aliases: [SDL, SDL3, Simple DirectMedia Layer]
relates_to: [游戏引擎架构, Dear ImGui]
supersedes: null
---
# SDL2

## 概述
SDL2（Simple DirectMedia Layer 2）是跨平台 C/C++ 媒体库，提供窗口创建、输入处理、音频、渲染上下文等操作系统抽象，是 C++ 游戏引擎平台层的首选起步工具。

## 关键内容
1. **核心功能**：跨平台窗口创建与管理、键鼠/手柄输入处理、OpenGL/Vulkan 上下文创建、基础音频播放
2. **适用场景**：新手搭建游戏引擎的平台层起步（对比 GLFW，SDL2 功能更全，含音频和更多输入支持）；与 OpenGL/Vulkan/[[Dear ImGui]] 联合使用
3. **版本说明**：SDL3 为最新版本，API 有较大变化；SDL2 仍为生产环境主流，文档和社区更成熟

## 来源
- [[C++ 游戏引擎搭建指南]] — 推荐为 C++ 游戏引擎平台层的新手首选库

## 相关
- [[游戏引擎架构]] — 平台层核心依赖
- [[Dear ImGui]] — 常与 SDL2 联合用于窗口+编辑器方案
