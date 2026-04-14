---
summary: "Plan for UrhoX direct score server integration, bypassing Host, using Redis pub/sub"
status: in_progress
last_updated: "2026-04-02"
read_when:
  - "modifying score server communication"
  - "working on Redis pub/sub integration"
  - "changing Host-UrhoX score architecture"
---

# Host 积分通信方式 & UrhoX 直连积分服接入

## 架构说明

- **Host 方式**：Host 通过 Redis 选一台积分服实例，publish 请求到该实例 channel，积分服处理完后 publish 到 Host 的 return_channel。
- **UrhoX 方式**：**UrhoX 直连积分服，不走 Host**。UrhoX 自己发消息给积分服，并自己订阅 return_channel 接收、处理积分服的回复。

---

## 一、原 Host 积分通信流程概览（供参考）

### 1. 积分服发现与 Channel 选择（GameSession::generateScoreChannelName）

- **数据源**：Redis Hash `discover::hmap::for_entrance`（与 Entrance 共用的服务发现）。
- **逻辑**：
  - 遍历 Hash，解析 value 为 JSON，筛选 `meta.type_name == "score"` 的实例；
  - 排除超过 20s 未更新的实例（`last_update_timestamp`）；
  - 若本次是“重选”（例如原积分服挂了），排除 `old_channel`；
  - 用 **session_id** 做 MurmurHash 对实例数取模，得到稳定映射：同一 session 总选同一台积分服；
  - 选中的实例 key（如 `inner_ip:port:pod_name`）写入 **m_score_channel**，即**发请求时用的“积分服 channel”**。

```cpp
// 核心：m_score_channel = 某台 ScoreArchive 实例在 discovery 中的 unique_key
// ScoreArchive 侧订阅的 channel 名 = 自身 "{inner_ip}:{port}:{pod_name}"
```

### 2. 发请求（ScoreArchiveAgent::sendMessage）

- 构造 `CEProto::ScoreArchive::Msg`：
  - `return_channel = "channel_s_to_host:" + local_ip + ":" + local_port`（**本 Host 进程收回复的 Redis channel**）；
  - 其他：request_id、message_type、message_body、src_map_name、target_map_name、game_session_id 等。
- **发送方式**：不经过 list，而是 **publish 到选中的那台积分服实例的 channel**：
  - `channel_name = gameSession_->getScoreChannelName()`（即 `m_score_channel`）；
  - `MessagePubSub::publishRowMessage(channel_name, serializeMsg)`。

### 3. 积分服收请求（ScoreArchive 侧）

- 除从 list `s_msg_channel` blpop 外，还 **subscribe 自身 channel** `{inner_ip}:{port}:{pod_name}`；
- 收到 publish 的 Msg 后，同样构造 `MessageContext(msg, nullptr, nullptr)`，走统一 ProcessMessage；
- 回复时因无 `m_channel`，走 Redis：`publish(return_channel, replyMsg)`。

### 4. Host 收回复

- **订阅**：`PlatformProcessor` 在初始化时注册  
  `"channel_s_to_host:" + local_ip + ":" + local_port` → `PlatformProcessor::processScoreArchiveMessage`。
- **路由**：解析出 `CEProto::ScoreArchive::Msg`，交给 `GameSessionManager::processScoreArchiveMessage`，用 **request_id** 查 `game_session_id`，再 `notifyGameMsgScoreArchive` 投递到对应 GameSession 的内部队列，由 `ScoreArchiveAgent::processMessage` 按 message_type 分发。

### 5. 失败重试（发请求时）

- `publishRowMessage` 的回调里若 publish 失败（如积分服挂了），会：
  - 调用 `game_session->generateScoreChannelName()` 重新选一台（会排除当前 channel）；
  - 用新的 `getScoreChannelName()` 再次 `publishRowMessage` 重发同一条 msg。

---

## 二、关键常量与约定

| 项目 | 值/约定 |
|------|---------|
| 积分服 list（多实例竞争消费） | `s_msg_channel`（RedisCustomKey::score_archive_msg） |
| 积分服单实例收请求 channel | 该实例在 discovery 中的 key：`{inner_ip}:{port}:{pod_name}` |
| Host 收回复 channel | `channel_s_to_host:{host_ip}:{host_port}` |
| UrhoX 收回复 channel（自定） | `channel_s_to_urhox:{identity}`（identity 通常为 session_id），需与请求中 `return_channel` 一致 |
| 服务发现 Hash | `discover::hmap::for_entrance`，value 含 `meta.type_name`、`last_update_timestamp` 等 |

---

## 三、UrhoX 直连积分服（不走 Host）

**UrhoX 不经过 Host**：由 UrhoX 直接向积分服发消息，积分服处理完后把回复 publish 到 UrhoX 提供的 `return_channel`，UrhoX 订阅该 channel 并自行处理所有回复。

**选定方案：方式 A**（与 Host 原机制一致，publish 到积分服实例 channel，便于复用 Host 侧逻辑与约定。）

### 流程概览

```
UrhoX  --[发请求]-->  积分服（Redis publish / lpush）
UrhoX  <--[收回复]--  积分服（Redis publish 到 return_channel）
```

