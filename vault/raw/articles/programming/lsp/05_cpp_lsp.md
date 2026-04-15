# C/C++ LSP 工具完整调研：clangd / ccls

> 版本：2025-04 | 覆盖：clangd 18.x / ccls 0.20.x / compile_commands.json 全解析

---

## 1. 生态概览

```
C/C++ LSP 生态
├── clangd         ← LLVM/Clang 官方 LSP，功能最全，首选
├── ccls           ← 高性能替代，C++17 最优秀的候选
└── cquery (已停更) ← ccls 的前身
```

---

## 2. clangd

### 2.1 简介与历史

clangd 是 LLVM 项目的一部分，基于 Clang 的 LibTooling 提供 C/C++/ObjC/CUDA 的语言服务。

| 时间 | 版本 | 关键特性 |
|------|------|---------|
| 2018 | 7.0 | 首个正式版，基础功能 |
| 2019 | 9.0 | 代码补全大幅改进 |
| 2020 | 10.0 | Semantic Highlighting |
| 2020 | 11.0 | Inlay Hints（实验）|
| 2021 | 12.0 | 大幅性能优化 |
| 2022 | 14.0 | C++20 支持改进 |
| 2022 | 15.0 | import/module 初步支持 |
| 2023 | 16.0 | C++23 支持 |
| 2023 | 17.0 | clang-tidy 集成改进 |
| 2024 | 18.0 | C++26 特性，Modules 改进 |
| 2024 | 19.0 | 当前稳定版 |

### 2.2 架构

```
clangd 进程
├── LSP Layer         ← JSON-RPC 处理
├── ClangdServer      ← 协调层
│   ├── TUScheduler   ← 翻译单元调度（异步，优先级）
│   │   ├── AST Worker (per-file)
│   │   └── Preamble Worker (per-file PCH)
│   ├── FileIndex     ← 后台索引（全 workspace）
│   │   ├── MemIndex  ← 内存中的快速索引
│   │   └── DiskIndex ← .cache/clangd/ 磁盘索引
│   └── GlobalCompilationDatabase ← compile_commands.json
│
└── Clang Frontend    ← Clang 解析器和语义分析
    ├── Lexer/Parser
    ├── Sema (语义分析)
    └── ASTContext
```

### 2.3 安装

```bash
# Ubuntu/Debian
sudo apt install clangd-18
# 设置默认版本
sudo update-alternatives --install /usr/bin/clangd clangd /usr/bin/clangd-18 100

# Arch Linux
pacman -S clang  # clangd 包含在内

# macOS (Homebrew)
brew install llvm
echo 'export PATH="/opt/homebrew/opt/llvm/bin:$PATH"' >> ~/.zshrc

# Windows - Visual Studio 安装包
# 或 LLVM 官方安装程序：https://releases.llvm.org/

# mason.nvim
:MasonInstall clangd

# 验证
clangd --version
```

### 2.4 从源码构建 (LLVM)

```bash
# 前置：CMake >= 3.20, Ninja, C++ 编译器, Python 3

# 获取源码
git clone https://github.com/llvm/llvm-project.git
cd llvm-project

# 最小化构建（仅 clangd）
cmake -S llvm -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra" \
  -DLLVM_TARGETS_TO_BUILD="X86;AArch64" \
  -DCMAKE_INSTALL_PREFIX=/usr/local \
  -DLLVM_ENABLE_ASSERTIONS=OFF \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_INCLUDE_BENCHMARKS=OFF

# 仅构建 clangd 目标（更快）
ninja -C build clangd

# 产出：build/bin/clangd

# 完整安装
ninja -C build install

# 使用 clang 自身构建（更快）
cmake -S llvm -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DLLVM_ENABLE_LLD=ON \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra" \
  -DLLVM_TARGETS_TO_BUILD="Native"

ninja -C build clangd
```

### 2.5 compile_commands.json

这是 clangd 的核心配置，告知编译参数。

#### CMake 项目

```bash
cmake -S . -B build \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
# 产出：build/compile_commands.json

# 软链接到项目根目录
ln -s build/compile_commands.json .
```

#### 手动 compile_commands.json

