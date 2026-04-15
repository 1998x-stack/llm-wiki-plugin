# TypeScript / JavaScript LSP 工具完整调研

> 版本：2025-04 | 覆盖：tsserver / typescript-language-server / vtsls / biome / deno / eslint-lsp

---

## 1. 生态全景

```
TypeScript/JavaScript LSP 生态
├── typescript-language-server (tsserver wrapper)  ← 最主流，开源
├── vtsls                                          ← VS Code TS 扩展包装，更强
├── eslint-lsp / vscode-eslint                    ← ESLint 诊断
├── biome (内置 LSP)                               ← Rust 实现，超快速
├── deno lsp                                       ← Deno 内置，TypeScript 原生
├── typescript-eslint-language-service            ← TypeScript + ESLint
└── flow (Facebook)                               ← Flow 类型系统 LSP
```

---

## 2. typescript-language-server (tsserver)

### 2.1 简介与背景

`typescript-language-server` 是对 TypeScript 内置 `tsserver` 的 LSP 适配层，由 TypeFox 维护。tsserver 本身是 TypeScript 的语言服务核心，typescript-language-server 将其包装为标准 LSP 协议。

**仓库**：https://github.com/typescript-language-server/typescript-language-server

### 2.2 版本历史

| 版本 | 时间 | 主要变更 |
|------|------|---------|
| 0.x | 2016-2019 | 早期 theia-ide 版本 |
| 1.0.0 | 2021-03 | 重写，完善 LSP 3.16 支持 |
| 2.0.0 | 2021-10 | Call Hierarchy、语义高亮 |
| 3.0.0 | 2022-06 | Inlay Hints 支持 |
| 3.3.0 | 2022-11 | 支持 TS 4.9 |
| 4.0.0 | 2023-04 | 支持 TS 5.0 |
| 4.1.0 | 2023-09 | 支持 TS 5.1/5.2 |
| 4.3.0 | 2024-03 | 支持 TS 5.4 |
| 4.3.3 | 2024-09 | 当前稳定版，TS 5.6 支持 |

### 2.3 架构

```
编辑器 (LSP Client)
    │ JSON-RPC (stdio)
    ▼
typescript-language-server (Node.js)
    │ TypeScript TSServer Protocol
    │ (IPC/pipe)
    ▼
tsserver (TypeScript 内置语言服务)
    ├── 语义分析
    ├── 类型检查
    ├── 代码补全
    └── 重构
```

### 2.4 安装

```bash
# npm 全局安装
npm install -g typescript-language-server typescript

# yarn
yarn global add typescript-language-server typescript

# pnpm
pnpm add -g typescript-language-server typescript

# 项目本地安装（配合本地 TypeScript 版本）
npm install --save-dev typescript-language-server typescript

# 验证
typescript-language-server --version
```

### 2.5 从源码构建

```bash
# 前置：Node.js >= 18, npm >= 8
git clone https://github.com/typescript-language-server/typescript-language-server.git
cd typescript-language-server

# 安装依赖
npm install

# 构建
npm run build
# 产出：lib/ 目录

# 运行测试
npm test

# 打包
npm pack
# 产出：typescript-language-server-x.x.x.tgz

# 链接到全局（开发使用）
npm link
```

### 2.6 核心配置

```json
// tsconfig.json（项目级别）
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 2.7 LSP 初始化配置

```json
// initializationOptions（通过 LSP Client 传入）
{
  "hostInfo": "neovim",
  "preferences": {
    "includeInlayParameterNameHints": "all",
    "includeInlayParameterNameHintsWhenArgumentMatchesName": false,
    "includeInlayFunctionParameterTypeHints": true,
    "includeInlayVariableTypeHints": true,
    "includeInlayVariableTypeHintsWhenTypeMatchesName": false,
    "includeInlayPropertyDeclarationTypeHints": true,
    "includeInlayFunctionLikeReturnTypeHints": true,
    "includeInlayEnumMemberValueHints": true,
    "importModuleSpecifierPreference": "non-relative",
    "quotePreference": "double"
  },
  "tsserver": {
    "logDirectory": "/tmp/tsserver-logs",
    "logVerbosity": "verbose",
    "trace": "verbose"
  }
}
```

### 2.8 Neovim 配置

```lua
require('lspconfig').ts_ls.setup({  -- 注意：新版 lspconfig 改名为 ts_ls
  on_attach = function(client, bufnr)
    -- 禁用格式化（使用 prettier/biome）
    client.server_capabilities.documentFormattingProvider = false
    client.server_capabilities.documentRangeFormattingProvider = false
    on_attach(client, bufnr)
  end,
  settings = {
    typescript = {
      inlayHints = {
        includeInlayParameterNameHints = "all",
        includeInlayParameterNameHintsWhenArgumentMatchesName = false,
        includeInlayFunctionParameterTypeHints = true,
        includeInlayVariableTypeHints = true,
        includeInlayPropertyDeclarationTypeHints = true,
        includeInlayFunctionLikeReturnTypeHints = true,
        includeInlayEnumMemberValueHints = true,
      },
    },
    javascript = {
      inlayHints = {
        includeInlayParameterNameHints = "all",
        includeInlayFunctionParameterTypeHints = true,
        includeInlayVariableTypeHints = true,
      },
    },
  },
})
```

---

## 3. vtsls（VS Code TypeScript Language Server）

### 3.1 简介

vtsls 直接使用 VS Code 内置的 TypeScript 扩展逻辑，而非原始 tsserver，因此可以使用 VS Code 插件（如 `@vue/typescript-plugin`），兼容性更好，功能更接近 VS Code 体验。

**仓库**：https://github.com/yioneko/vtsls

### 3.2 与 typescript-language-server 对比

| 特性 | typescript-language-server | vtsls |
|------|---------------------------|-------|
| 底层实现 | tsserver 直接包装 | VS Code TS 扩展包装 |
| Vue/Angular 支持 | 需要额外插件 | 原生支持 TS Plugin API |
| Inlay Hints | 支持 | 支持，更准确 |
| Code Actions | 标准 | 更多（VS Code 专有） |
| 性能 | 良好 | 类似 |
| 维护 | 社区活跃 | 个人维护 |
| TS Plugin 支持 | 有限 | 完整 |

### 3.3 安装与配置

```bash
# 安装
npm install -g @vtsls/language-server typescript

