---
summary: "WASM game loading progress tracking system with unified progress bar and byte-level download tracking"
last_updated: "2026-04-02"
---

# WebAssembly 游戏加载进度系统

## 概述

本文档描述 UrhoX WebAssembly 游戏页面（`wasm_player.html`）的加载进度跟踪系统设计与实现。

该系统提供了类似 Unity/UE 的专业加载界面，包含：
- 全局统一的进度条（0-100%）
- 分阶段的加载流程
- 字节级的下载进度跟踪
- 流畅的用户体验
- 支持多种下载模式（CDN、本地 API、ZIP 包）

### 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    用户访问 URL                              │
│                         ↓                                    │
│              检测 URL 参数（gameId?）                         │
│                    ↙         ↘                               │
│      有 gameId              无 gameId                         │
│          ↓                      ↓                            │
│    [CDN 下载模式]          [本地/ZIP 模式]                     │
│    获取游戏信息               本地 API 下载                    │
│    记录播放次数                   ↓                           │
│    下载 manifest          失败？ZIP 包回退                     │
│    下载 Lua 文件                 ↓                           │
│          ↓                      ↓                            │
│    [资源已就绪] ←───────────────┘                            │
│          ↓                                                   │
│    下载 .data 文件 (Emscripten 资源包)                        │
│          ↓                                                   │
│    下载 .wasm 文件 (引擎二进制)                               │
│          ↓                                                   │
│    编译 WebAssembly                                          │
│          ↓                                                   │
│    挂载文件到虚拟 FS                                          │
│          ↓                                                   │
│    设置入口脚本参数 (CDN 模式)                                 │
│          ↓                                                   │
│    游戏启动                                                   │
└─────────────────────────────────────────────────────────────┘

进度条：0% ════════════════════════════════════════ 100%
         API/CDN  .data   .wasm    挂载
         0-30%   30-60%  60-85%  85-100%
```

## 加载阶段划分

整个加载流程分为 **4 个主要阶段**，每个阶段占用全局进度的一部分：

| 阶段 | 全局进度范围 | 主要任务 | 进度来源 |
|------|-------------|---------|---------|
| **1. API 文件下载** | 0% - 30% | 下载游戏资源文件（Lua 脚本、配置等） | HTTP API 下载回调 |
| **2. .data 文件下载** | 30% - 60% | 下载 Emscripten 数据包（~18MB） | Fetch 拦截器 |
| **3. .wasm 文件下载** | 60% - 85% | 下载 WebAssembly 二进制 | instantiateWasm 钩子 |
| **4. 文件系统挂载** | 85% - 100% | 将文件挂载到虚拟 FS | 手动计数 |

## 下载模式

系统支持 **3 种下载模式**，根据 URL 参数和配置自动选择：

### 模式 1：CDN 下载（游戏平台模式）⭐ 新增

**URL 格式**：`UrhoXRuntime.html?gameId=abc123`

**触发条件**：URL 包含 `gameId` 参数

**工作流程**：
```
1. 调用后端 API：/api/games/{gameId}
   → 获取游戏名称、CDN 地址等信息

2. 记录播放次数：POST /api/games/{gameId}/play
   → 使用 sendBeacon 确保可靠发送

3. 下载清单文件：{cdn_base_url}/manifest.json
   → 获取文件列表和入口脚本路径

4. 下载 Lua 文件：并发下载（6 并发）
   → 保存到 IndexedDB

5. 存储入口脚本：gameEntryFile = "Scripts/main.lua"
   → 在文件挂载后设置 Module.arguments
```

**实现类**：`CdnFileDownloader` (wasm_player.html:845-1041)

**关键特性**：
- 🎮 支持游戏平台的多用户游戏托管
- 📊 自动统计游戏播放次数
- 🚀 从 CDN 快速下载（6 并发）
- 💾 游戏信息持久化到 localStorage
- 🎯 动态设置游戏入口脚本

### 模式 2：本地 API 下载（开发模式）

**URL 格式**：`UrhoXRuntime.html`（无参数）

**触发条件**：`ENABLE_API_DOWNLOAD = true` 且无 gameId 参数

**工作流程**：
```
1. 调用本地 API：/api/wark_dir?path=AgentProject
   → 获取文件列表

