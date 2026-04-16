---
title: "How and when to use subagents in Claude Code"
source: "https://claude.com/blog/subagents-in-claude-code"
author:
published: 2001-04-07
created: 2026-04-16
description: "When to delegate research, parallelize tasks, or get a fresh review with Claude Code subagents—and when to stick with the main session."
tags:
  - "clippings"
---
[Claude Code](https://code.claude.com/docs/en/overview) handles complex, multi-step projects well, but long sessions accumulate weight. Every file read, every tangent explored, every half-finished thought stays in the context window, slowing responses and driving up token costs.[Claude Code](https://code.claude.com/docs/en/overview) 能够很好地处理复杂的多步骤项目，但长时间的会话会累积负担。每一个读取的文件、每一次探索的偏离方向、每一个未完成的想法，都会保留在上下文窗口中，导致响应速度变慢，同时也会增加令牌成本。

Consider building a new feature in a large TypeScript monorepo. The main work is the implementation, but side tasks keep appearing: trace how an existing service handles auth, find the shared util for date formatting, check whether the design system already has a component close to what you need. None of these need the full project context, and running them inside the main session adds noise. What if you could run them in parallel?设想在一个大型 TypeScript 单仓库中开发新功能。核心工作是功能实现，但各类辅助任务不断出现：追踪现有服务的身份验证处理逻辑、查找日期格式化的共享工具函数、检查设计系统中是否存在与你所需功能相近的组件。这些任务都无需完整的项目上下文，若在主开发会话中执行，会产生干扰。那如果能并行处理这些任务呢？

Enter [subagents](https://code.claude.com/docs/en/sub-agents). A subagent is an isolated Claude instance with its own context window. It takes a task, does the work, and returns only the result. Think of subagents as the browser tabs of a Claude Code session: a place to chase a tangent without losing the main thread.引入 [子代理](https://code.claude.com/docs/en/sub-agents) 。子代理是一个拥有独立上下文窗口的独立 Claude 实例。它接收任务、完成工作后仅返回结果。可以将子代理视为 Claude 代码会话中的浏览器标签页：一个可以探索旁支思路而不中断主线的地方。

In this article, we discuss when it makes sense to use subagents, how to invoke them, and when the overhead isn't worth it.在本文中，我们将探讨何时适合使用子智能体、如何调用子智能体，以及何时相关的额外开销得不偿失。

## What is a subagent? 什么是子代理？

Subagents are self-contained agents that operate with their own context windows. When Claude spawns a subagent, that assistant works independently to read files, explore code, or make changes. When it completes its task, the subagent returns only the relevant results to the main conversation.子智能体是拥有独立上下文窗口的自包含智能体。当 Claude 生成一个子智能体时，该助手会独立开展工作，读取文件、探索代码或进行修改。完成任务后，子智能体仅会将相关结果返回至主对话中。

Each subagent starts fresh, unburdened by the history of the conversation or invoked skills. Multiple subagents can run in parallel, and each can have different permissions: a research subagent might have read-only access, while an implementation subagent gets full editing capabilities.每个子代理都从零开始，不受对话历史或已调用技能的影响。多个子代理可并行运行，且各自拥有不同权限：研究类子代理可能只有只读权限，而执行类子代理则具备完整的编辑能力。

Claude Code includes several built-in subagent types, including:Claude Code 包含多种内置的子代理类型，包括：

- **General-purpose agents** for complex multi-step tasks **通用型智能体** ，适用于复杂的多步骤任务
- **Plan agents** that research codebases before presenting implementation strategies **规划智能体** ，会先研究代码库，再提出实施策略
- **Explore agents** optimized for fast, read-only code search **探索型智能体** ，专为快速的只读代码搜索而优化

Claude Code often spawns subagents on its own to handle assigned tasks. It's also possible to direct that behavior explicitly and to define reusable specialists that Claude delegates to automatically. Knowing when to reach for subagents is what makes the feature useful. Claude Code 通常会自行生成子代理来处理分配的任务。也可以明确指定这种行为，并定义可复用的专业代理，让 Claude 自动委托给它们。知道何时调用子代理，是该功能发挥作用的关键。

## When should you use subagents? 什么时候应该使用子智能体？

Certain categories of work benefit clearly from subagent delegation. Learning to recognize them makes the feature far more effective.某些类型的工作显然能从子代理委托中获益。学会识别这些类型，能让该功能的效果大幅提升。

### Research-heavy tasks 研究类任务

When understanding how something works is a prerequisite to changing it, a subagent can explore the codebase and return a summary rather than dumping dozens of files into the conversation.当了解某个事物的运作方式是改变它的前提时，子智能体可以探索代码库并返回摘要，而不是将数十个文件直接丢到对话中。

**The signal:** Gathering context requires reading dozens of files.信号：</b>收集背景信息需要阅读数十个文件。

**The benefit:** The main conversation stays clean, and synthesized findings arrive instead of raw content.**好处在于：** 核心对话保持简洁，呈现的是整合后的结论而非原始内容。

### Multiple independent tasks 多个独立任务

When fixing errors across several files, updating patterns in multiple components, or making changes that don't depend on each other, parallel subagents complete the task faster.在修复多个文件中的错误、更新多个组件中的模式，或进行彼此不相关的修改时，并行子智能体能更快地完成任务。

**The signal:** Sub-tasks have no dependencies between them.**信号：** 子任务之间没有依赖关系

**The benefit:** Three subagents working simultaneously generally finish the task in less time.**优势：** 三个子代理同时工作通常能在更短的时间内完成任务。

### Fresh perspective needed 需要全新视角

When an unbiased review of an implementation is the goal, a subagent provides a clean slate because it doesn't inherit the assumptions, context, or blind spots from the primary conversation.当以对某个实现进行客观评估为目标时，子智能体是一张干净的白纸，因为它不会继承主对话中的假设、上下文或盲点。

**The signal:** Verification is needed without conversation history influencing the analysis.**核心要点：** 需要在不将对话历史纳入分析的情况下进行验证。

**The benefit:** Cleaner, more objective feedback.**好处：** 更清晰、更客观的反馈。

**Pro-tip:** The /clear command also resets context and conversation history, providing a similarly unbiased slate, but at the cost of losing that history entirely. A subagent achieves the same fresh perspective while the main conversation stays intact.**专业提示：** /clear 命令也会重置上下文和对话历史，提供一个同样无偏向的全新状态，但代价是会彻底丢失该历史记录。子智能体则能在主对话保持完整的情况下，实现同样的全新视角。

### Verification before committing 提交前验证

Before finalizing changes, an independent subagent can verify the implementation isn't overfitting to tests or missing edge cases.在最终确定修改之前，独立子智能体可以验证实现方式不会过度拟合测试用例，也不会遗漏边界情况。

**The signal:** A second opinion is warranted before committing code.**信号：** 提交代码前需要征求第二种意见。

**The benefit:** Catches issues that familiarity with the code might obscure.**好处：** 能发现因对代码过于熟悉而可能被忽略的问题。

### Pipeline workflows 流水线工作流

When a task has distinct phases (i.e., design, then implement, then test), each stage benefits from focused attention.当一项任务具有不同的阶段（即先设计、再实施、最后测试）时，每个阶段都需要集中精力来推进。

**The signal:** Sequential stages with clear handoffs.**信号：** 存在具有明确交接的连续阶段。

**The benefit:** Each subagent concentrates on its phase, without context from other stages creating noise.**优势：** 每个子智能体专注于自身阶段，不会因其他阶段的上下文产生干扰。

**Pro-tip:** When a task requires exploring ten or more files, or involves three or more independent pieces of work, that's a strong signal to direct Claude toward subagents.**专业提示：** 当一项任务需要浏览十个及以上文件，或涉及三个及以上独立工作内容时，这是引导 Claude 转向子智能体的强烈信号。

## How to direct subagent usage 如何指导子代理的使用

Several methods exist for invoking subagents, ranging from simple conversation to automated workflows. The right starting point depends on the workflow, and sophistication can be layered on as patterns emerge.调用子智能体的方法有多种，从简单对话到自动化工作流皆可。合适的起点取决于具体工作流，随着模式的形成，还可以逐步增加系统的复杂程度。

### Conversational invocation 对话式调用

The most flexible approach is simply asking Claude to use subagents in conversation. This works across all Claude Code interfaces: terminal, VS Code, JetBrains, the web, and desktop applications. 最灵活的方法是直接让 Claude 在对话中使用子代理。这适用于所有 Claude Code 界面：终端、VS Code、JetBrains、网页以及桌面应用程序。

Natural language patterns that reliably invoke subagents include:可可靠调用子智能体的自然语言模式包括：

- "Use a subagent to explore how authentication works in this codebase" “使用子代理探索此代码库中的身份验证工作原理”
- "Have a separate agent review this code for security issues" “让一个独立的智能体检查这段代码是否存在安全问题”
- "Research this in parallel. Check the API routes, database models, and frontend components simultaneously" “同步开展这项研究。同时检查API路由、数据库模型和前端组件”
- "Spin up subagents to fix these TypeScript errors across the different packages" 启动子代理来修复不同包中的这些 TypeScript 错误

Being explicit matters. Specify the scope, request parallel execution when tasks are independent, and describe the desired output.明确性至关重要。请明确范围，在任务相互独立时请求并行执行，并说明期望的输出结果。

Here's an effective prompt structure:这是一个高效的提示词结构：

```markdown
Use subagents to explore this codebase in parallel:

1. Find all API endpoints and summarize their purposes
2. Identify the database schema and relationships
3. Map out the authentication flow

Return a summary of each, not the full file contents.
```

This prompt works because it clearly defines three independent tasks, explicitly requests parallel execution, and specifies the output format. Claude understands the intent and spawns appropriate subagents.这个提示语之所以有效，是因为它明确定义了三项独立任务，明确要求并行执行，并指定了输出格式。Claude 能理解这一意图并生成相应的子智能体。

Tips for effective conversational invocation include:高效对话式调用的技巧包括：

- **Scope tasks clearly.** "Explore how payments work" beats "explore everything." **明确任务范围。** “探索支付系统的运作方式”比“探索所有事物”效果更好。
- **Request parallelization explicitly.** Say "these can run in parallel" or "work on all three simultaneously." **显式请求并行化。** 可以说“这些可以并行运行”或“同时处理全部三个”。
- **Specify what should be returned.** Summaries, specific findings, or recommendations. Naming the output format helps Claude deliver it.**指定需要返回的内容。** 摘要、具体发现或建议。明确输出格式有助于 Claude 生成相应内容。
- **Ask for fresh context when unbiased analysis matters.** "Use a subagent that does not see our previous discussion" ensures clean evaluation.**在需要客观分析时获取新的上下文。** “使用一个看不到我们之前讨论内容的子智能体”可确保评估的准确性。

**Pro-tip:** When a subagent is taking a while, Ctrl+B sends it to the background. The conversation can continue while it runs, and results surface automatically when it finishes. The /tasks command shows anything running in the background.**小技巧：** 当子代理需要较长时间时，按 Ctrl+B 可将其转入后台运行。在此期间可以继续对话，任务完成后结果会自动显示。/tasks 命令可查看所有后台运行的任务。

### Custom subagents 自定义子代理

When the same kind of subagent keeps getting requested (a security reviewer, a test writer, a docs proofreader), it can be defined once as a custom subagent. 当同一类子代理被反复请求（比如安全审核员、测试编写员、文档校对员）时，可将其一次性定义为自定义子代理。

Claude then delegates to it automatically whenever a task matches its description, no prompting required.当任务与描述匹配时，Claude 会自动将其委派给它，无需任何提示。

Custom subagents live as markdown files in `.claude/agents/ ` (project-level, shared with the team) or `~/.claude/agents/ ` (user-level, available across all projects). Each one gets its own system prompt, tool permissions, and optionally its own model.自定义子代理以 Markdown 文件的形式存储在 `.claude/agents/ ` （项目级，与团队共享）或 `~/.claude/agents/ ` （用户级，适用于所有项目）中。每个子代理都有自己的系统提示词、工具权限，还可选择配备专属模型。

The easiest way to create one is the /agents command, which walks through setup interactively and can generate a first draft from a description. The file can also be written by hand, for example:创建它最简单的方法是使用 /agents 命令，该命令会以交互方式引导完成设置，并能根据描述生成初稿。你也可以手动编写该文件，例如：

```markdown
---
name: security-reviewer
description: Reviews code changes for security vulnerabilities,
  injection risks, auth issues, and sensitive data exposure.
  Use proactively before commits touching auth, payments, or user data.
tools: Read, Grep, Glob
model: sonnet
---

You are a security-focused code reviewer. Analyze the provided
changes for:
- SQL injection, XSS, and command injection risks
- Authentication and authorization gaps
- Sensitive data in logs, errors, or responses
- Insecure dependencies or configurations

Return a prioritized list of findings with file:line references
and a recommended fix for each. Be critical. If you find nothing,
say so explicitly rather than inventing issues.
```

With this in place, Claude routes matching work to the subagent automatically. It can also be invoked by name: "Have the security-reviewer look at the staged changes." 完成这些设置后，Claude 会自动将匹配的工作分配给子智能体。你也可以直接通过名称调用它：“让安全审核员查看已暂存的更改。”

Custom subagents work best when: 自定义子智能体在以下情况下效果最佳：

- A specialist should be available for Claude to delegate to automatically when a task matches 当任务匹配时，应有专门人员可供 Claude 自动委派
- The work benefits from a tightly scoped system prompt and restricted tools 这项工作得益于范围明确的系统提示词和受限制的工具
- The configuration should be shared across a team or reused across projects 该配置应在团队间共享或在多个项目中重复使用

**Pro-tip:** The description field is what Claude uses to decide when to delegate. Be specific about the trigger conditions, not just the capability. "Reviews code for security issues before commits" routes better than "security expert." **专业提示：** Claude 会根据描述字段来判断何时进行任务委派。请具体说明触发条件，而非仅描述能力。“在提交代码前审查代码中的安全问题”比“安全专家”更易匹配到合适的任务分配。

For the full configuration reference, including permission modes and how project and user subagents interact, see our [Claude Code subagents docs.](https://code.claude.com/docs/en/sub-agents)有关完整的配置参考（包括权限模式以及项目和用户子代理的交互方式），请参阅我们的 [Claude Code 子代理文档](https://code.claude.com/docs/en/sub-agents) 。

### CLAUDE.md instructions CLAUDE.md 说明

Custom subagents define who the specialists are. CLAUDE.md files define the rules for when Claude should reach for them. If every code review should go through a read-only subagent, or every architecture question should trigger a research pass first, CLAUDE.md is where that policy lives. Claude reads it at the start of every conversation, so the behavior stays consistent across sessions and teammates without anyone needing to remember to ask.自定义子代理定义了专业人员的身份。CLAUDE.md 文件规定了克劳德何时应该调用这些专业人员的规则。如果每次代码审查都需要通过只读子代理，或者每个架构问题都需要先触发一次调研流程，那么相关策略就写在 CLAUDE.md 中。克劳德会在每次对话开始时读取该文件，因此无需任何人刻意提醒，其行为在不同会话和团队成员之间都能保持一致。

CLAUDE.md is a good fit for subagent instructions when:CLAUDE.md 适用于子智能体指令的情况为：

- Code reviews should always use read-only subagents 代码审查应始终使用只读子代理
- The project has specific research patterns Claude should follow 该项目有Claude应遵循的特定研究模式
- Consistent behavior is needed across team members and sessions 团队成员和会话之间需要保持一致的行为

Here’s an example of a simple CLAUDE.md file that triggers a subagent given specific conditions:下面是一个简单的 CLAUDE.md 文件示例，该文件会在特定条件下触发子智能体：

```markdown
## Code review standards

When asked to review code, ALWAYS use a subagent with READ-ONLY access
(Glob, Grep, Read only). The review should ALWAYS check for:
- Security vulnerabilities
- Performance issues
- Adherence to project patterns in /docs/architecture.md

Return findings as a prioritized list with file:line references.
```

With the above CLAUDE.md file, every code review request automatically uses the defined pattern, eliminating the need to specify it each time.有了上述的 CLAUDE.md 文件，所有代码审查请求都会自动使用定义好的模式，无需每次都手动指定。

For more on CLAUDE.md files, see [Customizing Claude Code for your codebase: setting up a CLAUDE.md file](https://preview.claude.ai/chat/link) and our Claude Code [CLAUDE.md](http://claude.md/) [file docs](https://code.claude.com/docs/en/memory#claude-md-files). 要了解更多关于 CLAUDE.md 文件的信息，请查看 [为你的代码库定制 Claude Code：设置 CLAUDE.md 文件](https://preview.claude.ai/chat/link) 以及我们的 Claude Code [CLAUDE.md](http://claude.md/) [文件文档](https://code.claude.com/docs/en/memory#claude-md-files) 。

### Skills 技能

For complex multi-step workflows that run repeatedly, skills provide a reusable interface. Define a skill once in.claude/skills/, then invoke it with /skill-name or let Claude load it automatically when a task matches its description.对于需要重复运行的复杂多步骤工作流，技能提供了可复用的接口。你可以在.claude/skills/ 目录下定义一次技能，然后通过 /技能名称 调用它，或者在任务与技能描述匹配时让 Claude 自动加载它。

Skills differ from CLAUDE.md files in scope. CLAUDE.md files are always loaded and shapes every interaction. A skill is loaded on demand, either because it was invoked explicitly or because Claude matched the current task to the skill's description field. That makes skills the right place for workflows that should be available but not applied to every prompt.技能在范围上与 CLAUDE.md 文件不同。CLAUDE.md 文件会始终被加载并影响每一次交互。技能则是按需加载的，要么是因为被显式调用，要么是因为 Claude 将当前任务与技能的描述字段相匹配。这使得技能非常适合那些需要可用但不应应用于每个提示词的工作流。

Skills fit well when: 技能适配的情况包括：

- Certain actions get run regularly 某些操作会被定期执行
- Different team members need access to the same complex operation 不同的团队成员需要访问同一个复杂操作
- Standardizing how certain tasks are performed across the team matters 在团队中统一部分任务的执行方式至关重要

Here’s an example of a deep-review skill for comprehensive code review:下面是一个用于全面代码审查的深度审查技能示例：

```markdown
# .claude/skills/deep-review/SKILL.md

---
name: deep-review
description: Comprehensive code review that checks security,
  performance, and style in parallel. Use when reviewing staged
  changes before a commit or PR.
---

Run three parallel subagent reviews on the staged changes:

1. Security review - check for vulnerabilities, injection risks,
   authentication issues, and sensitive data exposure
2. Performance review - check for N+1 queries, unnecessary iterations,
   memory leaks, and blocking operations
3. Style review - check for consistency with project patterns
   documented in /docs/style-guide.md

Synthesize findings into a single summary with priority-ranked issues.
Each issue should include the file, line number, and recommended fix.
```

In the code snippet above, /deep-review triggers a three-part subagent analysis on demand. Because the description mentions reviewing staged changes before commits, Claude can also reach for this skill automatically when that context comes up.在上面的代码片段中，/deep-review 会按需触发三部分子智能体分析。由于描述中提到了在提交前审查暂存的更改，当出现该上下文时，Claude 也能自动调用这项技能。

A skill is a directory, not a single file. Alongside `SKILL.md,` it can hold templates Claude fills in, example outputs showing the expected format, or scripts Claude executes as part of the workflow. The legacy `.claude/commands/ ` format was a single flat file, so everything had to live in the prompt itself.技能是一个目录，而非单个文件。除了 `SKILL.md,`之外，它还可以存放 Claude 填写的模板、展示预期格式的示例输出，或是 Claude 作为工作流一部分执行的脚本。传统的`.claude/commands/ ` 格式是单一的扁平文件，因此所有内容都必须放在提示词本身中。

For more on using skills with Claude Code, see our [Claude Code skills docs.](https://code.claude.com/docs/en/skills#extend-claude-with-skills)要了解如何在 Claude Code 中使用技能的更多信息，请查看我们的 [Claude Code 技能文档](https://code.claude.com/docs/en/skills#extend-claude-with-skills) 。

### Hooks 钩子

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. [Hooks](https://code.claude.com/docs/en/hooks-guide) can automate subagent workflows based on events. Hooks trigger on specific actions and run subagent tasks without manual invocation.钩子是用户定义的在 Claude Code 生命周期特定节点自动执行的 Shell 命令、HTTP 端点或大语言模型提示词。 [钩子](https://code.claude.com/docs/en/hooks-guide) 可基于事件自动化子智能体工作流。钩子会在特定操作触发时运行，无需手动调用即可执行子智能体任务。

Hooks are the right tool when: 钩子适用于以下场景：

- Every commit should be reviewed automatically before it's created 每次提交都应在创建前自动进行审核
- Security checks should run without anyone remembering to ask 安全检查应在无人提醒的情况下自动执行
- CI-like quality gates belong in the local development process 类CI的质量门禁应纳入本地开发流程

Here is an example of a Stop hook that blocks Claude from ending its turn until a test is passed:下面是一个停止钩子的示例，它会阻止 Claude 结束本轮对话，直到通过一项测试：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-tests.sh"
          }
        ]
      }
    ]
  }
}
```

And the script at `.claude/hooks/check-tests.sh`:以及位于 `.claude/hooks/check-tests.sh` 的脚本：

```bash
#!/bin/bash
INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# Don't loop forever — if we already blocked once this turn, let it through
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0
fi

