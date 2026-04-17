---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [游戏引擎, UrhoX, Lua, API, 生命周期, 时间]
aliases: [UrhoX Engine API, UrhoX Time API, 引擎生命周期]
relates_to: [UrhoX引擎, UrhoX Lua开发准则, Delta-time运动模式]
supersedes: null
---
# UrhoX引擎生命周期API

## 概述
[[UrhoX引擎|UrhoX]] `Engine` 和 `Time` 对象控制引擎[[游戏主循环模式|主循环]]与时间采样，二者均继承自 `Object`，通过[[UrhoX全局子系统|全局单例]]访问（Lua 中为 `engine` 和 `time`）。

## 关键内容
1. **Engine 帧率控制**：`minFps/maxFps` 设定帧率下限/上限（防止极低帧时步长过大）；`maxInactiveFps` 在后台/失焦时降低帧率节省资源；`timeStepSmoothing` 指定帧率平滑窗口（帧数），消除尖刺。
2. **Engine 状态查询**：`IsInitialized()/IsExiting()/IsHeadless()` 检查引擎状态；`headless` 用于服务端无渲染模式判断；`Exit()` 主动退出引擎。
3. **Engine 调试工具**：`DumpProfiler()` 打印性能分析数据；`DumpResources(dumpFileName)` 列出已加载资源；`DumpMemory()` 输出内存统计；`CreateConsole()/CreateDebugHud()` 动态创建调试界面。
4. **Engine 运行控制**：`RunFrame()` 手动推进一帧（非标准用法，通常由引擎自动调用）；`pauseMinimized` 控制最小化时是否暂停；`autoExit` 控制关闭窗口时是否自动退出。
5. **Time 时间采样**：`timeStep`（当前帧 delta-time，秒）是驱动物理/动画/移动的核心值；`elapsedTime` 为引擎启动以来累计秒数；`frameNumber` 为帧计数器（uint）。
6. **Time 工具方法**：`GetSystemTime()` 返回 Unix 时间戳（毫秒）；`GetTimeStamp()` 返回格式化时间字符串；`Sleep(ms)` 阻塞当前线程（谨慎使用，会卡住[[游戏主循环模式|主循环]]）；`timerPeriod` 为系统定时器精度（毫秒）。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/core]] — UrhoX Lua API Core Module，Engine 和 Time 类完整方法与属性列表

## 相关
- [[UrhoX引擎]] — part_of
- [[UrhoX Lua开发准则]] — relates_to，引擎配置规则
- [[Delta-time运动模式]] — timeStep 是 delta-time 运动的数据来源
- [[UrhoX场景系统API]] — Scene::SetTimeScale 与 Engine 时间控制协同
