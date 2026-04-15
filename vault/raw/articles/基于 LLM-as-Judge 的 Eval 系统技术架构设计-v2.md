**基于 LLM-as-Judge 的 Eval 系统技术架构设计-v2**

|  |
| --- |
| **文档版本**：v2.0 | **适用场景**：RAG 知识问答系统、多模型切换、知识库/API 持续演进场景 |

**一、系统全景架构**

**1.1 核心组件与数据流**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────────────────────┐ │ 触发层 (Trigger Layer) │ │ [代码变更 PR] [模型版本升级] [知识库更新] [API 变更] [定时任务] │ └───────────────────────────────┬─────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────┐ │ 测试用例管理层 (Case Registry) │ │ │ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │ │ │ 测试用例库 │ │ 版本绑定元数据 │ │ 自动生成用例流水线 │ │ │ │ (PostgreSQL)│ │ (知识版本标签) │ │ (Trap Question Gen) │ │ │ └──────────────┘ └──────────────┘ └──────────────────────────┘ │ └───────────────────────────────┬─────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────┐ │ 评估执行层 (Eval Engine) │ │ │ │ Layer 1 Layer 2 Layer 3 │ │ [规则检查] ──► [小模型预判] ──► [大模型 Ensemble] │ │ (零成本) (1/50 成本) (仅模糊区间/关键用例) │ │ │ │ ┌──────────────────────────────┐ │ │ │ 智能缓存层 (Redis) │ │ │ │ Key: hash(输入+模型+知识版本 │ │ │ │ +Prompt模板版本) │ │ │ └──────────────────────────────┘ │ └───────────────────────────────┬─────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────┐ │ 结果聚合层 (Result Aggregator) │ │ │ │ ┌─────────────────┐ ┌──────────────┐ ┌──────────────────────┐ │ │ │ Ensemble 仲裁 │ │ 非功能指标 │ │ 能力雷达图生成 │ │ │ │ (投票/平均分) │ │ (延迟/错误率) │ │ (多维度可视化) │ │ │ └─────────────────┘ └──────────────┘ └──────────────────────┘ │ └───────────────────────────────┬─────────────────────────────────────┘  │  ┌───────────┴───────────┐  ▼ ▼  ┌─────────────────┐ ┌──────────────────────┐  │ 自动通过/拦截 │ │ 人工审核队列 │  │ (CI/CD Gate) │ │ (HiTL Workflow) │  └─────────────────┘ └──────────────────────┘ |

**1.2 核心设计原则**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**二、核心技术点深度分析**

**技术点 1：多法官 Ensemble + 能力雷达图**

|  |
| --- |
| **应对场景**：新模型上线评估、多模型横向对比 |

**痛点**

单一法官模型存在系统性偏见——以 GPT-4 为例，其 RLHF 训练偏好可能使其对风格相近的输出评分虚高；且单点法官无法量化评估的不确定性。

**解决方案**

**法官组合设计：**

* 选取 2-3 个来自**不同训练路线**的 SOTA 模型（如 GPT-4o + Claude 3.5 Sonnet + Gemini 1.5 Pro）
* 所有法官注入**统一评分 Rubric**（防止因理解歧义导致的分差）

|  |
| --- |
| YAML # 统一评分 Rubric 模板（注入每个法官） rubric:  dimensions:  - name: factual\_accuracy  weight: 0.35  criteria: "回答中的每一个事实主张是否均可由知识库核实"  - name: reasoning\_quality  weight: 0.30  criteria: "推理链是否完整、逻辑是否严密、是否存在跳步"  - name: completeness  weight: 0.20  criteria: "是否覆盖了问题的所有关键子问题"  - name: format\_clarity  weight: 0.15  criteria: "输出格式是否清晰、层次是否合理"  score\_range: [1, 10]  output\_format: "JSON only" |

**投票与仲裁策略：**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**统计显著性保护：**
 当测试集样本量 < 100 时，禁止仅凭平均分得出"模型 A 优于模型 B"的结论，需附上 95% 置信区间。

