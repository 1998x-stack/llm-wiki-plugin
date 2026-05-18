---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [坐标系, Y-up, 左手坐标系, UrhoX, 游戏引擎, 旋转, 游戏开发]
aliases: [Y-up坐标系, 左手坐标系, Unity风格坐标系]
relates_to: [UrhoX引擎, 米制单位系统, 四元数Slerp路径陷阱]
supersedes: null
---

# Y-up左手坐标系

## 概述
[[UrhoX引擎|UrhoX]] 使用 Y-up 左手坐标系，与 Unity 引擎相同：Y 轴向上，X 轴向右，Z 轴向前，Yaw 绕 Y 轴旋转（左右转头），Pitch 绕 X 轴旋转（抬头低头）。

## 关键内容
1. **轴向定义**：`Vector3.UP = (0,1,0)` 向上；`Vector3.RIGHT = (1,0,0)` 向右；`Vector3.FORWARD = (0,0,1)` 向前。与 Unity 引擎完全一致。
2. **旋转约定**：Yaw（偏航角）绕 Y 轴旋转，控制左右转头；Pitch（俯仰角）绕 X 轴旋转，控制抬头低头。使用 `Quaternion(yaw, Vector3.UP)` 实现水平旋转，`Quaternion(pitch, Vector3.RIGHT)` 实现垂直旋转。
3. **实际应用**：`node.position = Vector3(0, 5, 10)` 表示节点位于上方 5 米、前方 10 米处。FPS/TPS 游戏中鼠标控制视角时，需配合 `input.mouseMode = MM_RELATIVE` 使用。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #0.5

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[米制单位系统]] — relates_to（同属空间坐标系统规范）
- [[四元数Slerp路径陷阱]] — relates_to（旋转相关概念）
