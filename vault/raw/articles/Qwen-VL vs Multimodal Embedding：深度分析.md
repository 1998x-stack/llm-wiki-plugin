**Qwen-VL vs Multimodal Embedding：深度分析**

*为什么 query text embedding 能很好匹配 Qwen-VL 提取文本对应的向量，而 query 的 multimodal embedding 很难匹配图片的 multimodal embedding？*

|  |
| --- |
| Qwen-VL + Text Embedding 效果好、Multimodal Embedding 直接匹配图片效果差，这并非某个模型的问题，而是 **多模态表示学习中一个根深蒂固的结构性挑战** — Modality Gap。  这个鸿沟来源于：   1. **神经网络初始化的几何特性**（锥体效应） 2. **对比学习训练范式的固有缺陷**（假负例、温度调度） 3. **图片与文本信息编码方式的根本差异**（信息不对称）   v14 实验进一步证实：   1. **领域迁移性差**：benchmark 上的强模型（qwen3-vl-embedding，MMEB-V2 第一名）在 3D 渲染图域表现不如预期，gap 甚至比 CLIP 更大 2. **管线 A 被生产验证**：text-embedding-v3 编码 VLM 生成的文本描述，判别力是 image 通道的 33.6 倍，是搜索质量提升的唯一贡献者 |

![](data:image/png;base64...)

![](data:image/png;base64...)

**1. 核心概念定义**

**1.1 Qwen-VL（Vision-Language 生成模型）**

Qwen-VL 是一个 **生成式多模态大语言模型**（Multimodal LLM）。它的核心能力是：

* **图像理解 → 文本生成**：输入一张图片，输出对图片内容的自然语言描述
* 本质上是一个 **跨模态翻译器**：将视觉信息"翻译"为文本信息
* 典型用途：OCR 文本提取、图片描述（captioning）、视觉问答（VQA）

当你用 Qwen-VL 处理图片时，它做的事情是：

|  |
| --- |
| Plaintext 图片 → [Qwen-VL] → 文本描述（自然语言）→ [Text Embedding Model] → 文本向量 |

**1.2 Multimodal Embedding（多模态嵌入模型）**

Multimodal Embedding 模型（如 CLIP、Jina CLIP、Voyage Multimodal、Qwen3-VL-Embedding）是 **表示学习模型**。它的核心能力是：

* 将 **不同模态**（文本、图片）映射到 **同一个向量空间**
* 通过对比学习（Contrastive Learning）训练
* 典型架构：双编码器（Dual Encoder），一个文本编码器 + 一个图像编码器

|  |
| --- |
| Plaintext 文本 → [Text Encoder] → 向量 (d维)  ↕ 同一空间，可计算余弦相似度 图片 → [Image Encoder] → 向量 (d维) |

**1.3 关键区别一览**

|  |  |  |
| --- | --- | --- |
| 维度 | Qwen-VL（生成模型） | Multimodal Embedding |
| **任务类型** | 生成式（image→text） | 表示式（input→vector） |
| **输出** | 自然语言文本 | 固定维度向量 |
| **检索管线** | 图片→提取文本→文本嵌入→匹配 | 图片→直接嵌入→匹配 |
| **信息中介** | 文本作为中间表示 | 无中间表示，端到端 |
| **模态转换** | 显式跨模态翻译 | 隐式跨模态对齐 |

**2. 为什么 Text Embedding 匹配效果好？**

**2.1 同模态匹配 — 天然优势**

当你使用 Qwen-VL 提取图片中的文本，然后用 text embedding 模型编码，整个管线变成：

|  |
| --- |
| Plaintext Query（文本）→ [Text Embedding] → query向量  ↕ 同模态！Text-Text 匹配 图片 → [Qwen-VL提取文本] → [Text Embedding] → doc向量 |

**这是纯粹的 text-to-text 检索**。两个向量来自同一个编码器，在同一个表示空间中，没有跨模态对齐的负担。

实验数据（Agentset 2025 benchmark）：

* 纯文本文档：Text Embedding Recall@1 = **96%**，Multimodal Embedding Recall@1 = 92%
* 文本嵌入在纯文本匹配上始终略优于多模态嵌入

**2.2 Text Embedding 模型的成熟度**

现代文本嵌入模型（如 OpenAI text-embedding-3、BGE、GTE 等）经过了：

* **海量纯文本语料** 训练（数十亿对）
* **长期迭代优化**，在文本语义匹配任务上高度成熟
* 专注于一个模态，参数效率高

