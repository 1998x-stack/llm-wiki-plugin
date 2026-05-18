---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-engineering, prompt-context, tools, file-operations, token-economics, AI工程]
aliases: ["Write Tools", "文件写入工具", "Write File Operations", "文件写入机制"]
relates_to: 
  - target: "[[Tool-Use]]"
    type: extends
  - target: "[[Prompt-Engineering]]"
    type: relates_to
  - target: "[[Context-Engineering]]"
    type: relates_to
  - target: "[[Claude Code]]"
    type: implemented_in
  - target: "[[Codex CLI]]"
    type: compares_to
  - target: "[[Cursor]]"
    type: compares_to
  - target: "[[atomic_write]]"
    type: uses
supersedes: null
---

# Write Tools

## 概述
[[Write]] [[Tool System|Tools]] 是一组分层的文件写入机制，提供多粒度的文件操作能力，包括整文件替换、块级替换和补丁应用。其设计受到 [[Token 经济学]]的深刻影响，需要在精确性、效率和成本之间取得平衡。

## 关键内容

1. **分层机制**：
   - **LLM 输出层 → 解析调度层 → 策略决策层 → [[Permissions|权限]]校验层 → I/O 执行层 → 验证反馈层**
   - 每一层都有独立的设计权衡，形成了完整的安全与效率保障体系

2. **多粒度设计与 [[Token 经济学]]**：
   - `write_file` / `create_file`：整文件替换，适用于新建文件、小文件[[重构]]（< 100 行）
   - `str_replace_editor`：块级 find-replace，适用于局部修改、函数替换（100~500 行）
   - `apply_patch`：[[unified diff]] 应用，适用于大文件精确修改（> 500 行）
   - **[[Token 经济学]]驱动选择**：`< 100 行 → full-replace`，`100~500 行 → str_replace`，`> 500 行 → patch`。500 行文件的 full-replace 约消耗 15K output tokens，成本极高。

3. **写入策略详解**：
   - **Full Replace**：最简单但最昂贵，token 消耗与文件大小线性正比，无 patch 失败风险
   - **str_replace**：核心武器，具有唯一性约束以确保精确定位。唯一性约束是精心设计的安全锁：强迫 LLM 提供足够的上下文来精确定位目标片段，防止误替换[[重复代码]]块。若重复，LLM 必须扩展 `old_str` 直到唯一
   - **Unified Patch**：最节省 token，但 LLM 对行号准确性差，fuzz 不匹配导致 apply 失败率高，工业实践中 [[Codex CLI|Codex]] [[Sandbox Mode|沙箱模式]]使用，[[Claude Code]] 则回避

4. **安全与[[Permissions|权限]]机制**：
   - [[Claude Code 沙箱机制|沙箱]]与[[Permissions|权限]]机制：[[Codex CLI|Codex]] 使用 OS 级隔离（macOS 的 `sandbox-exec`/[[Apple Sandbox|Seatbelt]]，Linux 的 `landlock` + `seccomp`），[[Claude Code]] 使用[[Permissions|权限]][[门控机制（Gating Mechanism）|门控]]（路径白名单检查 + 危险路径识别）
   - [[atomic_write|Atomic Write]]：使用 temp → fsync → rename 三步[[atomic_write|原子写入]]确保数据一致性，关键细节是 tempfile 必须在同一目录（同一文件系统），否则 `os.replace` 退化为 copy+delete，失去原子性保证
   - 唯一性约束：str_replace 要求 old_str 必须唯一，防止误替换[[重复代码]]块
   - Path traversal 检查：确保路径在工作区范围内，防止路径遍历攻击

5. **工作流程与用户体验**：
   - [[Approval Gate UI|Approval Gate]]：写入前[[计算]]并显示 [[unified diff]]（`+` 行绿色，`-` 行红色，`@@` 块青色），支持同步逐步（每次等 `y/n`）、YOLO 模式（跳过确认）、事后批量（先生成所有 diff 再统一审批）等交互模式
   - Read-before-[[Write]]：str_replace 策略要求先读取文件再修改，因为 `old_str` 与磁盘内容必须完全一致（空格、换行都算）
   - 大文件读取策略：行范围读取、Symbol-level 读取（[[Claude Code]] 方式，先提取 def/class [[骨骼系统|骨架]]再按需读函数体）、Semantic Chunking + RAG（构建代码知识图谱后 retrieve 相关上下文）

6. **架构对比**：
   - **[[Claude Code]]**：write / str_replace / patch 三件套，[[Permissions|权限]][[门控机制（Gating Mechanism）|门控]]（进程级），同步逐步/YOLO 审批，Symbol-level 大文件读取
   - **[[Codex CLI]]**：write / patch，OS [[Claude Code 沙箱机制|沙箱]]（内核级），suggest/auto-edit/full-auto 模式，行范围读取
   - **[[Cursor]]**：[[AST-based diff]]（最精确方案，直接在语法树层面做 diff，解决行号漂移问题），无[[Claude Code 沙箱机制|沙箱]]（IDE 内），inline accept/reject

## 来源
- [[write-tools.md]] — 一、本质：不是一个工具，是一组分层机制
- [[write-tools.md]] — 二、工具 Schema 与多粒度设计
- [[write-tools.md]] — 三、三种写入策略的核心差异
- [[write-tools.md]] — 四、沙箱与权限机制：两条不同的路
- [[write-tools.md]] — 五、Atomic Write — 不可妥协的底线
- [[write-tools.md]] — 六、Approval Gate 与 Diff 展示
- [[write-tools.md]] — 七、Read-before-Write 是架构级要求
- [[write-tools.md]] — 八、横向对比

## 相关
- [[Tool-Use]] — base_for
- [[atomic_write]] — uses
- [[Claude Code]] — implements
- [[Codex CLI]] — compares_to
- [[Cursor]] — compares_to
- [[上下文窗口经济学]] — relates_to