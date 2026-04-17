# 一份 完整状态机 JSON Schema / YAML 配置草案

> Source: SWE-agent 论文核心观点
> Time: 2026/4/15 11:00:20

## Question

一份 完整状态机 JSON Schema / YAML 配置草案

## Answer

已思考 9s

下面给你一份 “完整状态机 JSON Schema + YAML 配置草案”。
目标不是追求完美通用，而是能直接拿来做 Claude Code 的 edit → validate → reject/accept → repair → targeted verify → submit 控制层。


我分成 4 部分：


状态机设计目标

JSON Schema 草案

YAML 配置草案

一个实际运行例子



1. 设计目标


这套状态机主要解决 4 个问题：


edit 后不能直接漂到 build/test

lint/typecheck/LSP 的结果要变成状态

rejected edit 必须进入 repair loop

多文件任务要能逐文件收敛，再进入更大范围验证


所以我们显式区分三层状态：


task_state：整个任务现在到哪一步

edit_state：当前 edit 是否已被接受

verification_state：验证做到哪一层了



2. JSON Schema 草案


下面这份 schema 偏工程可落地，适合做：


hook 输出校验

状态文件持久化

agent runtime 里的状态对象

后续 telemetry / trajectory 分析


{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/claude-code-state-machine.schema.json",
  "title": "Claude Code Agent State Machine",
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
      "const": "1.0"
    },
    "task": {
      "type": "object",
      "required": [
        "task_id",
        "task_state",
        "goal"
      ],
      "properties": {
        "task_id": {
          "type": "string"
        },
        "goal": {
          "type": "string"
        },
        "task_state": {
          "type": "string",
          "enum": [
            "TASK_INIT",
            "TASK_LOCALIZED",
            "TASK_EDITING",
            "TASK_LOCAL_VALIDATE",
            "TASK_EDIT_REJECTED",
            "TASK_EDIT_ACCEPTED",
            "TASK_TARGETED_VERIFY",
            "TASK_READY_FOR_SUBMIT",
            "TASK_COMPLETED",
            "TASK_BLOCKED"
          ]
        },
        "summary": {
          "type": "string"
        },
        "changed_files": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "default": []
        },
        "related_tests": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "default": []
        }
      }
    },
    "current": {
      "type": "object",
      "required": [
        "edit_state",
        "verification_state",
        "blocking",
        "allowed_next_tools",
        "disallowed_next_tools"
      ],
      "properties": {
        "edit_state": {
          "type": "string",
          "enum": [
            "EDIT_NONE",
            "EDIT_PROPOSED",
            "EDIT_VALIDATING",
            "EDIT_REJECTED",
            "EDIT_REPAIRING",
            "EDIT_ACCEPTED"
          ]
        },
        "verification_state": {
          "type": "string",
          "enum": [
            "VERIFY_NONE",
            "VERIFY_LSP_ONLY",
            "VERIFY_LOCAL",
            "VERIFY_CHANGED_FILES",
            "VERIFY_TARGETED_TESTS",
            "VERIFY_BROAD"
          ]
        },
        "blocking": {
          "type": "boolean"
        },
        "reason": {
          "type": "string"
        },
        "repair_instruction": {
          "type": "string"
        },
        "allowed_next_tools": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "Read",
              "Edit",
              "Write",
              "LSP",
              "Bash",
              "Glob",
              "Grep",
              "Submit"
            ]
          }
        },
        "disallowed_next_tools": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "Read",
              "Edit",
              "Write",
              "LSP",
              "Bash",
              "Glob",
              "Grep",
              "Submit"
            ]
          }
        },
        "active_file": {
          "type": ["string", "null"]
        },
        "changed_ranges": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/range"
          },
          "default": []
        },
        "diagnostics": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/diagnostic"
          },
          "default": []
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
        "block_on_rejected_edit",
        "block_build_when_local_validation_fails",
        "prefer_targeted_verification",
        "require_local_validation_after_edit"
      ],
      "properties": {
        "require_local_validation_after_edit": {
          "type": "boolean",
          "default": true
        },
        "block_on_rejected_edit": {
          "type": "boolean",
          "default": true
        },
        "block_build_when_local_validation_fails": {
          "type": "boolean",
          "default": true
        },
        "prefer_targeted_verification": {
          "type": "boolean",
          "default": true
        },
        "blocking_sources": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "lsp",
              "lint",
              "typecheck",
              "parser",
              "policy"
            ]
          },
          "default": ["lsp", "lint", "typecheck", "parser", "policy"]
        },
        "non_blocking_sources": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "default": ["format", "style"]
        }
      }
    },
    "allowed_transitions": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/transition"
      }
    },
    "history": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/history_entry"
      },
      "default": []
    }
  },
  "$defs": {
    "range": {
      "type": "object",
      "required": [
        "start_line",
        "end_line"
      ],
      "properties": {
        "start_line": {
          "type": "integer",
          "minimum": 1
        },
        "end_line": {
          "type": "integer",
          "minimum": 1
        },
        "start_col": {
          "type": "integer",
          "minimum": 0
        },
        "end_col": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "diagnostic": {
      "type": "object",
      "required": [
        "source",
        "severity",
        "message"
      ],
      "properties": {
        "source": {
          "type": "string",
          "enum": [
            "lsp",
            "lint",
            "typecheck",
            "parser",
            "policy"
          ]
        },
        "severity": {
          "type": "string",
          "enum": [
            "info",
            "warning",
            "error"
          ]
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
        }
      }
    },
    "transition": {
      "type": "object",
      "required": [
        "from",
        "to",
        "when"
      ],
      "properties": {
        "from": {
          "type": "string"
        },
        "to": {
          "type": "string"
        },
        "when": {
          "type": "string"
        },
        "action": {
          "type": ["string", "null"]
        }
      }
    },
    "history_entry": {
      "type": "object",
      "required": [
        "timestamp",
        "event",
        "from_state",
        "to_state"
      ],
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time"
        },
        "event": {
          "type": "string"
        },
        "from_state": {
          "type": "string"
        },
        "to_state": {
          "type": "string"
        },
        "note": {
          "type": "string"
        }
      }
    }
  }
}



