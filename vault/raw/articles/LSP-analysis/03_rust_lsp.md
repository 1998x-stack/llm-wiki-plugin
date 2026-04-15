# Rust LSP 工具完整调研：rust-analyzer

> 版本：2025-04 | 覆盖：rust-analyzer / rls（历史）/ 构建系统深度分析

---

## 1. 历史与背景

### 1.1 演进历程

| 时间 | 事件 |
|------|------|
| 2017 | `rls`（Rust Language Server）发布，官方首个 Rust LSP |
| 2018-01 | Aleksey Kladov (@matklad) 启动 `rust-analyzer` 实验项目 |
| 2019 | rust-analyzer 逐渐超越 rls，社区转向支持 |
| 2020-01 | Rust 官方宣布 rust-analyzer 为 rls 的继任者 |
| 2022-07 | **rust-analyzer 合并进 rust-lang 官方组织** |
| 2022-09 | rls 正式弃用 |
| 2023-01 | rust-analyzer 随 rustup 默认分发 |
| 2024 | 发布节奏：每周滚动发布 |
| 2025 | 当前稳定通道，接近 1.0 稳定性 |

### 1.2 架构设计哲学

rust-analyzer 的设计有几个核心创新：

1. **Salsa 增量计算**：基于依赖追踪的增量分析，只重算变更部分
2. **Resilient 解析**：即使代码有语法错误也能提供服务
3. **离散数据结构**（Concrete Syntax Tree）：保留所有空白/注释信息
4. **无 panic 设计**：错误返回而非崩溃

---

## 2. 架构深度解析

### 2.1 整体架构

```
rust-analyzer 架构
├── crates/
│   ├── rust-analyzer/          ← LSP Server 入口
│   │   └── src/
│   │       ├── main_loop.rs    ← 事件循环
│   │       ├── handlers/       ← LSP 请求处理
│   │       └── config.rs       ← 配置管理
│   │
│   ├── ide/                    ← IDE 功能层（无 LSP 依赖）
│   │   ├── src/
│   │   │   ├── completion/     ← 代码补全
│   │   │   ├── hover/          ← 悬停信息
│   │   │   ├── diagnostics/    ← 诊断
│   │   │   ├── inlay_hints/    ← 内嵌提示
│   │   │   └── ...
│   │
│   ├── hir/                    ← 高层中间表示（类型系统）
│   │   ├── hir_def/            ← 定义层（函数、struct、trait）
│   │   ├── hir_ty/             ← 类型推断、trait 解析
│   │   └── hir_expand/         ← 宏展开
│   │
│   ├── syntax/                 ← CST 解析器（rowan 库）
│   │   ├── src/
│   │   │   ├── ast/            ← AST 类型定义
│   │   │   └── parsing/        ← 递归下降解析器
│   │
│   ├── base_db/                ← Salsa 数据库基础
│   ├── load-cargo/             ← Cargo 元数据加载
│   ├── project_model/          ← 项目结构模型
│   └── proc_macro_srv/         ← 过程宏服务器
│
└── lib/
    └── lsp-server/             ← 轻量 LSP 协议库（通用）
```

### 2.2 Salsa 增量计算

```rust
// Salsa 查询示例（概念）
#[salsa::query_group(HirDatabaseStorage)]
pub trait HirDatabase: InternDatabase + AstDatabase {
    // 这个查询会被增量缓存
    // 只有当 crate_def_map 依赖的输入变化时才重新计算
    fn crate_def_map(&self, krate: CrateId) -> Arc<DefMap>;
    
    // 函数体推断：只有该函数变化时重新计算
    fn infer(&self, def: DefWithBodyId) -> Arc<InferenceResult>;
}
```

### 2.3 过程宏服务器

```
rust-analyzer
    │ 命令行启动子进程
    ▼
proc-macro-srv（独立进程）
    │ 动态加载
    ▼
proc_macro dylib（用户项目编译的过程宏）
    │ 展开宏
    ▼
返回展开结果给 rust-analyzer
```

---

## 3. 安装方式

### 3.1 rustup（推荐）

```bash
# 安装 rust-analyzer 组件
rustup component add rust-analyzer

# 查看路径
rustup which rust-analyzer

# 更新（随 rustup 自动更新）
rustup update
```

### 3.2 预构建二进制

