---
summary: "WebAssembly source map debug configuration for local development and remote site debugging"
last_updated: "2026-04-02"
---

# WebAssembly Source Map 调试配置

## 概述

本配置支持以下场景：
1. ✅ **本地开发调试**：通过本地服务器测试
2. ✅ **远程站点调试**：访问部署在远程服务器的 WASM，但使用本地源码
3. ✅ **安全可控**：正式环境不部署 `.map` 文件即可禁用调试
4. ✅ **独立 Source Map**：`.wasm.map` 与 `.wasm` 分离，可选择性部署

## 核心原理

### 编译产物
```
build_agent_wasm/bin/
  ├── Urho3DPlayer.wasm     # 生产构建，无调试信息（~8 MB）
  └── Urho3DPlayer.wasm.map # Source map，映射到源码路径（~2 MB）
```

### Source Map 工作流程
1. 浏览器加载 `.wasm` 文件
2. 检测到 `sourceMappingURL` 注释，加载 `.wasm.map`
3. Source map 包含源码文件路径（相对路径）
4. 浏览器尝试从这些路径加载源码
5. **通过浏览器配置，将路径重定向到本地文件系统**

## 场景1：本地开发调试

### 步骤
1. **编译 WASM**（带调试信息）：
   ```batch
   cd tools\generators
   gen_wasm_agent.bat        # 使用 -g 标志，内嵌调试信息
   cd ..\..\build_agent_wasm
   mingw32-make Urho3DPlayer -j8
   ```

2. **启动本地服务器**：
   ```batch
   cd tools
   run_wasm_server.bat
   ```

3. **打开浏览器调试**：
   - 访问 `http://localhost:8000/Urho3DPlayer.html`
   - 打开 DevTools (F12)
   - 堆栈跟踪会显示函数名和文件位置
   - **注意**：在 localhost 上，Workspace 功能受限，但基本的调试符号（函数名、行号）依然可用

### 优点
- ✅ 零配置，开箱即用
- ✅ 函数名和行号都可见
- ✅ WASM 文件较大（~15 MB），但仅用于本地开发

## 场景2：远程站点调试（核心功能）

当您的 WASM 部署在远程服务器（如 `https://cdn.example.com/`）时，通过浏览器配置将 source map 中的源码路径映射到**本地文件系统**。

> **⚠️ 重要提示**：Chrome DevTools 的 Workspace 功能**仅在远程站点（https://）上有效**，在 `localhost` 上由于安全限制无法使用。这正好符合您的使用场景。

### Chrome/Edge 配置步骤

1. **打开远程站点**：
   - 访问 `https://cdn.example.com/Urho3DPlayer.html`（必须是远程服务器，不能是 localhost）
   - 打开 DevTools (F12)

2. **配置 Filesystem Workspace**：
   - 打开 DevTools → **Sources** 面板
   - 左侧面板中选择 **Filesystem** 选项卡
   - 点击 **+ Add folder to workspace**
   - 选择您的项目源码根目录：`G:\Workspace\SCE\NE\UrhoX\engine\Source`
   - 浏览器会请求访问权限，点击 **Allow**

3. **建立路径映射**（自动或手动）：
   
   **自动映射**（如果路径结构匹配）：
   - Chrome 会自动检测 source map 中的路径
   - 如果相对路径匹配，会自动关联本地文件
   
   **手动映射**（如果路径不匹配）：
   - 在 **Sources** 面板的 **Page** 选项卡中找到一个源文件
   - 右键点击文件 → 选择 **"Map to file system resource..."**
   - 从弹出的列表中选择对应的本地文件
   - Chrome 会记住这个映射关系，并自动映射相同目录下的其他文件

4. **验证映射**：
   - 触发一个错误或断点
   - 堆栈跟踪中应该显示本地文件路径
   - 点击可以直接查看本地源码

### Firefox 配置步骤

Firefox 不支持 workspace，但可以使用**浏览器扩展**：