3. YAML 配置草案


下面这份 YAML 更像“运行时规则配置”，方便你喂给：


自定义 orchestrator

hook runner

validator pipeline

policy engine


schema_version: "1.0"

task:
  task_id: "example-task-001"
  goal: "Implement feature/fix bug and ensure only accepted edits can enter broader verification."
  task_state: "TASK_INIT"
  summary: ""
  changed_files: []
  related_tests: []

current:
  edit_state: "EDIT_NONE"
  verification_state: "VERIFY_NONE"
  blocking: false
  reason: ""
  repair_instruction: ""
  allowed_next_tools:
    - Read
    - Glob
    - Grep
    - LSP
  disallowed_next_tools:
    - Submit
  active_file: null
  changed_ranges: []
  diagnostics: []
  last_tool: null
  last_tool_input: null

policy:
  require_local_validation_after_edit: true
  block_on_rejected_edit: true
  block_build_when_local_validation_fails: true
  prefer_targeted_verification: true

  blocking_sources:
    - lsp
    - lint
    - typecheck
    - parser
    - policy

  non_blocking_sources:
    - format
    - style

  allowed_tools_by_task_state:
    TASK_INIT:
      allow: [Read, Glob, Grep, LSP]
      deny: [Submit]
    TASK_LOCALIZED:
      allow: [Read, Glob, Grep, LSP, Edit, Write]
      deny: [Submit]
    TASK_EDITING:
      allow: [Read, LSP, Edit, Write]
      deny: [Submit]
    TASK_LOCAL_VALIDATE:
      allow: [Read, LSP]
      deny: [Submit]
    TASK_EDIT_REJECTED:
      allow: [Read, LSP, Edit, Write]
      deny: [Bash, Submit]
    TASK_EDIT_ACCEPTED:
      allow: [Read, LSP, Edit, Write, Bash]
      deny: [Submit]
    TASK_TARGETED_VERIFY:
      allow: [Read, LSP, Bash]
      deny: [Submit]
    TASK_READY_FOR_SUBMIT:
      allow: [Read, LSP, Bash, Submit]
      deny: []
    TASK_COMPLETED:
      allow: []
      deny: [Read, Edit, Write, LSP, Bash, Submit]

validators:
  on_edit:
    run_order:
      - lsp
      - parser
      - lint
      - typecheck
    stop_on_blocking: false
    classify:
      blocking:
        - source: parser
          severity: error
        - source: lsp
          severity: error
        - source: lint
          severity: error
        - source: typecheck
          severity: error
      non_blocking:
        - source: format
          severity: warning
        - source: style
          severity: warning

  on_accept:
    next_verification: "VERIFY_LOCAL"

  on_reject:
    next_task_state: "TASK_EDIT_REJECTED"
    next_edit_state: "EDIT_REJECTED"
    allowed_next_tools:
      - Read
      - Edit
      - Write
      - LSP
    disallowed_next_tools:
      - Bash
      - Submit
    repair_instruction_template: "Fix blocking diagnostics in the edited file before running build/test/submit."

verification:
  escalation_order:
    - VERIFY_LSP_ONLY
    - VERIFY_LOCAL
    - VERIFY_CHANGED_FILES
    - VERIFY_TARGETED_TESTS
    - VERIFY_BROAD

  prefer_smallest_relevant: true

  targeted_test_rules:
    enabled: true
    sources:
      - changed_files
      - related_tests
      - explicit_user_request