```bash
# GitHub Releases 下载
# https://github.com/rust-lang/rust-analyzer/releases

# Linux x86_64
curl -L https://github.com/rust-lang/rust-analyzer/releases/latest/download/rust-analyzer-x86_64-unknown-linux-gnu.gz \
  | gunzip -c > ~/.local/bin/rust-analyzer
chmod +x ~/.local/bin/rust-analyzer

# macOS Apple Silicon
curl -L https://github.com/rust-lang/rust-analyzer/releases/latest/download/rust-analyzer-aarch64-apple-darwin.gz \
  | gunzip -c > ~/.local/bin/rust-analyzer
chmod +x ~/.local/bin/rust-analyzer

# macOS x86_64
curl -L https://github.com/rust-lang/rust-analyzer/releases/latest/download/rust-analyzer-x86_64-apple-darwin.gz \
  | gunzip -c > ~/.local/bin/rust-analyzer
chmod +x ~/.local/bin/rust-analyzer

# Windows x64 (PowerShell)
Invoke-WebRequest `
  -Uri "https://github.com/rust-lang/rust-analyzer/releases/latest/download/rust-analyzer-x86_64-pc-windows-msvc.zip" `
  -OutFile "rust-analyzer.zip"
Expand-Archive rust-analyzer.zip -DestinationPath $env:LOCALAPPDATA\Programs\rust-analyzer
```

### 3.3 包管理器

```bash
# Arch Linux
pacman -S rust-analyzer

# Homebrew
brew install rust-analyzer

# Scoop (Windows)
scoop install rust-analyzer

# mason.nvim (Neovim)
:MasonInstall rust-analyzer
```

---

## 4. 从源码构建

### 4.1 标准构建

```bash
# 前置要求：Rust stable（最新版本推荐）
git clone https://github.com/rust-lang/rust-analyzer.git
cd rust-analyzer

# 构建 release 版本
cargo build --release -p rust-analyzer
# 产出：target/release/rust-analyzer

# 运行测试
cargo test --workspace

# 构建特定 crate
cargo build -p ide
cargo build -p hir

# 代码检查
cargo clippy --workspace --all-targets
```

### 4.2 交叉编译

```bash
# 为 Windows 交叉编译（在 Linux 上）
rustup target add x86_64-pc-windows-gnu
cargo build --release --target x86_64-pc-windows-gnu -p rust-analyzer

# 为 ARM 交叉编译
rustup target add aarch64-unknown-linux-gnu
cargo build --release --target aarch64-unknown-linux-gnu -p rust-analyzer
```

### 4.3 构建 VS Code 扩展

```bash
# 前置：Node.js >= 18, vsce
cd editors/code

# 安装依赖
npm install

# 构建 TypeScript
npm run build

# 打包扩展
npm install -g @vscode/vsce
vsce package --no-dependencies

# 包含预构建二进制
# 先下载对应平台的二进制到 server/ 目录
```

### 4.4 xtask（项目自定义构建工具）

```bash
# rust-analyzer 使用 xtask 模式
cargo xtask --help

# 运行完整 CI 检查
cargo xtask ci

# 生成文档
cargo xtask doc

# 安装到本地
cargo xtask install

# 运行基准测试
cargo xtask benchmark
```

---

## 5. 配置（rust-analyzer.json / rust-analyzer 设置）

### 5.1 完整配置参考

```json
{
  "rust-analyzer.cargo.features": "all",
  "rust-analyzer.cargo.target": null,
  "rust-analyzer.cargo.extraEnv": {},
  "rust-analyzer.cargo.buildScripts.enable": true,
  "rust-analyzer.cargo.buildScripts.useRustcWrapper": true,
  
  "rust-analyzer.checkOnSave": true,
  "rust-analyzer.check.command": "clippy",
  "rust-analyzer.check.extraArgs": [
    "--",
    "-W", "clippy::all",
    "-W", "clippy::pedantic"
  ],
  "rust-analyzer.check.targets": null,
  "rust-analyzer.check.features": "all",
  
  "rust-analyzer.procMacro.enable": true,
  "rust-analyzer.procMacro.server": null,
  
  "rust-analyzer.completion.autoimport.enable": true,
  "rust-analyzer.completion.postfix.enable": true,
  "rust-analyzer.completion.privateEditable.enable": false,
  "rust-analyzer.completion.fullFunctionSignatures.enable": true,
  
  "rust-analyzer.inlayHints.bindingModeHints.enable": true,
  "rust-analyzer.inlayHints.chainingHints.enable": true,
  "rust-analyzer.inlayHints.closingBraceHints.enable": true,
  "rust-analyzer.inlayHints.closureReturnTypeHints.enable": "with_block",
  "rust-analyzer.inlayHints.discriminantHints.enable": "fieldless",
  "rust-analyzer.inlayHints.expressionAdjustmentHints.enable": "reborrow",
  "rust-analyzer.inlayHints.lifetimeElisionHints.enable": "skip_trivial",
  "rust-analyzer.inlayHints.maxLength": 25,
  "rust-analyzer.inlayHints.parameterHints.enable": true,
  "rust-analyzer.inlayHints.rangeExclusiveHints.enable": true,
  "rust-analyzer.inlayHints.renderColons": true,
  "rust-analyzer.inlayHints.typeHints.enable": true,
  "rust-analyzer.inlayHints.typeHints.hideClosureInitialization": false,
  
  "rust-analyzer.lens.enable": true,
  "rust-analyzer.lens.run.enable": true,
  "rust-analyzer.lens.debug.enable": true,
  "rust-analyzer.lens.implementations.enable": true,
  "rust-analyzer.lens.references.adt.enable": true,
  "rust-analyzer.lens.references.enumVariant.enable": true,
  "rust-analyzer.lens.references.method.enable": true,
  "rust-analyzer.lens.references.trait.enable": true,
  
  "rust-analyzer.rustfmt.extraArgs": [],
  "rust-analyzer.rustfmt.overrideCommand": null,
  
  "rust-analyzer.diagnostics.enable": true,
  "rust-analyzer.diagnostics.experimental.enable": false,
  "rust-analyzer.diagnostics.disabled": [],
  "rust-analyzer.diagnostics.warningsAsHint": [],
  "rust-analyzer.diagnostics.warningsAsInfo": [],
  
  "rust-analyzer.imports.granularity.enforce": false,
  "rust-analyzer.imports.granularity.group": "crate",
  "rust-analyzer.imports.prefix": "plain",
  "rust-analyzer.imports.preferPrelude": true
}
```

