# LLM Skill 技术全景：工具调用、技能文件与 Agent 编排
> 论文调研系列 · 共 8 篇 · 2024–2025

---

## 系列导读

本系列从学术论文出发，系统梳理 LLM Skill / Tool Use 领域的核心研究脉络，最终落地到工程实践——尤其是 Claude Code `.skill` 文件的设计哲学。

| 篇次 | 标题 | 核心论文 |
|------|------|---------|
| 01 | 为什么 LLM 需要 Skill？演化全景 | ReAct、MRKL、Toolformer |
| 02 | 工具调用基础：LLM 如何学习使用 API | Toolformer、ToolkenGPT、Gorilla |
| 03 | 技能库范式：持久化存储与复用 | Voyager、GITM、SkiLL-iT |
| 04 | LLM as Tool Maker：让模型自造工具 | LATM、CRAFT、Creator |
| 05 | 大规模工具检索：泛化与对齐 | ToolBench/ToolLLM、AnyTool、API-Bank |
| 06 | 任务规划与技能编排 | HuggingGPT、AssistGPT、TaskBench |
| 07 | 代码即技能：可执行动作统一范式 | CodeAct、OpenAgents、AgentBench |
| 08 | 工程实践：Claude Code .skill 文件设计哲学 | 综合工程分析 |

---

# 第 01 篇：为什么 LLM 需要 Skill？从 ReAct 到 .skill 文件的演化全景

## 1.1 核心问题：纯 LLM 的认知边界

大型语言模型在参数中压缩了海量世界知识，但在实际部署中暴露出几个根本性局限：

**知识截止问题（Knowledge Cutoff）**：训练数据有截止日期，模型无法感知"今天的股价""最新的 API 版本"。

**幻觉问题（Hallucination）**：对精确计算、代码执行、数据库查询等需要确定性答案的任务，模型倾向于"编造"合理但错误的答案。

**上下文窗口限制**：即使 128K token 的上下文也无法容纳整个代码库、整个文档集合。

**无状态性**：单次推理无法"记住"上一步的执行结果并动态调整后续行为。

这些局限催生了一个核心设计模式：**将 LLM 从知识库变成控制器（Controller），通过调用外部工具（Tool / Skill）来弥补自身短板**。

---

## 1.2 第一代：工具增强的朴素尝试（2021–2022）

### MRKL Systems（Modular Reasoning, Knowledge and Language）

**论文**：Karpas et al., "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning", 2022.

MRKL 是最早系统性提出"神经符号混合"架构的工作之一。核心思想：

```
用户查询 → LLM Router → 路由到专家模块（计算器/数据库/搜索引擎）→ 汇总回答
```

MRKL 的局限：路由逻辑是硬编码的，LLM 本身不"理解"何时应该调用哪个模块，更像是规则系统而非真正的 Agent。

---

### WebGPT（OpenAI, 2021）

**论文**：Nakano et al., "WebGPT: Browser-assisted question-answering with human feedback", 2021.

WebGPT 是首批将"工具调用"与 RLHF 结合的工作。模型通过人类反馈学习：
- 何时触发搜索（`search("query")`）
- 如何点击链接、提取摘要
- 如何整合多源信息生成引用式回答

**启示**：工具调用不仅是工程问题，也是**学习问题**——模型需要学会"工具使用策略"。

---

## 1.3 第二代：ReAct 范式的统一（2022）

### ReAct: Synergizing Reasoning and Acting

**论文**：Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023.

ReAct 是整个 Skill/Tool Use 领域的**范式奠基论文**。

**核心贡献**：将 Chain-of-Thought（推理轨迹）与动作执行（Action）交织在同一序列中：

```
Thought: 需要查询当前天气数据
Act: search("北京今日天气")
Obs: 北京今日多云，气温 12°C
Thought: 已获得数据，可以回答用户
Act: finish("北京今日多云，气温 12°C")
```

**为何重要**：
- Thought 提供可解释的推理轨迹
- Act 与真实环境交互，获取 Obs 作为"ground truth"反馈
- 解决了纯 CoT 的幻觉问题（观测结果来自外部，不是模型生成的）

**实验结果**：在 HotpotQA、Fever、AlfWorld、WebShop 上均优于单纯 CoT 或单纯 Act。

**局限**：ReAct 是 prompting 框架，不涉及如何**定义**和**组织**技能库。

---

## 1.4 第三代：技能的系统化（2023）

从 2023 年开始，研究社区的关注点从"如何让 LLM 调用工具"转向更深层的问题：

- **技能从哪来？**（Tool Creation vs Tool Retrieval）
- **技能如何存储？**（Skill Library / Memory）
- **技能如何复用？**（Generalization）
- **谁来定义技能的边界？**（Granularity）

这三个问题催生了本系列后续六篇论文覆盖的三条研究路线：

```
                    ┌─────────────────────────────────────┐
                    │         LLM Skill 研究路线图          │
                    └─────────────────────────────────────┘
                              
  工具调用基础          技能库建设           工具生成            大规模工具           任务编排
  ──────────          ──────────           ──────────          ──────────          ──────────
  Toolformer          Voyager              LATM               ToolBench           HuggingGPT
  ToolkenGPT          GITM                 CRAFT              AnyTool             AssistGPT
  Gorilla             SkiLL-IT             Creator            API-Bank            TaskBench
                                                                                   
                          ↓                    ↓                    ↓
                    ┌─────────────────────────────────────┐
                    │    CodeAct / OpenAgents              │
                    │    代码即统一技能格式                  │
                    └─────────────────────────────────────┘
                                      ↓
                    ┌─────────────────────────────────────┐
                    │    Claude Code .skill 工程实践         │
                    └─────────────────────────────────────┘
```