transitions:
  - from: TASK_INIT
    to: TASK_LOCALIZED
    when: "relevant files or symbols identified"

  - from: TASK_LOCALIZED
    to: TASK_EDITING
    when: "first edit or write is proposed"

  - from: TASK_EDITING
    to: TASK_LOCAL_VALIDATE
    when: "an Edit or Write tool succeeds"

  - from: TASK_LOCAL_VALIDATE
    to: TASK_EDIT_REJECTED
    when: "blocking diagnostics exist after local validation"

  - from: TASK_LOCAL_VALIDATE
    to: TASK_EDIT_ACCEPTED
    when: "no blocking diagnostics remain"

  - from: TASK_EDIT_REJECTED
    to: TASK_EDITING
    when: "agent starts repair edit"

  - from: TASK_EDIT_ACCEPTED
    to: TASK_EDITING
    when: "more file changes are needed"

  - from: TASK_EDIT_ACCEPTED
    to: TASK_TARGETED_VERIFY
    when: "all required edits are locally accepted"

  - from: TASK_TARGETED_VERIFY
    to: TASK_EDITING
    when: "targeted verification fails"

  - from: TASK_TARGETED_VERIFY
    to: TASK_READY_FOR_SUBMIT
    when: "targeted verification passes"

  - from: TASK_READY_FOR_SUBMIT
    to: TASK_COMPLETED
    when: "submit succeeds"



4. 运行时实例


这是一个 edit 被 reject 的状态例子。


schema_version: "1.0"

task:
  task_id: "bugfix-142"
  goal: "Fix missing config error handling"
  task_state: "TASK_EDIT_REJECTED"
  summary: "A local edit introduced blocking diagnostics"
  changed_files:
    - "src/config.ts"
  related_tests:
    - "tests/config.test.ts"

current:
  edit_state: "EDIT_REJECTED"
  verification_state: "VERIFY_LOCAL"
  blocking: true
  reason: "Blocking TypeScript error after edit"
  repair_instruction: "Fix the blocking diagnostics in src/config.ts before running build/test."
  allowed_next_tools:
    - Read
    - Edit
    - Write
    - LSP
  disallowed_next_tools:
    - Bash
    - Submit
  active_file: "src/config.ts"
  changed_ranges:
    - start_line: 42
      end_line: 49
  diagnostics:
    - source: "lsp"
      severity: "error"
      code: "TS2339"
      message: "Property 'foo' does not exist on type 'Bar'."
      file: "src/config.ts"
      range:
        start_line: 44
        end_line: 44
        start_col: 12
        end_col: 15
      blocking: true
      newly_introduced: true
  last_tool: "Edit"
  last_tool_input:
    file_path: "src/config.ts"

policy:
  require_local_validation_after_edit: true
  block_on_rejected_edit: true
  block_build_when_local_validation_fails: true
  prefer_targeted_verification: true
  blocking_sources: ["lsp", "lint", "typecheck", "parser", "policy"]
  non_blocking_sources: ["format", "style"]

allowed_transitions:
  - from: "TASK_EDIT_REJECTED"
    to: "TASK_EDITING"
    when: "agent starts repair edit"
    action: "repair"

history:
  - timestamp: "2026-04-15T09:31:00Z"
    event: "edit_applied"
    from_state: "TASK_EDITING"
    to_state: "TASK_LOCAL_VALIDATE"
    note: "Edit on src/config.ts completed"
  - timestamp: "2026-04-15T09:31:02Z"
    event: "local_validation_failed"
    from_state: "TASK_LOCAL_VALIDATE"
    to_state: "TASK_EDIT_REJECTED"
    note: "TS2339 introduced by current edit"



5. 推荐的最小执行规则


如果你要把这套 schema 真接到 Claude Code 里，我建议最少做这 5 条：


规则 1


Edit|Write 成功后，强制进入：


task_state = TASK_LOCAL_VALIDATE

edit_state = EDIT_VALIDATING


规则 2


本地 validator 汇总：


LSP

parser

lint

typecheck


规则 3


只要有 blocking=true 的 diagnostic：


task_state = TASK_EDIT_REJECTED

edit_state = EDIT_REJECTED

禁止 Bash 和 Submit


规则 4


当 agent 再次发起针对同文件的修复 edit：


task_state = TASK_EDITING

edit_state = EDIT_REPAIRING


规则 5


只有在本地无 blocker 时：


task_state = TASK_EDIT_ACCEPTED

edit_state = EDIT_ACCEPTED

才允许升级到 VERIFY_CHANGED_FILES 或 VERIFY_TARGETED_TESTS



6. 一个更实用的扩展建议


如果你真的要落地，我建议再补两个字段。


scope


区分这次验证是：


single_file

changed_files

targeted_tests

broad


ownership


区分 blocker 是：


newly_introduced

pre_existing

unknown


因为实际工程里最常见的问题不是“有错误”，而是：

这个错误是不是这次 edit 新引入的。

这样状态机才不会因为仓库历史脏数据而误判。



7. 一句话总结


这份 JSON Schema / YAML 草案的核心思想就是：

把 Claude Code 的 edit、LSP、lint、typecheck、hooks 结果统一收敛成一个显式状态对象。

这样你就不再是“希望 Claude 记住规则”，而是可以明确地表达：


现在任务在哪个阶段

当前 edit 是否被接受

接下来允许哪些工具

什么时候能升级到 build/test

什么时候才能 submit


如果你愿意，我下一条可以继续直接给你一版：


“和 Claude Code hooks 对接的状态机 runtime 输出 JSON 格式”
或者
“TypeScript / Python 项目专用的 YAML 配置细化版”。
