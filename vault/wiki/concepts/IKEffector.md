---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["动画", "运动学", "UrhoX", "组件", "游戏开发"]
aliases: [末端执行器, IK末端]
relates_to: [逆向运动学, IKSolver, IK约束, 骨骼系统, UrhoX引擎]
supersedes: null
---
# IKEffector

## 概述
IKEffector 是 [[UrhoX引擎|UrhoX]] 的 IK 末端执行器组件，定义 IK 链的目标位置与旋转，挂载于需要 IK 驱动的末端关节，继承自 Component。

## 关键内容

### 核心概念
IKEffector 告诉 [[IKSolver]] "这个关节要达到哪里"。链长（chainLength）决定从此节点向上回溯多少个父节点参与 IK 求解，从而控制哪些关节被 IK 驱动。

### 目标控制方法

| 方法 | 说明 |
|------|------|
| `GetTargetNode() / SetTargetNode(Node*)` | 通过场景节点动态跟随目标 |
| `GetTargetName() / SetTargetName(String)` | 按节点名称设置目标（延迟绑定） |
| `GetTargetPosition() / SetTargetPosition(Vector3)` | 直接设置目标位置 |
| `GetTargetRotation() / SetTargetRotation(Quaternion)` | 设置目标旋转 |

### 链与权重参数

| 方法 | 说明 |
|------|------|
| `GetChainLength() / SetChainLength(unsigned)` | IK 影响的父节点层数 |
| `GetWeight() / SetWeight(float)` | 位置权重（0=不生效，1=完全跟随目标） |
| `GetRotationWeight() / SetRotationWeight(float)` | 旋转权重 |
| `GetRotationDecay() / SetRotationDecay(float)` | 旋转沿链向上的衰减率 |

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `targetNode` | Node* | 目标节点引用 |
| `targetName` | String | 目标节点名称 |
| `targetPosition` | Vector3 | 目标位置 |
| `targetRotation` | Quaternion | 目标旋转 |
| `chainLength` | unsigned | IK 链长度（父节点层数） |
| `weight` | float | 位置权重 [0, 1] |
| `rotationWeight` | float | 旋转权重 [0, 1] |
| `rotationDecay` | float | 旋转衰减率 |
| `WEIGHT_NLERP` | bool | 权重过渡使用 NLERP |
| `INHERIT_PARENT_ROTATION` | bool | 继承父节点旋转 |

### 典型用法
- 手部 IK：chainLength=2（手→前臂→上臂），跟随武器/交互点
- 脚部 IK：chainLength=2（脚→小腿→大腿），落在地形表面
- weight < 1 可实现 IK 与动画的混合叠加

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/ik.md]] — UrhoX Lua API IK 模块文档

## 相关
- [[逆向运动学]] — relates_to，IK 技术原理
- [[IKSolver]] — relates_to，IK 求解器，驱动此效应器
- [[IK约束]] — relates_to，配合使用的关节约束
- [[UrhoX引擎]] — relates_to，所属引擎
