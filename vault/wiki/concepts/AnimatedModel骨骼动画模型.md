---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["渲染", "动画", "骨骼动画", "3D引擎", "UrhoX", "游戏开发"]
aliases: [AnimatedModel, 骨骼模型, 蒙皮动画]
relates_to: [StaticModel静态网格体, UrhoX引擎]
supersedes: null
---
# AnimatedModel骨骼动画模型

## 概述
AnimatedModel 继承自 [[StaticModel静态网格体|StaticModel]]，支持骨骼蒙皮动画和 Morph 变形动画，通过 [[动画状态|AnimationState]] 管理多个动画轨道的混合播放。

## 关键内容
- **[[动画状态]]管理**：`AddAnimationState(animation)` 添加动画轨道，返回 [[动画状态|AnimationState]] 对象控制权重/速度
- **多动画混合**：同时添加多个 [[动画状态|AnimationState]]，通过权重混合（如走路+跑步过渡）
- **Morph 变形**：`SetMorphWeight(name, weight)` 控制顶点变形权重（用于表情等）
- **骨骼访问**：`skeleton` 属性访问[[骨骼系统|骨骼层级]]，可挂载子节点实现武器/配件附加
- **动画 LOD**：`animationLodBias` 调整动画更新频率，远处物体降低更新率节省 CPU
- **不可见更新**：`updateInvisible` 控制摄像机视锥外是否继续更新动画
- **主从模型**：`master` 属性标识主模型，多个 AnimatedModel 可共享同一骨骼

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/graphics.md]] — AnimatedModel : StaticModel API 文档

## 相关
- [[StaticModel静态网格体]] — relates_to
- [[LOD（细节层次）]] — relates_to
- [[UrhoX引擎]] — relates_to
