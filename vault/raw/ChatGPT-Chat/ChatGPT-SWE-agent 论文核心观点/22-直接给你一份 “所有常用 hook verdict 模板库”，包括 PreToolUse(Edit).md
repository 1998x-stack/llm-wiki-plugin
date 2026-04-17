# 直接给你一份 “所有常用 hook verdict 模板库”，包括 PreToolUse(Edit)、PreToolUse(Bash)、PostToolUse(

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:50:03

## Question

直接给你一份 “所有常用 hook verdict 模板库”，包括 PreToolUse(Edit)、PreToolUse(Bash)、PostToolUse(Edit)、PostToolUseFailure 四套。

verdict 和 hook有什么互为补充，有什么区别

## Answer

我先把常用 hook 返回格式按官方字段整理成模板，再顺手把“hook vs verdict”这个关系讲清楚，避免后面把两者混用。

浏览Claude Code官方文档


Hooks 参考 - Claude Code Docs


已思考 11s

下面直接给你一份常用 hook verdict 模板库。先提醒一个关键点：


verdict 不是一个独立的“平台对象类型名”，而是 hook 写到 stdout 的 JSON 输出，用来表达放行、阻断、补充上下文、修改输入/输出等控制结果。 Claude Code 官方把这套东西描述为 hook 的 JSON output、decision control 和 event-specific output。Claude+1



1. PreToolUse(Edit) 模板


1.1 放行


适合：普通编辑，未命中保护规则。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Edit is allowed by local policy."
  }
}


PreToolUse 现在推荐用 hookSpecificOutput.permissionDecision，可用值包括 allow、deny、ask、defer。Claude


1.2 阻断受保护文件编辑


适合：.env、锁文件、迁移脚本、生产配置等。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Editing this file is blocked by project policy."
  }
}


官方 hooks guide 就给了在 PreToolUse 上阻止受保护文件编辑的模式。Claude


1.3 允许但补充上下文


适合：编辑高风险文件，但想提醒 Claude 额外注意。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Edit allowed.",
    "additionalContext": "This file affects deployment behavior. Prefer minimal edits and re-check local validation after writing."
  }
}


PreToolUse 支持 additionalContext。Claude


1.4 修改输入后放行


适合：强制把某类写操作重定向、标准化、包装。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Input normalized by hook.",
    "updatedInput": {
      "file_path": "src/safe_target.ts"
    },
    "additionalContext": "The original path was rewritten to a safe target by project policy."
  }
}


官方文档说明 PreToolUse 支持 updatedInput。Claude



2. PreToolUse(Bash) 模板


2.1 放行普通 Bash


适合：只读命令、轻量校验命令。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Command is allowed."
  }
}


2.2 阻断危险命令


适合：rm -rf、数据库写入、生产环境命令等。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive Bash command blocked by policy."
  }
}


官方 agent-sdk hooks 文档明确把“在执行前阻止危险操作”列为 hooks 的典型用途。Claude


2.3 处于 EDIT_REJECTED_HARD 时阻断 build/test


适合：你前面设计的状态机。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Current edit is EDIT_REJECTED_HARD. Fix blocking local diagnostics before running build/test.",
    "additionalContext": "Allowed next tools: Read, Edit, Write, LSP. Disallowed now: broad build, broad tests, submit."
  }
}


2.4 中间态允许最小验证，不允许 broad build


适合：SOFT_INCOMPLETE 时只允许 changed-files 级验证。


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Limited Bash verification allowed during expected incomplete state.",
    "additionalContext": "Only run the smallest relevant changed-files or targeted verification. Do not run broad build or submit yet."
  }
}



3. PostToolUse(Edit) 模板


PostToolUse 常用于“编辑后自动处理”，官方 guide 给过 Edit|Write 后自动跑 Prettier 的例子。Claude


3.1 本地验证通过


适合：局部硬门通过。


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "STATE: EDIT_ACCEPTED_LOCAL\nLocal hard-gate validation passed. You may continue the next minimal related edit or run the smallest relevant verification."
  }
}


3.2 硬拒绝：局部状态坏了


适合：syntax/parser/文件损坏/明显本地 blocker。


{
  "decision": "block",
  "reason": "Hard reject: local validation failed after edit.",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "STATE: EDIT_REJECTED_HARD\nFix the blocking local diagnostics before any build/test/submit. Allowed next tools: Read, Edit, Write, LSP."
  }
}


对 PostToolUse，顶层 decision: "block" 和 reason 是合法用法，additionalContext 可继续补充信息。Claude


3.3 预期中间态：允许继续相关迁移


适合：跨文件类型迁移、接口替换、调用链收敛。


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "STATE: EDIT_INCOMPLETE_EXPECTED\nThe current edit is locally healthy, but related files still require migration updates. Continue the related edit sequence. Do not submit yet."
  }
}