```json
[
  {
    "directory": "/home/user/project",
    "file": "/home/user/project/src/main.cpp",
    "command": "g++ -std=c++20 -I/home/user/project/include -DDEBUG=1 -o main.o -c src/main.cpp"
  },
  {
    "directory": "/home/user/project",
    "file": "/home/user/project/src/util.cpp",
    "arguments": ["g++", "-std=c++20", "-I./include", "-c", "src/util.cpp", "-o", "util.o"]
  }
]
```

#### Bear（从 Makefile 生成）

```bash
# 安装 bear
sudo apt install bear  # Ubuntu
brew install bear      # macOS

# 包装构建命令
bear -- make
bear -- make -j8
# 产出：compile_commands.json
```

#### CMake 其他方式

```bash
# 使用 cmake-commands.json 导出工具
pip install compiledb
compiledb make

# 或 intercept-build（LLVM scan-build）
intercept-build make
```

### 2.6 .clangd 配置文件

```yaml
# .clangd（项目根目录）

CompileFlags:
  Add:
    - "-std=c++20"
    - "-Wall"
    - "-Wextra"
    - "-I./include"
    - "-DDEBUG"
  Remove:
    - "-W4"  # 移除 MSVC 风格 warning
  Compiler: g++  # 覆盖编译器
  CompilationDatabase: build/  # 指定 compile_commands.json 路径

Index:
  Background: Build  # 后台索引：Build/Skip
  StandardLibrary: Yes  # 索引标准库

Diagnostics:
  Suppress:
    - "pp_including_mainfile_in_preamble"
    - "-Wall"
  UnusedIncludes: Strict  # None/Strict
  MissingIncludes: Strict  # None/Strict
  ClangTidy:
    Add:
      - modernize-*
      - bugprone-*
      - clang-analyzer-*
      - performance-*
      - readability-identifier-naming
    Remove:
      - modernize-use-trailing-return-type
    CheckOptions:
      readability-identifier-naming.VariableCase: camelBack
      readability-identifier-naming.FunctionCase: camelBack
      readability-identifier-naming.ClassCase: CamelCase
      readability-identifier-naming.MemberCase: camelBack
      readability-identifier-naming.MemberPrefix: "m_"

InlayHints:
  Enabled: Yes
  ParameterNames: Yes
  DeducedTypes: Yes
  Designators: Yes

Hover:
  ShowAKA: Yes

---
# 针对特定路径覆盖配置
If:
  PathMatch: "tests/.*"
Diagnostics:
  ClangTidy:
    Remove: ["*"]  # 测试文件禁用 clang-tidy
```

### 2.7 Neovim 配置

```lua
require('lspconfig').clangd.setup({
  cmd = {
    "clangd",
    "--background-index",
    "--background-index-priority=normal",
    "--clang-tidy",
    "--clang-tidy-checks=*",
    "--completion-style=bundled",
    "--cross-file-rename",
    "--fallback-style=Google",
    "--header-insertion=iwyu",
    "--header-insertion-decorators",
    "--suggest-missing-includes",
    "--all-scopes-completion",
    "--pch-storage=memory",  -- 或 disk，节省内存
    "--log=error",
    "--j=4",  -- 并行任务数
    "--malloc-trim",  -- 定期释放内存
    "--offset-encoding=utf-16",
  },
  filetypes = { "c", "cpp", "objc", "objcpp", "cuda", "proto" },
  root_dir = require('lspconfig').util.root_pattern(
    ".clangd",
    ".clang-tidy",
    ".clang-format",
    "compile_commands.json",
    "compile_flags.txt",
    "configure.ac",
    "CMakeLists.txt"
  ),
  capabilities = vim.tbl_deep_extend("force",
    vim.lsp.protocol.make_client_capabilities(),
    {
      -- 启用 offset_encoding utf-8（clangd 16+ 支持）
      offsetEncoding = { "utf-8" }
    }
  ),
  on_attach = on_attach,
})
```

### 2.8 clangd 命令行参数详解

