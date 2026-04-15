# OpenClaw ① GATEWAY — 控制平面详解

> Gateway 是整个 OpenClaw 系统的"神经系统"，是所有消息进出的唯一入口。

---

## 1. 基本定义

| 属性 | 值 |
|------|----|
| **进程类型** | 长期运行的 WebSocket 服务器 |
| **默认端口** | `ws://127.0.0.1:18789` |
| **运行方式** | systemd（Linux）/ LaunchAgent（macOS）后台常驻 |
| **代码语言** | TypeScript |
| **连接规模** | 支持 40+ 渠道同时连接 |

---

## 2. Gateway 架构图

```
外部渠道
┌──────────────────────────────────────────────────────────┐
│ WhatsApp(Baileys) · Telegram(grammY) · Slack(Bolt)      │
│ Discord(discord.js) · Signal · iMessage · IRC · Matrix   │
│ Feishu · LINE · Mattermost · WeChat · Twitch · Nostr ... │
└────────────────────────┬─────────────────────────────────┘
                         │  各平台原生协议
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Channel Adapters 层                          │
│  标准化消息对象：{ sender, body, attachments, metadata }  │
│  语音/图片/视频 → 转写/转码管道                           │
└────────────────────────┬─────────────────────────────────┘
                         │  统一消息对象
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Session Router（会话路由）                    │
│  ├─ 根据 contact/channel/group 匹配目标 Agent             │
│  ├─ 分配或恢复 Session ID                                 │
│  └─ 支持多 Agent 路由（不同渠道 → 不同 Agent）            │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Lane Queue（串行队列）                        │
│  ├─ 每个 Session 独立队列，严格串行执行                    │
│  ├─ 防止同一会话内并发竞争（工具冲突/状态污染）            │
│  └─ 不同 Session 之间可并行                               │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
                  Agent Runner（Brain）
```

---

## 3. Channel Adapters 子系统

### 3.1 支持的渠道列表

| 渠道 | 适配库 | 特性 |
|------|--------|------|
| WhatsApp | Baileys | 多媒体、语音转写 |
| Telegram | grammY | 机器人 API、内联键盘 |
| Slack | Bolt | Workspace 集成、事件 API |
| Discord | discord.js | 服务器/频道路由 |
| Signal | signal-cli | 端到端加密 |
| iMessage | BlueBubbles（推荐）/ legcy imsg | macOS 原生 |
| Google Chat | Chat API | 企业集成 |
| Microsoft Teams | Teams API | 企业集成 |
| Matrix | 标准 Matrix SDK | 去中心化 |
| Feishu/飞书 | Feishu API | 中国企业常用 |
| IRC | 标准 IRC | 极轻量 |
| WeChat | @tencent-weixin/openclaw-weixin | 微信个人号 |
| WebChat | 内置 WebSocket | 浏览器直连 |
| LINE / Mattermost / Zalo / Nostr / Synology / Tlon / Twitch | 各自 SDK | 长尾渠道 |

### 3.2 消息规范化流程

```
原始消息（任意格式）
       │
       ├─ 文本消息 ─────────────────► { body: "text" }
       │
       ├─ 语音消息 ──► 转写（Whisper/本地ASR）─► { body: "transcript" }
       │
       ├─ 图片/视频 ──► base64 编码 ──────────► { attachments: [...] }
       │
       └─ 群组消息 ──► @提及过滤 ────────────► { isGroupMention: true }
                       reply-tag 路由

统一输出：InboundMessage {
  sessionId: string
  senderId: string
  channelType: ChannelType
  body: string
  attachments?: Attachment[]
  metadata: Record<string, any>
  timestamp: Date
}
```

---

## 4. Session 模型

### 4.1 Session 类型

| 类型 | 描述 |
|------|------|
| `main` | 默认主会话，个人直聊 |
| `group:<id>` | 群组隔离会话 |
| `activation:<mode>` | 特定激活模式下的会话 |

### 4.2 Session 生命周期

