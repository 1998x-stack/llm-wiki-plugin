---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏引擎", "Lua", "开发准则", "UrhoX", "最佳实践", "游戏开发"]
aliases: [UrhoX开发规则, UrhoX Lua规范]
relates_to: [UrhoX引擎, NanoVG, Lua基础语法, PBR材质系统]
supersedes: null
---

# UrhoX Lua开发准则

## 概述
[[UrhoX引擎|UrhoX Lua]] 引擎的强制性开发规则集，涵盖坐标系、代码组织、UI选型、物理系统、输入枚举等关键领域，违反可导致运行错误或逻辑缺陷。

## 关键内容
1. **代码存放与脚手架**：用户代码必须放在 `/workspace/scripts/`；必须基于对应类型脚手架起手（2D休闲/2D物理/3D场景/3D角色），禁止从零手写；`urhox-libs/` 为只读参考副本，修改不生效。
2. **坐标系与单位**：Y-up 左手坐标系（与 Unity 相同），单位为米；`SetMode()` 已禁用，通过 `GetWidth()/GetHeight()/GetDPR()` 获取屏幕参数；`orthoSize` 代表全高度，内部使用 `orthoSize * 0.5` 作为半高度。
3. **UI 系统选型**：必须使用 `urhox-libs/UI`（Yoga Flexbox + [[NanoVG]]，40+ 控件）；原生 Urho3D UIElement 已废弃；raw [[NanoVG]] 仅用于自定义图形，不做 UI/HUD。
4. **枚举值与类型**：鼠标/键盘事件必须使用枚举常量（`MOUSEB_LEFT`、`KEY_SPACE` 等），禁止用数字替代；未赋值变量必须加 `---@type` 类型标注，否则 LSP 报 undefined-field 错误。
5. **Lua 特性陷阱**：数组索引从 1 开始；`table.unpack()` 只在表构造器最后位置完全展开；`eventData` 用 `eventData["Key"]:GetInt()` 或更高效的 `eventData:GetInt("Key")` 访问。
6. **模块化阈值**：单文件超过 1500 行必须拆分；多轮迭代项目从第一轮就建立模块化结构；第三人称相机必须使用 `ThirdPersonCamera` 库，不要手动计算相机位置。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE]] — UrhoX Lua AI 开发指南入口，14条核心规则完整定义

## 相关
- [[UrhoX引擎]] — part_of
- [[NanoVG]] — relates_to
- [[Lua基础语法]] — relates_to
- [[PBR材质系统]] — relates_to
