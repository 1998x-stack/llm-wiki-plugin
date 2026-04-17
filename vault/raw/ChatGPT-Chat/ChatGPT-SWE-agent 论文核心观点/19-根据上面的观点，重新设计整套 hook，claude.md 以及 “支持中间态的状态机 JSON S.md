# 根据上面的观点，重新设计整套 hook，claude.md 以及 “支持中间态的状态机 JSON Schema 升级版”

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:19:40

## Question

根据上面的观点，重新设计整套 hook，claude.md 以及 “支持中间态的状态机 JSON Schema 升级版”

## Answer

我把方案重构成“可直接落地”的三件套：规则层、执行层、状态层。重点会把“中间态”正式纳入，不再把所有局部验证失败都当成硬拒绝。

已思考 10s

下面我给你一套重新设计后的完整方案，核心原则只有两条：


第一，不把所有 edit 后的验证失败都当成硬拒绝。
第二，把“中间态”正式编码进状态机、hook 和 CLAUDE.md。


也就是把原来粗糙的：


accepted

rejected


升级成至少三类：


HARD_REJECT：当前 edit 把局部状态写坏了，必须立刻修

SOFT_INCOMPLETE：当前 edit 局部健康，但任务级迁移还没完成

ACCEPTED：当前 edit 及当前阶段都达标，可以继续推进


这会直接解决你提的关键问题：
跨文件类型迁移、接口替换、调用链收敛时，中间几步不该被系统误杀。



一、整套新设计的总体结构


我建议把系统分成三层：


1. CLAUDE.md


负责策略、优先级、工作规则。


它告诉 Claude：


什么时候只做局部健康检查

什么时候允许带着中间态继续

什么时候必须停下来修

什么时候才能 build/test/submit


2. hooks


负责自动执行、结构化判断、阻断与放行。


它做三件事：


PostToolUse(Edit|Write) 后跑局部验证

必要时把状态标成 EDIT_REJECTED_HARD 或 EDIT_INCOMPLETE_EXPECTED

PreToolUse(Bash|Submit) 时根据状态决定是否阻断


3. 状态机 JSON Schema


负责把系统当前状态表示清楚。


明确记录：


task_state

edit_state

verification_state

diagnostics

是否阻断

是否属于预期中间态

下一步允许什么工具



二、重新设计后的状态定义


1. Task State


TASK_INIT
TASK_LOCALIZED
TASK_EDITING
TASK_LOCAL_VALIDATE
TASK_BATCH_VALIDATE
TASK_EDIT_REJECTED_HARD
TASK_EDIT_INCOMPLETE
TASK_EDIT_ACCEPTED
TASK_TARGETED_VERIFY
TASK_READY_FOR_SUBMIT
TASK_COMPLETED
TASK_BLOCKED


2. Edit State


EDIT_NONE
EDIT_PROPOSED
EDIT_VALIDATING_LOCAL
EDIT_REJECTED_HARD
EDIT_REPAIRING
EDIT_ACCEPTED_LOCAL
EDIT_INCOMPLETE_EXPECTED
EDIT_ACCEPTED_STAGE
EDIT_READY_FOR_SUBMIT


3. Verification State


VERIFY_NONE
VERIFY_LSP_ONLY
VERIFY_LOCAL_HARD_GATE
VERIFY_BATCH_CHANGED_FILES
VERIFY_TARGETED_TESTS
VERIFY_BROAD



三、重新设计后的判定逻辑


A. 每次 Edit/Write 后：只做“局部硬门”


这一步的目标不是判断任务完成没完成，而是判断：

当前 edit 有没有把局部状态写坏。

这一步只拦以下情况


syntax error

parser failure

文件损坏

明显不可解析 AST

明显局部 blocker（比如本文件直接炸掉的类型错误）

policy 定义的高优先级硬错误


结果只有两种


EDIT_REJECTED_HARD

EDIT_ACCEPTED_LOCAL


也就是说：


每次 edit 后，不要直接因为“跨文件还没改完”就硬拒绝。



B. End Turn / End Batch：判断是否是“预期中间态”


这一步的目标是判断：

当前虽然局部健康，但整个修改链是不是还没收敛。

这一步适合检查：


changed-files typecheck

changed-files lint

相关调用链是否仍有预期中的错误

这些错误是不是“合理未完成迁移”


结果分三种


EDIT_REJECTED_HARD

EDIT_INCOMPLETE_EXPECTED

EDIT_ACCEPTED_STAGE


这一步是整套方案的关键。
因为它把“局部没坏，但任务还没做完”独立成了一个正式状态。



C. Submit 前：严格验证


