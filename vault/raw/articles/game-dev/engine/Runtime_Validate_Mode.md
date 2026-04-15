# UrhoXRuntime -validate 模式

## 概述

`-validate` 模式让 UrhoXRuntime 在无 GPU/显示器的 Linux 服务器上以无头方式运行游戏项目，自动收集运行时错误并生成 JSON 报告。主要用于 **urhox-bench** 自动化评估 AI 生成的游戏项目。

### 验证范围

| 维度 | 检测内容 |
|------|----------|
| Lua 脚本错误 | 语法错误、运行时异常、API 调用错误 |
| 资源加载 | 缺失的纹理、模型、音效等资源文件 |
| 引擎错误 | 子系统初始化失败、组件创建错误 |
| 场景状态 | Scene 是否创建、节点/组件数量 |

### 工作原理

```
启动 → Bootstrap(Login/Ready) → 加载脚本 → 运行 N 帧 → 查询 Scene → 输出报告 → 退出
         (skip_login)           Load阶段     Run阶段      Scene阶段
```

使用 `EP_GRAPHICS_HEADLESS` 模式 + BGFX NOOP 渲染器：所有 Graphics/Renderer/UI 子系统正常创建，但不进行实际渲染。客户端 API 完全可用，无需 GPU。

---

## 构建

### 前置依赖

```bash
# Ubuntu/Debian
sudo apt install cmake ninja-build clang libssl-dev libx11-dev libgl-dev libasound2-dev
```

### 使用 gen_runtime.py 构建

```bash
cd /path/to/UrhoX

# 配置（validate 模式，Release）
python3 tools/generators/gen_runtime.py --validate --release

# 构建
cd build_validate
ninja UrhoXRuntime -j$(nproc)
```

构建产物：`build_validate/bin/UrhoXRuntime`

### gen_runtime.py 参数

| 参数 | 说明 |
|------|------|
| `--validate` | 无头验证构建（NOOP 渲染器，无 GPU 依赖） |
| `--release` | Release 优化构建 |
| `--build-dir <dir>` | 自定义构建目录（默认 `build_validate`） |
| `--ci` | CI 模式（跳过符号链接，使用 CMake 资源路径） |
| `--verbose` | 显示详细 CMake 参数 |

### validate 构建与正常客户端构建的区别

| CMake 选项 | validate | 正常客户端 |
|------------|----------|------------|
| `BGFX_RENDERER_NOOP` | 1 (无渲染) | 0 (真实渲染) |
| `FREETYPE` | 1 | 1 |
| `NAVIGATION` | 1 | 1 |
| `IK` | 0 | 1 |
| `REDIS` | 0 | 1 |
| `WEBSOCKET` | 0 | 1 |

---

## 使用

### 基本用法

```bash
./bin/UrhoXRuntime main.lua \
    -graphicsheadless \
    -validate \
    -skip_login \
    -validate-frames=60 \
    -validate-timeout=30 \
    -validate-output=report.json \
    -tapcode_dir=/path/to/project
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-graphicsheadless` | 启用无头图形模式（NOOP 渲染器） | — |
| `-validate` | 启用验证模式 | — |
| `-skip_login` | 跳过登录流程 | — |
| `-validate-frames=N` | 运行帧数 | 60 |
| `-validate-timeout=N` | 超时秒数 | 30 |
| `-validate-output=path` | JSON 报告输出路径（不指定则 stdout） | stdout |
| `-tapcode_dir=path` | 游戏项目根目录（脚本在 `scripts/` 子目录下） | — |

### 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | PASS — 无错误 |
| 1 | FAIL — 有运行时错误 |

### 项目目录结构

`-tapcode_dir` 指向的目录需要如下结构：

```
project/
├── scripts/
│   ├── main.lua      # 入口脚本
│   ├── game.lua
│   └── ...
└── assets/           # 资源文件（可选）
    ├── Textures/
    ├── Models/
    └── ...
```

---

## JSON 报告格式

```json
{
    "version": 1,
    "script": "main.lua",
    "result": "PASS | FAIL | TIMEOUT",
    "duration_ms": 1234,
    "frames_completed": 60,
    "phases": {
        "load": {
            "result": "PASS | FAIL",
            "errors": [
                {
                    "category": "lua | resource | engine",
                    "message": "错误详情",
                    "frame": 0
                }
            ]
        },
        "init": { "result": "PASS", "errors": [] },
        "run":  { "result": "PASS", "errors": [] },
        "scene": {
            "result": "PASS",
            "errors": [],
            "node_count": 5,
            "component_count": 8,
            "scene_exists": true
        }
    },
    "missing_resources": [
        "Textures/Missing.png",
        "Models/Player.mdl"
    ],
    "summary": {
        "lua_errors": 0,
        "resource_errors": 2,
        "engine_errors": 0,
        "total_errors": 2
    }
}
```