**能力雷达图输出（示例数据结构）：**

|  |
| --- |
| JSON {  "model\_id": "gpt-4o-2024-11-20",  "eval\_run\_id": "run\_20240315\_001",  "radar\_scores": {  "reasoning": { "score": 8.7, "ci\_95": [8.2, 9.1] },  "code\_generation":{ "score": 9.1, "ci\_95": [8.8, 9.4] },  "creative\_writing":{ "score": 7.3, "ci\_95": [6.9, 7.7] },  "factual\_qa": { "score": 8.2, "ci\_95": [7.8, 8.6] },  "instruction\_following": { "score": 9.0, "ci\_95": [8.7, 9.3] }  },  "baseline\_model\_id": "gpt-4-turbo-2024-04-09" } |

**权衡**

* ✅ 有效中和单一法官偏见，评估结果更可信
* ⚠️ 成本是单法官的 2-3 倍，需与分层策略联合使用
* ⚠️ 所有法官来自同一训练范式（RLHF）时，可能共享系统性偏见，建议定期引入人工黄金标注集做校准

**技术点 2：测试用例版本绑定 + 自动陷阱题生成**

|  |
| --- |
| **应对场景**：知识库持续更新、防止新旧知识混淆 |

**痛点**

知识库更新后，原有"正确答案"可能已失效，旧测试用例直接误报；同时无法验证模型是否真正学习了新知识，而非依赖参数记忆作答。

**解决方案**

**测试用例元数据模型：**

|  |
| --- |
| Python @dataclass class EvalCase:  case\_id: str  question: str  golden\_answer: str    # 版本绑定字段  min\_knowledge\_version: str # e.g. "kb\_v1.0.0"  max\_knowledge\_version: str # e.g. "kb\_v2.0.0"，None 表示永久有效  knowledge\_chunk\_ids: list[str] # 该用例依赖的知识块 ID    # 分类标签  case\_type: Literal[  "new\_knowledge", # 直接考查新知识  "conflict\_contrast", # 新旧知识对比（防混淆）  "boundary\_hallucination", # 知识库边界外（防幻觉）  "regression" # 回归旧知识是否遗忘  ]    # 生命周期  status: Literal["active", "deprecated", "pending\_review"]  created\_by: Literal["auto\_gen", "human"]  reviewed\_by: str | None # 人工审核者 ID  created\_at: datetime  deprecated\_at: datetime | None |

**版本路由规则：**

|  |
| --- |
| Python def get\_active\_cases(kb\_version: str, test\_type: str) -> list[EvalCase]:  """根据当前知识库版本和测试类型，路由到正确的用例集"""  if test\_type == "regression":  # 回归测试：加载 max\_version < current\_version 的旧用例  return cases\_where(max\_knowledge\_version < kb\_version)  else:  # 新功能测试：加载覆盖当前版本的用例  return cases\_where(  min\_knowledge\_version <= kb\_version <= max\_knowledge\_version  ) |

**自动陷阱题生成流水线：**

|  |
| --- |
| Plain Text 知识库更新事件  │  ▼ ┌─────────────────┐ │ Diff 提取 │ ← 对比新旧版本，提取变更知识块 │ (变更知识块) │ └────────┬────────┘  │  ▼ ┌─────────────────────────────────────────────────────┐ │ 问题生成 LLM（专用 Prompt） │ │ │ │ Per 变更块，生成三类题： │ │ ① 新知识题 ─── "根据最新规定，X 的处理方式是？" │ │ ② 对比题 ─── "之前 X 是 A，现在是否变更？" │ │ ③ 边界题 ─── "Y（知识库未覆盖）的情况如何？" │ └────────┬────────────────────────────────────────────┘  │  ▼ ┌─────────────────┐ ┌─────────────────────────────┐ │ 初步质检 │ ──► │ 人工抽检（分层抽样） │ │ (格式/去重) │ │ 新知识题: 100% 审核 │ │ │ │ 对比题: 50% 审核 │ │ │ │ 边界题: 30% 审核 │ └─────────────────┘ └────────────────┬────────────┘  │ 审核通过  ▼  ┌─────────────────────┐  │ 写入测试用例库 │  │ status=active │  └─────────────────────┘ |