1. **安装扩展**：[Source Map Switcher](https://addons.mozilla.org/firefox/addon/source-map-switcher/)
2. **配置映射规则**：
   ```
   https://cdn.example.com/engine/Source/* → file:///G:/Workspace/SCE/NE/UrhoX/engine/Source/*
   ```

### 工作原理

```
远程站点：
  https://cdn.example.com/Urho3DPlayer.html
  https://cdn.example.com/Urho3DPlayer.wasm
  https://cdn.example.com/Urho3DPlayer.wasm.map  ← 开发者下载此文件

Source Map 内容：
  {
    "sources": [
      "../../engine/Source/Urho3D/Core/Object.cpp",
      "../../engine/Source/Urho3D/Benchmark/BulletBenchmark.cpp"
    ]
  }

浏览器行为：
  1. 读取 source map
  2. 尝试加载 "../../engine/Source/Urho3D/Core/Object.cpp"
  3. ❌ 404 (远程服务器上没有这个文件)
  4. ✅ Workspace 重定向 → file:///G:/Workspace/.../Object.cpp
  5. ✅ 显示本地源码
```

## 场景3：正式环境部署

### 构建生产版本

**使用专用的 Release 构建脚本**（推荐）：
```batch
cd tools\generators
gen_wasm_agent_release.bat    # 无调试信息，最小体积
cd ..\..\build_agent_wasm_release
mingw32-make Urho3DPlayer -j8
```

这会生成：
- **Urho3DPlayer.wasm** - 优化后的生产版本（~8 MB）
- **没有** `.wasm.map` 文件
- **没有** 调试符号

### 部署清单

**正式环境（用户访问）**：
```
deploy/
  ├── Urho3DPlayer.html     ✅ 部署
  ├── Urho3DPlayer.js       ✅ 部署
  ├── Urho3DPlayer.wasm     ✅ 部署（Release版本，~8 MB）
  └── Urho3DPlayer.data     ✅ 部署
```

**如果需要调试生产环境问题**：
1. 使用 `gen_wasm_agent.bat` 重新编译（带 `-g` 调试信息）
2. 将编译出的 `.wasm` 文件仅提供给开发者
3. 开发者访问远程站点时，通过浏览器扩展替换 `.wasm` 文件为调试版本

### 加载 Source Map 的方式

#### 方式1：手动添加（推荐）
1. 从开发者调试包下载 `.wasm.map`
2. 在 Chrome DevTools 中：
   - **Sources** 面板 → 右键点击 `Urho3DPlayer.wasm`
   - 选择 **"Add source map..."**
   - 选择下载的 `.wasm.map` 文件

#### 方式2：浏览器扩展重定向
使用浏览器扩展拦截 `.wasm.map` 请求，重定向到本地文件。

#### 方式3：本地代理服务器
使用如 Charles、Fiddler 等工具，拦截 `.wasm.map` 请求并返回本地文件。

## 对比：不同构建配置

| 构建脚本 | 调试信息 | WASM 大小 | localhost 调试 | 远程调试 | 适用场景 |
|---------|---------|----------|---------------|---------|---------|
| `gen_wasm_agent.bat` | `-g` 内嵌 | ~15 MB | ✅ 函数名+行号 | ✅ 完整源码* | 本地开发 |
| `gen_wasm_agent_release.bat` | 无 | ~8 MB | ❌ 仅地址 | ❌ | 正式生产 |

\* 远程调试需要配置 Chrome DevTools Workspace

## 使用建议

### 本地开发
```batch
# 使用本地服务器，source map 自动工作
run_wasm_server.bat
```

### 测试/预发布环境
- 部署 `.wasm.map` 文件
- 开发者可以直接调试
- 使用 DevTools Workspace 映射本地源码

### 正式生产环境
- **不部署** `.wasm.map` 文件
- 或者只允许授权 IP 访问 `.wasm.map`（通过 CDN/服务器配置）

## 高级：动态 Source Map

如果需要为不同环境生成不同的 source map：

### 本地开发版
```batch
-sSOURCE_MAP_BASE='http://localhost:8000/'
```

### 远程调试版（不推荐）
```batch
-sSOURCE_MAP_BASE='https://source.example.com/'
```
然后在 `source.example.com` 上部署源码（**安全风险！**）

### 推荐：使用相对路径（当前配置）
```batch
# 不指定 SOURCE_MAP_BASE，使用相对路径
-gsource-map
```
让浏览器的 Workspace 功能自动处理映射。

## 故障排除

### 问题：Source map 未加载
**症状**：堆栈跟踪中没有源码信息

**解决**：
1. 检查 `.wasm` 文件末尾是否有：
   ```
   //# sourceMappingURL=Urho3DPlayer.wasm.map
   ```
2. 手动添加 source map（DevTools → Add source map）

### 问题：Source map 加载了但看不到源码
**症状**：堆栈显示文件名和行号，但点击后空白

**解决**：
1. **配置 Workspace**（见上文）
2. 或者使用本地服务器提供源码（见场景1）

### 问题：路径映射不正确
**症状**：Workspace 找不到对应的源文件

**解决**：
1. 查看 `.wasm.map` 中的 `sources` 字段：
   ```bash
   type build_agent_wasm\bin\Urho3DPlayer.wasm.map | findstr "sources"
   ```
2. 确保 Workspace 添加的目录包含这些路径
3. 使用 "Map to file system resource" 手动建立映射

## 浏览器支持

| 浏览器 | Workspace | Local Overrides | Source Map |
|--------|-----------|-----------------|------------|
| Chrome | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Firefox | ❌ (需扩展) | ❌ | ✅ |
| Safari | ⚠️ (有限) | ❌ | ✅ |

推荐使用 **Chrome 或 Edge** 进行 WASM 调试。

## 参考资料

- [Chrome DevTools: Map Preprocessed Code to Source Code](https://developer.chrome.com/docs/devtools/javascript/source-maps/)
- [Chrome DevTools: Edit files with Workspaces](https://developer.chrome.com/docs/devtools/workspaces/)
- [Emscripten Source Maps Documentation](https://emscripten.org/docs/debugging/Source-Maps.html)
- [WebAssembly Debugging Guide](https://developer.chrome.com/blog/wasm-debugging-2020/)
