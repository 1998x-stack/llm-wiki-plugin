# Agentic Commerce 生态全景深度研究

> **研究日期**：2026 年 4 月 | **状态**：快速演进中的新兴标准体系
>
> AI Agent 正从"对话助手"升级为"自主交易主体"，互联网支付基础设施正经历一场结构性重构。本文梳理这场变革中的核心协议、技术组件与关键玩家。

---

## 目录

1. [宏观背景：为什么现有支付体系不够用](#1-宏观背景)
2. [生态地图：协议层级与参与方](#2-生态地图)
3. [ACP — Agentic Commerce Protocol](#3-acp--agentic-commerce-protocol)
4. [MPP — Machine Payments Protocol](#4-mpp--machine-payments-protocol)
5. [SPT — Shared Payment Tokens（Stripe）](#5-spt--shared-payment-tokens)
6. [ACS — Agentic Commerce Suite（Stripe）](#6-acs--agentic-commerce-suite)
7. [x402 — HTTP 402 复活计划](#7-x402--http-402-复活计划)
8. [Tempo — 专为支付设计的 L1 区块链](#8-tempo--l1-区块链)
9. [Browserbase — Agent 的浏览器基础设施](#9-browserbase)
10. [横向对比：ACP vs MPP vs x402](#10-横向对比)
11. [技术架构深度剖析](#11-技术架构深度剖析)
12. [安全与反欺诈框架](#12-安全与反欺诈)
13. [开发者实战集成路径](#13-开发者集成路径)
14. [生态现状与关键玩家](#14-生态现状与关键玩家)
15. [挑战、风险与未来趋势](#15-挑战与趋势)

---

## 1. 宏观背景

### 1.1 人类支付 vs 机器支付的结构差异

传统互联网支付基础设施是为**人类操作者**设计的：

```
人类购物流程：
浏览商品 → 加购物车 → 填写地址 → 输入信用卡 → 点击支付 → 等待确认
```

这套流程依赖：
- 视觉渲染（商品图片、按钮位置）
- 人机交互（CAPTCHA、3DS 验证短信）
- 会话状态（Cookie、登录态）
- 心理信任（品牌标识、HTTPS 锁头）

当 **AI Agent** 作为购买主体时，上述每一环节都是障碍：

| 障碍 | 根因 | 后果 |
|------|------|------|
| CAPTCHA / 反机器人 | 被误判为恶意爬虫 | 支付流程中断 |
| 3DS 短信验证 | 无法接收/处理 | 支付失败 |
| 动态结账表单 | 每次结构不同 | 解析成本高、可靠性差 |
| API Key 注册 | 需要人工开户 | 无法零摩擦接入 |
| 支付凭证暴露 | Agent 持有完整卡号 | 安全风险极高 |

### 1.2 Cloudflare 的观察数据

> Cloudflare 上的网站每天向试图访问其内容和电子商务商店的机器人和爬虫发送超过**十亿个 HTTP 402 响应**。然而这些响应几乎全部石沉大海——因为没有统一标准规定如何处理。

这揭示了一个巨大的机会：**已经有海量服务想向机器收费，只是缺乏标准**。

### 1.3 市场时间线

```
2024 Q3  │  OpenAI 开始推进 ChatGPT 购物能力
2025 Q1  │  Stripe × Tempo 联合开发 MPP
2025 Q2  │  Coinbase 发布 x402 协议草案
2025 Q3  │  ACP 正式发布（Stripe × OpenAI）
          │  Cloudflare × Coinbase 共建 x402 Foundation
2025 Q4  │  Stripe 发布 ACS（Agentic Commerce Suite）
2026 Q1  │  Tempo 主网上线
2026 Q2  │  MPP 提交 IETF 规范草案
```

---

## 2. 生态地图

### 2.1 协议栈分层

```
┌─────────────────────────────────────────────────────────────────┐
│                     应用层 / 业务层                              │
│   ChatGPT Shopping │ Claude Tool Use │ 自定义 AI Agent          │
├─────────────────────────────────────────────────────────────────┤
│                   商务协议层（Commerce Protocol）                │
│         ACP (Agentic Commerce Protocol)                         │
│         [发现 → 结账配置 → 订单提交 → 履约]                      │
├─────────────────────────────────────────────────────────────────┤
│                   支付协议层（Payment Protocol）                 │
│   MPP (Machine Payments Protocol)  │  x402 (HTTP 402 标准)      │
│   [支付协商 → 凭证传递 → 结算 → 收据]                           │
├─────────────────────────────────────────────────────────────────┤
│                   支付原语层（Payment Primitives）               │
│   SPT (Shared Payment Tokens)  │  Stablecoin Wallets            │
│   [令牌化支付方式 │ 范围限制 │ 生命周期管理]                     │
├─────────────────────────────────────────────────────────────────┤
│                   结算层（Settlement Layer）                     │
│   Stripe (法币) │ Tempo L1 (稳定币) │ Lightning │ Solana        │
├─────────────────────────────────────────────────────────────────┤
│                   基础设施层                                     │
│   Browserbase (浏览器) │ Cloudflare (网络/安全) │ MCP (工具调用) │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 三方参与模型

所有协议均围绕**三方关系**构建：

```
     买家 (Buyer)
      │  注册支付方式
      │  设置消费授权
      ▼
  AI Agent ◄────────────────────► 商家 (Merchant / Business)
  • 代表买家行动                    • 维护商品目录
  • 持有 SPT/凭证                  • 控制结账逻辑
  • 发起支付请求                   • 保留订单履约权
      │                                    │
      └──────────── 支付处理商 ────────────┘
                  (Stripe / PSP)
                  • 令牌化支付方式
                  • 风控 & 反欺诈
                  • 结算 & 账单
```

---

## 3. ACP — Agentic Commerce Protocol

### 3.1 核心定位

**ACP（Agentic Commerce Protocol）** 是由 **Stripe × OpenAI** 联合开发、Apache 2.0 开源的**商务协议**——解决的是"Agent 如何与商家完成一次完整购物"的问题，而非底层支付机制。

> 首个上线的 AI 平台实现：**OpenAI ChatGPT**（首个兼容 ACP 的 AI 平台）
> 首个兼容的 PSP：**Stripe**（通过 Shared Payment Token）

### 3.2 协议核心流程

```
                        ┌──────────────┐
                        │   AI Agent   │
                        └──────┬───────┘
                               │ 1. 发送购物意图
                               │    "我需要一件 $40 以内的 L 码 T恤"
                               ▼
                      ┌────────────────┐
                      │  ACP Endpoint  │  ← 商家托管的 REST/MCP 端点
                      │  (商家实现)     │
                      └───────┬────────┘
                              │ 2. 返回商品清单 + 结账配置
                              │    {products, checkout_config, constraints}
                              ▼
                      ┌───────────────┐
                      │   AI Agent    │
                      │ (用户确认选择) │
                      └───────┬───────┘
                              │ 3. 提交结账请求
                              │    {product_id, SPT, shipping_info}
                              ▼
                      ┌────────────────┐
                      │  ACP Endpoint  │
                      │ (验证 + 下单)   │
                      └───────┬────────┘
                              │ 4. 返回订单确认
                              │    {order_id, status, fulfillment}
                              ▼
                      ┌───────────────┐
                      │   AI Agent    │
                      │ 告知用户结果   │
                      └───────────────┘
```

### 3.3 ACP 端点规范

商家需实现以下端点（REST 或 MCP 均可）：

```
GET  /.well-known/acp-configuration     # 发现配置
POST /acp/v1/catalog/search             # 商品搜索
POST /acp/v1/checkout/sessions          # 创建结账会话
GET  /acp/v1/checkout/sessions/{id}     # 查询会话状态
POST /acp/v1/checkout/sessions/{id}/complete  # 完成结账
```

**结账配置示例（Checkout Configuration）**：

```json
{
  "version": "1.0",
  "merchant": {
    "id": "merchant_abc123",
    "name": "Cartsy Shop",
    "supported_regions": ["US", "CA", "GB"]
  },
  "payment": {
    "accepted_tokens": ["stripe_spt"],
    "currencies": ["usd", "cad", "gbp"]
  },
  "constraints": {
    "max_order_amount": 50000,
    "require_user_confirmation": true,
    "allowed_agents": ["openai_chatgpt", "*"]
  },
  "fulfillment_types": ["physical", "digital", "subscription"]
}
```

### 3.4 商家视角的核心价值

| 维度 | 传统电商 | ACP 接入后 |
|------|---------|-----------|
| 流量来源 | 搜索引擎、社交 | + AI Agent 渠道 |
| 客户关系 | 完全自有 | **仍完全自有**（商家保持 MoR） |
| 库存控制 | 自行管理 | 可推送实时库存至 Agent |
| 定价权 | 自主设置 | Agent 不能绕过定价逻辑 |
| 集成成本 | — | 一次集成，支持所有兼容 Agent |

### 3.5 发现机制（Discovery）

当前阶段，ACP 的发现机制仍在建设中：
- 每个 AI 平台自行管理商家白名单（如 ChatGPT 需商家申请）
- 正在设计通用的 Discovery 标准（类似 `/.well-known/` 机制）
- 联系邮件：`acp@stripe.com`

---

## 4. MPP — Machine Payments Protocol

### 4.1 核心定位

**MPP（Machine Payments Protocol）** 由 **Tempo Labs × Stripe** 联合设计，基于 HTTP 402 状态码，已提交 **IETF 规范草案**。

MPP 解决的是更底层的问题：**任何 API 如何向任何客户端（Agent/App/人类）收取费用，无需注册、无需 API Key**。

> "按请求付费" 的互联网原语，对标 API Key 的革命性替代。

### 4.2 核心协议流程（5 步握手）

```
Client (Agent/App)                        Server (API Provider)
      │                                           │
      │──── 1. GET /resource ────────────────────►│
      │                                           │
      │◄─── 2. HTTP 402 Payment Required ─────────│
      │     WWW-Authenticate: Payment             │
      │     {                                     │
      │       "schemes": ["tempo", "stripe",      │
      │                   "lightning", "solana"],  │
      │       "amount": "0.001",                  │
      │       "currency": "USDC.e",               │
      │       "expires_in": 300                   │
      │     }                                     │
      │                                           │
      │  3. [Client 完成支付：签名/转账/扣款]       │
      │                                           │
      │──── 4. GET /resource ────────────────────►│
      │     Authorization: Payment <credential>   │
      │                                           │
      │◄─── 5. HTTP 200 OK ────────────────────── │
      │     Payment-Receipt: <receipt>            │
      │     [资源内容]                             │
```

### 4.3 支持的支付方式

MPP 设计为**支付方式无关**（payment-method-agnostic）：

```
支付方式          │  适用场景                │  结算特性
─────────────────│─────────────────────────│──────────────
Tempo (USDC.e)   │  微支付、Agent 间支付    │  ~0.6s 最终确认
Stripe (Card)    │  传统法币支付            │  T+1 结算
Lightning (BTC)  │  极小额、即时            │  链下通道，毫秒级
Solana           │  高频微支付              │  低手续费
Stellar          │  跨境支付                │  低成本
Monad            │  高吞吐场景              │  并行EVM
```

### 4.4 关键设计原则

**幂等性（Idempotency）**：每个支付凭证绑定唯一请求，防止重放攻击：

```
Credential = {
  payment_method: "tempo",
  tx_hash: "0xabc...",        // 链上交易哈希
  nonce: "req_unique_id",      // 请求唯一标识
  timestamp: 1714000000,
  signature: "..."             // 客户端签名
}
```

**收据（Receipts）**：服务端在响应头返回支付收据，构成支付闭环：

```http
HTTP/1.1 200 OK
Payment-Receipt: version=1,scheme=tempo,tx=0xabc...,
                 amount=0.001,currency=USDC.e,
                 timestamp=1714000001
```

### 4.5 MCP 传输层支持

MPP 专门适配了 Model Context Protocol（MCP）传输层，让 AI Agent 可以通过 Tool Call 完成支付：

```json
// MCP Tool Definition
{
  "name": "call_paid_api",
  "description": "调用需要按次付费的 API",
  "inputSchema": {
    "endpoint": "string",
    "payment_method": "string",
    "max_amount": "number"
  }
}
```

### 4.6 流式支付（Streamed Payments）

MPP 支持流式资源的按量付费：

```
场景：AI Agent 请求实时数据流（如市场行情），按每1000 token 计费

流程：
1. Agent 建立支付通道（Payment Channel）
2. 每接收 N 字节/N tokens，增量签名支付
3. 会话结束时链上结算汇总金额
```

---

## 5. SPT — Shared Payment Tokens

### 5.1 核心问题

在 AI Agent 代为购物的场景中，存在根本性的安全矛盾：

```
❌ 危险方式：
买家 ──[完整卡号/CVV]──► Agent ──[完整卡号]──► 商家
(凭证暴露给第三方，无法限制用途，一旦泄露影响所有商家)

✅ SPT 方式：
买家 ──[创建 SPT]──► Stripe ──[发放令牌]──► Agent ──[令牌]──► 商家
(商家只收到受限令牌，Agent 从不接触真实支付凭证)
```

### 5.2 SPT 的约束维度

每个 SPT 由买家（通过 AI 平台）创建时，可指定多维度限制：

```json
{
  "id": "spt_1RgaZcFPC5QUO6ZCDVZuVA8q",
  "object": "shared_payment.granted_token",
  "usage_limits": {
    "currency": "usd",
    "max_amount": 10000,        // 单位：分，即 $100.00
    "expires_at": 1751587220    // UNIX 时间戳
  },
  "seller_details": {
    "network_id": "internal",   // 限定商家网络
    "external_id": "cart_xyz"   // 绑定特定购物车
  }
}
```

**约束维度**：
- **金额上限**：Token 只能用于指定金额以内的交易
- **货币限制**：只能以特定货币结算
- **时间窗口**：超时自动失效
- **商家绑定**：可限制只能被特定商家使用
- **单次使用**：使用后自动注销（防重复扣款）

### 5.3 SPT 生命周期

```
                    ┌─────────────┐
                    │    买家      │
                    └──────┬──────┘
                           │ 在 Agent UI 授权
                           ▼
                    ┌─────────────┐
                    │  AI Platform │  (e.g. OpenAI)
                    │  发放 SPT    │
                    └──────┬──────┘
                           │ SPT = issued_token
                           ▼
                    ┌─────────────┐
                    │  AI Agent   │
                    │  持有 SPT    │  ← Agent 从不知道真实卡号
                    └──────┬──────┘
                           │ 传递给商家
                           ▼
                    ┌─────────────┐
                    │   商家      │
                    │  获得 granted_token │
                    └──────┬──────┘
                           │ 创建 PaymentIntent
                           ▼
                    ┌─────────────┐
                    │   Stripe    │
                    │  克隆支付方式│
                    │  完成扣款    │
                    └─────────────┘
```

### 5.4 Webhook 事件体系

SPT 的生命周期通过事件通知各方：

```
事件名称                              接收方      触发时机
────────────────────────────────────────────────────────────
shared_payment.granted_token.used     商家        商家使用 SPT 完成支付
shared_payment.granted_token.deactivated 商家      SPT 被撤销或过期
shared_payment.issued_token.used      Agent       商家使用了 SPT（买家通知）
shared_payment.issued_token.deactivated Agent     SPT 不再有效
```

### 5.5 代码示例：商家侧使用 SPT

```python
import stripe

stripe.api_key = "sk_live_..."

# 1. 商家收到 Agent 传来的 SPT
spt_token = "spt_1RgaZcFPC5QUO6ZCDVZuVA8q"

# 2. 验证 SPT 有效性（可选）
spt = stripe.shared_payment.GrantedToken.retrieve(spt_token)
if spt.usage_limits.max_amount < order_amount:
    raise ValueError("SPT 授权金额不足")

# 3. 创建 PaymentIntent，传入 SPT
payment_intent = stripe.PaymentIntent.create(
    amount=2999,      # $29.99
    currency="usd",
    shared_payment_granted_token=spt_token,
    confirm=True,
)

print(f"支付成功: {payment_intent.id}")
```

---

## 6. ACS — Agentic Commerce Suite

### 6.1 产品定位

**ACS（Agentic Commerce Suite）** 是 Stripe 于 2025 年 12 月发布的**一站式 SaaS 解决方案**，相当于把 ACP 集成的工程工作量（原本需要 6 个月）压缩到**几分钟单击配置**。

> ACS 不是协议，而是**协议的托管实现**——Stripe 帮你托管 ACP 端点、管理商品目录同步、对接各 AI Agent。

### 6.2 核心模块

```
┌──────────────────────────────────────────────────────────────┐
│                  Agentic Commerce Suite                       │
│                                                              │
│  ┌────────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │  商品发现模块   │  │  结账简化模块  │  │  支付 & 风控模块 │ │
│  │                │  │               │  │                 │ │
│  │ • 托管 ACP 端点 │  │ • Checkout    │  │ • SPT 处理      │ │
│  │ • 商品目录上传  │  │   Sessions API│  │ • Stripe Radar  │ │
│  │ • 多 Agent 分发 │  │ • Stripe Tax  │  │ • 欺诈信号      │ │
│  │ • 实时库存同步  │  │ • 动态运费     │  │ • 差错管理      │ │
│  └────────────────┘  └───────────────┘  └─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

**已接入 ACS 的商家（截至 2025 Q4）**：
- URBN（Anthropologie、Free People、Urban Outfitters）
- Etsy、Ashley Furniture、Coach、Kate Spade
- Nectar、Revolve、Halara、Abt Electronics

### 6.3 集成渠道

ACS 支持多种接入方式：

```
直接接入：
  Stripe Dashboard → 选择 AI Agent → 一键上线

电商平台插件：
  Wix │ WooCommerce │ BigCommerce │ Squarespace │ commercetools

全渠道商务平台：
  Akeneo │ Cymbio │ Logicbroker │ Mirakl │ Pipe17 │ Rithum
```

### 6.4 商家侧集成流程

```
步骤 1：连接商品目录
  ├── 直接上传 CSV/JSON 商品数据
  └── 或连接已有 PIM/商品分发平台

步骤 2：在 Dashboard 选择 AI Agent 渠道
  └── 目前支持：ChatGPT（更多 Agent 陆续接入）

步骤 3：Stripe 自动完成：
  ├── 托管 ACP 端点
  ├── 向 Agent 分发商品信息
  ├── 处理 SPT 支付
  └── 发送订单事件到商家系统

步骤 4：商家继续使用现有履约流程
  └── ACS 只处理发现 + 结账 + 支付，不改变履约逻辑
```

---

## 7. x402 — HTTP 402 复活计划

### 7.1 历史背景

HTTP 402 状态码（Payment Required）自 1991 年 HTTP/1.0 规范起就已存在，但从未被正式定义或广泛使用。**Coinbase** 决定"激活"这个沉睡了 30 年的状态码。

### 7.2 x402 与 MPP 的关系

```
x402 ← 协议理念/RFC 草案，聚焦"链上支付 + 稳定币"
MPP  ← 完整生产实现，支持 x402 + 传统支付方式

MPP 文档明确提供 "Upgrade your x402 integration" 迁移指南
两者可视为：x402 是子集，MPP 是超集
```

### 7.3 x402 核心交互流程（Coinbase 实现）

```
客户端                         x402 服务器
   │                               │
   │─── GET /premium-content ──────►│
   │                               │
   │◄── 402 Payment Required ───────│
   │    {                          │
   │      "accepts": [{            │
   │        "scheme": "exact",     │
   │        "network": "base",     │
   │        "amount": "0.001",     │
   │        "currency": "USDC",    │
   │        "payTo": "0xabc..."    │
   │      }]                       │
   │    }                          │
   │                               │
   │  [链上转账 USDC → payTo]       │
   │                               │
   │─── GET /premium-content ──────►│
   │    Authorization: X402        │
   │    x-payment: {tx_hash, ...}  │
   │                               │
   │◄── 200 OK ─────────────────── │
   │    x-receipt: {verified, ...} │
```

### 7.4 x402 Foundation（Cloudflare × Coinbase）

**使命**：推动 x402 成为互联网级开放标准

**Cloudflare 的贡献**：
- 在 Agents SDK 内置 x402 支持
- 在 MCP 集成中支持 x402 协议
- 提出"延迟支付方案"（Deferred Payment）

**延迟支付方案**（针对爬虫/Agent 批量访问场景）：

```json
// 服务器返回的延迟支付方案
{
  "accepts": [{
    "scheme": "deferred",
    "network": "example-network-provider",
    "resource": "https://example.com/page",
    "batch_settlement": "daily",           // 每日汇总结算
    "payment_method": ["card", "stablecoin"]
  }]
}
```

**按抓取付费（Pay-Per-Crawl）**：
- Cloudflare 正在封闭测试：网站可向 AI 爬虫按页面收费
- 爬虫抓取 → 生成审计日志 → 每日通过绑定的信用卡/银行账户汇总结算

---

## 8. Tempo — L1 区块链

### 8.1 定位

**Tempo** 是由 **Paradigm × Stripe 孵化**的专用支付 L1 区块链，2026 年 3 月主网上线。

> "为稳定币支付而生的区块链" — Tempo 不是通用智能合约平台，而是专门优化了支付场景的区块链基础设施。

### 8.2 核心技术参数

```
出块时间：    ~0.6 秒（确定性最终确认，无重组风险）
Gas Token：  USD 稳定币（无需持有 ETH/SOL 等波动资产）
主要资产：    USDC.e（bridged USDC）
手续费：     极低（设计目标：亚美分级别）
```

### 8.3 支付专项设计

| 特性 | 说明 | 对比传统链 |
|------|------|-----------|
| 专用支付通道 | 协议层保障 blockspace，高峰期费用不飙升 | Ethereum Gas 波动巨大 |
| 稳定币 Gas | 用 USDC.e 付手续费 | 其他链需原生代币 |
| 内置 DEX | 稳定币间低滑点兑换 | 需外部 AMM |
| 支付元数据 | 结构化备注字段（发票号/订单号） | 需链下维护映射 |
| 确定性结算 | 0.6s 最终性，无分叉风险 | ETH 需等 12 个区块 |
| 智能账户 | 批量交易、计划支付、Passkey 签名 | EOA 账户能力有限 |

### 8.4 Tempo 在 MPP 生态中的角色

Tempo 是 MPP 的**首选区块链结算层**，也是 MPP 官网 Demo 的默认支付方式：

```
MPP 流程中使用 Tempo：
1. Agent 从 Tempo 钱包获取 USDC.e
2. MPP Server 返回 402，包含 Tempo 支付地址
3. Agent 签名并广播 Tempo 交易
4. ~0.6s 确认后，提交 tx_hash 作为 Credential
5. Server 验证链上支付，返回资源
```

---

## 9. Browserbase

### 9.1 定位

**Browserbase** 是一个**无头浏览器云服务**，专为 AI Agent 提供可靠、可扩展的浏览器自动化基础设施。

在 Agentic Commerce 生态中，Browserbase 填补了"协议化支付覆盖不到的场景"——当商家尚未接入 ACP/MPP 时，Agent 仍需通过浏览器自动化完成购物。

### 9.2 在 Agentic Commerce 中的位置

```
理想状态（协议化）：
  Agent ──[ACP/MPP]──► 商家 API ──► 下单

现实状态（大量商家尚未接入协议）：
  Agent ──[Browserbase]──► 真实浏览器 ──► 商家网页 ──► 下单
```

### 9.3 核心能力

- **持久会话**：跨请求保持 Cookie、登录态、购物车状态
- **反检测**：规避商家网站的机器人检测
- **CAPTCHA 处理**：内置人工/AI 辅助解 CAPTCHA
- **视觉操作**：支持 Computer Use 场景（截图 + 点击 + 输入）
- **并发扩展**：支持数百个并发浏览器会话

### 9.4 与协议层的关系

Browserbase 是**过渡期基础设施**：随着 ACP/MPP 覆盖率提升，直接浏览器操作会逐渐被协议化 API 调用替代。两者共存是当前阶段的必然。

---

## 10. 横向对比

### 10.1 ACP vs MPP vs x402 核心差异

| 维度 | ACP | MPP | x402 |
|------|-----|-----|------|
| **解决问题** | 商务流程（发现/结账/履约） | 支付接口（任意 API 收费） | HTTP 支付标准化 |
| **抽象层级** | 高（业务语义） | 中（协议接口） | 低（HTTP 扩展） |
| **发起方** | Stripe + OpenAI | Tempo Labs + Stripe | Coinbase |
| **标准化路径** | 开源社区（Apache 2.0） | IETF 草案 | GitHub 开放规范 |
| **支付方式** | 通过 SPT 抽象（不直接处理） | 多种（稳定币/卡/闪电网络） | 主要稳定币/链上 |
| **法币支持** | ✅（通过 Stripe） | ✅（通过 Stripe 支付意图） | 🔄（延迟支付方案中） |
| **链上支付** | ❌（通过 PSP 抽象） | ✅（原生） | ✅（原生） |
| **商家集成** | 需实现 ACP Endpoint | 需实现 MPP Server | 需实现 402 处理 |
| **AI Agent 支持** | ✅（核心设计目标） | ✅（含 MCP 传输层） | ✅ |
| **成熟度** | 生产可用（Q3 2025） | Beta（IETF Draft） | 实验性 |

### 10.2 互补关系图

```
                        ACP
                    (商务协议层)
                   /           \
                  /             \
           MPP                   SPT
       (支付协议层)           (支付原语层)
        /   |   \                  |
       /    |    \                 |
  Tempo  Stripe  Lightning       Stripe
  (L1)   (Card)  (BTC)          (PSP)

          x402
      (HTTP 标准层)
          |
    Cloudflare + Coinbase
      (基础设施推广)
```

---

## 11. 技术架构深度剖析

### 11.1 身份与授权模型

```
传统 API 授权：
  服务注册 → API Key 颁发 → 每次请求携带 Key
  问题：需要人工开户，无法零摩擦接入

MPP/ACP 授权：
  支付本身即授权 → 付款凭证（Credential）即访问令牌
  优势：无需注册，即用即付

SPT 授权模型：
  买家 → 平台 → Agent → 商家
  每层都有明确的权限边界和撤销能力
```

### 11.2 ACP 的发现机制（Discovery）

```
当前方式（中心化）：
  Stripe 维护兼容商家白名单
  AI 平台通过 Stripe 发现商家

未来方向（去中心化）：
  /.well-known/acp-configuration  ← 商家自声明
  AI Agent 扫描域名 → 自动发现 ACP 端点
  类比：robots.txt / llms.txt 的支付版本
```

### 11.3 MPP 的幂等性保证

```python
# MPP Credential 结构（Python SDK pympp）
from pympp import Credential

credential = Credential(
    payment_method="tempo",
    transaction_hash="0xabc...",
    nonce="req_" + unique_id,      # 全局唯一请求 ID
    timestamp=int(time.time()),
    amount="0.001",
    currency="USDC.e",
    signature=wallet.sign(payload)  # 防篡改签名
)

# 服务器侧验证
def verify_credential(credential: Credential) -> bool:
    # 1. 检查 nonce 是否已使用（防重放）
    if nonce_store.exists(credential.nonce):
        return False
    
    # 2. 验证链上交易
    tx = tempo_client.get_transaction(credential.transaction_hash)
    if tx.amount < required_amount:
        return False
    
    # 3. 记录 nonce，防止重放
    nonce_store.set(credential.nonce, ttl=3600)
    return True
```

### 11.4 流式支付的状态机

```
MPP 流式支付状态机：

INIT ──[建立支付通道]──► CHANNEL_OPEN
                              │
                              │ [接收数据块]
                              ▼
                         STREAMING ◄──[增量支付签名]──┐
                              │                       │
                              │ [数据传输中]            │
                              └───────────────────────┘
                              │
                              │ [会话结束 / 超时]
                              ▼
                         SETTLING
                              │
                              │ [链上最终结算]
                              ▼
                          CLOSED
```

---

## 12. 安全与反欺诈

### 12.1 AI Agent 带来的新型欺诈向量

```
传统欺诈模式：
  - 盗卡欺诈（Card Testing）
  - 账号接管（Account Takeover）
  - 退款欺诈（Friendly Fraud）

Agent 特有欺诈模式：
  - Prompt Injection 操控（恶意网站通过注入 Prompt 诱导 Agent 消费）
  - Agent 误判指令（Agent 误解用户意图，下高额订单）
  - 批量自动化攻击（Agent 高速发起大量低价值交易）
  - 凭证泄露链（Agent 在多个商家间泄露 SPT）
```

### 12.2 Stripe Radar 的 Agent 适配

传统 Radar 风控信号基于"人类行为特征"（鼠标移动轨迹、打字速度等），在 Agent 流量中全部失效。Stripe 正在为 ACS 专门训练 Agent 流量的风控模型：

```
Agent 友好的风控信号：
  ✓ SPT 元数据（金额限制、商家绑定）
  ✓ Agent 平台身份（ChatGPT 官方 Agent vs 未知 Agent）
  ✓ 交易模式（时间分布、金额分布）
  ✓ SPT 使用历史（首次使用 vs 多次使用）
  
待开发的新信号：
  ? Agent 行为熵（请求频率规律性）
  ? 商品选择逻辑（是否符合用户历史偏好）
  ? 链上凭证质量（Tempo 账户历史）
```

### 12.3 SPT 安全模型的 Defense in Depth

```
层级 1：买家授权
  买家在 AI 平台 UI 中明确授权，设置金额/时间/商家限制

层级 2：令牌隔离
  Agent 持有的 SPT 不含真实支付信息，无法被反推出原始卡号

层级 3：商家范围限制
  SPT 可绑定特定 seller_details.network_id，跨商家使用会被拒绝

层级 4：单次使用 / 有限使用
  使用后状态变为 deactivated，Webhook 通知各方

层级 5：实时撤销
  买家可随时通过 AI 平台撤销 SPT，Agent 下次尝试使用即失败

层级 6：Radar 风控
  基于 Agent 流量特征的异常检测
```

---

## 13. 开发者集成路径

### 13.1 商家接入 ACP（使用 Stripe ACS）

**最快路径（使用 Stripe Dashboard，无需写代码）**：
1. 登录 Stripe Dashboard
2. 进入 Agentic Commerce 设置
3. 上传商品目录（CSV 或连接 PIM）
4. 选择目标 AI Agent 渠道（当前：ChatGPT）
5. 申请加入对应 AI 平台
6. 上线后，通过 Stripe Webhook 接收订单事件

**自定义 ACP Endpoint（需要编码）**：

```python
# FastAPI 实现 ACP Endpoint 示例
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CheckoutRequest(BaseModel):
    product_id: str
    quantity: int
    shared_payment_token: str
    shipping_address: dict

@app.get("/.well-known/acp-configuration")
async def acp_config():
    return {
        "version": "1.0",
        "merchant": {"id": "my_shop", "name": "My Shop"},
        "payment": {"accepted_tokens": ["stripe_spt"]},
        "endpoints": {
            "catalog": "/acp/v1/catalog/search",
            "checkout": "/acp/v1/checkout/sessions"
        }
    }

@app.post("/acp/v1/checkout/sessions")
async def create_checkout(req: CheckoutRequest):
    # 验证 SPT
    spt = stripe.shared_payment.GrantedToken.retrieve(
        req.shared_payment_token
    )
    
    # 创建订单
    order = create_order(req.product_id, req.quantity, req.shipping_address)
    
    # 发起支付
    payment_intent = stripe.PaymentIntent.create(
        amount=order.total,
        currency="usd",
        shared_payment_granted_token=req.shared_payment_token,
        confirm=True,
    )
    
    return {"order_id": order.id, "status": "confirmed"}
```

### 13.2 API 服务商接入 MPP

**Python SDK（pympp）**：

```python
from pympp import MPPServer, PaymentChallenge

server = MPPServer(
    price=0.001,           # 每次请求 0.001 USDC.e
    currency="USDC.e",
    accepted_methods=["tempo", "stripe"],
    tempo_address="0xYourAddress..."
)

@app.get("/api/premium-data")
@server.require_payment
async def get_premium_data():
    return {"data": "高价值数据内容"}
```

**TypeScript SDK（mppx）**：

```typescript
import { createMPPServer } from 'mppx';

const mpp = createMPPServer({
  price: '0.001',
  currency: 'USDC.e',
  methods: ['tempo', 'stripe'],
  tempoAddress: '0xYourAddress...',
});

app.get('/api/data', mpp.middleware(), (req, res) => {
  res.json({ data: '付费内容' });
});
```

### 13.3 AI Agent 集成 MPP（作为付款方）

```python
from pympp import MPPClient
from tempo import TempoWallet

# 初始化带钱包的 MPP 客户端
wallet = TempoWallet.from_private_key(os.getenv("TEMPO_PRIVATE_KEY"))
client = MPPClient(wallet=wallet)

# Agent 调用付费 API（自动处理 402 → 支付 → 重试）
async def call_paid_api(endpoint: str, params: dict):
    response = await client.get(endpoint, params=params)
    # client 自动：
    # 1. 发送请求
    # 2. 收到 402，解析支付要求
    # 3. 从钱包扣款
    # 4. 重试请求，携带支付凭证
    # 5. 返回最终响应
    return response.json()

# 在 Agent 工具中使用
result = await call_paid_api(
    "https://api.dataservice.com/market-data",
    {"symbol": "BTC", "interval": "1m"}
)
```

---

## 14. 生态现状与关键玩家

### 14.1 玩家全景图

```
协议制定者：
  Stripe           ── ACP + SPT + ACS + MPP（联合设计）
  OpenAI           ── ACP（联合设计）+ ChatGPT 首个实现
  Coinbase         ── x402 协议 + x402 Foundation
  Cloudflare       ── x402 Foundation + 按抓取付费
  Tempo Labs       ── MPP（联合设计）+ Tempo L1 区块链

基础设施：
  Browserbase      ── Agent 浏览器自动化
  Paradigm         ── Tempo 投资孵化方

早期采用商家：
  Etsy, URBN, Coach, Kate Spade, Ashley Furniture
  Revolve, Halara, Nectar, Abt Electronics

平台渠道：
  WooCommerce, Wix, BigCommerce, Squarespace, commercetools
  Akeneo, Cymbio, Logicbroker, Mirakl, Pipe17, Rithum
```

### 14.2 Stripe 的战略意图

Stripe 在本次 Agentic Commerce 浪潮中扮演了**协议制定者 + 最大受益者**的双重角色：

```
协议层：  主导 ACP + MPP 设计，确保 Stripe 是首选 PSP
产品层：  ACS 将 6 个月集成压缩为数分钟，降低迁移成本
数据层：  SPT 令牌化让所有 Agent 交易流经 Stripe
风控层：  Radar 扩展到 Agent 流量，构建护城河
```

### 14.3 OpenAI 的布局

ChatGPT 成为**首个**实现 ACP 的 AI 平台，意味着：
- 与 Stripe 深度绑定（商家通过 Stripe ACS 接入 ChatGPT 购物）
- 获得"AI 购物渠道"的先发优势
- 正在构建端到端的 AI 购物体验（类比 Apple Pay 之于手机支付）

---

## 15. 挑战与趋势

### 15.1 当前主要挑战

**技术挑战**：
- **发现机制缺失**：没有统一的 ACP 商家目录，AI 平台无法自动发现兼容商家
- **跨协议互操作**：ACP + MPP + x402 三套协议共存，开发者需要了解多套标准
- **链上支付的用户体验**：普通用户不熟悉钱包/稳定币，MPP 的区块链支付路径仍有摩擦

**商业挑战**：
- **商家覆盖率低**：目前支持 ACP 的商家极少，Agent 能买的东西有限
- **消费者教育**：用户是否愿意授权 AI 代为支付，需要建立信任
- **责任边界模糊**：Agent 误操作导致的退款/争议，谁承担责任？

**监管挑战**：
- **反洗钱合规**：Machine-to-Machine 支付如何进行 KYC/AML？
- **消费者保护**：Agent 代购场景下的退款权利如何保障？
- **稳定币监管**：MPP 的稳定币支付路径面临各国不同监管要求

### 15.2 未来趋势预测

**短期（2026）**：
- ACS 商家数量快速增长（目标数万商家）
- MPP IETF 草案正式提交，获得更多社区反馈
- x402 延迟支付方案落地，Cloudflare "按抓取付费"公测

**中期（2027-2028）**：
- ACP 发现机制标准化（`/.well-known/acp-configuration` 成为事实标准）
- 更多 AI 平台接入 ACP（Claude、Gemini 等）
- Tempo 链上稳定币支付成为 API 微支付的主流选择
- 监管框架逐渐清晰（欧盟/美国 AI 支付监管落地）

**长期（2029+）**：
- Agent 支付量超过人类直接支付量（部分品类）
- "支付即授权"模式重塑 API 经济
- 商家将 "Agent Channel Revenue" 列为独立财报项目

### 15.3 对 AI Agent 工程师的启示

```
今天需要做的事：

1. 关注 ACP 规范演进（github.com/agentic-commerce-protocol）
2. 在 Agent 工具调用层预留"支付能力"的接口设计
3. 评估 MPP Python SDK（pympp）用于 API 调用场景
4. 在系统设计中考虑 SPT 的凭证传递与安全存储
5. 对于 Agent 执行购买的场景，预置"用户确认"步骤
   （require_user_confirmation: true 是当前 ACP 的默认要求）
```

---

## 附录：关键资源汇总

| 资源 | URL | 用途 |
|------|-----|------|
| ACP 官网 | https://www.agenticcommerce.dev/ | 协议文档 + Demo |
| ACP GitHub | https://github.com/agentic-commerce-protocol/acp | 规范源码 |
| MPP 官网 | https://mpp.dev/ | 协议文档 + SDK |
| MPP IETF 规范 | https://paymentauth.org | 标准草案 |
| Stripe ACS 博客 | https://stripe.com/blog/agentic-commerce-suite | 产品介绍 |
| Stripe SPT 文档 | https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens | API 参考 |
| Stripe ACS 集成 | https://docs.stripe.com/agentic-commerce/enable-in-context-selling-on-ai-agents | 集成指南 |
| x402 GitHub | https://github.com/coinbase/x402 | 协议实现 |
| Cloudflare x402 | https://blog.cloudflare.com/x402/ | Foundation 公告 |
| Tempo | https://tempo.xyz/ | L1 区块链 |
| Browserbase | https://browserbase.com/ | Agent 浏览器基础设施 |

---

*本文基于 2026 年 4 月公开资料整理。Agentic Commerce 生态演进极快，建议定期查阅各官方文档获取最新动态。*
