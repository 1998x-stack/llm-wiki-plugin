---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-20
last_accessed: 2026-04-16
source_count: 3
tags: ["游戏引擎", "Lua", "3D", "2D", "UrhoX", "Urho3D", "NanoVG", "Box2D", "游戏开发"]
aliases: [UrhoX, UrhoX Lua, UrhoX游戏引擎]
relates_to: [UrhoXCLI, UrhoX材质库, NanoVG, PBR材质系统, Lua基础语法, 游戏脚手架模式, 米制单位系统, Y-up左手坐标系, 资源路径引用规范, Lua-eventData访问模式, Lua数组索引从1开始, table-unpack表构造器陷阱, NanoVG渲染事件模式, NanoVG字体创建规范, Emoji自动Fallback, UI系统选择规范, Lua类型标注规范, 枚举值使用规范, 代码模块化阈值, 第三人称相机库模式, 多人游戏模式判断, manifest-json检查规范, Urho3D, EmmyLua, Yoga-Flexbox, Box2D, tolua++, cjson]
supersedes: null
entity_type: project
---

# UrhoX引擎

## 概述
UrhoX 是基于 [[Urho3D]] 1.8 扩展的游戏引擎，使用 Lua 5.4 作为脚本语言，集成 [[NanoVG]] 矢量图形、Yoga Flexbox UI 系统、[[Box2D]]/3D 物理，面向 WebAssembly 平台发布。

## 关键内容
1. **核心兼容性**：基于 [[Urho3D]] 1.8，核心 API 95% 兼容，扩展了 [[NanoVG]]（C API 完全对齐）、新 UI 系统（Yoga Flexbox + [[NanoVG]]）、云变量/排行榜、视频播放等功能。
2. **脚本语言**：Lua 5.4，支持位运算符 `&|~<<>>`；事件数据通过 [[Lua脚本宿主模式|tolua]]++ 绑定访问（`eventData["Key"]:GetInt()` 或 `eventData:GetInt("Key")`）；数组索引从 1 开始。
3. **坐标系与单位**：Y-up [[Y-up左手坐标系|左手坐标系]]（与 Unity 相同），长度单位为米；Y 轴向上、X 轴向右、Z 轴向前。
4. **UI 系统**：新 UI 系统（`urhox-libs/UI`）基于 Yoga Flexbox + [[NanoVG]]，提供 40+ 内置控件；原生 [[Urho3D]] UIElement 系统已废弃。
5. **开发模式**：代码必须放在 `/workspace/scripts/`；必须基于标准脚手架起手（2D/2D物理/3D场景/3D角色四类模板）；`graphics:SetMode()` 已禁用，使用 `GetWidth()/GetHeight()/GetDPR()` 获取屏幕信息。
6. **多人/单机判断**：通过 `.project/settings.json` 的 `@runtime.multiplayer.enabled` 字段决定代码放置位置（Client.lua / Server.lua / Standalone.lua）。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南入口，包含完整开发规则与文档映射
- [[raw/articles/personal/ai-dev-kit/README]] — UrhoX AI Dev Kit 项目说明，含目录结构、NanoVG 特性、设计理念与示例统计I Dev Kit 项目说明，含目录结构、NanoVG 特性、设计理念与示例统计

## 相关
- [[UrhoXCLI]] — part_of
- [[UrhoX材质库]] — part_of
- [[NanoVG]] — uses
- [[PBR材质系统]] — uses
- [[Lua基础语法]] — uses
