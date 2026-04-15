---
summary: "Unit testing guide covering both C++ (Google Test) and Lua test systems"
last_updated: "2026-03-05"
---

# UrhoX 单元测试指南

本文档汇总 UrhoX 项目的全部单元测试体系，包括 C++ 和 Lua 两套测试。

---

## 一、C++ 单元测试

**框架**: Google Test 1.10.0
**CMake 开关**: `-DURHO3D_TESTING=1`（默认 OFF）
**源码位置**: `engine/Tests/`

### 测试 Target

| Target | 路径 | 编译条件 | 内容 |
|--------|------|----------|------|
| `ServerTests` | `engine/Tests/Server/` | `URHO3D_TESTING && !EMSCRIPTEN` | 命令行解析、空闲超时、游戏设置、安全性、Bootstrap、AuthKey |
| `NetworkTests` | `engine/Tests/Network/` | `URHO3D_TESTING && URHO3D_NETWORK && !EMSCRIPTEN` | 连接、传输层集成、多协议、Mock Transport |
| `RedisTests` | `engine/Tests/Redis/` | `URHO3D_TESTING && URHO3D_REDIS && !EMSCRIPTEN` | Redis 消息、URI 解析、Manager、集成测试 |

### 本地构建和运行

```bash
# 方式 1: 使用 gen_server.py（推荐，自动配置所有依赖）
python tools/generators/gen_server.py --with-tests
cd build_server

# 编译（VS）
cmake --build . --target ServerTests --config Debug

# 编译（Linux/Ninja）
ninja ServerTests

# 运行
./bin/ServerTests

# 运行并输出 XML 报告
./bin/ServerTests --gtest_output=xml:test_results.xml

# 只跑某个测试
./bin/ServerTests --gtest_filter="CommandLineParserTests.*"

# 用 CTest
ctest -R ServerTests -V
```

```bash
# 方式 2: 手动 CMake（需自行传所有参数）
cmake ../engine -DURHO3D_TESTING=1 -DURHO3D_NETWORK=1 -DURHO3D_REDIS=1 ...
```

### 辅助脚本

- `engine/Tests/Server/run_tests.bat` — Windows 快速运行
- `engine/Tests/Server/run_tests.sh` — Linux 快速运行

### 测试文件清单

**ServerTests**:

| 文件 | 说明 |
|------|------|
| `CommandLineParserTests.cpp` | 命令行参数解析 |
| `ServerBootstrapTests.cpp` | ServerBootstrapManager |
| `MockBootstrapTests.cpp` | Bootstrap Pipeline 模拟 |
| `IdleTimeoutTests.cpp` | 空闲超时机制 |
| `GameSettingsTests.cpp` | 游戏设置解析 |
| `SafetyTests.cpp` | 安全性测试 |
| `AuthKeyTests.cpp` | AuthKey 认证 |
| `LogInitTests.cpp` | 日志初始化 |
| `ModeArgsTests.cpp` | 模式参数 |
| `LobbyConnectTests.cpp` | Lobby 连接 |
| `LoadVersionStepTests.cpp` | 版本加载步骤 |
| `SettingsJsonIntegrationTest.cpp` | 设置 JSON 集成测试 |

**NetworkTests**:

| 文件 | 说明 |
|------|------|
| `ConnectionTests.cpp` | 连接测试 |
| `NetworkClassTests.cpp` | 网络类测试 |
| `TransportIntegrationTests.cpp` | 传输层集成 |
| `MultiProtocolTests.cpp` | 多协议 |
| `MockTransport.cpp/h` | Mock 传输层 |

**RedisTests**:

| 文件 | 说明 |
|------|------|
| `RedisMessageTests.cpp` | 消息序列化 |
| `RedisUriParsingTests.cpp` | URI 解析 |
| `RedisManagerTests.cpp` | Manager 逻辑 |
| `RedisIntegrationTests.cpp` | 集成测试 |
| `RedisProbeTest.cpp` | 连接探测 |

### CMake 配置参考

```cmake
# engine/CMakeLists.txt 中的测试配置
option (URHO3D_TESTING "Build unit tests" OFF)
if (URHO3D_TESTING)
    enable_testing ()
    add_subdirectory (3rd/googletest)
endif ()

if (URHO3D_TESTING AND URHO3D_NETWORK AND NOT EMSCRIPTEN)
    add_subdirectory (Tests/Network)
endif ()
if (URHO3D_TESTING AND NOT EMSCRIPTEN)
    add_subdirectory (Tests/Server)
endif ()
if (URHO3D_TESTING AND URHO3D_REDIS AND NOT EMSCRIPTEN)
    add_subdirectory (Tests/Redis)
endif ()
```

### 编写新的 C++ 测试

1. 在 `engine/Tests/<模块>/` 下新建 `XxxTests.cpp`
2. CMake 自动 GLOB，无需手动添加源文件
3. 使用 Google Test 宏：

