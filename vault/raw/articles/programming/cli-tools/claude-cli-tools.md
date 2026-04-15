# Claude CLI 工具全景图 2026

> 覆盖范围：官方 Anthropic 工具 + 主流第三方 CLI AI 编程代理（支持 Claude 模型）

---

## 🗺 全景分类

```
Claude CLI 生态
├── 官方工具
│   └── Claude Code (Anthropic)
├── 第三方 CLI 代理（支持 Claude 模型）
│   ├── Aider
│   ├── claude-engineer
│   ├── Cline
│   ├── Goose (Block)
│   └── OpenCode
└── AI 编程平台（有 CLI 接口）
    ├── Cursor CLI
    ├── Devin
    └── Kiro CLI (AWS)
```

---

## 🏆 官方工具：Claude Code

### 基本信息

| 属性 | 详情 |
|------|------|
| 开发者 | Anthropic |
| 安装方式 | `npm install -g @anthropic-ai/claude-code` 或 Homebrew |
| 认证 | Claude Pro/Max 订阅 或 Anthropic API Key |
| 平台 | macOS、Linux、Windows |
| 支持模型 | Claude Opus 4.6、Sonnet 4.6、Haiku 4.5 |
| IDE 集成 | VS Code、Cursor、Windsurf、JetBrains 全系列 |
| 收费 | Pro $20/mo · Max5 $100/mo · Max20 $200/mo · API 按 token |

### 核心能力

- **全代码库理解**：自动 agentic 搜索，无需手动选择上下文
- **多文件编辑**：跨文件原子性修改，理解依赖关系
- **Git 深度集成**：读 issue → 写代码 → 跑测试 → 提 PR 全流程
- **MCP 协议**：300+ 外部服务集成（GitHub、Slack、PostgreSQL、Jira...）
- **子代理系统**：并行多代理处理复杂任务
- **Hooks 系统**：PreToolUse / PostToolUse / Notification / Stop 钩子
- **CLAUDE.md**：项目级持久指令文件（编码规范、架构决策）
- **Web 模式**：`claude.ai/code` 浏览器运行，无需本地安装

### 完整 CLI 参数参考

```bash
# ── 基础使用 ──────────────────────────────────────────
claude "任务描述"          # 启动交互会话
claude -p "任务" --print   # 非交互模式，打印结果后退出
claude --continue / -c     # 继续上一次会话
claude --resume <session-id>  # 恢复指定会话
claude --from-pr <pr-url>  # 从 GitHub PR 恢复会话

# ── 模型与代理 ────────────────────────────────────────
claude --model sonnet           # 指定模型（sonnet/opus/haiku）
claude --fallback-model haiku   # 主模型过载时的降级模型
claude --agent <name>           # 指定自定义子代理
claude --agents '<json>'        # JSON 动态定义子代理

# ── 系统提示 ──────────────────────────────────────────
claude --system-prompt "..."         # 替换系统提示
claude --system-prompt-file <path>   # 从文件替换
claude --append-system-prompt "..."  # 追加到系统提示
claude --append-system-prompt-file <path>

# ── 工具与权限 ────────────────────────────────────────
claude --tools "Bash,Read,Edit"      # 限制可用工具
claude --allowedTools "Bash(git:*)"  # 无需确认直接执行的工具
claude --disallowedTools "Edit"      # 禁用指定工具
claude --permission-mode plan        # 计划模式（只规划不执行）
claude --dangerously-skip-permissions # 跳过所有权限确认（危险）

# ── 输出控制 ──────────────────────────────────────────
claude --output-format json          # 输出格式：text/json/stream-json
claude --input-format stream-json    # 输入格式
claude --verbose                     # 详细模式（完整 turn-by-turn 输出）

# ── 调试 ──────────────────────────────────────────────
claude --debug                       # 调试模式
claude --debug "api,mcp"             # 调试指定类别
claude --debug "!statsig,!file"      # 排除某类调试
```

### Slash 命令速查

