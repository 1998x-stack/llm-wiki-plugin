---
summary: "Resource UUID encoding format design and generation mechanism"
related_paths:
  - tools/generators/**
last_updated: "2025-12-11"
---

# 资源 UUID 设计

本文档描述 UrhoX 资源 UUID 的编码格式设计和生成机制。

---

## 📋 目录

- [设计目标](#设计目标)
- [UUID 编码格式](#uuid-编码格式)
  - [文件命名格式](#文件命名格式)
- [UUID 生成时机](#uuid-生成时机)
- [UUID 管理方案](#uuid-管理方案)

---

## 设计目标

| 目标 | 说明 |
|------|------|
| **UGC 分布式生成** | 任何作者、任何时间、在本地离线生成，无需中心服务器 |
| **全球唯一** | 不同作者、不同游戏生成的 UUID 不冲突 |
| **扁平化存储** | 所有资源在服务器上同一层级，纯靠 UUID 区分 |
| **表面隐藏信息** | 看起来完全随机，无法直接读出作者、时间等敏感信息 |
| **内部可追溯** | 服务端可解码出原始信息（作者归属、创建时间等） |
| **版本可升级** | 预留版本号字段，支持未来编码结构升级 |

---

## UUID 编码格式

### 编码结构（18 字节 = 24 Base64 字符，当前实现 Version = 1）

```
┌─────────┬────────────┬──────────┬──────────┬────────────┬─────────┐
│  V高    │   Random   │  Author  │   Game   │ Timestamp  │   V低   │
│ 3 bits  │ 26 bits    │ 4 bytes  │ 4 bytes  │ 6 bytes    │ 3 bits  │
├─────────┼────────────┼──────────┴──────────┴────────────┼─────────┤
│  明文 (29 bits)      │     动态混淆区 (14 bytes)        │  明文   │
└─────────┴────────────┴──────────────────────────────────┴─────────┘
                                     ↓
             Version(6 bits) + Random(26 bits) → SHA256 动态密钥
                                     ↓
                      对 Author + Game + Timestamp 进行 XOR 混淆
                                     ↓
                            URL-safe Base64
                                     ↓
                        Wjyfex0KT2watjVfL4xKfg0c
                        （表面看完全随机，共 24 字符）
```

---

### 字段说明

| 字段 | 位数/大小 | 说明 |
|------|-----------|------|
| **Version** | 6 bits（拆分为 V高3 + V低3） | 编码版本号（0-63），支持未来升级编码结构，**明文不混淆** |
| **Random** | 26 bits | 随机数（≈6700 万种），作为动态混淆种子，**明文不混淆** |
| **Author** | 4 bytes | 作者 ID 的 SHA256 哈希前 4 字节（≈42 亿种） |
| **Game** | 4 bytes | 游戏 ID 的 SHA256 哈希前 4 字节（≈42 亿种） |
| **Timestamp** | 6 bytes | 毫秒级时间戳（可用约 8900 年） |

**设计说明**：
- Version 保持明文，便于解码时确定版本和混淆方式
- Random 与 Version 共用 4 字节，既节省空间又作为动态混淆种子
- 去掉 Type 字段：文件扩展名已提供类型信息
- 去掉 Checksum 字段：资源不存在即可判定无效

---

### 动态混淆机制

**为什么需要动态混淆？**

固定 XOR 密钥的问题：相同作者 + 相同游戏的资源，混淆后前几字节完全相同，一眼就能看出关联性。

**动态混淆方案**：用 Version(6 bits) + Random(26 bits) 生成动态密钥，确保每个 UUID 的混淆结果完全不同。

```python
import hashlib

# 固定种子（用于生成动态密钥）
MIX_SEED = b'\x5a\x3c\x9f\x1e\x7b\x2d\x8a\x4f\x6c\x1a\x9e\x3b\x5d\x2f'

def mix(version: int, random_bits: int, payload: bytes) -> bytes:
    """
    动态混淆
    
    Args:
        version: 完整版本号（6 bits）
        random_bits: 随机数（26 bits）
        payload: Author + Game + Timestamp（14 字节），需要混淆
    
    Returns:
        混淆后的完整数据（18 字节）
    """
    # 用 Version + Random 生成动态密钥
    seed_data = bytes([version & 0x3F]) + random_bits.to_bytes(4, 'big')
    dynamic_key = hashlib.sha256(MIX_SEED + seed_data).digest()
    
    # 对 payload 进行 XOR 混淆
    mixed_payload = bytes(b ^ dynamic_key[i % len(dynamic_key)] for i, b in enumerate(payload))
    
    return mixed_payload

def unmix(version: int, random_bits: int, mixed_payload: bytes) -> bytes:
    """
    反混淆
    
    Args:
        version: 完整版本号（6 bits）
        random_bits: 随机数（26 bits）
        mixed_payload: 混淆后的 payload（14 字节）
    
    Returns:
        原始 payload（14 字节）
    """
    # 用相同方式生成动态密钥
    seed_data = bytes([version & 0x3F]) + random_bits.to_bytes(4, 'big')
    dynamic_key = hashlib.sha256(MIX_SEED + seed_data).digest()
    
    # XOR 反混淆
    return bytes(b ^ dynamic_key[i % len(dynamic_key)] for i, b in enumerate(mixed_payload))
```

**效果**：
- 即使同一作者、同一游戏的多个资源
- 因为 Random 不同 → 动态密钥不同 → 混淆结果完全不同
- 无法从 UUID 表面看出任何关联性

---

### 生成流程

```
输入：author_id, game_id
                    ↓
    1. version = 当前版本号（6 bits，拆为 V高3 + V低3）
    2. random = 随机数（26 bits）
    3. version_random = (V高 << 29) | (random << 3) | V低（组合为 4 字节，明文）
                    ↓
    4. author_hash = SHA256(author_id)[:4]
    5. game_hash = SHA256(game_id)[:4]
    6. timestamp = 当前毫秒时间戳（6 字节）
                    ↓
    7. payload = author_hash + game_hash + timestamp（14 字节）
    8. dynamic_key = SHA256(MIX_SEED + [version(1B) | random(4B)])
    9. mixed_payload = payload XOR dynamic_key（重复利用 key）
                    ↓
    10. full_data = version_random(4B 明文) + mixed_payload(14B) = 18 字节
    11. result = base64_urlsafe(full_data)
                    ↓
输出：URL-safe Base64 字符串（24 字符）
```

---

### 解码流程

```
输入：uuid_str（24 字符 Base64）
                    ↓
    1. data = base64_urlsafe_decode(uuid_str)（18 字节）
                    ↓
    2. version_random = data[:4]（明文）
    3. V高 = version_random[0] >> 5
    4. random = ((version_random[0] & 0x1F) << 21) | (version_random[1] << 13) | (version_random[2] << 5) | (version_random[3] >> 3)
    5. V低 = version_random[3] & 0x07
    6. version = (V高 << 3) | V低   （6 bits）
                    ↓
    7. dynamic_key = SHA256(MIX_SEED + [version(1B) | random(4B)])
    8. payload = data[4:] XOR dynamic_key（反混淆）
                    ↓
    9. 按字段偏移提取：
       - author_hash = payload[0:4].hex()
       - game_hash = payload[4:8].hex()
       - timestamp_ms = int.from_bytes(payload[8:14], 'big')
                    ↓
输出：{version, random, author_hash, game_hash, timestamp}
```

---

### 版本兼容策略

- 当前解码器 `uuid_decoder.py` 仅实现 Version = 1。
- 未来版本将以独立文件形式提供（例如 `uuid_decoder_v02.py`），旧版本工具保持可用。
- 生成器中的 `VERSION` 常量决定编码版本，解码器按版本拆分。

---

### 服务端验证能力

```python
# 验证 UUID 是否属于指定作者
def match_author(uuid_str: str, author_id: str) -> bool:
    info = decode(uuid_str)
    expected_hash = hashlib.sha256(author_id.encode()).hexdigest()[:8]
    return info["author_hash"] == expected_hash

# 验证 UUID 是否属于指定游戏
def match_game(uuid_str: str, game_id: str) -> bool:
    info = decode(uuid_str)
    expected_hash = hashlib.sha256(game_id.encode()).hexdigest()[:8]
    return info["game_hash"] == expected_hash

# 提取创建时间
def get_create_time(uuid_str: str) -> datetime:
    info = decode(uuid_str)
    return datetime.fromtimestamp(info["timestamp_ms"] / 1000)
```

---

### 冲突概率分析

| 条件 | 冲突概率 |
|------|----------|
| 同一作者 + 同一游戏 + 同一毫秒 | 1 / 2^26 ≈ 1 / 6700万 |
| 同一作者 + 不同游戏 | 几乎不可能（game_hash 不同） |
| 不同作者 | 几乎不可能（author_hash 不同） |
| 全局任意 | 需要 author + game + time + random 全部碰撞 |

---

### 输出格式

采用 **URL-safe Base64** 编码（去除填充符 `=`）：

| 字节数 | Base64 长度 | 说明 |
|--------|-------------|------|
| 18 字节 | **24 字符** | 最终格式 |

**编码规则**：
- 使用 URL-safe Base64：`A-Z`, `a-z`, `0-9`, `-`, `_`（替代标准的 `+`, `/`）
- 去除尾部填充符 `=`
- 文件名安全，URL 安全

```python
import base64

def encode_uuid(data: bytes) -> str:
    """编码为 URL-safe Base64（无填充）"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def decode_uuid(uuid_str: str) -> bytes:
    """解码 URL-safe Base64"""
    # 补齐填充
    padding = 4 - (len(uuid_str) % 4)
    if padding != 4:
        uuid_str += '=' * padding
    return base64.urlsafe_b64decode(uuid_str)
```

---

### 文件命名格式

**必须使用 `{uuid}.{ext}` 格式**（UUID + 扩展名）：

```
Wjyfex0KT2watjVfL4xKfg0c.png    # 贴图
Xk2mPqR9sT4vWxYz3bABcd.lua      # 脚本
7fXk2mPqR9sT4vWxYz3bAB.ogg      # 音频
```

#### 为什么必须保留扩展名？

**HTTP 静态服务器依赖扩展名设置 Content-Type**：

| 服务器 | 无扩展名时的行为 |
|--------|------------------|
| Python http.server | 返回 `application/octet-stream` |
| Express static | 返回 `application/octet-stream` |
| Nginx | 返回 `application/octet-stream` |
| 大多数 CDN | 返回 `application/octet-stream` |

**错误的 Content-Type 会导致**：
- 图片无法显示（浏览器当作下载）
- 音频无法播放
- JSON 无法解析
- 脚本可能被阻止执行

**保留扩展名的优势**：
- ✅ 任何静态服务器都能正确工作
- ✅ `python -m http.server` 直接可用
- ✅ Express `static` 中间件直接可用
- ✅ CDN 自动设置正确的 Content-Type
- ✅ 调试时一眼看出资源类型
- ✅ 无需额外配置

---

## UUID 生成时机

### 推荐方案：资源导入时生成 + 持久化

```
┌─────────────────────────────────────────────────────────────────────┐
│                    UUID 生成时机                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐                                                   │
│   │ 新资源添加   │ ───────────────────────────────────┐              │
│   └─────────────┘                                    ▼              │
│         │                                    ┌─────────────┐        │
│         │                                    │ 生成新 UUID  │        │
│         │                                    └─────────────┘        │
│         ▼                                           │               │
│   ┌─────────────┐                                   │               │
│   │ 检查 meta   │                                   │               │
│   └─────────────┘                                   │               │
│         │                                           │               │
│    已存在？                                          │               │
│    ├─ 是 ──▶ 保留现有 UUID ◀──────────────────────────┘               │
│    │                                                                │
│    └─ 否 ──▶ 检查内容哈希 ──▶ 匹配已删除资源？                         │
│                                  ├─ 是 ──▶ 恢复旧 UUID              │
│                                  └─ 否 ──▶ 生成新 UUID              │
│                                                                     │
│   ┌─────────────┐                                                   │
│   │ 资源重命名   │ ──────────────▶ 保留现有 UUID                      │
│   └─────────────┘                                                   │
│                                                                     │
│   ┌─────────────┐                                                   │
│   │ 资源修改    │ ──────────────▶ 保留现有 UUID + 更新哈希            │
│   └─────────────┘                                                   │
│                                                                     │
│   ┌─────────────┐                                                   │
│   │ 资源删除    │ ──────────────▶ 标记为 deprecated（不立即删除）     │
│   └─────────────┘                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 生成时机对比

| 时机 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **资源导入时** | 稳定、可预测；支持编辑器内引用 | 需要 meta 文件管理 | UrhoX 推荐 |
| **首次构建时** | 无需编辑器；实现简单 | 多次构建可能不一致；团队协作困难 | 简单项目 |
| **手动分配** | 完全可控；可读性好 | 工作量大；容易出错 | 小型项目 |
| **基于内容哈希** | 自动去重；天然缓存友好 | 内容变化 UUID 就变；无法稳定引用 | CDN 资源 |

---

## UUID 管理方案

### 方案：meta 文件 + 内容哈希辅助

```
┌─────────────────────────────────────────────────────────────────────┐
│                    UrhoX UUID 管理方案                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐                                                │
│  │  资源文件        │                                                │
│  │  player.png     │                                                │
│  └─────────────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐     ┌─────────────────┐                       │
│  │  meta 文件       │ ◀── │  gen_uuid 工具   │                       │
│  │  player.png.meta│     │                 │                       │
│  │                 │     │  扫描资源目录    │                       │
│  │  uuid: xxx      │     │  检测变更        │                       │
│  │  group: ui      │     │  生成/更新 UUID  │                       │
│  └─────────────────┘     └─────────────────┘                       │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │  build_project  │                                                │
│  │  构建工具        │                                                │
│  └─────────────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │  构建产物        │                                                │
│  │  manifest.json  │                                                │
│  │  {uuid}.{ext}   │                                                │
│  └─────────────────┘                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 场景示例

#### 场景1：添加新资源

```
开发者操作：
1. 将 new_texture.png 复制到 Assets/Textures/

UUID 生成流程：
1. 运行 `python gen_uuid.py --project .`
2. 工具扫描到新文件 Assets/Textures/new_texture.png
3. 检查是否有 .meta 文件，没有
4. 生成新 UUID
5. 创建 new_texture.png.meta 文件

结果：
new_texture.png.meta:
{
  "uuid": "Wjyfex0KT2watjVfL4xKfg0c",
  "created_at": "2025-12-07T10:00:00Z"
}

构建后文件名：Wjyfex0KT2watjVfL4xKfg0c.png
```

#### 场景2：重命名资源

```
开发者操作：
1. 将 player.png 重命名为 hero.png
2. 同时重命名 player.png.meta 为 hero.png.meta

结果：
UUID 保持不变（存储在 meta 文件中）
```

#### 场景3：修改资源内容

```
开发者操作：
1. 修改 player.png 的内容

结果：
UUID 保持不变（meta 文件不变）
构建时会生成新的内容哈希用于缓存控制
```

---

## 开发调试策略

### 策略选择：必须构建才能调试（策略A）

考虑到简单性和一致性，UrhoX 采用**构建后调试**的策略：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        开发调试流程                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  开发者修改资源 ──▶ 运行增量构建 ──▶ 启动调试                             │
│       │                │                │                               │
│       │                ▼                │                               │
│       │        Build/{version}/         │                               │
│       │        ├── manifest.json        │   (UUID ↔ path 映射)          │
│       │        └── assets/{uuid}.{ext}  │                               │
│       │                │                │                               │
│       │                ▼                │                               │
│       └──────▶ 本地服务器挂载 ◀─────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 策略优势

| 优势 | 说明 |
|------|------|
| **环境一致** | 开发和生产使用完全相同的资源加载逻辑 |
| **无额外维护** | 不需要开发专用的临时映射缓存 |
| **问题早发现** | 构建问题在开发阶段就能暴露 |
| **增量构建** | 只处理变更文件，速度可接受 |

### 开发工作流

```bash
# 1. 首次构建（完整）
python tools/build_project.py --project ./MyGame --version dev

# 2. 修改资源后（增量）
python tools/build_project.py --project ./MyGame --version dev --incremental

# 3. 启动本地调试服务器
python tools/dev_server.py --project ./MyGame --version dev
```

### 增量构建优化

为提升开发体验，增量构建应支持：

1. **文件监听模式**：`--watch` 参数，监听 Assets 变更自动重新构建
2. **只处理变更**：比对 uuid-map.json 中的 hash，跳过未修改文件
3. **秒级构建**：单文件变更应在 1-2 秒内完成

```bash
# 监听模式（推荐开发时使用）
python tools/build_project.py --project ./MyGame --version dev --watch
```

### 关键决策记录

| 决策点 | 决定 | 原因 |
|--------|------|------|
| 引用格式 | `{uuid}.{ext}` 必须带后缀 | CDN/MIME/同名meta友好 |
| **UUID 引用协议** | 统一使用 `uuid://` 协议 | 便于资源引用收集和解析 |
| 运行时前缀 | 不支持 `official://uuid` 等前缀语法 | UUID 全球唯一，manifest 已扁平化 source |
| 开发调试 | 必须构建后调试（策略A） | 简单一致，增量构建可优化体验 |
| 临时映射 | uuid-map.json 仅构建工具使用 | 运行时只读 manifest.json |

### UUID 引用规范

配置文件和序列化数据中引用 UUID 资源时，必须使用 `uuid://` 协议前缀：

| 格式 | 示例 | 说明 |
|------|------|------|
| `uuid://` | `uuid://C3y7ubiP8nQLJmOepTuuvfqU` | ✅ 正确 - 任何 UUID 资源 |
| 裸 UUID | `C3y7ubiP8nQLJmOepTuuvfqU` | ❌ 不再支持 |
| `official://uuid` | `official://C3y7ubiP8nQL...` | ❌ 不再支持 |
| `pub-xxx://uuid` | `pub-john://C3y7ubiP8nQL...` | ❌ 不再支持 |

> **设计原因**：
> - 统一的 `uuid://` 前缀便于资源引用收集工具识别
> - 与 `official://path`、`pub-xxx://path` 虚拟路径引用区分
> - UUID 全球唯一，无需通过协议区分来源

---

## 相关文档

- [INDEX.md](./INDEX.md) - 完整构建流程
- [meta-application-design.md](./meta-application-design.md) - Meta 应用设计

---

*最后更新: 2025-12-11*
