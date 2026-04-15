# Lua / Haskell / Ruby / PHP LSP 工具完整调研

> 版本：2025-04 | 覆盖：lua-language-server / hls / solargraph / intelephense / phpactor

---

## 第一部分：Lua LSP

---

## 1. lua-language-server (sumneko)

### 1.1 简介与历史

lua-language-server 由 sumneko（孙蒙可）开发，现为 LuaLS 组织维护，是 Lua 最主流的 LSP Server。使用 Lua/C++ 实现（核心用 Lua 写成，外围 C++）。

| 时间 | 版本 | 特性 |
|------|------|------|
| 2019 | 1.x | VS Code 插件初始版本 |
| 2021 | 2.x | 语义分析重写 |
| 2022-07 | 3.0.0 | **注释系统重写**，类型推断大幅提升 |
| 2022-12 | 3.5.x | Workspace diagnostics |
| 2023-06 | 3.6.0 | Lazy loading 改进 |
| 2023-11 | 3.7.0 | 类型系统增强 |
| 2024-05 | 3.8.0 | 诊断改进 |
| 2024-10 | 3.11.x | 当前稳定版 |

**仓库**：https://github.com/LuaLS/lua-language-server

### 1.2 安装

```bash
# Homebrew
brew install lua-language-server

# Arch Linux
pacman -S lua-language-server

# mason.nvim
:MasonInstall lua-language-server

# 手动下载预构建
VERSION="3.11.1"
# Linux x64
wget "https://github.com/LuaLS/lua-language-server/releases/download/${VERSION}/lua-language-server-${VERSION}-linux-x64.tar.gz"
tar -xzf lua-language-server-*.tar.gz -C ~/.local/share/lua-language-server

# 验证
lua-language-server --version
```

### 1.3 从源码构建

```bash
# 前置：CMake, Ninja, C++ 编译器, Git

git clone --recursive https://github.com/LuaLS/lua-language-server.git
cd lua-language-server

# macOS/Linux
cd 3rd/luamake
./compile/install.sh
cd ../..
./3rd/luamake/luamake rebuild

# Windows (需要 VS 2019+)
cd 3rd/luamake
compile\install.bat
cd ..\..
3rd\luamake\luamake.exe rebuild

# 产出：bin/lua-language-server
```

### 1.4 配置（.luarc.json）

```json
{
  "$schema": "https://raw.githubusercontent.com/LuaLS/vscode-lua/master/setting/schema.json",
  
  "Lua.runtime.version": "LuaJIT",
  "Lua.runtime.path": ["?.lua", "?/init.lua", "?/?.lua"],
  "Lua.runtime.pathStrict": false,
  
  "Lua.workspace.library": [
    "${3rd}/love2d/library",
    "${3rd}/luv/library",
    "/path/to/custom/library"
  ],
  "Lua.workspace.checkThirdParty": "Disable",
  "Lua.workspace.ignoreDir": ["node_modules", ".git", "dist"],
  "Lua.workspace.maxPreload": 5000,
  "Lua.workspace.preloadFileSize": 500,
  
  "Lua.diagnostics.enable": true,
  "Lua.diagnostics.globals": ["vim", "ngx", "love", "jit"],
  "Lua.diagnostics.disable": ["lowercase-global", "undefined-global"],
  "Lua.diagnostics.severity": {
    "deprecated": "Warning",
    "undefined-field": "Warning"
  },
  "Lua.diagnostics.unusedLocalExclude": ["_*"],
  
  "Lua.completion.enable": true,
  "Lua.completion.autoRequire": true,
  "Lua.completion.showWord": "Fallback",
  "Lua.completion.workspaceWord": true,
  
  "Lua.hover.enable": true,
  "Lua.hover.viewNumber": true,
  "Lua.hover.viewString": true,
  "Lua.hover.viewStringMax": 1000,
  
  "Lua.hint.enable": true,
  "Lua.hint.paramName": "All",
  "Lua.hint.paramType": true,
  "Lua.hint.setType": true,
  "Lua.hint.arrayIndex": "Enable",
  "Lua.hint.await": true,
  
  "Lua.format.enable": true,
  "Lua.format.defaultConfig": {
    "indent_style": "space",
    "indent_size": "4",
    "quote_style": "double",
    "trailing_table_separator": "always"
  },
  
  "Lua.semantic.enable": true,
  "Lua.semantic.annotation": true
}
```

### 1.5 Neovim 集成

```lua
require('lspconfig').lua_ls.setup({
  on_attach = on_attach,
  settings = {
    Lua = {
      runtime = {
        version = 'LuaJIT',
        path = vim.split(package.path, ';'),
      },
      diagnostics = {
        globals = { 'vim', 'require' },
        disable = { 'missing-fields' },
      },
      workspace = {
        library = {
          [vim.fn.expand('$VIMRUNTIME/lua')] = true,
          [vim.fn.stdpath('config') .. '/lua'] = true,
        },
        checkThirdParty = false,
        maxPreload = 100000,
        preloadFileSize = 10000,
      },
      telemetry = { enable = false },
      hint = {
        enable = true,
        paramName = "All",
        paramType = true,
        setType = true,
      },
      completion = {
        callSnippet = "Replace",
        keywordSnippet = "Both",
      },
    },
  },
})
```

