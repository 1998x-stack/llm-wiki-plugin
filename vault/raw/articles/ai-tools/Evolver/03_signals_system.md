# Evolver 信号系统（Signals）深度分析

> **源文件**: `src/gep/signals.js`
> **核心职责**: 从会话日志、内存文件、用户上下文中提取可操作的进化触发信号
> **调用时机**: 进化循环 Phase 1（ANALYSIS）末尾，`extractSignals()` 函数

---

## 1. 信号的本质

信号是**运行时观察与进化决策之间的桥梁**。原始日志文本 → 结构化信号列表 → Gene 选择器输入。

```
会话日志(.jsonl) ─┐
MEMORY.md ────────┤  extractSignals()  ──► ["log_error", "errsig:...", "user_feature_request:..."]
USER.md ──────────┤
recentEvents ─────┘
```

---

## 2. 信号三大类别

### 2.1 Defensive（防御型）— 错误与缺失

这类信号表示系统出现问题，**优先级最高**，会覆盖所有机会型信号。

#### 2.1.1 基础错误检测

正则覆盖英/中双语：
```js
// src/gep/signals.js:154
const errorHit = /\[error\]|error:|exception:|iserror":true|"status":\s*"error"|
  "status":\s*"failed"|错误\s*[：:]|异常\s*[：:]|报错\s*[：:]|失败\s*[：:]/.test(lower);

if (errorHit) signals.push('log_error');
```

#### 2.1.2 错误签名提取（Error Signature）

提取具体错误行，截取前 260 字符，用于匹配历史 Capsule：
```js
// src/gep/signals.js:158
const errLine = lines.find(l =>
  /\b(typeerror|referenceerror|syntaxerror)\b\s*:|error\s*:|exception\s*:/i.test(l)
) || null;

if (errLine) {
  signals.push('errsig:' + errLine.slice(0, 260));
}
```

**作用**：Capsule 的 `trigger` 数组中也存有 `errsig:...`，选择器通过规范化哈希实现模糊匹配：
```js
// 两个不同 errsig 可能映射到同一 errsig_norm:870c3a82
function normalizeErrorSig(errsig) {
  return 'errsig_norm:' + sha256(errsig).slice(0, 8);
}
```

#### 2.1.3 重复错误检测

同一错误出现 3+ 次时标记为 `recurring_error`：
```js
// src/gep/signals.js:188
const errorCounts = {};
const errPatterns = corpus.match(/(?:LLM error|"error"|"status":\s*"error")[^}]{0,200}/gi) || [];
// 统计出现频次 ...
const recurringErrors = Object.entries(errorCounts).filter(([_, n]) => n >= 3);
if (recurringErrors.length > 0) {
  signals.push('recurring_error');
  // 带频次的具体签名：recurring_errsig(5x):...
  signals.push('recurring_errsig(' + topCount + 'x):' + topErr.slice(0, 150));
}
```

#### 2.1.4 资源缺失信号

```js
if (lower.includes('memory.md missing'))     signals.push('memory_missing');
if (lower.includes('user.md missing'))        signals.push('user_missing');
if (lower.includes('key missing'))            signals.push('integration_key_missing');
if (lower.includes('no session logs found'))  signals.push('session_logs_missing');
```

#### 2.1.5 工具使用统计

高频工具调用可能表示低效自动化：
```js
// src/gep/signals.js:284
const toolUsage = {};
const toolMatches = corpus.match(/\[TOOL:\s*([\w-]+)\]/g) || [];
// 统计每个工具调用次数 ...
if (toolUsage[tool] >= 10) signals.push('high_tool_usage:' + tool);
if (tool === 'exec' && toolUsage[tool] >= 5) signals.push('repeated_tool_usage:exec');
```

---

### 2.2 Opportunity（机会型）— 创新触发

这类信号表示优化或扩展机会，**只在无 `log_error` 时才检测改进建议**。

#### 2.2.1 功能请求提取（4 语言支持）