---

## 1.5 Claude Code .skill 文件：学术研究的工程投影

在深入各篇论文之前，先建立参照系。Claude Code 的 `.skill` 文件是一种具体的工程实现，其设计决策与学术研究形成了有趣的对应关系：

```markdown
# 一个典型的 .skill 文件结构（以 manim-math/SKILL.md 为例）

---
name: manim-math
description: [触发条件描述]
---

## 技能概述
## 核心工作流
## 代码模板
## 约束规则
```

这对应了学术研究中的核心概念：
- **description** → Tool Retrieval 的向量嵌入锚点（见第 05 篇）
- **工作流** → Voyager 的 Skill Program（见第 03 篇）
- **代码模板** → CRAFT 的可复用代码块（见第 04 篇）
- **约束规则** → 安全护栏与 Few-shot 示例

> **本系列的核心目标**：理解每一篇论文，然后在第 08 篇中回答：当你设计 `.skill` 文件时，你其实在做什么？

---

# 第 02 篇：工具调用基础——LLM 如何学习使用 API

## 2.1 三篇奠基论文概览

| 论文 | 核心问题 | 方法 | 关键创新 |
|------|---------|------|---------|
| Toolformer | 模型能否自学工具调用？ | 自监督数据生成 + 语言模型微调 | 无需大量人工标注 |
| ToolkenGPT | 工具能否成为词汇表的一部分？ | 工具嵌入 token 化 | 推理时插入工具 |
| Gorilla | 如何让模型正确调用真实 API？ | 检索增强微调 | API 文档 → 函数调用 |

---

## 2.2 Toolformer：自学使用工具的语言模型

**论文**：Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools", NeurIPS 2023.

### 核心动机

标注"何时调用工具、调用参数是什么"的数据成本极高。Toolformer 提出：**让模型自己生成工具调用标注**。

### 方法详解

**Step 1：生成候选标注**

给定一个语料文本，用 few-shot prompt 让模型在合适位置插入 API 调用：

```
输入文本："法国首都是巴黎，人口约为 [Q(法国首都人口)] 210 万..."
候选插入：[Calculator(210*10000)] → 2,100,000
```

支持的工具类型：
- `Calculator(expr)` → 数学计算
- `WikiSearch(query)` → 百科检索  
- `MT(text, lang)` → 机器翻译
- `Calendar()` → 日期查询
- `QA(question)` → 问答

**Step 2：过滤有效标注**

对每个候选标注，计算：

```
L_i(z) = -sum(log P(t_j | t_1...t_{i-1}, z, e(c_i), t_{i+1}...))
```

即：插入工具调用后，后续 token 的预测损失是否降低？只保留"有帮助"的工具调用。

**Step 3：微调模型**

用过滤后的标注数据微调 GPT-J 6.7B，使模型学会"何时、如何"插入工具调用。

### 关键实验结果

在只使用 GPT-J 6.7B（远小于 GPT-3 175B）的情况下：
- 数学计算任务：超过 175B 的 GPT-3
- 问答任务：显著优于相同参数量的基线

### 对 .skill 设计的启示

Toolformer 的过滤标准（"调用后损失是否降低"）等价于问：**这个技能文件是否真的降低了任务难度？** 这是评估 `.skill` 文件质量的核心标准。

---

## 2.3 ToolkenGPT：工具作为特殊 Token

**论文**：Hao et al., "ToolkenGPT: Augmenting Frozen Language Models with Massive Tools via Tool Embeddings", NeurIPS 2023.

### 核心创新

Toolformer 需要微调整个模型。ToolkenGPT 提出：**冻结 LLM，只训练"工具 token 的嵌入向量"**。

每个工具被表示为词汇表中的一个特殊 token（toolken）：

```
词汇表扩展：[...正常词汇...] + [<calc>] + [<search>] + [<get_weather>] + ...
```

推理时，当模型生成了某个 toolken，就触发对应工具的执行。

### 架构设计

```
LLM（冻结）
    ↓
输出 logits over [普通词汇 ∪ 工具 token]
    ↓
若生成工具 token t_k：
    → 解析参数（仍由 LLM 生成）
    → 执行工具
    → 将结果注入上下文
    ↓
继续生成
```

Toolken 嵌入的训练目标：在包含工具调用的示范数据上，最大化工具 token 在正确位置出现的概率。

### 优势

1. **可扩展到海量工具**：只需为每个新工具训练一个 ~embedding_dim 大小的向量
2. **模型不变**：不需要对每种工具组合重新微调
3. **工具动态添加**：新工具 = 新 toolken，不影响已有能力

### 局限

工具嵌入的训练仍需要该工具的示范数据，在零样本工具上表现受限。

---

## 2.4 Gorilla：连接 LLM 与真实 API 生态

**论文**：Patil et al., "Gorilla: Large Language Model Connected with Massive APIs", NeurIPS 2023 Workshop.

### 核心问题

真实 API 的挑战与学术工具截然不同：
- API 有版本更新，文档频繁变化
- API 参数复杂，有必选/可选之分
- 有 1600+ HuggingFace 模型 API，选哪个？

### 方法：检索增强微调（Retrieve + Fine-tune）

**数据集构建**：

从 HuggingFace、TorchHub、TensorHub 爬取 API 文档，用 GPT-4 生成（instruction, API call）对，构建 APIBench 数据集（共 16,464 对）。

**两种推理模式**：

```python
# ZS 模式（零样本）：直接从微调权重调用
response = gorilla(instruction)

# Retrieval 模式：先检索文档，再生成调用
docs = retriever.search(instruction)
response = gorilla(instruction, docs=docs)
```

