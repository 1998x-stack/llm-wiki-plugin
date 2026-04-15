---
summary: "从全项目目录层级说明 UrhoX 二进制代码的依赖结构，以及各目录在 Runtime 和 Server 中的职责"
last_updated: "2026-04-04"
---

# UrhoX 二进制代码目录结构

本文档关注的是整个 UrhoX 项目里“会进入二进制”的源码目录结构，而不是单个可执行文件里的具体文件实现。

重点回答两个问题：

- 整个 UrhoX 项目的二进制代码目录是怎么分层的
- 每个目录在最终 `UrhoXRuntime` / `UrhoXServer` 中承担什么职责

本文不展开：

- 详细 CMake 选项和构建命令
- 单个 `.cpp/.h` 文件级别说明
- Samples、Tests、Docs 这类非主产品二进制目录

## 1. 先看整体依赖目录关系

从目录层级看，UrhoX 主二进制代码大致是下面这条链路：

```text
engine/Source/ThirdParty      \
3rd/                           > 底层第三方能力
                               
engine/Source/Urho3D           > 引擎核心库

engine/Source/Common           > 引擎侧平台/SDK补充
game/src/Common                > 项目级公共层
game/src/Engine                > 项目级引擎扩展层
game/src/Game                  > 项目级业务/运行时逻辑层

engine/Source/Tools/UrhoXRuntime
engine/Source/Tools/UrhoXServer > 最终二进制入口
```

如果只看主产品二进制，可以把目录角色理解成 6 层：

| 层级 | 主要目录 | 角色 |
|------|----------|------|
| 第三方依赖层 | `engine/Source/ThirdParty`、`3rd` | 提供渲染、脚本、网络、压缩、HTTP、Redis、视频、平台 SDK 等底层库 |
| 引擎核心层 | `engine/Source/Urho3D` | UrhoX 的基础引擎能力 |
| 引擎公共补充层 | `engine/Source/Common` | 引擎侧 Android / SDK 等补充 |
| 项目公共层 | `game/src/Common` | Proto、压缩、公用头、iOS 公共层 |
| 项目扩展层 | `game/src/Engine`、`game/src/Game` | 项目自己的引擎扩展与运行时功能模块 |
| 最终入口层 | `engine/Source/Tools/UrhoXRuntime`、`engine/Source/Tools/UrhoXServer` | 客户端和服务端可执行/运行时入口 |

## 2. 第三方依赖层

UrhoX 有两套第三方目录：

- `engine/Source/ThirdParty`
- `3rd`

它们都属于二进制代码的一部分，但定位不同。

### 2.1 `engine/Source/ThirdParty`

这一层更偏“引擎内建依赖”。`Urho3D` 核心库直接围绕这批目录组织。

### 2.1.1 图形与渲染相关

| 目录 | 用途 |
|------|------|
| `bgfx-all` | 现代渲染后端和 shader 工具链，是 UrhoX 当前渲染体系的重要基础 |
| `GLEW` | OpenGL 扩展加载 |
| `MojoShader` | 旧图形后端相关 shader 转换支持 |
| `renderdoc` | RenderDoc 集成接口 |
| `FreeType` | 字体栅格化 |
| `harfbuzz` | 文本 shaping，复杂字体排版 |
| `STB` | 图片/文件格式的轻量支持 |
| `WebP` | WebP 图像格式支持 |
| `libchardet` | 字符编码检测 |
| `minimp3` | MP3 解码支持 |

### 2.1.2 脚本与绑定相关

| 目录 | 用途 |
|------|------|
| `Lua` | Lua 运行时 |
| `LuaJIT` | LuaJIT 运行时 |
| `toluapp` | Lua 绑定代码生成和运行时桥接 |
| `AngelScript` | AngelScript 脚本支持 |
| `rapidjson` | JSON 解析支持，也被很多上层模块复用 |
| `PugiXml` | XML 解析支持 |
| `Mustache` | 模板渲染能力 |

### 2.1.3 网络、数据库与服务端相关

