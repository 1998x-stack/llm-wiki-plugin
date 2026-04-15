**AI 产品积分系统设计深度分析**

**Manus · v0.dev · 行业横向对比 · 可借鉴的设计原则**

|  |
| --- |
| 分析时间：2026 年 3 月 | 研究范围：Manus、v0.dev、Lovable、Bolt、Cursor、Replit、Builder.io |

**目录**

1. [Manus 积分系统解析](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#1-manus-%E7%A7%AF%E5%88%86%E7%B3%BB%E7%BB%9F%E8%A7%A3%E6%9E%90)
2. [v0.dev 积分系统解析](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#2-v0dev-%E7%A7%AF%E5%88%86%E7%B3%BB%E7%BB%9F%E8%A7%A3%E6%9E%90)
3. [行业横向对比](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#3-%E8%A1%8C%E4%B8%9A%E6%A8%AA%E5%90%91%E5%AF%B9%E6%AF%94)
4. [共性痛点与用户投诉](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#4-%E5%85%B1%E6%80%A7%E7%97%9B%E7%82%B9%E4%B8%8E%E7%94%A8%E6%88%B7%E6%8A%95%E8%AF%89)
5. [工程架构层面](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#5-%E5%B7%A5%E7%A8%8B%E6%9E%B6%E6%9E%84%E5%B1%82%E9%9D%A2)
6. [可借鉴的设计原则](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#6-%E5%8F%AF%E5%80%9F%E9%89%B4%E7%9A%84%E8%AE%BE%E8%AE%A1%E5%8E%9F%E5%88%99)
7. [综合建议与设计方案](https://claude.ai/chat/99342aeb-778c-4006-9b89-c919499049d6#7-%E7%BB%BC%E5%90%88%E5%BB%BA%E8%AE%AE%E4%B8%8E%E8%AE%BE%E8%AE%A1%E6%96%B9%E6%A1%88)

1. **Manus 积分系统解析**

**1.1 产品背景**

Manus 是由中国初创公司"蝴蝶效应"开发的自主 AI Agent 平台，区别于 ChatGPT 或 Claude 的对话式 AI，Manus 主打**无需持续人工介入的端到端任务自动化**。
 核心技术栈：LLM 链式调用 + 多工具协调 + 强化学习决策。

自 2025 年 3 月病毒式传播、邀请码被炒至 ¥50,000 后，2025 年 3 月 31 日正式上线付费计划。

**1.2 计划结构（当前）**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

|  |
| --- |
| 年付享 17% 折扣，Standard ~$16.60/月 |

**1.3 积分消耗机制**

|  |
| --- |
| Plain Text 任务积分消耗 = f(任务复杂度, 迭代次数, 工具调用数, 上下文长度) |

**关键特征：**

* **预执行无透明度**：Manus 在任务开始前**不显示预估积分消耗**，用户在提交请求时完全不知道花费
* **动态消耗**：Agent Mode 会根据任务难度自主决定工具调用次数，消耗极难预测
* **复杂任务开销**：据用户报告，单个复杂任务消耗 500–900 积分（占 Standard 计划月积分的 12%–22%）
* **失败不退积分**：Agent 陷入循环或任务执行失败，已消耗的积分不返还

**实际 ROI 计算（Standard $20/月）：**

|  |
| --- |
| Plain Text 4,000 积分 ÷ 每任务 500–900 积分 = 4–8 个有实质意义的任务/月 等效每任务成本：$2.50 – $5.00 |

**1.4 积分刷新策略**

|  |
| --- |
| Plain Text 每日刷新 300 积分（所有计划） ← 防止用户月初爆发式消耗 月度积分（4000 或 40000） ← 支撑大批量任务 首次注册奖励（1000 积分） ← 降低尝鲜门槛 |

**每日刷新设计的意图：**

* 保证轻度用户每天都有一定额度（即使月度积分耗尽）
* 拉长用户留存周期，避免"月初刷完、月底无用"
* 产生每日回访动机（类游戏的日常签到机制）

**1.5 团队积分池设计**

Team 计划采用**共享积分池**（Shared Credit Pool）：

* 所有成员共享同一个积分池
* 提供团队使用分析仪表盘
* 支持 SSO 和访问控制
* 单席位 4,000 积分/月（Pool 总量 = 席位数 × 4,000）

**优势**：灵活分配，避免成员独享配额浪费
**风险**：重度用户可能耗尽整个团队的积分

**1.6 用户体验痛点（来自真实用户反馈）**

|  |
| --- |
| Plain Text "Lost $39 in under 10 minutes" — Reddit 用户 "No warning, no control: Agent Mode 没有实时提醒，无法在用完前叫停" "Simple tasks = huge bills: 简单任务也可能螺旋式消耗数百积分" "I feel like I'm gambling every time I submit a prompt." |

**深层设计问题：**

1. 黑盒定价：积分消耗依赖算法黑盒，用户无法合理规划
2. Agent 自主性与可控性矛盾：越自主越好用，但越难预测成本
3. 无中断机制：执行中途没有"暂停并确认"的检查点

2. **v0.dev 积分系统解析**

**2.1 产品背景**

v0.dev 是 Vercel 开发的 AI 前端生成工具，核心定位是**text-to-UI 转换**：将自然语言描述直接转为 React + Tailwind CSS 组件。

**定价历史演进（关键节点）：**

|  |
| --- |
| Plain Text 早期（2023–2024）：~$20/月，近乎无限制生成 2024 年：200 message/月固定额度 2025 年 5 月：迁移至 token-based 信用体系 ← 引发社区强烈反弹 2025 年后：现行 token × model × 计划 三维定价体系 |

**2.2 计划结构（当前）**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**2.3 Token 计费机制（核心创新）**

v0 采用**双维度 token 计费**：

|  |
| --- |
| Plain Text 总费用 = (输入 token 数 × 输入单价) + (输出 token 数 × 输出单价) |

**不同模型的 token 单价（美元/百万 token）：**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

|  |
| --- |
| **输出 token 是输入的 5× 贵**，这是典型的生成式 AI 定价模式 |

**隐含 token 计费：**

* 聊天历史被计入输入 token（上下文感知代价）
* 上传文件（如 Figma 截图）计为大输入
* Vercel 专属知识库注入也计为输入

**2.4 积分滚存（Rollover）设计**

v0 的积分滚存政策是**行业较好实践之一**：

|  |
| --- |
| Plain Text 月度赠送积分 → 未使用 → 最多滚存 65 天后过期 购买额外积分 → 永不过期（年内）→ 先消耗月度赠送，再消耗购买积分 团队/企业计划 → 购买积分全团队共享 |

**设计意图：**

* 月度积分有限期避免公司收入确认（RevRec）复杂化
* 购买积分不过期，增加用户按需购买的意愿
* 消耗顺序：月度先行 → 购买兜底，符合用户直觉

**2.5 使用可视化（Dashboard）**

v0 提供相对完善的使用监控：

|  |
| --- |
| Plain Text /v0/settings/usage：  ├── 按日/周/月的使用汇总  ├── 每次交互的详细日志（日期、用户、事件类型、模型、费用）  └── 积分余额 + 账单页面  团队/企业版：  └── 全团队使用情况追踪（按成员维度） |

**2.6 迁移事件：从"无限"到"积分制"的教训**

2025 年 5 月，v0 将定价模式从固定月费（近乎无限使用）切换至 token 计费体系，引发社区强烈反弹：

**用户反应：**

|  |
| --- |
| Plain Text "We were paying to debug a tool still in beta." "I genuinely loved Vercel and v0. Now, I'm questioning everything." "Developers trust simplicity, predictability, and transparency." |

**事件分析：**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**Vercel 的修复措施：**

* 增加使用仪表盘
* 提供使用量预估
* 澄清 token-to-credit 换算关系

3. **行业横向对比**

**3.1 主流 AI 产品积分体系对比**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**3.2 定价模式分类**

|  |
| --- |
| Plain Text 模式 A：纯订阅（Flat Fee）  - 代表：ChatGPT Plus $20/月（对话）  - 优点：用户成本完全可预期  - 缺点：厂商难以控制重度用户成本  模式 B：按用量计费（Usage-Based）  - 代表：OpenAI API（$X/M tokens）  - 优点：线性成本，公平  - 缺点：用户焦虑，"惊喜账单"风险  模式 C：订阅 + 积分混合（Hybrid）  - 代表：v0.dev、Lovable、Cursor  - 优点：保底收入 + 控制超量  - 缺点：用户需要理解双层体系  模式 D：结果导向定价（Outcome-Based）  - 代表：Intercom Fin（$0.99/成功解决对话）  - 优点：极强的价值对齐  - 缺点："成功"定义复杂，争议多  模式 E：分层积分 + 每日刷新（Tiered + Daily Refresh）  - 代表：Manus（月度池 + 300/天）  - 优点：保持日活，轻度用户体验好  - 缺点：重度 Agent 任务成本黑盒 |

**3.3 Builder.io Agent Credits：最佳实践案例**

Builder.io 在 2025 年 8 月推出了目前行业内设计最合理的 Agent Credits 体系：

**核心设计特点：**

1. **统一货币**：所有 AI 操作共用一套积分体系
2. **Rollover with Cap**：未使用积分滚存到下月，但上限为月度额度的 2×（防止无限积累）
3. **差异化推理**：简单请求快速完成（消耗少），复杂任务深度推理（消耗多），费用自然反映工作量
4. **实时状态指示器**：Dashboard 清晰显示积分余额和即将耗尽警告

**设计哲学引述：**

|  |
| --- |
| "Quality first: The agent can think as long as needed without hitting arbitrary message caps.  Fair costs: You pay only for the computation you actually use.  No hidden limits: When a task gets hard, the agent scales up automatically." |

4. **共性痛点与用户投诉**

**4.1 "赌博感"问题（最普遍）**

几乎所有积分制 AI 产品都面临的核心矛盾：

|  |
| --- |
| Plain Text 用户提交任务 → 不知道花多少积分 → 积分消耗 → 事后才知道代价 |

**高频投诉原文：**

* "I feel like I'm gambling every time I submit a prompt"（Manus）
* "Three or four times today I found myself looking at my credit spend... This is not sustainable"（Lovable）
* "When I first saw Bolt I was in love... After using it for a couple of weeks, it is just burning tokens"（Bolt）
* "Lovable feels amazing at first—super fast iteration... but the credit burn starts creeping into your brain"（Lovable）

**4.2 Agent 循环耗积分（Agent-specific）**

**Agent Mode 的特有问题：**

* AI 陷入错误修复循环（fix → re-error → fix → re-error）
* 每轮循环消耗积分，但没有解决问题
* 没有"检测到循环→暂停"的机制
* 用户无法在积分耗尽前手动停止 Agent

**4.3 从无限到有限的信任崩塌**

v0 的案例是典型教训：从无限使用切换到积分制时：

* 老用户感到"产品倒退"
* 若期间产品质量未明显提升，用户认为在"为 Bug 付钱"
* 社区情绪蔓延，负面口碑扩散

**4.4 上下文成本隐性计费**

v0 将聊天历史、文件上传、知识库注入都计为输入 token，但很多用户不了解这一机制，导致：

* 同一个问题多次询问→消耗远超预期
* 上传高清图片→积分大幅消耗
* 长对话→上下文积累导致后续每次请求都更贵

5. **工程架构层面**

**5.1 积分系统的核心数据模型**

|  |
| --- |
| SQL -- 信用钱包表 CREATE TABLE credit\_wallets (  id UUID PRIMARY KEY,  customer\_id UUID NOT NULL,  credit\_type VARCHAR(50), -- "standard", "purchased", "promotional"  balance DECIMAL(18,6) NOT NULL DEFAULT 0,  created\_at TIMESTAMP,  updated\_at TIMESTAMP );  -- 积分明细账本（Append-Only Ledger） CREATE TABLE credit\_ledger (  id UUID PRIMARY KEY,  wallet\_id UUID REFERENCES credit\_wallets(id),  amount DECIMAL(18,6) NOT NULL, -- 正数为充值，负数为消耗  event\_type VARCHAR(50), -- "monthly\_grant", "purchase", "consumption", "refund", "expiry"  reference\_id UUID, -- 关联任务ID / 订阅ID  model\_used VARCHAR(50),  tokens\_input INT,  tokens\_output INT,  metadata JSONB,  created\_at TIMESTAMP NOT NULL );  -- 积分包 / Grant 表 CREATE TABLE credit\_grants (  id UUID PRIMARY KEY,  wallet\_id UUID REFERENCES credit\_wallets(id),  grant\_type VARCHAR(50), -- "recurring", "topup", "promotional"  initial\_amount DECIMAL(18,6),  remaining\_amount DECIMAL(18,6),  expires\_at TIMESTAMP,  rollover\_policy JSONB, -- {"max\_rollover": 2.0, "carry\_to\_next\_cycle": true}  priority INT -- 消耗顺序：月度赠送 > 购买积分 ); |

**5.2 原子性积分扣减**

**核心要求：积分扣减必须是原子操作**，防止并发导致超额消耗：

|  |
| --- |
| Python async def consume\_credits(wallet\_id: str, amount: float, reference\_id: str) -> bool:  async with db.transaction():  # 悲观锁 or 乐观锁  wallet = await db.query(  "SELECT \* FROM credit\_wallets WHERE id = $1 FOR UPDATE",  wallet\_id  )    if wallet.balance < amount:  raise InsufficientCreditsError(  available=wallet.balance,  required=amount  )    # 原子更新余额  await db.execute(  "UPDATE credit\_wallets SET balance = balance - $1 WHERE id = $2",  amount, wallet\_id  )    # 写入账本  await db.execute(  """INSERT INTO credit\_ledger   (wallet\_id, amount, event\_type, reference\_id)   VALUES ($1, $2, 'consumption', $3)""",  wallet\_id, -amount, reference\_id  )    return True |

**5.3 Rollover 策略实现**

|  |
| --- |
| Python class RolloverPolicy:  """  积分滚存策略  - 月度赠送积分：到期过期（或限期滚存 N 天）  - 购买积分：不过期（或 12 个月有效期）  - Builder.io 策略：滚存上限 = 当月额度 × 2  """    def apply\_rollover(self, wallet: CreditWallet, new\_cycle\_start: datetime):  grants = wallet.get\_active\_grants()    for grant in grants:  if grant.type == "monthly\_recurring":  if grant.rollover\_policy.get("carry\_to\_next\_cycle"):  max\_carry = grant.initial\_amount \* grant.rollover\_policy.get("max\_rollover", 1.0)  new\_balance = min(grant.remaining\_amount, max\_carry)  grant.remaining\_amount = new\_balance  grant.expires\_at = new\_cycle\_start + timedelta(days=65)  else:  grant.remaining\_amount = 0 # 过期清零    elif grant.type == "purchased":  pass # 购买积分不受周期影响 |

**5.4 预估成本（Pre-task Estimation）实现思路**

这是目前最关键的缺失功能，实现方案：

|  |
| --- |
| Python async def estimate\_task\_cost(task\_description: str, mode: str) -> CostEstimate:  """  任务执行前的成本预估    策略：  1. 基于历史任务相似度检索  2. 基于任务描述复杂度评分  3. 给出置信区间而非精确值  """    # 方案 A：基于历史数据的统计预估  similar\_tasks = await vector\_search(task\_description, top\_k=10)  if similar\_tasks:  costs = [t.actual\_cost for t in similar\_tasks]  return CostEstimate(  min\_credits=min(costs),  expected\_credits=np.percentile(costs, 50),  max\_credits=np.percentile(costs, 90),  confidence="high" if len(similar\_tasks) > 5 else "medium"  )    # 方案 B：基于 LLM 的复杂度评分  complexity\_score = await llm\_score\_complexity(task\_description)  base\_cost = BASE\_COSTS[mode]  estimated = base\_cost \* complexity\_score    return CostEstimate(  min\_credits=estimated \* 0.5,  expected\_credits=estimated,  max\_credits=estimated \* 3.0,  confidence="low"  ) |

6. **可借鉴的设计原则**

**原则 1：积分≠Token，需要抽象层**

**问题**：直接暴露 token 对普通用户没有直觉意义
**方案**：用"积分"、"Credits"、"消耗量"等抽象单位，在内部换算

|  |
| --- |
| Plain Text 用户看到：消耗了 50 积分 系统内部：150,000 input tokens + 80,000 output tokens |

**同时应该做**：在帮助文档中给出换算说明，让高级用户也能理解

**原则 2：执行前必须显示预估成本**

**当前行业现状**：几乎所有产品都不提供执行前预估（Manus 完全没有）
**用户期望**：就像出租车计价器，上车前知道大概多少钱

**最低可接受设计**：

|  |
| --- |
| Plain Text [提交按钮旁] ⚡ 预计消耗：50–200 积分（中等复杂任务） 📊 当前余额：1,200 积分 |

**高质量设计**：

|  |
| --- |
| Plain Text 任务分析结果：  · 预计步骤数：8–12 步  · 预计积分消耗：120–350 积分（P50: 180 积分）  · 历史相似任务平均：165 积分  · 置信度：中（首次尝试此类任务）  [确认执行] [调整任务范围] |

**原则 3：设置消耗上限 / 看门狗机制**

**专门针对 Agent Mode 的关键设计**：

|  |
| --- |
| Plain Text 用户可配置：  · 本次任务最多消耗 X 积分  · 达到 50% 时通知我  · 达到上限后：暂停并等待确认 / 直接停止  系统内置：  · 检测到 Agent 重复调用同一工具 N 次 → 暂停  · 检测到错误循环（连续 K 次失败）→ 暂停并报告 |

**原则 4：每日刷新机制**

Manus 的每日 300 积分是一个很好的设计：

**设计逻辑：**

|  |
| --- |
| Plain Text 每日刷新积分（较少）→ 保证所有用户每天有基本使用权 月度积分（较多）→ 支撑重度批量使用  效果：  · 轻度用户：主要依赖每日刷新，很少用到月度积分  · 重度用户：月度积分快速消耗，可能需要补购  · 流失用户：仍有每日少量使用，维持活跃度 |

**原则 5：Rollover 与积分生命周期管理**

**推荐方案（参考 Builder.io）：**

|  |
| --- |
| Plain Text 月度赠送积分：  ├── 未使用部分可滚存到下个周期  ├── 滚存上限 = 月度额度 × 2（防止无限积累）  └── 超出上限部分过期  购买积分：  ├── 永久有效（或 12 个月有效期）  ├── 消耗优先级低于月度赠送（先用赠送，再用购买）  └── 可在团队内共享  促销积分：  ├── 固定有效期（30/60/90 天）  └── 消耗优先级最高 |

**消耗顺序（优先级）：**

|  |
| --- |
| Plain Text 促销积分 > 月度赠送积分 > 购买积分 |

**原则 6：模型分级 + 用户自主选择**

v0 的模型分级（md/lg）是好的设计，但应该更明确地传达：

|  |
| --- |
| Plain Text 快速模式（经济型）：消耗 1× 积分，速度快，适合简单任务 标准模式：消耗 2× 积分，质量与速度平衡 深度模式（高级型）：消耗 5× 积分，最高质量，适合复杂任务  [用户主动选择，而非系统自动决定并事后计费] |

**原则 7：任务模式隔离计费**

**Manus 的 Chat Mode 与 Agent Mode 应该有清晰隔离：**

|  |
| --- |
| Plain Text Chat Mode（对话模式）：  · 低消耗：每次回复 1–5 积分  · 适合：问答、讨论、小任务  · 类比：出租车起步价  Agent Mode（自主任务模式）：  · 高消耗：每次任务 50–500+ 积分  · 适合：复杂端到端任务  · 类比：包车服务  [明确标识当前模式和对应的计费逻辑] |

**原则 8：使用量可视化仪表盘**

**v0 的做法是行业标杆，应该提供：**

|  |
| --- |
| Plain Text 使用量概览：  ├── 今日消耗 vs 昨日对比  ├── 本月消耗趋势图（折线图）  ├── 积分余额健康度（绿/黄/红）  └── 预计月底剩余积分  详细日志：  ├── 每次任务：时间、类型、消耗积分、使用模型  ├── 可按时间范围筛选  └── 可导出（CSV）  团队视图（Team 计划）：  ├── 按成员的消耗分布（横向柱状图）  ├── 高消耗任务识别  └── 积分配额分配建议 |

**原则 9：弹性追加与防断线设计**

**当积分耗尽时，用户不应直接断线：**

|  |
| --- |
| Plain Text 设计流程： 余额充足 → 正常执行 余额 < 20% → 警告提示（不阻断） 余额耗尽 →   · 已进行中的任务：继续完成当前步骤（不mid-task中断）  · 新任务：提示购买，展示快速充值选项  · 给予 24 小时宽限期积分（防止用户在关键时刻被打断） |

**原则 10：定价切换的用户教育**

v0 迁移事件的教训：

|  |
| --- |
| Plain Text 从旧模式迁移的 SOP：  1. 提前 30 天通知（邮件 + 产品内 banner）  2. 提供详细的对比说明：旧模式 vs 新模式  3. 给老用户过渡期额外积分奖励  4. 提供新模式下的使用量估算器  5. 开放 30 天双模式（用户自选）  6. 收集反馈并快速迭代说明文档 |

7. **综合建议与设计方案**

**7.1 理想积分系统架构图**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────────────┐ │ 积分系统全景 │ ├─────────────────┬───────────────────┬───────────────────────┤ │ 获取层 │ 消耗层 │ 管理层 │ │ │ │ │ │ · 订阅月度赠送 │ · 预估成本展示 │ · 实时余额展示 │ │ · 每日刷新积分 │ · 模型选择 │ · 消耗趋势图 │ │ · 购买额外积分 │ · 任务上限配置 │ · 详细日志 │ │ · 促销/推荐积分 │ · 模式切换（Chat │ · Rollover 状态 │ │ · 企业自定义 │ / Agent） │ · 快速充值入口 │ │ │ · 执行中进度追踪 │ · 低余额预警 │ │ │ · 超限暂停机制 │ · 团队分配分析 │ └─────────────────┴───────────────────┴───────────────────────┘ |

**7.2 推荐的积分计划结构**

|  |
| --- |
| Plain Text Free 计划（试用钩子）：  · 每日 X 积分刷新（固定）  · 首次注册额外奖励  · 功能：仅 Chat Mode，轻量任务  · 目的：体验价值，转化付费  基础付费计划（主力收入）：  · 月度积分池（较大）  · 每日刷新积分（较小，保底）  · 购买积分入口  · 全功能：Chat + Agent Mode  · Rollover：月度积分 1.5× 上限  高级/团队计划：  · 更大月度积分池  · 共享积分池（团队）  · 优先级处理队列  · 专属使用分析 + 配额分配  · Rollover：2× 上限 + 购买积分跨月 |

**7.3 关键成功指标（KPI）**

**业务层面：**

* 月活用户积分消耗率（太低 = 感知价值不足；太高 = 焦虑/流失）
* 积分用完前的流失率
* 追加购买积分转化率
* 积分耗尽→升级计划转化率

**产品体验层面：**

* 任务执行前预估积分准确率（P90 误差）
* 用户打开使用量 Dashboard 的频率
* 积分相关客服工单占比（越低越好）
* Agent Mode 循环耗积分事件发生率

**参考资料**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

*文档生成时间：2026 年 3 月 27 日*
*分析基于公开资料，产品定价可能随时更新，以各产品官方页面为准*