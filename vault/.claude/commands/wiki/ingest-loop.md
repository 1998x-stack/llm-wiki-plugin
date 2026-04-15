---
description: "Batch ingest files from a folder using ralph-loop mechanism"
argument-hint: "<folder_or_file_path> [--engine=qwen]"
---

# wiki:ingest-loop

批量处理 raw/ 中的源材料，逐个文件执行 ingest 流程。使用 ralph-loop 机制确保每个文件获得完整的处理上下文。

## 输入

$ARGUMENTS — 文件夹路径或文件路径（相对于 raw/），以及可选的引擎标志

## 参数解析

从 $ARGUMENTS 中解析：
- **path** — 第一个不以 `--` 开头的参数，即文件夹或文件路径
- **engine** — `--engine=qwen` 表示使用 Qwen API；默认（无此标志）使用 `claude`

## 引擎差异

| 方面 | claude（默认） | qwen |
|------|---------------|------|
| 提取引擎 | Claude（当前会话） | Qwen API |
| 设置脚本 | `setup-ingest-loop.sh` | `setup-ingest-loop-qwen.sh` |
| 状态文件 | `.claude/ingest-loop.local.md` | `.claude/ingest-loop-qwen.local.md` |
| 错误日志 | 无 | `.claude/ingest-loop-qwen.error.md` |
| 上下文消耗 | 占用 Claude 上下文 | 不占用 Claude 上下文 |
| 前置条件 | 无额外要求 | 需要 `$DASHSCOPE_API_KEY` |
| 完成标记 | `ALL_FILES_INGESTED` | `ALL_FILES_INGESTED_QWEN` |

## 流程

### 首次运行 — 设置阶段

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

3. **（qwen 引擎）生成已有页面上下文**

   在第一次迭代前，生成已有页面列表供 Qwen 使用：
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

4. **获取当前文件**
   - 从状态文件读取 `files[current_index]`
   - 如果 `current_index >= total`，跳到步骤 9

5. **执行 ingest**

   - **claude 引擎**：对当前文件执行完整的 wiki:ingest 流程：
     - 读取源文件
     - 提取实体和概念
     - 查找已有页面（读取 index.md）
     - 创建或更新 wiki 页面
     - 建立关系
     - 矛盾检查
     - 更新 index.md 和 log.md
     - 每个新建/更新的页面执行 BM25 更新：`Bash: bash scripts/wiki.sh bm25_index update <wiki_file>`

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
   - 将 `current_index` 加 1
   - 将文件添加到 `completed[]`（成功）或 `failed[]`（失败）
   - 写回状态文件

8. **报告进度**
   - **claude 引擎**：`[current_index/total] Ingested: filename` 或 `Failed: filename — reason`
   - **qwen 引擎**：`[current_index/total] Qwen ingested: filename (N pages created, M skipped, K with errors)` 或 `Failed: filename — reason`

### 完成处理

9. **全部完成时**
   - 运行 `Bash: bash scripts/wiki.sh lint_wiki` 检查所有新创建的页面
   - 运行 `Bash: bash scripts/wiki.sh snapshot_index --update` 确保 index.md 最终一致
   - **qwen 引擎额外步骤**：更新 log.md（追加批量 ingest 记录）
   - 输出最终摘要：
     - 创建：N 个页面
     - 跳过（去重）：N 个页面
     - 有错误（已保存需修复）：N 个页面
     - 失败（API 错误）：N 个文件
     - 错误日志：`.claude/ingest-loop-qwen.error.md`（如有错误）
   - 删除状态文件：
     - **claude 引擎**：`Bash: rm .claude/ingest-loop.local.md`
     - **qwen 引擎**：`Bash: rm .claude/ingest-loop-qwen.local.md`
   - 注意：`.claude/ingest-loop-qwen.error.md` **不删除**，保留供用户审查
   - **claude 引擎**：输出 `<promise>ALL_FILES_INGESTED</promise>`
   - **qwen 引擎**：输出 `<promise>ALL_FILES_INGESTED_QWEN</promise>`

## 质量要求

- 每个页面必须满足 `_schema/quality-rules.md` 标准
- 概述不超过 200 字
- 中文为主，专有名词保留英文
- 第一次提到的重要概念加 [[链接]]
- 有 YAML 错误的页面仍然保存，错误记录在 error log 中供后续修复
