---
title: "Context editing"
source: "https://platform.claude.com/docs/en/build-with-claude/context-editing"
author:
published:
created: 2026-04-16
description: "Automatically manage conversation context as it grows with context editing."
tags:
  - "clippings"
---
This feature is eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.此功能符合零数据保留（ZDR）</b>的条件。当你的组织签订了零数据保留协议后，通过此功能发送的数据在API响应返回后不会被存储。

## Overview 概述

For most use cases, [server-side compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) is the primary strategy for managing context in long-running conversations. The strategies on this page are useful for specific scenarios where you need more fine-grained control over what content is cleared.对于大多数使用场景， [服务器端压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) 是在长对话中管理上下文的主要策略。本页介绍的策略适用于需要对清除的内容进行更精细控制的特定场景。

Context editing allows you to selectively clear specific content from conversation history as it grows. Beyond optimizing costs and staying within limits, this is about actively curating what Claude sees: context is a finite resource with diminishing returns, and irrelevant content degrades model focus. Context editing gives you fine-grained runtime control over that curation. For the broader principles behind context management, see [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). This page covers:上下文编辑功能允许你在对话记录不断增加时，有选择地清除其中的特定内容。除了优化成本和不超出限制外，这还关乎主动管理 Claude 所看到的内容：上下文是一种有限资源，其收益会逐渐递减，无关内容会降低模型的注意力集中度。上下文编辑让你能在运行时对这种管理进行精细控制。有关上下文管理背后的核心原则，请参阅 [高效上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 。本页包含以下内容：

- **Tool result clearing** - Best for agentic workflows with heavy tool use where old tool results are no longer needed **工具结果清除** - 最适用于工具使用频繁的智能体工作流，在这些工作流中旧的工具结果不再需要
- **Thinking block clearing** - For managing thinking blocks when using extended thinking, with options to preserve recent thinking for context continuity **思维块清理** - 用于在使用扩展思维时管理思维块，可选择保留近期思维以保持上下文连续性
- **Client-side SDK compaction** - An SDK-based alternative for summary-based context management (server-side compaction is generally preferred) **客户端 SDK 压缩** ——一种基于 SDK 的替代方案，用于基于摘要的上下文管理（通常优先选择服务端压缩）

| Approach 方法 | Where it runs 适用场景 | Strategies 策略 | How it works 工作原理 |
| --- | --- | --- | --- |
| **Server-side 服务端** | API | Tool result clearing (`clear_tool_uses_20250919`) 工具结果清除（ `clear_tool_uses_20250919` ）   Thinking block clearing (`clear_thinking_20251015`) 思考块清除（ `clear_thinking_20251015` ） | Applied before the prompt reaches Claude. Clears specific content from conversation history. Each strategy can be configured independently.在提示词发送到 Claude 之前应用。清除对话历史中的特定内容。每种策略均可独立配置。 |
| **Client-side 客户端** | SDK 软件开发工具包 | Compaction 压缩 | Available in [Python, TypeScript, and Ruby SDKs](https://platform.claude.com/docs/en/api/client-sdks) when using [`tool_runner`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner). Generates a summary and replaces full conversation history. See [Client-side compaction](#client-side-compaction-sdk) below.在使用 [`tool_runner`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) 时， [Python、TypeScript 和 Ruby SDK](https://platform.claude.com/docs/en/api/client-sdks) 均支持此功能。该功能会生成摘要并替换完整的对话历史记录。详见下方 [客户端压缩](#client-side-compaction-sdk) 。 |

## Server-side strategies 服务端策略

Context editing is in beta with support for tool result clearing and thinking block clearing. To enable it, use the beta header `context-management-2025-06-27` in your API requests.上下文编辑功能处于测试阶段，支持清除工具结果和清除思考块。要启用此功能，请在 API 请求中使用测试版标头 `context-management-2025-06-27` 。

Share feedback on this feature through the [feedback form](https://forms.gle/YXC2EKGMhjN1c4L88).请通过 [反馈表单](https://forms.gle/YXC2EKGMhjN1c4L88) 分享对此功能的意见。

### Tool result clearing 工具结果清除

The `clear_tool_uses_20250919` strategy clears tool results when conversation context grows beyond your configured threshold. This is particularly useful for agentic workflows with heavy tool use. Older tool results (like file contents or search results) are no longer needed once Claude has processed them.`clear_tool_uses_20250919` 策略会在对话上下文超出你配置的阈值时清理工具结果。这对于大量使用工具的智能体工作流尤为有用。一旦 Claude 处理完旧的工具结果（如文件内容或搜索结果），这些结果就不再需要了。

When activated, the API automatically clears the oldest tool results in chronological order. The API replaces each cleared result with placeholder text so Claude knows it was removed. By default, only tool results are cleared. You can optionally clear both tool results and tool calls (the tool use parameters) by setting `clear_tool_inputs` to true.启用后，API 会按时间顺序自动清除最早的工具结果。API 会用占位文本替换每个被清除的结果，以便 Claude 知晓该结果已被移除。默认情况下，仅清除工具结果。你可以将 `clear_tool_inputs` 设置为 true，以选择同时清除工具结果和工具调用（工具使用参数）。

### Thinking block clearing 思考块清除

The `clear_thinking_20251015` strategy manages `thinking` blocks in conversations when extended thinking is enabled. This strategy gives you control over thinking preservation: you can choose to keep more thinking blocks to maintain reasoning continuity, or clear them more aggressively to save context space.`clear_thinking_20251015` 策略在启用扩展思考功能时，管理对话中的 `thinking` 块。该策略让你可以控制思考内容的保留规则：你可以选择保留更多思考块以维持推理的连贯性，也可以更主动地清除它们以节省上下文空间。

**Default behavior:** When extended thinking is enabled without configuring the `clear_thinking_20251015` strategy, the API automatically keeps only the thinking blocks from the last assistant turn (equivalent to `keep: {type: "thinking_turns", value: 1}`).**默认行为：** 在启用扩展思考功能但未配置 `clear_thinking_20251015` 策略时，API 会自动仅保留上一轮助手回复的思考块（等同于 `keep: {type: "thinking_turns", value: 1}` ）。

To maximize cache hits, preserve all thinking blocks by setting `keep: "all"`.要最大化缓存命中率，请通过设置 `keep: "all"` 来保留所有思考块。

An assistant conversation turn may include multiple content blocks (e.g. when using tools) and multiple thinking blocks (e.g. with [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking)).一次助手对话轮次可能包含多个内容块（例如在使用工具时）和多个思考块（例如结合 [穿插式思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking) ）。

### Context editing happens server-side 上下文编辑在服务器端进行

Context editing is applied server-side before the prompt reaches Claude. Your client application maintains the full, unmodified conversation history. You do not need to sync your client state with the edited version. Continue managing your full conversation history locally as you normally would.在提示到达Claude之前在服务器端应用上下文编辑。您的客户端应用程序维护完整的、未修改的对话历史记录。您不需要将客户端状态与编辑后的版本同步。像往常一样继续在本地管理完整的对话历史记录。

### Context editing and prompt caching 上下文编辑与提示缓存

Context editing's interaction with [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) varies by strategy:上下文编辑与 [提示词缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 的交互方式因策略而异：

- **Tool result clearing**: Invalidates cached prompt prefixes when content is cleared. To account for this, clear enough tokens to make the cache invalidation worthwhile. Use the `clear_at_least` parameter to ensure a minimum number of tokens is cleared each time. You'll incur cache write costs each time content is cleared, but subsequent requests can reuse the newly cached prefix.工具结果清除</b>：清除内容时使缓存的提示前缀失效。为实现这一操作，需清除足够多的令牌以确保缓存失效具有实际价值。使用 `clear_at_least` 参数可确保每次清除的令牌数量达到最小值。每次清除内容时都会产生缓存写入开销，但后续请求可以复用新缓存的前缀。
- **Thinking block clearing**: When thinking blocks are **kept** in context (not cleared), the prompt cache is preserved, enabling cache hits and reducing input token costs. When thinking blocks are **cleared**, the cache is invalidated at the point where clearing occurs. Configure the `keep` parameter based on whether you want to prioritize cache performance or context window availability.**思维块清理** ：当思维块在上下文中 **保留** （不清理）时，提示词缓存会被保留，从而实现缓存命中并降低输入令牌成本。当思维块被 **清理** 时，缓存会在清理发生的节点失效。请根据你希望优先考虑缓存性能还是上下文窗口可用性来配置 `keep` 参数。

## Supported models 支持的模型

Context editing is available on all supported Claude models.上下文编辑适用于所有支持的 Claude 模型。

## Tool result clearing usage 工具结果清除的使用方法

The simplest way to enable tool result clearing is to specify only the strategy type. All other [configuration options](#configuration-options-for-tool-result-clearing) use their default values:启用工具结果清除的最简单方法是仅指定策略类型。所有其他 [配置选项](#configuration-options-for-tool-result-clearing) 均使用其默认值：

```
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Search for recent developments in AI"
            }
        ],
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search"
            }
        ],
        "context_management": {
            "edits": [
                {"type": "clear_tool_uses_20250919"}
            ]
        }
    }'
```

### Advanced configuration 高级配置

You can customize the tool result clearing behavior with additional parameters:你可以使用额外参数自定义工具结果的清除行为：

```
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Create a simple command line calculator app using Python"
            }
        ],
        "tools": [
            {
                "type": "text_editor_20250728",
                "name": "str_replace_based_edit_tool",
                "max_characters": 10000
            },
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }
        ],
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    "keep": {
                        "type": "tool_uses",
                        "value": 3
                    },
                    "clear_at_least": {
                        "type": "input_tokens",
                        "value": 5000
                    },
                    "exclude_tools": ["web_search"]
                }
            ]
        }
    }'
```

## Thinking block clearing usage 思维块清除用法

Enable thinking block clearing to manage context and prompt caching effectively when extended thinking is enabled:启用思考块清除功能，可在开启扩展思考时有效管理上下文和提示缓存：

```
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": "Hello"}],
        "thinking": {
            "type": "enabled",
            "budget_tokens": 10000
        },
        "context_management": {
            "edits": [
                {
                    "type": "clear_thinking_20251015",
                    "keep": {
                        "type": "thinking_turns",
                        "value": 2
                    }
                }
            ]
        }
    }'
```

### Configuration options for thinking block clearing思考块清除的配置选项

The `clear_thinking_20251015` strategy supports the following configuration:`clear_thinking_20251015` 策略支持以下配置：

| Configuration option 配置选项 | Default 默认值 | Description 描述 |
| --- | --- | --- |
| `keep` | `{type: "thinking_turns", value: 1}` | Defines how many recent assistant turns with thinking blocks to preserve. Use `{type: "thinking_turns", value: N}` where N must be > 0 to keep the last N turns, or `"all"` to keep all thinking blocks.定义要保留的最近带有思考块的助手回复数量。使用 `{type: "thinking_turns", value: N}` 格式，其中 N 必须大于 0 以保留最近 N 次回复，或使用 `"all"` 以保留所有思考块。 |

**Example configurations: 示例配置：**

Keep thinking blocks from the last 3 assistant turns:保留最近3次助手回复的思考块：

```
{
  "type": "clear_thinking_20251015",
  "keep": {
    "type": "thinking_turns",
    "value": 3
  }
}
```

Keep all thinking blocks (maximizes cache hits):保留所有思考片段（最大化缓存命中）：

```
{
  "type": "clear_thinking_20251015",
  "keep": "all"
}
```

### Combining strategies 组合策略

You can use both thinking block clearing and tool result clearing together:你可以同时使用思考块清理和工具结果清理功能：

When using multiple strategies, the `clear_thinking_20251015` strategy must be listed first in the `edits` array.使用多种策略时， `clear_thinking_20251015` 策略必须在 `edits` 数组中排在首位。

```
ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
model: claude-opus-4-6
max_tokens: 16000
thinking:
  type: enabled
  budget_tokens: 10000
messages:
  - role: user
    content: Hello
tools:
  - type: web_search_20250305
    name: web_search
context_management:
  edits:
    - type: clear_thinking_20251015
      keep:
        type: thinking_turns
        value: 2
    - type: clear_tool_uses_20250919
      trigger:
        type: input_tokens
        value: 50000
      keep:
        type: tool_uses
        value: 5
YAML
```

## Configuration options for tool result clearing工具结果清理的配置选项

| Configuration option 配置选项 | Default 默认值 | Description 描述 |
| --- | --- | --- |
| `trigger` | 100,000 input tokens 100,000 输入令牌 | Defines when the context editing strategy activates. Once the prompt exceeds this threshold, clearing will begin. You can specify this value in either `input_tokens` or `tool_uses`.定义上下文编辑策略的激活时机。当提示词超过此阈值时，将开始清除操作。你可以通过 `input_tokens` 或 `tool_uses` 来指定此值。 |
| `keep` | 3 tool uses 3 次工具调用 | Defines how many recent tool use/result pairs to keep after clearing occurs. The API removes the oldest tool interactions first, preserving the most recent ones.定义了执行清除操作后保留的最近工具使用/结果对的数量。API 会优先移除最早的工具交互，保留最新的交互。 |
| `clear_at_least` | None 无 | Ensures a minimum number of tokens is cleared each time the strategy activates. If the API can't clear at least the specified amount, the strategy will not be applied. This helps determine if context clearing is worth breaking your prompt cache.确保每次策略激活时都清除至少指定数量的 token。如果 API 无法清除至少指定的数量，则不会应用该策略。这有助于判断清除上下文是否值得破坏你的提示词缓存。 |
| `exclude_tools` | None 无 | List of tool names whose tool uses and results should never be cleared. Useful for preserving important context.永远不应清除其工具使用情况和结果的工具名称列表。这对于保留重要上下文非常有用。 |
| `clear_tool_inputs` | `false` | Controls whether the tool call parameters are cleared along with the tool results. By default, only the tool results are cleared while keeping Claude's original tool calls visible.控制是否随工具结果一起清除工具调用参数。默认情况下，仅清除工具结果，同时保留 Claude 原始的工具调用记录。 |

## Context editing response 上下文编辑响应

You can see which context edits were applied to your request using the `context_management` response field, along with helpful statistics about the content and input tokens cleared.你可以通过 `context_management` 响应字段查看哪些上下文编辑已应用到你的请求，同时查看有关内容的有用统计信息以及已清除的输入令牌数量。

```
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    // ...
  ],
  "usage": {
    // ...
  },
  "context_management": {
    "applied_edits": [
      // When using \`clear_thinking_20251015\`
      {
        "type": "clear_thinking_20251015",
        "cleared_thinking_turns": 3,
        "cleared_input_tokens": 15000
      },
      // When using \`clear_tool_uses_20250919\`
      {
        "type": "clear_tool_uses_20250919",
        "cleared_tool_uses": 8,
        "cleared_input_tokens": 50000
      }
    ]
  }
}
```

For streaming responses, the context edits will be included in the final `message_delta` event:对于流式响应，上下文编辑将包含在最终的 `message_delta` 事件中：

Streaming Response 流式响应

```
{
  "type": "message_delta",
  "delta": {
    "stop_reason": "end_turn",
    "stop_sequence": null
  },
  "usage": {
    "output_tokens": 1024
  },
  "context_management": {
    "applied_edits": [
      // ...
    ]
  }
}
```

## Token counting 令牌计数

The [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) endpoint supports context management, allowing you to preview how many tokens your prompt will use after context editing is applied.[令牌计数](https://platform.claude.com/docs/en/build-with-claude/token-counting) 接口支持上下文管理，让你可以预览应用上下文编辑后，提示词将使用多少个令牌。

```
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "messages": [
            {
                "role": "user",
                "content": "Continue our conversation..."
            }
        ],
        "tools": [],
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    "keep": {
                        "type": "tool_uses",
                        "value": 5
                    }
                }
            ]
        }
    }'
```

```
{
  "input_tokens": 25000,
  "context_management": {
    "original_input_tokens": 70000
  }
}
```

The response shows both the final token count after context management is applied (`input_tokens`) and the original token count before any clearing occurred (`original_input_tokens`).该响应同时展示了应用上下文管理后的最终标记数（ `input_tokens` ）和进行任何清除操作前的原始标记数（ `original_input_tokens` ）。

## Using with the Memory Tool 与记忆工具配合使用

Context editing can be combined with the [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool). When your conversation context approaches the configured clearing threshold, Claude receives an automatic warning to preserve important information. This enables Claude to save tool results or context to its memory files before they're cleared from the conversation history.上下文编辑可与 [记忆工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) 结合使用。当你的对话上下文达到配置的清除阈值时，Claude 会收到自动警告，以保留重要信息。这使得 Claude 能够在工具结果或上下文从对话历史中被清除前，将其保存到记忆文件中。

This combination allows you to: 这种组合可让你实现以下功能：

- **Preserve important context**: Claude can write essential information from tool results to memory files before those results are cleared **保留重要上下文** ：在工具结果被清除之前，Claude 可以将工具结果中的关键信息写入记忆文件
- **Maintain long-running workflows**: Enable agentic workflows that would otherwise exceed context limits by offloading information to persistent storage **维护长期运行的工作流** ：通过将信息卸载到持久存储中，启用原本会超出上下文限制的智能体工作流
- **Access information on demand**: Claude can look up previously cleared information from memory files when needed, rather than keeping everything in the active context window **按需访问信息** ：Claude 可在需要时从记忆文件中调取之前已清理的信息，而非将所有内容都保留在活动上下文窗口中

For example, in a file editing workflow where Claude performs many operations, Claude can summarize completed changes to memory files as the context grows. When tool results are cleared, Claude retains access to that information through its memory system and can continue working effectively.例如，在Claude执行多项操作的文件编辑工作流中，随着上下文内容的增加，Claude可以将已完成的修改汇总到记忆文件中。当工具结果被清除后，Claude仍可通过其记忆系统获取该信息，从而继续高效开展工作。

To use both features together, enable them in your API request:要同时使用这两项功能，请在你的 API 请求中启用它们：

```
ant beta:messages create --beta context-management-2025-06-27 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello
tools:
  - type: memory_20250818
    name: memory
context_management:
  edits:
    - type: clear_tool_uses_20250919
YAML
```

For the full memory tool reference including commands and examples, see [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).有关内存工具的完整参考资料（包括命令和示例），请参阅 [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) 。

## Client-side compaction (SDK) 客户端压缩（SDK）

**Anthropic recommends server-side compaction over SDK compaction.** [Server-side compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) handles context management automatically with less integration complexity, better token usage calculation, and no client-side limitations. Use SDK compaction only if you specifically need client-side control over the summarization process.**Anthropic 推荐服务端压缩而非 SDK 压缩。** [服务端压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) 可自动处理上下文管理，集成复杂度更低、令牌使用计算更精准，且无客户端限制。仅当你明确需要对摘要流程进行客户端控制时，才使用 SDK 压缩。

Compaction is available in the [Python, TypeScript, and Ruby SDKs](https://platform.claude.com/docs/en/api/client-sdks) when using the [`tool_runner` method](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner).在使用 [`tool_runner` 方法](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner) 时， [Python、TypeScript 和 Ruby SDK](https://platform.claude.com/docs/en/api/client-sdks) 中提供了压缩功能。

Compaction is an SDK feature that automatically manages conversation context by generating summaries when token usage grows too large. Unlike server-side context editing strategies that clear content, compaction instructs Claude to summarize the conversation history, then replaces the full history with that summary. This allows Claude to continue working on long-running tasks that would otherwise exceed the [context window](https://platform.claude.com/docs/en/build-with-claude/context-windows).压缩是一项 SDK 功能，它会在令牌用量过大时通过生成摘要来自动管理对话上下文。与会清除内容的服务端上下文编辑策略不同，压缩会指示 Claude 对对话历史进行总结，随后用该摘要替换完整的历史记录。这使得 Claude 能够继续处理原本会超出 [上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 的长时运行任务。

### How compaction works 压缩机制

When compaction is enabled, the SDK monitors token usage after each model response:启用压缩功能后，SDK 会在每次模型响应后监控令牌使用情况：

1. **Threshold check:** The SDK calculates total tokens as `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`.**阈值检查：** SDK 将总令牌计算为 `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`
2. **Summary generation:** When the threshold is exceeded, a summary prompt is injected as a user turn, and Claude generates a structured summary wrapped in `<summary></summary>` tags.**摘要生成：** 当超过阈值时，会插入一个摘要提示作为用户轮次，Claude 会生成一个用 `<summary></summary>` 标签包裹的结构化摘要。
3. **Context replacement:** The SDK extracts the summary and replaces the entire message history with it.**上下文替换：** SDK 提取摘要并将其替换整个消息历史记录。
4. **Continuation:** The conversation resumes from the summary, with Claude picking up where it left off.**续篇：** 对话从摘要处继续，Claude 接着之前的内容展开。

### Using compaction 使用压缩

Add `compaction_control` to your `tool_runner` call to enable automatic summarization when token usage exceeds the threshold.在你的 `compaction_control` 调用中添加 `tool_runner` ，以便在令牌使用量超过阈值时启用自动摘要功能。

The CLI does not include a `tool_runner` helper. Use [server-side compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) instead, which handles compaction on Anthropic's servers without SDK-side integration.CLI 不包含 `tool_runner` 辅助工具。请改用 [服务端压缩](https://platform.claude.com/docs/en/build-with-claude/compaction) ，该方式会在 Anthropic 的服务器上执行压缩操作，无需 SDK 端集成。

#### What happens during compaction 压缩期间会发生什么

As the conversation grows, the message history accumulates:随着对话不断展开，消息历史会不断累积：

**Before compaction (approaching 100k tokens):压缩前（接近10万个标记）：**

```
[
  { "role": "user", "content": "Analyze all files and write a report..." },
  { "role": "assistant", "content": "I'll help. Let me start by reading..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "Based on file1.txt, I see..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "After analyzing file2.txt..." }
  // ... 50 more exchanges like this ...
]
```

When tokens exceed the threshold, the SDK injects a summary request and Claude generates a summary. The entire history is then replaced:当令牌超过阈值时，SDK 会注入摘要请求，Claude 会生成摘要。随后整个历史记录将被替换：

**After compaction (back to ~2-3k tokens):压缩后（恢复至约2000-3000个标记）：**

```
[
  {
    "role": "assistant",
    "content": "# Task Overview\nThe user requested analysis of directory files to produce a summary report...\n\n# Current State\nAnalyzed 52 files across 3 subdirectories. Key findings documented in report.md...\n\n# Important Discoveries\n- Configuration files use YAML format\n- Found 3 deprecated dependencies\n- Test coverage at 67%\n\n# Next Steps\n1. Analyze remaining files in /src/legacy\n2. Complete final report sections...\n\n# Context to Preserve\nUser prefers markdown format with executive summary first..."
  }
]
```

Claude continues working from this summary as if it were the original conversation history.Claude 会从这个摘要继续处理，就像它是原始的对话历史一样。

### Configuration options 配置选项

| Parameter 参数 | Type 类型 | Required 必填 | Default 默认值 | Description 描述 |
| --- | --- | --- | --- | --- |
| `enabled` | boolean 布尔值 | Yes 是 | \- | Whether to enable automatic compaction 是否启用自动压缩 |
| `context_token_threshold` | number 数字 | No 否 | 100,000 | Token count at which compaction triggers 触发压缩的令牌数量 |
| `model` | string 字符串 | No 否 | Same as main model 与主模型相同 | Model to use for generating summaries 用于生成摘要的模型 |
| `summary_prompt` | string 字符串 | No 否 | See below 见下文 | Custom prompt for summary generation 用于生成摘要的自定义提示词 |

#### Choosing a token threshold 选择令牌阈值

The threshold determines when compaction occurs. A lower threshold means more frequent compactions with smaller context windows. A higher threshold allows more context but risks hitting limits.阈值决定压缩何时发生。较低的阈值意味着在更小的上下文窗口下进行更频繁的压缩。较高的阈值能容纳更多上下文，但存在达到上限的风险。

```
# More frequent compaction for memory-constrained scenarios
compaction_control = {"enabled": True, "context_token_threshold": 50000}

# Less frequent compaction when you need more context
compaction_control = {"enabled": True, "context_token_threshold": 150000}
```

#### Using a different model for summaries使用不同的模型生成摘要

You can use a faster or cheaper model for generating summaries:你可以使用更快或更便宜的模型来生成摘要：

```
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "model": "claude-haiku-4-5",
}
```

#### Custom summary prompts 自定义摘要提示词

You can provide a custom prompt for domain-specific needs. Your prompt should instruct Claude to wrap its summary in `<summary></summary>` tags.你可以为特定领域的需求提供自定义提示词。你的提示词应指示 Claude 将其总结内容包裹在 \` `<summary></summary>` \` 标签中。

```
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "summary_prompt": """Summarize the research conducted so far, including:
- Sources consulted and key findings
- Questions answered and remaining unknowns
- Recommended next steps

Wrap your summary in <summary></summary> tags.""",
}
```

### Default summary prompt 默认摘要提示词

The built-in summary prompt instructs Claude to create a structured continuation summary including:内置的摘要提示词会指示 Claude 生成一份结构化的续篇摘要，其中包括：

1. **Task Overview:** The user's core request, success criteria, and constraints.**任务概述：** 用户的核心请求、成功标准和约束条件。
2. **Current State:** What has been completed, files modified, and artifacts produced.**当前状态：** 已完成的工作、修改的文件以及生成的成果。
3. **Important Discoveries:** Technical constraints, decisions made, errors resolved, and failed approaches.**重要发现：** 技术限制、做出的决策、解决的错误以及失败的方法。
4. **Next Steps:** Specific actions needed, blockers, and priority order.**后续步骤：** 所需的具体操作、阻碍因素以及优先级顺序。
5. **Context to Preserve:** User preferences, domain-specific details, and commitments made.**需保留的上下文：** 用户偏好、特定领域细节以及做出的承诺。

This structure enables Claude to resume work efficiently without losing important context or repeating mistakes.这种结构让 Claude 能够高效地恢复工作，同时不会丢失重要上下文或重复错误。

### Limitations 局限性

#### Server-side tools 服务端工具

Compaction requires special consideration when using server-side tools such as [web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) or [web fetch](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool).使用 [网页搜索](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) 或 [网页获取](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool) 等服务器端工具时，需要对压缩进行特殊考量。

When using server-side tools, the SDK may incorrectly calculate token usage, causing compaction to trigger at the wrong time.使用服务端工具时，SDK 可能会错误计算令牌使用量，导致压缩在错误的时间触发。

For example, after a web search operation, the API response might show:例如，在一次网页搜索操作后，API 响应可能会显示：

```
{
  "usage": {
    "input_tokens": 63000,
    "cache_read_input_tokens": 270000,
    "output_tokens": 1400
  }
}
```

The SDK calculates total usage as 63,000 + 270,000 = 333,000 tokens. However, the `cache_read_input_tokens` value includes accumulated reads from multiple internal API calls made by the server-side tool, not your actual conversation context. Your real context length might only be the 63,000 `input_tokens`, but the SDK sees 333k and triggers compaction prematurely.SDK 将总使用量计算为 63,000 + 270,000 = 333,000 个 token。但 `cache_read_input_tokens` 值包含了服务端工具发起的多次内部 API 调用的累计读取量，并非你实际的对话上下文。你的真实上下文长度可能只有 63,000 个 `input_tokens` ，但 SDK 会识别到 333,000 并提前触发压缩。

**Workarounds: 解决办法：**

- Use the [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) endpoint to get accurate context length 使用 [令牌计数](https://platform.claude.com/docs/en/build-with-claude/token-counting) 接口获取准确的上下文长度
- Avoid compaction when using server-side tools extensively 在大量使用服务端工具时避免压缩

#### Tool use edge cases 工具使用边缘情况

When the SDK triggers compaction while a tool use response is pending, it removes the tool use block from the message history before generating the summary. Claude will re-issue the tool call after resuming from the summary if still needed.当 SDK 在工具使用响应处于待处理状态时触发压缩，它会在生成摘要前从消息历史中移除工具使用模块。如果仍有需要，Claude 在完成摘要生成后会重新发出工具调用。

### Monitoring compaction 监控压缩

Understanding when compaction triggers helps you tune thresholds and verify expected behavior.了解压缩触发的时机有助于调整阈值并验证预期行为。

The Python SDK logs compaction events at the INFO level. Enable the `anthropic.lib.tools` logger:Python SDK 会在 INFO 级别记录压缩事件。启用 `anthropic.lib.tools` 日志记录器：

```
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("anthropic.lib.tools").setLevel(logging.INFO)

# Logs will show:
# INFO: Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
# INFO: Compaction complete. New token usage: 2500
```

### When to use compaction 何时使用压缩

**Good use cases: 适用的场景：**

- Long-running agent tasks that process many files or data sources 处理大量文件或数据源的长期智能体任务
- Research workflows that accumulate large amounts of information 积累大量信息的研究工作流程
- Multi-step tasks with clear, measurable progress 具有清晰、可衡量进度的多步骤任务
- Tasks that produce artifacts (files, reports) that persist outside the conversation 会生成在对话之外持续存在的成果物（文件、报告）的任务

**Less ideal use cases: 不太理想的用例：**

- Tasks requiring precise recall of early conversation details 需要精准回忆早期对话细节的任务
- Workflows using server-side tools extensively 大量使用服务器端工具的工作流
- Tasks that need to maintain exact state across many variables 需要在多个变量间保持精确状态的任务

Was this page helpful? 此页面是否有帮助？