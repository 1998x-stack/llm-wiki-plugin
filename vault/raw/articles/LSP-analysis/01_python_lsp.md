# Python LSP 工具完整调研

> 版本：2025-04 | 覆盖：pylsp / pyright / jedi-language-server / ruff-lsp / basedpyright

---

## 1. Python LSP 生态全景

```
Python LSP 生态
├── python-lsp-server (pylsp)       ← 社区维护，插件化，原 palantir/python-language-server
├── pyright                         ← Microsoft 出品，静态类型检查
├── basedpyright                    ← pyright 增强分支
├── jedi-language-server            ← 基于 jedi 库，轻量
├── ruff-lsp / ruff (内置 LSP)      ← Astral 出品，高速 linter/formatter
├── pylance                         ← VS Code 专属，基于 pyright（闭源）
└── anakin-language-server          ← 基于 anaconda + jedi（已停更）
```

---

## 2. python-lsp-server (pylsp)

### 2.1 简介与历史

| 时间 | 事件 |
|------|------|
| 2017 | Palantir 发布 `python-language-server` (pyls) |
| 2021-01 | Palantir 宣布停止维护 |
| 2021-03 | 社区 fork 为 `python-lsp-server` (pylsp) |
| 2022+ | 活跃维护，插件生态完善 |
| 2024 | v1.11.x，支持 Python 3.8–3.12 |

**仓库**：https://github.com/python-lsp/python-lsp-server

### 2.2 版本历史

| 版本 | 时间 | 主要变更 |
|------|------|---------|
| 1.0.0 | 2021-03 | 从 pyls fork，重命名 |
| 1.2.0 | 2021-07 | 修复 rope 重构问题 |
| 1.4.0 | 2022-01 | 增量文本同步优化 |
| 1.7.0 | 2023-01 | 改进 flake8/pylint 插件 |
| 1.9.0 | 2023-08 | 支持 ruff 作为 linter |
| 1.10.0 | 2024-01 | 改进 workspace/symbol |
| 1.11.0 | 2024-06 | Python 3.12 完整支持 |

### 2.3 安装

```bash
# 基础安装
pip install python-lsp-server

# 全功能安装（含所有可选依赖）
pip install "python-lsp-server[all]"

# 指定依赖安装
pip install "python-lsp-server[rope,flake8,autopep8,yapf,pylint,mccabe,pyflakes]"

# 开发版（从源码）
git clone https://github.com/python-lsp/python-lsp-server
cd python-lsp-server
pip install -e ".[all,dev]"
```

### 2.4 从源码构建

```bash
# 依赖
python >= 3.8
pip >= 21.0

# 克隆 & 安装
git clone https://github.com/python-lsp/python-lsp-server.git
cd python-lsp-server

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 开发模式安装
pip install -e ".[all,test]"

# 运行测试
pytest test/ -v

# 构建发行包
pip install build
python -m build
# 产出：dist/python_lsp_server-x.x.x-py3-none-any.whl
```

### 2.5 插件生态

| 插件 | 功能 | 安装 |
|------|------|------|
| `pylsp-mypy` | mypy 类型检查 | `pip install pylsp-mypy` |
| `pylsp-rope` | rope 重构 | `pip install pylsp-rope` |
| `python-lsp-black` | black 格式化 | `pip install python-lsp-black` |
| `python-lsp-ruff` | ruff linter/formatter | `pip install python-lsp-ruff` |
| `pylsp-isort` | isort 导入排序 | `pip install pylsp-isort` |
| `python-lsp-jsonrpc` | JSON-RPC 核心 | 内置依赖 |

### 2.6 配置（pylsp）

