# SCE Tools MCP Server

A powerful Model Context Protocol (MCP) server that provides SCE (Spark Creative Editor) game development tools for AI assistants like Claude Desktop and Cursor.

## ✨ Features

- 🎮 **Complete SCE Game Development Toolchain**: Project creation, compilation, upload, and debugging
- 🔄 **Full Python CLI Replacement**: All features exposed to AI assistants via MCP protocol
- 🚀 **Multiple Environment Support**: Optimized for TapTap Code, standalone, and tapmode environments
- 📚 **Automatic Documentation Generation**: Generates comprehensive SCE development documentation
- 🔧 **Smart Path Resolution**: Automatically detects and configures development environment paths
- 📦 **Automatic Dependency Management**: Downloads and installs necessary development tools
- 🔍 **Intelligent Documentation Search**: AI-powered RAG search with hybrid BM25 + vector semantic search
- ⚡ **High-Performance Caching**: Smart caching system with automatic expiration and background processing
- 🎯 **Absolute Path Enforcement**: All tools require absolute paths for enhanced reliability
- 🎉 **TapTap Publishing Integration**: 🆕 One-click game publishing to TapTap platform with configuration management

## 🚀 Quick Start

### Installation

```bash
# Global installation (recommended)
npm install -g sce-tools-mcp

# Or use npx directly
npx sce-tools-mcp
```

### Configuration in Claude Desktop

Edit Claude Desktop configuration file (`~/.claude_desktop_config.json`):

**Option 1: TapCode Environment**
```json
{
  "mcpServers": {
    "sce-tools": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "sce-tools-mcp"],
      "env": {
        "TAPCODE_MODE": "true",
        "TDS_MCP_MAC_TOKEN": "{\"kid\":\"your_kid\",\"mac_key\":\"your_mac_key\"}",
        "SCE_ENABLE_FILE_LOGGING": "1"
      }
    }
  }
}
```

**Option 2: Standalone Environment**
```json
{
  "mcpServers": {
    "sce-tools": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "sce-tools-mcp"],
      "env": {
        "SCE_TAP_TOKEN": "your_sce_tap_token",
        "SCE_ENABLE_FILE_LOGGING": "1"
      }
    }
  }
}
```

### Configuration in Cursor

Add to Cursor MCP configuration file (`~/.cursor/mcp.json`):

**Option 1: TapCode Environment**
```json
{
  "mcpServers": {
    "sce-tools": {
      "command": "npx",
      "args": ["-y", "sce-tools-mcp"],
      "env": {
        "TAPCODE_MODE": "true",
        "TDS_MCP_MAC_TOKEN": "{\"kid\":\"your_kid\",\"mac_key\":\"your_mac_key\"}",
        "SCE_ENABLE_FILE_LOGGING": "1"
      }
    }
  }
}
```

**Option 2: Standalone Environment**
```json
{
  "mcpServers": {
    "sce-tools": {
      "command": "npx",
      "args": ["-y", "sce-tools-mcp"],
      "env": {
        "SCE_TAP_TOKEN": "your_sce_tap_token",
        "SCE_ENABLE_FILE_LOGGING": "1"
      }
    }
  }
}
```

## 🎯 Main Features

### Universal SCE Development Tools

All tools support multiple environments and require **absolute paths** for enhanced reliability:

- **`create`**: Initialize new SCE game projects
  - Automatically apply for project ID (TapCode environment)
  - Create project copies from templates
  - Setup workspace links and configuration
  - Generate comprehensive development documentation
  - Works across TapCode, standalone, and tapmode environments

- **`debug`**: Full deployment workflow
  - Complete compile, package, and deploy to debug server
  - Automatically compile projects (Server-Debug + Client-Debug)
  - Generate reference packages and deployment packages
  - Upload to debug server and make available for testing
  - Takes 3-5 minutes for complete deployment

- **`compile`**: Fast compilation-only workflow
  - Compile SCE project without deployment (80-85% time savings)
  - Verify code correctness quickly
  - Perfect for CI/CD, local development, and code validation
  - Takes 30-60 seconds vs debug tool's 3-5 minutes

