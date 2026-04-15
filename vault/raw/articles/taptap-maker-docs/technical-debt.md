# Technical Debt

这篇只记录 **当前仍开放、且对实现或安全真正有影响** 的事项。
已解决项、长篇方案推演和重复背景已经移除。

## P0

### Token 与用户数据仍存放在 `localStorage`

- 代码位置：`apps/web/src/lib/auth.ts`
- 风险：XSS 时可直接读取 access token、refresh token 和用户信息
- 现状：仍是当前实现
- 建议：
  - 短期加 CSP
  - 中期迁移到 httpOnly cookie 或更安全的 token 策略

### Manager API 缺少强认证边界

- 代码位置：`apps/agent-server/src/app/manager.ts`
- 风险：Manager 侧创建 workspace、prompt、回滚等接口如果暴露到宿主机网络，边界过弱
- 建议：
  - Gateway -> Manager 增加 shared secret 或等效认证
  - 或进一步收紧监听地址和网络暴露面

### 用户容器权限过高

- 代码位置：`apps/agent-server/src/lib/docker.ts`
- 风险：
  - `root`
  - 高权限 capability
  - 安全配置过宽
- 建议：
  - 收缩 capability
  - 恢复 seccomp / AppArmor 等隔离
  - 验证非 root 运行可能性

### `ANTHROPIC_API_KEY` 注入用户容器

- 代码位置：`apps/agent-server/src/lib/docker.ts`
- 风险：用户代码可读取平台 key
- 建议：
  - 代理转发模式
  - 或短期 scoped token

### `FEISHU_MSG_BOT_KEY` 注入用户容器

- 代码位置：`apps/agent-server/src/routes/manager/userspace.ts`
- 风险：用户代码可直接滥用 webhook
- 建议：只在 Manager 进程使用，不再传入用户容器

## P1

### CSP 缺失

- 风险：Web 侧 XSS 防护能力弱
- 关联：这也是 `localStorage` token 风险的放大器
- 建议：先做最小可用 CSP，再逐步收紧

### 前端缺少 SRI / 外部资源完整性约束

- 风险：第三方资源被替换时缺少校验
- 建议：若继续依赖外部资源，补完整性校验策略

### 部署 / 健康检查 / 关键链路测试覆盖不足

- 风险：环境变更、部署脚本、服务编排和关键回调链路容易回归
- 建议：
  - 增加面向运行时的 smoke tests
  - 增加健康检查与启动链路验证

## P2

### UUID 转换仍较分散

- 主要位置：`packages/shared/src/uuid.ts` 被各层重复调用
- 风险：边界处容易遗漏，日志可读性也一般
- 建议：逐步把转换收拢到更稳定的边界层

### 日志脱敏仍不系统

- 风险：日志中可能出现敏感路径、token、用户数据或内部 URL
- 建议：统一 redaction 策略，不只靠调用方自觉

### SkillHub 设计与代码现实不一致

- 文档位置：`docs/skillhub-design.md`
- 代码现实：主 routes 和同步逻辑仍未完整启用
- 风险：agent 容易把设计案误当现成功能
- 建议：在真正落地前保持“设计案”定位，不要继续扩写成事实文档

## 处理顺序建议

1. 先处理容器密钥暴露和 Manager 认证边界
2. 再补 Web 侧 CSP
3. 再补运行时 smoke tests
4. 最后再做 UUID / 日志等结构性收敛

## 使用方式

如果你是 agent：

- 这篇文档只告诉你“哪些坑还在”
- 不代表这里列出的每一项都适合在当前任务里顺手处理
- 只在和当前任务直接相关时再展开源码检查