**Retrieval 模式的关键发现**：

即使检索到的文档不完全准确，也能显著提升生成准确率——**模型学会了"参考文档生成代码"的能力**，而不只是记忆 API。

### AST 级别的准确率评估

Gorilla 不用字符串匹配，而是解析 AST（抽象语法树）来判断 API 调用是否正确：

```python
# 字符串匹配会误判
predict: model.from_pretrained("bert-base-uncased", revision="v1")  
gold:    model.from_pretrained("bert-base-uncased")

# AST 匹配：函数名相同，必选参数相同 → 正确
```

### 对 .skill 设计的启示

Gorilla 的 Retrieval 模式直接对应了 `.skill` 文件的价值主张：**把 API/工具的使用文档注入 LLM 上下文，比让模型靠"记忆"调用更可靠**。这是 skill 文件存在的核心理由之一。

---

## 2.5 本篇小结：工具调用的三个维度

| 维度 | Toolformer | ToolkenGPT | Gorilla |
|------|-----------|------------|---------|
| 工具知识来源 | 自监督生成 | 示范数据微调 | 检索 API 文档 |
| 对 LLM 的改动 | 全量微调 | 冻结 + 嵌入微调 | 微调 + RAG |
| 工具数量规模 | 少量（5 种） | 中等（可扩展） | 大量（1600+） |
| 实时文档更新 | ✗ | ✗ | ✓ |

---

# 第 03 篇：技能库范式——Voyager 与持久化技能存储

## 3.1 从"一次性工具"到"可复用技能库"

第 02 篇的三篇论文解决了"如何调用单个工具"。但真实 Agent 面对的是**序列化的长期任务**：

- 今天学会了"如何挖矿"
- 明天遇到新任务时，还记得怎么挖矿吗？

这催生了**技能库（Skill Library）**的概念：一个可以**写入、检索、复用**技能程序的持久化存储。

---

## 3.2 Voyager：Minecraft 中的自动课程学习

**论文**：Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models", NeurIPS 2023.

### 背景与问题

Minecraft 是一个开放世界游戏，任务多样且需要大量基础技能积累（砍树→做木板→做工作台→做镐子→挖矿→...）。如何让 Agent 自主探索、积累技能、完成越来越复杂的目标？

### 系统架构

Voyager 由三个核心组件构成：

```
┌─────────────────────────────────────────────────────┐
│                    Voyager                           │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │ 自动课程模块  │  │ 技能库       │  │ 迭代提示 │  │
│  │ (任务生成)   │  │ (持久化存储) │  │ (代码修复)│  │
│  └──────┬───────┘  └──────┬───────┘  └────┬─────┘  │
│         │                 │               │        │
│         └─────────────────┼───────────────┘        │
│                           ↓                        │
│                    GPT-4 (LLM Core)                │
└─────────────────────────────────────────────────────┘
```

**组件一：自动课程（Automatic Curriculum）**

每次任务结束，问 GPT-4：

```
基于当前状态（背包物品、位置、已完成任务），
提出一个适当难度的下一个目标。
```

**组件二：迭代代码生成与自我修复**

用 JavaScript 代码描述技能（Mineflayer API）：

```javascript
// craftWoodenPickaxe 技能程序
async function craftWoodenPickaxe(bot) {
  const plankCount = bot.inventory.count(mcData.itemsByName["oak_planks"].id);
  if (plankCount < 3) {
    await craftOakPlanks(bot);
  }
  await craftItem(bot, "wooden_pickaxe", 1);
  bot.chat("Wooden pickaxe crafted!");
}
```

执行失败时，将错误信息反馈给 GPT-4，让其修复代码，最多循环 N 次。

**组件三：技能库（Skill Library）**

每个成功执行的技能程序被存储为：
```json
{
  "name": "craftWoodenPickaxe",
  "code": "...",
  "description": "制作一把木镐，需要3块木板和2根木棍",
  "embedding": [0.23, -0.11, ...]  // 用于语义检索
}
```

新任务时，检索相关技能：

```python
query_embedding = embed(task_description)
relevant_skills = skill_library.search(query_embedding, top_k=5)
# 注入到 LLM context 中作为参考
```

### 关键实验结果

与基线（ReAct、Reflexion、AutoGPT）对比：
- 解锁的 Minecraft 物品种类：Voyager 是第二名的 **3.3 倍**
- 旅行距离：显著更远
- **零样本泛化**：在新 seed 地图上，利用已学技能库仍能保持优势

### 对 .skill 设计的核心启示

Voyager 的技能库设计直接对应了 `.skill` 文件系统的工程逻辑：

| Voyager 技能库 | Claude Code .skill |
|--------------|-------------------|
| JavaScript 函数 | Markdown 工作流 + 代码模板 |
| 自然语言描述（嵌入用） | `description` 字段（触发检索用） |
| 执行反馈 → 自动修复 | 人工迭代优化 |
| 动态累积 | 静态预定义（目前） |

**核心差异**：Voyager 技能库是 Agent 在运行时**动态生成和积累**的；而 `.skill` 文件是工程师**预先定义**的。这代表了两种不同的设计哲学，第 04 篇和第 08 篇将深入讨论这一张力。

---

## 3.3 Ghost in the Minecraft（GITM）：分解而非单步

**论文**：Zhu et al., "Ghost in the Minecraft: Generally Capable Agents for Open-World Environments via Large Language Models with Text-based Knowledge and Memory", 2023.

### 与 Voyager 的关键差异

Voyager 用代码函数作为技能单元。GITM 认为：**对于复杂任务，应该先做任务分解，再映射到已知原语（primitive action）**。

