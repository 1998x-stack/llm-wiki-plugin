# 数据/标记/工具语言 LSP 完整调研

> 版本：2025-04 | 覆盖：JSON / YAML / SQL / Bash / Markdown / HTML/CSS / TOML / XML / Docker

---

## 1. JSON LSP

### 1.1 vscode-json-languageserver

由 Microsoft 开发，提供 JSON Schema 验证、补全、悬停等功能。

```bash
# 安装
npm install -g vscode-langservers-extracted

# 包含：vscode-json-language-server, vscode-css-language-server,
#        vscode-html-language-server, vscode-eslint-language-server

# 验证
vscode-json-language-server --version
```

#### Neovim 配置

```lua
local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities.textDocument.completion.completionItem.snippetSupport = true

require('lspconfig').jsonls.setup({
  capabilities = capabilities,
  settings = {
    json = {
      schemas = require('schemastore').json.schemas(),
      validate = { enable = true },
      format = { enable = true },
    },
  },
  on_attach = on_attach,
})
```

### 1.2 SchemaStore 集成

```lua
-- 安装 schemastore.nvim 插件
-- 提供数千个 JSON Schema（package.json, tsconfig, .eslintrc 等）
require('schemastore').json.schemas({
  select = {
    'package.json',
    'tsconfig.json',
    '.eslintrc',
    'GitHub Actions',
    'docker-compose.yml',
    'Prettier',
    'pyproject.toml',
  },
  extra = {
    {
      description = 'My custom schema',
      fileMatch = { 'config.json', '.config.json' },
      url = 'https://example.com/schema.json',
    }
  }
})
```

---

## 2. YAML LSP

### 2.1 yaml-language-server

```bash
# 安装
npm install -g yaml-language-server

# 验证
yaml-language-server --version
```

#### 配置

```lua
require('lspconfig').yamlls.setup({
  capabilities = capabilities,
  settings = {
    yaml = {
      keyOrdering = false,
      format = { enable = true, singleQuote = false, bracketSpacing = true },
      validate = true,
      hover = true,
      completion = true,
      schemaStore = { enable = false, url = "" },  -- 使用 schemastore.nvim
      schemas = require('schemastore').yaml.schemas(),
      -- 自定义 Schema 映射
      customTags = [
        "!And scalar", "!And mapping", "!And sequence",
        "!If scalar", "!If mapping", "!If sequence",
        "!Not scalar", "!Not mapping", "!Not sequence",
        "!Equals scalar", "!Equals mapping", "!Equals sequence",
        "!Or scalar", "!Or mapping", "!Or sequence",
      ],
    },
  },
  on_attach = on_attach,
})
```

#### .yamllint 配置

```yaml
# .yamllint
extends: default
rules:
  line-length: { max: 120 }
  truthy:
    allowed-values: ['true', 'false']
    check-keys: false
```

---

## 3. SQL LSP

### 3.1 sqls

```bash
# 安装
go install github.com/sqls-server/sqls@latest

# 配置文件 ~/.config/sqls/config.yml
connections:
  - alias: dev
    driver: mysql
    dataSourceName: "root:password@tcp(127.0.0.1:3306)/mydb"
  - alias: prod
    driver: postgresql
    dataSourceName: "host=localhost dbname=mydb user=admin password=secret sslmode=disable"
```

```lua
require('lspconfig').sqls.setup({
  on_attach = function(client, bufnr)
    require('sqls').on_attach(client, bufnr)
  end,
  settings = {
    sqls = {
      connections = {
        {
          driver = "mysql",
          dataSourceName = "root:@tcp(127.0.0.1:13306)/world",
        },
      },
    },
  },
})
```

### 3.2 sql-language-server

```bash
# 安装
npm install -g sql-language-server

# 项目配置 .sqllsrc.json
{
  "connections": [
    {
      "name": "mydb",
      "adapter": "mysql",
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "",
      "database": "mydb",
      "projectPaths": ["/home/user/myproject"]
    }
  ]
}
```

---

## 4. Bash LSP

### 4.1 bash-language-server

```bash
# 安装
npm install -g bash-language-server

# 需要 shellcheck（诊断）
sudo apt install shellcheck
brew install shellcheck
```

```lua
require('lspconfig').bashls.setup({
  cmd = { "bash-language-server", "start" },
  filetypes = { "sh", "bash" },
  settings = {
    bashIde = {
      globPattern = "*@(.sh|.inc|.bash|.command)",
      enableSourceErrorDiagnostics = false,
      shellcheckPath = "shellcheck",
      shellcheckArguments = "-e SC2148,SC2116",
      includeAllWorkspaceSymbols = true,
      logLevel = "info",
      backgroundAnalysisMaxFiles = 500,
    },
  },
  on_attach = on_attach,
})
```

### 4.2 shfmt 集成

