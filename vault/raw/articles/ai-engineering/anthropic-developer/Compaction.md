---
title: "Compaction"
source: "https://platform.claude.com/docs/en/build-with-claude/compaction"
author:
published:
created: 2026-04-16
description: "Server-side context compaction for managing long conversations that approach context window limits."
tags:
  - "clippings"
---
This feature is eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.此功能符合零数据保留（ZDR）</b>的条件。当你的组织签订了零数据保留协议后，通过此功能发送的数据在API响应返回后不会被存储。

Server-side compaction is the recommended strategy for managing context in long-running conversations and agentic workflows. It handles context management automatically with minimal integration work.服务端压缩是管理长时对话和智能体工作流上下文的推荐策略。它能自动处理上下文管理，集成工作量极小。

Compaction extends the effective context length for long-running conversations and tasks by automatically summarizing older context when approaching the context window limit. This isn't just about staying under a token cap. As conversations get longer, models struggle to maintain focus across the full history. Compaction keeps the active context focused and performant by replacing stale content with concise summaries.压缩功能通过在接近上下文窗口限制时自动总结较旧的上下文，为长期运行的对话和任务扩展有效上下文长度。这不仅仅是为了不超过令牌上限。随着对话变得越来越长，模型难以在完整的历史记录中保持注意力聚焦。压缩功能通过用简洁的摘要替换过时内容，让活跃上下文保持聚焦且运行高效。