这一步才去做：


targeted tests

更严格的 changed-files 验证

必要时 broader verify


结果分两种


EDIT_READY_FOR_SUBMIT

NEEDS_MORE_WORK



四、重新设计后的 CLAUDE.md


下面这份可以直接用。


# Claude Code Working Rules

## Core principle
Do not treat every post-edit validation failure as a hard rejection.

There are three important outcomes after edits:
1. HARD_REJECT: the current edit made the local state invalid and must be repaired immediately.
2. SOFT_INCOMPLETE: the current edit is locally healthy, but the broader migration/change is not finished yet.
3. ACCEPTED: the current edit and current stage are valid enough to move forward.

## State model

### Task states
- TASK_INIT
- TASK_LOCALIZED
- TASK_EDITING
- TASK_LOCAL_VALIDATE
- TASK_BATCH_VALIDATE
- TASK_EDIT_REJECTED_HARD
- TASK_EDIT_INCOMPLETE
- TASK_EDIT_ACCEPTED
- TASK_TARGETED_VERIFY
- TASK_READY_FOR_SUBMIT
- TASK_COMPLETED
- TASK_BLOCKED

### Edit states
- EDIT_NONE
- EDIT_PROPOSED
- EDIT_VALIDATING_LOCAL
- EDIT_REJECTED_HARD
- EDIT_REPAIRING
- EDIT_ACCEPTED_LOCAL
- EDIT_INCOMPLETE_EXPECTED
- EDIT_ACCEPTED_STAGE
- EDIT_READY_FOR_SUBMIT

## Required behavior

### After every Edit or Write
Treat the edit as EDIT_PROPOSED, then immediately inspect local validation.

### Local validation purpose
Local validation only decides whether the current edit has broken the local state.
It is not the final decision about whether the whole task is complete.

### HARD_REJECT conditions
Treat as HARD_REJECT if the edit causes:
- syntax errors
- parser failures
- file corruption
- invalid code structure
- blocking local diagnostics that make the current file/state unusable

When in EDIT_REJECTED_HARD:
- only use Read, Edit, Write, and LSP
- do not run broad build
- do not run broad tests
- do not submit
- do not continue unrelated edits

### SOFT_INCOMPLETE conditions
Treat as SOFT_INCOMPLETE if:
- the edit is locally healthy
- but changed-files or task-level checks show expected unfinished migration work
- for example: type or interface migration where more call sites still need updates

When in EDIT_INCOMPLETE_EXPECTED:
- continue the planned migration/edit sequence
- prefer the next smallest related edit
- do not submit
- do not treat this as a repair failure

### ACCEPTED conditions
Treat as ACCEPTED if:
- local validation passes
- and the current stage/batch has no blocking unresolved work

### Verification policy
Use verification in layers:
1. local hard gate after each edit
2. batch/changed-files validation at end of turn or end of a related edit batch
3. targeted verification before submit
4. broad verification only if necessary

### Tool policy
If the current state is EDIT_REJECTED_HARD:
- allowed tools: Read, Edit, Write, LSP
- disallowed tools: broad Bash build/test, Submit

If the current state is EDIT_INCOMPLETE_EXPECTED:
- allowed tools: Read, Edit, Write, LSP, limited Bash for changed-files checks
- disallowed tools: Submit

If the current state is EDIT_ACCEPTED_STAGE:
- allowed tools: Read, Edit, Write, LSP, Bash, Submit candidate path
- submit still requires targeted verification

## Progress reporting
When reporting progress, always mention:
- current task state
- current edit state
- whether the current status is HARD_REJECT, SOFT_INCOMPLETE, or ACCEPTED
- the smallest correct next action



五、重新设计后的 hooks 方案


这里我给你一套完整分层：


Hook 1：PostToolUse(Edit|Write)


职责：


运行局部硬门验证

输出：
EDIT_REJECTED_HARD

或 EDIT_ACCEPTED_LOCAL


不在这一层做的事


不在这里直接判断“整个迁移是否完成”

不把所有 typecheck 失败都当 hard reject



Hook 2：Stop/TurnEnd 或等价的“批次结束检查”


Claude Code 没有公开一个和 TurnEnd 完全同名、同语义的产品级 hook 给你像框架一样自由编排，所以工程上更实际的做法是：


通过第二个 hook 脚本 + 状态文件

在每次 Edit|Write 通过局部硬门后，记录 pending_batch_validation=true

下一次 Claude 试图执行 Bash 或准备扩大验证时，自动触发 batch validate


也就是说，batch validate 更适合在：


PreToolUse(Bash)

或某个自定义 run_batch_validate 命令