**用例老化策略：**

* 某知识块被删除 → 关联用例自动标记 deprecated
* 用例连续 90 天无触发 → 进入 pending\_review 等待人工决定是否保留

**权衡**

* ✅ 从根本上解决"误报"和"漏检"双重问题
* ⚠️ 自动生成的题目质量依赖生成 LLM 的能力，需要精心设计 Prompt 并定期评估生成质量
* ⚠️ 人工审核是瓶颈，需预留足够带宽，高峰期知识库变更频繁时尤为明显

**技术点 3：黄金输出语义相似度 + 非功能指标监控**

|  |
| --- |
| **应对场景**：API 升级、Prompt 重构、输出格式变更 |

**痛点**

API 升级后输出"措辞变了但意思对"，字符串精确匹配误报率极高；同时质量评估容易遮蔽性能退化（质量好但延迟翻倍同样不可接受）。

**解决方案**

**语义相似度计算：**

|  |
| --- |
| Python class SemanticSimilarityEvaluator:  def \_\_init\_\_(self, embedding\_model: str = "text-embedding-3-small"):  # 支持多种 Embedding 后端：OpenAI / BGE / BCE / Qwen-embedding  self.embedder = EmbeddingFactory.create(embedding\_model)    def precompute\_golden(self, case: EvalCase) -> np.ndarray:  """预计算黄金答案 Embedding，存入向量库，避免重复计算"""  return self.embedder.embed(case.golden\_answer)    def evaluate(  self,   current\_output: str,   golden\_embedding: np.ndarray,  llm\_judge\_score: float  ) -> EvalResult:  current\_embedding = self.embedder.embed(current\_output)  similarity = cosine\_similarity(current\_embedding, golden\_embedding)    # 判定逻辑（AND 条件，双重保险）  # 阈值来源：在标注数据集上用 F1 最大化确定，而非人工拍脑袋  passed = (llm\_judge\_score >= self.calibrated\_score\_threshold) \  and (similarity >= self.calibrated\_similarity\_threshold)    return EvalResult(  passed=passed,  llm\_score=llm\_judge\_score,  semantic\_similarity=similarity,  # 辅助排查：分析分歧情况  divergence\_flag=(llm\_judge\_score >= 8 and similarity < 0.75)  ) |

|  |
| --- |
| **关键：阈值校准** calibrated\_score\_threshold 和 calibrated\_similarity\_threshold 不应硬编码，而应在 **人工标注黄金集**（至少 200 条）上，通过最大化 F1-Score 搜索最优阈值组合，并在每次大版本升级后重新校准。 |

**Embedding 模型选型参考：**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**非功能指标监控体系：**

|  |
| --- |
| Python @dataclass class NonFunctionalMetrics:  # 性能指标  latency\_p50: float # ms  latency\_p99: float # ms（核心监控点）  tokens\_per\_second: float # 吞吐率    # 可靠性指标  error\_rate\_5xx: float # 服务端错误率  timeout\_rate: float # 超时率    # 成本指标（新增）  prompt\_tokens: int  completion\_tokens: int  estimated\_cost\_usd: float # 基于当前模型定价实时计算    # 动态告警阈值（基于过去 N 天滚动统计）  @classmethod  def compute\_dynamic\_threshold(  cls,   metric\_name: str,   lookback\_days: int = 7,  sigma\_multiplier: float = 2.0  ) -> tuple[float, float]:  """  返回 (下界, 上界) = (均值 - k\*σ, 均值 + k\*σ)  超出上界告警；成本类指标只设上界  """  history = MetricsDB.query(metric\_name, days=lookback\_days)  mean, std = np.mean(history), np.std(history)  return (mean - sigma\_multiplier \* std, mean + sigma\_multiplier \* std) |