For a deeper look at why long contexts degrade and how compaction helps, see [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).要深入了解长上下文为何会退化以及压缩如何发挥作用，请参阅 [高效上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 。

This is ideal for: 这非常适用于：

- Chat-based, multi-turn conversations where you want users to use one chat for a long period of time 适用于希望用户长时间使用同一聊天会话的基于聊天的多轮对话
- Task-oriented prompts that require a lot of follow-up work (often tool use) that may exceed the context window 需要大量后续工作（通常是工具调用）且可能超出上下文窗口的任务型提示词

Compaction is in beta. Include the [beta header](https://platform.claude.com/docs/en/api/beta-headers) `compact-2026-01-12` in your API requests to use this feature.压缩功能处于测试阶段。请在 API 请求中包含 [beta 标头](https://platform.claude.com/docs/en/api/beta-headers) `compact-2026-01-12` 以使用此功能。

## Supported models 支持的模型

Compaction is supported on the following models:以下模型支持压缩功能：

- [Claude Mythos Preview](https://anthropic.com/glasswing) (`claude-mythos-preview`) [Claude Mythos 预览版](https://anthropic.com/glasswing) (`claude-mythos-preview`)
- Claude Opus 4.6 (`claude-opus-4-6`) 克劳德作品4-6
- Claude Sonnet 4.6 (`claude-sonnet-4-6`) Claude Sonnet 4.6（ `claude-sonnet-4-6` ）

## How compaction works 压缩机制的工作原理

When compaction is enabled, Claude automatically summarizes your conversation when it approaches the configured token threshold. The API:启用压缩功能后，当对话接近配置的令牌阈值时，Claude 会自动总结你的对话。相关 API 如下：

1. Detects when input tokens exceed your specified trigger threshold.检测输入令牌何时超过指定的触发阈值。
2. Generates a summary of the current conversation.生成当前对话的摘要。
3. Creates a `compaction` block containing the summary.创建一个包含摘要的 `compaction` 块。
4. Continues the response with the compacted context.以压缩后的上下文继续完成回复。

On subsequent requests, append the response to your messages. The API automatically drops all message blocks prior to the `compaction` block, continuing the conversation from the summary.在后续的请求中，将回复附加到你的消息中。API 会自动删除 `compaction` 块之前的所有消息块，从摘要继续对话。

![Flow diagram showing the compaction process: when input tokens exceed the trigger threshold, Claude generates a summary in a compaction block and continues the response with the compacted context](https://platform.claude.com/docs/images/compaction-flow.svg)

## Basic usage 基本用法

Enable compaction by adding the `compact_20260112` strategy to `context_management.edits` in your Messages API request.在你的消息 API 请求中，向 `context_management.edits` 添加 `compact_20260112` 策略以启用压缩。

```
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: compact-2026-01-12" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": "Help me build a website"
        }
    ],
    "context_management": {
        "edits": [
            {
                "type": "compact_20260112"
            }
        ]
    }
}'
```

## Parameters 参数

| Parameter 参数 | Type 类型 | Default 默认值 | Description 描述 |
| --- | --- | --- | --- |
| `type` | string 字符串 | Required 必填 | Must be `"compact_20260112"` 必须为 `"compact_20260112"` |
| `trigger` | object 对象 | 150,000 tokens 150,000 个标记 | When to trigger compaction. Must be at least 50,000 tokens.何时触发压缩。至少需要50,000个标记。 |
| `pause_after_compaction` | boolean 布尔值 | `false` | Whether to pause after generating the compaction summary 生成压缩摘要后是否暂停 |
| `instructions` | string 字符串 | `null` | Custom summarization prompt. Completely replaces the default prompt when provided.自定义摘要提示词。提供后将完全替换默认提示词。 |

### Trigger configuration 触发配置

Configure when compaction triggers using the `trigger` parameter:使用 `trigger` 参数配置压缩的触发时机：

```
ant beta:messages create --beta compact-2026-01-12 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
      trigger:
        type: input_tokens
        value: 150000
YAML
```

### Custom summarization instructions 自定义摘要说明

By default, compaction uses the following summarization prompt:默认情况下，压缩使用以下摘要提示：

```
You have written a partial transcript for the initial task above. Please write a summary of the transcript. The purpose of this summary is to provide continuity so you can continue to make progress towards solving the task in a future context, where the raw history above may not be accessible and will be replaced with this summary. Write down anything that would be helpful, including the state, next steps, learnings etc. You must wrap your summary in a <summary></summary> block.
```

You can provide custom instructions via the `instructions` parameter to replace this prompt entirely. Custom instructions don't supplement the default; they completely replace it:你可以通过 `instructions` 参数提供自定义指令，以完全替换此提示。自定义指令不会补充默认内容，而是会将其完全替换：

```
ant beta:messages create --beta compact-2026-01-12 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
      instructions: >-
        Focus on preserving code snippets, variable names, and
        technical decisions.
YAML
```

### Pausing after compaction 压缩后暂停

Use `pause_after_compaction` to pause the API after generating the compaction summary. This allows you to add additional content blocks (such as preserving recent messages or specific instruction-oriented messages) before the API continues with the response.使用 `pause_after_compaction` 可在生成压缩摘要后暂停API。这允许你在API继续生成响应之前添加额外的内容块（例如保留最近的消息或特定的指令类消息）。

When enabled, the API returns a message with the `compaction` stop reason after generating the compaction block:启用后，API 在生成压缩块后会返回一条包含 `compaction` 停止原因的消息：

```
ant beta:messages create --beta compact-2026-01-12 \
  --transform '{stop_reason,content}' --format jsonl <<'YAML' > resp.json
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: "Hello, Claude"
context_management:
  edits:
    - type: compact_20260112
      pause_after_compaction: true
YAML

# Check if compaction triggered a pause
if grep -q '"stop_reason":"compaction"' resp.json; then
  # Response contains only the compaction block
  RESP=$(cat resp.json)
  CONTENT="${RESP#*\"content\":}"
  printf '%s' "${CONTENT%\}}" > content.json

  # Continue the request
  ant beta:messages create --beta compact-2026-01-12 <<YAML > /dev/null
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: "Hello, Claude"
  - role: assistant
    content: $(cat content.json)
context_management:
  edits:
    - type: compact_20260112
YAML
fi
```

#### Enforcing a total token budget 强制执行总令牌预算

When a model works on long tasks with many tool-use iterations, total token consumption can grow significantly. You can combine `pause_after_compaction` with a compaction counter to estimate cumulative usage and gracefully wrap up the task once a budget is reached:当模型处理需要多次调用工具的长任务时，总令牌消耗量会显著增加。你可以将 `pause_after_compaction` 与压缩计数器结合使用，来估算累计消耗量，并在达到预算时妥善结束任务：

```
client = anthropic.Anthropic()
messages = [{"role": "user", "content": "Hello, Claude"}]
TRIGGER_THRESHOLD = 100_000
TOTAL_TOKEN_BUDGET = 3_000_000
n_compactions = 0

response = client.beta.messages.create(
    betas=["compact-2026-01-12"],
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=messages,
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": TRIGGER_THRESHOLD},
                "pause_after_compaction": True,
            }
        ]
    },
)

if response.stop_reason == "compaction":
    n_compactions += 1
    messages.append({"role": "assistant", "content": response.content})

    # Estimate total tokens consumed; prompt wrap-up if over budget
    if n_compactions * TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET:
        messages.append(
            {
                "role": "user",
                "content": "Please wrap up your current work and summarize the final state.",
            }
        )
```

## Working with compaction blocks 处理压缩块

When compaction is triggered, the API returns a `compaction` block at the start of the assistant response.触发压缩时，API 会在助手回复的开头返回一个 `compaction` 块。

A long-running conversation may result in multiple compactions. The last compaction block reflects the final state of the prompt, replacing content prior to it with the generated summary.一次长时间的对话可能会产生多次压缩操作。最后一个压缩块会反映提示词的最终状态，并将其之前的内容替换为生成的摘要。

```
{
  "content": [
    {
      "type": "compaction",
      "content": "Summary of the conversation: The user requested help building a web scraper..."
    },
    {
      "type": "text",
      "text": "Based on our conversation so far..."
    }
  ]
}
```

### Passing compaction blocks back 回传压缩块

You must pass the `compaction` block back to the API on subsequent requests to continue the conversation with the shortened prompt. The simplest approach is to append the entire response content to your messages:在后续的请求中，你必须将 `compaction` 块传回 API，以继续使用缩短后的提示词进行对话。最简单的方法是将整个响应内容附加到你的消息中：

```
ant beta:messages create --beta compact-2026-01-12 \
  --transform content --format jsonl <<'YAML' > content.json
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
YAML

# After receiving a response with a compaction block, append it as the
# assistant turn and continue the conversation
ant beta:messages create --beta compact-2026-01-12 <<YAML
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello, Claude
  - role: assistant
    content: $(cat content.json)
  - role: user
    content: Now add error handling
context_management:
  edits:
    - type: compact_20260112
YAML
```

When the API receives a `compaction` block, all content blocks before it are ignored. You can either:当 API 接收到 `compaction` 块时，其之前的所有内容块都将被忽略。你可以选择以下任一方式：

- Keep the original messages in your list and let the API handle removing the compacted content 保留列表中的原始消息，让 API 负责删除已压缩的内容
- Manually drop the compacted messages and only include the compaction block onwards 手动删除已压缩的消息，仅保留压缩块及之后的内容

### Streaming 流式处理

When streaming responses with compaction enabled, you'll receive a `content_block_start` event when compaction begins. The compaction block streams differently from text blocks. You'll receive a `content_block_start` event, followed by a single `content_block_delta` with the complete summary content (no intermediate streaming), and then a `content_block_stop` event.启用压缩后流式响应时，压缩开始时你会收到一个 `content_block_start` 事件。压缩块的流式传输方式与文本块不同。你会先收到一个 `content_block_start` 事件，随后是一个包含完整摘要内容的单个 `content_block_delta` （无中间流式传输），接着是一个 `content_block_stop` 事件。

```
ant beta:messages create --stream --format jsonl \
  --beta compact-2026-01-12 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
YAML
```

### Prompt caching 提示缓存

Compaction works well with [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). You can add a `cache_control` breakpoint on compaction blocks to cache the summarized content. The original compacted content is ignored.压缩与 [提示词缓存](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 配合效果良好。你可以在压缩块上添加一个 `cache_control` 断点来缓存汇总后的内容。原始的压缩内容将被忽略。

```
{
  "role": "assistant",
  "content": [
    {
      "type": "compaction",
      "content": "[summary text]",
      "cache_control": { "type": "ephemeral" }
    },
    {
      "type": "text",
      "text": "Based on our conversation..."
    }
  ]
}
```

#### Maximizing cache hits with system prompts利用系统提示词最大化缓存命中率

When compaction occurs, the summary becomes new content that needs to be written to the cache. Without additional cache breakpoints, this would also invalidate any cached system prompt, requiring it to be re-cached along with the compaction summary.当发生压缩时，摘要会成为需要写入缓存的新内容。如果没有额外的缓存断点，这还会使所有已缓存的系统提示失效，需要将其与压缩摘要一起重新缓存。

To maximize cache hit rates, add a `cache_control` breakpoint at the end of your system prompt. This keeps the system prompt cached separately from the conversation, so when compaction occurs:为了最大化缓存命中率，请在系统提示词的末尾添加一个 `cache_control` 断点。这会将系统提示词与对话分开缓存，因此在进行压缩时：

- The system prompt cache remains valid and is read from cache 系统提示缓存保持有效，并从缓存中读取
- Only the compaction summary needs to be written as a new cache entry 只有压缩摘要需要作为新的缓存条目写入

```
ant beta:messages create --beta compact-2026-01-12 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
system:
  - type: text
    text: You are a helpful coding assistant...
    cache_control:
      type: ephemeral
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
YAML
```

This approach is particularly beneficial for long system prompts, as they remain cached even across multiple compaction events throughout a conversation.这种方法对长系统提示词特别有益，因为即便是在整个对话过程中多次压缩事件，这些提示词仍会保持缓存状态。

## Understanding usage 理解用法

Compaction requires an additional sampling step, which contributes to rate limits and billing. The API returns detailed usage information in the response:压缩需要额外的采样步骤，这会对速率限制和计费产生影响。API 会在响应中返回详细的使用信息：

```
{
  "usage": {
    "input_tokens": 23000,
    "output_tokens": 1000,
    "iterations": [
      {
        "type": "compaction",
        "input_tokens": 180000,
        "output_tokens": 3500
      },
      {
        "type": "message",
        "input_tokens": 23000,
        "output_tokens": 1000
      }
    ]
  }
}
```

The `iterations` array shows usage for each sampling iteration. When compaction occurs, you'll see a `compaction` iteration followed by the main `message` iteration. The top-level `input_tokens` and `output_tokens` match the `message` iteration exactly in this example because there is only one non-compaction iteration. The final iteration's token counts reflect the effective context size after compaction.`iterations` 数组显示每个采样迭代的使用情况。发生压缩时，你会看到一个 `compaction` 迭代，随后是主 `message` 迭代。在本示例中，顶级的 `input_tokens` 和 `output_tokens` 与 `message` 迭代完全一致，因为只有一个非压缩迭代。最终迭代的标记数量反映了压缩后的有效上下文大小。

The top-level `input_tokens` and `output_tokens` do not include compaction iteration usage. They reflect the sum of all non-compaction iterations. To calculate total tokens consumed and billed for a request, sum across all entries in the `usage.iterations` array.顶级的 `input_tokens` 和 `output_tokens` 不包含压缩迭代的使用量。它们反映了所有非压缩迭代的总和。要计算某个请求消耗和计费的总令牌数，请对 `usage.iterations` 数组中的所有条目求和。

If you previously relied on `usage.input_tokens` and `usage.output_tokens` for cost tracking or auditing, you'll need to update your tracking logic to aggregate across `usage.iterations` when compaction is enabled. The `iterations` array is only populated when a new compaction is triggered during the request. Re-applying a previous `compaction` block incurs no additional compaction cost, and the top-level usage fields remain accurate in that case.如果你之前依赖 `usage.input_tokens` 和 `usage.output_tokens` 进行成本跟踪或审计，那么在启用压缩时，你需要更新跟踪逻辑，以跨 `usage.iterations` 进行聚合。 `iterations` 数组仅在请求期间触发新压缩时才会填充。重新应用之前的 `compaction` 块不会产生额外的压缩成本，此时顶级的用量字段仍保持准确。

## Combining with other features 与其他功能结合

### Server tools 服务器工具

When using server tools (like web search), the compaction trigger is checked at the start of each sampling iteration. Compaction may occur multiple times within a single request depending on your trigger threshold and the amount of output generated.使用服务器工具（如网络搜索）时，会在每次采样迭代开始时检查压缩触发器。根据你的触发器阈值和生成的输出量，在单个请求内可能会多次触发压缩。

### Token counting 令牌计数

The token counting endpoint (`/v1/messages/count_tokens`) applies existing `compaction` blocks in your prompt but does not trigger new compactions. Use it to check your effective token count after previous compactions:令牌计数端点（ `/v1/messages/count_tokens` ）会应用提示词中已有的 `compaction` 块，但不会触发新的压缩操作。你可以使用它来查看经过先前压缩后的有效令牌数量：

```
cat > request.yaml <<'YAML'
model: claude-opus-4-6
messages:
  - role: user
    content: Hello, Claude
context_management:
  edits:
    - type: compact_20260112
YAML

CURRENT=$(ant beta:messages count-tokens \
  --beta compact-2026-01-12 \
  --transform input_tokens --format yaml < request.yaml)

ORIGINAL=$(ant beta:messages count-tokens \
  --beta compact-2026-01-12 \
  --transform context_management.original_input_tokens \
  --format yaml < request.yaml)

printf 'Current tokens: %s\n' "$CURRENT"
printf 'Original tokens: %s\n' "$ORIGINAL"
```

## Examples 示例

Here's a complete example of a long-running conversation with compaction:下面是一个带压缩的长对话完整示例：

```
# The CLI handles individual turns; maintain the messages array in the
# calling script. See the SDK tabs for the full chat() loop. Single-turn
# request shape:
ant beta:messages create --beta compact-2026-01-12 \
  --transform 'content.#(type=="text").text' --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Help me build a Python web scraper
context_management:
  edits:
    - type: compact_20260112
      trigger:
        type: input_tokens
        value: 100000
YAML
```

Here's an example that uses `pause_after_compaction` to preserve the prior exchange and the current user message (three messages total) verbatim instead of summarizing them:下面是一个使用 `pause_after_compaction` 逐字保留先前对话和当前用户消息（共三条消息）而非对其进行总结的示例：

```
# The CLI handles individual turns; maintain the messages array in the
# calling script. See the SDK tabs for the full chat() loop with
# pause-and-preserve handling. Single-turn request shape:
ant beta:messages create --beta compact-2026-01-12 \
  --transform 'content.#(type=="text").text' --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
messages:
  - role: user
    content: Help me build a Python web scraper
context_management:
  edits:
    - type: compact_20260112
      trigger:
        type: input_tokens
        value: 100000
      pause_after_compaction: true
YAML
```

## Current limitations 当前限制

- **Same model for summarization:** The model specified in your request is used for summarization. There is no option to use a different (for example, cheaper) model for the summary.**用于摘要生成的相同模型：** 你请求中指定的模型将用于摘要生成。没有选项可以为摘要使用不同的（例如，成本更低的）模型。[Session memory compaction cookbook 会话内存压缩指南](https://platform.claude.com/cookbook/misc-session-memory-compaction)

[

Explore a practical implementation that manages long-running conversations with instant session memory compaction using background threading and prompt caching.探索一种实际实现方案，该方案借助后台线程和提示词缓存来管理长时对话，并实现即时的会话内存压缩。

](https://platform.claude.com/cookbook/misc-session-memory-compaction)[

Context windows 上下文窗口

Learn about context window sizes and management strategies.了解上下文窗口大小及管理策略。

](https://platform.claude.com/docs/en/build-with-claude/context-windows)[

Context editing 上下文编辑

Explore other strategies for managing conversation context like tool result clearing and thinking block clearing.探索其他管理对话上下文的策略，例如工具结果清理和思维块清理。

](https://platform.claude.com/docs/en/build-with-claude/context-editing)

Was this page helpful? 此页面是否有帮助？