里被触发，而不是强求“每个 turn 末尾”一定有平台级事件。


它的职责


判断：


当前 changed-files 的错误是否属于预期中间态

是否进入：
EDIT_INCOMPLETE_EXPECTED

EDIT_ACCEPTED_STAGE

EDIT_REJECTED_HARD



Hook 3：PreToolUse(Bash)


职责：


当 Claude 想跑 Bash 时，先看当前状态

决定是：
直接放行

先做 batch validate

还是阻断


阻断规则


如果当前是 EDIT_REJECTED_HARD：


阻断 broad build/test

阻断 submit 前命令


如果当前是 EDIT_INCOMPLETE_EXPECTED：


允许最小必要的 changed-files check

不允许 submit

不建议 broad build



Hook 4：PreToolUse(Submit) 或等价提交保护


职责：


只有 EDIT_READY_FOR_SUBMIT 或 TASK_READY_FOR_SUBMIT 才允许提交

否则阻断并说明缺什么验证



六、hooks 的新状态流


新状态流如下：


每次 edit 后


EDIT_PROPOSED
→ EDIT_VALIDATING_LOCAL
→
如果本地坏了：EDIT_REJECTED_HARD
如果本地健康：EDIT_ACCEPTED_LOCAL


批次检查后


EDIT_ACCEPTED_LOCAL
→
如果仍有预期迁移未完成：EDIT_INCOMPLETE_EXPECTED
如果当前批次已收敛：EDIT_ACCEPTED_STAGE


submit 前


EDIT_ACCEPTED_STAGE
→ targeted verify
→
通过：EDIT_READY_FOR_SUBMIT
失败：EDIT_INCOMPLETE_EXPECTED 或 EDIT_REJECTED_HARD



七、支持中间态的状态机 JSON Schema 升级版


下面是升级后的 schema。你可以直接拿去做状态文件、hook verdict 或运行时 schema。