它们在"文本 ↔ 文本"这个任务上几乎已经达到了天花板水平。

**2.3 Qwen-VL 的文本提取质量**

Qwen-VL 作为多模态 LLM，其 OCR 和图像理解能力已经非常强大：

* 能准确提取图片中的文字
* 能生成结构化的内容描述
* 将视觉信息"无损"转化为文本信息（对于文字密集型文档尤其如此）

因此 Qwen-VL提取的文本 + Text Embedding 形成了一个强大的组合：

* 模态内匹配 → 无 modality gap
* 高质量文本提取 → 信息保真度高
* 成熟的文本嵌入 → 语义匹配精准

**3. 为什么 Multimodal Embedding 匹配图片困难？**

这是本文的核心问题。答案涉及多个深层原因：

**3.1 模态鸿沟（Modality Gap）— 最根本的原因**

**这是一个已被学术界广泛研究和确认的结构性问题。**

*"Different data modalities (e.g. images and text) are embedded at arm's length in their shared representation space."
— Liang et al., NeurIPS 2022, "Mind the Gap"*

**什么是 Modality Gap？**

即使经过对比学习训练，图片向量和文本向量在共享向量空间中 **仍然占据不同的区域**，形成两个分离的聚类。

|  |
| --- |
| Plaintext 向量空间可视化（概念图）：   Text Cluster Image Cluster  ┌─────────┐ ┌─────────┐  │ t1 t2 │ │ i1 i2 │  │ t3 │ ← 模态鸿沟 → │ i3 │  │ t4 t5 │ │ i4 i5 │  └─────────┘ └─────────┘   文本向量之间的平均余弦相似度 >> 匹配的图文对之间的余弦相似度 |

Jina AI 在 Flickr8k 上的实验（2024）清楚展示了这一点：

* **Text-Text 匹配对**的余弦相似度分布集中在 **0.7-0.9**
* **Image-Text 匹配对**的余弦相似度分布集中在 **0.2-0.5**
* 两个分布几乎不重叠

**Modality Gap 的三大成因**

**① 锥体效应（Cone Effect）— 初始化偏差**

CLIP 架构本质上是两个独立的编码器拼接在一起。在训练开始前：

|  |
| --- |
| Plaintext Text Encoder（随机初始化或预训练）→ 文本向量全部落在空间的某个"锥形区域" Image Encoder（随机初始化或预训练）→ 图片向量全部落在另一个"锥形区域" |

深度神经网络的输出在初始化时天然被限制在一个 **窄锥体（narrow cone）** 内。两个独立编码器的锥体方向不同，导致两类向量从一开始就分离。

***即使完全随机初始化（非预训练），锥体效应依然存在。这是网络结构的固有属性。***

**② 对比学习的局限性 — 假负例问题（False Negative Problem）**

对比学习的训练方式：

* **正例**：匹配的图文对 → 拉近距离
* **负例**：batch 内随机配对的不匹配图文 → 推远距离

问题在于：随机配对的"负例"中，可能存在 **语义部分重叠** 的对：

|  |
| --- |
| Plaintext 图片：一只狗在雪地里 文本："The dog sits by a snowdrift"  ↓ 被当作负例 但它们其实有语义重叠（都有狗）→ 训练把"狗"的图像和文本表示推得更远 |

这种系统性的假负例效应，**累积起来会把所有图片和所有文本整体推离**，加剧模态鸿沟。

**③ 训练温度（Temperature）的影响**

* **高温度**（高随机性）：向量在训练中移动幅度大，有助于打破初始锥体结构，缩小模态鸿沟
* **低温度**（低随机性）：向量移动小，很难克服初始偏差

实践中的矛盾：

* 高温度能缩小模态鸿沟，但会严重损害模型性能（检索准确率暴跌）
* 标准训练流程从高温开始逐渐降温，但最终低温阶段"固化"了模态鸿沟

**3.2 信息不对称（Information Imbalance）**

图片和文本承载信息的方式根本不同：

|  |  |  |
| --- | --- | --- |
| 特征 | 文本 | 图片 |
| **信息密度** | 高度浓缩、显式语义 | 分布式、像素级 |
| **语义粒度** | 精确词汇、明确概念 | 连续视觉特征、隐式语义 |
| **结构** | 线性序列 | 2D 空间布局 |
| **歧义性** | 较低（语言有约束） | 较高（同一图片可有多种解读） |
| **编码维度** | 主要编码"what"（是什么） | 同时编码 what + where + how（什么 + 在哪 + 怎样） |

