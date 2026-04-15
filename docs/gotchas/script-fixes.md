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

---

> 2026-04-15

**问题**：`lint_wiki.py` 孤页检测（O1）使用**精确文件名匹配**（`f.stem`），空格 vs 连字符不等价。
例如 `Claude-Mem.md` 的 `## 相关` 中写 `[[Alex Newman]]`，但文件名是 `Alex-Newman.md`（stem=`Alex-Newman`），
因此 lint 不认为 Alex-Newman 有入链，仍报孤页。

**修复**：相关节中使用 pipe 别名格式 `[[Alex-Newman|Alex Newman]]`，确保 `[[` 之后的第一段与文件名 stem 完全一致。

---

**问题**：`lint_wiki.py` I2 检查（索引旧条目）会**误报注释模板**。
`index.md` 中的注释 `<!-- 格式：- [[页面名]] -->` 被当作真实 wikilink，误判为指向不存在页面的旧条目。

**状态**：已确认为假阳性，注释内容不会影响 Obsidian，可忽略。

---

**问题**：批量创建新 wiki 页面后，**BM25 索引** 和 **主题图** (`maps/*.md`) 不会自动更新。
Hook 仅在 Write/Edit 到 `wiki/**/*.md` 时触发，但新创建的页面需手动加入 `maps/*.md`，
否则 M2 检查持续报告这些页面"未收录于任何主题图"。

**修复**：每次批量 ingest 后运行 `wiki:lint`，按 M2 列表逐一将新页面加入对应 maps 文件。
