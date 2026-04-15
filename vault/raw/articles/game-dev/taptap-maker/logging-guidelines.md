# Logging Guidelines

统一日志系统使用指南。

## 基本原则

### 1. 日志级别选择

- **DEBUG**: 详细调试信息（开发环境）
  - 变量值、函数参数、执行路径
  - 仅在开发环境启用

- **INFO**: 业务流程关键节点
  - 服务启动/停止
  - 重要业务操作（创建项目、创建 Chat）
  - 定时任务执行

- **WARN**: 潜在问题，不影响正常运行
  - 使用默认值、降级策略
  - 接近资源限制（磁盘空间、内存）
  - 第三方服务响应慢

- **ERROR**: 错误但可恢复
  - API 调用失败（可重试）
  - 数据库操作失败
  - 文件读写错误

- **FATAL**: 严重错误，服务无法继续
  - 数据库连接失败
  - 配置文件缺失
  - 必需依赖服务不可用

### 2. 日志内容规范

**明确的问题描述**

```typescript
// ❌ 不好
logger.error("Error occurred");

// ✅ 好
logger.error("Failed to create chat", {
  chatId,
  appId,
  error: err.message,
});
```

**包含上下文信息**

```typescript
// ❌ 缺少上下文
logger.warn("Rate limit exceeded");

// ✅ 包含上下文
logger.warn("Rate limit exceeded", {
  userId,
  endpoint: "/api/chats",
  limit: 100,
  current: 150,
});
```

**避免敏感信息**

```typescript
// ❌ 记录敏感信息
logger.info("User logged in", {
  password: req.body.password, // ❌
});

// ✅ 过滤敏感信息
logger.info("User logged in", {
  userId,
  ip: req.ip,
});
```

## 环境变量配置

系统使用单个环境变量 `LOGS_ROOT` 配置所有日志目录：

### 日志目录结构

- **`<LOGS_ROOT>/central-server/YYYY-MM-DD.log`**
  - Central Server 服务日志

- **`<LOGS_ROOT>/agent-server/YYYY-MM-DD.log`**
  - Agent Server 服务日志

- **`<LOGS_ROOT>/web-server/YYYY-MM-DD.log`**
  - Web Server 服务日志（生产环境/SSR）

- **`<LOGS_ROOT>/devel-client/YYYY-MM-DD.log`**
  - 开发环境客户端日志上报

- **`<LOGS_ROOT>/preview-server/<userId>/<appId>/YYYY-MM-DD.log`**
  - 用户项目预览服务器日志

- **`<LOGS_ROOT>/user-client/<userId>/<appId>/YYYY-MM-DD.log`**
  - 用户项目客户端日志上报

### 配置示例

开发环境 `.env`：

```bash
# 统一日志根目录
LOGS_ROOT=./logs
```

生产环境 `.env`：

```bash
# 统一日志根目录
LOGS_ROOT=/var/log/taptap-code
```

## 使用方法

### 基础使用

```typescript
import { BaseLogger, ConsoleOutput, LogLevel } from "@taptap-code/logger";

// 创建 logger 实例
const logger = new BaseLogger({
  level: LogLevel.INFO,
  outputs: [new ConsoleOutput({ colors: true })],
  enabled: true,
});

// 记录日志
logger.info("Server started", { port: 3000 });
logger.error("Database connection failed", {
  error: err.message,
  retries: 3,
});
```

### 多输出配置

```typescript
import {
  BaseLogger,
  ConsoleOutput,
  FileOutput,
  DatabaseOutput,
  LogLevel,
} from "@taptap-code/logger";
import { Database } from "@taptap-code/database";

const db = new Database();

const logger = new BaseLogger({
  level: LogLevel.DEBUG,
  outputs: [
    // 控制台：所有日志
    new ConsoleOutput({ colors: true }),

    // 文件：INFO 及以上
    new FileOutput({
      dir: "./.logs",
      rotate: "daily",
      keep: 30,
      maxSize: 100 * 1024 * 1024, // 100MB
    }),

    // 数据库：仅 ERROR 和 FATAL（使用独立日志数据库）
    new DatabaseOutput({
      db: db.getLogsDB(),
      minLevel: LogLevel.ERROR,
    }),
  ],
});
```

### 服务器日志配置

使用 `LOGS_ROOT` 环境变量配置日志目录：

```typescript
const isProd = process.env.NODE_ENV === "production";
const logRoot = process.env.LOGS_ROOT ?? "./logs";

// Central Server
const centralLogger = new BaseLogger({
  level: isProd ? LogLevel.INFO : LogLevel.DEBUG,
  outputs: [
    new ConsoleOutput({ colors: !isProd }),
    new FileOutput({
      dir: `${logRoot}/central-server`,
      rotate: "daily",
      keep: isProd ? 90 : 30,
    }),
    new DatabaseOutput({
      db: db.getLogsDB(),
      minLevel: LogLevel.ERROR,
    }),
  ],
});

// Agent Server
const agentLogger = new BaseLogger({
  level: isProd ? LogLevel.INFO : LogLevel.DEBUG,
  outputs: [
    new ConsoleOutput({ colors: !isProd }),
    new FileOutput({
      dir: `${logRoot}/agent-server`,
      rotate: "daily",
      keep: isProd ? 90 : 30,
    }),
    new DatabaseOutput({
      db: db.getLogsDB(),
      minLevel: LogLevel.ERROR,
    }),
  ],
});

// Web Server (SSR/Production)
const webLogger = new BaseLogger({
  level: isProd ? LogLevel.INFO : LogLevel.DEBUG,
  outputs: [
    new ConsoleOutput({ colors: !isProd }),
    new FileOutput({
      dir: `${logRoot}/web-server`,
      rotate: "daily",
      keep: isProd ? 90 : 30,
    }),
    new DatabaseOutput({
      db: db.getLogsDB(),
      minLevel: LogLevel.ERROR,
    }),
  ],
});
```