### 5.2 .rust-analyzer.json（项目级别）

```json
{
  "$schema": "https://rust-analyzer.github.io/manual.html",
  "cargo": {
    "features": ["async", "serde"],
    "target": "x86_64-unknown-linux-gnu"
  },
  "check": {
    "command": "clippy",
    "extraArgs": ["--", "-D", "warnings"]
  },
  "rust": {
    "analyzerTargetDir": "target/rust-analyzer"
  }
}
```

---

## 6. Neovim 集成

### 6.1 基础配置

```lua
require('lspconfig').rust_analyzer.setup({
  on_attach = function(client, bufnr)
    -- 保存时自动格式化
    vim.api.nvim_create_autocmd("BufWritePre", {
      buffer = bufnr,
      callback = function()
        vim.lsp.buf.format({ async = false })
      end
    })
    on_attach(client, bufnr)
  end,
  settings = {
    ["rust-analyzer"] = {
      cargo = {
        features = "all",
        buildScripts = { enable = true },
      },
      check = {
        command = "clippy",
        extraArgs = { "--", "-W", "clippy::pedantic" },
      },
      procMacro = { enable = true },
      inlayHints = {
        bindingModeHints = { enable = true },
        closureReturnTypeHints = { enable = "with_block" },
        lifetimeElisionHints = { enable = "skip_trivial" },
        typeHints = { enable = true },
        chainingHints = { enable = true },
      },
      completion = {
        autoimport = { enable = true },
        postfix = { enable = true },
      },
      diagnostics = {
        enable = true,
        experimental = { enable = true },
      },
    }
  },
})
```

### 6.2 rustaceanvim（推荐替代）

```lua
-- rustaceanvim 是专为 Neovim 设计的 rust-analyzer 插件
-- 提供比 lspconfig 更好的 Rust 开发体验
vim.g.rustaceanvim = {
  server = {
    on_attach = on_attach,
    settings = {
      ["rust-analyzer"] = {
        check = { command = "clippy" },
        inlayHints = {
          lifetimeElisionHints = { enable = "skip_trivial" },
        },
      }
    },
  },
  tools = {
    hover_actions = { replace_builtin_hover = true },
    code_action_group = true,
  },
  dap = {
    adapter = {
      type = "executable",
      command = "codelldb",
      name = "rt_lldb",
    },
  },
}
```

---

## 7. 特性详解

### 7.1 Inlay Hints 类型

| Hint 类型 | 示例 |
|-----------|------|
| 类型注解 | `let x/*: i32*/ = 5;` |
| 参数名 | `foo(/*value:*/ 42)` |
| 链式调用 | `.iter()/*: Iter<&str>*/` |
| 生命周期 | `fn foo<'a>(x: &/*'a */str)` |
| 绑定模式 | `let &/*ref */x = &5` |
| 闭包返回类型 | `\|x\| /*-> i32 */{ x + 1 }` |
| 判别值 | `enum Foo { A/*= 0*/, B/*= 1*/ }` |

### 7.2 语义高亮 Token 类型

```
namespace, type, class, enum, interface, struct, typeParameter,
function, method, property, macro, variable, parameter, label,
keyword, comment, string, number, regexp, operator, decorator,
selfKeyword, builtinType, attribute, toolModule, generic
```

### 7.3 Code Actions 列表

