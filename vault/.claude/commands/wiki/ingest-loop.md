---
description: "Batch ingest files from a folder using ralph-loop mechanism"
argument-hint: "<folder_or_file_path> [--engine=qwen]"
---

# wiki:ingest-loop

批量处理 raw/ 中的源材料，逐个文件执行 ingest 流程。

- **claude 引擎**（默认）：每个文件分派独立 Agent 子代理处理，避免上下文污染。**同时最多 3 个子代理并行**，防止堵塞
- **qwen 引擎**：调用 Qwen API，不占用 Claude 上下文

## 输入

$ARGUMENTS — 文件夹路径或文件路径（相对于 raw/），以及可选的引擎标志

## 参数解析

从 $ARGUMENTS 中解析：
- **path** — 第一个不以 `--` 开头的参数，即文件夹或文件路径
- **engine** — `--engine=qwen` 表示使用 Qwen API；默认（无此标志）使用 `claude`

## 引擎差异

| 方面 | claude（默认） | qwen |
|------|---------------|------|
| 提取引擎 | Agent 子代理（每文件独立上下文） | Qwen API |
| 设置脚本 | `setup-ingest-loop.sh` | `setup-ingest-loop-qwen.sh` |
| 状态文件 | `.claude/ingest-loop.local.md` | `.claude/ingest-loop-qwen.local.md` |
| 错误日志 | `.claude/ingest-loop.error.md` | `.claude/ingest-loop-qwen.error.md` |
| 上下文隔离 | 每文件独立子代理，互不污染 | 每文件独立 API 调用 |
| 前置条件 | 无额外要求 | 需要 `$DASHSCOPE_API_KEY` |
| 完成标记 | `ALL_FILES_INGESTED` | `ALL_FILES_INGESTED_QWEN` |

## 流程

### 首次运行 — 设置阶段

0. **非 markdown 文件预检查**

   检查目标路径中是否存在非 markdown 文件：
   ```bash
   find raw/$path -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.pptx" -o -name "*.xlsx" -o -name "*.html" -o -name "*.epub" -o -name "*.csv" \) 2>/dev/null | head -5
   ```
   - 如果找到非 markdown 文件 → 提示用户先运行 `wiki:convert-to-markdown $path` 转换，列出发现的文件数量和类型
   - 如果没有非 markdown 文件 → 继续

1. **运行设置脚本**

   - **claude 引擎：**
     ```
     Bash: bash scripts/setup-ingest-loop.sh "$path"
     ```
   - **qwen 引擎：**
     ```
     Bash: bash scripts/setup-ingest-loop-qwen.sh "$path"
     ```

   - 如果输出包含 `SINGLE_FILE=`，提取文件路径：
     - **claude 引擎**：直接执行 wiki:ingest 逻辑处理该文件，跳过循环机制
     - **qwen 引擎**：直接执行 `Bash: bash scripts/wiki.sh qwen_ingest --raw "$file"`，跳过循环机制
   - 如果设置成功，继续到步骤 2

2. **读取状态文件**
   - **claude 引擎**：读取 `.claude/ingest-loop.local.md`
   - **qwen 引擎**：读取 `.claude/ingest-loop-qwen.local.md`

   获取文件列表和当前索引。

3. **构建上下文包**

   - **claude 引擎**：构建一次性上下文包供所有子代理使用。
   
     首先判断源材料的主题（从文件夹路径或文件内容推断），然后按主题构建上下文包：
     ```
     Bash: bash scripts/wiki.sh build_ingest_context --topic <推断的主题>
     ```
     如果无法确定主题，不传 `--topic`（回退到全量模式）。
     
     解析 JSON 输出，提取：
     - `existing_pages` — 该主题的已有页面列表（用于去重）
     - `schema_compact` — 合并后的 schema 规则
     - `template` — wiki-page 模板
     - `stats` — 当前页面统计
     - `topic_filter` — 实际使用的主题过滤（如有）

   - **qwen 引擎**：生成已有页面上下文供 Qwen 使用：
     ```
     Bash: python3 -c "
     import sys; sys.path.insert(0, '.')
     from scripts.snapshot_index import scan_wiki
     pages = scan_wiki()
     for name in sorted(pages.keys()):
         print(f'- {name}')
     " > /tmp/wiki_pages_context.txt
     ```

     同时初始化错误日志文件（如果不存在）：
     ```
     Bash: cat > .claude/ingest-loop-qwen.error.md << 'EOF'
     # Qwen Ingest Errors

     > 此文件记录 Qwen 批量 ingest 中的错误，用于后续修复。
     > 使用 `wiki:lint` 可自动修复大部分问题。

     EOF
     ```

