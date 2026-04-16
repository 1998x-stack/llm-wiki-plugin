# 一份 可直接落地的 CLAUDE.md + hooks 模板

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 10:57:01

## Question

一份 可直接落地的 CLAUDE.md + hooks 模板

## Answer

Determining whether to use web search for template-related answer


用户询问的是模板问题，无需特定公司信息。尽管可以利用文件搜索，手头没有相关文档，且问法是关于通用模板而不是特定应用。若事实可能已更新，考虑使用网络搜索获取最新信息。


回答关于模板的通用问题


查找官方文档


我需要查找官方文档来确认具体细节。这样能确保我提供的信息是准确的，并且与最新的标准一致。如果有任何变化或更新，我也能及时拿到最新的资料。


搜索 Claude Code 官方文档


使用 hooks 自动化工作流 - Claude Code Docs


已思考 14s

下面给你一份可直接落地的模板，目标只有一个：

把 Edit/Write → 本地 validate → rejected/accepted → repair/retest 变成强约束闭环。

我分成三部分给你：


CLAUDE.md 模板：定义策略与状态机规则

.claude/settings.json 模板：用 hooks 强制触发

hooks 脚本模板：把 edit 后的 validate 结果结构化回灌给 Claude


这样分层是因为 Claude Code 官方能力本来就是这样分工的：CLAUDE.md 是会话启动时加载的项目规则；hooks 能在生命周期事件上自动执行，实现确定性控制；PostToolUse 能匹配 Edit|Write；而 LSP 会在每次文件编辑后自动报告类型错误和警告。Claude+2Claude+2



CLAUDE.md 模板


把下面内容放在项目根目录的 CLAUDE.md。


# Claude Code Working Rules

## Goal
Keep edits locally correct before broad verification.
Do not use build/test to compensate for a rejected local edit.

## State machine

### Task states
- TASK_INIT
- TASK_LOCALIZED
- TASK_EDITING
- TASK_LOCAL_VALIDATE
- TASK_EDIT_REJECTED
- TASK_EDIT_ACCEPTED
- TASK_TARGETED_VERIFY
- TASK_READY_FOR_SUBMIT
- TASK_COMPLETED

### Edit states
- EDIT_PROPOSED
- EDIT_VALIDATING
- EDIT_REJECTED
- EDIT_REPAIRING
- EDIT_ACCEPTED

## Core policy

1. After every Edit or Write, always treat the result as EDIT_PROPOSED.
2. Immediately inspect local validation feedback:
   - built-in LSP diagnostics
   - hook-produced validation result
3. If validation returns blocking diagnostics, the edit is EDIT_REJECTED.
4. When an edit is EDIT_REJECTED:
   - do not run broad build
   - do not run broad tests
   - do not submit
   - do not continue unrelated edits
   - only use Read, Edit, Write, and LSP until the blocking diagnostics are resolved
5. Only when local validation passes should the edit become EDIT_ACCEPTED.
6. After EDIT_ACCEPTED:
   - continue with the next minimal edit, or
   - run the smallest relevant verification
7. Prefer targeted verification over broad verification.
8. Multi-file tasks should converge file-by-file, then run changed-files verification, then targeted tests.
9. If local validation and targeted verification both pass, the task may enter TASK_READY_FOR_SUBMIT.

## Validation policy

### Blocking diagnostics
Treat these as blockers:
- syntax errors
- parser failures
- unresolved imports/symbols caused by the current edit
- type errors caused by the current edit
- project-configured hard lint failures

### Non-blocking diagnostics
These should be fixed, but do not force immediate rejection unless the hook says so:
- formatting issues
- style-only warnings
- existing pre-existing non-critical warnings outside the edited scope

## Repair loop policy

When an edit is rejected:
1. Read the structured validation output carefully.
2. Fix only the blocking diagnostics first.
3. Re-run local validation through the normal edit flow.
4. Do not escalate to build/test until the edit is accepted.

