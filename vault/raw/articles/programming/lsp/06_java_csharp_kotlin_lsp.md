# Java / C# / Kotlin LSP 工具完整调研

> 版本：2025-04 | 覆盖：eclipse.jdt.ls / OmniSharp / roslyn / kotlin-language-server

---

## 第一部分：Java LSP

---

## 1. eclipse.jdt.ls（Java Language Server）

### 1.1 简介与历史

eclipse.jdt.ls 是基于 Eclipse JDT（Java Development Tools）的 LSP Server，由 Red Hat 维护，是最主流的 Java LSP 实现。

| 时间 | 版本 | 特性 |
|------|------|------|
| 2016-10 | 0.1.0 | 首次发布（随 VS Code Java 插件） |
| 2018-09 | 0.32.0 | Gradle 支持改进 |
| 2019-12 | 0.54.0 | 重构支持 |
| 2020-09 | 0.70.0 | Java 15 支持 |
| 2021-09 | 1.3.0 | Java 17 支持 |
| 2022-03 | 1.10.0 | Jakarta EE 命名 |
| 2023-09 | 1.30.0 | Java 21 支持 |
| 2024-04 | 1.37.0 | Java 22 支持 |
| 2024-10 | 1.40.x | Java 23，当前稳定版 |

**仓库**：https://github.com/eclipse-jdtls/eclipse.jdt.ls

### 1.2 架构

```
eclipse.jdt.ls
├── 基于 Eclipse Equinox OSGi 容器
├── JDT Core（Java 解析、类型解析）
├── JDT UI（重构、代码生成）
├── M2Eclipse（Maven 集成）
├── Buildship（Gradle 集成）
└── LSP 协议层（自定义扩展）
```

### 1.3 安装

```bash
# 方式一：下载预构建包
# https://download.eclipse.org/jdtls/milestones/
VERSION="1.40.0"
TIMESTAMP="202409261450"
wget "https://download.eclipse.org/jdtls/milestones/${VERSION}/jdt-language-server-${VERSION}-${TIMESTAMP}.tar.gz"
tar -xzf jdt-language-server-*.tar.gz -C ~/.local/share/jdtls

# 方式二：mason.nvim
:MasonInstall jdtls

# 方式三：包管理器
# AUR
yay -S jdtls
```

### 1.4 从源码构建

```bash
# 前置：JDK >= 17, Maven 3.x

git clone https://github.com/eclipse-jdtls/eclipse.jdt.ls.git
cd eclipse.jdt.ls

# 构建（需要 Maven）
./mvnw clean verify -DskipTests

# 带测试构建
./mvnw clean verify

# 产出目录
ls org.eclipse.jdt.ls.product/target/repository/

# 打包为 tar.gz
ls org.eclipse.jdt.ls.product/target/jdt-language-server-*.tar.gz
```

### 1.5 Neovim 集成（nvim-jdtls）