### 每次迭代

4. **获取当前批次文件**
   - 从状态文件读取接下来最多 3 个未处理文件：`files[current_index]` 到 `files[min(current_index+2, total-1)]`
   - 如果 `current_index >= total`，跳到步骤 9

5. **执行 ingest**

   - **claude 引擎**：**同时分派最多 3 个** Agent 子代理并行处理当前批次。在一条消息中发出所有 Agent 调用，让它们并行运行。等待所有子代理返回后再进入步骤 7。

     每个子代理使用 Agent 工具，设置 `model: sonnet`，prompt 包含以下内容：

     ````
     你是一个 wiki 知识提取器。处理一个源文件，将知识编译为 wiki 页面。

     ## 工作目录
     /Users/mx/Desktop/series/核心项目系列/llm-wiki/vault

     ## 源文件
     使用 Read 工具读取: {当前文件路径}

     ## 已有页面（检查重复，不要创建同名页面）
     {existing_pages 内容}

     ## Schema 规则
     {schema_compact 内容}

     ## 页面模板
     {template 内容}

     ## 指令
     1. 读取源文件
     2. 识别文中提到的实体（人物、公司、项目、工具、论文、书籍）和核心概念
     3. 对每个实体/概念，检查"已有页面"列表避免重复
     4. 创建新页面（Write 工具）：
        - 实体 → wiki/entities/<名称>.md
        - 概念 → wiki/concepts/<名称>.md
        - 文件名用自然中文
        - 遵循模板格式，填写完整 frontmatter
        - 概述不超过 200 字符
        - 中文为主，专有名词保留英文
        - 用 [[双链]] 引用相关概念
     5. 已有页面 → 使用 Read 读取，然后 Edit 追加新信息，更新 confidence 和 source_count
     6. 建立 relates_to 关系（同时更新被关联页面）
     7. 每个新建/更新的页面执行 BM25 索引：
        Bash: bash scripts/wiki.sh bm25_index update <wiki_file_path>
     8. 完成后执行：Bash: bash scripts/wiki.sh snapshot_index --update

     ## 输出
     最后一行输出 JSON 格式的摘要：
     {"created": ["页面1.md", "页面2.md"], "updated": ["页面3.md"], "error": null}
     如果出错：{"created": [], "updated": [], "error": "错误描述"}
     ````

     **重要**：子代理拥有独立上下文，处理完成后上下文自动释放，不影响后续文件。

   - **qwen 引擎**：调用 Qwen ingest（多页面模式）：
     ```
     Bash: bash scripts/wiki.sh qwen_ingest --raw "$file" --context-pages /tmp/wiki_pages_context.txt
     ```
     注意：不传 `--wiki` 参数，使用多页面模式。可选传 `--model` 指定模型。

     解析 stdout JSON：
     - `status: "SUCCESS"` → `pages` 数组包含提取的页面列表
     - `status: "ERROR"` → 添加到 failed[]，记录错误到 error log，继续下一个文件

     对 `pages` 数组中的每个页面：
     - 读取 `type`（entity/concept）和 `wiki_name`
     - 确定路径：`wiki/entities/<wiki_name>.md` 或 `wiki/concepts/<wiki_name>.md`

     **去重检查**：如果页面包含 `existing_path` 字段：
     - 表示该页面已存在于 wiki 中
     - **跳过写入**，报告 SKIPPED（已存在）
     - 记录到进度输出

     **错误处理**：如果页面包含 `errors` 字段：
     - **仍然写入文件**（让 Claude 或 wiki:lint 后续修复）
     - 追加错误详情到 `.claude/ingest-loop-qwen.error.md`：
       ```markdown
       ## [源文件名] — YYYY-MM-DD HH:MM
       - **wiki/entities/X.md** — ERRORS: ["错误1", "错误2"]
         - 文件已保存，需要手动修复或运行 `wiki:lint`
       ```

     **成功**：无 `errors` 且无 `existing_path`：
     - 将 `markdown` 字段内容写入目标文件
     - 更新 BM25 索引：`Bash: bash scripts/wiki.sh bm25_index update "<wiki_path>"`

