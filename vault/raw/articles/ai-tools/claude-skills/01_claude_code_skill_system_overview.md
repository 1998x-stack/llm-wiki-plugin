# Claude Code SKILL / Plugin 系统架构全景

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：01 / 09  
> **适用版本**：Claude Code（2025年10月起 Agent Skills 正式稳定）  

---

## 一、背景：从"自定义斜杠命令"到"Agent Skills"

Claude Code 最初提供的可扩展机制叫做 **Custom Slash Commands**——开发者在 `.claude/commands/` 目录下放一个 Markdown 文件，就能用 `/command-name` 触发对应 Prompt 模板。

2025 年中期，Anthropic 与社区共同制定了 **Agent Skills 规范（agentskills.io/specification）**，该规范随即被 Claude Code、OpenAI Codex、Cursor、Gemini CLI 等主流 AI 编码工具采用。Skills 是 Custom Slash Commands 的超集，全面替代了后者。

> **关键变化**：Skills 不再是"单文件 Prompt 模板"，而是包含说明文档、辅助脚本、参考资料的**完整目录结构**。

---

## 二、Claude Code 扩展机制全家桶（一次性消歧）

在深入 Skills 之前，有必要厘清 Claude Code 生态中所有扩展概念：

| 机制 | 本质 | 特点 |
|------|------|------|
| **CLAUDE.md** | 项目持久记忆 | 每次会话自动加载；告知 Claude 项目规范、技术栈等"永久上下文" |
| **Custom Slash Commands** | 简单 Prompt 模板 | 已并入 Skills；`.claude/commands/*.md` 文件 |
| **Agent Skills (SKILL.md)** | 目录级可复用能力包 | 可按需激活；可捆绑脚本、参考文档；支持动态注入 |
| **MCP Servers** | 进程级工具服务 | 独立进程；通过 Model Context Protocol 暴露工具和数据 |
| **Claude Connectors** | 远程 MCP 服务 | 连接 Slack、Figma、Asana 等 SaaS；OAuth 鉴权 |
| **Plugins** | 发布单元 | 捆绑 Skills + Agents + Hooks + MCP Server；一条命令安装 |
| **Agents** | 专用子智能体 | 插件中定义；有独立 system prompt；可被技能或 recipe 调用 |
| **Hooks** | 生命周期钩子 | 在 Claude Code 特定阶段（PreTool、PostTool 等）自动执行 |

---

## 三、SKILL.md 文件结构详解

每个 Skill 是一个**目录**，必须包含 `SKILL.md`，可选包含其他文件：

```
skill-name/
├── SKILL.md              # 核心：YAML frontmatter + Markdown 指令
├── scripts/
│   └── helper.sh         # 可被 Claude 执行的辅助脚本
├── references/
│   └── REFERENCE.md      # 参考资料（按需加载）
└── assets/               # 图片、模板等静态资源
```

### 3.1 YAML Frontmatter 字段

```yaml
---
name: frontend-design                    # 唯一标识符（kebab-case）
description: |                           # ⚡ 关键字段：触发条件描述
  Create distinctive, production-grade frontend interfaces...
  Use this skill when the user asks to build web components,
  pages, artifacts, posters, or applications.
argument-hint: "<component-description>" # 填写后可作为 /skill-name 斜杠命令调用
context: fork                            # 可选：在独立 subagent 中运行（无对话历史）
license: Custom (see LICENSE.txt)        # 可选：授权说明
---
```

**`description` 字段的重要性**：  
Claude Code 启动时仅加载每个 Skill 的 `name` 和 `description`（约 100 tokens / skill），通过语义匹配决定是否激活。描述模糊的 Skill 激活不稳定；包含明确触发短语的描述激活最可靠。

### 3.2 Markdown 指令正文

YAML frontmatter 之后的 Markdown 内容就是 Claude 的具体指令，支持：

- 标准 Markdown（标题、列表、代码块）
- `$ARGUMENTS` / `$0`, `$1`, `$2` 参数占位符
- `` !`shell-command` `` 语法：将命令输出注入到 Prompt 上下文
- 引用 `ultrathink` 关键字：自动启用 Extended Thinking 模式

```markdown
# Frontend Design Skill

Before writing any code, run:
!`cat package.json | grep '"react"'`

Then design a component that matches the current React version.

Implement: $ARGUMENTS
```

---

## 四、三层渐进式加载机制（Progressive Disclosure）

这是 Agent Skills 最精妙的设计，解决了"大量 Skill 导致 Context Window 爆炸"的核心矛盾：

```
第 1 层（启动时，始终加载）
  ├─ skill-a: name + description     ~100 tokens
  ├─ skill-b: name + description     ~100 tokens
  └─ skill-n: name + description     ~100 tokens
  
第 2 层（任务匹配后，按需加载）
  └─ skill-b: 完整 SKILL.md 内容     <5,000 tokens

第 3 层（执行过程中，明确需要时）
  └─ skill-b/references/REFERENCE.md  仅在 Claude 决定需要时加载
```

**上下文占用估算**：
- 20 个 Skills 常驻：20 × 100 = 2,000 tokens（仅 ~0.5% 典型上下文）
- 激活 2 个 Skills：2 × 5,000 = 10,000 tokens  
- 总开销：~12,000 tokens，完全可控

---

## 五、Skill 作用域与优先级

Skills 可安装在四个层次，优先级从高到低：