```bash
clangd \
  --background-index         # 后台建立全 workspace 索引
  --background-index-priority=low|normal|high  # 索引优先级
  --clang-tidy               # 启用 clang-tidy 诊断
  --completion-style=detailed|bundled  # 补全样式
  --fallback-style=LLVM|Google|Chromium|Mozilla|WebKit  # 无 .clang-format 时的格式化风格
  --header-insertion=iwyu|never  # 自动插入头文件
  --all-scopes-completion    # 补全包含不在当前作用域的符号
  --pch-storage=disk|memory  # PCH 存储位置（disk 省内存，memory 快）
  --j=8                      # 异步工作线程数
  --log=verbose|info|error   # 日志级别
  --pretty                   # 格式化 JSON 输出（调试用）
  --query-driver=...         # 允许 clangd 查询特定编译器的系统头文件
  --enable-config            # 读取 .clangd 配置文件（默认启用）
  --offset-encoding=utf-8|utf-16|utf-32
  --malloc-trim              # 定期释放内存（Linux）
  --remote-index-address=host:port  # 远程索引服务器
```

---

## 3. ccls

### 3.1 简介

ccls 是 cquery 的继承者，专注于性能和 C++17 特性，使用 Clang libclang 而非 libTooling。

**仓库**：https://github.com/MaskRay/ccls

### 3.2 版本历史

| 版本 | 时间 | 特性 |
|------|------|------|
| 0.20180424 | 2018 | 从 cquery fork |
| 0.20190823 | 2019 | 大幅重写 |
| 0.20220729 | 2022 | LLVM 14 支持 |
| 0.20241108 | 2024 | 当前版本，LLVM 18 支持 |

### 3.3 安装

```bash
# Ubuntu/Debian
sudo apt install ccls

# Arch Linux
pacman -S ccls

# macOS
brew install ccls

# 从源码构建（见下节）
```

### 3.4 从源码构建

```bash
# 前置：CMake >= 3.8, LLVM/Clang 开发库, rapidjson

# Ubuntu 安装依赖
sudo apt install cmake libclang-18-dev libclang-cpp18-dev rapidjson-dev

git clone --depth=1 --recursive https://github.com/MaskRay/ccls
cd ccls

# 构建
cmake -S . -B Release \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=/usr/lib/llvm-18 \
  -DUSE_SYSTEM_RAPIDJSON=ON

cmake --build Release -j$(nproc)
# 产出：Release/ccls

# macOS
cmake -S . -B Release \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH=$(brew --prefix llvm)

cmake --build Release -j$(sysctl -n hw.ncpu)

# 安装
sudo cmake --install Release
```

### 3.5 ccls 配置

```json
// .ccls（项目根目录）
%compile_commands.json
%cpp -std=c++20
-I./include
-DDEBUG
```

```json
// 或 ccls.json
{
  "compilationDatabaseDirectory": "build",
  "cache": {
    "directory": "/tmp/ccls-cache",
    "format": "json"
  },
  "clang": {
    "extraArgs": ["-std=c++20", "-Wall"],
    "excludeArgs": ["-W4"]
  },
  "index": {
    "threads": 4,
    "onChange": false
  },
  "codeLens": {
    "localVariables": true
  }
}
```

### 3.6 Neovim 配置

```lua
require('lspconfig').ccls.setup({
  init_options = {
    compilationDatabaseDirectory = "build",
    index = {
      threads = 0,  -- 0 = 使用所有 CPU
      onChange = false,
    },
    clang = {
      excludeArgs = { "-frounding-math" },
    },
    cache = {
      directory = ".ccls-cache",
    },
    highlight = {
      lsRanges = true,
    },
  },
  on_attach = on_attach,
})
```

---

## 4. clangd vs ccls 对比

| 特性 | clangd | ccls |
|------|--------|------|
| 维护状态 | LLVM 官方，活跃 | 社区，偶尔更新 |
| 底层 | LibTooling | libclang |
| 索引方式 | 后台增量 | 全量 cache |
| 索引存储 | `.cache/clangd/` | `.ccls-cache/` |
| 内存使用 | 较高 | 中等 |
| C++20 Modules | 初步支持 | 有限 |
| CUDA | ✓ | ✓ |
| ObjC/ObjC++ | ✓ | 有限 |
| clang-tidy | 内置集成 | 无直接集成 |
| Format | clang-format | clang-format |
| 跨文件重命名 | ✓ | ✓ |
| Call Hierarchy | ✓ | ✓ |
| Type Hierarchy | ✓ | ✗ |
| Inlay Hints | ✓ | ✗ |
| Semantic Tokens | ✓ | ✓ |
| **推荐场景** | 所有新项目 | 超大型旧项目 |

