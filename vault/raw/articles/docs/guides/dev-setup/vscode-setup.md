# Visual Studio Code Setup Guide

This guide helps you configure VS Code for UrhoX engine development.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- CMake 3.10+
- Clang/Clang++ (Linux) or MSVC (Windows)
- Python 3.x (for build scripts)

## Recommended Extensions

Install these extensions for the best development experience:

```bash
# Core C++ Development
code --install-extension ms-vscode.cpptools
code --install-extension ms-vscode.cmake-tools
code --install-extension llvm-vs-code-extensions.vscode-clangd

# Debugging
code --install-extension vadimcn.vscode-lldb  # Linux/macOS
code --install-extension ms-vscode.cpptools   # Windows

# Optional but useful
code --install-extension stkb.rewrap          # Comment formatting
code --install-extension eamodio.gitlens      # Git integration
```

## Linux Agent Development Configuration

### Quick Setup

Create a workspace file for Linux Agent development:

```bash
# From project root
cat > UrhoX-linux.code-workspace << 'EOF'
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "cmake.configureOnOpen": true,
    "cmake.sourceDirectory": "${workspaceFolder}/engine",
    "cmake.buildDirectory": "${workspaceFolder}/build_linux_agent",
    "cmake.preferredGenerators": [
      "Unix Makefiles"
    ],
    "cmake.configureArgs": [
      "-DURHO3D_SERVER=1",
      "-DURHO3D_BGFX_SHADERC_STATIC=0",
      "-DURHO3D_BGFX_SHADERC_ENABLE=0",
      "-DURHO3D_ANGELSCRIPT=0",
      "-DURHO3D_IK=0",
      "-DURHO3D_PHYSICS=1",
      "-DURHO3D_NAVIGATION=0",
      "-DURHO3D_PLAYER=1",
      "-DURHO3D_BGFX=1",
      "-DBGFX_VIEW_DEBUG=0",
      "-DURHO3D_LIB_TYPE=STATIC",
      "-DURHO3D_BGFX_RENDERER_NOOP=1",
      "-DURHO3D_FREETYPE=0",
      "-DURHO3D_HARFBUZZ=0",
      "-DURHO3D_WEBP=0",
      "-DURHO3D_USD_MANAGER=0",
      "-DUSE_MALLOC_PROFILER=0",
      "-DUSE_MIMALLOC=0",
      "-DURHO3D_PCH=0",
      "-DVIDEO_WAYLAND=OFF",
      "-DURHO3D_LUA=1",
      "-DBINARY_VERSION=9999999",
      "-DURHO3D_AGENT=1",
      "-DCMAKE_C_COMPILER=clang",
      "-DCMAKE_CXX_COMPILER=clang++"
    ],
    "clangd.arguments": [
      "--compile-commands-dir=${workspaceFolder}/build_linux_agent"
    ]
  },
  "tasks": {
    "version": "2.0.0",
    "tasks": [
      {
        "label": "Build Urho3DPlayer",
        "type": "shell",
        "command": "cmake",
        "args": [
          "--build",
          "${workspaceFolder}/build_linux_agent",
          "--target",
          "Urho3DPlayer",
          "-j8"
        ],
        "options": {
          "cwd": "${workspaceFolder}"
        },
        "group": {
          "kind": "build",
          "isDefault": true
        },
        "problemMatcher": []
      },
      {
        "label": "Run Urho3DPlayer",
        "type": "shell",
        "command": "${workspaceFolder}/build_linux_agent/bin/Urho3DPlayer",
        "args": [
          "aaaa.lua"
        ],
        "dependsOn": "Build Urho3DPlayer",
        "presentation": {
          "focus": true,
          "panel": "dedicated"
        }
      }
    ]
  },
  "launch": {
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Debug Urho3DPlayer (codelldb)",
        "type": "lldb",
        "request": "launch",
        "program": "${workspaceFolder}/build_linux_agent/bin/Urho3DPlayer",
        "args": [
          "Scripts/Test1.lua"
        ],
        "cwd": "${workspaceFolder}",
        "preLaunchTask": "Build Urho3DPlayer",
        "terminal": "integrated"
      }
    ]
  }
}
EOF

# Open the workspace
code UrhoX-linux.code-workspace
```