一段文本 "a red car on a highway" 精确描述了一个概念。
一张红色汽车在高速公路上的图片还包含：天气、光照、角度、背景建筑、路面纹理、车型细节……

**这种信息的不对称性意味着：文本query向量 和 图片向量 即使描述同一事物，它们编码的信息维度也不同，难以精确对齐。**

*Schrodi et al. (2024) 在 "Two Effects, One Trigger" 中指出：图片天然比文本携带更多信息，对比学习倾向于让图像编码器聚焦于"物体"（object bias），而忽略属性、关系等细粒度信息——这与文本编码器的表示方式产生结构性错位。*

**3.3 对齐训练数据的质量瓶颈**

训练多模态嵌入模型需要大量高质量的图文对：

* 网络爬取的图文对 **噪声极大**（alt-text 通常质量低）
* 高质量人工标注的图文对 **数量有限**（相比纯文本语料少几个数量级）
* 训练数据的分布不均匀导致模型在某些领域对齐好、某些领域对齐差

对比：纯文本语义匹配模型可以使用 **数十亿** 高质量文本对训练，而多模态对齐通常只有 **数百万到数亿** 对（OpenAI CLIP 用了 4 亿对，已属于极大规模）。

**3.4 编码器架构的固有限制**

CLIP 风格的双编码器架构存在根本性限制：

|  |
| --- |
| Plaintext  独立编码，无交互 文本 → [Text Encoder] ──────────→ 文本向量  cos(·,·) ← 唯一的交互点 图片 → [Image Encoder] ─────────→ 图片向量 |

* 两个编码器 **独立工作**，直到最后才通过余弦相似度交互
* 没有 cross-attention 机制来做细粒度的模态间对齐
* 所有跨模态理解的负担都压缩在了一个标量（相似度分数）上

这就是为什么 **Cross-Encoder**（如 Qwen3-VL-Reranker）能显著提升跨模态匹配质量——它允许两个模态在编码过程中直接交互。

**4. Qwen3-VL-Embedding：试图弥合鸿沟的新尝试**

阿里在 2026 年 1 月发布的 Qwen3-VL-Embedding 代表了最新的尝试：

**架构特点**

* 基于 **Qwen3-VL 基础模型**（而非独立的双编码器）
* **统一的 backbone** 处理文本和图片，共享底层参数
* 多阶段训练：大规模对比预训练 → Reranker 蒸馏
* 支持 Matryoshka Representation Learning（灵活嵌入维度）
* 支持多达 32k token 输入

**为什么统一 backbone 有助于缩小模态鸿沟？**

|  |
| --- |
| Plaintext 传统 CLIP:  Text Encoder (独立参数) ──→ 文本向量  Image Encoder (独立参数) ──→ 图片向量  → 两个独立的锥体，天然分离  Qwen3-VL-Embedding:  [共享 VL Backbone] ← 文本/图片都经过它  ↓  统一表示空间的向量  → 共享参数强制两个模态的表示更接近 |

**性能表现**

* MMEB-V2 综合评分 **77.8**，排名第一（截至 2026.01.08）
* 在多模态检索任务上显著优于传统 CLIP 模型

但即使是这样的模型，**模态鸿沟依然存在**，只是被缩小了。

**5. 两条管线的对比分析**

**管线 A：Qwen-VL 提取文本 + Text Embedding（你说的"效果好"的方案）**

|  |
| --- |
| Plaintext ┌──────────┐ ┌──────────┐ ┌────────────────┐ ┌──────────┐ │ 图片 │ ──→ │ Qwen-VL │ ──→ │ 提取的文本 │ ──→ │ Text │ ──→ doc向量 │ │ │ (生成模型)│ │ (自然语言) │ │ Embedding│ └──────────┘ └──────────┘ └────────────────┘ └──────────┘  ┌──────────┐ ┌──────────┐ │ Query │ ────────────────────────────────────────────→ │ Text │ ──→ query向量 │ (文本) │ │ Embedding│ └──────────┘ └──────────┘  → 同模态匹配，无 modality gap，余弦相似度直接可比 |

**优点：**

* 完全消除 modality gap（因为是 text-text 匹配）
* 利用成熟的文本嵌入模型
* 对文字密集型内容（文档、表格中的文字）效果极好

**缺点：**

* 信息损失：视觉布局、空间关系、颜色、图表结构在文本提取中可能丢失
* 延迟高：需要先运行 VLM 推理
* 对纯视觉内容（照片、艺术作品）效果差