GITM 的技能层次：

```
复杂目标："制作钻石剑"
    ↓ LLM 分解
子目标树：
├── 获取2个钻石
│   ├── 制作钻石镐
│   │   ├── 获取铁锭 × 3
│   │   └── 获取木棍 × 2
│   └── 挖矿到钻石层（Y < 16）
└── 获取1根木棍
```

**记忆模块（Memory）**：

GITM 维护两类记忆：
- **成功记忆**：哪些分解策略有效
- **失败记忆**：哪些路径会死锁（如"想挖矿但没有镐"）

这些记忆在后续任务中作为 few-shot 示例注入 LLM。

### 对 .skill 设计的启示

GITM 的分解范式对应了 `.skill` 文件中的**工作流（Workflow）**设计：将复杂任务拆解为有序步骤，每步骤对应一个可验证的子目标。

---

## 3.4 SkiLL-IT：技能数据选择与课程学习

**论文**：Chen et al., "SKILL-IT! A Data-Driven Skills Framework for Understanding and Training Language Models", NeurIPS 2023.

### 问题：技能不是同等重要的

该论文提出：可以将语言模型的能力分解为一组**正交技能**（Orthogonal Skills），不同技能之间存在**前置依赖关系**（Prerequisite Graph）。

**发现**：按照技能图的拓扑顺序（先学基础技能）组织训练数据，可以用更少数据达到相同效果。

### 技能依赖图示例

```
基础语法
    ↓
句子结构理解
    ↓
段落逻辑推理
    ↓
复杂指令理解
    ↓
工具调用（Tool Use）
```

### 对 .skill 设计的启示

当你为 Agent 设计技能文件集合时，应该问：**技能之间是否有依赖关系？是否需要一个"前置技能检查"机制？** 例如，`manim-math.skill` 依赖于 `python-execution.skill`。

---

# 第 04 篇：LLM as Tool Maker——让模型自造工具

## 4.1 从"工具使用者"到"工具制造者"

前三篇论文假设工具是预先存在的。但现实是：**很多任务需要的工具并不存在**，或者通用工具无法高效解决特定问题。

这催生了一个更激进的问题：**能否让 LLM 自己定义和创造工具（即 .skill 文件）？**

---

## 4.2 LATM：大型语言模型作为工具制造者

**论文**：Cai et al., "Large Language Models as Tool Makers", ICLR 2024.

### 核心创新

LATM 提出**双 LLM 架构**：

```
┌──────────────────────────────────────────────────┐
│                  LATM 系统                        │
│                                                  │
│   Tool Maker (GPT-4)          Tool User (GPT-3.5)│
│   ──────────────────          ──────────────────  │
│   接受任务描述                  接受任务 + 工具函数   │
│   生成 Python 工具函数          调用工具完成任务      │
│   存入工具库                    ↑                  │
│        │                       │                  │
│        └───────────────────────┘                  │
│                工具库（Tool Cache）                │
└──────────────────────────────────────────────────┘
```

**关键洞见**：
1. 工具制造需要强推理能力（用 GPT-4）
2. 工具使用可以用更小的模型（用 GPT-3.5），**降低推理成本**
3. 同类任务只需制造一次工具，后续**批量复用**

### 工具制造过程

输入：若干同类型任务的示例
```
任务1：判断 42 是否为质数
任务2：判断 97 是否为质数
...
```

GPT-4 生成可复用工具：
```python
def is_prime(n: int) -> bool:
    """判断一个整数是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

后续任务直接调用此工具，无需 GPT-4 参与。

### 实验结果

在 Big-Bench Hard（BBH）任务集上：
- LATM（GPT-4 制造 + GPT-3.5 使用）**优于**纯 GPT-4 CoT
- 成本仅为纯 GPT-4 的约 **1/7**

### 对 .skill 设计的深层启示

LATM 的"工具制造"与 `.skill` 文件的**人工编写**是同一件事的两种模式：

| 维度 | LATM 自动生成 | 人工编写 .skill |
|------|-------------|--------------|
| 质量 | 受 LLM 能力限制 | 可以更精细 |
| 速度 | 自动，快 | 慢，需要专家 |
| 适用场景 | 可自动化的结构性任务 | 需要经验沉淀的复杂工作流 |
| 泛化性 | 针对特定任务集 | 面向宽泛场景 |

---

## 4.3 CRAFT：上下文学习中的可复用代码工具

**论文**：Yuan et al., "CRAFT: Customized LLM Agents Through Retrieval and Reuse of Code", 2023.

### 核心问题

每次遇到相似任务都让 LLM 从头生成代码，是巨大浪费。CRAFT 提出：**维护一个代码片段库，新任务时检索相关代码并组合**。

### 系统流程

```
新任务
  ↓
语义检索 → 代码库 → 相关代码片段 Top-K
  ↓
LLM（GPT-4）组合和适配代码片段
  ↓
执行验证
  ↓