```
- 添加缺失的 import
- 移除未使用的 import
- 创建新文件/模块
- 展开宏
- 内联/提取变量
- 内联/提取函数
- 转换 if let 为 match
- 填充 match 缺失 arm
- 添加 derive
- 生成 getter/setter
- 实现缺失的 trait 方法
- 添加生命周期注解
- 去掉不必要的括号
- 类型转换（as/From/Into）
- 移除 dbg! 宏
```

---

## 8. 多 Cargo Workspace 配置

### 8.1 Cargo Workspaces

```toml
# 根目录 Cargo.toml
[workspace]
members = [
  "crates/core",
  "crates/server",
  "crates/client",
]
resolver = "2"
```

### 8.2 rust-analyzer Cargo 链接模式

```json
// 大型 workspace 优化：使用独立 target 目录
{
  "rust-analyzer.rust.analyzerTargetDir": "target/rust-analyzer"
}
```

### 8.3 build.rs 脚本支持

```json
{
  "rust-analyzer.cargo.buildScripts.enable": true,
  "rust-analyzer.cargo.buildScripts.useRustcWrapper": true,
  // 缓存 build 脚本输出，避免重复执行
  "rust-analyzer.cargo.buildScripts.rebuildOnSave": false
}
```

---

## 9. 性能调优

### 9.1 大型项目优化

```json
{
  // 只分析打开的文件（不做全 workspace 检查）
  "rust-analyzer.diagnostics.experimental.enable": false,
  
  // 禁用过程宏（如果不使用）
  "rust-analyzer.procMacro.enable": false,
  
  // 仅 check 当前工作区，不 check 依赖
  "rust-analyzer.check.noDefaultFeatures": true,
  
  // 使用更快的 check 替代 clippy
  "rust-analyzer.check.command": "check",
  
  // 限制 Inlay Hints 长度
  "rust-analyzer.inlayHints.maxLength": 20
}
```

### 9.2 内存使用

| 项目规模 | 内存使用 |
|---------|---------|
| 小型（< 10k LOC） | ~100MB |
| 中型（~100k LOC） | ~500MB |
| 大型（rust-lang/rust 本身）| 2-4GB |

### 9.3 并行化

```bash
# rust-analyzer 使用 Rayon 并行分析
# 可通过环境变量控制线程数
export RAYON_NUM_THREADS=4
rust-analyzer
```

---

## 10. 调试 rust-analyzer 本身

### 10.1 内部日志

```bash
# 启用详细日志
export RA_LOG=info
rust-analyzer

# 特定模块日志
export RA_LOG=rust_analyzer::lsp_utils=debug,hir_ty=warn
```

### 10.2 状态查询

```
# Neovim 中查看 rust-analyzer 状态
:lua print(vim.inspect(vim.lsp.get_active_clients()[1].server_capabilities))

# 发送 rust-analyzer 专有命令
:lua vim.lsp.buf_request(0, 'rust-analyzer/analyzerStatus', nil, function(err, result) print(vim.inspect(result)) end)
```

### 10.3 常见问题

```bash
# 问题：proc macros 无法展开
# 解决：确保项目已完整 cargo build
cargo build
# 并确保 procMacro.enable = true

# 问题：大型项目响应慢
# 解决：使用 analyzerTargetDir 隔离分析 target

# 问题：找不到 rust-analyzer
# 解决：
rustup component add rust-analyzer
rustup which rust-analyzer  # 确认路径在 PATH 中
```

---

## 11. rls（历史参考）

rls 是 rust-analyzer 之前的官方 LSP Server，现已弃用，仅作历史参考。

| 特性 | rls | rust-analyzer |
|------|-----|---------------|
| 实现语言 | Rust | Rust |
| 底层 | rustc 内部 API | 独立解析器 |
| 增量分析 | 有限 | Salsa 完整支持 |
| 错误恢复 | 差 | 优秀 |
| 宏展开 | 有限 | 完整 |
| 维护状态 | **已弃用** | **活跃维护** |

```bash
# rls 已在 rust 1.65+ 从 rustup 默认组件中移除
# 如需旧版：
rustup component add rls  # 可能不可用
```

---

## 12. 参考资源

| 资源 | 链接 |
|------|------|
| rust-analyzer 官网 | https://rust-analyzer.github.io/ |
| 用户手册 | https://rust-analyzer.github.io/manual.html |
| GitHub | https://github.com/rust-lang/rust-analyzer |
| 架构文档 | https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md |
| 每周更新日志 | https://rust-analyzer.github.io/blog/ |
| rustaceanvim | https://github.com/mrcjkb/rustaceanvim |
| 配置参考 | https://rust-analyzer.github.io/manual.html#configuration |
