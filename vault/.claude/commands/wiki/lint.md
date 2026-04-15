# wiki:lint

对知识库进行健康检查并自动修复可修复的问题。

> 只诊断不修复？请用 `wiki:check`。

## 流程

### 1. 诊断

运行 `wiki:check` 的完整流程（步骤 1-5），获取所有问题清单。

### 2. 自动修复

对 check 报告中的每个问题，按以下规则修复：

| 检查项 | 修复方式 |
|--------|---------|
| **A. Frontmatter 缺失** | 自动填入默认值（confidence 根据 source_count 估算） |
| **B. 孤页** | 尝试在相关页面中添加 [[链接]]；无法自动链接的 → 跳过 |
| **C. 断链** | 近似名称页面 → 自动修正链接目标；否则 → 跳过 |
| **D. 矛盾** | 基于 confidence 和 source_count 提出建议（不自动解决） |
| **E. 过期** | 标记 status=stale（不删除） |
| **F. index.md** | 执行 `Bash: bash scripts/wiki.sh snapshot_index --update` 同步 |
| **G. BM25** | 执行 `Bash: bash scripts/wiki.sh bm25_index update <missing_file>` |
| **H. 图谱** | 跳过（由 wiki:build 负责） |
| **I. 模板** | 跳过（报告即可） |

### 3. 生成报告

- 追加到 log.md，格式：
  ```
  ## [YYYY-MM-DD HH:MM] lint
  - 扫描: N 个页面
  - ERROR: M 个 | WARNING: K 个 | INFO: J 个
  - 自动修复: X 个
  - 需要人工处理: Y 个
  ```
- 列出具体问题清单（已修复和未修复分开列出）

### 4. 更新 dashboard.md

- 更新 "最近 lint" 日期
