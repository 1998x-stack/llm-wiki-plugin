---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [动画, 运动学, UrhoX, 组件]
aliases: [IKConstraint, IK关节约束]
relates_to: [逆向运动学, IKSolver, IKEffector, 骨骼系统, UrhoX引擎]
supersedes: null
---
# IK约束

## 概述
IK约束（IKConstraint）是 [[UrhoX引擎|UrhoX]] 的关节约束组件，通过刚性、伸展性和长度范围限制 IK 关节的活动，防止非自然姿态，继承自 Component。

## 关键内容

### 参数说明

| 方法 | 属性 | 说明 |
|------|------|------|
| `GetStiffness() / SetStiffness(float)` | stiffness | 关节刚性 [0, 1]，1 = 完全刚性不可旋转 |
| `GetStretchiness() / SetStretchiness(float)` | stretchiness | 骨骼可拉伸程度 [0, 1]，0 = 不可拉伸 |
| `GetLengthConstraints() / SetLengthConstraints(Vector2)` | lengthConstraints | 骨骼长度范围（min, max），超出则截断 |

### 使用模式
- 挂载于骨骼链中需要限制的关节节点
- 需在 [[IKSolver]] 上启用 `CONSTRAINTS = true` 才生效
- stiffness 接近 1 适合脊柱等刚性部位；接近 0 适合柔性肢体
- lengthConstraints 可防止手臂被 IK 拉伸到不自然长度

### 设计意图
IK 求解器在无约束时可能将关节旋转到任意角度或拉伸骨骼超出物理范围。IKConstraint 通过局部限制配合全局求解，在保持求解灵活性的同时维持动画自然度。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/ik.md]] — UrhoX Lua API IK 模块文档

## 相关
- [[逆向运动学]] — relates_to，IK 技术原理
- [[IKSolver]] — relates_to，启用约束的求解器
- [[IKEffector]] — relates_to，配合使用的末端执行器
- [[UrhoX引擎]] — relates_to，所属引擎