2. 清理过期文件：删除服务器上不存在的文件

3. 并发下载：10 个并发下载文件
   → 保存到 IndexedDB
```

**实现类**：`ApiFileDownloader` (wasm_player.html:591-841)

**适用场景**：本地开发、调试

### 模式 3：ZIP 包下载（回退模式）

**URL 格式**：`UrhoXRuntime.html`

**触发条件**：CDN 和 API 下载都失败时

**工作流程**：
```
1. 下载 ZIP 包：AgentProject.zip
2. 解压文件
3. 保存到 IndexedDB
```

**实现类**：`PackageDownloader` (在 PackageDownload.js 中定义)

**适用场景**：无后端支持时的静态部署

## 详细加载流程

### 阶段 1：游戏资源下载 (0% - 30%)

**触发时机**：页面加载后立即开始

#### 模式 1：CDN 下载
```
0%    "Connecting to game server..."     - 初始化
0-5%  "Loading game: {游戏名称}"         - 获取游戏信息
5-10% "Preparing to download X files..." - 加载清单
10-80% "Downloading game scripts (X/Y, XX KB)" - 下载 Lua 文件（6 并发）
80-100% "Saving to cache (X/Y)..."      - 保存到 IndexedDB
```

**进度计算**：
```javascript
// 游戏信息：0-5% of apiDownload stage
updateGlobalProgress('apiDownload', 5, 'Loading game: ' + gameName);

// 清单加载：5-10%
updateGlobalProgress('apiDownload', 10, 'Preparing to download ' + totalFiles + ' files...');

// 下载阶段：10-80%
const stagePercent = 10 + (current / total) * 70;
updateGlobalProgress('apiDownload', stagePercent, statusText);

// 保存阶段：80-100%
const stagePercent = 80 + (current / total) * 20;
updateGlobalProgress('apiDownload', stagePercent, statusText);

// 映射到全局进度：0-30%
globalPercent = stagePercent * 0.3;
```

**关键代码**：`wasm_player.html:1297-1388`

#### 模式 2：本地 API 下载
```
0%    "Preparing download..."           - 获取文件列表
0-3%  "Cleaning up old files..."        - 清理过期缓存
3-24% "Downloading game assets..."      - 并发下载文件（10 并发）
24-30% "Saving to cache..."             - 保存到 IndexedDB
```

**关键代码**：`wasm_player.html:1221-1294`

#### 模式 3：ZIP 包下载
```
0-24% "Downloading package..."          - 下载 ZIP
24-27% "Extracting files..."            - 解压
27-30% "Saving to cache..."             - 保存到 IndexedDB
```

**关键代码**：`wasm_player.html:1390-1431`

### 阶段 2：.data 文件下载 (30% - 60%)

**触发时机**：Emscripten 初始化时自动请求 `.data` 文件

**主要步骤**：
```
30%   开始下载 UrhoXRuntime.data
30-60% "Downloading game data (X.X MB / 18.8 MB)"
60%   "Game data loaded"
```

**进度计算**：
```javascript
// 字节级进度
var loaded = 0;
var total = 18874368;  // 从 Content-Length 获取
var percent = Math.floor((loaded / total) * 100);

// 映射到全局进度：30-60%
globalPercent = 30 + percent * 0.3;
```

**实现方式**：拦截全局 `fetch()` API
```javascript
window.fetch = function(url, options) {
  if (url.includes('.data')) {
    // 使用 ReadableStream 逐块读取
    reader.read().then(result => {
      loaded += result.value.length;
      updateGlobalProgress('dataFile', percent, statusText);
    });
  }
}
```

**关键代码**：`wasm_player.html:334-422`

### 阶段 3：.wasm 文件下载 (60% - 85%)

**触发时机**：加载 `UrhoXRuntime.js` 后

**主要步骤**：
```
60%   开始下载 UrhoXRuntime.wasm
60-85% "Downloading WebAssembly (X.X MB / Y.Y MB)"
85%   "Compiling WebAssembly..."
85%   编译完成，准备挂载文件
```

**进度计算**：
```javascript
// 字节级进度
var percent = Math.floor((loaded / total) * 100);

