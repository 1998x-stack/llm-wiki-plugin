**基于 LLM-as-Judge 的 Eval 系统技术架构设计 v3.0**

|  |
| --- |
| **版本**：v3.0（论文驱动增强版） **理论依据**：GAMA-Bench / MT-Bench / Judging the Judges / Prometheus 2 / RAGAS / Preference Leakage **更新日期**：2025 年 3 月 |

**一、系统全景架构**

**1.1 整体数据流**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────────────────────────────┐ │ 触发层 (Trigger Layer) │ │ │ │ [PR / 代码变更] [模型版本升级] [知识库 Diff] [API Changelog] [定时任务] │ │ │ │ │ │ │ │ │ └────────────────┴───────────────┴───────────────┴─────────────┘ │ │ │ │ │ 事件分类 & 路由 │ │ ┌──────────────┼──────────────┐ │ │ 模型切换 知识变动 API变动 │ └────────────────────┼──────────────┼──────────────┼──────────────────────────┘  │ │ │  ▼ ▼ ▼ ┌─────────────────────────────────────────────────────────────────────────────┐ │ 测试用例管理层 (Case Registry v2) │ │ │ │ ┌──────────────────┐ ┌─────────────────────┐ ┌───────────────────────┐ │ │ │ 静态用例库 │ │ 版本绑定元数据 │ │ 动态用例生成器 │ │ │ │ (PostgreSQL) │ │ (KB版本 + 知识块ID) │ │ (GAMA风格参数化生成) │ │ │ │ · 人工标注集 │ │ min/max\_kb\_version │ │ · 自动陷阱题生成 │ │ │ │ · 黄金答案集 │ │ judge\_prompt\_ver │ │ · 对抗场景生成 │ │ │ └──────────────────┘ └─────────────────────┘ └───────────────────────┘ │ └─────────────────────────────────────────────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────────────┐ │ 法官健康检查层 (Judge Health Check) │ │ ← 论文依据：Judging the Judges (2406.07791) │ │ │ │ 每次评估前，对法官本身运行偏差校验： │ │ · RS (重复稳定性) ≥ 0.85 · PC (位置一致性) ≥ 0.80 │ │ · PF (偏好公平性) 0.45-0.55 · 偏好泄漏风险检测 │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ 法官池 (Judge Pool) — 跨家族选取，防 Preference Leakage │ │ │ │ Judge-A: GPT-4o (OpenAI 家族) │ │ │ │ Judge-B: Claude-3.5 (Anthropic 家族) │ │ │ │ Judge-C: Prometheus-2 (开源独立专用评估模型) │ │ │ └────────────────────────────────────────────────────────┘ │ └─────────────────────────────────────────────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────────────┐ │ 评估执行层 (Eval Engine v2) │ │ │ │ Layer 1 Layer 2 Layer 3 │ │ [规则层] ──────► [小模型预判] ──────► [Ensemble 法官] │ │ (格式/关键词) (Prometheus-2 (仅模糊区间) │ │ 成本: ~$0 或开源小模型) 成本: ~$8 per 10K │ │ 成本: ~$2 │ │ │ │ ┌─────────────────────────────────────────────────────────────┐ │ │ │ 评估类型路由 (Eval Mode Router) │ │ │ │ 模型切换 → 成对排名 (Pairwise) + 能力雷达图 │ │ │ │ 知识变动 → RAGAS 四维评估 + 幻觉检测 │ │ │ │ API变动 → 语义相似度 + 非功能指标 + 单答案打分 │ │ │ └─────────────────────────────────────────────────────────────┘ │ │ │ │ ┌─────────────────────────────────────────────────────────────┐ │ │ │ 智能缓存层 (Redis) │ │ │ │ Key: hash(输入 + 模型版本 + KB版本 + judge\_prompt版本) │ │ │ └─────────────────────────────────────────────────────────────┘ │ └─────────────────────────────────────────────────────────────────────────────┘  │  ▼ ┌─────────────────────────────────────────────────────────────────────────────┐ │ 结果聚合层 (Result Aggregator v2) │ │ │ │ ┌──────────────────┐ ┌─────────────────┐ ┌────────────────────────────┐ │ │ │ Ensemble 仲裁 │ │ RAGAS 指标聚合 │ │ 非功能指标 (延迟/错误率) │ │ │ │ (跨家族投票) │ │ (Faithfulness │ │ 动态阈值 (7天均值±2σ) │ │ │ │ 偏差修正后输出 │ │ + 4维评估) │ │ 成本追踪 (token用量) │ │ │ └──────────────────┘ └─────────────────┘ └────────────────────────────┘ │ └─────────────────────────────────────────────────────────────────────────────┘  │  ┌───────────┴───────────┐  ▼ ▼  ┌─────────────────┐ ┌──────────────────────┐  │ CI/CD Gate 决策 │ │ 人工审核队列 (HiTL) │  │ (自动通过/拦截) │ │ 偏差分歧/边界用例 │  └─────────────────┘ └──────────────────────┘ |

