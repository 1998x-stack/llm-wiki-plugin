---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, multimodal, CLIP, 机器学习]
aliases: [Radford et al. 2021, CLIP 论文]
relates_to:
  - target: Alec Radford
    relation: authored_by
  - target: CLIP
    relation: introduced
  - target: 零样本学习
    relation: demonstrated
supersedes: null
---

# Learning Transferable Visual Models From Natural Language Supervision (2021 论文)

## 概述
提出 CLIP 模型的论文，通过[[CLIP|对比语言-图像预训练]]实现[[零样本学习|零样本]]视觉理解。

## 关键内容

1. **[[对比学习]]**：训练图像和文本编码器，使匹配的图文对在嵌入空间中靠近，不匹配的远离。
2. **[[零样本学习|零样本]]迁移**：CLIP 可以在未见过的类别上进行[[零样本学习|零样本]]分类，只需提供类别名称的文本描述。
3. **多模态对齐**：建立了文本和视觉的统一表示空间，为 [[DALL-E]] 等文生图模型奠定基础。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[Alec Radford]] — authored_by
- [[CLIP]] — introduced
- [[零样本学习]] — demonstrated
- [[DALL-E]] — relates_to
