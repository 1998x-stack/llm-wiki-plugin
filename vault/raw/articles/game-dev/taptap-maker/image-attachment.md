# 图片附件研究：Claude Agent SDK

## 研究目标

探索如何在 Claude Agent SDK 中发送图片或其他附件给 Claude。

## 研究结果

### ✅ 1. Anthropic SDK 直接支持图片附件

**测试代码**: `test-direct-api-image.ts`

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: testImageBase64,
          },
        },
        {
          type: "text",
          text: "What color is this image?",
        },
      ],
    },
  ],
});
```

**结果**: ✅ **成功** - Claude 正确识别了图片内容

### ❓ 2. Claude Agent SDK 的图片支持情况

**测试代码**: `test-image-attachment.ts`

#### 方法 1: 使用简单字符串 prompt

```typescript
const simpleQuery = query({
  prompt: "Hello, can you see images?",
  options: { maxTurns: 1 },
});
```

**结果**: ✅ 工作正常（但没有实际发送图片）

#### 方法 2: 使用 AsyncIterable<SDKUserMessage> 发送图片

```typescript
async function* userMessages() {
  yield {
    type: "user" as const,
    session_id: "test-session",
    message: {
      role: "user" as const,
      content: [
        {
          type: "image" as const,
          source: {
            type: "base64" as const,
            media_type: "image/png" as const,
            data: testImageBase64,
          },
        },
        {
          type: "text" as const,
          text: "What color is this image?",
        },
      ],
    },
    parent_tool_use_id: null,
  };
}

const imageQuery = query({
  prompt: userMessages(),
  options: { maxTurns: 1 },
});
```

**结果**: ❌ **失败** - Claude 回复 "I don't see any image attached to your message"

### 分析

#### 可能的原因

1. **SDK 处理 AsyncIterable 时丢失了图片数据**
   - Agent SDK 可能在内部转换消息时只提取了文本内容
   - 图片 block 可能被过滤或忽略了

2. **SDK 设计问题**
   - Agent SDK 主要设计用于工具调用和代码操作
   - 可能没有考虑多模态输入的场景

3. **消息格式问题**
   - 虽然类型定义支持 `APIUserMessage`（包含图片），但实际实现可能有限制

## 支持的附件类型（基于 Anthropic API）

### 图片格式

- **支持**: JPEG, PNG, GIF, WebP
- **大小限制**: 单张图片最大 5MB
- **数量限制**: 每次请求最多 100 张图片
- **推荐大小**: 小于 1.15 megapixels 以获得最佳性能

### 文档格式

- **支持**: PDF
- **使用类型**: `document` block（而不是 `image` block）

```typescript
{
  type: 'document',
  source: {
    type: 'base64',
    media_type: 'application/pdf',
    data: pdfBase64Data,
  }
}
```

## 结论与建议

### 当前状态

| 方式                      | 图片支持              | 状态           |
| ------------------------- | --------------------- | -------------- |
| Anthropic SDK 直接调用    | ✅ 完全支持           | 推荐           |
| Agent SDK (字符串 prompt) | ❌ 不支持             | -              |
| Agent SDK (AsyncIterable) | ❓ 理论支持，实测失败 | 需要进一步调查 |

### 建议方案

#### 方案 1: 使用 Anthropic SDK 直接调用（推荐）

如果需要发送图片：

1. 直接使用 `@anthropic-ai/sdk` 的 `client.messages.create()`
2. 不使用 Agent SDK 的工具调用功能
3. 自己实现工具调用逻辑

**优点**:

- ✅ 完全支持多模态输入
- ✅ API 稳定，文档完善
- ✅ 可以混合文本和图片

**缺点**:

- ❌ 失去 Agent SDK 的工具调用能力
- ❌ 需要自己实现权限管理
- ❌ 需要自己处理消息流

#### 方案 2: 混合使用两个 SDK

对于需要图片的请求：

1. 使用 Anthropic SDK 发送带图片的消息
2. 获取 Claude 的初步回复
3. 将回复作为上下文传递给 Agent SDK
4. 使用 Agent SDK 进行工具调用和代码操作

**优点**:

- ✅ 同时获得图片支持和工具调用能力
- ✅ 灵活性高

**缺点**:

- ❌ 复杂度高
- ❌ 需要维护两套会话状态
- ❌ 上下文传递可能有损失

#### 方案 3: 等待 Agent SDK 更新

**当前建议**: 如果 Agent SDK 未来支持多模态输入，这将是最佳方案。

可以：

1. 向 Anthropic 提 issue 或功能请求
2. 关注 SDK 更新日志
3. 临时使用方案 1 或方案 2

## 实际应用场景

### 场景 1: 用户上传截图，让 AI 分析代码

```typescript
// 使用 Anthropic SDK
const response = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: screenshotBase64,
          },
        },
        {
          type: "text",
          text: "这段代码有什么问题？请帮我修复。",
        },
      ],
    },
  ],
});

// 如果需要工具调用，将回复传递给 Agent SDK
const agentQuery = query({
  prompt: `User asked about this code: ${response.content[0].text}\n\nPlease help fix the issues.`,
  options: {
    /* ... */
  },
});
```

### 场景 2: 用户上传设计稿，生成代码

这个场景**必须使用图片**，因此：

- ✅ 使用 Anthropic SDK
- ❌ 无法直接使用 Agent SDK 的工具调用

### 场景 3: 纯文本交互 + 工具调用

这是 Agent SDK 的最佳使用场景：

- ✅ 使用 Agent SDK
- ✅ 完整的工具调用支持
- ✅ 权限管理
- ✅ 文件操作

## 技术细节

### Base64 编码

```typescript
import { readFileSync } from "fs";

// 从文件读取
const imageBuffer = readFileSync("/path/to/image.png");
const base64Image = imageBuffer.toString("base64");

// 从 URL 下载
const response = await fetch("https://example.com/image.jpg");
const arrayBuffer = await response.arrayBuffer();
const base64Image = Buffer.from(arrayBuffer).toString("base64");

// 从浏览器 File API
const file = document.getElementById("fileInput").files[0];
const reader = new FileReader();
reader.onloadend = () => {
  const base64Image = reader.result.split(",")[1]; // 移除 data:image/png;base64, 前缀
};
reader.readAsDataURL(file);
```

### 图片优化建议

1. **压缩图片** - 保持在 1.15 megapixels 以下
2. **选择合适的格式** - JPEG 用于照片，PNG 用于截图
3. **批量处理** - 如果有多张图片，考虑合并为一张或分批发送

## 下一步行动

- [ ] 向 Anthropic 提 feature request，询问 Agent SDK 何时支持多模态输入
- [ ] 在 TapTap Maker 中实现方案 1 或方案 2
- [ ] 测试更多边界情况（大图片、多张图片、PDF 等）
- [ ] 编写文档说明何时使用哪个 SDK

## 参考资源

- [Anthropic Vision API 文档](https://docs.claude.com/en/docs/build-with-claude/vision)
- [Agent SDK TypeScript 文档](https://docs.claude.com/en/api/agent-sdk/typescript)
- [Anthropic SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript)
- [Agent SDK TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript)