| 目录 | 用途 |
|------|------|
| `Civetweb` | HTTP/Web 服务器支持 |
| `SLikeNet` | 原生 UDP 网络支持 |
| `SQLite` | SQLite 数据库支持 |
| `nanodbc` | ODBC 数据库支持 |

### 2.1.4 物理、导航和 2D/动画相关

| 目录 | 用途 |
|------|------|
| `Bullet` | 3D 物理 |
| `ik` | 逆运动学 |
| `Recast` | 导航网格生成 |
| `Detour` | 路径查询 |
| `DetourCrowd` | 群体导航 |
| `DetourTileCache` | 导航瓦片缓存 |
| `Box2D` | 2D 物理 |
| `spine` | Spine 动画支持 |
| `StanHull` | 几何/凸包相关工具支持 |

### 2.1.5 平台与其他基础库

| 目录 | 用途 |
|------|------|
| `SDL` | 窗口、输入、平台层封装 |
| `LZ4` | 压缩 |
| `LibCpuId` | CPU 能力检测 |
| `boost` | 部分脚本/平台组合下的补充依赖 |
| `msgpack` | 消息序列化支持 |
| `Assimp` | 模型导入能力，更多被工具链使用 |

### 2.2 `3rd`

这一层更偏“项目侧依赖”，很多库不是 Urho3D 原始核心的一部分，而是 UrhoX 项目功能额外接入的。

### 2.2.1 压缩、资源和打包相关

| 目录 | 用途 |
|------|------|
| `zlib` | 通用压缩能力 |
| `7z` | 资源包、整包压缩解压 |
| `zstd` | 高性能压缩 |
| `astc-encoder` | ASTC 纹理压缩 |
| `bc7enc_rdo` | BC7 纹理压缩 |

### 2.2.2 网络与异步运行时

| 目录 | 用途 |
|------|------|
| `libuv` | 事件循环和异步 IO |
| `curl` | HTTP 客户端 |
| `libhv` | HTTP / WebSocket 相关能力 |
| `hiredis` | Redis Pub/Sub，主要服务端用 |
| `luasocket` | Windows 下 Lua socket 支持 |

### 2.2.3 平台、内存和崩溃相关

| 目录 | 用途 |
|------|------|
| `mimalloc` | Windows 下内存分配器 |
| `ndcrash` | Android 崩溃捕获 |
| `ObjectCBridge` | iOS 原生桥接 |
| `openssl-prebuilt` | 各平台预编译 OpenSSL |

### 2.2.4 媒体、布局和项目扩展

| 目录 | 用途 |
|------|------|
| `ffmpeg` | 原生平台视频播放 |
| `libyuv` | Android 视频像素格式转换 |
| `yoga` | UI 布局系统 |
| `qrcode` | 二维码相关能力 |
| `lmprof` | Lua profiling |
| `lua54` / `lua-protobuf` | 项目侧 Lua 5.4 和 protobuf 绑定支持 |

### 2.3 这两层的关系

- `engine/Source/ThirdParty` 偏引擎内建
- `3rd` 偏项目扩展和平台/业务补充
- 两者共同构成了 `Urho3D` 以及上层 `game/src` 模块的二进制基础

## 3. 引擎核心层：`engine/Source/Urho3D`

这是 UrhoX 主二进制最核心的一层。可以把它理解成“引擎公共库本体”。

### 3.1 基础设施目录

| 目录 | 用途 |
|------|------|
| `Common` | 基础公共定义和跨模块共享头 |
| `Container` | 容器、字符串、集合等基础数据结构 |
| `Core` | 对象系统、事件系统、上下文、子系统注册、主线程基础设施 |
| `Math` | 向量、矩阵、几何计算 |
| `Memory` | 内存管理与内存调试辅助 |
| `Atomic` | 原子操作和线程安全基础类型 |
| `TLS` | 线程本地存储封装 |
| `TypeTraits` | 模板类型萃取和编译期工具 |

### 3.2 运行时主子系统目录