### 验证阶段

| 阶段 | 时机 | 捕获内容 |
|------|------|----------|
| **load** | 脚本加载 + 前 1 帧 | 语法错误、模块缺失、初始资源加载失败 |
| **init** | 第 1 帧 | Start() 函数执行错误 |
| **run** | 第 2 帧 ~ 第 N 帧 | Update() 运行时错误、延迟加载资源失败 |
| **scene** | 运行结束后 | 查询全局 `scene` 变量的节点/组件数量 |

### 错误分类

| 分类 | 匹配规则 |
|------|----------|
| `resource` | 包含 "Could not find resource" / "Could not load" / "Failed to load resource" |
| `lua` | `customLog == "lua"` 或包含 "Lua" / "lua" |
| `engine` | 其他 ERROR 级别日志 |

### 过滤规则

以下错误在 validate 模式下被自动过滤（不计入报告）：
- Shader 编译错误（NOOP 渲染器不支持编译 shader，属于预期行为）

---

## 与 urhox-bench 集成

### 评估管线

urhox-bench 的评估流程为 L0 → L1 → L2：

| 层级 | 方式 | 说明 |
|------|------|------|
| **L0** | 文件检查 | main.lua 是否存在、目录结构是否正确 |
| **L1** | LuaLS 静态分析 | 语法检查、类型检查、未定义变量 |
| **L2** | UrhoXRuntime -validate | 运行时验证（本功能） |

L2 在 L0 通过后执行。L1 和 L2 可以并行运行。

### L2 评估器调用示例（TypeScript）

```typescript
import { spawn } from 'child_process';

const proc = spawn(runtimePath, [
    'main.lua',
    '-graphicsheadless',
    '-validate',
    '-skip_login',
    `-validate-frames=${frames}`,
    `-validate-timeout=${timeout}`,
    `-validate-output=${reportPath}`,
    `-tapcode_dir=${workspace}`,
], {
    cwd: path.dirname(runtimePath),
    timeout: (timeout + 5) * 1000,
});

// 等待退出，读取 reportPath 的 JSON
```

### 判定逻辑

```
exitCode == 0 && total_errors == 0  →  L2 PASS
exitCode == 1                       →  L2 FAIL（查看 phases 定位问题）
exitCode == 139 (SIGSEGV)           →  引擎崩溃（非脚本问题）
result == "TIMEOUT"                 →  脚本可能有死循环
```

### 报告解读示例

**场景 1：脚本语法错误**
```json
{
    "result": "FAIL",
    "phases": {
        "load": {
            "result": "FAIL",
            "errors": [{ "category": "lua", "message": "...unexpected symbol near '}'..." }]
        }
    }
}
```

**场景 2：资源缺失**
```json
{
    "result": "FAIL",
    "missing_resources": ["Textures/player.png", "Models/enemy.mdl"],
    "summary": { "resource_errors": 2 }
}
```

**场景 3：运行时逻辑错误**
```json
{
    "result": "FAIL",
    "phases": {
        "run": {
            "result": "FAIL",
            "errors": [{ "category": "lua", "message": "...attempt to index a nil value..." , "frame": 15 }]
        }
    }
}
```

**场景 4：完全通过**
```json
{
    "result": "PASS",
    "frames_completed": 60,
    "phases": {
        "scene": { "scene_exists": true, "node_count": 12, "component_count": 25 }
    },
    "summary": { "total_errors": 0 }
}
```

---

## 已知限制

1. **Shader 不编译** — NOOP 渲染器不编译 shader，依赖特定 shader 效果的逻辑无法验证
2. **无真实渲染输出** — 无法验证视觉正确性（颜色、布局、动画效果）
3. **音频设备** — 无声卡环境会输出 "Could not initialize audio output" 警告（已过滤）
4. **网络功能** — validate 模式不启动网络连接，联机游戏逻辑无法验证
5. **IK 未启用** — validate 构建未开启 IK 模块，使用 IK 的脚本会报错