**1.2 核心设计原则（论文驱动）**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**二、场景一：模型切换的核心技术设计**

|  |
| --- |
| **论文基础**：MT-Bench / Judging the Judges / Prometheus 2 / Preference Leakage |

**痛点**

单一法官的多重偏差风险：自我增强偏差（偏好同家族模型输出）、位置偏差（偏好 Prompt 中排第一的候选）、Preference Leakage（若评估模型和被测模型都用 GPT 系训练数据，分数虚高）。

**解决方案**

**法官 Ensemble 设计（跨家族原则）**

|  |
| --- |
| Python # 法官池设计 — 基于 Preference Leakage 论文的防污染原则 JUDGE\_POOL = {  "judge\_a": {  "model": "gpt-4o-2024-11-20",  "family": "openai", # 家族标签，用于偏漏检测  "type": "proprietary",  },  "judge\_b": {  "model": "claude-3-5-sonnet-20241022",  "family": "anthropic",  "type": "proprietary",  },  "judge\_c": {  "model": "prometheus-2-8x7b", # 完全独立的专用评估模型  "family": "open\_source\_eval", # 非 RLHF 同源  "type": "open\_source",  }, }  # 被测模型与法官的家族冲突检测 def check\_preference\_leakage\_risk(  target\_model\_family: str, judge\_pool: dict ) -> list[str]:  """  若法官与被测模型同家族，自动降权或排除该法官  返回: 低风险法官 ID 列表  """  safe\_judges = []  for judge\_id, info in judge\_pool.items():  if info["family"] != target\_model\_family:  safe\_judges.append(judge\_id)  else:  logger.warning(f"Judge {judge\_id} shares family with target model, excluded")  return safe\_judges |

**法官偏差校验（Judging the Judges 实践）**

|  |
| --- |
| Python @dataclass class JudgeBiasMetrics:  """  三指标偏差校验体系 — 基于 Shi et al. (2406.07791)  """  repetition\_stability: float # RS: 同问题重复3次，最高频选择的占比  position\_consistency: float # PC: 交换候选顺序后，判断一致的比率  preference\_fairness: float # PF: 整体偏向某位置的程度（理想值 ~0.5）    def is\_reliable(self) -> bool:  return (  self.repetition\_stability >= 0.85 and  self.position\_consistency >= 0.80 and  0.40 <= self.preference\_fairness <= 0.60  )    def bias\_warning(self) -> str | None:  if self.position\_consistency < 0.80:  return f"⚠️ 位置偏差严重 (PC={self.position\_consistency:.2f}), 建议排除此法官"  if not (0.40 <= self.preference\_fairness <= 0.60):  return f"⚠️ 偏好不公平 (PF={self.preference\_fairness:.2f}), 建议随机交换候选顺序"  return None |

**统一评分 Rubric（MT-Bench / Prometheus 2 范式）**

