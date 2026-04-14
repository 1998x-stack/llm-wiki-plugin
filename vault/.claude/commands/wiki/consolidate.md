# wiki:consolidate

执行记忆层的晋升和衰减。管理 Working → Episodic → Semantic → Procedural 的知识生命周期。

## 输入

$ARGUMENTS — 可选：`--deep` 执行完整的深度整合（包含 semantic→procedural 晋升）。默认只做日常整合。

## 流程

### 1. Working → Episodic 压缩

- 扫描 `_memory/working/` 中 status=unprocessed 的文件
- 对每个文件：
  - 提取关键观察
  - 合并到当天的 `_memory/episodic/YYYY-MM-DD.md`
    - 如果当天文件不存在 → 创建，frontmatter:
      ```yaml
      type: episodic-memory
      date: YYYY-MM-DD
      confidence: 0.6
      last_accessed: YYYY-MM-DD
      access_count: 1
      source_sessions: []
      ```
    - 如果已存在 → 追加新观察，更新 source_sessions
  - 将 working memory 文件标记为 `status: processed`

### 2. Episodic → Semantic 晋升

- 扫描 `_memory/episodic/` 中最近 30 天的文件
- 找出在 3+ 个不同 episode 中重复出现的观察/事实
- 对每个候选：
  - 检查 `_memory/semantic/` 中是否已有对应条目
  - 如果没有 → 创建新 semantic memory 文件：
    ```yaml
    type: semantic-memory
    fact: "..."
    confidence: 0.7
    first_observed: YYYY-MM-DD
    last_confirmed: YYYY-MM-DD
    confirmation_count: 3
    sources: []
    contradicted_by: []
    supersedes: null
    decay_rate: medium
    ```
  - 如果已有 → 更新 last_confirmed, confirmation_count, confidence（每次确认 +0.05，上限 0.95）

### 3. 置信度衰减

- 扫描 `_memory/semantic/` 中所有文件
- 对每个文件：
  - 计算距 last_confirmed 的天数
  - 按 decay_rate 计算新 confidence:
    - slow: `confidence * 0.5^(days/180)`
    - medium: `confidence * 0.5^(days/60)`
    - fast: `confidence * 0.5^(days/14)`
  - 如果新 confidence < 0.3 → 标记 status=stale
  - 更新 frontmatter

### 4. Journal 模式扫描

- 扫描 `journal/daily/` 中最近 7 天的文件
- 找出重复主题（同一 [[链接]] 或关键词在 3+ 天出现）→ 记录到 log.md
- 找出行为模式（5+ 次同类决策偏向）→ 更新 `journal/growth/cognitive-patterns.md`
- 找出成长信号（某领域提及频率增长）→ 更新 `journal/growth/skills-tracker.md`

### 5. 深度整合（--deep 时执行）

- **Semantic → Procedural 晋升**
  - 扫描 `_memory/semantic/` 中 confidence ≥ 0.8 的条目
  - 找出 5+ 个语义记忆描述同一行为模式或工作流
  - 提取为 `_memory/procedural/` 条目
- **月度/季度报告**
  - 如果当天是月初 → 生成月度 growth 报告
  - 如果当天是季初 → 生成季度报告到 `journal/growth/quarterly/`

### 6. 记录

- 追加 log.md：`## [YYYY-MM-DD] consolidate | 处理了 N 个 working, 晋升了 N 个 semantic, 衰减了 N 个`
- 更新 dashboard.md 的 "最近 consolidate" 日期
