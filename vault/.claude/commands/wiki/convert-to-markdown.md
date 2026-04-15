---
description: "Convert non-markdown files in raw/ to markdown using markitdown"
argument-hint: "[subfolder]"
---

# wiki:convert-to-markdown

扫描 raw/ 中的非 markdown 文件，使用 markitdown 转换为 markdown 格式并删除原始文件。

## 输入

$ARGUMENTS — 可选的子目录路径（相对于 raw/）。默认扫描整个 raw/。

## 支持格式

`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.epub`, `.csv`

## 流程

### 1. 扫描文件

```bash
find raw/$ARGUMENTS -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.pptx" -o -name "*.xlsx" -o -name "*.html" -o -name "*.epub" -o -name "*.csv" \) 2>/dev/null | sort
```

如果没有找到文件 → 报告"没有需要转换的文件"并停止。

### 2. 逐个转换

对每个找到的文件：

1. 检查同名 `.md` 文件是否已存在 → 如已存在，跳过并报告
2. 执行转换：
   ```bash
   markitdown "<source_path>" > "<source_path_without_ext>.md"
   ```
3. 验证输出文件非空：
   ```bash
   test -s "<output_path>" && echo "OK" || echo "EMPTY"
   ```
4. 如果输出非空 → 删除原始文件：`rm "<source_path>"`
5. 如果输出为空或转换失败 → 删除空的 .md 文件，保留原始文件，记录为失败

### 3. 报告

输出转换摘要：
- 转换成功: N 个文件
- 跳过（已有 .md）: M 个文件
- 转换失败: K 个文件（列出文件名和原因）

### 4. 更新 log.md

追加到 log.md：

```markdown
## [YYYY-MM-DD HH:MM] convert-to-markdown
- 扫描: raw/$ARGUMENTS
- 转换: N 成功, M 跳过, K 失败
```

## 注意事项

- 此命令是 `wiki:ingest` 的前置步骤 — 先转换，再 ingest
- 推荐工作流: `convert-to-markdown` → `ingest-loop`
- `markitdown` 必须已安装 (`pip install markitdown`)
- 转换后的 .md 文件保留在 raw/ 中，遵循 raw/ 不可变原则（转换是一次性预处理）