带原文片段，帮助 Gene 理解具体需求：
```js
// 英语
const featEn = corpus.match(
  /\b(add|implement|create|build|make|develop)\b[^.?!\n]{3,120}\b(feature|function|module|capability|tool)\b/i
);

// 中文简体
if (/加个|实现一下|做个|想要\s*一个|需要\s*一个/.test(corpus)) { ... }

// 中文繁体
if (/加個|實現一下|做個|想要\s*一個/.test(corpus)) { ... }

// 日语
if (/追加|実装|作って|機能を|が欲しい/.test(corpus)) { ... }

signals.push('user_feature_request:' + featureRequestSnippet);  // 含原文
```

#### 2.2.2 改进建议（无错误时才检测）

```js
// src/gep/signals.js:246
if (!errorHit) {
  const impEn = corpus.match(
    /.{0,80}\b(should be|could be better|improve|enhance|refactor|clean up|simplify)\b.{0,80}/i
  );
  if (impEn) signals.push('user_improvement_suggestion:' + snippet);
}
```

#### 2.2.3 性能瓶颈

```js
if (/\b(slow|timeout|timed?\s*out|latency|bottleneck|high cpu|high memory|oom)\b/i.test(lower)) {
  signals.push('perf_bottleneck');
}
```

#### 2.2.4 能力缺口

```js
if (/\b(not supported|cannot|doesn'?t support|missing feature|unsupported|not implemented)\b/i.test(lower)) {
  // 排除已知资源缺失信号，避免重复
  if (!signals.includes('memory_missing') && !signals.includes('user_missing')) {
    signals.push('capability_gap');
  }
}
```

---

### 2.3 Meta（元信号）— 系统状态感知

这类信号由**历史分析**产生，描述进化系统本身的健康状态。

| 元信号 | 触发条件 | 效果 |
|--------|---------|------|
| `evolution_stagnation_detected` | 所有信号被抑制（停滞）| 强制切换策略 |
| `stable_success_plateau` | 无信号 / 信号全被抑制 | 转向优化模式 |
| `repair_loop_detected` | 连续 3+ 次失败修复 | 移除错误信号，注入创新触发 |
| `force_innovation_after_repair_loop` | 修复循环断路 | 强制 innovate 意图 |
| `empty_cycle_loop_detected` | 最近 8 轮 50%+ 为空轮 | 停止空转，切换策略 |
| `evolution_saturation` | 连续 3+ 个空轮 | 进入饱和降级 |
| `force_steady_state` | 连续 5+ 个空轮 | 强制稳态模式 |
| `consecutive_failure_streak_N` | 连续 N 次失败 | N 标记在信号中 |
| `failure_loop_detected` | 连续 5+ 次失败 | 触发基因封禁 |
| `ban_gene:<gene_id>` | 连续 5+ 次失败 | 封禁主导失败基因 |

---

## 3. 信号去重（防循环核心机制）

### 3.1 历史分析

```js
// src/gep/signals.js:28
function analyzeRecentHistory(recentEvents) {
  const tail = recentEvents.slice(-8);  // 分析最近 8 个事件

  // 统计各信号类型出现频次
  const signalFreq = {};
  for (const event of tail) {
    for (const sig of event.signals || []) {
      // 归一化：errsig:xxx → 'errsig'，user_feature_request:xxx → 'user_feature_request'
      const key = normalizeSignalKey(sig);
      signalFreq[key] = (signalFreq[key] || 0) + 1;
    }
  }

  // 出现 >= 3 次的信号加入抑制集合
  const suppressedSignals = new Set();
  for (const [sig, count] of Object.entries(signalFreq)) {
    if (count >= 3) suppressedSignals.add(sig);
  }

  return {
    suppressedSignals,
    consecutiveRepairCount,
    emptyCycleCount,
    consecutiveEmptyCycles,
    consecutiveFailureCount,
    geneFreq
  };
}
```

### 3.2 抑制逻辑

```js
// 过滤被抑制的信号
signals = signals.filter(s => !history.suppressedSignals.has(normalizeSignalKey(s)));

// 如果所有信号都被过滤掉，注入停滞信号
if (beforeDedup > 0 && signals.length === 0) {
  signals.push('evolution_stagnation_detected');
  signals.push('stable_success_plateau');
}
```

### 3.3 各级断路逻辑（依次检测）

