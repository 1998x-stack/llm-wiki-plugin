# Obsidian Brain

融合三套方法论的个人知识操作系统：以 Obsidian vault 为核心数据层，AI Agent 为深度处理引擎。

## 方法论来源

| 来源 | 核心贡献 |
|------|---------|
| [LLM Wiki v1](llm-wiki-v1.md)（Karpathy） | 三层架构（raw/wiki/schema）、三个操作（ingest/query/lint） |
| [LLM Wiki v2](llm-wiki-v2.md)（agentmemory） | 四层记忆、知识图谱、置信度衰减、结晶化、自动化 hooks |
| [kepano-Obsidian](kepano-Obsidian%20使用方法论.md) | File-over-app、links-over-folders、低摩擦输入、分形回顾 |

## 系统定位

个人"第二大脑"——全面覆盖思考、学习、工作、成长。

**核心特征**：
- **Obsidian vault 即数据层**：所有数据都是 markdown 文件，无独立后端
- **AI Agent 做一切战术操作**：ingest、query、lint、consolidate、crystallize
- **四层记忆**：Working → Episodic → Semantic → Procedural，自动晋升与衰减
- **个人层与知识层分离**：journal/ 与 wiki/ 物理分离，自由互链
- **高度自动化**：新文件自动 ingest、每日自动 consolidate、每周自动 lint

## Vault 结构

```
obsidian-brain/
├── _schema/          # 系统规则（CLAUDE.md + 类型定义）
├── _memory/          # 四层记忆系统
│   ├── working/      # 当前会话观察
│   ├── episodic/     # 会话摘要
│   ├── semantic/     # 跨会话事实
│   └── procedural/   # 工作流与模式
├── raw/              # 不可变源材料
├── wiki/             # LLM 生成的知识页面
├── journal/          # 个人日记/思考/判断/成长
├── templates/        # 模板
├── index.md          # 内容目录
└── log.md            # 操作日志
```

## Agent Skills

| Skill | 功能 |
|-------|------|
| `wiki:ingest` | 源材料 → wiki 页面 + 更新 index/log |
| `wiki:query` | 搜索 → 综合答案 → 高质量答案自动归档 |
| `wiki:lint` | 检查孤页/矛盾/过期/缺失链接 → 自动修复 |
| `wiki:consolidate` | 记忆晋升 + 置信度衰减 |
| `wiki:crystallize` | 探索过程 → 结构化摘要 |
| `wiki:journal` | 辅助写日记，自动链接知识页面 |
| `wiki:review` | kepano 式分形回顾 |
| `wiki:qa-import` | QA jsonl → 洞见提取 → 双向链接 |

## 文档

- [设计文档](docs/superpowers/specs/2026-04-14-obsidian-brain-design.md) — 完整系统设计
- [v1 vs v2 对比](compare.md) — 两版 LLM Wiki 深度分析

## 交互入口

- **Obsidian**：日常快速记录、浏览、链接
- **AI Agent CLI**（Claude Code / Codex / OpenCode）：深度处理
- **Web App**（可选）：只读视图层

## 实施路径

1. 最小可行：vault 结构 + schema + ingest skill
2. 知识重建：迁移源文件并重新 ingest
3. 个人层：daily notes + journal + review
4. 记忆系统：四层记忆 + consolidate + crystallize
5. QA 集成：qa-import skill
6. 搜索增强：qmd MCP server（按需）
7. 自动化完善：fswatch + cron + hooks