**管线 B：Multimodal Embedding 直接编码（你说的"效果差"的方案）**

|  |
| --- |
| Plaintext ┌──────────┐ ┌────────────────┐ │ 图片 │ ──→ │ Multimodal │ ──→ image向量 │ │ │ Embedding │ └──────────┘ │ (Image Enc.) │  └────────────────┘  ↕ 跨模态匹配，存在 modality gap！ ┌──────────┐ ┌────────────────┐ │ Query │ ──→ │ Multimodal │ ──→ query向量 │ (文本) │ │ Embedding │ └──────────┘ │ (Text Enc.) │  └────────────────┘  → 跨模态匹配，受 modality gap 影响，余弦相似度可能系统性偏低 |

**优点：**

* 保留完整视觉信息（布局、空间关系、颜色）
* 端到端，延迟低
* 对表格（+12% Recall@1）、图表等视觉结构内容有优势

**缺点：**

* 受 modality gap 影响，绝对相似度分数偏低
* 跨模态匹配不如同模态匹配精准
* 对纯文本内容略逊于文本嵌入

**6. 深层原因总结：为什么一个好匹配，一个难匹配？**

|  |
| --- |
| Plaintext  ┌─────────────────────────────────────┐  │ 根本原因：模态本质差异 │  └──────────┬──────────────────────────┘  │  ┌────────────────┼────────────────┐  ▼ ▼ ▼  ┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐  │ 锥体效应 │ │ 信息不对称 │ │ 对比学习局限 │  │ (初始化偏差) │ │ (编码维度 │ │ (假负例/温度) │  │ │ │ 不同) │ │ │  └────────┬────────┘ └──────┬───────┘ └────────┬─────────┘  │ │ │  └────────────────┼───────────────────┘  ▼  ┌─────────────────────────────┐  │ Modality Gap (模态鸿沟) │  │ 图片和文本向量系统性分离 │  └──────────┬──────────────────┘  │  ┌────────────────┼────────────────┐  ▼ ▼  ┌───────────────────┐ ┌───────────────────┐  │ Text→Text 匹配 │ │ Text→Image 匹配 │  │ 无鸿沟，高相似度 │ │ 有鸿沟，低相似度 │  │ ✅ 效果好 │ │ ❌ 效果差 │  └───────────────────┘ └───────────────────┘ |

**一句话总结：**

*Qwen-VL 将图片"翻译"成文本后，匹配问题变成了同模态的 text-text 检索，绕开了 modality gap；而 multimodal embedding 的 text-image 检索必须直面 modality gap 这一尚未彻底解决的结构性难题。*

**7. 实践建议**

**7.1 何时用哪条管线？**

|  |  |  |
| --- | --- | --- |
| 内容类型 | 推荐管线 | 原因 |
| **文字密集型文档**（PDF、文章） | Qwen-VL + Text Embedding | 文本提取质量高，text-text 匹配精准 |
| **表格** | Multimodal Embedding | 表格的行列关系在文本化中损失大（Recall@1 差 12%） |
| **图表/图解** | 混合方案 | Multimodal 略优（+2%），但差距不大 |
| **自然图片**（照片、设计） | Multimodal Embedding | 无法有效文本化 |
| **混合文档** | Hybrid: 两条管线并行 + reranker 融合 | 取两者之长 |

**7.2 缓解 Modality Gap 的策略**

1. **使用更新的统一架构模型**（如 Qwen3-VL-Embedding），而非传统 CLIP
2. **Reranker 二次排序**：用 Cross-Encoder（如 Qwen3-VL-Reranker）对初检结果精排
3. **Hybrid 检索**：同时走两条管线，合并结果后去重排序
4. **模态特定的相似度阈值**：不要用同一个阈值比较 text-text 和 text-image 的分数
5. **Prompt 工程**：为图片生成丰富的文本描述作为辅助索引

**8. 前沿研究方向**

|  |  |  |
| --- | --- | --- |
| 方向 | 论文/工作 | 核心思路 |
| 理解模态鸿沟 | "Mind the Gap" (Liang et al., NeurIPS 2022) | 揭示锥体效应和对比学习的结构性问题 |
| 缩小模态鸿沟 | "Mitigate the Gap" (Eslami & de Melo, ICLR 2025) | 改进 CLIP 的跨模态对齐方法 |
| 模态内错位 | "Cross the Gap" (ICLR 2025) | 发现 CLIP 在模态内部也存在错位 |
| 信息不平衡 | "Two Effects, One Trigger" (Schrodi et al., 2024) | 分析对比学习中的信息不对称和物体偏差 |
| 统一嵌入框架 | Qwen3-VL-Embedding (Li et al., 2026) | 基于 VLM 的统一多模态嵌入 |
| VLM 用于检索 | GME (Zhang et al., 2024) | 用多模态 LLM 改进通用多模态检索 |