**修复循环断路**（3+ 次连续失败修复）：
```js
if (history.consecutiveRepairCount >= 3) {
  // 1. 移除所有错误信号
  signals = signals.filter(s => s !== 'log_error' && !s.startsWith('errsig:'));
  // 2. 如果信号为空，注入修复循环信号
  if (signals.length === 0) signals.push('repair_loop_detected', 'stable_success_plateau');
  // 3. 注入强制创新
  signals.push('force_innovation_after_repair_loop');
}
```

**空轮检测**（最近 8 轮中 4+ 轮零代码变更）：
```js
if (history.emptyCycleCount >= 4) {
  signals = signals.filter(s => s !== 'log_error' && !s.startsWith('errsig:'));
  signals.push('empty_cycle_loop_detected', 'stable_success_plateau');
}
```

**稳态降级**（Echo-MingXuan 失败案例的教训）：
```js
// 案例：Cycle #55 命中 "no committable changes"，负载飙到 1.30，因为没有降级策略
if (history.consecutiveEmptyCycles >= 5) {
  signals.push('force_steady_state', 'evolution_saturation');
} else if (history.consecutiveEmptyCycles >= 3) {
  signals.push('evolution_saturation');
}
```

**失败连串基因封禁**（5+ 次连续失败）：
```js
if (history.consecutiveFailureCount >= 5) {
  signals.push('failure_loop_detected');
  // 找出主导失败的基因
  const dominantGene = Object.entries(history.geneFreq)
    .sort(([,a], [,b]) => b - a)[0]?.[0];
  if (dominantGene) signals.push('ban_gene:' + dominantGene);
}
```

---

## 4. 信号优先级规则

**规则 1**：有 actionable 信号时，移除"装饰性"信号：
```js
const actionable = signals.filter(s =>
  s !== 'user_missing' &&
  s !== 'memory_missing' &&
  s !== 'session_logs_missing'
);
if (actionable.length > 0) signals = actionable;
```

**规则 2**：改进建议只在无错误时检测（`!errorHit`）

**规则 3**：默认兜底：
```js
if (signals.length === 0) signals.push('stable_success_plateau');
```

**最终去重**（Array → Set → Array）：
```js
return Array.from(new Set(signals));
```

---

## 5. 信号完整流转示例

**场景**：Agent 崩溃后自动修复循环

```
第 1 轮：log_error + errsig:TypeError → 选 gene_repair → 修复失败
第 2 轮：log_error + errsig:TypeError → 选 gene_repair → 修复失败
第 3 轮：log_error + errsig:TypeError → 选 gene_repair → 修复失败
                                        ↓
                              [连续3次修复失败 → 断路器触发]
                                        ↓
第 4 轮：force_innovation_after_repair_loop + stable_success_plateau
        → 选 gene_innovate_from_opportunity
        → 用新方法绕过问题 → 成功
                                        ↓
第 5 轮：stable_success_plateau → 选 gene_optimize → 精细化改进
```

---

## 6. 数据源读取细节

`extractSignals()` 的输入来自 `evolve.js`：

```js
// src/evolve.js:813
const recentMasterLog = readRealSessionLog();   // 最近 6 个会话，24h 内，总量约 120KB
const todayLog        = readRecentLog(TODAY_LOG);  // 今日日志
const memorySnippet   = readMemorySnippet();     // MEMORY.md（最多 50KB）
const userSnippet     = readUserSnippet();       // USER.md（用户偏好）
const recentEvents    = readAllEvents().slice(-80); // 最近 80 条 EvolutionEvent

const signals = extractSignals({
  recentSessionTranscript: recentMasterLog,
  todayLog,
  memorySnippet,
  userSnippet,
  recentEvents,
});
```

**会话日志读取策略**：
```js
// 读取 24h 内最多 6 个活跃会话，每个最多 20KB，总量约 120KB
const ACTIVE_WINDOW_MS = 24 * 60 * 60 * 1000;
const TARGET_BYTES = 120000;
const PER_SESSION_BYTES = 20000;
```

**Session Scoping**（`EVOLVER_SESSION_SCOPE`）：
- 支持按 channel ID、项目名等隔离进化状态
- MEMORY.md 和 USER.md 也按 scope 隔离读取