## Verification policy

Use the smallest relevant verification first:
1. local validation
2. changed-files validation
3. targeted tests
4. broader verification only when necessary

## Output behavior

When reporting progress:
- explicitly mention the current task state
- explicitly mention whether the current edit is accepted or rejected
- if rejected, explain the blocking diagnostic and the minimal repair plan


这个文件的作用是：把“Claude 应该怎么做”写成持续生效的项目规则。Claude Code 官方说明 CLAUDE.md 会在每个 session 开始时读取，适合放 coding standards、architecture decisions、review checklists 这类长期规则。Claude



.claude/settings.json 模板


这个模板做三件事：


PostToolUse(Edit|Write) 后自动跑本地 validate

PreToolUse(Bash) 在 edit 被 reject 时，阻止 build/test/submit 类命令

用 SessionStart 提醒 Claude 当前项目启用了“先 local validate，再 broader verify”的规则


把下面内容放在项目根目录的 .claude/settings.json。


{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[STATE_MACHINE] This project enforces local validation after every Edit/Write. Blocking local diagnostics must be fixed before broad build/test/submit.'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-edit-validate.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-bash-guard.sh"
          }
        ]
      }
    ]
  }
}


为什么这么配：


Claude Code 官方的 hooks 支持在生命周期特定点自动运行，提供确定性控制，避免只靠模型自己记住规则。Claude+1

官方示例明确展示了 PostToolUse 配 Edit|Write 的模式。Claude+1



post-edit-validate.sh 模板


路径：.claude/hooks/post-edit-validate.sh


这个脚本的职责是：


读取 Claude Code 传入的 hook JSON

找到刚刚被修改的文件

对该文件做本地验证

产出结构化 verdict

保存一个状态文件，供后续 PreToolUse(Bash) 判断是否允许 build/test


下面是一个语言无关、可直接改造的 Bash 模板。
我先用通用逻辑写，你再按项目技术栈替换其中的验证命令。


#!/usr/bin/env bash
set -euo pipefail

INPUT_JSON="$(cat)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
STATE_DIR="$PROJECT_DIR/.claude/state"
STATE_FILE="$STATE_DIR/edit-validation-state.json"

mkdir -p "$STATE_DIR"

# 依赖 jq
FILE_PATH="$(printf '%s' "$INPUT_JSON" | jq -r '.tool_input.file_path // empty')"
TOOL_NAME="$(printf '%s' "$INPUT_JSON" | jq -r '.tool_name // empty')"

if [ -z "$FILE_PATH" ]; then
  cat <<'JSON'
{
  "continue": true,
  "additionalContext": "[local-validate] No file_path found in hook input; skipping validation."
}
JSON
  exit 0
fi

ABS_FILE="$PROJECT_DIR/$FILE_PATH"
if [ ! -f "$ABS_FILE" ]; then
  cat <<JSON
{
  "continue": true,
  "additionalContext": "[local-validate] File not found after $TOOL_NAME: $FILE_PATH"
}
JSON
  exit 0
fi

BLOCKING=false
SUMMARY=""
DETAILS=""

EXT="${FILE_PATH##*.}"

run_python_checks() {
  local file="$1"
  local syntax_out=""
  local lint_out=""

  if ! syntax_out="$(python -m py_compile "$file" 2>&1)"; then
    BLOCKING=true
    SUMMARY="${SUMMARY}\n- Python syntax check failed"
    DETAILS="${DETAILS}\n[py_compile]\n${syntax_out}\n"
  fi

  if command -v ruff >/dev/null 2>&1; then
    # 可按项目需要替换为更严格/更轻量的规则
    if ! lint_out="$(ruff check "$file" 2>&1)"; then
      BLOCKING=true
      SUMMARY="${SUMMARY}\n- Ruff check failed"
      DETAILS="${DETAILS}\n[ruff]\n${lint_out}\n"
    fi
  fi
}