**黄金输出更新机制（常被忽视）：**
 当 API **有意变更**输出格式时（如从 Markdown 改为纯文本），需走"黄金输出升级流程"：人工确认变更意图 → 批量更新关联用例的 golden\_answer 和 golden\_embedding → 同步更新 min\_knowledge\_version 标签。禁止静默覆盖。

**权衡**

* ✅ 语义匹配大幅降低误报，AND 条件提高精准度
* ⚠️ 两个阈值需要持续维护，引入标注成本
* ⚠️ divergence\_flag（法官高分但语义低相似）是重要信号，需定期分析，可能暴露法官 Prompt 的问题

**技术点 4：分层评估策略 + 智能缓存**

|  |
| --- |
| **应对场景**：大规模测试集（万级用例）、高频 CI 触发 |

**痛点**

10,000 条用例全量走大模型法官，单次 Eval 成本约 $50-100，且单次运行时间可能超过 2 小时，无法作为 PR 合并的实时 Gate。

**解决方案**

**三层漏斗策略（成本从低到高）：**

|  |
| --- |
| Plain Text 10,000 条用例  │  ▼ Layer 1：规则层（成本≈$0，速度：毫秒级） ┌─────────────────────────────────────────┐ │ · JSON/XML 格式合法性校验 │ │ · 必填字段存在性检查 │ │ · 关键词黑名单过滤（幻觉词/禁用词） │ │ · 长度合法性检查（过短/过长均异常） │ └──────────────┬──────────────────────────┘  │ 通过: ~80% 失败: ~20% → 直接标记 FAIL  ▼ Layer 2：小模型层（成本≈$2，速度：分钟级） ┌─────────────────────────────────────────┐ │ · 使用 Llama-3.1-8B / Qwen2.5-7B │ │ · 输出置信区间而非单一分数 │ │ · 高置信通过（≥7.5分，置信度高）→ PASS │ │ · 高置信失败（≤3.5分，置信度高）→ FAIL │ │ · 模糊区间 (3.5-7.5) → 进入 Layer 3 │ └──────────────┬──────────────────────────┘  │ 模糊区间: ~25%  ▼ Layer 3：大模型 Ensemble（成本≈$8，速度：分钟级） ┌─────────────────────────────────────────┐ │ · 仅处理模糊区间用例 + 所有关键用例 │ │ · 2-3 个 SOTA 法官 Ensemble │ │ · 输出最终评分 + 详细推理链 │ └─────────────────────────────────────────┘  总成本：≈$10（vs 全量走大模型的 $100），节省约 90% |

|  |
| --- |
| **Layer 2 校准要求**：小模型的"高置信区间"边界需在标注数据集上验证。目标：小模型高置信判断的准确率应 > 95%，确保不会把需要大模型判断的案例错误过滤。 |

**智能缓存设计：**

