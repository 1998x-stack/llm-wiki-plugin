---
type: entity
entity_type: project
status: active
confidence: 0.82
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI工程]
aliases: ["MetaFind 3D检索", "ESSGNN"]
relates_to:
  - target: "[[多模态检索]]"
    type: implements
    confidence: 0.9
  - target: "CLIP"
    type: uses
    confidence: 0.85
  - target: "[[Modality Gap]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# MetaFind

## 概述

MetaFind 是元宇宙/3D 场景感知的多模态资产检索系统，核心创新是 ESSGNN（场景感知等变图编码器）+ ULIP-2 三模态对齐，实现文本/图片/3D 模型任意组合查询，并能感知场景上下文（已有家具的风格/尺寸/功能关系）。

## 关键内容

1. **[[双塔模型|双塔架构]]**：
   - **画廊编码器（Gallery Encoder）**：提前编码所有 3D 资产（3D 形状+图像+文字描述）生成"数字暗号"（向量），离线存储
   - **查询编码器（Query Encoder）**：将用户输入（文本/图片/3D 草稿任意组合）编码为同格式向量
   - **ULIP-2**：统一翻译器，使文本/图片/3D 三模态向量可互相比较（三模态[[对比学习]]对齐）

2. **核心创新 ESSGNN（Scene-Aware Equivariant Graph [[场景树|Scene Graph]] Neural Network）**：
   - 将已有场景布局建模为图（节点=家具，节点特征=尺寸+风格+3D 位置，边=空间关系+功能关系）
   - 保持 **SE(3) 等变性**：无论场景如何旋转/平移，相对关系保持不变（沙发在电视前方始终正确）
   - 让查询编码器能"读懂整个场景上下文"，推荐与已有家具风格/尺寸/功能匹配的资产

3. **训练策略**：两阶段训练（先学基础跨模态对齐，再针对场景感知微调）+ 鲁棒性优化（随机遮挡部分节点，防止过拟合）。

4. **参考论文**：ESSGNN 相关论文 arXiv:2510.04057（2.5 ESSGNN: Scene-Aware Equivariant Graph Encoder）。

5. **典型应用场景**：元宇宙装修助手——用户上传已有家具图片/3D 模型/文字描述，系统在资产库中找风格/功能/尺寸匹配的搭配建议。

## 来源

- `raw/articles/ai-engineering/search-retrieval/MetaFind.md`

## 相关

- [[多模态检索]] — implements
- CLIP — uses（ULIP-2 基于 CLIP 思路扩展）
- [[Modality Gap]] — compares_to
