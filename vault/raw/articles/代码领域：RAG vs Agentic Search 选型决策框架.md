**代码领域：RAG vs Agentic Search 选型决策框架**

|  |
| --- |
| **核心问题**：什么样的代码项目适合用 RAG？什么适合用 Agentic Search？ **参考来源**：Claude Code、Cline、Cursor、Relace FAS、SmartScope 实践报告 |

**重要说明**

|  |
| --- |
| **⚠️ SmartScope（2026）警告**： "基于代码行数的阈值论断（'超过X行用RAG'）是弱论点，缺乏可复现性。真正有意义的判断维度是：**任务类型、查询特征、团队约束**——而非单纯的 LOC 数字。" |

本文提供**多维度决策框架**，LOC 只是其中一个参考维度，不是唯一判断标准。

|  |
| --- |
| [**重要说明**](#heading_0)  [**1. 核心判断维度**](#heading_1)  [**2. 维度1：代码规模（LOC / 文件数）**](#heading_2)  [**参考区间（经验值，非硬性规则）**](#heading_3)  [**为什么规模影响选择？**](#heading_4)  [**Qodo 的企业实践数据**](#heading_5)  [**3. 维度2：任务类型**](#heading_6)  [**任务类型 vs 推荐方案**](#heading_7)  [**任务维度决策矩阵**](#heading_8)  [**4. 维度3：查询特征**](#heading_9)  [**查询类型分类**](#heading_10)  [**查询特征 → 推荐方案**](#heading_11)  [**5. 维度4：工程约束**](#heading_12)  [**延迟要求**](#heading_13)  [**Token 预算**](#heading_14)  [**代码更新频率**](#heading_15)  [**6. 维度5：团队与部署**](#heading_16)  [**安全与隐私**](#heading_17)  [**维护成本**](#heading_18)  [**7. 综合决策矩阵**](#heading_19)  [**评分矩阵（各维度加权）**](#heading_20)  [**8. 决策流程图**](#heading_21)  [**9. 混合架构设计**](#heading_22)  [**推荐：Hybrid 架构（大多数生产场景的最优解）**](#heading_23)  [**Hybrid 工作流**](#heading_24)  [**10. 实际案例分析**](#heading_25)  [**案例1：小型 Python 服务（15K LOC）**](#heading_26)  [**案例2：企业级 Java 服务（800K LOC）**](#heading_27)  [**案例3：开源项目贡献（200K LOC）**](#heading_28)  [**案例4：10K 仓库企业平台（Qodo 实践）**](#heading_29)  [**案例5：Claude Code 代码助手**](#heading_30)  [**11. KPI 驱动的决策方法**](#heading_31)  [**3步 KPI 决策法**](#heading_32)  [**关键 KPI 指标**](#heading_33)  [**总结**](#heading_34)  [**一句话决策原则**](#heading_35)  [**快速对照表**](#heading_36) |

1. **核心判断维度**

选型应从以下**5个维度**综合评估：

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────────┐ │ 选型判断框架 │ │ │ │ 维度1：代码规模 维度2：任务类型 维度3：查询特征 │ │ ├─ LOC ├─ QA vs 修改 ├─ 概念性 vs 符号 │ │ ├─ 文件数 ├─ 单文件 vs 跨文件 ├─ 单跳 vs 多跳 │ │ └─ 仓库数量 └─ 探索 vs 生成 └─ 精确 vs 模糊 │ │ │ │ 维度4：工程约束 维度5：团队约束 │ │ ├─ 延迟要求 ├─ 安全/隐私 │ │ │ ├─ Token预算 ├─ 维护成本 │ │ │ └─ 更新频率 └─ 技术栈偏好 │ │ └─────────────────────────────────────────────────────────┘ |

2. **维度1：代码规模（LOC / 文件数）**

|  |
| --- |
| **说明**：规模是重要参考，但只有结合任务类型才有意义。 |

**参考区间（经验值，非硬性规则）**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**为什么规模影响选择？**

|  |
| --- |
| Plain Text 小型仓库（< 50K LOC）：  ├─ 模型可在有限 turns 内探索完关键路径  ├─ Agentic Search：grep + read 可快速覆盖  └─ RAG 的建设成本 > 收益  大型仓库（> 500K LOC）：  ├─ Agentic Search 的 token 消耗爆炸性增长  ├─ 无边界探索 → "最坏情况 token 爆炸"  └─ RAG 提供预检索范围收窄，防止搜索发散 |

**Qodo 的企业实践数据**

|  |
| --- |
| "10K 个仓库，数百万行代码 —— 此规模下，RAG 不是可选项，而是必须品。纯 Agentic Search 的 token 消耗无法支撑企业级场景。" |

3. **维度2：任务类型**

**任务类型是最重要的判断维度，权重高于代码规模。**

**任务类型 vs 推荐方案**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**任务维度决策矩阵**

|  |
| --- |
| Plain Text  单跳推理 ←────────────────────────────── 多跳推理  │ │ 静态知识 RAG Agentic Search  │ │ 动态探索 Agentic Search Agentic Search（必须） |

4. **维度3：查询特征**

**查询类型分类**

|  |
| --- |
| Plain Text 概念性查询（模糊）：  示例："认证相关的代码在哪里？"  特征：用自然语言描述功能，不知道具体符号名  推荐：RAG（语义搜索）→ 找到候选后 Agentic 深入  符号性查询（精确）：  示例："UserService.create\_user 的实现在哪？"  特征：已知具体的类名/函数名  推荐：Agentic Search（grep/LSP，比向量检索更准）  行为性查询（复杂）：  示例："为什么订单创建后库存没有扣减？"  特征：需要追踪多个系统的交互  推荐：Agentic Search（多步追踪必须）  生成性查询：  示例："实现一个支持分页的用户列表接口"  特征：需要理解现有约定，然后生成新代码  推荐：Agentic Search（先探索约定）→ 代码生成 |

**查询特征 → 推荐方案**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

5. **维度4：工程约束**

**延迟要求**

|  |
| --- |
| Plain Text 严格延迟（< 2s）：→ 必须 RAG  └─ 用户即时问答、IDE 代码补全  宽松延迟（5-30s）：→ Agentic Search 可用  └─ 后台分析、代码审查建议  无延迟要求（> 30s）：→ Agentic Search 全力发挥  └─ 批量分析、深度研究任务 |

**Token 预算**

|  |
| --- |
| Plain Text 低预算（< 10K tokens/query）：→ RAG  └─ 成本敏感型产品（$20/月 SaaS）  中预算（10K-100K tokens）：→ Hybrid  └─ 企业内部工具  高预算（100K+ tokens）：→ Agentic Search  └─ 开发者工具、CI/CD 集成 |

**代码更新频率**

|  |
| --- |
| Plain Text 频繁更新（每天多次 PR）：→ Agentic Search 更好  └─ 索引维护成本极高，Agentic 始终读最新代码  低频更新（周级/月级）：→ RAG 可胜任  └─ 索引可保持较长有效期 |

6. **维度5：团队与部署**

**安全与隐私**

|  |
| --- |
| Plain Text 高安全要求：→ 倾向 Agentic Search  ├─ RAG 需要将代码向量化存储，双重安全面  ├─ Agentic 直接读本地文件，无需外部向量库  └─ Cline 团队选择不索引代码库，核心理由：安全  低安全要求（内部工具）：→ RAG 可接受  └─ 索引存储在私有向量库，可接受 |

**维护成本**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

7. **综合决策矩阵**

**评分矩阵（各维度加权）**

对你的场景按每项打分（1-5），计算总分：

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**评分方式**：每维度打 1-5 分，RAG 倾向=1，Agentic 倾向=5，加权平均。

|  |
| --- |
| Plain Text 总分 1.0-2.0：→ 传统 RAG 总分 2.1-3.5：→ Hybrid（RAG + Agentic Search） 总分 3.6-5.0：→ Agentic Search 为主 |

8. **决策流程图**

|  |
| --- |
| Plain Text START：你的代码任务  │  ▼ Q1: 你的任务需要跨文件追踪调用链吗？  │  ├─ YES ──► Agentic Search（多步推理必须）  │  └─ NO  │  ▼  Q2: 代码库是否 > 500K LOC 或 > 5000 个文件？  │  ├─ YES  │ │  │ ▼  │ Q3: 查询类型是概念性模糊查询吗？  │ ├─ YES ──► RAG 为主（语义检索）+ Agentic 跟进  │ └─ NO ──► Hybrid（RAG 范围收窄 + Agentic 精确探索）  │  └─ NO（中小型代码库）  │  ▼  Q4: 对延迟要求严格（< 2s）吗？  ├─ YES ──► RAG  └─ NO  │  ▼  Q5: 有安全/隐私顾虑（不想向量化代码）？  ├─ YES ──► Agentic Search（不建索引）  └─ NO ──► Agentic Search（灵活）or RAG（成本低） |

9. **混合架构设计**

**推荐：Hybrid 架构（大多数生产场景的最优解）**

|  |
| --- |
| Plain Text ┌──────────────────────────────────────────────────────────┐ │ Hybrid Code Intelligence System │ │ │ │ ┌─────────────────┐ ┌────────────────────────┐ │ │ │ Query Router │ │ RAG Index Layer │ │ │ │ │ │ │ │ │ │ 概念性查询 ────►│──RAG──► │ · 向量搜索（语义） │ │ │ │ 精确符号 ────►│──grep──► │ · BM25（关键词） │ │ │ │ 跨文件追踪 ────►│──Agent──►│ · 函数签名索引 │ │ │ │ Bug修复 ────►│──Agent──►│ │ │ │ └─────────────────┘ └────────────────────────┘ │ │ │ │ │ ┌──────────────────────────────────────▼──────────────┐ │ │ │ Agentic Search Layer │ │ │ │ │ │ │ │ grep/ls/read ◄── RAG 结果作为起点 ──► LSP/Symbols │ │ │ │ │ │ │ │ RAG 提供导航地图，Agentic 做精细探索 │ │ │ └─────────────────────────────────────────────────────┘ │ └──────────────────────────────────────────────────────────┘ |

**Hybrid 工作流**

|  |
| --- |
| Python def hybrid\_code\_search(query: str, task\_type: str) -> str:  """  混合策略：RAG 收窄范围，Agentic 深入探索  """  if task\_type == "qa":  # 纯 RAG：快速精确  return rag\_search(query, top\_k=5)    elif task\_type == "concept\_explore":  # RAG 导航 → Agentic 深读  rag\_results = rag\_search(query, top\_k=10)  candidate\_files = [r["file\_path"] for r in rag\_results]  return agentic\_deep\_read(query, candidate\_files=candidate\_files)    elif task\_type == "bug\_fix":  # 纯 Agentic：多步追踪  return agentic\_search(query, tools=[grep, read\_file, lsp\_refs])    elif task\_type == "large\_repo\_refactor":  # RAG 过滤范围 → Agentic 在小范围内精确探索  scope\_files = rag\_filter\_scope(query, max\_files=50)  return agentic\_search(query, scope=scope\_files) |

10. **实际案例分析**

**案例1：小型 Python 服务（15K LOC）**

|  |
| --- |
| Plain Text 背景：FastAPI 后端，~150个文件，团队3人 任务：修复用户登录失败的 bug  → 选 Agentic Search 理由：  ✓ 规模小，grep + read 可快速覆盖  ✓ Bug 修复需要追踪调用链  ✓ 无需建索引维护成本  ✓ 安全起见不想外传代码 |

**案例2：企业级 Java 服务（800K LOC）**

|  |
| --- |
| Plain Text 背景：金融后台系统，~8000个文件，多团队协作 任务：回答"支付流程是怎样的？"  → 选 RAG（主）+ Agentic（辅） 理由：  ✓ 规模大，纯 Agentic 会 token 爆炸  ✓ 概念性问答，RAG 语义搜索更合适  ✓ 有完整 CI/CD，索引可自动维护  ✓ 快速回答需求（< 5s） |

**案例3：开源项目贡献（200K LOC）**

|  |
| --- |
| Plain Text 背景：参与大型开源项目，理解架构并实现新功能 任务：理解 rendering pipeline 并添加新渲染器  → 选 Hybrid 阶段1 RAG：语义搜索"rendering pipeline"相关文件  → 快速获得候选文件列表（10-20 个文件） 阶段2 Agentic：在候选范围内深入追踪  → grep + read 理解具体实现 阶段3 生成：基于理解生成新渲染器代码 |

**案例4：10K 仓库企业平台（Qodo 实践）**

|  |
| --- |
| Plain Text 背景：SaaS 平台，服务企业客户，每个客户有多个仓库 任务：代码审查、问答、生成建议  → 必须 RAG（有向量索引） 理由：  ✓ 规模：10K个仓库，数百万文件，Agentic 完全不可行  ✓ 延迟：用户期望秒级响应  ✓ 多租户：每个客户独立向量索引  ✓ 持续更新：git hook 触发增量索引 |

**案例5：Claude Code 代码助手**

|  |
| --- |
| Plain Text 背景：本地 IDE 插件，用户单项目使用 任务：通用代码协助（问答/修复/生成）  → 选 Agentic Search（官方决策） 理由：  ✓ 本地代码，不想建外部向量库（安全）  ✓ 索引同步麻烦（代码频繁变化）  ✓ 模型足够强，可以自主探索  ✓ 大 context window 降低了 Agentic 成本 |

11. **KPI 驱动的决策方法**

|  |
| --- |
| SmartScope 推荐：不要用 LOC 阈值做决策，用可测量的 KPI 做 A/B 对比。 |

**3步 KPI 决策法**

|  |
| --- |
| Plain Text Step 1: 准备对比任务集（2-3个典型任务）  └─ Bug 修复任务 / 概念问答任务 / 新功能任务  Step 2: 同时用 RAG 和 Agentic Search 执行  └─ 记录：准确率 / token消耗 / 延迟 / 相关文件召回  Step 3: 基于数据做决策  └─ 哪个方案在你的任务集上综合表现更好 |

**关键 KPI 指标**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**总结**

**一句话决策原则**

|  |
| --- |
| Plain Text 代码规模小 + 任务复杂（多跳追踪）→ Agentic Search 代码规模大 + 任务简单（QA/文档）→ RAG 代码规模大 + 任务复杂 → Hybrid（RAG 收窄范围 + Agentic 深探） 延迟敏感 → RAG 安全敏感 → Agentic Search（无需外传代码） |

**快速对照表**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

|  |
| --- |
| **最终建议**：以 **Agentic Search 为骨架，RAG 为补充工具**。 对于大多数中小型项目，从纯 Agentic Search 开始，当且仅当遇到 token 爆炸或概念搜索瓶颈时，才引入 RAG 语义索引作为补充导航层。 |