|  |
| --- |
| Python class EvalCache:  """  缓存 Key 的设计决定了缓存的有效性和安全性  任何影响输出的因素变化，都必须使缓存失效  """    @staticmethod  def build\_cache\_key(eval\_request: EvalRequest) -> str:  components = {  "input\_hash": sha256(eval\_request.input\_text),  "model\_id": eval\_request.model\_id, # e.g. "gpt-4o-2024-11-20"  "kb\_version": eval\_request.kb\_version, # e.g. "kb\_v2.3.1"  "judge\_prompt\_version": eval\_request.judge\_prompt\_version, # e.g. "judge\_v1.4"  "rubric\_version": eval\_request.rubric\_version, # e.g. "rubric\_v2.0"  }  return sha256(json.dumps(components, sort\_keys=True))    def get\_or\_evaluate(self, request: EvalRequest) -> EvalResult:  key = self.build\_cache\_key(request)    if cached := self.redis.get(key):  self.metrics.increment("cache\_hit")  return EvalResult.from\_cache(cached)    self.metrics.increment("cache\_miss")  result = self.evaluator.run(request)  self.redis.setex(key, ttl=self.ttl\_seconds, value=result.to\_json())  return result |

|  |
| --- |
| **缓存监控指标**：cache\_hit\_rate 应持续跟踪。正常情况下，纯回归测试的命中率应 > 70%；若长期低于 30%，说明某个版本字段频繁变化，需检查发布节奏。 |

**优先级调度（大规模场景补充）：**

|  |
| --- |
| YAML # 测试用例优先级配置 priority\_config:  P0\_critical: # 立即执行，阻塞 CI Gate  - case\_type: boundary\_hallucination  - case\_type: conflict\_contrast  - tags: ["safety", "core\_business"]    P1\_high: # 30min 内完成  - case\_type: new\_knowledge  - tags: ["regression\_core"]    P2\_normal: # 可异步完成，不阻塞合并  - case\_type: regression  - tags: ["edge\_case"] |

**权衡**

* ✅ 成本降低 80-90%，CI 反馈时间从小时级缩短到分钟级
* ⚠️ Layer 2 小模型校准是核心风险点，需持续监控其"假高分"和"假低分"率
* ⚠️ 缓存 TTL 设置需权衡：太短节省不了钱，太长可能在模型热修复后返回过期结果

**三、测试集生命周期管理**

|  |
| --- |
| Plain Text 创建阶段 运行阶段 维护阶段 退役阶段  │ │ │ │  ▼ ▼ ▼ ▼ 人工设计/自动生成 → CI/CD 触发执行 → 定期质量审查 → 版本 EOL 归档  │ │ │  │ 结果持久化 发现低质量用例  │ (每次Eval完整记录) (假阳性率高)  │ │  └──────────────────────────────────────►  人工修订/替换 |

**测试集健康度指标（每月审查）：**

* **覆盖率**：知识库各领域的用例分布是否均衡
* **假阳性率**：(被判 PASS 但人工认为应 FAIL 的用例数) / 总用例数 < 2%
* **老化率**：deprecated 状态用例占比，超过 20% 需触发全面清理

**四、CI/CD 集成设计**

|  |
| --- |
| Plain Text 代码/模型/知识库变更 Push  │  ▼  [PR Opened / Merged]  │  ├─── P0 用例集（~500条）────► 分层评估（5min）────► CI Gate 决策  │ │  │ Pass ◄──┤──► Fail → 阻塞合并  │ │ + 通知责任人  └─── P1/P2 用例集（全量）───► 异步后台运行 ──────────► 结果写入 Dashboard |

**Gate 判定规则：**

|  |
| --- |
| YAML ci\_gate\_policy:  block\_merge\_if:  - p0\_pass\_rate < 0.95 # P0 用例通过率低于 95%  - any\_p0\_safety\_case\_failed # 任意安全类 P0 用例失败  - latency\_p99\_regression > 0.3 # P99 延迟回归超过 30%  - error\_rate\_5xx > 0.01 # 错误率超过 1%    warn\_only\_if:  - overall\_pass\_rate < 0.90 # 全量通过率低于 90%（警告但不阻塞）  - cost\_increase > 0.20 # 单次推理成本增长超过 20% |

**五、人工介入（HiTL）工作流**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**六、关键指标 Dashboard**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**七、快速决策参考**

**选择法官评估模式：**

|  |
| --- |
| Plain Text 问题："哪个更好，A 还是 B？" → 排名制（多数票决） 问题："这个回答质量如何？" → 评分制（加权平均） 问题："多个维度分别怎么样？" → 维度制（雷达图） |

**选择 Embedding 策略：**

|  |
| --- |
| Plain Text 私有化部署 + 中文为主 → BGE-M3 / Qwen3-Embedding OpenAI 生态 → text-embedding-3-small 成本极度敏感 → text-embedding-3-small（极低成本） |

**缓存 TTL 推荐：**

|  |
| --- |
| Plain Text 开发环境（频繁变更） → TTL = 1小时 Staging 环境 → TTL = 24小时 生产环境回归测试 → TTL = 7天（只要版本 Key 未变） |