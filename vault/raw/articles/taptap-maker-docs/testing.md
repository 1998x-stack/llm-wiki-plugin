# 测试指南

这篇只保留当前链路下仍然有效的本地测试入口。
如果你需要完整启动步骤，先看 [local-development.md](./local-development.md)。

## 本地最小测试路径

1. 准备 `.env`

```bash
cp .env.example .env
```

2. 启动依赖和应用

```bash
cd infra && docker compose --env-file ../.env up -d && cd ..
pnpm install
pnpm central:dev
pnpm gateway:dev
pnpm web:dev
```

3. 进行 fake login

```bash
curl -X POST http://127.0.0.1:3026/api/auth/fake-login
```

或者直接打开：

```text
http://127.0.0.1:3016?fake-login=true
```

## 当前聊天链路怎么测

当前聊天主链路是：

- 前端页面：`http://127.0.0.1:3016`
- Central Server：`http://127.0.0.1:3026`
- Gateway：
  - HTTP：`http://127.0.0.1:3366`
  - WebSocket：`ws://127.0.0.1:3344/ws`
- Manager：`http://127.0.0.1:${MANAGER_PORT}`

不要再按旧的 SSE / `x-user-id` / `:3036` 代理模型排查聊天页。

## 推荐检查项

### Chat 页面

1. 创建一个测试 app
2. 进入 `/chat/:chatId`
3. 发送一条 prompt
4. 确认：
   - 页面能建立 WebSocket 会话
   - 消息列表正常更新
   - `prompt/stopped` 后界面状态能恢复

### 发布面板

1. 打开 PublishPanel
2. 确认能获取或创建 publish session
3. 触发一次生成或刷新操作
4. 确认 `prompt/stopped` 后能重新读取 `project.json`

### 语音输入

1. 确认浏览器麦克风权限
2. 按住语音按钮
3. 观察是否能收到 `_taptap/voice/started`
4. 观察 `partial` / `partial-final` / `final`

## 常见问题

### 页面空白或路由异常

- 检查浏览器控制台错误
- 运行 `pnpm lint`
- 检查 `apps/web` 最近改动是否引入类型错误或渲染异常

### 聊天消息不返回

- 确认 Central `:3026`、Gateway `:3366/:3344`、Manager 端口都已启动
- 确认 `VITE_WS_BASE_URL` 带 `/ws`
- 确认 `HTTP_AGENT_SERVER_URL` 和 `MANAGER_PORT` 一致
- 确认 `JWT_SECRET` 在所有服务中一致

### fake login 不生效

- 确认 `.env` 中启用了 `ENABLE_FAKE_LOGIN=true`
- 检查浏览器中的 `taptap_access_token` / `taptap_user`

### Manager / workspace 相关失败

- 确认 Docker daemon 正常
- 确认 `/var/run/docker.sock` 可用
- 确认 `WORKSPACES_ROOT` 是绝对路径
- 确认 `MYSQL_URL` 已配置

## 常用命令

```bash
pnpm lint
pnpm test:unit
pnpm test:integration
pnpm db:health
pnpm stop
```

如果你在测试当前实现，优先相信源码入口和 [architecture.md](./architecture.md)，不要再按旧的 SSE 文档心智排查。