| 目录 | 用途 |
|------|------|
| `IO` | 文件系统、日志、路径、流读写 |
| `Resource` | 资源缓存、资源加载、资源路由 |
| `Scene` | 场景树、节点、组件体系 |
| `Engine` | 应用启动、主循环、运行时宿主框架 |
| `Input` | 输入系统 |
| `Graphics` | 渲染核心、材质、模型、shader、视频等图形能力 |
| `Audio` | 音频系统 |
| `UI` | 传统 UI 系统 |
| `NanoVG` | 基于 NanoVG/BGFX 的矢量 UI 和绘制能力 |
| `Network` | 引擎级网络传输、HTTP、Redis、WebSocket 等 |

### 3.3 脚本、数据和语言桥接目录

| 目录 | 用途 |
|------|------|
| `LuaScript` | Lua 脚本子系统和绑定 |
| `AngelScript` | AngelScript 子系统 |
| `Database` | 数据库统一接口 |
| `TypeScript` | 主要保存 Lua API 的 TypeScript 声明/描述文件，属于脚本开发辅助层 |

### 3.4 功能域目录

| 目录 | 用途 |
|------|------|
| `Physics` | 3D 物理封装 |
| `Navigation` | 导航网格与寻路 |
| `IK` | 逆运动学封装 |
| `Urho2D` | 2D 功能域 |
| `GamePlay` | 游戏玩法侧通用组件，如角色组件、碰撞层等 |
| `RuntimeDebugger` | 运行时调试能力 |
| `Benchmark` | 基准测试与能力探测 |

### 3.5 这一层在最终二进制里的角色

- `UrhoXRuntime` 和 `UrhoXServer` 都建立在这层之上
- 这层解决的是“通用引擎能力”
- 再往上的目录才开始引入 UrhoX 项目自己的业务含义

## 4. 引擎公共补充层：`engine/Source/Common`

这是介于“核心引擎”和“项目逻辑”之间的一层，主要补平台和 SDK 能力。

| 目录 | 用途 |
|------|------|
| `SDK` | TapTap / Themis / GME 等 SDK 的引擎侧适配，是运行时二进制里很重要的平台桥接层 |
| `Android` | Android 侧公共工具，如 Activity 辅助等 |

这一层的特点是：

- 还属于引擎侧代码
- 但已经开始明显带有 UrhoX 项目的平台集成属性

## 5. 项目公共层：`game/src/Common`

这一层是整个项目运行时的公共基础层。

| 目录 | 用途 |
|------|------|
| `Header` | 项目级共享头文件目录，很多模块都会包含这里的定义；虽然不直接产出目标文件，但它是二进制代码结构的重要“接口层” |
| `Proto` | 项目协议定义生成层，负责把 `.proto` 变成 C++ 可链接代码 |
| `CompressCommon` | 项目公共压缩能力 |
| `IOSCommon` | iOS 平台公共层 |

这层的角色通常是：

- 统一协议
- 统一公共头
- 统一平台补充

## 6. 项目引擎扩展层：`game/src/Engine`

这层可以理解成“UrhoX 自己在引擎之上补出来的一层项目引擎能力”。

| 目录 | 用途 |
|------|------|
| `CommonFunction` | 项目最常用的公共函数库，很多上层模块都会经过它 |
| `CEParticle` | 项目自己的粒子系统扩展 |
| `Scene` | 项目级场景扩展，对场景和组件体系做额外封装 |
| `LogUploader` | 日志上传相关能力 |

这一层和 `game/src/Game` 的区别是：

- `game/src/Engine` 更偏“引擎扩展”
- `game/src/Game` 更偏“玩法/业务运行时”

## 7. 项目业务运行时层：`game/src/Game`

这一层是 UrhoX 项目最贴近运行时业务的一层，主要服务客户端和服务端逻辑。

### 7.1 启动与基础运行时

| 目录 | 用途 |
|------|------|
| `Bootstrap` | 启动链路、资源准备、脚本入口切换，是 Runtime / Server 都很关键的上层目录 |
| `EventLoop` | 事件循环能力 |
| `Singleton` | 全局状态/单例式公共能力 |
| `NetManager` | 网络管理封装 |