# Neovim lspconfig
require('lspconfig').vtsls.setup({
  settings = {
    typescript = {
      tsdk = "node_modules/typescript/lib",  -- 使用项目本地 TS
      inlayHints = {
        parameterNames = { enabled = "all" },
        parameterTypes = { enabled = true },
        variableTypes = { enabled = true },
        returnTypes = { enabled = true },
        enumMemberValues = { enabled = true },
      },
    },
    vtsls = {
      experimental = {
        completion = {
          enableServerSideFuzzyMatch = true,
        }
      }
    }
  }
})
```

---

## 4. Biome LSP

### 4.1 简介

Biome（前身 Rome Tools）是用 Rust 编写的一体化前端工具链，内置 LSP Server，提供极快的 linting 和 formatting。

**仓库**：https://github.com/biomejs/biome

### 4.2 版本历史

| 版本 | 时间 | 特性 |
|------|------|------|
| Rome 0.x | 2021-2022 | 早期 TS 实现 |
| Rome 11 | 2022-11 | Rust 重写 |
| Biome 1.0 | 2023-08 | 品牌重命名，稳定 API |
| Biome 1.4 | 2023-12 | CSS 支持 |
| Biome 1.6 | 2024-03 | GraphQL 格式化 |
| Biome 1.8 | 2024-06 | CSS linting，.editorconfig |
| Biome 1.9 | 2024-09 | stable CSS/GraphQL |
| Biome 2.0 | 2025-03 | 插件系统，GritQL |

### 4.3 安装

```bash
# npm
npm install -g @biomejs/biome
# 或项目级别（推荐）
npm install --save-dev @biomejs/biome

# cargo
cargo install biome

# brew
brew install biome

# 启动 LSP 服务器
biome lsp-proxy
```

### 4.4 从源码构建

```bash
# 前置：Rust >= 1.75, cargo, Node.js >= 18
git clone https://github.com/biomejs/biome.git
cd biome

# 构建 CLI
cargo build --release -p biome_cli
# 产出：target/release/biome

# 构建 WASM（用于浏览器）
cargo build --release --target wasm32-unknown-unknown -p biome_wasm

# 构建 npm 包
cd packages/@biomejs/biome
npm run build

# 运行测试
cargo test --workspace
```

### 4.5 biome.json 配置

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["dist/**", "node_modules/**"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "noVar": "error",
        "useConst": "error"
      },
      "correctness": {
        "noUnusedVariables": "warn"
      },
      "suspicious": {
        "noConsoleLog": "warn"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "trailingCommas": "all",
      "semicolons": "always"
    }
  },
  "overrides": [
    {
      "include": ["**/*.test.ts"],
      "linter": {
        "rules": { "suspicious": { "noConsoleLog": "off" } }
      }
    }
  ]
}
```

### 4.6 Neovim 集成

```lua
require('lspconfig').biome.setup({
  root_dir = require('lspconfig').util.root_pattern(
    'biome.json', 'biome.jsonc', 'package.json'
  ),
})

-- 配合 conform.nvim 格式化
require('conform').setup({
  formatters_by_ft = {
    javascript = { "biome", stop_after_first = true },
    typescript = { "biome", stop_after_first = true },
    typescriptreact = { "biome", stop_after_first = true },
    json = { "biome" },
    css = { "biome" },
  }
})
```

---

## 5. ESLint LSP (eslint-lsp)

### 5.1 简介

vscode-eslint 提供了 ESLint 的 LSP 适配，通过 `vscode-eslint` 项目或独立的 `eslint-lsp` 使用。

### 5.2 安装配置

```bash
# 安装 vscode-langservers-extracted（包含 eslint, html, css, json）
npm install -g vscode-langservers-extracted

# 验证
vscode-eslint-language-server --version
```

