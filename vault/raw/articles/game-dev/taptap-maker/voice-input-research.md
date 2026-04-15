# 语音输入功能方案调研

## 目标

实现类似 [Typeless](https://www.typeless.com/) 的 AI 语音输入功能：

- 低延迟语音转文本（STT）
- LLM 矫正（去填充词、重复、自动格式化）
- 支持多语言（中英为主）

## 技术方案对比

### 语音识别服务

| 服务                | 延迟     | 中文支持 | 部署方式   | 成本         |
| ------------------- | -------- | -------- | ---------- | ------------ |
| **阿里 SenseVoice** | 70ms/10s | 优秀     | 自部署/云  | 免费（开源） |
| 阿里云 ASR          | ~300ms   | 优秀     | 云服务     | 按量付费     |
| OpenAI Whisper      | ~2s      | 良好     | 自部署/API | 自部署免费   |
| Deepgram            | ~200ms   | 一般     | 云服务     | $0.0125/min  |

**选择：SenseVoice**

- 10s 音频推理仅 70ms，比 Whisper-Large 快 15 倍
- 中文识别效果优于 Whisper
- 支持情感、语气词检测（可用于优化 LLM 矫正）
- 开源免费，可自部署控制成本

### 实时流式方案

| 方案                                                                         | 特点                       | 延迟   |
| ---------------------------------------------------------------------------- | -------------------------- | ------ |
| [api4sensevoice](https://github.com/0x5446/api4sensevoice)                   | WebSocket + VAD + 实时识别 | ~100ms |
| [streaming-sensevoice](https://github.com/pengzhendong/streaming-sensevoice) | 伪流式 + Hotwords          | ~200ms |
| [FunASR](https://github.com/modelscope/FunASR)                               | 完整 2pass 方案            | ~100ms |

**选择：FunASR 2pass 方案**

- 实时显示（online）+ 句尾矫正（offline）
- 支持 VAD、标点预测、ITN（数字转换）
- 官方维护，社区活跃
- Docker 一键部署，支持多并发

## 系统架构

复用项目现有 WebSocket 基础设施（ws 库），通过 `_taptap/voice/*` 方法前缀区分语音消息。

```
┌─────────────────────────────────────────────────────────────────┐
│                         Browser                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │ Mic Input   │───▶│ Audio       │───▶│ WebSocket Client    │ │
│  │ (MediaAPI)  │    │ Processor   │    │ (JSON-RPC + Binary) │ │
│  └─────────────┘    └─────────────┘    └──────────┬──────────┘ │
│                                                    │            │
│  ┌─────────────────────────────────────────────────┴──────────┐ │
│  │                    Voice Input UI                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │ Real-time    │  │ Final Text   │  │ LLM Correction   │ │ │
│  │  │ Preview      │  │ Display      │  │ Toggle           │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │ WebSocket (JSON-RPC + Binary PCM)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Gateway Server (existing feWSServer)             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │ WebSocket       │───▶│ VoiceHandler    │                    │
│  │ Server (ws)     │    │ (_taptap/voice) │                    │
│  │ (existing)      │    └────────┬────────┘                    │
│  └─────────────────┘             │                              │
│                                  ▼                              │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │ FunASR Client   │───▶│ LLM Corrector   │                    │
│  │ (WebSocket)     │    │ (Claude API)    │                    │
│  └─────────────────┘    └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

**复用现有 WebSocket 的优势**：

- 鉴权复用（accessToken 验证）
- 心跳检测已实现
- 消息路由统一（`_taptap/*` 前缀）
- 无需额外端口/路由配置

## 核心流程

### 1. 音频采集 (Browser)

使用 AudioWorklet（ScriptProcessorNode 已废弃）：

```typescript
// packages/voice-input/src/client/pcm-processor.worklet.ts
class PCMProcessor extends AudioWorkletProcessor {
  process(inputs: Float32Array[][]): boolean {
    const input = inputs[0]?.[0];
    if (input) {
      // 转换为 16-bit PCM
      const int16 = new Int16Array(input.length);
      for (let i = 0; i < input.length; i++) {
        int16[i] = Math.max(-32768, Math.min(32767, input[i] * 32768));
      }
      this.port.postMessage(int16.buffer, [int16.buffer]);
    }
    return true;
  }
}
registerProcessor("pcm-processor", PCMProcessor);
```

```typescript
// packages/voice-input/src/client/audio-capture.ts
const stream = await navigator.mediaDevices.getUserMedia({
  audio: {
    channelCount: 1,
    sampleRate: 16000,
    echoCancellation: true,
    noiseSuppression: true,
  },
});

const audioContext = new AudioContext({ sampleRate: 16000 });
await audioContext.audioWorklet.addModule("/pcm-processor.worklet.js");

const source = audioContext.createMediaStreamSource(stream);
const processor = new AudioWorkletNode(audioContext, "pcm-processor");

processor.port.onmessage = (e: MessageEvent<ArrayBuffer>) => {
  ws.send(e.data); // Binary PCM data
};

source.connect(processor);
```

### 2. WebSocket 协议（JSON-RPC 风格）

复用现有 WebSocket 连接，通过 `_taptap/voice/*` 方法前缀区分语音消息。

**Client → Server**

```typescript
// 开始录音
ws.send(
  JSON.stringify({
    jsonrpc: "2.0",
    method: "_taptap/voice/start",
    params: { mode: "general", enableCorrection: true },
  }),
);

// 发送音频帧（Binary）
ws.send(pcmArrayBuffer); // PCM 16kHz, 16-bit, mono

// 停止录音
ws.send(
  JSON.stringify({
    jsonrpc: "2.0",
    method: "_taptap/voice/stop",
  }),
);
```

**Server → Client**

```typescript
// 实时识别结果（2pass online）
{ jsonrpc: '2.0', method: '_taptap/voice/partial', params: { text: '我想要' } }

// 最终结果（2pass offline + LLM 矫正）
{
  jsonrpc: '2.0',
  method: '_taptap/voice/final',
  params: {
    raw: '我想我想要一杯咖啡',    // 原始识别
    corrected: '我想要一杯咖啡'   // LLM 矫正后
  }
}

// 错误
{
  jsonrpc: '2.0',
  method: '_taptap/voice/error',
  error: { code: -32000, message: '[ASR_ERROR] ...' }
}
```

### 3. LLM 矫正策略

**输入模式**

不同场景需要不同的矫正策略：

| 模式      | 场景          | 矫正强度                     |
| --------- | ------------- | ---------------------------- |
| `general` | 通用文本输入  | 删除填充词、修正错字         |
| `code`    | 代码/命令输入 | 仅修正明显错字，保留所有内容 |
| `chat`    | 游戏对话编写  | 保留语气词，仅修正错字       |

**Prompt Template (general):**

```
你是一个语音转文字的后处理助手。请对以下语音识别结果进行矫正：

原始文本：{raw_text}

矫正规则：
1. 删除填充词（嗯、啊、那个、就是、然后）
2. 删除重复（我我我 → 我）
3. 修正明显的同音错字
4. 保持原意，不要添加内容

仅输出矫正后的文本，不要任何解释。
```

**Prompt Template (code):**

```
修正以下语音识别的代码/命令，仅修正明显的同音错字，保留所有技术术语和变量名：

原始文本：{raw_text}

仅输出矫正后的文本。
```

**触发条件：**

- 句尾检测到 VAD 静音
- 累计文本超过阈值（如 20 字）
- 检测到句末标点

**优化策略：**

- 缓存常见矫正模式，减少 API 调用
- 短句（<10 字）跳过 LLM，使用规则矫正
- 批量处理连续短句

## Monorepo 子仓库设计

```
packages/
└── voice-input/                  # @taptap-code/voice-input
    ├── src/
    │   ├── client/               # 浏览器端
    │   │   ├── audio-capture.ts  # 麦克风采集 + AudioWorklet
    │   │   ├── use-voice-input.ts # React Hook
    │   │   └── index.ts
    │   │
    │   ├── server/               # 服务端
    │   │   ├── voice-handler.ts  # WebSocket 消息处理
    │   │   ├── voice-session.ts  # 会话管理
    │   │   ├── asr-client.ts     # FunASR WebSocket 客户端
    │   │   ├── llm-corrector.ts  # LLM 矫正服务
    │   │   └── index.ts
    │   │
    │   ├── shared/               # 共享类型
    │   │   ├── events.ts         # JSON-RPC 方法定义
    │   │   └── types.ts          # TypeScript 类型
    │   │
    │   └── index.ts              # 统一导出
    │
    ├── docker/                   # ASR 容器配置
    │   └── docker-compose.yml    # FunASR 开发环境
    │
    ├── package.json
    └── tsconfig.json
```

### package.json

```json
{
  "name": "@taptap-code/voice-input",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "exports": {
    "./client": "./src/client/index.ts",
    "./server": "./src/server/index.ts",
    "./shared": "./src/shared/index.ts"
  },
  "peerDependencies": {
    "ws": ">=8.0.0",
    "@anthropic-ai/sdk": ">=0.30.0",
    "react": ">=18.0.0"
  }
}
```

### 集成到现有系统

**服务端：扩展现有 feWSServer**

```typescript
// apps/server/src/gateway-server/servers/feWSServer.ts
import { createVoiceHandler, isVoiceMethod } from "@taptap-code/voice-input/server";

// 初始化 VoiceHandler
const voiceHandler = createVoiceHandler({
  asrEndpoint: process.env.FUNASR_ENDPOINT || "ws://localhost:10095",
  anthropicClient, // 可选，用于 LLM 矫正
});

// 在 handleIncomingMessage 中添加语音消息处理
function handleIncomingMessage(wsFE: FrontendWebSocket, data: WebSocket.RawData, userId: string) {
  // 处理二进制音频数据
  if (data instanceof Buffer) {
    voiceHandler.handleAudioData(wsFE.chatId!, data);
    return;
  }

  const msgStr = data.toString();
  const parsed = JSON.parse(msgStr);

  // 处理语音相关消息
  if (isVoiceMethod(parsed.method)) {
    voiceHandler.handleMessage(wsFE.chatId!, parsed, (msg) => sendToFrontendClient(wsFE, msg));
    return;
  }

  // 其他消息处理...
}

// 在 handleClose 中清理语音会话
function handleClose(wsFE: FrontendWebSocket) {
  voiceHandler.handleDisconnect(wsFE.chatId!);
  // ...
}
```

**客户端：React Hook**

```typescript
// apps/web/src/components/VoiceInput.tsx
import { useVoiceInput, isVoiceMethod } from '@taptap-code/voice-input/client';
import { useWebSocket } from '@/hooks/useWebSocket';

function VoiceInput({ onResult }) {
  const { ws, sendMessage, sendBinary } = useWebSocket();

  const { isRecording, partialText, start, stop, handleMessage } = useVoiceInput({
    sendMessage,
    sendBinary,
    mode: 'general',
    onFinal: (result) => onResult(result.corrected),
  });

  // 在 WebSocket 消息处理器中调用 handleMessage
  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      if (typeof event.data === 'string') {
        const msg = JSON.parse(event.data);
        if (isVoiceMethod(msg.method)) {
          handleMessage(msg);
        }
      }
    };
    ws?.addEventListener('message', onMessage);
    return () => ws?.removeEventListener('message', onMessage);
  }, [ws, handleMessage]);

  return (
    <div>
      <button onClick={isRecording ? stop : start}>
        {isRecording ? 'Recording...' : 'Voice Input'}
      </button>
      {partialText && <span>{partialText}</span>}
    </div>
  );
}
```

## 部署方案

### 开发环境

```yaml
# packages/voice-input/docker/docker-compose.yml
services:
  funasr:
    image: registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
    ports:
      - "10095:10095" # WebSocket
    environment:
      - FUNASR_MODEL_DIR=/workspace/models
    volumes:
      - ./models:/workspace/models
```

### 生产环境

- **方案 A**: 自建 FunASR 服务（GPU 推荐）
  - 优点：完全控制，无外部依赖
  - 缺点：需要维护 GPU 服务器

- **方案 B**: 阿里云百炼 API
  - 优点：免运维，按量付费
  - 缺点：外部依赖，有调用成本

**建议：** 开发阶段用自建，验证后根据流量决定

## 性能指标

| 指标     | 目标值 | 说明                       |
| -------- | ------ | -------------------------- |
| 首字延迟 | <300ms | 用户开始说话到首个字符显示 |
| 流式延迟 | <100ms | 持续说话时的更新间隔       |
| 句尾延迟 | <500ms | 停止说话到最终结果         |
| LLM 矫正 | <1s    | 矫正后文本返回时间         |

## 风险与缓解

| 风险           | 影响             | 缓解措施                |
| -------------- | ---------------- | ----------------------- |
| ASR 服务不稳定 | 用户体验差       | 客户端缓冲 + 重连机制   |
| LLM 矫正延迟高 | 等待时间长       | 可选开关 + 先显示原文   |
| 浏览器兼容性   | 部分用户无法使用 | 检测 + 降级提示         |
| 隐私顾虑       | 用户不愿使用     | 明确提示 + 可选本地处理 |

## 浏览器兼容性

| 浏览器        | MediaDevices | AudioWorklet | WebSocket | 备注           |
| ------------- | ------------ | ------------ | --------- | -------------- |
| Chrome 66+    | ✅           | ✅           | ✅        |                |
| Firefox 76+   | ✅           | ✅           | ✅        |                |
| Safari 14.1+  | ✅           | ✅           | ✅        |                |
| Mobile Chrome | ✅           | ✅           | ✅        |                |
| Mobile Safari | ⚠️           | ✅           | ✅        | 需用户手势触发 |

## 移动端适配（后续）

> 当前阶段专注 Web 桌面端，移动端适配作为 P3 优先级后续实现。

需要处理的问题：

- 权限请求时机（用户手势触发）
- 后台中断处理（visibilitychange）
- 低端设备性能检测

## 参考资料

- [Typeless](https://www.typeless.com/) - AI 语音输入产品
- [FunASR](https://github.com/modelscope/FunASR) - 阿里语音识别工具包
- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) - 阿里开源语音模型
- [api4sensevoice](https://github.com/0x5446/api4sensevoice) - SenseVoice WebSocket 封装
- [阿里云实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition) - 云服务文档

## PoC 验证指南

### 快速开始（Mock 模式，无需 Docker）

适合开发调试，使用模拟 ASR 服务器：

```bash
# 终端 1: 启动 Mock 服务器
npx tsx packages/voice-input/scripts/mock-asr-server.ts

# 终端 2: 运行测试
npx tsx packages/voice-input/scripts/test-asr.ts
```

Mock 服务器返回模拟的中文识别结果，用于验证端到端流程。

### 完整验证（FunASR Docker）

需要 Docker 环境，测量真实延迟：

```bash
# 1. 启动 FunASR 容器
cd packages/voice-input/docker
docker-compose up -d

# 2. 等待模型加载（查看日志）
docker-compose logs -f
# 看到 "server is running on" 表示就绪

# 3. 运行 PoC 测试
npx tsx packages/voice-input/scripts/test-asr.ts
```

### 测试脚本说明

| 脚本                         | 用途                        |
| ---------------------------- | --------------------------- |
| `scripts/test-asr.ts`        | 完整 PoC 测试，测量延迟     |
| `scripts/mock-asr-server.ts` | Mock ASR 服务器（开发用）   |
| `scripts/test-asr-native.ts` | 使用 Node.js 原生 WebSocket |

### 验证标准

| 指标     | 目标     | 说明                     |
| -------- | -------- | ------------------------ |
| 首字延迟 | < 300ms  | 从发送音频到收到首个结果 |
| 总延迟   | < 1000ms | 从发送音频到收到最终结果 |
| 连接成功 | ✅       | WebSocket 能正常建立     |

### 常见问题

**Docker 启动失败**

- 检查 Docker 服务是否运行：`docker ps`
- 检查端口 10095 是否被占用：`lsof -i :10095`

**连接超时**

- FunASR 首次启动需要加载模型（1-2 分钟）
- 查看日志确认就绪状态

**延迟过高**

- CPU 版本延迟约 200-300ms，GPU 版本约 50-100ms
- 网络延迟也会影响结果

## 实施计划

### Phase 0: PoC 验证 ✅

**目标**：验证核心技术可行性

- [x] 创建 `packages/voice-input` 子包
- [x] 实现 Mock ASR 服务器和测试脚本
- [x] Docker Compose 配置 FunASR
- [x] 本地运行 FunASR 验证真实延迟

**PoC 测试结果 (2026-02-01)**

| 指标            | 目标    | 实测                        | 结果    |
| --------------- | ------- | --------------------------- | ------- |
| FunASR 容器启动 | 成功    | ✅                          | 通过    |
| WebSocket 连接  | 成功    | ✅                          | 通过    |
| ASR 处理延迟    | < 300ms | ~206ms                      | ✅ 通过 |
| 2pass 识别      | 正常    | online: "嗯", offline: "。" | ✅ 通过 |

**测试环境**：

- FunASR CPU 版本 (`funasr-runtime-sdk-online-cpu-0.1.12`)
- 测试音频：3 秒 440Hz 正弦波（模拟）
- 延迟计算：从 `is_speaking=false` 到收到 `online_res` 的时间差

**结论**：FunASR CPU 版本延迟满足要求，可进入 Phase 1

### Phase 1: Web MVP（3-5 天）

**目标**：端到端跑通，桌面 Chrome 可用

1. **子包初始化** ✅
   - [x] 创建 `packages/voice-input` 目录结构
   - [x] 配置 package.json、tsconfig.json

2. **客户端实现** ✅
   - [x] AudioWorklet 音频采集
   - [x] React Hook: `useVoiceInput`
   - [x] 浏览器兼容性检测

3. **服务端实现** ✅
   - [x] VoiceHandler 消息处理
   - [x] FunASR WebSocket 客户端
   - [x] LLM 矫正服务（Claude）
   - [x] 会话管理（VoiceSession）

4. **集成测试**
   - [x] 集成到现有 feWSServer（VoiceHandler + 二进制消息处理）
   - [x] VoiceInputButton 组件（`apps/web/src/components/chat/VoiceInputButton.tsx`）
   - [ ] 端到端测试验证（需要启动服务器 + FunASR）

### Phase 2: 功能完善（3-5 天）

**目标**：生产可用

1. **稳定性**
   - [ ] WebSocket 重连（指数退避）
   - [ ] 错误码完整定义
   - [ ] 鉴权中间件

2. **UI 组件**
   - [ ] 录音状态指示
   - [ ] 实时预览 + 最终结果
   - [ ] 矫正开关

### Phase 3: 优化（后续）

- 移动端适配
- 性能调优
- 多语言支持