成功 → 存入代码库（可供未来检索）
失败 → 报错反馈 → 重新生成
```

### 代码库条目格式

```json
{
  "task_description": "将列表按第二个元素排序",
  "code": "sorted_list = sorted(lst, key=lambda x: x[1])",
  "verified": true,
  "usage_count": 47
}
```

### 关键实验

在 TabMWP（表格数学问答）和 MATH 数据集上：
- CRAFT 比 PoT（Program of Thought）基线提升 **4-7%**
- 代码复用率随任务数增加而提升（技能库的价值随时间增长）

### 对 .skill 设计的启示

CRAFT 的代码库对应了 `.skill` 文件中的**代码模板**部分。有趣的是，CRAFT 是动态积累的，而 `.skill` 文件中的代码模板是静态的——这正是人工 skill 与自动 skill 的核心区别。

---

## 4.4 Creator：工具的发现与复用的统一框架

**论文**：Qian et al., "CREATOR: Disentangling Abstract and Concrete Reasonings of Large Language Models", EMNLP 2023.

### 框架分层

Creator 将工具创建与使用分为四个阶段：

```
Creation（创造）→ Decision（决策）→ Execution（执行）→ Rectification（修正）
```

**Creation 阶段**：
- 判断现有工具是否足够
- 若不足，抽象生成新工具（先写工具规格，再实现）

**Rectification 阶段**（区别于其他论文）：
- 不只是修复代码错误
- 还会反思"工具设计是否合理"，必要时重新设计工具

### 对 .skill 设计的启示

Creator 的 Rectification 阶段对应了 `.skill` 文件的**迭代优化**过程：工具不是一次性创建的，而是在使用中不断修正和改进的。

---

# 第 05 篇：大规模工具检索——泛化与对齐

## 5.1 核心挑战：从几个工具到数千个 API

前四篇论文的工具规模较小（5–50个）。现实 API 生态系统有：
- HuggingFace：数万个模型 API
- RapidAPI：数千个 Web API
- 企业内部：数百个微服务接口

当工具库规模扩大 100 倍时，面临两个新挑战：

1. **检索挑战**：如何从数千工具中找到正确的那几个？
2. **幻觉挑战**：模型可能生成"看起来合理但不存在"的 API 调用？

---

## 5.2 ToolBench / ToolLLM：大规模 API 工具调用基准

**论文**：Qin et al., "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs", ICLR 2024.

### 数据集：ToolBench

覆盖 RapidAPI 上 **49 类、16,464 个真实 API**，构建了：
- 268,000 条工具使用指令
- 多工具协作场景（需要 3-5 个 API 组合完成）

### 核心创新：DFSDT（深度优先搜索决策树）

传统 ReAct 是线性的：失败了就重试。DFSDT 将工具调用建模为决策树搜索：

```
              Root（初始状态）
             /        \
          调用 API_A   调用 API_B
          /    \           \
       成功   失败        成功
        ↓      ↓
      继续   回溯→尝试其他路径
```

**优势**：遇到工具调用失败时，不是无脑重试，而是系统性探索替代路径。

### ToolEval：新评估指标

- **通过率（Pass Rate）**：任务是否成功完成
- **偏好胜率（Win Rate）**：人类偏好哪个解决方案（相对于 ChatGPT-ReAct）

ToolLLaMA（基于 ToolBench 微调的 LLaMA-2）在 Win Rate 上达到 ChatGPT 的 **83%**。

---

## 5.3 AnyTool：层次化工具检索

**论文**：Du et al., "AnyTool: Self-Reflective, Large-Scale API Usage without Exhaustive Testing", 2024.

### 核心问题

当有 16,000 个工具时，直接向量检索会产生大量噪声。AnyTool 提出**层次化检索**：

```
用户意图
    ↓
L1：API 类别检索（49类 → Top-5类）
    ↓
L2：类别内工具检索（每类 → Top-10工具）
    ↓
L3：工具参数匹配（精确对齐）
```

### 自反思机制

若初次检索结果无法完成任务，启动 Self-Reflection：
- 分析失败原因（工具不存在？参数错误？类别判断偏差？）
- 在相邻类别中扩大检索范围

### 实验结果

在 ToolBench 测试集上：
- 无需任务特定微调，通过率超过 ToolLLaMA **12%**
- 检索效率：平均只需遍历全量工具的 **3%**

---

## 5.4 API-Bank：工具增强 LLM 的系统性评估

**论文**：Li et al., "API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs", EMNLP 2023.

### 贡献

API-Bank 是首个**端到端**评估工具增强 LLM 的基准，覆盖：

```
L1：正确调用单个 API（53个 API）
L2：顺序调用多个 API 完成复杂任务
L3：规划 + 检索 + 调用的完整 Pipeline
```

### 关键发现

- GPT-4 在 L1 可达 **94%**，L3 下降到 **53%**
- 工具文档质量对准确率影响极大（差文档 → 下降 20%+）

### 对 .skill 设计的核心启示

**工具文档质量是整个系统的瓶颈。** 这直接解释了为何 `.skill` 文件要花大量篇幅写清楚：何时触发、如何使用、注意事项——这不是"好看"，而是决定 LLM 能否正确使用该技能的关键。

---

# 第 06 篇：任务规划与技能编排

## 6.1 从"使用单个工具"到"编排多个技能"

前面五篇解决了"如何使用/创造/检索单个工具"。真实复杂任务需要**多个技能的协调编排**：

```
用户：帮我分析这份报告，生成摘要，翻译成英文，并发邮件给我的团队

需要：
1. PDF 解析技能
2. 文本摘要技能  
3. 机器翻译技能
4. 邮件发送技能

按照依赖关系编排：1 → 2 → 3 → (1+3结果) → 4
```

---

## 6.2 HuggingGPT / JARVIS：AI 模型作为工具的编排器

**论文**：Shen et al., "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace", NeurIPS 2023.

### 核心思想

将 HuggingFace 上数千个专门 AI 模型（图像分类、翻译、语音识别等）都视为可调用的"工具"，用 ChatGPT 作为**任务规划器和编排器**。

### 四阶段工作流

```
Stage 1: Task Planning（任务规划）
─────────────────────────────────
ChatGPT 解析用户意图，分解为子任务列表
输出：[{"task": "image-classification", "dep": [], "args": {...}}, ...]