```lua
-- 使用 nvim-jdtls 插件（强烈推荐）
local jdtls = require('jdtls')

-- 数据目录（每个项目独立）
local home = os.getenv('HOME')
local workspace_path = home .. "/.local/share/eclipse/" ..
    vim.fn.fnamemodify(vim.fn.getcwd(), ':p:h:t')

-- JDK 路径（runtimes）
local runtimes = {
  { name = "JavaSE-11", path = "/usr/lib/jvm/java-11-openjdk" },
  { name = "JavaSE-17", path = "/usr/lib/jvm/java-17-openjdk", default = true },
  { name = "JavaSE-21", path = "/usr/lib/jvm/java-21-openjdk" },
}

local config = {
  cmd = {
    "java",
    "-Declipse.application=org.eclipse.jdt.ls.core.id1",
    "-Dosgi.bundles.defaultStartLevel=4",
    "-Declipse.product=org.eclipse.jdt.ls.core.product",
    "-Dlog.protocol=true",
    "-Dlog.level=ALL",
    "-Xmx2g",
    "--add-modules=ALL-SYSTEM",
    "--add-opens", "java.base/java.util=ALL-UNNAMED",
    "--add-opens", "java.base/java.lang=ALL-UNNAMED",
    "-jar", vim.fn.glob(
      home .. "/.local/share/nvim/mason/packages/jdtls/plugins/org.eclipse.equinox.launcher_*.jar"
    ),
    "-configuration", home .. "/.local/share/nvim/mason/packages/jdtls/config_linux",
    "-data", workspace_path,
  },
  root_dir = require('jdtls.setup').find_root(
    { ".git", "mvnw", "gradlew", "pom.xml", "build.gradle" }
  ),
  settings = {
    java = {
      home = "/usr/lib/jvm/java-17-openjdk",
      eclipse = { downloadSources = true },
      configuration = {
        updateBuildConfiguration = "interactive",
        runtimes = runtimes,
      },
      maven = { downloadSources = true },
      implementationsCodeLens = { enabled = true },
      referencesCodeLens = { enabled = true },
      references = { includeDecompiledSources = true },
      format = {
        enabled = true,
        settings = {
          url = home .. "/.config/nvim/eclipse-java-google-style.xml",
          profile = "GoogleStyle",
        },
      },
      contentProvider = { preferred = "fernflower" },
      completion = {
        favoriteStaticMembers = {
          "org.junit.Assert.*",
          "org.mockito.Mockito.*",
        },
        filteredTypes = { "com.sun.*", "sun.*", "jdk.*" },
        guessMethodArguments = true,
      },
      sources = {
        organizeImports = {
          starThreshold = 9999,
          staticStarThreshold = 9999,
        },
      },
      codeGeneration = {
        toString = { template = "${object.className}{${member.name()}=${member.value}, ${otherMembers}}" },
        useBlocks = true,
      },
    },
  },
  init_options = {
    bundles = {
      -- java-debug 调试支持
      vim.fn.glob(home .. "/.local/share/nvim/mason/packages/java-debug-adapter/extension/server/com.microsoft.java.debug.plugin-*.jar"),
      -- vscode-java-test 测试支持
    },
  },
  on_attach = function(client, bufnr)
    jdtls.setup_dap({ hotcodereplace = "auto" })
    jdtls.setup.add_commands()
    on_attach(client, bufnr)
    
    -- Java 专有快捷键
    local opts = { buffer = bufnr }
    vim.keymap.set('n', '<leader>ji', jdtls.organize_imports, opts)
    vim.keymap.set('n', '<leader>jt', jdtls.test_class, opts)
    vim.keymap.set('n', '<leader>jn', jdtls.test_nearest_method, opts)
    vim.keymap.set('n', '<leader>jev', jdtls.extract_variable, opts)
    vim.keymap.set('v', '<leader>jem', jdtls.extract_method, opts)
    vim.keymap.set('n', '<leader>jec', jdtls.extract_constant, opts)
  end,
}

jdtls.start_or_attach(config)
```

---

## 第二部分：C# LSP

---

## 2. OmniSharp

### 2.1 简介与历史

OmniSharp 是 .NET/C# 的传统 LSP Server，基于 Roslyn。

| 版本 | 时间 | 特性 |
|------|------|------|
| 1.0 | 2015 | 首个 LSP 版本 |
| 1.35 | 2020 | .NET 5 支持 |
| 1.37 | 2021 | .NET 6, LSP 模式 |
| 1.39 | 2022 | .NET 7 |
| 1.39.11 | 2023 | 最后一个稳定版 |
| **弃用** | 2024 | Microsoft 转向 roslyn LSP |

**仓库**：https://github.com/OmniSharp/omnisharp-roslyn

### 2.2 安装（遗留支持）

```bash
# 通过 mason.nvim
:MasonInstall omnisharp

# 手动下载
# https://github.com/OmniSharp/omnisharp-roslyn/releases
wget https://github.com/OmniSharp/omnisharp-roslyn/releases/download/v1.39.11/omnisharp-linux-x64-net6.0.tar.gz

# 运行
~/.local/share/nvim/mason/packages/omnisharp/OmniSharp
```

---

## 3. roslyn（Microsoft 官方新 LSP）

### 3.1 简介

