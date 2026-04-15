# LSP 语言服务器协议 — 总览与架构调研

> 版本：2025-04 | 覆盖：LSP 3.x 完整规范

---

## 1. 历史背景

| 时间 | 事件 |
|------|------|
| 2015-06 | Microsoft 在 VS Code 中引入 OmniSharp C# 语言服务，内部采用 JSON-RPC |
| 2016-06 | Microsoft 正式发布 **Language Server Protocol 1.0**，与 Red Hat/Codenvy 联合推出 |
| 2016-09 | LSP 2.0：增加 WorkspaceEdit、增量同步 |
| 2017-04 | LSP 3.0：CodeAction、DocumentHighlight |
| 2018-05 | LSP 3.13：Work Done Progress、Call Hierarchy 草案 |
| 2019-06 | LSP 3.15：Progress notification、SelectionRange |
| 2020-04 | LSP 3.16：Semantic Tokens（语义高亮）、Call Hierarchy 正式化 |
| 2021-06 | LSP 3.17：Type Hierarchy、Inlay Hints、Notebooks |
| 2023-05 | LSP 3.17.0（当前稳定版） |
| 2024-Q3 | LSP 3.18 草案：Diagnostic Pull Model 增强、MCP 集成讨论 |

---

## 2. 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                        编辑器 / IDE                          │
│  ┌──────────┐    JSON-RPC 2.0     ┌─────────────────────┐  │
│  │  LSP     │◄───────────────────►│   Language Server   │  │
│  │  Client  │   stdio / socket    │   (独立进程)         │  │
│  └──────────┘                    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 传输层

| 传输方式 | 说明 | 典型使用 |
|----------|------|----------|
| **stdio** | 标准输入/输出，最常见 | 几乎所有 LSP Server |
| **TCP socket** | 本地端口，支持多客户端 | clangd `--enable-process-picker` |
| **pipe (Windows)** | Named pipe | OmniSharp on Windows |
| **WebSocket** | 浏览器端 IDE | Theia、Eclipse Che |

### 2.2 消息类型

```
LSP 消息
├── Request (id + method + params)  →  Server 必须回复 Response
├── Response (id + result/error)    →  对应 Request 的回复
└── Notification (method + params)  →  单向，无需回复
    ├── Client → Server: textDocument/didOpen, didChange...
    └── Server → Client: textDocument/publishDiagnostics...
```

---

## 3. 完整能力矩阵 (LSP 3.17)

### 3.1 文本同步

| 能力 | 说明 |
|------|------|
| `textDocument/didOpen` | 文件打开通知 |
| `textDocument/didChange` | 内容变更（全量/增量） |
| `textDocument/didSave` | 保存通知 |
| `textDocument/didClose` | 关闭通知 |
| `textDocument/willSave` | 保存前通知（可取消） |

### 3.2 语言特性

| 特性 | Method | 版本引入 |
|------|--------|---------|
| 代码补全 | `textDocument/completion` | 1.0 |
| 悬停信息 | `textDocument/hover` | 1.0 |
| 签名帮助 | `textDocument/signatureHelp` | 1.0 |
| 跳转定义 | `textDocument/definition` | 1.0 |
| 跳转声明 | `textDocument/declaration` | 3.14 |
| 跳转实现 | `textDocument/implementation` | 3.6 |
| 类型定义 | `textDocument/typeDefinition` | 3.6 |
| 引用查找 | `textDocument/references` | 1.0 |
| 文档高亮 | `textDocument/documentHighlight` | 1.0 |
| 文档符号 | `textDocument/documentSymbol` | 1.0 |
| 代码动作 | `textDocument/codeAction` | 1.0 |
| 代码镜头 | `textDocument/codeLens` | 1.0 |
| 文档链接 | `textDocument/documentLink` | 3.0 |
| 颜色提取 | `textDocument/documentColor` | 3.6 |
| 格式化 | `textDocument/formatting` | 1.0 |
| 范围格式化 | `textDocument/rangeFormatting` | 1.0 |
| 重命名 | `textDocument/rename` | 1.0 |
| 折叠范围 | `textDocument/foldingRange` | 3.10 |
| 语义标记 | `textDocument/semanticTokens` | 3.16 |
| Inlay Hints | `textDocument/inlayHint` | 3.17 |
| 诊断拉取 | `textDocument/diagnostic` | 3.17 |
| 调用层次 | `textDocument/callHierarchy` | 3.16 |
| 类型层次 | `textDocument/typeHierarchy` | 3.17 |
| 选择范围 | `textDocument/selectionRange` | 3.15 |
| Monikers | `textDocument/moniker` | 3.16 |

### 3.3 工作空间特性

| 特性 | Method |
|------|--------|
| 工作空间符号 | `workspace/symbol` |
| 执行命令 | `workspace/executeCommand` |
| 工作空间编辑 | `workspace/applyEdit` |
| 配置变更 | `workspace/didChangeConfiguration` |
| 监视文件 | `workspace/didChangeWatchedFiles` |