Stage 2: Model Selection（模型选择）
─────────────────────────────────
从 HuggingFace 模型卡（描述文本）中检索最合适的模型
策略：In-context model selection（few-shot 示例）

Stage 3: Task Execution（并行执行）
─────────────────────────────────
无依赖的子任务并行执行
有依赖的子任务按序执行，将上游结果注入下游

Stage 4: Response Generation（结果整合）
─────────────────────────────────
将所有子任务结果整合为最终自然语言回答
```

### 技能描述格式

```json
{
  "task": "image-classification",
  "description": "Classify the category of the input image",
  "input": "image URL or base64",
  "output": "classification label with confidence"
}
```

**注意**：这与 `.skill` 文件中 `description` 字段的作用完全对应——它是 LLM 选择该技能的依据。

---

## 6.3 TaskBench：系统评估任务编排能力

**论文**：Shen et al., "TaskBench: Benchmarking Large Language Models for Task Automation", 2024.

### 评估维度

TaskBench 从三个维度评估 LLM 的技能编排能力：

```
1. Tool Graph Construction（工具图构建）
   └─ 能否正确识别任务依赖关系？

2. Tool Selection（工具选择）
   └─ 能否在多个可选工具中选最合适的？

3. Parameter Prediction（参数预测）
   └─ 能否正确填写工具调用的参数？
```

### 关键发现

- GPT-4 在工具图构建上显著优于其他模型（复杂依赖推理）
- **工具描述歧义**是导致工具选择错误的首要原因（43% 的错误）
- 工具数量超过 20 个时，所有模型性能均显著下降

---

## 6.4 AssistGPT：视觉任务的技能编排

**论文**：Gao et al., "AssistGPT: A General Multi-modal Assistant that can Plan, Execute, Inspect, and Learn", 2023.

### PEIL 框架

AssistGPT 提出四步循环框架（PEIL）：

```
Plan（规划）→ Execute（执行）→ Inspect（检查）→ Learn（学习）
     ↑_______________________________________|
```

**Inspect 阶段**（区别于其他方法）：
- 检查中间结果是否符合预期
- 若不符合，**主动重新规划**（而非等到最终失败）

**Learn 阶段**：
- 记录成功和失败的规划策略
- 作为 few-shot 示例指导未来规划

### 对 .skill 设计的启示

AssistGPT 的 Inspect 阶段对应了 `.skill` 文件中需要包含的**验证步骤**：技能执行后，如何判断是否成功？一个好的 `.skill` 文件不只有"怎么做"，还应有"如何验证"。

---

# 第 07 篇：代码即技能——可执行动作统一范式

## 7.1 从"文本动作"到"代码动作"

前面六篇论文的工具调用大多以结构化 JSON 或自然语言描述的方式触发。

一个更激进的想法：**用代码本身作为 Agent 动作的统一表示形式**。

```python
# 传统工具调用（结构化 JSON）
{"tool": "file_write", "args": {"path": "output.txt", "content": "Hello"}}

# CodeAct（Python 代码）
with open("output.txt", "w") as f:
    f.write("Hello")
```

**优势**：代码比 JSON schema 更灵活，能表达条件分支、循环、变量传递、函数组合——所有这些都是"技能组合"。

---

## 7.2 CodeAct：可执行 Python 代码作为统一动作空间

**论文**：Wang et al., "Executable Code Actions Elicit Better LLM Agents", ICML 2024.

### 核心主张

传统 Agent 动作空间：
- 结构化动作（JSON tool call）：表达力有限
- 自然语言动作：模糊，执行引擎难以解析

CodeAct 主张：**Python 代码是最优动作格式**。

```
表达力：Python > JSON > 自然语言
可执行性：Python = JSON > 自然语言
可组合性：Python >> JSON >> 自然语言
```

### 实验设计

在 17 个多样化任务上比较：
- Text（自然语言动作）
- JSON（结构化工具调用）
- CodeAct（Python 代码）

**结果**：CodeAct 在 15/17 任务上表现最优，平均提升 **20%+**。

### 为何代码优于 JSON？

关键在于**状态传递**：

```python
# JSON 方式：中间结果需要人为管理
result1 = tool_call({"tool": "read_csv", "path": "data.csv"})
# 如何把 result1 传给下一步？需要特殊语法或变量绑定机制

