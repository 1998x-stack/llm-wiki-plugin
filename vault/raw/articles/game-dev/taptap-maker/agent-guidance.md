# AI / Agent 文档导航

这篇文档只做一件事：帮助 AI / agent 用更少的 token 找到更可靠的信息。
默认优先级永远是 `源码 > 当前总览文档 > 当前专题文档 > 历史文档`。

## 先看什么

如果你要理解整个项目，先读这几个入口：

1. `docs/architecture.md`
2. `apps/server/src/central-server/index.ts`
3. `apps/server/src/gateway-server/index.ts`
4. `apps/agent-server/src/bin/Manager.ts`
5. `packages/database/src/schema.ts`
6. `packages/config/src/config.ts`

如果你要改某个子系统，只读这个子系统的入口和一篇当前文档，不要先扫完整个 `docs/`。

## 最权威的目录

- `apps/server/src/central-server`
- `apps/server/src/gateway-server`
- `apps/agent-server/src/{bin,app,routes,lib}`
- `packages/{database,config,shared,types,logger,voice-input}`
- `apps/web/src/{pages,components,contexts,hooks,lib}`

这些目录里的入口文件和 schema，通常比历史文档更可信。

## token-aware 检索方式

- 先按子系统搜文件名，不要直接读 `docs/*.md`。
- 先读 1 篇当前文档，再看源码。
- 如果文档标题里有 `plan`、`summary`、`fix`、`analysis`、`migration`、`test`，默认把它当作快照，而不是当前事实源。
- 如果文档很长，先找标题和目录，再定点跳读，不要整篇吞。
- 如果你发现文档和源码冲突，立刻以源码为准。

## 推荐阅读顺序

### 全局

- `docs/architecture.md`
- `docs/local-development.md`
- `docs/technical-debt.md`

### 业务专题

- `docs/publish-panel-implementation.md`
- `docs/skillhub-design.md`

### 如果你在处理语音输入

- `packages/voice-input/src/shared/events.ts`
- `packages/voice-input/src/shared/types.ts`
- `packages/voice-input/src/client/use-voice-input.ts`
- `packages/voice-input/src/server/index.ts`

### 如果你在处理数据模型或消息链路

- `packages/database/src/schema.ts`
- `apps/server/src/central-server/chats.routes.ts`
- `apps/server/src/gateway-server/servers/feWSServer.ts`

## 要谨慎的历史文档

这些入口可能仍带有历史表述，使用时应始终回到源码确认：

- `packages/voice-input/README.md`
- `apps/server/README.md`

经验上，如果一篇文档看起来像一次修复、一次迁移、一次测试、一次总结，就不要依赖它。

## 简单规则

- 先找当前代码，再找当前总览文档。
- 只在需要时才读历史文档。
- 不要因为文档存在就假设它是对的。
- 不要一次性读完所有专题文档。