```json
// .vscode/settings.json 或 neovim lspconfig settings
{
  "pylsp.plugins.pyflakes.enabled": true,
  "pylsp.plugins.pycodestyle.enabled": true,
  "pylsp.plugins.pylint.enabled": false,
  "pylsp.plugins.flake8.enabled": false,
  "pylsp.plugins.black.enabled": true,
  "pylsp.plugins.autopep8.enabled": false,
  "pylsp.plugins.yapf.enabled": false,
  "pylsp.plugins.isort.enabled": true,
  "pylsp.plugins.rope_autoimport.enabled": true,
  "pylsp.plugins.rope_completion.enabled": true,
  "pylsp.configurationSources": ["pycodestyle"],
  "pylsp.plugins.pycodestyle.maxLineLength": 120
}
```

### 2.7 Neovim 集成

```lua
require('lspconfig').pylsp.setup({
  settings = {
    pylsp = {
      plugins = {
        pyflakes = { enabled = true },
        pycodestyle = { enabled = true, maxLineLength = 120 },
        pylint = { enabled = false },
        black = { enabled = true, line_length = 120 },
        isort = { enabled = true },
        rope_autoimport = { enabled = true },
      }
    }
  },
  on_attach = on_attach,
})
```

### 2.8 内置插件完整列表

| 插件名 | 默认启用 | 功能 |
|--------|---------|------|
| `autopep8` | ✓ | PEP8 自动格式化 |
| `definition` | ✓ | 跳转定义 (jedi) |
| `flake8` | ✗ | flake8 linting |
| `folding` | ✓ | 代码折叠 |
| `highlight` | ✓ | 文档高亮 |
| `hover` | ✓ | 悬停信息 (jedi) |
| `jedi_completion` | ✓ | jedi 代码补全 |
| `jedi_rename` | ✓ | jedi 重命名 |
| `mccabe` | ✓ | 圈复杂度检测 |
| `preload` | ✓ | 预加载模块 |
| `pycodestyle` | ✓ | PEP8 风格检查 |
| `pydocstyle` | ✗ | 文档字符串规范 |
| `pyflakes` | ✓ | 语法/未使用变量检查 |
| `pylint` | ✗ | pylint 分析 |
| `references` | ✓ | 引用查找 |
| `rope_autoimport` | ✗ | rope 自动导入 |
| `rope_completion` | ✗ | rope 补全 |
| `signature` | ✓ | 函数签名 |
| `symbols` | ✓ | 文档符号 |
| `yapf` | ✗ | YAPF 格式化 |

---

## 3. Pyright

### 3.1 简介

Pyright 是 Microsoft 开发的静态类型检查器，同时作为语言服务器提供 LSP 支持。采用 TypeScript 编写，使用 Node.js 运行。

**仓库**：https://github.com/microsoft/pyright

### 3.2 版本历史

| 版本 | 时间 | 主要特性 |
|------|------|---------|
| 1.0.0 | 2019-08 | 首次发布 |
| 1.1.x | 2020 | 增量分析、Protocol 类型 |
| 1.1.100 | 2021 | TypeGuard、ParamSpec |
| 1.1.200 | 2022 | TypeVarTuple、Unpack |
| 1.1.300 | 2023 | TypeIs、override 支持 |
| 1.1.350+ | 2024 | PEP 695 type alias、PEP 696 TypeVar defaults |
| 1.1.370+ | 2024-10 | Python 3.13 完整支持 |
| 1.1.390+ | 2025-03 | 当前稳定版 |

### 3.3 架构

```
pyright
├── packages/
│   ├── pyright-internal/     ← 核心分析引擎（TypeScript）
│   │   ├── analyzer/         ← 类型推断、符号解析
│   │   ├── parser/           ← Python AST 解析器
│   │   ├── typestubs-fallback/  ← 内置 typeshed
│   │   └── tests/
│   ├── pyright/              ← CLI 工具
│   └── vscode-pyright/       ← VS Code 扩展
└── ...
```

### 3.4 安装

```bash
# npm 全局安装（推荐）
npm install -g pyright

# pip 安装（包装版本）
pip install pyright

# 验证
pyright --version
pyright-langserver --version

# 通过 npx 使用（无需全局安装）
npx pyright --version
```