### Configuration Explanation

**CMake Settings:**
- `URHO3D_SERVER=1` - Enable server mode (headless, no rendering)
- `URHO3D_AGENT=1` - Enable agent-specific features
- `URHO3D_LUA=1` - Enable Lua scripting support
- `URHO3D_BGFX_RENDERER_NOOP=1` - Use no-op renderer for server builds
- `CMAKE_C_COMPILER=clang` - Use Clang compiler for better diagnostics

**Build Tasks:**
- `Ctrl+Shift+B` - Build Urho3DPlayer (default task)
- Manual run via Command Palette: "Tasks: Run Task" → "Run Urho3DPlayer"

**Debug Configuration:**
- `F5` - Start debugging with CodeLLDB
- Automatically builds before launching
- Default script: `Scripts/Test1.lua`

## Windows Development Configuration

For Windows development with MSVC:

```bash
cat > UrhoX-windows.code-workspace << 'EOF'
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "cmake.configureOnOpen": true,
    "cmake.sourceDirectory": "${workspaceFolder}/engine",
    "cmake.buildDirectory": "${workspaceFolder}/build_windows",
    "cmake.preferredGenerators": [
      "Visual Studio 17 2022"
    ],
    "cmake.configureArgs": [
      "-DURHO3D_PLAYER=1",
      "-DURHO3D_LUA=1",
      "-DURHO3D_BGFX=1"
    ]
  }
}
EOF
```

> **Note:** Windows developers may prefer using Visual Studio IDE directly.

## IntelliSense Configuration

### Using clangd (Recommended)

1. Install the `clangd` extension
2. Disable the default C++ extension IntelliSense:
   ```json
   "C_Cpp.intelliSenseEngine": "Disabled"
   ```
3. Ensure `compile_commands.json` is generated in your build directory

### Using Microsoft C/C++ Extension

If you prefer the default extension:
1. Ensure CMake Tools extension is installed
2. It will automatically detect CMake project settings
3. No additional configuration needed

## Common Tasks

### Initial Build

```bash
# Configure CMake
cmake -B build_linux_agent -S engine -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++

# Build
cmake --build build_linux_agent --target Urho3DPlayer -j8
```

### Running Tests

```bash
cd build_linux_agent
ctest --output-on-failure
```

### Cleaning Build

```bash
rm -rf build_linux_agent
# Then reconfigure from VS Code (CMake will auto-configure)
```

## Troubleshooting

### IntelliSense not working

1. Check that `compile_commands.json` exists in your build directory:
   ```bash
   ls build_linux_agent/compile_commands.json
   ```

2. Verify clangd is using the correct database:
   - Open Command Palette (`Ctrl+Shift+P`)
   - Run "clangd: Restart language server"

### Build task fails

1. Ensure CMake configured successfully:
   ```bash
   cmake -B build_linux_agent -S engine
   ```

2. Check compiler availability:
   ```bash
   clang --version
   clang++ --version
   ```

### Debugging doesn't start

1. Install CodeLLDB extension:
   ```bash
   code --install-extension vadimcn.vscode-lldb
   ```

2. Verify the executable exists:
   ```bash
   ls build_linux_agent/bin/Urho3DPlayer
   ```

## Additional Resources

- [CMake Tools Documentation](https://github.com/microsoft/vscode-cmake-tools/blob/main/docs/README.md)
- [clangd User Manual](https://clangd.llvm.org/)
- [CodeLLDB Manual](https://github.com/vadimcn/vscode-lldb/blob/master/MANUAL.md)
- [UrhoX Development Gotchas](../../gotchas/development-gotchas.md)

## Notes

- The `.code-workspace` file is excluded from git (see `.gitignore`)
- Feel free to customize the configuration for your workflow
- For multi-platform development, create separate workspace files (e.g., `UrhoX-linux.code-workspace`, `UrhoX-windows.code-workspace`)