if ! npm test --silent > /dev/null 2>&1; then
  jq -n '{
    decision: "block",
    reason: "Tests are failing. Run \`npm test\` to see the failures and fix them before finishing."
  }'
  exit 0
fi

exit 0
```

When Claude finishes its turn, the Stop event fires. The script runs the test suite—if tests fail, it returns JSON with `decision: "block"` and a `reason`. Claude Code reads that, doesn't let Claude stop, and feeds the reason back into the conversation as instruction to keep working. The `stop_hook_active` guard at the top prevents infinite loops: if Claude is already continuing because of a previous stop-hook block, the script lets it exit.当 Claude 完成一轮回复后，Stop 事件触发。脚本运行测试套件——如果测试失败，它会返回包含 `decision: "block"` 和 `reason` 的 JSON 数据。Claude Code 读取该数据后，不会让 Claude 停止，而是将失败原因作为指令反馈到对话中，让其继续工作。顶部的 `stop_hook_active` 保护机制可防止无限循环：若 Claude 因之前的停止钩子模块而处于继续状态，脚本会允许其退出。

Hooks represent the most automated approach to subagent orchestration. Conversational invocation or CLAUDE.md instructions are the better starting point; hooks come later, as workflows mature.Hooks 是子代理编排最自动化的方式。对话式调用或 CLAUDE.md 说明是更好的起点；随着工作流成熟，再引入 Hooks 会更合适。

For complete hooks configuration, see [Claude Code power user customization: how to configure hooks](https://claude.com/blog/how-to-configure-hooks) or our [Claude Code hooks docs](https://code.claude.com/docs/en/hooks).有关完整的 hooks 配置，请参阅 [Claude Code 高级用户自定义：如何配置 hooks](https://claude.com/blog/how-to-configure-hooks) 或我们的 [Claude Code hooks 文档](https://code.claude.com/docs/en/hooks) 。

## Practical patterns for using subagents使用子智能体的实用模式

The following patterns demonstrate subagent direction applied to common scenarios.以下模式展示了应用于常见场景的子代理指导方法。

### Research before implementing 实施前调研

When adding a feature to unfamiliar code, delegating research to a subagent first keeps the implementation discussion informed rather than exploratory, for example: 在给不熟悉的代码添加功能时，先将调研工作委托给子智能体，能让实现讨论始终围绕既定方向展开，而非漫无目的地探索，例如：

```markdown
Before I implement user notifications, use a subagent to research:
- How are emails currently sent in this codebase?
- What notification patterns already exist?
- Where should new notification logic live based on the current architecture?