- 请求：UrhoX 构造 `CEProto::ScoreArchive::Msg`，设好 `return_channel`，通过 Redis 发给积分服。
- 回复：积分服处理完后对 `return_channel` 做 **publish(replyMsg)**，UrhoX 在 **subscribe(return_channel)** 的回调里解析并处理回复（按 request_id 分发）。

### 方式 A：publish 到积分服实例 channel（与 Host 同机制，**已选用**）

1. **选积分服 channel（启动时一次，全程不切换）**
   - 读 Redis `discover::hmap::for_entrance`，筛 `type_name == "score"`、按存活时间过滤，用 UrhoX 的 identity（如 session_id）做 hash 选一台，得到 `score_channel`（该实例的 `{inner_ip}:{port}:{pod_name}`）。
   - **UrhoX 实现**：在 `ScoreArchiveChannel::Start()` 时选定并缓存，后续所有发送均使用该 channel，**中途不切换**，以保证发往同一积分服实例的消息先后顺序。可参考 Host 的 `generateScoreChannelName()` 做 discovery 逻辑。

2. **发请求**
   - 构造 `CEProto::ScoreArchive::Msg`（COMMIT、MULTI_SCORE_INIT、查询等），填 `request_id`、`message_type`、`message_body`、`src_map_name`/`target_map_name` 等；
   - **必须** `set_return_channel(urhox_reply_channel)`，例如 `"channel_s_to_urhox:" + identity`（identity 可为 session_id 字符串）；
   - 发送：**publish(score_channel, msg)**，其中 `score_channel` 为启动时选定的固定 channel。

3. **收回复并处理**
   - UrhoX 进程启动时 **subscribe(urhox_reply_channel)**；
   - 回调里：解析为 `CEProto::ScoreArchive::Msg`，根据 **request_id** 找到对应请求的回调，再按 **message_type** 处理（COMMON_RESPONSE、SCORE_INIT_RES、MULTI_SCORE_INIT_RES 等）。

4. **request_id**
   - 格式：**request_id = (sessionId << 32) | 自增序列**，保证全局唯一且同一 session 内严格自增。UrhoX 侧维护 request_id → 回调的映射，收到回复时按 request_id 派发。

### 方式 B：走 list，不选具体实例

- 不查 discovery，直接 **lpush("s_msg_channel", msg.SerializeAsString())**；
- 同样必须设 **return_channel** 为 UrhoX 的回复 channel，并 **subscribe(return_channel)**，用 request_id 关联请求与回复；
- 积分服任意实例 blpop 到后处理并 **publish(return_channel, reply)**。

---

## 四、UrhoX 侧实现要点（方式 A，与 Host 一致）

按方式 A 实现时，UrhoX 侧需做以下内容，与第一章 Host 流程一一对应。实现集中在 **ScoreArchiveChannel**（`engine/Source/Tools/UrhoXServer/ScoreArchiveChannel.h/.cpp`）。

| 步骤 | 说明（方式 A） |
|------|----------------|
| 1. 选积分服 channel | 从 Redis `discover::hmap::for_entrance` 筛 `meta.type_name == "score"`、按 `last_update_timestamp` 排除超过 20s 未更新实例，用 UrhoX 的 identity（如 session_id）做**确定性 hash** 对实例数取模，得到 `score_channel`（即该实例 key：`{inner_ip}:{port}:{pod_name}`）。Host 用 MurmurHash，UrhoX 用 `String::ToHash`，均保证同一 identity 稳定映射且分布均匀。**在 `ScoreArchiveChannel::Start()` 时选一次并缓存，全程不切换**，以保证消息先后顺序。 |
| 2. 设 return_channel | 请求 `CEProto::ScoreArchive::Msg` 中 `set_return_channel(urhox_reply_channel)`，例如 `"channel_s_to_urhox:" + identity`（identity 为 session_id 等），与 Host 的 `channel_s_to_host` 命名方式一致。 |
| 3. 发请求 | **publish(score_channel, msg)**，其中 `score_channel` 为启动时选定的固定 channel，与 Host 的 `publishRowMessage(score_channel, ...)` 一致。 |
| 4. 收回复并处理 | 进程启动时 **subscribe(urhox_reply_channel)**，在 Redis MessageCallback 中解析为 `CEProto::ScoreArchive::Msg`，按 **request_id** 查回调，再按 **message_type** 处理（COMMON_RESPONSE、SCORE_INIT_RES、MULTI_SCORE_INIT_RES 等）。 |
| 5. request_id 与回调 | **request_id = (sessionId << 32) | 自增序列**，由 `ScoreArchiveChannel::NextRequestId()` 生成；维护 request_id → 回调的映射，收到回复时派发。 |
| 6. 重试/换实例 | UrhoX 当前实现为**不中途换实例**，以保证发往同一积分服的消息顺序；若启动时未选到实例，SendMessage 会失败直至下次 Start。 |

按上述方式即可实现 **UrhoX 直连积分服、不走 Host，与 Host 机制保持一致**。