- **`check_environment`**: Comprehensive environment status
  - Development environment status checking
  - Authentication and token validation
  - Project binding information
  - MCP workspace roots integration

- **`locate_sce_docs`**: Documentation location and overview
  - Find SCE development documentation directories
  - Get overview of available documentation files
  - Integration with intelligent search functionality

- **`pull_game_log`**: Pull game runtime logs from debug server
  - Retrieve log files from deployed game on debug server
  - Save/append logs locally with automatic file locking
  - Track read status to avoid duplicate log entries
  - Support clearing local logs for fresh starts

- **`publish_to_taptap`**: 🎉 NEW - Publish games to TapTap platform
  - Configuration-based publishing workflow with JSON config files
  - Automatic game creation and update detection
  - Support for game metadata, assets (icons, screenshots, videos)
  - Complete integration with TapTap API
  - Developer identity management and game list retrieval


## 📋 Requirements

- **Node.js**: >= 16.0.0
- **.NET SDK**: >= 6.0 (for SCE project compilation)
- **Operating System**: Windows, macOS, Linux
- **Memory**: Minimum 2GB RAM (4GB+ recommended for documentation search)
- **Storage**: ~50MB for vector caches and documentation indices

## ⚙️ Configuration

### Smart Token Selection Mechanism

SCE Tools automatically selects the appropriate token source based on the environment:

**🏢 TapCode Environment** (`TAPCODE_MODE=true`):
- Primary: `TDS_MCP_MAC_TOKEN` (JSON format)
- Fallback: Environment-specific tokens (`TDS_MCP_MAC_TOKEN_ALPHA`, etc.)
- Use case: Running within TapTap Code development environment

**🏠 Standalone Environment** (default, `TAPCODE_MODE≠true`):
- Primary: `SCE_TAP_TOKEN` environment variable
- Fallback: Token from YAML configuration files
- Use case: Independent development, CI/CD, local testing

### Configuration File Locations

SCE Tools searches for configuration files in priority order:

1. **Environment variables** (highest priority):
   - `TAPCODE_MODE`: Environment mode selector (true/false)
   - `SCE_CONFIG_PATH`: Path to config file
   - `SCE_TOKEN_PATH`: Path to token file
   - `TDS_MCP_MAC_TOKEN`: TapCode environment token (JSON format)
   - `SCE_TAP_TOKEN`: Standalone environment token
   - `TDS_MCP_MAC_TOKEN_ALPHA`, `TDS_MCP_MAC_TOKEN_BETA`, etc.: Environment-specific tokens

2. **User directory** (recommended):
   - `~/.sce/config.yaml`
   - `~/.sce/token.yaml`
   - `~/.sce/sce-config.yaml`
   - `~/.sce/sce-token.yaml`

3. **Project directory**:
   - `./sce-config.yaml`
   - `./sce-token.yaml`

4. **Legacy CLI compatibility**:
   - `~/.tapcode-sce-config.yaml`
   - `~/.tapcode-token.yaml`

### Configuration File Examples

```yaml
# ~/.sce/config.yaml
env: "alpha"  # Environment: master, alpha, beta, pd

# Optional path configuration (usually auto-detected)
# template_path: "/path/to/sce-template-for-ai"
# dotnet_path: "/path/to/dotnet"
# wasi_core_sdk_path: "/path/to/WasiCoreSDK"
# tapcode_helper_url: "custom_url"  # Override default helper URL
```

```yaml
# ~/.sce/token.yaml
alpha: "your_mac_value$your_kid_value"
beta: "beta_mac_value$beta_kid_value"

# Or JSON format:
# alpha: |
#   {
#     "kid": "your_kid_value", 
#     "mac_key": "your_mac_value"
#   }
```

### Environment Variables

