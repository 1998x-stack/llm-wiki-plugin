---
description: "Batch ingest files using Qwen API with ralph-loop mechanism"
argument-hint: "<folder_or_file_path>"
---

# wiki:ingest-loop-qwen

使用 Qwen API 批量处理 raw/ 中的源材料。每个文件通过 qwen_ingest.py 脚本调用 Qwen 3-plus 模型提取知识。

## 前置条件

- 环境变量 `$DASHSCOPE_API_KEY` 已设置
- Python 依赖已安装（openai, pyyaml, jieba, rank_bm25）

## 输入

$ARGUMENTS — 文件夹路径或文件路径（相对于 vault/raw/）

## 流程

### 首次运行 — 设置阶段

1. **运行设置脚本**
   ```
   Bash: bash scripts/setup-ingest-loop-qwen.sh "$ARGUMENTS"
   ```
   - 如果输出包含 `SINGLE_FILE=`，提取文件路径，直接执行单文件 Qwen ingest（步骤 4），跳过循环机制
   - 如果设置成功，继续到步骤 2

2. **读取状态文件**
   - 读取 `.claude/ingest-loop-qwen.local.md` 获取文件列表和当前索引

### 每次迭代

3. **获取当前文件**
   - 从状态文件读取 `files[current_index]`
   - 如果 `current_index >= total`，跳到步骤 8

4. **调用 Qwen ingest（多页面模式）**
   ```
   Bash: cd vault && python3 scripts/qwen_ingest.py --raw "<raw_path>"
   ```
   注意：不传 `--wiki` 参数，使用多页面模式。

5. **解析 JSON 结果**
   - 解析 stdout JSON：
     - `status: "SUCCESS"` → `pages` 数组包含提取的页面列表
     - `status: "ERROR"` → 添加到 failed[]，记录错误信息，继续下一个文件
   - 对 `pages` 数组中的每个页面：
     - 读取 `type`（entity/concept）和 `wiki_name`
     - 确定路径：`wiki/entities/<wiki_name>.md` 或 `wiki/concepts/<wiki_name>.md`
     - 将 `markdown` 字段内容写入目标文件
     - 更新 BM25 索引：`python3 scripts/bm25_index.py update "<wiki_path>"`
   - 记录：一个源文件可能产出多个 wiki 页面

7. **更新状态**
   - 读取 `.claude/ingest-loop-qwen.local.md`
   - 将 `current_index` 加 1
   - 更新 completed[] 或 failed[]
   - 写回状态文件
   - 输出进度：`[current_index/total] Qwen ingested: filename` 或 `Failed: filename — reason`

### 完成处理

8. **全部完成时**
   - 运行 `Bash: python3 scripts/lint_wiki.py` 检查所有新创建的页面
   - 更新 index.md：将所有新页面添加到对应分类下
   - 更新 log.md：追加批量 ingest 记录
   - 输出最终摘要：成功/警告/失败 数量
   - 删除状态文件：`Bash: rm .claude/ingest-loop-qwen.local.md`
   - 输出：`<promise>ALL_FILES_INGESTED_QWEN</promise>`

## 与 wiki:ingest-loop 的区别

| 方面 | ingest-loop | ingest-loop-qwen |
|------|-------------|-----------------|
| 提取引擎 | Claude（当前会话） | Qwen 3-plus API |
| 上下文消耗 | 占用 Claude 上下文 | 不占用 Claude 上下文 |
| 适用场景 | 高质量提取 | 大批量快速处理 |
| 环境要求 | 无额外要求 | 需要 DASHSCOPE_API_KEY |