```cpp
#include <gtest/gtest.h>

TEST(MyFeatureTests, ShouldDoSomething)
{
    EXPECT_EQ(1 + 1, 2);
}
```

---

## 二、Lua 单元测试

**框架**: LuaUnit（内置于 `urhox-libs/Testing/luaunit`）
**入口程序**: `UrhoXRuntime.exe`

### 两套测试集

#### 1. 引擎 API 测试

- **入口**: `engine/bin/Data/LuaScripts/Tests/run_tests.lua`
- **运行**: `UrhoXRuntime.exe LuaScripts/Tests/run_tests.lua`
- **测试需手动注册**（在 `run_tests.lua` 中 require）

| 文件 | 说明 |
|------|------|
| `test_basic_api.lua` | 基础引擎 API |
| `test_hand_picked_games.lua` | 手工游戏验证 |
| `test_authkey.lua` | AuthKey 认证 |
| `test_variant_map.lua` | VariantMap Set/Get API |
| `test_json_api.lua` | JSON API |
| `test_isolation.lua` | 文件沙箱隔离（必须最后加载） |

#### 2. urhox-libs UI 组件测试

- **入口**: `engine/bin/Data/urhox-libs/Testing/Tests/run_tests.lua`
- **特性**: 自动发现 `test_*.lua` 文件，无需手动注册
- **两种运行模式**:

```bash
# 可视模式 — 显示 UI 结果面板
UrhoXRuntime.exe urhox-libs/Testing/Tests/run_tests.lua

# Headless/CI 模式 — 控制台输出，返回退出码（0=pass, 1=fail）
UrhoXRuntime.exe urhox-libs/Testing/Tests/run_tests.lua -headless
```

| 文件 | 说明 |
|------|------|
| `test_ButtonGroupDropdown.lua` | ButtonGroup + Dropdown |
| `test_ScrollView_StickyAndFlexShrink.lua` | ScrollView 吸附和收缩 |
| `test_OverflowScroll_MaxHeightAutoFix.lua` | 溢出滚动自动修复 |
| `test_PaddingTable_ScissorLeak.lua` | Padding 裁剪泄漏 |
| `test_VirtualButton.lua` | VirtualButton |
| `test_WidgetPropertyRouting.lua` | Widget 属性路由 |
| `test_WidgetsGallery.lua` | Widget 画廊 |

### 编写新的 Lua 测试

**引擎 API 测试**:
1. 在 `engine/bin/Data/LuaScripts/Tests/` 下新建 `test_xxx.lua`
2. 在 `run_tests.lua` 中添加 `require "LuaScripts.Tests.test_xxx"`

**urhox-libs 测试**（推荐，自动发现）:
1. 在 `engine/bin/Data/urhox-libs/Testing/Tests/` 下新建 `test_Xxx.lua`
2. 文件名匹配 `test_*.lua` 即可，无需额外注册

```lua
local lu = require("urhox-libs/Testing/luaunit")

TestMyFeature = {}

function TestMyFeature:test_should_do_something()
    lu.assertEquals(1 + 1, 2)
end

function TestMyFeature:test_should_handle_edge_case()
    lu.assertNotNil(scene)
end
```

---

## 三、CI/CD 自动化

### GitHub Workflow

**文件**: `.github/workflows/server-tests.yml`

| 项目 | 说明 |
|------|------|
| 触发条件 | PR 创建/更新、push 到 main、手动触发 |
| 运行环境 | 自托管 runner（`urhox-self-hosted`），Docker 容器 |
| 构建工具 | Ninja + ccache |
| 测试目标 | `ServerTests`（C++） |
| 产物 | `test_results.xml`（JUnit 格式） |
| 失败通知 | PR 自动评论 + Step Summary |

**排除路径**: `*.md`, `docs/**`, `engine/bin/Data/**`, `tools/**` 等变更不触发。

### CI 当前覆盖

- C++ `ServerTests` — 已集成
- C++ `NetworkTests` — 未集成（需 network 环境）
- C++ `RedisTests` — 未集成（需 Redis 服务）
- Lua 引擎 API 测试 — 未集成
- Lua urhox-libs 测试 — 未集成

---

## 四、快速命令速查

```bash
# === C++ 测试 ===

# 生成带测试的服务端构建
python tools/generators/gen_server.py --with-tests

# 编译 ServerTests（VS）
cmake --build build_server --target ServerTests --config Debug

# 运行全部 ServerTests
./build_server/bin/ServerTests

# 运行指定测试
./build_server/bin/ServerTests --gtest_filter="IdleTimeout*"

# === Lua 测试 ===

# 引擎 API 测试（可视模式）
UrhoXRuntime.exe LuaScripts/Tests/run_tests.lua

# urhox-libs 测试（可视模式）
UrhoXRuntime.exe urhox-libs/Testing/Tests/run_tests.lua

# urhox-libs 测试（headless，适合 CI）
UrhoXRuntime.exe urhox-libs/Testing/Tests/run_tests.lua -headless
```

---

*最后更新: 2026-03-05*