```bash
# 安装 shfmt
go install mvdan.cc/sh/v3/cmd/shfmt@latest
brew install shfmt

# 使用 conform.nvim 格式化
require('conform').setup({
  formatters_by_ft = {
    sh = { "shfmt" },
    bash = { "shfmt" },
  },
  formatters = {
    shfmt = {
      prepend_args = { "-i", "2", "-ci", "-bn" },
    },
  },
})
```

---

## 5. Markdown LSP

### 5.1 marksman

```bash
# 安装
# GitHub Releases 下载
wget https://github.com/artempyanykh/marksman/releases/latest/download/marksman-linux-x64
chmod +x marksman-linux-x64
mv marksman-linux-x64 ~/.local/bin/marksman

# Homebrew
brew install marksman

# mason.nvim
:MasonInstall marksman
```

```lua
require('lspconfig').marksman.setup({
  filetypes = { "markdown", "markdown.mdx" },
  root_dir = require('lspconfig').util.root_pattern(".marksman.toml", ".git"),
  on_attach = on_attach,
})
```

### 5.2 markdown-oxide

```bash
# 安装（Obsidian-like 工作流）
cargo install --locked markdown-oxide

# Neovim
require('lspconfig').markdown_oxide.setup({
  capabilities = vim.tbl_deep_extend(
    "force", capabilities,
    { workspace = { didChangeWatchedFiles = { dynamicRegistration = true } } }
  ),
  on_attach = on_attach,
})
```

### 5.3 vale-ls（文档写作风格检查）

```bash
# 安装 vale
brew install vale
# 配置 .vale.ini
StylesPath = styles
MinAlertLevel = suggestion
[*.md]
BasedOnStyles = Vale, Google, write-good
```

```lua
require('lspconfig').vale_ls.setup({
  filetypes = { "markdown", "text", "rst", "asciidoc" },
  on_attach = on_attach,
})
```

---

## 6. HTML / CSS LSP

### 6.1 vscode-html-languageserver

```bash
npm install -g vscode-langservers-extracted
```

```lua
require('lspconfig').html.setup({
  capabilities = capabilities,
  filetypes = { "html", "htmldjango", "jinja", "templ" },
  init_options = {
    configurationSection = { "html", "css", "javascript" },
    embeddedLanguages = { css = true, javascript = true },
    provideFormatter = true,
  },
  settings = {
    html = {
      format = {
        enable = true,
        templating = true,
        wrapLineLength = 120,
        wrapAttributes = "auto",
        indentInnerHtml = false,
      },
      hover = {
        documentation = true,
        references = true,
      },
      completion = {
        attributeDefaultValue = "doublequotes",
      },
      validate = {
        scripts = true,
        styles = true,
      },
    },
  },
})
```

### 6.2 CSS / SCSS / Less

```lua
require('lspconfig').cssls.setup({
  capabilities = capabilities,
  settings = {
    css = {
      validate = true,
      lint = { unknownAtRules = "ignore" },
    },
    scss = { validate = true },
    less = { validate = true },
  },
})

-- Tailwind CSS
require('lspconfig').tailwindcss.setup({
  settings = {
    tailwindCSS = {
      experimental = {
        classRegex = {
          { "cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]" },
          { "cx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)" },
        },
      },
      validate = true,
      lint = {
        cssConflict = "warning",
        invalidApply = "error",
        invalidScreen = "error",
        invalidVariant = "error",
        invalidConfigPath = "error",
        invalidTailwindDirective = "error",
        recommendedVariantOrder = "warning",
      },
    },
  },
})
```

---

## 7. TOML LSP

### 7.1 taplo

```bash
# 安装（Rust 实现）
cargo install taplo-cli --features lsp

# 或 npm
npm install -g @taplo/cli

# 预构建：https://github.com/tamasfe/taplo/releases

# mason.nvim
:MasonInstall taplo
```

```lua
require('lspconfig').taplo.setup({
  settings = {
    taplo = {
      schema = {
        enabled = true,
        associations = {
          ["^(.*(/|\\\\)Cargo\\.toml|Cargo\\.toml)$"] =
            "https://raw.githubusercontent.com/SchemaStore/schemastore/master/src/schemas/json/cargo.json",
          ["^(.*(/|\\\\)pyproject\\.toml|pyproject\\.toml)$"] =
            "https://json.schemastore.org/pyproject.json",
        },
        repositoryEnabled = true,
        repositoryUrl = "https://taplo.tamasfe.dev/schema_index.json",
      },
      formatter = {
        alignEntries = false,
        alignComments = true,
        arrayTrailingComma = true,
        arrayAutoExpand = true,
        arrayAutoCollapse = true,
        compactArrays = true,
        compactInlineTables = false,
        indentTables = false,
        indentEntries = false,
        inlineTableExpand = true,
        trailingNewline = true,
        reorderKeys = false,
        allowedBlankLines = 2,
        indentString = "  ",
        columnWidth = 80,
      },
    },
  },
  on_attach = on_attach,
})
```

---

## 8. XML LSP

### 8.1 lemminx（Eclipse LemMinX）