---

## 4. JSON-RPC 消息格式详解

### 4.1 Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "textDocument/completion",
  "params": {
    "textDocument": { "uri": "file:///path/to/file.py" },
    "position": { "line": 10, "character": 5 },
    "context": { "triggerKind": 1 }
  }
}
```

### 4.2 Response (Success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "isIncomplete": false,
    "items": [
      {
        "label": "print",
        "kind": 3,
        "detail": "builtin function",
        "documentation": "Print objects to text stream",
        "insertText": "print(${1:object})",
        "insertTextFormat": 2
      }
    ]
  }
}
```

### 4.3 Response (Error)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

### 4.4 消息头格式

```
Content-Length: 158\r\n
Content-Type: application/vscode-jsonrpc; charset=utf8\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"initialize",...}
```

---

## 5. 初始化握手流程

```
Client                                    Server
  │                                          │
  │──── initialize (capabilities) ──────────►│
  │                                          │ (服务端准备)
  │◄─── initializeResult (capabilities) ────│
  │                                          │
  │──── initialized (notification) ─────────►│
  │                                          │
  │  ── 正常工作阶段 ──────────────────────  │
  │                                          │
  │──── shutdown ────────────────────────────►│
  │◄─── shutdown response ───────────────────│
  │──── exit (notification) ─────────────────►│
```

### ClientCapabilities 关键字段 (示例)

```json
{
  "workspace": {
    "workspaceFolders": true,
    "configuration": true,
    "semanticTokens": { "refreshSupport": true }
  },
  "textDocument": {
    "synchronization": {
      "dynamicRegistration": true,
      "willSave": true,
      "willSaveWaitUntil": true,
      "didSave": true
    },
    "completion": {
      "completionItem": {
        "snippetSupport": true,
        "documentationFormat": ["markdown", "plaintext"],
        "resolveSupport": { "properties": ["documentation", "detail"] }
      }
    },
    "semanticTokens": {
      "tokenTypes": ["namespace", "type", "class", "function", ...],
      "formats": ["relative"]
    }
  }
}
```

---

## 6. Semantic Tokens 详解 (3.16+)

语义标记是 LSP 3.16 最重要的特性，提供超越 TextMate 语法的精确着色。

### 6.1 编码格式 (Delta)

服务端返回 5 个整数一组的数组：
```
[deltaLine, deltaStartChar, length, tokenType, tokenModifiers]
```

```python
# 示例：解码 semantic tokens
tokens_raw = [0, 0, 5, 0, 1,   # 第1个token: line0, char0, len5, type=namespace, mod=declaration
              0, 6, 3, 1, 0]    # 第2个token: same line, char6, len3, type=type

def decode_tokens(raw, legend):
    tokens = []
    line, char = 0, 0
    for i in range(0, len(raw), 5):
        delta_line = raw[i]
        delta_char = raw[i+1]
        length     = raw[i+2]
        type_idx   = raw[i+3]
        mods_bits  = raw[i+4]
        
        if delta_line != 0:
            line += delta_line
            char = delta_char
        else:
            char += delta_char
        
        tokens.append({
            "line": line, "char": char, "length": length,
            "type": legend["tokenTypes"][type_idx],
            "modifiers": [legend["tokenModifiers"][j] 
                         for j in range(len(legend["tokenModifiers"])) 
                         if mods_bits & (1 << j)]
        })
    return tokens
```

---

## 7. LSP Server 实现框架汇总

### 7.1 各语言 LSP Server SDK

| 语言 | 框架 | 仓库 |
|------|------|------|
| **Python** | `pygls` | github.com/openlawlibrary/pygls |
| **Python** | `lsp-types` (仅类型) | github.com/microsoft/lsprotocol |
| **TypeScript** | `vscode-languageserver-node` | github.com/microsoft/vscode-languageserver-node |
| **Rust** | `tower-lsp` | github.com/ebkalderon/tower-lsp |
| **Rust** | `lsp-server` | github.com/rust-lang/rust-analyzer (内部) |
| **Go** | `glsp` | github.com/tliron/glsp |
| **Go** | `protocol` | golang.org/x/tools/internal/lsp/protocol |
| **Java** | `lsp4j` | github.com/eclipse-langserver/lsp4j |
| **C#** | `OmniSharp.Extensions.LanguageServer` | github.com/OmniSharp/csharp-language-server-protocol |
| **Haskell** | `lsp` | hackage.haskell.org/package/lsp |
| **OCaml** | `linol` | github.com/c-cube/linol |

### 7.2 pygls 示例（自建 LSP Server）

