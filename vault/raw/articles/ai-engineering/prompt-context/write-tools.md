## 一、本质：不是一个工具，是一组分层机制

Write 工具的调用链路如图所示，每一层都有独立的设计权衡：

**LLM 输出层 → 解析调度层 → 策略决策层 → 权限校验层 → I/O 执行层 → 验证反馈层**

---

## 二、工具 Schema 与多粒度设计

所有主流框架均遵循 Anthropic / OpenAI `tool_use` 协议。但关键洞察是：**Claude Code 并非只有一个 `write_file`，而是暴露了三个写入粒度的工具**，根据 ECC 仓库分析：

| 工具 | 粒度 | 适用场景 |
|------|------|---------|
| `write_file` / `create_file` | 整文件替换 | 新建文件、小文件重构 |
| `str_replace_editor` | 块级 find-replace | 局部修改、函数替换 |
| `apply_patch` | unified diff | 大文件精确修改 |

**Token 经济学驱动选择**：`< 100 行 → full-replace`，`100~500 行 → str_replace`，`> 500 行 → patch`。500 行文件的 full-replace 约消耗 15K output tokens，成本极高。

---

## 三、三种写入策略的核心差异

### 3.1 Full Replace — 最简单，最贵

整文件覆盖写入，无 patch 失败风险。问题是 token 消耗与文件大小线性正比，长文件几乎不可行。

### 3.2 str_replace — 核心武器，有唯一性约束

```python
def str_replace(path, old_str, new_str):
    content = open(path).read()
    count = content.count(old_str)
    if count == 0: raise ToolError("not found")
    if count > 1:  raise ToolError(f"matches {count} locations, must be unique")
    atomic_write(path, content.replace(old_str, new_str, 1))
```

**唯一性约束是精心设计的安全锁**：强迫 LLM 提供足够的上下文来精确定位目标片段，防止误替换重复代码块。若重复，LLM 必须扩展 `old_str` 直到唯一。这是 Claude Code 最常用的写入工具。

### 3.3 Unified Patch — 最省 token，最难驾驭

LLM 生成标准 unified diff，通过自实现的 apply 函数执行。token 效率最高，但 LLM 对行号的准确性很差，fuzz 不匹配导致 apply 失败率高。工业实践上 Codex 沙箱模式用它，Claude Code 则回避，优先推 str_replace。

---

## 四、沙箱与权限机制：两条不同的路

**Codex CLI 走 OS 级隔离**：macOS 用 `sandbox-exec` (Seatbelt)，Linux 用 `landlock` + `seccomp` 过滤系统调用。三种模式（suggest / auto-edit / full-auto）对应不同的文件系统权限和网络权限。隔离强度达内核级别，但跨平台实现复杂度高。

**Claude Code 走权限门控**：在工具调用层做路径白名单检查 + 危险路径识别（`~/.bashrc`、`.ssh/`、`.git/config` 等）。实现简单、跨平台，但隔离强度弱于 OS 沙箱，依赖规则覆盖度。

---

## 五、Atomic Write — 不可妥协的底线

所有框架都使用 `temp → fsync → rename` 三步原子写入：

```python
def atomic_write(path, content):
    dir_path = os.path.dirname(os.path.abspath(path))
    with tempfile.NamedTemporaryFile(mode='w', dir=dir_path, delete=False) as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())   # 确保数据落盘
        tmp_path = f.name
    os.replace(tmp_path, path) # POSIX atomic rename
```

关键细节：`tempfile` 必须在**同一目录**（同一文件系统），否则 `os.replace` 退化为 copy+delete，失去原子性保证。

---

## 六、Approval Gate 与 Diff 展示

写入前先计算 unified diff 并彩色渲染，是所有工具的共同范式：`+` 行绿色，`-` 行红色，`@@` 块青色。然后进入三种交互模式之一：**同步逐步**（每次等 `y/n`）、**YOLO 模式**（跳过确认，适合 CI）、**事后批量**（Codex 的 suggest 模式，先生成所有 diff 再统一审批）。

值得注意的是 Codex 的 suggest 模式有一个独特优势：用户可以看到**整个计划**再决定是否执行，比逐步确认更有全局感。

---

## 七、Read-before-Write 是架构级要求

str_replace 策略要求 `old_str` 与磁盘内容完全一致（空格、换行都算），所以 LLM 必须先读文件再写。正确流程：

```
read_file → [LLM thinking 中规划修改] → str_replace_editor
```

大文件的读取策略有三档：**行范围读取**（最简单）、**Symbol-level 读取**（Claude Code 方式，先提取 def/class 骨架再按需读函数体）、**Semantic Chunking + RAG**（构建代码知识图谱后 retrieve 相关上下文，`code_graph` 项目解决的正是这个问题）。

---

## 八、横向对比

| 维度 | Claude Code | Codex CLI | Cursor |
|------|-------------|-----------|--------|
| 写入粒度 | write / str_replace / patch | write / patch | AST-based diff |
| 沙箱机制 | 权限门控（进程级） | OS 沙箱（内核级） | 无（IDE 内） |
| Approval | 同步逐步 / YOLO | suggest / auto-edit / full-auto | inline accept/reject |
| Atomic Write | ✅ | ✅ | ✅ |
| 大文件策略 | Symbol-level 读取 | 行范围 | AST 感知 |
| 多文件事务 | 无（逐文件） | 无（逐文件） | 部分（Composer） |

Cursor 的 AST-based diff 是目前最精确的方案——它不依赖行号，直接在语法树层面做 diff，彻底解决了 unified patch 的行号漂移问题。这也是未来工具的演进方向。

---

## 九、Pi Agent 实现参考

结合 Pi Agent 的分层 TypeScript 架构，Python 版的 Write 工具层建议放在 `pi_agent_core/tools/write_tools.py`，核心设计五条原则：

1. **多粒度工具**：`write_file` + `str_replace` + `apply_patch` 三件套，让 LLM 按文件大小选择
2. **唯一性约束强制报错**：`str_replace` 中 `old_str` 不唯一时给出精确的错误信息和建议扩展方向
3. **Atomic Write 是底线**：任何写入路径都要经过 `temp → fsync → rename`
4. **Diff-first**：写入前计算并展示 diff，记录进 `WriteTransaction` 支持 rollback
5. **Path traversal 检查**：`path.resolve().is_relative_to(workspace.resolve())` 是第一道安全门