```
企业级（Managed Settings）         ← 最高优先级，不可覆盖
    ↓
用户级 (~/.claude/skills/)         ← 跨所有项目私人 Skills
    ↓  
项目级 (.claude/skills/)           ← 随 Git 共享给团队
    ↓
目录级 (packages/frontend/.claude/skills/)  ← Monorepo 子包级别
```

**命名冲突规则**：
- 高优先级 Skill 覆盖同名低优先级 Skill
- Plugin Skills 使用 `plugin-name:skill-name` 命名空间，永远不与用户 Skills 冲突

---

## 六、Plugin 发布格式

Plugin 是将多个 Skills（以及 Agents、Hooks、MCP Servers）打包分发的容器：

```
my-plugin/
├── .claude-plugin
│   └── plugin.json          # Plugin 元数据（name, version, description）
├── skills/
│   ├── skill-a/
│   │   └── SKILL.md
│   └── skill-b/
│       └── SKILL.md
├── agents/
│   └── my-agent/
│       └── AGENT.md
└── mcp/
    └── my-server/           # 捆绑的 MCP Server
```

**Plugin Marketplace 命令**：

```bash
# 添加 Marketplace 源
/plugin marketplace add anthropics/skills

# 安装指定插件
/plugin install frontend-design@anthropics/skills

# 查看已安装插件
/plugin menu

# 卸载
/plugin uninstall frontend-design@anthropics/skills

# 重新加载（修改后生效）
/reload-plugins
```

---

## 七、Skill 的调用方式

### 7.1 语义自动激活（最常用）

无需任何命令，直接向 Claude 描述任务：

```
"Build a responsive dashboard with React and Tailwind"
```

Claude 扫描所有 Skills 的 `description`，匹配后自动加载 `frontend-design` Skill。

### 7.2 斜杠命令显式调用（需 `argument-hint`）

```bash
/frontend-design "Build a responsive dashboard with sidebar nav"

/migrate-component SearchBar React Vue    # 多参数：$0 $1 $2
```

### 7.3 `ultrathink` 启用深度推理

在 SKILL.md 正文中任意位置加入 `ultrathink`，Claude 将对该 Skill 的执行启用扩展推理。适合复杂架构决策类 Skills。

### 7.4 `context: fork` 隔离执行

```yaml
context: fork
```

Skill 在独立的 subagent 中执行，**不能访问当前对话历史**。适合完全独立的生成任务（如批量代码迁移）。

---

## 八、Skills 与 Agents 的协作模式

Claude Code Plugins 中可定义专用 **Agents**（子智能体），它们有独立的 system prompt，Skills 可以调用 Agents，Agents 也可以调用其他 Skills：

```
/recipe-implement "Add user auth"          ← Recipe Skill 入口
         ↓
  requirement-analyzer Agent              ← 分析规模，确定工作流
         ↓
  frontend-executor Agent                 ← 使用 React/TypeScript 规则执行
         ↓
  design-sync Agent                       ← 验证前后端接口一致性
```

这种"Skill → Agent → Skill"的嵌套调用构成了完整的**多智能体工作流**，是当前 Claude Code 生态最强大的模式。

---

## 九、Context Window 限制与最佳实践

> Claude Code 将 Skill `description` 字段总量限制在约 **上下文窗口的 2%**，超出部分被**静默忽略**。

**最佳实践**：

1. **不要装太多 Plugin**：`dev-skills` 和 `dev-workflows` 包含相同 Skills，同时安装会使 description 重复出现两次，可能触发限制
2. **description 要精确**：避免宽泛描述，使用明确的触发短语
3. **合理分层**：个人通用 Skills 放 `~/.claude/skills/`，项目专属 Skills 放 `.claude/skills/` 并提交 Git
4. **优先用 Plugins 分发**：插件命名空间隔离，更新方便，避免手动复制文件

---

## 十、Agent Skills 规范的跨工具可移植性

**agentskills.io/specification** 是开放标准，已被以下工具支持：

| 工具 | 支持状态 |
|------|---------|
| Claude Code | ✅ 原生支持 |
| OpenAI Codex | ✅ 支持 |
| Cursor | ✅ 支持 |
| Gemini CLI | ✅ 支持 |
| VS Code (Copilot Agent Mode) | 🚧 实验性 |

这意味着你为 Claude Code 编写的 `frontend-design` Skill，理论上可以无修改地在 Cursor 中使用。**SKILL.md 是一次编写、多处运行的前端 AI 能力包。**

---

## 十一、小结

| 概念 | 一句话 |
|------|--------|
| SKILL.md | Skill 的核心：YAML 元数据 + Markdown 指令 |
| description 字段 | 触发开关：精确描述决定 Skill 是否被正确激活 |
| 三层加载 | 元数据 → 全文 → 资源，Context 效率最优 |
| Plugins | Skill 集合的发布容器，支持 Marketplace 一键安装 |
| Agents | Skill 可调用的专用子智能体，构建多步工作流 |
| 跨工具兼容 | Agent Skills 规范被 Claude/Codex/Cursor/Gemini CLI 共同采用 |

---

**下一篇** → `02_anthropic_official_frontend_design_skill.md`  
Anthropic 官方 `frontend-design` Skill 深度解析：设计哲学、Anti-AI-Slop 方法论与完整指令剖析

---

*调查时间：2025年4月 | 数据来源：code.claude.com/docs, agentskills.io, snyk.io, travisvn/awesome-claude-skills*