```lua
-- Neovim 配置
require('lspconfig').eslint.setup({
  on_attach = function(client, bufnr)
    -- 保存时自动修复
    vim.api.nvim_create_autocmd("BufWritePre", {
      buffer = bufnr,
      command = "EslintFixAll",
    })
  end,
  settings = {
    workingDirectory = { mode = "auto" },
    format = true,
    codeAction = {
      disableRuleComment = { enable = true, location = "separateLine" },
      showDocumentation = { enable = true }
    },
    experimental = { useFlatConfig = false },  -- ESLint 9 flat config
  }
})
```

---

## 6. Deno LSP

### 6.1 简介

Deno 内置 LSP 服务器，支持 TypeScript/JavaScript/JSX，无需 tsconfig.json，直接支持 URL imports。

**仓库**：https://github.com/denoland/deno

### 6.2 版本历史

| Deno 版本 | LSP 特性 |
|-----------|---------|
| 1.0 | 基础 LSP 支持 |
| 1.6 | 内置 `deno lsp` 命令 |
| 1.20 | Import 补全、类型检查 |
| 1.30 | npm 包支持 |
| 1.40 | Deno 2.0 准备 |
| 2.0 | npm/Node 完整兼容 |

### 6.3 安装

```bash
# 安装 Deno（包含 LSP）
curl -fsSL https://deno.land/install.sh | sh

# Windows
irm https://deno.land/install.ps1 | iex

# 启动 LSP
deno lsp
```

### 6.4 Neovim 配置

```lua
require('lspconfig').denols.setup({
  root_dir = require('lspconfig').util.root_pattern("deno.json", "deno.jsonc"),
  settings = {
    deno = {
      enable = true,
      suggest = {
        imports = {
          hosts = {
            ["https://deno.land"] = true,
            ["https://esm.sh"] = true,
          }
        }
      },
      unstable = true,
      lint = true,
      inlayHints = {
        parameterNames = { enabled = "all" },
        parameterTypes = { enabled = true },
        variableTypes = { enabled = true },
        returnTypes = { enabled = true },
      }
    }
  }
})

-- 注意：防止 ts_ls 和 denols 冲突
require('lspconfig').ts_ls.setup({
  root_dir = require('lspconfig').util.root_pattern(
    "package.json", "tsconfig.json"
    -- 不包含 deno.json
  ),
  single_file_support = false, -- 防止单文件时启动
})
```

---

## 7. 性能对比基准

### 7.1 启动时间（中型项目，约 50k LOC）

| LSP Server | 冷启动 | 增量重载 |
|------------|--------|---------|
| typescript-language-server | ~2-4s | ~200ms |
| vtsls | ~2-4s | ~200ms |
| biome lsp | ~100ms | ~10ms |
| deno lsp | ~1-2s | ~150ms |
| eslint lsp | ~500ms | ~100ms |

### 7.2 内存占用

| LSP Server | 空项目 | 大型项目 |
|------------|--------|---------|
| typescript-language-server | ~100MB | ~500MB+ |
| vtsls | ~120MB | ~600MB+ |
| biome | ~20MB | ~50MB |
| deno lsp | ~80MB | ~300MB |

---

## 8. 推荐方案

### 8.1 纯 TypeScript 项目

```
typescript-language-server 或 vtsls
+ biome（快速 linting/formatting）
```

### 8.2 Vue 3 + TypeScript

```
vtsls（支持 @vue/typescript-plugin）
+ volar（Vue 模板分析）
+ biome 或 eslint
```

### 8.3 Deno 项目

```
deno lsp（全包）
```

### 8.4 Node.js + ESLint 传统项目

```
typescript-language-server
+ eslint-lsp
+ prettier（格式化）
```

---

## 9. 调试与故障排除

### 9.1 tsserver 日志

```bash
# 开启 tsserver 详细日志
# 在 LSP 初始化参数中添加：
{
  "tsserver": {
    "logDirectory": "/tmp/tsserver",
    "logVerbosity": "verbose"
  }
}

# 查看日志
tail -f /tmp/tsserver/ti-*.log
```

### 9.2 常见问题

```bash
# 问题：无法解析路径别名 @/
# 解决：确保 tsconfig.json 有 paths 配置，且 LSP 能读取到

# 问题：与 biome 同时使用时重复错误
# 解决：在 ts_ls 的 on_attach 中禁用 diagnosticProvider

# 问题：monorepo 中使用错误的 tsconfig
# 解决：在工作区根目录添加 tsconfig.base.json
```

---

## 10. 参考资源

| 资源 | 链接 |
|------|------|
| typescript-language-server | https://github.com/typescript-language-server/typescript-language-server |
| vtsls | https://github.com/yioneko/vtsls |
| Biome | https://github.com/biomejs/biome |
| Deno LSP | https://docs.deno.com/runtime/reference/lsp_integration/ |
| TSServer Protocol | https://github.com/microsoft/TypeScript/wiki/Standalone-Server-(tsserver) |
| vscode-langservers | https://github.com/hrsh7th/vscode-langservers-extracted |
