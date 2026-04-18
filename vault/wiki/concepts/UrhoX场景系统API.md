---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏引擎", "UrhoX", "Lua", "API", "场景管理", "游戏开发"]
aliases: [UrhoX Scene, 场景API, Scene API]
relates_to: [UrhoX引擎, UrhoX节点系统API, UrhoX组件系统API, 场景树]
supersedes: null
---
# UrhoX场景系统API

## 概述
[[UrhoX引擎|UrhoX]] `Scene` 继承自 `Node`，是[[场景树]]的根节点，负责序列化（XML/JSON/Binary）、异步加载、时间控制和网络同步，所有节点和组件都挂载在其下。

## 关键内容
1. **序列化格式**：支持三种格式互换——`Load/Save`（Binary）、`LoadXML/SaveXML`、`LoadJSON/SaveJSON`；可从文件路径或 `File*` 流读写。
2. **场景实例化**：`Instantiate/InstantiateXML/InstantiateJSON` 在指定位置/旋转处创建预制体节点，`CreateMode` 控制 REPLICATED（网络同步）或 LOCAL（本地私有）。
3. **异步加载**：`LoadAsync/LoadAsyncXML` 配合 `LoadMode`（LOAD_SCENE_AND_RESOURCES / LOAD_RESOURCES_ONLY）分帧加载；通过 `asyncProgress`（0.0~1.0）监控进度，`StopAsyncLoading()` 可取消。
4. **时间控制**：`timeScale` 调整全局时间倍率（慢动作/快进）；`smoothingConstant` 和 `snapThreshold` 控制网络平滑插值行为。
5. **节点查找**：`GetNode(id)` 按数字 ID 精确查找；`GetNodesWithTag(tag)` 批量获取带标签节点；`GetComponent(id)` 跨树查找组件。
6. **网络更新**：`MarkNetworkUpdate`/`MarkReplicationDirty` 标记需要同步的节点/组件；`CleanupConnection` 清理断开的连接；`BeginThreadedUpdate/EndThreadedUpdate` 允许多线程组件更新。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/core]] — UrhoX Lua API Core Module，Scene 类完整方法与属性列表

## 相关
- [[UrhoX节点系统API]] — Scene 继承自 Node，所有节点操作同样适用
- [[UrhoX组件系统API]] — 组件挂载在 Scene 子树中的节点上
- [[场景树]] — relates_to，Scene 是场景树的根
- [[UrhoX引擎]] — part_of