// 映射到全局进度：60-85%
globalPercent = 60 + percent * 0.25;
```

**实现方式**：覆盖 `Module.instantiateWasm`
```javascript
Module = {
  instantiateWasm: function(imports, successCallback) {
    fetch('UrhoXRuntime.wasm').then(response => {
      reader.read().then(result => {
        loaded += result.value.length;
        updateGlobalProgress('wasmFile', percent, statusText);
      });
    });
  }
}
```

**关键代码**：`wasm_player.html:425-503`

### 阶段 4：文件系统挂载 (85% - 100%)

**触发时机**：`Module.preRun` 阶段

**主要步骤**：
```
85%   "Reading files from cache..."      - 从 IndexedDB 读取文件（阻塞 2-3 秒）
86%   "Starting to mount X files..."     - 开始挂载
86-100% "Mounting files (X/Y)..."        - 分批挂载到虚拟 FS
100%  "Game starting..."                 - 游戏启动
```

**进度计算**：
```javascript
// 读取阶段完成后：5% of mounting stage
globalPercent = 85 + 5 * 0.15 = 85.75%;

// 挂载进度：5-100% of mounting stage
var mountPercent = (mountedCount / totalFiles) * 100;
var stagePercent = 5 + mountPercent * 0.95;
globalPercent = 85 + stagePercent * 0.15;
```

**实现方式**：分批挂载 + setTimeout 让出控制权
```javascript
// 每 5 个文件一批
for (let i = 0; i < files.length; i += 5) {
  const batch = files.slice(i, i + 5);
  for (const file of batch) {
    FS.writeFile(fsPath, fileData);
  }
  updateGlobalProgress('mounting', percent, statusText);
  await new Promise(resolve => setTimeout(resolve, 0));  // 让出控制权
}
```

**关键代码**：`wasm_player.html:894-987`

## 核心技术实现

### 1. 全局进度管理

**核心函数**：`updateGlobalProgress(stage, stagePercent, statusText)`

```javascript
var progressStages = {
  apiDownload: { start: 0, end: 30 },
  dataFile:    { start: 30, end: 60 },
  wasmFile:    { start: 60, end: 85 },
  mounting:    { start: 85, end: 100 }
};

function updateGlobalProgress(stage, stagePercent, statusText) {
  var stageInfo = progressStages[stage];
  var globalPercent = stageInfo.start +
    (stageInfo.end - stageInfo.start) * (stagePercent / 100);

  // 更新 UI
  loadingProgressBar.style.width = globalPercent + '%';
  loadingPercent.textContent = globalPercent + '%';
  loadingStatus.textContent = statusText;
}
```

**位置**：`wasm_player.html:286-332`

**优点**：
- 统一的进度计算方式
- 各阶段独立，易于调整
- 进度条永不回退

### 2. 性能优化：节流更新

**问题**：每个下载 chunk（几 KB）都更新 UI 会导致数千次 DOM 操作

**解决方案**：节流 - 每 100ms 或进度变化 1% 才更新

```javascript
var lastProgressUpdate = {
  time: 0,
  percent: -1
};

