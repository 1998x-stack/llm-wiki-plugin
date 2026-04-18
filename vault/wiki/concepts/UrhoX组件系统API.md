---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏引擎", "UrhoX", "Lua", "API", "组件", "序列化", "动画", "游戏开发"]
aliases: [UrhoX Component, 组件API, Component API]
relates_to: [UrhoX引擎, UrhoX节点系统API, 属性动画]
supersedes: null
---
# UrhoX组件系统API

## 概述
[[UrhoX引擎|UrhoX]] 组件继承链为 `Object → Serializable → Animatable → Component`，每层叠加能力：事件系统、属性序列化、[[属性动画]]、场景挂载。`Component` 作为所有引擎功能（[[StaticModel静态网格体|StaticModel]]、RigidBody 等）的基类。

## 关键内容
1. **Object 层（事件基础）**：`SendEvent(name, data)` 发送事件；`HasSubscribedToEvent` 查询订阅状态；`SetBlockEvents` 临时屏蔽接收事件；所有引擎对象均从此层获得 `type/typeName/category` 类型信息。
2. **Serializable 层（属性系统）**：`SetTemporary(true)` 标记为临时对象（不参与序列化）；`SetInterceptNetworkUpdate(attrName, enable)` 拦截指定属性的网络同步，适用于需要客户端预测的属性。
3. **Animatable 层（[[属性动画]]）**：`SetObjectAnimation(ObjectAnimation*)` 应用整体动画资源；`SetAttributeAnimation(name, ValueAnimation*, wrapMode, speed)` 对单个属性（如颜色、位置）做关键帧动画；`wrapMode` 可选 WM_LOOP / WM_ONCE / WM_CLAMP；`SetAnimationEnabled/SetAnimationTime` 控制播放。
4. **Component 核心接口**：`GetNode()` 返回所属节点；`GetScene()` 直达场景根；`GetComponent(type)` 获取同节点上的兄弟组件；`DrawDebugGeometry(debug, depthTest)` 绘制调试辅助图形；`enabledEffective` 综合考虑节点启用状态的最终有效值。
5. **CreateMode 语义**：REPLICATED（跟随网络同步）vs LOCAL（纯本地，不参与网络）；在单机场景中两者无区别，多人游戏中关键[[区分]]。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/core]] — UrhoX Lua API Core Module，Component/Serializable/Animatable/Object 类完整方法列表

## 相关
- [[UrhoX节点系统API]] — 组件通过 Node::CreateComponent 附加到节点
- [[属性动画]] — Animatable 层提供的属性动画能力
- [[UrhoX音频系统API]] — 音频组件同属此组件体系
- [[UrhoX引擎]] — part_of
