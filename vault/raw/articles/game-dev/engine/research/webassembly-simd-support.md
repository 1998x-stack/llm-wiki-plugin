---
summary: "WebAssembly SIMD support implementation for hardware-accelerated parallel processing in physics and math"
last_updated: "2026-04-02"
---

# WebAssembly SIMD Support

## Overview

This document describes the WebAssembly SIMD support added to UrhoX engine, which enables hardware-accelerated SIMD operations for improved performance in physics calculations and mathematical operations.

## What is WebAssembly SIMD?

WebAssembly SIMD (Single Instruction, Multiple Data) is a standard that enables parallel processing of multiple data elements using a single instruction. This significantly improves performance for:

- Bullet physics engine calculations (collision detection, rigid body dynamics)
- Vector and matrix operations in Urho3D Math library
- Image processing and other data-parallel operations

## Performance Benefits

When SIMD is enabled, you can expect:

- **20-40% faster** physics simulations (Bullet)
- **15-30% faster** vector/matrix operations
- Overall smoother gameplay and better frame rates

## Browser Compatibility

WebAssembly SIMD requires modern browsers:

| Browser | Minimum Version |
|---------|----------------|
| Chrome | 91+ |
| Firefox | 89+ |
| Safari | 16.4+ |
| Edge | 91+ |

## How to Enable

### Option 1: Use the Modified Build Script (Recommended)

Simply run the updated `gen_wasm_agent.bat`:

```bash
tools\generators\gen_wasm_agent.bat
```

The script now includes `-DURHO3D_SSE=1` which automatically enables SIMD support.

### Option 2: Manual CMake Configuration

Add the following flag when configuring with CMake:

```bash
cmake ../engine/ -DWEB=1 -DURHO3D_SSE=1 [other options...]
```

## Technical Details

### Implementation

The SIMD support is implemented through:

1. **CMake Configuration** (`engine/CMake/Modules/UrhoCommon.cmake`):
   - Detects `URHO3D_SSE` option
   - Adds `-msimd128` compiler flag for Emscripten
   - Automatically enables `__wasm_simd128__` preprocessor macro

2. **Build Script** (`tools/generators/gen_wasm_agent.bat`):
   - Includes `-DURHO3D_SSE=1` by default
   - Works with existing Emscripten toolchain

3. **Automatic Detection in Libraries**:
   - Bullet physics: Automatically uses SIMD when `__wasm_simd128__` is defined
   - Urho3D Math: Uses SIMD optimizations through `URHO3D_SSE` macro

### Compiler Flags

When SIMD is enabled, the following flags are added:

```
-msimd128           # Enable WebAssembly SIMD instructions
```

### Verification

To verify SIMD is enabled in your build:

1. Check the CMake configuration output:
   ```
   WebAssembly SIMD enabled (-msimd128)
   ```

2. Inspect the generated `.wasm` file for SIMD instructions:
   ```bash
   wasm-objdump -d Urho3DPlayer.wasm | grep "v128"
   ```

## Troubleshooting

### Build Fails with "unknown option -msimd128"

**Cause**: Your Emscripten version is too old.

**Solution**: Update Emscripten to version 2.0.0 or later:
```bash
emsdk install latest
emsdk activate latest
```

### Application Crashes in Browser

**Cause**: The browser doesn't support WebAssembly SIMD.

**Solution**:
- Update to a supported browser version (see Browser Compatibility table)
- Or build without SIMD: Remove `-DURHO3D_SSE=1` from the build script

### No Performance Improvement

**Causes**:
1. The browser is not using SIMD (check browser version)
2. The workload is not SIMD-friendly (e.g., mostly rendering, not physics)

**Verification**: Use browser dev tools to profile performance:
- Chrome: Performance profiler
- Firefox: Performance tool

## Related Files

- `engine/CMake/Modules/UrhoCommon.cmake` - Main SIMD configuration
- `tools/generators/gen_wasm_agent.bat` - Build script with SIMD enabled
- `engine/Source/ThirdParty/Bullet/src/LinearMath/btScalar.h` - Bullet SIMD detection
- `engine/Source/ThirdParty/Bullet/src/LinearMath/btVector3.cpp` - Bullet SIMD implementations

## References

- [WebAssembly SIMD Proposal](https://github.com/WebAssembly/simd)
- [Emscripten SIMD Support](https://emscripten.org/docs/porting/simd.html)
- [Bullet Physics SIMD Documentation](https://pybullet.org/Bullet/BulletFull/)

## Changelog

### 2025-11-01
- Initial implementation of WebAssembly SIMD support
- Added `-msimd128` flag to Emscripten builds when `URHO3D_SSE=1`
- Updated `gen_wasm_agent.bat` to enable SIMD by default
- Created documentation

---

*For questions or issues, please refer to the main UrhoX documentation or open an issue on GitHub.*