|  |
| --- |
| YAML # judge\_rubric\_v2.1.yaml — 版本化管理，不静默变更 rubric\_version: "v2.1" created\_at: "2025-03-15" changelog: "增加游戏场景专用维度：任务执行准确性"  # 要求法官必须输出 CoT 推理链（MT-Bench 实证有效） require\_chain\_of\_thought: true  dimensions:  - id: factual\_accuracy  name: 事实准确性  weight: 0.35  prompt: "回答中每一个事实主张是否均可由知识库验证？"  score\_anchors:  1: "存在明显的事实错误或完全幻觉"  3: "部分事实准确，但存在一处以上的错误或遗漏"  5: "所有事实均可在知识库中核实"   - id: reasoning\_quality  name: 推理质量  weight: 0.25  prompt: "推理链是否完整？逻辑是否严密？是否存在跳步？"   - id: task\_execution  name: 任务执行准确性（游戏场景专用）  weight: 0.25  prompt: "Agent 是否正确理解并执行了游戏任务指令？边界条件处理是否正确？"   - id: format\_clarity  name: 格式清晰度  weight: 0.15  prompt: "输出格式是否清晰？层次是否合理？"  output\_format: "JSON: {reasoning: string, scores: {dim\_id: int}, final\_score: float}" |

**仲裁策略（含统计显著性保护）**

|  |
| --- |
| Python class EnsembleArbiter:  def arbitrate(self, judge\_results: list[JudgeResult]) -> ArbiterOutput:  scores = [r.final\_score for r in judge\_results]  mean\_score = np.mean(scores)  std\_score = np.std(scores)  max\_diff = max(scores) - min(scores)    # 加权平均（按法官可靠性指标加权）  weights = [self.\_compute\_judge\_weight(r.judge\_id) for r in judge\_results]  weighted\_score = np.average(scores, weights=weights)    # 人工介入触发条件  needs\_human = (  max\_diff > 2.5 or # 任意两法官分差过大  std\_score > 1.5 or # 方差过高  any(r.divergence\_flag for r in judge\_results) # 高分低相似  )    # 统计显著性保护（样本量 < 100 时禁止绝对结论）  sample\_size = len(judge\_results)  ci\_95 = self.\_compute\_confidence\_interval(scores, sample\_size)    return ArbiterOutput(  final\_score=weighted\_score,  confidence\_interval=ci\_95,  needs\_human\_review=needs\_human,  arbitration\_note=f"std={std\_score:.2f}, max\_diff={max\_diff:.2f}",  # 统计警告：样本量不足时附加警告  statistical\_warning=(  "⚠️ 样本量 < 100，置信区间较宽，不建议作出'模型A优于B'的绝对结论"  if sample\_size < 100 else None  ),  ) |

**能力雷达图输出**

|  |
| --- |
| JSON {  "eval\_run\_id": "run\_20250315\_model\_switch\_001",  "target\_model": "gpt-4o-2025-01-01",  "baseline\_model": "gpt-4o-2024-11-20",  "judges\_used": ["judge\_a\_claude35", "judge\_c\_prometheus2"],  "judges\_excluded": ["judge\_b\_gpt4o (same family as target)"],  "radar\_scores": {  "factual\_accuracy": { "target": 8.7, "baseline": 8.2, "delta": +0.5, "ci\_95": [8.3, 9.1] },  "reasoning\_quality": { "target": 9.1, "baseline": 8.8, "delta": +0.3, "ci\_95": [8.7, 9.4] },  "task\_execution": { "target": 7.3, "baseline": 7.8, "delta": -0.5, "ci\_95": [6.9, 7.7] },  "format\_clarity": { "target": 8.5, "baseline": 8.4, "delta": +0.1, "ci\_95": [8.2, 8.8] }  },  "regression\_alert": "task\_execution 出现回退 (delta=-0.5)，建议人工审查",  "preference\_leakage\_risk": "低（已排除同家族法官）" } |

**三、场景二：知识变动的核心技术设计**

|  |
| --- |
| **论文基础**：RAGAS / GAMA-Bench 动态场景 / MT-Bench |

**痛点**

知识库更新后，旧测试题的"正确答案"可能已失效，导致误报；无法验证模型是否真正学到了新知识；传统字符串匹配无法区分"回答措辞变化"和"内容变化"。