```bash
# =====================
# Token Configuration (Choose ONE method)
# =====================

# Method 1: TapCode Environment (when TAPCODE_MODE=true)
export TAPCODE_MODE=true
export TDS_MCP_MAC_TOKEN='{"kid":"your_kid","mac_key":"your_mac_key"}'

# Method 2: Standalone Environment (when TAPCODE_MODE≠true or not set)
export SCE_TAP_TOKEN='your_sce_tap_token'

# Environment-specific tokens (fallback when using TDS_MCP_MAC_TOKEN)
export TDS_MCP_MAC_TOKEN_ALPHA='your_alpha_token'
export TDS_MCP_MAC_TOKEN_BETA='your_beta_token'

# =====================
# Additional Configuration
# =====================

# Enable file logging
export SCE_ENABLE_FILE_LOGGING=1  # Logs to ~/.sce/run.log

# Custom configuration paths
export SCE_CONFIG_PATH='/path/to/custom/config.yaml'
export SCE_TOKEN_PATH='/path/to/custom/token.yaml'

# Custom TapCode client ID (only when TAPCODE_MODE=true)
export TDS_MCP_CLIENT_ID='your_custom_client_id'
```

## 🛠️ Development

### Local Development

```bash
git clone <repository>
cd packages/mcp-sce-server
npm install
npm run build
npm run test
```

### Running Tests

```bash
npm test                 # Run all tests
npm run test:watch      # Watch mode
npm run test:coverage   # Coverage report
```

## 📚 Usage Examples

### Using with AI Assistants

```
// Initialize new SCE project (ABSOLUTE PATH REQUIRED)
Please help me initialize a new SCE game project at C:/Dev/my-new-game

// AI assistant will automatically call create tool
// Creates project structure, applies project ID, generates docs, etc.

// Quick compilation check
Please compile my SCE project at C:/Dev/my-existing-game to check for errors

// AI assistant will call compile tool (fast, 30-60 seconds)
// Only compiles, doesn't deploy

// Full deployment for testing
Please deploy my SCE project at C:/Dev/my-existing-game for debugging

// AI assistant will call debug tool (complete workflow, 3-5 minutes)
// Compiles, packages, uploads to debug server, ready for testing

// Publish game to TapTap platform
Please publish my game at C:/Dev/my-game to TapTap platform using the config at .sce/taptap-publish.json

// AI assistant will call publish_to_taptap tool
// Reads config, creates/updates game on TapTap, uploads assets, returns publish status

// Search SCE documentation
How do I create an Actor in SCE? Please search the documentation.

// AI assistant will call search_docs tool
// Returns relevant API documentation with examples
```

### TapTap Publishing Workflow

```
// Step 1: Create configuration file (AI or manual)
Create a TapTap publish configuration file at C:/Dev/my-game/.sce/taptap-publish.json with:
- Game title: "My Awesome Game"
- Category: "rpg"
- SCE project ID: "p123456"
- Screen orientation: landscape

// AI assistant will create JSON file:
{
  "version": "1.0",
  "game_info": {
    "title": "My Awesome Game",
    "description": "An epic RPG adventure",
    "category": "rpg",
    "sce_project_id": "p123456",
    "screen_orientation": 2
  },
  "assets": {
    "icon": "./assets/icon.png",
    "screenshots": ["./assets/screenshot1.png", "./assets/screenshot2.png"]
  },
  "metadata": {
    "created_at": "2025-01-27T10:00:00.000Z",
    "created_by": "llm"
  }
}

// Step 2: Publish to TapTap
Publish my game at C:/Dev/my-game to TapTap

// AI reads config and calls publish_to_taptap tool
// Result: Game published to TapTap with app_id and TapTap URL

// Step 3: Update and republish
Update the game description to "A legendary RPG adventure" and republish

// AI updates config file and calls publish_to_taptap again
// Tool detects existing app_id and performs update instead of create
```

### Documentation Search

```
// API method search
Please search for "CreateActor" in the SCE documentation

// Natural language search
How do I handle UI button click events in SCE?

// System learning
I want to learn about the physics system in SCE

// AI assistant will use search_docs tool with intelligent hybrid search
// Combines symbol matching, BM25 text search, and vector semantic search
```