### 1.6 EmmyLua 注释类型系统

```lua
---@class Vector
---@field x number X 分量
---@field y number Y 分量
---@field z number? 可选 Z 分量
local Vector = {}

---创建新向量
---@param x number
---@param y number
---@param z? number
---@return Vector
function Vector.new(x, y, z)
  return setmetatable({ x = x, y = y, z = z or 0 }, { __index = Vector })
end

---@param other Vector
---@return Vector
function Vector:add(other)
  return Vector.new(self.x + other.x, self.y + other.y, self.z + other.z)
end

---@alias Callback fun(event: string, data: any): boolean

---@param fn Callback
local function register(fn) end

---@type table<string, Vector>
local registry = {}

---@enum Direction
local Direction = {
  North = 0,
  South = 1,
  East  = 2,
  West  = 3,
}
```

---

## 第二部分：Haskell LSP

---

## 2. Haskell Language Server (HLS)

### 2.1 简介

HLS 是 Haskell 的官方 LSP Server，整合了多个 Haskell 工具（ghc, hlint, ormolu, fourmolu 等）。

**仓库**：https://github.com/haskell/haskell-language-server

### 2.2 版本历史

| 版本 | 时间 | 特性 |
|------|------|------|
| 0.1.0 | 2020-07 | 首次发布（整合多个项目）|
| 1.0.0 | 2021-04 | 稳定版 |
| 1.8.0 | 2022-07 | GHC 9.2 支持 |
| 2.0.0 | 2023-01 | GHC 9.4 支持 |
| 2.5.0 | 2023-09 | GHC 9.6 |
| 2.9.0 | 2024-07 | GHC 9.10 |
| 2.10.x | 2024-12 | 当前版本 |

### 2.3 安装

```bash
# GHCup（强烈推荐，处理 GHC 版本匹配）
ghcup install hls
ghcup set hls 2.10.0

# 指定 GHC 版本安装对应 HLS
ghcup install hls --ghc 9.4.8

# 验证
haskell-language-server --version
haskell-language-server-wrapper --version  # 自动选择版本
```

### 2.4 从源码构建

```bash
# HLS 必须与项目使用的 GHC 版本匹配
# 前置：GHC, cabal 或 stack

git clone https://github.com/haskell/haskell-language-server.git
cd haskell-language-server

# cabal 构建
cabal build haskell-language-server haskell-language-server-wrapper
cabal install haskell-language-server haskell-language-server-wrapper

# stack 构建
stack build haskell-language-server haskell-language-server-wrapper
stack install haskell-language-server haskell-language-server-wrapper

# 特定 GHC 版本构建
cabal build --with-compiler=ghc-9.4.8
```

### 2.5 Neovim 配置

```lua
require('lspconfig').hls.setup({
  cmd = { "haskell-language-server-wrapper", "--lsp" },
  filetypes = { "haskell", "lhaskell", "cabal" },
  root_dir = require('lspconfig').util.root_pattern(
    "*.cabal", "stack.yaml", "cabal.project", "package.yaml", "hie.yaml"
  ),
  settings = {
    haskell = {
      checkParents = "CheckOnSaveAndClose",
      checkProject = true,
      formattingProvider = "ormolu",  -- ormolu/fourmolu/stylish-haskell/brittany/none
      maxCompletions = 40,
      plugin = {
        alternateNumberFormat = { globalOn = true },
        callHierarchy = { globalOn = true },
        changeTypeSignature = { globalOn = true },
        class = { codeLensOn = true, globalOn = true },
        eval = { globalOn = true, config = { diff = true, exception = true } },
        ghcide_hover = { globalOn = true },
        hlint = { config = { flags = [] }, diagnosticsOn = true, globalOn = true },
        importLens = { globalOn = true, codeLensOn = true },
        moduleName = { globalOn = true },
        ormolu = { globalOn = true },
        pragmas = { codeActionsOn = true, completionOn = true },
        qualifyImportedIdentifiers = { globalOn = true },
        rename = { config = { crossModule = true } },
        retrie = { globalOn = true },
        semanticTokens = { globalOn = true },
        splice = { globalOn = true },
        tactics = { globalOn = true },
      },
    },
  },
  on_attach = on_attach,
})
```

---

## 第三部分：Ruby LSP

---

## 3. Ruby LSP 生态

### 3.1 Solargraph

```bash
# 安装
gem install solargraph

# 生成文档（核心库）
solargraph download-core

# 项目初始化
solargraph config .  # 生成 .solargraph.yml

# Neovim
require('lspconfig').solargraph.setup({
  cmd = { "solargraph", "stdio" },
  settings = {
    solargraph = {
      autoformat = false,
      checkGemVersion = true,
      completion = true,
      definitions = true,
      diagnostics = true,
      folding = true,
      formatting = false,
      hover = true,
      logLevel = "warn",
      references = true,
      rename = true,
      symbols = true,
    }
  }
})
```

### 3.2 ruby-lsp（Shopify 官方）