**解决方案**

**测试用例版本绑定数据模型**

|  |
| --- |
| Python @dataclass class EvalCase:  case\_id: str  question: str  golden\_answer: str  golden\_embedding: np.ndarray # 预计算，避免重复 Embedding    # 版本绑定字段  min\_kb\_version: str # e.g. "kb\_v1.0.0"  max\_kb\_version: str | None # None 表示永久有效  kb\_chunk\_ids: list[str] # 依赖的知识块 ID    # RAGAS 专用字段  expected\_contexts: list[str] # 期望被检索到的上下文（用于 Context Recall）    # 题型分类（基于 GAMA-Bench 分类思想）  case\_type: Literal[  "new\_knowledge", # 直接考查新知识  "conflict\_contrast", # 新旧知识对比（防混淆）  "boundary\_hallucination", # 知识库边界外（防幻觉）  "regression", # 回归旧知识是否遗忘  ]    status: Literal["active", "deprecated", "pending\_review"]  reviewed\_by: str | None |

**RAGAS 四维评估集成**

|  |
| --- |
| Python class KnowledgeChangeEvaluator:  """  基于 RAGAS 框架的知识变动专用评估器  论文：Es et al., EACL 2024 (2309.15217)  """    def evaluate(  self,  case: EvalCase,  retrieved\_contexts: list[str],  generated\_answer: str,  ) -> RAGASResult:    # 维度1：上下文精度 — 检索的内容中多少是真正需要的  context\_precision = self.\_compute\_context\_precision(  question=case.question,  retrieved\_contexts=retrieved\_contexts,  golden\_contexts=case.expected\_contexts,  )    # 维度2：上下文召回 — 需要的信息是否都检索回来了  context\_recall = self.\_compute\_context\_recall(  golden\_answer=case.golden\_answer,  retrieved\_contexts=retrieved\_contexts,  )    # 维度3：忠实度 — 回答有无幻觉（原子化分解策略）  faithfulness = self.\_compute\_faithfulness\_atomic(  generated\_answer=generated\_answer,  retrieved\_contexts=retrieved\_contexts,  )    # 维度4：答案相关性 — 回答是否真的回答了问题  answer\_relevance = self.\_compute\_answer\_relevance(  question=case.question,  generated\_answer=generated\_answer,  )    # 知识变动专属：幻觉位置定位  hallucination\_statements = self.\_locate\_hallucination(  generated\_answer=generated\_answer,  retrieved\_contexts=retrieved\_contexts,  )    return RAGASResult(  context\_precision=context\_precision,  context\_recall=context\_recall,  faithfulness=faithfulness,  answer\_relevance=answer\_relevance,  hallucination\_statements=hallucination\_statements,  # 通过标准：所有维度 > 0.8 AND faithfulness > 0.9（忠实度要求更严）  passed=(  min(context\_precision, context\_recall, answer\_relevance) > 0.8  and faithfulness > 0.9  ),  )    def \_compute\_faithfulness\_atomic(  self, generated\_answer: str, retrieved\_contexts: list[str]  ) -> float:  """  RAGAS 的原子化分解策略：  1. LLM 将回答拆分为最小原子陈述  2. 逐条验证每个陈述是否在上下文中有依据  3. faithfulness = 有依据的陈述数 / 总陈述数  """  statements = self.\_decompose\_to\_atoms(generated\_answer)  supported = sum(  1 for stmt in statements  if self.\_is\_supported\_by\_context(stmt, retrieved\_contexts)  )  return supported / len(statements) if statements else 0.0 |

**自动陷阱题生成流水线（GAMA-Bench 动态场景思想）**

