# Script Fixes

> From docs/gotchas.md #15-17

---

## 15. lint_wiki.py load_index_links 别名链接 regex（已修复）

> 2026-04-15

**问题**：`load_index_links()` 使用 `\[\[([^\]]+)\]\]` regex，不处理 `[[A|B]]` 别名格式，与 `snapshot_index.py` 同一个 bug。

**修复**：改为 `\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]`。

---

## 16. build_graph.py relates_to 字符串类型崩溃（已修复）

> 2026-04-15

**问题**：部分 wiki 页面的 `relates_to` 字段包含字符串而非字典（如 `"[[某页面]]"` 而非 `{target: "[[某页面]]", type: ...}`），导致 `entry.get("target")` 报 `AttributeError`。

**修复**：在遍历 `relates_to` 时跳过非 dict 条目。

---

## 17. wiki HTML 页面无数学公式渲染（已修复）

> 2026-04-15

**问题**：wiki 页面包含 LaTeX 数学公式（`$$...$$`、`$...$`），但生成的 HTML 无 KaTeX/MathJax，公式显示为原始 LaTeX 源码。

**修复**：在 `build_wiki_pages.py` 的 HTML 模板中添加 KaTeX CDN + auto-render 脚本，支持 `$$`/`$`/`\[`/`\(` 四种定界符。
