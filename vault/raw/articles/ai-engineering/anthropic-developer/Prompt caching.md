---
title: "Prompt caching"
source: "https://platform.claude.com/docs/en/build-with-claude/prompt-caching"
author:
published:
created: 2026-04-16
description: "Claude API Documentation"
tags:
  - "clippings"
---
Prompt caching optimizes your API usage by allowing resuming from specific prefixes in your prompts. This significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements.提示词缓存通过允许从提示词中的特定前缀恢复，来优化你的 API 调用。这能显著减少重复性任务或包含固定元素的提示词的处理时间与成本。

This feature is eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.此功能符合零数据保留（ZDR）</b>的条件。当你的组织签订了零数据保留协议后，通过此功能发送的数据在API响应返回后不会被存储。

There are two ways to enable prompt caching:启用提示词缓存有两种方式：

- **[Automatic caching](#automatic-caching)**: Add a single `cache_control` field at the top level of your request. The system automatically applies the cache breakpoint to the last cacheable block and moves it forward as conversations grow. Best for multi-turn conversations where the growing message history should be cached automatically.**[自动缓存](#automatic-caching)** ：在请求的顶层添加单个 `cache_control` 字段。系统会自动将缓存断点应用于最后一个可缓存的块，并随着对话的进行向前移动该断点。最适用于需要自动缓存不断增长的消息历史的多轮对话。
- **[Explicit cache breakpoints](#explicit-cache-breakpoints)**: Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached.**[显式缓存断点](#explicit-cache-breakpoints)** ：将 `cache_control` 直接应用于各个内容块，以精确控制具体缓存内容。

The simplest way to start is with automatic caching:最简单的入门方式是使用自动缓存：

```
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the major themes in Pride and Prejudice."
      }
    ]
  }'
```

With automatic caching, the system caches all content up to and including the last cacheable block. On subsequent requests with the same prefix, cached content is reused automatically.启用自动缓存后，系统会缓存所有内容，直至并包含最后一个可缓存块。在后续使用相同前缀的请求中，缓存的内容将被自动复用。

---

## How prompt caching works 提示缓存的工作原理

When you send a request with prompt caching enabled:当你发送启用了提示缓存的请求时：

1. The system checks if a prompt prefix, up to a specified cache breakpoint, is already cached from a recent query.系统会检查截至指定缓存断点的提示前缀是否已来自最近的查询并完成缓存。
2. If found, it uses the cached version, reducing processing time and costs.如果找到，系统会使用缓存版本，从而减少处理时间和成本。
3. Otherwise, it processes the full prompt and caches the prefix once the response begins.否则，它会处理完整的提示词，并在响应开始时缓存前缀。

This is especially useful for: 这一点对以下情况特别有用：

- Prompts with many examples 包含大量示例的提示词
- Large amounts of context or background information 大量上下文或背景信息
- Repetitive tasks with consistent instructions 指令一致的重复性任务
- Long multi-turn conversations 长多轮对话

By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used.默认情况下，缓存的有效期为5分钟。每次使用缓存内容时，缓存都会免费刷新。

If you find that 5 minutes is too short, Anthropic also offers a 1-hour cache duration [at additional cost](#pricing).如果你发现5分钟的时长太短，Anthropic 还提供1小时的缓存时长， [需额外付费](#pricing) 。

For more information, see [1-hour cache duration](#1-hour-cache-duration).有关更多信息，请参阅 [1小时缓存时长](#1-hour-cache-duration) 。

**Prompt caching caches the full prefix 提示缓存会缓存完整前缀**

Prompt caching references the entire prompt - `tools`, `system`, and `messages` (in that order) up to and including the block designated with `cache_control`.提示缓存会引用整个提示词—— `tools` 、 `system` 和 `messages` （按此顺序），直至并包含用 `cache_control` 标记的块。

---

## Pricing 定价

Prompt caching introduces a new pricing structure. The table below shows the price per million tokens for each supported model:提示词缓存引入了全新的定价体系。下表列出了各支持模型的每百万令牌价格：

| Model 模型 | Base Input Tokens 基础输入令牌 | 5m Cache Writes 5分钟缓存写入 | 1h Cache Writes 1小时缓存写入 | Cache Hits & Refreshes 缓存命中与刷新 | Output Tokens 输出令牌 |
| --- | --- | --- | --- | --- | --- |
| Claude Opus 4.6 克劳德作品4.6 | $5 / MTok 5美元/百万令牌 | $6.25 / MTok 6.25美元/百万令牌 | $10 / MTok $10 / 百万令牌 | $0.50 / MTok $0.50 / 百万令牌 | $25 / MTok $25 / 百万令牌 |
| Claude Opus 4.5 克劳德作品4.5 | $5 / MTok 5美元/百万令牌 | $6.25 / MTok $6.25 / 百万令牌 | $10 / MTok $10 / 百万令牌 | $0.50 / MTok $0.50 / 百万令牌 | $25 / MTok $25 / 百万令牌 |
| Claude Opus 4.1 克劳德作品4.1 | $15 / MTok $15 / 百万令牌 | $18.75 / MTok $18.75 / 百万令牌 | $30 / MTok $30 / 百万令牌 | $1.50 / MTok 1.50美元/百万令牌 | $75 / MTok 75美元/百万令牌 |
| Claude Opus 4 克劳德作品4 | $15 / MTok $15 / 百万令牌 | $18.75 / MTok 18.75美元/百万令牌 | $30 / MTok 30美元/百万令牌 | $1.50 / MTok 1.50美元/百万令牌 | $75 / MTok $75 / 百万令牌 |
| Claude Sonnet 4.6 | $3 / MTok 3美元/百万令牌 | $3.75 / MTok 3.75美元/百万令牌 | $6 / MTok $6 / 百万令牌 | $0.30 / MTok $0.30 / 百万令牌 | $15 / MTok 15美元/百万令牌 |
| Claude Sonnet 4.5 Claude 索努 4.5 | $3 / MTok 3美元/百万令牌 | $3.75 / MTok 3.75美元/百万令牌 | $6 / MTok $6 / 百万令牌 | $0.30 / MTok 0.30美元/千令牌 | $15 / MTok $15 / 百万令牌 |
| Claude Sonnet 4 | $3 / MTok 3美元/百万令牌 | $3.75 / MTok 3.75美元/百万令牌 | $6 / MTok $6 / 百万令牌 | $0.30 / MTok 0.30美元/千令牌 | $15 / MTok $15 / 百万令牌 |
| Claude Sonnet 3.7 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations)) Claude Sonnet 3.7（ [已弃用](https://platform.claude.com/docs/en/about-claude/model-deprecations) ） | $3 / MTok 3美元/百万令牌 | $3.75 / MTok 3.75美元/百万令牌 | $6 / MTok $6 / 百万令牌 | $0.30 / MTok 0.30美元/千令牌 | $15 / MTok $15 / 百万令牌 |
| Claude Haiku 4.5 Claude 短诗 4.5 | $1 / MTok 1美元/千令牌 | $1.25 / MTok 1.25美元/千令牌 | $2 / MTok $2 / 百万令牌 | $0.10 / MTok $0.10 / 百万令牌 | $5 / MTok 5美元/百万令牌 |
| Claude Haiku 3.5 | $0.80 / MTok 0.80美元/千令牌 | $1 / MTok 1美元/千令牌 | $1.6 / MTok $1.6 / 百万令牌 | $0.08 / MTok 0.08美元/百万令牌 | $4 / MTok 4美元/百万令牌 |
| Claude Opus 3 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations)) Claude Opus 3（ [已弃用](https://platform.claude.com/docs/en/about-claude/model-deprecations) ） | $15 / MTok $15 / 百万令牌 | $18.75 / MTok $18.75 / 百万令牌 | $30 / MTok 30美元/百万令牌 | $1.50 / MTok 1.50美元/百万令牌 | $75 / MTok $75 / 百万令牌 |
| Claude Haiku 3 | $0.25 / MTok 0.25美元/百万令牌 | $0.30 / MTok 0.30美元/千令牌 | $0.50 / MTok $0.50 / 百万令牌 | $0.03 / MTok $0.03 / 百万令牌 | $1.25 / MTok 1.25美元/百万令牌 |

The table above reflects the following pricing multipliers for prompt caching:上表反映了提示缓存的以下定价乘数：

- 5-minute cache write tokens are 1.25 times the base input tokens price 5分钟缓存写入令牌的价格是基础输入令牌价格的1.25倍
- 1-hour cache write tokens are 2 times the base input tokens price 1小时缓存写入令牌的价格是基础输入令牌价格的2倍
- Cache read tokens are 0.1 times the base input tokens price 缓存读取令牌的价格是基础输入令牌价格的0.1倍

These multipliers stack with other pricing modifiers such as the Batch API discount and data residency. See [pricing](https://platform.claude.com/docs/en/about-claude/pricing) for full details.这些乘数会与批量API折扣和数据驻留等其他定价调整项叠加生效。完整详情请参见 [定价](https://platform.claude.com/docs/en/about-claude/pricing) 。

---

## Supported models 支持的模型

Prompt caching (both automatic and explicit) is supported on all [active Claude models](https://platform.claude.com/docs/en/about-claude/models/overview).所有 [可用的 Claude 模型](https://platform.claude.com/docs/en/about-claude/models/overview) 均支持提示缓存（包括自动缓存和显式缓存）。

---

## Automatic caching 自动缓存

Automatic caching is the simplest way to enable prompt caching. Instead of placing `cache_control` on individual content blocks, add a single `cache_control` field at the top level of your request body. The system automatically applies the cache breakpoint to the last cacheable block.自动缓存是启用提示缓存的最简单方式。无需在单个内容块上设置 `cache_control` ，只需在请求体的顶层添加一个 `cache_control` 字段即可。系统会自动将缓存断点应用到最后一个可缓存的块。

```
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are a helpful assistant that remembers our conversation.",
    "messages": [
      {"role": "user", "content": "My name is Alex. I work on machine learning."},
      {"role": "assistant", "content": "Nice to meet you, Alex! How can I help with your ML work today?"},
      {"role": "user", "content": "What did I say I work on?"}
    ]
  }'
```

### How automatic caching works in multi-turn conversations多轮对话中自动缓存的工作原理

With automatic caching, the cache point moves forward automatically as conversations grow. Each new request caches everything up to the last cacheable block, and previous content is read from cache.启用自动缓存后，缓存点会随着对话的推进自动后移。每个新请求都会缓存到最后一个可缓存块的所有内容，而之前的内容则从缓存中读取。

| Request 请求 | Content 内容 | Cache behavior 缓存行为 |
| --- | --- | --- |
| Request 1 请求 1 | System 系统   \+ User(1) + Asst(1) +用户（1）+分支（1）   \+ **User(2)** ◀ cache \+ **用户(2)** ◀ 缓存 | Everything written to cache 所有内容都写入缓存 |
| Request 2 请求2 | System 系统   \+ User(1) + Asst(1) +用户（1）+分支（1）   \+ User(2) + Asst(2) +用户（2）+Ast（2）   \+ **User(3)** ◀ cache \+ **用户(3)** ◀ 缓存 | System through User(2) read from cache; 系统通过用户2读取缓存；   Asst(2) + User(3) written to cache Asst(2) + User(3) 写入缓存 |
| Request 3 请求3 | System 系统   \+ User(1) + Asst(1) +用户（1）+分支（1）   \+ User(2) + Asst(2) +用户（2）+Ast（2）   \+ User(3) + Asst(3) +用户（3）+分支（3）   \+ **User(4)** ◀ cache \+ **用户(4)** ◀ 缓存 | System through User(3) read from cache; 系统通过用户(3)从缓存读取；   Asst(3) + User(4) written to cache 助手(3) + 用户(4) 被写入缓存 |

The cache breakpoint automatically moves to the last cacheable block in each request, so you don't need to update any `cache_control` markers as the conversation grows.缓存断点会自动移动到每个请求中最后一个可缓存的块，因此随着对话的进行，你无需更新任何 `cache_control` 标记。

### TTL support 生存时间支持

By default, automatic caching uses a 5-minute TTL. You can specify a 1-hour TTL at 2x the base input token price:默认情况下，自动缓存使用 5 分钟的生存时间（TTL）。你可以指定 1 小时的生存时间（TTL），价格为基础输入令牌价格的 2 倍：

```
{ "cache_control": { "type": "ephemeral", "ttl": "1h" } }
```

### Combining with block-level caching 与块级缓存结合使用

Automatic caching is compatible with [explicit cache breakpoints](#explicit-cache-breakpoints). When used together, the automatic cache breakpoint uses one of the 4 available breakpoint slots.自动缓存与 [显式缓存断点](#explicit-cache-breakpoints) 兼容。同时使用时，自动缓存断点会占用 4 个可用断点槽位中的一个。

This lets you combine both approaches. For example, use explicit breakpoints to cache your system prompt and tools independently, while automatic caching handles the conversation:这让你可以将两种方法结合起来。例如，使用显式断点独立缓存系统提示词和工具，同时通过自动缓存来处理对话：

```
{
  "model": "claude-opus-4-6",
  "max_tokens": 1024,
  "cache_control": { "type": "ephemeral" },
  "system": [
    {
      "type": "text",
      "text": "You are a helpful assistant.",
      "cache_control": { "type": "ephemeral" }
    }
  ],
  "messages": [{ "role": "user", "content": "What are the key terms?" }]
}
```

### What stays the same 保持不变的内容

Automatic caching uses the same underlying caching infrastructure. Pricing, minimum token thresholds, context ordering requirements, and the 20-block lookback window all apply the same as with explicit breakpoints.自动缓存使用相同的底层缓存基础设施。定价、最小令牌阈值、上下文排序要求以及20个块的回溯窗口均与显式断点的规则完全相同。

### Edge cases 边缘情况

- If the last block already has an explicit `cache_control` with the same TTL, automatic caching is a no-op.如果最后一个块已具有相同 TTL 的显式 `cache_control` ，则自动缓存为无操作。
- If the last block has an explicit `cache_control` with a different TTL, the API returns a 400 error.如果最后一个块带有显式的 `cache_control` 且 TTL 不同，API 将返回 400 错误。
- If 4 explicit block-level breakpoints already exist, the API returns a 400 error (no slots left for automatic caching).如果已存在 4 个显式的块级断点，API 将返回 400 错误（自动缓存无剩余可用槽位）。
- If the last block is not eligible as an automatic cache breakpoint target, the system silently walks backwards to find the nearest eligible block. If none is found, caching is skipped.如果最后一个区块不符合自动缓存断点目标的条件，系统会静默地向后查找最近的符合条件的区块。如果未找到任何区块，则跳过缓存操作。

Automatic caching is available on the Claude API and Azure AI Foundry (preview). Support for Amazon Bedrock and Google Vertex AI is coming later.Claude API 以及 Azure AI 创新平台（预览版）支持自动缓存。亚马逊 Bedrock 和谷歌 Vertex AI 的支持即将推出。

---

## Explicit cache breakpoints 显式缓存断点

For more control over caching, you can place `cache_control` directly on individual content blocks. This is useful when you need to cache different sections that change at different frequencies, or need fine-grained control over exactly what gets cached.若要对缓存进行更精细的控制，你可以直接在各个内容块上设置 `cache_control` 。当你需要缓存不同更新频率的部分，或需要对缓存内容进行精准控制时，这种方式非常实用。

### Structuring your prompt 组织你的提示词

Place static content (tool definitions, system instructions, context, examples) at the beginning of your prompt. Mark the end of the reusable content for caching using the `cache_control` parameter.将静态内容（工具定义、系统指令、上下文、示例）放在提示符的开头。使用 `cache_control` 参数标记可重用内容的末尾以进行缓存。

Cache prefixes are created in the following order: `tools`, `system`, then `messages`. This order forms a hierarchy where each level builds upon the previous ones.缓存前缀按以下顺序创建： `tools` 、 `system` ，然后是 `messages` 。该顺序形成了一个层级结构，每个层级都建立在前一级的基础之上。

#### How automatic prefix checking works 自动前缀检查的工作原理

You can use just one cache breakpoint at the end of your static content, and the system will automatically find the longest prefix that a prior request already wrote to the cache. Understanding how this works helps you optimize your caching strategy.你可以在静态内容末尾仅使用一个缓存断点，系统会自动找到先前请求已写入缓存的最长前缀。理解其工作原理有助于优化缓存策略。

**Three core principles: 三大核心原则：**

1. **Cache writes happen only at your breakpoint.** Marking a block with `cache_control` writes exactly one cache entry: a hash of the prefix ending at that block. The system does not write entries for any earlier position. Because the hash is cumulative, covering everything up to and including the breakpoint, changing any block at or before the breakpoint produces a different hash on the next request.**缓存写入仅在你的断点处发生。** 使用 `cache_control` 标记一个块时，只会写入一个缓存项：即该块之前前缀的哈希值。系统不会为任何更早的位置写入条目。由于该哈希是累积性的，涵盖了直至断点且包含断点的所有内容，因此更改断点处或断点之前的任何块，都会在下一次请求中生成不同的哈希值。
2. **Cache reads look backward for entries that prior requests wrote.** On each request the system computes the prefix hash at your breakpoint and checks for a matching cache entry. If none exists, it walks backward one block at a time, checking whether the prefix hash at each earlier position matches something already in the cache. It is looking for prior writes, not for stable content.**缓存读取会向后查找先前请求写入的条目。** 在每次请求时，系统会计算断点处的前缀哈希，并检查是否存在匹配的缓存条目。如果不存在，系统会一次向后遍历一个数据块，检查每个更早位置的前缀哈希是否与缓存中已有的内容匹配。它查找的是先前的写入内容，而非稳定内容。
3. **The lookback window is 20 blocks.** The system checks at most 20 positions per breakpoint, counting the breakpoint itself as the first. If the system finds no matching entry in that window, checking stops (or resumes from the next explicit breakpoint, if any).**回溯窗口为20个区块。** 系统在每个断点最多检查20个位置，将断点本身计为第一个位置。如果系统在该窗口中未找到匹配项，则停止检查（或从下一个显式断点恢复检查，若存在）。

**Example: Lookback in a growing conversation 示例：持续对话中的回溯查找**

You append new blocks each turn and set `cache_control` on the final block of each request:你在每一轮都追加新的区块，并在每次请求的最后一个区块上设置缓存控制</b>：

- **Turn 1:** 10 blocks, breakpoint on block 10. No prior cache entries exist. The system writes an entry at block 10.**轮次1：** 10个块，在第10块处设置断点。此前不存在任何缓存条目。系统在第10块处写入一个条目。
- **Turn 2:** 15 blocks, breakpoint on block 15. Block 15 has no entry, so the system walks back to block 10 and finds the turn-1 entry. Cache hit at block 10; the system processes only blocks 11 through 15 fresh and writes a new entry at block 15.**第2轮：** 15个块，第15块处设置断点。第15块无入口，系统回溯至第10块并找到第1轮的入口。第10块缓存命中；系统仅重新处理第11至15块，并在第15块写入新入口。
- **Turn 3:** 35 blocks, breakpoint on block 35. The system checks 20 positions (blocks 35 through 16) and finds nothing. The turn-2 entry at block 15 is one position outside the window, so there is no cache hit. Adding a second breakpoint at block 15 starts a second lookback window there, which finds the turn-2 entry.**回合3：** 35个数据块，在第35个数据块处设置断点。系统检查20个位置（第35个至第16个数据块），未找到任何内容。第15个数据块处的回合2条目位于窗口外一个位置，因此未命中缓存。在第15个数据块处添加第二个断点，会在该位置启动第二个回溯窗口，从而找到该回合2条目。

**Common mistake: Breakpoint on content that changes every request 常见错误：在每次请求都会变化的内容上设置断点**

Your prompt has a large static system context (blocks 1 through 5) followed by a per-request block containing a timestamp and the user message (block 6). You set `cache_control` on block 6:你的提示词包含一段较大的静态系统上下文（第1至第5块），随后是每个请求对应的块，其中包含时间戳和用户消息（第6块）。你在第6块上设置了 `cache_control` ：

- **Request 1:** Cache write at block 6. The hash includes the timestamp.**请求 1：** 在第 6 块写入缓存。哈希值包含时间戳。
- **Request 2:** The timestamp differs, so the prefix hash at block 6 differs. The lookback walks through blocks 5, 4, 3, 2, and 1, but the system never wrote an entry at any of those positions. No cache hit. You pay for a fresh cache write on every request and never get a read.**请求 2：** 时间戳存在差异，因此第 6 个区块的前缀哈希值也不同。回溯遍历了第 5、4、3、2 和 1 个区块，但系统从未在这些位置写入过任何条目。未命中缓存。每次请求都需要为全新的缓存写入付费，却永远无法读取到数据。

The lookback does not find stable content behind your breakpoint and cache it. It finds entries that prior requests already wrote, and writes happen only at breakpoints. Move `cache_control` to block 5, the last block that stays the same across requests, and every subsequent request reads the cached prefix. [Automatic caching](#automatic-caching) hits the same trap: it places the breakpoint on the last cacheable block, which in this structure is the one that changes every request, so use an explicit breakpoint on block 5 instead.回溯功能不会在你的断点后方找到稳定内容并进行缓存。它会查找先前请求已写入的条目，而写入操作仅在断点处发生。将 `cache_control` 移至第5块——这是所有请求中保持不变的最后一块，此后的每个请求都会读取缓存的前缀。 [自动缓存](#automatic-caching) 也会陷入同样的误区：它会将断点设置在最后一个可缓存块上，而在该结构中，这个块会随每个请求发生变化，因此请改为对第5块使用显式断点。

**Key takeaway:** Place `cache_control` on the last block whose prefix is identical across the requests you want to share a cache. In a growing conversation the final block works as long as each turn adds fewer than 20 blocks: earlier content never changes, so the next request's lookback finds the prior write. For a prompt with a varying suffix (timestamps, per-request context, the incoming message), place the breakpoint at the end of the static prefix, not on the varying block.**核心要点：** 将 `cache_control` 应用于所有你希望共享缓存的请求中前缀完全相同的最后一个块。在不断扩展的对话中，只要每一轮新增的块数少于20个，最后一个块即可生效：早期内容永远不会改变，因此下一个请求的回溯查找能定位到之前的写入操作。对于后缀不固定的提示词（时间戳、每个请求的上下文、传入的消息），请将断点设置在静态前缀的末尾，而非不固定的块上。

#### When to use multiple breakpoints 何时使用多个断点

You can define up to 4 cache breakpoints if you want to:如果需要，你最多可以定义 4 个缓存断点：

- Cache different sections that change at different frequencies (for example, tools rarely change, but context updates daily) 对不同频率变化的不同部分进行缓存（例如，工具很少变化，但上下文每天更新）
- Have more control over exactly what gets cached 更精准地控制具体要缓存的内容
- Ensure a cache hit when a growing conversation pushes your breakpoint 20 or more blocks past the last cache write 当不断增长的对话使你的断点比上次缓存写入的位置超出 20 个或更多块时，确保触发缓存命中

**Important limitation:** The lookback can only find entries that earlier requests already wrote. If a growing conversation pushes your breakpoint 20 or more blocks past the last write, the lookback window misses it. Add a second breakpoint closer to that position from the start so a write accumulates there before you need it.**重要限制：** 回溯功能只能找到之前的请求已经写入的条目。如果持续增长的对话将你的断点推至最后写入位置之后超过 20 个区块，回溯窗口就会遗漏该位置。请在起始位置附近添加第二个断点，以便在你需要之前，写入操作能在那里累积。

### Understanding cache breakpoint costs 理解缓存断点成本

**Cache breakpoints themselves don't add any cost.** You are only charged for:**缓存断点本身不会产生任何额外成本。** 仅对以下项目收费：

- **Cache writes**: When new content is written to the cache (25% more than base input tokens for 5-minute TTL) **缓存写入** ：当新内容被写入缓存时（5分钟生存时间内，比基础输入令牌多25%）
- **Cache reads**: When cached content is used (10% of base input token price) **缓存读取** ：使用缓存内容时（为基础输入代币价格的10%）
- **Regular input tokens**: For any uncached content **常规输入令牌** ：适用于所有未缓存的内容

Adding more `cache_control` breakpoints doesn't increase your costs - you still pay the same amount based on what content is actually cached and read. The breakpoints simply give you control over what sections can be cached independently.添加更多的 `cache_control` 断点并不会增加你的成本——你仍需根据实际缓存和读取的内容支付相同的费用。这些断点只是让你能够独立控制哪些部分可以被缓存。

---

## Caching strategies and considerations缓存策略与注意事项

### Cache limitations 缓存限制

The minimum cacheable prompt length is:可缓存提示词的最小长度为：

- 4096 tokens for [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.6, and Claude Opus 4.5 4096 个 token 适用于 [Claude Mythos Preview](https://anthropic.com/glasswing) 、Claude Opus 4.6 以及 Claude Opus 4.5
- 2048 tokens for Claude Sonnet 4.6 2048 个 token 适用于 Claude Sonnet 4.6
- 1024 tokens for Claude Sonnet 4.5, Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4, and Claude Sonnet 3.7 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations)) Claude Sonnet 4.5、Claude Opus 4.1、Claude Opus 4、Claude Sonnet 4 以及 Claude Sonnet 3.7（ [已弃用](https://platform.claude.com/docs/en/about-claude/model-deprecations) ）支持 1024 个 token
- 4096 tokens for Claude Haiku 4.5 4096 个 token 适用于 Claude Haiku 4.5
- 2048 tokens for Claude Haiku 3.5 ([deprecated](https://platform.claude.com/docs/en/about-claude/model-deprecations)) and Claude Haiku 3 2048 个 token，适用于 Claude Haiku 3.5（ [已弃用](https://platform.claude.com/docs/en/about-claude/model-deprecations) ）和 Claude Haiku 3

Shorter prompts cannot be cached, even if marked with `cache_control`. Any requests to cache fewer than this number of tokens will be processed without caching, and no error is returned. To verify whether a prompt was cached, check the response usage [fields](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#tracking-cache-performance): if both `cache_creation_input_tokens` and `cache_read_input_tokens` are 0, the prompt was not cached (likely because it did not meet the minimum length requirement).较短的提示词无法被缓存，即使标记了 `cache_control` 也是如此。任何要求缓存的令牌数量少于此数值的请求都将在不进行缓存的情况下处理，且不会返回错误。要验证提示词是否已被缓存，请查看响应使用情况的 [字段](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#tracking-cache-performance) ：如果 `cache_creation_input_tokens` 和 `cache_read_input_tokens` 均为0，则说明提示词未被缓存（原因很可能是未达到最小长度要求）。

If your prompt falls just short of the minimum for the model you are using, expanding the cached content to reach the threshold is often worthwhile. Cache reads cost significantly less than uncached input tokens, so reaching the minimum can reduce costs for frequently reused prompts.如果你的提示词刚好达不到所用模型的最低要求，将缓存内容扩充至达到该阈值通常是值得的。缓存读取的成本远低于未缓存的输入令牌，因此达到最低要求能降低频繁复用提示词的成本。

For concurrent requests, note that a cache entry only becomes available after the first response begins. If you need cache hits for parallel requests, wait for the first response before sending subsequent requests.对于并发请求，请注意缓存条目仅在第一个响应开始后才可用。如果需要并行请求能够命中缓存，请等待第一个响应后再发送后续请求。

Currently, "ephemeral" is the only supported cache type, which by default has a 5-minute lifetime.目前，“临时”是唯一受支持的缓存类型，其默认生命周期为5分钟。

### What can be cached 哪些内容可以被缓存

Most blocks in the request can be cached. This includes:请求中的大多数块都可以被缓存，其中包括：

- Tools: Tool definitions in the `tools` array 工具： `tools` 数组中的工具定义
- System messages: Content blocks in the `system` array 系统消息： `system` 数组中的内容块
- Text messages: Content blocks in the `messages.content` array, for both user and assistant turns 短信： `messages.content` 数组中的内容块，适用于用户和助手的对话回合
- Images & Documents: Content blocks in the `messages.content` array, in user turns 图片与文档：用户轮次中 `messages.content` 数组内的内容块
- Tool use and tool results: Content blocks in the `messages.content` array, in both user and assistant turns 工具使用与工具结果：用户和助手回合的 `messages.content` 数组中的内容块

Each of these elements can be cached, either automatically or by marking them with `cache_control`.这些元素中的每一个都可以进行缓存，既可以自动缓存，也可以通过用 `cache_control` 标记它们来实现。

### What cannot be cached 无法缓存的内容

While most request blocks can be cached, there are some exceptions:虽然大多数请求块都可以被缓存，但也存在一些例外情况：

- Thinking blocks cannot be cached directly with `cache_control`. However, thinking blocks CAN be cached alongside other content when they appear in previous assistant turns. When cached this way, they DO count as input tokens when read from cache.思考块无法直接使用 `cache_control` 进行缓存。不过，当思考块出现在之前的助手回复中时，可以与其他内容一起缓存。以这种方式缓存后，从缓存中读取时它们会计入输入令牌数量。
- Sub-content blocks (like [citations](https://platform.claude.com/docs/en/build-with-claude/citations)) themselves cannot be cached directly. Instead, cache the top-level block.子内容块（如 [引用](https://platform.claude.com/docs/en/build-with-claude/citations) ）本身无法直接缓存。请改为缓存顶级块。
	In the case of citations, the top-level document content blocks that serve as the source material for citations can be cached. This allows you to use prompt caching with citations effectively by caching the documents that citations will reference.在引用场景下，可对作为引用源素材的顶级文档内容块进行缓存。通过缓存引用将要指向的文档，你就能高效地将提示缓存与引用功能结合使用。
- Empty text blocks cannot be cached.空文本块无法被缓存。

### What invalidates the cache 是什么会使缓存失效

Modifications to cached content can invalidate some or all of the cache.对缓存内容的修改可能会使部分或全部缓存失效。

As described in [Structuring your prompt](#structuring-your-prompt), the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels.如 [构建提示词](#structuring-your-prompt) 中所述，缓存遵循以下层级： `tools` → `system` → `messages` 。每个层级的更改都会使该层级及所有后续层级失效。

The following table shows which parts of the cache are invalidated by different types of changes. ✘ indicates that the cache is invalidated, while ✓ indicates that the cache remains valid.下表展示了不同类型的更改会使缓存的哪些部分失效。✘ 表示缓存失效，✓ 表示缓存保持有效。

| What changes 哪些更改 | Tools cache 工具缓存 | System cache 系统缓存 | Messages cache 消息缓存 | Impact 影响 |
| --- | --- | --- | --- | --- |
| **Tool definitions 工具定义** | ✘ | ✘ | ✘ | Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache 修改工具定义（名称、描述、参数）会使整个缓存失效 |
| **Web search toggle 网页搜索开关** | ✓ | ✘ | ✘ | Enabling/disabling web search modifies the system prompt 启用或禁用网络搜索会修改系统提示 |
| **Citations toggle 引用切换** | ✓ | ✘ | ✘ | Enabling/disabling citations modifies the system prompt 启用或禁用引用会修改系统提示 |
| **Speed setting 速度设置** | ✓ | ✘ | ✘ | Switching between [`speed: "fast"` and standard speed](https://platform.claude.com/docs/en/build-with-claude/fast-mode) invalidates system and message caches 在 [`speed: "fast"` 与标准速度](https://platform.claude.com/docs/en/build-with-claude/fast-mode) 之间切换会使系统缓存和消息缓存失效 |
| **Tool choice 工具选择** | ✓ | ✓ | ✘ | Changes to `tool_choice` parameter only affect message blocks 对 `tool_choice` 参数的修改仅影响消息块 |
| **Images 图片** | ✓ | ✓ | ✘ | Adding/removing images anywhere in the prompt affects message blocks 在提示词的任意位置添加或删除图片都会影响消息块 |
| **Thinking parameters 思考参数** | ✓ | ✓ | ✘ | Changes to extended thinking settings (enable/disable, budget) affect message blocks 扩展思考设置的更改（启用/禁用、预算）会影响消息块 |
| **Non-tool results passed to extended thinking requests 非工具结果传递至扩展思考请求** | ✓ | ✓ | ✘ | When non-tool results are passed in requests while extended thinking is enabled, all previously-cached thinking blocks are stripped from context, and any messages in context that follow those thinking blocks are removed from the cache. For more details, see [Caching with thinking blocks](#caching-with-thinking-blocks).当启用扩展思考功能且在请求中传入非工具结果时，所有先前缓存的思考块都会从上下文中移除，并且缓存中那些思考块之后的所有消息也会被删除。有关更多详细信息，请参阅 [带思考块的缓存](#caching-with-thinking-blocks) 。 |

### Tracking cache performance 跟踪缓存性能

Monitor cache performance using these API response fields, within `usage` in the response (or `message_start` event if [streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)):使用以下 API 响应字段监控缓存性能，需参考响应中的 `usage` （若为 [流式传输](https://platform.claude.com/docs/en/build-with-claude/streaming) ，则参考 `message_start` 事件）：

- `cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry.`cache_creation_input_tokens` ：创建新条目时写入缓存的令牌数。
- `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request.`cache_read_input_tokens` ：为此请求从缓存中检索的令牌数。
- `input_tokens`: Number of input tokens which were not read from or used to create a cache (that is, tokens after the last cache breakpoint).`input_tokens` ：未从缓存读取或未用于创建缓存的输入令牌数量（即最后一个缓存断点之后的令牌）。

**Understanding the token breakdown 理解令牌细分**

The `input_tokens` field represents only the tokens that come **after the last cache breakpoint** in your request - not all the input tokens you sent.`input_tokens` 字段仅表示你的请求中 **最后一个缓存断点之后** 的标记，而非你发送的所有输入标记。

To calculate total input tokens: 计算总输入令牌数：

```
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens总输入令牌数 = 缓存读取输入令牌数 + 缓存创建输入令牌数 + 输入令牌数
```

**Spatial explanation: 空间说明：**

- `cache_read_input_tokens` = tokens before breakpoint already cached (reads) `cache_read_input_tokens` = 断点前已缓存的令牌（读取）
- `cache_creation_input_tokens` = tokens before breakpoint being cached now (writes) `cache_creation_input_tokens` = 断点前当前正在被缓存的令牌（写入操作）
- `input_tokens` = tokens after your last breakpoint (not eligible for cache) `input_tokens` = 上一个断点之后的令牌（不符合缓存条件）

**Example:** If you have a request with 100,000 tokens of cached content (read from cache), 0 tokens of new content being cached, and 50 tokens in your user message (after the cache breakpoint):**示例：** 假设你的请求中有 100,000 个标记的缓存内容（从缓存中读取）、0 个标记的新缓存内容，且用户消息中（缓存断点之后）有 50 个标记：

- `cache_read_input_tokens`: 100,000 `cache_read_input_tokens` ：100,000
- `cache_creation_input_tokens`: 0 `cache_creation_input_tokens` ：0
- `input_tokens`: 50 `input_tokens` ：50
- **Total input tokens processed**: 100,050 tokens **已处理的总输入令牌数** ：100,050 个令牌

This is important for understanding both costs and rate limits, as `input_tokens` will typically be much smaller than your total input when using caching effectively.这一点对于理解成本和速率限制都很重要，因为在有效使用缓存时， `input_tokens` 通常会远小于你的总输入量。

### Caching with thinking blocks 结合思考块进行缓存

When using [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) with prompt caching, thinking blocks have special behavior:在将 [扩展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) 与提示词缓存配合使用时，思考块具有特殊行为：

**Automatic caching alongside other content**: While thinking blocks cannot be explicitly marked with `cache_control`, they get cached as part of the request content when you make subsequent API calls with tool results. This commonly happens during tool use when you pass thinking blocks back to continue the conversation.**与其他内容一同自动缓存** ：尽管思考块无法通过 `cache_control` 显式标记，但当你借助工具结果发起后续 API 调用时，它们会作为请求内容的一部分被缓存。这种情况通常发生在你回传思考块以继续对话的工具使用过程中。

**Input token counting**: When thinking blocks are read from cache, they count as input tokens in your usage metrics. This is important for cost calculation and token budgeting.**输入令牌计数** ：当从缓存中读取思考块时，它们会计入你的使用指标中的输入令牌。这对于成本计算和令牌预算编制至关重要。

**Cache invalidation patterns**: **缓存失效模式** ：

- Cache remains valid when only tool results are provided as user messages 仅将工具结果作为用户消息提供时，缓存保持有效
- Cache gets invalidated when non-tool-result user content is added, causing all previous thinking blocks to be stripped 添加非工具结果的用户内容时，缓存会失效，导致所有先前的思考块被清除
- This caching behavior occurs even without explicit `cache_control` markers 即使没有显式的 `cache_control` 标记，这种缓存行为也会生效

For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).有关缓存失效的更多详细信息，请参阅 [什么会使缓存失效](#what-invalidates-the-cache) 。

**Example with tool use**: **结合工具使用的示例** ：

```
Request 1: User: "What's the weather in Paris?"
Response: [thinking_block_1] + [tool_use block 1]

Request 2:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
Response: [thinking_block_2] + [text block 2]
# Request 2 caches its request content (not the response)
# The cache includes: user message, thinking_block_1, tool_use block 1, and tool_result_1

Request 3:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
# Non-tool-result user block causes all thinking blocks to be ignored
# This request is processed as if thinking blocks were never present请求1：用户：“巴黎的天气如何？”
回复：[思考块1] + [工具调用块1]
请求2：用户：["巴黎的天气如何？"]，助手：[思考块1] + [工具调用块1]，用户：[工具结果1，缓存=True]
回复：[思考块2] + [文本块2]
# 请求2缓存其请求内容（非回复）
# 缓存包含：用户消息、思考块1、工具调用块1和工具结果1
请求3：用户：["巴黎的天气如何？"]，助手：[思考块1] + [工具调用块1]，用户：[工具结果1，缓存=True]，助手：[思考块2] + [文本块2]，用户：[文本回复，缓存=True]
# 非工具结果的用户块会导致所有思考块被忽略
# 该请求的处理方式等同于思考块从未存在过
```

When a non-tool-result user block is included, it designates a new assistant loop and all previous thinking blocks are removed from context.当包含非工具结果的用户块时，它会指定一个新的助手循环，并且所有先前的思考块都会从上下文中移除。

For more detailed information, see the [extended thinking documentation](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior).有关更详细的信息，请参阅 [扩展思考文档](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior) 。

### Cache storage and sharing 缓存存储与共享

Starting February 5, 2026, prompt caching will use workspace-level isolation instead of organization-level isolation. Caches will be isolated per workspace, ensuring data separation between workspaces within the same organization. This change applies to the Claude API and Azure AI Foundry (preview); Amazon Bedrock and Google Vertex AI will maintain organization-level cache isolation. If you use multiple workspaces, review your caching strategy to account for this change.自2026年2月5日起，提示缓存将采用工作区级隔离，而非组织级隔离。缓存将按工作区级进行隔离，确保同一组织内不同工作区之间的数据分离。此变更适用于Claude API和Azure AI Foundry（预览版）；Amazon Bedrock和Google Vertex AI将维持组织级缓存隔离。如果你使用多个工作区，请查看你的缓存策略以适应这一变更。

- **Organization Isolation**: Caches are isolated between organizations. Different organizations never share caches, even if they use identical prompts.**组织隔离** ：不同组织之间的缓存相互隔离。即便使用相同的提示词，不同组织也绝不会共享缓存。
- **Exact Matching**: Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control.**精确匹配** ：缓存命中要求提示片段100%完全一致，包括所有文本和图片，直至并包含标有缓存控制的块。
- **Output Token Generation**: Prompt caching has no effect on output token generation. The response you receive will be identical to what you would get if prompt caching was not used.**输出令牌生成** ：提示缓存对输出令牌生成没有影响。你收到的响应将与不使用提示缓存时获得的响应完全相同。

### Best practices for effective caching高效缓存的最佳实践

To optimize prompt caching performance:为优化提示词缓存性能：

- Start with [automatic caching](#automatic-caching) for multi-turn conversations. It handles breakpoint management automatically.从 [自动缓存](#automatic-caching) 开始，适用于多轮对话。它会自动处理断点管理。
- Use [explicit block-level breakpoints](#explicit-cache-breakpoints) when you need to cache different sections with different change frequencies.当你需要以不同的更改频率缓存不同部分时，请使用 [显式块级断点](#explicit-cache-breakpoints) 。
- Cache stable, reusable content like system instructions, background information, large contexts, or frequent tool definitions.缓存稳定且可重复使用的内容，例如系统指令、背景信息、大型上下文或频繁使用的工具定义。
- Place cached content at the prompt's beginning for best performance.为获得最佳性能，请将缓存内容放在提示词的开头。
- Use cache breakpoints strategically to separate different cacheable prefix sections.策略性地使用缓存断点来分隔不同的可缓存前缀部分。
- Place the breakpoint on the last block that stays identical across requests. For a prompt with a static prefix and a varying suffix (timestamps, per-request context, the incoming message), that is the end of the prefix, not the varying block.将断点设置在所有请求中保持不变的最后一个代码块上。对于带有静态前缀和动态后缀（时间戳、每次请求的上下文、传入消息）的提示词，断点应位于前缀的末尾，而非动态代码块的位置。
- Regularly analyze cache hit rates and adjust your strategy as needed.定期分析缓存命中率，并根据需要调整你的策略。

### Optimizing for different use cases 针对不同使用场景进行优化

Tailor your prompt caching strategy to your scenario:根据你的使用场景定制提示词缓存策略：

- Conversational agents: Reduce cost and latency for extended conversations, especially those with long instructions or uploaded documents.对话式智能体：降低长对话的成本和延迟，尤其是那些包含长指令或上传文档的对话。
- Coding assistants: Improve autocomplete and codebase Q&A by keeping relevant sections or a summarized version of the codebase in the prompt.代码助手：通过在提示词中保留相关代码库部分或代码库的摘要版本，改进自动完成功能和代码库问答能力。
- Large document processing: Incorporate complete long-form material including images in your prompt without increasing response latency.大文档处理：在提示词中纳入包含图片在内的完整长文本内容，同时不增加响应延迟。
- Detailed instruction sets: Share extensive lists of instructions, procedures, and examples to fine-tune Claude's responses. Developers often include an example or two in the prompt, but with prompt caching you can get even better performance by including 20+ diverse examples of high quality answers.详细指令集：分享大量指令、流程和示例，以微调 Claude 的回复。开发人员通常会在提示词中加入一两个示例，但借助提示词缓存功能，包含 20 个以上高质量答案的多样化示例能进一步提升性能。
- Agentic tool use: Enhance performance for scenarios involving multiple tool calls and iterative code changes, where each step typically requires a new API call.智能体工具使用：针对涉及多次工具调用和迭代代码修改的场景提升性能，此类场景中每个步骤通常都需要新的API调用。
- Talk to books, papers, documentation, podcast transcripts, and other longform content: Bring any knowledge base alive by embedding the entire document(s) into the prompt, and letting users ask it questions.与书籍、论文、文档、播客文稿及其他长篇内容互动：将整个文档嵌入提示词中，让知识库“活”起来，使用户能向其提问。

### Troubleshooting common issues 排查常见问题

If experiencing unexpected behavior:若遇到异常行为：

- Ensure cached sections are identical across calls. For explicit breakpoints, verify that `cache_control` markers are in the same locations 确保缓存的部分在所有调用中保持一致。对于显式断点，请验证 `cache_control` 标记是否位于相同位置
- Check that calls are made within the cache lifetime (5 minutes by default) 检查调用是否在缓存有效期内进行（默认5分钟）
- Verify that `tool_choice` and image usage remain consistent between calls 确认 `tool_choice` 和图片使用在各次调用之间保持一致
- Validate that you are caching at least the minimum number of tokens for the model you are using (see [Cache limitations](#cache-limitations)). Length-based caching failures are silent: the request succeeds but both `cache_creation_input_tokens` and `cache_read_input_tokens` will be 0 确认你至少为所使用的模型缓存了最低数量的令牌（请参阅 [缓存限制](#cache-limitations) ）。基于长度的缓存失败是静默的：请求会成功，但 `cache_creation_input_tokens` 和 `cache_read_input_tokens` 均会显示为 0
- Confirm your breakpoint is on a block that stays identical across requests. Cache writes happen only at the breakpoint, and if that block changes (timestamps, per-request context, the incoming message), the prefix hash never matches. The lookback does not find stable content behind the breakpoint; it only finds entries that earlier requests wrote at their own breakpoints 确认你的断点位于一个在所有请求中保持不变的代码块上。缓存仅在该断点处写入；如果该代码块发生变化（例如时间戳、每次请求的上下文、传入的消息），前缀哈希值将永远不会匹配。回溯无法在断点之后找到稳定的内容，只能找到早期请求在各自断点处写入的条目
- Verify that the keys in your `tool_use` content blocks have stable ordering as some languages (for example, Swift, Go) randomize key order during JSON conversion, breaking caches 请确保你的 `tool_use` 内容块中的键具有稳定的顺序，因为某些语言（例如 Swift、Go）会在 JSON 转换过程中随机化键的顺序，从而导致缓存失效

Changes to `tool_choice` or the presence/absence of images anywhere in the prompt will invalidate the cache, requiring a new cache entry to be created. For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).对 `tool_choice` 的修改或提示中任意位置是否存在图片，都会使缓存失效，需要创建新的缓存条目。有关缓存失效的更多详细信息，请参阅 [什么会使缓存失效](#what-invalidates-the-cache) 。

---

## 1-hour cache duration 1小时缓存时长

If you find that 5 minutes is too short, Anthropic also offers a 1-hour cache duration [at additional cost](#pricing).如果你发现5分钟的时长太短，Anthropic 还提供1小时的缓存时长， [需额外付费](#pricing) 。

To use the extended cache, include `ttl` in the `cache_control` definition like this:要使用扩展缓存，请在 `cache_control` 定义中包含 `ttl` ，如下所示：

```
"cache_control": {
  "type": "ephemeral",
  "ttl": "1h"
}
```

The response will include detailed cache information like the following:响应将包含如下所示的详细缓存信息：

```
{
  "usage": {
    "input_tokens": 2048,
    "cache_read_input_tokens": 1800,
    "cache_creation_input_tokens": 248,
    "output_tokens": 503,

    "cache_creation": {
      "ephemeral_5m_input_tokens": 456,
      "ephemeral_1h_input_tokens": 100
    }
  }
}
```

Note that the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object.请注意，当前的 `cache_creation_input_tokens` 字段等于 `cache_creation` 对象中各值的总和。

### When to use the 1-hour cache 何时使用1小时缓存

If you have prompts that are used at a regular cadence (that is, system prompts that are used more frequently than every 5 minutes), continue to use the 5-minute cache, since this will continue to be refreshed at no additional charge.如果你的提示词以固定频率使用（即系统提示词的使用频率超过每5分钟一次），请继续使用5分钟缓存，因为这仍会免费刷新，无需额外费用。

The 1-hour cache is best used in the following scenarios:1小时缓存最适用于以下场景：

- When you have prompts that are likely used less frequently than 5 minutes, but more frequently than every hour. For example, when an agentic side-agent will take longer than 5 minutes, or when storing a long chat conversation with a user and you generally expect that user may not respond in the next 5 minutes.当你的提示词使用频率低于每5分钟一次，但高于每小时一次时。例如，当一个智能体副任务处理时间超过5分钟时，或者当你需要存储与用户的长对话，且通常预计该用户在接下来5分钟内不会回复时。
- When latency is important and your follow up prompts may be sent beyond 5 minutes.当延迟很重要且你的后续提示可能在5分钟后发送时。
- When you want to improve your rate limit utilization, since cache hits are not deducted against your rate limit.当你想要提高你的速率限制利用率时，因为缓存命中不会从你的速率限制中扣除。

The 5-minute and 1-hour cache behave the same with respect to latency. You will generally see improved time-to-first-token for long documents.5分钟和1小时的缓存在延迟方面表现一致。对于长文档，你通常会看到首令牌生成时间有所缩短。

### Mixing different TTLs 混合不同的生存时间

You can use both 1-hour and 5-minute cache controls in the same request, but with an important constraint: Cache entries with longer TTL must appear before shorter TTLs (that is, a 1-hour cache entry must appear before any 5-minute cache entries).你可以在同一个请求中同时使用1小时和5分钟的缓存控制，但有一个重要限制：具有更长TTL的缓存条目必须出现在更短TTL的条目之前（也就是说，1小时的缓存条目必须排在任何5分钟的缓存条目之前）。

When mixing TTLs, the API determines three billing locations in your prompt:混合使用生存时间（TTL）时，API 会在你的提示词中确定三个计费位置：

1. Position `A`: The token count at the highest cache hit (or 0 if no hits).`A` 位置：最高缓存命中时的令牌数（若无命中则为0）。
2. Position `B`: The token count at the highest 1-hour `cache_control` block after `A` (or equals `A` if none exist).位置 `B` ： `A` 之后最高 1 小时 `cache_control` 块的令牌数（若无则等于 `A` ）。
3. Position `C`: The token count at the last `cache_control` block.`C` 位置：最后一个 `cache_control` 块的令牌数

If `B` and/or `C` are larger than `A`, they will necessarily be cache misses, because `A` is the highest cache hit.如果 `B` 和/或 `C` 大于 `A` ，则它们必然会出现缓存未命中，因为 `A` 是最高的缓存命中值。

You'll be charged for: 你将被收取以下费用：

1. Cache read tokens for `A`. 为 `A` 的缓存读取令牌计费。
2. 1-hour cache write tokens for `(B - A)`.1小时缓存写入令牌，对应 `(B - A)` 。
3. 5-minute cache write tokens for `(C - B)`.5分钟缓存写入令牌，对应 `(C - B)` 。

Here are 3 examples. This depicts the input tokens of 3 requests, each of which has different cache hits and cache misses. Each has a different calculated pricing, shown in the colored boxes, as a result. 这里有3个示例。该图展示了3个请求的输入令牌，每个请求的缓存命中和缓存命中次数均不相同。因此，每个请求的计算定价也各不相同，如彩色框中所示。 ![Mixing TTLs Diagram](https://platform.claude.com/docs/images/prompt-cache-mixed-ttl.svg)

---

## Prompt caching examples 提示缓存示例

To help you get started with prompt caching, the [prompt caching cookbook](https://platform.claude.com/cookbook/misc-prompt-caching) provides detailed examples and best practices.为帮助你开始使用提示缓存， [提示缓存操作指南](https://platform.claude.com/cookbook/misc-prompt-caching) 提供了详细示例和最佳实践。

The following code snippets showcase various prompt caching patterns. These examples demonstrate how to implement caching in different scenarios, helping you understand the practical applications of this feature:以下代码片段展示了多种提示词缓存模式。这些示例演示了如何在不同场景中实现缓存，帮助你理解该功能的实际应用：

## Data retention 数据保留

Prompt caching (both automatic and explicit) is ZDR eligible. Anthropic does not store the raw text of your prompts or Claude's responses.提示缓存（包括自动和显式两种方式）符合零数据保留（ZDR）要求。Anthropic 不会存储你的原始提示文本或 Claude 的回复内容。

KV (key-value) cache representations and cryptographic hashes of cached content are held in memory only and are not stored at rest. Cached entries have a minimum lifetime of 5 minutes (standard) or 60 minutes (extended), after which they are promptly, though not immediately, deleted. Cache entries are isolated between organizations.KV（键值）缓存表示形式和缓存内容的加密哈希值仅保存在内存中，不会持久存储。缓存条目的最短生存期为5分钟（标准）或60分钟（扩展），此后会尽快（但并非立即）被删除。不同组织之间的缓存条目相互隔离。

For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention).要了解所有功能的 ZDR 资格，请查看 [API 与数据保留](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention) 。