```bash
# 最推荐的现代 Ruby LSP
gem install ruby-lsp

# Neovim
require('lspconfig').ruby_lsp.setup({
  cmd = { "ruby-lsp" },
  init_options = {
    enabledFeatures = {
      codeActions = true,
      codeLens = true,
      completion = true,
      definition = true,
      diagnostics = true,
      documentHighlights = true,
      documentLink = true,
      documentSymbols = true,
      foldingRanges = true,
      formatting = true,
      hover = true,
      inlayHint = true,
      onTypeFormatting = true,
      references = true,
      rename = true,
      selectionRanges = true,
      semanticHighlighting = true,
      signatureHelp = true,
      typeHierarchy = true,
      workspaceSymbol = true,
    },
    formatter = "auto",  -- auto/rubocop/syntax_tree/none
    linters = { "rubocop", "standard" },
  }
})
```

### 3.3 steep（类型检查）

```bash
# Sorbet/RBS 类型系统 LSP
gem install steep

# Neovim
require('lspconfig').steep.setup({})
```

---

## 第四部分：PHP LSP

---

## 4. intelephense

### 4.1 简介

intelephense 是 PHP 最流行的 LSP Server，由 Ben Mewburn 开发，免费版本功能已非常完善，付费版提供更多功能。

```bash
# 安装
npm install -g intelephense

# Neovim
require('lspconfig').intelephense.setup({
  settings = {
    intelephense = {
      stubs = {
        "apache", "bcmath", "bz2", "calendar", "com_dotnet", "Core",
        "ctype", "curl", "date", "dba", "dom", "enchant", "exif",
        "FFI", "fileinfo", "filter", "fpm", "ftp", "gd", "gettext",
        "gmp", "hash", "iconv", "imap", "intl", "json", "ldap",
        "libxml", "mbstring", "meta", "mysqli", "oci8", "odbc",
        "openssl", "opentelemetry", "pcntl", "pcre", "PDO", "pdo_ibm",
        "pdo_mysql", "pdo_pgsql", "pdo_sqlite", "pgsql", "Phar",
        "posix", "pspell", "random", "readline", "Reflection",
        "session", "shmop", "SimpleXML", "snmp", "soap", "sockets",
        "sodium", "SPL", "sqlite3", "standard", "superglobals",
        "sysvmsg", "sysvsem", "sysvshm", "tidy", "tokenizer",
        "xml", "xmlreader", "xmlrpc", "xmlwriter", "xsl", "Zend OPcache",
        "zip", "zlib",
        "wordpress", "phpunit",  -- 框架 stub
      },
      environment = {
        phpVersion = "8.2",
        includePaths = { "./vendor/php-stubs", "./vendor/jetbrains/phpstorm-stubs" },
      },
      files = {
        maxSize = 5000000,
        associations = { "*.php", "*.phtml" },
        exclude = { "**/.git/**", "**/node_modules/**", "**/vendor/**" },
      },
      completion = {
        insertUseDeclaration = true,
        fullyQualifyGlobalConstantsAndFunctions = false,
        triggerParameterHints = true,
        maxItems = 100,
      },
      format = {
        enable = true,
      },
      diagnostics = {
        enable = true,
      },
    },
  },
  on_attach = on_attach,
})
```

### 4.2 phpactor

```bash
# 安装
composer require --dev phpactor/phpactor
./vendor/bin/phpactor status

# 全局安装
composer global require phpactor/phpactor
phpactor status

# Neovim
require('lspconfig').phpactor.setup({
  cmd = { "phpactor", "language-server" },
  on_attach = on_attach,
  init_options = {
    ["language_server_phpstan.enabled"] = false,
    ["language_server_psalm.enabled"] = false,
  }
})
```

### 4.3 PHP LSP 对比

| 特性 | intelephense | phpactor |
|------|-------------|---------|
| 补全质量 | 优秀 | 良好 |
| 类型推断 | 优秀 | 中等 |
| 重构 | 付费版完整 | ✓ (免费) |
| Laravel 支持 | ✓ | ✓ |
| Composer 集成 | ✓ | ✓ |
| PHPStan 集成 | ✗ | 插件 |
| Psalm 集成 | ✗ | 插件 |
| 价格 | 免费/付费 | 免费 |
| 运行时 | Node.js | PHP |

---

## 5. 参考资源

| 语言 | 资源 | 链接 |
|------|------|------|
| Lua | lua-language-server | https://github.com/LuaLS/lua-language-server |
| Lua | 配置文档 | https://luals.github.io/wiki/settings/ |
| Lua | 注释系统 | https://luals.github.io/wiki/annotations/ |
| Haskell | haskell-language-server | https://github.com/haskell/haskell-language-server |
| Haskell | HLS 文档 | https://haskell-language-server.readthedocs.io/ |
| Ruby | ruby-lsp | https://github.com/Shopify/ruby-lsp |
| Ruby | Solargraph | https://solargraph.org/ |
| Ruby | Steep | https://github.com/soutaro/steep |
| PHP | intelephense | https://intelephense.com/ |
| PHP | phpactor | https://github.com/phpactor/phpactor |
