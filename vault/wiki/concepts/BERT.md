---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "NLP", "预训练", "Transformer", "LLM基础", "机器学习"]
aliases: ["BERT", "Bidirectional Encoder Representations from Transformers", "双向编码器表示"]
relates_to:
  - target: "[[Transformer架构]]"
    type: depends_on
    confidence: 0.95
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: depends_on
    confidence: 0.95
  - target: "[[掩码语言模型（MLM）]]"
    type: depends_on
    confidence: 0.95
  - target: "[[下一句预测（NSP）]]"
    type: depends_on
    confidence: 0.9
  - target: "[[预训练-微调范式]]"
    type: caused
    confidence: 0.95
  - target: "[[词嵌入（Word Embedding）]]"
    type: extends
    confidence: 0.9
  - target: "[[Word2Vec]]"
    type: supersedes
    confidence: 0.85
  - target: "[[编码器-解码器架构（Seq2Seq）]]"
    type: compares_to
    confidence: 0.8
  - target: "[[GPT]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Self-Attention机制]]"
    type: depends_on
    confidence: 0.95
supersedes: null
---

# BERT

## 概述

BERT（Bidirectional Encoder Representations from [[Transformer 架构|Transformer]]s）是 [[Google]] 于 2018 年提出的双向 [[Transformer 架构|Transformer]] 预训练模型，通过[[掩码语言模型（MLM）|掩码语言模型]]和[[下一句预测（NSP）|下一句预测]]任务学习深层双向语言表示，一次性刷新 11 项 NLP 基准，确立了"预训练+微调"的 NLP 标准[[规范化理论|范式]]。

## 关键内容

### 历史背景：单向语言模型的局限

2018 年 [[GPT]] 使用 [[Transformer 架构|Transformer]] Decoder 做**单向**（从左到右）语言模型预训练，只能利用左侧上下文。自然语言理解任务（情感分析、问答、NER）需要**双向**理解上下文，单向模型天然受限。[[Google]] 团队提出关键问题：能否预训练出真正双向的语言表示？

### 架构设计：纯 Transformer Encoder

BERT 本质是**纯 [[Transformer 架构|Transformer]] Encoder 堆叠**，无 Decoder：

1. **输入嵌入**：Token [[Embedding]]（[[WordPiece]] 分词，30522 个 token）+ Segment [[Embedding]]（[[区分]]句子 A/B）+ Position [[Embedding]]（可学习，非正弦）
2. **[[Transformer 架构|Transformer]] Encoder Layer × L**：[[多头注意力]] + Add & [[Layer Normalization|LayerNorm]] + Feed-Forward + Add & [[Layer Normalization|LayerNorm]]
3. **输出**：各位置的上下文化表示，每个 token 都能看到完整序列

| 配置 | 层数 L | 隐藏维度 H | 注意力头数 A | 参数量 |
|------|--------|-----------|------------|--------|
| BERT-Base | 12 | 768 | 12 | 110M |
| BERT-Large | 24 | 1024 | 16 | 340M |

### 两大预训练任务

**任务一：[[掩码语言模型（MLM）]]** — 随机掩盖 15% 的词，模型必须同时利用左右两侧上下文预测被遮盖的词，强制双向理解。15% 中 80% 替换为 [MASK]，10% 替换为随机词，10% 保持不变（防止测试集分布偏移）。

**任务二：[[下一句预测（NSP）]]** — 输入 [CLS] 句子A [SEP] 句子B [SEP]，预测 B 是否为 A 的真实下一句。让模型理解句子间关系（对 QA、NLI 任务有帮助）。后续研究（RoBERTa）发现 NSP 效果有限，可去掉。

### 微调范式："预训练+微调"

BERT 确立了 NLP 的主流[[规范化理论|范式]]（详见 [[预训练-微调范式]]）：