### 客户端日志配置

```typescript
const logRoot = process.env.LOGS_ROOT || "./logs";

// 开发环境客户端日志路径
function getDevelClientLogPath(): string {
  return `${logRoot}/devel-client`;
}

// 用户项目客户端日志路径
function getUserClientLogPath(userId: string, appId: string): string {
  return `${logRoot}/user-client/${userId}/${appId}`;
}
```

### 用户项目预览服务器日志配置

```typescript
const logRoot = process.env.LOGS_ROOT || "./logs";

// 用户项目预览服务器日志
function createPreviewLogger(userId: string, appId: string) {
  return new BaseLogger({
    level: LogLevel.INFO,
    outputs: [
      new FileOutput({
        dir: `${logRoot}/preview-server/${userId}/${appId}`,
        rotate: "daily",
        keep: 30,
      }),
    ],
  });
}
```

## 最佳实践

### 1. 结构化日志

使用 meta 对象传递结构化数据：

```typescript
logger.info("Chat message received", {
  chatId,
  messageId,
  type: "user_prompt",
  length: content.length,
  timestamp: Date.now(),
});
```

### 2. 错误处理

捕获异常时记录完整堆栈：

```typescript
try {
  await createChat(appId, title);
} catch (err) {
  logger.error("Failed to create chat", {
    appId,
    title,
    error: err instanceof Error ? err.message : String(err),
    stack: err instanceof Error ? err.stack : undefined,
  });
  throw err;
}
```

### 3. 性能关键路径

避免在高频路径记录 DEBUG：

```typescript
// ❌ 每个消息都记录 DEBUG
app.post("/messages", (req, res) => {
  logger.debug("Message received", req.body); // 高频操作
  // ...
});

// ✅ 仅记录关键事件
app.post("/messages", (req, res) => {
  if (req.body.length > 10000) {
    logger.warn("Large message received", {
      size: req.body.length,
    });
  }
  // ...
});
```

### 4. 异步操作

Logger 异步写入，无需 await：

```typescript
// ✅ 正确：fire-and-forget
logger.info("Processing started", { taskId });
await processTask(taskId);
logger.info("Processing completed", { taskId });

// ❌ 错误：不需要 await
// await logger.info(...); // Logger.info 返回 void
```

### 5. 服务关闭

优雅关闭时清理资源：

```typescript
process.on("SIGTERM", async () => {
  logger.info("Shutting down gracefully");

  // 关闭 logger（等待写入完成）
  await logger.close();

  process.exit(0);
});
```

## 日志轮转

### 保留策略

不同环境使用不同的日志保留策略（在 `apps/server/src/shared/logger.ts` 中配置）：

- **开发环境**：保留 30 天
- **生产环境**：保留 90 天

策略由环境变量 `NODE_ENV` 控制：

- `NODE_ENV=production` → 90 天
- 其他值（包括未设置） → 30 天

### 自动轮转（FileOutput）

FileOutput 自动按策略轮转：

- `daily`: 每天创建新文件（默认）
- `weekly`: 每周创建新文件
- `monthly`: 每月创建新文件

超过 `maxSize` 时自动轮转当前文件（重命名为 `.log.timestamp`）。

### 手动清理（rotate-logs.sh）

使用 `LOGS_ROOT` 目录：

```bash
# 开发环境：清理 30 天前的日志
./packages/logger/scripts/rotate-logs.sh ./.logs 30

# 生产环境：清理 90 天前的日志
./packages/logger/scripts/rotate-logs.sh /var/log/taptap-code 90
```

定时任务（cron）：

```cron
# 每天凌晨 2 点清理日志
0 2 * * * /path/to/rotate-logs.sh /var/log/taptap-code 90
```

## 常见问题

### Q: 日志文件过大怎么办？

A: 调整 `maxSize` 和 `keep` 参数：

```typescript
new FileOutput({
  maxSize: 50 * 1024 * 1024, // 减小单文件大小
  keep: 14, // 减少保留天数
});
```

### Q: 如何禁用某个输出？

A: 移除对应的 output：

```typescript
const logger = new BaseLogger({
  outputs: [
    new ConsoleOutput(), // 仅保留控制台
    // FileOutput 已移除
  ],
});
```

### Q: 如何临时提升日志级别？

A: 通过环境变量控制：

```typescript
const logger = new BaseLogger({
  level: (process.env.LOG_LEVEL as LogLevel) || LogLevel.INFO,
});
```

```bash
# 启动时设置
LOG_LEVEL=debug bun run dev
```

### Q: 数据库日志表会无限增长吗？

A: 需要定期清理：

```sql
-- 删除 90 天前的日志
DELETE FROM system_logs
WHERE timestamp < (strftime('%s', 'now', '-90 days') * 1000);
```

建议创建定时任务（Agent Server 启动时执行）。

## 参考

- `packages/logger/src/types.ts` - 接口定义
- `packages/logger/src/logger.ts` - 核心实现
- `packages/logger/src/outputs/` - 输出实现
- `packages/database/src/schema.ts` - system_logs 表定义