# CodeAct 方式：Python 原生支持
df = pd.read_csv("data.csv")
filtered = df[df["age"] > 18]  # 直接引用上一步结果
filtered.to_csv("output.csv")
```

### 对 .skill 设计的影响

这解释了为何现代 `.skill` 文件倾向于包含可执行的代码模板，而不仅仅是自然语言描述。代码模板让 Agent 可以直接组合和执行技能，而不需要中间解析层。

---

## 7.3 OpenAgents：面向真实用户的开放 Agent 平台

**论文**：Xie et al., "OpenAgents: An Open Platform for Language Agents in the Wild", 2023.

### 三个专门化 Agent

OpenAgents 构建了三个落地 Agent，每个都是特定技能的专家：

**DataAgent**：
```python
# 技能集：Python 数据分析
tools = [pandas, matplotlib, sklearn, seaborn]
# 用户上传 CSV，Agent 自主写代码分析
```

**PluginsAgent**：
```python
# 技能集：200+ ChatGPT Plugins
tools = [wolfram_alpha, web_search, weather, maps, ...]
# 类似 HuggingGPT 但针对 Web 服务
```

**WebAgent**：
```python
# 技能集：浏览器操作
tools = [click, type, scroll, navigate, extract_text]
# 类似 Playwright 自动化但由 LLM 控制
```

### 关键工程洞见

OpenAgents 实践了一个重要发现：**专门化 Agent（Specialized Agent）在特定领域远胜通用 Agent（General Agent）**。

这对 `.skill` 文件设计有直接影响：与其设计一个"什么都能做"的超级技能，不如设计**深度垂直的专门技能文件**，配合 Agent Router 进行分发。

---

## 7.4 AgentBench：Agent 能力全面评估

**论文**：Liu et al., "AgentBench: Evaluating LLMs as Agents", ICLR 2024.

### 八大测试环境

AgentBench 在 8 个不同环境中测试 Agent 能力：

| 环境 | 核心技能 |
|------|---------|
| OS（操作系统操作） | Bash 命令、文件管理 |
| DB（数据库） | SQL 查询、数据操作 |
| KG（知识图谱） | SPARQL、推理 |
| Digital Card Game | 规则理解、策略规划 |
| Lateral Thinking Puzzle | 创意推理 |
| House Holding（模拟家务） | 多步骤物理规划 |
| Web Shopping | 搜索、比较、决策 |
| Web Browsing | DOM 操作、信息提取 |

### 关键发现

- GPT-4 总分约为第二名的 **2 倍**（存在显著能力断层）
- 开源模型在"需要多步规划的环境"（OS、DB）上远落后于 GPT-4
- **工具调用的稳定性**（格式正确率）是区分模型的关键指标

---

# 第 08 篇：工程实践——Claude Code .skill 文件的设计哲学

## 8.1 回望：学术研究与工程实践的对应关系

经过前七篇的论文梳理，现在可以用学术语言重新解释 `.skill` 文件系统的每一个设计决策。

### 完整对应关系表

| 学术概念 | 代表论文 | .skill 工程对应 |
|---------|---------|---------------|
| Tool Retrieval（工具检索） | Gorilla, AnyTool | `description` 字段语义 |
| Skill Library（技能库） | Voyager | `available_skills` 目录 |
| Task Decomposition（任务分解） | GITM, HuggingGPT | 多 skill 协同 |
| Few-shot Demonstration（示范） | ReAct, Toolformer | SKILL.md 中的示例 |
| Tool Documentation（文档质量） | API-Bank | 技能文件的完整性 |
| Skill Verification（技能验证） | AssistGPT PEIL | verify_geometry.py 等验证脚本 |
| Code as Action（代码动作） | CodeAct | 技能中的可执行模板 |
| Tool Prerequisite（前置依赖） | SkiLL-IT | 技能间依赖声明 |

---

## 8.2 .skill 文件的核心设计原则（学术支撑版）

### 原则一：description 是检索锚点，不是说明文字

**学术依据**：Gorilla 证明检索质量决定调用准确率；AnyTool 证明层次化检索优于暴力检索。

**工程含义**：

```markdown
# 坏的 description（说明文字风格）
"这个技能用于数学动画制作，支持各种场景"

# 好的 description（触发词密集风格）
"Professional mathematical teaching animation for K-12 students using Manim 0.19.2. 
Use when creating educational math videos with precise geometry, animated proofs, 
step-by-step explanations... Triggers on requests to: create math animations, 
build teaching videos, visualize geometry problems..."
```

描述中高密度的**触发词**（trigger words）是 LLM 检索相关 skill 的"锚点"，与 Gorilla 中 API 文档的 embedding 逻辑完全一致。

---

### 原则二：代码模板是 CRAFT 的人工版本

**学术依据**：CRAFT 证明代码复用显著提升任务完成率；CodeAct 证明代码是比 JSON 更强的动作格式。

**工程含义**：

`.skill` 文件中的代码模板不是"参考示例"，而是 **Agent 的可执行骨架**——它直接降低了 LLM 从零生成代码时的错误率。

```python
# manim-math.skill 中的代码模板（CRAFT 代码库的人工预填版本）
class MathAnimation(Scene):
    def construct(self):
        # [在此插入具体数学内容]
        # 约束：x ∈ [-4,4], y ∈ [-7.5,7.5]
        # 字体：Text(font="Noto Sans CJK SC")
```

---

### 原则三：工作流是 GITM 分解树的线性展开

**学术依据**：GITM 证明任务分解树显著提升复杂任务完成率；HuggingGPT 的四阶段流程是技能编排的最佳实践。

**工程含义**：

`.skill` 文件中的**工作流步骤**不是废话，是将复杂任务分解为可验证子目标的关键结构。

```markdown
## 工作流

1. **读取 SKILL.md** → 确认技能参数
2. **几何预计算** → verify_geometry.py 验证
3. **生成代码骨架** → 填入具体内容
4. **本地渲染验证** → manim -pql scene.py
5. **输出到 /outputs** → 标注渲染参数
```

每一步对应 AssistGPT PEIL 框架中的一个阶段，步骤 4 的渲染验证正是 **Inspect** 阶段的工程实现。

---

### 原则四：约束规则是负样本 few-shot

**学术依据**：Toolformer 的过滤机制本质是"负反馈"；API-Bank 发现文档歧义是首要错误来源。

**工程含义**：

`.skill` 文件中的"❌ 禁止事项"不是在说废话，而是在向 LLM 注入**负样本 few-shot**，等价于在微调数据中加入反例。

```markdown
## 约束