```bash
# 安装
# 下载预构建（native image）
wget https://github.com/eclipse/lemminx/releases/latest/download/lemminx-linux.zip
unzip lemminx-linux.zip
chmod +x lemminx-linux
mv lemminx-linux ~/.local/bin/lemminx

# mason.nvim
:MasonInstall lemminx
```

```lua
require('lspconfig').lemminx.setup({
  settings = {
    xml = {
      catalogs = {},
      logs = { client = false },
      format = {
        enabled = true,
        joinCDATALines = false,
        joinCommentLines = false,
        joinContentLines = false,
        spaceBeforeEmptyCloseTag = true,
        formatComments = true,
        preserveAttributeLineBreaks = false,
        preservedNewlines = 2,
        insertSpaces = true,
        tabSize = 2,
      },
      validation = {
        enabled = true,
        schema = { enabled = "always" },
        noGrammar = "hint",
      },
    },
  },
  on_attach = on_attach,
})
```

---

## 9. Docker LSP

### 9.1 dockerfile-language-server

```bash
npm install -g dockerfile-language-server-nodejs
```

```lua
require('lspconfig').dockerls.setup({
  settings = {
    docker = {
      languageserver = {
        formatter = { ignoreMultilineInstructions = true },
      },
    },
  },
  on_attach = on_attach,
})
```

### 9.2 docker-compose-language-service

```bash
npm install -g @microsoft/compose-language-service
```

```lua
require('lspconfig').docker_compose_language_service.setup({
  filetypes = { "yaml.docker-compose" },
  root_dir = require('lspconfig').util.root_pattern(
    "docker-compose.yml", "docker-compose.yaml",
    "compose.yml", "compose.yaml"
  ),
  on_attach = on_attach,
})
```

---

## 10. Terraform / HCL LSP

### 10.1 terraform-ls

```bash
# 安装（HashiCorp 官方）
brew install hashicorp/tap/terraform-ls

# 下载：https://releases.hashicorp.com/terraform-ls/

# mason.nvim
:MasonInstall terraform-ls
```

```lua
require('lspconfig').terraformls.setup({
  filetypes = { "terraform", "tf", "terraform-vars" },
  on_attach = on_attach,
})

-- tfmt 格式化
require('conform').setup({
  formatters_by_ft = {
    terraform = { "terraform_fmt" },
    tf = { "terraform_fmt" },
  },
})
```

---

## 11. 综合对比表

| 语言 | LSP Server | npm/cargo/go/其他 | 速度 | Schema 支持 |
|------|-----------|------------------|------|------------|
| JSON | vscode-json-languageserver | npm | 快 | ✓ (SchemaStore) |
| YAML | yaml-language-server | npm | 快 | ✓ (SchemaStore) |
| TOML | taplo | cargo/npm | 极快 | ✓ |
| XML | lemminx | native binary | 快 | ✓ |
| SQL | sqls / sql-language-server | go / npm | 中 | DB Schema |
| Bash | bash-language-server | npm | 快 | - |
| Markdown | marksman | binary | 快 | - |
| HTML | vscode-html-languageserver | npm | 快 | - |
| CSS/SCSS | vscode-css-languageserver | npm | 快 | - |
| Dockerfile | dockerfile-ls | npm | 快 | - |
| Terraform | terraform-ls | binary (Go) | 中 | Registry |

---

## 12. 通用配置技巧

### 12.1 mason.nvim 批量安装

```lua
require('mason-lspconfig').setup({
  ensure_installed = {
    -- 数据/标记
    "jsonls", "yamlls", "taplo", "lemminx",
    -- Shell/脚本
    "bashls",
    -- Web
    "html", "cssls", "tailwindcss",
    -- DevOps
    "dockerls", "docker_compose_language_service", "terraformls",
    -- 文档
    "marksman",
  }
})
```

### 12.2 schemastore 自动 Schema

```lua
-- 自动为所有 JSON/YAML 文件关联 Schema
require('lspconfig').jsonls.setup({
  settings = {
    json = {
      schemas = vim.list_extend(
        require('schemastore').json.schemas(),
        {
          -- 自定义公司内部 Schema
          { fileMatch = { "infra/*.json" }, url = "https://internal.company.com/schemas/infra.json" }
        }
      ),
    },
  },
})
```

---

## 13. 参考资源

| 资源 | 链接 |
|------|------|
| vscode-langservers-extracted | https://github.com/hrsh7th/vscode-langservers-extracted |
| yaml-language-server | https://github.com/redhat-developer/yaml-language-server |
| SchemaStore | https://www.schemastore.org/ |
| schemastore.nvim | https://github.com/b0o/schemastore.nvim |
| bash-language-server | https://github.com/bash-lsp/bash-language-server |
| marksman | https://github.com/artempyanykh/marksman |
| taplo | https://taplo.tamasfe.dev/ |
| lemminx | https://github.com/eclipse/lemminx |
| sqls | https://github.com/sqls-server/sqls |
| terraform-ls | https://github.com/hashicorp/terraform-ls |