Summarize findings, then we'll plan the implementation together.
```

A synthesized summary arrives instead of twenty files of raw context, and the implementation discussion starts from a solid foundation.得到的是一份综合摘要，而非二十份原始上下文文件，实施讨论也能从扎实的基础上展开。

### Parallel modifications 并行修改

When the same pattern needs updating across multiple files, parallel subagents finish faster and maintain focus, for example: 当需要在多个文件中更新同一模式时，并行子智能体的完成速度更快，且能保持专注，例如：

```markdown
Use parallel subagents to update the error handling in these files:
- src/api/users.ts
- src/api/orders.ts
- src/api/products.ts

Each should follow the pattern established in src/api/auth.ts.
Work on all three simultaneously.
```

Three subagents working in parallel complete in roughly the time one would take. Each focuses on its file without context from the others creating confusion or inconsistency.三个并行工作的子智能体完成任务的时间大致与单个智能体所需时间相当。每个子智能体都专注于自己的文件，不会接收其他子智能体的上下文信息，从而避免产生混乱或不一致的情况。

### Independent review 独立审查

After implementing something complex, verification from a subagent that hasn't been influenced by the implementation journey catches what familiarity obscures, for example: 在完成某项复杂的实施工作后，由未受实施过程影响的子代理进行验证，能够发现熟悉感所掩盖的问题，例如：

```markdown
Use a fresh subagent with read-only access to review my implementation of the payment flow. It should not see our previous discussion. I want an unbiased review.