Microsoft 在 2024 年推出基于最新 Roslyn LSP protocol 的 C# 语言服务，是 OmniSharp 的官方继任者。

**仓库**：https://github.com/dotnet/vscode-csharp（VS Code 插件包含）

### 3.2 安装

```bash
# 通过 .NET SDK（推荐）
dotnet tool install --global Microsoft.CodeAnalysis.LanguageServer

# mason.nvim（使用 roslyn.nvim 插件）
# 需要先安装 mason
:MasonInstall roslyn
```

### 3.3 Neovim 集成

```lua
-- 使用 roslyn.nvim 插件
require('roslyn').setup({
  args = {
    "--stdio",
    "--logLevel", "Warning",
    "--extensionLogDirectory", vim.fs.dirname(vim.lsp.get_log_path()),
  },
  config = {
    on_attach = on_attach,
    settings = {
      ["csharp|inlay_hints"] = {
        csharp_enable_inlay_hints_for_implicit_object_creation = true,
        csharp_enable_inlay_hints_for_implicit_variable_types = true,
        csharp_enable_inlay_hints_for_lambda_parameter_types = true,
        csharp_enable_inlay_hints_for_types = true,
        dotnet_enable_inlay_hints_for_indexer_parameters = true,
        dotnet_enable_inlay_hints_for_literal_parameters = true,
        dotnet_enable_inlay_hints_for_object_creation_parameters = true,
        dotnet_enable_inlay_hints_for_other_parameters = true,
        dotnet_enable_inlay_hints_for_parameters = true,
        dotnet_suppress_inlay_hints_for_parameters_that_differ_only_by_suffix = false,
        dotnet_suppress_inlay_hints_for_parameters_that_match_argument_name = false,
        dotnet_suppress_inlay_hints_for_parameters_that_match_method_intent = false,
      },
      ["csharp|code_lens"] = {
        dotnet_enable_references_code_lens = true,
      },
    },
  },
})
```

---

## 4. csharp-ls

### 4.1 简介

`csharp-ls` 是基于 Roslyn 的社区 LSP 实现，比 OmniSharp 更轻量。

```bash
# 安装
dotnet tool install --global csharp-ls

# 验证
csharp-ls --version

# Neovim
require('lspconfig').csharp_ls.setup({
  on_attach = on_attach,
})
```

---

## 5. C# LSP 对比

| 特性 | OmniSharp | roslyn | csharp-ls |
|------|-----------|--------|-----------|
| 维护状态 | 停更 | 微软活跃 | 社区活跃 |
| .NET SDK 要求 | .NET 6/7 | .NET 8+ | .NET 8+ |
| 补全质量 | 良好 | 优秀 | 良好 |
| Inlay Hints | 有限 | 完整 | 部分 |
| 语义高亮 | 有限 | 完整 | 部分 |
| Razor/Blazor | 有限 | ✓ | ✗ |
| 多目标框架 | ✓ | ✓ | ✓ |
| 内存占用 | ~500MB | ~300MB | ~200MB |
| **推荐** | 遗留项目 | **新项目** | 轻量场景 |

---

## 第三部分：Kotlin LSP

---

## 6. kotlin-language-server

### 6.1 简介

kotlin-language-server 是 Kotlin 的社区 LSP Server，基于 Kotlin 编译器 API 构建。

**仓库**：https://github.com/fwcd/kotlin-language-server

### 6.2 版本历史

| 版本 | 时间 | 特性 |
|------|------|------|
| 0.x | 2018 | 初始实现 |
| 1.0 | 2020 | 稳定版 |
| 1.2 | 2021 | Gradle 支持改进 |
| 1.3 | 2022 | Kotlin 1.7 |
| 1.4 | 2023 | Kotlin 1.9, K2 编译器初步 |
| 1.5 | 2024 | 当前版本 |

### 6.3 安装

```bash
# 下载预构建包
VERSION="1.5.0"
wget "https://github.com/fwcd/kotlin-language-server/releases/download/${VERSION}/server.zip"
unzip server.zip -d ~/.local/share/kotlin-language-server

# mason.nvim
:MasonInstall kotlin-language-server

# 验证
~/.local/share/nvim/mason/bin/kotlin-language-server --version
```

