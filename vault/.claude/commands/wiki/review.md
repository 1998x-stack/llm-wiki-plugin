# wiki:review

kepano 式分形回顾。扫描近期 journal 内容，辅助升维和建立连接。

## 输入

$ARGUMENTS — 回顾范围（可选）。默认为 "weekly"。
- `weekly` — 过去 7 天的 daily notes
- `monthly` — 过去 30 天
- `quarterly` — 过去 90 天

## 流程

### weekly

1. **收集素材**
   - 读取 `journal/daily/` 中过去 7 天的所有 daily notes
   - 读取 `journal/reflections/` 和 `journal/judgments/` 中过去 7 天创建的文件

2. **生成周报草稿**
   - 用 `templates/weekly-review.md` 创建 `journal/daily/YYYY-WNN.md`
   - 填充"本周发生了什么"——从 daily notes 中提取关键条目
   - 填充"新的连接和发现"——找出本周新增的 [[链接]] 关系

2.5. **搜索知识关联**
   - 对本周高频主题，执行：`Bash: python3 scripts/search_wiki.py "<theme>" --top 5 --json`
   - 将搜索结果中的 topic_context 用于"升维建议"——知道该主题属于哪个知识领域

3. **升维建议**
   - 识别本周反复出现的主题（同一概念在 3+ 天被提到）
   - 对每个高频主题：
     - 如果 wiki/ 中还没有对应概念页 → 建议创建，并提供草稿
     - 如果已有 → 建议更新
   - 识别值得升级为正式 reflection 或 judgment 的 daily 内容

4. **链接补全**
   - 检查本周 daily notes 中提到但未加 [[链接]] 的概念
   - 自动在 daily notes 中补充 [[链接]]

5. **记录**
   - 追加 log.md：`## [YYYY-MM-DD] review | weekly`

### monthly

在 weekly 基础上增加：
- 扫描本月所有 reflections 和 judgments，提议哪些可以合并为 wiki/syntheses/ 综合页面
- 更新 `journal/growth/skills-tracker.md`

### quarterly

在 monthly 基础上增加：
- 生成 `journal/growth/quarterly/YYYY-QN.md` 季度成长报告
- 更新 `journal/growth/cognitive-patterns.md`
- 分析技能领域的变化趋势
