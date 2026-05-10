# Script Fixes Gotchas

脚本误报和解析问题。

---

## #1 — B1: TOML/JSON 语法误触发断链警告

**Status**: New (2026-04-19)

**问题描述**:

`lint_wiki.py` 的 B1 (Broken Link) 检查使用正则表达式匹配 `[[...]]` 语法来识别 wikilink。这导致 TOML 配置文件中的 `[[rule]]`、`[[array]]` 等语法被误识别为断链。

**When it bites**:
- 在 wiki 页面中包含 TOML 配置示例时
- 在代码块中展示 JSON 或配置文件格式时
- Maps/*.md 文件中的链接列表显示异常截断时（可能也是解析边界问题）

**Workaround/Fix**:
- 当前 workaround: 人工识别并忽略此类误报
- 建议修复: 修改 B1 检查逻辑，排除代码块（```...``` 或 `...` 包裹的内容）内的 `[[...]]` 匹配
- 优先级: 低（不影响核心功能，只是报告噪音）

---

## #2 — B1: Map 文件链接显示截断

**Status**: New (2026-04-19)

**问题描述**:

`maps/*.md` 文件中的链接条目在 lint 报告中显示为截断状态，例如：
```
maps/机器人学.md: [[Tomas Lozano-Per
maps/推荐系统.md: [[Self-At
```

这可能是以下原因之一：
1. `build_maps.py` 生成时的截断逻辑问题
2. `relink.py` 或 `lint_wiki.py` 解析长链接时的边界问题
3. 实际文件内容确实被截断（需要验证）

**When it bites**:
- 运行 `wiki:check` 或 `wiki:lint` 时产生大量疑似断链警告
- 难以区分真正的断链和显示截断

**Workaround/Fix**:
- 需要人工抽样验证：打开 maps/*.md 检查实际内容
- 如果是解析问题，修复 lint_wiki.py 的行读取逻辑
- 如果是生成问题，修复 build_maps.py 的截断逻辑

---