```bash
# ── 文件与代码引用 ────────────────────────────────────
@./src/auth.ts          # 引用指定文件
@./src/                 # 引用目录
!git status             # 直接执行 shell 命令（跳过 token）

# ── 会话管理 ──────────────────────────────────────────
/clear                  # 清除上下文，开始新会话
/compact                # 压缩上下文（保留摘要）
/context                # 查看当前上下文使用量（彩色网格）
/cost                   # 查看 token 消耗统计

# ── 项目 & 配置 ───────────────────────────────────────
/init                   # 生成 CLAUDE.md 项目文件
/config                 # 通用设置（可搜索过滤）
/permissions            # 管理工具权限
/model                  # 切换模型
/hooks                  # 查看已配置的 Hooks

# ── 子代理 & 技能 ─────────────────────────────────────
/skills                 # 列出可用 Skills
/commands               # 列出所有命令和技能
/plugin                 # 插件管理

# ── Git & GitHub ──────────────────────────────────────
/install-github-app     # 安装 PR 自动 Review GitHub App

# ── 调试 & 诊断 ───────────────────────────────────────
/doctor                 # 运行诊断
/debug                  # 故障排查
/bug                    # 报告 Bug（发送对话给 Anthropic）

# ── 界面 ──────────────────────────────────────────────
/theme                  # 主题选择器（Ctrl+T 切换语法高亮）
/vim                    # 进入 Vim 模式
/terminal-setup         # 配置终端（Kitty/Alacritty/Zed/Warp）
```

### MCP 集成

```bash
claude mcp add                    # 交互式添加 MCP server
claude mcp add <name> <url>       # 添加指定 server
claude mcp list                   # 列出已配置 server
claude mcp remove <name>          # 删除 server

# 常见 MCP server 示例
claude mcp add github https://github.mcp.claude.com/mcp
claude mcp add postgres postgresql://...
claude mcp add slack https://slack.mcp.claude.com/mcp
```

### CLAUDE.md 模板

```markdown
# 项目：[项目名]

## 架构
- Monorepo，packages/ 下各子包
- React 前端 / FastAPI 后端 / Neo4j 图数据库

## 编码规范
- Python 3.12+，全量类型注解
- PEP 8 + 中文 PEP 257 文档字符串
- loguru 日志，不用 print
- 配置走 YAML，不硬编码

## 常用命令
- `uv run pytest` — 运行测试
- `uv run ruff check .` — Lint 检查
- `docker compose up -d` — 启动服务
```

### Hooks 配置示例

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "uv run ruff format $CLAUDE_FILE_PATHS"
        }]
      }
    ]
  }
}
```

---

## 🔧 第三方 Claude CLI 工具

### Aider

| 属性 | 详情 |
|------|------|
| 开发者 | Paul Gauthier（开源） |
| 安装 | `uv tool install aider-chat` |
| 定位 | Git-native AI 结对编程 |
| 特点 | 最强 Git 集成，自动 commit，架构最轻量 |
| 支持模型 | Claude、GPT-4o、Gemini、本地模型 |
| 评测排名 | 综合最高效（52.7% 准确率，126k tokens，257s） |

```bash
aider --model claude-sonnet-4-5              # 指定模型
aider --message "重构认证模块" src/auth.py   # 非交互单次执行
aider --yes                                  # 自动确认所有更改
aider --no-git                               # 不使用 git
```

### claude-engineer (v3)

| 属性 | 详情 |
|------|------|
| 开发者 | Doriandarko（开源） |
| 安装 | `pip install claude-engineer` |
| 定位 | 自扩展工具框架，Claude 动态创建自己的工具 |
| 特点 | Tool Creator（动态工具生成）、E2B 代码执行 |
| 特色 | CLI + Web UI 双界面 |

```bash
# 内置工具
# fileedit / diffedit / duckduckgo / webscraper / browser / screenshot
ce "帮我分析这个 Python 项目并优化性能瓶颈"
```

### Cline

| 属性 | 详情 |
|------|------|
| 开发者 | cline.bot（开源） |
| 安装 | VS Code 扩展 + CLI 模式 |
| 定位 | VS Code 内嵌 AI Agent |
| 特点 | 可视化 diff、浏览器操作、MCP 集成 |
| 支持模型 | Claude、GPT-4o、Gemini、本地模型 |

### Goose（Block/Square）

| 属性 | 详情 |
|------|------|
| 开发者 | Block（Jack Dorsey） |
| 安装 | `curl -fsSL https://github.com/block/goose/releases/...` |
| 定位 | 通用 AI Agent，不限于编程 |
| 特点 | 多后端模型支持，插件生态 |
| 注意 | 评测中代码准确率偏低（基础执行问题） |

