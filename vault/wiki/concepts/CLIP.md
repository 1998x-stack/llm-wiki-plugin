---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [multimodal, "computer vision", nlp, "contrastive learning", 机器学习]
aliases: ["CLIP", "Contrastive Language-Image Pre-training", "对比语言-图像预训练"]
relates_to:
  - target: "[[Learning Transferable Visual Models from Natural Language Supervision (2021 论文)]]"
    type: described_in
  - target: "[[Alec Radford]]"
    type: created_by
  - target: "[[OpenAI]]"
    type: developed_at
  - target: "[[零样本学习]]"
    type: enables
  - target: "[[Multimodal Learning]]"
    type: exemplifies
  - target: "[[Contrastive Learning]]"
    type: uses
  - target: "[[DALL-E]]"
    type: relates_to
supersedes: null
---

# CLIP

## 概述
CLIP（Contrastive Language-Image Pre-training）是一种[[多模态模型]]，通过[[对比学习]][[联合训练]]图像和文本编码器，实现图文匹配和[[零样本学习|零样本]]视觉识别。

## 关键内容

1. **[[对比学习]]架构**：CLIP使用[[双塔模型|双塔架构]]，分别训练图像编码器和文本编码器，通过对比损失函数使匹配的图文对在嵌入空间中距离更近，不匹配的图文对距离更远。

2. **[[零样本学习|零样本]]能力**：经过大规模图文对训练后，CLIP能够对未见过的图像分类任务实现[[零样本学习|零样本]]迁移，仅需提供类别名称而无需额外训练。

3. **应用影响**：CLIP为多模态AI开辟了新的方向，影响了后续的[[DALL-E]]、GPT-4 Vision等多种[[多模态模型]]的设计思路。

4. **[[对比学习]]**：训练图像和文本编码器，使匹配的图文对在嵌入空间中靠近，不匹配的远离。

5. **[[零样本学习|零样本]]分类**：CLIP 可以在未见过的类别上进行[[零样本学习|零样本]]分类，只需提供类别名称的文本描述。

6. **多模态对齐**：建立了文本和视觉的统一表示空间，为 [[DALL-E]] 等文生图模型奠定基础。

## 来源
- [[ai_papers_timeline.md]] — 2021年CLIP提出
- [[Learning Transferable Visual Models from Natural Language Supervision (2021 论文)]] — Alec Radford等人在OpenAI的研究

## 相关
- [[Learning Transferable Visual Models from Natural Language Supervision (2021 论文)]] — described_in
- [[Alec Radford]] — created_by
- [[OpenAI]] — developed_at
- [[零样本学习]] — enables
- [[Multimodal Learning]] — exemplifies
- [[Contrastive Learning]] — uses
- [[DALL-E]] — relates_to