function updateGlobalProgress(stage, stagePercent, statusText) {
  var now = Date.now();
  var timeSinceLastUpdate = now - lastProgressUpdate.time;
  var percentChange = Math.abs(globalPercent - lastProgressUpdate.percent);

  // 节流：至少间隔 100ms 或变化 1%
  if (timeSinceLastUpdate < 100 && percentChange < 1 &&
      globalPercent !== 0 && globalPercent !== 100) {
    return;  // 跳过本次更新
  }

  lastProgressUpdate.time = now;
  lastProgressUpdate.percent = globalPercent;

  // 更新 UI
  // ...
}
```

**效果**：
- DOM 更新次数从 ~3000 次降低到 ~20 次
- 不影响流畅度（100ms 间隔人眼无法察觉）

### 3. Fetch API 拦截

用于跟踪 `.data` 文件的下载进度：

```javascript
(function() {
  var originalFetch = window.fetch;
  window.fetch = function(url, options) {
    if (url.includes('.data')) {
      return originalFetch(url, options).then(response => {
        var reader = response.body.getReader();
        var stream = new ReadableStream({
          start: function(controller) {
            function push() {
              reader.read().then(result => {
                if (!result.done) {
                  loaded += result.value.length;
                  updateGlobalProgress('dataFile', percent, statusText);
                  controller.enqueue(result.value);
                  push();
                }
              });
            }
            push();
          }
        });
        return new Response(stream, { headers: response.headers });
      });
    }
    return originalFetch(url, options);
  };
})();
```

**关键点**：
- 透明拦截，Emscripten 无感知
- 使用 ReadableStream 保持流式传输
- 不影响下载性能

## 已知限制与注意事项

### 1. IndexedDB 读取阶段会阻塞

**问题描述**：
在 "Reading files from cache..." 阶段（85%），进度条会暂停 2-3 秒。

**原因**：
```javascript
const files = await downloader.getAllFiles();  // 阻塞主线程
```

- `getAllFiles()` 是同步阻塞操作
- 虽然返回 Promise，但内部读取是同步的
- JavaScript 单线程特性，无法在读取期间更新 UI

**用户体验**：
- ✅ 进度条的 shimmer 光泽动画继续运行（CSS 动画在合成器线程）
- ❌ 百分比数字不更新（JavaScript 被阻塞）
- ✅ 状态文本显示 "Reading files from cache..."

**为什么不能分批读取？**
```javascript
// ❌ 这样会导致 transaction 失效
cursor.onsuccess = async function() {
  await setTimeout(0);  // 跳到下一个事件循环
  cursor.continue();    // 报错：transaction not active
}
```

IndexedDB 的 transaction 在事件循环结束后自动关闭，无法在异步操作中继续使用。

### 2. 进度百分比是估算值

**原因**：
- 各阶段耗时不同（网络条件、文件数量、设备性能）
- 进度范围是固定分配的（30%、30%、25%、15%）

**实际情况**：
- 如果 .data 文件下载很快，进度会在 30-60% 快速跳跃
- 如果文件挂载很慢，85-100% 会感觉较长

**优化建议**：
可以根据实际测试数据调整各阶段的进度范围。

### 3. 浏览器兼容性

**要求**：
- ✅ 支持 `fetch()` API
- ✅ 支持 `ReadableStream`
- ✅ 支持 `async/await`
- ✅ 支持 IndexedDB

**兼容性**：
- Chrome 52+
- Firefox 65+
- Safari 14.1+
- Edge 79+

**不支持的浏览器**：
- IE 11（不支持 WebAssembly）
- 旧版移动浏览器

## 视觉设计

### 加载界面元素

```
┌──────────────────────────────────────────┐
│                                          │
│            [UrhoX Logo]                  │
│              (淡入动画)                   │
│                                          │
│  ════════════════════ 45% ═════         │
│        (蓝色渐变进度条 + 光泽动画)         │
│                                          │
│     Downloading game data               │
│       (8.5 MB / 18.8 MB)                │
│                                          │
│              45%                         │
│          (当前百分比)                     │
│                                          │
└──────────────────────────────────────────┘
```

### 动画效果

**1. Logo 淡入 + 呼吸**
```css
@keyframes logoFadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes logoPulse {
  0%, 100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.3)); }
  50% { filter: drop-shadow(0 0 30px rgba(255,255,255,0.5)); }
}
```

**2. 进度条光泽流动**
```css
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
```

**3. 完成后淡出**
```css
#loading-screen.hidden {
  opacity: 0;
  transition: opacity 0.5s ease-out;
  pointer-events: none;
}
```

## 控制台日志示例

### CDN 下载模式

```
=== Game Platform Mode Detected ===
Game ID: abc123
API Base URL: https://games.example.com

=== Attempting CDN-based file download ===
[CDN] Fetching game info from: https://games.example.com/api/games/abc123
[CDN] Game info: { name: "飞扬的小鸟", cdn_base_url: "...", ... }
[CDN] Play count recorded (sendBeacon)
[CDN] Fetching manifest from: https://cdn.example.com/games/abc123/manifest.json
[CDN] Manifest loaded: { entry_file: "Scripts/main.lua", files: [...] }
[CDN] Found 23 Lua files to download
[CDN] Starting parallel downloads (6 concurrent)
[CDN] Downloaded 6/23 files → Global: 15%
[CDN] Downloaded 23/23 files → Global: 24%
[CDN] Download complete: 23/23 files
[CDN] Saved 23 files to IndexedDB
✓ Entry file stored globally: Scripts/main.lua
=== CDN Download Complete ===