|  |
| --- |
| Plain Text 知识库更新 Diff 提取  │  ▼ ┌─────────────────────────────────────────────────────────┐ │ 参数化题目生成（GAMA 动态场景范式） │ │ │ │ 输入参数： │ │ · changed\_chunks: 变更的知识块列表 │ │ · change\_type: [新增/更新/删除] │ │ · domain: [游戏规则/NPC对话/技能系统/...] │ │ │ │ 输出三类题（每变更块各生成）： │ │ ① 新知识题 → "根据最新规则，X 技能的冷却时间是？" │ │ ② 对比题 → "该技能的冷却时间从 3 秒改为多少秒？" │ │ ③ 边界题 → "X 技能在 [未记录的边缘场景] 下如何？" │ └──────────────────────┬──────────────────────────────────┘  │  ▼  分层抽检（新知识100%，对比题50%，边界题30%）  │  ▼ 审核通过  写入用例库（case\_type + kb\_version 标签） |

**评估结果 × 用例类型矩阵**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**四、场景三：API 变动的核心技术设计**

|  |
| --- |
| **论文基础**：MT-Bench 单答案打分 / Prometheus 2 可定制 Rubric / RAGAS 忠实度 |

**痛点**

API 升级后输出"措辞变了但意思对"，字符串匹配误报率极高；需要同时保障质量和性能不退化；黄金输出随 API 有意变更时需要安全更新机制。

**解决方案**

**语义相似度 + LLM 法官双重验证**

|  |
| --- |
| Python class APIChangeEvaluator:  """  API 变动专用评估器：语义相似度 AND 法官评分双重门控  阈值基于标注集 F1 最大化校准，非人工拍脑袋  """    def evaluate(  self,  case: EvalCase,  current\_output: str,  judge\_score: float,  ) -> APIEvalResult:  # 语义相似度（使用预计算的黄金 Embedding）  current\_embedding = self.embedder.embed(current\_output)  similarity = cosine\_similarity(current\_embedding, case.golden\_embedding)    # 双重门控判定  passed = (  judge\_score >= self.calibrated\_score\_threshold # 默认 >= 7.5，校准后决定  and similarity >= self.calibrated\_similarity\_threshold # 默认 >= 0.85  )    # 分歧信号：法官高分但语义低相似 → 可能是法官 Prompt 有漏洞  divergence\_flag = (judge\_score >= 8.0 and similarity < 0.70)    return APIEvalResult(  passed=passed,  judge\_score=judge\_score,  semantic\_similarity=similarity,  divergence\_flag=divergence\_flag,  ) |

|  |
| --- |
| **阈值校准方法**：在人工标注的黄金集（至少 200 条）上，通过格搜索 (score\_threshold, similarity\_threshold) 组合，找到 F1-Score 最大的参数对，每次大版本升级后重新校准一次。 |

**黄金输出安全更新协议**

|  |
| --- |
| Plain Text 触发场景：API 有意变更输出格式（如从 Markdown 改为纯文本）  安全更新流程：  Step 1: 工程师在 PR 中标记 "golden\_update" 类型  Step 2: CI 自动检测关联的测试用例（通过 kb\_chunk\_ids）  Step 3: 生成新旧对比报告供人工确认意图  Step 4: 确认后批量重新计算 golden\_embedding  Step 5: 同步更新 min\_kb\_version 标签  ⚠️ 禁止静默覆盖：必须留下变更记录 + 责任人签名 |

**非功能指标监控体系**

|  |
| --- |
| Python @dataclass class NonFunctionalMetrics:  # 性能指标  latency\_p50\_ms: float  latency\_p99\_ms: float # 核心监控点  tokens\_per\_second: float    # 可靠性  error\_rate\_5xx: float  timeout\_rate: float    # 成本（API 变动后尤为重要）  prompt\_tokens: int  completion\_tokens: int  estimated\_cost\_usd: float # 实时计算    # 动态告警阈值（7天滚动均值 ± 2σ）  @classmethod  def compute\_dynamic\_threshold(  cls,  metric\_name: str,  lookback\_days: int = 7,  sigma\_multiplier: float = 2.0,  ) -> tuple[float, float]:  history = MetricsDB.query(metric\_name, days=lookback\_days)  mean, std = np.mean(history), np.std(history)  return (mean - sigma\_multiplier \* std, mean + sigma\_multiplier \* std) |

**API 变动 CI Gate 条件**：