### 6.4 从源码构建

```bash
# 前置：JDK >= 11, Gradle

git clone https://github.com/fwcd/kotlin-language-server.git
cd kotlin-language-server

# 构建
./gradlew :server:installDist
# 产出：server/build/install/server/

# 打包为 zip
./gradlew :server:distZip
# 产出：server/build/distributions/server.zip

# 运行测试
./gradlew test
```

### 6.5 Neovim 配置

```lua
require('lspconfig').kotlin_language_server.setup({
  cmd = { 
    vim.fn.expand("~/.local/share/nvim/mason/bin/kotlin-language-server") 
  },
  settings = {
    kotlin = {
      compiler = {
        jvm = {
          target = "17",
        }
      },
      completion = {
        snippets = {
          enabled = true,
        }
      },
      debugAdapter = {
        enabled = true,
        path = vim.fn.expand("~/.local/share/nvim/mason/packages/kotlin-debug-adapter/adapter/bin/kotlin-debug-adapter"),
      },
      externalSources = {
        useKlsScheme = true,
        autoConvertToKotlin = true,
      },
      inlayHints = {
        typeHints = true,
        parameterHints = true,
        chainedHints = true,
      },
    }
  },
  on_attach = on_attach,
})
```

---

## 7. Scala LSP（Metals）

### 7.1 简介

Metals 是 Scala 的官方 LSP Server，由 Scalameta 团队维护。

### 7.2 安装

```bash
# coursier（推荐）
cs install metals

# 或
brew install coursier/formulas/coursier
cs install metals

# mason.nvim
:MasonInstall metals
```

### 7.3 Neovim 集成（nvim-metals）

```lua
-- 使用 nvim-metals 插件
local metals_config = require("metals").bare_config()

metals_config.settings = {
  showImplicitArguments = true,
  showImplicitConversionsAndClasses = true,
  showInferredType = true,
  superMethodLensesEnabled = true,
  enableSemanticHighlighting = true,
  testUserInterface = "Test Explorer",
}

metals_config.init_options.statusBarProvider = "off"
metals_config.capabilities = require("cmp_nvim_lsp").default_capabilities()

metals_config.on_attach = function(client, bufnr)
  require("metals").setup_dap()
  on_attach(client, bufnr)
end

-- 启动
vim.api.nvim_create_autocmd("FileType", {
  pattern = { "scala", "sbt", "java" },
  callback = function()
    require("metals").initialize_or_attach(metals_config)
  end
})
```

---

## 8. 性能对比（JVM 系 LSP）

| LSP Server | 语言 | 启动时间 | 内存 | 索引方式 |
|------------|------|---------|------|---------|
| eclipse.jdt.ls | Java | ~5-10s | ~500MB | Eclipse JDT |
| roslyn | C# | ~3-5s | ~300MB | Roslyn 增量 |
| OmniSharp | C# | ~3-5s | ~500MB | Roslyn |
| kotlin-language-server | Kotlin | ~3-8s | ~400MB | Kotlin compiler API |
| Metals | Scala | ~10-30s | ~500MB+ | SemanticDB |

**注意**：JVM 系 LSP 启动时间较长，建议使用长期保活策略（如 `nvim-jdtls`、`nvim-metals`）。

---

## 9. 参考资源

| 资源 | 链接 |
|------|------|
| eclipse.jdt.ls | https://github.com/eclipse-jdtls/eclipse.jdt.ls |
| nvim-jdtls | https://github.com/mfussenegger/nvim-jdtls |
| OmniSharp | https://github.com/OmniSharp/omnisharp-roslyn |
| roslyn.nvim | https://github.com/seblj/roslyn.nvim |
| csharp-ls | https://github.com/razzmatazz/csharp-language-server |
| kotlin-language-server | https://github.com/fwcd/kotlin-language-server |
| Metals | https://scalameta.org/metals/ |
| nvim-metals | https://github.com/scalameta/nvim-metals |