=== Intercepted .data file request: UrhoXRuntime.data ===
[DATA] Stage progress: 50% → Global: 45%
[DATA] Download complete: 18.8 MB

=== Starting .wasm download from: UrhoXRuntime.wasm ===
[WASM] Stage progress: 50% → Global: 72%
[WASM] Download complete: 5.8 MB

=== Starting FS Mount Process ===
✓ Loaded 23 files from cache in 234ms
✓ Files mounted successfully (23 files)
✓ Set Module.arguments: ["Scripts/main.lua"]  ⭐ 动态设置入口脚本
✓ Entry script will be launched: Scripts/main.lua
=== Module.postRun: Game started successfully ===
```

### 本地 API 下载模式

```
=== Local Development Mode ===
=== Attempting API-based file download ===
[API] File list received: 450 files
[API] Downloaded 100/450 files → Global: 15%
[API] Downloaded 450/450 files → Global: 30%
=== API Download Complete ===

=== Intercepted .data file request: UrhoXRuntime.data ===
[DATA] Stage progress: 10% → Global: 33%
[DATA] Stage progress: 50% → Global: 45%
[DATA] Stage progress: 100% → Global: 60%
[DATA] Download complete: 18.8 MB

=== Starting .wasm download from: UrhoXRuntime.wasm ===
[WASM] Stage progress: 10% → Global: 62%
[WASM] Stage progress: 50% → Global: 72%
[WASM] Stage progress: 100% → Global: 85%
[WASM] Download complete: 5.8 MB
=== .wasm compiled and instantiated successfully ===

=== Starting FS Mount Process ===
✓ Loaded 450 files from cache in 2340ms
[Mounting] Stage progress: 50% → Global: 92%
✓ All files mounted in 3120ms total
=== Module.postRun: Game started successfully ===
```

## 游戏启动参数

系统支持两种方式指定游戏入口脚本：

### 方式 1：游戏平台模式（动态设置）⭐ 推荐

**URL 格式**：`UrhoXRuntime.html?gameId=abc123`

**流程**：
```javascript
// 1. CDN 下载器从 manifest 获取入口脚本
const result = await cdnDownloader.downloadAndSaveFiles();
gameEntryFile = result.entryFile;  // "Scripts/main.lua"

// 2. 在文件挂载后设置 Module.arguments（最安全的时机）
mountFilesToFS(packageDownloader).then(function(count) {
  if (gameEntryFile) {
    window.gameScript = gameEntryFile;
    if (!Module.arguments) Module.arguments = [];
    Module.arguments.unshift(gameEntryFile);  // 插入到开头
    console.log('✓ Entry script will be launched:', gameEntryFile);
  }
  Module.removeRunDependency('packageFiles');  // 触发游戏启动
});
```

**关键代码**：wasm_player.html:512-522, 1370

**优点**：
- ✅ 从服务器动态获取入口脚本，无需硬编码
- ✅ 支持不同游戏使用不同入口脚本
- ✅ 时序安全：在文件挂载完成后才设置参数

### 方式 2：直接脚本模式（向后兼容）

**URL 格式**：`UrhoXRuntime.html?Scripts/FlappyBird.lua`

**流程**：
```javascript
// 解析 URL 参数
const queryString = window.location.search;  // "?Scripts/FlappyBird.lua"
const scriptParam = queryString.substring(1); // "Scripts/FlappyBird.lua"