- **第一阶段**：大规模无监督预训练（33 亿词，MLM + NSP，自监督）
- **第二阶段**：小规模有监督微调，只需少量标注数据，添加简单任务特定输出层

下游任务适配方式：
- **单句分类**（情感分析）：[CLS] → Linear → 类别
- **句对分类**（NLI）：[CLS] 句子A [SEP] 句子B → Linear → 关系
- **序列标注**（NER）：每个 Token 位置 → Linear → 标签
- **阅读理解**（SQuAD）：两个线性层分别预测答案的起止位置

### 震撼性实验结果

2018 年 10 月，BERT 一次性刷新 11 个 NLP 基准：

| 任务 | 之前 SOTA | BERT | 提升 |
|------|---------|------|------|
| GLUE | 72.8 | 80.5 | +7.7 |
| SQuAD 1.1 F1 | 91.7 | 93.2 | +1.5（超人类！） |
| SQuAD 2.0 F1 | 76.3 | 86.3 | +10.0 |
| MultiNLI | 86.7 | 86.7（Large:90.9）| — |
| CoNLL NER F1 | 91.9 | 92.8 | +0.9 |

### 训练工程细节

- **优化器**：[[AdamW]]，β₁=0.9，β₂=0.999
- **学习率**：Warmup 10000 步 → 线性衰减
- **Batch Size**：256 sequences（最大长度 512）
- **训练步数**：1,000,000 步
- **语料**：Wikipedia（25 亿词）+ BooksCorpus（8 亿词）
- **硬件**：64 块 TPU v2，训练 4 天（BERT-Large）

### BERT 与 GPT 的对比

| 维度 | BERT（Encoder Only） | GPT（Decoder Only） |
|------|---------------------|---------------------|
| 方向性 | 双向 | 单向（[[AR 模型（自回归模型）|自回归]]） |
| 预训练任务 | MLM + NSP | [[AR 模型（自回归模型）|自回归]]语言模型 |
| 擅长领域 | 分类/NER/QA | 文本生成 |
| 上下文利用 | 完整序列 | 仅左侧 |

### 后继者谱系

BERT（2018，[[Google]]）→ RoBERTa（2019，[[Meta|Facebook]]，去掉 NSP，更大数据，动态掩码）→ DistilBERT（2019，HuggingFace，66% 参数量，97% 性能）→ ERNIE 1.0/2.0（百度，实体/知识增强）→ ALBert → DeBERTa（2020，微软）。

BERT（Encoder Only）与 GPT（Decoder Only）最终汇聚于 T5/BART（2020，Encoder+Decoder 统一框架），再演进至 GPT-3/4、Claude、[[Gemini CLI|Gemini]]（Scale Up Decoder）。

## 来源

- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — Devlin et al., NAACL 2019, arXiv 2018
- [[raw/articles/ai-papers/machine-learning/15_bert_2018.md]] — 详细解读与代码实现

## 相关

- [[Transformer架构]] — depends_on（BERT 基于纯 Transformer Encoder 构建）
- [[注意力机制（Attention Mechanism）]] — depends_on（BERT 的核心是 [[Self-Attention机制]]）
- [[掩码语言模型（MLM）]] — depends_on（BERT 的第一个预训练任务）
- [[下一句预测（NSP）]] — depends_on（BERT 的第二个预训练任务）
- [[预训练-微调范式]] — caused（BERT 确立了这一 NLP 标准范式）
- [[词嵌入（Word Embedding）]] — extends（从静态词向量到上下文相关词向量）
- [[Word2Vec]] — supersedes（BERT 的上下文词向量取代了 Word2Vec 的静态词向量）
- [[编码器-解码器架构（Seq2Seq）]] — compares_to（BERT 只用 Encoder，Seq2Seq 用 Encoder+Decoder）
- [[GPT]] — compares_to（双向 vs 单向，理解 vs 生成）
- [[Self-Attention机制]] — depends_on（BERT 的核心计算模块）
