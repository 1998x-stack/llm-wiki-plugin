# hook verdict 长什么样

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:28:37

## Question

hook verdict 长什么样

## Answer

我去对一下 Claude Code hooks 官方文档里的返回格式和字段，再给你一个“官方能用 + 工程上好用”的 verdict 结构。

浏览官方文档获取Claude Code相关信息


Hooks 参考 - Claude Code Docs
用了这套配置，Claude Code 终于不用我反复交代背景了 ...
Claude Code settings.json 详解（三）：hooks 钩子全解析


查找官方文档和相关字段信息


Hooks reference - Claude Code Docs


简洁地回答并提供引用


我需要将答案简化，并确保所有事实都有互联网引用。可以提到“hook”作为一个非正式术语，并建议使用JSON输出。也许可以通过提供通用和具体的例子来说明，重点提到顶层字段“hookSpecificOutput”及其与事件的变化关联，同时确保控制选项和JSON输出的布局。


提供精确JSON输出示例和控制选项


Hooks reference - Claude Code Docs


已思考 20s

严格说，hook verdict 没有一个单一固定长相。
它是 hook 写到 stdout 的 JSON 输出，其中有一组所有事件通用的顶层字段，再加上一组按事件变化的 hookSpecificOutput 字段。Claude Code 官方把这叫做 JSON output / decision control，而不是单独的“verdict”术语。Claude+2Claude+2


最通用的骨架长这样：


{
  "continue": true,
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}


这里面并不是每个字段都要同时出现。continue、stopReason、suppressOutput、systemMessage 是通用顶层控制字段；而 decision / reason 只适用于一部分事件；hookSpecificOutput 里再放事件专属字段。Claude+1



1. 通用顶层字段长什么样


Claude Code 官方文档给出的通用 JSON 输出字段主要有：


{
  "continue": true,
  "stopReason": "optional message",
  "suppressOutput": false,
  "systemMessage": "optional warning"
}


含义是：


continue: false：让 Claude 整个停止继续处理，而且它优先级高于事件专属 decision。

stopReason：当 continue: false 时，展示给用户的停止原因，不展示给 Claude。

suppressOutput: true：不把 stdout 记进 debug log。

systemMessage：给用户的警告信息。 Claude+1


一个最小的“全局停止” verdict 例子：


{
  "continue": false,
  "stopReason": "Build failed, fix errors before continuing"
}


这是官方文档直接给出的模式。Claude+1



2. 适用于很多事件的“顶层 block verdict”


对 UserPromptSubmit、PostToolUse、PostToolUseFailure、Stop、SubagentStop、ConfigChange、PreCompact 这些事件，常见 verdict 是顶层：


{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}


这里：


decision 目前只有 "block" 这个值

reason 是给 Claude 看的解释

如果你不返回 decision，或者直接 exit 0 且不输出 JSON，就表示放行。 Claude+1



3. PreToolUse 的 verdict 长什么样


PreToolUse 比较特殊。官方明确说：它现在应该用 hookSpecificOutput.permissionDecision，而不是旧的顶层 decision / reason。 Claude


标准形状是：


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed"
  }
}


permissionDecision 常见值包括：


allow

deny

ask

defer


而且你还可以附带：


updatedInput

additionalContext。Claude+1


更完整一点的例子：


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Validated by local policy",
    "updatedInput": {
      "command": "npm run lint"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}


这是官方文档里给出的完整模式之一。Claude



4. PostToolUse 的 verdict 长什么样


PostToolUse 常见有两类：


放行并补充上下文


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Local validation passed. You may proceed with targeted verification."
  }
}


阻断并补充上下文


{
  "decision": "block",
  "reason": "Blocking diagnostics detected",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Fix the local validation errors before running build/test/submit."
  }
}


官方文档对 PostToolUse 明确列了可用字段：


顶层 decision

顶层 reason

hookSpecificOutput.additionalContext

以及 MCP 工具场景下的 updatedMCPToolOutput。Claude



5. PostToolUseFailure 的 verdict 长什么样


它最常见的是给 Claude 附加失败解释：


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "The failure is expected during migration. Continue updating related call sites."
  }
}


官方说明里，PostToolUseFailure 可以在工具失败后给 Claude 补充上下文。Claude



6. PermissionDenied 的 verdict 长什么样


这个事件可以告诉模型“你可以重试一次”：


{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}


这是官方直接给出的例子。Claude



7. 工程上最好怎么理解它


所以你可以把 hook verdict 记成这条规则：

通用顶层字段控制“是否整体继续”，事件专属字段控制“这个事件该怎么处理”。 Claude+1

最常用的几种形状其实就 4 类：


A. 什么都不做，直接放行


{}


或者根本不输出 JSON，直接 exit 0。Claude


B. 全局停止


{
  "continue": false,
  "stopReason": "Build failed, fix errors before continuing"
}


Claude+1


C. 事件级阻断


{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}


Claude+1


D. 事件级专属控制


{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}


Claude+1



8. 针对你前面做状态机的场景，推荐 verdict 长这样


如果你要做 lint rejected edit / soft incomplete / accepted 这类状态机，我建议你的 hook verdict 在官方字段之外，把状态信息放进 additionalContext，或者你自己的状态文件里；然后用官方支持的字段真正控制 Claude。一个比较稳的 PostToolUse(Edit) verdict 可以写成：


{
  "decision": "block",
  "reason": "Hard reject: local validation failed",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "STATE: EDIT_REJECTED_HARD\nFix syntax/parser/local blocking diagnostics before any build/test."
  }
}


或者如果只是中间态，不阻断，只提示：


{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "STATE: EDIT_INCOMPLETE_EXPECTED\nThe local edit is healthy, but related call sites still need migration. Continue the related edits; do not submit yet."
  }
}


因为从官方能力边界看，真正能被 Claude Code 识别并执行的控制字段还是这些：


continue

stopReason

decision

reason

hookSpecificOutput.* 的事件专属字段。Claude+3Claude+3Claude+3


如果你要，我下一条可以直接给你一份 “所有常用 hook verdict 模板库”，包括 PreToolUse(Edit)、PreToolUse(Bash)、PostToolUse(Edit)、PostToolUseFailure 四套。



Sources:


Hooks reference - Claude Code Docs
