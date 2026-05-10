---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏", "工具", "游戏开发"]
aliases: [UrhoX Audio API, 音频模块, SoundSource, SoundSource3D]
relates_to:
  - target: "[[UrhoX引擎]]"
    type: part_of
    confidence: 0.9
  - target: "[[UrhoX Lua开发准则]]"
    type: extends
    confidence: 0.8
supersedes: null
---
# UrhoX音频系统API

## 概述

[[UrhoX引擎|UrhoX]] 引擎音频模块提供五个核心类：Audio（子系统）、Sound（资源）、SoundSource（2D音源组件）、SoundSource3D（3D空间音源）、SoundListener（听者组件），支持 WAV、OGG Vorbis、MP3 及原始 PCM 格式。

## 关键内容

### 类层级

- `Audio : Object` — 音频子系统，管理混音、主音量、声音类型暂停/恢复
- `Sound : ResourceWithMetadata` — 音频资源，支持 WAV/OGG/MP3/PCM
- `SoundSource : Component` — 2D 音源组件，挂载到节点，控制播放/增益/声像
- `SoundSource3D : SoundSource` — 3D 空间音源，增加距离衰减与角度衰减
- `SoundListener : Component` — 听者位置组件，挂载到相机或角色节点

### Audio 子系统

主要方法：
- `SetMode(bufferLengthMSec, mixRate, stereo, interpolation)` — 初始化混音器
- `SetMasterGain(type, gain)` — 按声音类型[[Settings|设置]]主音量（如 `"Music"`、`"Effect"`）
- `PauseSoundType(type)` / `ResumeSoundType(type)` / `ResumeAll()` — 声音类型暂停控制
- `SetListener(listener)` — 绑定听者组件
- `StopSound(sound)` — 停止指定 Sound 资源的所有播放实例

### Sound 资源加载

推荐通过资源缓存加载，引擎自动按扩展名识别格式：
```lua
local sound = cache:GetResource("Sound", "Sounds/effect.ogg")
```
低层接口：`LoadWav()` / `LoadOggVorbis()` / `LoadMp3()` / `LoadRaw()`

循环设置：`sound.looped = true` 或 `sound:SetLoop(repeatOffset, endOffset)`

### SoundSource 组件

播放重载：
```lua
soundSource:Play(sound)
soundSource:Play(sound, frequency)
soundSource:Play(sound, frequency, gain)
soundSource:Play(sound, frequency, gain, panning)
```

关键属性：
- `soundType` — 声音分类字符串，与 `Audio:SetMasterGain` 对应
- `gain` — 音量（0.0～1.0+）
- `panning` — 声像（-1.0 左～+1.0 右）
- `attenuation` — 衰减系数
- `autoRemoveMode` — 播放完成后自动移除节点模式

### SoundSource3D 空间音频

在 SoundSource 基础上增加：
- `SetDistanceAttenuation(nearDistance, farDistance, rolloffFactor)` — 距离衰减范围
- `SetAngleAttenuation(innerAngle, outerAngle)` — 方向性锥角衰减
- 属性：`nearDistance`、`farDistance`、`innerAngle`、`outerAngle`、`rolloffFactor`

3D 音效需配合 `SoundListener` 组件（挂载到相机节点）方可正确计算空间位置。

### 典型用法（Lua）

```lua
-- 2D 音效
local sfxNode = scene:CreateChild("SFX")
local src = sfxNode:CreateComponent("SoundSource")
src.soundType = "Effect"
src:Play(cache:GetResource("Sound", "Sounds/jump.ogg"))

-- 3D 音效
local src3d = enemyNode:CreateComponent("SoundSource3D")
src3d:SetDistanceAttenuation(1.0, 30.0, 1.0)
src3d:Play(cache:GetResource("Sound", "Sounds/growl.ogg"))
```

## 来源

- [[raw/articles/personal/ai-dev-kit/engine-docs/api/audio.md]] — UrhoX Lua API Audio Module 文档

## 相关

- [[UrhoX引擎]] — part_of：音频模块是 UrhoX 引擎子系统之一
- [[UrhoX Lua开发准则]] — extends：音频 API 遵循 UrhoX Lua 开发规范