### Environment Check

```
Please check my SCE development environment status for project C:/Dev/my-game

// AI assistant will call check_environment tool
// Shows configuration, authentication status, project bindings, workspace roots, etc.
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failed**: 
   - **Check environment mode**: The system uses different tokens based on `TAPCODE_MODE`
   - **TapCode Environment** (`TAPCODE_MODE=true`): Use `TDS_MCP_MAC_TOKEN`
   - **Standalone Environment** (default): Use `SCE_TAP_TOKEN` or config file
   - Verify token format: JSON string `{"kid":"...", "mac_key":"..."}` or simple format
   - Try environment-specific tokens: `TDS_MCP_MAC_TOKEN_ALPHA`, etc.

2. **Compilation Failed**: 
   - Ensure .NET SDK is installed and accessible via `dotnet` command
   - Check WASI Core SDK path configuration
   - Verify project structure (src/GameEntry.csproj file exists)

3. **Path Issues**: 
   - **CRITICAL**: All tools now require absolute paths
   - Use full paths like `C:\Dev\my-project` or `/home/user/my-project`
   - Relative paths like `.` or `./project` are not supported
   - Ensure paths exist and have proper permissions

4. **Documentation Search Issues**:
   - If search is slow on first use, vector cache is being built (one-time, ~25 seconds)
   - Cache is stored in `~/.sce/vector-cache/` and expires after 7 days
   - Search requires sce-openhands-kit documentation in workspace

### Debug Logging

MCP server outputs detailed logging to stderr for diagnostics:

```bash
# Run server directly to view logs
sce-tools-mcp

# Enable file logging (logs to ~/.sce/run.log)
export SCE_ENABLE_FILE_LOGGING=1
sce-tools-mcp

# Check log file
tail -f ~/.sce/run.log
```

### Performance Tips

1. **Documentation Search Performance**:
   - First search builds vector cache (~25 seconds, one-time)
   - Subsequent searches are millisecond-fast
   - Cache automatically refreshes after 7 days

2. **Development Workflow**:
   - Use `compile` tool for quick code validation
   - Use `debug` tool only when you need full deployment
   - Keep workspace paths consistent for better caching

## 🧪 Testing and Development

### Interactive Testing Tools

The project includes powerful testing tools for documentation search:

```bash
cd packages/mcp-sce-server

# Interactive documentation search testing
npm run test:docs

# Performance testing (skip cache)
npm run test:docs:no-cache

# Pure BM25 testing (no vector search)
npm run test:docs:bm25

# Rebuild cache and test
npm run test:docs:rebuild

# Verbose output
npm run test:docs --verbose
```

### Local Development

```bash
git clone <repository>
cd packages/mcp-sce-server
npm install
npm run build
npm run test
```

### Running Tests

```bash
npm test                 # Run all tests
npm run test:watch      # Watch mode
npm run test:coverage   # Coverage report
```

## 📊 Performance Metrics

### Documentation Search Performance
- **Document Processing**: ~8,000 document chunks from 120+ files
- **Symbol Extraction**: 6,500+ API symbols
- **Search Response**: 3-68ms (with cache)
- **Cache Build Time**: 5-7 seconds (one-time)
- **Vector Cache Size**: ~50MB
- **Cache Persistence**: 7 days auto-expiration

### System Performance
- **Compilation Time**: 30-60 seconds (compile tool)
- **Full Deployment**: 3-5 minutes (debug tool)
- **Environment Check**: < 1 second
- **Documentation Location**: < 1 second

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Development Guidelines
1. All new tools must enforce absolute paths
2. Add comprehensive error handling and user-friendly messages
3. Include both unit tests and integration tests
4. Update documentation and examples
5. Follow TypeScript best practices

## 📄 License

MIT License

## 🔗 Related Links

- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [TapTap Code Development Documentation](https://developers.taptap.cn/)
- [SCE Development Guide](./docs/)
- [Project Documentation](../../docs/) - Comprehensive development guides and architecture docs