{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/claude-code-state-machine-v2.schema.json",
  "title": "Claude Code Agent State Machine V2",
  "type": "object",
  "required": [
    "schema_version",
    "task",
    "current",
    "policy",
    "allowed_transitions"
  ],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "2.0"
    },
    "task": {
      "type": "object",
      "required": ["task_id", "goal", "task_state"],
      "properties": {
        "task_id": { "type": "string" },
        "goal": { "type": "string" },
        "task_state": {
          "type": "string",
          "enum": [
            "TASK_INIT",
            "TASK_LOCALIZED",
            "TASK_EDITING",
            "TASK_LOCAL_VALIDATE",
            "TASK_BATCH_VALIDATE",
            "TASK_EDIT_REJECTED_HARD",
            "TASK_EDIT_INCOMPLETE",
            "TASK_EDIT_ACCEPTED",
            "TASK_TARGETED_VERIFY",
            "TASK_READY_FOR_SUBMIT",
            "TASK_COMPLETED",
            "TASK_BLOCKED"
          ]
        },
        "summary": { "type": "string" },
        "changed_files": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "related_tests": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "migration_mode": {
          "type": "boolean",
          "default": false
        }
      }
    },
    "current": {
      "type": "object",
      "required": [
        "edit_state",
        "verification_state",
        "blocking",
        "status_class",
        "allowed_next_tools",
        "disallowed_next_tools"
      ],
      "properties": {
        "edit_state": {
          "type": "string",
          "enum": [
            "EDIT_NONE",
            "EDIT_PROPOSED",
            "EDIT_VALIDATING_LOCAL",
            "EDIT_REJECTED_HARD",
            "EDIT_REPAIRING",
            "EDIT_ACCEPTED_LOCAL",
            "EDIT_INCOMPLETE_EXPECTED",
            "EDIT_ACCEPTED_STAGE",
            "EDIT_READY_FOR_SUBMIT"
          ]
        },
        "verification_state": {
          "type": "string",
          "enum": [
            "VERIFY_NONE",
            "VERIFY_LSP_ONLY",
            "VERIFY_LOCAL_HARD_GATE",
            "VERIFY_BATCH_CHANGED_FILES",
            "VERIFY_TARGETED_TESTS",
            "VERIFY_BROAD"
          ]
        },
        "status_class": {
          "type": "string",
          "enum": [
            "HARD_REJECT",
            "SOFT_INCOMPLETE",
            "ACCEPTED"
          ]
        },
        "blocking": { "type": "boolean" },
        "reason": { "type": "string" },
        "repair_instruction": { "type": "string" },
        "active_file": {
          "type": ["string", "null"]
        },
        "changed_ranges": {
          "type": "array",
          "items": { "$ref": "#/$defs/range" },
          "default": []
        },
        "diagnostics": {
          "type": "array",
          "items": { "$ref": "#/$defs/diagnostic" },
          "default": []
        },
        "incomplete_reasons": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        },
        "allowed_next_tools": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["Read", "Edit", "Write", "LSP", "Bash", "Glob", "Grep", "Submit"]
          }
        },
        "disallowed_next_tools": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["Read", "Edit", "Write", "LSP", "Bash", "Glob", "Grep", "Submit"]
          }
        },
        "last_tool": {
          "type": ["string", "null"]
        },
        "last_tool_input": {
          "type": ["object", "null"]
        }
      }
    },
    "policy": {
      "type": "object",
      "required": [
        "require_local_validation_after_edit",
        "allow_expected_incomplete_between_related_edits",
        "block_build_on_hard_reject",
        "block_submit_unless_ready"
      ],
      "properties": {
        "require_local_validation_after_edit": {
          "type": "boolean",
          "default": true
        },
        "allow_expected_incomplete_between_related_edits": {
          "type": "boolean",
          "default": true
        },
        "block_build_on_hard_reject": {
          "type": "boolean",
          "default": true
        },
        "block_submit_unless_ready": {
          "type": "boolean",
          "default": true
        },
        "hard_reject_sources": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["lsp", "lint", "typecheck", "parser", "policy"]
          },
          "default": ["parser", "policy"]
        },
        "soft_incomplete_sources": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["lsp", "lint", "typecheck", "batch_validation"]
          },
          "default": ["lsp", "typecheck", "batch_validation"]
        }
      }
    },
    "allowed_transitions": {
      "type": "array",
      "items": { "$ref": "#/$defs/transition" }
    },
    "history": {
      "type": "array",
      "items": { "$ref": "#/$defs/history_entry" },
      "default": []
    }
  },
  "$defs": {
    "range": {
      "type": "object",
      "required": ["start_line", "end_line"],
      "properties": {
        "start_line": { "type": "integer", "minimum": 1 },
        "end_line": { "type": "integer", "minimum": 1 },
        "start_col": { "type": "integer", "minimum": 0 },
        "end_col": { "type": "integer", "minimum": 0 }
      }
    },
    "diagnostic": {
      "type": "object",
      "required": ["source", "severity", "message"],
      "properties": {
        "source": {
          "type": "string",
          "enum": ["lsp", "lint", "typecheck", "parser", "policy", "batch_validation"]
        },
        "severity": {
          "type": "string",
          "enum": ["info", "warning", "error"]
        },
        "code": {
          "type": ["string", "null"]
        },
        "message": {
          "type": "string"
        },
        "file": {
          "type": ["string", "null"]
        },
        "range": {
          "anyOf": [
            { "$ref": "#/$defs/range" },
            { "type": "null" }
          ]
        },
        "blocking": {
          "type": "boolean",
          "default": false
        },
        "newly_introduced": {
          "type": "boolean",
          "default": true
        },
        "expected_incomplete": {
          "type": "boolean",
          "default": false
        }
      }
    },
    "transition": {
      "type": "object",
      "required": ["from", "to", "when"],
      "properties": {
        "from": { "type": "string" },
        "to": { "type": "string" },
        "when": { "type": "string" },
        "action": {
          "type": ["string", "null"]
        }
      }
    },
    "history_entry": {
      "type": "object",
      "required": ["timestamp", "event", "from_state", "to_state"],
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time"
        },
        "event": { "type": "string" },
        "from_state": { "type": "string" },
        "to_state": { "type": "string" },
        "note": { "type": "string" }
      }
    }
  }
}



八、hooks 的实际新判定规则


PostToolUse(Edit|Write) 新规则


输出 1：HARD_REJECT


条件：


syntax error

parser failure

文件被写坏

当前文件无法工作


设置：


task_state = TASK_EDIT_REJECTED_HARD

edit_state = EDIT_REJECTED_HARD

status_class = HARD_REJECT

禁止 Bash/Submit


输出 2：ACCEPTED_LOCAL


条件：


本地硬门通过


设置：


task_state = TASK_LOCAL_VALIDATE

edit_state = EDIT_ACCEPTED_LOCAL

status_class = ACCEPTED


然后打标：


needs_batch_validation = true



PreToolUse(Bash) 新规则


当 Claude 要执行 Bash：


如果当前是 EDIT_REJECTED_HARD


直接阻断 broad build/test。


如果当前是 EDIT_ACCEPTED_LOCAL 且 needs_batch_validation = true


先自动做 batch validate：


如果结果是预期中间态


设置：


