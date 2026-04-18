---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "NLP", "预训练", "语言模型", "LLM基础"]
aliases: ["Masked Language Model", "MLM", "掩码语言模型", "填空语言模型"]
relates_to:
  - target: "[[BERT]]"
    type: part_of
    confidence: 0.95
  - target: "[[Word2Vec]]"
    type: extends
    confidence: 0.85
  - target: "[[词嵌入（Word Embedding）]]"
    type: extends
    confidence: 0.9
  - target: "[[下一句预测（NSP）]]"
    type: compares_to
    confidence: 0.8
  - target: "[[自注意力机制]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# 掩码语言模型（MLM）

## 概述

掩码语言模型（Masked Language Model, MLM）是 BERT 的核心预训练任务，通过随机掩盖输入序列中 15% 的词并让模型预测被遮盖的词，强制模型同时利用左右两侧上下文，实现真正的双向语言理解。

## 关键内容

### 核心机制

MLM 的工作流程：

1. **随机掩盖**：从输入序列中随机选择 15% 的词进行掩盖
2. **模型预测**：模型根据未被掩盖的上下文预测被遮盖的词
3. **损失计算**：仅对被掩盖位置的预测计算[[二元交叉熵|交叉熵损失]]

```
原始句子：The cat sat on the mat
          ↓ 随机掩盖 15% 的词
输入序列：The cat [MASK] on the mat
预训练目标：预测被遮盖的词 "sat"

→ 模型必须同时利用 "The cat"（左侧）和 "on the mat"（右侧）
→ 强制双向理解！
```

### 15% 掩盖策略的细节分配

为防止微调时出现分布偏移（测试集中没有 [MASK] token），15% 被选中的词按以下比例处理：

| 比例 | 处理方式 | 示例 |
|------|---------|------|
| 80% | 替换为 [MASK] | "The cat [MASK] on the mat" |
| 10% | 替换为随机词 | "The cat apple on the mat" |
| 10% | 保持不变 | "The cat sat on the mat" |

这种混合策略使模型：
- 80% 学习利用上下文预测 [MASK]
- 10% 学习处理噪声输入（增强鲁棒性）
- 10% 学习保持原始表示（防止 [MASK] 分布偏移）

### 与 Word2Vec CBOW 的关系

MLM 可视为 [[Word2Vec]] 中 CBOW（Continuous Bag of Words）的**深度化扩展**：
- CBOW：用周围词的**平均嵌入**预测中心词（浅层线性模型）
- MLM：用深层 [[Transformer架构]] 编码的上下文化表示预测中心词（非线性、多层、[[Self-Attention机制|自注意力]]）

### 动态掩码 vs 静态掩码

- **BERT 原始方案**：每次训练时动态生成掩码（每次看到的掩盖模式不同）
- **后续优化**（RoBERTa）：确认动态掩码的重要性，静态预掩码会限制模型看到的上下文组合

### 在 BERT 中的作用

MLM 是 [[BERT]] 两大预训练任务之一（另一个是 [[下一句预测（NSP）]]）。MLM 负责学习词级别的语义表示，NSP 负责学习句子级别的关系理解。后续研究表明 MLM 是核心有效组件，NSP 的贡献有限。

### 后继影响

MLM [[规范化理论|范式]]被后续多个模型采用：RoBERTa、DistilBERT、ALBert、DeBERTa、XLM-R 等。MLM 也成为评估语言模型双向理解能力的标准预训练任务。

## 来源

- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — 首次提出 MLM 预训练任务
- [[raw/articles/ai-papers/machine-learning/15_bert_2018.md]] — MLM 机制详解与代码实现

## 相关

- [[BERT]] — part_of（MLM 是 BERT 的核心预训练任务）
- [[Word2Vec]] — extends（MLM 是 CBOW 的深度化扩展）
- [[词嵌入（Word Embedding）]] — extends（MLM 学习上下文相关的词嵌入）
- [[下一句预测（NSP）]] — compares_to（BERT 的另一预训练任务，句子级别 vs 词级别）
- [[自注意力机制]] — depends_on（MLM 依赖自注意力实现双向上下文编码）