```
首次消息
    │
    ▼
生成 Session ID（基于 senderId + channelType）
    │
    ▼
加载历史记录（JSONL transcript）
    │
    ▼
进入 Lane Queue 等待执行
    │
    ▼
执行完成 → 写回持久化 → Session 挂起（等待下一条消息）
```

### 4.3 群组路由规则

```yaml
group_rules:
  mention_gating: true          # 仅响应 @Agent 的消息
  reply_tag_routing: true       # 通过 reply-tag 选择 Agent
  per_channel_chunking: true    # 长消息自动分片
  owner_only_commands: true     # /status /reset 等命令仅 owner 可用
```

---

## 5. Lane Queue — 串行执行队列

### 5.1 为什么必须串行？

```
❌ 并发场景下的问题示例：

消息 A："把 report.md 的第一段替换成 X"
消息 B："把 report.md 的第一段替换成 Y"

如果并发执行：
- A 读取 report.md（此时 B 尚未写入）
- B 读取 report.md（此时 A 尚未写入）
- A 写入 → Y 被覆盖
- B 写入 → X 被覆盖

结果：最终写入随机，历史记录不一致，工具调用冲突

✅ 串行方案：A 完整执行 → B 开始执行，状态一致
```

### 5.2 队列配置

```yaml
lane_queue:
  mode: serial                  # serial | parallel（实验性）
  max_queue_depth: 50           # 最大排队深度
  timeout_per_turn: 300s        # 单次 Agent Loop 超时
  overflow_policy: drop_oldest  # 超出时策略
```

---

## 6. Gateway 客户端连接

Gateway 通过 WebSocket 统一对内部客户端暴露控制接口：

```
ws://127.0.0.1:18789
       │
       ├─ Pi Agent（RPC 模式，工具流/块流）
       ├─ CLI（openclaw 命令行工具）
       ├─ WebChat UI（浏览器界面）
       ├─ macOS App（菜单栏控制面板）
       └─ iOS / Android 节点（移动端配对）
```

### 6.1 常用 Gateway 命令

| 命令 | 说明 |
|------|------|
| `/status` | 显示当前 Session 状态（模型、Token 数、费用） |
| `/reset` | 重置当前会话历史 |
| `openclaw status` | CLI 查看 Gateway 健康状态 |
| `openclaw logs` | 查看实时日志流 |

---

## 7. 远程访问：Tailscale 集成

OpenClaw 支持通过 Tailscale 将 Gateway 安全暴露到远程：

```
本机 Gateway (ws://127.0.0.1:18789)
        │
        ▼
Tailscale Serve/Funnel
        │
        ▼
远程设备通过 Tailscale IP 安全访问
（无需暴露公网 IP，无需 VPN 配置）
```

---

## 8. 媒体处理管道

```
输入媒体
   │
   ├─ 图片（JPEG/PNG/WebP）
   │       └─► 压缩到限制尺寸 → base64 → 传入 LLM vision API
   │
   ├─ 语音（OGG/MP3/M4A）
   │       └─► 转写（Whisper API 或本地 Whisper）→ 文本注入
   │
   └─ 视频（MP4）
           └─► 提取关键帧 → 图片流程 / 音轨提取 → 语音流程

临时文件生命周期：执行结束后自动清理
```

---

## 9. macOS 专属功能

| 功能 | 描述 |
|------|------|
| 菜单栏控制面板 | Gateway 健康监控、一键重启 |
| Voice Wake | 语音唤醒词触发 Agent |
| PTT（Push-to-Talk）| 按住说话模式 |
| Talk Mode Overlay | 全屏语音交互界面 |
| Canvas 界面 | 实时渲染 Agent 输出的可视化面板 |

---

## 10. 关键设计决策总结

| 决策 | 原因 |
|------|------|
| 单一 WebSocket 控制平面 | 统一路由，避免多进程竞争 |
| Lane Queue 强制串行 | 防止状态竞争，保证历史一致性 |
| Channel Adapter 模式 | 模型与渠道完全解耦，新渠道零改动接入 |
| 本地 WebSocket 绑定 | 默认不暴露网络，最小攻击面 |
| 消息归一化 | LLM 只看到干净结构化输入，提升输出质量 |