|  |
| --- |
| YAML api\_change\_gate:  block\_if:  - semantic\_similarity\_avg < 0.80 # 语义退化  - judge\_score\_avg < 7.0 # 质量退化  - latency\_p99\_regression\_pct > 0.30 # P99 延迟回归超 30%  - error\_rate\_5xx > 0.01 # 错误率超 1%  - divergence\_flag\_rate > 0.15 # 高分低相似（法官 Prompt 可能有问题）  warn\_if:  - cost\_increase\_pct > 0.20 # 成本增加超 20%  - golden\_embedding\_staleness\_days > 30 # 黄金 Embedding 超 30 天未更新 |

**五、降本增效：分层评估 + 智能缓存 v2**

**三层漏斗（含 Prometheus 2 作为 Layer 2）**

|  |
| --- |
| Plain Text 10,000 条用例  │  ▼ Layer 1：规则层（成本≈$0，速度：毫秒） ┌────────────────────────────────────────────────────┐ │ · JSON/XML 格式合法性 │ │ · 必填字段存在性 + 关键词黑名单 │ │ · 幻觉词检测（直接拒绝） │ │ 通过: ~80% 失败: ~20% → 直接 FAIL │ └───────────────────────┬────────────────────────────┘  │  ▼ Layer 2：Prometheus-2 小模型层（成本≈$2） ┌────────────────────────────────────────────────────┐ │ · 使用 Prometheus-2-7B 进行自定义 Rubric 评估 │ │ · 优势：支持与 Layer 3 相同的 Rubric，分数可比 │ │ · 高置信 PASS (≥7.5分, confidence>0.9) → PASS │ │ · 高置信 FAIL (≤3.5分, confidence>0.9) → FAIL │ │ · 模糊区间 (3.5-7.5) → 进入 Layer 3 │ └───────────────────────┬────────────────────────────┘  │ 约 25% 进入 Layer 3  ▼ Layer 3：跨家族 Ensemble（成本≈$8） ┌────────────────────────────────────────────────────┐ │ · 2-3 个不同家族 SOTA 法官 │ │ · 输出完整 CoT 推理链 + 维度分解分数 │ │ · 仅处理模糊区间 + 所有 P0 关键用例 │ └────────────────────────────────────────────────────┘  总成本对比：  全量走大模型：≈ $100  三层漏斗： ≈ $10 (节省 90%) |

|  |
| --- |
| **Layer 2 校准要求**：Prometheus-2 在模糊区间的分类准确率必须 > 95%（在标注集上验证），防止"假高分"绕过 Layer 3 漏检。 |

**智能缓存 Key 设计**