// 立即设置 Module.arguments（页面加载时）
window.gameScript = scriptParam;
if (!Module.arguments) Module.arguments = [];
Module.arguments.unshift(scriptParam);
```

**关键代码**：wasm_player.html:1427-1459

**适用场景**：
- 开发调试时快速指定脚本
- 不依赖游戏平台的独立部署

### 时序对比

| 方式 | 设置时机 | 文件是否已挂载 | 优先级 |
|------|---------|---------------|--------|
| 游戏平台模式 | `mountFilesToFS().then()` | ✅ 是 | 高（推荐）|
| 直接脚本模式 | 页面加载时 | ❌ 否 | 低（兼容）|

**注意**：如果同时使用 `gameId` 和脚本参数，游戏平台模式优先（因为它在挂载后才设置，会覆盖）。

## 维护建议

### 调整进度范围

如果发现某个阶段耗时特别长，可以调整进度分配：

```javascript
// wasm_player.html:287-292
var progressStages = {
  apiDownload: { start: 0,  end: 20  },  // 减少到 20%
  dataFile:    { start: 20, end: 60  },  // 增加到 40%
  wasmFile:    { start: 60, end: 85  },
  mounting:    { start: 85, end: 100 }
};
```

### 添加新的加载阶段

1. 在 `progressStages` 中定义新阶段
2. 调整其他阶段的范围
3. 在相应代码中调用 `updateGlobalProgress(newStage, percent, text)`

### 性能监控

添加更详细的日志来监控各阶段耗时：

```javascript
const stageTimings = {};
stageTimings['apiDownload'] = performance.now();
// ... 阶段完成后
console.log('[Timing] API Download:', performance.now() - stageTimings['apiDownload'], 'ms');
```

## 游戏平台集成

### CdnFileDownloader API

**后端 API 接口**：

#### 1. 获取游戏信息
```
GET /api/games/{gameId}

Response:
{
  "id": "abc123",
  "name": "飞扬的小鸟",
  "cdn_base_url": "https://cdn.example.com/games/abc123",
  "created_at": "2025-01-17T00:00:00Z",
  ...
}
```

#### 2. 记录播放次数
```
POST /api/games/{gameId}/play

Request: {}
Response: { "success": true, "play_count": 42 }
```

**实现特点**：
- 使用 `navigator.sendBeacon()` 确保可靠发送（即使页面关闭）
- 回退到 `fetch()` with `keepalive: true`

#### 3. 下载清单文件
```
GET {cdn_base_url}/manifest.json

Response:
{
  "entry_file": "Scripts/main.lua",
  "base_url": "https://cdn.example.com/games/abc123",
  "files": [
    { "path": "Scripts/main.lua", "size": 1234, "hash": "..." },
    { "path": "Scripts/utils.lua", "size": 567, "hash": "..." },
    ...
  ]
}
```

### LocalStorage 持久化

游戏平台模式会将游戏信息保存到 localStorage：

```javascript
localStorage.setItem('current_game_id', gameId);
localStorage.setItem('current_game_name', gameName);
```

**用途**：
- 记录用户最后玩的游戏
- 快速访问（下次打开页面时可以显示游戏名）
- 离线支持（缓存游戏信息）

## 下载模式选择逻辑

**启动流程** (wasm_player.html:1349-1410)：

```javascript
const urlParams = new URLSearchParams(window.location.search);
const gameId = urlParams.get('gameId');

// 优先级 1: CDN 下载（检测到 gameId）
if (gameId && typeof CdnFileDownloader === 'function') {
  success = await tryCdnDownload(gameId, apiBaseUrl);
  if (!success) {
    // CDN 下载失败，无法继续（游戏文件未知）
    return;
  }
}

// 优先级 2: 本地 API 下载（开发模式）
else if (ENABLE_API_DOWNLOAD && typeof ApiFileDownloader === 'function') {
  success = await tryApiDownload();
}

// 优先级 3: ZIP 包下载（回退）
if (!success && ENABLE_PACKAGE_DOWNLOAD) {
  success = await fallbackToZipDownload();
}

// 优先级 4: 使用缓存文件
if (!success) {
  loadGame();  // 尝试使用已缓存的文件
}
```

**决策树**：
```
URL 包含 gameId?
  ├─ 是 → CDN 下载
  │      ├─ 成功 → 启动游戏
  │      └─ 失败 → 显示错误（无法继续）
  │
  └─ 否 → 本地 API 下载
         ├─ 成功 → 启动游戏
         └─ 失败 → ZIP 包下载
                  ├─ 成功 → 启动游戏
                  └─ 失败 → 使用缓存文件
```

## 参考资料

- **Emscripten 文档**: https://emscripten.org/docs/
- **IndexedDB API**: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- **ReadableStream**: https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
- **Unity/UE 加载界面设计**: 参考标准的游戏引擎开屏页
- **Navigator.sendBeacon**: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon

## 更新日志

- **2025-01-17**: 初始文档创建，记录完整的加载进度系统设计
- **2025-01-17**: 添加 CDN 下载模式、游戏平台集成、动态入口脚本设置