### 7.2 联机、账号和业务服务

| 目录 | 用途 |
|------|------|
| `Network` | 项目级网络封装，衔接协议、事件循环、SDK 和引擎网络能力 |
| `Lobby` | 大厅、房间、联机前后流程 |
| `Login` | 登录流程 |
| `Score` | 分数、排行榜、云变量等客户端侧逻辑 |
| `FileUploader` | 文件上传能力 |

### 7.3 表现与运行时附加能力

| 目录 | 用途 |
|------|------|
| `CEAnimation` | 项目动画扩展 |
| `ProfilerAdaptor` | profiler 对接适配 |
| `ProfilerCustomTag` | 项目侧 profiler 标签体系 |
| `GameStatistics` | 游戏统计能力 |

### 7.4 这一层在目录依赖中的位置

这层是连接“项目公共能力”和“最终可执行入口”的最后一层业务代码：

```text
game/src/Common
  -> game/src/Engine
  -> game/src/Game
  -> UrhoXRuntime / UrhoXServer
```

## 8. 最终二进制入口层

到这一层，目录已经不再是“功能库目录”，而是最终二进制本体的入口目录。

### 8.1 `engine/Source/Tools/UrhoXRuntime`

这个目录负责把前面所有层串成客户端运行时。

它的定位不是“再提供一套通用库”，而是：

- 作为最终运行时入口
- 组织应用生命周期
- 切换脚本和运行时模式
- 提供宿主桥接和嵌入接口
- 处理 validate / host sandbox / 编辑器调试等运行时特化能力

如果从全项目目录结构里看，它位于最上层：

```text
ThirdParty + 3rd
  -> Urho3D
  -> engine/Source/Common
  -> game/src/Common
  -> game/src/Engine
  -> game/src/Game
  -> UrhoXRuntime
```

### 8.2 `engine/Source/Tools/UrhoXServer`

这个目录负责把同一套下层能力串成无头服务器运行时。

它的特点是“服务端特化”比较明显：

- 服务器配置解析
- 端口监听和连接认证
- 无头运行循环
- Lua 服务端脚本初始化
- Redis / Orchestrator / ScoreArchive 通道
- 玩家重连、空闲退出、房间状态维护

从全项目目录结构里看，它和 Runtime 共享大部分下层目录，只是在最终入口层做了服务端化切分：

```text
ThirdParty + 3rd
  -> Urho3D
  -> engine/Source/Common
  -> game/src/Common
  -> game/src/Engine
  -> game/src/Game
  -> UrhoXServer
```

## 9. 主产品二进制目录的阅读顺序

如果目的是理解“整个 UrhoX 项目的二进制目录结构”，推荐按下面顺序读：

1. `engine/Source/Urho3D`
2. `engine/Source/Common`
3. `game/src/Common`
4. `game/src/Engine`
5. `game/src/Game`
6. `engine/Source/Tools/UrhoXRuntime`
7. `engine/Source/Tools/UrhoXServer`

如果目的是理解“依赖关系从哪里往上叠”，推荐看这条线：

```text
engine/Source/ThirdParty + 3rd
  -> engine/Source/Urho3D
  -> engine/Source/Common + game/src/Common
  -> game/src/Engine
  -> game/src/Game
  -> UrhoXRuntime / UrhoXServer
```

## 10. 一句话总结

UrhoX 的主产品二进制代码不是“只有 Runtime 和 Server 两个目录”，而是一整套分层目录体系：

- `engine/Source/ThirdParty` 和 `3rd` 提供底层依赖
- `engine/Source/Urho3D` 提供引擎核心能力
- `engine/Source/Common`、`game/src/Common`、`game/src/Engine`、`game/src/Game` 提供项目自己的平台、协议、扩展和业务能力
- `engine/Source/Tools/UrhoXRuntime` 和 `engine/Source/Tools/UrhoXServer` 把这些层最终收口成客户端和服务端二进制

如果从目录用途看，真正应该重点关注的不是单个文件，而是这几层目录在整个二进制体系里的分工边界。
