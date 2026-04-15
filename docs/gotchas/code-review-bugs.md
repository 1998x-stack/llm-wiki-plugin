# Code Review Bugs (V2.1-V2.3)

> From docs/gotchas.md #10

> 2026-04-15 code review session

---

### CRITICAL

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Aliased wikilink regex | `snapshot_index.py:88` | `[[A|B]]` 被解析为 `"A|B"` 字符串，导致所有使用别名链接的页面被误报为 orphaned | 改用 pipe-aware regex `r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]"` |
| Missing guard | `snapshot_index.py:112` | `update_index()` 在 `index.md` 不存在时直接 `read_text()` 会 crash | 添加 `INDEX_PATH.exists()` 检查 |

### HIGH

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Duplicate stats | `snapshot_index.py:168` | `"综合分析" in line` 匹配了 section header 和 stats 行，产生重复 | 改为 `startswith("- 综合分析：")` |
| Falsy confidence | `build_wiki_pages.py:414` | `if conf` 对 `0.0` 为 False，不显示 badge | 改为 `if conf is not None` |
| String formatting | `build_wiki_pages.py:296,414` | YAML 中 confidence 可能是字符串，`f"{conf:.2f}"` 会 crash | 改为 `f"{float(conf):.2f}"` |
| API no try/except | `qwen_ingest.py:273` | API 调用无异常处理，网络/认证错误导致 traceback | 包裹 try/except，输出 JSON error |
| Stale graph.json | `build_graph.py:220` | `--full` 模式下自定义 `--output` 路径时 `vault/graph.json` 未更新，`build_statistics.py` 读到旧数据 | `--full` 时始终更新 `vault/graph.json` |
| Mixed stdout | `build_graph.py:232` | `--full` 的 debug prints 和 JSON 混在 stdout，破坏解析 | debug 改输出到 stderr |
| No res.ok check | `statistics.html:219` | 404 时 HTML body 传给 `res.json()` 抛 SyntaxError | 添加 `if (!res.ok) throw new Error(res.status)` |
| Lint blocks deploy | `deploy.yml:39` | `continue-on-error: false` 导致 lint warnings（exit 1）阻断所有部署 | 改为 `continue-on-error: true` |

### MEDIUM (Doc inconsistency)

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Missing scripts | `CLAUDE.md` | 4 个 shell 脚本未出现在 Scripts 表 | 添加 setup-ingest-loop/qwen, watch-raw, cron-setup |
| Stale vault CLAUDE.md | `vault/CLAUDE.md` | 缺 3 个 Python 脚本，缺 wiki:reindex，"New Commands" 标签过时 | 全部更新 |
