---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [feature, easter-egg, gacha-system]
aliases: ["BUDDY", "Terminal Pet System"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends
-->

# Buddy

## 概述
[[Claude Code]] 中的终端电子宠物（Tamagotchi）系统，是一个完整的宠物养成游戏功能。

## 关键内容

1. **功能特性**：
   - 电子宠物系统，被称为终端里的 Tamagotchi
   - 预计 2026 年 4 月 1-7 日预告（愚人节彩蛋），2026 年 5 月正式发布
   - 使用 Mulberry32 伪随机数[[生成器]][[算法]]，以用户 ID 哈希加盐 'friend-2026-401' 为种子
   - 相同用户 ID 永远生成相同的宠物（确定性随机），确保每位用户拥有唯一宠物

2. **物种系统**：
   - 普通（Common）：60% - Pebblecrab, Dustbunny, Mossfrog, Twigling, Dewdrop, Puddlefish
   - 罕见（Uncommon）：25% - Cloudferret, Gustowl, Bramblebear, Thornfox
   - 稀有（Rare）：10% - Crystaldrake, Deepstag, Lavapup
   - 史诗（Epic）：4% - Stormwyrm, Voidcat, Aetherling
   - 传说（Legendary）：1% - Cosmoshale, Nebulynx
   - 独立闪光（Shiny）概率 1%，闪光传说宠物概率仅为 0.01%（1/10000）

3. **属性与外观**：
   - 5 个属性（0-100 分）：DEBUGGING（调试能力）、PATIENCE（耐心度）、CHAOS（混乱值）、WISDOM（智慧度）、SNARK（吐槽指数）
   - 6 种眼睛样式和 8 种帽子（高稀有度解锁更多帽子）
   - 以 5 行高、12 字符宽的 ASCII 艺术渲染，包含多帧动画（空闲、反应、互动动画）

## 来源
- [[Claude Code 源码泄露深度解析（七）：终端渲染引擎与彩蛋——BUDDY、ULTRAPLAN 与 VOICE_MODE]] — BUDDY：终端里的 Tamagotchi

## 相关
- [[Claude Code]] — part_of
- [[Gacha System]] — implements