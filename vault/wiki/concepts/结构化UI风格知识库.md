---
type: concept
title: "结构化 UI 风格知识库"
status: active
confidence: 0.88
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [UI, 设计, AI, 知识库, 设计系统]
aliases:
  - UI风格体系
  - 可机器处理的风格知识
  - styles.csv
relates_to:
  - target: "[[UI-UX-Pro-Max]]"
    type: part_of
    confidence: 0.95
  - target: "[[AI设计推理层]]"
    type: related_to
    confidence: 0.9
supersedes: null
---

# 结构化 UI 风格知识库

## 概述

结构化 UI 风格知识库是将每种 UI 视觉风格编码为**可机器检索和直接输出的结构化记录**的设计模式：除风格描述外，每条记录携带 AI Prompt 关键词、CSS 变量模板、实现检查清单和反模式警告，使 AI 能直接生成代码而非仅作风格推荐。

## 关键内容

### 数据结构（UUPM styles.csv v2.2+）

```
id, name, category, best_for, keywords, description,
performance, accessibility,
ai_prompt_keywords,         ← AI Prompt 提示词（直接复制）
css_keywords,               ← CSS 实现关键词
implementation_checklist,   ← 可操作实现清单
design_system_variables     ← CSS 自定义属性模板
```

### 三层分类体系（67 种风格）

```
67 种 UI 风格
├── 通用风格（49 种）   ← 覆盖从复古到前沿的核心风格库
├── 落地页风格（8 种）  ← 按转化策略分类（Hero-Centric / Conversion-Optimized 等）
└── BI 仪表板风格（10 种）← 数据可视化专项
```

### 代表性风格示例

| 风格 | 特征 | 典型场景 | 关键限制 |
|------|------|---------|---------|
| Glassmorphism | `backdrop-filter: blur()` 磨砂玻璃 | SaaS、金融仪表板 | 低端设备需降级方案 |
| Neumorphism | 双向 `box-shadow` 凸起/凹陷 | 健康/wellness | 只适合浅色单色背景 |
| Brutalism | 粗边框、非对称、高对比色 | 设计师作品集 | 受众极为特定 |
| Claymorphism | 内部高光 + 外部阴影模拟黏土质感 | 教育、SaaS Onboarding | 2022 年兴起 |
| AI-Native UI | 打字机效果、脉冲加载、流式渲染 | AI 产品、Chatbot | 高信任场景禁用（银行/医疗） |
| Spatial UI / VisionOS | 玻璃窗口、三维空间感、凝视交互 | VR/AR | Apple Vision Pro 引领 |
| Liquid Glass | 流动有机边缘、彩虹折射 | 高端 SaaS、奢侈电商 | SVG feTurbulence 技术 |

### 风格选择决策流

```
用户输入 → 匹配产品类型 → 行业黑名单过滤（反模式）
→ BM25 相关性排序 → 输出 Top 3 推荐 + 理由
```

金融类产品：排除 AI-Native UI（信任问题）；儿童类：排除 Brutalism / Cyberpunk。

### 关键设计原则

传统设计资源只告诉 AI「用玻璃拟态」，结构化知识库让 AI 同时得到：
1. **为什么**用这种风格（产品类型匹配逻辑）
2. **怎么实现**（CSS 变量、检查清单）
3. **不能做什么**（反模式警告）

这是该知识库比自然语言描述效果好 10 倍的根本原因。

## 来源

- [[raw/articles/UI-skill/blog-02-styles.md]]

## 相关

- [[UI-UX-Pro-Max]] — 该知识库的宿主系统
- [[AI设计推理层]] — 知识库驱动的设计推理架构
