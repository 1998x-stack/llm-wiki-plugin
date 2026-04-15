---
description: "wiki:relink"
---

# wiki:relink

自动扫描所有 wiki 页面，将未链接的术语、实体名、别名自动添加 `[[wikilinks]]`。

## 输入

无参数。对整个 `wiki/` 目录执行。

## 算法

1. **构建术语词典** — 扫描所有 wiki 页面的文件名（stem）+ frontmatter `aliases`，构建 `{term: page_name}` 映射
2. **按长度降序排列** — 保证最长匹配优先（如 `矩阵分解` 优先于 `矩阵`）
3. **逐页面扫描** — 对每个 wiki 页面的正文文本，查找未链接的术语提及
4. **插入链接** — 将裸文本替换为 `[[page_name|matched_text]]` 或 `[[matched_text]]`（term 等于 page_name 时）

## 保护区域（不插入链接）

- **Frontmatter** (`---` ... `---`)
- **已有 `[[wikilinks]]`**
- **代码块** (``` ... ``` 和行内 `` ` ``)
- **标题行** (`# ...`)
- **`## 来源` 至 `## 相关` 段落**（含后续内容至 EOF）

## 冲突解决

- 术语按长度降序处理，最长匹配优先
- 已匹配的字符范围被标记为已消费，更短的术语跳过重叠位置
- 示例：文本 "矩阵分解算法" → "矩阵分解" 先匹配（4字），"矩阵" 跳过（位置已消费）

## 自引用跳过

- 每个页面不会链接自己的标题或别名

## 流程

### 1. Dry-run 预览

```bash
bash scripts/wiki.sh relink --dry-run
```

解析 JSON 输出：
- `terms_count`: 术语词典大小
- `pages_scanned`: 扫描的页面数
- `pages_modified`: 会被修改的页面数
- `links_added`: 会添加的链接总数
- `details`: 每个页面的详情

### 2. 执行

```bash
bash scripts/wiki.sh relink
```

### 3. 解析结果

| 字段 | 含义 |
|------|------|
| `status` | `"ok"` 成功 |
| `terms_count` | 术语词典条目数 |
| `pages_scanned` | 扫描页面数 |
| `pages_modified` | 实际修改的页面数 |
| `links_added` | 添加的链接总数 |
| `details` | 每页详情列表 |

### 4. 更新 log.md

在 `log.md` 的 frontmatter 之后、第一个 `##` 之前插入：

```
## [YYYY-MM-DD HH:MM] relink
- 术语词典: T 个
- 扫描: S 个页面
- 修改: M 个页面, L 条新链接
```