---

## 5. 构建系统集成

### 5.1 CMake

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(MyProject CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # 关键
set(CMAKE_CXX_STANDARD 20)

add_executable(myapp src/main.cpp src/util.cpp)
target_include_directories(myapp PUBLIC include/)
target_compile_options(myapp PRIVATE -Wall -Wextra)
```

### 5.2 Meson

```bash
meson setup build
cd build
# Meson 自动生成 compile_commands.json
ls compile_commands.json
```

### 5.3 Bazel

```bash
# 使用 bazel-compile-commands-extractor
pip install bazel-compile-commands-extractor
# 或
bazel run @hedron_compile_commands//:refresh_all

# 生成 compile_commands.json
```

### 5.4 Makefile（无 CMake）

```bash
# compile_flags.txt（简单项目）
-std=c++20
-I./include
-DDEBUG
-Wall

# 或使用 bear
bear -- make -j8
```

### 5.5 XCode（iOS/macOS）

```bash
# 使用 xcodeproj-to-compile-commands
pip install xcodeproj-to-compile-commands
xcbuild-compile-commands MyProject.xcodeproj

# 或 XcodeGen + CMake
```

---

## 6. clang-tidy 集成

### 6.1 .clang-tidy 配置

```yaml
# .clang-tidy
Checks: >
  -*,
  bugprone-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  portability-*,
  readability-*,
  -bugprone-easily-swappable-parameters,
  -cppcoreguidelines-avoid-magic-numbers,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers

WarningsAsErrors: ""
HeaderFilterRegex: ".*"
FormatStyle: "file"

CheckOptions:
  - key: readability-identifier-naming.VariableCase
    value: camelBack
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: modernize-use-default-member-init.UseAssignment
    value: "1"
```

### 6.2 自动修复

```bash
# 对单个文件修复
clang-tidy --fix src/main.cpp

# 对整个项目（使用 run-clang-tidy.py）
run-clang-tidy.py -fix -format -p build/
```

---

## 7. 远程开发场景

### 7.1 SSH + clangd

```bash
# VS Code Remote SSH：clangd 运行在远程机器上
# 配置 clangd 路径
# settings.json
{
  "clangd.path": "/usr/bin/clangd-18"
}
```

### 7.2 clangd-remote（分布式索引）

```bash
# 实验性特性：使用远程索引服务器
# 服务端（高性能机器）：
clangd-indexer --executor=all-TUs . > project.idx
clangd-remote-server --project-root=. --index-file=project.idx --server-address=0.0.0.0:50051

# 客户端（本地 clangd）：
clangd --remote-index-address=server:50051 --project-root=.
```

---

## 8. 调试 clangd

```bash
# 开启详细日志
clangd --log=verbose 2>/tmp/clangd.log

# 查看解析特定文件的命令
clangd --check=/path/to/file.cpp

# 检查 compile_commands.json 解析
clangd --check=/path/to/file.cpp 2>&1 | grep "compile command"

# 常见问题诊断
# 1. "No compile commands found" -> 检查 compile_commands.json 路径
# 2. "includes not found" -> 检查 --query-driver 或头文件路径
# 3. 内存过高 -> 使用 --pch-storage=disk，降低 --j 值
```

---

## 9. 参考资源

| 资源 | 链接 |
|------|------|
| clangd 官网 | https://clangd.llvm.org/ |
| clangd 配置文档 | https://clangd.llvm.org/config |
| clangd GitHub | https://github.com/llvm/llvm-project/tree/main/clang-tools-extra/clangd |
| ccls GitHub | https://github.com/MaskRay/ccls |
| ccls 配置 | https://github.com/MaskRay/ccls/wiki/Customization |
| Bear | https://github.com/rizsotto/Bear |
| clang-tidy 文档 | https://clang.llvm.org/extra/clang-tidy/ |
| compile_commands 规范 | https://clang.llvm.org/docs/JSONCompilationDatabase.html |
