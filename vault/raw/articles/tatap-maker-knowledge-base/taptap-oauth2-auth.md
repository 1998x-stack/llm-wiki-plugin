# TapTap OAuth 2.0 授权登录接入指南

## 概述

TapTap 使用 OAuth 2.0 Authorization Code Grant 流程（带 PKCE 扩展）提供第三方授权登录能力，允许外部应用获取用户的头像、昵称、openId、unionId 等基本信息。

### 环境地址

| 环境         | 授权页面                               | Token 接口                                    | 用户信息接口                                              |
| ------------ | -------------------------------------- | --------------------------------------------- | --------------------------------------------------------- |
| **生产环境** | `https://accounts.taptap.cn/authorize` | `https://accounts.tapapis.cn/oauth2/v1/token` | -                                                         |
| **RND 沙盒** | `https://accounts.xdrnd.cn/authorize`  | `https://oauth.api.xdrnd.cn/oauth2/v1/token`  | `https://open.api.xdrnd.cn/account/profile/v1?client_id=` |

**外部接入参考：** [OAuth 2.0 接入外部 Web 流程](https://OAuth 2.0 接入 外部 Web 流程)

## 接入流程概览

TapTap OAuth 2.0 提供两种接入方式：

| 接入方式          | 适用场景           | 安全机制              |
| ----------------- | ------------------ | --------------------- |
| **Server Secret** | 服务端调用         | 使用 `client_secret`  |
| **PKCE**          | 客户端调用（推荐） | 使用 `code_challenge` |

### 标准授权流程

```
┌─────────────┐
│   用户点击   │
│  TapTap 登录 │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 1. 跳转到授权页面                      │
│    GET /authorize                    │
│    - client_id                       │
│    - redirect_uri                    │
│    - scope                           │
│    - state                           │
│    - code_challenge (PKCE)           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│   用户授权   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 2. 回调到应用                         │
│    redirect_uri?code=xxx&state=xxx   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 3. 获取 Access Token                 │
│    POST /oauth2/v1/token             │
│    - code                            │
│    - code_verifier (PKCE)            │
│    - client_secret (Server)          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│   登录成功   │
└─────────────┘
```

## API 接口详解

### 1. 请求授权页面

**接口地址：** `GET https://accounts.taptap.cn/authorize`

#### 必填参数

| 参数            | 类型   | 说明                                                 |
| --------------- | ------ | ---------------------------------------------------- |
| `client_id`     | string | 应用的 Client ID（在开发者中心获取）                 |
| `response_type` | string | 固定值：`code`                                       |
| `scope`         | string | 权限范围，如 `public_profile`。多个 scope 用逗号分隔 |
| `redirect_uri`  | string | 授权成功后的回调地址                                 |
| `state`         | string | 用于防止 CSRF 攻击的随机字符串，回调时会原样返回     |

#### PKCE 相关参数（客户端接入推荐）

| 参数                    | 类型   | 说明                                     |
| ----------------------- | ------ | ---------------------------------------- |
| `code_challenge`        | string | `base64urlencode(sha256(code_verifier))` |
| `code_challenge_method` | string | 固定值：`S256`                           |

**code_verifier 生成规则：**

- 字符集：`A-Z`, `a-z`, `0-9`, `-`, `.`, `_`, `~`
- 长度：43-128 个字符
- 加密方式：SHA256 哈希后 Base64 URL 编码

#### 可选参数

| 参数                   | 说明                                                |
| ---------------------- | --------------------------------------------------- |
| `x_phone_verify_token` | 阿里云号码认证 token，用于一键登录                  |
| `x_login_type`         | 优先展示的登录方式：`phone` 或 `email`              |
| `theme_mode`           | UI 主题模式                                         |
| `platform`             | 平台标识：`android`、`ios`、`web`                   |
| `version`              | SDK 版本号，如 `3.19.3`                             |
| `info`                 | 设备信息 JSON，如 `{"device_id":"Xiaomi 2203121C"}` |
| `session_id`           | 登录埋点串端需求                                    |
| `session_type`         | 登录埋点类型：`taptap` 或 `tapsdk`                  |
| `show_type`            | 展示类型：`full` 或 `half`                          |

#### 请求示例

```http
GET https://accounts.taptap.cn/authorize?
  client_id=znaefihegkbapi5jho&
  response_type=code&
  scope=public_profile&
  redirect_uri=https%3A%2F%2Fwww.example.com%2Fcallback&
  state=269e94cd-ac2b-4edc-b227-e10f327cbbbc&
  code_challenge_method=S256&
  code_challenge=_qxt5tSmAsyz4E_XHmQN07N9qkbsoa-Nvo1viK_O1yo
```

#### 回调示例

**授权成功：**

```
https://www.example.com/callback?code=8aee60afd7d3f616cd20b9bed236bb7d&state=269e94cd-ac2b-4edc-b227-e10f327cbbbc
```

**授权失败：**

```
https://www.example.com/callback?error=access_denied&state=269e94cd-ac2b-4edc-b227-e10f327cbbbc
```

### 2. 获取 Access Token

**接口地址：** `POST https://accounts.tapapis.cn/oauth2/v1/token`

> ⚠️ **重要**：此接口要求使用 `application/x-www-form-urlencoded` 格式，**不是** JSON 格式（文档示例有误）。

#### 请求参数

| 参数            | 必填 | 类型   | 说明                                        |
| --------------- | ---- | ------ | ------------------------------------------- |
| `client_id`     | 是   | string | 应用的 Client ID                            |
| `grant_type`    | 是   | string | 固定值：`authorization_code`                |
| `secret_type`   | 是   | string | 固定值：`hmac-sha-1`                        |
| `code`          | 是   | string | 授权页面返回的 code                         |
| `redirect_uri`  | 是   | string | 必须与授权请求中的 `redirect_uri` 完全一致  |
| `client_secret` | 否\* | string | 服务端密钥（服务端流程必填，PKCE 流程不填） |
| `code_verifier` | 否\* | string | PKCE 流程必填，即第一步生成的随机字符串     |

_注：`client_secret` 和 `code_verifier` 二选一_

#### 返回数据

TapTap API 返回格式为 `{ data: {...}, success: true }`，实际的 token 数据在 `data` 字段中：

| 字段                 | 类型    | 说明                       |
| -------------------- | ------- | -------------------------- |
| `success`            | boolean | 请求是否成功               |
| `now`                | number  | 服务器时间戳               |
| `data.kid`           | string  | MAC Key ID                 |
| `data.access_token`  | string  | 访问令牌                   |
| `data.token_type`    | string  | 令牌类型，固定为 `mac`     |
| `data.mac_key`       | string  | MAC 密钥                   |
| `data.mac_algorithm` | string  | MAC 算法名称：`hmac-sha-1` |
| `data.scope`         | string  | 授权的 scope               |

#### 请求示例

**正确格式（form-urlencoded）：**

```bash
curl -X POST https://accounts.tapapis.cn/oauth2/v1/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=znaefihegkbapi5jho" \
  -d "grant_type=authorization_code" \
  -d "secret_type=hmac-sha-1" \
  -d "code=8aee60afd7d3f616cd20b9bed236bb7d" \
  -d "redirect_uri=https://www.example.com/callback" \
  -d "code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
```

**返回示例：**

```json
{
  "data": {
    "kid": "1/KThGmmzzbOAaK7ENQpHQ...",
    "access_token": "1/KThGmmzzbOAaK7ENQpHQ...",
    "token_type": "mac",
    "mac_key": "jzu9DBWyHMjMoH7ZaPI35T56znCgD6YG",
    "mac_algorithm": "hmac-sha-1",
    "scope": "public_profile"
  },
  "now": 1760442639,
  "success": true
}
```

## 特殊授权流程

### PC Localhost 流程

适用于桌面应用，使用 localhost 作为回调地址。

#### 实现步骤

1. **应用监听本地端口**
   - 监听 `http://localhost:{port}/authorize` 或 `http://127.0.0.1:{port}/authorize`
   - 同时监听自定义 scheme：`open-taptap-{clientId_lowercase}://authorize`

2. **打开授权页面**
   - 使用系统默认浏览器打开授权 URL
   - `redirect_uri` 设置为 `http://localhost:{port}/authorize`
   - 添加参数 `flow=pc_localhost`

3. **接收授权结果**
   - TapTap 授权页会发起两个请求：
     - 自定义 scheme 唤起应用 UI
     - HTTP 请求传递 code 或 error

#### 示例 URL

```
https://accounts.taptap.com/authorize?
  client_id=tIgVThkG9cxrX9uq1w&
  response_type=code&
  redirect_uri=http%3A%2F%2Flocalhost%3A9091%2Fauthorize&
  state=269e94&
  scope=public_profile,user_friends&
  code_challenge_method=S256&
  flow=pc_localhost
```

#### 回调示例

**同意授权时：**

1. `open-taptap-{clientId}://authorize`（唤起应用）
2. `http://127.0.0.1:58416/authorize?code=xxx&state=269e94`

**拒绝授权时：**

1. `open-taptap-{clientId}://authorize`（唤起应用）
2. `http://127.0.0.1:58416/authorize?error=access_denied&state=269e94`

**注意：** Safari 18+ 强制所有请求使用 HTTPS，此方案在 Safari 上不可用。

### Custom URI Scheme 流程（已废弃）

> ⚠️ 根据内部讨论，此方案可能不在 SDK 中出现，仅作参考。

当用户点击 TapTap 登录时：

1. 应用监听 `open-taptap-{clientId}://authorize`
2. 使用系统浏览器打开授权页面，`redirect_uri` 设置为自定义 scheme
3. 用户授权后，TapTap 跳转到中间页，自动或手动唤起应用
4. 应用通过 scheme 接收 `code` 和 `state` 参数

**示例：**

```
open-taptap-S2HQeMV6a0U2af0U0N://authorize?code=xxx&state=abc
```

## Scope 权限范围

| Scope            | 说明                                     |
| ---------------- | ---------------------------------------- |
| `public_profile` | 获取用户公开资料（头像、昵称等）         |
| `basic_info`     | 基本信息（系统会自动授权，跳过确认步骤） |
| `user_friends`   | 好友列表                                 |

多个 scope 使用逗号分隔，例如：`public_profile,user_friends`

## 安全建议

1. **State 参数**
   - 必须使用随机生成的不可预测字符串
   - 回调时验证 state 参数，防止 CSRF 攻击

2. **PKCE 流程**
   - 客户端应用强烈推荐使用 PKCE
   - `code_verifier` 应在本地生成，不可泄露

3. **Redirect URI**
   - 必须在开发者中心预先配置白名单
   - 回调地址必须完全匹配（包括协议、域名、路径）

4. **Client Secret**
   - 仅用于服务端，切勿暴露到客户端代码中
   - 定期轮换密钥

## 常见问题

### Q: 如何在开发测试环境中调试？

**使用沙盒环境 (sandbox)：**

1. **获取沙盒凭证**：在 TapTap 开发者中心创建测试应用，获取沙盒环境的 `client_id`
2. **配置环境**：在配置文件中设置 `env: "sandbox"`
3. **配置回调地址**：在开发者中心配置测试环境的 `redirect_uri` 白名单（如 `http://localhost:8080/api/auth/callback`）

**环境切换：**

只需修改配置中的 `env` 字段，URL 会自动切换：

```json
{
  "auth": {
    "taptap": {
      "clientId": "your_client_id",
      "redirectUri": "http://localhost:8080/api/auth/callback",
      "env": "sandbox" // 或 "production"
    }
  }
}
```

URLs 映射：

- `sandbox` → `https://accounts.xdrnd.cn/*`
- `production` → `https://accounts.taptap.cn/*`

### Q: PKCE 和 Server Secret 如何选择？

- **客户端应用**（Web、移动应用、桌面应用）：使用 PKCE，无需保存 `client_secret`
- **服务端应用**：使用 Server Secret，在服务器端安全存储 `client_secret`

### Q: 如何生成 code_verifier 和 code_challenge？

```javascript
// 生成 code_verifier（43-128 位随机字符串）
function generateCodeVerifier() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

// 生成 code_challenge
async function generateCodeChallenge(verifier) {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return base64UrlEncode(new Uint8Array(hash));
}

function base64UrlEncode(buffer) {
  return btoa(String.fromCharCode(...buffer))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=/g, "");
}
```

### Q: 授权后如何使用 Access Token？

获取到 `access_token` 和 `mac_key` 后，需要按照 MAC Token 规范构造 HTTP 请求头。具体使用方法请参考 [MAC Access Authentication](https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac) 规范。

### Q: 为什么总是提示 "GrantType 必填"？

这是最常见的错误。原因是使用了错误的 Content-Type：

❌ **错误用法（JSON）：**

```bash
curl -X POST https://oauth.api.xdrnd.cn/oauth2/v1/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "authorization_code", ...}'
```

✅ **正确用法（form-urlencoded）：**

```bash
curl -X POST https://oauth.api.xdrnd.cn/oauth2/v1/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&..."
```

**关键点：**

- 必须使用 `application/x-www-form-urlencoded` 格式
- 字段名使用 snake_case（`grant_type`，不是 `GrantType`）
- 响应数据在 `data` 字段中，需要解包

### Q: 如何解析 TapTap API 的响应？

TapTap API 统一使用以下响应格式：

```typescript
interface TapTapResponse<T> {
  success: boolean;
  now: number; // 服务器时间戳
  data?: T; // 成功时返回
  error?: string; // 失败时返回错误码
  msg?: string; // 失败时返回错误消息
}
```

**示例代码：**

```typescript
const response = await fetch(tokenUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ grant_type: 'authorization_code', ... }),
});

const result = await response.json();

if (!result.success || !result.data) {
  throw new Error(result.msg || 'Unknown error');
}

// 使用 result.data 中的实际数据
const { access_token, mac_key } = result.data;
```

## 参考资料

- [OAuth 2.0 Authorization Code Grant](https://tools.ietf.org/html/rfc6749#section-4.1)
- [PKCE Extension](https://tools.ietf.org/html/rfc7636)
- [云游戏授权登录协议](https://云游戏授权登录协议)

## 更新日志

- 最新版本支持 PKCE 扩展
- 新增 `pc_localhost` 流程支持桌面应用
- 废弃 `custom_uri_scheme` 流程
