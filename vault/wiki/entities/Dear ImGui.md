---
type: tool
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏开发, UI, C++, 工具库]
aliases: [ImGui, DearImGui]
relates_to: [游戏引擎架构, 场景树]
supersedes: null
---
# Dear ImGui

## 概述
Dear ImGui 是一个轻量级 C++ 即时模式 GUI 库，广泛用于游戏引擎和工具的调试/编辑器界面，无需外部依赖，可快速集成进任何渲染器。

## 关键内容
1. **即时模式（Immediate Mode）**：每帧直接描述 UI 状态，无需维护 UI 对象树，代码简洁，适合工具和调试面板
2. **游戏引擎编辑器应用**：常用于实现 Hierarchy 面板、Inspector、Scene View、Asset Browser、Console 等编辑器核心面板
3. **集成方式**：Runtime + Editor 分离，Editor 本质是 Runtime + ImGui 调试面板；支持 OpenGL、Vulkan、DirectX 等多种渲染后端

## 来源
- [[C++ 游戏引擎搭建指南]] — 推荐作为 C++ 游戏引擎编辑器层的快速实现方案

## 相关
- [[游戏引擎架构]] — 编辑器层首选工具
- SDL2 — 常与 SDL2/GLFW 联合使用作为平台后端
