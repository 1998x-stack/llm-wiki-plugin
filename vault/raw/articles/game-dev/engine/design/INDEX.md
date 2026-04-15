# 架构设计文档

> 写入者: Agent/人 | 生命周期: 长期维护 | 防腐策略: 代码变更时交叉检查；定期巡检

## 动画系统

| 文档 | 摘要 |
|------|------|
| [animation-system-design](animation-system-design.md) | AI 友好的声明式动画系统架构 |
| [animation-retargeting-design](animation-retargeting-design.md) | 基于 UE5 IK Retargeter 的骨骼重定向 |
| [runtime-animation-retargeting](runtime-animation-retargeting.md) | 运行时透明动画重定向 |
| [animation-editor-architecture](animation-editor-architecture.md) | 动画编辑器三模块架构（Preview/Window/StateMachine） |
| [state-machine-editor-architecture](state-machine-editor-architecture.md) | 状态机可视化编辑器完整功能 |

## 渲染系统

| 文档 | 摘要 |
|------|------|
| [screen-space-algorithm-design](screen-space-algorithm-design.md) | HiZ, SSAO, SSR, TAA 屏幕空间算法 |
| [nanovg-drawcall-batching-design](nanovg-drawcall-batching-design.md) | NanoVG BGFX 后端 DC 合批优化 |
| [nanovg-font-system-refactor](nanovg-font-system-refactor.md) | NanoVG 字体系统切换到引擎 Font |
| [hlod-world-partition-design](hlod-world-partition-design.md) | HLOD + World Partition 大场景方案 |

## 地形系统

| 文档 | 摘要 |
|------|------|
| [tile-terrain-design](tile-terrain-design.md) | TileTerrain 核心架构（程序层 + 场景层） |
| [tile-terrain-mesh-merge-design](tile-terrain-mesh-merge-design.md) | 运行时网格合并 + HLOD |
| [tile-terrain-blend-material-design](tile-terrain-blend-material-design.md) | ID+Weight Control Map 地形混合材质 |

## 网络系统

| 文档 | 摘要 |
|------|------|
| [network-transport-design](network-transport-design.md) | Transport 抽象层 v2（UDP/WebSocket/KCP） |
| [kcp-transport-integration-design](kcp-transport-integration-design.md) | KCP 传输集成设计 |

## 视频播放

| 文档 | 摘要 |
|------|------|
| [videoplayer-crossplatform-design](videoplayer-crossplatform-design.md) | 跨平台视频播放器架构（FFmpeg/MediaCodec/AVFoundation） |
| [videoplayer-asyncload-design](videoplayer-asyncload-design.md) | Native 平台异步加载设计 |

## 边玩边下 (DWP)

| 文档 | 摘要 |
|------|------|
| [dwp-render-blocking-preload-design](dwp-render-blocking-preload-design.md) | RenderBlocking 资源预加载兜底设计 |

## 安全与沙箱

| 文档 | 摘要 |
|------|------|
| [sandbox-isolation-design](sandbox-isolation-design.md) | Lua 游戏脚本文件沙箱隔离 |

## UI 布局

| 文档 | 摘要 |
|------|------|
| [yoga-integration](yoga-integration.md) | Yoga 布局引擎集成（C++20→C++17 适配） |

## 角色控制

| 文档 | 摘要 |
|------|------|
| [character-component-air-control](character-component-air-control.md) | CharacterComponent 空中控制系统改进 |

## 示例项目

| 文档 | 摘要 |
|------|------|
| [minecraft-texture-pack-system](minecraft-texture-pack-system.md) | Minecraft 材质包系统 + HD PBR 支持 |

## 构建管线 ([build-pipeline/](build-pipeline/INDEX.md))

| 文档 | 摘要 |
|------|------|
| [meta-application-design](build-pipeline/meta-application-design.md) | .meta 文件策略 |
| [resource-uuid-design](build-pipeline/resource-uuid-design.md) | UUID 编码（18 bytes, Base64）用于 UGC 分发 |
| [project-builder](build-pipeline/project-builder.md) | Manifest + 资源生成 |
| [native-bootstrap-loader](build-pipeline/native-bootstrap-loader.md) | Native 平台（Windows/Android/iOS）游戏加载 |
| [web-bootstrap-loader](build-pipeline/web-bootstrap-loader.md) | WASM 平台游戏加载 |

---

*最后更新: 2026-04-02*