### 3.5 从源码构建

```bash
# 前置要求
node >= 18.0.0
npm >= 8.0.0

git clone https://github.com/microsoft/pyright.git
cd pyright

# 安装依赖
npm install

# 构建
npm run build

# 运行测试
npm run test

# 打包 CLI
cd packages/pyright
npm pack
# 产出：pyright-x.x.x.tgz

# 打包 VS Code 扩展
cd packages/vscode-pyright
npm install -g vsce
vsce package
# 产出：vscode-pyright-x.x.x.vsix
```

### 3.6 pyrightconfig.json 配置

```json
{
  "include": ["src", "tests"],
  "exclude": ["**/node_modules", "**/.venv", "**/dist"],
  "ignore": ["src/legacy/**"],
  "defineConstant": {
    "DEBUG": true
  },
  "venvPath": ".",
  "venv": ".venv",
  "pythonVersion": "3.11",
  "pythonPlatform": "Linux",
  "typeCheckingMode": "strict",
  "useLibraryCodeForTypes": true,
  "autoSearchPaths": true,
  "extraPaths": ["./stubs"],
  "reportMissingImports": "error",
  "reportMissingTypeStubs": "warning",
  "reportUnknownMemberType": "none",
  "stubPath": "typings",
  "executionEnvironments": [
    {
      "root": "src/web",
      "pythonVersion": "3.12",
      "pythonPlatform": "Windows"
    }
  ]
}
```

### 3.7 类型检查模式对比

| 模式 | 说明 |
|------|------|
| `off` | 不报告类型错误 |
| `basic` | 基础检查，推断可用类型 |
| `standard` | 标准检查（默认） |
| `strict` | 严格检查，所有变量需类型注释 |

### 3.8 Neovim 集成

```lua
require('lspconfig').pyright.setup({
  settings = {
    pyright = {
      -- 使用 ruff 处理 imports，禁用 pyright 的 organize imports
      disableOrganizeImports = true,
    },
    python = {
      analysis = {
        autoSearchPaths = true,
        diagnosticMode = "openFilesOnly", -- 或 "workspace"
        useLibraryCodeForTypes = true,
        typeCheckingMode = "basic",       -- off/basic/standard/strict
        autoImportCompletions = true,
      },
    },
  },
  on_attach = on_attach,
})
```

---

## 4. basedpyright

### 4.1 简介

basedpyright 是 pyright 的社区 fork，修复了 pyright 的一些设计争议，增加了更多诊断选项。

**仓库**：https://github.com/DetachHead/basedpyright

### 4.2 与 pyright 的差异

| 特性 | pyright | basedpyright |
|------|---------|--------------|
| 未知类型报告 | 较宽松 | 更严格可选项 |
| `reportUnreachable` | 有限 | 增强 |
| `reportAny` | 无 | 新增 |
| `reportExplicitAny` | 无 | 新增 |
| `reportIgnoreCommentWithoutRule` | 无 | 新增 |
| hover 类型显示 | 标准 | 更详细 |
| baseline 系统 | 无 | 支持错误基线 |
| VS Code 扩展 | pylance (闭源) | 开源版本 |

### 4.3 安装

```bash
pip install basedpyright
# 或
npm install -g basedpyright

# Neovim lspconfig
require('lspconfig').basedpyright.setup({
  settings = {
    basedpyright = {
      analysis = {
        typeCheckingMode = "standard",
        reportAny = false,
      }
    }
  }
})
```

---

## 5. jedi-language-server

### 5.1 简介

基于 `jedi` 库构建的轻量 LSP Server，适合不需要严格类型检查的场景。

**仓库**：https://github.com/pappasam/jedi-language-server

### 5.2 版本历史