### OpenCode

| 属性 | 详情 |
|------|------|
| 开发者 | 社区开源 |
| 安装 | `npm i -g opencode` |
| 定位 | 轻量 Claude Code 替代，支持更多模型 |
| 特点 | 跨模型兼容，含 Gemini CLI 生态 |

---

## 📊 CLI 工具横向评测（2025 Q4 benchmark）

基于 10 个真实 Web 开发场景，~600 个原子验证点：

```
┌────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ 工具            │ 综合准确率    │ 前端准确率    │ 后端准确率    │ Token 消耗   │
├────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ OpenAI Codex   │ 67.7% 🥇    │ 89.2%        │ 58.5%        │ 260k         │
│ Junie (JB)     │ 63.5% 🥈    │ 85.0%        │ 54.3%        │ 370k         │
│ Kiro CLI       │ 58.1%        │ —            │ —            │ 46.1 credits │
│ Claude Code    │ 55.5% 🥉    │ 95.0% 🏅    │ 38.6%        │ 397k         │
│ Aider          │ 52.7%        │ —            │ —            │ 126k ⭐      │
│ Cline          │ ~33%         │ 33.3%        │ 26.7%        │ —            │
│ Goose          │ ~7%          │ 10.0%        │ 3.1%         │ —            │
└────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

> **解读**：  
> - Claude Code 前端能力最强，但后端合约/路由处理弱  
> - Aider 是 token 效率冠军（126k vs Claude Code 的 397k）  
> - Codex CLI 综合第一，后端能力领先 5+ 个百分点  
> - Goose 基础执行能力存在问题，不推荐纯编程场景

---

## 🛠 AI Agent 工具链推荐配置

### 极速 Python AI 项目（推荐）

```bash
# 工具链
uv init my-ai-project
uv add langchain fastapi uvicorn
uv add --dev pytest ruff

# 使用 Claude Code
claude --model sonnet "分析 src/ 目录，为所有 FastAPI 端点补充类型注解和单元测试"
```

### Manim 动画工作流（XM 专属）

```bash
# 项目初始化
uv init manim-videos
uv add manim

# 让 Claude Code 生成动画
claude "根据 storyboard.md 生成 Manim 动画代码，中文用 Text(font='Noto Sans CJK SC')，
       验证几何计算后输出到 animations/ 目录"
```

### RAG / 知识图谱项目

```bash
uv add langraph neo4j milvus-lite dashscope fastapi

# CLAUDE.md 中写明：
# - 使用 Qwen/DashScope 模型
# - MinHash LSH 去重已在 dedup.py 中实现
# - Neo4j 连接配置在 config.yaml
```

---

## 🔮 2026 趋势展望

```
1. Claude Code Skill 生态爆发
   → 社区 SKILL.md 兼容 Claude Code / Cursor / Codex / Gemini CLI
   
2. MCP 成为标准协议
   → 8M+ 下载，300+ 集成，企业级工具链标配
   
3. 子代理并行化
   → 复杂任务拆分为并行子代理，类 MapReduce 编程模式
   
4. 跨工具 Skill 通用化
   → 同一 SKILL.md 在 11 种 AI 编程工具中通用

5. 云原生 Agent
   → claude.ai/code Web 模式 + GitHub Actions 原生集成
```

---

## 📚 参考资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [完整 CLI 指南 (Cranot)](https://github.com/Cranot/claude-code-guide)
- [Aider 官网](https://aider.chat)
- [claude-engineer v3](https://github.com/Doriandarko/claude-engineer)
- [AI CLI 代理评测 (AIMultiple)](https://aimultiple.com/agentic-cli)
- [claude-skills 社区库](https://github.com/alirezarezvani/claude-skills)
