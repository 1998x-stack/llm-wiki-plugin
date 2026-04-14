---
summary: "Testing guide for verifying WebAssembly SIMD correctness and performance improvements"
last_updated: "2026-04-02"
---

# WebAssembly SIMD 测试指南

## 🎯 测试目标

本次测试旨在验证 WebAssembly SIMD 支持的正确性和性能提升效果。

---

## 📋 测试前准备

### 1. 拉取测试分支

```bash
git fetch origin
git checkout feature/wasm-simd-support
```

### 2. 环境要求

#### **必需环境**:
- ✅ Emscripten SDK 2.0.0+ ([安装指南](https://emscripten.org/docs/getting_started/downloads.html))
- ✅ CMake 3.10+
- ✅ MinGW (Windows) 或 GCC/Clang (Linux/Mac)
- ✅ 现代浏览器（见下方兼容性表）

#### **浏览器兼容性**:
| 浏览器 | 最低版本 | 推荐版本 |
|--------|----------|----------|
| Chrome | 91+ | 最新版 |
| Firefox | 89+ | 最新版 |
| Safari | 16.4+ | 最新版 |
| Edge | 91+ | 最新版 |

### 3. 验证 Emscripten 版本

```bash
emcc --version
# 应显示 2.0.0 或更高版本
```

---

## 🔨 构建测试

### Step 1: 清理之前的构建（可选）

```bash
# 如果之前有构建过 WASM，建议清理
rm -rf build_agent_wasm
```

### Step 2: 运行构建脚本

```bash
cd C:\Dev\taptap\UrhoX
tools\generators\gen_wasm_agent.bat
```

**预期输出**:
```
...
-- WebAssembly SIMD enabled (-msimd128)
...
-- Configuring done
-- Generating done
```

### Step 3: 编译

```bash
cd build_agent_wasm
mingw32-make Urho3DPlayer -j16
```

**预期结果**:
- 编译成功，无错误
- 生成文件: `bin/Urho3DPlayer.js`, `bin/Urho3DPlayer.wasm`, `bin/Urho3DPlayer.data`

### Step 4: 验证 SIMD 指令存在

```bash
# 检查 .wasm 文件中是否包含 SIMD 指令
wasm-objdump -d bin/Urho3DPlayer.wasm | grep "v128" | head -10
```

**预期输出**: 应该看到类似 `v128.load`, `f32x4.mul` 等 SIMD 指令

---

## 🚀 运行时测试

### Step 1: 启动本地服务器

```bash
cd C:\Dev\taptap\UrhoX
tools\run_wasm_server.bat
```

**预期输出**:
```
Starting WebAssembly server on http://localhost:8000
Server is running...
```

### Step 2: 在浏览器中打开

打开浏览器访问: `http://localhost:8000/Urho3DPlayer.html`

### Step 3: 检查浏览器控制台

**按 F12 打开开发者工具**，查看 Console 输出：

✅ **成功标志**:
```
WebAssembly SIMD enabled
Bullet Physics initialized with SIMD
```

❌ **失败标志**:
```
Error: WebAssembly.instantiate(): Compiling function #xxx:
       invalid SIMD operation
```

---

## 📊 性能测试

### 测试场景 1: 物理引擎密集场景

#### 测试步骤:
1. 在应用中创建一个包含大量刚体的物理场景
2. 记录 FPS 和物理更新时间

#### 对比测试:
```bash
# 构建无 SIMD 版本（对照组）
# 编辑 tools/generators/gen_wasm_agent.bat，删除 -DURHO3D_SSE=1
# 重新构建并测试

# 构建有 SIMD 版本（实验组）
# 使用原始配置构建并测试
```

#### 预期结果:
- **FPS 提升**: 15-30%（取决于场景复杂度）
- **物理更新时间**: 减少 20-40%

### 测试场景 2: 向量/矩阵运算

创建测试脚本（Lua）:

```lua
-- 测试向量运算性能
local start_time = GetTimeStamp()
local result = Vector3(0, 0, 0)

for i = 1, 100000 do
    local v1 = Vector3(i, i+1, i+2)
    local v2 = Vector3(i*2, i*3, i*4)
    result = result + v1:CrossProduct(v2)
end

local elapsed = GetTimeStamp() - start_time
print("Vector operations time: " .. elapsed .. "ms")
```

#### 预期结果:
- **SIMD 版本**: 约 50-100ms
- **非 SIMD 版本**: 约 80-150ms
- **性能提升**: 20-35%

---

## ✅ 测试检查清单

### 构建阶段
- [ ] CMake 配置输出包含 "WebAssembly SIMD enabled"
- [ ] 编译无错误
- [ ] 生成的 .wasm 文件包含 SIMD 指令（使用 wasm-objdump 验证）

### 运行时测试
- [ ] 在 Chrome 中正常运行
- [ ] 在 Firefox 中正常运行
- [ ] 在 Safari 中正常运行（如果有 Mac）
- [ ] 浏览器控制台无 SIMD 相关错误

### 性能测试
- [ ] 物理场景 FPS 提升明显
- [ ] 向量运算速度提升明显
- [ ] 无明显性能回退或异常

### 兼容性测试
- [ ] 在不支持 SIMD 的旧浏览器中给出友好错误提示
- [ ] 文件大小增长在可接受范围（< 5%）

---

## 🐛 已知问题和解决方案

### Issue 1: "unknown option -msimd128"

**原因**: Emscripten 版本过低

**解决方案**:
```bash
emsdk install latest
emsdk activate latest
source ./emsdk_env.sh  # Linux/Mac
emsdk_env.bat          # Windows
```

### Issue 2: 浏览器报 "invalid SIMD operation"

**原因**: 浏览器不支持 WebAssembly SIMD

**解决方案**:
- 更新浏览器到最新版本
- 或使用支持 SIMD 的浏览器（Chrome 91+, Firefox 89+）

### Issue 3: 性能没有提升

**可能原因**:
1. 浏览器没有真正启用 SIMD（检查 `chrome://flags` 中的 WebAssembly 设置）
2. 测试场景不涉及密集的向量/物理运算
3. 浏览器开发者工具降低了性能

**验证方法**:
```javascript
// 在浏览器控制台运行
WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 123, 3, 2, 1, 0, 10, 10, 1, 8, 0, 65, 0, 253, 17, 11]))
// 返回 true 表示支持 SIMD
```

---

## 📝 测试报告模板

测试完成后，请填写以下报告：

### 环境信息
- **操作系统**: Windows 10 / macOS / Linux
- **Emscripten 版本**:
- **浏览器及版本**:
- **CMake 版本**:

### 构建测试结果
- [ ] 构建成功 / [ ] 构建失败
- **编译时间**:
- **文件大小变化**:

### 运行时测试结果
- [ ] 运行成功 / [ ] 运行失败
- **是否检测到 SIMD**: 是 / 否
- **控制台错误**: 无 / 有（请附上错误信息）

### 性能测试结果
| 测试场景 | 无 SIMD (FPS/ms) | 有 SIMD (FPS/ms) | 提升比例 |
|---------|------------------|------------------|---------|
| 物理场景 |                  |                  |         |
| 向量运算 |                  |                  |         |

### 问题和建议
（请描述测试中遇到的问题和改进建议）

---

## 📞 联系方式

测试过程中如有问题，请联系：
- **分支创建者**: [你的名字]
- **GitHub Issue**: https://github.com/taptap/UrhoX/issues
- **相关文档**: `docs/research/webassembly-simd-support.md`

---

## 🎯 测试目标完成标准

✅ **通过标准**:
- 所有浏览器测试通过
- 性能提升 > 15%
- 无严重 bug 或兼容性问题

✅ **可合并到 main 的条件**:
- 至少 2 名同事完成测试并反馈
- 所有严重问题已解决
- 文档完整且准确

---

*祝测试顺利！* 🚀
