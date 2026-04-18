---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [深度学习, 架构模式, 推荐系统, 大语言模型, LLM能力]
aliases: [MoE, 混合专家模型, Mixture of Experts]
relates_to: [MMoE, 多任务学习, 大语言模型]
supersedes: null
---

# Mixture-of-Experts

## 概述
Mixture-of-Experts(MoE)是一种深度学习架构，训练多个小型专家网络处理输入空间不同区域，通过[[门控机制（Gating Mechanism）|门控]]网络决定各专家意见的权重。

## 关键内容

### 核心思想
- 概念源自 Jacobs 等人 1991 年的工作："Adaptive mixtures of local experts"
- 与其训练一个大型网络处理所有情况，不如训练多个小型专家网络各自擅长不同区域
- [[门控机制（Gating Mechanism）|门控]]网络(Gating Network)决定对给定输入应咨询哪些专家及各专家权重
- 数学表达：`y = Σ g(x)_i * f_i(x)`，其中 `g(x)` 通过 softmax 产生，权重和为 1

### 从 MoE 到多任务学习的演进
- **OMoE**(One-gate MoE)：将 MoE 应用于[[多任务学习]]的直接方式，所有任务共享同一[[门控机制（Gating Mechanism）|门控]]网络
- **MMoE**(Multi-gate MoE)：为每任务配备独立[[门控机制（Gating Mechanism）|门控]]网络，实现任务特定的专家选择
- MMoE 相比 Shared-Bottom 的进步：将底层网络模块化，不同输入激活不同专家组合

### 在大模型时代的复兴
- 2024-2025 年 MoE 架构成为大模型领域最热门技术方向之一
- **Mixtral 8x7B**(Mistral AI, 2024)：总参数 47B，每 token 仅激活 13B，匹敌 LLaMA-2-70B
- **DeepSeek-V3/R1**(2024-2025)：总参数 671B，活跃参数仅 37B，采用多级 MoE 设计
- **Qwen3-235B**(阿里巴巴, 2025)：235B 总参数，22B 活跃参数，128 个专家中 top-8 路由
- **GPT-5**([[OpenAI]], 2025)：从稠密 [[Transformer架构|Transformer]] 转向 MoE 架构，标志 MoE 成为主流

### LLM 中的 MoE vs 推荐系统中的 MoE
- LLM 中：token 级别的稀疏路由，通常使用 top-k [[门控机制（Gating Mechanism）|门控]]
- 推荐系统中(MMoE)：样本级别的软路由，所有专家都有非零权重
- 核心思想一脉相承：用[[门控机制（Gating Mechanism）|门控]]/路由机制决定哪些专家处理当前输入

### 未解之题
- **专家特化 vs 专家冗余**：如何确保不同专家学到不同知识而非彼此重复
- **路由优化不稳定性**：[[门控机制（Gating Mechanism）|门控]]/路由网络训练是否稳定，是否出现负载不均衡
- **最优专家数量**：给定计算预算，应设置多少专家，每次激活多少
- 这些问题跨越推荐系统和大模型两个领域，构成 MoE 研究的核心挑战

## 来源
- raw/books/推荐系统/14-mmoe.md — MMoE 深度解读文章，包含 MoE 历史和大模型时代复兴

## 相关
- MMoE — MoE 在多任务学习中的关键应用
- [[多任务学习]] — MoE 的重要应用领域
- 大语言模型 — MoE 在大模型时代的规模化复兴