```python
from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    CompletionItem, CompletionList, CompletionParams,
    TEXT_DOCUMENT_HOVER, Hover, HoverParams, MarkupContent, MarkupKind,
)

server = LanguageServer("my-language-server", "v0.1")

@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams) -> CompletionList:
    items = [
        CompletionItem(label="Hello"),
        CompletionItem(label="World"),
    ]
    return CompletionList(is_incomplete=False, items=items)

@server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: HoverParams) -> Hover:
    return Hover(
        contents=MarkupContent(kind=MarkupKind.Markdown, value="**Hello from LSP!**")
    )

if __name__ == "__main__":
    server.start_io()
```

---

## 8. 主流编辑器 LSP 客户端集成

### 8.1 Neovim (nvim-lspconfig)

```lua
-- 最小化配置示例
require('lspconfig').pyright.setup({
  on_attach = function(client, bufnr)
    local opts = { buffer = bufnr }
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'K',  vim.lsp.buf.hover, opts)
    vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
  end,
  settings = {
    python = { analysis = { typeCheckingMode = "basic" } }
  }
})
```

### 8.2 VS Code (Extension API)

```typescript
// extension.ts
import * as vscode from 'vscode';
import { LanguageClient, ServerOptions, TransportKind } from 'vscode-languageclient/node';

export function activate(context: vscode.ExtensionContext) {
  const serverOptions: ServerOptions = {
    run: { command: 'my-lsp-server', transport: TransportKind.stdio },
    debug: { command: 'my-lsp-server', args: ['--debug'], transport: TransportKind.stdio }
  };
  const client = new LanguageClient('myLanguage', 'My Language', serverOptions, {
    documentSelector: [{ scheme: 'file', language: 'mylang' }]
  });
  client.start();
}
```

### 8.3 Emacs (eglot / lsp-mode)

```emacs-lisp
;; eglot (内置 Emacs 29+)
(add-hook 'python-mode-hook 'eglot-ensure)
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '(python-mode . ("pyright-langserver" "--stdio"))))

;; lsp-mode
(use-package lsp-mode
  :hook ((python-mode . lsp-deferred))
  :commands lsp
  :config
  (setq lsp-idle-delay 0.1
        lsp-log-io nil
        lsp-completion-provider :none))
```

### 8.4 Helix

```toml
# languages.toml
[[language]]
name = "python"
language-servers = ["pyright", "ruff"]

[language-server.pyright]
command = "pyright-langserver"
args = ["--stdio"]

[language-server.ruff]
command = "ruff-lsp"
```

---

## 9. LSIF — 静态索引格式

LSIF (Language Server Index Format) 是 LSP 的"离线版本"，用于代码搜索/代码导航（GitHub、Sourcegraph）。

```
LSIF Graph 示意：

vertex:document  ──── contains ──── vertex:range
                                         │
                                    resultSet
                                    ├── definitionResult
                                    ├── referencesResult
                                    └── hoverResult
```

### LSIF 生成工具

| 语言 | 工具 |
|------|------|
| Go | `lsif-go` |
| TypeScript | `lsif-tsc` |
| Python | `lsif-py` |
| Java | `lsif-java` |
| C++ | `lsif-clang` |
| Rust | `rust-analyzer --dump-lsif` |

---

## 10. LSP 调试工具

### 10.1 日志追踪

```bash
# Neovim 开启 LSP 日志
vim.lsp.set_log_level("debug")
# 日志位置
:lua print(vim.lsp.get_log_path())

# VS Code: 开发者工具 → 控制台 → 搜索 LSP
```

### 10.2 lsp-devtools

```bash
pip install lsp-devtools

# 拦截并记录 LSP 消息
lsp-devtools record -- pyright-langserver --stdio

# 可视化分析
lsp-devtools tui
```

### 10.3 netcat 手动测试

```bash
# 手动发送 initialize 请求
MSG='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"processId":null,"rootUri":null,"capabilities":{}}}'
printf "Content-Length: ${#MSG}\r\n\r\n${MSG}" | pyright-langserver --stdio
```

---

## 11. 性能优化要点

| 优化项 | 建议 |
|--------|------|
| **增量同步** | 使用 `TextDocumentSyncKind.Incremental` 而非 `Full` |
| **防抖** | 编辑器侧设置 100~500ms 延迟再触发诊断 |
| **部分结果** | 使用 `$/progress` 流式返回大结果 |
| **工作区索引** | 后台异步建立索引，避免阻塞 |
| **取消请求** | 实现 `$/cancelRequest` 取消过期请求 |
| **缓存** | 缓存 AST 解析结果，按文件 hash 失效 |

---

## 12. 参考资源

| 资源 | 链接 |
|------|------|
| 官方规范 | https://microsoft.github.io/language-server-protocol/ |
| LSP 3.17 规范 | https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/ |
| awesome-lsp-servers | https://github.com/ozdrgnaDiies/awesome-lsp-servers |
| mason.nvim 注册表 | https://github.com/mason-org/mason-registry |
| lsp-devtools | https://github.com/swyddfa/lsp-devtools |
| lsprotocol (MS官方类型) | https://github.com/microsoft/lsprotocol |
