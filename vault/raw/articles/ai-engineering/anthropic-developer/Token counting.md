---
title: "Token counting"
source: "https://platform.claude.com/docs/en/build-with-claude/token-counting"
author:
published:
created: 2026-04-16
description: "Claude API Documentation"
tags:
  - "clippings"
---
Token counting enables you to determine the number of tokens in a message before sending it to Claude, helping you make informed decisions about your prompts and usage. With token counting, you can 令牌计数功能可让你在将消息发送给 Claude 之前确定其中的令牌数量，从而帮助你针对提示词和使用情况做出明智的决策。借助令牌计数功能，你可以

- Proactively manage rate limits and costs 主动管理速率限制和成本
- Make smart model routing decisions 做出明智的模型路由决策
- Optimize prompts to be a specific length 将提示词优化为特定长度

This feature is eligible for [Zero Data Retention (ZDR)](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.此功能符合零数据保留（ZDR）</b>的条件。当你的组织签订了零数据保留协议后，通过此功能发送的数据在 API 响应返回后不会被存储。

---

## How to count message tokens 如何计算消息令牌

The [token counting](https://platform.claude.com/docs/en/api/messages-count-tokens) endpoint accepts the same structured list of inputs for creating a message, including support for system prompts, [tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), [images](https://platform.claude.com/docs/en/build-with-claude/vision), and [PDFs](https://platform.claude.com/docs/en/build-with-claude/pdf-support). The response contains the total number of input tokens.[令牌计数](https://platform.claude.com/docs/en/api/messages-count-tokens) 端点接受用于创建消息的相同结构化输入列表，包括支持系统提示、 [工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) 、 [图片](https://platform.claude.com/docs/en/build-with-claude/vision) 和 [PDF](https://platform.claude.com/docs/en/build-with-claude/pdf-support) 。响应包含输入令牌的总数。

The token count should be considered an **estimate**. In some cases, the actual number of input tokens used when creating a message may differ by a small amount.令牌计数应被视为 **估算值** 。在某些情况下，创建消息时实际使用的输入令牌数量可能会有少量偏差。

Token counts may include tokens added automatically by Anthropic for system optimizations. **You are not billed for system-added tokens**. Billing reflects only your content.Token 计数可能包含 Anthropic 为系统优化自动添加的 Token。 **系统添加的 Token 不会向你计费** 。计费仅针对你的内容。

### Supported models 支持的模型

All [active models](https://platform.claude.com/docs/en/about-claude/models/overview) support token counting.所有 [活跃模型](https://platform.claude.com/docs/en/about-claude/models/overview) 均支持令牌计数。

### Count tokens in basic messages 统计基础消息中的令牌

```
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-opus-4-6",
      "system": "You are a scientist",
      "messages": [{
        "role": "user",
        "content": "Hello, Claude"
      }]
    }'
```

```
{ "input_tokens": 14 }
```

### Count tokens in messages with tools统计含工具的消息中的令牌数

[Server tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) token counts only apply to the first sampling call.[服务器工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools) 的令牌计数仅适用于首次采样调用。

```
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-opus-4-6",
      "tools": [
        {
          "name": "get_weather",
          "description": "Get the current weather in a given location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              }
            },
            "required": ["location"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "What'\''s the weather like in San Francisco?"
        }
      ]
    }'
```

```
{ "input_tokens": 403 }
```

### Count tokens in messages with images统计含图片的消息中的令牌数

```
#!/bin/sh

IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
IMAGE_MEDIA_TYPE="image/jpeg"
IMAGE_BASE64=$(curl -s "$IMAGE_URL" | base64 | tr -d '\n')

curl https://api.anthropic.com/v1/messages/count_tokens \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data @- <<EOF
{
    "model": "claude-opus-4-6",
    "messages": [
        {"role": "user", "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "$IMAGE_MEDIA_TYPE",
                "data": "$IMAGE_BASE64"
            }},
            {"type": "text", "text": "Describe this image"}
        ]}
    ]
}
EOF
```

```
{ "input_tokens": 1551 }
```

### Count tokens in messages with extended thinking统计包含扩展思考的消息中的令牌数

See [how the context window is calculated with extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#how-context-window-is-calculated-with-extended-thinking) for more details 请查看 [扩展思维下上下文窗口的计算方式](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#how-context-window-is-calculated-with-extended-thinking) 以了解更多详细信息

- Thinking blocks from **previous** assistant turns are ignored and **do not** count toward your input tokens 来自 **之前** 助手回合的思考块将被忽略，且 **不会** 计入你的输入令牌数
- **Current** assistant turn thinking **does** count toward your input tokens **当前** 助手回合的思考内容 **会** 计入你的输入令牌

```
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data '{
      "model": "claude-sonnet-4-6",
      "thinking": {
        "type": "enabled",
        "budget_tokens": 16000
      },
      "messages": [
        {
          "role": "user",
          "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "thinking",
              "thinking": "This is a nice number theory question. Lets think about it step by step...",
              "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
            },
            {
              "type": "text",
              "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
            }
          ]
        },
        {
          "role": "user",
          "content": "Can you write a formal proof?"
        }
      ]
    }'
```

```
{ "input_tokens": 88 }
```

### Count tokens in messages with PDFs 统计含 PDF 的消息中的令牌数

Token counting supports PDFs with the same [limitations](https://platform.claude.com/docs/en/build-with-claude/pdf-support#pdf-support-limitations) as the Messages API.令牌计数功能支持 PDF 文件，其限制与 Messages API 相同 [限制](https://platform.claude.com/docs/en/build-with-claude/pdf-support#pdf-support-limitations) 。

```
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "content-type: application/json" \
    --header "anthropic-version: 2023-06-01" \
    --data @- <<EOF
{
  "model": "claude-opus-4-6",
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "$PDF_BASE64"
        }
      },
      {
        "type": "text",
        "text": "Please summarize this document."
      }
    ]
  }]
}
EOF
```

```
{ "input_tokens": 2188 }
```

---

## Pricing and rate limits 定价与速率限制

Token counting is **free to use** but subject to requests per minute rate limits based on your [usage tier](https://platform.claude.com/docs/en/api/rate-limits#rate-limits). If you need higher limits, contact sales through the [Claude Console](https://platform.claude.com/settings/limits).令牌计数 **免费使用** ，但会根据你的 [使用层级](https://platform.claude.com/docs/en/api/rate-limits#rate-limits) 受到每分钟请求次数的限制。若你需要更高的限制，请通过 [Claude 控制台](https://platform.claude.com/settings/limits) 联系销售团队。

| Usage tier 使用层级 | Requests per minute (RPM) 每分钟请求数（RPM） |
| --- | --- |
| 1 | 100 |
| 2 | 2,000 |
| 3 | 4,000 |
| 4 | 8,000 |

Token counting and message creation have separate and independent rate limits. Usage of one does not count against the limits of the other.令牌计数和消息创建拥有独立且互不关联的速率限制。其中一项的使用不会计入另一项的限制额度。