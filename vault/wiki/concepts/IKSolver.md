---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [动画, 运动学, UrhoX, 组件]
aliases: [IK求解器]
relates_to: [逆向运动学, IKEffector, IK约束, 骨骼系统, UrhoX引擎]
supersedes: null
---
# IKSolver

## 概述
[[逆向运动学|IK]]Solver 是 [[UrhoX引擎|UrhoX]] 的[[逆向运动学]]求解器组件，挂载于骨骼根节点，负责管理 [[逆向运动学|IK]] 链并驱动关节求解，继承自 Component。

## 关键内容

### 方法

| 方法 | 说明 |
|------|------|
| `RebuildChainTrees()` | 重建 [[逆向运动学|IK]] 链树，场景结构变化后调用 |
| `RecalculateSegmentLengths()` | 重新计算各段骨骼长度 |
| `CalculateJointRotations()` | 计算关节旋转（通常由 Solve 内部调用） |
| `Solve()` | 执行一次 [[逆向运动学|IK]] 求解迭代 |
| `ApplyOriginalPoseToScene()` | 将原始姿态写回场景节点 |
| `ApplySceneToOriginalPose()` | 从场景节点读取并保存为原始姿态 |
| `ApplyActivePoseToScene()` | 将当前活动姿态写回场景节点 |
| `ApplySceneToActivePose()` | 从场景节点读取并保存为活动姿态 |
| `ApplyOriginalPoseToActivePose()` | 将原始姿态复制到活动姿态 |
| `DrawDebugGeometry(bool depthTest)` | 绘制 [[逆向运动学|IK]] 链调试几何体 |

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `algorithm` | [[逆向运动学|IK]]Solver::Algorithm | [[逆向运动学|IK]] 算法（如 FABR[[逆向运动学|IK]]） |
| `maximumIterations` | unsigned | 最大迭代次数 |
| `tolerance` | float | 收敛误差阈值 |
| `JOINT_ROTATIONS` | bool | 启用关节旋转计算 |
| `TARGET_ROTATIONS` | bool | 末端目标也旋转匹配 |
| `UPDATE_ORIGINAL_POSE` | bool | 每帧更新原始姿态 |
| `UPDATE_ACTIVE_POSE` | bool | 每帧更新活动姿态 |
| `USE_ORIGINAL_POSE` | bool | 每次求解前从原始姿态开始 |
| `CONSTRAINTS` | bool | 启用关节约束 |
| `AUTO_SOLVE` | bool | 每帧自动执行求解 |

### 使用模式
- 将 [[逆向运动学|IK]]Solver 挂载到骨骼根节点
- 在子节点挂载 [[IKEffector]] 指定目标
- 可选在关节节点挂载 [[IK约束]] 限制活动范围
- 设置 `AUTO_SOLVE = true` 自动驱动，或手动调用 `Solve()`

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/ik.md]] — UrhoX Lua API IK 模块文档

## 相关
- [[逆向运动学]] — relates_to，IK 技术原理
- [[IKEffector]] — relates_to，末端执行器，与 IKSolver 配合
- [[IK约束]] — relates_to，关节约束组件
- [[UrhoX引擎]] — relates_to，所属引擎
