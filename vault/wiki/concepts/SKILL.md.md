---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, configuration, specification]
aliases: ["SKILL.md", "Skill Definition File"]
relates_to:
  - target: "[[Agent Skills]]"
    type: implements
  - target: "[[Claude Code]]"
    type: used_by
supersedes: null
---

# SKILL.md

## 概述
[[Agent Skills]]的核心文件，包含YAML frontmatter元数据和Markdown指令，定义了AI[[Skills|技能]]的具体行为和[[Configuration|配置]]。

## 关键内容

1. **文件结构**：
   ```
   skill-name/
   ├── SKILL.md              # 核心：YAML frontmatter + Markdown 指令
   ├── scripts/
   │   └── helper.sh         # 可被 Claude 执行的辅助脚本
   ├── references/
   │   └── REFERENCE.md      # 参考资料（按需加载）
   └── assets/               # 图片、模板等静态资源
   ```

2. **YAML Frontmatter字段**：
   - name: 唯一标识符（kebab-case）
   - description: 触发条件描述，影响技能的自动激活
   - argument-hint: 参数提示，使技能可通过斜杠命令调用
   - context: 可选字段，fork表示在独立subagent中运行
   - license: 可选字段，授权说明

3. **Markdown指令特性**：
   - 支持标准Markdown语法
   - $ARGUMENTS / $0, $1, $2 参数占位符
   - !`shell-command` 语法：将命令输出注入Prompt上下文
   - 可使用ultrathink关键字启用[[扩展思维|Extended Thinking]]模式

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Agent Skills]] — implements
- [[Claude Code]] — used_by