run_js_ts_checks() {
  local file="$1"
  local lint_out=""

  if command -v eslint >/dev/null 2>&1; then
    if ! lint_out="$(eslint "$file" 2>&1)"; then
      BLOCKING=true
      SUMMARY="${SUMMARY}\n- ESLint failed"
      DETAILS="${DETAILS}\n[eslint]\n${lint_out}\n"
    fi
  fi

  # 可选：若项目有独立的单文件 typecheck wrapper，可以在这里调用
  # 例如：pnpm exec tsc-files --noEmit "$file"
}

run_go_checks() {
  local file="$1"
  local vet_out=""

  if command -v golangci-lint >/dev/null 2>&1; then
    if ! vet_out="$(golangci-lint run "$file" 2>&1)"; then
      BLOCKING=true
      SUMMARY="${SUMMARY}\n- golangci-lint failed"
      DETAILS="${DETAILS}\n[golangci-lint]\n${vet_out}\n"
    fi
  fi
}

case "$EXT" in
  py)
    run_python_checks "$ABS_FILE"
    ;;
  js|jsx|ts|tsx)
    run_js_ts_checks "$ABS_FILE"
    ;;
  go)
    run_go_checks "$ABS_FILE"
    ;;
  *)
    SUMMARY="${SUMMARY}\n- No language-specific local validator configured for .$EXT"
    ;;
esac

if [ "$BLOCKING" = true ]; then
  cat > "$STATE_FILE" <<JSON
{
  "task_state": "TASK_EDIT_REJECTED",
  "edit_state": "EDIT_REJECTED",
  "verification_state": "VERIFY_LOCAL",
  "blocking": true,
  "file": "$FILE_PATH",
  "last_tool": "$TOOL_NAME"
}
JSON

  cat <<JSON
{
  "continue": true,
  "additionalContext": "[local-validate] EDIT_REJECTED for $FILE_PATH\nBlocking diagnostics detected. Fix the local validation errors before running broad build/test/submit.\nSummary:${SUMMARY}\nDetails:${DETAILS}\nAllowed next tools: Read, Edit, Write, LSP\nDisallowed next actions: broad build, broad tests, submit"
}
JSON
else
  cat > "$STATE_FILE" <<JSON
{
  "task_state": "TASK_EDIT_ACCEPTED",
  "edit_state": "EDIT_ACCEPTED",
  "verification_state": "VERIFY_LOCAL",
  "blocking": false,
  "file": "$FILE_PATH",
  "last_tool": "$TOOL_NAME"
}
JSON

  cat <<JSON
{
  "continue": true,
  "additionalContext": "[local-validate] EDIT_ACCEPTED for $FILE_PATH\nLocal validation passed. You may proceed with the next minimal edit or the smallest relevant verification."
}
JSON
fi


这个脚本为什么这样设计：


hooks 会把 JSON 上下文传给命令处理器。官方 hooks 参考明确说了，事件触发时 Claude Code 会把 JSON context 传给 hook。Claude+1

PostToolUse(Edit|Write) 是官方推荐的自动化点之一，官方示例就是在 edit 后自动格式化。我们这里把它换成自动 validate。Claude+1

additionalContext 可以把结构化结果回灌给 Claude，让它进入 repair loop，而不是自己“脑补接下来怎么办”。这是 hooks 作为 deterministic control 的核心价值。Claude+1



pre-bash-guard.sh 模板


路径：.claude/hooks/pre-bash-guard.sh


这个脚本的职责是：


在 Claude 尝试执行 Bash 前检查最近一次 edit 是否仍然是 EDIT_REJECTED

如果是，并且当前 Bash 看起来像 build/test/submit 类命令，就直接阻止


这样可以直接解决你图里的问题：
edit 已被拒绝，却还想继续 build。


#!/usr/bin/env bash
set -euo pipefail

INPUT_JSON="$(cat)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
STATE_FILE="$PROJECT_DIR/.claude/state/edit-validation-state.json"