- ❌ 禁止使用 `Text(font="Arial")` → 中文字符乱码
- ❌ 禁止将 MathTex 与 Text 混用颜色动画
- ✓ 所有坐标必须在安全帧范围内 (x ∈ [-4,4])
```

---

### 原则五：skill 文件本身是 LATM 工具制造的人工高质量版本

**学术依据**：LATM 的核心洞见是"工具可以被 LLM 创造"；但实验也显示人工创建的工具质量更高。

**工程含义**：

随着 Agent 能力增强，`.skill` 文件未来可能走向**半自动生成**：

```
1. Agent 执行任务 → 记录成功路径
2. LATM 式工具提取 → 生成候选 skill 草稿
3. 人工 Review + 精炼 → 正式 skill 文件
4. 加入 skill 库 → 供后续任务复用
```

这是从"纯人工"到"人机协作 skill 工厂"的演化路径。

---

## 8.3 尚未解决的工程问题（来自论文的开放挑战）

| 挑战 | 对应论文发现 | 当前 .skill 现状 |
|------|-----------|----------------|
| 技能冲突处理 | TaskBench：工具歧义是首要错误 | 无冲突解决机制 |
| 动态技能生成 | Voyager：技能应在运行时积累 | 静态预定义 |
| 技能依赖声明 | SkiLL-IT：前置依赖影响效果 | 未标准化 |
| 技能版本管理 | Gorilla：API 版本更新是大问题 | 未实现 |
| 跨 skill 状态传递 | CodeAct：变量传递是关键 | 依赖上下文窗口 |

---

## 8.4 最终：一张 .skill 文件的"学术注解版"模板

```markdown
---
name: example-skill
# [AnyTool] 层次检索锚点：类别词 + 具体触发词
description: |
  [类别：X类任务]
  [核心功能：Z]
  [触发场景：当用户说…/提到…/需要…时激活]
  [反向排除：不适用于…]
---

## 概述
[Toolformer 逻辑：这个工具何时有帮助？何时没帮助？]

## 工作流
[GITM 分解树 + AssistGPT PEIL 框架的线性展开]
1. [Plan 阶段]
2. [Execute 阶段]
3. [Inspect 阶段：验证步骤]
4. [输出阶段]

## 核心代码模板
[CRAFT 代码库预填 + CodeAct 可执行骨架]
\`\`\`python
# 可直接执行的代码框架
\`\`\`

## 约束与禁忌
[Toolformer 负样本 + API-Bank 文档歧义消除]
- ✓ 必须做…
- ❌ 禁止做…（理由）

## 示例
[ReAct few-shot + Gorilla 检索示范]
用户问：...
正确调用：...
```

---

## 8.5 系列总结

```
              LLM Skill 技术演化路径（2022 → 2025）
              
2022: ReAct ─────────── 推理 + 动作交织的基础范式
                              ↓
2023: Toolformer ─────── LLM 自学工具调用（自监督）
      Voyager ──────────  持久化技能库 + 自动课程
      LATM ────────────  LLM 作为工具制造者
      Gorilla ─────────  检索增强 API 调用
      HuggingGPT ──────  多技能编排框架
      ToolBench ───────  大规模工具泛化基准
                              ↓
2024: CodeAct ───────── 代码作为统一动作格式
      AnyTool ─────────  层次化大规模工具检索
      AgentBench ──────  Agent 能力全面评估
                              ↓
工程: Claude Code .skill ─── 学术洞见的工程沉淀
      Pi Agent ──────────  多层架构中技能系统的再设计
```

**核心结论**：

`.skill` 文件不是一个简单的"Markdown 提示词"，而是学术界五年研究的工程投影：
- 它的 `description` 是 **Gorilla 检索机制**的实现
- 它的代码模板是 **CRAFT 代码复用**的人工版本  
- 它的工作流是 **GITM 任务分解树**的线性化
- 它的约束规则是 **Toolformer 负样本过滤**的静态预填
- 它的整体设计是 **LATM 工具制造**的人工高质量变体

理解这些对应关系，才能设计出真正"高质量"的技能文件——不是凭直觉，而是基于有理论依据的设计原则。

---

## 附录：本系列核心论文速查表

| 论文 | 发表 | ArXiv / 会议 | 核心贡献 |
|------|------|------------|---------|
| ReAct | 2022 | ICLR 2023 | 推理+动作交织范式 |
| Toolformer | 2023 | NeurIPS 2023 | 自监督工具调用学习 |
| ToolkenGPT | 2023 | NeurIPS 2023 | 工具 token 化嵌入 |
| Gorilla | 2023 | NeurIPS 2023 Workshop | 检索增强 API 调用 |
| Voyager | 2023 | NeurIPS 2023 | 持久化技能库 |
| GITM | 2023 | arXiv 2305 | 任务分解 + 失败记忆 |
| SkiLL-IT | 2023 | NeurIPS 2023 | 技能课程学习 |
| LATM | 2023 | ICLR 2024 | LLM 作为工具制造者 |
| CRAFT | 2023 | arXiv 2309 | 代码片段检索复用 |
| Creator | 2023 | EMNLP 2023 | 工具创造+修正框架 |
| ToolBench/ToolLLM | 2023 | ICLR 2024 | 大规模 API 基准 |
| AnyTool | 2024 | arXiv 2402 | 层次化工具检索 |
| API-Bank | 2023 | EMNLP 2023 | 工具评估基准 |
| HuggingGPT | 2023 | NeurIPS 2023 | AI 模型编排器 |
| TaskBench | 2023 | arXiv 2311 | 技能编排评估 |
| AssistGPT | 2023 | arXiv 2306 | PEIL 规划框架 |
| CodeAct | 2024 | ICML 2024 | 代码即统一动作 |
| OpenAgents | 2023 | arXiv 2310 | 开放 Agent 平台 |
| AgentBench | 2023 | ICLR 2024 | Agent 全面评估 |

---

*本系列完*  
*作者：XM · TapTap Maker*  
*版本：v1.0 · 2025*