Check for: security vulnerabilities, unhandled edge cases, and error handling gaps. Be critical.
```

The review subagent evaluates the code without knowing what tradeoffs were considered, what approaches were rejected, or what assumptions were made. This outside perspective surfaces issues the main conversation might miss.审查子智能体在评估代码时，并不了解当初考虑了哪些权衡、拒绝了哪些方案，也不清楚做出了哪些假设。这种外部视角能发现主对话中可能遗漏的问题。

### Pipeline workflow 流水线工作流程

For multi-stage tasks, chaining subagents with explicit handoffs between phases keeps each stage focused, for example: 对于多阶段任务，在各阶段之间通过显式交接来串联子智能体，可让每个阶段保持专注，例如：

```markdown
Let's build this feature as a pipeline:

1. First subagent: Design the API contract and write it to docs/api-spec.md
2. Second subagent: Implement the backend endpoints based on that spec
3. Third subagent: Write integration tests for the implementation

Each stage should complete before the next begins. Use the output
files as the handoff mechanism between stages.
```

Using a pipeline workflow, each stage in the task receives focused context. The design subagent isn't distracted by implementation concerns, the implementation subagent works from a clean spec, and the testing subagent evaluates the result independently. 采用流水线工作流时，任务中的每个阶段都会接收聚焦的上下文。设计子智能体不会被实现问题分散注意力，实现子智能体依据清晰的规范开展工作，测试子智能体则独立评估结果。

## When shouldn’t you use subagents? 什么时候不应该使用子代理？

While subagents are a useful feature, subagents carry overhead. Each one spins up its own context, consumes tokens, and adds a layer of indirection between the developer and the work. They're worth that cost when context isolation, parallelism, or a fresh perspective actually helps. 虽然子智能体是一项实用功能，但它们也会带来额外开销。每个子智能体都会启动独立的上下文、消耗令牌，并在开发者与具体任务之间增加一层间接性。只有当上下文隔离、并行处理或全新视角确实能带来帮助时，这些成本才是值得的。

For smaller or tightly sequential tasks, sticking to the main conversation is usually simpler, for example: 对于较小或紧序的任务，坚持在主对话中进行通常更简单，例如：

- **Sequential, dependent work.** When step two needs the full output of step one, and step three needs both, a single session handling the chain is usually cleaner than a relay of subagents passing state through files.**顺序化的依赖型工作。** 当第二步需要第一步的完整输出，而第三步需要前两者的结果时，由单个会话处理整个流程通常比由子代理通过文件传递状态的方式更简洁。
- **Same-file edits.** Two subagents editing the same file in parallel is a recipe for conflict. In this scenario, keep tightly coupled changes in one context window.**同文件编辑。** 两个子代理并行编辑同一个文件极易引发冲突。在这种情况下，需将紧密耦合的修改放在同一个上下文窗口中。
- **Small tasks.** For a quick fix or a focused question, the overhead of delegation outweighs the benefit. Just prompt or ask in your main conversation. **小任务。** 如果只是为了快速解决问题或解答某个具体问题，委托他人的额外成本会超过其带来的好处。直接在你的主对话中提示或询问即可。
- **Too many specialist agents.** It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable. Most teams settle on a handful of well-scoped agents rather than a sprawling roster.**专业智能体过多。** 为所有事物都定义一个自定义子智能体固然诱人，但向 Claude 提供过多选项会降低自动委托的可靠性。大多数团队最终会选择少数几个范围明确的智能体，而非组建庞大的智能体队伍。
- **Work that needs agents to coordinate with each other.** Subagents report back to the main conversation but can't talk to one another. For tasks where subagents need to communicate, use [agent teams](https://code.claude.com/docs/en/agent-teams). With agent teams, subagents coordinate across separate sessions rather than within one, which makes them heavier and more expensive. For more guidance on when to use subagents vs Agent Teams, check out our [Claude Code agent teams docs](https://code.claude.com/docs/en/agent-teams).**需要智能体相互协作的工作。** 子智能体向主对话汇报，但彼此之间无法交流。对于子智能体需要沟通的任务，请使用 [智能体团队](https://code.claude.com/docs/en/agent-teams) 。借助智能体团队，子智能体需在不同会话间进行协调，而非在单个会话内，这会使其运行成本更高、资源消耗更大。有关何时使用子智能体与智能体团队的更多指导，请查阅我们的 [Claude Code 智能体团队文档](https://code.claude.com/docs/en/agent-teams) 。

The signals described earlier (i.e., needing a second opinion, a lack of dependencies between sub-tasks, and extensive research) make it clear when delegation to a subagent is worth it.前文提到的几个信号——即需要听取他人意见、子任务之间缺乏依赖关系以及需要进行大量研究——都明确表明何时将任务委托给子智能体是值得的。

## Start conversational, automate later先以对话形式启动，后续再实现自动化

Subagents deliver their full value when used deliberately. The automatic invocation Claude provides is helpful, but knowing when to delegate research, parallelize work, and request a fresh perspective produces better results than leaving it to chance.子智能体在被有目的地使用时才能发挥全部价值。Claude 提供的自动调用功能固然有用，但知道何时委派研究任务、并行开展工作并寻求全新视角，会比听天由命带来更优的结果。

When using subagents, start with conversational prompts. Notice which requests keep occurring and build automation as those patterns clarify. The goal is to make subagent delegation effortless, so your attention stays on the work that matters.使用子智能体时，从对话式提示开始。留意哪些请求会反复出现，并在这些模式变得清晰时构建自动化功能。目标是让子智能体的委派变得轻松，这样你的注意力就能集中在重要的工作上。