COMMAND="$(printf '%s' "$INPUT_JSON" | jq -r '.tool_input.command // empty')"

if [ ! -f "$STATE_FILE" ]; then
  cat <<'JSON'
{
  "continue": true
}
JSON
  exit 0
fi

EDIT_STATE="$(jq -r '.edit_state // empty' "$STATE_FILE")"
BLOCKING="$(jq -r '.blocking // false' "$STATE_FILE")"
FILE_PATH="$(jq -r '.file // empty' "$STATE_FILE")"

if [ "$EDIT_STATE" = "EDIT_REJECTED" ] && [ "$BLOCKING" = "true" ]; then
  if printf '%s' "$COMMAND" | grep -Eiq '(^| )(npm|pnpm|yarn|bun|pytest|go test|cargo test|mvn test|gradle test|make|tsc|vite build|next build|webpack|turbo|bazel|just)( |$)'; then
    cat <<JSON
{
  "continue": false,
  "stopReason": "Blocked by state machine: current edit is EDIT_REJECTED for $FILE_PATH. Fix blocking local diagnostics before running build/test."
}
JSON
    exit 0
  fi
fi

cat <<'JSON'
{
  "continue": true
}
JSON


为什么要这样做：


官方 hooks 参考里，PreToolUse 就是工具执行前的事件点。Claude+1

用它来拦截 build/test 是最自然的，因为“是否允许继续”本身就是状态机控制逻辑，不应该只靠 Claude 记住。Claude



目录结构建议


最终目录建议长这样：


project-root/
  CLAUDE.md
  .claude/
    settings.json
    hooks/
      post-edit-validate.sh
      pre-bash-guard.sh
    state/
      edit-validation-state.json



你还需要替换的地方


上面模板是可落地的骨架，但你最好按语言栈替换本地 validate 命令：


Python 项目


建议保留：


python -m py_compile

ruff check <file>

可选：mypy <file> 或项目内单文件 typecheck wrapper


TS/JS 项目


建议至少：


eslint <file>

可选：项目自定义的单文件 typecheck wrapper
因为原生 tsc 常常更偏全项目，不适合每次 edit 后都跑


Go 项目


建议：


golangci-lint run

或项目已有的轻量 wrapper


Rust 项目


建议：


cargo check --quiet 不适合每次 edit 后全量跑

更好的做法是做 changed-files / package-level wrapper


核心原则别变：

每次 edit 后先跑最小本地验证。不要一上来全量。

这也符合 Claude Code hooks 设计的定位：自动化重复任务、强制项目规则，而不是把所有决策都交给模型。Claude+1



这套模板最终实现了什么


它会把你的流程强制变成：


Claude Edit/Write

自动触发本地 validate

validate 结果写入状态文件，并回灌给 Claude

如果 EDIT_REJECTED，Claude 只能 repair

如果 Claude 想偷跑 build/test，PreToolUse(Bash) 直接拦截

只有 EDIT_ACCEPTED 才能进入 targeted verification


也就是把你一直想要的：


lint rejected edit → 重新设计 repair loop


真正落到了 Claude Code 的能力边界里，而不是只写一句规则希望它记住。hooks 的官方定位就是“deterministic control”，而不是依赖 LLM 自己选择去做。Claude+1



一个最小增强建议


如果你准备进一步升级，我建议下一步加两件事：


第一，把 post-edit-validate.sh 的输出做成真正 JSON 化诊断，而不是把 details 拼在文本里。
第二，把 LSP 诊断也并入 verdict。Claude Code 官方说明 LSP 会在每次编辑后自动报告类型错误和警告，所以你可以把它视为第一层快速诊断源，再让 hook 补充 lint/parser/project policy。Claude+1


要的话，我下一条可以直接给你一版：


“TypeScript 项目专用的 CLAUDE.md + hooks 模板”
或者
“Python 项目专用的 CLAUDE.md + hooks 模板”。



Sources:


Claude Code overview - Claude Code Docs
