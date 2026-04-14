# MemoryMiddleware 与 SkillsMiddleware

**源码路径：**

- `libs/deepagents/deepagents/middleware/memory.py`
- `libs/deepagents/deepagents/middleware/skills.py`

---

## 1. 总览：共同点

两者都通过 **后端路径** 读取内容（不假设本地直连磁盘的具体实现方式由 `BackendProtocol` 完成），并在 **系统消息** 侧增强模型可见上下文：

| 维度 | MemoryMiddleware | SkillsMiddleware |
|------|------------------|------------------|
| 内容性质 | 持久「记忆」：`AGENTS.md` 全文注入 | 技能：目录 + `SKILL.md`，**渐进式披露**（目录级元数据进提示，全文按需阅读） |
| 多源策略 | 按 `sources` 顺序**拼接**，后出现的源排在后面 | 按 `sources` 顺序加载，**同名技能后者覆盖前者**（last wins） |
| 加载时机 | `before_agent` / `abefore_agent` 首次写入 `memory_contents` | `before_agent` / `abefore_agent` 首次写入 `skills_metadata` |
| 每次 LLM 调用 | `wrap_model_call` → `modify_request` 将状态中的内容格式化为系统提示片段 | 同上，注入技能说明与列表 |

---

## 2. MemoryMiddleware（`memory.py`）

### 2.1 职责

从可配置的 **AGENTS.md 路径列表** 读取内容，合并后注入系统提示；实现上对 [AGENTS.md 规范](https://agents.md/) 的兼容加载（模块文档明确引用该规范）。

### 2.2 数据源与顺序

- **典型路径示例：** `["~/.deepagents/AGENTS.md", "./.deepagents/AGENTS.md"]`。
- **合并规则：** 多个源按配置顺序处理；`_format_agent_memory` 中按 `self.sources` 顺序输出 `"{path}\n{content}"` 段落，**靠后的源在拼接结果中位于更后**。
- **展示名：** 文档说明由路径自动推导（无需单独配置 display name 字段）。

### 2.3 状态与加载

- **状态模式：** `MemoryState` 含私有字段 `memory_contents: dict[str, str]`（路径 → 内容）。
- **缓存：** 若状态中已有 `memory_contents`，`before_agent` / `abefore_agent` 直接返回 `None`，不重复下载。
- **错误处理：** `file_not_found` 跳过该源；其他错误抛出 `ValueError`。

### 2.4 注入方式

`modify_request` 使用 `MEMORY_SYSTEM_PROMPT` 模板，将内容包在 `<agent_memory>` 中，并附带较长的 `<memory_guidelines>`（引导通过 `edit_file` 等更新记忆、何时记录/不记录等）。最终通过 `append_to_system_message` 拼到当前 `system_message`。

### 2.5 AGENTS.md 格式

标准 Markdown，**无强制章节结构**；常见内容包括项目概览、构建/测试命令、代码风格、架构说明等。

---

## 3. SkillsMiddleware（`skills.py`）

### 3.1 职责与模式

- 实现 **Anthropic 风格的 Agent Skills** 思路，配合 **渐进式披露（progressive disclosure）**：系统提示中展示**技能目录（名称、描述、路径等）**，完整工作流在需要时再读取对应 `SKILL.md`。
- **仅通过后端 API**（`ls`、`download_files` 等）访问存储，便于 Filesystem / State / 远程等后端互换。

### 3.2 技能目录结构

每个技能为**子目录**，其下必须有 `SKILL.md`（YAML frontmatter + Markdown 正文）；可有 `helper.py` 等辅助文件。

### 3.3 SkillMetadata（与规范对齐的 TypedDict）

解析自 `SKILL.md`  frontmatter，主要字段包括：

- **`name`：** 技能标识（规范建议 1–64 字符、小写与连字符等；实现中含校验与警告）。
- **`description`：** 描述（最长 1024 字符，超长截断）。
- **`path`：** 后端中 `SKILL.md` 的路径。
- **可选：** `license`、`compatibility`（最长 500）、`metadata`（`dict[str, str]`）、`allowed_tools`（来自 `allowed-tools`，支持空格分隔；兼容逗号分隔的解析）。

另有 **`MAX_SKILL_FILE_SIZE`**（10MB）防止过大文件。

### 3.4 多源与覆盖（layering）

- `sources` 为后端上的技能根路径列表，例如 `["/skills/base/", "/skills/user/", "/skills/project/"]`。
- 加载时对每个源调用 `_list_skills` / `_alist_skills`，再以 **`all_skills[skill["name"]] = skill`** 合并——**后遍历的源覆盖同名技能**，从而支持 base → user → project → team 分层。

### 3.5 系统提示内容

`SKILLS_SYSTEM_PROMPT` 包含：

- 技能库位置说明（`_format_skills_locations`，最后一项标注更高优先级）。
- **可用技能列表**（`_format_skills_list`）：名称、描述、可选 license/compatibility、`allowed_tools`、以及 **「读取 `path` 获取完整说明」** 的指引。
- 渐进式使用步骤与示例工作流。

### 3.6 路径约定

使用 **`PurePosixPath`** 构造虚拟 POSIX 路径，与平台无关；具体后端负责落地映射。

---

## 4. 设计对比小结

- **Memory** 偏向「始终在场的项目/用户长期上下文」；**Skills** 偏向「可插拔、可覆盖的程序化能力与流程说明」。
- 二者都支持 **多源**；Memory 是**顺序拼接**，Skills 是**按名合并、后者胜**。
- 二者都依赖 **`append_to_system_message`** 与 **后端工厂/实例解析**（`ToolRuntime` 构造方式与 Summarization 等中间件一致）。

---

## 5. 模块依赖关系（简图）

```
deepagents.backends.protocol (BackendProtocol)
        ↑
MemoryMiddleware / SkillsMiddleware
        → langchain.agents.middleware.types (AgentMiddleware, ModelRequest, …)
        → deepagents.middleware._utils.append_to_system_message
```

`skills.py` 中技能列表扫描依赖 `backend.ls` / `als` 与 `download_files` / `adownload_files`；`memory.py` 仅依赖批量 `download_files` / `adownload_files` 与路径列表对齐解析。