|  |
| --- |
| Python def build\_cache\_key(request: EvalRequest) -> str:  """  Cache Key 必须覆盖所有影响输出的因素  任何一个因素变化都必须使缓存失效  """  components = {  "input\_hash": sha256(request.input\_text),  "target\_model\_id": request.target\_model\_id, # e.g. "gpt-4o-2024-11-20"  "kb\_version": request.kb\_version, # e.g. "kb\_v2.3.1"  "judge\_prompt\_version": request.judge\_prompt\_version, # e.g. "judge\_v2.1"  "rubric\_version": request.rubric\_version, # e.g. "rubric\_v2.1"  "eval\_mode": request.eval\_mode, # pairwise/single/ragas  }  return sha256(json.dumps(components, sort\_keys=True)) |

**缓存命中率监控**：cache\_hit\_rate 正常应 > 60%。若持续 < 30%，说明某版本字段频繁变化，需排查发布节奏。

**六、法官偏差元评估体系（Eval-of-Eval）**

|  |
| --- |
| 对评估系统本身进行定期校验，防止系统性偏差累积 |

**月度元评估流程**

|  |
| --- |
| Plain Text Step 1: 构建元评估数据集  从历史用例中抽取 200 条，人工重新标注"真实分数"  → 形成 200 条 (问答 + 人工分数) 的黄金集  Step 2: 运行当前法官 Ensemble  用相同 200 条送入法官，获得法官分数  Step 3: 计算偏差指标  · Pearson 相关系数（法官 vs 人工）  · 系统性偏差方向（法官是否一贯偏高/偏低）  · 维度偏差分布（哪个维度偏差最大）  Step 4: 偏差修正  若 Pearson < 0.85 → 重新校准 Rubric 或替换法官  若系统性偏差 > 0.5分 → 引入偏差修正系数  Step 5: 记录元评估报告  归档，作为下次架构审查的依据 |

**偏差修正系数（Score Calibration）**

|  |
| --- |
| Python class JudgeCalibrator:  """  基于人工标注黄金集，对法官输出进行偏差修正  类似 Prometheus 2 中的对齐训练思想  """  def fit(self, judge\_scores: list[float], human\_scores: list[float]):  # 线性校准：score\_calibrated = α × score\_raw + β  self.alpha, self.beta = np.polyfit(judge\_scores, human\_scores, 1)    def calibrate(self, raw\_score: float) -> float:  return self.alpha \* raw\_score + self.beta |

**七、CI/CD 集成设计**

|  |
| --- |
| Plain Text 代码/模型/知识库变更 Push  │  ▼  [PR Opened / Merged]  │  ├── 触发类型判断 ──────────────────────────────────────────┐  │ │  │ 模型切换 知识变动 API 变动 │  │ │ │ │ │  │ Pairwise RAGAS 四维 语义相似度 │  │ + 雷达图 + 幻觉定位 + 非功能指标 │  │ │  └───────────────────────────────────────────────────────────┘  │  ┌─────────┴──────────┐  ▼ ▼  P0 用例集(~500) P1/P2 用例集(全量)  5min 内完成 异步后台运行  │ │  ▼ ▼  CI Gate 决策 Dashboard 更新 |

**Gate 判定规则**

|  |
| --- |
| YAML ci\_gate\_policy:  # 任一条件触发则阻塞合并  block\_merge\_if:  - p0\_pass\_rate < 0.95  - any\_p0\_hallucination\_case\_failed # 幻觉类 P0 用例失败  - ragas\_faithfulness\_avg < 0.85 # 忠实度回退（知识变动场景）  - latency\_p99\_regression\_pct > 0.30 # P99 延迟回归  - error\_rate\_5xx > 0.01  - judge\_bias\_check\_failed # 法官偏差校验不通过  - preference\_leakage\_risk == "HIGH" # 高偏漏风险    # 警告但不阻塞  warn\_only\_if:  - overall\_pass\_rate < 0.90  - cost\_increase\_pct > 0.20  - cache\_hit\_rate < 0.30  - golden\_embedding\_staleness\_days > 30  - judge\_divergence\_rate > 0.20 # Ensemble 分歧率过高 |

**八、人工介入（HiTL）工作流**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**九、核心指标 Dashboard**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**十、快速决策参考卡**

|  |
| --- |
| Plain Text Q: 选哪种评估模式？  新模型上线对比 → Pairwise + 能力雷达图  质量绝对打分 → Single Answer Grading + Rubric  RAG 知识变动 → RAGAS 四维评估  API 格式变更 → 语义相似度 + 单答案打分  Q: 法官应该怎么选？  优先考虑家族多样性（防 Preference Leakage）  部署成本敏感 → Prometheus-2 7B（内网，免费）  最高评估质量 → GPT-4o + Claude-3.5 Ensemble  游戏领域专化 → 在 Prometheus-2 上微调自定义 Rubric  Q: 什么时候必须人工介入？  Ensemble 分差 > 2.5 分 → 立刻  RAGAS faithfulness < 0.70 → 立刻（严重幻觉）  偏好泄漏风险 HIGH → 立刻  法官偏差校验失败 → 24小时内  Q: RAGAS 哪个维度最重要？  防幻觉 → Faithfulness（最重要，阈值设最严）  检索质量 → Context Precision + Context Recall  用户体验 → Answer Relevance |

*v3.0 更新内容：新增法官健康检查层、Preference Leakage 防护、RAGAS 四维集成、Prometheus-2 作为 Layer 2、元评估体系。理论依据全部来源于 2024-2025 年顶会论文。*