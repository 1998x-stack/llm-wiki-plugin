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

---

## #35 — B1: lint_wiki.py 误报代码块内的 TOML [[table]] 语法为断链

**Status**: Fixed (2026-04-15)

`lint_wiki.py` 的 B1（断链）检查器使用正则扫描全文，**不跳过 fenced code block（` ``` ` 区块）内的内容**。
因此，TOML 的数组表语法 `[[rule]]` 以及嵌套数组字面量 `[["git", "status"]]` 会被误识别为 wikilink，触发 B1 警告：

```
[WARN] B1 wiki/concepts/ExecPolicy.md: Broken link: [[rule]]
[WARN] B1 wiki/concepts/ExecPolicy.md: Broken link: [["git", "push", "origin"]]
[WARN] B1 wiki/concepts/ExecPolicy.md: Broken link: [["git", "status"]]
```

**When it bites**: 任何 wiki 页面的代码块中包含 `[[...]]` 形式的文本时都会触发，典型场景：TOML（`[[section]]`）、Python 列表嵌套（`[[a, b], [c, d]]`）、Markdown 表格内的 wikilink 示例。

**Workaround/Fix**: 将代码块中包含 `[[...]]` 的 TOML 示例改为注释风格（`# key = value`）或纯文字描述，避免在代码块里出现双方括号。根本修复需在 `lint_wiki.py` 的 B1 检查前先剥离 fenced code block 内容再扫描。

---

## #44 — I1/I2: index.md 使用纯文本列举页面导致全量 I1 误报

**Status**: New (2026-04-17)

`index.md` 的 `## 全部页面` 章节以逗号分隔纯文本列举所有 wiki 页面（如 `A3C, ACI 设计原则, ACP协议, ...`），而非 `[[wikilink]]` 格式。`lint_wiki.py` 的 `load_index_links()` 只提取 `[[...]]` 格式的链接，仅捕获到表格中的 23 个 map 引用（如 `[[maps/AI工程]]`），因此所有 953 个实际 wiki 页面均触发 I1（"Page not listed in index.md"）。同时，这 23 个 map 引用被 I2 检查与 `wiki/` 页面集合对比，全部误报为 "stale index entries"。

**When it bites**: 每次运行 `wiki:check` / `wiki:lint` 时必然触发，导致 953 条 I1 + 23 条 I2 噪声警告，掩盖真实问题。

**Workaround/Fix**: 忽略 I1/I2 报告，或将 index.md 的 `## 全部页面` 节改为 `[[wikilink]]` 格式（与 `load_index_links()` 匹配）。根本修复可选：在 `build_statistics.py` / `lint_wiki.py` 中同时支持纯文本格式的页面检测。