3.4 修改 MCP 工具输出后再给 Claude


适合：你用 MCP 工具做本地 validate，想把原始输出转成更适合 Claude 的摘要。


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedMCPToolOutput": {
      "content": [
        {
          "type": "text",
          "text": "Local validation summary: 1 blocking parser error in src/foo.ts"
        }
      ]
    },
    "additionalContext": "STATE: EDIT_REJECTED_HARD\nRepair the parser error first."
  }
}


官方文档说明 PostToolUse 支持 updatedMCPToolOutput。Claude



4. PostToolUseFailure 模板


4.1 工具失败，但这是可恢复的


适合：临时失败、可重试、预期中的中间态。


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "The tool failed, but this is recoverable. Check whether the failure is due to an expected intermediate migration state before changing strategy."
  }
}


官方文档说明 PostToolUseFailure 可通过 additionalContext 给 Claude 补充失败后的解释。Claude


4.2 工具失败，建议最小修复路径


适合：局部命令失败但不该导致任务漂移。


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "The previous operation failed. Prefer the smallest corrective action: inspect the active file, check local diagnostics, then retry the minimal edit."
  }
}


4.3 工具失败，应停止整个流程


适合：严重状态损坏、上下文失真、不可恢复。


{
  "continue": false,
  "stopReason": "The previous tool failure left the workspace in an unsafe state. Stop and repair manually before continuing."
}


continue: false 会让 Claude Code 直接停止当前处理，而且优先级高于事件专属 decision。stopReason 给用户看，不给 Claude 看。Claude



5. 一个通用“空放行”模板


如果 hook 只是记录日志、不想改变行为，最简单就是：


{}


或者根本不输出 JSON，直接成功退出。官方文档说明，hook 可以可选地返回 decision；不返回专门控制字段时，就是默认继续。Claude+1



6. verdict 和 hook 的区别，以及它们怎么互补


这是最容易混淆的点。


6.1 hook 是“什么时候执行的机制”


hook 是生命周期里的触发点和处理器机制。
Claude Code 会在特定事件触发时运行你配置的 shell 命令、HTTP endpoint 或 prompt hook，比如：


SessionStart

UserPromptSubmit

PreToolUse

PostToolUse

PostToolUseFailure。Claude


所以 hook 回答的是：

“什么时候、在哪个事件点运行你的逻辑？”


6.2 verdict 是“运行完之后给出的裁决结果”


verdict 是 hook 处理完输入后，通过 stdout 返回的 JSON 控制结果。
它回答的是：

“这次事件该继续、阻断、补充什么上下文、是否修改输入输出？” Claude


6.3 二者的关系


可以把它们理解成：


hook = 时机 + 执行器

verdict = 执行器的返回裁决


更具体地说：


没有 hook，就没有事件点去运行你的规则

没有 verdict，hook 也可以做副作用动作，但很难精确控制 Claude 后续行为

二者结合后，你才能做出真正的 deterministic control。官方 guide 也强调 hooks 的价值就在于给 Claude Code 提供确定性控制，而不是依赖 LLM 自己选择去做。Claude+1



6.4 它们怎么互补


最实用的理解方式是：


hook 负责“拦住正确的时机”


比如：


PreToolUse(Edit)：在编辑前检查路径是否受保护

PostToolUse(Edit)：在编辑后跑本地验证

PreToolUse(Bash)：在 build/test 前看当前状态是否允许


verdict 负责“在这个时机做出明确裁决”


比如：


allow

deny / block

stop

注入 additionalContext

修改 updatedInput

修改 updatedMCPToolOutput


所以：

hook 决定“你什么时候能管”，verdict 决定“你管了以后怎么判”。


6.5 用你前面的状态机场景举例


如果你做 lint rejected edit：


PostToolUse(Edit) 是 hook

它跑完 local validate 后输出：
EDIT_REJECTED_HARD

或 EDIT_INCOMPLETE_EXPECTED

或 EDIT_ACCEPTED_LOCAL


这个输出 JSON，就是 verdict。


接着：


PreToolUse(Bash) 是另一个 hook

它读取当前状态文件后，决定：
deny broad build

allow targeted check

或放行 submit candidate path


这里给 Claude Code 的 JSON 返回，又是新的 verdict。



6.6 一句话总结


hook 是生命周期里的“执行点”，verdict 是 hook 在这个执行点上给出的“裁决结果”。
hook 解决的是“何时介入”，verdict 解决的是“介入后怎么控制 Claude 的后续行为”。两者一起，才能把规则、验证和状态机真正落成可执行系统。Claude+1


如果你愿意，我下一条可以直接给你一套 “支持 HARD_REJECT / SOFT_INCOMPLETE / ACCEPTED 的完整 hook verdict JSON 模板库”，按你前面的状态机字段统一成一个风格。



Sources:


Hooks reference - Claude Code Docs