**9. 实验验证：v14 Prefab 搜索实测数据（2026-03-31）**

*以下数据来自 prefab\_search\_v14 实验，在 657 个游戏 3D Prefab + 128 条中文测试查询上进行，验证了上述理论分析。*

**9.1 实验设计**

在 3-channel RRF (BM25 + Text + Image) 检索管线中，将本地模型替换为 DashScope API 模型：

|  |  |  |  |
| --- | --- | --- | --- |
| 通道 | v13 模型 | v14 模型 | 维度 |
| Text | BGE-base-zh（本地） | text-embedding-v3（API） | 768d → 1024d |
| Image | CLIP-ViT-B/32（本地） | qwen3-vl-embedding（API） | 512d → 1024d |
| BM25 | jieba + enhanced corpus | 不变 | — |

Image 通道编码方式：每个 Prefab 的 4 视角（默认/正面/侧面/顶面）分别通过 qwen3-vl-embedding 编码后 mean pooling 为单向量。

**9.2 通道判别力实测**

判别力公式：power = max((correct\_mean - wrong\_mean) / std\_all, 0.01)

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 通道 | 模型 | 正确样本均值 | 错误样本均值 | Gap | 判别力 |
| BM25 | jieba（不变） | 10.32 | 8.81 | +1.51 | 0.270 |
| Text | text-embedding-v3 | 0.691 | 0.669 | **+0.022** | **0.336** |
| Image | qwen3-vl-embedding | 0.497 | 0.536 | **-0.039** | 0.010 |

对比 v13 (CLIP)：

|  |  |  |  |
| --- | --- | --- | --- |
| 通道 | v13 Gap (CLIP) | v14 Gap (qwen3-vl) | 变化 |
| Image | -0.024 | **-0.039** | **更差** |

**关键发现：qwen3-vl-embedding 的 modality gap 比 CLIP 更大（-0.039 vs -0.024），统一 backbone 并未缩小鸿沟。**

**9.3 为什么统一 backbone 在本场景失效？**

Section 4 分析了 qwen3-vl-embedding 的统一 backbone 理论上应有助于缩小模态鸿沟。但实测数据反驳了这一预期，原因如下：

**① 领域错配：游戏 3D 渲染图 ≠ 训练域**

qwen3-vl-embedding 在 MMEB-V2 benchmark（自然图片、文档、图表）上排名第一（77.8 分），但我们的数据是：

* **图像端**：Unity/Unreal 渲染的 3D Prefab 预览图，纯色背景，无自然光照，标准视角
* **文本端**：中文口语化查询（"那个绿色圆圆的小恐龙"、"踩上去会爆炸的东西"）

模型的跨模态对齐主要在自然图片域习得，迁移到 3D 渲染图域时对齐能力下降。CLIP 虽然架构更简单，但其 4 亿图文对的大规模训练在通用视觉概念（颜色、形状、物体类型）上建立了较粗粒度但更鲁棒的对齐。

**② 4-view 均值池化稀释了视角信息**

|  |
| --- |
| Plaintext default\_view + front\_view + side\_view + top\_view → mean → 单向量 |

每个视角编码了不同的几何/纹理特征，平均后变成"哪个视角都不像"的模糊表示。这种模糊表示之间的互相似度高（wrong\_mean=0.536），但与精确文本描述的匹配度低。这是 Section 3.2 信息不对称在 3D 资产场景中的极端表现。

**③ 复杂训练目标引入领域偏差**

qwen3-vl-embedding 采用多阶段训练（对比预训练 + Reranker 蒸馏），优化目标涵盖文档理解、表格解析等任务。对于简单的"query 文本 vs 3D 预览图"场景，这种复杂训练可能引入了不相关的表示偏差，使得模型在本域表现反而不如专注于图文对齐的 CLIP。

**9.4 Text 通道验证：管线 A 的实测成功**

text-embedding-v3 的判别力（0.336）远超 image 通道（0.010），**是 image 通道的 33.6 倍**。这直接验证了 Section 5 的分析：

