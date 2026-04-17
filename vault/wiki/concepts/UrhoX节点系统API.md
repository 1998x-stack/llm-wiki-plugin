---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏引擎, UrhoX, Lua, API, 节点, 变换]
aliases: [UrhoX Node, 节点API, Node API]
relates_to: [UrhoX引擎, UrhoX场景系统API, UrhoX组件系统API, 场景树]
supersedes: null
---
# UrhoX节点系统API

## 概述
[[UrhoX引擎|UrhoX]] `Node` 继承自 `Animatable`，是[[场景树]]的基本单元，封装了 3D/2D 变换（位置/旋转/缩放）、父子层级管理和组件容器，坐标系为 Y-up 左手系，单位为米。

## 关键内容
1. **变换体系**：区分 Local（父节点相对）和 World（世界绝对）两套接口——`SetPosition/SetWorldPosition`、`GetTransform/GetWorldTransform`；2D 游戏使用 `SetPosition2D/SetRotation2D/SetScale2D` 对应接口。
2. **旋转操作**：`Translate/Rotate` 支持 `TransformSpace`（TS_LOCAL / TS_WO[[强化学习|RL]]D / TS_PARENT）指定参考系；`Pitch/Yaw/Roll` 分别绕 X/Y/Z 轴旋转；`LookAt(target, upAxis, space)` 使节点朝向目标。
3. **坐标转换**：`LocalToWorld/WorldToLocal`（支持 Vector3 和 Vector4 齐次坐标）实现空间转换，是射线投射和相机映射的基础。
4. **父子管理**：`CreateChild(name, mode, id)` 创建子节点；`AddChild/RemoveChild/RemoveAllChildren`；`Clone(mode)` 深拷贝子树；`SetParent` 重挂父节点；`GetChild(name/hash/index, recursive)` 递归查找。
5. **组件管理**：`CreateComponent(type, mode, id)`/`GetOrCreateComponent`/`RemoveComponent`；`GetComponent(type, recursive)` 向下递归查找；`GetParentComponent(type, recursive)` 向上查找；支持按类型批量操作 `RemoveComponents(type)`。
6. **标签系统**：`AddTag/RemoveTag/HasTag/GetTags` 管理节点标签；配合 `Scene::GetNodesWithTag` 实现按标签批量查询（如"enemy"、"pickup"）。
7. **Lua 脚本对象**：`CreateScriptObject(type)` 在节点上附加 Lua 脚本组件；`GetScriptObject()` 取回 [[Lua-table-用法|Lua 表]]。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/core]] — UrhoX Lua API Core Module，Node 类完整方法与属性列表

## 相关
- [[UrhoX场景系统API]] — Scene 继承自 Node，是场景树的根
- [[UrhoX组件系统API]] — 组件挂载在 Node 上
- [[场景树]] — relates_to，Node 是场景树的节点类型
- [[UrhoX引擎]] — part_of
- [[UrhoX Lua开发准则]] — 坐标系规则（Y-up 左手，米单位）
