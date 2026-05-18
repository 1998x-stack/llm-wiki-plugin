---
type: map
topic: "LLM能力"
page_count: 51
updated: 2026-05-18
---

# LLM能力

## 概述

LLM能力 相关概念与实体的集群。核心主题：AI Slop、AI 寒冬、Batch Normalization、Beam Search 生成。

## 概念

- [[AI Slop]] — AI 生成的前端界面高度同质化现象，表现为千篇一律的字体、配色、布局和缺乏记忆点的"模板感"设计。 (confidence: 0.9)
- [[AI 寒冬]] — AI 寒冬指 1969 年 [[Marvin Minsky|Minsky]]-[[Seymour Papert|Papert]]《[[Perceptrons ( (confidence: 0.85)
- [[Batch Normalization]] — 在一个 batch 上对某一特征维度统计均值和方差并做归一化，解决[[内部协变量偏移]]问题。在 CNN 中广泛使用，使训练速度提升 14 倍，大幅降低对初始化 (confidence: 0.95)
- [[Beam Search 生成]] — [[P5 论文]]使用的推理方法，通过 beam size=20 的束搜索[[AR 模型（自回归模型）|自回归]]生成物品 ID 或文本，是 LLM 推荐的核心 (confidence: 0.8)
- [[Compact Instructions]] — [[上下文压缩（Context Compaction）|Compact]] Instructions 是 [[CLAUDE.md]] 中定义的压缩策略，用于在[ (confidence: 0.8)
- [[Context Engineering]] — 多步骤系统中信息流的全局架构设计方法论，与[[Prompt-Engineering|提示词工程]]（单次调用措辞优化）本质不同，关注如何为每个[[Subagen (confidence: 0.9)
- [[Context Rot]] — LLM 在[[上下文窗口]]逐渐填满后，生成质量系统性降级的物理现象，表现为[[注意力预算|注意力稀释]]、风格漂移、幻觉决策等问题。 (confidence: 0.9)
- [[Diffie-Hellman 密钥交换协议]] — 人类历史上第一个公钥密钥交换协议，允许两个此前从未接触过的用户通过不安全的公开信道建立共享秘密，基于离散对数问题的数学困难性实现安全性。 (confidence: 0.9)
- [[HyDE]] — HyDE（Hypothetical Document Embeddings，假设文档嵌入）是一种零样本稠密检索方法，通过生成假设文档来改善向量检索效果，与上下文 (confidence: 0.75)
- [[LATM]] — LATM（[[Language-Model|Large Language Model]]s as Tool Makers）是由Cai等人提出的概念，提出双LLM (confidence: 0.75)
- [[LLM-Skill-技术全景]] — LLM [[Skills|Skill]]技术是指让大型[[Language-Model|语言模型]]能够调用外部工具、使用API以及执行具体任务的工程技术体系。 (confidence: 0.8)
- [[LLM-工程三阶段]] — LLM 工程的三个发展阶段：从 [[Prompt Engineering]]（[[Prompt Engineering|提示工程]]）到 [[Context E (confidence: 0.9)
- [[LLM-工程三阶段对比分析]] — 对比分析 [[Prompt Engineering]]、[[Context Engineering]] 和 [[Harness-Engineering|Harn (confidence: 0.8)
- [[LLM推理策略]] — LLM推理策略是一套用于优化大型[[Language-Model|语言模型]]调用频率和成本的技术方案，通过频率控制和智能复用来减少不必要的API调用。 (confidence: 0.8)
- [[Layer Normalization]] — 对单个样本内部的特征维度做标准化，稳定网络中的数值分布，使训练更稳定。是 [[Transformer架构|Transformer]] 的基础组件，不依赖 bat (confidence: 0.92)
- [[Mixture-of-Experts]] — Mixture-of-Experts(MoE)是一种深度学习架构，训练多个小型专家网络处理输入空间不同区域，通过[[门控机制（Gating Mechanism） (confidence: 0.85)
- [[Prompt 缓存]] — [[Hermes Agent]] 为 [[Anthropic]] API 模式实现的[[KV 缓存命中率|前缀缓存]]机制，标记 System Prompt 中 (confidence: 0.5)
- [[Self-Attention机制]] — Self-Attention（自注意力）是 [[Transformer架构|Transformer]] 的核心机制，让序列中每个位置根据内容动态关注其他所有位置 (confidence: 0.9)
- [[Token 经济学]] — Token 经济学研究在 LLM [[上下文窗口]]有限的约束下，如何最大化单位 token 的信息传递效率，是 AI 记忆系统和 RAG 架构的核心优化维度。 (confidence: 0.5)
- [[Transformer架构]] — [[Transformer 架构|Transformer]] 是 2017 年提出的序列到序列神经网络架构，以 [[Self-Attention机制]] 替代  (confidence: 0.85)
- [[上下文检索]] — 上下文检索（Contextual Retrieval）是 Anthropic 提出的一种 RAG 改进方法，通过在文本块嵌入和索引前添加语境化解释前缀，解决传统 (confidence: 0.9)
- [[上下文策略]] — 上下文策略是一组针对 L[[LM Agent]] [[上下文窗口]]管理的系统化方法，将上下文视为需要 malloc/free 的内存资源，通过[[固定栈分配] (confidence: 0.85)
- [[上下文管理系统]] — [[Context Management|上下文管理]]系统是[[Claude Code]]中用于管理和优化AI模型[[上下文窗口]]的机制，包括自动压缩、层级 (confidence: 0.8)
- [[上下文预算管理]] — 上下文预算管理是在编写 [[CLAUDE.md]] 等 Agent 提示词时，预先估算各部分 token 消耗并确保总量在安全范围内的策略，目标是保持上下文使用 (confidence: 0.8)
- [[令牌计数（Token Counting）]] — [[Anthropic]] API 的 `/v1/messages/count_tokens` 端点，用于在发送消息给 [[Claude_Code|Claude (confidence: 0.85)
- [[位置编码]] — 位置编码（Positional Encoding）是 [[Transformer架构|Transformer]] 中补充序列顺序信息的机制。[[Self-Att (confidence: 0.92)
- [[冻结快照模式]] — [[Hermes Agent|Hermes]] 记忆系统的关键设计决策：会话开始时将 [[语义记忆|MEMORY.md]] 和 USER.md 加载为冻结快照注 (confidence: 0.7)
- [[冻结快照设计]] — [[Hermes Agent]] 的 Prompt 组装策略：[[语义记忆|MEMORY.md]] 和 USER.md 在会话开始时捕获一次，整个会话期间不变， (confidence: 0.5)
- [[因果掩码]] — 因果掩码（Causal Masking）是 [[Transformer架构|Transformer]] 中实现[[AR 模型（自回归模型）|自回归]]预测的关键 (confidence: 0.9)
- [[固定提示栈（Fixed Prompt Stack）]] — 固定提示栈是一种 Agent 上下文分配模式，每次迭代向 Agent 注入完全相同的完整规范内容（[[CLAUDE.md]]），以"浪费性重复"为代价换取零 [ (confidence: 0.8)
- [[固定栈分配]] — 固定栈分配是[[上下文策略]]之一，要求每次 Agent 迭代以完全相同的顺序和方式分配上下文栈，确保关键约束始终位于注意力最高的开头和结尾位置，避免"lost (confidence: 0.8)
- [[多头注意力]] — 多头注意力（Multi-Head Attention）在 h 个独立子空间中并行执行 [[Self-Attention机制]]，再拼接并线性变换，使模型同时捕获 (confidence: 0.9)
- [[大语言模型与计算边界]] — 探讨大[[Language-Model|语言模型]]（LLM）在[[图灵机]]和[[Church-Turing论题]]所划定的[[计算]]边界内的能力与局限性， (confidence: 0.7)
- [[实体缩写]] — 实体缩写是 [[AAAK 方言]]中的核心压缩机制，通过在文档首次出现时建立实体到缩写的映射，后续全部使用缩写，在大规模重复实体场景下实现 30:1 的压缩比。 (confidence: 0.5)
- [[掩码语言模型（MLM）]] — 掩码[[Language-Model|语言模型]]（Masked Language Model, MLM）是 BERT 的核心预训练任务，通过随机掩盖输入序列中 (confidence: 0.95)
- [[残差连接]] — 将子层输入直接加到子层输出上：$x + \text{Sublayer}(x)$，缓解深层网络[[梯度消失]]问题，是 [[Transformer架构|Trans (confidence: 0.85)
- [[相对位置编码]] — 相对[[位置编码]]关注两个 token 之间相隔多远，而非各自处于第几位。位置信息直接注入注意力分数[[计算]]，使模型在决定"该关注谁"时显式考虑相对距离  (confidence: 0.9)
- [[知识社会学]] — 研究知识与社会结构关系的理论传统，分析知识如何被社会位置、权力关系与历史条件所塑造。 (confidence: 0.9)
- [[绝对位置编码]] — 绝对[[位置编码]]直接告知模型当前 token 处于第几个位置。分固定式（正弦/余弦公式）和可学习式两种，是原始 [[Transformer架构|Transf (confidence: 0.9)
- [[缩放点积注意力]] — 缩放[[Luong注意力|点积注意力]]（Scaled Dot-Product Attention）是 [[Transformer架构|Transformer] (confidence: 0.88)
- [[自注意力机制]] — [[Self-Attention机制|Self-Attention]]（[[Self-Attention机制|自注意力]]）是 [[Transformer架构| (confidence: 0.88)
- [[词向量（Word Embedding）]] — 将离散词汇映射为稠密低维连续向量空间中的表示，捕捉语义和语法相似性。 (confidence: 0.95)

## 实体

- [[Claude-Haiku-4-5]] — [[Claude_Code|Claude]] Haiku 4.5 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] Haik (confidence: 0.9)
- [[Claude-Mythos-Preview]] — [[Claude_Code|Claude]] Mythos Preview 是 [[Anthropic]] 发布的预览版 [[Claude_Code|Claud (confidence: 0.85)
- [[Claude-Opus-4-6]] — [[Claude_Opus_4.6|Claude Opus 4.6]] 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] O (confidence: 0.9)
- [[Claude-Sonnet-3-7]] — [[Claude_Code|Claude]] Sonnet 3.7 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] Son (confidence: 0.9)
- [[Claude-Sonnet-4]] — [[Claude_Code|Claude]] Sonnet 4 是 [[Anthropic]] 已弃用的 [[Claude_Code|Claude]] Sonn (confidence: 0.8)
- [[Claude-Sonnet-4-5]] — [[Claude-Sonnet-4|Claude Sonnet 4]].5 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] (confidence: 0.9)
- [[Claude-Sonnet-4-6]] — [[Claude-Sonnet-4|Claude Sonnet 4]].6 是 [[Anthropic]] 发布的 [[Claude_Code|Claude]] (confidence: 0.9)
- [[Martin E. Hellman]] — 美国电气工程师和密码学家，斯坦福大学教授，公钥密码学的共同创始人之一。与Whitfield Diffie合作发表了改变密码学历史的《New Directions (confidence: 0.95)
- [[T5]] — [[Google]] 提出的 Text-to-Text Transfer [[Transformer架构|Transformer]]，将所有 NLP 任务统一为 (confidence: 0.9)
