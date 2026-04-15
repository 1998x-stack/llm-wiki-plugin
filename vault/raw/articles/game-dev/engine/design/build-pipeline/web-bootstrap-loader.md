---
summary: "Web platform (WebAssembly) bootstrap loading system with Project Index architecture"
related_paths:
  - tools/generators/**
last_updated: "2025-12-17"
---

# Web 启动加载器 - Project Index 架构

本文档描述 UrhoX Web 平台（WebAssembly）的启动加载系统，对应原生平台的 [native-bootstrap-loader.md](./native-bootstrap-loader.md)。

---

## 📋 目录

- [概述](#概述)
- [文件结构](#文件结构)
- [加载流程](#加载流程)
- [核心组件](#核心组件)
- [进度更新](#进度更新)
- [智能缓存策略](#智能缓存策略)
- [远程加载（game_url）](#远程加载game_url)
- [构建打包](#构建打包)
- [API 参考](#api-参考)

---

## 概述

### 与原生平台对比

| 特性 | Web (project-index) | Native (Bootstrap) |
|------|---------------------|-------------------|
| 入口文件 | `index.html` + `index.js` | C++ BootstrapManager |
| 资源加载 | Emscripten + fetch | HTTP 下载到本地缓存 |
| 进度来源 | Module.setStatus 解析 | Step 回调 |
| 文件映射 | JS fileMap | ManifestResolver |
| 整包下载 | 不支持（Emscripten 内置） | assets.7z |

### 核心特性

| 特性 | 说明 |
|------|------|
| **Manifest 驱动** | 从 CDN 加载 manifest，构建文件映射表 |
| **动态资源加载** | Logo、version.json 等从 manifest 获取 CDN URL |
| **远程加载支持** | 通过 `game_url` 参数加载远程项目 |
| **智能缓存** | 含 hash 的文件名不加时间戳 |
| **JS 打包** | 多个 JS 文件合并为 index.js |

---

## 文件结构

### 源文件（开发时）

```
tools/templates/
├── project-index.html          # 入口 HTML 模板
├── project-index.js            # 主加载器
└── extensions/                 # 扩展功能
    ├── web_audio_unlock.js     # 音频解锁
    ├── floating_action_button.js
    ├── error_clipboard.js      # 错误复制
    ├── postmessage_bridge.js   # PostMessage 桥接
    └── user_script_loader.js   # 用户脚本加载
```

### 构建产物

```
build_agent_wasm/bin/
├── index.html                  # 入口页面（从 project-index.html）
├── index.js                    # 打包后的 JS（project-index.js + extensions）
├── UrhoXRuntime.html           # 旧版入口（兼容）
├── UrhoXRuntime.js             # Emscripten 生成
├── UrhoXRuntime.wasm           # WebAssembly 二进制
└── UrhoXRuntime.data           # Emscripten 数据包
```

---

## 加载流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      project-index.js 加载流程                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. loadProjectInfo()                                                   │
│     └── project.json → 获取 project_id（供 C++ 使用）                    │
│         └── 支持 game_url 参数指定远程项目                               │
│                                                                         │
│  2. loadManifests()                                                     │
│     ├── latest.json → 版本信息                                          │
│     ├── {version}/engine-{tag}.json → 引擎源配置                        │
│     ├── {base_url}/{version}/version.json → 版本详情                    │
│     ├── {base_url}/{version}/manifest-{hash}.json → 资源清单            │
│     └── buildFileMap() → 构建 fs_path → CDN URL 映射                   │
│                                                                         │
│  3. 动态资源加载                                                         │
│     ├── LogoLarge.png → 从 fileMap 获取 CDN URL                        │
│     └── version.json → __ENGINE_BUILD_INFO__                           │
│                                                                         │
│  4. loadEngine()                                                        │
│     └── UrhoXRuntime.js → 从 fileMap 获取 CDN URL，动态 <script> 加载   │
│                                                                         │
│  5. Emscripten 加载                                                     │
│     ├── Module.locateFile() → .wasm/.data 重定向到 CDN                  │
│     └── Module.setStatus() → 解析下载进度                                │
│                                                                         │
│  6. Module.preRun                                                       │
│     └── triggerInitCallback() → UrhoX.onReady() 回调                    │
│                                                                         │
│  7. Module.postRun                                                      │
│     └── 隐藏加载界面，C++ Bootstrap 处理项目资源                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 时序图

```
浏览器                    project-index.js              CDN
  │                             │                        │
  │  DOMContentLoaded           │                        │
  │ ─────────────────────────▶  │                        │
  │                             │  fetch project.json    │
  │                             │ ─────────────────────▶ │
  │                             │ ◀───────────────────── │
  │                             │                        │
  │                             │  fetch latest.json     │
  │                             │ ─────────────────────▶ │
  │                             │ ◀───────────────────── │
  │                             │                        │
  │                             │  fetch engine-*.json   │
  │                             │ ─────────────────────▶ │
  │                             │ ◀───────────────────── │
  │                             │                        │
  │                             │  fetch manifest-*.json │
  │                             │ ─────────────────────▶ │
  │                             │ ◀───────────────────── │
  │                             │                        │
  │                             │  buildFileMap()        │
  │                             │ ──────────┐            │
  │                             │ ◀─────────┘            │
  │                             │                        │
  │  <script> UrhoXRuntime.js   │                        │
  │ ◀───────────────────────────│                        │
  │                             │                        │
  │  Module.locateFile()        │                        │
  │ ─────────────────────────▶  │  return CDN URL        │
  │ ◀───────────────────────────│                        │
  │                             │                        │
  │  fetch .wasm/.data          │                        │
  │ ─────────────────────────────────────────────────▶   │
  │ ◀───────────────────────────────────────────────── │
  │                             │                        │
  │  Module.preRun              │                        │
  │ ─────────────────────────▶  │  triggerInitCallback   │
  │                             │                        │
  │  Module.postRun             │                        │
  │ ─────────────────────────▶  │  游戏启动               │
```

---

## 核心组件

### 文件映射表（fileMap）

从 manifest 构建 `fs_path → CDN URL` 的映射：

```javascript
const fileMap = new Map();  // fs_path -> CDN URL
let engineJsUrl = null;     // UrhoXRuntime.js 的 CDN URL

function buildFileMap(files, baseUrl) {
  for (const f of files) {
    // 格式: {uuid}-{hash}{ext}  (ext 已包含点，如 ".png")
    if (f.fs_path && f.uuid && f.hash && f.ext) {
      const cdnUrl = baseUrl + f.uuid + '-' + f.hash + f.ext;
      fileMap.set(f.fs_path, cdnUrl);
      
      // 记录引擎 JS 的 URL
      if (f.fs_path === 'UrhoXRuntime.js') {
        engineJsUrl = cdnUrl;
      }
    }
  }
}
```

### 引擎加载（loadEngine）

从 fileMap 获取 `UrhoXRuntime.js` 的 CDN URL，动态插入 `<script>` 加载：

```javascript
function loadEngine() {
  // 优先使用 manifest 中的 CDN URL，否则用本地
  const jsUrl = engineJsUrl || 'UrhoXRuntime.js';
  
  updateStatus('Loading engine...');
  
  const s = document.createElement('script');
  s.src = jsUrl;
  s.onload = () => log('✓ Engine loaded');
  s.onerror = () => updateStatus('Engine failed');
  document.body.appendChild(s);
}
```

**加载顺序**：
1. `UrhoXRuntime.js` 加载完成
2. Emscripten 初始化，调用 `Module.locateFile()` 获取 `.wasm` / `.data` 路径
3. 下载 `UrhoXRuntime.wasm`（WebAssembly 二进制，~6MB）
4. 下载 `UrhoXRuntime.data`（Emscripten 数据包，~18MB）
5. 编译 WebAssembly，挂载虚拟文件系统
6. 触发 `Module.preRun` → `Module.postRun`

### Module Hook（关键！）

`window.Module` 必须在 `UrhoXRuntime.js` 加载**之前**定义，Emscripten 会读取这些 hook：

```javascript
window.Module = {
  // ========== 生命周期 ==========
  preRun: [function() {
    // WASM 编译完成，虚拟 FS 已挂载，游戏即将启动
    triggerInitCallback({ success: true, versionInfo, message: 'Ready' });
  }],
  
  postRun: [function() {
    // 游戏已启动
    updateStatus('Running');
    const screen = document.getElementById('loading-screen');
    if (screen) screen.classList.add('hidden');
  }],
  
  // ========== 资源重定向（核心）==========
  // Emscripten 加载 .wasm/.data 时调用此函数获取 URL
  locateFile: function(path, prefix) {
    // 从 fileMap 查找 CDN URL
    const cdnUrl = fileMap.get(path);
    if (cdnUrl) {
      logV('locateFile:', path, '->', cdnUrl);
      return cdnUrl;
    }
    // 未找到则使用默认路径
    return prefix + path;
  },
  
  // ========== 进度回调 ==========
  // Emscripten 下载进度通知
  setStatus: function(text) {
    if (!text) return;
    
    // 解析 Emscripten 进度: "Downloading data... (X/Y)"
    const m = text.match(/\((\d+)\/(\d+)\)/);
    if (m) {
      const current = parseInt(m[1], 10);
      const total = parseInt(m[2], 10);
      if (total > 0) {
        updateProgress((current / total) * 100);
      }
    }
    
    if (text.includes('Downloading')) {
      updateStatus('Downloading...');
    }
  },
  
  // ========== 其他 ==========
  print: text => console.log(text),
  printErr: text => console.error(text),
  
  canvas: document.getElementById('canvas')
};
```

**关键点**：
- `locateFile` 是实现 CDN 加载的核心，将 `.wasm` / `.data` 重定向到 manifest 中的 CDN URL
- `setStatus` 用于解析 Emscripten 的下载进度文本
- `preRun` / `postRun` 是生命周期 hook，用于初始化回调和隐藏加载界面

### UrhoX 命名空间

```javascript
window.UrhoX = {
  // 获取版本信息
  getVersionInfo: () => window.__ENGINE_BUILD_INFO__ || null,
  
  // 引擎就绪回调
  onReady: function(callback) { ... },
  
  // 是否为 Tapcode 环境
  isTapcode: () => true,
  
  // 获取当前页面 URL
  getTapcodeUrl: () => location.origin + location.pathname.replace(/[^/]*$/, ''),
  
  // 获取项目 ID
  getTapcodeGameID: () => tapcodeGameID
};
```

---

## 进度更新

### 进度来源

| 阶段 | 进度来源 | 说明 |
|------|---------|------|
| Manifest 加载 | 无进度 | 文件小，直接显示 "Loading..." |
| 引擎加载 | 无进度 | 显示 "Loading engine..." |
| .wasm/.data 下载 | Module.setStatus | 解析 Emscripten 输出 |

### 进度解析

Emscripten 输出格式：`"Downloading data... (12345/67890)"`

```javascript
setStatus: function(text) {
  // 解析 Emscripten 进度: "Downloading data... (X/Y)"
  const m = text.match(/\((\d+)\/(\d+)\)/);
  if (m) {
    const current = parseInt(m[1], 10);
    const total = parseInt(m[2], 10);
    if (total > 0) {
      updateProgress((current / total) * 100);
    }
  }
  
  if (text.includes('Downloading')) {
    updateStatus('Downloading...');
  }
}
```

### UI 更新

```javascript
function updateProgress(percent) {
  const bar = document.getElementById('loading-progress-bar');
  if (bar) bar.style.width = percent + '%';
  
  const txt = document.getElementById('loading-percent');
  if (txt) txt.textContent = Math.floor(percent) + '%';
}

function updateStatus(text) {
  const el = document.getElementById('loading-status');
  if (el) el.textContent = text;
}
```

---

## 智能缓存策略

### 问题

- 动态文件（`latest.json`）需要加时间戳防缓存
- 版本化文件（`manifest-abc123.json`）不需要，文件名已含 hash

### 解决方案

`fetchJson()` 根据文件名自动判断：

```javascript
async function fetchJson(url, noCache = false) {
  // 检测文件名是否包含 hash：/-[a-f0-9]{8,}\./i
  const hasHash = /-[a-f0-9]{8,}\./i.test(url);
  
  let fetchUrl = url;
  if (noCache || !hasHash) {
    // 需要加时间戳防缓存
    fetchUrl = url + (url.includes('?') ? '&' : '?') + 'v=' + (Date.now() / 1000 | 0);
  }
  
  const r = await fetch(fetchUrl);
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${url}`);
  return r.json();
}
```

### 缓存行为

| 文件类型 | 示例 | 加时间戳 |
|---------|------|---------|
| 动态文件 | `latest.json`, `project.json`, `version.json` | ✅ 是 |
| 版本化文件 | `manifest-a1b2c3d4.json`, `engine-abc123.json` | ❌ 否 |
| CDN 资源 | `{uuid}-{hash}.png` | ❌ 否（通过 fileMap 访问）|

---

## 远程加载（game_url）

### 用法

```
index.html?game_url=https://cdn.example.com/games/my-game/
```

### 行为

1. 优先从 `game_url` 加载 `latest.json` 和 `project.json`
2. 若未指定，使用本地文件（开发模式）
3. 自动补全末尾斜杠

### 实现

```javascript
const urlParams = new URLSearchParams(location.search);

// 解析 game_url 参数
let gameUrl = urlParams.get('game_url') || '';
if (gameUrl && !gameUrl.endsWith('/')) gameUrl += '/';

// 加载时优先使用 game_url
const latestUrl = gameUrl ? gameUrl + 'latest.json' : 'latest.json';
const projectUrl = gameUrl ? gameUrl + 'project.json' : 'project.json';
```

### 典型场景

| 场景 | URL | 说明 |
|------|-----|------|
| 本地开发 | `index.html` | 使用本地文件 |
| 远程加载 | `index.html?game_url=https://cdn/game/` | 加载 CDN 上的项目 |
| 调试模式 | `index.html?verbose=true` | 显示详细日志 |

---

## 构建打包

### gen_wasm_agent.py

`bundle_javascript()` 函数将多个 JS 文件打包为 `index.js`：

```
打包顺序：
1. project-index.js        - 主加载器
2. web_audio_unlock.js     - 音频解锁
3. floating_action_button.js - 浮动按钮
4. error_clipboard.js      - 错误复制
5. postmessage_bridge.js   - PostMessage 桥接
6. user_script_loader.js   - 用户脚本加载
         ↓
      index.js (打包输出)
```

### 模板替换

构建后 `index.html` 中的脚本引用自动替换：

```
project-index.js  →  index.js
```

### 构建命令

```bash
# 完整构建
python tools/generators/gen_wasm_agent.py

# 查看详细输出
python tools/generators/gen_wasm_agent.py --verbose
```

---

## API 参考

### UrhoX.getVersionInfo()

获取引擎构建信息：

```javascript
const info = UrhoX.getVersionInfo();
// 返回: { binary_hash, commit_hash, branch, timestamp } 或 null
```

### UrhoX.onReady(callback)

注册引擎就绪回调：

```javascript
UrhoX.onReady(function(result) {
  if (result.success) {
    console.log('Engine ready:', result.versionInfo);
  } else {
    console.error('Engine failed:', result.error);
  }
});
```

### UrhoX.getTapcodeGameID()

获取当前项目 ID：

```javascript
const gameId = UrhoX.getTapcodeGameID();
// 返回: "p_xxxx" 或空字符串
```

### UrhoX.getTapcodeUrl()

获取当前页面基础 URL：

```javascript
const baseUrl = UrhoX.getTapcodeUrl();
// 返回: "https://example.com/games/my-game/"
```

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [native-bootstrap-loader.md](./native-bootstrap-loader.md) | 原生平台启动加载器 |
| [INDEX.md](./INDEX.md) | 项目构建流程 |
| [project-builder.md](./project-builder.md) | 构建工具实现 |

---

*最后更新: 2025-12-17*