| 版本 | 特点 |
|------|------|
| 0.x | 初期版本 |
| 0.34.x | 当前版本，支持 jedi 0.19.x |
| 0.41.x | 2024，Python 3.12 支持 |

### 5.3 安装与配置

```bash
pip install jedi-language-server

# Neovim
require('lspconfig').jedi_language_server.setup({
  init_options = {
    workspace = {
      extraPaths = [],
      environmentPath = "/path/to/.venv/bin/python",
      symbols = { maxSymbols = 20, ignoreFolders = [".nox", ".tox", ".venv"] }
    },
    completion = { disableSnippets = false, resolveEagerly = false },
    diagnostics = { enable = true, didOpen = true, didSave = true, didChange = true },
    hover = { enable = true, disable = { keyword = { all = false } } },
    markupKindPreferred = "markdown",
  }
})
```

---

## 6. ruff-lsp / ruff (内置 LSP)

### 6.1 简介

Ruff 是用 Rust 编写的极速 Python linter，从 0.4.0 版本开始内置 LSP 服务器。

**仓库**：https://github.com/astral-sh/ruff

### 6.2 版本演进

| 版本 | 时间 | 特性 |
|------|------|------|
| 0.0.x | 2022 | 初始 linter |
| 0.1.0 | 2023-08 | 稳定 API，ruff-lsp 独立包 |
| 0.2.0 | 2024-01 | formatter 稳定版 |
| 0.4.0 | 2024-04 | **内置 LSP server** (`ruff server`) |
| 0.5.0 | 2024-07 | ruff-lsp **弃用**，统一到 `ruff server` |
| 0.7.0 | 2024-10 | 扩展规则集，D/NPY 规则 |
| 0.9.x | 2025-01 | 当前稳定版 |

### 6.3 安装

```bash
# pip
pip install ruff

# cargo（从源码）
cargo install ruff

# uv（推荐）
uv tool install ruff

# homebrew
brew install ruff

# 验证内置 LSP
ruff server --version
```

### 6.4 从源码构建

```bash
# 前置：Rust >= 1.75, cargo
git clone https://github.com/astral-sh/ruff.git
cd ruff

# 构建 release
cargo build --release -p ruff
# 产出：target/release/ruff

# 运行测试
cargo test --workspace

# 构建 Python wheels
pip install maturin
maturin build --release
# 产出：target/wheels/ruff-x.x.x-*.whl
```

### 6.5 ruff.toml / pyproject.toml 配置

```toml
# ruff.toml
line-length = 120
indent-width = 4
target-version = "py311"

[lint]
select = ["E", "F", "W", "I", "N", "UP", "ANN", "B", "SIM"]
ignore = ["E501", "ANN101", "ANN102"]
fixable = ["ALL"]
unfixable = ["B"]

[lint.isort]
known-first-party = ["mypackage"]

[lint.per-file-ignores]
"tests/**" = ["ANN", "S"]
"__init__.py" = ["F401"]

[format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### 6.6 Neovim 集成

```lua
-- 使用内置 ruff server（推荐，ruff >= 0.4.0）
require('lspconfig').ruff.setup({
  on_attach = function(client, bufnr)
    -- 禁用 ruff hover（使用 pyright/pylsp 的 hover）
    client.server_capabilities.hoverProvider = false
  end,
  init_options = {
    settings = {
      -- ruff LSP 设置
      lineLength = 120,
      fixAll = true,
      organizeImports = true,
    }
  }
})