|  |
| --- |
| Plaintext 管线 A（我们的 Text 通道）:  图片 → [Qwen-VL 生成 structured\_description] → 文本 → [text-embedding-v3] → doc向量  查询 → [text-embedding-v3] → query向量  → 同模态匹配，判别力 0.336 ✅  管线 B（我们的 Image 通道）:  图片 → [qwen3-vl-embedding] → image向量  查询 → [qwen3-vl-embedding] → query向量  → 跨模态匹配，判别力 0.010（接近随机）❌ |

我们的 structured\_description（由 Qwen-VL 生成的中文资产描述）本质上就是管线 A 的文本中间表示。v14 将 text-embedding-v3 用于这些文本描述后，搜索质量大幅提升（UUID Hit@1 +3.9pp），完全归功于 text 通道。

**9.5 搜索质量实测**

|  |  |  |  |
| --- | --- | --- | --- |
| 指标 | v13（本地模型） | v14（API 模型） | 变化 |
| UUID Hit@1 | 0.7188 | **0.7578** | **+3.90pp** |
| UUID MRR | 0.8081 | **0.8359** | **+2.78pp** |
| 坏案例数 | 15 | **12** | -3 |

**提升完全来自 text 通道**（text-embedding-v3 替代 BGE），image 通道（qwen3-vl-embedding 替代 CLIP）贡献为零甚至略负。

**9.6 实验结论**

1. **统一 backbone 不等于消除 modality gap。** qwen3-vl-embedding 在游戏 3D 资产域的 gap（-0.039）比 CLIP（-0.024）更大，说明 Section 3.1 的锥体效应和 Section 3.2 的信息不对称是结构性的，不因模型架构改进而消失。
2. **模型在目标域的表现与 benchmark 排名不相关。** qwen3-vl-embedding 的 MMEB-V2 第一名来自自然图片和文档域，无法迁移到 3D 渲染图域。
3. **管线 A（VLM 提取文本 + Text Embedding）在实际生产系统中被验证为最优路径。** v14 的 +3.9pp Hit@1 改进完全来自 text-embedding-v3 对文本描述的更好编码。
4. **Image 通道的合理定位：权重 ≤ 0.02 或直接移除。** 在 image 通道判别力为负的情况下，保留 0.02 权重仅作为极端边界case的补充，而非质量贡献者。

**10. 结论**

Qwen-VL + Text Embedding 效果好、Multimodal Embedding 直接匹配图片效果差，这并非某个模型的问题，而是 **多模态表示学习中一个根深蒂固的结构性挑战** — Modality Gap。

这个鸿沟来源于：

1. **神经网络初始化的几何特性**（锥体效应）
2. **对比学习训练范式的固有缺陷**（假负例、温度调度）
3. **图片与文本信息编码方式的根本差异**（信息不对称）

v14 实验进一步证实：

1. **领域迁移性差**：benchmark 上的强模型（qwen3-vl-embedding，MMEB-V2 第一名）在 3D 渲染图域表现不如预期，gap 甚至比 CLIP 更大
2. **管线 A 被生产验证**：text-embedding-v3 编码 VLM 生成的文本描述，判别力是 image 通道的 33.6 倍，是搜索质量提升的唯一贡献者

Qwen-VL 的"巧妙之处"在于：通过显式的模态转换（图片→文本），将跨模态检索问题降维为同模态检索问题，从而绕开了 modality gap。这不是"作弊"，而是工程上的务实选择——在 modality gap 问题被彻底解决之前，这种方案在文字密集场景下仍然是最可靠的。

**v14 实验数据是这一观点最直接的工程证据。**

*参考文献：*

* *Liang et al. "Mind the Gap: Understanding the Modality Gap in Multi-modal Contrastive Representation Learning." NeurIPS 2022.*
* *Eslami & de Melo. "Mitigate the Gap: Improving Cross-Modal Alignment in CLIP." ICLR 2025.*
* *Schrodi et al. "Two Effects, One Trigger: On the Modality Gap, Object Bias, and Information Imbalance." 2024.*
* *Li et al. "Qwen3-VL-Embedding and Qwen3-VL-Reranker: A Unified Framework." arXiv:2601.04720, 2026.*
* *Jina AI. "The What and Why of Text-Image Modality Gap in CLIP Models." 2024.*
* *Agentset. "Multimodal vs Text Embeddings: Performance Comparison." 2025.*
* *Lumer et al. "Comparison of Text-Based and Image-Based Retrieval in Modern Multimodal RAG Systems." 2025.*