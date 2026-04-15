# Hooks & Path Issues

---

## 18. Hook 路径双重 vault/ 错误（已修复）

> 2026-04-15

**问题**：`vault/.claude/settings.local.json` 中配置的 hook 命令使用相对路径 `vault/scripts/hook_*.sh`，但 session 的 CWD 本身已经是 `vault/`，导致实际解析路径为 `vault/vault/scripts/hook_*.sh`（不存在），三个 hook 全部报错：

```
PostToolUse:Write hook error
Failed with non-blocking status code: bash: vault/scripts/hook_lint.sh: No such file or directory
```

**根因**：Claude Code session 在 `vault/` 目录下启动，`settings.local.json` 在 `vault/.claude/` 中，hook 命令的相对路径从 CWD（即 `vault/`）解析，所以 `vault/scripts/...` 成了 `vault/vault/scripts/...`。

**修复**：将 `vault/.claude/settings.local.json` 中的 hook 命令路径从：

```json
"command": "bash vault/scripts/hook_lint.sh \"$CLAUDE_TOOL_ARG_file_path\""
```

改为：

```json
"command": "bash scripts/hook_lint.sh \"$CLAUDE_TOOL_ARG_file_path\""
```

所有三个 hook（`hook_lint.sh`、`hook_bm25.sh`、`hook_graph.sh`）同步修复。

**注意**：hook 脚本内部使用 `$(cd "$(dirname "$0")/.." && pwd)` 自解析 vault 目录，不受 CWD 影响，无需改动脚本本身。

---

## 19. maps/*.md M1 假阳性：summary 中的内嵌链接

> 2026-04-15

**问题**：`wiki:reindex` 生成 `maps/*.md` 时，从 wiki 页面正文提取 summary 行，summary 中可能包含 `[[内嵌链接]]`（如 `Itô 积分将[[Wiener积分]]推广至...`）。`lint_wiki.py` 的 M1 检查扫描 maps 文件中的所有 `[[...]]`，将这些 summary 内嵌链接误报为"引用了不存在的页面"。

**修复**：在地图生成脚本中，从正文提取 summary 后，用正则表达式将 `[[页面名]]` 替换为纯文本 `页面名`：

```python
line = re.sub(r'\[\[([^\]]+)\]\]', r'\1', line)  # strip wiki links
```

重新生成所有 maps 后，M1 假阳性消失。

---

## 20. Reindex 主题分类被通用 tag 主导

> 2026-04-15

**问题**：`wiki:reindex` 按页面 tag 分配主题 cluster 时，几乎所有页面都带 `研究`（122 个）和 `技术`（118 个）tag，导致 "最高频 tag = 最优 cluster" 算法把 122 个页面分入 `研究` cluster，`其他` 高达 65 页。

**修复**：在 cluster 分配前过滤掉通用 meta tag（`研究`, `技术`, `历史`, `数学`, `学习`, `个人`, `工作`），仅使用主题性 tag（`数值分析`, `概率论`, `矩阵理论`, `AI`, `工具`等）分配 cluster：

```python
META_TAGS = {"研究", "技术", "历史", "数学", "学习", "个人", "工作"}
topic_tags = [t for t in tags if t not in META_TAGS]
```

**结果**：156 页面完整分入 6 个主题 cluster（数值分析 61, 概率论 39, 矩阵理论 30, AI 16, 组合数学 5, 工具 5），`其他` 清零。

**连带操作**：65 个实体/概念页面需补充主题 tag（如 `数值分析`、`概率论`、`矩阵理论`），以便正确分配 cluster。

---

## 21. 新 ingest 页面缺少主题 tag 导致落入"其他"

> 2026-04-15

**问题**：新 ingest 的页面（如 `Context-Engineering.md`、`分层记忆架构.md`）只带通用 tag `[技术, 方法论]`，无主题性 tag，经过 meta tag 过滤后 topic_tags 仅剩 `方法论`（频率 9，低于其他主题），实际页面数不足 3，被合并到 `其他` cluster。

**修复**：为这类 AI/LLM 领域页面添加 `AI` tag，确保正确落入 AI cluster。

**通用规则**：ingest 生成新页面时，除通用 tag（技术、研究）外，必须加一个**领域主题 tag**：

| 领域 | 推荐 tag |
|------|---------|
| LLM/AI 工具 | `AI` |
| 数值算法 | `数值分析` |
| 概率/随机 | `概率论` |
| 矩阵/谱理论 | `矩阵理论` |
| CLI/工具 | `工具` |
| 方法论/设计 | `方法论`（+`AI` 如涉及 LLM） |