-- 与 pyright 共存（推荐组合）
require('lspconfig').pyright.setup({
  settings = {
    pyright = { disableOrganizeImports = true },
    python = { analysis = { ignore = { "*" } } } -- 把诊断交给 ruff
  }
})
```

---

## 7. 综合对比

### 7.1 功能矩阵

| 特性 | pylsp | pyright | basedpyright | jedi-lsp | ruff-lsp |
|------|-------|---------|--------------|----------|----------|
| 代码补全 | ✓ (jedi) | ✓ | ✓ | ✓ (jedi) | ✗ |
| 跳转定义 | ✓ | ✓ | ✓ | ✓ | ✗ |
| 类型检查 | 有限 | ✓✓ | ✓✓+ | ✗ | ✗ |
| Linting | ✓ (插件) | ✓ | ✓ | 基础 | ✓✓ |
| 格式化 | ✓ (插件) | ✗ | ✗ | ✗ | ✓✓ |
| 重命名 | ✓ | ✓ | ✓ | ✓ | ✗ |
| 悬停信息 | ✓ | ✓ | ✓ | ✓ | ✗ |
| 语义高亮 | ✗ | ✓ | ✓ | ✗ | ✓ |
| Inlay Hints | ✗ | ✓ | ✓ | ✗ | ✗ |
| 自动导入 | ✓ (rope) | ✓ | ✓ | ✓ | ✓ |
| Import 排序 | ✓ (isort) | ✗ | ✗ | ✗ | ✓ |
| **速度** | 中等 | 快 | 快 | 中等 | 极快 |
| **运行时** | Python | Node.js | Node.js | Python | Rust |

### 7.2 推荐组合

```
# 推荐 1：极致类型安全 + 快速 linting
basedpyright（类型检查 + 补全）+ ruff（linting + formatting）

# 推荐 2：轻量快速
jedi-language-server（补全/导航）+ ruff（linting + formatting）

# 推荐 3：最大兼容性
pylsp + python-lsp-black + python-lsp-ruff + pylsp-mypy

# 推荐 4：VS Code 用户
pylance（自动）+ ruff（扩展）
```

---

## 8. 虚拟环境处理

### 8.1 自动检测

所有 Python LSP 都支持通过以下方式检测虚拟环境：

```bash
# 工程目录下创建 .venv
python -m venv .venv
source .venv/bin/activate

# 配置文件中指定 python 路径
# pyrightconfig.json
{
  "venvPath": ".",
  "venv": ".venv"
}
```

### 8.2 pyenv 集成

```bash
# .python-version 文件会被自动识别
echo "3.11.6" > .python-version
pyenv local 3.11.6

# pyright 通过 pythonVersion 字段匹配
```

### 8.3 conda 集成

```json
// pyrightconfig.json
{
  "pythonPath": "/opt/conda/envs/myenv/bin/python"
}
```

---

## 9. 调试与故障排除

### 9.1 常见问题

```bash
# 问题：pylsp 无法找到已安装的包
# 解决：确保在项目 venv 中安装 pylsp
source .venv/bin/activate
pip install python-lsp-server

# 问题：pyright 报 "Import could not be resolved"
# 解决：检查 pyrightconfig.json 的 venvPath 和 venv 设置

# 问题：ruff server 不工作
# 解决：确保 ruff >= 0.4.0
ruff --version
# 如果 < 0.4.0，使用 ruff-lsp（旧版）
pip install ruff-lsp
```

### 9.2 日志调试

```bash
# pylsp 调试日志
pylsp --log-file /tmp/pylsp.log --verbose

# pyright 详细输出
pyright --verbose /path/to/project

# ruff 检查配置
ruff check --show-settings /path/to/file.py
```

---

## 10. 参考资源

| 资源 | 链接 |
|------|------|
| python-lsp-server | https://github.com/python-lsp/python-lsp-server |
| pyright | https://github.com/microsoft/pyright |
| pyright 配置参考 | https://github.com/microsoft/pyright/blob/main/docs/configuration.md |
| basedpyright | https://github.com/DetachHead/basedpyright |
| jedi-language-server | https://github.com/pappasam/jedi-language-server |
| ruff | https://github.com/astral-sh/ruff |
| ruff LSP 文档 | https://docs.astral.sh/ruff/editors/ |
| nvim-lspconfig Python | https://github.com/neovim/nvim-lspconfig/blob/master/doc/configs.md#pyright |