6. **（qwen 引擎）增量更新 index.md**

   每个文件处理完成后（不等到全部完成），执行：
   ```
   Bash: bash scripts/wiki.sh snapshot_index --update
   ```
   这样如果循环中途崩溃，index.md 保持同步。

7. **更新状态**
   - 读取对应状态文件
   - 将 `current_index` 加上本批次文件数（最多 3）
   - 将文件添加到 `completed[]`（成功）或 `failed[]`（失败）
   - 写回状态文件

8. **报告进度**
   - **claude 引擎**：对批次中每个文件输出 `[index/total] Ingested: filename → N created, M updated` 或 `Failed: filename — reason`
   - **qwen 引擎**：`[current_index/total] Qwen ingested: filename (N pages created, M skipped, K with errors)` 或 `Failed: filename — reason`

### 完成处理

9. **全部完成时**
   - 运行 `Bash: bash scripts/wiki.sh lint_wiki` 检查所有新创建的页面
   - 运行 `Bash: bash scripts/wiki.sh snapshot_index --update` 确保 index.md 最终一致
   - **qwen 引擎额外步骤**：更新 log.md（追加批量 ingest 记录）
   - **claude 引擎额外步骤**：更新 log.md（追加批量 ingest 记录）
   - 输出最终摘要：
     - 创建：N 个页面
     - 更新：N 个页面
     - 跳过（去重）：N 个页面
     - 失败：N 个文件
   - 删除状态文件：
     - **claude 引擎**：`Bash: rm .claude/ingest-loop.local.md`
     - **qwen 引擎**：`Bash: rm .claude/ingest-loop-qwen.local.md`
   - 注意：错误日志文件 **不删除**，保留供用户审查
   - **claude 引擎**：输出 `<promise>ALL_FILES_INGESTED</promise>`
   - **qwen 引擎**：输出 `<promise>ALL_FILES_INGESTED_QWEN</promise>`

## 质量要求

- 每个页面必须满足 `_schema/quality-rules.md` 标准
- 概述不超过 200 字
- 中文为主，专有名词保留英文
- 第一次提到的重要概念加 [[链接]]
- 有 YAML 错误的页面仍然保存，错误记录在 error log 中供后续修复

## 设计原则

### 上下文隔离与并发控制（claude 引擎）

每个源文件由独立的 Agent 子代理处理，**同时最多 3 个并行**，确保：
- **无上下文污染**：前一个文件的源内容和生成页面不会影响下一个文件
- **稳定质量**：第 50 个文件和第 1 个文件获得同等质量的处理
- **容错性**：单个文件失败不影响其他文件，编排器继续处理下一个
- **防止堵塞**：限制最多 3 个并行子代理，超过 3 个容易导致系统堵塞

### 上下文包（build_ingest_context）

一次性构建的上下文包（~2.5K tokens）包含：
- 已有页面列表（去重检查）
- Schema 规则（实体类型 + 关系类型 + 质量规则）
- 页面模板

上下文包在循环开始时构建一次，所有子代理共享同一份。最终 `snapshot_index --update` 确保一致性。