task_state = TASK_EDIT_INCOMPLETE

edit_state = EDIT_INCOMPLETE_EXPECTED

status_class = SOFT_INCOMPLETE


允许：


继续相关 edit

changed-files 级别检查


不允许：


submit


如果结果是阶段完成


设置：


task_state = TASK_EDIT_ACCEPTED

edit_state = EDIT_ACCEPTED_STAGE

status_class = ACCEPTED


允许：


targeted verify

后续 build/test



PreToolUse(Submit) 新规则


只有：


edit_state = EDIT_READY_FOR_SUBMIT

或 task_state = TASK_READY_FOR_SUBMIT


才允许提交。


否则阻断。



九、一份更推荐的状态实例


这是一个“预期中间态”的例子。


{
  "schema_version": "2.0",
  "task": {
    "task_id": "type-migration-001",
    "goal": "Migrate UserId from string to object form across related files",
    "task_state": "TASK_EDIT_INCOMPLETE",
    "summary": "Definition updated, some call sites still pending",
    "changed_files": ["src/types.ts", "src/service.ts"],
    "related_tests": ["tests/service.test.ts"],
    "migration_mode": true
  },
  "current": {
    "edit_state": "EDIT_INCOMPLETE_EXPECTED",
    "verification_state": "VERIFY_BATCH_CHANGED_FILES",
    "status_class": "SOFT_INCOMPLETE",
    "blocking": false,
    "reason": "Local edit is valid, but related call sites still need migration",
    "repair_instruction": "Continue updating the remaining affected call sites before targeted verification.",
    "active_file": "src/service.ts",
    "changed_ranges": [
      {
        "start_line": 12,
        "end_line": 20
      }
    ],
    "diagnostics": [
      {
        "source": "batch_validation",
        "severity": "error",
        "code": "TS2345",
        "message": "Argument of type 'string' is not assignable to parameter of type 'UserIdObject'.",
        "file": "src/controller.ts",
        "range": {
          "start_line": 44,
          "end_line": 44
        },
        "blocking": false,
        "newly_introduced": true,
        "expected_incomplete": true
      }
    ],
    "incomplete_reasons": [
      "Remaining call sites still use old UserId form",
      "Migration is in progress across related files"
    ],
    "allowed_next_tools": ["Read", "Edit", "Write", "LSP", "Bash"],
    "disallowed_next_tools": ["Submit"],
    "last_tool": "Edit",
    "last_tool_input": {
      "file_path": "src/service.ts"
    }
  },
  "policy": {
    "require_local_validation_after_edit": true,
    "allow_expected_incomplete_between_related_edits": true,
    "block_build_on_hard_reject": true,
    "block_submit_unless_ready": true,
    "hard_reject_sources": ["parser", "policy"],
    "soft_incomplete_sources": ["lsp", "typecheck", "batch_validation"]
  },
  "allowed_transitions": [
    {
      "from": "TASK_EDIT_INCOMPLETE",
      "to": "TASK_EDITING",
      "when": "agent continues related migration edits",
      "action": "continue_migration"
    },
    {
      "from": "TASK_EDIT_INCOMPLETE",
      "to": "TASK_TARGETED_VERIFY",
      "when": "all expected incomplete diagnostics are resolved",
      "action": "run_targeted_verification"
    }
  ],
  "history": []
}



十、最终推荐落地方式


如果你现在就要改造现有系统，我建议按这个顺序：


第一步


把 CLAUDE.md 改成上面的新版策略，明确三类结果：


HARD_REJECT

SOFT_INCOMPLETE

ACCEPTED


第二步


把 PostToolUse(Edit|Write) 改成只做局部硬门，不要直接把所有 type/lint 失败都判死刑。


第三步


在 PreToolUse(Bash) 加 batch validate，把：


EDIT_ACCEPTED_LOCAL
进一步分成：

EDIT_INCOMPLETE_EXPECTED

EDIT_ACCEPTED_STAGE


第四步


在 PreToolUse(Submit) 只允许 READY_FOR_SUBMIT 状态提交。



十一、一句话总结


重新设计后的整套系统，核心变化就是：

每次 edit 后只拦“坏状态”，不拦“合理中间态”；而 end-turn / batch-level 验证负责判断当前是不是仍处于预期中的未完成迁移。

也就是：


after-edit：防坏

batch-end：识别中间态

pre-submit：严格收口


这比“每次 edit 后都必须 lint/typecheck 全绿”的设计稳得多，也更符合真实跨文件修改的工作流。


如果你愿意，我下一条可以直接继续给你一份：
“新版 .claude/settings.json + 两个 hook 脚本的完整可运行模板”。
